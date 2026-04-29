# WriteOnce Walking Skeleton 实现设计

- 状态: 已批准（design-review 2026-04-29 通过）
- 主题: Markdown → Medium 端到端的 walking-skeleton 实现 + PlatformAdapter 抽象层
- 节点: `hf-design`
- 上游: `features/001-walking-skeleton/spec.md`（已批准）

## 1. 概述

WriteOnce v0 由四层组成：

```
CLI  (cli.ts)
  └─> PublishService  (publish/publish-service.ts)
        └─> PlatformAdapter (platform/platform-adapter.ts) — Map<string, PlatformAdapter>
              ├─> MediumAdapter  (platform/medium-adapter.ts)  ← walking skeleton 实现
              ├─> ZhihuAdapter   (platform/zhihu-adapter.ts)   ← 仅声明扩展点（notImplemented = true）
              └─> WeChatMpAdapter (platform/wechat-mp-adapter.ts) ← 仅声明扩展点
        └─> MarkdownParser (parser/markdown-parser.ts) — 把 .md 解析成 Post
HttpClient (platform/http-client.ts)  — 通过构造注入 MediumAdapter；walking-skeleton 测试用 RecordingHttpClient
```

walking-skeleton 实现真正端到端覆盖的路径：CLI → PublishService → MarkdownParser → MediumAdapter → RecordingHttpClient。

## 2. 设计驱动因素

| 驱动 | 来源 |
|---|---|
| FR-1 / FR-3 / FR-4：CLI 端到端 + adapter 抽象 + dry-run | spec.md section 8 |
| FR-2 / FR-6：未实现平台必须显式失败、不静默 | spec.md section 8 |
| NFR-Reliability-1：所有失败路径返回结构化对象 | spec.md section 9 |
| NFR-Maintainability-1：加平台 = 加文件 + 一行注册 | spec.md section 9 |
| NFR-Testability-1：e2e 离线 + < 1 s | spec.md section 9 |
| 约束：禁止真实网络 | spec.md section 11 |
| 约束：TypeScript strict + 文件 kebab-case | spec.md section 11 |

## 3. 需求覆盖与追溯

| FR / NFR | 设计承接 |
|---|---|
| FR-1 | `PublishService.publish(file, opts)` → `MarkdownParser.parse` → `MediumAdapter.publish` → `HttpClient.request` |
| FR-2 | `PublishService` 在查找 adapter 时分两种失败：`unknown platform` / `not implemented in v0`；CLI 把结构化错误翻译成非零退出码 |
| FR-3 | `PlatformAdapter` interface + `adapters: Map<string, PlatformAdapter>`，只在 `publish-service.ts` 顶部注册一次（ADR-0002）|
| FR-4 | `PublishService.publish` 支持 `dryRun` 选项，传给 adapter；adapter 在 dryRun 时返回 payload 而不调用 HttpClient（用 spy 验证）|
| FR-5 | 所有 service 边界返回 `PublishResult = { ok: true, payload } \| { ok: false, code, message }`；CLI 处理 union |
| FR-6 | `--to all` 在 PublishService 内对 `adapters` Map 全 entries 串行执行，每个 entry 独立返回结果，结果汇总返回数组；任何一个失败不阻塞其它 |
| NFR-Reliability-1 | `PublishService.publish` 包一层 try/catch 把任何抛出转成 `{ ok:false, code:'INTERNAL', message }`；adapter 自身也包同样的边界 |
| NFR-Maintainability-1 | 见 FR-3；ADR-0002 |
| NFR-Testability-1 | `MediumAdapter` 通过构造注入 `HttpClient`；测试用 `RecordingHttpClient` 收集 request 调用，不开 socket（ADR-0003）|

## 4. Domain Strategic Model (Bounded Context / Ubiquitous Language / Context Map)

WriteOnce v0 walking-skeleton **不做** DDD 战略建模。理由：

- 系统只有 1 个 Bounded Context（"把一篇 Post 发到一个 Platform"），不存在跨 Context 关系。
- spec section 14 术语表只 5 条，Ubiquitous Language 不需要扩展。
- 没有跨系统集成需要 Context Map。

显式跳过此节，符合 design-doc-template "本轮不做战略建模时显式写明理由" 的要求。

## 4.5 Tactical Model per Bounded Context

WriteOnce v0 walking-skeleton **不做** DDD 战术建模。触发条件检查：

- Bounded Context 数量 ≥ 2 → ❌ 仅 1 个
- 单 Context 内多实体 + 跨实体一致性约束 → ❌ Post 是 VO（无身份），Platform 是无状态适配器
- 并发修改 / 事务边界 / 领域事件 / 跨聚合不变量 → ❌ 单进程 + 无状态 + 无事务

任一触发条件都不满足，按模板要求显式跳过。

GoF 代码模式（Strategy / Adapter）**不**写入本节——它们留给 `hf-test-driven-dev` 的 REFACTOR 步按 Fowler 重构词汇浮现处理。

## 5. Event Storming Snapshot

Profile = `lightweight`，按模板用纯自然语言描述：

> CLI 接收 `publish <file> --to <platform>` 命令 → PublishService 触发 `MarkdownReadRequested`（隐式）→ MarkdownParser 产出 `Post` → PublishService 查找 adapter，触发 `PlatformResolved` 或 `PlatformResolutionFailed`（隐式）→ MediumAdapter 触发 `PublishAttempted`（隐式）→ HttpClient 完成请求（或在 dryRun 时短路）→ adapter 返回 `PublishResult` → PublishService 汇总 → CLI 翻译成 stdout / 退出码。
>
> 异常路径：文件不存在 → `FileReadFailed`；解析失败 → `ParseFailed`；adapter 不存在 / 未实现 → 上述两种；HTTP 失败 → `RequestFailed`。所有 \*Failed 事件最终都被翻译成 `{ ok: false, code, message }`。

## 6. 架构模式选择

- **Adapter pattern**（GoF）：在实现层 emergent 浮现；本设计不预先指定 Adapter 类层次结构。`PlatformAdapter` interface 是 SDD 层面的"端口/适配器"边界（Hexagonal 风味），**不**等价于 GoF Adapter 模式的实现。
- **Front Controller**（PoEAA）：CLI 是单点入口，`commander` 的 `publish` 子命令承担 controller 角色。
- **Strategy pattern**（GoF）：可能在 `--to all` 的 dispatcher 实现中浮现，但同样是实现层产物，不在本设计中预设。

## 7. 候选方案总览

参见 ADR-0002 候选方案 X / Y / Z；ADR-0003 候选方案 P / Q / R。

## 8. 候选方案对比与 trade-offs

### Adapter 边界（详见 ADR-0002）

| 方案 | 核心思路 | 优点 | 主要代价 / 风险 | NFR / 约束适配 (对 QAS) | 对 Success Metrics 的影响 | 可逆性 |
|---|---|---|---|---|---|---|
| X (选定) | `PlatformAdapter` interface + Map 注册 | 加平台 = 加文件 + 一行注册；publish-service 不知道平台名 | Map 是中央化点；接口 Hyrum 风险 | NFR-Maintainability-1 ✅；NFR-Testability-1 ✅ | 直接支撑 Threshold (a) 16 节点工件齐全 + (d) 端到端运行 | 中 |
| Y | `publish-service.ts` 内 if-else 分发 | 实现最简 | 加平台要改 publish-service；违反 FR-3 / NFR-Maintainability-1 | NFR-Maintainability-1 ❌ | 直接破坏 Threshold (a) 中"adapter 抽象层"诚实度 | 高 |
| Z | 插件机制（动态加载 npm 模块） | 运行时可扩展 | 需引入插件加载器；超出 walking skeleton 范围 | NFR-Testability-1 ❌（增加测试面）；NFR-Maintainability-1 OK | 引入复杂度，拖慢 Threshold (b) RED/GREEN evidence 节奏 | 低 |

### HTTP 层（详见 ADR-0003）

| 方案 | 核心思路 | 优点 | 主要代价 / 风险 | NFR / 约束适配 | Success Metrics 影响 | 可逆性 |
|---|---|---|---|---|---|---|
| P (选定) | `HttpClient` interface 注入 + `RecordingHttpClient` 测试替身 | 离线 + 真实形态 | 多写一个接口 + 一个 RecordingHttpClient | NFR-Testability-1 ✅；spec.section 11 ✅ | Threshold (b)(c) RED/GREEN + 100% 测试通过都依赖此 | 高 |
| Q | `nock` 拦截 fetch | 不改 adapter 形态 | 引入 nock 大依赖；walking skeleton 复杂度过剩 | NFR-Testability-1 ✅；额外依赖与 spec section 10 "不引入 HTTP 库" 精神不符 | 多一份依赖管理负担 | 中 |
| R | 完全不写网络层 | 实现最快 | adapter 失去说服力，违反 HYP-F-2 | NFR-Testability-1 OK；HYP-F-2 ❌ | demo 失去 design 可读性 | 高 |

## 9. 选定方案与关键决策

- adapter 边界 = **方案 X**（ADR-0002）
- HTTP 层 = **方案 P**（ADR-0003）
- CLI = `commander` 单文件 `cli.ts`（无候选；spec section 10 已声明）
- Markdown parser = 极简手写，覆盖 spec section 6 列出的 CommonMark 子集，**不**引入大依赖

## 10. 架构视图

### C4 Context（文字版）

```
[Author (CLI user)]
    │ 输入：post.md + --to <platform> [--dry-run]
    ▼
[WriteOnce CLI System]
    │ 调用：HTTP POST (stub in walking skeleton)
    ▼
[Medium API]   [Zhihu]   [WeChat MP]
   ✅ 接通      ⏸ 扩展点  ⏸ 扩展点
```

### C4 Container（文字版）

WriteOnce CLI System 内部容器：

```
+--------------------+      +-----------------------+
|  CLI               | ───▶ |  Publish Service      |
|  (commander)       |      |                       |
+--------------------+      +-----------+-----------+
                                        │
                          +-------------+-------------+
                          ▼                           ▼
                +-----------------+         +-------------------+
                | Markdown Parser |         | Platform Adapter  |
                |                 |         | Registry (Map)    |
                +-----------------+         +---------+---------+
                                                      │
                                +---------------------+---------------------+
                                ▼                     ▼                     ▼
                       +----------------+   +----------------+   +-------------------+
                       | Medium Adapter |   | Zhihu Adapter  |   | WeChat MP Adapter |
                       | (impl)         |   | (notImpl=true) |   | (notImpl=true)    |
                       +-------+--------+   +----------------+   +-------------------+
                               │
                               ▼
                       +----------------+
                       | HttpClient     |
                       | (interface)    |
                       +----------------+
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
         Node20FetchHttpClient     RecordingHttpClient
         (production, unused       (tests / dry-run)
          in walking skeleton)
```

## 11. 模块职责与边界

| 模块 | 职责 | 不做的事 |
|---|---|---|
| `cli.ts` | 解析 CLI flags；翻译结构化结果到 stdout/stderr/exit code | 任何 publish 业务逻辑 |
| `publish/publish-service.ts` | 编排 parser → adapter；处理 `--to all` 与单平台分发；包 try/catch 把异常转结构化错误 | 任何具体平台知识；任何 HTTP 调用 |
| `parser/markdown-parser.ts` | 把 `.md` 文本解析为 `Post = { title, body, codeBlocks, images }` | 任何 platform-specific 转换 |
| `platform/platform-adapter.ts` | 定义 `PlatformAdapter` interface + `PublishResult` union 类型 | 任何具体实现 |
| `platform/medium-adapter.ts` | 把 `Post` 转 Medium API payload；调用 `HttpClient.request` | 业务编排 |
| `platform/zhihu-adapter.ts` | 实现 `PlatformAdapter` interface，但 `publish` 直接返回 `{ ok:false, code:'NOT_IMPLEMENTED', message:'platform "zhihu" is declared but not implemented in v0' }` | 任何真实集成 |
| `platform/wechat-mp-adapter.ts` | 同上 | 同上 |
| `platform/http-client.ts` | 定义 `HttpClient` interface；提供 `Node20FetchHttpClient` 与 `RecordingHttpClient` | 任何 platform-specific 知识 |

## 12. 数据流、控制流与关键交互

```
+-------+      +-----------+      +---------+      +--------+      +---------+      +-------------+
| CLI   | ───▶ | Publish   | ───▶ | Parser  | ───▶ | Adapter| ───▶ | HttpClient | ───▶ | exit code |
| flags |      | Service   |      |         |      | (Map)  |      |            |      |             |
+-------+      +-----------+      +---------+      +--------+      +-------------+      +-------------+
                    │                                  │                  │
                    │ 错误 / 未知平台                  │                  │ 错误
                    └────────► PublishResult { ok:false, code, message } ◄┘
```

`--to all` 时控制流：PublishService 遍历 `adapters.entries()` 串行执行，每个 entry 独立产生 PublishResult，最终汇总成 `PublishResult[]` 返回 CLI；CLI 退出码：全部 `ok:true` → 0；任何一个 `ok:false` → 非零（编码：`1`）。

## 13. 接口、契约与关键不变量

参见 `contracts/platform-adapter.contract.md`（草稿契约，本 feature 内）。

关键不变量：
- `PublishService.publish` 永不抛出（`Promise.reject` 也算抛出）；任何运行时错误都翻成 `PublishResult`。
- `PlatformAdapter.publish` 同上不变量。
- `PlatformAdapter.notImplemented === true` 时，`publish` 必须返回 code `NOT_IMPLEMENTED`，**不**得真实尝试发布。

## 14. 非功能需求与 QAS 承接

| NFR ID (来自 spec) | 设计承接模块 | 机制 | 可观测 | 验证方式 |
|---|---|---|---|---|
| NFR-Reliability-1 | `PublishService` + 每个 adapter | 边界 try/catch + 结构化 PublishResult union | stderr 上 `error code=...` | 单元测试覆盖每个失败路径；e2e 测试覆盖整链 |
| NFR-Maintainability-1 | `PlatformAdapter` interface + 注册 Map | adapter 文件 + 注册行为唯一中央化点 | `git diff` | 加一个 fake adapter 测试，diff 检查 |
| NFR-Testability-1 | `HttpClient` interface + `RecordingHttpClient` | 构造注入；e2e 测试用 RecordingHttpClient | 测试运行时间 + 0 socket 调用 | vitest 计时；用 `RecordingHttpClient` 的 `requests` 数组验证 |

## 15. Threat Model (STRIDE 轻量版)

触发条件检查：

- Spec 有 Security NFR → ❌ 无
- 跨信任边界数据流 → ❌ walking skeleton 不真集成；HTTP 走 RecordingHttpClient
- 处理认证 / 授权 / 敏感数据 → ❌ 无 token；spec section 11 显式禁止
- 审计 / 合规要求 → ❌ 无

不触发，按模板可省略。但为了 demo 完整性，给 1 条预防性条目：

| 资产 / 数据流 | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| 未来真实 Medium token (v0 不存在) | N/A | N/A | N/A | 未来需走 secret manager | N/A | 未来需角色限制 |

含义：**v0 walking skeleton 不引入 token**。任何未来真实集成必须在那一时点重新做 STRIDE 评估，本设计不替未来的真集成做提前担保。

## 16. 测试与验证策略

最薄验证路径：

- **e2e（walking skeleton 验证）**：1 条端到端测试 `walking-skeleton.test.ts`：
  1. 写一个 fixture `post.md` 到临时目录；
  2. 用 `RecordingHttpClient` 注入 `MediumAdapter`；
  3. 通过 `PublishService.publish(file, { to: 'medium' })` 触发；
  4. 断言：返回 `{ ok: true }`；`RecordingHttpClient.requests` 含 1 条；payload 含 title 与 fenced code block 内容。
- **unit**：`MarkdownParser`、`PublishService`、每个 adapter（含 `ZhihuAdapter` / `WeChatMpAdapter` 的 NOT_IMPLEMENTED 路径）。
- **fuzz / property**：v0 不做。

CI 触发：`npm test`。Profile = lightweight，覆盖率不设硬阈值，但要求所有 FR Acceptance 都至少有 1 条测试覆盖（traceability-review 节点会校验）。

## 17. 失败模式与韧性策略

| 失败模式 | 检测 | 韧性策略 |
|---|---|---|
| 输入文件不存在 | `fs.access` 抛错 | PublishService 包 try/catch 转 `code: 'FILE_NOT_FOUND'` |
| Markdown parse 失败 | parser 抛错 | 同上转 `code: 'PARSE_FAILED'` |
| 未知平台 | `adapters.get(name)` 返回 undefined | 返回 `code: 'UNKNOWN_PLATFORM'` |
| 平台未实现 (Zhihu / WeChat MP) | adapter 返回 `code: 'NOT_IMPLEMENTED'` | 透传 |
| HttpClient 抛错（未来真实集成场景） | adapter 包 try/catch | 转 `code: 'HTTP_FAILED'` |
| `--to all` 中部分失败 | PublishService 遍历独立处理 | 不阻塞其它 adapter 执行；CLI 汇总后退出码非零 |

## 18. 任务规划准备度

可拆解维度：
- (T1) walking-skeleton 端到端：从 fixture post.md 到 `RecordingHttpClient` 收到 1 个请求，e2e 测试绿。**这是 v0 的唯一 Current Active Task**。
- (T2) ZhihuAdapter / WeChatMpAdapter 的 NOT_IMPLEMENTED 单元测试。
- (T3) `--to all` 串行 dispatcher。
- (T4) CLI flag 解析与 stderr / exit code 翻译。

`hf-tasks` 节点会在此基础上做 INVEST + 依赖排序。

## 19. 关键决策记录（ADR 摘要）

- `examples/writeonce/docs/adr/0001-record-architecture-decisions.md` — 启用 ADR
- `examples/writeonce/docs/adr/0002-platform-adapter-as-extension-boundary.md` — 选定 adapter Map 方案
- `examples/writeonce/docs/adr/0003-no-real-network-in-walking-skeleton.md` — 选定 HttpClient 注入方案

## 20. 明确排除与延后项

- 真实 Medium 集成（含 OAuth / token / 速率限制）—— v0.x
- Zhihu / WeChat MP 真实集成 —— v0.x
- 内容编辑 / Notion 源 / 多文件源 —— v0.x
- GUI / Electron —— 不规划
- CI/CD 部署 —— 与 ADR-001 D1 P-Honest 一致，HF v0.1.0 demo 不假装有

## 21. 风险与开放问题

- 无阻塞项。
- 非阻塞：`PlatformAdapter.notImplemented = true` 是 v0 的"诚实占位符"，`hf-code-review` 在审 ZhihuAdapter / WeChatMpAdapter 时会 cross-check 此约定是否被滥用为"以后慢慢补"。

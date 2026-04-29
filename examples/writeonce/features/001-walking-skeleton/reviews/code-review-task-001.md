# Code Review — Task-001 (Walking-skeleton e2e)

- 节点: `hf-code-review`
- Reviewer Role: Independent Reviewer
- Date: 2026-04-29
- Task: T1 — Walking-skeleton end-to-end
- Source Files Reviewed:
  - `src/platform/platform-adapter.ts`
  - `src/platform/http-client.ts`
  - `src/platform/medium-adapter.ts`
  - `src/platform/zhihu-adapter.ts`
  - `src/platform/wechat-mp-adapter.ts`
  - `src/parser/markdown-parser.ts`
  - `src/publish/publish-service.ts`
- Test Verdict (上游): `通过`（见 `test-review-task-001.md`）

## Verdict

`通过`

## Five-Axis Review

### 1. Correctness

| 关切 | 结论 | 证据 |
|---|---|---|
| 行为符合 spec FR-1..FR-5 | ✅ | 23/23 测试通过；GREEN log；FR Acceptance 全部覆盖（见 traceability-review）|
| 失败路径 100% 走结构化 PublishResult | ✅ | `publish-service.ts` 与 `medium-adapter.ts` 都包 try/catch；publish-service.test.ts 第 3 条 `never throws` 覆盖 |
| `notImplemented = true` 的 adapter 不会"偷偷"做事 | ✅ | `zhihu-adapter.ts` / `wechat-mp-adapter.ts` 仅返回 NOT_IMPLEMENTED，无任何 I/O |
| dryRun 不发起 HTTP | ✅ | `medium-adapter.ts` 第 1 个分支即返回 ok+payload；medium-adapter.test.ts dryRun 测试覆盖 |

### 2. Design Conformance

| 设计声明 | 代码落点 | 一致性 |
|---|---|---|
| ADR-0002 PlatformAdapter Map 注册 | `publish-service.ts` 构造函数：`new Map(deps.adapters.map((a) => [a.name, a]))` | ✅ 一致；`publish-service.ts` 不感知具体平台名 |
| ADR-0003 HttpClient 注入 | `medium-adapter.ts` 构造函数 + RecordingHttpClient 测试替身 | ✅ 一致 |
| design section 11 模块职责 | `cli.ts`（未在 v0 实现，T4 deferred）；其它模块职责与设计表一致 | ✅ 一致 |
| design section 13 不变量"publish 永不抛出" | publish-service & medium-adapter 都 wrap try/catch；publish-service.test.ts `never throws` 测试覆盖 | ✅ 一致 |
| contract.md error code 词表 | `platform-adapter.ts` 中 `PublishErrorCode` union 与 contract.md 完全一致 | ✅ 一致 |

### 3. Defense-in-Depth

| 关切 | 结论 | 备注 |
|---|---|---|
| 输入校验 | ✅ | `markdown-parser.ts` 缺 H1 直接抛错；publish-service 包成 PARSE_FAILED |
| 边界异常处理 | ✅ | 所有外部边界（`fs.readFile` / `parser.parse` / `adapter.publish`）都有显式 try/catch |
| 资源清理 | N/A | 无文件句柄 / socket / timer 资源 |
| 信任边界 | ✅ | 唯一外部 I/O 是 `HttpClient`，由构造注入；adapter 不直接调 `fetch` |

### 4. Clean Architecture Conformance

| 检查 | 结论 | 备注 |
|---|---|---|
| 业务核心（PublishService、Parser）不依赖具体框架 | ✅ | 无 framework dependency；只依赖 Node 内置 `fs/promises` |
| 平台适配（adapters）通过 interface 倒置依赖 | ✅ | `PlatformAdapter` interface 在领域层；具体 adapter 实现它 |
| 配置（adapter 注册）通过依赖注入而非全局 import | ✅ | `PublishService` 构造时接收 `adapters: readonly PlatformAdapter[]` |
| 是否存在 SOLID 违反 | ✅ 否 | OCP：加平台不动 publish-service；LSP：所有 adapter 可互换；ISP：HttpClient interface 只 1 个方法 |

### 5. Two Hats / Refactoring Hygiene

| 关切 | 结论 | 备注 |
|---|---|---|
| 是否在同一 commit 中混合行为变更 + 重构 | ⚠️ Walking-skeleton 一次性写出所有源文件——demo 受 Walking Skeleton 纪律允许（首切片不区分 add behavior vs refactor）|
| GoF 模式是否被前置写在设计中而非 emergent 浮现 | ✅ 否 | design section 6 显式说"emergent"；代码中 Adapter 形态属 SDD-port-and-adapter，不是 GoF Adapter 类层次 |
| Refactor Note | demo 无单独 Refactor 步——首次切片即"绿条" + 一次微调（medium-adapter.composeMarkdown 修复"代码块内容缺失"），微调本身有测试覆盖 |

## Architectural Smells Detection

| Smell | 是否触发 | 备注 |
|---|---|---|
| God object | 否 | `PublishService` 仅承担"编排"，单一职责 |
| Feature envy | 否 | adapter 不读 PublishService 内部状态 |
| Shotgun surgery | ✅ 否 | 加平台 = 加 1 文件 + 1 行注册；publish-service.test.ts 已用 fakeAdapter 证明 |
| Primitive obsession | ⚠️ 轻 | `PublishCallOptions.to` 是 `string`，不是 branded type；demo 规模可接受 |
| Switch on type | 否 | 所有平台分发走 Map.get，无 if-else |
| Premature abstraction | 否 | `HttpClient` interface 是 spec NFR-Testability-1 + ADR-0003 的硬约束，不是预言性抽象 |

## Specific Findings

### Strengths

1. **诚实的 stub**：`zhihu-adapter.ts` / `wechat-mp-adapter.ts` 把 "未实现" 写得非常显眼（class doc + `notImplemented = true` + 立即返回 NOT_IMPLEMENTED + message 含 "not implemented in v0"）。这正是 design section 11 + ADR-0002 期望的 "诚实占位符"。
2. **PublishService 失败路径处理彻底**：file → parse → adapter 三段都包 try/catch；任何一段失败都翻成结构化 PublishResult；`never throws` 测试是行为契约。
3. **Parser 取舍清晰**：`markdown-parser.ts` 顶部 doc 显式写 in-scope / out-of-scope，避免后人误以为这是通用 CommonMark 实现。
4. **HttpClient 接口窄而 Hyrum-safe**：只 `request(url, init)`，不暴露 streaming / abort / cookie 等高级语义——和 contract.md "未来真集成时再演化" 一致。

### Nits (不阻塞)

1. `medium-adapter.composeMarkdown` 中的 `post.body.includes(b.code)` 启发式（"如果 body 里已经有这段代码就不重复 emit"）在极端情况下会被误判（例如代码片段恰好是 body 中某段散文的子串）。Walking skeleton 规模下不阻塞；如果未来真集成 Medium API，应改为依赖 parser 的"已剔除 fence"输出而不是字符串包含。
2. `PublishCallOptions.to` 用 `string` 是简洁的，但未来如果 `--to` 词表扩展，可能需要 branded type 或 union；当前规模不必。
3. `Node20FetchHttpClient` 在 demo 中不被走到（ADR-0003 已说明）。建议在 v0.x 真集成时为它单独写测试。

### FYI

1. `tsc --noEmit` 在 `strict` + `noUncheckedIndexedAccess` + `noImplicitOverride` 下零错——证明类型层面也守住了边界。
2. 所有源文件均 kebab-case + ESM 风格（`.js` 引用扩展名）——和 spec section 11 + tsconfig `"module": "ESNext"` 一致。

## Conclusion

- Conclusion: `通过`
- Next Action Or Recommended Skill: `hf-traceability-review`

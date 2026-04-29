# WriteOnce Walking Skeleton 需求规格说明

- 状态: 已批准（spec-review 2026-04-29 通过）
- 主题: 把 Markdown 文件通过 CLI 一次性发布到 Medium 的 walking-skeleton 实现，并为 Zhihu / WeChat MP 留扩展点
- 节点: `hf-specify`
- Workflow Profile: `lightweight`
- 上游输入:
  - `examples/writeonce/docs/insights/2026-04-29-writeonce-discovery.md`（已批准）
  - `examples/writeonce/docs/insights/2026-04-29-writeonce-spec-bridge.md`（已批准）

## 1. 背景与问题陈述

技术内容创作者在写完一篇技术 Markdown 文章后，需要把同一份内容手工搬运到 Medium、Zhihu、WeChat MP 等多个平台，每次重复 30–60 分钟低价值劳动。WriteOnce 试图把"作者已经决定要发布的同一份 Markdown，从一份源头一次性推到目标平台"这个最末端动作做掉。

这一节承接 discovery section 1 (problem statement) 与 section 10 (Jobs Story)。

## 2. 目标与成功标准

WriteOnce v0 walking skeleton 的目标是：

- 提供 `writeonce publish <markdown-file>` CLI，可在不修改源文件的前提下把 Markdown 推到 Medium。
- 提供 `PlatformAdapter` 抽象层，使 "增加一个平台" 是新增一个 adapter 文件 + 在配置中声明的事，而不需要改 publish 主流程。
- 留下 HarnessFlow v0.1.0 demo 所需的 16 节点工件痕迹（详见 section 3 Threshold）。

具体可验证度量见 section 3。

## 3. Success Metrics

承接 discovery section 9 与 spec-bridge section 3：

| 字段 | 值 |
|---|---|
| Outcome Metric | "任意打开 `examples/writeonce/` 的工程师能在 10 分钟内沿 HF 主链工件读完、并复述出 HF 16 个节点的角色" |
| Threshold | (a) 16 节点工件齐全；(b) walking skeleton 任务的 RED/GREEN evidence 齐全；(c) 测试 100% 通过；(d) `writeonce publish ./post.md` 在 stub 网络下可端到端运行成功 |
| Leading Indicator | walking-skeleton end-to-end 测试 CI 首跑通过率 |
| Lagging Indicator | demo 合入 main 后 "看不懂 HF 主链" 类反馈减少（demo 不强求采集） |
| Measurement Method | Demo 评估者自报；测试结果以 `evidence/` 下日志文件为准 |
| Non-goal Metrics | (a) 不追求 demo 在真实 Medium 账号上发出真实文章；(b) 不追求 Zhihu / WeChat MP 真实集成；(c) 不追求 CLI 的真实活跃度 |
| Instrumentation Debt | 不做埋点；本 spec 显式声明 v0 不投入 |

## 4. Key Hypotheses

承接 discovery section 6 与 spec-bridge section 4：

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-D-1 | 技术内容创作者愿意把"发布"动作让给 CLI 工具 | D | wedge 商业价值降低，但**不**影响 demo 留下 HF 主链可读痕迹 | 弱 | 不验证（接受为假设保留） | No |
| HYP-F-1 | Markdown 解析 + Medium adapter 在 Node 20 + TS 内可在 walking-skeleton 工作量内跑通 | F | 重选技术栈或缩小 walking-skeleton 范围 | 高 | 由 `hf-test-driven-dev` 节点 RED/GREEN 自然验证 | No |
| HYP-F-2 | Zhihu / WeChat MP "留扩展点 + 不实现"对 demo 受众是可接受的 | F | 抽象层不真实，demo 失去说服力 | 高 | 由 `hf-design-review` 在审 PlatformAdapter 接口时确认 | No |
| HYP-V-1 | demo 不追 SaaS 商业可行性 | V | demo 边界扩张到不可控 | 高 | 由 ADR-001 D9 + demo README "Limits" 段守住 | No |
| HYP-U-1 | `writeonce publish ./post.md` 一条命令对目标用户足够直观 | U | CLI 设计要重做 | 高 | 由 `hf-code-review` 在审 CLI 入口时确认 | No |

无 Blocking 假设。`hf-spec-review=通过` 不会因假设未验证被阻塞。

## 5. 用户角色与关键场景

**角色**：技术内容创作者（独立开发者 / 写技术博客的工程师）。

**关键场景**：

1. 作者在本地写完 `post.md`，希望发布到 Medium：
   ```bash
   writeonce publish ./post.md --to medium
   ```
2. 作者希望把同一文件发到所有已声明的目标平台：
   ```bash
   writeonce publish ./post.md --to all
   ```
   v0 的 `--to all` 会调用所有已注册的 `PlatformAdapter`，未实现的（Zhihu / WeChat MP）会**显式失败并打印 "not implemented in v0"**，**不**静默跳过（防止用户误以为发布成功）。
3. 作者使用未配置 token 的环境（dry-run）：
   ```bash
   writeonce publish ./post.md --to medium --dry-run
   ```
   不发出真实 HTTP 请求，只打印将发出的 payload 摘要。

## 6. 当前轮范围与关键边界

In-scope：

- 单 Markdown 源文件输入（CommonMark 子集：纯文本、标题、段落、有序/无序列表、超链接、行内代码、fenced code block 含语言标识、图片）。
- `PlatformAdapter` 抽象层（接口 + Medium 实现）。
- `MediumAdapter` 在 walking skeleton 中实现到"调用 stub HTTP 客户端发出请求"为止；真实 Medium API 集成不在 v0 内。
- CLI：`publish <file>` 子命令；`--to <platform|all>` 选项；`--dry-run` 选项。
- 结构化错误返回：`{ ok: false, code, message }`。
- 单元测试 + 1 条 walking-skeleton 端到端测试。

Out-of-scope（也见 section 7）：

- 真实 Medium 账号集成 / 真实 token / 真实 HTTP 调用
- Zhihu / WeChat MP 的实现
- 内容编辑 / 重写 / 摘要生成
- Notion / Obsidian / 多文件源
- 调度 / 评论同步 / 阅读数据回流
- GUI / Electron
- CI/CD pipeline / 镜像 / 自动发版

## 7. 范围外内容

来自 spec-bridge section 6（剪枝来源即 discovery section 7）：

- **方案 B** — 一次性 3 平台都接通真实集成（剪枝）。
- **方案 C** — Web GUI / Electron 桌面端（剪枝）。
- **方案 D** — Notion / Obsidian / 多文件源（剪枝）。
- 真实 token 管理 / OAuth 流程（v0 仅以"环境变量 stub 形式"出现在测试中）。
- 任何形式的 release / ops / CI（与 ADR-001 D1 P-Honest 一致——HF v0.1.0 主链不含 release/ops；demo 也不假装有）。

## 8. 功能需求

| ID | Statement (EARS) | Acceptance (BDD) | Priority | Source |
|---|---|---|---|---|
| FR-1 | When the user runs `writeonce publish <file> --to medium`, the system shall parse the file as Markdown and emit one HTTP POST request payload addressed to the Medium "create post" endpoint. | Given a valid Markdown file with title "Hello" and one fenced code block, When `writeonce publish post.md --to medium --dry-run` is invoked, Then the printed payload contains `title: "Hello"`, `contentFormat: "markdown"`, and the original code block content. | Must | HYP-F-1, demo Threshold (d) |
| FR-2 | When the user runs `writeonce publish <file> --to <unknown-or-unimplemented-platform>`, the system shall fail with a non-zero exit code and an error message that names the platform and the reason ("unknown" or "not implemented in v0"). | Given a valid file, When the user runs `--to zhihu`, Then exit code is non-zero and stderr contains "platform 'zhihu' is declared but not implemented in v0". | Must | HYP-F-2 (扩展点真实性) |
| FR-3 | The system shall expose a `PlatformAdapter` interface such that adding a new platform requires (a) creating a new adapter file implementing the interface and (b) registering it in a single configuration point — without modifying `publish-service.ts`. | Given the existing `MediumAdapter`, When a new `FakePlatformAdapter` is created and registered in tests, Then `publish-service.ts` source code does not change between the two runs. | Must | HYP-F-2 |
| FR-4 | When the user runs `writeonce publish <file> --to medium --dry-run`, the system shall not invoke the underlying HTTP client. | Given a `--dry-run` flag, When publish runs, Then the HTTP client's `request` method is not called (verified by spy). | Must | section 5 场景 3 |
| FR-5 | The system shall return structured errors `{ ok: false, code, message }` for all failure paths in `publish-service.ts`. | Given any failure path, When publish returns, Then the returned object contains exactly the keys `ok`, `code`, `message` and no thrown exception escapes the service boundary. | Should | NFR-Reliability-1 |
| FR-6 | The CLI shall accept `--to all` and dispatch to every registered `PlatformAdapter`. Unimplemented adapters (Zhihu, WeChat MP in v0) shall report failure individually without aborting the others. | Given Medium implemented and Zhihu / WeChat MP stubbed, When `--to all` runs, Then results array has 3 entries: 1 success, 2 explicit failures with reason "not implemented in v0". | Should | section 5 场景 2 |

## 9. 非功能需求 (ISO 25010 + Quality Attribute Scenarios)

### NFR-Reliability-1 (Reliability — Maturity)

| QAS 字段 | 值 |
|---|---|
| Stimulus Source | The CLI user (or an automated invocation) |
| Stimulus | Invokes `writeonce publish <file> --to <platform>` where any single failure mode occurs (file missing / parser failure / adapter declared-not-implemented / HTTP client failure) |
| Environment | Local terminal, Node.js 20, no network in test mode |
| Response | The system returns a structured `{ ok: false, code, message }` object; the process exits with a non-zero code; no thrown exception escapes the service boundary |
| Response Measure | 100% of unit-test failure-path cases return the structured object; 0 uncaught exceptions in the walking-skeleton e2e test |

Acceptance (BDD):
- Given a non-existent input file, When `writeonce publish missing.md --to medium` runs, Then exit code is non-zero and stderr starts with `error code=`.

### NFR-Maintainability-1 (Maintainability — Modularity)

| QAS 字段 | 值 |
|---|---|
| Stimulus Source | A future contributor |
| Stimulus | Adds a third platform implementation |
| Environment | Existing v0 walking-skeleton codebase |
| Response | Only an adapter file and a single registration line change; `publish-service.ts` and existing adapters do not change |
| Response Measure | `git diff` after the addition shows changes only in: 1 new adapter file + the registration point |

Acceptance (BDD): see FR-3 acceptance.

### NFR-Testability-1 (Maintainability — Testability)

| QAS 字段 | 值 |
|---|---|
| Stimulus Source | Test runner |
| Stimulus | Runs the e2e walking-skeleton test on an offline machine |
| Environment | No network connectivity |
| Response | The test passes by using the injected `HttpClient` test double; no real network call is attempted |
| Response Measure | E2E test runs in < 1 s; 0 real network attempts (verified by `nock` or by injecting a non-network HttpClient) |

Acceptance (BDD): Given the e2e test, When it runs with `NODE_ENV=test`, Then no DNS lookup or socket open is attempted.

## 10. 外部接口与依赖

- **Node.js 20+**：内置 `fetch`, `fs/promises`, `path`. 失效影响：低（Node 20 是 LTS）。
- **`commander`** (CLI args parser)：版本最新稳定。失效影响：低（接口稳定）。
- **`vitest`** (test runner)：版本最新稳定。失效影响：低；可换为 jest。

不引入：
- HTTP 客户端库（用 Node 内置 `fetch` 即可）。
- Markdown parser 库——v0 用一个**极简手写 parser**（只够覆盖 section 6 列出的 CommonMark 子集），避免引入大依赖。复杂的 Markdown 集成留到 v0.x。

## 11. 约束与兼容性要求

- **不**允许在 walking skeleton 中发起真实网络请求。所有 HTTP 必须经 `HttpClient` 接口注入测试 double。来源：HYP-V-1 + spec section 7 + NFR-Testability-1。
- **不**允许把真实 Medium token 写到代码 / 测试 / 工件中。来源：常识安全约束 + demo 不真集成。
- 代码风格遵循 TypeScript `strict: true`；ESLint 默认推荐；文件名 kebab-case。

## 12. 假设与失效影响

承接 section 4 的非 Blocking 假设。section 4 已显式标 confidence 与 fallback。

## 13. 开放问题

- 无阻塞项。
- 非阻塞：v0 后续若要支持真实 Medium 集成，需补 OAuth / token 管理 spec；本轮不展开。

## 14. 术语与定义

| 术语 | 定义 |
|---|---|
| WriteOnce | 本 demo 工具的产品名 |
| Walking Skeleton | Alistair Cockburn 提出的"端到端最薄实现"模式；HF 用来约束 v0 任务范围 |
| PlatformAdapter | WriteOnce 的核心抽象：把"对一个平台发布一篇文章"做成统一接口 |
| Post | parser 解析后的中间数据结构（title / body / codeBlocks 等） |
| Adapter Registration | 在 `publish-service.ts` 顶部 import 并加入 `adapters` Map 的动作 |

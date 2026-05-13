---
name: hf-regression-gate
description: 适用于 traceability review 通过后需回归验证、用户要求 regression check 的场景。不适用于判断任务完成（→ hf-completion-gate）、状态收尾（→ hf-finalize）、阶段不清（→ hf-workflow-router）。
---

# HF Regression Gate

防止"修好了本地但破坏了相邻模块"。在最小回归验证范围内收集 fresh evidence，判断回归面是否健康。运行在 traceability-review 之后。

不是 completion gate（判断当前任务完成），也不是 finalize（收尾）。

## Methodology

本 skill 融合以下已验证方法：

- **Regression Testing Best Practice (ISTQB)**: 定义回归范围时区分 full/standard/lightweight 三级覆盖，确保投入与风险匹配。
- **Impact-Based Testing**: 回归范围基于 traceability review 识别的影响区域，而非机械运行全部测试。
- **Fresh Evidence Principle**: 回归证据必须在当前会话内实际产生，不接受历史运行结果替代。

## When to Use

适用：traceability review 通过后需回归验证；用户要求 regression check。

不适用：判断任务完成 → `hf-completion-gate`；状态收尾 → `hf-finalize`；阶段不清 → `hf-workflow-router`。

## Hard Gates

- 无当前会话 fresh evidence 不得宣称回归通过
- 上游 review/gate 记录缺失不得通过
- worktree-active 时 evidence 必须锚定同一 Worktree Path

## Workflow

### 1. 对齐上游结论

确认当前 profile 必需的 review/gate 记录齐全且结论支持继续。

Profile-aware 回归范围：
- `full`：traceability 识别的所有区域
- `standard`：直接相关模块
- `lightweight`：最小 build/test 入口

Evidence-tier 回归范围（按当前 task / traceability 影响面叠加，不被 profile 降级覆盖）：

| Evidence Tier | 可证明什么 | 不能证明什么 |
|---|---|---|
| `mocked-unit` | 纯逻辑、局部函数、隔离组件行为 | 真实浏览器、真实 API、App 根配置、跨组件集成 |
| `component-integration` | 真实子组件组合、provider / router / store 配置 | 真实浏览器网络栈、后端契约 |
| `api-contract` | 前后端路径、method、status、DTO 字段、base URL / proxy 一致 | 浏览器渲染和用户交互 |
| `browser-runtime` | DOM / Console / Network 三层真实浏览器行为 | 后端持久化完整性、非浏览器服务间流程 |
| `full-stack-smoke` | 启动服务、健康检查、关键端到端用户流 | 大规模性能、全量业务覆盖 |

触发规则：
- 触碰 UI route、App 根组件、UI provider、浏览器存储、表单、前端 API client、Vite proxy/env → 至少需要 `browser-runtime`；若有后端交互，同时需要 `api-contract` 或 `full-stack-smoke`
- 触碰 UI surface / visual token / layout / component library usage → `browser-runtime` 必须包含 UI conformance evidence：截图路由+viewport、DOM anchors、console/network 记录、与 UI Implementation Contract 的匹配结论
- 触碰 HTTP controller / API DTO / auth / CORS / base URL / proxy → 至少需要 `api-contract`
- 触碰跨前后端用户流 → 需要 `full-stack-smoke`
- `happy-dom` / jsdom / mock fetch / mocked provider 只能归为 `mocked-unit` 或 `component-integration`，不得写成 `browser-runtime` 或 `api-contract`
- 若任务 DoD 或项目级 runtime-smoke profile 要求某 tier，缺失该 tier 即为强制验证未完成

### 1.5 Precheck：能否合法进入 gate

检查：上游 review / traceability 记录是否齐全、实现交接块是否稳定、worktree 状态与当前验证位置是否一致。

- 上游结论缺失或 route/stage/profile 冲突 → `阻塞`，下一步 `hf-workflow-router`
- worktree-active 但 evidence 无法锚定同一 `Worktree Path` → `阻塞`，下一步 `hf-regression-gate`
- precheck 通过 → 继续定义回归面

### 2. 定义回归面

明确回归覆盖：哪些模块/命令/测试套。不覆盖什么要显式写出。

### 3. 执行回归检查

运行完整回归命令。不用更弱证据替代。

### 4. 阅读结果

检查退出码、失败数量、输出是否支持"回归通过"结论、结果是否属于当前代码。

### 4A. 回归信号判定表

先把当前信号映射到**一类回归结论**，再写 record。不要只说“测试大致没问题”。

| 信号 | 最少需要的 fresh evidence | conclusion | next_action_or_recommended_skill |
|---|---|---|---|
| build / typecheck / lint 失败 | 失败命令、退出码、关键报错摘录 | `需修改` | `hf-test-driven-dev` |
| 测试通过但覆盖率低于 项目级覆盖率门槛或当前任务门槛 | 覆盖率命令、实际结果、门槛来源 | `需修改` | `hf-test-driven-dev` |
| UI / API / full-stack 影响面缺少对应 evidence tier | 影响面、缺失 tier、已有 weaker evidence、DoD / 项目约定来源 | `需修改`；若工具链 / 环境不可用且无降级许可 → `阻塞` | `hf-test-driven-dev` 或 `hf-regression-gate` |
| UI conformance claim 缺少截图 / DOM anchors / console-network evidence，或截图未对照 UI Implementation Contract | UI surface、缺失证据、contract anchor、已有 weaker evidence | `需修改`；若环境不可用且无降级许可 → `阻塞` | `hf-test-driven-dev` 或 `hf-regression-gate` |
| 记录把 happy-dom / jsdom / mock fetch 称作真实浏览器或真实 API 集成 | 测试环境、mock 边界、错误分类的证据摘录 | `需修改` | `hf-test-driven-dev` |
| `lightweight` 且仅文档 / 配置类变更 | 最小相关验证（如 docs build、lint、config parse）+ 明确未覆盖区域 | 结果驱动 | 通过时 `hf-completion-gate`，否则 `hf-test-driven-dev` |
| 强制集成 / e2e 验证因环境不可用而未跑 | 项目约定 / DoD 是否允许降级；若允许，给出替代验证结果；若不允许，写明阻塞原因 | 无降级许可 → `阻塞`；有许可则按结果判断 | 无降级许可 → `hf-regression-gate` |
| `worktree-active` 但证据来自其他目录或旧代码状态 | 当前 `Worktree Path`、证据来源路径 / 时间锚点 | `阻塞` | `hf-regression-gate` |
| 上游 review/gate 缺失，或 route / stage / profile 冲突 | 缺失项或冲突项清单 | `阻塞` | `hf-workflow-router` |

补充规则：
- 构建、类型检查、静态检查失败都属于 regression signal，不因测试通过而忽略
- 若准备因为 `lightweight`、文档-only 或环境问题而缩小回归范围，先检查 项目约定 / DoD 是否明文允许
- `interactive`：无明文允许时，先展示“建议缩减到什么 / 为什么 / 未覆盖什么”，等真人确认
- `auto`：无明文允许时不得自行降级，直接 `阻塞`

### 5. 形成 evidence bundle

记录：回归面定义、命令、退出码、结果摘要、新鲜度锚点、覆盖边界、未覆盖区域。

若项目未覆写格式，默认把 evidence bundle 映射到本 skill 模板 `references/verification-record-template.md` 的这些字段：
- `Metadata`：`Verification Type=regression-gate`、Scope、Record Path、Worktree Path / Branch（若适用）
- `Upstream Evidence Consumed`：已消费的 traceability / review / handoff / task-progress 记录
- `Verification Scope`：Included Coverage、Uncovered Areas
- `Evidence Tier Coverage`：列出 mocked-unit / component-integration / api-contract / browser-runtime / full-stack-smoke 的 required / provided / N/A 状态
- `UI Conformance Evidence`：列出 screenshots、viewports、DOM anchors、console/network assertions、UI contract anchors、visual drift / token bypass 检查结果
- `Commands And Results`：命令、退出码、Summary、Notable Output
- `Freshness Anchor`：为什么这些结果锚定当前代码状态
- `Conclusion`：`通过` / `需修改` / `阻塞` + 唯一 `Next Action Or Recommended Skill`

### 6. 门禁判断

- `通过` → `hf-completion-gate`
- `需修改` → `hf-test-driven-dev`
- `阻塞`(环境) → 重试 `hf-regression-gate`
- `阻塞`(上游) → `hf-workflow-router`

## Output Contract

记录保存到 项目声明的 verification 路径；若无项目覆写，默认使用 `features/<active>/verification/regression-YYYY-MM-DD.md`（如需对应到具体任务，可写 `regression-task-NNN.md`）。若项目无专用格式，默认使用本 skill 模板 `references/verification-record-template.md`。

最少应包含：
- 已消费的上游证据（至少写清 implementation handoff、traceability review、相关 review/gate records）
- 回归面定义、Included Coverage 与 Uncovered Areas
- evidence tier 覆盖矩阵；若存在 UI / API / full-stack 影响面，必须写出 runtime / contract / smoke 是否已覆盖
- 若存在 UI surface / visual token / layout 影响面，必须写出 UI conformance evidence：截图路径、viewport、DOM anchors、console/network 摘要、UI Implementation Contract 对照结论
- 命令、退出码、结果摘要、关键失败/警告摘录
- 新鲜度锚点与 worktree 锚点（若适用）
- 若使用 coverage / docs build / config parse / integration fallback，必须写出依据来源（项目约定 / DoD）
- 唯一门禁结论与唯一下一步

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/verification-record-template.md` | regression verification record 模板（与 `hf-completion-gate` 同形态） |
| `references/runtime-smoke-profile.md` | 项目侧 runtime smoke / health check / API contract / browser routes 声明模板 |
| `references/ui-conformance-evidence-profile.md` | UI 截图、viewport、DOM/console/network 与 design contract 对照声明模板 |

## Red Flags

- 不读上游 review 记录就跑回归
- "本地测试通过"等同于"回归安全"
- 依赖旧运行结果
- worktree-active 但 evidence 没锚定同一路径

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "影响面分析跳过，直接看 CI 绿。" | Hard Gates: impact-based regression 要求基于 design + code change 显式列影响面；CI 绿不等于覆盖到位。 |
| "evidence bundle 里少一条 trace 不影响结论。" | Workflow stop rule: bundle 任一必需证据缺失即判 fail，不允许"不影响"裁量。 |
| "我先放过这次，下次回归再补全。" | Hard Gates (soul.md): gate 不能替用户降低门禁；补全才能 pass。 |

## Verification

- [ ] regression record 已落盘
- [ ] 回归面定义、evidence bundle 已写清
- [ ] precheck blocker 与 worktree 锚点（若适用）已写清
- [ ] 基于最新证据给出唯一门禁结论
- [ ] feature `progress.md` 已同步

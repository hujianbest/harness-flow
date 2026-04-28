---
name: df-finalize
description: Use when a work item must be formally closed out. Two closeout types: (a) implementation closeout for AR / DTS / CHANGE — triggered after df-completion-gate verdict 通过; promotes ar-design + (if applicable) component-design + optional sub-assets to docs/; (b) analysis closeout for SR — triggered after df-spec-review (no component design revision) or df-component-design-review (with component design revision); promotes only component-design (if revised) + the SR's AR Breakdown Candidates handed back to the requirement owner. Also used when the user explicitly asks "做收尾 / closeout / 把这个 SR / AR 收掉". Not for new implementation (→ df-tdd-implementation), not for completion judgment (→ df-completion-gate), not for stage / route confusion (→ df-workflow-router).
---

# df 收尾（覆盖 implementation closeout 与 analysis closeout）

正式做 work item 的 closeout：消费上游 verdict，把过程产物里的正式设计同步到组件仓库 `docs/`，把 work item 状态收口为 `closed`。

df 默认每个 work item 一次 finalize；不维护 task queue。本 skill 同时承担两类 closeout：

1. **Implementation closeout**（AR / DTS / CHANGE，profile = 实现 profile）
   - 触发：`df-completion-gate` verdict = `通过`
   - 同步：`docs/ar-designs/AR<id>-<slug>.md`（必填）+ `docs/component-design.md`（component-impact 时必填）+ 项目已启用的可选子资产 + release 锚点（按团队约定）
   - evidence：要求 implementation handoff、test-check、code-review、completion 全套证据

2. **Analysis closeout**（SR，profile = `requirement-analysis`）
   - 触发：`df-spec-review` 通过且 SR 不需要修订组件设计；或 `df-component-design-review` 通过且 SR 需要修订组件设计
   - 同步：`docs/component-design.md`（仅当本 SR 修订了组件设计）+ 项目已启用的可选子资产 + AR Breakdown Candidates（写入 SR 的 closeout，由需求负责人按候选**新建** AR work item，由 router 重新分流）
   - evidence：**不**要求 implementation / test / code-review evidence；不 promote 到 `docs/ar-designs/`

本 skill **不**做新实现、**不**替 completion gate 判断完成、**不**修改其他组件、**不**创造新需求方向、**不**替需求负责人决定候选 AR 何时新建。

## When to Use

适用：

- **Implementation closeout**：`df-completion-gate` verdict = `通过`（AR / DTS / CHANGE 实现子街区）
- **Analysis closeout（SR）**：`df-spec-review` verdict = `通过` 且 SR 不需要修订组件设计；或 `df-component-design-review` verdict = `通过` 且 SR 需要修订组件设计
- 用户明确要求「做收尾 / closeout / 把这个 SR / AR 收掉」
- 当前剩余工作主要是：状态收口、长期资产同步（`docs/component-design.md`、`docs/ar-designs/` 仅 implementation closeout，以及项目已启用的可选子资产）、handoff 给团队 / 提交 / 合并

不适用 → 改用：

- 实现子街区 completion gate 还没通过 → `df-completion-gate`
- 还需要新实现 → `df-tdd-implementation`
- SR 还没通过 spec-review 或还需修订组件设计 → 回 `df-spec-review` / `df-component-design-review`
- 阶段不清 → `df-workflow-router`

## Hard Gates

通用：

- 不混入新实现；发现需改动 → 停下回上游
- 长期资产同步必须按 promotion rules（见 `references/promotion-checklist.md` 与 `docs/df-shared-conventions.md` 的 Promotion Rules 节）执行
- 必须显式记录 **Closeout Type** = `implementation` / `analysis` / `blocked`
- 必须记录 closeout verdict（`closed` / `blocked`）
- 不修改其他组件
- 不替模块架构师 / 开发负责人决定是否合并 / 发布

Implementation closeout 专属：

- 无 `df-completion-gate` `通过` verdict 不得进入
- AR work item 必须 promote `docs/ar-designs/AR<id>-<slug>.md`

Analysis closeout 专属：

- 无 `df-spec-review`（SR 不修订组件设计场景）或 `df-component-design-review`（SR 修订组件设计场景）`通过` verdict 不得进入
- **不得**消费 implementation handoff / test-check / code-review / completion 证据；这些证据对 SR 不存在
- **不得** promote 到 `docs/ar-designs/`；SR 不是 AR 的设计
- 必须把 SR 的 `AR Breakdown Candidates` 定稿后写入 closeout，作为给需求负责人的交付产物；候选 AR 是否新建 work item **不**由 df 决定
- closeout 后 SR work item 即关闭；不允许在同一 work item 内续接实现节点

## Object Contract

- Primary Object: closeout pack（含 evidence matrix、长期资产同步清单、状态字段、Closeout Type）
- Frontend Input Object（按 Closeout Type）：
  - **Implementation closeout**：`features/<id>/completion.md`（应 `通过`）、`features/<id>/ar-design-draft.md`、`features/<id>/component-design-draft.md`（component-impact 时）、所有 review 记录、`docs/component-design.md` / `docs/ar-designs/` 现状、项目已启用的可选子资产、`features/<id>/progress.md`
  - **Analysis closeout**：`features/<id>/requirement.md`、`features/<id>/reviews/spec-review.md`（应 `通过`）、`features/<id>/component-design-draft.md` + `features/<id>/reviews/component-design-review.md`（仅当 SR 修订组件设计）、`docs/component-design.md` 现状、项目已启用的可选子资产、`features/<id>/progress.md`、`features/<id>/README.md`
- Backend Output Object：
  - `features/<id>/closeout.md`（含 Closeout Type 字段）
  - 同步到 `docs/component-design.md`（implementation closeout component-impact 或 analysis closeout 修订组件设计时）
  - 同步到 `docs/ar-designs/AR<id>-<slug>.md`（**仅** implementation closeout 的 AR 工作项必填；DTS 不修改 AR 设计时与 SR 一律不写本路径）
  - 同步到 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（仅当项目已启用对应可选子资产，且本次触发变化；未启用的，把变化合并进 `docs/component-design.md`）
  - `features/<id>/progress.md` 收口为 `Current Stage = closed`
  - `features/<id>/README.md` 状态收口
  - **仅 analysis closeout**：`features/<id>/closeout.md` 含定稿的 `AR Breakdown Candidates` 章节，作为给需求负责人的交付清单
- Object Transformation: 把过程产物 promote 为长期资产 + 状态收口
- Object Boundaries: 不写代码 / 不动其他组件 / 不动其他 work item / 不替需求负责人新建候选 AR
- Object Invariants: closeout 后 `Next Action Or Recommended Skill = null`（已完成）

## Methodology

- **Project Closeout**: 系统性收尾，确认交付物完成、状态同步、handoff 完整
- **Promotion Rules**: 过程目录 → 长期资产（详细规则见 `references/promotion-checklist.md`）
- **Evidence Bundle Pattern**: closeout pack 列出已消费的所有证据
- **Sync-On-Presence**: 项目当前未启用的可选资产不构成 `blocked`
- **Single-Work-Item Discipline**: 一次 finalize 对应一个 AR / DTS

## Workflow

### 1. 判定 Closeout Type 并读取最少必要输入

按 work item 的 `Workflow Profile` 与最近一次 verdict 判定 Closeout Type：

| Profile + 上游 verdict | Closeout Type |
|---|---|
| 实现 profile + `df-completion-gate` `通过` | `implementation` |
| `requirement-analysis` + `df-spec-review` `通过`（SR 不修订组件设计） | `analysis` |
| `requirement-analysis` + `df-component-design-review` `通过`（SR 修订组件设计） | `analysis` |
| 其他 | `blocked` |

按 Read-On-Presence 读取对应输入：

- **Implementation**：`features/<id>/completion.md`（应 `通过`）、所有 review 记录、ar-design-draft.md、component-design-draft.md（若有）、`docs/component-design.md` / `docs/ar-designs/` 现状、项目已启用的可选子资产、`features/<id>/progress.md`、`features/<id>/README.md`、`AGENTS.md`
- **Analysis**：`features/<id>/requirement.md`、`features/<id>/reviews/spec-review.md`、`features/<id>/component-design-draft.md` + `features/<id>/reviews/component-design-review.md`（仅当 SR 修订组件设计）、`docs/component-design.md` 现状、项目已启用的可选子资产、`features/<id>/progress.md`、`features/<id>/README.md`、`AGENTS.md`

### 1.5 Precheck

通用：

- profile / route / 上游 verdict 冲突 → blocked-workflow，`reroute_via_router=true`，下一步 `df-workflow-router`

Implementation 专属：

- completion 缺记录 → blocked-content，回 `df-completion-gate`
- AR 工作项缺 `docs/ar-designs/` 同步路径 → blocked-content，先在本节点完成 promote

Analysis 专属：

- spec-review 未通过 → blocked-content，回 `df-spec-review`
- SR 声明需修订组件设计但 component-design-review 未通过 → blocked-content，回 `df-component-design-review`
- AR Breakdown Candidates 章节缺失且未声明「无可拆分 AR」 → blocked-content，回 `df-specify`
- SR work item 试图走 implementation closeout → blocked-workflow，`reroute_via_router=true`

否则进入步骤 2。

### 2. 同步长期资产（按 Closeout Type 分支）

按 Promotion Rules（详见 `references/promotion-checklist.md`），按 Sync-On-Presence。

**Implementation closeout**：

- **AR 工作项必须同步**：把 `features/<id>/ar-design-draft.md` promote 到 `docs/ar-designs/AR<id>-<slug>.md`（保留 AR ID / SR / IR / Owner / 测试设计章节锚点；去掉 Open Questions / 过程笔记）
- **component-impact 必须同步**：把 `features/<id>/component-design-draft.md` 合并到 `docs/component-design.md`（必要时新增章节 / 修订条目，并补变更记录）
- **接口 / 依赖 / 运行时行为如有变更**：sync-on-presence；未启用的合并进 `docs/component-design.md`，不自动新建可选子资产
- **DTS 不修改 AR 设计**：closeout pack `Long-Term Assets Sync` 对应行写 `N/A`；若 DTS 修改了组件级行为仍需同步 `docs/component-design.md`

**Analysis closeout**：

- **不**写 `docs/ar-designs/`（SR 不是 AR 设计）
- **仅当**本 SR 修订了组件设计：把 `features/<id>/component-design-draft.md` 合并到 `docs/component-design.md`，并按 sync-on-presence 同步项目已启用的可选子资产
- **必须**把 `AR Breakdown Candidates` 章节定稿写入 `features/<id>/closeout.md`（每条候选含 Candidate ID / Scope / Owning Component / Covers SR Rows / Hand-off Owner），作为给需求负责人的交付物；候选 AR 由需求负责人决定何时新建对应 work item，**不**由本 skill 自动新建
- 项目当前未启用的可选资产 → 写 `N/A（项目未启用）`，不阻塞

### 3. 同步 work item 状态

按 Canonical Field Sync：

- `features/<id>/progress.md`：`Current Stage = closed`、`Pending Reviews And Gates` 清空、`Next Action Or Recommended Skill = null`、`Last Updated` 当前时间
- `features/<id>/README.md`：`Closed` 当前日期；`Closeout Verdict = closed`；`Process Artifacts` 表 Closeout 行更新为 `present`；`Reviews & Gates` 表 completion-gate 行更新

### 4. 形成 evidence matrix

按 Evidence Bundle Pattern 列出每条证据的路径与状态（含 `N/A`）；项目未启用的可选资产显式标注 `N/A（项目未启用）`，避免被误判为 blocked。

### 5. 产出 closeout pack

按 `templates/df-closeout-template.md` 写入 `features/<id>/closeout.md`，包含 Closeout Summary、Evidence Matrix、Long-Term Assets Sync、State Sync、Handoff。pack 缺关键字段 → 回步骤 2-4 补齐。

### 6. Handoff

按 Handoff Pack Pattern 给团队 closeout summary（含分支 / MR / PR 信息、长期资产同步清单、未闭合风险）。**不**替开发负责人 / 模块架构师决定是否合并 / 发布。

## Output Contract

- `features/<id>/closeout.md`，按 `templates/df-closeout-template.md`
- 长期资产同步：
  - AR 工作项：`docs/ar-designs/AR<id>-<slug>.md` 必填
  - component-impact：`docs/component-design.md`（+ 仅当项目已启用并触发变化时同步 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`）
  - 未触发资产变化：closeout pack 中显式写 `N/A`
- `features/<id>/progress.md` 收口为 `Current Stage = closed`、`Next Action Or Recommended Skill = null`
- `features/<id>/README.md` 状态收口
- 结构化 handoff 摘要：work_item_id、closeout_verdict、long_term_assets_synced、blockers、`next_action_or_recommended_skill = null`

## Red Flags

- completion gate 没通过就开始 finalize
- 长期资产未同步就声称 closeout 完成
- AR 工作项跳过 `docs/ar-designs/` 同步
- 把过程目录里的草稿直接当作长期资产（应做 promote 改写：去掉草稿专属内容、补全长期文档结构）
- 修改其他组件
- 没记录 closeout verdict
- 把闭口后的 work item 移到 `features/archived/`（破坏反向引用）
- closeout 后再写 `Next Action Or Recommended Skill = df-workflow-router`（应为 `null`）

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 把 ar-design-draft.md 原样复制到 docs/ar-designs/ | 做必要的语义化改写（去掉草稿过程笔记、补长期资产章节标题） |
| component-impact 但漏同步 docs/component-design.md | 阻塞，回到步骤 3 |
| closeout pack 没列 N/A 项 | 显式列出，避免被误判 blocked |

## Verification

通用：

- [ ] precheck 结果与 Closeout Type 显式记录
- [ ] 长期资产同步已执行（按 Closeout Type 与 sync-on-presence）
- [ ] `features/<id>/closeout.md` 已落盘，含 `Closeout Type` 字段
- [ ] `features/<id>/progress.md` 收口为 `Current Stage = closed`、`Next Action Or Recommended Skill = null`
- [ ] `features/<id>/README.md` 状态收口
- [ ] handoff 摘要含 closeout_type / closeout_verdict / long_term_assets_synced / next_action_or_recommended_skill = null
- [ ] 未混入新实现
- [ ] feature 目录平铺保留在 `features/`（未被移动到 `features/archived/`）

Implementation closeout 额外：

- [ ] completion verdict = `通过` 已确认
- [ ] AR 工作项已 promote 到 `docs/ar-designs/AR<id>-<slug>.md`（DTS 不修改 AR 设计时显式 N/A）
- [ ] component-impact 时 `docs/component-design.md` 已更新

Analysis closeout（SR）额外：

- [ ] spec-review verdict = `通过` 已确认；如 SR 修订组件设计，component-design-review verdict = `通过` 也已确认
- [ ] AR Breakdown Candidates 章节已定稿写入 closeout，每条候选字段齐全；或显式声明「无可拆分 AR」并由需求负责人确认
- [ ] **未** promote 到 `docs/ar-designs/`
- [ ] **未**消费 implementation handoff / test-check / code-review / completion 证据

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/promotion-checklist.md` | 长期资产 promote 路径 + 写法约定 |
| `templates/df-closeout-template.md` | closeout pack 模板 |
| `docs/df-shared-conventions.md` | 路径、canonical 字段、Promotion Rules |

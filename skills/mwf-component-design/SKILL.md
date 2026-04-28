---
name: mwf-component-design
description: Use when the workflow profile is component-impact and the owning component lacks a current implementation design, when the existing docs/component-design.md is stale or inconsistent with code, when an AR or DTS adds/changes SOA interfaces / component dependencies / state machines / runtime mechanisms, or when mwf-component-design-review returns 需修改/阻塞. Not for AR-level code design (→ mwf-ar-design), not for general spec clarification (→ mwf-specify), not for routine within-component changes (→ mwf-ar-design directly).
---

# mwf 组件实现设计

为唯一所属组件产出或修订**组件实现设计**，描述该组件的职责、SOA 接口、依赖、数据 / 状态、运行机制和对 AR 实现设计的约束。

本 skill 不写单个 AR 的代码层设计（那是 `mwf-ar-design` 的职责），不写代码，不修改其他组件。它的输出是组件长期资产，受团队组件设计模板约束。

## When to Use

适用：

- `mwf-workflow-router` 已升级到 `component-impact` profile 且组件设计需要新增 / 修订
- 当前 AR / DTS 新增组件、修改 SOA 接口、修改组件职责或依赖方向、修改状态机或运行时机制
- 现有 `docs/component-design.md` 缺失、过期或与代码明显不一致
- `mwf-component-design-review` 返回 `需修改` / `阻塞` 需修订

不适用 → 改用：

- 仅修改本组件内部实现而不影响接口 / 依赖 / 状态机 → `mwf-ar-design`
- 需求不清 → `mwf-specify`
- 直接进入 AR 代码层设计 → `mwf-ar-design`
- 阶段不清 / 证据冲突 → `mwf-workflow-router`

## Hard Gates

- 组件实现设计必须遵循团队模板（`templates/mwf-component-design-template.md`；模板留空时由模块架构师手动补齐章节后再交评审）
- 不替模块架构师拍板组件边界 / SOA 接口 / 跨组件依赖；模块架构师必须 sign-off
- 组件实现设计 review 通过前，AR 实现设计**不得**消费本设计的草稿版本
- 组件实现设计中**不得**写单个 AR 的代码层设计
- 不修改其他组件
- 未经 router 升级到 component-impact profile，不得直接进入本节点

## Object Contract

- Primary Object: component implementation design model
- Frontend Input Object: `features/<id>/requirement.md`（已通过 spec-review）、`features/<id>/traceability.md`、当前 `docs/component-design.md`（如存在）、相关 SR / AR 上游锚点、组件代码现状摘要
- Backend Output Object: `features/<id>/component-design-draft.md`（过程版） + 同步到 `docs/component-design.md`（review 通过且模块架构师 sign-off 后）
- Object Transformation: 把组件职责 / 接口 / 依赖 / 数据 / 运行机制写成长期可消费的设计
- Object Boundaries: 不写 AR 代码层设计；不修改其他组件；不写代码
- Object Invariants: 组件名、所属子系统、模块架构师 owner 在 review 通过前保持稳定

## Methodology

- **SOA Component Boundary Analysis**: 显式说明组件职责 / 接口 / 依赖 / 跨组件影响
- **Clean Architecture Boundary Discipline**: 保持依赖方向稳定；不让实现细节倒灌到上层
- **Interface Segregation**: 组件对外接口尽量内聚、最小知识
- **C / C++ Defensive Design**: 组件级内存模型、并发模型、错误处理 / 资源生命周期约束
- **Template-Constrained Design**: 设计文档结构由团队模板决定（`templates/mwf-component-design-template.md`，留空待团队补齐）
- **Embedded Risk Awareness**: 实时性 / 中断上下文 / ABI 兼容 / 编译条件作为一等约束

## Workflow

### 1. 对齐输入与角色

按 Read-On-Presence 读取 `features/<id>/requirement.md`、`features/<id>/reviews/spec-review.md`（verdict 应 `通过`）、当前 `docs/component-design.md` / `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（若存在）、组件代码现状的最少必要摘要。spec-review 未通过 → 阻塞，回 `mwf-workflow-router`；模块架构师 owner 未指定 → 阻塞，回需求负责人。

### 2. 判定本次是新增 / 修订 / 单纯消费

对照 requirement.md 的 Component Impact Assessment 与当前 docs 状态，三选一：

- `new`：新增组件 / 新增章节
- `revise`：修订现有 `docs/component-design.md` 的某些章节
- `consume-only`：本次只消费现有组件设计 → 标 `reroute_via_router=true`，下一步 `mwf-workflow-router`（router 应把 profile 退回 standard，不应进入本节点）

### 3. 加载团队模板

按 Template-Constrained Design，加载 `templates/mwf-component-design-template.md`（项目 `AGENTS.md` 模板覆盖优先）。模板章节留空（团队未补齐）时**不阻塞写作**，但草稿中显式标注「使用 mwf 占位模板，待团队模板补齐」；review 前由模块架构师把模板章节补齐到团队规定结构。

### 4. 起草 / 修订设计

按 SOA Component Boundary Analysis + Clean Architecture + Interface Segregation + C/C++ Defensive Design 写 `features/<id>/component-design-draft.md`。具体结构遵循团队模板；模板未补齐时按团队预期结构占位，至少覆盖：组件职责与非职责、SOA 服务与接口（服务名 / 参数 / 错误码 / 时序约束 / 兼容性）、依赖组件（内部依赖 / 版本约束 / 初始化与 shutdown 顺序）、数据模型与状态机、并发 / 实时性 / 资源生命周期、错误处理与降级、配置项与编译条件、对 AR 实现设计的约束。章节缺失或与团队模板不符 → 显式标注，由 reviewer 判定。

### 5. 校验跨组件影响

按 SOA Component Boundary Analysis 列出修订接口 / 依赖 / 状态机带来的下游组件影响，以及是否需要在其他组件仓库分别开 work item / 升级 component-impact。跨组件协调点未确认 → 标为 Open Question 回需求负责人 / 模块架构师，不在本设计中替其他组件做决策。

### 6. 同步 traceability 与 progress

按 Requirements Traceability 在 `features/<id>/traceability.md` 补「Component Design Section」列，并把 `features/<id>/progress.md` 写为 `Current Stage = mwf-component-design`、`Pending Reviews And Gates` 含 `component-design-review`、`Next Action Or Recommended Skill = mwf-component-design-review`。canonical 字段不允许自由文本。

### 7. 自检与 handoff

进入 handoff 前自检：组件职责 / 非职责清晰；SOA 接口含错误码 / 时序约束 / 兼容性；依赖方向无环；状态机覆盖核心生命周期；并发 / 实时性 / 资源 / 错误处理已落到具体章节；「对 AR 实现设计的约束」章节存在；团队模板章节齐全或显式占位；跨组件影响已显式列出。任一失败 → 回步骤 4。自检通过 → 父会话派发独立 reviewer subagent 执行 `mwf-component-design-review`。

## Output Contract

- `features/<id>/component-design-draft.md`（过程版本）
- review 通过且模块架构师 sign-off 后，**由 `mwf-finalize` 同步**到 `docs/component-design.md`（必要时同步 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`）
- `features/<id>/traceability.md` 补充组件设计章节锚点
- `features/<id>/progress.md` 同步：
  - `Current Stage = mwf-component-design`
  - `Next Action Or Recommended Skill = mwf-component-design-review`
  - `Pending Reviews And Gates` 含 `component-design-review`
- handoff 摘要按 mwf-shared-conventions 字段；`reviewer_dispatch_request` 字段指向 `mwf-component-design-review`

## Red Flags

- 把单个 AR 的代码层设计写进组件设计
- 在 AR 上下文里临时改写组件架构（应停下回到本节点或上抛模块架构师）
- 修改其他组件
- 模板未补齐就让 reviewer 给 `通过`（应该让 reviewer 把模板留空作为 finding）
- 把模糊词（"高效"、"必要时"）作为组件级约束
- 跨组件协调未确认就声称设计完整

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 把"AR-XYZ 的实现思路"写进组件设计 | 抽离回 `mwf-ar-design`；本设计只写组件级约束 |
| 团队模板留空，写得很短 | 显式标注待补齐章节；不要伪装完整 |
| 修订 SOA 接口未列错误码兼容性 | 补完错误码集合 + 兼容性策略 |

## Verification

- [ ] `features/<id>/component-design-draft.md` 已落盘
- [ ] 团队模板章节齐全或显式标注待补齐
- [ ] SOA 接口、依赖、数据 / 状态、并发 / 实时性 / 资源、错误处理、配置项、对 AR 设计的约束章节存在
- [ ] 跨组件影响已显式列出
- [ ] traceability.md 已补充组件设计章节锚点
- [ ] progress.md 已 canonical 同步，下一步 `mwf-component-design-review`
- [ ] 模块架构师 owner 已记录
- [ ] 父会话准备派发独立 reviewer subagent

## Supporting References

| 文件 | 用途 |
|---|---|
| `skills/templates/mwf-component-design-template.md` | 团队组件设计模板（待团队补齐） |
| `skills/docs/mwf-workflow-shared-conventions.md` | 工件路径、canonical 字段、handoff |
| `docs/mwf-principles/03 artifact-layout.md` | `docs/component-design.md` 必含项 |
| `mwf-workflow-router/references/profile-and-route-map.md` | component-impact route 触发条件 |

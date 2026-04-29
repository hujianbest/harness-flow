---
name: hf-increment
description: 适用于用户明确要求增删改需求/范围/验收/约束、hf-workflow-router 判定属于 increment 分支的场景。不适用于实现缺陷修复（→ hf-hotfix）、继续实现（→ hf-test-driven-dev）、阶段不清/证据冲突（→ hf-workflow-router）。
---

# HF 增量变更

处理需求变更，但不能把变化偷偷渗透到主链下游。负责变更分析、失效判断、工件同步与 canonical re-entry handoff，不直接推进实现。

## Methodology

本 skill 融合以下已验证方法：

- **Change Impact Analysis (Boehm/Pfleeger)**: 系统性分析变更对已批准工件（规格、设计、任务、验证证据）的影响，识别哪些失效、哪些可保留。
- **Re-entry Pattern (State Machine)**: 根据影响分析结果，将主链安全回流到唯一 canonical 节点重新开始，而非就地打补丁。
- **Baseline-before-Change**: 变更前先锁定当前基线状态，确保变更可追溯、可回退。
- **Separation of Analysis and Implementation**: increment 只做分析和工件同步，不直接推进实现。

## Overview

这个 skill 用来把“范围、验收或约束变化”重新锚定回正确阶段。

高质量 increment 不只是记录“需求变了”，而是判断：

- 当前变化是不是 increment，而不是 hotfix 或单纯澄清
- 哪些批准、任务、验证证据和活动任务已经失效
- 应该把主链安全地回流到哪个唯一 canonical 节点

## When to Use

在这些场景使用：

- 用户明确要求增删改需求、范围、验收标准或约束
- `hf-workflow-router` 已判定当前属于 increment 分支
- 已批准规格 / 设计 / 任务 / 验证依据发生了实质性变化
- 当前需要先完成影响分析与工件同步，再决定回到哪个主链节点
- 当前变化已经稳定到足以形成结构化变更包，而不是直接改实现

不要在这些场景使用：

- 当前问题本质上是“原本应成立的行为没有被正确实现”，改用 `hf-hotfix`
- 当前已经明确进入实现阶段，需要继续实现，改用 `hf-test-driven-dev`
- 当前请求只是阶段不清、profile 不稳或证据链冲突，先回到 `hf-workflow-router`
- 当前变化仍然含糊、无法稳定结构化，先回 `hf-specify` 或 `hf-workflow-router`

这个 skill 的职责是把变化重新锚定回正确阶段，而不是自己替代 `hf-specify`、`hf-design`、`hf-tasks` 或 `hf-test-driven-dev`。

## Hard Gates

- 在完成影响分析与失效判断前，不得把当前 increment 直接交给下游实现节点。
- 如果当前输入工件还不足以判定 stage / route，不直接开始 increment 分析。
- `hf-increment` 不直接替代规格、设计、任务、实现、review 或 gate 节点；它只负责同步变化并选唯一 re-entry 节点。

## Workflow

### 1. 固定当前基线并判断 branch 类型

在给出结论前，先读取并固定以下证据来源：

- 当前变更请求本身
- feature `progress.md`（默认 `features/<active>/progress.md`）中的 `Workflow Profile`、`Current Stage`、`Current Active Task` 与 `Pending Reviews And Gates`
- 当前已批准规格、设计、任务工件
- 当前已存在的 review / gate / 验证证据（如受影响）
- 项目级工件路径、批准规则、状态字段和 re-entry 约定（若项目已声明）

先回答：

- 具体变了什么
- 哪些内容仍然有效
- 当前变化更像 increment 还是 hotfix
- 当前是否已经出现 profile 升级信号

### 1.5 Precheck

在继续形成 `New / Modified / Deprecated` 变更包前，先确认：

- 当前基线已经固定：`Workflow Profile`、`Current Stage`、`Current Active Task`、`Pending Reviews And Gates`、worktree 字段、已批准工件和受影响验证证据都可回读
- 当前变化已经稳定到足以结构化，而不是仍停留在模糊意图或口头方向
- route / stage / worktree / evidence 之间没有明显冲突，不会一边做 increment 分析一边继续漂移

若不满足，不继续补脑产出完整影响矩阵，而是写出阻塞原因和唯一下一步：

- 更像实现缺陷：`hf-hotfix`
- 变化仍需重新收敛需求表达：`hf-specify`
- route / stage / profile / worktree 仍不清：`hf-workflow-router`

### 2. 形成结构化变更包与影响矩阵

把本次变化整理成至少以下结构：

- `New`
- `Modified`
- `Deprecated`

然后评估对以下内容的影响：

- 范围与需求
- 约束或验收标准
- 架构或接口
- 任务顺序与依赖
- 测试与验证策略
- 已完成实现

同时显式写出：

- 受影响工件
- 失效的批准状态
- 失效的任务 / `Current Active Task`
- 失效的测试设计 / 验证证据 / review 结论
- 是否出现 profile 升级信号

如果当前变化仍然太含糊，无法稳定写成 `New / Modified / Deprecated`，不要补脑继续：

- 若 blocker 是“本质上这是实现缺陷修复，而不是需求变更”，下一步交回 `hf-hotfix`
- 若 blocker 是 route / stage / profile 不清，下一步交回 `hf-workflow-router`
- 若 profile 与当前阶段仍然清楚，但变化本身需要重新收敛需求表达，下一步交回 `hf-specify`

### 3. 更新最小必要工件

规则如下：

- 需求变化先落到需求规格
- 只有当需求变化影响“如何实现”时，才继续更新设计
- 只有当设计或范围变化影响执行时，才更新任务计划
- 当行为结论或风险边界变化时，要同步更新验证策略与完成依据
- 如果用户可见结果或项目状态受影响，也要同步更新发布说明和进度记录

若某个 review 结论因本次变更失效，不要只写“需要重审”；应写出对应 canonical review 节点，例如：

- `hf-spec-review`
- `hf-design-review`
- `hf-tasks-review`
- `hf-test-review`
- `hf-code-review`
- `hf-traceability-review`

### 4. 决定唯一 re-entry 节点

下一步规则：

- 变化仍然含糊，需要重新收敛需求：`hf-specify`
- 当前判断其实是实现缺陷修复：`hf-hotfix`
- 规格发生实质变化，需要重新产出规格：`hf-specify`
- 规格已同步完成，且下一步是重新规格评审：`hf-spec-review`
- 设计变化过大，不适合在 increment 中就地同步：`hf-design`
- 设计已同步完成，且下一步是重新设计评审：`hf-design-review`
- 任务计划、活动任务、测试设计种子或验证依据需要重新收敛：`hf-tasks`
- 工件已保持一致、批准仍然有效、当前活动任务仍可执行，且可以继续实现：`hf-test-driven-dev`
- 若 route / stage / profile 仍不清，或需要重新决定分支：`hf-workflow-router`

如果同时有多个失效 review 需要重派发，则：

- 将最早应恢复的 canonical 节点写入 `Next Action Or Recommended Skill`
- 其余节点继续写入 `Pending Reviews And Gates`

### 5. 写回状态与回流说明

变更影响分析完成后，默认应把本次记录同步到项目变更记录；若项目级约定无项目覆写，可至少落到：

- `features/<active>/reviews/increment-<topic>.md`
- feature `progress.md`（默认 `features/<active>/progress.md`）
- 相关规格 / 设计 / 任务工件（默认 `features/<active>/spec.md` / `design.md` / `tasks.md`）

模板优先使用 `references/change-impact-sync-record-template.md`；若项目级约定为当前项目声明了等价模板路径，优先遵循。

至少同步：

1. `Current Stage`
2. `Workflow Profile`（如出现升级信号）
3. `Current Active Task`：仅在原任务仍然有效时保留；若已失效则清空或写 `pending reselection`
4. `Pending Reviews And Gates`
5. 唯一 canonical `Next Action Or Recommended Skill`

若当前 workflow 已存在 `worktree-active`，或上游已将后续实现标记为 `worktree-required`，不要在 increment 状态同步中把这些字段静默清空。

若 `Next Action Or Recommended Skill` 指向 review 节点，其含义是父会话或 `hf-workflow-router` 会按 review dispatch protocol 派发 reviewer subagent，而不是当前 increment 会话直接内联继续评审。

## Output Contract

变更记录正文请严格使用以下结构：

```markdown
## 变更摘要

- 变更摘要
- 当前判断：真实 increment | 更像 hotfix | 仍需进一步规格化 | blocked
- 当前 workflow profile / 当前阶段

## 基线快照

- `Workflow Profile`
- `Current Stage`
- `Current Active Task`
- `Pending Reviews And Gates`
- `Worktree Path`
- `Worktree Branch`

## 变更包

- New
- Modified
- Deprecated

## 影响矩阵

- 受影响工件
- 失效的批准状态
- 失效的任务 / Active Task
- 失效的测试设计 / 验证证据 / review 结论
- 需重新派发的 reviewer / review 节点（如有）
- Profile 升级信号（如有）

## 同步更新项

- 更新项
- 明确不做的内容

## 待同步项

- 工件
- 原因 / 建议动作

## 状态回流

- `Current Stage`
- `Workflow Profile`
- `Current Active Task`（保留原值或写 `pending reselection`）
- `Pending Reviews And Gates`
- `Next Action Or Recommended Skill`: `hf-specify` | `hf-hotfix` | `hf-spec-review` | `hf-design` | `hf-design-review` | `hf-tasks` | `hf-test-driven-dev` | `hf-workflow-router`
```

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-hotfix` | 处理已上线功能的缺陷修复（复现→根因→最小修复）；本 skill 处理需求/范围/验收变更 |
| `hf-test-driven-dev` | 写/修代码、TDD 实现；本 skill 只做变更分析和工件同步，不直接推进实现 |
| `hf-workflow-router` | 编排/路由/阶段判断；本 skill 只处理已明确判定为 increment 的变更分支 |
| `hf-specify` | 写/改规格；本 skill 判断变更影响并决定回流到哪个 canonical 节点 |

## Red Flags

- 把需求变更误当成单纯任务调整
- 把实现缺陷误判成 increment，导致错分支
- 范围实质变化后仍假定旧批准有效
- 不显式标记失效的批准、任务或验证证据
- 没有完成影响分析，就提前回到实现阶段
- `Next Action Or Recommended Skill` 写成自由文本或自然语言阶段名

## Verification

只有在以下两种情况之一成立时，这个 skill 才算完成：

- [ ] 已形成稳定的变更包，受影响工件与失效项已被同步或显式标记，并写回唯一 canonical `Next Action Or Recommended Skill`
- [ ] 已明确记录“当前变化仍不足以稳定结构化或已判断为错分支”的阻塞 / 重分类状态、最小必要影响记录与唯一下一步（`hf-specify`、`hf-hotfix` 或 `hf-workflow-router`），且没有伪造更下游的 re-entry handoff

无论属于哪种完成路径，还应满足：

- [ ] 当前基线快照已固定，后续会话可回读 profile / stage / active task / worktree 语义
- [ ] `Current Stage`、`Workflow Profile`、`Current Active Task` 与 `Pending Reviews And Gates` 已按需要同步
- [ ] 若存在多个失效 review / gate，唯一最早节点已写入 `Next Action Or Recommended Skill`，其余已保留在 `Pending Reviews And Gates`
- [ ] 当前结论已经足以让父会话恢复到正确主链节点，而不是继续补脑推进

# 路由证据指南

当项目已采用这套 skills 作业体系，但尚未统一工件布局或路由证据时，可使用本指南。

本指南回答 3 个问题：

1. 路由时优先看什么。
2. 什么证据算有效，什么证据不够。
3. 当证据冲突时，应该保守地退回到哪里。

## 推荐工件布局

除非项目已有已批准的等价路径，否则默认使用以下布局（与 `workflow-shared-conventions.md` 的 *Default 逻辑工件布局* 对齐）：

| 逻辑工件 | 推荐路径 | 说明 |
|---|---|---|
| feature 入口 | `features/<active>/README.md` | 单 feature 状态总览，路由时第一时间读 |
| 需求规格 | `features/<active>/spec.md` | 定义做什么 |
| 设计文档 | `features/<active>/design.md` | 定义怎么做 |
| 任务计划 | `features/<active>/tasks.md` | 定义执行顺序 |
| 进度记录 | `features/<active>/progress.md` | 支撑跨会话连续推进；仓库根不再保留全局 progress 文件 |
| 评审记录 | `features/<active>/reviews/<kind>-<scope>-YYYY-MM-DD.md` | 可选但建议提供 |
| approval 记录 | `features/<active>/approvals/<kind>-<scope>-YYYY-MM-DD.md` | `interactive` / `auto` 下的 approval 证据 |
| 验证记录 | `features/<active>/verification/<kind>-<scope>-YYYY-MM-DD.md` | 可选但建议提供 |
| closeout pack | `features/<active>/closeout.md` | finalize 之后必需 |
| 发布说明 | `docs/release-notes/vX.Y.Z.md` + `CHANGELOG.md` | 面向用户的变更说明 |
| ADR pool | `docs/adr/NNNN-<slug>.md` | 仓库级长期资产，design 阶段直接落 |
| 顶层导航 | `docs/index.md` | 列当前 active feature / 最近 closeout |

## 最小路由证据

优先使用项目已有工件，不要额外依赖根目录 JSON 信号文件。

推荐的路由证据包括（**read-on-presence**：`docs/` 下的可选载体缺失视为该资产档位未启用，不阻塞路由）：

- 顶层导航中标注的当前 active feature：档 0/1 读仓库根 `README.md`；档 2 读 `docs/index.md`。两者都缺失时，回退到扫 `features/` 下最新的、未含 `closeout.md` 的目录
- 当前 active feature 目录下的 `README.md` 与 `progress.md`（若存在 `Workspace Isolation` / `Worktree Path` / `Worktree Branch`，也应一并读取）
- 当前 active feature 目录下的 `spec.md` / `design.md` / `tasks.md` 的存在情况与批准状态
- `features/<active>/reviews/` 下的评审记录
- `features/<active>/approvals/` 下的 approval 记录
- `features/<active>/verification/` 下的验证记录
- `features/<active>/closeout.md`（如已存在，意味着 feature 已 closeout）
- 用户明确提出的变更请求或热修复请求

## 路由时的证据优先级

在会话开始时，`hf-workflow-router` 应按以下顺序判断：

1. 项目级 `hf-workflow` 映射与审批约定（若项目已声明）
2. 顶层导航：`docs/index.md`（档 2，若存在）→ 仓库根 `README.md`（档 0/1）→ 扫 `features/` 兜底
3. `features/<active>/README.md` 与 `progress.md`
4. `features/<active>/spec.md` / `design.md` / `tasks.md` 的存在情况与批准状态
5. `features/<active>/reviews/`
6. `features/<active>/approvals/`
7. `features/<active>/verification/`
8. `features/<active>/closeout.md`（如存在）
9. release notes：`docs/release-notes/`（档 2，若存在）→ 仓库根 `CHANGELOG.md`（档 0 起）
10. 用户当前请求

若较高优先级工件与较低优先级工件冲突，应优先相信更基础、更上游的工件状态。

## 推荐路由输入

在会话开始时，`hf-workflow-router` 应优先只检查：

1. 项目级 `hf-workflow` 配置（若项目已声明）
2. 规格 / 设计 / 任务工件的存在情况和批准状态
3. 进度、评审和验证记录
   - 若当前 workflow 已使用 worktree，还要读取 `Workspace Isolation` / `Worktree Path` / `Worktree Branch`
4. 用户当前请求

在完成阶段路由前，避免大范围代码探索。

## 哪些证据不够

以下情况默认不能视为已批准或可继续下游：

- 聊天里说“这个已经确认过了”，但工件中没有对应证据
- 只存在草稿文档，没有状态字段或批准记录
- review 结论是 `通过`，但没有 approval step 完成证据
- feature `progress.md` 写着“继续实现”，但 `spec.md` / `design.md` / `tasks.md` 没有批准证据
- 只凭 `docs/release-notes/` 或 `CHANGELOG.md` 或零散提交信息推断阶段已经结束
- 因为 `docs/index.md` 缺失就阻塞路由（档 0/1 时应回退到仓库根 `README.md`；都没有时回退到扫 `features/`）
- 因为 `docs/runbooks/` / `docs/slo/` 等档 2 目录缺失就阻塞路由（这些目录未启用是合法状态）

## 批准信号

优先寻找显式批准标记，例如：

- 若 项目已声明 verdict 别名，优先采用其中的 approved / pass / revise / blocked 映射
- `状态: 已批准`
- 兼容旧写法：`Status: Approved`
- 带有 `通过` 结论的评审章节
- 兼容旧写法：带有 `PASS` 结论的评审章节
- 进度或验证记录中的阶段标记

对规格和设计而言，仅有评审通过还不够；还应能看出 approval step 已经完成。

approval step 的等价证据可以是：

- `interactive` 模式下的真人确认记录
- `auto` 模式下基于 review record 写入的 approval record

如果批准状态不明确，应回路由到上游评审 skill，而不是直接假设已批准。

补充判断：

- 规格评审通过但缺少 approval step，不算已批准，应继续按需求阶段处理
- 设计评审通过但缺少 approval step，不算已批准，应继续按设计阶段处理
- 任务评审通过但缺少 approval step，不算已批准，应继续按任务阶段处理

## 证据冲突时的保守规则

出现以下冲突时，采用保守处理：

- feature `progress.md` 显示“进入实现”，但任务计划没有批准证据
- 评审记录显示 `通过`，但工件状态仍是草稿
- 用户说“继续编码”，但更上游工件仍未批准

保守处理原则：

1. 不选择更激进的下游阶段
2. 回到更上游、证据更完整的阶段
3. 在路由输出中显式说明冲突点和处理方式

## review-only 场景的证据示例

- 用户明确要求“只做规格评审”：
  - 需求规格草稿存在
  - 当前 workflow profile 为 `full`，或当前证据要求先升级到 `full`
  - 当前请求仅要求 review
  - 路由到 `hf-spec-review`（若当前不是 `full`，先升级后重编排）
- 用户明确要求“只做设计评审”：
  - 设计草稿存在
  - 当前 workflow profile 为 `full`，或当前证据要求先升级到 `full`
  - 当前请求仅要求 review
  - 路由到 `hf-design-review`（若当前不是 `full`，先升级后重编排）
- 用户明确要求“只做任务评审”：
  - 任务计划草稿存在
  - 当前请求仅要求 review
  - 路由到 `hf-tasks-review`

## 变更 / 热修场景的证据示例

- increment：
  - 用户明确提出新增、删改需求
  - 或现有工件表明范围 / 验收标准变化
  - 路由到 `hf-increment`
- hotfix：
  - 用户明确提出紧急缺陷修复
  - 或验证结果表明已有线上 / 交付前缺陷
  - 路由到 `hf-hotfix`

## 主链流程

```text
hf-workflow-router
-> hf-specify
-> hf-spec-review
-> 规格真人确认
-> hf-design
-> hf-design-review
-> 设计真人确认
-> hf-tasks
-> hf-tasks-review
-> 任务真人确认
-> hf-test-driven-dev
-> hf-test-review
-> hf-code-review
-> hf-traceability-review
-> hf-regression-gate
-> hf-completion-gate
-> hf-finalize
```

## 支线流程

- 明确的变更请求 -> `hf-increment`
- 明确的热修复请求 -> `hf-hotfix`

两条支线都必须把项目带回正确的评审或实现阶段，不能绕过主链纪律。

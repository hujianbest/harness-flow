---
name: hf-subagent-driven-dev
description: 适用于已批准 task plan 中单一活跃任务可被完整封装给 fresh implementer subagent 的实现场景。不适用于任务强耦合、缺少可读上下文、需并行多任务、或 reviewer/gate verdict 可被跳过的场景。
---

# HF Subagent-Driven Development

HF 的可选实现 leaf：父会话保持 controller 角色，把一个已锁定 `Current Active Task` 封装给 `hf-implementer` 执行，并在实现完成后派发 `hf-reviewer` 进入既有 HF review/gate 链。它不替代 `hf-test-driven-dev` 的 TDD 纪律，也不改变 Fagan review、gate、approval 或 closeout 的 verdict 责任。

## Methodology

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **Fresh Subagent Per Task** | 每个实现任务使用干净上下文，避免父会话污染实现判断 | Superpowers subagent-driven development pattern | 步骤 3 |
| **Named Role Contracts** | 只定义 `hf-implementer` 与 `hf-reviewer` 两个 subagent role，避免泛化成 team mode | `references/agent-role-contracts.md` | 步骤 2-6 |
| **Controller / Worker Separation** | 父会话只负责编排、补上下文、消费状态；实现由 `hf-implementer` 完成 | 项目化实践（role separation） | 步骤 1-6 |
| **TDD Delegation** | `hf-implementer` 必须使用 `hf-test-driven-dev` 完成 task 实现 | `hf-test-driven-dev` | 步骤 2-5 |
| **Status-Driven Recovery** | `hf-implementer` 返回结构化状态，父会话按状态补上下文、升级模型、拆任务或停下 | Superpowers implementer status contract | 步骤 4 |

## When to Use

适用：
- 已有批准的 spec / design / tasks，且 router 已唯一锁定 `Current Active Task`
- 当前任务文本、上下文路径、DoD、测试种子和边界能完整写进 dispatch prompt
- 任务大到值得隔离上下文，但仍是一个单 task 的垂直切片
- 父会话需要保持低上下文占用，只做 orchestration

不适用：
- 上游工件未批准或 route/profile 仍不清 → `hf-workflow-router`
- 当前任务与其它未完成任务强耦合，无法给出完整单 task 边界 → `hf-test-driven-dev`
- `hf-implementer` 要并行处理多个任务 → 回 `hf-workflow-router` 重新切任务
- 用户要求 review/gate skip、作者自审、或跳过 RED/GREEN evidence → 停下并回对应 review/gate
- hotfix 无复现路径 → `hf-hotfix`

## Hard Gates

- 只允许一个 `Current Active Task`；不得并行派发多个 `hf-implementer` 写代码。
- 父会话必须提供完整 task text 与最小必要上下文；不得让 subagent 自行从大型 plan 中猜任务边界。
- `hf-implementer` 必须使用 `hf-test-driven-dev` 的测试设计、RED/GREEN、Two Hats、Refactor Note、wisdom delta 与 `tasks.progress.json` 规则完成实现。
- `hf-implementer` 的 self-review 不能替代 `hf-reviewer` 执行的 `hf-test-review`、`hf-code-review`、`hf-traceability-review` 或任何 gate verdict。
- `hf-implementer` 返回 `NEEDS_CONTEXT` / `BLOCKED` 时，父会话必须改变输入、拆任务、升级 route 或停下；不得原样重试。
- `DONE_WITH_CONCERNS` 的 concerns 必须先分类处理；范围、正确性或 evidence concerns 未处理前不得进入 review 链。
- `hf-reviewer` 只执行独立 review；不得编辑实现代码、不得替 gate 下 verdict、不得推进 workflow 而不返回 reviewer contract。

## Object Contract

- **Primary Object**: 单一 active task 的 subagent implementation attempt。
- **Frontend Input Object**: router handoff + approved task text + spec/design/tasks anchors + worktree context + wisdom summary。
- **Backend Output Object**: `hf-implementer` return summary + 实现交接块 + fresh evidence anchors + `hf-reviewer` review records + canonical next action。
- **Object Transformation**: 父会话把 approved task 封装成 bounded prompt；`hf-implementer` 在隔离上下文中用 `hf-test-driven-dev` 完成 TDD；`hf-reviewer` 独立评审；父会话按状态推进或回修。
- **Object Boundaries**: 本 skill 不写 review/gate verdict，不选择下一任务，不修改上游 spec/design/tasks，不替代 `hf-ultrawork` 的 fast-lane audit。
- **Object Invariants**: task ID 不变；worktree path 不变；review/gate 链不被压缩；所有完成声明必须可从仓库工件恢复。

## Workflow

### 1. 确认 subagent eligibility

读 router handoff、feature `progress.md`、当前 task plan 条目、worktree 状态与 wisdom summary。若 active task 不唯一、task text 不完整、上下文路径不可读、或工作区隔离未准备，回 `hf-workflow-router` 或 `hf-test-driven-dev`。

### 2. 构造 `hf-implementer` dispatch request

父会话写出最小 request，不传聊天历史。必须包含：

- task ID、完整任务文本、DoD / acceptance、测试种子
- spec / design / tasks / prior findings / wisdom summary 的最小路径
- Workspace Isolation、Worktree Path、Worktree Branch
- 明确角色：`agent_role = hf-implementer`
- 必须加载并遵守 `hf-test-driven-dev` 的 TDD、fresh evidence、Two Hats 与 Refactor Note 规则
- 期望返回状态：`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`

### 3. 派发 fresh `hf-implementer`

`hf-implementer` 在给定 worktree 中通过 `hf-test-driven-dev` 实现、测试、提交或准备可提交 diff，并写实现交接块。它可以提问；父会话必须回答后用更新后的 request 重新派发，而不是让它猜。

### 4. 消费 `hf-implementer` status

按 `references/implementer-return-contract.md` 处理：

- `DONE`：读取 evidence anchors，进入步骤 5
- `DONE_WITH_CONCERNS`：先判断 concern 是否影响 scope / correctness / evidence；影响则补上下文或回修，不影响才进入步骤 5
- `NEEDS_CONTEXT`：补充缺失上下文并重新派发
- `BLOCKED`：若是上下文缺口则补上下文；若任务过大则回 `hf-workflow-router` 拆任务；若计划错误则回 `hf-increment` 或上游

### 5. 同步实现交接与状态

确认实现交接块包含 RED/GREEN evidence、Refactor Note、wisdom delta、`tasks.progress.json` 更新、changed artifacts、remaining risk、pending reviews/gates 与 canonical next action。缺任一项则回 `hf-implementer` 修订。

### 6. 派发 `hf-reviewer` 并回到 HF review/gate 链

full/standard profile 通常派发 `hf-reviewer` 执行 `hf-test-review`，再按 verdict 进入 `hf-code-review` 与 `hf-traceability-review`。lightweight profile 通常进入 `hf-regression-gate`，但任何 review 节点仍由 `hf-reviewer` 执行对应 `hf-*review` skill。若触碰 runtime surface，仍由 router 判定是否插入 `hf-browser-testing`。后续 gate 均按既有 gate contract 执行。

## Output Contract

| 输出 | 默认位置 / 形式 | 要求 |
|---|---|---|
| `hf-implementer` return summary | 父会话消费的结构化摘要 | role、状态、changed artifacts、evidence anchors、concerns/blockers |
| 实现交接块 | `features/<active>/summaries/task-<TASK-ID>.md` 或项目等价路径 | 与 `hf-test-driven-dev` 交接块字段兼容 |
| `hf-reviewer` return summary | reviewer return contract | conclusion、record_path、next action、reroute flag |
| task step state | `features/<active>/tasks.progress.json` | current_step 最终可恢复到 `DONE` 或明确 blocked step |
| wisdom delta | `features/<active>/notepads/` + `progress.md` `## Wisdom Delta` | 遵守 `hf-wisdom-notebook` schema |

## Red Flags

- 派发多个 `hf-implementer` 同时修改代码
- 让 `hf-implementer` 自己读完整 plan 并挑任务
- `hf-implementer` 说 `BLOCKED` 后原样重试
- `DONE_WITH_CONCERNS` 未处理就进入 review
- `hf-implementer` self-review 被当成 `hf-reviewer` verdict
- `hf-reviewer` 修改代码或替 gate verdict
- 缺 RED/GREEN fresh evidence 仍标记完成
- task 完成后直接切下一任务，绕过 completion gate / router

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/agent-role-contracts.md` | `hf-implementer` / `hf-reviewer` 两个 subagent role 的职责、边界与父会话 enforcement |
| `references/implementer-return-contract.md` | implementer subagent 返回摘要字段、状态语义与父会话消费规则 |
| `../hf-test-driven-dev/SKILL.md` | TDD、Refactor Note、fresh evidence、wisdom delta 与 task progress 规则 |
| `../hf-workflow-router/references/review-dispatch-protocol.md` | 后续 review 节点的 independent reviewer dispatch 规则 |

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "`hf-implementer` 已经 self-review 了，可以跳过 `hf-reviewer`。" | Hard Gates: implementer self-review 不是 Fagan review；仍必须由 `hf-reviewer` 执行 `hf-test-review` / `hf-code-review` / `hf-traceability-review` 或 profile 对应 review。 |
| "任务都在同一个 plan 里，派几个 `hf-implementer` 并行更快。" | Hard Gates: HF 一次只有一个 `Current Active Task`；并行实现会破坏 task 边界与 evidence recovery。 |
| "`hf-implementer` 说缺上下文，但我可以让它先猜。" | Status-driven recovery: `NEEDS_CONTEXT` 必须补上下文后重派；猜测会污染实现与验收边界。 |
| "DONE_WITH_CONCERNS 只是客套，可以忽略。" | Workflow stop rule: correctness / scope / evidence concern 未分类处理前不得进入 review 链。 |
| "`hf-reviewer` 顺手把问题修了更快。" | Role boundary: `hf-reviewer` 只评审并写 record；修复必须回 `hf-implementer` 或 router。 |

## Verification

- [ ] 当前只有一个 `Current Active Task`
- [ ] task text、DoD、测试种子与上下文路径已完整写入 dispatch request
- [ ] `hf-implementer` 使用 fresh context，未继承父会话历史
- [ ] `hf-implementer` 已明确加载并遵守 `hf-test-driven-dev`
- [ ] `hf-implementer` status 已按 return contract 消费
- [ ] RED/GREEN evidence、Refactor Note、wisdom delta、`tasks.progress.json` 均已同步
- [ ] `hf-reviewer` 已执行对应 review skill，未把 self-review 当成 review/gate verdict
- [ ] canonical next action 回到既有 HF review/gate 链

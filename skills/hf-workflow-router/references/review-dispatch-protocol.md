# Review Dispatch Protocol

## 目的

这份协议说明 `hf-workflow-router` 与各上游产出 skill 在遇到 review 节点时，如何把评审动作派发给独立 reviewer subagent，而不是在父会话里内联执行 review。

## 核心原则

1. review 节点仍然是 workflow 的 canonical 节点。
2. 进入 review 节点时，父会话不直接执行评审判断。
3. 父会话要构造 review request，并启动独立 reviewer subagent。
4. reviewer subagent 在 fresh context 中读取对应 `hf-*review` skill 与最小必要工件。
5. reviewer subagent 负责写 review 记录并回传结构化摘要。
6. 父会话消费该摘要，继续主链推进或进入 approval step。

其中 reviewer 摘要里的 canonical handoff 字段应与 family vocabulary 对齐，统一使用 `next_action_or_recommended_skill`。

## 当前适用节点

| Canonical review 节点 | reviewer subagent 调用的 skill |
| --- | --- |
| `hf-spec-review` | `hf-spec-review` |
| `hf-design-review` | `hf-design-review` |
| `hf-ui-review` | `hf-ui-review`（仅当规格声明 UI surface 且 `hf-ui-design` 已产出草稿时） |
| `hf-tasks-review` | `hf-tasks-review` |
| `hf-test-review` | `hf-test-review` |
| `hf-code-review` | `hf-code-review` |
| `hf-traceability-review` | `hf-traceability-review` |

## review request 最小字段

建议父会话至少构造以下字段：

```json
{
  "review_type": "spec|design|ui|tasks|test|code|traceability",
  "review_skill": "hf-xxx-review",
  "topic": "本次评审主题",
  "artifact_paths": [
    "被检视交付件路径"
  ],
  "supporting_context_paths": [
    "最小必要辅助上下文路径"
  ],
  "workspace_isolation": "in-place|worktree-required|worktree-active",
  "worktree_path": "当前候选实现所在 worktree 根路径（若存在）",
  "worktree_branch": "当前候选实现分支（若存在）",
  "expected_record_path": "docs/reviews/... 或项目映射路径",
  "current_profile": "full|standard|lightweight",
  "design_execution_mode": "parallel|architecture-first|ui-first"
}
```

当 `review_type=ui` 时，`supporting_context_paths` 至少包含对应 `hf-design` 最新草稿路径，便于 reviewer 比对 peer 交接块一致性。

## 父会话职责

父会话负责：

- 判断当前是否应进入 review 节点
- 选择正确的 review skill
- 组装最小 review request
- 若当前 `Workspace Isolation=worktree-active`，把 `Worktree Path` / `Worktree Branch` 明确带入 review request
- 启动 reviewer subagent
- 消费 reviewer 返回摘要
- 在需要时发起 approval step，或在 `Execution Mode=auto` 下自动落盘批准
- 根据摘要继续推进或回流修订

父会话在消费 reviewer 摘要时，应直接读取 `next_action_or_recommended_skill` 并进入迁移判断。

父会话不负责：

- 在当前上下文直接执行 review 判断
- 代替 reviewer 写 review 记录

## reviewer subagent 职责

reviewer subagent 负责：

- 读取对应 `hf-*review` skill
- 读取 review request 指定的最小必要工件
- 若 review request 提供 `worktree_path`，在该 worktree 视角下读取候选实现，而不是退回仓库根目录读取另一份状态
- 按 skill 要求执行评审
- 把评审记录写到约定路径
- 按统一 return contract 回传摘要

reviewer subagent 不负责：

- 推进整个 workflow 到下一主链节点
- 代替父会话做 approval step 决策或落盘

## Approval Step 归属

以下场景中，reviewer 只返回“已经达到可确认状态”，approval step 仍由父会话执行：

- `hf-spec-review`
- `hf-design-review`
- `hf-ui-review`
- `hf-tasks-review`

处理约束：

- `interactive`：父会话等待用户确认
- `auto`：父会话按 policy 写 approval record 后继续推进

**联合 design approval 特殊规则**：当规格含 UI surface、`hf-design-review` 与 `hf-ui-review` 都被激活时，父会话只有在两条 review 均返回 `通过` 后才发起 `设计真人确认`；任一 `通过` 单独到达时，结论暂存，等待另一条汇合。任一返回 `需修改` / `阻塞` 时，对应起草 skill 回修，另一条 skill 的稳定部分保留。

## 失败与重编排

如果 reviewer 发现当前问题不是简单回修，而是：

- 缺少上游已批准工件
- 当前 profile 不再成立
- 当前 review 输入与 workflow 状态冲突

则 reviewer 应在返回摘要中明确要求父会话经 `hf-workflow-router` 重编排，而不是让下游 skill 自行补位推进。

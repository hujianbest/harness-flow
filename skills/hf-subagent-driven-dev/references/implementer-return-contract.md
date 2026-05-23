# Implementer Return Contract

## Purpose

本文件定义 `hf-subagent-driven-dev` 派发的 `hf-implementer` 返回给父会话的最小结构化摘要。它只描述实现尝试的状态，不替代 `hf-reviewer` 或 gate verdict。

## Minimal return format

```json
{
  "agent_role": "hf-implementer",
  "status": "DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED",
  "task_id": "TASK-001",
  "changed_artifacts": ["path/to/file"],
  "evidence_anchors": ["command or artifact path"],
  "handoff_path": "features/<active>/summaries/task-TASK-001.md",
  "concerns": ["optional concern"],
  "blockers": ["optional blocker"],
  "next_action_or_recommended_skill": "hf-test-review"
}
```

## Status vocabulary

| status | Meaning | Parent action |
|---|---|---|
| `DONE` | Implementation, tests, handoff, wisdom delta, and task progress sync are complete | Validate anchors, then enter the normal HF review/gate chain |
| `DONE_WITH_CONCERNS` | Work is complete, but implementer flags doubts or residual risk | Classify concerns before review; scope/correctness/evidence concerns must be resolved first |
| `NEEDS_CONTEXT` | Implementer cannot proceed without specific missing context | Provide the missing context and re-dispatch with an updated request |
| `BLOCKED` | Implementer cannot complete the task under current plan/input | Change something: add context, use a more capable agent, split the task, reroute, or escalate |

## Field rules

- `status` must be one of the four values above.
- `agent_role` must be `hf-implementer`.
- `task_id` must match the current `Current Active Task`.
- `changed_artifacts` lists touched files or generated workflow artifacts; it is not a review finding list.
- `evidence_anchors` must point to fresh RED/GREEN commands, logs, or verification artifacts.
- `handoff_path` must point to the implementation handoff or task summary that downstream review can read.
- `next_action_or_recommended_skill` must use the shared canonical vocabulary.
- `concerns` is required for `DONE_WITH_CONCERNS`.
- `blockers` is required for `BLOCKED`.

## Parent consumption order

1. Verify `task_id` matches the active task and worktree context.
2. Check `status`.
3. For `DONE`, verify evidence anchors and handoff completeness before dispatching `hf-reviewer` or entering the next HF node.
4. For `DONE_WITH_CONCERNS`, classify every concern:
   - scope/correctness/evidence concern: resolve or re-dispatch before review
   - advisory observation: record in remaining risk, then continue
5. For `NEEDS_CONTEXT`, provide the missing context and re-dispatch; do not ask the implementer to guess.
6. For `BLOCKED`, decide whether to add context, upgrade model, split task, route to `hf-increment`, or return to `hf-workflow-router`.

## Boundary

This contract is not a reviewer return contract. It does not use `conclusion`, does not write `record_path`, and does not authorize approval, completion, or closeout. `hf-reviewer` remains responsible for review records through the normal reviewer return contract.

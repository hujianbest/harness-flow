# Task Board

使用说明：

- 这是 `hf` 中用于 task-to-task 自动推进的可选 coordination artifact 模板。
- 它应与已批准任务计划和 feature 范围内的 `progress.md` 配合使用；任务计划负责定义任务拓扑、依赖与完成条件，task board 负责投影当前队列状态。
- **默认保存路径：`features/<NNN>-<slug>/task-board.md`**，并在 `features/<NNN>-<slug>/progress.md` 中通过 `Task Board Path` 显式引用。
- `Current Active Task` 仍以 feature 的 `progress.md` 为权威；task board 中最多只应有一个 `in_progress` 任务，并且它应与 `Current Active Task` 保持一致。
- 若 task board 与已批准任务计划冲突，或无法唯一判断 `next-ready task`，应停止自动推进并回到 `hf-workflow-router`。

## Metadata

- Topic:
- Source Task Plan:
- Board Path:
- Owner:
- Last Updated:
- Board Mode: `artifact-first + board-assisted`

## Selection Rules

- Current Active Task:
- Selection Rule:
  - 选择依赖已满足、状态为 `ready` 的唯一最高优先级任务
- Conflict Policy:
  - 若存在多个同等候选，或依赖 / 状态冲突，则回到 `hf-workflow-router`
- Ready Semantics:
- Done Semantics:

## Status Vocabulary

- `pending`: 前置依赖或 ready 条件尚未满足
- `ready`: 可被 router 锁定为下一任务
- `in_progress`: 已被锁定为当前唯一活跃任务
- `done`: 当前任务已完成实现质量链，并通过 `hf-completion-gate`
- `blocked`: 任务当前无法推进，需要外部条件或上游修订
- `cancelled`: 任务已失效、被改范围覆盖或不再执行

## Queue Snapshot

- Ready Tasks:
- Pending Tasks:
- Blocked Tasks:
- Done Tasks:
- Last Completion Record:
- Next Router Action:

## Task Queue

| Task ID | Title | Status | Depends On | Ready When | Selection Priority | Last Outcome / Record | Notes |
|---|---|---|---|---|---|---|---|
| T1 | <task title> | ready | - | <ready condition> | P1 | N/A | <notes> |
| T2 | <task title> | pending | T1 | T1=`done` | P2 | N/A | <notes> |

## State Change Log

- Date:
  - Change:
  - Evidence / Record:

## Notes

- Additional Notes:

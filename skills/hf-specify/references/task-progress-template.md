# Task Progress

使用说明：

- 这是 `hf` 中的通用任务进度模板。
- 适合记录当前目标、workflow 状态、证据和下一步；可与 `hf-*` workflow skills 配合使用（runtime 编排以 `hf-workflow-router` 为准）。
- **默认保存路径：`features/<NNN>-<slug>/progress.md`**（feature 周期内的唯一权威 progress 落点）。仓库根**不再保留全局 `task-progress.md`**；"当前 active feature 是哪个"由 `docs/index.md` 与 active feature 的 `progress.md` 共同表达。
- 优先使用下面的 canonical 字段名，不再把 `Current Task` / `Next Action` 当作主字段。
- 该模板定义的是 minimal canonical core；项目可按需追加附加工件区块，但不应改写核心字段名。
- 若 workflow 需要 task-to-task 自动推进，建议额外提供 `Task Board Path`（默认 `features/<NNN>-<slug>/task-board.md`）或等价队列投影视图；`Current Active Task` 只记录当前锁定任务，不承担整个任务队列状态。可配合 `hf-tasks` 的 `references/task-board-template.md` 使用。

## Goal

- Goal:
- Owner:
- Status:
- Last Updated:

## Current Workflow State

- Current Stage:
- Workflow Profile:
- Execution Mode:
- Current Active Feature:                  # 例：features/003-rate-limiting/
- Current Active Task:
- Pending Reviews And Gates:
- Relevant Files:
- Constraints:

## Progress Notes

- What Changed:
- Evidence Paths:                          # 例：features/<active>/evidence/...
- Session Log:
- Open Risks:

## Optional Coordination Fields

- Task Board Path:                         # 默认 features/<active>/task-board.md
- Task Queue Notes:
- Workspace Isolation:
- Worktree Path:
- Worktree Branch:

## Next Step

- Next Action Or Recommended Skill:
- Blockers:
- Notes:

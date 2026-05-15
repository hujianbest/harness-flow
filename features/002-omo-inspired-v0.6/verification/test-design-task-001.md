# Test Design — TASK-001 (tasks.progress.json schema)

- Task: TASK-001（定义 `tasks.progress.json` schema）
- SUT Form: **`emergent`**（schema 定义类任务，无需前置模式；refactor 阶段按需 emerge）
- Test Strategy: stdlib python validator + positive/negative fixtures + structural assertions

## 待验证行为

1. `skills/hf-test-driven-dev/references/tasks-progress-schema.md` 文件存在
2. 文件内含有效 JSON Schema fenced block（解析为合法 JSON）
3. canonical 正例 fixture（典型 in-progress task）通过 schema 校验
4. 至少 3 个负例 fixture（缺 `current_task` / 非法 `current_step` / 缺 `step_history` 数组）必须 reject

## 测试分层

- 单一脚本 `tests/test_tasks_progress_schema.py`（stdlib only：`json` + `unittest`）；不接入更大 test framework（与 `audit-skill-anatomy.py` / `validate-wisdom-notebook.py` 同等地位）

## 预期 I/O

| Test | Input fixture | 预期 |
|---|---|---|
| `test_schema_file_exists` | （无）| 文件存在 |
| `test_schema_block_is_valid_json` | schema doc 中的 fenced JSON block | `json.loads` 不抛异常 |
| `test_positive_in_progress_task` | `fixtures/positive-in-progress.json` | validator returns OK |
| `test_negative_missing_current_task` | `fixtures/negative-missing-current-task.json` | validator returns FAIL |
| `test_negative_invalid_step_format` | `fixtures/negative-invalid-step.json` | validator returns FAIL |
| `test_negative_step_history_not_array` | `fixtures/negative-step-history-not-array.json` | validator returns FAIL |

## 与 design.md §4.3 一致性

design §4.3 提及 `tasks.progress.json` 的 step-level recovery 用途；本 schema 必须含：
- `current_task`：string，task ID（如 `TASK-001`）
- `current_step`：string，TDD 步级（`RED-N` / `GREEN-N` / `REFACTOR-N` / `TEST-DESIGN` / `APPROVAL` / `DONE`）
- `last_updated`：ISO 8601 timestamp
- `step_history[]`：array of `{step, timestamp, outcome}`

## SUT Form 说明

`emergent`：本任务的"SUT"是 schema 文档 + validator，不需要承载任何战术模式或 GoF 模式。Refactor 阶段如发现 validator 内有重复逻辑，按 Fowler vocabulary 重构（Extract Function / Rename）。

## Approval

按 ADR-009 D2 fast lane，本测试设计在 architect explicit auto mode 下自动 approved，不停下抛回。

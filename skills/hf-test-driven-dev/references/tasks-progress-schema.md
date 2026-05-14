# `tasks.progress.json` Schema (v0.6 / TASK-001)

> Step-level progress recovery file written by `hf-test-driven-dev` per active task.
> Consumed by `hf-workflow-router` for step-level (intra-task) recovery; complements feature-level `progress.md` (which only tracks node-level transitions).

- Schema version: 1
- File location: `features/<active>/tasks.progress.json`
- Lifecycle: created when `hf-test-driven-dev` enters TEST-DESIGN for the active task; updated atomically (write-temp + rename) at every TDD step transition; archived (renamed to `tasks.progress.<task-id>.json`) when the task reaches `DONE`.
- Stdlib-only validators: `tests/test_tasks_progress_schema.py` (this repo) + the `tasks.progress.json` stanza of any future `hf-completion-gate` checks.
- Related: `hf-workflow-router/references/profile-node-and-transition-map.md` ("step-level recovery" section, added in TASK-011); `features/002-omo-inspired-v0.6/design.md` §4.3.

## Field summary

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | integer | yes | Always `1` for v0.6. Future schema bumps must be additive or guarded by version. |
| `current_task` | string | yes | Active task ID, e.g. `TASK-003`. Must match a task in the feature's approved `tasks.md`. |
| `current_step` | string (enum) | yes | Current TDD step. Allowed: `TEST-DESIGN` / `APPROVAL` / `RED-N` / `GREEN-N` / `REFACTOR-N` / `DONE` (N = positive integer). |
| `last_updated` | string (ISO 8601) | yes | UTC, second precision, suffix `Z`. |
| `step_history` | array of objects | yes | Append-only ordered log of step transitions for the active task. Empty array allowed at TEST-DESIGN entry. |
| `step_history[].step` | string (enum, same as `current_step`) | yes | The step that was *exited* by this entry. |
| `step_history[].timestamp` | string (ISO 8601) | yes | When the step exited. |
| `step_history[].outcome` | string (enum) | yes | One of: `approved` / `failed-as-expected` / `passed` / `refactored-clean` / `escalated` / `aborted`. |

## JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "harnessflow.tasks.progress.v1",
  "type": "object",
  "required": ["schema_version", "current_task", "current_step", "last_updated", "step_history"],
  "properties": {
    "schema_version": {"type": "integer", "enum": [1]},
    "current_task": {"type": "string", "pattern": "^TASK-[0-9]{3,}$"},
    "current_step": {
      "type": "string",
      "pattern": "^(TEST-DESIGN|APPROVAL|DONE|RED-[0-9]+|GREEN-[0-9]+|REFACTOR-[0-9]+)$"
    },
    "last_updated": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    },
    "step_history": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step", "timestamp", "outcome"],
        "properties": {
          "step": {
            "type": "string",
            "pattern": "^(TEST-DESIGN|APPROVAL|DONE|RED-[0-9]+|GREEN-[0-9]+|REFACTOR-[0-9]+)$"
          },
          "timestamp": {
            "type": "string",
            "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
          },
          "outcome": {
            "type": "string",
            "enum": ["approved", "failed-as-expected", "passed", "refactored-clean", "escalated", "aborted"]
          }
        }
      }
    }
  }
}
```

## Canonical positive example

See `tasks-progress-fixtures/positive-in-progress.json` (parsed and validated by `tests/test_tasks_progress_schema.py::test_positive_in_progress_validates`).

## Negative examples

`tasks-progress-fixtures/negative-*.json` — three rejection cases covering: missing `current_task`, invalid `current_step` value, and `step_history` not an array. Each is asserted by a dedicated test in `tests/test_tasks_progress_schema.py`.

## Atomic write protocol

1. Compute the new state in memory.
2. Serialize to `features/<active>/tasks.progress.json.tmp`.
3. `rename(tmp, final)` — atomic on POSIX.
4. Never partial-write the canonical file directly.

## Recovery semantics consumed by `hf-workflow-router`

When a session resumes, the router (per the `step-level recovery` rule, to be landed in TASK-011) reads `tasks.progress.json` and:

- If `current_step ∈ {RED-N, GREEN-N}` → resume `hf-test-driven-dev` at that step (no re-design).
- If `current_step == REFACTOR-N` → resume `hf-test-driven-dev` step 4A.
- If `current_step == APPROVAL` → resume by writing the approval record (auto mode) or asking the architect (standard mode).
- If `current_step == DONE` → archive file and let router pick the next active task.

Future v0.7 `harnessflow-runtime` may automate atomic writes via the `progress-store` tool (ADR-010 P0 module), but the schema must remain stable.

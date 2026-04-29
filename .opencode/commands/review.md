---
description: Use when an artifact (discovery, spec, design, UI design, tasks, tests, code, traceability) is ready for an independent review. Router resolves which hf-*-review to dispatch.
argument-hint: [artifact type or task id, e.g. "spec" / "TASK-003 code"]
---

# /review — bias toward `hf-*-review` (router decides which)

HarnessFlow keeps every review as an independent leaf with author/reviewer role separation (Fagan-style). `/review` is the user-facing handle; the router picks the actual review skill from artifact evidence.

## What HF should do

1. Pass `$ARGUMENTS` to `using-hf-workflow` with `command_bias=/review`.
2. Have `hf-workflow-router` pick the target review leaf from `$ARGUMENTS` shape and the latest fresh artifact:
   - "discovery" / discovery draft just produced → `hf-discovery-review`
   - "spec" / spec just drafted or revised → `hf-spec-review`
   - "design" / design draft just produced → `hf-design-review`
   - "ui" / "ui design" → `hf-ui-review`
   - "tasks" / "task plan" → `hf-tasks-review`
   - "test" / "tests" / "test design" of the active task → `hf-test-review`
   - "code" / "TASK-NNN code" → `hf-code-review`
   - "traceability" / cross-artifact zigzag check → `hf-traceability-review`
3. Dispatch the chosen review leaf as a subagent per `hf-workflow-router/references/review-dispatch-protocol.md` (do not inline reviews into the parent session).

## HF guardrails

- `/review` does **not** let HF act as both author and reviewer in the same session — that breaks `docs/principles/soul.md`'s "HF 不替用户验收自己" rule.
- `/review` does **not** synthesize a verdict from chat memory. The verdict comes from the review leaf, written to a review record on disk.
- If `$ARGUMENTS` is ambiguous and multiple review leaves could match, ask one minimal clarification question rather than picking arbitrarily.

User intent: $ARGUMENTS

---
description: Use when a unique current active task is selected and you want to implement it under HF's gated TDD discipline. Bias: hf-test-driven-dev.
argument-hint: [optional task id or focus]
---

# /build — bias toward `hf-test-driven-dev`

Implement the unique current active task under Canon TDD with fresh RED/GREEN evidence, Two Hats discipline, and Clean Architecture conformance.

## What HF should do

1. Pass `$ARGUMENTS` to `using-hf-workflow` with `command_bias=/build`.
2. Confirm preconditions before entering `hf-test-driven-dev`:
   - approved spec exists
   - approved design exists (and approved UI design if a UI surface was declared)
   - approved task plan exists
   - exactly one Current Active Task is selected
3. If any precondition is missing, fall back to `hf-workflow-router` — never let `/build` jump implementation ahead of upstream approvals.
4. Otherwise enter `hf-test-driven-dev`'s minimum kickoff: read the active task, its acceptance criteria, design conformance points, and existing tests; do not start writing code before test design exists.

## HF guardrails

- `/build` does **not** silently switch active task. If `$ARGUMENTS` references a different task id, surface the conflict to the architect and let the router decide.
- `/build` does **not** skip RED. If the implementation is going to land before a failing test exists, abort and reroute.
- `/build` does **not** trigger any review or gate node — that's the router's job after `hf-test-driven-dev` produces fresh evidence.

User intent: $ARGUMENTS

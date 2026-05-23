---
description: Implement the current active HarnessFlow task with TDD and fresh evidence (hf-test-driven-dev). Only valid when exactly one Current Active Task is locked.
---

Bias toward the HarnessFlow `hf-test-driven-dev` skill.

Steps:

1. Enter via `skills/using-hf-workflow/SKILL.md` and hand off to `skills/hf-workflow-router/SKILL.md`.
2. Tell the router that the user's intent is "implement the current active task".
3. The router checks preconditions:
   - exactly one `Current Active Task` is locked,
   - upstream design / tasks / approvals are in place,
   - no blocking gate is open against this task.
4. If preconditions hold, the router routes into `skills/hf-test-driven-dev/SKILL.md`.
5. If preconditions do not hold, the router routes back to the upstream node (e.g. `hf-tasks`, `hf-design-review`) instead of starting implementation.

Hard rules carried by `hf-test-driven-dev`:

- Canon TDD: write the test design first, RED must exist before GREEN.
- Walking Skeleton + Two Hats discipline; opportunistic / preparatory refactoring inside the same node.
- Fresh Evidence Principle: RED / GREEN evidence must be re-captured for the current run.
- Clean Architecture conformance check is part of the node, not deferred to review.

The user request following this command is optional implementation hint or scope reminder. The router does not need it to identify the active task.

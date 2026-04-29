---
description: Use when an approved spec needs to be turned into design and/or task plan. Covers both hf-design (architecture) and hf-tasks (WBS). Router resolves design-vs-tasks by artifact evidence.
argument-hint: [scope or revision focus]
---

# /plan — bias toward planning stage (`hf-design` ‖ `hf-ui-design` ‖ `hf-tasks`)

`/plan` merges the planning stage into a single user-facing command. The router decides which leaf to enter based on which artifacts already exist.

## What HF should do

1. Pass `$ARGUMENTS` to `using-hf-workflow` with `command_bias=/plan`.
2. Have `hf-workflow-router` read evidence and pick the actual target:
   - approved spec exists, no design yet → `hf-design` (and `hf-ui-design` in parallel if the spec declares a UI surface; see `hf-workflow-router/references/ui-surface-activation.md`)
   - approved design exists, no task plan yet → `hf-tasks`
   - design returned by `hf-design-review` (or `hf-ui-review`) for revision → re-enter the corresponding design leaf
   - tasks returned by `hf-tasks-review` for revision → re-enter `hf-tasks`
   - task plan exists and the next active task is not yet selected → router selects via `task reselection`, target becomes `hf-test-driven-dev`
3. If the spec is **not** approved yet, fall back to `hf-workflow-router` (which will likely reroute to `hf-specify` / `hf-spec-review`); never let `/plan` skip spec approval.

## HF guardrails

- `/plan` is one command for two leaves; that is intentional per ADR-001 D4 (planning is one user intent; the router has accurate evidence-based dispatch).
- Never let `/plan` enter `hf-design` and `hf-tasks` in the same turn. Pick one leaf per turn; the next leaf comes from canonical handoff.
- Do not let `/plan` cross the "approval" boundary — if a design or task plan revision needs human confirmation per Execution Mode = `interactive`, stop and wait.

User intent: $ARGUMENTS

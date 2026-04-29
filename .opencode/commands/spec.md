---
description: Use when no approved spec exists, the current spec is still a draft, or hf-spec-review returned the spec for revision. Bias: hf-specify; router has the final say.
argument-hint: [feature topic or spec revision focus]
---

# /spec — bias toward `hf-specify`

Invoke HarnessFlow with a bias toward spec authoring or revision, then let `using-hf-workflow` confirm route-first vs direct invoke.

## What HF should do

1. Pass `$ARGUMENTS` to `using-hf-workflow` with `command_bias=/spec`.
2. Apply the entry-bias matrix for "spec drafting / revising" (target leaf: `hf-specify`; fallback: `hf-workflow-router`).
3. If the active feature already has an **approved** spec and `$ARGUMENTS` is not a revision request, do **not** force `hf-specify` — fall back to `hf-workflow-router` (per the "command is bias, not authority" rule in `using-hf-workflow` step 6).
4. Otherwise enter `hf-specify`'s minimum kickoff in the same turn (intake the smallest necessary set of clarification questions, do not pre-write the spec).

## HF guardrails

- `/spec` does **not** skip artifact checks. If a draft spec already exists at the project's spec path, read it before asking new questions.
- `/spec` does **not** allow HF to lock direction / trade-offs / acceptance criteria on the architect's behalf — surface those back per `docs/principles/soul.md`.

User intent: $ARGUMENTS

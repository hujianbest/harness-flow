---
description: HarnessFlow default entry — route by artifacts, not chat memory. Use when current node / profile / next-step is unclear, or you simply want HF to figure out where you are.
argument-hint: [optional free-text intent]
---

# /hf — HarnessFlow default entry (route-first)

Invoke the HarnessFlow `using-hf-workflow` skill, then hand off to `hf-workflow-router` to recover orchestration from on-disk artifacts.

## What HF should do

1. Treat anything in `$ARGUMENTS` as an intent hint, not a target skill.
2. Read the minimal necessary evidence (active feature `progress.md`, `reviews/`, `verification/`, top-level navigation per `using-hf-workflow` step 2) to determine:
   - Workflow Profile (`full` / `standard` / `lightweight`)
   - Execution Mode (`interactive` / `auto`)
   - Workspace Isolation (`worktree-required` / `in-place`)
   - The single canonical next node — branch (`hf-hotfix` / `hf-increment`), authoring, review, gate, finalize, or experiment.
3. Output the route decision in the 3-line clear-case format defined by `using-hf-workflow` (`Entry Classification` / `Target Skill` / `Why`), then continue into the target leaf skill's minimum kickoff in the same turn (no extra "should I continue?" round).

## HF guardrails (from `docs/principles/soul.md` and `using-hf-workflow`)

- This command is a **bias**, not authority. Do not skip artifact checks because the user typed `/hf`.
- If `$ARGUMENTS` looks like a directional / trade-off / standard call, surface it back to the architect — do not decide it yourself.
- Never invoke `using-hf-workflow` as a runtime handoff target; it is the public entry only.

## Intent → bias hint

| `$ARGUMENTS` shape | Bias toward |
|---|---|
| empty / "继续" / "推进" / "where am I" | `using-hf-workflow` → `hf-workflow-router` (recovery) |
| product thesis / wedge / probe wording | `hf-product-discovery` |
| spec drafting / revising | `hf-specify` |
| "review" / "check" wording | `hf-*-review` (router decides which) |
| "implement" / "active task" / "build" | `hf-test-driven-dev` |
| "regression" / "completion" / "done?" | `hf-regression-gate` / `hf-completion-gate` |
| "closeout" / "finalize" / "wrap up" | `hf-completion-gate` → `hf-finalize` |
| "production bug" / "hotfix" | `hf-hotfix` |
| "scope change" / "increment" | `hf-increment` |

User intent: $ARGUMENTS

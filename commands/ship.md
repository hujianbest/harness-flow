---
description: Ask the HarnessFlow completion gate whether the current task or workflow can be closed out, then enter hf-finalize if the gate allows.
---

Bias toward HarnessFlow's closeout chain: `hf-completion-gate` -> `hf-finalize`.

Steps:

1. Enter via `skills/using-hf-workflow/SKILL.md` and hand off to `skills/hf-workflow-router/SKILL.md`.
2. Tell the router that the user's intent is "closeout / finalize".
3. The router routes into `skills/hf-completion-gate/SKILL.md` first.
4. The completion gate evaluates the evidence bundle (regression evidence, doc freshness, traceability, reviewer verdicts) against the Definition of Done.
5. Outcome:
   - if the gate's verdict allows finalize, the router routes into `skills/hf-finalize/SKILL.md`,
   - if not, the router routes back to the missing upstream node (often `hf-regression-gate`, `hf-doc-freshness-gate`, or a specific reviewer / implementation node).

Scope honesty (ADR-001 D1): HarnessFlow's main chain ends at `hf-finalize`, which is **engineering-level closeout** (state sync, release notes, handoff pack). It is **not** production deployment, observability, incident response, or post-launch ops — those are not first-class stages in v0.1.0. Surface this gap to the user instead of treating "merged" as "shipped".

The user request following this command is optional context (e.g. "close TASK-003" or "close the workflow"). The router uses on-disk state to decide which closeout scope applies.

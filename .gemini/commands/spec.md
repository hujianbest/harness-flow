---
description: Bias the next HarnessFlow step toward spec authoring or revision (hf-specify). The router still validates upstream preconditions before letting hf-specify run.
---

Bias toward the HarnessFlow `hf-specify` skill, but **do not bypass the router**.

Steps:

1. Enter via `skills/using-hf-workflow/SKILL.md` and hand off to `skills/hf-workflow-router/SKILL.md`.
2. Tell the router that the user's intent is "spec authoring or revision".
3. The router decides:
   - if upstream discovery / discovery-review preconditions are not satisfied, it routes back to `hf-product-discovery` or `hf-discovery-review` first,
   - if they are satisfied, it routes into `skills/hf-specify/SKILL.md`.
4. Follow `hf-specify`'s own SKILL.md (EARS / BDD / MoSCoW / INVEST / ISO 25010 / QAS / Success Metrics) to produce the spec artifact.

Hard rule: this command is a **bias**, not a bypass. Workflow position is decided by on-disk artifacts, not by the command name.

The user request following this command is the spec topic / revision intent.

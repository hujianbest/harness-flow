---
description: Bias toward the HarnessFlow planning stage — design (and UI design when the spec declares a UI surface) plus task breakdown. The router decides whether to enter hf-design, hf-ui-design, or hf-tasks based on artifact evidence.
---

Bias toward the HarnessFlow planning stage. This single command covers **both** architecture/UI design and task breakdown — it is intentionally not split into `/design` and `/tasks` (see ADR-001 D4).

> **Gemini CLI naming note (ADR-002 D2)**: this command is `/planning`, not `/plan`. Gemini CLI ships an internal `/plan` command, so HarnessFlow on Gemini CLI uses `/planning` to avoid the conflict. On Claude Code (and any other client without the conflict) the corresponding command is `/plan`.

Steps:

1. Enter via `skills/using-hf-workflow/SKILL.md` and hand off to `skills/hf-workflow-router/SKILL.md`.
2. Tell the router that the user's intent is "planning" (design and/or task breakdown).
3. The router inspects on-disk artifacts and decides:
   - if the spec is not approved, it routes back to `hf-specify` / `hf-spec-review`,
   - if the spec is approved but no design exists, it routes into `skills/hf-design/SKILL.md` (and in parallel `skills/hf-ui-design/SKILL.md` when the spec declares a UI surface — see `skills/hf-workflow-router/references/ui-surface-activation.md`),
   - if design is approved but tasks are missing, it routes into `skills/hf-tasks/SKILL.md`,
   - reviews (`hf-design-review`, `hf-ui-review`, `hf-tasks-review`) are independent nodes and must be respected.
4. Follow whichever leaf skill the router selected.

Hard rule: do not start `hf-test-driven-dev` from this command — that is `/build`'s job and only runs when a single `Current Active Task` is locked.

The user request following this command is the planning intent or specific design / tasks question.

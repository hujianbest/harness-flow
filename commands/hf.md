---
description: Route-first entry. When you are not sure which HarnessFlow node should run next, use this. The router will recover the right next node from on-disk artifacts.
---

Invoke the HarnessFlow `using-hf-workflow` skill, then hand off to `hf-workflow-router`.

Do NOT jump to any leaf skill (specify / design / tasks / test-driven-dev / *-review / *-gate / finalize) directly from this command.

Steps:

1. Load `skills/using-hf-workflow/SKILL.md` and follow it as the entry shell.
2. Hand off to `skills/hf-workflow-router/SKILL.md` so the router can:
   - inspect on-disk artifacts under the active feature directory,
   - decide the canonical next node,
   - and emit a single `Next Action Or Recommended Skill`.
3. Respect HarnessFlow's hard rules:
   - one `Current Active Task` at a time,
   - approvals and gates are first-class nodes (do not skip),
   - evidence-based routing, not chat memory.

The user request following this command is the new intent the router should consider.

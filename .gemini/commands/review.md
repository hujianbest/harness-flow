---
description: Request a HarnessFlow review. The router dispatches to the correct hf-*-review skill (discovery / spec / design / ui / tasks / test / code / traceability) based on artifact context.
---

Bias toward HarnessFlow's review nodes. There is **no single "review" skill** — review responsibility is intentionally split across independent nodes (Fagan-style separation), and the router decides which one to dispatch.

Steps:

1. Enter via `skills/using-hf-workflow/SKILL.md` and hand off to `skills/hf-workflow-router/SKILL.md`.
2. Tell the router that the user's intent is "review request" and pass any specific artifact target the user mentioned (e.g. "review the spec", "review TASK-003 code").
3. The router consults `skills/hf-workflow-router/references/review-dispatch-protocol.md` and routes to one of:
   - `skills/hf-discovery-review/SKILL.md`
   - `skills/hf-spec-review/SKILL.md`
   - `skills/hf-design-review/SKILL.md`
   - `skills/hf-ui-review/SKILL.md`
   - `skills/hf-tasks-review/SKILL.md`
   - `skills/hf-test-review/SKILL.md`
   - `skills/hf-code-review/SKILL.md`
   - `skills/hf-traceability-review/SKILL.md`
4. The selected reviewer runs as an **independent author/reviewer separation**; do not let it edit the artifact under review.

Hard rule: review nodes return a verdict + reviewer return contract; the router (not this command) decides what happens next based on that verdict.

The user request following this command should describe **what** needs reviewing.

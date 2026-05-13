# UI Traceability Matrix

Use this matrix when a task touches UI surface, visual styling, component library usage, App shell/provider, routes, or forms. It raises traceability from "element exists" to "design intent is implemented and evidenced".

```markdown
| UI Contract Anchor | Task Acceptance | Implementation Evidence | Test / Browser Evidence | Status | Notes |
|---|---|---|---|---|---|
| Home hero: primary color uses color.primary, no purple/blue gradient | TASK-013 AC-02 visual invariant | `Home.vue` classes / token usage | screenshot `/` desktop+mobile; console clean | covered / missing / drift |  |
```

## Required Checks

- Every critical `UI Implementation Contract` row has a task acceptance anchor.
- Every task acceptance anchor maps to implementation files and not only to tests.
- Evidence must include browser screenshot/DOM/console/network artifacts when the claim is visual or runtime UI conformance.
- Text-only tests, shallow component mounts, happy-dom, or mocked provider tests can support lower-tier behavior but cannot by themselves prove UI design conformance.
- If implementation intentionally diverges from the approved UI design, traceability review must require upstream UI design update and review before allowing completion.

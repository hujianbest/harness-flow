# UI Implementation Contract

Use this section inside `ui-design.md` for every UI surface that will be implemented. It turns visual direction into implementation constraints that downstream tasks, reviews, traceability, and gates can verify.

## Page / Component Contract Template

```markdown
### <route-or-component-name>

- Scope:
- Route / Story / Entry Point:
- Primary user task:
- Source anchors:
  - Spec:
  - UI design:
  - hf-design dependency:

#### Visual Invariants

| Invariant | Required Value / Pattern | Source Token / Decision | Must Not Do |
|---|---|---|---|
| Primary color use |  |  |  |
| Typography rhythm |  |  |  |
| Layout / grid |  |  |  |
| Surface / elevation |  |  |  |
| Motion |  |  |  |

#### Token Consumption

| UI element | Required token(s) | Allowed local utility mapping | Forbidden hardcoded styles |
|---|---|---|---|
|  |  |  |  |

#### Interaction And State Coverage

| Interaction | idle | hover | focus | active | disabled | loading | empty | error | success |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |

#### Evidence Targets

- Browser routes / stories to capture:
- Required viewports:
- Required screenshot artifacts:
- DOM anchors / selectors:
- Console / network assertions:
- Allowed visual deviations:
- Deviation handling: update UI design first, then implementation; do not silently drift in code.
```

## Contract Rules

- Each critical page or reusable UI component must have a contract before task planning.
- A contract must name forbidden visual drift explicitly when the design makes a choice, for example "no purple/blue gradient hero", "no fifth shadow tier", or "no default dashboard KPI grid".
- Token consumption may map to framework utilities, but the mapping must be explicit. Utility classes are not evidence of token conformance by themselves.
- Screenshot targets must include at least one desktop viewport and one narrow/mobile viewport when responsive behavior is in scope.
- If design assets or copy are missing, the contract must use semantic placeholders such as `{{ image:article-cover }}` or `{{ copy:hero-headline-pending }}` instead of inventing finished assets.

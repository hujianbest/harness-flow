# UI Conformance Evidence Profile

Use this profile for UI tasks that need browser-runtime evidence. It complements `runtime-smoke-profile.md` by checking whether the UI implementation matches the approved UI design contract.

## Project Fill-In Template

```markdown
## UI Conformance Evidence Profile

- App start command:
- Base URL:
- Browser(s):
- Required viewports:
  - desktop:
  - mobile:
- Screenshot artifact directory:
- Console policy:
- Network policy:

## Surfaces

| Surface | Route / Story | UI Contract Anchor | Required Viewports | DOM Anchors | Network Assertions | Screenshot Name |
|---|---|---|---|---|---|---|
| Home hero | `/` | `ui-design.md#home-hero-contract` | desktop, mobile | `#app`, `main`, hero heading | no 5xx; expected API paths only | `home-hero-{viewport}.png` |
```

## Minimum Pass Criteria

- Screenshots exist for each required surface and viewport.
- DOM anchors are present and non-empty.
- Browser console has no uncaught exceptions or framework provider errors.
- Network log has no unexpected API host/path/status drift and no 5xx for critical requests.
- Visual review notes explicitly state whether the screenshot matches the relevant UI Implementation Contract.
- Any deviation from visual invariants, token mapping, forbidden drift, or state matrix is recorded as a finding, not as a caveat on a pass verdict.

## Downgrade Rules

- Component tests, happy-dom/jsdom, and mocked provider/fetch tests cannot replace screenshot evidence for visual conformance claims.
- If screenshots cannot be captured due to environment constraints, the gate is blocked unless the task DoD or project profile explicitly allows a named fallback.
- A fallback must still preserve DOM, console, network, and token/contract checks where possible.

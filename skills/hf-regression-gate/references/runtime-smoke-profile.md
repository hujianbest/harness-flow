# Runtime Smoke Profile

Use this project-side profile when a task touches UI, API, or full-stack runtime behavior. Store the filled version in the feature or project convention path, then reference it from `tasks.md`, regression records, and completion records.

## Service Startup

- Frontend command:
- Frontend URL:
- Backend command:
- Backend URL:
- Additional services:

## Health Checks

| Service | Command / URL | Expected |
|---|---|---|
| frontend |  |  |
| backend |  |  |

## API Contract Surface

- API Base URL:
- Contract source: OpenAPI / controller routes / generated client / documented DTOs / other
- Required auth / seed data:
- Critical endpoints:

| Endpoint | Method | Expected Status | Required Response Fields |
|---|---|---|---|
|  |  |  |  |

## Browser Smoke Routes

| Route | Purpose | Required Checks |
|---|---|---|
| `/` | entry route | app root non-empty, no uncaught errors |
|  |  |  |

## Form / Interaction Checks

| Flow | Inputs | Expected Feedback |
|---|---|---|
| empty submit |  | validation shown, no white screen |
| invalid input |  | validation or API error shown |

## Console / Network Policy

- Console errors allowed? `no` by default. If yes, list exact allowed patterns:
- Critical network failures allowed? `no` by default. If yes, list exact allowed patterns:
- HTML response where JSON is expected is always a failure unless explicitly documented.
- Requests to the wrong host / port / path are always a failure unless explicitly documented.

## Downgrade Policy

- Can browser-runtime be skipped? `no` by default.
- Can api-contract be skipped? `no` by default.
- Who can approve downgrade:
- Required replacement evidence:

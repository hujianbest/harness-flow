# Verification Record — Regression Gate

## Metadata

- Verification Type: regression
- Scope: WriteOnce demo (entire `examples/writeonce/`)
- Date: 2026-04-29
- Record Path: `features/001-walking-skeleton/verification/regression-2026-04-29.md`
- Worktree Path / Worktree Branch: `cursor/m6-writeonce-demo-87a5` (in-place)

## Upstream Evidence Consumed

- Implementation Handoff: `evidence/task-001-green.log` (final GREEN)
- Review / Gate Records:
  - `reviews/test-review-task-001.md` (通过)
  - `reviews/code-review-task-001.md` (通过)
  - `reviews/traceability-review.md` (通过)
- Task / Progress Anchors: `tasks.md` T1 + `progress.md` (live)

## Claim Being Verified

- Claim: T1 (walking-skeleton e2e) implementation does not regress any
  existing behavior. Since this is a greenfield demo (no prior baseline),
  the regression check reduces to: "the full unit + e2e suite is fully
  green on the latest revision, on a fresh invocation, with no flaky
  failures over 1 run".

## Verification Scope

- Included Coverage:
  - `walking-skeleton.test.ts` (5 e2e cases)
  - `markdown-parser.test.ts` (5 unit cases)
  - `medium-adapter.test.ts` (5 unit cases)
  - `zhihu-adapter.test.ts` (2 unit cases)
  - `wechat-mp-adapter.test.ts` (2 unit cases)
  - `publish-service.test.ts` (4 unit cases)
- Uncovered Areas:
  - `Node20FetchHttpClient` (per ADR-0003: not exercised by walking
    skeleton; future real integration must add tests)
  - T2 / T3 / T4 deferred features

## Commands And Results

```text
cd examples/writeonce && npm test
```

- Exit Code: `0`
- Summary: `Test Files 6 passed (6)`, `Tests 23 passed (23)`, duration `367 ms`
- Notable Output: see `evidence/regression-2026-04-29.log` (full vitest output captured)

Type-check sanity:

```text
cd examples/writeonce && npx tsc --noEmit
```

- Exit Code: `0`
- Summary: 0 TypeScript errors under `strict` + `noUncheckedIndexedAccess`
  + `noImplicitOverride`.

## Freshness Anchor

- Why this evidence is for the latest relevant code state: the regression
  log was captured **after** the `hf-test-review`, `hf-code-review`,
  `hf-traceability-review` round; no source / test edit has occurred
  between that capture and this gate decision.
- Output Log / Terminal / Artifact: `evidence/regression-2026-04-29.log`
  (also see `evidence/task-001-green.log` for the GREEN evidence captured
  during the TDD node).

## Conclusion

- Conclusion: `通过`
- Next Action Or Recommended Skill: `hf-doc-freshness-gate`

## Scope / Remaining Work Notes

- Remaining Task Decision: T2 / T3 / T4 confirmed as v0.x backlog by tasks
  approval; not within v0.1.0 demo regression scope.
- Notes: `npm test` runs in 367 ms, well within NFR-Testability-1's < 1 s
  budget (which itself is for the e2e walking-skeleton case alone — the
  full suite includes 23 cases).

## Related Artifacts

- `evidence/task-001-red.log`
- `evidence/task-001-green.log`
- `evidence/regression-2026-04-29.log`
- `reviews/test-review-task-001.md`
- `reviews/code-review-task-001.md`
- `reviews/traceability-review.md`

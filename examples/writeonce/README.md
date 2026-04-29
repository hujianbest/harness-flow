# WriteOnce — HarnessFlow v0.1.0 Quickstart Demo

> **Purpose.** WriteOnce is the [HarnessFlow](https://github.com/hujianbest/harness-flow) v0.1.0 quickstart demo. It exists to give a **single, reviewable end-to-end trace** of HarnessFlow's main chain (`hf-product-discovery` → `hf-finalize`) on a real-ish project, so that anyone evaluating HarnessFlow can read the artifacts, follow the routing decisions, and see what HF-style engineering output looks like.
>
> **WriteOnce is the demo. The product itself is a deliberately scoped illustration, not a production tool.**

## What "shipped" means in this demo

Per ADR-001 D9 (the HarnessFlow-level ADR locking v0.1.0 release scope), the **deliverable** of this demo is the trail of HarnessFlow artifacts itself, not a polished SaaS product:

- `features/001-walking-skeleton/` — every artifact a HarnessFlow main-chain pass produces, in the canonical layout (`docs/principles/sdd-artifact-layout.md`):
  - `README.md`, `spec.md`, `design.md`, `tasks.md`, `progress.md`
  - `reviews/`, `approvals/`, `verification/`, `evidence/`
  - `closeout.md`
- `docs/adr/` — ADR pool for the demo (separate from HarnessFlow's own `docs/decisions/` ADRs).
- `docs/insights/` — discovery draft + spec-bridge notes.
- A **walking-skeleton CLI** that picks a Markdown file and "publishes" it to a single platform (Medium), with the other two declared platforms (Zhihu, WeChat MP) explicitly stubbed and traceable through the design + tasks artifacts.

The walking skeleton is **deliberately thin** — it implements one happy path end to end, not the full product. That matches both Walking Skeleton discipline (`hf-test-driven-dev`) and ADR-001 D9's stance: the demo's job is to make HarnessFlow's main chain visible, not to be a finished publishing tool.

## Product framing (locked by `cursor agent` per user delegation, 2026-04-29)

The user explicitly delegated product scope to the cursor agent (overriding the "leave it to discovery" framing in ADR-001 D9 sub-decision b). The locked seeds:

| Slot | Value |
|---|---|
| Target users | Technical content creators (independent developers, engineers who blog) |
| Initial platforms | **Medium** (Walking Skeleton implementation), **Zhihu** + **WeChat MP** (declared in design + tasks, not implemented in v0 walking skeleton) |
| MVP boundary | Single Markdown source file → publish to Medium; cover plain text + images + fenced code blocks; no comment sync, no analytics back-flow, no scheduling. |
| Tech stack | Node.js 20 + TypeScript + minimal CLI (`writeonce publish ./post.md`) |
| Walking-skeleton coverage | One platform (Medium) wired end to end via TDD; other two platforms shown as `PlatformAdapter` extension points, not implemented |

These seeds enter the discovery + spec artifacts as confirmed inputs (with explicit attribution to user delegation), so HarnessFlow's `hf-product-discovery` and `hf-specify` nodes still get to do their job (problem framing, JTBD, OST, NFR QAS, success metrics, etc.) on top of stable seeds.

## Layout

```
examples/writeonce/
├── README.md                              # this file
├── docs/
│   ├── adr/                               # demo-internal ADRs (separate from HF repo's docs/decisions/)
│   │   └── 0001-record-architecture-decisions.md
│   └── insights/                          # discovery drafts (sdd-artifact-layout tier 2)
│       ├── 2026-04-29-writeonce-discovery.md
│       └── 2026-04-29-writeonce-spec-bridge.md
├── CHANGELOG.md                           # demo-internal changelog
└── features/
    └── 001-walking-skeleton/              # the one-and-only feature for v0.1.0 demo
        ├── README.md                      # feature entry
        ├── spec.md                        # hf-specify output
        ├── design.md                      # hf-design output
        ├── tasks.md                       # hf-tasks output
        ├── progress.md                    # task-progress
        ├── reviews/
        │   ├── discovery-review-2026-04-29.md
        │   ├── spec-review-2026-04-29.md
        │   ├── design-review-2026-04-29.md
        │   ├── tasks-review-2026-04-29.md
        │   ├── test-review-task-001.md
        │   ├── code-review-task-001.md
        │   └── traceability-review.md
        ├── approvals/
        │   ├── discovery-approval-2026-04-29.md
        │   ├── spec-approval-2026-04-29.md
        │   ├── design-approval-2026-04-29.md
        │   └── tasks-approval-2026-04-29.md
        ├── verification/
        │   ├── regression-2026-04-29.md
        │   └── completion-task-001.md
        ├── evidence/
        │   ├── task-001-red.log
        │   └── task-001-green.log
        ├── contracts/
        │   └── platform-adapter.contract.md
        └── closeout.md
```

## How to read it

For someone evaluating HarnessFlow:

1. Start at this README to see the framing.
2. Read `docs/insights/2026-04-29-writeonce-discovery.md` to see what `hf-product-discovery` produces.
3. Read `features/001-walking-skeleton/README.md` to see the feature entry / status snapshot.
4. Walk top-to-bottom through `spec.md` → `design.md` → `tasks.md` → `reviews/` → `verification/` → `closeout.md`. The order matches the HarnessFlow main chain.
5. Look at the source code under `src/` and tests under `test/` to see the walking skeleton itself.

## Code

The implementation is **deliberately small**. It exists to give the TDD node real RED/GREEN evidence, not to be a usable Medium publisher. Network calls are stubbed in the walking skeleton.

```
src/
├── cli.ts                       # entry: writeonce publish <file>
├── parser/
│   └── markdown-parser.ts       # markdown -> structured Post
├── platform/
│   ├── platform-adapter.ts      # interface (the Hyrum-safe boundary)
│   ├── medium-adapter.ts        # walking-skeleton implementation (HTTP stub)
│   ├── zhihu-adapter.ts         # extension point only (throws "not implemented")
│   └── wechat-mp-adapter.ts     # extension point only
└── publish/
    └── publish-service.ts       # orchestration

test/
└── walking-skeleton.test.ts     # one end-to-end test: read post.md -> Medium adapter
```

## What HarnessFlow's main chain looks like, run on this demo

| Node | Artifact in this repo |
|---|---|
| `hf-product-discovery` | `docs/insights/2026-04-29-writeonce-discovery.md` |
| `hf-discovery-review` | `features/001-walking-skeleton/reviews/discovery-review-2026-04-29.md` + approval |
| `hf-specify` | `features/001-walking-skeleton/spec.md` |
| `hf-spec-review` | `features/001-walking-skeleton/reviews/spec-review-2026-04-29.md` + approval |
| `hf-design` | `features/001-walking-skeleton/design.md` |
| `hf-design-review` | `features/001-walking-skeleton/reviews/design-review-2026-04-29.md` + approval |
| `hf-tasks` | `features/001-walking-skeleton/tasks.md` |
| `hf-tasks-review` | `features/001-walking-skeleton/reviews/tasks-review-2026-04-29.md` + approval |
| `hf-test-driven-dev` | `src/`, `test/`, `evidence/task-001-red.log`, `evidence/task-001-green.log` |
| `hf-test-review` | `features/001-walking-skeleton/reviews/test-review-task-001.md` |
| `hf-code-review` | `features/001-walking-skeleton/reviews/code-review-task-001.md` |
| `hf-traceability-review` | `features/001-walking-skeleton/reviews/traceability-review.md` |
| `hf-regression-gate` | `features/001-walking-skeleton/verification/regression-2026-04-29.md` |
| `hf-doc-freshness-gate` | covered inside `closeout.md` "Release / Docs Sync" |
| `hf-completion-gate` | `features/001-walking-skeleton/verification/completion-task-001.md` |
| `hf-finalize` | `features/001-walking-skeleton/closeout.md` + this README + demo `CHANGELOG.md` |

## Limits

- The two non-implemented platforms (Zhihu, WeChat MP) are **only** declared at the design + tasks level. They do not have working adapters. This is intentional: walking-skeleton scope, not feature scope.
- The Medium adapter does not call the real Medium API. The HTTP call is stubbed so tests stay deterministic and offline.
- This demo's `docs/adr/` is **independent** of the HarnessFlow repo's `docs/decisions/`. Don't conflate them.
- This demo deliberately does **not** ship a CI/CD pipeline. ADR-001 D1 (P-Honest) keeps release / ops out of HarnessFlow v0.1.0; the demo respects that.

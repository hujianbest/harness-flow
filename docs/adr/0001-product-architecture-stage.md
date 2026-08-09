# ADR 0001: Product architecture stage

## Status

Accepted

## Context

After aligning the main chain with Matt Pocock's skills flow, feature work still needed a durable **codebase map** so agents do not rescan the whole repository on every feature. The earlier HarnessFlow product layer used `product/architecture.md` for that purpose.

## Decision

Keep an explicit stage skill `hf-to-product-architecture` that writes or refreshes `product/architecture.md` (and related product-layer files as needed). The stage sits after grilling / docs and before `hf-to-spec`.

Product architecture is **recommended** for greenfield and large brownfield delivery, not a hard blocker enforced by tooling. Agents should still read `product/architecture.md` when present before exploring code.

## Consequences

- Feature `architecture.md` (from `hf-to-architecture`) remains the per-feature design artifact.
- Product `architecture.md` remains the repo-level map.
- Progress for this stage is recorded in `product/progress.md` and confirmed via `hf-review`.

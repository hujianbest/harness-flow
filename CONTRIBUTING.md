# Contributing to HarnessFlow

Thanks for your interest in HarnessFlow.

This document is intentionally short. HarnessFlow is currently a **single-maintainer** pre-release (`v0.5.0`). The goal of this guide is to make small, well-scoped contributions easy to land and to keep larger changes from blocking on review forever.

## Before You Start

1. **Read [`README.md`](README.md)** (or [`README.zh-CN.md`](README.zh-CN.md)) end-to-end. Pay particular attention to the **Scope Note** at the top — `v0.5.0` is deliberately narrow (Claude Code + OpenCode + Cursor only; main chain ends at `hf-finalize`; v0.4.0 added `hf-release` as a release-tier standalone skill; v0.5.0 added a closeout HTML companion report to `hf-finalize` + new `scripts/render-closeout-html.py`; the other 5 ops/release skills (deployment / monitoring / rollback / etc.) remain out of scope; no new clients, no personas). Many "missing feature" reports are actually documented scope choices.
2. **Read the relevant ADR**. Release scope decisions are locked in [`docs/decisions/ADR-005-release-scope-v0.5.0.md`](docs/decisions/ADR-005-release-scope-v0.5.0.md) (hf-finalize closeout HTML companion + scripts/render-closeout-html.py; hf-shipping-and-launch stays v0.6+), [`docs/decisions/ADR-004-hf-release-skill.md`](docs/decisions/ADR-004-hf-release-skill.md) (hf-release standalone skill + /release command), [`docs/decisions/ADR-003-release-scope-v0.3.0.md`](docs/decisions/ADR-003-release-scope-v0.3.0.md) (Cursor-only client expansion; no new skills; no personas), [`docs/decisions/ADR-002-release-scope-v0.2.0.md`](docs/decisions/ADR-002-release-scope-v0.2.0.md) (含 D11 校准撤回 D2/D3/D4/D8 的说明) and [`docs/decisions/ADR-001-release-scope-v0.1.0.md`](docs/decisions/ADR-001-release-scope-v0.1.0.md). If your contribution conflicts with an ADR decision, please open an issue first to discuss whether the ADR should be revisited.
3. **Read the [Code of Conduct](CODE_OF_CONDUCT.md)**. By participating you agree to abide by it.

## What HarnessFlow Will and Won't Accept Right Now

### Will accept

- Bug fixes (broken links, typos, factual errors in skill `SKILL.md` files, demo bugs).
- Documentation improvements that respect the Scope Note.
- Setup instructions for clients that v0.5.0 doesn't yet support (Gemini CLI / Windsurf / GitHub Copilot / Kiro), **clearly marked** as additions, not as v0.5.0 commitments.
- Improvements to the WriteOnce demo's walking-skeleton implementation that respect ADR-001 D9 (the demo is not a finished publishing tool; HTTP must stay stubbed).

### Will defer (please open an issue first)

- New `hf-*` skills, especially deployment / ops / monitoring skills (out of scope per ADR-001 D1 + ADR-002 D1 + ADR-003 D2 + ADR-004 D2 + ADR-005 D7; remaining 5 ops/release skills tracked for v0.6+; v0.4.0 already added `hf-release` for the engineer-level version-cut slice; v0.5.0 added closeout HTML companion to `hf-finalize` without growing the skill set).
- Major restructuring of an existing `SKILL.md` (per ADR-001 D11 + ADR-003 D2 + ADR-004 + ADR-005 D4 the 24 skills are deliberately maintained as-is; only `Common Rationalizations` (required) and `和其他 Skill 的区别` (forbidden) are hard rules per ADR-002 D9 / D10; v0.5.0 only adds step 6A to `hf-finalize` without restructuring).
- Anything that touches `docs/principles/` (ADR-001 D11 + ADR-003 D9 + ADR-004 + ADR-005 mark these as design references; treat them as authored documents, not editable specs).
- New `agents/` personas (`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — ADR-002 D11 + ADR-003 D3 + ADR-004 + ADR-005 D5 keep these deferred to v0.6+.

### Will probably reject (please don't spend time on these without prior discussion)

- Force-pushes / amended commits to shared branches.
- Sweeping rewrites without a referenced ADR or issue.
- Changes that re-introduce the anatomy audit script as a release gate (D11 explicitly removed it).
- Removing the `Scope Note` or `Acknowledgements` sections from the READMEs.

## How to Submit a Change

1. **Open an issue first** for anything beyond a typo or one-line fix. This avoids spending time on a PR that won't land.
2. **Branch from `main`**. Suggested prefix: `contrib/<short-topic>` (or `cursor/<topic>-<suffix>` if you are running this repository's own cloud-agent flow).
3. **Make small, logical commits**. One commit per logical change is preferred; we avoid batching unrelated edits.
4. **Sync long-lived assets** if your change touches `examples/writeonce/` or any feature directory. Specifically:
   - If you change a feature's spec / design / tasks, also update the corresponding feature `README.md` Status Snapshot.
   - If you change a demo source file, run `cd examples/writeonce && npm test && npx tsc --noEmit` and confirm both pass.
   - If you change a long-term asset under `docs/`, update `CHANGELOG.md`'s `[Unreleased]` section.
5. **Open a PR** with a description that:
   - Names the issue (or ADR section) you are addressing
   - Lists what files changed and why
   - Includes any test or build output as evidence
   - Calls out anything you deliberately left out of scope
6. **Use draft PRs** for work-in-progress; mark ready-for-review only when CI (when we have it — see "Known Limitations") and your own checks pass.

## Style

- **Markdown**: keep lines under ~120 characters where reasonable; prefer fenced code blocks with language identifiers; use sentence-case for headings.
- **TypeScript** (in `examples/writeonce/`): follow the existing `tsconfig.json` (`strict` + `noUncheckedIndexedAccess` + `noImplicitOverride`); kebab-case file names; ESM with `.js` import suffixes.
- **Commit messages**: imperative mood; first line ≤ 72 chars; if the change is part of a HarnessFlow main-chain run, reference the relevant feature directory in a `Refs:` trailer (example: `Refs: examples/writeonce/features/001-walking-skeleton`).

## Demo (`examples/writeonce/`) Specific Rules

- The walking-skeleton implementation is intentionally small. Resist the urge to "round it out" — many gaps (no real Medium API, two stubbed adapters, no CLI ergonomic layer) are documented in `examples/writeonce/features/001-walking-skeleton/tasks.md` as deferred.
- HTTP must stay stubbed (`RecordingHttpClient`). Do not introduce real network calls in tests or in the walking-skeleton path.
- `examples/writeonce/docs/adr/` is **independent** of the repository-root `docs/decisions/`. Don't conflate them.

## Known Limitations of the Contribution Process

These are honest gaps, not preferences:

- **No CI yet.** v0.5.0 still ships without GitHub Actions. PR authors should run `cd examples/writeonce && npm test && npx tsc --noEmit` locally and paste the output in the PR. For changes touching `scripts/`, also run `python3 scripts/audit-skill-anatomy.py` and the `python3 scripts/test_*.py` files. CI remains a v0.6+ work item.
- **Single maintainer.** Reviews can be slow. If a PR has been quiet for more than 14 days, a polite ping in the PR thread is welcome.
- **`SKILL.md` lint is advisory.** `scripts/audit-skill-anatomy.py` exists since v0.2.0 (ADR-002 D5) but is **advisory** (does not block PR merge); ADR-003 D8 / ADR-004 / ADR-005 keep this stance. Please be careful when editing `SKILL.md` files and follow the implicit structure used by neighbouring skills.
- **No real-environment install smoke as a release hard gate.** ADR-002 D11 revoked the proposed hard gate; ADR-003 D7 / ADR-004 / ADR-005 keep this stance for v0.5.0 (3 clients still small enough that maintainer self-verification is sufficient). The first real Cursor / Claude Code / OpenCode install verification on a clean user environment is community-driven; please open an issue if anything install-related breaks.
- **No formal release cadence.** v0.5.0 is a pre-release; patch releases (`v0.5.x`) ship when meaningful fixes accumulate, not on a fixed schedule. Note: maintainer-side release cuts use the v0.4.0 `hf-release` skill itself (dogfood); v0.5.0 is the second dogfood pass; see `skills/hf-release/SKILL.md` and `features/release-v0.5.0/release-pack.md` for the v0.5.0 release pack as a worked example.

## Reporting Bugs and Requesting Features

Please use the issue templates under `.github/ISSUE_TEMPLATE/`:

- `bug_report.md` — for things that look broken in HarnessFlow itself.
- `feature_request.md` — for new behavior. Please check the Scope Note and ADR-005 (then ADR-004, ADR-003, ADR-002, ADR-001) first; many "missing features" are deliberate scope choices for v0.5.0.

For security issues, see [`SECURITY.md`](SECURITY.md).

## Attribution

This `CONTRIBUTING.md` is intentionally narrow because HarnessFlow's own `Acknowledgements` section in the README does the heavier lifting of attributing methods. If you contribute a new skill or substantial reference document, please add the relevant source to that section in the same PR.

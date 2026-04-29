# Changelog

All notable changes to HarnessFlow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versions before `v0.1.0` (the first public pre-release) are not tracked here;
see git history for pre-public development.

## [Unreleased]

## [0.1.0] - 2026-04-29 (pre-release)

First public pre-release of HarnessFlow. Scope and limits are locked by
[`docs/decisions/ADR-001-release-scope-v0.1.0.md`](docs/decisions/ADR-001-release-scope-v0.1.0.md).

### What ships

- 23 `hf-*` workflow skills + `using-hf-workflow` public entry — the full main
  chain from `hf-product-discovery` through `hf-finalize`, with branch nodes
  (`hf-hotfix` / `hf-increment`) and the knowledge side node `hf-bug-patterns`.
- Constitution layer under `docs/principles/` (`soul.md`, `skill-anatomy.md`,
  `skill-node-define.md`, `sdd-artifact-layout.md`, `coding-principles.md`,
  plus methodology references).
- Six short-alias slash commands: `/hf` `/spec` `/plan` `/build` `/review`
  `/ship`. `/plan` merges design + tasks; router decides design vs tasks by
  artifact evidence.
- Integration paths for **Claude Code** and **OpenCode** only.
- `examples/writeonce/` quickstart that runs the full main chain end-to-end
  on a personal multi-platform writing & publishing app.
- MIT license; English + 中文 README; this CHANGELOG.

### What does NOT ship (explicit Scope Notes)

Per ADR-001 D1 (Pillar C = P-Honest):

- **No release / ops skills** — no `hf-security-hardening`,
  `hf-performance-gate`, `hf-deprecation-and-migration`,
  `hf-shipping-and-launch`, `hf-ci-cd-and-automation`,
  `hf-debugging-and-error-recovery`, or `hf-browser-runtime-evidence`. The
  main chain terminates at `hf-finalize` (engineering closeout); deployment
  pipelines, observability, incident response, metrics feedback, and post-launch
  ops are out of v0.1.0 scope.
- **No automated SKILL.md anatomy / quality baseline** — per D11, files under
  `docs/principles/` are design reference, not a compliance baseline; no audit
  script ships in v0.1.0.
- **No anti-rationalization tables across SKILL.md** — per D11 (which
  superseded D8), node-internal anti-rationalization is deferred to a
  post-release iteration based on actual feedback.
- **No platform support beyond Claude Code and OpenCode** — Cursor / Gemini
  CLI / Windsurf / Copilot / Kiro deferred to v0.2+. The repository remains
  usable from those clients, but it is not on the v0.1.0 supported-platform
  promise list.
- **No package-name pre-claim** on npm / PyPI / any marketplace.
- **No CI integration** of any quality gate.

### Why pre-release

`v0.1.0` is intentionally tagged as a GitHub pre-release. The skill family is
ready for adoption by individual users and small teams who want HarnessFlow's
spec-driven + TDD workflow discipline, but the scope above is narrower than
the long-term vision (see `README.md` § Roadmap). Stability and API surface
may shift before `v1.0.0`.

### Acknowledgements

See `README.md` § Acknowledgements for the methodology lineage that this
release builds on (Karpathy / Forrest, Google SWE Book, DDD, Beck, Fowler,
Martin, Fagan, Brown, Starke, ISO, STRIDE, Nielsen, WCAG, PMBOK, JTBD, OST).

[Unreleased]: https://github.com/hujianbest/harness-flow/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.1.0

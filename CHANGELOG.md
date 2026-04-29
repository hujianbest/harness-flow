# Changelog

All notable changes to HarnessFlow will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - pre-release

> **First public release.** Marked as a **pre-release** on GitHub Releases.
>
> Release scope, alternatives considered, and reversibility for every decision below are recorded in [`docs/decisions/ADR-001-release-scope-v0.1.0.md`](docs/decisions/ADR-001-release-scope-v0.1.0.md).

### Added

- **MIT `LICENSE`** at the repository root. Copyright `hujianbest`. (ADR-001 D2)
- **Claude Code plugin manifest**:
  - `.claude-plugin/plugin.json` — name `harness-flow`, version `0.1.0`, MIT, repo `hujianbest/harness-flow`.
  - `.claude-plugin/marketplace.json` — marketplace entry for `/plugin marketplace add hujianbest/harness-flow`.
  (ADR-001 D3, D5)
- **6 short slash commands** for Claude Code (ADR-001 D4):
  - `/hf` — route-first default (`using-hf-workflow` → `hf-workflow-router`).
  - `/spec` — bias toward `hf-specify`.
  - `/plan` — combined design + tasks (router decides between `hf-design`, `hf-ui-design`, `hf-tasks`).
  - `/build` — bias toward `hf-test-driven-dev` (only when one `Current Active Task` is locked).
  - `/review` — router dispatches to the matching `hf-*-review`.
  - `/ship` — `hf-completion-gate` → `hf-finalize`.
- **`docs/claude-code-setup.md`** — Claude Code install (marketplace + local), verify, troubleshooting.
- **`docs/opencode-setup.md`** — OpenCode setup using agent-driven routing; no `AGENTS.md` sidecar required (ADR-001 D3).
- **README Scope Note** at the top of `README.md` and `README.zh-CN.md`: pre-release; Claude Code + OpenCode only; main chain ends at `hf-finalize` (engineering-level closeout); release / ops out of scope. (ADR-001 D1, D6)
- **Acknowledgements** section in both READMEs listing every method source and where it lands in HarnessFlow (Karpathy skills, Google SWE / engineering-practices, Evans, Vernon, Brandolini, Beck, Fowler, Martin, Fagan, Brown, Starke, ISO/IEC 25010, STRIDE, Nielsen, WCAG, PMBOK, Ulwick / Christensen JTBD, Torres OST). (ADR-001 D7)
- **`CHANGELOG.md`** (this file). Versioning starts at `v0.1.0`. (ADR-001 D6)

### Decided

- **Pillar C = P-Honest (narrow but hard).** v0.1.0 does **not** add release / ops skills (no `hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`, `hf-browser-runtime-evidence`). Main chain terminates at `hf-finalize`. (ADR-001 D1)
- **Officially supported clients = Claude Code + OpenCode only.** Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro are deferred to v0.2+. HarnessFlow is plain Markdown so it may run elsewhere, but those paths are not part of the v0.1.0 commitment. (ADR-001 D3)
- **Repository ownership stays at `hujianbest/harness-flow`.** No org migration; no npm / PyPI / marketplace name pre-claim for v0.1.0. (ADR-001 D5)
- **Versioning policy: SemVer; `v0.1.0` is a pre-release.** GitHub Release will have "Set as a pre-release" checked. (ADR-001 D6)
- **`docs/principles/` is design reference only**, not a runtime dependency, not a release gate, and not a SKILL.md compliance baseline. `soul.md` remains the constitution layer for the user-as-architect / HF-as-engineering-team contract only. (ADR-001 D11)
- **R1 (quality baseline hardening) concluded.** v0.1.0 maintains the existing 24 `hf-*` skills + `using-hf-workflow` as-is. No SKILL.md content edits in this release. (ADR-001 D11)

### Deferred (to v0.2+)

- All release / deployment / observability / incident-response / security-hardening / performance-gate / deprecation-and-migration / browser-runtime-evidence skills.
- Plugin / setup support for Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro.
- `/hotfix` slash command (use natural language + `/hf` so the router can branch into `hf-hotfix` / `hf-increment`).
- `/gate` slash command (gates are pulled by the canonical next action of upstream nodes, not pushed by the user).
- Any batched `Common Rationalizations` / `Object Contract` rewrites across the 24 skills.
- Automated SKILL.md anatomy audit script and `docs/audits/` baseline reports.

### Voided / Superseded

- **ADR-001 D8** (force every SKILL.md to add `Common Rationalizations`) — **superseded by D11**. v0.1.0 does not require this; future versions may re-evaluate based on actual feedback.
- **ADR-001 D10** (Object Contract enforcement level: recommended in v0.1.0, mandatory in v0.2.0) — **voided by D11**. Object Contract is back to "author writes it when needed", neither mandatory nor recommended in v0.1.0.

### Quickstart demo (planned, separate work)

`examples/writeonce/` quickstart demo (ADR-001 D9) is **not** part of this changelog entry's deliverables. The demo's product scope (target platforms, MVP boundary, tech stack) is intentionally **not** locked by ADR-001 — it must be produced by running the HarnessFlow main chain itself (`hf-product-discovery` → ... → `hf-finalize`), with user approval at the discovery-review and spec-review gates. Tracked separately.

[Unreleased]: https://github.com/hujianbest/harness-flow/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.1.0

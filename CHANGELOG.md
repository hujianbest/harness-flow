# Changelog

All notable changes to HarnessFlow will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed

- **`hf-bug-patterns` skill removed.** The standalone "knowledge side node" was deleted along with its `references/`, `evals/`, and `test-prompts.json`. The skill was an optional learning loop, not part of the canonical main chain or any review/gate. Risk-input language in `hf-test-review` (description, methodology row, workflow step 1, checklist `TT3`) now points to "项目缺陷模式记录 / 风险清单 / hotfix 历史" instead of the removed skill, so projects that maintain a defect catalog under their own conventions are still consumed as risk input. The `docs/bug-patterns/catalog.md` artifact slot was removed from `docs/principles/sdd-artifact-layout.md`, `skills/hf-workflow-router/references/workflow-shared-conventions.md`, and `skills/hf-finalize/SKILL.md` — projects that still want a bug catalog can declare their own path in project-level conventions. README skill counts updated to **22 `hf-*` skills + `using-hf-workflow`** (Claude Code marketplace description, OpenCode setup, Claude Code setup, both READMEs).

### Added

- `SECURITY.md` — security policy with scope, supported versions, private reporting via GitHub Security Advisory.
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1.
- `CONTRIBUTING.md` — narrow, single-maintainer-aware contribution guide aligned with ADR-001 D1 / D11 scope.
- `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md` — issue templates that prompt readers to check the Scope Note + ADR-001 before filing.
- `.github/ISSUE_TEMPLATE/config.yml` — disables blank issues; adds contact links to security advisory + Code of Conduct + Scope Note.
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template with Scope Note check + per-area testing prompts (no CI yet, see `CONTRIBUTING.md` "Known Limitations").

### Fixed

- **OpenCode install path** now actually works out-of-the-box. The previous setup told users to "clone the repo and open it in OpenCode", but OpenCode's [`skill` tool](https://opencode.ai/docs/skills/) only auto-discovers `SKILL.md` files under `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`, or their global counterparts — a top-level `skills/` directory was never picked up, so `using-hf-workflow` and the 23 leaf skills were invisible to OpenCode agents. Added a `.opencode/skills -> ../skills` symlink so clone-and-open works without duplicating files.
- **`docs/opencode-setup.md`** rewritten to describe OpenCode's real skill-discovery model and the three legitimate install topologies (clone-and-open, vendor into another project's `.opencode/skills/`, global install under `~/.config/opencode/skills/`), with a `/skills` verification step and updated troubleshooting.
- **`README.md` + `README.zh-CN.md`** OpenCode sections updated to match: shipped symlink + verification command + cross-project install guidance.

### Notes

- These additions are governance / hygiene only; no `skills/`, `docs/principles/`, or `examples/writeonce/` content changes.
- Real-environment install verification of the Claude Code marketplace path and the OpenCode setup path is the remaining `v0.1.x` stabilization item that **cannot** be completed inside this repository — see `CONTRIBUTING.md` "Known Limitations".

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

### Quickstart demo (delivered)

- **`examples/writeonce/` — WriteOnce demo, full HarnessFlow main-chain trace** (ADR-001 D9):
  - 16 HF nodes (`hf-product-discovery` → `hf-finalize`) each produced a reviewable artifact under `examples/writeonce/features/001-walking-skeleton/` and `examples/writeonce/docs/insights/`.
  - Walking-skeleton implementation: Node.js 20 + TypeScript + minimal CLI; Markdown → Medium with Zhihu / WeChat MP declared as extension points but not implemented; 23 vitest cases passing offline in ~370 ms.
  - 3 demo-internal ADRs (`examples/writeonce/docs/adr/0001..0003`).
  - Demo-internal `examples/writeonce/CHANGELOG.md`.
- Per ADR-001 D9: the demo's **deliverable is the trail of HF main-chain artifacts**, not a finished product. The demo does not publish to a real Medium account; all HTTP is intercepted by `RecordingHttpClient`.
- Per the user's 2026-04-29 delegation, the demo's product scope (target users / platforms / MVP / tech stack) was locked by the cursor agent and recorded as `seed input` in `examples/writeonce/docs/insights/2026-04-29-writeonce-discovery.md` section 0, then carried forward by `hf-specify`. Discovery / spec / design / tasks approval gates were each signed off by the cursor agent on that delegation.

[Unreleased]: https://github.com/hujianbest/harness-flow/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.1.0

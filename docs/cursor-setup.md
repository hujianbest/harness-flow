# HarnessFlow on Cursor

HarnessFlow v0.6.0 supports Cursor through Cursor's **rules** mechanism. Skills are plain Markdown, so the same `skills/` tree that ships in this repository is consumed by Cursor as a project-level (or globally-registered) `alwaysApply` rule that points the agent at the canonical entry shell + router.

> **Scope (v0.6.0 pre-release).** v0.6.0 officially supports 3 clients (unchanged from v0.3.0): **Claude Code**, **OpenCode**, and **Cursor**. The 4 remaining client expansions (Gemini CLI / Windsurf / GitHub Copilot / Kiro) stay deferred to v0.7+. v0.6.0 introduces repo-root `install.sh` + `uninstall.sh` + `tests/test_install_scripts.sh` (per ADR-007 + ADR-008): one-command vendoring covers Cursor / OpenCode / both targets × copy / symlink topologies = 6 combinations + 2 negative-path scenarios = 14 e2e PASS; manifest-based uninstall preserves user-added skills; pure bash 3.2+ with zero new runtime dependencies. v0.5.x lineage (ADR-005 closeout HTML companion + ADR-006 anatomy v2 vendoring fix) stays in effect. v0.4.0's `hf-release` is unchanged; on Cursor it is invoked via natural language ("cut a release / tag a version") through the entry shell's bias row, which then **direct invokes** `hf-release` without going through `hf-workflow-router` (ADR-004 D3). The HarnessFlow main chain still ends at `hf-finalize` (single-feature engineering-level closeout). The remaining 5 ops/release skills (`hf-shipping-and-launch` / etc.) and personas all stay deferred to v0.7+ (ADR-005 D5 / D7 / ADR-008 D5). See `docs/decisions/ADR-008-release-scope-v0.6.0.md` for the full v0.6.0 scope decisions.

## How Cursor sees HF skills

Cursor doesn't have a native skill-pack auto-discovery mechanism. Instead it loads:

- **Project rules**: any file under `.cursor/rules/<name>.md` (or `<name>.mdc`) is auto-loaded for the workspace.
- **Always-on rules**: rules with `alwaysApply: true` frontmatter are injected on every turn.
- **AGENTS.md** (optional): Cursor reads a top-level `AGENTS.md` for persistent context. HarnessFlow does not require this — see "Why no `AGENTS.md` sidecar?" in `docs/opencode-setup.md`; the same reasoning applies here.

HarnessFlow keeps every `hf-*` skill self-contained under the top-level `skills/` directory. To make these reachable from Cursor's rule loader, the repository ships a single project rule that points Cursor at the canonical entry skill plus the router — no `SKILL.md` duplication into `.cursor/`.

## 1. Install

You have two install topologies. Pick whichever matches how you already use Cursor.

### A. Use the HarnessFlow repository directly (recommended for trying it out)

```bash
git clone https://github.com/hujianbest/harness-flow.git
cursor harness-flow
```

The repository ships `.cursor/rules/harness-flow.mdc` (added in v0.3.0). Opening the repo in Cursor is enough — the rule auto-loads on every session because of `alwaysApply: true`.

### B. Vendor HarnessFlow into your own project (recommended: install script)

If you want HarnessFlow available inside another repository, the easiest path is the bundled install script (added in feature 001-install-scripts; see ADR-007):

```bash
# From the harness-flow repository, target your host repo:
bash /path/to/harness-flow/install.sh --target cursor --host /path/to/your/project

# Or symlink topology to track HF upstream automatically:
bash /path/to/harness-flow/install.sh --target cursor --topology symlink \
     --host /path/to/your/project
```

The script vendors `skills/` to `<host>/.cursor/harness-flow-skills/` and copies (or symlinks) `harness-flow.mdc` to `<host>/.cursor/rules/`. It also writes a `.harnessflow-install-manifest.json` and a `.harnessflow-install-readme.md` with quick-verify and uninstall instructions. To uninstall later:

```bash
bash /path/to/harness-flow/uninstall.sh --host /path/to/your/project
```

If you want both Cursor and OpenCode integrations at once, use `--target both`.

> **Cursor rule path note**: `harness-flow.mdc` references `skills/using-hf-workflow/SKILL.md` relatively. After vendoring, the correct path is `.cursor/harness-flow-skills/using-hf-workflow/SKILL.md`. The post-install README in your host repo reminds you of this; v0.6+ may rewrite paths automatically (ADR-007 D4 Alternatives A3, deferred).

#### Manual fallback (advanced users)

If you prefer to vendor by hand:

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .cursor/rules
cp ../harness-flow/.cursor/rules/harness-flow.mdc .cursor/rules/

# And expose the skills tree itself (the rule references skills/ paths):
ln -s ../harness-flow/skills .cursor/harness-flow-skills
```

Each `hf-*` skill is self-contained, so a `cp -R ../harness-flow/skills .cursor/harness-flow-skills` is also fine if you don't want a symlink. The rule looks for `skills/using-hf-workflow/SKILL.md` and `skills/hf-workflow-router/SKILL.md` relative to the workspace root, so make sure those paths resolve (either via the symlink above, or by keeping `skills/` at the project root). The install script automates this and also writes a manifest for clean uninstall.

## 2. The shipped rule

`.cursor/rules/harness-flow.mdc` (frontmatter: `alwaysApply: true`) tells Cursor:

1. Load `skills/using-hf-workflow/SKILL.md` as the entry shell on every session.
2. Hand off to `skills/hf-workflow-router/SKILL.md` whenever the user's intent is ambiguous, when a review/gate just finished, or when artifacts conflict.
3. Honor HarnessFlow's hard rules: one `Current Active Task` at a time, approvals and gates are first-class nodes, evidence-based routing (not chat memory), author/reviewer separation.

You should NOT replace this rule with a bespoke "HF cheatsheet" — Cursor will silently de-prioritize the actual `SKILL.md` content if you summarize it. The rule exists to **dispatch**, not to mirror skill content.

## 3. Verify the install

In Cursor, ask:

> Use HarnessFlow from this repo. Load `using-hf-workflow` and route me through the correct HF workflow. I want to add rate limiting to our notifications API. Do not jump straight to code.

Expected behavior:

1. Cursor reads `skills/using-hf-workflow/SKILL.md`.
2. Hands off to `skills/hf-workflow-router/SKILL.md`.
3. For a feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify` (depending on what evidence already exists).

If Cursor jumps straight into `hf-test-driven-dev` without an approved spec / design / tasks chain, that is a **bug** — please open an issue.

## 4. Mapping from natural-language intent to HF nodes

Cursor doesn't ship HF slash commands in v0.5.0 (commands are bias and conflict-prone across packs; the router's evidence-based selection is sufficient for main-chain work, and `hf-release` has its own NL bias row in the entry shell). This is the same shape as OpenCode integration. Use natural language:

| Intent | Selected node |
|---|---|
| "I'm not sure where we are, route me." | `using-hf-workflow` → `hf-workflow-router` (default entry) |
| "Write / revise the spec for X." | `hf-specify` (after upstream discovery preconditions) |
| "Plan this — design and tasks." | `hf-design` (and `hf-ui-design` when the spec declares a UI surface) → `hf-tasks` |
| "Implement the current active task with TDD." | `hf-test-driven-dev` (only when one `Current Active Task` is locked) |
| "Verify the UI in a browser." | `hf-browser-testing` (after `hf-test-driven-dev` GREEN, when the spec declares a UI surface) |
| "Review the [spec / design / UI / tasks / tests / code / traceability]." | corresponding `hf-*-review` |
| "Close out this task / workflow." | `hf-completion-gate` → `hf-finalize` |
| "Production defect, hotfix needed." | `hf-hotfix` |
| "Scope change, re-enter the workflow." | `hf-increment` |
| **"Cut a release / tag vX.Y.Z / write release notes."** | **direct invoke** `hf-release` (does **not** go through `hf-workflow-router`; ADR-004 D3). Engineer-level release only — does **not** deploy or staged-rollout. |

Hard rule: the first 9 intents are **bias**, not bypass — the router inspects on-disk artifacts and routes to the correct upstream node if preconditions are missing. The "cut a release" intent is the exception: the entry shell direct-invokes `hf-release`, which has its own internal Hard Gates (candidate features must be `workflow-closeout`, release-wide regression must be fresh, no auto `git tag`).

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| Cursor ignores HF and writes code directly | Re-prompt explicitly: "Use HarnessFlow. Load `using-hf-workflow` first." Then verify `.cursor/rules/harness-flow.mdc` exists and has `alwaysApply: true`. |
| Cursor says "no rule loaded" | The rule file lives in `.cursor/rules/` (lowercase, plural `rules/`); files in `.cursorrules` (legacy single-file format) are not recommended for HF. |
| Skills reference broken paths | Ensure `skills/` is reachable from the project root (or symlinked under `.cursor/harness-flow-skills` when vendoring). |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md`. |
| `hf-test-driven-dev` keeps refusing to start | No `Current Active Task` is locked; ask the router to plan first (NL: "plan this — design and tasks"). |
| `hf-finalize` keeps bouncing back | A gate (regression / doc-freshness / completion) failed; follow the canonical next action it returned. |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue. |

## 6. What is NOT included in v0.5.0

Per ADR-001 D1 + ADR-002 D1 / D11 + ADR-003 D2 / D3 / D6 + ADR-004 D2 / D3 (P-Honest, "narrow but hard"):

- All 6 originally-deferred ops/release skills (`hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`) remain out of scope. v0.4.0 added a **new** skill `hf-release` (release-tier engineer-level version cut), and v0.5.0 added a **closeout HTML companion report** to `hf-finalize` — neither is one of the 6 original deferred ops/release skills, and neither replaces `hf-shipping-and-launch`; all three slices are orthogonal (closeout reviewer experience vs. version cut vs. ship to production).
- `hf-release` does **not** enter the router transition map — it is a release-tier standalone skill, decoupled from the main chain (ADR-004 D3).
- `hf-release` does **not** auto-execute `git tag` or `git push --tags`. The skill produces a readiness pack only; tag operations are project-maintainer actions.
- No HF-specific slash commands on Cursor (use natural language; the entry shell direct-invokes `hf-release` for release intents, the router picks the leaf skill for everything else). This matches OpenCode integration; Claude Code's 7 short slash commands are a Claude-Code-specific decision (ADR-001 D4 + ADR-004 D4) and are not replicated to Cursor (ADR-003 D6).
- No 4-client expansion (Gemini CLI / Windsurf / GitHub Copilot / Kiro) — Cursor was added in v0.3.0; the other 4 stay deferred to v0.6+.
- No 3 user-facing personas (`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — ADR-002 D11 revoked; ADR-003 D3 / ADR-004 / ADR-005 D5 keep deferred to v0.6+.
- The SKILL.md anatomy audit script `scripts/audit-skill-anatomy.py` is **advisory** (does not block PR merge in maintainer workflows); ADR-003 D8 / ADR-004 keep this stance.
- Real-environment Cursor install smoke is **not** a release hard gate (ADR-003 D7 / ADR-004 inherits). The first-time real Cursor verification is performed by users in their own Cursor environment; `CONTRIBUTING.md` "Known Limitations" carries this gap explicitly.

These constraints are intentional. They keep the v0.5.0 surface small enough to be honest about what the release actually covers (1 closeout HTML companion report + 1 new stdlib-only render script, no new skills, no new clients, no new personas, no new ops skills).

## 7. Cross-references

- ADR-004 (v0.4.0 release scope: hf-release standalone skill + /release command): `docs/decisions/ADR-004-hf-release-skill.md`
- ADR-005 (v0.5.0 release scope: hf-finalize closeout HTML companion + skills/hf-finalize/scripts/render-closeout-html.py): `docs/decisions/ADR-005-release-scope-v0.5.0.md`
- ADR-003 (v0.3.0 release scope decisions): `docs/decisions/ADR-003-release-scope-v0.3.0.md`
- ADR-002 (v0.2.0 release scope, with D11 narrowing): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- ADR-001 (v0.1.0 release scope): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- Other supported client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md`
- Cursor docs on rules: <https://docs.cursor.com/context/rules>

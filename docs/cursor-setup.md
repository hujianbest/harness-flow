# HarnessFlow on Cursor

HarnessFlow v0.3.0 supports Cursor through Cursor's **rules** mechanism. Skills are plain Markdown, so the same `skills/` tree that ships in this repository is consumed by Cursor as a project-level (or globally-registered) `alwaysApply` rule that points the agent at the canonical entry shell + router.

> **Scope (v0.3.0 pre-release).** v0.3.0 officially supports 3 clients: **Claude Code**, **OpenCode**, and **Cursor** (newly added in this release). The 4 remaining client expansions (Gemini CLI / Windsurf / GitHub Copilot / Kiro) stay deferred to v0.4+. The HarnessFlow main chain still ends at `hf-finalize` (engineering-level closeout); v0.3.0 added **no** new `hf-*` skills and **no** personas, so release pipelines / deployment / monitoring / security hardening / performance gating / debugging-and-error-recovery / deprecation-and-migration remain out of scope. See `docs/decisions/ADR-003-release-scope-v0.3.0.md` D1 / D2 / D3.

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

### B. Vendor HarnessFlow into your own project

If you want HarnessFlow available inside another repository:

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .cursor/rules
cp ../harness-flow/.cursor/rules/harness-flow.mdc .cursor/rules/

# And expose the skills tree itself (the rule references skills/ paths):
ln -s ../harness-flow/skills .cursor/harness-flow-skills
```

Each `hf-*` skill is self-contained, so a `cp -R ../harness-flow/skills .cursor/harness-flow-skills` is also fine if you don't want a symlink. The rule looks for `skills/using-hf-workflow/SKILL.md` and `skills/hf-workflow-router/SKILL.md` relative to the workspace root, so make sure those paths resolve (either via the symlink above, or by keeping `skills/` at the project root).

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

Cursor doesn't ship HF slash commands in v0.3.0 (commands are bias and conflict-prone across packs; the router's evidence-based selection is sufficient). This is the same shape as OpenCode integration. Use natural language:

| Intent | Router selects |
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

Hard rule: every intent above is a **bias**, not a bypass. The router still inspects on-disk artifacts and routes to the correct upstream node if preconditions are missing.

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

## 6. What is NOT included in v0.3.0

Per ADR-001 D1 + ADR-002 D1 / D11 + ADR-003 D2 / D3 / D6 (P-Honest, "narrow but hard"):

- 6 deferred ops/release skills remain out of scope (`hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`). v0.3.0 introduced no new `hf-*` skills (ADR-003 D2).
- No HF-specific slash commands on Cursor (use natural language; the router will pick the leaf skill). This matches OpenCode integration; Claude Code's 6 short slash commands are a Claude-Code-specific historical decision (ADR-001 D4) and are not replicated to Cursor (ADR-003 D6).
- No 4-client expansion (Gemini CLI / Windsurf / GitHub Copilot / Kiro) — ADR-003 D1 keeps them deferred to v0.4+; v0.3.0 only adds Cursor.
- No 3 user-facing personas (`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — ADR-002 D11 revoked, ADR-003 D3 keeps deferred to v0.4+.
- The SKILL.md anatomy audit script `scripts/audit-skill-anatomy.py` is **advisory** (does not block PR merge in maintainer workflows); ADR-003 D8 keeps this stance.
- Real-environment Cursor install smoke is **not** a release hard gate (ADR-003 D7). The first-time real Cursor verification is performed by users in their own Cursor environment; `CONTRIBUTING.md` "Known Limitations" carries this gap explicitly.

These constraints are intentional. They keep the v0.3.0 surface small enough to be honest about what the release actually covers (1 new client, no new skills, no new personas).

## 7. Cross-references

- ADR-003 (v0.3.0 release scope decisions): `docs/decisions/ADR-003-release-scope-v0.3.0.md`
- ADR-002 (v0.2.0 release scope, with D11 narrowing): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- ADR-001 (v0.1.0 release scope): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- Other supported client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md`
- Cursor docs on rules: <https://docs.cursor.com/context/rules>

# HarnessFlow on Cursor

HarnessFlow v0.2.0 supports Cursor through Cursor's **rules** mechanism. Skills are plain Markdown, so the same `skills/` tree that ships in this repository is consumed by Cursor as a set of project-level (or globally-registered) rule references.

> **Scope (v0.2.0 pre-release).** v0.2.0 officially supports 7 clients: Claude Code, OpenCode, Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro. The HarnessFlow main chain ends at `hf-finalize` (engineering-level closeout); release / ops / monitoring are intentionally still out of scope (only `hf-browser-testing` was added in v0.2.0). See ADR-002 D1 / D2.

## How Cursor sees HF skills

Cursor doesn't have native auto-discovery of skill packs. Instead it loads:

- **Project rules**: any file under `.cursor/rules/<name>.md` (or `<name>.mdc`) is auto-loaded for the workspace.
- **Always-on rules**: rules with `alwaysApply: true` frontmatter are injected on every turn.
- **AGENTS.md**: Cursor reads a top-level `AGENTS.md` for persistent context (HF does not require this — see "Why no `AGENTS.md` sidecar?" in `docs/opencode-setup.md`; the same reasoning applies here).

HarnessFlow keeps every `hf-*` skill self-contained under the top-level `skills/` directory. To make these reachable from Cursor's rule loader, ship a single project rule that points Cursor at the canonical entry skill plus the router.

## 1. Install

You have two install topologies. Pick whichever matches how you already use Cursor.

### A. Use the HarnessFlow repository directly

```bash
git clone https://github.com/hujianbest/harness-flow.git
cursor harness-flow
```

The repository ships `.cursor/rules/harness-flow.mdc` (created in v0.2.0; see below if you are vendoring HF into another project). Opening the repo in Cursor is enough.

### B. Vendor HarnessFlow into your own project

If you want HarnessFlow available inside another repository:

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .cursor/rules
cp ../harness-flow/.cursor/rules/harness-flow.mdc .cursor/rules/

# And expose the skills tree itself (Cursor reads files referenced by the rule):
ln -s ../harness-flow/skills .cursor/harness-flow-skills
```

Each `hf-*` skill is self-contained, so a `cp -R` is also fine if you don't want a symlink.

## 2. The shipped rule

`.cursor/rules/harness-flow.mdc` (frontmatter: `alwaysApply: true`) tells Cursor:

1. Load `skills/using-hf-workflow/SKILL.md` as the entry shell on every session.
2. Hand off to `skills/hf-workflow-router/SKILL.md` whenever the user's intent is ambiguous, when a review/gate just finished, or when artifacts conflict.
3. Honor HarnessFlow's hard rules: one `Current Active Task` at a time, approvals and gates are first-class nodes, evidence-based routing (not chat memory).

You should NOT replace this rule with a bespoke "HF cheatsheet" — Cursor will silently de-prioritize the actual `SKILL.md` content if you summarize it.

## 3. Verify the install

In Cursor, ask:

> Use HarnessFlow from this repo. Load `using-hf-workflow` and route me through the correct HF workflow. I want to add rate limiting to our notifications API. Do not jump straight to code.

Expected:

1. Cursor reads `skills/using-hf-workflow/SKILL.md`.
2. Hands off to `skills/hf-workflow-router/SKILL.md`.
3. For a feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify`.

If Cursor jumps straight into `hf-test-driven-dev` without an approved spec/design/tasks chain, that is a **bug** — please open an issue.

## 4. Mapping from natural-language intent to HF nodes

Cursor doesn't ship slash commands for HF in v0.2.0 (commands are bias and conflict-prone across packs; the router's evidence-based selection is sufficient). Use natural language:

| Intent | Router selects |
|---|---|
| "I'm not sure where we are, route me." | `using-hf-workflow` → `hf-workflow-router` (default entry) |
| "Write / revise the spec for X." | `hf-specify` (after upstream discovery preconditions) |
| "Plan this — design and tasks." | `hf-design` (and `hf-ui-design` when spec declares a UI surface) → `hf-tasks` |
| "Implement the current active task with TDD." | `hf-test-driven-dev` (only when one `Current Active Task` is locked) |
| "Verify the UI in a browser." | `hf-browser-testing` (after `hf-test-driven-dev` GREEN, when spec declares UI surface) |
| "Review the [spec / design / UI / tasks / tests / code / traceability]." | corresponding `hf-*-review` |
| "Close out this task / workflow." | `hf-completion-gate` → `hf-finalize` |
| "Production defect, hotfix needed." | `hf-hotfix` |
| "Scope change, re-enter the workflow." | `hf-increment` |

Hard rule: every intent above is a **bias**. The router still inspects on-disk artifacts and routes to the correct upstream node if preconditions are missing.

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| Cursor ignores HF and writes code directly | Re-prompt explicitly: "Use HarnessFlow. Load `using-hf-workflow` first." Then verify `.cursor/rules/harness-flow.mdc` exists and has `alwaysApply: true`. |
| Cursor says "no rule loaded" | The rule file lives in `.cursor/rules/` (lowercase, plural `rules/`); files in `.cursorrules` (legacy) are not recommended. |
| Skills reference broken paths | Ensure `skills/` is reachable from the project root (or symlinked). |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md`. |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue. |

## 6. What is NOT included in v0.2.0

Per ADR-002 D1:

- Only `hf-browser-testing` was added in v0.2.0; the other 6 ops/release skills (`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`) stay deferred to v0.3+.
- No HF-specific slash commands on Cursor (use natural language; the router will pick the leaf skill).

## 7. Cross-references

- ADR-002 (v0.2.0 release scope decisions): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- Other client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/gemini-cli-setup.md` / `docs/windsurf-setup.md` / `docs/copilot-setup.md` / `docs/kiro-setup.md`
- Cursor docs on rules: <https://docs.cursor.com/context/rules>

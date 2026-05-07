# HarnessFlow on Windsurf

HarnessFlow v0.2.0 supports Windsurf through Windsurf's **rules** mechanism. Skills are plain Markdown, so the same `skills/` tree consumed by Claude Code / Cursor / OpenCode is consumed by Windsurf as a rule reference.

> **Scope (v0.2.0 pre-release).** v0.2.0 officially supports 7 clients: Claude Code, OpenCode, Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro. Main chain ends at `hf-finalize` (engineering-level closeout); only `hf-browser-testing` was added in v0.2.0 from the deferred ops list. See ADR-002 D1 / D2.

## How Windsurf sees HF skills

Windsurf doesn't auto-discover skill packs. Instead it loads:

- **Workspace rules**: `.windsurf/rules.md` (or `.windsurfrules`, legacy) — auto-loaded for the workspace.
- **Global rules**: `~/.codeium/windsurf/memories/` — applied across projects.

HarnessFlow keeps every `hf-*` skill self-contained under the top-level `skills/` directory. To make these reachable from Windsurf, ship a single workspace rule that points Windsurf at the canonical entry skill plus the router.

## 1. Install

You have two install topologies.

### A. Use the HarnessFlow repository directly

```bash
git clone https://github.com/hujianbest/harness-flow.git
windsurf harness-flow   # or: open the folder via the Windsurf UI
```

The repository ships `.windsurf/rules.md` (created in v0.2.0). Opening the repo in Windsurf is enough.

### B. Vendor HarnessFlow into your own project

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .windsurf
cp ../harness-flow/.windsurf/rules.md .windsurf/

# And expose the skills tree itself:
ln -s ../harness-flow/skills .windsurf/harness-flow-skills
```

Each `hf-*` skill is self-contained; `cp -R` is also fine if you don't want a symlink.

## 2. The shipped rule

`.windsurf/rules.md` (auto-loaded on every session) tells Windsurf:

1. Load `skills/using-hf-workflow/SKILL.md` as the entry shell.
2. Hand off to `skills/hf-workflow-router/SKILL.md` whenever intent is ambiguous, a review/gate just finished, or artifacts conflict.
3. Honor HarnessFlow's hard rules: one `Current Active Task` at a time, approvals and gates are first-class nodes, evidence-based routing.

Do not replace this rule with a bespoke "HF cheatsheet" — Windsurf will silently de-prioritize the actual `SKILL.md` content if you summarize it.

## 3. Verify the install

In Windsurf, ask:

> Use HarnessFlow from this repo. Load `using-hf-workflow` and route me through the correct HF workflow. I want to add rate limiting to our notifications API. Do not jump straight to code.

Expected:

1. Windsurf reads `skills/using-hf-workflow/SKILL.md`.
2. Hands off to `skills/hf-workflow-router/SKILL.md`.
3. For a feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify`.

If Windsurf jumps straight into `hf-test-driven-dev` without an approved spec/design/tasks chain, that is a **bug** — please open an issue.

## 4. Mapping from natural-language intent to HF nodes

Windsurf doesn't ship slash commands for HF in v0.2.0. Use natural language; the router selects:

| Intent | Router selects |
|---|---|
| "I'm not sure where we are, route me." | `using-hf-workflow` → `hf-workflow-router` |
| "Write / revise the spec for X." | `hf-specify` (after upstream discovery) |
| "Plan this — design and tasks." | `hf-design` (and `hf-ui-design` when UI surface declared) → `hf-tasks` |
| "Implement the current active task with TDD." | `hf-test-driven-dev` |
| "Verify the UI in a browser." | `hf-browser-testing` (post-GREEN, UI surface only) |
| "Review the [spec / design / UI / tasks / tests / code / traceability]." | corresponding `hf-*-review` |
| "Close out this task / workflow." | `hf-completion-gate` → `hf-finalize` |
| "Production defect, hotfix needed." | `hf-hotfix` |
| "Scope change, re-enter the workflow." | `hf-increment` |

Hard rule: every intent above is a **bias**. The router still inspects on-disk artifacts.

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| Windsurf ignores HF and writes code directly | Re-prompt: "Use HarnessFlow. Load `using-hf-workflow` first." Verify `.windsurf/rules.md` exists. |
| Windsurf says "no rule loaded" | The rule file lives in `.windsurf/rules.md`; legacy `.windsurfrules` may also work but newer Windsurf expects `.windsurf/`. |
| Skills reference broken paths | Ensure `skills/` is reachable from the project root (or symlinked). |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md`. |

## 6. What is NOT included in v0.2.0

Per ADR-002 D1:

- Only `hf-browser-testing` was added in v0.2.0; 6 other ops/release skills stay deferred to v0.3+.
- No HF-specific slash commands on Windsurf.

## 7. Cross-references

- ADR-002 (v0.2.0 release scope decisions): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- Other client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/cursor-setup.md` / `docs/gemini-cli-setup.md` / `docs/copilot-setup.md` / `docs/kiro-setup.md`
- Windsurf docs on rules: <https://docs.codeium.com/windsurf/memories#workspace-rules>

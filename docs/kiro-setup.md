# HarnessFlow on Kiro IDE & CLI

HarnessFlow v0.2.0 supports Kiro through Kiro's native **skills** system. Kiro reads `SKILL.md` files from `.kiro/skills/` (project) and `~/.kiro/skills/` (global), so the same `skills/` tree HarnessFlow ships is consumed natively.

> **Scope (v0.2.0 pre-release).** v0.2.0 officially supports 7 clients: Claude Code, OpenCode, Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro. Main chain ends at `hf-finalize` (engineering-level closeout); only `hf-browser-testing` was added in v0.2.0. See ADR-002 D1 / D2.

## How Kiro discovers HF skills

Kiro auto-discovers skills from these locations (per [kiro.dev/docs/skills](https://kiro.dev/docs/skills/)):

- `.kiro/skills/<name>/SKILL.md` (project-local)
- `~/.kiro/skills/<name>/SKILL.md` (global)

Kiro also supports `AGENTS.md` for persistent context. HarnessFlow does NOT require an `AGENTS.md` sidecar (same reasoning as the OpenCode setup; see `docs/opencode-setup.md` § "Why no AGENTS.md sidecar?").

HarnessFlow keeps every `hf-*` skill self-contained under the top-level `skills/` directory. To make these discoverable to Kiro, ship a symlink from `.kiro/skills` to `skills/` (or copy the directory).

## 1. Install

You have three install topologies.

### A. Use the HarnessFlow repository directly

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
# The repo ships .kiro/skills -> ../skills as a symlink (created in v0.2.0).
kiro .
```

### B. Vendor HarnessFlow skills into your own project

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .kiro
cp -R ../harness-flow/skills .kiro/skills

# Or, to track upstream automatically:
ln -s ../harness-flow/skills .kiro/skills
```

Each `hf-*` skill is self-contained (its `SKILL.md`, `references/`, and `evals/` ship together), so a plain `cp -R` is enough.

### C. Install HarnessFlow globally for every Kiro session

```bash
mkdir -p ~/.kiro/skills
cp -R /path/to/harness-flow/skills/* ~/.kiro/skills/
```

Project-local copies win on name collision.

## 2. Verify the install

In Kiro, run the equivalent of `/skills` (Kiro's built-in skill listing):

You should see at least 24 skills:

- `using-hf-workflow`
- `hf-workflow-router`
- `hf-product-discovery`, `hf-discovery-review`
- `hf-specify`, `hf-spec-review`
- `hf-design`, `hf-ui-design`, `hf-design-review`, `hf-ui-review`
- `hf-tasks`, `hf-tasks-review`
- `hf-test-driven-dev`, `hf-test-review`
- `hf-code-review`, `hf-traceability-review`
- `hf-regression-gate`, `hf-doc-freshness-gate`, `hf-completion-gate`
- `hf-finalize`
- `hf-hotfix`, `hf-increment`, `hf-experiment`
- **`hf-browser-testing`** (new in v0.2.0)

If the list is empty, see [§5 Troubleshooting](#5-troubleshooting).

## 3. Mapping from natural-language intent to HF nodes

Kiro doesn't ship slash commands for HF in v0.2.0. Use natural language; the router selects:

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

## 4. Recommended first prompt

```text
Use HarnessFlow from this repo. Load `using-hf-workflow` via the skill tool and
route me through the correct HF workflow. I want to add rate limiting to our
notifications API. Do not jump straight to code.
```

Expected:

1. Kiro calls its skill loader on `using-hf-workflow`.
2. Hands off to `hf-workflow-router`.
3. For a new feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify`.

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| Skill listing shows no `hf-*` entries | The current project has no `.kiro/skills/`, **and** there are no skills under `~/.kiro/skills/`. Re-do step 1 (one of A / B / C). |
| Some skills missing, others present | Skill name collision across discovery locations — Kiro requires unique names. Remove duplicates from one of the locations. |
| Symlink `.kiro/skills -> ../skills` broken | Restore with `ln -snf ../skills .kiro/skills` from the harness-flow repo root. |
| Kiro ignores HF and writes code directly | Re-prompt: "Use HarnessFlow. Load `using-hf-workflow` first." |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md`. |

## 6. What is NOT included in v0.2.0

Per ADR-002 D1 / D2:

- Only `hf-browser-testing` was added in v0.2.0; 6 other ops/release skills stay deferred to v0.3+.
- No HF-specific slash commands on Kiro.

## 7. Cross-references

- ADR-002 (v0.2.0 release scope decisions): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- Other client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/cursor-setup.md` / `docs/gemini-cli-setup.md` / `docs/windsurf-setup.md` / `docs/copilot-setup.md`
- Kiro skills documentation: <https://kiro.dev/docs/skills/>

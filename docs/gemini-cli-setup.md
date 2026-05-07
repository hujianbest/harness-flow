# HarnessFlow on Gemini CLI

HarnessFlow v0.2.0 supports Gemini CLI through Gemini CLI's native **skills** + **commands** systems. Skills are auto-discovered via `gemini skills install`, and 6 short slash commands map to the same biases that Claude Code ships, with one rename to avoid a Gemini CLI internal conflict.

> **Scope (v0.2.0 pre-release).** v0.2.0 officially supports 7 clients: Claude Code, OpenCode, Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro. Main chain ends at `hf-finalize` (engineering-level closeout); only `hf-browser-testing` was added in v0.2.0. See ADR-002 D1 / D2.

## How Gemini CLI sees HF skills

Gemini CLI auto-discovers skills installed via:

- `gemini skills install <git URL or local path>` — installs skills under the user's Gemini config dir.
- `.gemini/skills/<name>/SKILL.md` — project-local skills.
- `.gemini/commands/<command>.md` — project-local slash commands.

HarnessFlow's `skills/` directory is consumed natively by Gemini CLI's skill loader. The repository also ships 6 slash commands under `.gemini/commands/`.

## 1. Install

You have two install topologies.

### A. Use the HarnessFlow repository directly

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
gemini skills install ./skills/
```

The repository ships `.gemini/commands/` × 6 (created in v0.2.0). Opening the repo with Gemini CLI picks them up.

### B. Install from the public HarnessFlow repo

```bash
gemini skills install https://github.com/hujianbest/harness-flow.git --path skills
```

This installs all 24 skills (22 `hf-*` + `using-hf-workflow` + `hf-browser-testing`) globally.

For slash commands, copy `.gemini/commands/` into your project:

```bash
mkdir -p .gemini/commands
cp /path/to/harness-flow/.gemini/commands/*.md .gemini/commands/
```

## 2. Slash commands (6)

| Command | Bias | Notes |
|---|---|---|
| `/hf` | route-first default — `using-hf-workflow` → `hf-workflow-router` | Use this when intent is unclear. |
| `/spec` | `hf-specify` | Spec authoring or revision; router validates upstream discovery first. |
| `/planning` | `hf-design` (and `hf-ui-design` when UI surface declared) → `hf-tasks` | **Note**: this command is `/planning`, not `/plan`, because Gemini CLI ships an internal `/plan` command. ADR-002 D2 sub-decision. |
| `/build` | `hf-test-driven-dev` | Only when one Current Active Task is locked. |
| `/review` | router dispatches to the matching `hf-*-review` | Covers spec / design / UI / tasks / tests / code / traceability / discovery review. |
| `/ship` | `hf-completion-gate` → `hf-finalize` | Closeout; gate decides if finalize can run. |

Hard rule: every command above is a **bias**, not a bypass. The router still inspects on-disk artifacts and routes to the correct upstream node if preconditions are missing.

Cut from v0.1.0 / v0.2.0:

- `/hotfix` — use natural language ("Production defect, hotfix needed.") + `/hf` and let the router branch into `hf-hotfix`.
- `/gate` — gates are pulled by the canonical next action of upstream nodes, not pushed by the user.

## 3. Verify the install

After install, run:

```bash
gemini skills list | grep -E "hf-|using-hf"
```

You should see at least 24 entries:

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

For commands:

```bash
gemini commands list | grep -E "/hf|/spec|/planning|/build|/review|/ship"
```

## 4. Recommended first prompt

```text
/hf I want to add rate limiting to our notifications API. Do not jump straight to code.
```

Expected behavior:

1. Gemini CLI invokes `using-hf-workflow`.
2. Hands off to `hf-workflow-router`.
3. For a new feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify`.

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| `/plan` doesn't trigger HF | HF on Gemini CLI uses `/planning`, not `/plan`, to avoid Gemini CLI's internal command. Use `/planning`. |
| Skill listing shows no `hf-*` entries | Re-run `gemini skills install` (step 1). |
| Some skills missing, others present | Skill name collision — Gemini CLI requires unique names across all install locations. |
| Gemini ignores HF and writes code directly | Re-prompt with `/hf` first; verify skills + commands are both installed. |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md`. |

## 6. What is NOT included in v0.2.0

Per ADR-002 D1 / D2:

- Only `hf-browser-testing` was added in v0.2.0; 6 other ops/release skills stay deferred to v0.3+.
- No `/plan` (renamed to `/planning` to avoid Gemini CLI internal conflict).
- No `/hotfix` / `/gate` (cut by ADR-001 D4 and kept cut by ADR-002).

## 7. Cross-references

- ADR-002 (v0.2.0 release scope decisions): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- Other client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/cursor-setup.md` / `docs/windsurf-setup.md` / `docs/copilot-setup.md` / `docs/kiro-setup.md`
- Gemini CLI skills documentation: <https://github.com/google-gemini/gemini-cli>

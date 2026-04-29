# Claude Code setup

HarnessFlow ships first-class support for **Claude Code** in v0.1.0. This guide gets you from zero to a working `/hf` prompt in under a minute.

> **Scope reminder.** v0.1.0 supports **Claude Code + OpenCode only** (per [`ADR-001-release-scope-v0.1.0.md`](../docs/decisions/ADR-001-release-scope-v0.1.0.md) D3). Other clients (Cursor / Gemini CLI / Windsurf / Copilot / Kiro) are deferred to v0.2+; the repository remains usable from those clients but is not on the v0.1.0 supported-platform promise list.

## Requirements

- Claude Code **v2.1.77 or later** (older versions reject the modern `marketplace.json` schema; see [anthropics/claude-code#34369](https://github.com/anthropics/claude-code/issues/34369))
- Network access to `github.com/hujianbest/harness-flow`

## Install — option 1: marketplace (recommended)

```text
/plugin marketplace add hujianbest/harness-flow
/plugin install harness-flow@harness-flow
```

You should now see the 6 short-alias commands in `/help`:

| Command | When to use |
|---|---|
| `/hf` | Default entry. HF routes by artifacts; use when current node / next-step is unclear. |
| `/spec` | No approved spec yet, or current spec needs revision. |
| `/plan` | Approved spec → design and/or task plan. Router resolves design vs tasks. |
| `/build` | Unique current active task selected; implement under gated TDD. |
| `/review` | Any artifact ready for an independent review. |
| `/ship` | Closeout (task or workflow). NOT a deployment trigger. |

## Install — option 2: local clone

If you want to hack on HF itself, or your environment cannot reach the marketplace:

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
claude --plugin-dir "$(pwd)"
```

This gives you the same 6 commands plus the full `skills/` tree with no `git pull` overhead between iterations.

## What gets registered

The repository contains:

- `.claude-plugin/marketplace.json` — registers `harness-flow` v0.1.0 as a Claude Code marketplace.
- `.claude-plugin/plugin.json` — plugin manifest pointing at `commands` and `skills`.
- `.claude/commands/{hf,spec,plan,build,review,ship}.md` — the 6 slash command bodies.
- `skills/` — the 23 `hf-*` workflow skills + `using-hf-workflow` public entry.

Claude Code auto-loads any `SKILL.md` directly under `skills/`; no manual import is needed.

## First run smoke test

After install, in any project where you want HF discipline:

```text
/hf
```

You should see HF reply with:

1. An entry classification line (`direct invoke` or `route-first`).
2. A target skill (e.g. `using-hf-workflow → hf-workflow-router`).
3. A 1-2 line "why" tied to current artifacts (or to the absence of any HF feature folder, in a fresh project).

That confirms the plugin is active and the `using-hf-workflow` entry skill is reachable.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `/plugin marketplace add` fails with a schema error mentioning `plugins.N.source` | Claude Code older than v2.1.77 | Upgrade Claude Code |
| `/hf` is not listed in `/help` | Plugin not enabled, or commands directory not loaded | `/plugin list` to verify; reinstall if missing |
| HF answers without invoking `using-hf-workflow` | The plugin's `skills/` was not auto-discovered | Verify `.claude-plugin/plugin.json` ships `"skills": "./skills/"`; check that the SKILL.md files exist under `skills/using-hf-workflow/` |
| All commands appear but always answer "I cannot find HF artifacts" | Working in a project that has not yet started any HF feature | Expected — `/hf` will route you to `hf-product-discovery` or `hf-specify` to begin one |

## What HF will and will not do

HF's behavioral contract lives in [`docs/principles/soul.md`](../docs/principles/soul.md) (the constitution layer). Two non-negotiable rules to know up front:

- HF will **not** pick direction / trade-offs / acceptance standards on your behalf — those are the architect's responsibility. It will surface them back as explicit questions instead.
- HF will **not** self-approve completion. Every "done" verdict comes from an independent gate (`hf-completion-gate`) writing a record to disk, not from a chat statement.

If you need that to be different, edit `soul.md` for your fork — but be aware that most other HF behaviors (review separation, fresh-evidence requirements, gate-based completion) descend from these two rules.

## Next

- Read [`README.md`](../README.md) for the full v0.1.0 scope and the methodology lineage.
- Run [`examples/writeonce/`](../examples/writeonce/) once it lands (see [PR-D in the v0.1.0 plan](../docs/decisions/ADR-001-release-scope-v0.1.0.md)).
- Open an issue if any of the 6 commands routed somewhere unexpected — `/hf` is supposed to be the safe default.

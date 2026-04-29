# OpenCode setup

HarnessFlow ships first-class support for **OpenCode** in v0.1.0. Setup is slightly more manual than Claude Code because OpenCode does not have a unified marketplace concept yet — you point OpenCode at this repository and it discovers everything else.

> **Scope reminder.** v0.1.0 supports **Claude Code + OpenCode only** (per [`ADR-001-release-scope-v0.1.0.md`](../docs/decisions/ADR-001-release-scope-v0.1.0.md) D3). Other clients are deferred to v0.2+.

## Requirements

- A recent OpenCode build with the native `skill` tool (any version that lists "Agent Skills" under [`opencode.ai/docs/skills`](https://opencode.ai/docs/skills) is fine)
- Network access to clone `github.com/hujianbest/harness-flow`

## Install

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
opencode
```

That's it. OpenCode's discovery picks everything up automatically:

- The 24 SKILL.md files under `skills/` are discovered via the `skills.paths` entry in [`opencode.json`](../opencode.json).
- The 6 short-alias commands (`/hf` `/spec` `/plan` `/build` `/review` `/ship`) are discovered from `.opencode/commands/*.md`.

You should see HF skills listed when you run any prompt that triggers the `skill` tool's tool-listing, and the 6 commands appear in OpenCode's command palette.

## What gets registered

The repository contains:

- `opencode.json` — declares `skills.paths: ["./skills"]` so OpenCode loads the full HF skill tree, and `permission.skill: { "*": "allow" }` so HF skills load without per-skill prompts.
- `.opencode/commands/{hf,spec,plan,build,review,ship}.md` — the 6 slash command bodies for OpenCode (kept byte-identical to `.claude/commands/*.md`; see "Why two copies" below).
- `skills/` — the 23 `hf-*` workflow skills + `using-hf-workflow` public entry.

## First run smoke test

In any project where you want HF discipline, from a working directory **inside** the cloned `harness-flow` repo (or any project where this repo has been added as a git submodule under `skills/`):

```text
/hf
```

You should see HF reply with:

1. An entry classification (`direct invoke` or `route-first`).
2. A target skill (e.g. `using-hf-workflow → hf-workflow-router`).
3. A 1-2 line "why" tied to current artifacts (or to the absence of any HF feature folder, in a fresh project).

That confirms the skill discovery and the 6 commands are wired correctly.

## Use HF in a different project

OpenCode walks up from your working directory to the git worktree root looking for skills. To use HF in a project of yours without forking the repo, the simplest options are:

1. **Submodule** the HF repo under your project, then OpenCode discovers `skills/<your-submodule-path>/skills/*/SKILL.md` automatically.
2. **Clone HF globally** and add HF's `skills/` to your `~/.config/opencode/opencode.json`:

   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "skills": {
       "paths": ["/absolute/path/to/harness-flow/skills"]
     },
     "permission": {
       "skill": {
         "*": "allow"
       }
     }
   }
   ```

   Then copy the 6 command files into `~/.config/opencode/commands/` so the slash commands are also globally available.

3. **Per-project copy** of just the bits you need: copy `.opencode/commands/` and add a `skills.paths` entry in your project's `opencode.json` pointing at HF's `skills/` directory. Useful when you want to pin to a specific HF git ref.

## Why two copies of the command files (`.claude/` and `.opencode/`)

OpenCode discovers commands from `.opencode/commands/`, while Claude Code discovers them from `.claude/commands/`. Both clients use a near-identical markdown + YAML frontmatter format, so the 6 command bodies are byte-identical between the two directories.

If you fork HF and want to edit a command, edit **both** copies and keep them in sync. We do not maintain a script for this in v0.1.0 because the file count is fixed at 6 and the diff is trivially auditable. If the count grows in v0.2+, this is a candidate for automation.

## What HF will and will not do

HF's behavioral contract lives in [`docs/principles/soul.md`](../docs/principles/soul.md). Two non-negotiable rules to know up front:

- HF will **not** pick direction / trade-offs / acceptance standards on your behalf. It surfaces them back as explicit questions.
- HF will **not** self-approve completion. Every "done" verdict comes from an independent gate (`hf-completion-gate`) writing a record to disk.

## Optional: AGENTS.md

OpenCode reads `AGENTS.md` from your project root as global rules. HarnessFlow does **not** require an `AGENTS.md` (per the PR #21 decoupling: each SKILL.md is self-contained and does not depend on a sidecar). However, if you already maintain an `AGENTS.md`, you can add a one-liner like:

```md
This project uses HarnessFlow (https://github.com/hujianbest/harness-flow).
For any non-trivial change, use the `/hf` command (or one of /spec, /plan, /build, /review, /ship) before writing code.
```

That's all the bridging HF needs from `AGENTS.md`. If you do not maintain one, HF still works.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `/hf` is not listed | Working directory is outside the git worktree containing `.opencode/commands/` | `cd` into the cloned `harness-flow` repo, or copy the commands into `~/.config/opencode/commands/` for global use |
| HF skills not visible to the `skill` tool | `skills.paths` not configured | Verify `opencode.json` (project or global) has `skills: { paths: ["./skills"] }` (relative paths resolve against the config file location) |
| Skills load but `/hf` skips `using-hf-workflow` | Permission set to `ask` or `deny` for `using-hf-workflow` | Check `permission.skill` in `opencode.json`; the shipped value is `"*": "allow"` |
| OpenCode prompts for permission on every skill load | `permission.skill` not configured | Use the shipped `opencode.json` or set `"*": "allow"` in your own config |

## Next

- Read [`README.md`](../README.md) for the full v0.1.0 scope and the methodology lineage.
- Run [`examples/writeonce/`](../examples/writeonce/) once it lands (see PR-D in the v0.1.0 plan).
- Open an issue if a command routed somewhere unexpected.

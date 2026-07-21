# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A constraint-based workflow for building software products with AI agents: seven invariants, three user checkpoints, a product truth layout on disk — and full freedom of method inside those walls.**

HarnessFlow v4 is built on one first-principles observation: **constrain where verification is cheap, free where verification is expensive.** Whether a file exists on disk, whether a command exited 0, whether the user approved a decision — cheap to verify, so these become hard constraints. Whether the agent planned in the "right" order, used the "right" template, followed step 3.2 — expensive to verify and barely correlated with product quality, so v4 deliberately does not prescribe any of it. Given the right constraints, good ways of working emerge on their own; nobody needs to script them.

## The seven invariants

The constitution ([skills/harness/SKILL.md](skills/harness/SKILL.md)) is the only binding document. At any moment, restoring a violated invariant is the highest-priority work:

1. **Truth lives on disk.** Every persistent fact about the product — intent, state, decisions, evidence — lives in `product/` and `work/` files. Chat is scratch paper; any new session cold-starts from disk alone.
2. **Claims need evidence.** Every "it works / tests pass / it's fixed" must point to machine output produced by `harness.py run`, with a reproducible command. A claim without evidence did not happen.
3. **Signal before build.** Before the product changes, a falsifiable success signal exists in `work/<slug>/signal.md`. Its form is free — tests, smoke scripts, checkable UI states — but it precedes the implementation.
4. **The trunk stays green.** The verification entry recorded in `product/state.md` actually runs at all times. If it breaks, fixing it beats all new work.
5. **Decision rights are layered.** The user owns *what and whether* (intent, tradeoffs, external commitments, irreversible actions); the agent owns *how* (design, tools, order, method) and records significant choices in `product/decisions.md`. When ownership is unclear, it belongs to the user.
6. **Independent perspective.** Nothing is declared done until a perspective that did not produce it has examined it — a fresh-context review or the user — with the verdict in `work/<slug>/review.md`. Authors don't grade their own homework.
7. **Reversibility first.** Prefer rollbackable paths; irreversible actions must pass the release checkpoint.

## The three checkpoints (all of user sovereignty)

| Checkpoint | When | What the agent brings |
|---|---|---|
| Intent | starting a product, or materially changing `product/intent.md` | the intent draft/diff, awaiting confirmation |
| Tradeoff | a choice will change user-visible behavior or conflicts with intent | options + a recommendation, awaiting the pick |
| Release | before anything irreversible or external | action + evidence + rollback plan, awaiting go |

Outside these three, the agent never asks permission — it acts. In auto mode the agent may exercise intent/tradeoff on the user's behalf per `intent.md` (recorded in `decisions.md`); the release checkpoint always waits for the user.

## Product truth layout

```
product/
  intent.md     who it's for, what problem, success markers, explicit non-goals — user-owned
  state.md      what the product does now, how to run it, the verification entry, known issues
  decisions.md  append-only decision log (date, decision, why, reversibility)
  backlog.md    candidate work and open questions
work/<slug>/    one directory per line of work
  signal.md     the falsifiable success signal (exists before implementation)
  evidence/     machine output from harness.py run (hand-editing = fabrication)
  review.md     the independent perspective's verdict
```

No file has a required internal format — write for the next cold-starting reader, not for a template.

## The evidence protocol

One stdlib-only script, [skills/harness/scripts/harness.py](skills/harness/scripts/harness.py), which records but never adjudicates:

```bash
# Create the product truth skeleton (never overwrites):
python3 skills/harness/scripts/harness.py init

# Run any command that backs a claim; raw output + exit code + content hash land on disk:
python3 skills/harness/scripts/harness.py run --work work/rate-limit --label signal-red -- pytest tests/

# Verify evidence integrity (recomputed hash must match; careless tampering fails loudly):
python3 skills/harness/scripts/harness.py check --work work/rate-limit
```

There is no `gate check --to <stage>` anymore — there are no stages. Risk scaling is emergent: a typo fix pays near-zero invariant cost; a data migration is naturally forced into specs, reviews and rollback plans by invariants 3, 6 and 7. That's a property of the constraint design, not a tier table.

## Playbooks (advice, never law)

`skills/harness/references/` ships four playbooks: [shaping](skills/harness/references/shaping.md) (idea → intent.md), [building](skills/harness/references/building.md) (increments & signals), [reviewing](skills/harness/references/reviewing.md) (how independent review works), [releasing](skills/harness/references/releasing.md) (release & consolidation). Deviating from a playbook needs no approval; violating an invariant is never allowed.

## Install

HarnessFlow is plain Markdown plus one stdlib-only Python script. For Cursor and OpenCode use the installer:

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
python scripts/install.py --target both --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

Add `--mode symlink` to have the target project follow this checkout.

- **Cursor**: installs skills under `.cursor/harness-flow-skills/` and writes a path-rewritten `.cursor/rules/harness-flow.mdc`.
- **Claude Code**: install as a plugin (`/plugin marketplace add <this repo>`), or vendor `skills/`.
- **OpenCode / others**: installs under `.opencode/skills/`, preserving user-defined skills.

Then just ask naturally: *"I want a CLI that publishes Markdown to my blog."* The agent loads the constitution, cold-starts from `product/`, and works freely within the invariants.

## Design principles

- **Constrain outcomes, not steps.** The framework verifies what's cheap to verify (files, exit codes, user approvals) and stays silent about method.
- **Evidence is machine output.** "All tests green" is prose; a hash-sealed log with an exit code is evidence.
- **Sovereignty is enumerable.** Exactly three checkpoints belong to the user; everything else is the agent's to decide — which is what makes autonomy safe.
- **Process overhead is emergent, not configured.** No risk tiers, no stage gates; the invariants price risk automatically.
- **The whole law fits in one read.** One constitution under 120 lines; playbooks are optional reading.

## License

MIT

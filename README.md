# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A harness that drives AI coding agents from a raw idea to a working app — and through everyday feature delivery: product-layer shaping + main-chain discipline (SDD + TDD) + mechanical gates + demo-gated acceptance + pluggable domain extensions.**

HarnessFlow is designed against four unreliable factors, and every mechanism derives from one of them:

1. **The model is unreliable** → mechanical gates: stage transitions are adjudicated by `hf_gate.py` from files, verdict lines, exit codes and timestamps; evidence can only be produced by wrapping real command runs. Narrative is never evidence.
2. **Intent is underspecified** → no silent gap-filling: whenever the user hasn't decided something, the agent proposes an opinionated default, records it in the `product/assumptions.md` ledger, and proceeds. Users can overturn any assumption later, triggering controlled rework.
3. **Sessions die** → all state lives on disk; `hf_gate.py status` cold-starts any new session (product layer state, per-feature stage, next step).
4. **Users don't read code** → demo-gated acceptance: user-perceivable slices can only ship with demo evidence (recording / screenshot / preview probe) plus an on-disk user acceptance. A user saying "looks good" to a spec is a cheap signal; reacting to the running product is the real one.

## Two entry paths

**Idea → App (greenfield).** The user brings an idea; there is no code yet. The path mirrors the classic software-engineering lifecycle — define the product, design the architecture, break down the requirements, then build and test each one:

```
shape (product definition) → architect (architecture + breakdown) → S-1 walking skeleton → slice loop ⟲ → evolve
```

- `hf-shape` runs a structured interview (who is it for / what pain / what does success look like / what's explicitly out) and produces `product/product.md` (vision, success criteria, MVP boundary, not-doing list) plus the decision/assumption ledgers.
- `hf-architect` makes the tech-stack decision from opinionated presets (non-technical users are never forced to pick a framework), sketches a **one-page `product/architecture.md`** (system shape, module boundaries, core data model, key flows, cross-cutting conventions), then breaks the MVP down into `backlog.md` — vertical, demoable slices that each map onto named modules and flows.
- `hf-skeleton` makes slice S-1 a walking skeleton: scaffold, one-command `dev`/`test`, one thinnest real end-to-end path, something the user can open on day 0. It is the first real validation of the architecture — integration risk surfaces immediately and the feedback loop starts before any feature work.
- Each subsequent slice runs the delivery chain and exits through a demo the user experiences; feedback flows back into the backlog, the ledgers, and the architecture map at ship time.

**Existing codebase delivery.** Requirements are known and code exists → enter directly at `hf-frame`. No product layer needed; projects with recurring delivery are encouraged to keep just a `product/architecture.md` codebase map (see `hf-architect`).

`architecture.md` doubles as the **codebase map**: every delivery-chain stage reads the map first and then only the relevant code — never a whole-repo rescan per feature. This is HarnessFlow's main token-saving mechanism, alongside on-demand skill loading, per-artifact line budgets, and passing subagents file paths instead of pasted contents. Each stage also carries its classic software-engineering activity (requirements engineering, architecture design, TDD, V&V, retrospective…), and the agent names that activity in one sentence at each stage transition — users learn software engineering by walking the graph, at a one-sentence token cost.

## The delivery chain, dual modes, and risk tiers

```
build mode (default): frame → plan → build → verify → ship
exploration mode:     frame → build → close      (disposable prototypes)
```

Mode is decided by one variable: **will the code be kept?** Build mode gets full discipline (TDD, reviews, evidence). Exploration mode is for validating a direction fast — tier 1 risk only, can never ship, closes with a `conclusion.md`; prototypes may only inform a rewrite, never be promoted.

| Stage | Skill | Output | Gate |
|-------|-------|--------|------|
| Shape | `hf-shape` | `product.md` (product definition) + ledgers | on-disk user confirmation |
| Architect | `hf-architect` | one-page `architecture.md` + sliced `backlog.md` | `gate check --product` |
| (S-1) | `hf-skeleton` | runnable app shell (via the delivery chain) | same as chain |
| Frame | `hf-frame` | `frame.md` — intent, mode, risk tier, user-perceivable flag, environment baseline | `gate check` |
| Plan | `hf-plan` | `plan.md` (tier 2) or `spec.md` + `design.md` (tier 3) | independent review + user confirmation + `gate check` |
| Build | `hf-build` | subagent-authored code + tests, one task at a time, red→green→refactor with per-task logs | all tasks checked + `gate check` |
| Verify | `hf-verify` | runtime smoke + independent code review + demo acceptance | `gate check` |
| Ship | `hf-ship` | acceptance traced to every requirement, feedback written back to the product layer | all criteria closed |

Process overhead scales with risk: **tier 1** (micro changes) runs frame → build → verify → ship; **tier 2** (default) uses a single `plan.md`; only **tier 3** (data / security / cross-module) splits spec from design with three review rounds. Under-tiering is a blocking review finding.

All artifacts and evidence live in `product/` and `features/<NNN>-<slug>/` (`frame.md`, `plan.md`, `progress.md`, `evidence/`, `reviews/`). Any new session recovers with one command — never from chat memory.

## Mechanical gates

```bash
gate=skills/hf-workflow/scripts/hf_gate.py
python3 $gate init                     # scaffold the product layer (greenfield first step)
python3 $gate status                   # cold-start recovery: product layer + per-feature stage + next step
python3 $gate next                     # first unfinished slice from the backlog
python3 $gate run --feature features/001-x --label t1-red -- pytest tests/    # the only legitimate way to produce evidence
python3 $gate check --feature features/001-x --to build                       # may we enter this stage?
python3 $gate check --product                                                 # product definition + architecture both confirmed?
```

Typical fabrications the gate blocks mechanically: a "red" with no failing run on record, a "green" whose latest run still fails, a full suite never rerun after the last change, missing smoke evidence, a perceivable slice shipping without demo evidence or on-disk acceptance, an exploration prototype trying to ship, and a degraded (same-session) review auto-approving itself. The gate checks form only; semantic quality is owned by independent review and the user's demo acceptance — you need all of them.

## Skills

| Skill | Role |
|-------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | Entry point: entry paths, SE-activity map, delivery chain, dual modes, risk tiers, artifact layout, token economy, gate usage, state recovery, extension loading |
| [hf-shape](skills/hf-shape/SKILL.md) | Idea → product definition: structured interview, MVP boundary, not-doing list, assumption ledger |
| [hf-architect](skills/hf-architect/SKILL.md) | Architecture + breakdown: opinionated stack presets, one-page architecture/codebase map, vertical-slice backlog |
| [hf-skeleton](skills/hf-skeleton/SKILL.md) | Slice S-1: walking skeleton — scaffold, one-command dev/test, thinnest real end-to-end path, day-0 architecture validation |
| [hf-frame](skills/hf-frame/SKILL.md) | Pin down intent, mode, risk tier, user-perceivable flag, and the environment baseline |
| [hf-plan](skills/hf-plan/SKILL.md) | Testable requirements + design + machine-readable task list; template-slot hallucination forbidden |
| [hf-build](skills/hf-build/SKILL.md) | Build mode: each implementation task runs in a subagent with red-green-refactor logs (TDD). Exploration mode: fast disposable prototypes closed with a conclusion |
| [hf-verify](skills/hf-verify/SKILL.md) | Runtime smoke, independent code review, demo acceptance for perceivable slices, mechanical gate |
| [hf-review](skills/hf-review/SKILL.md) | Review protocol: subagent/fresh-session only, degraded reviews cannot self-approve; code reviewers rerun tests themselves |
| [hf-ship](skills/hf-ship/SKILL.md) | Final acceptance, feedback write-back (backlog checkoff, new slices, assumption settlement), closeout |
| [ext-ui-design](skills/ext-ui-design/SKILL.md) | Extension: UI features (IA, interaction states, design tokens, a11y, real-render evidence) |

## Extensions

Extensions live in `skills/ext-*/` and declare **binding stages** (a subset of shape/architect/frame/plan/build/verify/ship) and **trigger conditions** in their frontmatter description. Before each stage, `hf-workflow` scans them and loads the ones that match the current feature (e.g. "feature has a UI", "project is C++"). Extensions may only tighten requirements — they can never relax the main-chain gates.

To write your own, see [extension authoring](skills/hf-workflow/references/extension-authoring.md).

## Install

HarnessFlow is plain Markdown plus stdlib-only Python scripts (they travel inside this repo, zero dependencies). The recommended path for Cursor and OpenCode is the installer:

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
python scripts/install.py --target both --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

By default the installer copies HarnessFlow assets. Add `--mode symlink` (or `-Mode symlink` in PowerShell) when you want the target project to follow this checkout.

- **Cursor**: installs vendored skills under Cursor's auto-discovered `.cursor/skills/` directory, preserves unrelated project skills, and writes an always-applied `.cursor/rules/harness-flow.mdc` with paths rewritten for that layout.
- **Claude Code**: install as a plugin (`/plugin marketplace add <this repo>`), or vendor `skills/` into your project — skills are discovered by their frontmatter descriptions.
- **OpenCode / other clients**: installs HarnessFlow skills under `.opencode/skills/` while preserving any user-defined skills already there. OpenCode only discovers skills under that path (not the top-level `skills/` source), so the copy is generated by the installer and is gitignored — `skills/` remains the single source of truth. To use this repo itself in OpenCode: `python scripts/install.py --target opencode --dest .`

Then just ask for work naturally: *"I have an idea: an app that helps me track my reading notes"* — the agent enters `hf-shape` and drives from idea through product definition and architecture to a running skeleton and shipped slices. Or: *"Use HarnessFlow: add rate limiting to the notifications API"* — the agent enters `hf-frame`, recovers the stage via the gate, and proceeds.

## Execution modes

- `interactive` (default): after plan-layer reviews and at demo acceptance, the agent shows the verdict/demo and waits for your confirmation.
- `auto`: say "auto mode / don't wait for me" and passing reviews + a passing gate advance automatically. Hard floors remain: implementation tasks must run in subagents, reviews must run in a separate subagent/fresh session (a degraded review is a hard stop in auto), the gate can never be bypassed, every choice made on your behalf lands in the assumption ledger, and demo evidence is proactively presented at the next interaction.

## Design principles

- **Evidence is machine output.** "All tests green" is not evidence; a raw log with an exit code in `evidence/` is.
- **The product is the acceptance medium.** For anything users can perceive, acceptance happens against the running product, not a document.
- **Underspecification is explicit.** Defaults are proposed and ledgered, never silently hallucinated.
- **Machines judge form, reviews judge substance.** Anything mechanically decidable is never left to the model's discipline; anything requiring judgment happens in a clean context.
- **Process overhead scales with risk — and with permanence.** Micro changes don't pay the full-ceremony tax; disposable prototypes don't pay the TDD tax (and can never ship).
- **Process lives on disk.** Verdicts, approvals, ledgers and evidence logs are files, so any session can cold-start.
- **The architecture page is the map.** One page answers "what lives where and what are the conventions"; stages read the map first and only the relevant code — never a whole-repo rescan per feature.
- **Tokens are the user's money.** On-demand skill loading, per-artifact line budgets, single source of truth, paths-not-pastes for subagents, one-sentence teaching.
- **The graph teaches software engineering.** Each stage names its classic SE activity at the transition, so users absorb the discipline while shipping.
- **Extensions are conventions, not code.** Adding a domain skill never requires touching the main chain.

## License

MIT

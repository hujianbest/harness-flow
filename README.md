# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A three-layer skill suite that drives AI coding agents toward stable delivery: main-chain discipline (SDD + TDD) + mechanical gates + pluggable domain extensions.**

Core assumption: **the model is the least reliable component in the system.** A model that writes fake tests will just as happily write a fake "review passed". So HarnessFlow v3 does not entrust discipline to the model's goodwill — every gate that can be decided mechanically is decided by a script; every "tests pass / it runs" claim must be backed by raw command output on disk; every review must happen in an independent context that never saw the author's reasoning.

1. **Layer 1 — main-chain discipline**: `frame → plan → build → verify → ship`, spec-driven + test-driven, with process overhead scaled by risk tier.
2. **Layer 2 — mechanical gates**: `hf_gate.py` adjudicates stage transitions from files, verdict lines, exit codes and timestamps; evidence can only be produced by wrapping real command runs.
3. **Layer 3 — extensions**: domain skills (UI design, language standards, …) load into the main chain per stage; they may only tighten, never relax.

## The main chain and risk tiers

```
frame → plan → build → verify → ship
```

| Stage | Skill | Output | Gate |
|-------|-------|--------|------|
| Frame | `hf-frame` | `frame.md` — intent, risk tier, environment baseline evidence | `gate check` |
| Plan | `hf-plan` | `plan.md` (tier 2) or `spec.md` + `design.md` (tier 3) | independent review + user confirmation + `gate check` |
| Build | `hf-build` | code + tests, one task at a time, red→green→refactor with per-task logs | all tasks checked + `gate check` |
| Verify | `hf-verify` | runtime smoke evidence + independent code review | `gate check` |
| Ship | `hf-ship` | acceptance traced to every requirement, closeout report | all criteria closed |

Process overhead scales with risk: **tier 1** (micro changes) runs frame → build → verify → ship; **tier 2** (default) uses a single `plan.md`; only **tier 3** (data / security / cross-module) splits spec from design with three review rounds. Under-tiering is a blocking review finding.

All artifacts and evidence live in `features/<NNN>-<slug>/` (`frame.md`, `plan.md`, `progress.md`, `evidence/`, `reviews/`). Any new session recovers the current stage by probing with `gate check` — never from chat memory.

## Mechanical gates

```bash
# Produce evidence — the only legitimate way to run tests/builds/smoke (raw output + exit code on disk):
python3 skills/hf-workflow/scripts/hf_gate.py run --feature features/001-x --label t1-red -- pytest tests/

# Check whether a stage transition is allowed (files, review verdicts, red/green logs, exit codes, timestamps):
python3 skills/hf-workflow/scripts/hf_gate.py check --feature features/001-x --to build
```

Typical fabrications the gate blocks mechanically: a "red" with no failing run on record, a "green" whose latest run still fails, a full suite that was never rerun after the last change, missing smoke evidence, and a degraded (same-session) review auto-approving itself. The gate checks form only; semantic quality is owned by independent review — you need both.

## Skills

| Skill | Role |
|-------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | Entry point: main chain, risk tiers, artifact/evidence layout, gate usage, state recovery, extension loading |
| [hf-frame](skills/hf-frame/SKILL.md) | Pin down intent, risk tier, and the environment baseline (can this project actually be verified?) |
| [hf-plan](skills/hf-plan/SKILL.md) | Testable requirements + design + machine-readable task list; template-slot hallucination forbidden |
| [hf-build](skills/hf-build/SKILL.md) | Red-green-refactor per task, every run logged via `hf_gate.py run` (TDD) |
| [hf-verify](skills/hf-verify/SKILL.md) | Three-layer verification: runtime smoke, independent code review, mechanical gate |
| [hf-review](skills/hf-review/SKILL.md) | Review protocol: subagent/fresh-session only, degraded reviews cannot self-approve; code reviewers rerun tests themselves |
| [hf-ship](skills/hf-ship/SKILL.md) | Final acceptance, docs, closeout |
| [ext-ui-design](skills/ext-ui-design/SKILL.md) | Extension: UI features (IA, interaction states, design tokens, a11y, real-render evidence) |
| [ext-cpp](skills/ext-cpp/SKILL.md) | Extension: C++ projects (GoogleTest discipline, RAII, test anti-patterns) |

## Extensions (layer 3)

Extensions live in `skills/ext-*/` and declare **binding stages** (a subset of frame/plan/build/verify/ship) and **trigger conditions** in their frontmatter description. Before each stage, `hf-workflow` scans them and loads the ones that match the current feature (e.g. "feature has a UI", "project is C++"). Extensions may only tighten requirements — they can never relax the main-chain gates.

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

- **Cursor**: installs vendored skills under `.cursor/harness-flow-skills/` and writes `.cursor/rules/harness-flow.mdc` with paths rewritten for that layout.
- **Claude Code**: install as a plugin (`/plugin marketplace add <this repo>`), or vendor `skills/` into your project — skills are discovered by their frontmatter descriptions.
- **OpenCode / other clients**: installs HarnessFlow skills under `.opencode/skills/` while preserving any user-defined skills already there.

Then just ask for work naturally: *"Use HarnessFlow: I want to add rate limiting to the notifications API."* The agent enters `hf-workflow`, recovers the stage via the gate, and proceeds.

## Execution modes

- `interactive` (default): after plan-layer reviews pass, the agent shows the verdict and waits for your confirmation.
- `auto`: say "auto mode / don't wait for me" and passing reviews + a passing gate advance automatically. Two hard floors remain: reviews must run in a subagent/fresh session (a degraded review is a hard stop in auto), and the gate can never be bypassed.

## Design principles

- **Evidence is machine output.** "All tests green" is not evidence; a raw log with an exit code in `evidence/` is.
- **Machines judge form, reviews judge substance.** Anything mechanically decidable is never left to the model's discipline; anything requiring judgment happens in a clean context.
- **Process overhead scales with risk.** Micro changes don't pay the full-ceremony tax; risky changes can't escape three review rounds.
- **Process lives on disk.** Verdicts, approvals, and evidence logs are files, so any session can cold-start.
- **Extensions are conventions, not code.** Adding a domain skill never requires touching the main chain.

## License

MIT

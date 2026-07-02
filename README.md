# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A three-layer skill suite that constrains AI coding agents to produce high-quality code: spec-driven development (SDD) + test-driven development (TDD) + pluggable domain extensions.**

AI coding agents tend to jump from a vague request straight to implementation. HarnessFlow forces a narrower, harder path:

1. **Layer 1 — SDD**: turn intent into a reviewable, testable spec before anything else.
2. **Layer 2 — TDD**: every behavior is pulled into existence by a failing test, so shipped code is verified, not "probably fine".
3. **Layer 3 — Extensions**: domain skills (UI design, language standards, …) load into the main chain per stage, and you can keep adding your own.

## The main chain

```
specify → review → design → review → tdd → review → ship
```

| Stage | Skill | Output | Gate |
|-------|-------|--------|------|
| Specify | `hf-specify` | `spec.md` — numbered, testable requirements | spec review + user confirmation |
| Design | `hf-design` | `design.md` — architecture, contracts, ordered task list | design review + user confirmation |
| Implement | `hf-tdd` | code + tests, one task at a time, red→green→refactor | all tasks green |
| Review | `hf-review` | on-disk verdict + findings at every gate | verdict is `通过` (pass) |
| Ship | `hf-ship` | acceptance traced to every requirement, closeout report | all criteria closed |

All artifacts live in `features/<NNN>-<slug>/` (`spec.md`, `design.md`, `progress.md`, `reviews/`). Any new session recovers the current stage from these files — never from chat memory.

## Skills

| Skill | Role |
|-------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | Entry point: main chain, artifact layout, gates, state recovery, extension loading |
| [hf-specify](skills/hf-specify/SKILL.md) | Clarify intent into a testable spec (SDD) |
| [hf-design](skills/hf-design/SKILL.md) | Technical design + ordered task breakdown |
| [hf-review](skills/hf-review/SKILL.md) | One review protocol, three stage checklists, author/reviewer separation |
| [hf-tdd](skills/hf-tdd/SKILL.md) | Red-green-refactor per task with fresh evidence (TDD) |
| [hf-ship](skills/hf-ship/SKILL.md) | Final acceptance, docs, closeout |
| [ext-ui-design](skills/ext-ui-design/SKILL.md) | Extension: UI features (IA, interaction states, design tokens, a11y, anti-slop) |
| [ext-cpp](skills/ext-cpp/SKILL.md) | Extension: C++ projects (GoogleTest discipline, RAII, test anti-patterns) |

## Extensions (layer 3)

Extensions live in `skills/ext-*/` and declare **binding stages** and **trigger conditions** in their frontmatter description. Before each stage, `hf-workflow` scans them and loads the ones that match the current feature (e.g. "feature has a UI", "project is C++"). Extensions may only tighten requirements — they can never relax the main-chain gates.

To write your own, see [extension authoring](skills/hf-workflow/references/extension-authoring.md).

## Install

HarnessFlow is plain Markdown. Copy (or submodule) this repo's `skills/` directory into your project, then wire up your client:

- **Cursor**: also copy `.cursor/rules/harness-flow.mdc` into your project's `.cursor/rules/`. The rule loads `hf-workflow` on every development task.
- **Claude Code**: install as a plugin (`/plugin marketplace add <this repo>`), or vendor `skills/` into your project — skills are discovered by their frontmatter descriptions.
- **OpenCode / other clients**: point the client's skill directory at `skills/` (this repo keeps `.opencode/skills` as a symlink for that purpose).

Then just ask for work naturally: *"Use HarnessFlow: I want to add rate limiting to the notifications API."* The agent enters `hf-workflow`, recovers the stage from artifacts, and proceeds.

## Execution modes

- `interactive` (default): after spec and design reviews pass, the agent shows the verdict and waits for your confirmation.
- `auto`: say "auto mode / don't wait for me" and passing reviews auto-approve (recorded in `progress.md`). Reviews and gates still run — auto never deletes them.

## Design principles

- **Process lives on disk.** Reviews, approvals, task progress, and test evidence are files, so any session can cold-start.
- **Author/reviewer separation.** Whoever wrote an artifact never approves it.
- **One skill, one job.** Six core skills, no meta-machinery; the review protocol is written once and reused at every gate.
- **Extensions are conventions, not code.** Adding a domain skill never requires touching the main chain.

## License

MIT

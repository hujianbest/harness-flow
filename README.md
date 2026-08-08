# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A harness that drives AI coding agents from idea to shipped work — Matt-aligned main chain under `hf-*` names, plus mechanical gates, progress recovery, auto mode, demo-gated acceptance, and pluggable `ext-*` extensions.**

Main-chain skill content is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT; copying authorized). HarnessFlow keeps the shell: `hf_gate.py`, `progress.md`, interactive/auto, and cross-stage `hf-review`.

## Main chain

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-spec            — hf-review (spec) —
  → hf-to-architecture    — hf-review (architecture) —
  → hf-to-tickets
  → hf-implement          — hf-review → hf-code-review —
  → hf-ship
```

Exploration: `hf-prototype` / `模式: 探索` → `check --to close` (never ship). Incoming issues: `hf-triage`. Hard bugs: `hf-diagnosing-bugs`.

## Mechanical gates

```bash
gate=skills/hf-workflow/scripts/hf_gate.py
python3 $gate init
python3 $gate status
python3 $gate next
python3 $gate check --product
python3 $gate check --feature features/001-x --to to-architecture
```

`--to` stages: `to-spec` | `to-architecture` | `to-tickets` | `implement` | `ship` | `close`.

Gates check artifacts and review verdict lines on disk — not model narration. Semantic quality is owned by `hf-review` / `hf-code-review` and demo acceptance.

## Skills (core)

| Skill | Role |
|-------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | Entry, routing, auto, extensions, gate usage |
| [hf-grill-with-docs](skills/hf-grill-with-docs/SKILL.md) | Interview + CONTEXT.md / ADR |
| [hf-to-spec](skills/hf-to-spec/SKILL.md) | Synthesize a spec |
| [hf-to-architecture](skills/hf-to-architecture/SKILL.md) | Feature architecture after spec |
| [hf-to-tickets](skills/hf-to-tickets/SKILL.md) | Tracer-bullet tickets + blockers |
| [hf-implement](skills/hf-implement/SKILL.md) | Build tickets via `hf-tdd` |
| [hf-review](skills/hf-review/SKILL.md) | Cross-stage review protocol |
| [hf-code-review](skills/hf-code-review/SKILL.md) | Two-axis code review (Standards + Spec) |
| [hf-ship](skills/hf-ship/SKILL.md) | Closeout + write-back |

Meta / on-ramps include `hf-tdd`, `hf-grilling`, `hf-domain-modeling`, `hf-codebase-design`, `hf-prototype`, `hf-setup-skills`, and others under `skills/hf-*`.

## Extensions

`ext-ui-design` (to-spec / implement / code-review), `ext-design-md` (to-architecture / ship). See [extension authoring](skills/hf-workflow/references/extension-authoring.md).

## Install

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

## Execution modes

- **interactive** (default): wait for confirmation after reviews and demo acceptance.
- **auto**: say so explicitly; passing review + gate advances with `auto-approved`. Floors remain: subagent implement/review, no degraded self-approve, gate never skipped, assumptions ledgered.

## License

MIT. Main-chain skill prose adapted from mattpocock/skills (MIT).

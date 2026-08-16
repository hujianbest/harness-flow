# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A harness that drives AI coding agents from idea to shipped work — Matt-aligned main chain under `hf-*` names, plus progress recovery, auto mode, review discipline, and demo acceptance.**

Main-chain skill content is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT; copying authorized). HarnessFlow keeps `progress.md`, interactive/auto, and cross-stage `hf-review`.

## Install

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

- **Cursor**: copies skills into `.cursor/skills/` and writes an always-on `.cursor/rules/harness-flow.mdc` (paths rewritten). Unrelated project skills are preserved. Use `--mode symlink` to follow this checkout.
- **OpenCode**: installs under `.opencode/skills/` (generated, gitignored); top-level `skills/` remains the source of truth.
- **Claude Code**: install as a plugin from this repo’s marketplace, or vendor `skills/` into the project.

In this repo itself (OpenCode): `python scripts/install.py --target opencode --dest .`

## Usage

### 1. One-time project setup

Ask the agent to run `hf-grill-with-docs` and create the product layer from `skills/hf-workflow/references/product-layer-templates.md` (`CONTEXT.md`, `product/…`, `docs/adr/`, `features/`). Specs and tickets live under `features/<id>/`.

### 2. Start work (talk naturally)

The agent should load `hf-workflow` first. Example prompts:

| Goal | Example |
|------|---------|
| Idea → app | “I have an idea: an app that tracks reading notes. Use HarnessFlow.” |
| Existing codebase feature | “Use HarnessFlow: add rate limiting to the notifications API.” |
| Continue after a break | “Continue” / “Resume HarnessFlow progress.” |
| Auto mode | “Auto mode — don’t wait for my confirmation unless blocked.” |
| Exploration | “Try this state model as throwaway exploration.” |

### 3. Follow the main chain

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-product-architecture — hf-review (product architecture) —
  → hf-to-spec            — hf-review (spec) —
  → hf-to-architecture    — hf-review (architecture) —
  → hf-to-tickets
  → hf-implement          — hf-review (incl. code gate) —
  → hf-ship
```

What you should see on disk as you go:

| Stage | Typical artifacts |
|-------|-------------------|
| Grill | `CONTEXT.md`, ADRs, `product/assumptions.md`, optional `features/<NNN>-<slug>/` |
| Product architecture | `product/architecture.md` + `product/reviews/product-architecture-review.md` |
| Spec | `features/.../spec.md` + `reviews/spec-review.md` |
| Architecture | `features/.../architecture.md` (incremental vs product map) + `reviews/architecture-review.md` |
| Tickets | `features/.../tickets.md` (`- [ ] T-01 ...`) |
| Implement | code + tests via `hf-tdd`; tickets checked off |
| Code review | `reviews/code-review.md` |
| Ship | write-back to CONTEXT / product architecture / assumptions; `progress` → `done` |
| Perceivable UI | demo evidence + `reviews/demo-acceptance.md` before ship |

Exploration path: `模式: 探索` → `conclusion.md` (**never ship**; no promoting exploration code).

### 4. Recover from disk (don’t rely on chat)

Read `product/progress.md` and each `features/<id>/progress.md` to see stage and next step. Artifact layout is defined by the stage skills and `skills/hf-workflow/references/product-layer-templates.md`.

**Rules of thumb**

- Spec / product architecture / feature architecture / code should get independent `hf-review` (code gate is Standards + Spec inside that skill).
- Underspecified choices: propose a default → `product/assumptions.md` → continue.
- Say **auto** only when you want passing reviews to advance without waiting; degraded same-session review is a hard stop in auto.

### 5. Execution modes

- **interactive** (default): wait for your confirmation after reviews and demo acceptance.
- **auto**: you must say so explicitly. Passing review advances with `auto-approved`. Floors: implement/review in subagents, no degraded self-approve, assumptions ledgered; present demo evidence at the next human interaction.

## Skills (core)

| Skill | Role |
|-------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | Entry, routing, auto |
| [hf-grill-with-docs](skills/hf-grill-with-docs/SKILL.md) | Interview + CONTEXT.md / ADR |
| [hf-to-product-architecture](skills/hf-to-product-architecture/SKILL.md) | Product-level architecture map (characteristics-driven, volatility-based, evolutionary) |
| [hf-to-spec](skills/hf-to-spec/SKILL.md) | Synthesize a spec |
| [hf-to-architecture](skills/hf-to-architecture/SKILL.md) | Feature architecture (incremental) after spec |
| [hf-to-tickets](skills/hf-to-tickets/SKILL.md) | Tracer-bullet tickets + blockers |
| [hf-implement](skills/hf-implement/SKILL.md) | Build tickets via `hf-tdd` |
| [hf-review](skills/hf-review/SKILL.md) | Cross-stage review, including Standards + Spec code gate |
| [hf-ship](skills/hf-ship/SKILL.md) | Closeout + write-back |
| [hf-ui-design](skills/hf-ui-design/SKILL.md) | UI discipline when the feature has a user interface |

Meta: `hf-tdd`, `hf-grilling`, `hf-domain-modeling`, `hf-codebase-design`.

## License

MIT. Main-chain skill prose adapted from mattpocock/skills (MIT).

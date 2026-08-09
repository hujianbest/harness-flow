# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**A harness that drives AI coding agents from idea to shipped work — Matt-aligned main chain under `hf-*` names, plus progress recovery, auto mode, review discipline, demo acceptance, and pluggable `ext-*` extensions. `hf_gate.py` is an optional status/self-check tool — not a mandatory gate.**

Main-chain skill content is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT; copying authorized). HarnessFlow keeps `progress.md`, interactive/auto, and cross-stage `hf-review`. There is **no forced mechanical gate**.

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

In the target project, ask the agent once:

> Run `hf-setup-skills` and configure the issue tracker (local files are fine), triage labels if needed, and where CONTEXT/ADRs live.

Or let greenfield `hf_gate.py init` create `CONTEXT.md`, `product/assumptions.md`, `product/decisions.md`, `product/architecture.md`, `docs/adr/`, and `features/`, then refine with `hf-setup-skills` when you want a real tracker.

### 2. Start work (talk naturally)

The agent should load `hf-workflow` first. Example prompts:

| Goal | Example |
|------|---------|
| Idea → app | “I have an idea: an app that tracks reading notes. Use HarnessFlow.” |
| Existing codebase feature | “Use HarnessFlow: add rate limiting to the notifications API.” |
| Continue after a break | “Continue” / “Resume HarnessFlow progress.” |
| Auto mode | “Auto mode — don’t wait for my confirmation unless blocked.” |
| Exploration / prototype | “Prototype whether this state model feels right (throwaway).” |
| Incoming bug pile | “Triage open issues, then implement what’s ready-for-agent.” |

### 3. Follow the main chain

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-product-architecture — hf-review (product architecture) —
  → hf-to-spec            — hf-review (spec) —
  → hf-to-architecture    — hf-review (architecture) —
  → hf-to-tickets
  → hf-implement          — hf-review → hf-code-review —
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

Exploration path: `hf-prototype` or `模式: 探索` → `conclusion.md` (**never ship**; no promoting prototype code).

### 4. Optional status / self-check (don’t rely on chat)

```bash
gate=skills/hf-workflow/scripts/hf_gate.py   # after Cursor install: .cursor/skills/hf-workflow/scripts/hf_gate.py
python3 $gate status                         # product layer + where each feature is stuck + next step
python3 $gate next                           # next unfinished feature / stage
python3 $gate check --product
python3 $gate check --feature features/001-x --to to-architecture
```

`--to` stages: `to-spec` | `to-architecture` | `to-tickets` | `implement` | `ship` | `close`.

**Rules of thumb**

- **No mandatory gate**: you do **not** need `check --to` PASS to enter a stage. `hf_gate.py check` is optional diagnostics only.
- Prefer `status` to recover progress from disk after a break.
- Spec / product architecture / feature architecture / code should still get independent `hf-review` (code also uses `hf-code-review`) — that is review discipline, not a script veto.
- Underspecified choices: propose a default → `product/assumptions.md` → continue.
- Say **auto** only when you want passing reviews to advance without waiting; degraded same-session review is a hard stop in auto. Auto does **not** require gate PASS.

### 5. Execution modes

- **interactive** (default): wait for your confirmation after reviews and demo acceptance.
- **auto**: you must say so explicitly. Passing review advances with `auto-approved`. Floors: implement/review in subagents, no degraded self-approve, assumptions ledgered; present demo evidence at the next human interaction.

## Skills (core)

| Skill | Role |
|-------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | Entry, routing, auto, extensions, optional status tool |
| [hf-grill-with-docs](skills/hf-grill-with-docs/SKILL.md) | Interview + CONTEXT.md / ADR |
| [hf-to-product-architecture](skills/hf-to-product-architecture/SKILL.md) | Product-level architecture map |
| [hf-to-spec](skills/hf-to-spec/SKILL.md) | Synthesize a spec |
| [hf-to-architecture](skills/hf-to-architecture/SKILL.md) | Feature architecture (incremental) after spec |
| [hf-to-tickets](skills/hf-to-tickets/SKILL.md) | Tracer-bullet tickets + blockers |
| [hf-implement](skills/hf-implement/SKILL.md) | Build tickets via `hf-tdd` |
| [hf-review](skills/hf-review/SKILL.md) | Cross-stage review protocol |
| [hf-code-review](skills/hf-code-review/SKILL.md) | Two-axis code review (Standards + Spec) |
| [hf-ship](skills/hf-ship/SKILL.md) | Closeout + write-back |
| [hf-setup-skills](skills/hf-setup-skills/SKILL.md) | Per-repo tracker / labels / domain docs |

Meta / on-ramps: `hf-tdd`, `hf-grilling`, `hf-domain-modeling`, `hf-codebase-design`, `hf-prototype`, `hf-triage`, `hf-diagnosing-bugs`, `hf-wayfinder`, `hf-handoff`, `hf-wizard`, and others under `skills/hf-*`.

## Extensions

Loaded when frontmatter **binding stage** + **trigger** match:

- [ext-ui-design](skills/ext-ui-design/SKILL.md) — `to-spec` / `implement` / `code-review` when the feature has UI
- [ext-design-md](skills/ext-design-md/SKILL.md) — `to-architecture` / `ship` when using a `DESIGN.md` token source

Extensions only tighten requirements. Authoring: [extension-authoring](skills/hf-workflow/references/extension-authoring.md).

## License

MIT. Main-chain skill prose adapted from mattpocock/skills (MIT).

# HarnessFlow Agents Configuration

This repository ships HarnessFlow, a skill pack for spec-anchored SDD, gated TDD, evidence-based routing, independent reviews, and formal closeout. This `AGENTS.md` is the always-loaded entry for OpenCode and other agents that consume the cross-tool `AGENTS.md` standard.

## HF Orchestrator (always on)

On every session, **read `agents/hf-orchestrator.md` and act as that persona**. The orchestrator is HarnessFlow's always-on agent persona that:

- Decides Workflow Profile (full/standard/lightweight), Execution Mode (interactive/auto), and Workspace Isolation (in-place/worktree-required/worktree-active)
- Reads on-disk artifacts (`features/<active>/progress.md`, recent reviews, verification, spec/design/tasks) to determine the canonical next step
- Invokes leaf skills under `skills/hf-*/` to do work, and dispatches independent reviewer subagents at review/gate nodes (Fagan author/reviewer separation)
- Knows when to pause (hard stops) vs continue (auto/interactive Execution Mode)

The 24 `hf-*` skills under `skills/` are SOPs to be invoked by the orchestrator; they are not routing authorities. The orchestrator's progressive-disclosure references (FSM transition map / dispatch protocol / reviewer return contract / evidence guides) live at `agents/references/*.md`.

## Hard rules

- **One Current Active Task at a time.** Cross-task switches are decided by the orchestrator, not by you.
- **Approvals and gates are first-class nodes.** Don't skip `hf-spec-review` / `hf-design-review` / `hf-tasks-review` / `hf-test-review` / `hf-code-review` / `hf-traceability-review` / `hf-regression-gate` / `hf-doc-freshness-gate` / `hf-completion-gate`.
- **Evidence-based routing.** Recover the next step from on-disk artifacts, not from chat memory.
- **Author / reviewer separation (Fagan).** Whoever wrote the artifact under review must NOT also approve it.
- **`hf-release` is standalone**, not orchestrator-coupled (ADR-004 D3 + ADR-007 D1 关键先例).
- **`using-hf-workflow` / `hf-workflow-router` are deprecated aliases (v0.6.0+).** Their content has been merged into `agents/hf-orchestrator.md`. Old skill files remain as redirect stubs through the v0.6.x line; physical deletion is scheduled for v0.7.0+ per ADR-007 D3 Step 6.

## Scope

HarnessFlow's main chain ends at `hf-finalize` (engineering-level closeout). It is NOT production deployment, observability, incident response, or post-launch ops. v0.6.0 introduces the **HF three-layer architecture invariant** (Doer Skills / Reviewer-Gate Skills / Orchestrator Agent per ADR-007 D1) without growing the leaf skill set (still 24 `hf-*`), without adding slash commands (still 7), and without changing closeout pack schema / reviewer verdict vocabulary / `hf-release` behavior. See `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` for the full rationale.

## Setup details

See [`docs/opencode-setup.md`](docs/opencode-setup.md) for installation flow + `.opencode/skills/` symlink layout.

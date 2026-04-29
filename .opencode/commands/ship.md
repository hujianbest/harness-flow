---
description: Use when an active task (or the whole workflow cycle) looks complete and you want HF to gate-check + close it out. Bias: hf-completion-gate → hf-finalize.
argument-hint: ["task" | "workflow" | optional task id]
---

# /ship — bias toward closeout (`hf-completion-gate` → `hf-finalize`)

`/ship` is HF's user-facing closeout entry. It does **not** mean "deploy" or "release to production" — v0.1.0's main chain terminates at engineering closeout (per `docs/principles/soul.md` § "现状脚注" and ADR-001 D1).

## What HF should do

1. Pass `$ARGUMENTS` to `using-hf-workflow` with `command_bias=/ship`.
2. Have `hf-workflow-router` resolve closeout scope:
   - default / "task" → close out the current completed task (run `hf-regression-gate` → `hf-doc-freshness-gate` → `hf-completion-gate`; on pass, `hf-completion-gate` decides whether to reselect a next task or hand off to `hf-finalize`)
   - "workflow" / "wrap up" / "all tasks done" → run completion gate, then enter `hf-finalize` for workflow closeout (CHANGELOG / handoff pack)
3. If any of the gate's evidence requirements are not met (fresh RED/GREEN missing, traceability not closed, regression not run, doc freshness not synced), do **not** forge a verdict — reroute to the missing upstream node.

## HF guardrails

- `/ship` is **not** a deployment trigger. v0.1.0 has no release / ops skills (per ADR-001 D1, P-Honest). If the user actually means "deploy to production", surface that back as out-of-scope for v0.1.0.
- `/ship` does **not** allow HF to self-approve completion. The completion verdict is a `hf-completion-gate` record on disk, not a chat statement.
- `/ship` for workflow scope still requires the architect's confirmation per Execution Mode = `interactive` before `hf-finalize` writes release notes / handoff pack.

User intent: $ARGUMENTS

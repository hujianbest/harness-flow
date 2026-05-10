<!-- HF v0.6.0 deprecated alias: see agents/hf-orchestrator.md -->
---
name: using-hf-workflow
description: deprecated alias, see agents/hf-orchestrator.md (HF v0.6.0+)
---

# using-hf-workflow (deprecated alias)

**This skill is deprecated as of HarnessFlow v0.6.0** (2026-05-10).

The `using-hf-workflow` public entry shell + `hf-workflow-router` runtime authority have been merged into a single **always-on agent persona** at:

→ **[`agents/hf-orchestrator.md`](../../agents/hf-orchestrator.md)**

The orchestrator agent is auto-loaded by every supported host (Cursor `.cursor/rules/harness-flow.mdc` / Claude Code `CLAUDE.md` + plugin manifest / OpenCode `AGENTS.md`). You do not need to load anything manually.

If you arrived here from a v0.5.x tutorial link, please update your reference to `agents/hf-orchestrator.md`.

**Compatibility window**: this stub remains in the v0.6.x line for external tutorial-link grace; physical deletion is scheduled for v0.7.0+ per [ADR-007 D3 Step 6](../../docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md).

For the migration rationale see [ADR-007](../../docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md) and [`features/001-orchestrator-extraction/`](../../features/001-orchestrator-extraction/).

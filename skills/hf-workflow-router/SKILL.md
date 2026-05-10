<!-- HF v0.6.0 deprecated alias: see agents/hf-orchestrator.md -->
---
name: hf-workflow-router
description: deprecated alias, see agents/hf-orchestrator.md (HF v0.6.0+)
---

# hf-workflow-router (deprecated alias)

**This skill is deprecated as of HarnessFlow v0.6.0** (2026-05-10).

The runtime routing authority previously held by `hf-workflow-router` has been merged with `using-hf-workflow` into a single **always-on agent persona** at:

→ **[`agents/hf-orchestrator.md`](../../agents/hf-orchestrator.md)**

The 9 reference files that used to live under `skills/hf-workflow-router/references/` have been physically migrated to `agents/references/` (same filenames). The old reference paths are also deprecated stubs in this directory.

**Runtime canonical names**: in v0.6.0+ use `hf-orchestrator` (replaces `hf-workflow-router`) and `reroute_via_orchestrator` (replaces `reroute_via_router`). Old names remain readable as synonyms during the v0.6.x compatibility window.

**Compatibility window**: this stub remains in the v0.6.x line for external tutorial-link grace; physical deletion is scheduled for v0.7.0+ per [ADR-007 D3 Step 6](../../docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md).

For the migration rationale see [ADR-007](../../docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md) and [`features/001-orchestrator-extraction/`](../../features/001-orchestrator-extraction/).

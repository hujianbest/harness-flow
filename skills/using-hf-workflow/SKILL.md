<!-- HF v0.6.0 plugin-install loading channel for the orchestrator persona; see agents/hf-orchestrator.md -->
---
name: using-hf-workflow
description: HarnessFlow workflow entry. Use when starting a new HF session, when the user expresses /hf-* intent, when unsure which leaf skill to invoke next, when reviewing/gating just finished and you need to decide what's next, or when route/stage/profile/evidence is unclear. Loads agents/hf-orchestrator.md as the always-on orchestrator persona for the rest of the session.
---

# HF Orchestrator Entry (plugin-install loading channel)

**This skill is the Claude Code / OpenCode plugin loading channel for the HF Orchestrator agent persona.** Activate it on any HF-relevant intent, then immediately load and adopt `agents/hf-orchestrator.md` as the persona for the rest of the session.

> **v0.6.0 architectural note**: ADR-007 D1 introduced `agents/hf-orchestrator.md` as the always-on agent persona (Layer 3 of the HF three-layer architecture: Doer Skills 12 / Reviewer-Gate Skills 11 / Orchestrator Agent 1). For direct-clone hosts (Cursor) the orchestrator is auto-loaded via `.cursor/rules/harness-flow.mdc`. For plugin-install hosts (Claude Code, OpenCode), Claude Code's plugin schema does not currently support always-active agent persona registration (see ADR-007 D1 Amendment, v0.6.0 pre-tag fix), so this skill exists as the description-triggered loading channel that the plugin's skill-discovery mechanism can find. **Functionally**, activating this skill should be equivalent to having `agents/hf-orchestrator.md` always-on. **Architecturally**, `agents/hf-orchestrator.md` is the canonical single source of truth; this file is a thin loader.

## On activation (operating loop entry)

When this skill is activated, do the following **in this exact order**:

1. **Read `agents/hf-orchestrator.md`** (use the Read tool; the file is at the repository root under `agents/hf-orchestrator.md`). Adopt that file's `# HF Orchestrator` persona for the rest of this session — its identity declaration ("I am the HF Orchestrator"), Operating Loop (10 steps), Hard Stops, Workflow Profile / Execution Mode / Workspace Isolation decision entries, FSM transition map entry, Reviewer Dispatch entry, Skill Catalog (24 hf-* + 1 entry), Output Contract, Red Flags, Common Rationalizations, and Verification self-check apply.

2. **Continue with the user's actual request** using the Operating Loop you just adopted. Read minimal evidence from `features/<active>/progress.md`, recent `reviews/`, and `verification/` artifacts. Decide Workflow Profile / Execution Mode / Workspace Isolation. Decide canonical next skill via the FSM transition map (now at `agents/references/profile-node-and-transition-map.md`). Pause on hard stops; otherwise continue same-turn.

3. **Use canonical naming**: `hf-orchestrator` and `reroute_via_orchestrator`. Old aliases `hf-workflow-router` and `reroute_via_router` remain readable as synonyms during v0.6.x compatibility but should not appear in new `Next Action Or Recommended Skill` field values.

## Why this skill exists in v0.6.0

ADR-007 D1 made the orchestrator a separate Layer 3 (not a leaf skill). For Claude Code plugin loading, the practical reality is that:

- Plugin schema doesn't support `agents` array registration with `alwaysActive: true` (rejected with `agents: Invalid input` validation error during `/plugin install`; PR #46 fix engaged spec C-005 fallback)
- `CLAUDE.md` always-load works only for the **target project root**, not for installed-plugin repos — so `harness-flow/CLAUDE.md` is never injected into the user's project session
- The remaining channel: Claude Code's skill-discovery mechanism reads installed plugin's `skills/<name>/SKILL.md` files and triggers based on `description` matching against user intent

This skill's `description` matches HF-entry intent (new session / `/hf-*` command / continue / review-gate completed / route unclear). On activation, body redirects loading to the canonical orchestrator file.

This is a **loading channel**, not a competing source of truth. `agents/hf-orchestrator.md` remains the canonical document.

## When this skill is **not** the right activation

- User is already deep inside a leaf skill workflow → continue that leaf
- User is asking a non-HF question → do not activate
- User wants to invoke a specific leaf skill by name (e.g. "run hf-test-driven-dev for task-N") → the leaf skill's own description should activate it; this skill is a fallback for unclear intent

## Compatibility note

`skills/hf-workflow-router/` (the v0.5.x runtime authority) and `skills/hf-workflow-router/references/*` (its 9 reference files) remain as redirect stubs in v0.6.x, pointing at `agents/hf-orchestrator.md` and `agents/references/*` respectively. Physical deletion of all v0.5.x deprecated paths is scheduled for v0.8.0+ per ADR-007 D3 Step 6.

For the full migration rationale see [`docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`](../../docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md) and [`features/001-orchestrator-extraction/`](../../features/001-orchestrator-extraction/).

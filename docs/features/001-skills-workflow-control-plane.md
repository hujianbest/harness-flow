# Skills Workflow Control Plane — Next Action Plan

- Feature ID: `001-skills-workflow-control-plane`
- Status: proposed
- Date: 2026-04-27
- Context:
  - Strategic anchor: `skills/principles/soul.md`
  - Node contract: `skills/principles/skill-node-define.md`
  - Artifact layout: `skills/principles/sdd-artifact-layout.md`

## Goal

Turn the current HF skills design from a principled skill library into a recoverable, auditable, and testable workflow control plane.

The expected outcome is not "more skills". The expected outcome is that an agent can enter HF from a cold session, read disk evidence, select the correct next node, execute one bounded step, leave durable evidence, and hand off a unique next action.

## Industry Insight Summary

The current direction is sound: HF treats skills as workflow nodes with explicit responsibility, object, method, evidence, and handoff contracts. This is stronger than a loose prompt chain and aligns with current agent architecture practice.

The main risk is overestimating what skills can enforce by themselves. Skills are best at encoding knowledge, procedures, and judgment. Runtime reliability still needs structured artifacts, deterministic validators, route maps, eval fixtures, and isolated reviewer/subagent execution where independence matters.

## Target Architecture

HF should be implemented as four cooperating layers:

| Layer | Responsibility | HF Artifact |
|---|---|---|
| Skill layer | Defines node behavior, boundaries, methods, hard gates | `skills/hf-*/SKILL.md` |
| State layer | Stores recoverable workflow state and evidence | `docs/features/<active>/progress.md`, records, evidence |
| Routing layer | Selects canonical next node from disk evidence | `hf-workflow-router` references and transition map |
| Verification layer | Tests that skills, routing, and gates behave as intended | eval fixtures, validators, review records |

## Phase 0 — Normalize The Foundation

Purpose: remove layout ambiguity before adding more workflow behavior.

Actions:

1. Establish `docs/features/` as the official process-artifact root.
2. Decide whether `docs/fearures/` is a temporary typo directory or a legacy location that needs migration.
3. Update principle cross-links that still reference stale paths such as `docs/principles/sdd-artifact-layout.md` if the canonical file is now `skills/principles/sdd-artifact-layout.md` (the principle pack has been relocated to `skills/principles/` to make the skills pack self-contained).
4. Add a top-level navigation pointer in `README.md` for the active feature once HF workflow execution begins.

Deliverables:

- `docs/features/001-skills-workflow-control-plane/README.md`
- A short path cleanup decision record, either in this feature directory or as an ADR if the path decision affects long-term compatibility.

Exit criteria:

- A new agent can identify where process artifacts belong.
- No principle document points to a non-existing canonical path without an intentional compatibility note.

## Phase 1 — Define Machine-Readable Workflow State

Purpose: make workflow recovery depend on structured evidence, not conversation memory.

Actions:

1. Define the minimum `progress.md` schema for an active feature:
   - active feature ID
   - current profile
   - current stage
   - current node
   - current active task
   - last verdict
   - blockers
   - next action
   - relevant artifact paths
2. Define common record fields for review, approval, gate, and implementation handoff records.
3. Define canonical values for verdicts and next actions.
4. Document conflict precedence when user request, progress, review record, and evidence disagree.

Deliverables:

- `skills/docs/hf-workflow-shared-conventions.md` update or equivalent reference.
- `docs/features/001-skills-workflow-control-plane/progress.md` fixture.
- Example records under `docs/features/001-skills-workflow-control-plane/reviews/` and `verification/`.

Exit criteria:

- Router can recover state from files without relying on chat history.
- Every state-changing node has a durable record target.

## Phase 2 — Make Routing Deterministic First

Purpose: keep `hf-workflow-router` from becoming a prose-based guesser.

Actions:

1. Convert the route/profile/stage rules into a compact transition table.
2. Specify the exact evidence required for each legal transition.
3. Define blocked states for missing evidence, conflicting evidence, illegal profile downgrade, and non-unique next action.
4. Add a lightweight route validation script or fixture runner if prose checks become hard to maintain.

Deliverables:

- Updated route map reference.
- Router eval fixtures covering happy path, missing approval, conflicting review verdicts, and non-unique next action.

Exit criteria:

- Given the same artifact bundle, router returns the same canonical next node.
- Ambiguity routes to `blocked` or `hf-workflow-router`, not to an arbitrary leaf skill.

## Phase 3 — Build One Thin Vertical Slice

Purpose: prove the architecture with the smallest end-to-end workflow before expanding nodes.

Recommended slice:

`using-hf-workflow -> hf-workflow-router -> hf-specify -> hf-spec-review -> human approval -> hf-design`

Actions:

1. Pick a small real feature as a fixture.
2. Run the slice with fresh sessions where possible.
3. Record every artifact, review, approval, and handoff.
4. Capture where the agent misroutes, over-asks, self-approves, or loses context.
5. Feed those observations back into skill descriptions, hard gates, and shared conventions.

Deliverables:

- One completed slice under `docs/features/`.
- At least three eval cases derived from real failures.

Exit criteria:

- A cold agent can resume the slice at each boundary.
- Review and approval boundaries are not bypassed.

## Phase 4 — Harden Review And Gate Independence

Purpose: make "HF does not approve itself" operational, not just aspirational.

Actions:

1. Require review skills to produce structured findings and a single verdict.
2. Run high-risk reviews in fresh context or subagents.
3. Prevent authoring nodes from editing review records after verdict.
4. Require gates to consume records and evidence only; they must not manufacture missing evidence.

Deliverables:

- Review record templates.
- Gate record templates.
- Evals for reviewer independence and gate refusal behavior.

Exit criteria:

- Authoring, review, approval, implementation, and gate responsibilities remain separate in artifacts.
- A missing or failed review cannot be silently converted into progress.

## Phase 5 — Add Profile-Aware Rigor

Purpose: avoid turning every task into a heavyweight ceremony.

Actions:

1. Define `lightweight`, `standard`, and `full` profiles.
2. For each profile, specify which artifacts, reviews, approvals, and gates are required.
3. Define escalation triggers from lightweight to standard or full.
4. Forbid silent downgrade once risk has been discovered.

Deliverables:

- Profile matrix.
- Router fixtures for profile escalation.
- Skill updates where hard gates depend on profile.

Exit criteria:

- Small changes can move quickly without losing evidence discipline.
- High-risk changes automatically receive stronger workflow rigor.

## Phase 6 — Close The Productization Gap

Purpose: move from "high-quality engineering change" toward the soul target of "idea to product".

Actions:

1. Define what "product landed" means for HF:
   - merged code only
   - releasable artifact
   - deployed system
   - observable production behavior
2. Add explicit handoff points for deployment, observability, release notes, runbooks, and post-release measurement.
3. Keep unimplemented productization capabilities visible as blockers or deferred scope, not hidden assumptions.

Deliverables:

- Productization capability map.
- Future feature plan for release/deploy/observe/measure workflows.

Exit criteria:

- HF no longer conflates code completion with product landing.
- The workflow clearly tells the user which downstream product steps remain outside the current automation boundary.

## Priority Order

1. Fix path and artifact layout ambiguity.
2. Define shared workflow state and record schemas.
3. Make router transitions deterministic.
4. Prove one thin vertical slice.
5. Harden independent review and gates.
6. Add profile-aware rigor.
7. Extend toward release, deployment, observability, and measurement.

## Immediate Next Task

Create the minimum shared workflow state contract:

- Decide the exact fields for `docs/features/<active>/progress.md`.
- Decide the canonical verdict vocabulary.
- Decide how `next_action_or_recommended_skill` is represented.
- Add two sample progress files: one valid, one blocked.

This is the highest-leverage next step because every later skill-node, router rule, review, and gate depends on a stable state object.

# Agent Role Contracts

## Purpose

`hf-subagent-driven-dev` uses exactly two named subagent roles. Their canonical definitions live in the top-level `agents/` directory:

1. `agents/hf-implementer.md`
2. `agents/hf-reviewer.md`

These are role contracts, not new canonical workflow nodes. The router still routes to `hf-subagent-driven-dev` for implementation and to existing `hf-*review` skills for review verdicts.

## `hf-implementer`

### Responsibility

`hf-implementer` implements one locked `Current Active Task` in a fresh context. See `agents/hf-implementer.md`.

### Required skill

`hf-implementer` MUST use `hf-test-driven-dev` as its implementation discipline:

- write and confirm test design before implementation
- produce fresh RED evidence
- produce fresh GREEN evidence
- keep RED / GREEN / REFACTOR separated by Two Hats
- write the full Refactor Note
- sync wisdom delta and `tasks.progress.json`
- return the status shape defined in `implementer-return-contract.md`

### Not allowed

`hf-implementer` MUST NOT:

- choose a different task
- implement multiple tasks in parallel
- treat self-review as `hf-code-review`
- write review or gate verdicts
- skip RED/GREEN evidence because a reviewer will check later

## `hf-reviewer`

### Responsibility

`hf-reviewer` performs independent review in a fresh context for any canonical review node, not only after TDD implementation. See `agents/hf-reviewer.md`.

### Required skill

`hf-reviewer` MUST load and apply the specific review skill selected by the parent session:

- `hf-discovery-review`
- `hf-spec-review`
- `hf-design-review`
- `hf-ui-review`
- `hf-tasks-review`
- `hf-test-review`
- `hf-code-review`
- `hf-traceability-review`

It returns the normal reviewer return contract, including `conclusion`, `record_path`, `next_action_or_recommended_skill`, `needs_human_confirmation`, and `reroute_via_router`.

### Not allowed

`hf-reviewer` MUST NOT:

- edit implementation code
- silently fix issues instead of reporting findings
- approve its own implementation
- replace gate verdicts
- advance the workflow without the parent session consuming the return contract

## Parent session enforcement

The parent session enforces the role split:

1. dispatch `hf-implementer` with bounded task text and required `hf-test-driven-dev` discipline
2. reject any implementer `DONE` response missing RED/GREEN evidence or Refactor Note
3. return to `hf-workflow-router` after implementer handoff is complete; dispatch `hf-reviewer` when the router starts the batch review chain
4. reject reviewer output that lacks the reviewer return contract fields
5. route fixes back to `hf-implementer` or `hf-workflow-router` based on the reviewer verdict

## Boundary

The two-role model improves subagent-driven execution without introducing team mode. There is still one authoritative `Current Active Task`, one parent session controller, and the HF review/gate verdict chain remains authoritative even when executed once per batch.

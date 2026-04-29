---
name: Feature request
about: Propose new behavior or a new HarnessFlow skill / setup path
title: "FEATURE: <short description>"
labels: ["enhancement"]
assignees: []
---

## Before you file

- [ ] I have read the **Scope Note** at the top of `README.md` / `README.zh-CN.md` and confirmed this feature is not explicitly out of scope for v0.1.0 (e.g. release / ops / monitoring / additional clients beyond Claude Code + OpenCode).
- [ ] I have read `docs/decisions/ADR-001-release-scope-v0.1.0.md` (especially **D1 P-Honest**, **D3 platforms**, **D11 docs/principles is reference only**) and confirmed this proposal does not directly contradict an accepted decision. If it does, I am explicitly asking to revisit that decision in section "ADR Impact" below.
- [ ] I have searched existing [open and closed issues](https://github.com/hujianbest/harness-flow/issues?q=is%3Aissue) for similar proposals.

## Problem

What problem does this feature solve? Who is the target user (skill author, agent runtime user, vendor, ...)? Please describe the **problem first**, not the solution.

## Proposed solution

What you'd like HarnessFlow to do. Be specific:

- Which file(s) / directory(ies) change
- Which `hf-*` skill(s) are involved (if any)
- Whether this is additive or breaks an existing contract

## Alternatives considered

What other approaches did you think about, and why this one?

## Scope check

- [ ] This proposal fits within v0.1.x (a patch release on top of `v0.1.0`).
- [ ] This proposal is for v0.2+ (e.g. additional client setup, new `hf-*` skill).
- [ ] This proposal is for v1.0+ (e.g. release / ops / monitoring main-chain extension).

## ADR Impact

If this proposal touches a decision in `docs/decisions/ADR-001-release-scope-v0.1.0.md`, list which decisions and explain what would need to change in the ADR for this feature to land.

| ADR ID | Current decision | What this proposal asks |
|---|---|---|
| (e.g. D3) | (Claude Code + OpenCode only) | (Add Cursor as supported client) |

## Additional context

Anything else relevant — links to similar features in other tools (e.g. `addyosmani/agent-skills`), upstream specifications, related issues, etc.

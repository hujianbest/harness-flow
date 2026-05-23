# Pre-Release Engineering Checklist — v1.0.0

- Release: `v1.0.0`
- Date: 2026-05-23
- Conclusion: PASS

## Code & Evidence

- [x] release-wide regression passed (`features/release-v1.0.0/verification/release-regression.md`)
- [x] cross-release traceability summary written (`features/release-v1.0.0/verification/release-traceability.md`)
- [x] SKILL.md anatomy audit passed
- [x] install/uninstall suite passed
- [x] Cursor installed rule points at `.cursor/harness-flow-skills/...`
- [x] plugin and marketplace JSON validate

## Documentation Sync

- [x] `CHANGELOG.md` has `[1.0.0] - 2026-05-23`
- [x] `README.md` / `README.zh-CN.md` mention `skills/`, `agents/`, and `commands/`
- [x] `docs/claude-code-setup.md` updated for v1.0.0 + `commands/`
- [x] `docs/opencode-setup.md` updated for v1.0.0 + `agents/`
- [x] `docs/cursor-setup.md` updated for v1.0.0 + `agents/`
- [x] `SECURITY.md` supported versions updated for `1.0.x`
- [x] release scope ADR written and accepted

## Versioning Hygiene

- [x] `.claude-plugin/plugin.json` version = `1.0.0`
- [x] `.claude-plugin/plugin.json` commands path = `./commands`
- [x] `.claude-plugin/marketplace.json` description refreshed for v1.0.0
- [x] `features/release-v1.0.0/release-pack.md` written

## Worktree / Branch State

- [x] Release work is on branch `cursor/subagent-driven-dev-771d`
- [x] PR #61 should be merged before tag
- [x] No automatic tag executed
- [x] No worktree deletion attempted

## Out of Scope

- [x] No deployment
- [x] No staged rollout
- [x] No monitoring / SLO configuration
- [x] No rollback procedure or drill
- [x] No automatic GitHub Release creation

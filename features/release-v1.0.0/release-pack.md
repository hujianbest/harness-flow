# Release Pack — v1.0.0

## Release Summary

- Version: **v1.0.0**
- Pre-release: **no**
- Bump Type: **major** (v0.6.0 → v1.0.0)
- Scope ADR: `docs/decisions/ADR-012-release-scope-v1.0.0.md`
- Status: **ready-for-tag**
- Started At: 2026-05-23
- Finalized At: 2026-05-23
- Author: cursor cloud agent (按架构师 2026-05-23 "hf发布到v1.0.0版本" 委托执行 release tier)

## Scope Summary

### Included Features / Changes

- **Stable markdown workflow surface**:
  - 29 `hf-*` skills + `using-hf-workflow`
  - existing v0.6 author-side discipline and fast-lane mechanics retained
  - release remains engineer-level tag readiness only
- **`hf-subagent-driven-dev` optional implementation leaf**:
  - delegates one locked `Current Active Task` to `hf-implementer`
  - keeps `hf-test-driven-dev` as the required implementation discipline
  - returns to the existing HF review/gate chain
- **Top-level `agents/` runtime assets**:
  - `agents/hf-implementer.md`
  - `agents/hf-reviewer.md`
  - `hf-reviewer` covers every canonical `hf-*review` node, not only post-TDD reviews
- **Top-level `commands/` runtime assets**:
  - 7 slash command definitions moved from `.claude/commands/`
  - `.claude-plugin/plugin.json` now points at `./commands`
- **Install topology update**:
  - `install.sh` vendors `agents/` alongside `skills/`
  - `uninstall.sh` treats `agents/` as an empty-only parent directory
  - install regression suite covers copy / symlink paths for Cursor and OpenCode

### Deferred / Out of Scope

- Deployment, staged rollout, monitoring, rollback, health check, and post-launch operations remain out of scope.
- `harnessflow-runtime` remains a future optional sidecar per ADR-010.
- Remaining client expansions remain future work.
- No automatic `git tag` or `git push --tags`.

### Reference

- `docs/decisions/ADR-012-release-scope-v1.0.0.md`

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | `features/release-v1.0.0/verification/release-regression.md` | present | Full repo Python/unittest + install suite + JSON validation + diff check |
| cross-feature traceability | `features/release-v1.0.0/verification/release-traceability.md` | present | v1.0.0 scope mapped to changed runtime assets and verification |
| pre-release engineering checklist | `features/release-v1.0.0/verification/pre-release-checklist.md` | present | PASS / N/A items recorded |
| scope ADR | `docs/decisions/ADR-012-release-scope-v1.0.0.md` | present | accepted |
| CHANGELOG entry | `CHANGELOG.md` | present | `[1.0.0] - 2026-05-23` |
| release notes（档 2） | N/A | N/A（项目档 0/1 未启用） | `CHANGELOG.md` is the release note source |

## Docs Sync (sync-on-presence 实际同步路径)

- CHANGELOG Path: `CHANGELOG.md`
- Release Notes Path: N/A（项目档 0/1 未启用）
- ADR Status:
  - `docs/decisions/ADR-012-release-scope-v1.0.0.md`: accepted
- Long-Term Assets Sync:
  - `README.md` / `README.zh-CN.md`: runtime asset layout (`skills/` + `agents/` + `commands/`)
  - `docs/claude-code-setup.md`: v1.0.0 scope + `commands/`
  - `docs/opencode-setup.md`: v1.0.0 scope + `agents/`
  - `docs/cursor-setup.md`: v1.0.0 scope + `agents/`
  - `SECURITY.md`: supported versions updated to `1.0.x`
- Project Metadata Sync:
  - `.claude-plugin/plugin.json`: version → `1.0.0`, commands → `./commands`
  - `.claude-plugin/marketplace.json`: v1.0.0 description

## Tag Readiness

- Suggested Tag: `v1.0.0`
- Suggested Commit: merge commit for PR #61 after it lands on `main`
- Release Base Branch: `main`
- PR Status: PR #61 open; tag after merge
- Tag 操作执行者: 项目维护者（**本 skill 不自动执行 git tag / git push --tags**）

## Worktree Disposition

| Feature / Release Work | Disposition | Notes |
|---|---|---|
| `features/release-v1.0.0/` | in-place | release pack produced on current branch |
| PR #61 branch | kept-for-pr | merge before tagging |

## Final Confirmation (interactive only)

- Confirmation Status: confirmed by user intent (`hf发布到v1.0.0版本`)
- Confirmed By: user / architect
- Confirmed At: 2026-05-23 UTC
- Next Action Or Recommended Skill: `null`（tag 操作交项目维护者）

## Limits / Open Notes

- Out-of-scope capabilities handled by project-owned processes:
  - deployment / staged rollout / monitoring / rollback / health check / post-launch operations
- Known limitations:
  - OpenCode / Cursor do not consume `commands/` as slash commands; they continue to use natural-language intent + `using-hf-workflow`
  - `harnessflow-runtime` is not included in v1.0.0
- Open questions:
  - Future client-specific command adapters can now reuse top-level `commands/`

## Handoff

- Next Action Or Recommended Skill: `null`
- **不**写回 hf-workflow-router（本 skill 与 router 解耦）
- PR / Branch Status: PR #61 should be merged before maintainer tags
- Suggested Maintainer Actions:
  1. Merge PR #61 into `main`
  2. `git tag v1.0.0 <merge-commit>`
  3. `git push origin v1.0.0`
  4. Create GitHub Release from `CHANGELOG.md` `[1.0.0]` section

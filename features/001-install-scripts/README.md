# Feature: 001-install-scripts

## Metadata

- Feature ID: `001-install-scripts`
- Title: 为 HarnessFlow 增加 Cursor / OpenCode 安装脚本
- Owner: cursor agent（按用户 2026-05-11 委托执行；参考 `affaan-m/everything-claude-code` 的 install/uninstall 拓扑）
- Started: 2026-05-11
- Closed:
- Workflow Profile: full
- Execution Mode: auto

## Status Snapshot

- Current Stage: hf-design
- Current Active Task:
- Pending Reviews And Gates: hf-design-review
- Closeout Type:

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Spec | `spec.md` | approved（2026-05-11）|
| Spec Deferred Backlog | `spec-deferred.md` | present |
| Design | `design.md` | draft（待 hf-design-review）|
| UI Design（如适用） | `ui-design.md` | N/A（CLI-only，无 UI surface）|
| Data Model（如分文件） | `data-model.md` | N/A |
| API Contracts（草稿） | `contracts/` | N/A |
| Tasks | `tasks.md` | pending |
| Task Board（如适用） | `task-board.md` | N/A（任务量小，由 tasks.md 直承）|
| Progress | `progress.md` | live |
| Closeout | `closeout.md` | pending |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| spec-review | `reviews/spec-review-2026-05-11.md` | 通过（Round 2）| 2026-05-11 |
| spec-approval | `approvals/spec-approval-2026-05-11.md` | APPROVED | 2026-05-11 |
| design-review | `reviews/design-review-2026-05-11.md` | | |
| design-approval | `approvals/design-approval-2026-05-11.md` | | |
| tasks-review | `reviews/tasks-review-2026-05-11.md` | | |
| tasks-approval | `approvals/tasks-approval-2026-05-11.md` | | |
| code-review（每任务） | `reviews/code-review-task-NNN.md` | | |
| test-review（每任务） | `reviews/test-review-task-NNN.md` | | |
| traceability-review | `reviews/traceability-review.md` | | |

## Verification

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| regression | `verification/regression-2026-05-11.md` | | |
| completion（每任务） | `verification/completion-task-NNN.md` | | |

## Linked Long-Term Assets

- ADRs: `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md`（proposed）
- arc42 sections affected: N/A（HF 仓库未启用 arc42）
- Runbooks updated/created: N/A
- SLO updated: N/A
- Release notes: N/A（本 feature 在下一个 vX.Y.Z release 时统一记入）
- CHANGELOG entry: 拟在 `CHANGELOG.md` 下一个 Unreleased 段记录

## Worktree

- Workspace Isolation: in-place
- Worktree Path: /workspace
- Worktree Branch: cursor/install-scripts-c90e
- Worktree Disposition:

## Backlinks

- Supersedes prior feature:
- Superseded by future feature:
- Related hotfix incidents:

# Feature: 002-html-closeout-report

HF closeout 阶段产出一份**可视化 HTML 工作总结报告**，作为现有 `closeout.md` 的衍生 view，使非工程读者也能直观读出本轮 workflow 的工件、评审、覆盖率等关键证据。

## Metadata

- Feature ID: `002-html-closeout-report`
- Title: HF closeout 增加可视化 HTML 工作总结报告
- Owner: cloud-agent (HarnessFlow maintainers TBD)
- Started: 2026-05-09
- Closed:
- Workflow Profile: full
- Execution Mode: interactive
- Targeted Release: v0.4+（v0.3.0 已锁定范围 — 见 ADR-003 D2，本 feature 修改 `hf-finalize` 输出契约不应夹入 v0.3.0 GA）

## Status Snapshot

- Current Stage: `hf-specify`
- Current Active Task: 起草 spec.md
- Pending Reviews And Gates: spec-review
- Closeout Type:

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Spec | `spec.md` | revising-after-review |
| Spec Deferred Backlog | `spec-deferred.md` | present |
| Design | `design.md` | pending |
| UI Design（如适用） | `ui-design.md` | pending（HTML 模板涉及 UI surface） |
| Data Model | `data-model.md` | N/A |
| API Contracts | `contracts/` | N/A |
| Tasks | `tasks.md` | pending |
| Task Board | `task-board.md` | N/A |
| Progress | `progress.md` | live |
| Closeout | `closeout.md` | pending |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| spec-review (round 1) | `reviews/spec-review-2026-05-09.md` | 需修改（10 LLM-FIXABLE） | 2026-05-09 |
| spec-approval | `approvals/spec-approval-YYYY-MM-DD.md` | | |
| design-review | `reviews/design-review-YYYY-MM-DD.md` | | |
| ui-review | `reviews/ui-review-YYYY-MM-DD.md` | | |
| design-approval | `approvals/design-approval-YYYY-MM-DD.md` | | |
| tasks-review | `reviews/tasks-review-YYYY-MM-DD.md` | | |
| tasks-approval | `approvals/tasks-approval-YYYY-MM-DD.md` | | |
| code-review（每任务） | `reviews/code-review-task-NNN.md` | | |
| test-review（每任务） | `reviews/test-review-task-NNN.md` | | |
| traceability-review | `reviews/traceability-review.md` | | |

## Verification

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| regression | `verification/regression-YYYY-MM-DD.md` | | |
| completion（每任务） | `verification/completion-task-NNN.md` | | |

## Linked Long-Term Assets

- ADRs:
- arc42 sections affected:
- Runbooks updated/created:
- SLO updated:
- Release notes:
- CHANGELOG entry:

## Worktree

- Workspace Isolation: in-place
- Worktree Path:
- Worktree Branch: cursor/closeout-html-report-17d3
- Worktree Disposition:

## Backlinks

- Supersedes prior feature:
- Superseded by future feature:
- Related hotfix incidents:

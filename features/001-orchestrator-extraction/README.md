# Feature: 001-orchestrator-extraction

## Metadata

- Feature ID: `001-orchestrator-extraction`
- Title: 把 workflow 编排从 leaf skill 抽出为 always-on agent persona，让 leaf skill 回到 Anthropic Agent Skills 原始定位
- Owner: HF maintainers
- Started: 2026-05-10
- Closed:
- Workflow Profile: full（架构 invariant 引入；router 最终决定）
- Execution Mode: interactive（默认；cloud agent 上下文按 auto 推进）

## Status Snapshot

- Current Stage: hf-tasks-review
- Current Active Task: （tasks 阶段后填入）
- Pending Reviews And Gates: hf-tasks-review
- Closeout Type:

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Discovery 上游 | `../../docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md` | approved（discovery-review 通过） |
| Discovery review | `../../docs/reviews/discovery-review-hf-orchestrator-extraction.md` | 通过 |
| Spec | `spec.md` | approved |
| Design | `design.md` | approved |
| UI Design（如适用） | `ui-design.md` | N/A（HF 自架构 feature，无 UI surface） |
| Data Model（如分文件） | `data-model.md` | N/A |
| API Contracts（草稿） | `contracts/` | N/A |
| Tasks | `tasks.md` | draft |
| Task Board（如适用） | `task-board.md` | （按需） |
| Progress | `progress.md` | live |
| Closeout | `closeout.md` | pending |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| discovery-review | `../../docs/reviews/discovery-review-hf-orchestrator-extraction.md` | 通过（minor LLM-FIXABLE × 3 已在 spec 吸收） | 2026-05-10 |
| spec-review | `reviews/spec-review-2026-05-10.md` | Round 1 需修改 → Round 2 通过（6 finding 全部修订，0 新 finding） | 2026-05-10 |
| spec-approval | `approvals/spec-approval-2026-05-10.md` | 已批准（auto mode；router § 8 关键分支） | 2026-05-10 |
| design-review | `reviews/design-review-2026-05-10.md` | 通过（3 minor LLM-FIXABLE 已在 design commit 内吸收） | 2026-05-10 |
| design-approval | `approvals/design-approval-2026-05-10.md` | 已批准（auto mode） | 2026-05-10 |
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

- ADRs: ADR-007（候选；本 feature 起草，路径 `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`）
- arc42 sections affected: N/A（HF 当前不维护 arc42）
- Runbooks updated/created: N/A
- SLO updated: N/A
- Release notes: 计划在 v0.6.0 release pack 引入；本 feature 触发 HF 第 4 次 dogfood `hf-release`
- CHANGELOG entry: 计划在 v0.6.0 minor 一行段记入

## Worktree

- Workspace Isolation: in-place（discovery + spec 阶段为文档工件，无代码改动；进入 implement 后由 router 重新评估）
- Worktree Path:
- Worktree Branch:
- Worktree Disposition:

## Backlinks

- Supersedes prior feature: 无（HF 第一个 coding-family feature，前作均为 release-tier）
- Superseded by future feature:
- Related hotfix incidents: 无

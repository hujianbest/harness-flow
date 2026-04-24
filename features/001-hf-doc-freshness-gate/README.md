# Feature: 001-hf-doc-freshness-gate

## Metadata

- Feature ID: `001-hf-doc-freshness-gate`
- Title: 在 HF 主链上引入独立 gate `hf-doc-freshness-gate`，确保每次完成增量开发后对外可见文档（README / 模块 README / 公共 API doc / i18n 副本 / 用户文档站）按 sync-on-presence 同步
- Owner: Cursor Cloud Agent (HF self-application)
- Started: 2026-04-23
- Closed:
- Workflow Profile: standard
- Execution Mode: auto

## Status Snapshot

- Current Stage: hf-tasks（已起草）→ hf-tasks-review pending
- Current Active Task: 待 tasks-approval 后由 router 锁定 T1
- Pending Reviews And Gates: hf-tasks-review → 任务真人确认 → hf-test-driven-dev (T1..T7 闭环) → test/code/traceability review → regression-gate / doc-freshness-gate (dogfooding) / completion-gate → hf-finalize
- Closeout Type:

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Spec | `spec.md` | approved (spec-approval-2026-04-23.md) |
| Design | `design.md` | approved (design-approval-2026-04-23.md；含 6 LLM-FIXABLE 已回修) |
| UI Design（如适用） | `ui-design.md` | N/A（无 UI surface） |
| Data Model（如分文件） | `data-model.md` | N/A |
| API Contracts（草稿） | `contracts/` | N/A |
| Tasks | `tasks.md` | approved (tasks-approval-2026-04-23.md；含 11 LLM-FIXABLE 已回修) |
| Task Board（如适用） | `task-board.md` | N/A |
| Progress | `progress.md` | live |
| Closeout | `closeout.md` | pending |
| Discovery（上游） | `../../docs/insights/2026-04-23-hf-doc-freshness-gate-discovery.md` | approved |
| Discovery Review | `../../docs/reviews/discovery-review-hf-doc-freshness-gate.md` | 通过 |
| Experiment HYP-001 | `../../docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/` | Pass |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| discovery-review | `../../docs/reviews/discovery-review-hf-doc-freshness-gate.md` | 通过 | 2026-04-23 |
| spec-review | `reviews/spec-review-2026-04-23.md` | 通过（Reviewer Agent ID: 1fb2f95f-bad4-48c0-b0be-7932b3d093eb） | 2026-04-23 |
| spec-approval（规格真人确认） | `approvals/spec-approval-2026-04-23.md` | approved (auto-mode follow-up 授权落盘) | 2026-04-23 |
| design-review | `reviews/design-review-2026-04-23.md` | 需修改 → 6 LLM-FIXABLE 全部已回修 (Reviewer Agent ID: 0876f73f-23da-4f99-9cfa-305c1d62ca78) | 2026-04-23 |
| ui-review（如适用） | N/A（无 UI surface） | | |
| design-approval | `approvals/design-approval-2026-04-23.md` | approved (auto-mode follow-up; reviewer 协议允许 LLM-FIXABLE post-fix 直接 approve) | 2026-04-23 |
| tasks-review | `reviews/tasks-review-2026-04-23.md` | 需修改 → 11 LLM-FIXABLE 全部已回修 (Reviewer Agent ID: ee4d8ebb-6cd7-4f90-a200-e377569301f3) | 2026-04-23 |
| tasks-approval | `approvals/tasks-approval-2026-04-23.md` | approved (auto-mode follow-up; 同 spec/design approval 边界) | 2026-04-23 |
| code-review（每任务） | `reviews/code-review-task-NNN.md` | | |
| test-review（每任务） | `reviews/test-review-task-NNN.md` | | |
| traceability-review | `reviews/traceability-review.md` | | |

## Verification

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| regression | `verification/regression-YYYY-MM-DD.md` | | |
| completion（每任务） | `verification/completion-task-NNN.md` | | |

## Linked Long-Term Assets

- ADRs: ADR-0001（启用 ADR pool）/ ADR-0002（独立 gate 节点）/ ADR-0003（router 位置 regression 后、completion 前）—— 状态全为 `proposed`，待 design-review 通过 + 设计真人确认 + hf-finalize 翻为 `accepted`
- arc42 sections affected: 项目当前未启用 `docs/arc42/`，按 `sdd-artifact-layout.md` 档 0 用 `README.md` + ADR pool 承接
- Runbooks updated/created: N/A（本 feature 不引入运维点）
- SLO updated: N/A
- Release notes: 待 closeout
- CHANGELOG entry: 待 closeout

## Worktree

- Workspace Isolation: in-place
- Worktree Path: N/A
- Worktree Branch: `cursor/discovery-doc-freshness-gate-d0e2`
- Worktree Disposition:

## Backlinks

- Supersedes prior feature: N/A（首个 feature）
- Superseded by future feature:
- Related hotfix incidents: N/A

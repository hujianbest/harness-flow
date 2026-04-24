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

- Current Stage: hf-design（已起草）→ hf-design-review pending
- Current Active Task:
- Pending Reviews And Gates: hf-design-review → 设计真人确认 → hf-tasks → hf-tasks-review → 任务真人确认 → hf-test-driven-dev → 测试 / 代码 / 追溯评审 → 回归 / 完成 / doc-freshness gate → 收尾
- Closeout Type:

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Spec | `spec.md` | approved (spec-approval-2026-04-23.md) |
| Design | `design.md` | draft（含 §10 lightweight checklist 草样 / §16 walking skeleton / §14 NFR 承接全表）；待 hf-design-review |
| UI Design（如适用） | `ui-design.md` | N/A（无 UI surface） |
| Data Model（如分文件） | `data-model.md` | N/A |
| API Contracts（草稿） | `contracts/` | N/A |
| Tasks | `tasks.md` | N/A（待 design 通过） |
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
| design-review | `reviews/design-review-2026-04-23.md` | pending（reviewer subagent 待派发） | |
| ui-review（如适用） | N/A（无 UI surface） | | |
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

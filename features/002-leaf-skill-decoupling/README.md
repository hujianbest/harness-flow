# Feature: 002-leaf-skill-decoupling

## Metadata

- Feature ID: `002-leaf-skill-decoupling`
- Title: 实施 ADR-007 D3 Step 2-5 — leaf skill 解耦使其真正成为 standalone-usable SOPs；v0.7.0 一次性发布完整版
- Owner: HF maintainers
- Started: 2026-05-10
- Closed:
- Workflow Profile: full（24 leaf 批量修改 + release-blocking 假设升级到运行时等价证明）
- Execution Mode: auto

## Status Snapshot

- Current Stage: hf-tasks（继承 ADR-007 + ADR-008；不重新 spec/design）
- Current Active Task: （tasks-review 通过后启动 Tier 1）
- Pending Reviews And Gates: hf-tasks-review → hf-test-driven-dev (Tier 1+2) → hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-completion-gate → hf-finalize → hf-release
- Closeout Type:

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Upstream ADR (architecture) | `../../docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` | accepted (v0.6.0 closeout) |
| Upstream ADR (release scope) | `../../docs/decisions/ADR-008-v0.7.0-skip-v0.6.0-tag-and-deliver-step-2-5-as-single-release.md` | 起草中 |
| Upstream feature (Step 1) | `../001-orchestrator-extraction/` | workflow-closeout (v0.6.0 中间产物) |
| Spec | （继承 features/001 spec.md + ADR-007 D3 Step 2-5；不创建独立 spec） | inherited |
| Design | （继承 features/001 design.md + ADR-007 D1 Amendment；不创建独立 design） | inherited |
| Tasks | `tasks.md` | draft |
| Progress | `progress.md` | live |
| Closeout | `closeout.md` | pending |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| tasks-review | `reviews/tasks-review-2026-05-10.md` | | |
| tasks-approval | `approvals/tasks-approval-2026-05-10.md` | | |
| test-review (Tier 1) | `reviews/test-review-tier1-2026-05-10.md` | | |
| test-review (Tier 2) | `reviews/test-review-tier2-2026-05-10.md` | | |
| code-review | `reviews/code-review-2026-05-10.md` | | |
| traceability-review | `reviews/traceability-review-2026-05-10.md` | | |

## Verification

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| regression-gate (HYP-002 + HYP-005 release-blocking 升级到运行时等价) | `verification/regression-gate-2026-05-10.md` | | |
| completion-gate | `verification/completion-gate-2026-05-10.md` | | |
| walking-skeleton 端到端 (HYP-002 升级版) | `verification/walking-skeleton-runtime-2026-05-10.md` | | |
| HYP-005 验证 (orchestrator 纯 artifact 驱动) | `verification/orchestrator-pure-artifact-driven-2026-05-10.md` | | |

## Linked Long-Term Assets

- ADRs: ADR-007 (architecture; v0.6.0 已 accepted) + ADR-008 (本 release 范围；起草中，待本 feature closeout 翻 accepted)
- Release Notes / CHANGELOG: 整合为单 `[0.7.0]` 段（per ADR-008 D6；删除原 `[0.6.0]` 段）
- arc42 sections affected: N/A
- Runbooks updated/created: N/A
- SLO updated: N/A

## Worktree

- Workspace Isolation: in-place（24 leaf 批量修改 + 文档同步；纯 markdown 工作）
- Worktree Path: cursor/v0.7.0-leaf-skill-decoupling-e404
- Worktree Branch: cursor/v0.7.0-leaf-skill-decoupling-e404
- Worktree Disposition:

## Backlinks

- Supersedes prior feature: `features/001-orchestrator-extraction/`（v0.6.0 Step 1，已 workflow-closeout 但不打 tag；本 feature 实施 Step 2-5 完整兑现）
- Superseded by future feature: 无
- Related hotfix incidents: 无（v0.6.0 pre-tag 阶段的 PR #46 + #47 fix 已合并到 main，作为本 feature 的实施基础）

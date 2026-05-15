# Feature: 002-omo-inspired-v0.6

## Metadata

- Feature ID: `002-omo-inspired-v0.6`
- Title: HF v0.6 — Author-side discipline 升级 + Execution Mode fast lane（参照 OMO 已验证机制）
- Owner: cursor cloud agent（架构师 2026-05-13 委托执行；参考 `code-yeongyu/oh-my-openagent` 的实现）
- Started: 2026-05-13
- Closed: —
- Workflow Profile: full
- Execution Mode: auto（架构师本会话原话："auto mode 完成，中间不要停下来"——按 ADR-009 治理）

## Status Snapshot

- Current Stage: `hf-specify`（spec 草稿已落，等 `hf-spec-review`）
- Current Active Task: 待 spec / design / tasks 走完后由 router 锁定
- Pending Reviews And Gates: spec-review
- Closeout Type: 待定（v0.6 release 时可能并入 release-v0.6 release-pack）

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Spec | `spec.md` | 草稿（2026-05-13） |
| Spec Deferred Backlog | `spec-deferred.md` | TBD（spec-review 后按需创建） |
| Design | `design.md` | 未开始（需 spec approval） |
| UI Design | `ui-design.md` | N/A（HF 自身是纯 markdown skill pack，无 UI surface） |
| Data Model | `data-model.md` | TBD（wisdom-notebook 5 文件 schema 可能拆出） |
| API Contracts | `contracts/` | N/A（无外部 API；runtime 接口在 v0.7 feature） |
| Tasks | `tasks.md` | 未开始（需 design approval） |
| Task Board | `task-board.md` | TBD（task 数量 ≥ 12 时拆） |
| Progress | `progress.md` | live（auto mode 下含 Fast Lane Decisions 段，按 ADR-009 D4 schema） |
| Closeout | `closeout.md` | 未开始 |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| spec-review | `reviews/spec-review-YYYY-MM-DD.md` | 待 | — |
| spec-approval | `approvals/spec-approval-YYYY-MM-DD.md` | 待 | — |
| design-review | `reviews/design-review-YYYY-MM-DD.md` | — | — |
| design-approval | `approvals/design-approval-YYYY-MM-DD.md` | — | — |
| tasks-review | `reviews/tasks-review-YYYY-MM-DD.md` | — | — |
| tasks-approval | `approvals/tasks-approval-YYYY-MM-DD.md` | — | — |
| code-review | `reviews/code-review-YYYY-MM-DD.md` | — | — |
| test-review | `reviews/test-review-YYYY-MM-DD.md` | — | — |
| traceability-review | `reviews/traceability-review.md` | — | — |

> **Auto mode 注**（按 ADR-009 D2）：本 feature 在 auto mode 下，spec / design / tasks 的 approval step 可由 `hf-ultrawork` 自动 APPROVED 并写工件，但 8 个 Fagan review 节点 + 3 个 gate 不可绕过；reviewer 必须是与作者不同的 agent session（含本会话之外的后续会话 / 不同 cloud agent / 用户本人）。

## Verification

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| regression | `verification/regression-YYYY-MM-DD.md` | — | — |
| doc-freshness | `verification/doc-freshness-YYYY-MM-DD.md` | — | — |
| completion | `verification/completion-YYYY-MM-DD.md` | — | — |

## Linked Long-Term Assets

- ADRs:
  - `docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md`（accepted，本 feature 的范围锚点）
  - `docs/decisions/ADR-009-execution-mode-fast-lane-governance.md`（accepted，本 feature 的 fast lane 治理）
  - `docs/decisions/ADR-010-harnessflow-runtime-sidecar-boundary.md`（accepted，与本 feature 解耦的 v0.7 runtime 边界）
- arc42 sections affected: N/A（HF 仓库未启用 arc42）
- Runbooks updated/created: N/A
- SLO updated: N/A
- Release notes: 计划在 v0.6 release（`features/release-v0.6/`）时统一记入
- CHANGELOG entry: 拟在 `CHANGELOG.md` 下一个 Unreleased 段记录"v0.6 author-side + fast lane scope"

## Worktree

- Workspace Isolation: in-place
- Worktree Path: /workspace
- Worktree Branch: cursor/v06-omo-inspired-roadmap-and-first-feature-spec-5b22
- Worktree Disposition: 待 spec/design/tasks 走完后再决定是否切独立 worktree

## Backlinks

- Supersedes prior feature: 无
- Superseded by future feature: 无
- Related hotfix incidents: 无
- Related sibling features: `features/003-harnessflow-runtime/`（未创建；v0.7 触发时另起）

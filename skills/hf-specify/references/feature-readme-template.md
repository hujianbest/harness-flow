# Feature: <NNN>-<slug>

使用说明：

- 这是 `features/<NNN>-<slug>/README.md` 模板。
- 它是 feature 周期内的入口与状态总览页。在没有 schema 校验/CI lint 的前提下，本 README 同时承担"索引"与"缺件检查表"的双重职责，新接手的人/agent 只读这一页就能定位本 feature 的所有过程交付件。
- 必须由 `hf-specify` 在 feature 启动时创建，并由后续每个 hf-* skill 在产出新工件时同步更新对应行的状态与路径。
- 若项目在 项目声明了等价模板，优先遵循项目约定。

## Metadata

- Feature ID: 例如 `003-rate-limiting`
- Title: 一句话主题
- Owner:
- Started:
- Closed:                                  # closeout 之后写入
- Workflow Profile:                        # full / standard / lightweight
- Execution Mode:                          # interactive / auto

## Status Snapshot

- Current Stage:                           # canonical 节点名
- Current Active Task:
- Pending Reviews And Gates:
- Closeout Type:                           # 未 closeout 时留空；之后写 task-closeout / workflow-closeout

## Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Spec | `spec.md` | draft / approved |
| Design | `design.md` | draft / approved |
| UI Design（如适用） | `ui-design.md` | draft / approved / N/A |
| Data Model（如分文件） | `data-model.md` | present / N/A |
| API Contracts（草稿） | `contracts/` | present / N/A |
| Tasks | `tasks.md` | draft / approved |
| Task Board（如适用） | `task-board.md` | present / N/A |
| Progress | `progress.md` | live |
| Closeout | `closeout.md` | pending / present |

## Reviews & Approvals

| 节点 | 记录路径 | 结论 | 日期 |
|---|---|---|---|
| spec-review | `reviews/spec-review-YYYY-MM-DD.md` | | |
| spec-approval | `approvals/spec-approval-YYYY-MM-DD.md` | | |
| design-review | `reviews/design-review-YYYY-MM-DD.md` | | |
| ui-review（如适用） | `reviews/ui-review-YYYY-MM-DD.md` | | |
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

- ADRs:                                    # 例：ADR-0042, ADR-0043
- arc42 sections affected:                 # 例：docs/arc42/05_building_block_view.md
- Runbooks updated/created:                # 例：docs/runbooks/rate-limiter.md
- SLO updated:                             # 例：docs/slo/notification-api.md
- Release notes:                           # 例：docs/release-notes/v1.5.0.md
- CHANGELOG entry:                         # 例：CHANGELOG.md v1.5.0

## Worktree

- Workspace Isolation:                     # in-place / worktree-required / worktree-active
- Worktree Path:
- Worktree Branch:
- Worktree Disposition:                    # closeout 之后写入

## Backlinks

- Supersedes prior feature:                # 如有
- Superseded by future feature:            # closeout 后被新 feature 改写时回填
- Related hotfix incidents:                # 如有

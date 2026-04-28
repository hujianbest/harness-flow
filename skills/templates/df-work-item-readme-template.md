# Work Item: <Work Item ID>-<slug>

使用说明：

- 这是 `features/AR<id>-<slug>/README.md` 或 `features/DTS<id>-<slug>/README.md` 模板。
- 由 `df-specify`（需求开发）或 `df-problem-fix`（DTS / hotfix）在 work item 启动时创建，并由后续每个 `df-*` skill 在产出新工件时同步更新对应行。
- 若项目在 `AGENTS.md` 中声明了等价模板，优先遵循项目约定。

## Metadata

- Work Item Type:                          # AR / DTS / CHANGE
- Work Item ID:                            # 例：AR12345 / DTS67890
- Title:
- Owning Component:                        # 唯一所属组件
- Related IR:
- Related SR:
- Related AR:                              # DTS 影响功能需求时填写
- Owner / Assignee:
- Started:
- Closed:                                  # closeout 之后写入
- Workflow Profile:                        # standard / component-impact / hotfix / lightweight
- Execution Mode:                          # interactive / auto

## Status Snapshot

- Current Stage:                           # canonical df-* 节点
- Pending Reviews And Gates:
- Blockers:
- Closeout Verdict:                        # 未 closeout 时留空

## Process Artifacts

| 工件 | 路径 | 状态 |
|---|---|---|
| Requirement | `requirement.md` | draft / approved / N/A |
| Reproduction（DTS） | `reproduction.md` | present / N/A |
| Root Cause（DTS） | `root-cause.md` | present / N/A |
| Fix Design（DTS） | `fix-design.md` | present / N/A |
| AR Design Draft | `ar-design-draft.md` | draft / approved |
| Traceability | `traceability.md` | live |
| Implementation Log | `implementation-log.md` | live |
| Progress | `progress.md` | live |
| Completion | `completion.md` | pending / present |
| Closeout | `closeout.md` | pending / present |

## Reviews & Gates

| 节点 | 记录路径 | Verdict | 日期 |
|---|---|---|---|
| spec-review | `reviews/spec-review.md` | | |
| component-design-review | `reviews/component-design-review.md` | | |
| ar-design-review | `reviews/ar-design-review.md` | | |
| test-check | `reviews/test-check.md` | | |
| code-review | `reviews/code-review.md` | | |
| completion-gate | `completion.md` | | |

## Long-Term Assets Affected

- Component Implementation Design:        # docs/component-design.md，本次是否新增/修订
- AR Implementation Design:               # docs/ar-designs/AR<id>-<slug>.md
- Interfaces:                             # 可选：docs/interfaces.md，仅当项目已启用；未启用写 N/A
- Dependencies:                           # 可选：docs/dependencies.md，仅当项目已启用；未启用写 N/A
- Runtime Behavior:                       # 可选：docs/runtime-behavior.md，仅当项目已启用；未启用写 N/A

## Backlinks

- Supersedes prior work item:
- Superseded by future work item:
- Related hotfix incidents:

# Work Item: <Work Item ID>-<slug>

使用说明：

- 这是 work item README 模板，覆盖以下场景：
  - `features/SR<id>-<slug>/README.md`（需求分析子街区）
  - `features/AR<id>-<slug>/README.md` / `features/DTS<id>-<slug>/README.md` / `features/CHANGE<id>-<slug>/README.md`（实现子街区）
- 由 `df-specify`（需求 / SR 澄清）或 `df-problem-fix`（DTS / hotfix）在 work item 启动时创建，并由后续每个 `df-*` skill 在产出新工件时同步更新对应行。
- 若项目在 `AGENTS.md` 中声明了等价模板，优先遵循项目约定。

## Metadata

- Work Item Type:                          # SR / AR / DTS / CHANGE
- Work Item ID:                            # 例：SR1234 / AR12345 / DTS67890
- Title:
- Owning Component:                        # AR / DTS / CHANGE 必填；SR 可空（子系统级）
- Owning Subsystem:                        # SR 必填；AR / DTS / CHANGE 可空
- Related IR:
- Related SR:                              # AR 工作项必填
- Related AR:                              # DTS 影响功能需求时填写
- Owner / Assignee:
- Started:
- Closed:                                  # closeout 之后写入
- Workflow Profile:                        # requirement-analysis（SR）/ standard / component-impact / hotfix / lightweight
- Execution Mode:                          # interactive / auto

## Status Snapshot

- Current Stage:                           # canonical df-* 节点
- Pending Reviews And Gates:
- Blockers:
- Closeout Type:                           # closeout 之后写入：implementation / analysis / blocked
- Closeout Verdict:                        # 未 closeout 时留空：closed / blocked

## Process Artifacts

| 工件 | 路径 | 状态 | 适用 work item |
|---|---|---|---|
| Requirement | `requirement.md` | draft / approved / N/A | 通用 |
| Reproduction（DTS） | `reproduction.md` | present / N/A | DTS |
| Root Cause（DTS） | `root-cause.md` | present / N/A | DTS |
| Fix Design（DTS） | `fix-design.md` | present / N/A | DTS |
| Component Design Draft | `component-design-draft.md` | draft / approved / N/A | SR / AR component-impact |
| AR Design Draft | `ar-design-draft.md` | draft / approved / N/A | AR / DTS（**不**适用 SR） |
| Traceability | `traceability.md` | live | 通用（列集按类型） |
| Implementation Log | `implementation-log.md` | live / N/A | AR / DTS / CHANGE |
| Progress | `progress.md` | live | 通用 |
| Completion | `completion.md` | pending / present / N/A | AR / DTS / CHANGE（SR 写 N/A） |
| Closeout | `closeout.md` | pending / present | 通用 |

## Reviews & Gates

| 节点 | 记录路径 | Verdict | 日期 | 适用 work item |
|---|---|---|---|---|
| spec-review | `reviews/spec-review.md` | | | 通用 |
| component-design-review | `reviews/component-design-review.md` | | | SR（修订组件设计时）/ AR component-impact |
| ar-design-review | `reviews/ar-design-review.md` | | | AR / DTS（**不**适用 SR） |
| test-check | `reviews/test-check.md` | | | AR / DTS / CHANGE |
| code-review | `reviews/code-review.md` | | | AR / DTS / CHANGE |
| completion-gate | `completion.md` | | | AR / DTS / CHANGE（**不**适用 SR） |

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

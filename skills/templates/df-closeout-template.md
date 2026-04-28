# df Closeout

使用说明：

- 这是 `df-finalize` 的 closeout 记录模板。
- **默认保存路径：`features/<Work Item Id>-<slug>/closeout.md`**
- df 单 work item 的 finalize 不再判断剩余任务（df 以单 AR / DTS 为最小开发单元，不维护 task queue），因此 closeout 默认是 work item 收口。
- 若项目在 `AGENTS.md` 中声明了等价模板或路径，优先遵循项目约定。

## Closeout Summary

- Work Item Type:                          # AR / DTS / CHANGE
- Work Item ID:
- Owning Component:
- Closeout Verdict: `closed` | `blocked`
- Based On Completion Record:              # features/<id>/completion.md
- Date:

## Evidence Matrix

| 工件 | 路径 | 状态 |
|---|---|---|
| Requirement | `requirement.md` | present |
| Spec Review | `reviews/spec-review.md` | 通过 |
| Component Design Review | `reviews/component-design-review.md` | 通过 / N/A |
| AR Design Review | `reviews/ar-design-review.md` | 通过 |
| Test Effectiveness Review | `reviews/test-check.md` | 通过 |
| Code Review | `reviews/code-review.md` | 通过 |
| Completion Gate | `completion.md` | 通过 |

## Long-Term Assets Sync

| 长期资产 | 路径 | 本次是否同步 | 备注 |
|---|---|---|---|
| Component Implementation Design | `docs/component-design.md` | yes / no / N/A | |
| AR Implementation Design | `docs/ar-designs/AR<id>-<slug>.md` | yes / N/A | DTS 不修改 AR 设计时写 N/A |
| Interfaces（可选） | `docs/interfaces.md` | yes / no / N/A（项目未启用） | |
| Dependencies（可选） | `docs/dependencies.md` | yes / no / N/A（项目未启用） | |
| Runtime Behavior（可选） | `docs/runtime-behavior.md` | yes / no / N/A（项目未启用） | |

填写规则：

- 已启用资产 + 本次触发变化 → `yes`
- 已启用资产 + 本次未触发变化 → `no`
- 项目尚未启用此可选资产 → `N/A（项目未启用）`，**不**算 blocked；相关变化应已合并进 `docs/component-design.md` 对应章节
- AR 工作项**必须**在 `docs/ar-designs/` 留下本 AR 的正式设计文档；DTS 不修改 AR 设计时该行写 `N/A`

## State Sync

- Final `Current Stage`:                   # closed / completed
- Final `Next Action Or Recommended Skill`:  # null（已完成）
- Outstanding Risks Recorded To:           # 例：组件级 risk log / backlog 路径

## Handoff

- 提交 / 合并状态:                         # branch / MR / PR 信息
- 团队同步说明:
- Limits / Open Items:

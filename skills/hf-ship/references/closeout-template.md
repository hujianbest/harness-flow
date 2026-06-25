# closeout.md 模板

使用说明：`hf-ship` 生成组件根下 `features/<id>-<slug>/closeout.md`（或团队覆盖路径）。closeout 是结构化收尾记录，不是模糊总结。一页内。

```markdown
# <id>-<slug> 收尾

## DoD 核验结果

逐项结论（满足 / 缺口 + 去向）。不是"整体通过"。

| DoD 项 | 结论 | 证据 / 去向 |
|---|---|---|
| 1. spec 存在且 R1 通过 | 满足 | reviews/spec-r1.md verdict=pass |
| ... | ... | ... |

## Promotion 路径表

| 过程工件 | 长期资产路径 | 状态 |
|---|---|---|
| spec.md | docs/ar-specs/<id>-<slug>.md | 已同步（Promoted From @ <commit>） |
| design.md | docs/ar-designs/<id>-<slug>.md | 已同步 |
| component-design-draft.md | docs/component-design.md | 已同步（仅状态机章节） |
| spec.md（缺陷工作项） | —— | N/A（无规格变更） |

## 遗留债务

| 债务 | 去向 |
|---|---|
| <描述> | 新工作项 <id> / issue <链接> |

（无债务时写「无」；「后续优化」无去向 = 未登记债务。）

## 复盘

一句话：本次流程哪里最磨损，反哺哪个 skill 或模板。
```

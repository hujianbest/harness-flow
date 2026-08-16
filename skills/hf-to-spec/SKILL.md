---
name: hf-to-spec
description: 把当前会话综合为规格并写入 features/<id>/spec.md，不进行访谈。HarnessFlow 主链步骤；完成后宜经 hf-review 规格评审再进 architecture。
---

# hf-to-spec

综合已有对话与代码库理解，产出规格。**不要访谈**——只综合已知内容。

## HarnessFlow 桥接

1. 更新 `progress.md` 当前阶段为 `to-spec`。有 UI 时加载 `hf-ui-design`。
2. 把规格写入 `features/<id>/spec.md`。
3. 写完后执行 `hf-review`（规格检查清单）→ `reviews/spec-review.md` + 用户确认/`auto-approved`。
4. 评审通过后进入 `hf-to-architecture`。

## 流程

1. 必要时探索仓库。使用 `CONTEXT.md` 中的词汇；遵守 ADR。

2. 勾勒测试缝。优先使用既有缝；尽可能选择最高层的缝；数量越少越好（理想情况：一个）。与用户确认这些缝（`auto`：如必须代为选择，则记录假设）。

3. 使用下方模板编写规格。

## 规格模板

## Problem Statement

从用户视角描述问题。

## Solution

从用户视角描述方案。

## User Stories

一长串编号列表：

1. As an \<actor\>, I want a \<feature\>, so that \<benefit\>

## Implementation Decisions

触及的模块/接口、技术澄清、schema/API 约定。避免会过期的文件路径清单。能编码决策的原型片段可内联并标明来源。

## Testing Decisions

何为好测试（外部行为）；测哪些模块/缝；仓库中的既有范例。

## Out of Scope

## Further Notes

文末加：

```markdown
- 用户确认:
```

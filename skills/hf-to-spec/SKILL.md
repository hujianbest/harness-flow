---
name: hf-to-spec
description: 把当前会话综合为规格并写入特性目录/任务跟踪器，不进行访谈。HarnessFlow 主链第三步；进入前运行 gate check --to to-spec。完成后必须经 hf-review 规格评审，才能进入 architecture 阶段。
---

# hf-to-spec

综合已有对话与代码库理解，产出规格。**不要访谈**——只综合已知内容。

## HarnessFlow 桥接

1. 运行 `hf_gate.py check --feature features/<id> --to to-spec`，将 `RESULT` 写入 `progress.md`。结果为 `FAIL` 时停止。
2. 未配置任务跟踪器时，默认把规格写入 `features/<id>/spec.md`；若已运行 `hf-setup-skills`，则按其任务跟踪器配置发布。
3. 写完后执行 `hf-review`（规格检查清单）→ `reviews/spec-review.md` + 用户确认/`auto-approved`。
4. 通过后才能 `check --to to-architecture`。

## 流程

1. 必要时探索仓库。使用 `CONTEXT.md` 中的词汇；遵守 ADR。

2. 勾勒测试缝。优先使用既有缝；尽可能选择最高层的缝；数量越少越好（理想情况：一个）。与用户确认这些缝（`auto`：如必须代为选择，则记录假设）。

3. 使用下方模板编写规格。发布到真实任务跟踪器时应用 `ready-for-agent`。

## 规格模板

## 问题陈述

从用户视角描述问题。

## 解决方案

从用户视角描述解决方案。

## 用户故事

一份很长的编号列表：

1. 作为 \<actor\>，我想要 \<feature\>，从而获得 \<benefit\>

## 实现决策

涉及的模块/接口、技术澄清、模式/API 契约。不要罗列会过时的文件路径。可以内联体现某项决策的原型片段，并明确标注其为原型。

## 测试决策

说明什么是良好的测试（外部行为）、测试哪些模块/缝，以及仓库中可参考的既有做法。

## 范围外事项

## 补充说明

文末加:

```markdown
- 用户确认:
```

---
name: hf-review
description: HarnessFlow 独立评审。规格、设计或实现完成后必须经本技能给出正式评审结论,才能进入下一阶段。适用于评审 spec.md、design.md 或已完成的代码与测试;按阶段加载对应 checklist。不修改被评审对象,只产出结论与 findings。
---

# 评审 (Review)

一套评审协议,三份阶段 checklist。评审的产出是**落盘的结论**,不是聊天里的一句"看起来不错"。

## 独立性

**作者不能给自己评审结论。** 按优先级选择评审执行方式:

1. **派发独立 subagent**(有 subagent 能力时,如 Cursor/Claude Code 的 Task 工具):只给它被评审工件的路径、上游工件路径、本技能与对应 checklist 的路径,**不带作者会话的推理过程**,让它冷读后返回结论与 findings。
2. **主会话冷读**(无 subagent 能力时):放下作者立场,只依据磁盘上的工件逐条过 checklist,不引用"我当时为什么这么写"的记忆为问题开脱。

## 流程

### 1. 确定评审对象与 checklist

| 评审对象 | Checklist | 记录路径 |
|---------|-----------|---------|
| `spec.md` | `references/spec-checklist.md` | `reviews/spec-review.md` |
| `design.md` | `references/design-checklist.md` | `reviews/design-review.md` |
| 实现代码 + 测试 | `references/code-checklist.md` | `reviews/code-review.md` |

### 2. 冷读并逐条检查

通读被评审工件与其上游(评设计要读规格,评代码要读设计与规格)。逐条过 checklist,每发现一个问题记一条 finding:

```markdown
- [严重|一般|建议] <位置>: <问题描述> → <修改建议>
```

- **严重**:不修就会导致下游阶段建立在错误基础上(需求不可测、设计漏掉需求、测试造假)
- **一般**:应当在批准前修复的质量问题
- **建议**:可选改进,不阻塞

### 3. 给出结论并落盘

写入对应的 `reviews/*.md`:

```markdown
# <对象> 评审 (第 N 轮)

- 日期: YYYY-MM-DD
- 结论: 通过 | 需修改

## Findings
<逐条列出;"通过"且无 findings 时写"无">
```

结论规则:存在**严重**或**一般** finding → `需修改`;只有**建议**级 → 可以`通过`并附带建议。不允许"通过但是……"的混合结论。

### 4. 结论处理

- `需修改` → 回到作者阶段(hf-specify / hf-design / hf-tdd),**只修 findings 指出的问题**,然后重新评审;复审只需确认 findings 是否闭合,不从头再评。
- `通过` → 规格与设计评审在 `interactive` 模式下向用户展示 1-2 句结论摘要并等待确认;`auto` 模式下记录 `auto-approved` 后直接进入下一阶段。代码评审通过后进入 `hf-ship`。

## 红线

- 评审者顺手修改被评审对象("我帮你改了"→ 应写成 finding)
- 用作者会话的上下文替代冷读("我记得这里是有原因的")
- findings 不指向具体位置,只有"整体感觉不够好"
- 明知有严重问题仍给"通过",理由是"后面再补"
- 复审时重新翻案已闭合的 findings 或扩大评审范围

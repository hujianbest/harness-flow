---
name: hf-bug-patterns
description: Use when AI notices repeated mistakes, recurring review findings, or bugfix lessons that may deserve codifying as a reusable bug pattern with human confirmation before writing to a catalog.
---

# HF Bug Patterns

把“这次又犯了同一种错”从会话记忆变成可复用经验。这个 skill 不是 HF workflow 的 mandatory gate，而是一个独立的经验固化旁路：当 AI 发现某类错误在不同任务、review、hotfix 或会话里重复出现时，用它判断这条经验是否值得沉淀成团队 bug pattern，并先征求真人确认。

## Methodology

本 skill 融合以下已验证方法：

- **Defect Pattern Catalog (Beizer/Ostrand)**: 将历史缺陷分类为可复用的模式家族（边界/null、状态/时序、资源泄露、AI 盲点），让团队从错误中系统性学习。
- **Blameless Post-Mortem / Learning Review**: 把“谁写错了”改写成“什么机制容易反复出错”，让经验能跨任务复用。
- **Human-In-The-Loop Knowledge Curation**: 经验是否固化为长期目录，由真人确认，不让 AI 自动把偶发事件写成团队规范。

## When to Use

适用：
- 这次问题和之前犯过的错误明显相似，AI 怀疑它会重复发生
- review / hotfix / debug / code review 中出现 recurring finding，值得提炼成通用模式
- 用户明确要求“把这条经验固化”“沉淀成 bug pattern”“更新缺陷模式目录”
- AI 已能指出当前案例 + 至少一个历史案例或明确的高风险复发信号

不适用：
- 当前主要任务是写/修代码 → `hf-test-driven-dev`
- 当前主要任务是评审测试或代码质量 → `hf-test-review` / `hf-code-review`
- 只有一次模糊直觉，没有“重复/高损失/高复发”的证据
- 想把它当成 `hf-test-review` 前的必经 gate

## Hard Rules

- 不得把本 skill 作为 HF 主链的 mandatory next action
- 不得在没有真人确认时写入或改写 bug pattern catalog
- 不得编造“以前也发生过”的历史；重复信号必须有证据锚点
- 不得只保留事故叙事，必须抽象成“怎么识别 / 怎么预防 / 怎么验证”的模式
- 不用 canonical workflow next action 代替“是否固化”的人工确认问题

## Workflow

### 1. 建立候选经验的证据基线

读取最小必要证据：
- 当前案例：review finding、hotfix 记录、代码锚点、失败测试、实现交接块或相关 diff
- 历史相似案例：过去 review / hotfix / bugfix / 复盘记录，或用户明确提供的“以前也犯过”
- 现有目录：若已有 bug pattern catalog，先查是否已经存在同类模式
- 模板：`references/bug-pattern-catalog-template.md`

### 2. 判断“值不值得固化”

只有满足以下至少 2 条，才值得进入候选草稿：
- **重复性**：至少出现过一次相似历史案例，或当前就是高复发信号
- **可泛化**：问题不是某个文件的偶发 typo，而是同类机制都会中招
- **可行动**：能写出明确的识别信号、预防动作和验证建议
- **价值足够高**：高频、高损失、评审中容易漏掉，或 AI 特别容易重复犯

若不满足，明确说明“暂不值得固化”，并停止，不勉强落盘。

`not-yet` 结论也要给出最小观察计划，而不是只说“不固化”。至少补 3 件事：
- 目前缺什么证据（历史案例、稳定复现、可泛化机制、验证建议等）
- 下一次再出现时应该记录什么信号
- 满足什么升级条件后可以重新考虑写入 catalog

### 3. 起草候选 bug pattern

把案例抽象成候选模式，而不是事故纪要。至少写清：
- 候选模式名（可临时命名）
- 当前案例 + 历史案例的证据锚点
- 问题表现
- 根因模式
- 识别信号
- 预防动作
- 验证建议
- 扩散面检查

### 4. 人工确认检查点

在写入前，必须先问真人是否固化。默认提问格式：

> 这条经验看起来值得固化成 bug pattern。是否要我把它写入 `<catalog_path>`？

约束：
- 即使当前 `Execution Mode=auto`，这里也必须暂停，不能自动落盘
- 如果用户说“先不固化”，就保持为候选，不写文件
- 如果用户说“合并到已有模式”，则更新现有条目而不是重复新增

### 5. 写入或更新 catalog（仅在确认后）

保存位置优先级：
- 若项目级约定中声明了 engineering insights / bug pattern catalog 路径，优先遵循
- 否则默认：`docs/insights/bug-pattern-catalog.md`

若文件不存在，按 `references/bug-pattern-catalog-template.md` 初始化；若已存在，则追加新模式或合并更新现有模式。

### 6. 返回结果与可选后续

本 skill 的主要产出是：
- 是否值得固化
- 候选模式草稿
- 是否已获真人确认
- 若已写入，则返回 `catalog_path` 和模式 ID

若结论是 `not-yet`，还要返回：
- 缺失证据
- 观察项
- 升级条件

如果当前任务还需要修复或补测试，可**额外建议** `hf-test-driven-dev` / `hf-test-review` 等，但不要把本 skill 写成 HF 主链上的必经节点。

## Output Contract

默认输出结构：

```markdown
## 候选模式判断

- 候选名称：
- 是否值得固化：yes | no | not-yet
- 主要依据：
- 当前案例证据：
- 历史案例证据：

## 候选模式草稿

- 问题表现：
- 根因模式：
- 识别信号：
- 预防动作：
- 验证建议：
- 扩散面检查：

## 人工确认

- 目录路径：
- 问题：是否要我把它固化到该目录？
```

若结论是 `not-yet`，改为：

```markdown
## 暂不固化

- 缺失证据：
- 观察项：
- 升级条件：
```

用户确认后，再写文件并补：

```markdown
## 落盘结果

- catalog_path：
- pattern_id：
- 写入方式：new | update
```

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-test-driven-dev` | 写/修代码、TDD 实现；本 skill 只判断经验是否值得固化，不改代码 |
| `hf-test-review` | 评审当前测试是否充分；本 skill 负责把跨会话 recurring mistake 提炼成长期模式 |
| `hf-code-review` | 评审当前代码质量；本 skill 关注“这类错误是否值得进入经验目录” |
| `hf-hotfix` | 处理单个线上缺陷的复现与最小修复边界；本 skill 抽象跨案例可复用教训 |
| `hf-workflow-router` | 决定 HF 主链下一步；本 skill 不是 workflow router，也不产出 canonical gate 结论 |

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/bug-pattern-catalog-template.md` | bug pattern catalog 模板；新建或更新目录时使用 |

## Red Flags

- 只有一次模糊直觉，就急着固化成长期经验
- 没有人类确认就直接写目录
- 把当前事故原样复制进去，没有抽象成通用模式
- 发明“以前也发生过”的历史案例
- 继续把本 skill 当成 `hf-test-review` 前的 mandatory gate

## Verification

- [ ] 当前案例与历史案例证据已明确
- [ ] 已判断这条经验是否值得固化
- [ ] 已向真人明确询问是否落盘
- [ ] 若用户确认，catalog 已写入或更新
- [ ] 若用户未确认，未擅自写文件
- [ ] `not-yet` 时已给出缺失证据、观察项和升级条件
- [ ] 输出包含候选模式名、机制、预防动作和验证建议

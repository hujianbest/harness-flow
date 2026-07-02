---
name: hf-workflow
description: HarnessFlow 主工作流入口。凡是开发新功能、修改已有行为、修复缺陷,或用户提到"开始开发""继续""恢复进度""harness-flow"时,必须先加载本技能。它定义 specify → review → design → review → tdd → review → ship 主链、工件布局、阶段门禁、状态恢复规则,以及领域扩展技能 (ext-*) 的加载方式。不适用于纯问答、代码阅读等不产生代码变更的请求。
---

# HarnessFlow 主工作流

HarnessFlow 用一条固定的主链约束 AI 编码工作,分三层:

1. **SDD 层(规范驱动)**:先把"要做什么"写成可评审、可验收的规格,再谈实现。
2. **TDD 层(测试驱动)**:实现必须由失败的测试驱动,交付时每条需求都有通过的测试作证据。
3. **扩展层(领域技能)**:UI 设计、语言规范等 `ext-*` 技能在对应阶段被加载,增强但不替代主链。

## 主链

```
specify → review → design → review → tdd → review → ship
```

| # | 阶段 | 技能 | 产出 | 通过门禁 |
|---|------|------|------|----------|
| 1 | 规格 | `hf-specify` | `spec.md` | 规格评审通过 + 用户确认 |
| 2 | 规格评审 | `hf-review` | `reviews/spec-review.md` | 结论为"通过" |
| 3 | 设计 | `hf-design` | `design.md`(含任务清单) | 设计评审通过 + 用户确认 |
| 4 | 设计评审 | `hf-review` | `reviews/design-review.md` | 结论为"通过" |
| 5 | 实现 | `hf-tdd` | 代码 + 测试 + 任务勾选 | 全部任务完成,测试全绿 |
| 6 | 代码评审 | `hf-review` | `reviews/code-review.md` | 结论为"通过" |
| 7 | 交付 | `hf-ship` | 验收报告 + 收尾 | 验收标准逐条闭合 |

到达某一阶段时,读取并遵循对应技能的 `SKILL.md`,不要凭印象执行。

## 工件布局

每个特性一个目录,所有阶段产物落盘于此:

```
features/<NNN>-<slug>/
  spec.md          # 需求规格 (hf-specify)
  design.md        # 技术设计 + 任务清单 (hf-design)
  progress.md      # 状态文件:当前阶段、任务进度、下一步
  reviews/         # 评审记录 (hf-review)
```

`<NNN>` 取 `features/` 下已有编号的下一个,从 `001` 开始。`progress.md` 最小格式:

```markdown
# 进度

- 特性: <NNN>-<slug>
- 当前阶段: specify | spec-review | design | design-review | tdd | code-review | ship | done
- 执行模式: interactive | auto
- 已加载扩展: <ext-* 列表或"无">
- 下一步: <一句话>

## 任务进度
<tdd 阶段起,从 design.md 任务清单同步,逐项勾选并附测试命令>
```

## 状态恢复

**从磁盘工件恢复状态,不依赖聊天记忆。** 用户说"继续"或开启新会话时,按下表判定:

| 磁盘证据 | 当前阶段 |
|---------|---------|
| 无 `spec.md` | specify |
| 有 `spec.md`,无通过的 spec-review | spec-review |
| spec 已批准,无 `design.md` | design |
| 有 `design.md`,无通过的 design-review | design-review |
| design 已批准,任务清单未全部完成 | tdd(锁定首个未完成任务) |
| 任务全完成,无通过的 code-review | code-review |
| code-review 通过,未收尾 | ship |

`progress.md` 与工件冲突时,以工件为准并修正 `progress.md`。

## 硬性规则

- **门禁不可跳过**:上一阶段未通过评审(及用户确认)前,不进入下一阶段。评审结论为"需修改"时回到作者阶段修订,再评审。
- **作者与评审者分离**:产出工件的一方不能给自己评审结论,见 `hf-review`。
- **单任务推进**:tdd 阶段同一时间只做一个任务,做完勾掉再取下一个。
- **证据落盘**:评审结论、任务勾选、测试命令都写入特性目录,让任何新会话可以冷启动接续。

## 执行模式

- `interactive`(默认):spec 与 design 的评审通过后,向用户展示结论并等待确认,用户确认后才进入下一阶段。
- `auto`:用户明确说"自动执行/不用等我确认"时启用。评审通过即视为确认并在 `progress.md` 记录 `auto-approved`,连续推进直到 ship 完成或评审失败需要用户输入。auto 不删除任何评审与门禁。

## 轻量通道

仅限**微小改动**(文档、注释、typo、单行低风险修复):向用户说明后可压缩为 tdd → review → ship,由一段简短的 `progress.md` 记录改动意图代替 spec/design。用户不同意或改动触碰行为边界时,走完整主链。

## 加载扩展技能 (第三层)

扩展技能放在 `skills/ext-*/`,每个扩展在 SKILL.md 开头声明**绑定阶段**与**触发条件**。

进入每个阶段前:

1. 列出 `skills/` 下所有 `ext-*` 目录,读取各自 frontmatter 的 `description`。
2. 触发条件与当前特性匹配(如:特性含 UI 界面、项目是 C++ 技术栈)且绑定阶段等于当前阶段的,加载其 SKILL.md 并遵循。
3. 把已加载的扩展记入 `progress.md` 的"已加载扩展",后续阶段保持一致。

扩展只能收紧要求(追加检查项、规范、产出章节),不能放松主链门禁。编写新扩展见 `references/extension-authoring.md`。

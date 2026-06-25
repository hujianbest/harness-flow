# HF Skill 质量契约

> 适用于 HarnessFlow 全部技能（阶段、overlay、领域、工具）。无论生成还是手写都必须满足。
> 来源：DevFlow 契约 + 高星仓库蒸馏（Superpowers、anthropics/skills、awesome-claude-skills、awesome-cursorrules）。

## 1. 命名与布局

- 目录与 frontmatter `name` 一致，全小写、连字符。
- 阶段技能名前缀 `hf-`；语言标准 `<language>-coding-standards`；领域 `<domain>-development`。
- 布局：

```text
skills/<name>/
  SKILL.md            # 高频高危内容（阶段 ≤~400 行；coding-standards ≤300 行硬上限）
  references/         # 可选：低频细则、模板、契约
  evals/evals.json    # 必需：>=3 压力场景
```

## 2. Frontmatter

`description` 只写**触发条件**（含正/负触发），不总结内部流程。模式：

```yaml
description: 在 <具体场景/文件类型/症状> 时使用。<2-3 句正触发>。不适用于 <相邻负触发>。
```

证据（Superpowers writing-skills）：把 description 写成流程摘要会让模型照摘要走、跳过正文。

## 3. 每条规则三要素

1. **可判定性**：能对一段具体代码/工件裁定违规/不违规。出现"良好/合理/适当/尽量"即不合格。
2. **事故类**：防止什么真实失败（一句话，决定 severity）。
3. **正反例**：目标语言/场景的最小 ❌/✅ 对比。反例选模型真实会写出的形态，不是稻草人。

禁止形态："禁止 X"而不给替代；纯表格平铺无代码的主题节。

## 4. 反合理化表

点名具体偷懒话术 + 反驳，把违规框定为"破坏信任"而非"效率问题"：

```text
| 话术 | 现实 |
|---|---|
| 「测试全绿，所以没问题」 | 测试只证明外部行为，不替代 clean-code 自检 |
```

## 5. 自检清单

每个主题节至少一条可勾选项。完成声明必须由"通过的测试/构建输出/评审记录"支撑，而非"看起来对"。

## 6. evals

`evals/evals.json` >=3 场景，覆盖该技能最高危失败。每个场景：诱导违规的 prompt（含看似合理的理由）+ expected（应触发的拒绝/修正）+ expectations（可勾选检查点）。

## 7. 单一职责 + 范围纪律

一个技能解决一个问题。显式写"不做什么"（堵住膨胀）：一次性任务、已有文档标准、项目约定（→ AGENTS.md）、可正则强制的机械约束，不收入技能。

## 8. artifact-first 恢复

进度从工件恢复（`plan.md`、`reviews/`、`traceability.md`），不依赖聊天记忆。新会话只读工件即可续作。

## 9. 写作风格

祈使句 + 解释 why，不堆砌 `MUST`（anthropics 明确把过量 MUST 列为 smell）。前置决策树/速查表，中段示例，结尾 Common Mistakes。

## 10. 校验

- `python3 scripts/validate_harnessflow.py` 必须通过（技能清单、frontmatter、旧名残留、evals >=3、coding-standards ≤300 行、markdown 链接、agent frontmatter）。
- `python3 -m pytest tests/test_validate_harnessflow.py` 必须通过。

# `<language>-coding-standards` 结构契约

> 配套 `coding-standards-creator`。任何语言编码规范技能（无论生成还是手写）都必须满足本契约。
> 本契约是**语言专属**结构契约，叠加在通用 `hf-skill-quality-contract.md` 之上（通用基线不再重复）。
> 契约存在的目的：让每个语言技能都能被 HarnessFlow 各阶段以同一种方式消费，新增语言不需要改动任何阶段技能。

## 1. 命名与布局

- 目录与 frontmatter `name` 一致：`<language>-coding-standards`，全小写、连字符；`<language>` 使用项目内约定的语言标识
- 布局：

```text
skills/<language>-coding-standards/
  SKILL.md            # 高频高危规则（≤300 行硬上限）
  references/         # 可选：低频细则、团队规则号对照表、框架专项
  evals/evals.json    # 必需：≥3 个压力场景
```

## 2. Frontmatter

description 只写触发条件，模式：

```yaml
description: 在编写、修改或评审 <语言> 代码（<源文件/测试/构建脚本等具体形态>）时使用。
  提供 <3-5 个核心主题> 的具体规则与正反例。只适用于 <语言>；其他语言代码使用对应语言自己的 coding-standards 技能。
```

要点：含语言名与典型文件类型等触发词；写清适用边界与相邻语言的负触发，但不要引用具体相邻技能名称；不总结技能内部流程（通用要求见 `hf-skill-quality-contract.md` §2）。

## 3. 职责边界

**只收语言级规则**——离开这门语言就不成立的规则：

- 资源/内存/所有权在该语言的正确表达（RAII、try-with-resources、context manager）
- 语言陷阱与未定义/意外行为（宏多次求值、整数提升、可变默认参数、equals/hashCode）
- 错误处理在该语言的惯用形态（错误码/异常/Result/checked exception 策略）
- 类型系统的正确使用（const/final/Optional/类型注解）
- 语言专属工具链（编译警告基线、linter、格式化、静态分析、sanitizer）
- 通用规则的**语言特化形态**（PEP 8 命名细则属于 Python 技能；"命名要表意"不属于）

**三不收**：

1. 通用整洁代码规则 → `hf-clean-code`（技能开头一行引用："本技能在 `hf-clean-code` 之上叠加 <语言> 规则，不能替代通用 clean-code 自检"）
2. 工程领域规则（中断、实时性、ASIL、Web 安全策略等） → 对应领域技能
3. 流程规则（评审/提交/分支/文档） → AGENTS.md 或团队流程文档

**冲突标注**：团队规则覆盖 HarnessFlow 默认时，规则处显式写"团队约定，覆盖 HarnessFlow 默认 X"。隐藏冲突会让模型在两份指令间随机摇摆。

## 4. 章节形态

```text
# <Language> Coding Standards
## 总览          —— 该语言的核心危险或核心承诺一两句；声明"项目已声明的标准子集优先，
                    本文是未声明时的默认底线"；声明建立在 hf-clean-code 之上
## <主题节> × 4-8 —— 按事故密度排序；每节 = 规则 + 正反例 + 针对的事故类
## 工具链         —— 真实命令与基线：警告级别、linter/格式化配置、静态分析处理纪律
                    （新增项修复或带理由抑制；"历史就有"不豁免本次触碰）
## 自检清单       —— 每个主题节至少一条可勾选项
```

可选节：合理化反驳表（该语言常见的偷懒话术）、references 索引表。

## 5. 规则写法三要素

每条规则必须有（通用要求见 `hf-skill-quality-contract.md` §3）：

1. **可判定性**：能对一段具体代码裁定违规/不违规。出现"良好/合理/适当/尽量"即不合格。
2. **事故类**：防止什么真实失败。写在规则旁（一句话即可），它决定 severity 与取舍。
3. **正反例**：目标语言的最小代码对比。❌ 在前 ✅ 在后或并列；反例选模型真实会写出的形态，不是稻草人。

禁止形态："禁止 X"而不给替代；纯表格平铺无代码的章节（速查表可以有，但主题节不能只有表）。

## 6. 规模与 progressive disclosure

- SKILL.md ≤ ~300 行（`validate_harnessflow.py` 的硬上限）：装不下说明取舍没做完——按"事故密度 × 出现频率"裁剪，长尾进 references/
- references/ 文件按主题命名（如 `concurrency-rules.md`、`team-rule-mapping.md`），SKILL.md 给出明确指针
- 团队内部规则编号与技能规则的对照表（审计需要时）放 references/，不占主文件

## 7. 消费点（语言技能如何被 HarnessFlow 使用）

语言技能自身不是流程阶段，也不是 `hf-clean-code` 的替代品。被以下位置按"适用的 `<language>-coding-standards`"约定引用时，必须与 `hf-clean-code` 同时进入 Quality Stack——**因此新增语言无需改任何阶段技能**：

| 消费方 | 用法 |
|---|---|
| `hf-design` | 设计接口契约/错误模型时遵循语言的错误策略与所有权表达 |
| `hf-tdd` / implementer subagent | 实现与重构时遵循；Context Pack 的 `required_skill_files` 同时列出 `hf-clean-code` 与适用语言技能路径，返回的 `loaded_skills` 必须覆盖二者 |
| `hf-review` code rubric | "语言与领域规则"节逐项检查 |
| `hf-ship` DoD | 适用约束审计表中每种语言一行（clean / documented-debt / critical-open / N/A） |
| `using-hf` | 按命名约定发现：工作项触及语言 X 的代码 → 叠加 `<x>-coding-standards`（存在时） |

## 8. evals 要求

`evals/evals.json` ≥3 个场景，覆盖该语言最高危的事故类。每个场景：一段诱导模型违规的 prompt（含一个看似合理的理由）+ expected 列出技能应触发的拒绝/修正行为。需要参考时，选择一个既有 `<language>-coding-standards` 的 evals，按目标语言改写。格式与 HF 全部技能一致（通用要求见 `hf-skill-quality-contract.md` §6）。

## 9. 验收清单

- [ ] 命名、布局、frontmatter 符合 §1-2
- [ ] 全部规则是语言级；与 `hf-clean-code` / 领域技能零重复；冲突已标注；总览明确本技能叠加在 `hf-clean-code` 之上且不能替代它
- [ ] 每条规则三要素齐全；无不可判定词
- [ ] 每个主题节至少一组目标语言正反例
- [ ] 工具链节是真实命令与基线，不是泛泛建议
- [ ] SKILL.md ≤ 300 行；长尾在 references/ 且有指针
- [ ] evals ≥3 场景且对准高危事故类
- [ ] 技能名已追加进 `scripts/validate_harnessflow.py` 的 `EXPECTED_SKILLS`
- [ ] `python3 scripts/validate_harnessflow.py` 与 `python3 -m pytest tests/test_validate_harnessflow.py` 通过

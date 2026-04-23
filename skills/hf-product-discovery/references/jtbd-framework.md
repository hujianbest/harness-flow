# JTBD / Jobs Stories 参考

## Purpose

本参考为 `hf-product-discovery` 提供 **Jobs-to-be-Done (JTBD)** 的最小落地形态，用于把「用户想要什么能力」重新锚定到「用户在某情境下想取得什么进展、为什么现有方案不够好」。

它不是独立节点，也不是强制格式；只要 discovery 草稿能冷读出「job / situation / progress / struggling moment」四要素，就算符合 JTBD 最小契约。

## One-Line Rule

需求不是功能列表，而是 **用户在特定情境下想要取得的进展**。

## Core Framing

| 要素 | 含义 | 常见误区 |
|---|---|---|
| Job | 用户想要取得的进展（功能 / 情感 / 社交维度） | 把产品功能当作 job |
| Situation | 触发这个 job 的具体情境 | 只写"谁" 不写"在什么情况下" |
| Struggling Moment | 现有方案让用户难受的那一刻 | 只写抱怨，没写具体触发 |
| Progress | 如果 job 完成了，用户状态会变成什么 | 只写"用户满意"，缺具体可观察变化 |
| Pushes / Pulls / Anxieties / Habits | 驱动切换的四力（Christensen） | 只写"他就是想要" |

## Jobs Stories 写法（Alan Klement）

取代传统 user story 的实现驱动结构，用情境驱动的语法：

```text
When  <situation>,
I want to <motivation / progress I'm trying to make>,
so I can <expected outcome>.
```

最小示例：

```text
When 我刚收到一份陌生产品方向需求，
I want to 先判断这个方向值不值得做、打哪个 wedge 最快见效，
so I can 避免直接进入 spec 后才发现方向本身不成立。
```

规则：

- `situation` 写**触发场景**，不写人物头衔
- `motivation` 写**想取得的进展**，不写功能
- `outcome` 写**可观察的状态变化**，不写"效率更高 / 体验更好"这类无阈值口号
- 一条 job story 只覆盖一个主要 job；副 job 拆到下一条

## JTBD 与 discovery 模板的对接

discovery 草稿中，JTBD 信息不必新设章节，而是渗透到以下现有章节：

| discovery 章节 | 应从 JTBD 带入的语义 |
|---|---|
| 问题陈述 | Struggling moment + Situation |
| 目标用户与使用情境 | Situation + Job Performer |
| Why now / 当前价值判断 | Pushes / Pulls / Anxieties 的力量变化 |
| 当前轮 wedge | 最值得先解决的 Job |
| 已确认事实 | 来自真实访谈 / 数据的 job 证据 |
| 关键假设 | 假设的 job / situation / outcome，尚未验证 |
| 候选方向 | 围绕同一个 job 的不同方案 |
| Bridge to Spec | 哪些 job 已稳定到可进入规格 |

## 和四力分析（Forces of Progress）的关系

若主题属于「切换型」场景（用户从旧方案切到新方案），建议额外写出四力：

- **Push of the situation**：现状的推力（为什么非要变）
- **Pull of the new solution**：新方案的吸引力（为什么选它）
- **Anxiety of the new solution**：对新方案的焦虑（为什么犹豫）
- **Habit of the present**：对现有习惯的黏性（为什么留下）

不是每个主题都需要四力分析；只有在**切换决策本身是主要障碍**时才做。

## 最小签入条件

discovery 草稿要进入 `hf-discovery-review` 前，JTBD 维度至少满足：

- [ ] 已能写出一条主 job story（情境驱动，而不是功能驱动）
- [ ] `situation` 是具体触发场景，不是"用户一般来说……"
- [ ] `progress` 不是空泛愿景，而是可观察的状态变化
- [ ] 若有多条候选 job，已经收敛出当前轮主 job（其余进入 later ideas）

## 常见 Red Flag

- 只写"用户想要 X 功能"，没写"用户在什么情境下要取得什么进展"
- 把产品功能（"查看审批流程"）当作 job
- `outcome` 写成实现语言（"系统返回 JSON"）
- 一条 job story 里混着 3 个并列 job
- JTBD 描述脱离真实证据，纯靠猜测

## 衔接

- 结构化候选方向与当前轮 wedge 的选择见 `opportunity-solution-tree.md`
- 当出现多个候选 job / solution、需要量化取舍时，参考 `prioritization-quant.md`

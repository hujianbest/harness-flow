# 量化优先级参考（RICE / ICE / Kano）

## Purpose

在 discovery 与 spec 阶段，当存在**多个候选 opportunity / solution / 需求**，且仅靠 MoSCoW 的 Must/Should/Could/Won't 难以收敛时，本参考提供两套轻量量化方法：**RICE** 和 **ICE**；以及一套质量感知方法 **Kano**。

这些方法**不替代** MoSCoW，而是作为 MoSCoW 的量化补充：MoSCoW 决定「进不进当前轮」，RICE / ICE 决定「同等优先级里先打哪个」，Kano 决定「做到什么档位」。

## One-Line Rule

量化优先级是为了**在多个合理候选之间可被冷读地比较**，不是为了给产品决策贴精确分数。

## 何时使用

- discovery 阶段存在多个候选 opportunity 或多个候选 solution，需要收敛到当前轮 wedge
- spec 阶段有多条 `Must` 候选，互相冲突或超出当前轮容量
- 评审过程中，reviewer 要求 "为什么是它不是另一条"

**不要**在以下场景过度套用：

- 候选只有 1 个或候选完全不同层级
- 数据完全靠猜测，分数只是装饰
- 已经有更强的业务约束（法规 / 合同）直接决定优先级

## RICE

面向 discovery / spec 的**粗粒度**打分法（Intercom 提出）。

```text
RICE = (Reach × Impact × Confidence) / Effort
```

| 维度 | 含义 | 建议取值 |
|---|---|---|
| **Reach** | 单位时间内受影响的用户 / 请求数 | 真实数据优先；无数据写"估算 XX/月"并标注来源 |
| **Impact** | 对单个受影响用户的改善幅度 | 3=massive / 2=high / 1=medium / 0.5=low / 0.25=minimal |
| **Confidence** | 对 Reach × Impact 估算的信心 | 100%=高 / 80%=中 / 50%=低 / <50% 基本不用进候选 |
| **Effort** | 所需 person-month 或等价单位 | 粗粒度即可，1 位有效数字 |

### 写法约定

- 每个维度都必须写**来源 / 证据**，不允许纯凭直觉
- Confidence < 50% 的候选不进入 RICE 汇总；先转成 `hf-experiment` 的假设
- 分数只保留到 1–2 位有效数字，避免"精确到 0.01"的误导
- 分数相近（如 ±20%）的候选**不允许直接拍板**，要补定性理由

### 最小示例

```markdown
| 候选 | Reach | Impact | Confidence | Effort | RICE | 来源 |
|---|---|---|---|---|---|---|
| 入口追问 outcome | 100/月 | 2 | 80% | 0.5 | 320 | 入口会话采样 |
| 首屏显式 OST 骨架 | 100/月 | 1 | 80% | 1 | 80 | 同上 |
| 自动生成 JTBD 模板 | 50/月 | 3 | 50% | 2 | 37.5 | 仅团队猜测，信心偏低 |
```

## ICE

**更轻量**的替代方法（Sean Ellis 提出），适合候选只有 3–5 个、或没有成熟 Reach 数据时。

```text
ICE = Impact × Confidence × Ease
```

| 维度 | 含义 | 建议取值 |
|---|---|---|
| **Impact** | 成功后对 outcome 的改善幅度 | 1–10 |
| **Confidence** | 对效果估算的信心 | 1–10 |
| **Ease** | 实施难度（越容易越高分） | 1–10 |

写法约定与 RICE 相同（每维度带来源、分数相近不自动拍板）。

## RICE vs ICE 选择

| 场景 | 推荐 |
|---|---|
| 有 Reach 数据，或候选涉及不同用户规模 | RICE |
| 候选粒度相近，Reach 基本一致 | ICE |
| 早期 discovery 仅需粗排 | ICE |
| 进入 spec 阶段对多条 Must 排优先级 | RICE |

## Kano（质量感知）

Kano 解决另一维度问题：**一个功能做到什么档位才值得**。分三类：

- **Basic / 必备型**：缺了用户会明显不满；做得再好也不会额外满意（默认门槛）
- **Performance / 期望型**：做得越多越好，线性相关
- **Excitement / 惊喜型**：用户没预期，但做了会惊喜

### 在 HF 中的落点

- 进入 spec 阶段，若某个需求同时存在「最低标准」和「惊喜做法」两条路径时，显式标出 Kano 类别
- discovery 阶段一般不强制 Kano，但若候选 solution 明显属于"做最低档就够" vs "做到惊喜"不同策略，建议备注

### 常见误区

- 把所有候选都打成 "Excitement" （幻想型 Kano）
- 把 Basic 需求当成可延后项
- 用 Kano 代替 MoSCoW（它们回答的是不同问题）

## 与 MoSCoW 的关系

| 问题 | 方法 |
|---|---|
| 这条需求进不进当前轮？ | MoSCoW |
| 同一批候选里先打哪个？ | RICE / ICE |
| 这条需求要做到什么档位？ | Kano |

三者组合写法（discovery / spec 表格示例）：

```markdown
| ID | 描述 | MoSCoW | RICE | Kano |
|---|---|---|---|---|
| OPP-1 | ... | Must | 320 | Basic |
| OPP-2 | ... | Should | 80 | Performance |
| OPP-3 | ... | Could | 37.5 | Excitement |
```

## 和 discovery / spec 的对接

- discovery 阶段：在候选 opportunity / solution 视图中补充 RICE 或 ICE 分数；低 confidence 的候选先转为假设，交 `hf-experiment` 验证
- spec 阶段：对多条 `Must` 候选排 RICE；若涉及档位策略，补 Kano
- 在 discovery 草稿或 spec 中展示的分数必须**附证据来源**，否则视为无效分数

## 常见 Red Flag

- 每个维度都写成"高 / 中 / 低"，没有数字也没有来源
- 分数精确到小数点后两位，但证据是团队想象
- 用 RICE 筛掉 confidence 低的候选，但不把它们转成 experiment
- Kano 被滥用成"给所有候选贴标签"
- MoSCoW 和 RICE 结果相互矛盾，但没有给出任何说明

## 衔接

- JTBD / 情境框架见 `jtbd-framework.md`
- OST 骨架与剪枝原则见 `opportunity-solution-tree.md`
- 假设 / 实验落盘见 `hf-experiment`（最小版 probe plan）

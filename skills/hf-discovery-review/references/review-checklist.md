# 产品发现评审检查清单

评审 discovery 文档时，至少对以下 5 个维度逐项审查。每个维度内部评分 `0-10`，帮助区分轻微缺口与阻塞问题。

## 评分辅助规则

- 任一关键维度低于 `6/10` → 不得返回 `通过`
- 任一维度低于 `8/10` → 通常至少对应一条具体 finding

## 评审维度

| ID | 维度 | Pass Condition |
|---|---|---|
| `P1` | 问题与用户聚焦 | 问题、目标用户和使用情境清楚，不是功能口号堆砌 |
| `W1` | Why-now 与 wedge 收敛 | 当前轮最小 wedge 明确，why-now 不是空泛价值宣言 |
| `A1` | Facts / Assumptions 分离 | 已确认事实、关键假设和 later ideas 显式区分 |
| `R1` | Probe / 风险清晰度 | 高风险假设或建议 probe 方向可回读，不是“以后再看” |
| `B1` | Bridge-to-spec 准备度 | reviewer 能冷读出哪些结论足以进入 `hf-specify`，哪些仍需保留为 assumptions |

## 反模式检测

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `W2` | 只有功能清单，没有问题定义 | 文档主要是 feature bullets | 回到 problem framing 与 user context |
| `A2` | 假设伪装成事实 | 未确认说法被写成稳定结论 | 显式标记为 assumption 或 open question |
| `B2` | 无 bridge 语义 | reviewer 不知道怎么进入 spec | 单列 bridge-to-spec 小节 |
| `D1` | 设计泄漏 | 接口、数据库、服务边界进入 discovery 正文 | 只保留业务意图，把实现细节移出 discovery |
| `L1` | later ideas 隐藏在 prose | 后续候选项没有显式处理 | 写入候选方向 / later ideas 区域 |

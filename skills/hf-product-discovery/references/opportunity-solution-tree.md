# Opportunity Solution Tree 参考

## Purpose

本参考把 Teresa Torres 在 *Continuous Discovery Habits* 中提出的 **Opportunity Solution Tree (OST)** 作为 `hf-product-discovery` 的结构化骨架，用来在 discovery 阶段显式连接：

```text
期望成果 (Desired Outcome)
  ├─ 机会 (Opportunity) ← 从用户 job / pain / desire 发现
  │   ├─ 候选解决方案 (Solution)
  │   │   └─ 假设与实验 (Assumption / Experiment)
  │   └─ 候选解决方案 (Solution)
  └─ 机会 (Opportunity) ...
```

它回答 discovery 阶段最核心的三个问题：

1. 我们这一轮想让什么成果变好？
2. 阻挡这个成果变好的真实用户机会是什么？
3. 我们打算用什么候选方案去打它，这些方案有哪些假设需要先验证？

## One-Line Rule

先锁 **Outcome**，再从 **Opportunity** 长出 **Solution**，再用 **Experiment** 打穿假设；不要直接从方案倒推问题。

## 层次释义

### 1. Desired Outcome（当前轮想变好的成果）

- 必须是**结果指标**，不是产出或活动
- 若项目已有 North Star / OKR，尽量锚定到该体系的一个或少数几个指标
- 一轮 discovery 只围绕 1 个主 outcome，避免"既要又要"
- 示例：
  - 合适：「新用户在首次会话内完成一次可评审 discovery 草稿的比例提高」
  - 不合适：「让产品更好用」

### 2. Opportunity（机会）

- 来自真实证据（访谈、数据、反馈），而不是假想
- 每个 opportunity 都要能回答：**哪个用户 / 情境 / 具体痛点阻挡了 outcome**
- 用 JTBD 的「struggling moment / pushes / anxieties」描述，而不是功能想法
- 同级 opportunity 之间应**互斥**，方便后续优先级判断
- 示例：
  - 合适：「新用户在第一次输入模糊想法时，不知道现在是在做 discovery 还是 spec」
  - 不合适：「新用户需要更清晰的引导」（没有可观察的 struggling moment）

### 3. Solution（候选解决方案）

- **多个候选，而不是一个方案**：每个 opportunity 至少挂 2–3 个候选方案
- solution 要具体到可以被讨论成本 / 风险 / 可逆性，但**不要写成实现细节**
- 不合格的 solution：
  - 「优化引导体验」（太虚）
  - 「用 FSM 重写 router 并改 schema」（已进入 design 层）
- 合格的 solution：
  - 「在 discovery 草稿第一页显式列出 JTBD / Outcome / Opportunity 骨架」
  - 「在 `using-hf-workflow` 入口先追问一次 outcome 再路由」

### 4. Assumption & Experiment（假设与实验）

- 每个 solution 至少写出 1 个关键假设：**如果这个假设不成立，solution 本身就站不住**
- 假设分四类（Teresa Torres 归纳）：
  - **Desirability**：用户真的想要吗？
  - **Viability**：对业务有价值吗？
  - **Feasibility**：技术上做得到吗？
  - **Usability**：用户能用得起来吗？
- 每个关键假设对应一个最小 experiment / probe，留给 `hf-experiment` 负责落盘

## OST 与 discovery 模板对接

discovery 草稿中不一定画出完整的树形图，但应能冷读出以下四层：

| discovery 章节 | 对应 OST 层 | 最小表达 |
|---|---|---|
| Why now / 当前价值判断 + 成功标准 | Desired Outcome | 至少 1 个可判断的 outcome 指标 |
| 当前轮 wedge + 目标用户与情境 | Opportunity | 1 个主 opportunity（可挂 1–2 个子 opportunity） |
| 候选方向与排除项 | Solution | 至少 2 个候选 solution |
| 关键假设 + 建议 probe | Assumption & Experiment | 每个候选 solution 至少 1 个可验证假设 |

示例（放在 discovery 草稿尾部作为收敛视图即可）：

```markdown
## OST Snapshot

Desired Outcome: 新 discovery 会话在单次内达到可评审状态的比例 ≥ 70%

Opportunity A：新用户不知道当前是在 discovery 还是 spec
  Solution A1：入口追问 outcome
  Solution A2：discovery 草稿首屏显式 OST 骨架
    Assumption：用户愿意回答 outcome 问题
    Probe：5 次真实用户对话记录抽检

Opportunity B：...
```

## 如何与候选方向 / 排除项衔接

- OST 中被选中的 solution → 写入 discovery 的 `候选方向`
- OST 中被明确剪掉的 opportunity / solution → 写入 `排除项`，说明**剪的理由**（不合规、证据不足、与当前 outcome 无关等）
- 不允许出现 `候选方向` 里有 solution，但 OST 树里没有对应 opportunity 的情况

## 剪枝原则

OST 不是越大越好，discovery 阶段的树要保持**浅且锐利**：

- Outcome：1
- Opportunity：3–5 个候选，最终选 1 个主 opportunity 进入当前轮
- Solution：每个选中 opportunity 下 2–3 个候选
- Assumption：每个 solution 至多 2 个关键假设，其余写入"次要假设"

超过这个规模时，应考虑：

- 是不是 outcome 太大？拆成两轮 discovery
- 是不是 opportunity 互相重叠？合并或剪枝
- 是不是 solution 已经进入 design 层？回到合适粒度

## 常见 Red Flag

- OST 根节点写的是产品名 / 功能名，而不是 outcome
- Opportunity 直接是"缺 XX 功能"
- Solution 只给一个（没有真实候选）
- 假设写成"用户会喜欢"这种无法证伪的口号
- OST 画得很大，但 discovery 正文里没有对应的 struggling moment 证据
- 用 OST 覆盖了所有产品问题，而不是当前轮 wedge

## 衔接

- 用户 / 情境 / job 的描述来源见 `jtbd-framework.md`
- 多个 opportunity / solution 之间的量化取舍见 `prioritization-quant.md`
- 每个假设的实验落盘由 `hf-experiment` 负责；discovery 本身只写出假设与 probe 建议

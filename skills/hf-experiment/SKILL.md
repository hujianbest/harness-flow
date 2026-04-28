---
name: hf-experiment
description: 适用于产品发现或规格阶段存在低 confidence、高风险或 Blocking 的关键假设，需要一次最小可验证 probe 再决定是否推进主链。不适用于无假设驱动的纯澄清（→ hf-specify）、需新起 discovery（→ hf-product-discovery）、进入正式实现（→ hf-test-driven-dev）、阶段不清（→ hf-workflow-router）。
---

# HF Experiment

在进入 `hf-specify` 前（或 `hf-specify` 内部 Blocking 假设未关闭时），为一条或少数几条**关键假设**产出一份结构化 **probe plan**：明确假设是什么、如何最小验证、多长时间、什么结果算通过、证据落在哪、结果如何回流。

本 skill 是 Phase 0 引入的**轻量节点**，不是完整的实验平台，也不替代 A/B testing 基础设施。它的核心价值在于：**把 discovery / spec 阶段模糊的"我们假设"变成可证伪的"一次小验证"**，避免把未经检验的假设硬推给下游设计或实现。

## Methodology

本 skill 融合以下已验证方法：

| 方法 | 核心原则 | 来源 | 落地步骤 |
|---|---|---|---|
| **Hypothesis-Driven Development** | 把产品决策拆成可证伪假设，而不是先做再看 | Lean Startup, Ries 2011；Intuit *Hypothesis-Driven Development* | 步骤 2 / 3 |
| **Build-Measure-Learn** | 最小构建 → 最小测量 → 显式学习回流 | *The Lean Startup* | 步骤 3–5 |
| **Four Types of Assumptions** | Desirability / Viability / Feasibility / Usability 分类假设 | Teresa Torres *Continuous Discovery Habits* | 步骤 2 |
| **Smallest Testable Probe** | 用最小代价打穿最高风险假设 | Spotify *Think It Build It Ship It Tweak It*；Design Sprint | 步骤 3 |
| **Pre-registered Success Threshold** | 事先声明通过阈值，事后不允许移动门柱 | 研究方法学通行做法 | 步骤 3；步骤 5 回流 |

## When to Use

适用：

- `hf-product-discovery` 或 `hf-discovery-review` 识别出低 confidence / 高风险假设，正式推进前值得先验证
- `hf-specify` 中 Key Hypotheses 存在 `Blocking? = 是` 的假设，规格不能在未验证前通过评审
- 用户明确要求"先做个小验证再决定"
- reviewer 在 discovery-review / spec-review 中返回"请先验证假设 HYP-xxx"

不适用：

- 所有 hypothesis 都已关闭或 confidence 高 → 继续主链
- 问题本质是澄清需求，而不是验证假设 → `hf-specify`
- 需要完整新做 discovery → `hf-product-discovery`
- 进入实现阶段 → `hf-test-driven-dev`
- 阶段 / route / 证据冲突 → `hf-workflow-router`

Direct invoke 信号："先不要写 spec，先做一次最小验证"、"这条假设我们得先 probe"、"review 要求先验证 HYP-003"。

## Hard Gates

- probe plan 未产出 fresh evidence 前，不得宣布假设已验证
- probe plan 的 success threshold 必须**事先**写下，结果出来后不得移动门柱
- 不得把多个假设塞进同一条 probe；一条 probe 对应一条或少数互相耦合的假设
- 不得把 probe 变成隐形实现（写代码 + 上线 = 实现，不是 probe）
- 若验证结果与假设相反，禁止"合理化"推进主链；必须显式回流到 `hf-product-discovery` 或 `hf-specify`
- 若请求已明显跨过假设验证进入设计 / 实现，回到 `hf-workflow-router`

## Workflow

### 1. 读取最少必要上下文

只读完成 probe plan 所需的最少材料：

- 上游 discovery 草稿（默认 `docs/insights/*-discovery.md`）或已在起草的 `features/<active>/spec.md`
- 相关 review 记录（若 reviewer 点名了假设）
- 项目级路径约定（若项目已声明）（若存在）

归纳：

- 要验证的**关键假设**（来自 discovery 的 OST 或 spec 的 Key Hypotheses）
- 每条假设的 Type（Desirability / Viability / Feasibility / Usability）
- 当前 confidence 与 Impact If False
- 该假设是否 Blocking

### 2. 聚焦假设（不要一次打穿所有假设）

选择本轮 probe 的**假设集合**，原则：

- 优先打 **Blocking** 假设
- 其次打 **高 Impact + 低 Confidence** 假设
- 一次 probe 最多同时打 1–2 条假设；且这些假设必须具有**同一个验证路径**的可能
- 其余假设留到后续 probe 或显式接受风险

在 probe plan 中显式列出"本轮 probe 假设"与"本轮 probe 不覆盖的假设"。

### 3. 设计最小 probe

对每条被选中的假设，产出下表最小字段：

| 字段 | 含义 | 要求 |
|---|---|---|
| **Assumption ID** | 对应 `HYP-xxx` 或 discovery OST 中的 assumption | 必须可回指上游 |
| **Restatement** | 重述假设为可证伪的一句话 | 一句话，陈述式 |
| **Type** | Desirability / Viability / Feasibility / Usability | 强制分类 |
| **Method** | 采用的验证方式 | 见下方推荐列表 |
| **Participants / Sample** | 样本 / 参与者 / 数据范围 | 数量 + 来源 |
| **Setup** | 需要搭建 / 准备什么 | 不允许悄悄写产品代码；若非用不可，显式标"一次性原型" |
| **Success Threshold** | 事先声明的通过阈值 | 可证伪，不允许"看起来不错" |
| **Failure Threshold** | 事先声明的失败阈值 | 让结果能落到 Pass / Fail / Inconclusive 三档之一 |
| **Timebox** | 最大允许投入的时间窗口 | 明确的小时 / 天数；超时 = Inconclusive |
| **Evidence Path** | 证据归档位置 | 默认 `docs/experiments/<date>-<slug>/`，见下 |
| **Rollback / Cleanup** | 一次性原型是否需要清理 | 若有则必须写 |

推荐验证方式（按代价由低到高）：

- Desk research / 已有数据再分析
- 用户访谈 / 小范围问卷
- 纸面原型 / wireframe 走查
- 可交互原型（非生产代码）
- 灰度 A/B（仅在已有灰度能力时用，避免为 probe 新建基础设施）
- Spike solution（技术 feasibility 的最小 PoC，运行在隔离目录，明确一次性）

### 4. 产出 probe plan 工件

按 `references/probe-plan-template.md` 写入：

- 默认路径：`docs/experiments/<YYYY-MM-DD>-<slug>/probe-plan.md`
- 若已进入 feature 目录，可放 `features/<active>/experiments/<slug>/probe-plan.md`

plan 文档必须包含：

- 假设列表（含 Restatement / Type）
- 方法、样本、Setup
- Success / Failure Threshold（事先写死）
- Timebox
- 证据归档路径
- 与 discovery / spec 的上游锚点
- 下游回流目标：probe 完成后该回到 `hf-product-discovery` / `hf-specify` / `hf-workflow-router` 的哪一个

### 5. 执行、记录与回流

probe 执行完毕后（或触发 Timebox），产出 **probe result** 文档：

- 默认路径：`docs/experiments/<YYYY-MM-DD>-<slug>/probe-result.md`
- 结论分三档：`Pass` / `Fail` / `Inconclusive`
- 必须回答：结果是否达到 **事先声明** 的 Success Threshold；如果 Fail 或 Inconclusive，为什么

按结果显式回流：

| 结果 | 回流目标 |
|---|---|
| Pass（且对应假设不再 Blocking） | `hf-specify`（若 spec 已在起草）或 `hf-product-discovery`（discovery 阶段） |
| Fail（假设被证伪） | 回 `hf-product-discovery`：修订 OST、重写候选方向；或回 `hf-specify` 修订对应 FR/NFR；必要时回 `hf-workflow-router` 重新路由 |
| Inconclusive（超时 / 样本不够 / 方法缺陷） | 决定：(a) 追加一次小 probe；(b) 显式接受风险并写入 Key Hypotheses 的 "accepted-risk" 标记；(c) 回 `hf-workflow-router` |

回流时必须：

- 把 `HYP-xxx` 的 Confidence 更新写回 spec（若已存在）或 discovery 草稿
- 若假设被证伪，同步把 discovery 的 OST / 候选方向 / 排除项调整过来
- 不允许在主链上"当作没发生"继续往下走

## Output Contract

完成时产出：

- `docs/experiments/<date>-<slug>/probe-plan.md`（必有）
- `docs/experiments/<date>-<slug>/probe-result.md`（probe 执行后必有）
- 如有原始数据 / 截图 / 访谈摘要，归档到同目录的 `artifacts/` 下
- 对上游 discovery / spec 的 HYP 条目做 Confidence / Blocking 更新（若已存在）
- 进度同步：
  - 若在 discovery 阶段，discovery 进度记录的 `Next Action Or Recommended Skill` 暂指向 `hf-experiment`，probe 回流后改回 `hf-discovery-review` 或 `hf-specify`
  - 若在 spec 阶段，feature `progress.md` 的 `Next Action Or Recommended Skill` 暂指向 `hf-experiment`，probe 回流后改回 `hf-specify` 或 `hf-spec-review`

若 probe 结果尚未生成，不伪造回流；明确写出当前停在哪一步。

## 和其他 Skill 的区别

| Skill | 区别 |
|---|---|
| `hf-product-discovery` | discovery 回答"要不要做、打哪个 wedge、有哪些假设"；experiment 回答"关键假设是否站得住"。 |
| `hf-discovery-review` | review 负责独立评审 discovery 草稿质量；experiment 负责执行假设验证。 |
| `hf-specify` | specify 回答"正式做什么、做到什么程度算完成"；experiment 在 Blocking 假设未关闭时先插入。 |
| `hf-workflow-router` | router 负责 runtime routing；本 skill 假设已明确在做假设验证。 |
| `hf-test-driven-dev` | TDD 是在已批准 spec 与 design 之后的实现验证；experiment 是在 spec 之前或之中的**假设**验证。不允许互相替代。 |

## Red Flags

- 一次 probe 同时塞了 4 条假设
- Success Threshold 结果出来后才写
- Probe 悄悄变成了"顺便写一版产品代码"
- 假设被证伪，但仍继续往 spec 推进
- Probe 的 setup 留下了未清理的生产侧改动
- Probe 文档缺失，只有口头结论
- Evidence 归档路径不存在或无法回指上游 HYP

## Reference Guide

按需加载详细参考内容。任一 reference 未命中其"加载时机"时，不需要提前读取。

| 主题 | Reference | 加载时机 | 最小 profile |
|---|---|---|---|
| probe plan / result 模板 | `references/probe-plan-template.md` | 起草 plan 或记录 result 时；每次 probe 至少读一次 | 全档必读 |

加载策略：

- 本 skill 仅在 `full` profile 下激活（standard / lightweight 不激活 `hf-experiment`）
- reference 数量仅 1，full profile 下直接读即可

## Verification

- [ ] probe plan 已保存到约定路径
- [ ] 每条选中假设都有 Restatement / Type / Success Threshold / Failure Threshold / Timebox
- [ ] Success / Failure Threshold 是**事先**写下的
- [ ] 一次 probe 覆盖的假设数量合理（默认 ≤ 2 且共享验证路径）
- [ ] 证据归档路径存在，上游 HYP 可回指
- [ ] 若 probe 已执行，probe-result 文档产出；结论为 Pass / Fail / Inconclusive 之一
- [ ] 结果回流到 discovery / spec：HYP 的 Confidence / Blocking 已更新
- [ ] 若假设被证伪，discovery / spec 的相关部分已同步修订，不以"没发生过"继续推进
- [ ] 进度记录同步：`Next Action Or Recommended Skill` 在 probe 结束后已切回正确节点

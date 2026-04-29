---
name: hf-product-discovery
description: 适用于仍在判断产品问题、目标用户、wedge、关键假设或 probe 方向，尚未收敛到 formal spec 的场景。不适用于已明确进入 spec/design/tasks（→ hf-specify / hf-workflow-router）、或只需评审已有 discovery 草稿（→ hf-discovery-review）。
---

# HF 产品发现

把模糊的产品想法收敛成一份可评审的 discovery 草稿，明确问题、用户、wedge、关键假设与进入 formal spec 前仍需验证的事项。本 skill 不写正式规格，不替代 `hf-specify`。

## Methodology

本 skill 融合以下已验证方法。每条方法都有对应的 reference 与落地章节。

| 方法 | 核心原则 | 来源 | 落地 |
|------|----------|------|------|
| **Problem Framing** | 先定义用户、问题、阻塞进展与 why-now，而不是从功能清单反推问题 | 项目化实践（discovery 通用方法） | 步骤 3；discovery 正文 section 1–3 |
| **Hypothesis-Driven Discovery** | 把"我们觉得应该这样做"拆成可验证假设、风险和 probe 方向，避免把猜测直接写成已确认需求 | Lean Startup, Ries 2011；Teresa Torres *Continuous Discovery Habits* | 步骤 3；discovery 正文 section 6 / 8 |
| **Opportunity / Wedge Mapping** | 在多个候选方向之间收敛当前轮最小 wedge，明确哪些能力进入当前轮、哪些只是后续候选 | 项目化实践（wedge 收敛通用做法） | 步骤 2；discovery 正文 section 4 / 7 |
| **Assumption Surfacing** | 显式写出已确认事实、未确认假设和 open questions，为后续 `hf-specify` 提供稳定 bridge | 项目化实践（HF 上游证据约定） | 步骤 3；discovery 正文 section 5–6 / 13；Bridge to Spec |
| **JTBD / Jobs Stories**（Phase 0 新增） | 需求锚定到「用户在某情境下想取得的进展」，而非功能 | Christensen *Competing Against Luck*；Alan Klement *When Coffee & Kale Compete* | 步骤 3；discovery 正文 section 10；见 `references/jtbd-framework.md` |
| **Opportunity Solution Tree**（Phase 0 新增） | Outcome → Opportunity → Solution → Assumption / Experiment 的收敛骨架 | Teresa Torres *Continuous Discovery Habits* | 步骤 3–4；discovery 正文 section 11；见 `references/opportunity-solution-tree.md` |
| **量化优先级 RICE / ICE / Kano**（Phase 0 新增） | 在多个合理候选之间做可被冷读的比较；不替代 MoSCoW | Intercom (RICE)；Sean Ellis (ICE)；Noriaki Kano (Kano) | 步骤 3；discovery 正文 section 7 / 11；见 `references/prioritization-quant.md` |
| **Desired Outcome / North Star Framing**（Phase 0 新增） | 显式写出当前轮成功度量与门槛，防止下游 Success Criteria 凭空生成 | Sean Ellis *Hacking Growth*；Amplitude *North Star Playbook* | 步骤 4；discovery 正文 section 9；Bridge to Spec |

## When to Use

适用：
- 用户还在问“这个问题值不值得做”“为什么当前方向不够好”
- 用户还在收敛 target user、problem statement、wedge 或最小机会点
- 用户还在讨论关键假设、probe、验证方向，尚未进入 formal spec
- 现有输入主要是 brainstorming notes、会议纪要或零散想法，且目标是形成可进入规格阶段的 discovery 草稿

不适用：
- 已明确要写 formal spec / design / tasks → `hf-specify` / 对应下游 skill
- 只需评审已有 discovery 草稿 → `hf-discovery-review`
- route / stage / 证据冲突，需要 authoritative 判断 → `hf-workflow-router`

Direct invoke 信号：“先帮我把产品方向想清楚”“先收敛问题和 wedge”“还没到写 spec，先做 discovery”。

## Hard Gates

- discovery 草稿未通过评审前，不得把它当作正式规格输入
- 不得把猜测、口号或实现偏好伪装成已确认业务需求
- 不得顺手进入 formal spec、设计或任务拆解
- 若请求已明显进入 coding family，不继续停留在本节点

## Workflow

### 1. 读取最少必要上游输入

只读完成 discovery 所需的最少材料：用户请求、已有会议纪要 / notes / insight docs、项目级上下文约定（若项目已声明）、以及少量仓库背景用于理解当前主题。

先归纳：
- 当前想解决的核心问题
- 涉及的用户 / 角色
- 已确认事实
- 待确认假设
- 候选 wedge / opportunity
- 明显越界到 spec / design 的内容

### 2. 收敛当前轮 discovery 目标

若输入同时混有多个方向，先明确这一轮只回答：
- 当前要收敛哪个问题
- 针对哪个用户 / 场景
- 哪个最小 wedge 最值得推进
- 哪些候选能力先放入 parking lot

不要把多个不相关方向揉成一份大而空的 discovery 文档。

### 3. 结构化整理 discovery 输入（JTBD + OST 视角）

把原始输入至少归一化为：
- `Problem / User / Why now`
- `Confirmed facts`
- `Assumptions / risks`（按 Desirability / Viability / Feasibility / Usability 分类，若适用）
- `Candidate wedges`
- `Probe ideas`
- `Likely out-of-scope / later`

在这一步同时引入两个视角：

- **JTBD 视角**：至少能写出一条 Jobs Story（`When <situation>, I want to <motivation>, so I can <outcome>`），避免从"功能清单"反推用户（见 `references/jtbd-framework.md`）。切换型主题（从旧方案切到新方案）额外做四力分析（push / pull / anxiety / habit）。
- **OST 视角**：把 outcome → opportunity → solution → assumption 画成紧凑快照（见 `references/opportunity-solution-tree.md`）。规模控制在 Outcome 1 个、Opportunity 3–5 个（选 1 主）、每个 opportunity 下 Solution 2–3 个。

若输入里夹带明显实现细节（接口、数据库表、服务名、技术栈），只保留其业务意图，不把它写成 discovery 结论。

若候选 opportunity / solution ≥ 2 个且仅凭 MoSCoW 难以收敛，引入 **RICE / ICE** 做量化辅助（见 `references/prioritization-quant.md`）；分数必须带来源，严禁纯凭直觉。低 confidence 的候选不进入 wedge 候选，而是转成假设交给 `hf-experiment`。

### 4. 锁定 Desired Outcome 与 Success Threshold

在进入 draft 之前，必须显式写出本轮的 **成功度量**：

- 至少 1 个 **Desired Outcome**（结果指标，不是产出或活动）
- 至少 1 个可判断的 **Success Threshold**（让我们承认 wedge 成功的最小门槛）
- 若项目已有 North Star / OKR，显式锚定；否则写"项目当前无 North Star 声明"，不允许留空
- 显式写出本轮 **Non-goal Metrics**，防止 outcome 在下游被隐式扩大

这些度量直接成为 `Bridge to Spec` 的上游输入，对应后续 `hf-specify` 正文中的 Success Criteria / Success Metrics。

### 5. 形成 discovery 草稿

按 `references/discovery-template.md`（或 项目级覆盖模板）起草 discovery 文档。

默认应显式写出：
- 问题陈述与目标用户（含 JTBD situation / struggling moment）
- why-now / 当前价值判断
- 当前轮 wedge / 最小机会点（= OST 中选中的主 opportunity）
- 已确认事实 vs 仍未确认假设
- 建议 probe 方向或验证优先级
- **Desired Outcome / North Star 锚定 / Success Threshold / Non-goal Metrics**
- JTBD 视图（Jobs Story，必要时含四力）
- OST Snapshot（当候选方向 ≥ 2 时必填）
- 哪些内容已经足够进入 formal spec
- 哪些仍只能作为 assumption / open question

章节密度按 `references/discovery-template.md` 的 profile-aware 表格执行：`lightweight` 允许压缩 JTBD / OST 为最简形式，但 Desired Outcome + Success Threshold + Bridge to Spec 始终是 hard requirement。

### 6. 进入 Bridge to Spec 语义

若 discovery 草稿已经足够稳定，应在文档中单列 `Bridge to Spec` 小节，说明：
- 推荐带入 `hf-specify` 的范围边界
- 可直接转成规格输入的稳定结论
- 需要继续保留为 assumption 的内容
- 当前不进入 spec 的候选项
- 已锁定的 Desired Outcome 与 Success Threshold，作为 spec 阶段 Success Criteria 的上游锚点
- 待 `hf-experiment` 验证的关键假设清单（若存在）

`Bridge to Spec` 是 discovery 输出的一部分，不要求先拆成独立文件。

### 7. 评审前自检与 handoff

交给 `hf-discovery-review` 前确认：
- discovery 不是功能清单堆砌
- 已区分事实 / 假设 / later ideas
- 已明确当前轮 wedge（= OST 主 opportunity）
- 至少一条合格 Jobs Story（情境驱动、可观察 outcome）
- 候选方向 ≥ 2 时，OST Snapshot 存在且剪枝理由已写
- Desired Outcome + Success Threshold 已显式落下，不是"体验更好"这类口号
- 未把 spec / design 细节提前写进正文
- 已明确 `Bridge to Spec` 中哪些结论可进入 `hf-specify`
- 若存在高风险、低 confidence 的核心假设，已标注"建议走 `hf-experiment` 先验证"

## Output Contract

完成时产出：
- discovery 草稿（默认路径：`docs/insights/YYYY-MM-DD-<topic>-discovery.md`；若 项目级覆盖，优先遵循）
  - discovery 阶段 feature 尚未创建，因此 discovery 草稿落到 `docs/insights/` 长期资产目录；只有当 discovery 通过评审并决定推进为 feature 时，才由 `hf-specify` 创建 `features/<NNN>-<slug>/`
- 文档中明确的 spec bridge 小节，作为后续 `hf-specify` 起草 `features/<NNN>-<slug>/spec.md` 的输入
- discovery 阶段的进度可临时记录在 discovery 草稿中或与 discovery 同目录的 progress 文件；进入 feature 后，进度统一迁到 `features/<NNN>-<slug>/progress.md`

若草稿未达评审门槛，不伪造 handoff；明确还缺什么。

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `using-hf-workflow` | 入口层只负责判断是否该进入 discovery；本 skill 负责真正起草 discovery 正文。 |
| `hf-discovery-review` | review 负责独立评审 discovery 草稿；本 skill 只负责起草和回修。 |
| `hf-specify` | discovery 回答“为什么值得做、当前 wedge 是什么、哪些假设仍未关闭”；specify 回答“这一轮正式做什么、做到什么程度算完成”。 |
| `hf-workflow-router` | router 负责 authoritative runtime routing；本 skill 假设当前已明确在做 discovery authoring。 |

## Red Flags

- 把 brainstorming notes 直接当成已稳定结论
- 用功能列表代替问题定义和 wedge 收敛
- discovery 文档混入接口、表结构、服务名等设计细节
- 没区分 confirmed facts 和 assumptions
- 没说明哪些结论足够进入 spec，handoff 仍写"可以继续"
- 还在判断产品是否值得做，却直接起 formal spec
- Jobs Story 把产品功能当作 job，或 outcome 写成"体验更好"这类无阈值口号
- OST 根节点写的是产品名而不是 outcome；opportunity 直接是"缺 XX 功能"
- RICE / ICE 分数没有来源，或用来当装饰品
- Desired Outcome 缺失，或 Success Threshold 不可判断
- 高风险假设 confidence 很低却仍被直接写进 candidate wedges，而不是转成 `hf-experiment` 假设

## Reference Guide

按需加载详细参考内容。任一 reference 未命中其"加载时机"时，不需要提前读取。

| 主题 | Reference | 加载时机 | 最小 profile |
|------|-----------|---------|--------------|
| discovery 文档骨架 | `references/discovery-template.md` | 起草 discovery 草稿时；每次会话至少读一次 | lightweight / standard / full 全档必读 |
| JTBD / Jobs Stories / 四力 | `references/jtbd-framework.md` | 需要把"要功能"翻译成"要进展"；或主题属于切换型（push/pull/anxiety/habit） | standard / full；lightweight 仅当问题陈述仍卡在功能语言时 |
| Opportunity Solution Tree | `references/opportunity-solution-tree.md` | 候选方向 ≥ 2 个、或需要剪枝到当前轮 wedge | standard / full；lightweight 候选 ≤ 1 可跳过 |
| RICE / ICE / Kano 量化优先级 | `references/prioritization-quant.md` | 多个候选 opportunity / solution 难以用 MoSCoW 直接收敛 | 按需；候选 ≤ 2 或分数无法带来源时跳过 |

加载策略：

- `lightweight` 会话默认只读 `discovery-template.md`；JTBD / OST / 量化只在模板章节显式触发时再按上表加载
- `standard` 会话默认读 `discovery-template.md` + `jtbd-framework.md`；其余按命中条件
- `full` 会话按实际需要加载；若主题已明确为切换型或多候选并排，预读对应 reference

## Verification

- [ ] discovery 草稿已保存到约定路径
- [ ] 问题、用户、why-now、当前 wedge 已写清，且 situation / struggling moment 足以冷读
- [ ] 至少一条合格 Jobs Story（情境驱动，非功能驱动）
- [ ] 候选方向 ≥ 2 时，OST Snapshot 存在，且剪枝理由显式
- [ ] Desired Outcome 已锁定，Success Threshold 可判断；North Star 锚定或"无声明"已显式写出
- [ ] Leading / Lagging 指标（standard / full 密度）已写出
- [ ] Non-goal Metrics 已显式写出（full 密度强制；standard 建议）
- [ ] confirmed facts、assumptions（Desirability/Viability/Feasibility/Usability 适用时分类）、later ideas 已显式分开
- [ ] RICE / ICE 分数（若使用）带来源；低 confidence 候选已转为假设
- [ ] bridge 语义已明确，足以支撑 `hf-specify` 读取；Desired Outcome / Success Threshold 已并入 Bridge to Spec
- [ ] 高风险、低 confidence 关键假设已标注"建议走 `hf-experiment` 先验证"
- [ ] discovery 正文未混入 formal spec / design 细节
- [ ] discovery 阶段进度记录（若使用）已同步到 `hf-discovery-review`；进入 feature 后续 progress 落到 `features/<NNN>-<slug>/progress.md`

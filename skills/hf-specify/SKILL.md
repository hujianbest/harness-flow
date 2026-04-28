---
name: hf-specify
description: 适用于尚无已批准规格、现有规格仍是草稿、或规格被 hf-spec-review 退回需修订的场景。不适用于已有批准规格（→ hf-design）、需要任务计划（→ hf-tasks）或阶段不清（→ hf-workflow-router）。
---

# HF 需求澄清

创建一份定义"做什么、为什么做、做到什么程度算完成"的需求规格说明，准备到可交给 `hf-spec-review` 的状态。

本 skill 不给设计方案，只把需求收敛成后续节点不需要猜测推进的规格草稿。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **EARS (Easy Approach to Requirements Syntax)** | 需求语句使用结构化触发模式（Ubiquitous / Event-driven / State-driven / Optional / Unwanted），确保每条需求可观察、可判断 | Mavin et al., REFSQ 2009 | 步骤 4 — 需求 Statement 写作 |
| **BDD / Gherkin (Given-When-Then)** | 验收标准采用行为驱动格式，建立从需求到测试的可追溯桥梁 | Dan North, 2006 "Introducing BDD" | 步骤 4 — Acceptance Criteria 写作 |
| **MoSCoW Prioritization** | 需求优先级使用 Must/Should/Could/Won't 四级分类，驱动范围收敛与 deferred 判断 | DSDM Consortium, Clegg & Seddon 1994 | 步骤 4 — Priority 标注；步骤 5 — 延后判断 |
| **需求六分类 (FR/NFR/CON/IFR/ASM/EXC)** | 将需求按功能、非功能、约束、接口、假设、排除六类组织，覆盖完整需求空间。参考 IEEE 830/ISO 29148 的分类思想，经项目化裁剪 | IEEE 830-1993 / ISO/IEC 29148:2018 | 步骤 4 — requirement rows 分类 |
| **Socratic Elicitation** | 澄清过程遵循 Capture → Challenge → Clarify 三段式提问模型，通过结构化提问驱动收敛而非假设填充 | 苏格拉底式提问；Paul & Elder 批判性思维框架 | 步骤 3 — 分轮澄清 |
| **INVEST 质量标准** | 每条需求应满足 Independent（独立）、Negotiable（可协商）、Valuable（有价值）、Estimable（可估算）、Small（足够小）、Testable（可测试）六项质量属性 | Bill Wake, 2003；敏捷用户故事实践 | 步骤 5 — 粒度检查；步骤 8 — 评审前自检 |
| **ISO/IEC 25010 + Quality Attribute Scenarios**（Phase 0 新增） | 每条核心 NFR 按 25010 质量维度分类，并以 QAS 五要素（Source/Stimulus/Environment/Response/Response Measure）表达 | ISO/IEC 25010:2011；Bass/Clements/Kazman *Software Architecture in Practice* | 步骤 4 — NFR 行写作；步骤 8 — 自检；详见 `references/nfr-quality-attribute-scenarios.md` |
| **Success Metrics & Key Hypotheses Framing**（Phase 0 新增） | 显式落下可判断的成功度量与关键假设，供下游 design / tasks / gate / experiment 消费 | Sean Ellis *Hacking Growth*；Teresa Torres *Continuous Discovery Habits*（四类假设） | 步骤 4 — 正文章节 3 / 4；详见 `references/success-metrics-and-hypotheses.md` |
| **量化优先级 RICE / ICE / Kano**（Phase 0 新增，承接自 hf-product-discovery） | 在多条 Must 候选间做可冷读的量化取舍，不替代 MoSCoW | Intercom (RICE)；Sean Ellis (ICE)；Noriaki Kano (Kano) | 步骤 4 — Priority 行；步骤 5 — 延后判断；详见 `hf-product-discovery/references/prioritization-quant.md` |

详细规则见 `references/requirement-authoring-contract.md`（EARS patterns、BDD 格式、MoSCoW 规则）、`references/granularity-and-deferral.md`（INVEST 对应的粒度检查信号）、`references/nfr-quality-attribute-scenarios.md`（NFR QAS 最小契约）、`references/success-metrics-and-hypotheses.md`（Success Metrics / Key Hypotheses 最小契约）。

## When to Use

适用：
- 尚无已批准需求规格
- 现有规格仍为草稿或待收敛
- `hf-spec-review` 返回 `需修改` 或 `阻塞`，需按 findings 修订
- 用户需要先澄清范围、验收标准、边界、约束、非目标

不适用 → 改用：
- 已有批准规格，问题在 HOW 层 → `hf-design`
- 规格和设计都已批准，需要任务计划 → `hf-tasks`
- 热修复/增量变更/阶段不清 → `hf-workflow-router`
- 还在判断产品是否值得做 → `hf-product-discovery`

Direct invoke 信号："先把需求梳理清楚"、"帮我写规格"、"规格被 review 打回了"、"先别做设计"。

## Hard Gates

- 规格通过评审前，不得开始设计、任务拆解或实现
- `hf-spec-review` 给出"通过"前，不发起 approval step
- 不得为缺失的业务规则、优先级或来源锚点自行编造
- 不得把延后需求只藏在 prose 里而不显式标成延后项
- 若请求未经过入口判断，先回到 `hf-workflow-router`

## Workflow

### 1. 了解最少必要上下文

只读完成规格澄清所需的最少材料：用户请求、与规格草稿相关的 bridge / insight docs（若项目存在，例如 `docs/insights/*-spec-bridge.md`）、相关项目文档、现有草稿/评审记录、项目级路径约定（若项目已声明）、当前 active feature 的 `progress.md`（默认 `features/<active>/progress.md`）。

若是新 feature 启动（无现有 active feature），先创建 `features/<NNN>-<slug>/` 目录骨架（双根目录布局：feature 周期内工件落到 `features/<NNN>-<slug>/`，长期资产落到 `docs/`）：
- `<NNN>` = `ls features/ | grep -E '^[0-9]{3}-' | sort | tail -n1` 的下一个数字（从 `001` 起）
- `README.md`（基于 `references/feature-readme-template.md`）
- `progress.md`（基于 `references/task-progress-template.md`）

先提炼：已确认事实、当前轮目标与成功标准、范围内/范围外、约束与依赖、显式 assumptions、未知项与矛盾点。

### 2. 收敛当前轮范围

若请求包含多个独立系统/阶段/能力，先帮用户收敛：
- 这一轮最值得优先解决的核心问题
- 哪些能力必须进入当前版本
- 哪些应推迟到后续增量

规格服务于当前轮可被评审、可被设计的范围。

若输入明显还是 brainstorming notes（零散想法、候选能力混写、真假需求未分、实现词汇夹杂）：
- 先归一化为 `已确认事实 / 待确认假设 / 候选需求 / 明显设计决策 / deferred 候选`
- 不把头脑风暴原文直接抄成规格正文
- 优先消除会改变当前轮范围、成功标准或关键边界的歧义，再进入 requirement rows
- 明显属于上游价值判断的问题（如“这个产品是否值得做”）不要在本节点硬收敛；回到 product discovery 上游

### 3. 分轮澄清需求 (Socratic Elicitation)

遵循 `Capture → Challenge → Clarify` 三段式提问模型（参考 Paul & Elder 批判性思维框架）。默认检查覆盖面：

1. 问题、用户、目标、成功标准与非目标
2. 核心行为与关键流程
3. 边界、异常与失败路径
4. 约束、依赖、接口、兼容性与业务边界
5. 非功能需求与验收口径
6. 术语、assumptions 与待确认项

**这是 coverage checklist，不是 6 轮脚本。** 已覆盖的跳过；只剩 1-2 个阻塞事实的合并在一轮问完。

提问规则：先问范围/角色/成功标准，再问边界细节；合并共享同一决策的问题；用 assume-and-confirm 加速；每轮结束前总结已锁定与待确认项。

若用户先给的是 brainstorming 式输入，先做一次紧凑归纳，再发起澄清：
- 先把内容整理成 3-5 个候选能力或边界主题，避免逐条追问碎片笔记
- 对每个主题只追问是否进入当前轮、成功标准、关键排除项
- 已明显属于设计层的内容（接口、表结构、服务名、重试次数）只保留业务意图，不把实现细节带进问题列表
- 若用户要求“一次问完”，优先把共享同一决策面的阻塞问题编号合并

若因 review findings 重新进入：只针对阻塞项补充确认，不重新发起整轮澄清。

### 4. 整理 requirement rows (六分类 + EARS + BDD + MoSCoW + NFR QAS)

写规格前，先把确认内容整理成结构化行。默认使用六分类法（FR/NFR/CON/IFR/ASM/EXC，参考 IEEE 830/ISO 29148 分类思想）：`FR`、`NFR`、`CON`、`IFR`、`ASM`、`EXC`。

核心需求编号如 `FR-001`、`NFR-001`。最小字段契约见 `references/requirement-authoring-contract.md`，每条至少：
- `ID` + `Statement`（使用 EARS 句式模式，可观察、可判断）
- `Acceptance`（使用 BDD Given/When/Then 格式，至少一个可验证标准）
- `Priority`（使用 MoSCoW 四级：`Must/Should/Could/Won't`）
- `Source / Trace Anchor`（Phase 0 起允许并鼓励指向 `HYP-xxx` 或某条 Success Metric）

#### NFR Quality Attribute Scenarios（Phase 0 新增）

每条核心 `NFR` 必须：

- 归类到 **ISO/IEC 25010** 质量维度（Performance Efficiency / Reliability / Security / Maintainability / Usability / Compatibility / Portability / Functional Suitability）
- 用 **Quality Attribute Scenario (QAS)** 五要素表达：Stimulus Source / Stimulus / Environment / Response / Response Measure
- Response Measure 必须含阈值或明确判定，不允许"足够快""合理"
- Acceptance（BDD）应与 QAS 一致，不矛盾

详见 `references/nfr-quality-attribute-scenarios.md`。无法写出 QAS 的 NFR 说明描述还不够具体，回到澄清。

#### 量化优先级（多条 Must 候选冲突时）

当存在多条 `Must` 候选且互相冲突、或超出当前轮容量时，引入 **RICE / ICE** 做量化取舍（见 `hf-product-discovery/references/prioritization-quant.md`）。分数必须带来源；分数相近（±20%）时不自动拍板，补定性理由。MoSCoW 决定"进不进当前轮"，RICE / ICE 决定"同等优先级里先打哪个"。

若来源是 brainstorming notes，先把每条笔记映射为以下之一，再决定是否进入 rows：
- 已确认的业务行为 → `FR`
- 可判断的质量门槛 → `NFR`（必须能写成 QAS）
- 硬性限制 / 外部依赖 → `CON` / `IFR`
- 仅是猜测、口号或待确认说法 → `ASM` 或开放问题；核心假设同步进入 **Key Hypotheses** 章节
- 当前轮不做但真实存在的能力 → deferred backlog / `EXC`

### 5. 粒度检查与延后判断 (INVEST + Scope-Fit)

按 `references/granularity-and-deferral.md` 检查。对照 INVEST 质量标准（Independent/Negotiable/Valuable/Estimable/Small/Testable，来源: Bill Wake 2003）：
- 是否命中 G1-G6 oversized 信号（对应 Small 和 Independent 维度）
- 哪些需求属于后续增量而非当前轮（对应 Valuable 和 Negotiable 维度）
- `EXC` 是真正非目标还是应回收到 deferred backlog

1-3 个不改变范围的拆分可在草稿中直接建议；4 个及以上或改变范围边界的必须向用户确认。deferred 需求写入 backlog。

### 6. 起草规格

按 `references/spec-template.md` 的默认结构起草。若 项目声明了模板覆盖，优先遵循。

编写要求：背景写"为什么"不写方案；功能需求写可观察行为；非功能需求写可判断条件并带 QAS；约束写硬性限制；假设写失效风险。

Phase 0 起必须显式落下以下 **hard anchor** 章节，不可省略：

- **Success Metrics**（按 `references/success-metrics-and-hypotheses.md`）：承接 discovery 的 Desired Outcome / Threshold / Non-goal Metrics；无 discovery 上游时仍必须按最小契约填写
- **Key Hypotheses**（同上 reference）：含 ID / Statement / Type (D/V/F/U) / Impact If False / Confidence / Validation Plan / Blocking?；Blocking 假设未验证前，规格不允许通过评审

默认要显式落下以下文档级语义，而不是只散落在 prose 里：
- 当前轮目标与 success criteria
- Success Metrics 与 Non-goal Metrics
- Key Hypotheses 与其阻塞状态
- 范围、范围外与关键边界
- 假设及其失效影响
- 开放问题的阻塞 / 非阻塞分类

`lightweight / standard / full` 三档密度按 `references/spec-template.md` 的 profile-aware 表格执行；即便 lightweight，Success Metrics / Key Hypotheses / 至少 1–2 条核心 NFR 的 QAS 仍是硬门槛。

### 7. 区分开放问题

- **已确认**：直接写入正文
- **需用户确认**：先问清再写
- **非阻塞**：可保留但不影响主干
- **阻塞**：交 reviewer 前必须解决（核心范围摇摆、主要成功标准未定、关键约束未知等）

### 8. 评审前自检 (INVEST + Phase 0 Anchors)

交 `hf-spec-review` 前确认：
- 问题陈述、目标、主要用户清楚
- **Success Metrics 章节存在**：Outcome Metric + Threshold + Measurement Method 齐全；Non-goal Metrics 显式写出或显式标"无"
- **Key Hypotheses 章节存在**：每条含 Type / Impact If False / Confidence；低 confidence 假设有 Validation Plan；Blocking 假设如仍未验证，暂停评审
- 范围内/范围外显式说明
- 核心功能需求逐条可观察、可验证、带 ID
- 核心 NFR 已归类到 ISO 25010 维度并给出 QAS 五要素；Response Measure 有阈值；Acceptance 与 QAS 一致
- 需求与验收标准粒度对应
- G1-G6 oversized 已拆分或标注
- 多条 Must 候选冲突时已用 RICE / ICE 辅助取舍，且分数带来源
- deferred requirements 已写入 backlog
- 模糊词已量化、需求未混入设计选择
- 阻塞性开放问题已解决
- 每条核心需求满足 INVEST 标准（至少 Small + Testable + Independent 无违规）

### 9. 派发 reviewer

按 `references/reviewer-handoff.md` 派发独立 reviewer subagent 执行 `hf-spec-review`，不内联执行。reviewer 返回后按协议处理结果。

## Output Contract

完成时产出：
- 可评审规格草稿（默认路径 `features/<active>/spec.md`；若 项目声明的覆盖路径，优先遵循）
- 如适用，deferred backlog（相邻路径，默认 `features/<active>/spec-deferred.md`）
- feature `README.md` 已更新：Title / Owner / Started / Status Snapshot / Artifacts 表中 Spec 行
- feature `progress.md` 状态同步：`Current Stage` → `hf-specify`，`Next Action Or Recommended Skill` → `hf-spec-review`

若草稿未达评审门槛，不伪造 handoff；明确写出仍缺什么。

## 和其他 Skill 的区别

| 场景 | 用 hf-specify | 不用 |
|------|---------------|------|
| 尚无规格或规格仍为草稿 | ✅ | |
| 已有批准规格，问题在 HOW 层 | | → `hf-design` |
| 规格和设计都已批准，需要任务计划 | | → `hf-tasks` |
| 评审规格草稿质量 | | → `hf-spec-review` |
| 阶段不清/证据冲突 | | → `hf-workflow-router` |

## Red Flags

- 从用户想法直接跳到架构设计
- 把头脑风暴笔记当成已批准规格
- 不先归一化 brainstorming 输入就逐条抄进 FR/NFR
- 规格里写任务、里程碑或提交计划
- 多个独立能力打包成一句"大需求"
- 核心需求缺少 Priority 或 Source
- 只写 happy path，不写边界和失败路径
- 提前使用 class、endpoint、table 等设计语言
- "后续再做"只留在 prose 里无 backlog
- 成功标准留成隐含信息
- **Success Metrics 章节缺失**，或只写"体验更好"无阈值口号
- **Key Hypotheses 章节缺失**，或全部假设 confidence 高但无证据锚点
- **Blocking 假设仍未验证却继续走 review**
- 核心 NFR 无 QAS / 无 ISO 25010 归类；Response Measure 写"足够快"
- NFR 一条覆盖多个不同质量维度
- handoff 缺失却声称"可以继续往下走"

## Reference Guide

按需加载详细参考内容。任一 reference 未命中其"加载时机"时，不需要提前读取。

| 主题 | Reference | 加载时机 | 最小 profile |
|------|-----------|---------|--------------|
| 需求最小字段契约 | `references/requirement-authoring-contract.md` | 写 FR / NFR / CON / IFR / ASM / EXC 条目时；每次 spec 至少读一次 | 全档必读 |
| 粒度与延后判断 | `references/granularity-and-deferral.md` | 核心需求出现 G1-G6 过大信号、或需要判断是否进 deferred backlog 时 | standard / full；lightweight 仅当确实命中过大信号 |
| 规格文档模板 | `references/spec-template.md` | 起草或修订 spec 文档时；每次会话至少读一次 | 全档必读 |
| reviewer 派发协议 | `references/reviewer-handoff.md` | 准备派发 `hf-spec-review` 时 | 全档必读（派发时机） |
| NFR + QAS 最小契约 | `references/nfr-quality-attribute-scenarios.md` | 写任一核心 NFR 时；或 NFR 章节 Response Measure 缺阈值时 | 全档必读（存在 NFR 时） |
| Success Metrics / Key Hypotheses | `references/success-metrics-and-hypotheses.md` | 起草 section 3 / section 4；或承接 discovery 的 Desired Outcome / OST 假设时 | 全档必读 |
| 跨 skill：量化优先级 | `hf-product-discovery/references/prioritization-quant.md` | 多条 Must 候选冲突、或需要 RICE / ICE 辅助取舍时 | 按需；默认不加载 |

加载策略：

- `lightweight`：默认读 `spec-template.md` + `requirement-authoring-contract.md` + `success-metrics-and-hypotheses.md`；NFR 存在时加 `nfr-quality-attribute-scenarios.md`。其余按命中条件
- `standard`：在 lightweight 基础上预读 `granularity-and-deferral.md`
- `full`：按实际需要加载；多 Must 冲突时预读跨 skill 量化优先级

## Verification

- [ ] 规格草稿已保存到 `features/<active>/spec.md`（或 项目级覆盖路径）
- [ ] 若是新 feature，目录骨架（`README.md`、`progress.md`）已按模板创建
- [ ] 当前轮目标、success criteria、范围、范围外、关键边界已写清
- [ ] **Success Metrics 章节存在**：Outcome Metric + Threshold + Measurement Method 齐全；Non-goal Metrics 显式写出或标"无"
- [ ] **Key Hypotheses 章节存在**：每条含 Type / Impact If False / Confidence / Validation Plan / Blocking?
- [ ] Blocking 假设如仍未验证，已显式记录并阻塞评审进入
- [ ] 核心 FR/NFR 具备 ID、Priority (MoSCoW)、Source（允许指向 `HYP-xxx` 或 Success Metric）
- [ ] 需求 Statement 使用 EARS 句式模式
- [ ] 验收标准使用 BDD Given/When/Then 格式
- [ ] 核心 NFR 已归类到 ISO 25010 维度，并给出 QAS 五要素；Response Measure 可判定；Acceptance 与 QAS 一致
- [ ] 多条 Must 候选冲突时已使用 RICE / ICE 辅助取舍且分数带来源（若适用）
- [ ] assumptions 已显式写出，且失效影响可回读
- [ ] oversized 需求已按 G1-G6 处理
- [ ] 核心需求通过 INVEST 质量抽查（至少 Small + Testable + Independent）
- [ ] deferred requirements 已写入 backlog 或明确不存在
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项已解决
- [ ] `features/<active>/progress.md` 已按 canonical schema 同步，下一步为 `hf-spec-review`
- [ ] feature `README.md` 中 Artifacts 表的 Spec 行已更新

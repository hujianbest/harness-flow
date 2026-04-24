# HF Methodology Coherence（方法论协作与冲突地图）

## Purpose

HF 目前引用的方法论已超过 30 种（见 `README.md` / `README.zh-CN.md` 的 pack-level methodology 表）。这带来一个现实问题：**它们之间会不会冲突？按什么规则协作？什么时候允许激活哪些？**

本文回答三件事：

1. 每条方法论在 HF 中**落在哪个层 / 哪个字段**——避免"看起来重叠但实际不冲突"被误当成冲突
2. 哪些方法**看起来可以替代但实际不允许**——显式标注成反替代规则
3. 每条方法论**在哪个 Phase 激活、可以在哪个 profile 下被跳过**——避免上下文过长与过度堆叠

本文是**治理文档**，不是新的 skill。任何时候给 HF 加入新方法，都应回到本文检查它是否与已有方法产生冲突、在哪个 Phase 与 profile 下激活。

## 一、分工地图（按 HF 六层分组）

HF 的设计前提是：方法论按**层**先分工，再按**字段**分工，再按**Phase**激活。同一层里才可能冲突，跨层天然不冲突。

### 意图层（spec-anchored SDD）

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| Problem Framing | 总体意图收敛（用户 / 问题 / why-now） | 描述 job；组织候选 |
| JTBD / Jobs Stories | 情境驱动的 job 描述（situation / progress / outcome） | 组织候选 / 打优先级 |
| 四力（Push/Pull/Anxiety/Habit） | 切换决策场景下的障碍分析 | 非切换型场景不激活 |
| Opportunity Solution Tree | Outcome → Opportunity → Solution → Assumption 的收敛骨架 | job 定义；具体度量 |
| MoSCoW | 当前轮"进不进"优先级 | 同级内先打哪个 |
| RICE / ICE | 同级内"先打哪个"的量化 | 决定进不进当前轮 |
| Kano | 做到什么档位（Basic / Performance / Excitement） | 优先级排序 |
| Desired Outcome / North Star | 结果指标与成功门槛 | 具体 FR / NFR |
| EARS | 单条需求的可观察句式 | 验收标准 |
| BDD / Gherkin | 验收标准的 Given / When / Then | 需求陈述 |
| 六分类（FR/NFR/CON/IFR/ASM/EXC） | 需求分类法 | 单条字段格式 |
| INVEST | 单条需求的质量六维度 | 分类；优先级 |
| ISO/IEC 25010 | NFR 质量维度分类 | NFR 表达格式 |
| Quality Attribute Scenarios | NFR 表达的五要素格式 | 分类；验证方法 |
| Socratic Elicitation | 澄清过程的 Capture → Challenge → Clarify | 写规格正文 |

### 架构 / 设计层

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| DDD Strategic Modeling | 锁 Bounded Context / Ubiquitous Language / Context Map | 画视图；画部署 |
| DDD Tactical Modeling | 每个 Bounded Context 内的 Aggregate / VO / Repository / Domain Service / Application Service / Domain Event | GoF 代码模式前置决策（留给实现层 emergent） |
| Event Storming | spec→design 桥，事件视角摊开流程 | 直接定模块；替代 sequence 图 |
| C4 Model | Container / Component 视图 | 战略边界；关键决策 |
| ADR (Nygard) | 关键决策及可逆性 | 方案对比视图 |
| ARC42（partial） | 设计文档整体结构 | 单一视图 |
| Risk-Driven Architecture | 投入按风险分配 | 决策本身 |
| YAGNI + Complexity Matching | 不为假设的未来需求投入 | 具体技术选型 |
| NFR Uptake（nfr-checklist） | 把 QAS 落到模块 / 机制 / observability / 验证 | 定义 QAS |
| STRIDE（轻量） | 威胁列表 × 缓解 | 完整威胁建模流程（留 Phase 2） |
| Clean Architecture / SOLID | 依赖方向 / 模块边界 | 具体实现模式 |
| Atomic Design（UI） | 组件分层 | 系统架构 |
| Design Tokens（UI） | 视觉一致性基元 | 交互状态 |
| Interaction State Inventory（UI） | idle/hover/focus/active/disabled/loading/empty/error/success | 视觉 token |
| Nielsen 启发式（UI） | 可用性冷读 | 可访问性硬门 |
| WCAG 2.2 AA（UI） | 可访问性硬门 | 可用性冷读 |

### 执行层（gated TDD）

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| Canon TDD（Kent Beck） | test list → RED → GREEN → REFACTOR | 跨任务重构 |
| Walking Skeleton | 最薄端到端路径 | 完整回归覆盖 |
| Test Design Before Implementation | 实现前的测试设计 approval | 实现阶段 |
| Fresh Evidence Principle | 本会话内的 RED / GREEN / regression / completion 证据 | 代替测试本身 |
| Two Hats（Beck/Fowler） | 同一时刻只戴 Change 或 Refactor 一顶帽子 | 跨任务重构 |
| Opportunistic / Boy Scout Refactoring | in-task cleanup | 结构性重构 |
| Preparatory Refactoring | RED 之前的扩展点重构 | 混进 RED |
| Refactoring to Patterns（Kerievsky）/ Emergent GoF | REFACTOR 步按 Fowler vocabulary 浮现 GoF 模式（Strategy / Factory / Adapter / ...） | 前置 GoF 决策；浮现理由写 "未来可能" |
| SUT Form Declaration | 测试设计 approval 中声明 `naive / pattern:<tactical> / emergent`，锁定本轮 RGR 合法形态 | 在声明中写 GoF 模式名 |
| Hypothesis-Driven Development | 把假设变成 probe | 代替实现 |
| Build-Measure-Learn | probe 循环 | 自动上线 |
| Pre-registered Success Threshold | probe 事先声明阈值 | 事后合理化 |

### 路由层

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| Finite State Machine Routing | 基于工件证据的 canonical 节点选择 | 工件内容 |
| Evidence-Based Decision Making | 证据冲突时保守判断 | 补脑猜测 |
| Escalation Pattern | profile 渐进升级（lightweight → standard → full） | 降级回退 |
| Front Controller | `using-hf-workflow` 入口 | 运行时恢复 |

### 评审层

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| Fagan Inspection | 独立 reviewer 角色 + 分阶段检查 | 实现 / 回修 |
| Structured Walkthrough | 按 checklist 冷读 | 实时讨论 |
| ATAM | 架构评审 quality attribute 驱动 | 实现评审 |
| Separation of Author/Reviewer Roles | 不自审自交 | 单人合并作者 + 评审 |
| Traceability（End-to-End / Zigzag） | spec ↔ design ↔ tasks ↔ code ↔ tests 的双向追溯 | 发现新问题而不记录 |

### 验证 / 门禁层

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| Regression Testing BP | 影响域 + fresh evidence | 代替 completion |
| Definition of Done | 完成判定 | 代替 regression |
| Evidence Bundle | reviews + gates + 交接块 必须齐全 | 单点证据 |
| Profile-Aware Rigor | full / standard / lightweight 不同证据量 | 代替质量纪律 |

### 收尾层

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| Project Closeout（PMBOK） | 状态 / 文档 / release notes 收口 | 新实现 |
| Release Readiness Review | 外部记录闭环 | 门禁 |
| Handoff Pack Pattern | 下个会话冷启动 | 继续编排 |

### 分支 / 经验沉淀层

| 方法 | 主要职责 | 不承担的事 |
|---|---|---|
| RCA / 5 Whys | hotfix 的根因归因 | 修代码 |
| Minimal Safe Fix Boundary | 最小安全修复边界 | 结构性重构 |
| Change Impact Analysis | increment 的失效影响 | 实现 |
| Re-entry Pattern | 安全回流到正确主链节点 | 就地打补丁 |
| Baseline-before-Change | 变更前锁基线 | 修代码 |
| Defect Pattern Catalog | 重复缺陷模式沉淀 | mandatory gate |
| Blameless Post-Mortem | 归因不归咎 | 实现 |

## 二、显式"不允许替代"清单

以下是 HF 中**看起来可以互换但严禁替代**的配对。任何方法替代尝试都应被 Red Flag 直接拦截。

| 左 | 右 | 规则 | 落地位置 |
|---|---|---|---|
| MoSCoW | RICE / ICE | RICE / ICE **不得**替代 MoSCoW；一个决定"进不进当前轮"，一个决定"同级里先打哪个" | `hf-product-discovery/references/prioritization-quant.md` |
| MoSCoW | Kano | Kano **不得**替代 MoSCoW；Kano 决定"做到什么档位" | 同上 |
| EARS | BDD / Gherkin | 两者**同时存在**于同一条需求的不同字段，不互替 | `hf-specify/references/requirement-authoring-contract.md` |
| ISO 25010 | QAS | ISO 25010 是分类，QAS 是格式；必须**同时**满足，不互替 | `hf-specify/references/nfr-quality-attribute-scenarios.md` |
| DDD Bounded Context | C4 Container / Component | Container / Component 切分**必须与 Bounded Context 一致**，不允许静默不一致；不一致时用 ADR 显式解释 | `hf-design/SKILL.md` MUST DO + Verification |
| DDD Tactical Pattern 前置决策 | GoF Pattern 前置决策 | 两者**不互相替代**。战术模式（Aggregate / VO / Repository / Domain Service / Application Service / Domain Event）在 `hf-design` § 4.5 前置决策；GoF 模式刻意 emergent，在 `hf-test-driven-dev` REFACTOR 步按 Fowler vocabulary 浮现 | `docs/principles/emergent-vs-upfront-patterns.md`；`hf-design-review` `A11`；`hf-test-driven-dev` sut_form allowlist |
| SUT Form 声明 `pattern:<tactical>` | SUT Form 声明 `pattern:<GoF>` | allowlist 仅含战术模式；GoF 名写入 sut_form 声明 = 前置 over-abstraction，不合法；GoF 只能作为 Refactor Note 的 `Pattern Actual` 浮现结果出现 | `hf-test-driven-dev/SKILL.md` Hard Gates；`refactoring-playbook.md` Pattern Emergence 节 |
| Fowler refactoring 浮现 GoF | 省略 REFACTOR 步 | 浮现必须是 **Fowler vocabulary 驱动的结果**（Replace Conditional with Polymorphism / Extract Factory Method / ...）；没有 vocabulary 命名 = undocumented-refactor（CA7） | `refactoring-playbook.md`；`hf-code-review` `CA7` |
| Event Storming | sequence diagram | Event Storming 要记**业务事件**，不是接口交互；不能把两者混写成一张图 | `hf-design/references/event-storming.md` Red Flags |
| Canon TDD「test list」 | HF「测试设计 approval」 | HF 在 Canon 前加了"测试设计 approval"前置步；不允许以 Canon 为由跳过 approval | `hf-test-driven-dev/SKILL.md` |
| Two Hats | Preparatory Refactoring | 都是 Beck / Fowler 纪律；preparatory 必须**独立成步**且在 RED 之前，不允许混进 RED | `hf-test-driven-dev/SKILL.md` workflow |
| `hf-experiment` | `hf-test-driven-dev` | experiment 是在 spec 之前或之中的**假设**验证；TDD 是在已批准 spec / design 之后的**实现**验证；**互相不得替代** | `hf-experiment/SKILL.md` 区别表 |
| `hf-bug-patterns`（mandatory gate） | `hf-bug-patterns`（可选经验沉淀） | `hf-bug-patterns` 只是**可选旁路**，不得写成 `hf-test-review` 前的 mandatory gate | `docs/principles/hf-sdd-tdd-skill-design.md` |
| Fagan inspection full protocol | HF review skills | HF 只取"独立 reviewer"纪律，不搬 Fagan 完整流程 | review skills 的 Methodology 表 |
| ATAM full protocol | HF design-review | 同上：取"QA driven"精神，不跑 ATAM 完整会议流程 | `hf-design-review` |

## 三、剩余需要继续盯的冲突点

Phase 0 之后仍存在的冲突风险，按优先级排列：

### P0 — 假设类信息两层存在

**问题**：`hf-specify` 的 section 4 Key Hypotheses 与 section 12 "假设与失效影响" 都讲假设。

**分工**（已在 `spec-template.md` 写明，但值得再强调）：

| 章节 | 覆盖什么 | 下游消费者 |
|---|---|---|
| Section 4 Key Hypotheses | **决定 spec 本身是否成立**的关键假设（通常承接自 discovery 的 OST）；每条带 Type (D/V/F/U) / Impact If False / Confidence / Blocking? | `hf-experiment` / `hf-spec-review` |
| Section 12 假设与失效影响 | spec 独有的**运行假设**（例如网络稳定 / 第三方配额 / 部署环境稳定）；不用 D/V/F/U 分类 | `hf-design` / `hf-tasks` / 运维 |

**红线**：不允许把 spec 的运行假设写进 section 4，也不允许把决定 spec 是否成立的假设藏在 section 12。

### P1 — STRIDE 轻量 vs Phase 2 独立 `hf-threat-model`

**问题**：Phase 0 的 STRIDE 是 design 内嵌 list；Phase 2 将抽出独立 `hf-threat-model` skill + `hf-security-gate`。

**规避**：Phase 2 引入独立节点时，必须一次性迁移口径——design 内嵌 list 降级为 threat list 的"最小可冷读视图"，真实威胁建模工件迁移到新 skill 的产出路径。Phase 2 立项时回到本文件更新。

### P2 — Success Metrics 与 FR/NFR 的 Source 锚点

**问题**：Phase 0 鼓励 `Source` 指向 `HYP-xxx` 或 Success Metric；但 FR 也可以指向用户请求 / 上游工件。

**规避**：允许多来源，但每条 FR 的 `Source` **至少**能回指一个稳定上游锚点（用户请求 / spec-bridge / review finding / HYP / Success Metric / 外部约束）；不允许"无来源"。已写入 `requirement-authoring-contract.md`。

### P3 — 将来引入 Performance budget / SLO 时与 QAS 的关系

**问题**：Phase 1 将在 design 引入 Performance budget + `Observability-by-Design`；这可能与 spec 层的 QAS Response Measure 表达重复。

**规避规则（预先约定）**：QAS Response Measure 是**目标值**；design 的 performance budget / SLO 是**工程预算**。两者可以不同（例如 QAS 写"p95 ≤ 500ms"，SLO 写"p95 ≤ 400ms, error budget 0.1%"）。design 阶段必须显式写清两者的关系，不允许只写其中一个。

## 四、Phase × Profile 激活矩阵

每条方法论只在特定 Phase 引入，并按 profile 决定是否强制激活。

| 方法 | Phase 引入 | lightweight | standard | full |
|---|---|---|---|---|
| Problem Framing / Wedge / Assumption Surfacing | Phase 0 之前 | 必须 | 必须 | 必须 |
| JTBD / Jobs Stories | Phase 0 | 条件（问题陈述仍卡在功能语言时） | 必须（至少 1 条 Jobs Story） | 必须（切换型加四力） |
| OST | Phase 0 | 候选 ≥ 2 时必须 | 必须 | 必须（完整 Assumption / Probe） |
| RICE / ICE / Kano | Phase 0 | 按需 | 按需 | 按需 |
| Desired Outcome / North Star | Phase 0 | 必须（至少 Outcome + Threshold） | 必须（加 Leading / Lagging） | 必须（全字段） |
| EARS / BDD / MoSCoW / INVEST / 六分类 | Phase 0 之前 | 必须 | 必须 | 必须 |
| ISO 25010 + QAS | Phase 0 | 对关键 1–2 条 NFR | 核心 NFR 均需 | 全部核心 + 次要 NFR |
| Key Hypotheses | Phase 0 | 至少 1 条或显式"无 Blocking" | 列表形式 | 全字段表格 |
| `hf-experiment`（skill） | Phase 0 | 不激活 | 不激活 | 按 Blocking 假设激活 |
| DDD Strategic Modeling | Phase 0 | 显式跳过允许 | 跨系统或多角色时必须 | Bounded Context ≥ 2 时必须 |
| DDD Tactical Modeling | Phase 0 | 显式跳过允许 | 触发条件满足时必须（单 Context 多实体 + 一致性约束 / 事务边界 / 领域事件 / 跨聚合不变量） | Bounded Context ≥ 2 或存在聚合 / 事件时必须 |
| Emergent vs Upfront Patterns（治理文档） | Phase 0 | 必读（一次 / 每次设计决策前） | 必读 | 必读 |
| SUT Form Declaration（测试设计 approval 字段） | Phase 0 | 必须（sut_form ∈ naive / pattern:<tactical> / emergent） | 必须 | 必须 |
| Event Storming | Phase 0 | 自然语言描述 | Event Timeline | + Process Modeling |
| STRIDE（轻量） | Phase 0 | 触发时必须 | 触发时必须 | 触发时必须 |
| ADR / C4 / ARC42 / YAGNI / Risk-Driven | Phase 0 之前 | 必须 | 必须 | 必须 |
| Canon TDD / Walking Skeleton / Two Hats / Clean Arch | Phase 0 之前 | 必须 | 必须 | 必须 |
| Fresh Evidence（RED/GREEN/regression/completion） | Phase 0 之前 | 必须 | 必须 | 必须 |
| Observability-by-Design / Performance budget | **Phase 1**（未落地） | — | — | — |
| Privacy by Design checklist | **Phase 1**（未落地） | — | — | — |
| DORA 最小子集 + 产品指标回流 | **Phase 1**（未落地） | — | — | — |
| 独立 Threat Model / Compliance / Security / Perf / a11y / Contract gate | **Phase 2**（未落地） | — | — | — |
| CI/CD / progressive delivery / incident / postmortem / deprecation / DORA 完整 | **Phase 3**（未落地） | — | — | — |
| RACI / code owner / fitness functions / dependency lifecycle / architecture review | **Phase 4**（未落地） | — | — | — |
| 数据 / ML / LLMOps / eval harness / engineering learnings | **Phase 5**（未落地） | — | — | — |

## 五、给后续 Phase 的引入约束

任何 Phase ≥ 1 引入新方法时，应先来这里回答三个问题：

1. **它落在 HF 六层的哪一层？**——如果无法归层，通常说明方法本身职责不够单一
2. **它是否与表格中某条方法**看似重叠但实际分工不同？——如果是，在本文件追加一行分工规则，并在目标 skill 的 Red Flags 里加反替代项
3. **它在 lightweight / standard / full 下分别强制到什么程度？**——至少写一行激活矩阵；如果 lightweight 必须激活，必须同时给出"最小加载形态"

对应地，对应 `SKILL.md` 的 Reference Guide 也要同步写「加载时机」与「最小 profile」，避免所有 reference 一次性拉满。

## 六、本文件的维护节奏

- 每次 Phase 新增 / 调整方法时，**必须**更新本文件
- 每次 skill 的 Methodology 表改动，**必须**对应检查本文件
- `hf-bug-patterns` / `hf-retrospective`（Phase 1 起引入）中若沉淀出方法冲突的新案例，应**反馈**到本文件而非在各 skill 里散落修复

---

Bottom line：HF 的方法论规模已经可以撑起"从 idea 到产品落地"的骨架，但**治理不能靠约定俗成**。本文件把分工、反替代、Phase 激活显式落盘，任何未来新增方法都应通过这份地图来检验，防止"方法堆砌"退化成"方法打架"。

---
name: hf-design
description: 适用于需求规格已批准但设计尚未批准、或设计评审返回需修改/阻塞需修订的场景。不适用于规格仍是草稿/待批准、设计已批准需拆任务、仅需执行设计评审、阶段不清或证据冲突。
---

# HF 设计

把已批准规格转化为可评审的设计文档，说明"如何"实现，让后续任务规划与实现不再靠猜测推进。

**职责边界**：本 skill 只负责 **架构 / 模块 / API 契约 / 数据模型 / 后端 NFR**。若规格声明 UI surface，UI 设计 作为 **design stage 的 conditional peer skill** 与本 skill 并行处理 IA / wireframe / 交互 / 视觉 / 前端 a11y / i18n / 响应式。两条 skill 独立起草、独立 review。

## Methodology

本 skill 融合以下已验证方法：

- **ADR (Architecture Decision Records, Nygard format)**: 所有影响后续任务的关键决策用 ADR 格式记录，包含上下文、决策、后果与可逆性评估。详见 `references/adr-template.md`。
- **C4 Model (Context-Container-Component-Code)**: 架构视图按 Context → Container → Component 层次递进，提供最少必要视图（逻辑架构、组件关系、关键交互），优先 Mermaid。
- **Risk-Driven Architecture (Fairbanks)**: 架构投入按风险驱动——先识别哪些设计决策风险最高，对高风险决策投入更多分析和备选方案比较，而非均匀铺开。
- **YAGNI + Complexity Matching**: 决策必须由当前已确认需求驱动；架构复杂度匹配团队规模和系统规模（solo + 本地运行不引入微服务/消息队列）。
- **ARC42 (partial)**: 设计文档结构覆盖 ARC42 核心维度：约束、决策、视图、风险/技术债务、 Glossary（通过 spec-template 衔接）。
- **DDD Strategic Modeling（Phase 0 新增）**: 进入 C4 视图前，先锁定 Bounded Context、Ubiquitous Language、Context Map，让边界先于结构。详见 `references/ddd-strategic-modeling.md`。
- **DDD Tactical Modeling（Phase 0 新增）**: 在战略建模之后、C4 Component 之前，回答每个 Bounded Context **内部**的 Entity / Value Object / Aggregate / Repository / Domain Service / Application Service / Domain Event。让"写代码前要考虑好模式"落到**领域语义驱动**的选择上，而不是 GoF 直觉驱动。详见 `references/ddd-tactical-modeling.md`。
- **Emergent vs Upfront Patterns（HF 立场，硬性约束）**: 本 skill 只前置**领域语义驱动**的战术模式（Entity / VO / Aggregate / Repository / Domain Service / Application Service / Domain Event）；**GoF 代码模式**（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton 等）**刻意不在本 skill 前置决策**——它们属于实现层 emergent 浮现，留给 TDD REFACTOR 步按 Fowler 重构词汇（Replace Conditional with Polymorphism / Extract Factory Method / ...）浮现处理。强行前置等于 over-abstraction，违反 YAGNI 与 Clean Architecture dependency rule。理由：上游需求 / 真实接入点未稳定时锁定具体扩展点会让"灵活性"绑定到错误的轴上；TDD REFACTOR 阶段的 Two Hats 纪律保证了重构窗口存在；Fowler 重构词汇足以表达后期模式选择。
- **Event Storming as spec→design bridge（Phase 0 新增）**: 用事件视角把业务流程摊开，Big Picture / Process Modeling 两档按 profile 使用。详见 `references/event-storming.md`。
- **Quality Attribute Scenarios（Phase 0 承接）**: 承接已批准规格中的 QAS（ISO 25010 + Source/Stimulus/Environment/Response/Response Measure），把每条 QAS 映射到具体模块 / 机制 / observability / 验证。详见 `references/nfr-checklist.md`。
- **STRIDE 轻量威胁建模（Phase 0 新增）**: 在激活条件满足时产出最小 STRIDE list，落到具体缓解与 ADR。详见 `references/threat-model-stride.md`。

## When to Use

使用：

- 需求规格已批准，但设计尚未批准
- 设计评审返回 `需修改` 或 `阻塞`，需要按 findings 修订
- 当前问题已进入 HOW 层，需要明确架构、模块边界、接口、数据流、技术决策和测试策略

不使用：

- 规格仍是草稿 / 待评审 / 待批准
- 设计已批准，正在拆解或执行任务
- 只要求执行设计评审
- 阶段不清或证据冲突

直接调用信号："开始做设计"、"把实现方案写出来"、"设计被打回了"、"先别拆任务，把架构想清楚"。

## Chain Contract

读取：已批准规格（默认 `features/<active>/spec.md`）、feature `progress.md`（默认 `features/<active>/progress.md`）、项目级路径约定（若项目已声明）、其中声明的项目级设计原则锚点（默认 `docs/principles/`，承载**项目自身**的 architecture/product principles 等）、当前架构概述（按 *Minimal docs Tiers*：档 1 读 `docs/architecture.md`，档 2 读 `docs/arc42/`；二者择一存在），外加最少必要技术上下文。当 UI 设计 被激活时，也读取其最新草稿以标记 peer 依赖条目。

**read-on-presence**：上述 `docs/` 资产若不存在，视为该资产未启用（项目当前在档 0），不阻塞当前节点；按"项目当前未启用此类资产"作为判断结论，仍可继续设计。

产出：可评审设计草稿（默认 `features/<active>/design.md`）+ 设计层追溯与关键决策；若有 UI 设计 并行，还需在文档中写明 peer 依赖交接块（本设计依赖对方锁定的条目、本设计已锁定、冲突或待协商）。

**关键决策必须以 ADR 形式落到仓库级 ADR pool（默认 `docs/adr/NNNN-<slug>.md`，4 位顺序号、仓库级唯一、永不复用）**，而不是内联在 `design.md` 内。`design.md` 通过 ADR ID 引用，例如 "see ADR-0042"。新建 ADR 时状态字段写 `proposed`；设计评审通过且 `设计真人确认` 完成后翻为 `accepted`。源码化图（Structurizr DSL / PlantUML）允许直接落到 `docs/diagrams/`，与 design review 一并审核 diff。

产出：可评审的设计文档；交独立 reviewer 执行设计评审。

**联合 design approval**：当 UI 设计 作为 conditional peer 激活时，本 skill 与 ui-design 各自的评审均通过后，父会话才发起 `设计真人确认`。本 skill 的 review 通过不等于可以单独进入 approval。

## Hard Gates

- 关键决策必须以 ADR 形式落到仓库级 ADR pool（默认 `docs/adr/NNNN-<slug>.md`），不内联在 `design.md`
- 至少比较两个可行方案，trade-off 必须显式
- 核心 NFR 按 ISO 25010 + Quality Attribute Scenario 五要素承接（见 `references/nfr-checklist.md`）
- Domain Strategic Modeling 触发条件满足时必填（见 `references/ddd-strategic-modeling.md`）
- Tactical Modeling 触发条件满足时必填（见 `references/ddd-tactical-modeling.md`）；GoF 代码模式禁止前置决策
- STRIDE 触发条件满足时必填（Security NFR / 跨信任边界 / PII；见 `references/threat-model-stride.md`）

## Design Constraints

### MUST DO

- 用 ADR 记录所有影响后续任务规划的关键决策
- 逐项处理非功能需求，按 QAS 映射到模块 / 机制 / observability / 验证（见 `references/nfr-checklist.md`）
- 至少比较两个可行方案，权衡 trade-offs；候选对比需显式评估对 Success Metrics 的影响
- 分析关键路径的失败模式并给出缓解策略
- 识别架构模式并说明选择理由和天然限制
- 提供最少必要的架构视图（优先 Mermaid）
- 规格存在多概念 / 多角色 / 跨系统交互时，先做 Domain Strategic Modeling（Bounded Context / Ubiquitous Language / Context Map）
- 战术建模触发条件满足时（Bounded Context ≥ 2 / 单 Context 内多实体 + 一致性约束 / 并发或事务边界 / 领域事件 / 跨聚合不变量），产出 DDD Tactical Model（见 `references/ddd-tactical-modeling.md`）
- 触发条件满足时产出轻量 STRIDE threat list（见 `references/threat-model-stride.md`）

### MUST NOT DO

- 为假设的未来需求过度设计（YAGNI）
- 不评估备选方案就选定技术或模式
- 忽略运维复杂度和部署成本
- 在没理解需求前就开始画架构图
- 跳过安全性和隐私考量（Security NFR 存在或跨信任边界存在时，必须产出 STRIDE list）
- 让模块 / 组件切分与 Bounded Context 不一致却不作解释
- **把 GoF 代码模式（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton 等）前置决策到 design 阶段**——这类模式属于实现层 emergent 浮现，强行前置等于 over-abstraction，违反 YAGNI 与 Clean Arch dependency rule。战术模式（Entity / VO / Aggregate / Repository / ...）不在此禁令内——它们是**领域语义**选择，必须前置
- 战术建模触发条件满足却静默跳过（无"本 Context 不做战术建模"说明）

## Workflow

### 1. 阅读已批准规格并提取设计驱动因素

读取 项目级路径约定（若项目已声明）、feature `progress.md`（默认 `features/<active>/progress.md`）当前阶段、已批准规格（默认 `features/<active>/spec.md`）相关部分。

提取：核心范围、成功标准与验收标准、约束、非功能需求、集成点、关键需求编号、显式 assumptions、会影响架构选择的开放问题。

规格中若有阻塞架构判断的未决问题：
- 会改变范围/验收标准/约束/接口的：回到上游需求层澄清，不在本 skill 内消化
- 属于实现上下文级澄清、不改变需求边界的 → 可在当前轮次补充确认

### 2. 了解最少必要技术上下文

阅读现有架构 / 项目布局、当前框架与运行时约束、已知部署 / 集成 / 兼容限制、可复用模块与边界。

识别架构模式（按 `references/architecture-patterns.md` 的维度判断）。

不提前进入实现规划。

若用户输入仍是 brainstorming 式实现想法（多种做法混写、优缺点零散、夹带局部技术偏好）：
- 先归一化为 `候选方案 / 决策驱动因素 / 硬性约束 / 假设 / 明显越界的实现细节`
- 不把"大家随口提过的方案名"直接当作已比较完成的候选方案
- 先抽出真正影响方案选择的比较维度，再进入候选方案比较

### 2.5 Domain Strategic Modeling（Phase 0 新增）

进入 C4 视图之前，先回答"哪些边界需要存在"：

- 按 `references/ddd-strategic-modeling.md` 起草 Bounded Context 清单（1–4 个为宜）
- 为每个 Context 写 Purpose / Core Concepts / Language / Ownership
- 把 spec section 14 术语扩展为 Ubiquitous Language 的 design 侧入口；显式列出跨 Context 冲突
- 画 Context Map（用 Mermaid 或紧凑列表）表达 Shared Kernel / Customer-Supplier / ACL / Conformist / Open-Host / Published Language / Separate Ways / Partnership 的真实关系
- 若项目规模不匹配（单模块脚本、单一稳定 Context），可显式标注"本轮不做战略建模"并说明理由

### 2.6 Event Storming Snapshot（Phase 0 新增，按 profile 分档）

按 `references/event-storming.md` 选择合适深度：

- `lightweight`：一段自然语言描述主要事件 / 命令 / 异常流
- `standard`：Event Timeline（Mermaid sequence 或文字时序），含异常路径
- `full`：Event Timeline + Process Modeling（命令 / 策略 / Read Model / 外部系统 / Hotspot 标记）

Hotspot（争议 / 不清楚）应转化为 ADR 候选决策或 STRIDE list 的关注项。事件聚类是候选 Bounded Context 的边界输入。

### 2.7 DDD Tactical Modeling（Phase 0 新增）

在战略建模锁定 Bounded Context 之后、进入候选方案比较之前，回答每个 Context **内部**的领域模型长什么样。

触发条件（任一满足即必须产出；否则显式写明跳过理由）：

- Bounded Context 数量 ≥ 2
- 单个 Bounded Context 内存在**多实体 + 跨实体一致性约束**
- 存在**并发修改**或**事务边界**需要回答
- 存在**领域事件**（业务状态变化需要跨聚合 / Context 感知）
- 规格中存在跨聚合的业务不变量

产出：按 `references/ddd-tactical-modeling.md` 的最小结构，对每个触发 Context 填写 Aggregates / Value Objects / Repositories / Domain Services / Application Services / Domain Events，落到设计文档 § 4.5。

关键决策（聚合边界切分、Domain Event vs 同步调用、乐观 vs 悲观锁）落到 ADR，不内联。

**边界**：本步骤只处理**领域语义驱动**的模式（Entity / VO / Aggregate / Repository / Domain Service / Application Service / Domain Event）。GoF 代码模式（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton 等）**不**在本步骤前置决策——它们属于实现层 emergent 浮现，由实现层 TDD 在 REFACTOR 步按 Fowler 重构词汇处理（详见本 skill Methodology 中 *Emergent vs Upfront Patterns*）。

### 3. 提出 2-3 个候选方案并形成结构化决策

对每个候选方案说明：如何工作、适合原因、主要优缺点、对约束和 NFR 的影响、关键风险。

默认应形成一个紧凑的 compare view，而不是只写 prose。至少让 reviewer 能冷读出：
- 候选方案之间最关键的 trade-offs
- 选定方案为什么比另外方案更匹配当前轮边界
- 哪些决策已经稳定，哪些仍待后续澄清

默认 compare view 至少要能回答以下维度；可用表格、矩阵或等价紧凑结构表达：
- `方案名 / 核心思路`
- `最适合的场景或约束`
- `主要收益`
- `主要代价 / 风险`
- `对关键 NFR / 约束的匹配度`
- `对后续 task planning 的影响`

若复用现有架构、历史方案或团队偏好作为候选项之一，仍要把它放进 compare view，而不是只写“沿用旧方案”。

推荐方案时使用 ADR 格式记录关键决策（按 `references/adr-template.md`）。

若是因 设计评审打回而重入：先读评审 findings → 修复阻塞问题 → 不重做未受影响的部分。

### 4. 校验设计原则

选定方案后、编写设计文档前，校验以下维度：

若 项目声明了项目级设计原则、architecture principles、soul docs 或等价价值锚点，先按声明路径读取，并把它作为候选方案筛选准则；不要假设固定目录、固定文件名或 Garage 特定路径。

- **YAGNI 校验**：决策是否由当前已确认需求驱动？"未来可能需要"标记为过度工程候选
- **复杂度适配**：Solo + 本地运行 → 不引入微服务/消息队列/分布式数据库；文档型 → 不引入重型框架；组件 < 10 → 不需要服务发现
- **模块边界**：依赖单向（内层不依赖外层）、最小知识（接口只暴露最小必要信息）、开闭原则
- **Bounded Context 一致性（Phase 0 新增）**：C4 Container / Component 切分与 Bounded Context 一致；若不一致，必须在 ADR 中显式解释
- **Tactical Model 触发判断（Phase 0 新增）**：满足触发条件时，每个 Bounded Context 产出战术模型（Aggregates / VOs / Repositories / Domain Services / Application Services / Domain Events）；不触发时显式写明跳过理由
- **Emergent vs Upfront 模式边界（Phase 0 新增）**：DDD 战术模式（领域语义驱动）前置决策；GoF 代码模式（实现细节）刻意保持 emergent，不在 design 章节前置列举（详见本 skill Methodology 中 *Emergent vs Upfront Patterns*）
- **NFR QAS 承接（Phase 0 新增）**：每条 spec 中的 QAS 都有对应设计承接（模块 / 机制 / observability / 验证），见 `references/nfr-checklist.md`
- **Security / Threat 触发判断（Phase 0 新增）**：若 Security NFR 存在或跨信任边界存在，必须产出 STRIDE list
- **失败模式**：按 `references/failure-modes.md` 分析关键路径，确认单点故障、错误处理四层次
- **可测试性**：关键行为可隔离验证；存在 Walking Skeleton 最薄端到端路径

### 5. 编写设计文档

按 `references/design-doc-template.md` 的默认结构（或 项目级覆盖的模板）。

明确区分规格层（做什么）、设计层（如何实现）、任务层（分步实施，属于任务规划阶段）。

对非 trivial 设计，提供 2-3 类最少必要视图（逻辑架构、组件/接口关系、关键交互、数据视图），优先 Mermaid。

默认要显式落下以下文档级语义：
- 候选方案对比与选定理由
- 测试与验证策略，尤其是后续 后续实现的最薄验证路径
- task planning readiness：哪些边界、接口、风险已经足够支撑后续任务规划
- 开放问题的阻塞 / 非阻塞分类

### 6. 评审前自检与 handoff

交独立设计评审 前确认：

- [ ] 设计不是规格复述，也不是实现说明
- [ ] 至少比较了两个可行方案并说明选定理由；候选对比已显式评估对 Success Metrics 的影响
- [ ] 关键决策用 ADR 格式记录（含可逆性评估）
- [ ] **Domain Strategic Model（Phase 0）**：Bounded Context / Ubiquitous Language / Context Map 已产出，或显式标注跳过理由
- [ ] **DDD Tactical Model（Phase 0）**：触发条件满足时已产出（每个 Context 的 Aggregates / VOs / Repositories / Domain Services / Application Services / Domain Events）；未触发时显式写明跳过理由
- [ ] **GoF 模式未被前置决策（Phase 0）**：设计文档未列出 Strategy / Factory / Adapter / Observer / Decorator 等实现层模式候选（这些交给实现层 TDD 在 REFACTOR 步 emergent 浮现）
- [ ] **Event Storming Snapshot（Phase 0）**：按当前 profile 产出（lightweight 自然语言 / standard Event Timeline / full + Process Modeling）
- [ ] NFR 逐项落实到具体模块 / 机制（按 `references/nfr-checklist.md`），包含 observability 与验证方法
- [ ] **STRIDE Threat List（Phase 0）**：若 Security NFR 存在或跨信任边界存在，已产出；否则显式标注跳过理由
- [ ] 失败模式覆盖关键路径
- [ ] task planning readiness 已明确，不把未定设计硬推给任务规划
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项不会污染后续任务拆解
- [ ] 明确列出排除项和延后项
- [ ] 设计草稿已保存到 `features/<active>/design.md`（或 项目级覆盖路径）
- [ ] 关键决策已落到 `docs/adr/NNNN-<slug>.md`，状态写 `proposed`，`design.md` 通过 ADR ID 引用而非内联全文
- [ ] feature `progress.md` 已按 canonical schema 更新 Current Stage 和 Next Action

准备好后，启动独立 reviewer subagent 执行设计评审，不在父会话内联评审。

## Reference Guide

按需加载详细参考内容。任一 reference 未命中其"加载时机"时，不需要提前读取。

| 主题 | Reference | 加载时机 | 最小 profile |
|------|-----------|---------|--------------|
| 项目级设计原则锚点 | 项目级约定（查找 design principles / architecture principles / soul docs 的声明路径） | 项目存在这类价值锚点时，先按声明路径加载并用于筛选候选方案 | 全档必读（存在时） |
| ADR 模板 | `references/adr-template.md` | 记录关键决策时 | 全档必读 |
| NFR 检查清单（含 QAS 承接 / observability） | `references/nfr-checklist.md` | 处理非功能需求时 | 全档必读（存在 NFR 时） |
| 失败模式分析 | `references/failure-modes.md` | 分析关键路径韧性时 | standard / full；lightweight 仅关键路径存在时 |
| 架构模式选择 | `references/architecture-patterns.md` | 识别架构模式时 | standard / full；lightweight 仅明显需要选型时 |
| 设计文档模板（含 Phase 0 新章节） | `references/design-doc-template.md` | 编写设计文档时；每次会话至少读一次 | 全档必读 |
| DDD 战略建模 | `references/ddd-strategic-modeling.md` | 进入 C4 前锁边界 / 统一语言 / Context Map；Bounded Context 预计 ≥ 2 时 | full；standard 当跨系统交互或多角色时加载 |
| DDD 战术建模 | `references/ddd-tactical-modeling.md` | 战略建模之后、候选方案比较之前；触发条件（Bounded Context ≥ 2 / 单 Context 多实体 + 一致性约束 / 并发或事务边界 / 领域事件 / 跨聚合不变量）满足时加载 | standard / full；lightweight 允许显式跳过 |
| Emergent vs Upfront 模式立场 | 本 skill Methodology 段 *Emergent vs Upfront Patterns*（已内联） | 判断某个模式该前置还是 emergent 时直接读本 skill 内立场 | 全档必读 |
| Event Storming | `references/event-storming.md` | spec → design 桥接，按 profile 分档 | standard / full；lightweight 允许纯自然语言跳过加载 |
| 轻量 STRIDE 威胁建模 | `references/threat-model-stride.md` | Security NFR 或跨信任边界激活时 | 全档必读（触发时） |

加载策略：

- `lightweight`：默认读 `design-doc-template.md` + `nfr-checklist.md`，并参考本 skill Methodology 段 *Emergent vs Upfront Patterns* 内联立场；ADR 记录时加 `adr-template.md`；STRIDE 触发时加 `threat-model-stride.md`；其余按命中条件
- `standard`：在 lightweight 基础上加 `failure-modes.md` 与 `architecture-patterns.md`；跨系统或多角色时加 `ddd-strategic-modeling.md` 与 `event-storming.md`；战术触发时加 `ddd-tactical-modeling.md`
- `full`：按实际需要加载；Bounded Context 预计 ≥ 2 或存在多 Context 集成时，预读 DDD 战略 + 战术 + Event Storming 三篇

## Red Flags

- 设计文档写成实现伪代码
- 复制需求规格而无设计决策
- 只给一个方案不讨论权衡
- 候选方案只有名称或口号，没有可冷读的 compare view
- 候选对比未显式评估对 Success Metrics 的影响
- 设计文档里直接拆任务
- 只写模块名不写边界、交互和契约
- NFR 只在概述中出现，没落实到具体模块
- NFR 承接表缺 observability 手段或验证方法
- Bounded Context 与 C4 模块切分不一致却无解释
- Ubiquitous Language 只是抄了一遍 spec 术语表，没有澄清冲突
- 战术建模触发条件满足却静默省略，或用"本 Context 简单所以跳过"这种模糊理由
- Aggregate 用 "XxxAggregate" 技术后缀；Repository 服务多个 Aggregate Root；Application Service 里写 if 业务规则（这些都指向战术建模未认真做）
- 设计文档列出 Strategy / Factory / Adapter / Observer / Decorator 等 GoF 候选模式作为前置决策（这是 over-abstraction；GoF 应 emergent 浮现）
- "为了通用 / 为了扩展 / 为了未来可能多一种实现"而在 design 阶段引入抽象层，但当前只有 1 种实现
- Security NFR 存在或跨信任边界存在，却跳过 STRIDE list
- STRIDE list 只填了两三个字母，其余留空
- Event Storming 被画成 sequence diagram 的别名（只记交互，不记业务事件）
- 决策理由含"未来可能需要"而无当前需求支撑
- 没分析关键路径失败模式
- handoff 缺失却声称"设计可以直接往下走"

## Output Contract

完成时产出：

- 可评审设计草稿（默认 `features/<active>/design.md`）
- 关键 ADR（默认 `docs/adr/NNNN-<slug>.md`，状态 `proposed`），design.md 通过 ID 引用
- 源码化图（如有变更，默认 `docs/diagrams/`）
- 设计驱动因素、关键决策、边界与最少必要视图
- feature `README.md` 中 Artifacts 表的 Design 行与 Linked Long-Term Assets 中的 ADRs 行已更新
- 若有 feature 进度记录文件，更新当前阶段标识为 设计阶段

推荐输出：

```markdown
设计文档草稿已起草完成，下一步应派发独立 reviewer subagent 执行设计评审。

产出可评审设计文档
```

如果设计稿仍未达评审门槛，不伪造 handoff；明确还缺什么，继续修订。

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "DDD 战略 / 战术对小 feature 太重，跳过。" | Hard Gates: bounded context + ubiquitous language 是 design 必需输出；缺位时设计评审判 fail。 |
| "我直接套 GoF 模式，不需要在 § 4.5 列战术模式。" | Hard Gates: 实现层 SUT Form `pattern:<name>` 只允许承接 design § 4.5 已批准的 DDD 战术模式（与 SUT Form 形成对位约束），GoF 是 emergent 而非 upfront。 |
| "ADR 留到实现时再补。" | Workflow stop rule: 重大架构决策必须在 design 阶段以 ADR 形式落盘；事后补 ADR 违反 evidence-based routing。 |
| "STRIDE 风险建模等安全审计阶段做。" | Hard Gates: lightweight STRIDE 是 design 阶段必需输出；当项目尚未引入独立安全加固阶段时，design 是唯一安全捕获点。 |

## Verification

- [ ] 设计草稿已保存到 `features/<active>/design.md`（非规格文件、非任务文件）
- [ ] 至少两个候选方案已比较，选定理由已用 ADR 格式记录到 `docs/adr/NNNN-<slug>.md`（status: proposed）
- [ ] 候选方案 compare view 显式评估对 Success Metrics 的影响
- [ ] 至少保留一个可冷读的候选方案 compare view（表格、矩阵或等价紧凑结构）
- [ ] **Domain Strategic Model**：Bounded Context / Ubiquitous Language / Context Map 已产出，或显式写明跳过理由
- [ ] **DDD Tactical Model**：触发条件满足时每个 Context 的 Aggregates / VOs / Repositories / Domain Services / Application Services / Domain Events 已产出；未触发时显式写明跳过理由
- [ ] **Emergent vs Upfront 模式边界**：设计文档未把 GoF 代码模式（Strategy / Factory / Adapter / Observer / Decorator 等）当作前置决策列入
- [ ] **Event Storming Snapshot**：按当前 profile 产出；Hotspot（若有）已转化为 ADR 候选或 STRIDE 关注项
- [ ] NFR 逐项落实到具体模块 / 机制（不是只在概述中出现）；每条关键 NFR 有 observability 手段与验证方法
- [ ] **STRIDE Threat List**：若 Security NFR 激活或跨信任边界存在，已产出完整 S/T/R/I/D/E 六字母；否则显式写明跳过理由
- [ ] 关键路径失败模式已分析，缓解策略已给出
- [ ] task planning readiness 已明确，足以进入任务规划
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项已关闭或回上游
- [ ] feature `progress.md` 已按 canonical schema 更新 Current Stage 和 Next Action
- [ ] feature `README.md` 中 Design / ADRs 引用已更新
- [ ] handoff 目标唯一指向独立设计评审
- [ ] 设计草稿不含任务拆解或实现伪代码

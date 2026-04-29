# 设计评审检查清单

评审设计文档时，至少对以下 6 个维度逐项审查。每个维度内部评分 `0-10`，评分帮助区分轻微缺口与阻塞问题。

## 评分辅助规则

- 任一关键维度低于 `6/10` → 不得返回 `通过`
- 任一维度低于 `8/10` → 通常至少对应一条具体发现项或薄弱点

## 评审维度

| ID | 维度 | Pass Condition |
|---|---|---|
| `D1` | 需求覆盖与追溯 | 设计覆盖关键需求，新增关键能力可回指到已批准规格 |
| `D2` | 架构一致性 | 边界、职责、关键视图与关键交互足够清楚，不是松散组件清单 |
| `D3` | 决策质量与 trade-offs | 至少比较两个可行方案，选型理由、收益、代价与风险显式写清 |
| `D4` | 约束与 NFR 适配 | 约束、NFR、集成点真正进入设计，而不是只在概述里被提到 |
| `D5` | 接口与任务规划准备度 | 契约、边界与关键交互足够稳定，`hf-tasks` 不需要替设计补洞 |
| `D6` | 测试准备度与隐藏假设 | 存在设计层测试策略，关键 assumptions 已显式写出且不污染后续任务 |

### `D1` 需求覆盖与追溯

- 设计是否覆盖了规格中的关键需求？
- 主要行为是否映射到了组件、模块、流程或接口？
- 关键需求能否回指到稳定需求条目、需求编号或等价规格锚点？
- 是否存在新增行为、接口、数据持久化或运营流程，却无法追溯到已批准规格？

### `D2` 架构一致性

- 职责和边界是否清晰？
- 模块之间的交互是否容易理解？
- 设计是否是连贯架构，而不是组件清单？
- 关键视图、关键交互或关键流程是否已经清楚到足以支撑评审？
- **DDD Tactical Model 承接（Phase 0 新增）**：触发条件满足时（Bounded Context ≥ 2 / 单 Context 多实体 + 一致性约束 / 并发或事务边界 / 领域事件 / 跨聚合不变量），每个 Context 是否产出 Aggregates / VOs / Repositories / Application Services / Domain Events？聚合的 Transaction Boundary 与 Concurrency Strategy 是否显式？Repository 是否一对一服务 Aggregate Root？未触发时是否显式写明跳过理由？

### `D3` 决策质量与 trade-offs

- 是否真的比较了至少两个可行方案？
- 是否说明为什么选定当前方案？
- 是否记录了主要收益、代价、风险与缓解思路？
- reviewer 能否冷读出 trade-off，而不需要从 prose 猜测？
- **Emergent vs Upfront 模式边界（Phase 0 新增）**：设计是否把**领域语义驱动的模式**（Entity / VO / Aggregate / Repository / Domain Service / Application Service / Domain Event）前置决策，同时**不**把 GoF 代码模式（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton 等）作为前置决策列入？若设计列出 GoF 候选模式作为"为了扩展 / 通用 / 未来可能"，应视为 over-abstraction 征兆。HF 立场：GoF 代码模式属于实现层 emergent 浮现，由 `hf-test-driven-dev` 在 REFACTOR 步按 Fowler 重构词汇浮现处理，不前置决策。

### `D4` 约束与非功能需求适配

- 设计是否体现了已声明约束？
- 是否考虑了非功能需求和集成点？
- 这些要求是否真正影响了设计，而不是只在概述里被提到？

### `D5` 接口与任务规划准备度

- 关键契约是否足够明确，可以支撑任务规划？
- 主要数据流和控制流是否清晰？
- 模块边界是否已经稳定到可以继续拆任务？
- 是否还存在会直接破坏任务拆解顺序的设计空洞？
- 文档是否显式说明了 task planning readiness，而不是把缺口留给下游猜？

### `D6` 测试准备度与隐藏假设

- 设计是否包含设计层面的测试策略？
- 该设计是否可测试，而不依赖隐藏假设？
- 是否指出了需要在后续任务规划或实现阶段优先验证的高风险点？
- 关键 assumptions 是否显式写出，并说明失效时会影响什么？

## Anti-Pattern 检测

评审时主动检测以下常见反模式：

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `A1` | 无 NFR 评估 | 设计只通过功能测试但忽略性能/安全/可扩展 | 必须评估性能、安全、可扩展性 |
| `A2` | 只审 happy path | 系统在错误边界失败，不在正常路径 | 审查失败模式、重试行为、熔断 |
| `A3` | 无权衡文档 | 隐藏的 trade-off 变成未来意外 | 显式记录所有权衡及理由 |
| `A4` | 单点故障未记录 | 系统有隐性脆弱点，负载下才暴露 | 映射所有 SPOF，要求缓解计划 |
| `A5` | 实现后评审 | 结构性问题发现太晚，修复成本 10-100x | 在设计阶段、代码编写前评审 |
| `A6` | 上帝模块 | 单个模块/服务处理多个领域 | 按领域拆分职责 |
| `A7` | 循环依赖 | 模块间相互引用 | 强制单向依赖，内层不依赖外层 |
| `A8` | 分布式单体 | 表面是微服务，实际共享数据库耦合 | 按领域边界独立数据 |
| `A9` | task planning gap | 接口边界或 readiness 缺口被留给 `hf-tasks` 猜 | 在设计层显式关闭或标出阻塞 |
| `A10` | tactical-model-absent | Tactical 触发条件满足但设计文档 § 4.5 空白或只写 "此处略过" | 按 `ddd-tactical-modeling.md` 补全每个触发 Context 的 Aggregates / VOs / Repositories / Application Services / Domain Events；或显式写明跳过理由 |
| `A11` | upfront-gof-pattern | 设计文档列出 GoF 代码模式（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton）作为前置决策，理由是 "为了扩展 / 通用 / 未来可能多一种实现" | 从设计文档移除；GoF 模式应 emergent 浮现，由 `hf-test-driven-dev` REFACTOR 步按 Fowler 重构词汇（Replace Conditional with Polymorphism / Extract Factory Method / ...）处理 |

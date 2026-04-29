# DDD 战术建模参考（Entity / Value Object / Aggregate / Repository / Domain Service / Application Service / Domain Event）

## Purpose

本参考把 **Eric Evans** *Domain-Driven Design* 的**战术**部分作为 `hf-design` 中 Bounded Context 内部的**结构化骨架**，用来：

- 在战略建模（`ddd-strategic-modeling.md`）锁定 Bounded Context 之后，回答每个 Context **内部**的模型长什么样
- 把 "写代码前要考虑好模式" 这件事落到**领域语义驱动**的选择上，而不是 GoF 直觉驱动
- 给 `hf-test-driven-dev` 提供稳定的实现契约：测试命名、类 / 接口命名、聚合边界、事务边界在 design 阶段先定，REFACTOR 步不再被迫调整结构

战术建模的目标是**让领域模型可表达 + 事务边界清楚**，不是穷举所有模式。

## One-Line Rule

**模式跟着语义走**：先回答"这个东西有没有身份？能不能单独存在？谁能改它？改它要锁什么？"，再回答"用 Entity 还是 Value Object、放在哪个 Aggregate 里"。

## Scope 与职责边界

| 本参考覆盖 | 本参考不覆盖 |
|---|---|
| Bounded Context **内部**的模型构件（Entity / VO / Aggregate / Repository / Domain Service / Application Service / Domain Event） | Bounded Context 边界与 Context Map（见 `ddd-strategic-modeling.md`） |
| 聚合边界与事务边界（一致性规则） | 基础设施适配层的具体实现（见 `hf-test-driven-dev`） |
| 领域事件的发布时机与不变量 | 消息队列 / 事件总线的技术选型（属于架构模式，见 `architecture-patterns.md`） |
| 仓储接口签名的职责分层 | 仓储背后的 ORM / SQL / 存储实现 |
| **tactical pattern 的命名选择**（Repository vs DAO / Domain Service vs Application Service） | **GoF 代码模式**（Strategy / Factory / Adapter / Observer / Decorator 等）——这些属于实现层 emergent 选择，由 `hf-test-driven-dev` 的 REFACTOR 步按 Fowler 重构词汇浮现处理 |

## 何时激活（触发条件）

满足任一条件即**必须产出**战术模型；否则可在 design 文档中显式写明跳过理由。

- Bounded Context 数量 ≥ 2
- 单个 Bounded Context 内存在**多实体 + 跨实体一致性约束**（例如 "订单创建时库存必须同步扣减"）
- 存在**并发修改**或**事务边界**需要回答
- 存在**领域事件**（业务状态变化需要被其他 Context / 外部系统感知）
- 规格中存在跨聚合的业务不变量（invariant spanning aggregates）

**不触发**的典型场景：

- 纯工具 / CLI 脚本，无持久化实体
- 单 Bounded Context 且只有 CRUD，无不变量
- 纯运维 / DX / 工程设施（无领域概念）

跳过时仍需保留一小节解释"为什么不做战术建模"，而不是沉默省略。

## 核心构件

### 1. Entity（实体）

**判断信号**：拥有**跨时间的身份（identity）**、状态可变、即使所有属性都变了它仍是"同一个"。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Name** | 采用 Ubiquitous Language 中的名词 | 不使用 "XxxEntity" / "XxxModel" 这类技术后缀 |
| **Identity** | 标识来源（自然键 / 生成 ID / 复合键） | 显式说明 identity 生成时机 |
| **Invariants** | 该实体必须始终成立的业务规则 | 一行一条；违反时的失败模式见 `failure-modes.md` |
| **Lifecycle** | 创建 / 激活 / 归档 / 删除 的合法转换 | 不合法的状态转换必须被拒绝，不是被忽略 |
| **Aggregate Membership** | 属于哪个 Aggregate（自身是 root 还是 member） | 每个 Entity 必须归属一个 Aggregate |

### 2. Value Object（值对象）

**判断信号**：**没有身份**、仅由属性值定义相等性、**不可变**、替换而非修改。

典型例子：金额（Money）、日期范围（DateRange）、地址（Address）、坐标（GeoPoint）。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Name** | Ubiquitous Language 中的名词 | 避免 "XxxVO" 后缀 |
| **Attributes** | 构成该值的所有属性 | 全部参与相等性判断 |
| **Invariants** | 值本身的合法性约束（例如 Money 的币种非空 + 金额非负） | 构造时校验，不允许非法状态 |
| **Operations** | 该值支持的纯函数操作（add / scale / within） | 不修改 self，返回新值 |

### 3. Aggregate（聚合）

**判断信号**：一组需要**共同维护某个业务不变量**的 Entity + Value Object；外部只能通过 **Aggregate Root** 访问。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Root** | 聚合根实体 | 每个 Aggregate 恰有一个 root |
| **Members** | 包含的 Entity / Value Object | 内部 Entity 的 identity 只在 Aggregate 内唯一 |
| **Invariants Enforced** | 该聚合负责维护的业务不变量 | 每条必须说明"违反时会怎样" |
| **Transaction Boundary** | 一次事务最多修改一个 Aggregate 实例 | 跨聚合一致性走领域事件 + 最终一致，不走分布式事务 |
| **Concurrency Strategy** | 乐观锁 / 悲观锁 / 无锁 + 版本号 | 必须显式回答，不允许"默认行为" |
| **External References** | 如何引用其他 Aggregate | **只通过 ID 引用**，不持有其他聚合的对象引用 |

**聚合大小规则**（Vaughn Vernon, *Implementing Domain-Driven Design*）：

- 优先设计**小聚合**（root + 少量 VO）
- 跨聚合一致性通过**领域事件 + 最终一致性**实现，不通过一次事务修改多个 Aggregate
- 若发现 "必须一次事务同时改多个 Aggregate"，先质疑聚合边界是否切错了

### 4. Repository（仓储）

**判断信号**：为某个 Aggregate Root 提供**集合式**的持久化抽象；领域层只看到"集合"，不看到数据库。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Target Aggregate** | 仓储服务的 Aggregate Root | **一个 Repository 只服务一个 Aggregate Root** |
| **Interface Signature** | `save / findById / findBy<业务查询> / remove` 等 | 接口定义在领域层；实现放在基础设施层（DIP） |
| **Query Style** | Specification / Named Query / Criteria | 不暴露 SQL / ORM 细节到领域层 |
| **Transactional Contract** | 单次 save 是否原子、是否触发事件发布 | 显式写明 |

**Repository ≠ DAO**：Repository 是领域视角的集合抽象；DAO 是数据访问视角的表操作封装。若本轮只做 CRUD、无聚合不变量，可以直接用 DAO 而不强行套 Repository，但需在设计文档里显式声明"本 Context 无聚合，使用 DAO"。

### 5. Domain Service（领域服务）

**判断信号**：某个业务行为**不自然属于任何一个 Entity 或 Value Object**，但仍是领域逻辑。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Name** | 动词短语（Ubiquitous Language） | 避免 "XxxService" 泛化后缀；名字要能读出业务动作 |
| **Inputs / Outputs** | 明确类型（通常是 Entity / VO） | 不接受 DTO / 原始 dict |
| **Side Effects** | 是否修改状态、是否发布领域事件 | 显式写清 |
| **Stateless** | 自身无状态 | 若需要状态，应改建模为 Entity 或拆到 Application Service |

**Domain Service ≠ Application Service**（见下条）。

### 6. Application Service（应用服务）

**判断信号**：编排一次**用例（use case）**——接收外部请求、校验授权、协调 Aggregate + Domain Service + Repository、管理事务、发布 Integration Event。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Use Case Name** | 一次用例（例如 PlaceOrder / CancelReservation） | 与 spec 中的 FR 编号 / BDD 场景对齐 |
| **Orchestration** | 依次调用了哪些 Domain Service / Aggregate / Repository | 不含业务规则；业务规则在 Domain 层 |
| **Transaction Scope** | 本用例的事务边界 | 通常 1 个 Aggregate / 1 次事务 |
| **Authorization** | 访问控制检查点 | 必须显式（即使是 `public`） |
| **Integration Events Emitted** | 本用例对外发布的事件 | 列出事件名 + 触发条件 |

**红线**：Application Service 里**不允许出现业务规则判断**（if 条件 + 业务含义）。一旦发现，把该规则迁回 Entity / Aggregate / Domain Service。

### 7. Domain Event（领域事件）

**判断信号**：业务状态**已经发生**的事实（过去时命名：`OrderPlaced` / `ReservationCancelled`），其他聚合 / Context / 外部系统可能需要感知。

| 字段 | 含义 | 约束 |
|---|---|---|
| **Name** | 过去时 + 业务语言 | 不使用 "XxxEvent" 之外的技术后缀也可接受，但语义必须是"已发生" |
| **Payload** | 事件携带的最小必要数据 | 不携带聚合引用；只携带 ID + 业务必要字段 |
| **Emitted By** | 发出该事件的 Aggregate / Use Case | 必须在事务提交后发布（或事务内写 outbox） |
| **Consumers** | 本 Context 内订阅方 + 跨 Context 的 Integration Event 映射 | 区分 Domain Event vs Integration Event：前者内部、后者跨 Context |
| **Delivery Guarantee** | at-least-once / at-most-once / exactly-once | 与 NFR 的一致性要求对齐 |

## 选型决策表

在每个 Bounded Context 内部，按以下顺序回答：

```
这个概念有身份吗？
  否 → Value Object
  是 ↓
它能单独存在于任何事务之外吗？
  否（必须由其他实体守护） → 归入某个 Aggregate 作为 Member
  是 ↓
它是聚合根候选。它维护哪些跨成员的不变量？
  无 → 大概率是贫血的 Entity；质疑是否真的需要独立 Aggregate
  有 ↓
这些不变量能在"一次修改 = 一个 Aggregate"下维护吗？
  否 → 拆聚合；跨聚合走领域事件 + 最终一致
  是 ↓
该 Aggregate Root 需要集合式持久化抽象吗？
  是 → 配一个 Repository（仅服务该 root）
  否 → 纯内存计算（例如策略对象），不需要 Repository
---
有行为属于领域但不归属任何 Entity / VO 吗？
  是 → Domain Service（动词命名）
  否 → 不强造
---
有跨 Aggregate 的业务事实需要通知吗？
  是 → Domain Event（过去时命名）+ 必要时升级为 Integration Event
  否 → 不强造
---
最外层用例编排放在哪里？
  → Application Service（一次用例一个入口）
```

## 输出到 design 文档的最小结构

在 `design-doc-template.md` 的 `§ 4.5 Tactical Model per Bounded Context` 章节，每个需要战术建模的 Bounded Context 至少写一份：

```markdown
### Bounded Context: <Name>

**Aggregates**

| Aggregate Root | Members | Invariants Enforced | Transaction Boundary | Concurrency |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

**Value Objects**

| Name | Attributes | Key Operations |
|---|---|---|
| ... | ... | ... |

**Repositories**

| Target Aggregate Root | Key Methods | Query Style |
|---|---|---|
| ... | ... | ... |

**Domain Services** (optional)

| Name | Inputs → Outputs | Side Effects |
|---|---|---|
| ... | ... | ... |

**Application Services** (use cases)

| Use Case | FR Ref | Orchestration | Tx Scope | Events Emitted |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

**Domain Events**

| Event (past tense) | Payload | Emitted By | Consumers | Delivery |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
```

若本 Context 不做战术建模，写：

```markdown
### Bounded Context: <Name>

本轮不做战术建模，理由：<单聚合 CRUD / 无不变量 / 纯查询 / ...>
```

## 与其他参考的衔接

| 关系 | 说明 |
|---|---|
| `ddd-strategic-modeling.md` | 本参考的**上游**；战术建模发生在 Bounded Context 锁定之后 |
| `architecture-patterns.md` | 本参考的**平行层**；战术模式回答"领域内部怎么建模"，架构模式回答"系统整体怎么部署" |
| `nfr-checklist.md` | 聚合的 Concurrency Strategy / Domain Event 的 Delivery Guarantee 必须承接 NFR 中的一致性 / 可用性 QAS |
| `failure-modes.md` | 聚合不变量违反、事件投递失败是关键失败模式候选 |
| `adr-template.md` | 关键战术决策（聚合边界切分、Domain Event vs 同步调用、乐观 vs 悲观锁）落到 ADR |
| Emergent vs Upfront 立场（已内联到 `hf-design/SKILL.md` Methodology 段） | **GoF 代码模式不在本参考范围**；HF 刻意让 GoF 在 `hf-test-driven-dev` REFACTOR 步 emergent 浮现，不前置决策 |

## 反模式（Red Flags）

- **Entity 用 "XxxEntity / XxxModel" 后缀**：暴露技术思维；用 Ubiquitous Language 命名
- **Aggregate 巨无霸**：一个 Aggregate 包含 ≥ 5 个 Entity，一次事务改一堆成员 → 大概率切错了
- **Repository 服务多个 Aggregate Root**：违反"一个 Repository 一个 root"
- **Repository 接口泄漏 SQL / JPA / ORM 注解到领域层**：违反 DIP
- **Domain Service 承担编排**：应该是 Application Service 的职责
- **Application Service 里写 if 业务规则**：业务规则外泄；迁回 Domain 层
- **跨 Aggregate 一次事务修改**：要么重切聚合，要么走领域事件 + 最终一致
- **Domain Event 命名用现在时 / 将来时**（`PlaceOrder` / `WillCancel`）：事件语义要求**已发生**
- **Domain Event 直接传整个聚合对象**：应只传 ID + 必要字段
- **本来只有 CRUD 硬套 Aggregate / Repository**：过度工程；显式声明"本 Context 无聚合，使用 DAO"
- **把 GoF 模式（Strategy / Factory / Adapter）塞到战术模型章节**：越权；GoF 是实现层 emergent 选择，由 `hf-test-driven-dev` REFACTOR 步按 Fowler 重构词汇浮现处理（HF 立场已内联 `hf-design/SKILL.md` Methodology 段）

## 规模控制

| Context 规模 | Aggregate 数量 | Domain Service 数量 | 备注 |
|---|---|---|---|
| 小 | 1–2 | 0–1 | 常见于 MVP / discovery 级 |
| 中 | 3–5 | 1–3 | 标准规模 |
| 大 | 6+ | 3+ | 先质疑 Bounded Context 是否应拆分 |

Application Service 数量通常 = 本 Context 的核心用例数（FR 主线数），不做额外聚合。

## Bottom Line

- 战术建模回答 "Bounded Context **内部**怎么长"，是 `hf-design` 从 "系统结构" 下沉到 "领域语义" 的必要一步
- 触发条件满足时必须做；不满足时显式跳过
- 战术模式 ≠ GoF 代码模式：前者前置决策（领域语义稳定），后者 emergent 浮现（实现细节随需要演化）
- 所有战术决策的可逆性 / 权衡落到 ADR，不内联进 `design.md` 正文

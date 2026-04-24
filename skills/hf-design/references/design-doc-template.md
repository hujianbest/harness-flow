# 设计文档模板

若 `AGENTS.md` 为当前项目声明了设计模板，优先使用项目约定。以下为默认结构。

## 默认结构

```markdown
# <主题> 实现设计

- 状态: 草稿
- 主题: <主题>

## 1. 概述
## 2. 设计驱动因素
## 3. 需求覆盖与追溯
## 4. Domain Strategic Model (Bounded Context / Ubiquitous Language / Context Map)
## 4.5 Tactical Model per Bounded Context (Aggregates / VOs / Repositories / Domain Services / Application Services / Domain Events)
## 5. Event Storming Snapshot（按 profile 分档；lightweight 允许纯自然语言）
## 6. 架构模式选择
## 7. 候选方案总览
## 8. 候选方案对比与 trade-offs
## 9. 选定方案与关键决策
## 10. 架构视图（C4 Context / Container / Component）
## 11. 模块职责与边界
## 12. 数据流、控制流与关键交互
## 13. 接口、契约与关键不变量
## 14. 非功能需求与 QAS 承接（逐条 → 模块 / 机制 / 可观测 / 验证）
## 15. Threat Model (STRIDE 轻量版，触发条件满足时必填)
## 16. 测试与验证策略
## 17. 失败模式与韧性策略
## 18. 任务规划准备度
## 19. 关键决策记录（ADR 摘要）
## 20. 明确排除与延后项
## 21. 风险与开放问题（区分阻塞 / 非阻塞）
```

Phase 0 新增章节（4 / 4.5 / 5 / 14 / 15）是**结构化锚点**：

- 章节 4（Domain Strategic Model）在 spec 存在多概念 / 多角色 / 跨系统交互时必填；纯脚本 / 单模块可显式跳过并说明理由。
- 章节 4.5（Tactical Model per Bounded Context）在战术触发条件满足时必填（Bounded Context ≥ 2 / 单 Context 多实体 + 一致性约束 / 并发或事务边界 / 领域事件 / 跨聚合不变量）；不触发时显式跳过并说明理由。**GoF 代码模式不写入本章节**（见 `docs/principles/emergent-vs-upfront-patterns.md`）。
- 章节 5（Event Storming Snapshot）按 profile 分档：`lightweight` 自然语言、`standard` Event Timeline、`full` Event Timeline + Process Modeling。
- 章节 14（NFR QAS 承接）必填；承接 spec 中的 QAS，按 `nfr-checklist.md` 结构化表格。
- 章节 15（STRIDE Threat Model）在触发条件满足时必填（见 `threat-model-stride.md`）。

## 编写要求

- 区分需求与设计
- 清晰定义边界和职责
- 用追溯视角说明关键需求被哪些模块、流程或接口承接
- 解释为什么所选方案适合该规格
- 至少保留一个紧凑的候选方案对比视图，不让 reviewer 只能从 prose 猜 trade-off
- NFR QAS 承接表必须按 `nfr-checklist.md` 填写
- 测试与验证策略至少说明一条可落到 `hf-test-driven-dev` 的最薄验证路径
- 任务规划准备度要说明哪些边界、接口和风险已经足够支撑 `hf-tasks`
- 说明设计怎样支撑后续任务规划，但不要写成任务计划
- 提供足够支撑任务拆解的细节，但不要写成逐行编码说明

## Domain Strategic Model 最小要求

按 `ddd-strategic-modeling.md`：

- Bounded Context 清单（1–4 个为宜）
- Ubiquitous Language 词表（先覆盖跨 Context 容易歧义的术语）
- Context Map（用 Mermaid 或紧凑列表；表达 Shared Kernel / Customer-Supplier / ACL / Conformist / Open-Host / Published Language / Separate Ways / Partnership 中的现实关系）
- 若本轮不做战略建模，显式写明理由

## Tactical Model 最小要求

按 `ddd-tactical-modeling.md`：

**触发条件**（任一满足即必填；否则每个 Context 下显式写 "本 Context 不做战术建模，理由：..."）：

- Bounded Context 数量 ≥ 2
- 单个 Bounded Context 内存在多实体 + 跨实体一致性约束
- 存在并发修改 / 事务边界 / 领域事件 / 跨聚合不变量

**每个触发 Context 至少填**（按 `ddd-tactical-modeling.md` 提供的紧凑表格）：

- Aggregates（Root / Members / Invariants / Transaction Boundary / Concurrency）
- Value Objects（Attributes / Operations）
- Repositories（Target Aggregate Root / Key Methods / Query Style）
- Application Services（Use Case / FR Ref / Orchestration / Tx Scope / Events Emitted）
- Domain Events（过去时命名 / Payload / Emitted By / Consumers / Delivery）

可选：Domain Services（动词短语命名；仅在行为不属于任何 Entity / VO 时引入）。

**禁止**：

- 把 GoF 代码模式（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton 等）作为前置决策列入本章节——这类模式属于实现层 emergent 浮现，见 `docs/principles/emergent-vs-upfront-patterns.md`
- 用 "XxxAggregate" / "XxxEntity" / "XxxVO" 这类技术后缀命名，应直接使用 Ubiquitous Language 名词
- 未显式回答事务边界 / 并发策略的聚合
- 服务多个 Aggregate Root 的 Repository
- 现在时 / 将来时命名的 Domain Event

## Event Storming Snapshot 最小要求（按 profile）

- `lightweight`：一段自然语言描述"主要事件 / 命令 / 异常流"
- `standard`：Event Timeline（文字 / Mermaid sequence），含异常路径
- `full`：Event Timeline + Process Modeling（命令 / 策略 / Read Model / 外部系统 / Hotspot）

Hotspot（红色标记）与 ADR、STRIDE 的关系必须显式交叉引用。

## 候选方案最小对比视图

若项目模板未声明更强结构，`## 8. 候选方案对比与 trade-offs` 默认至少提供一个紧凑矩阵，让 reviewer 冷读出关键差异：

```markdown
| 方案 | 核心思路 | 优点 | 主要代价 / 风险 | NFR / 约束适配 (对 QAS) | 对 Success Metrics 的影响 | 可逆性 |
|------|----------|------|------------------|--------------------------|----------------------------|--------|
| A | ... | ... | ... | ... | ... | 高 / 中 / 低 |
| B | ... | ... | ... | ... | ... | 高 / 中 / 低 |
```

至少满足：

- 比较 2 个及以上真实可行方案，而不是"推荐方案 + 稻草人"
- `主要代价 / 风险` 不能留空；必须说明为什么不是所有方案都同样好
- `NFR / 约束适配` 要显式承接规格中的关键 QAS（不是空泛"影响性能"）
- `对 Success Metrics 的影响` 必须回指 spec section 3 的 Outcome Metric（Phase 0 新增）
- `可逆性` 应与 ADR 中的可逆性评估口径一致
- 若复用既有架构，也要把"复用现状"当作候选方案之一写入矩阵，而不是跳过比较

## Threat Model (STRIDE) 触发与最小结构

见 `threat-model-stride.md`。触发条件：

- spec 有 Security NFR
- 存在跨信任边界数据流
- 处理认证 / 授权 / 敏感数据
- 有审计 / 合规要求

每条关键资产 / 数据流 / 信任边界在 STRIDE 六字母下均要写"威胁 + 缓解"或"不适用 + 理由"，不允许留空。

## 保存路径

默认：`features/<active>/design.md`

若 `AGENTS.md` 声明了设计路径映射，优先使用映射路径。

## 状态同步

设计草稿交评审后，应同步：
- 设计文档状态（`状态: 草稿`）
- feature `progress.md`（默认 `features/<active>/progress.md`）中的 `Current Stage: hf-design`
- feature `progress.md` 中的 `Next Action Or Recommended Skill: hf-design-review`

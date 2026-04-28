# df Component Design Review Rubric

> 配套 `df-component-design-review/SKILL.md`。展开 7 维度评分细则与 rule IDs。

## 7 维度评分

| 维度 | 关键检查 | < 6 的典型信号 |
|---|---|---|
| **CD1 Identity & Template Conformance** | 组件名 / 子系统 / Owner / 模板版本完整；团队模板章节齐全或显式标注占位 | 模板留空但未标注；Owner 缺失 |
| **CD2 Responsibility & Non-Responsibility** | 职责 / 非职责清晰，未越界承接其他组件 | 职责模糊；与相邻组件重叠 |
| **CD3 SOA Interface Quality** | 接口名 / 参数 / 错误码 / 时序约束 / 兼容性 | 缺错误码；缺时序；接口聚合多个无关用途（违反 ISP） |
| **CD4 Dependency & Direction** | 依赖方向无环；初始化 / shutdown 顺序明确；版本约束清晰 | 循环依赖；初始化顺序模糊 |
| **CD5 Data Model & State Machine** | 数据模型与状态机覆盖核心生命周期；转换条件清晰 | 状态机缺关键路径；异常状态无说明 |
| **CD6 Concurrency / Real-time / Resource / Error Handling** | 中断上下文限制、锁策略、资源回收、错误处理、ABI / API 兼容 | 中断上下文无说明；资源回收缺 |
| **CD7 AR Design Constraints & Cross-Component Impact** | 「对 AR 实现设计的约束」章节存在；跨组件影响显式列出且与下游协调 | 对 AR 设计无任何约束；跨组件影响只字未提 |

任一关键维度 < 6 → 不得 `通过`。

## Rule IDs

### Group CD1 - Identity & Template

- `CD1.1` 模板版本与团队模板对齐（或显式标注占位）
- `CD1.2` Owner（模块架构师）显式记录
- `CD1.3` 变更记录完整（修订时必须填）

### Group CD2 - Responsibility

- `CD2.1` 职责正向描述清晰可冷读
- `CD2.2` 非职责显式列出，未模糊化（"按需"、"必要时"）
- `CD2.3` 与相邻组件无职责重叠（或解释了边界协议）

### Group CD3 - SOA Interface

- `CD3.1` 每个接口含名 / 参数 / 返回值 / 错误码
- `CD3.2` 时序约束（同步 / 异步、超时、阻塞 / 非阻塞）
- `CD3.3` 兼容性策略（向前 / 向后兼容、deprecation 路径）
- `CD3.4` 接口最小知识（不强迫消费方依赖无关字段）

### Group CD4 - Dependency

- `CD4.1` 依赖方向无环
- `CD4.2` 初始化 / shutdown 顺序明确
- `CD4.3` 版本约束 / 编译条件清晰
- `CD4.4` 不暴露内部实现给上层

### Group CD5 - Data & State

- `CD5.1` 数据模型字段语义清晰、约束（取值范围、单位、时序）显式
- `CD5.2` 状态机覆盖关键生命周期
- `CD5.3` 状态转换条件、异常状态、恢复路径明确

### Group CD6 - Embedded Risk

- `CD6.1` 中断上下文允许 / 禁止的操作显式
- `CD6.2` 锁 / 临界区策略 + 死锁规避
- `CD6.3` 内存模型（静态 / 动态、池化、栈深度）
- `CD6.4` 实时性 / 调度 / 时钟 / 节拍约束
- `CD6.5` 资源生命周期（句柄、文件、缓冲区）配对
- `CD6.6` 错误处理统一策略 + 降级路径
- `CD6.7` ABI / API 兼容（跨版本、跨平台）

### Group CD7 - AR Constraints & Cross-Component

- `CD7.1` 「对 AR 实现设计的约束」章节存在并具体
- `CD7.2` 跨组件影响显式列出
- `CD7.3` 跨组件协调路径（哪些下游组件需要同步开 work item）明确

## Severity 分级

- `critical`：阻塞 AR 设计（缺 SOA 接口、循环依赖、状态机关键路径缺失、对 AR 设计无任何约束）
- `important`：approval 前应修（错误码不全、时序约束模糊、跨组件影响未列）
- `minor`：建议改进（措辞、排版、章节顺序）

## Classification

- `USER-INPUT`：业务方向 / 跨子系统协调 / 模块架构师 sign-off
- `LLM-FIXABLE`：模板章节缺、措辞模糊、错误码列表不完整、状态机示意补全
- `TEAM-EXPERT`：组件边界、SOA 接口最终决策、并发 / 实时性架构选型 → 上抛模块架构师 / 资深嵌入式工程师

## Verdict 决策

| 评分 / findings 状态 | verdict | needs_human_confirmation |
|---|---|---|
| 7 维度均 ≥ 6、无 critical USER-INPUT、模块架构师可被请求 sign-off | `通过` | `true`（等 sign-off） |
| 评分某项 < 6 但 findings 可 1-2 轮定向修订 | `需修改` | `false` |
| 评分多项 < 6 / critical TEAM-EXPERT 阻塞 / 组件边界严重不清 | `阻塞`（内容） | `false` |
| route / stage / profile / 上游证据冲突 | `阻塞`（workflow） + `reroute_via_router=true` | `false` |

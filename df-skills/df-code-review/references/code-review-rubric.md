# df Code Review Rubric

> 配套 `df-code-review/SKILL.md`。展开 8 维度评分细则与 rule IDs。

## 8 维度评分

| 维度 | 关键检查 |
|---|---|
| **CR1 Correctness** | 实现是否真正完成 AR 行为；逻辑无 off-by-one / 边界遗漏 |
| **CR2 Design Conformance** | 实现是否遵循 AR 设计 + 组件设计；偏离需有理由且可追溯 |
| **CR3 SOA Boundary Conformance** | 不破坏 SOA 边界；不引入未解释跨组件依赖；不绕过组件接口 |
| **CR4 Memory & Resource Lifecycle** | 内存模型符合组件设计；句柄 / 文件 / 缓冲区配对释放；无泄漏路径 |
| **CR5 Concurrency & Real-time** | 中断上下文允许 / 禁止操作；锁策略；临界区；实时性约束 |
| **CR6 Error Handling & Defensive Design** | 输入校验；错误码；降级路径；ABI / API 兼容 |
| **CR7 Coding Standard & Static Analysis** | MISRA / CERT / 团队编码规范；编译告警；静态分析 critical 项已闭环 |
| **CR8 Refactor Note & Architectural Health** | Refactor Note 完整；cleanup 守 Two Hats；未触发 escalation 边界 |

CR3 / CR4 / CR5 / CR6 是嵌入式核心维度；任一 < 7 即不得 `通过`（其他维度 < 6 不得 `通过`）。

## Rule IDs

### Group CR1 - Correctness

- `CR1.1` 实现完整覆盖 AR 行为
- `CR1.2` 边界条件处理正确
- `CR1.3` 死代码 / 不可达分支已清理或解释

### Group CR2 - Design Conformance

- `CR2.1` 实现遵循 ar-design-draft.md
- `CR2.2` 与 component-design.md 一致
- `CR2.3` 偏离设计的部分有显式理由 + 追溯锚点

### Group CR3 - SOA Boundary

- `CR3.1` 不绕过组件 SOA 接口
- `CR3.2` 不引入未声明的跨组件依赖
- `CR3.3` 接口实现的错误码 / 时序约束与组件级接口契约一致（项目已启用 `docs/interfaces.md` 时以该文件为准；未启用时以 `docs/component-design.md` 的 SOA 服务 / 接口章节为准）
- `CR3.4` 内部细节未通过公共符号泄漏

### Group CR4 - Memory & Resource

- `CR4.1` 内存模型符合 component-design（静态 / 动态、池化）
- `CR4.2` 句柄 / 文件 / 缓冲区获取与释放配对
- `CR4.3` 异常路径下无资源泄漏
- `CR4.4` 栈深度 / 大对象使用受控
- `CR4.5` 指针生命周期清晰，无悬垂

### Group CR5 - Concurrency & Real-time

- `CR5.1` 中断上下文中代码不调用阻塞 API
- `CR5.2` 锁 / 临界区遵循组件锁策略；无嵌套锁循环
- `CR5.3` 共享数据访问受保护，无竞态
- `CR5.4` 实时性约束（latency、deadline）已通过测试或注释 / 静态分析证据
- `CR5.5` 阻塞 / 非阻塞语义符合接口约定

### Group CR6 - Error Handling

- `CR6.1` 外部输入有校验；非法输入返回团队规定错误码
- `CR6.2` 错误码不被静默吞掉
- `CR6.3` 降级路径符合 component-design
- `CR6.4` ABI / API 兼容性策略落地（参数变更、错误码扩展）
- `CR6.5` 日志 / 诊断信息符合团队规范，不暴露敏感数据

### Group CR7 - Coding Standard & Static Analysis

- `CR7.1` 符合团队 C / C++ 编码规范（命名、注释、格式）
- `CR7.2` 符合 MISRA / CERT 子集（按 `AGENTS.md` 声明）
- `CR7.3` 编译告警：critical 项已闭环
- `CR7.4` 静态分析报告：critical / blocker 项已修 / 解释 / 抑制（带理由）
- `CR7.5` 无显式禁止用法（如 raw `new`/`delete`、动态分配在中断上下文）

### Group CR8 - Refactor Note & Health

- `CR8.1` Refactor Note 完整：Hat Discipline / In-task Cleanups / Architectural Conformance / Documented Debt / Escalation Triggers / Static Analysis Evidence
- `CR8.2` In-task Cleanups 使用 Fowler vocabulary 命名
- `CR8.3` Hat Discipline 守住，GREEN 步无 cleanup
- `CR8.4` 触碰范围内可见 architectural smell（god-class / cyclic-dep / layering-violation / leaky-abstraction）已识别 / 分类
- `CR8.5` 未触发 escalation-bypass（CR8 critical）：跨 ≥3 模块的结构性重构 / 改 ADR / 改组件边界 / 引入设计未声明的新抽象层均不得在 task 内悄悄做掉
- `CR8.6` 触碰文件 Boy Scout：离开时 clean code 健康度未退化

## Severity 分级

- `critical`：阻塞 completion gate（核心逻辑错、内存 / 并发 / 实时性 / 错误处理高风险、SOA 边界破坏、escalation-bypass、未解释 critical 静态分析项）
- `important`：completion 前应修（边界遗漏、Refactor Note 字段缺、Boy Scout 退化、smell 未分类）
- `minor`：建议改进（命名、注释、风格）

## Classification

- `USER-INPUT`：实现偏离设计且涉及业务取舍 → 上抛开发负责人
- `LLM-FIXABLE`：代码结构 / 错误处理 / 命名 / 边界 / 防御性检查 / Refactor Note 字段补全 / in-task 范围 smell → 由 `df-tdd-implementation` 回修
- `TEAM-EXPERT`：组件边界冲突 / SOA 接口冲突 / 实时性 / 内存模型 → 上抛模块架构师 / 资深嵌入式工程师

## Verdict 决策

| 评分 / findings 状态 | verdict |
|---|---|
| 8 维度均 ≥ 6、CR3/CR4/CR5/CR6 ≥ 7、CR8 主维度 ≥ 8 / 子维度 ≥ 6、无未解释 critical 静态分析项 | `通过` |
| findings 可 1-2 轮定向修订 | `需修改` |
| 核心逻辑错误 / 内存或并发安全漏洞 / SOA 边界破坏可在 task 内回修 | `阻塞`（内容） |
| 实质修改 ADR / 组件边界 / SOA 接口 / 跨 ≥3 模块结构性变更 / escalation-bypass / 上游证据冲突 | `阻塞`（workflow） + `reroute_via_router=true` |

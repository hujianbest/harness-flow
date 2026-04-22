# NFR Quality Attribute Scenarios（NFR QAS）参考

## Purpose

本参考为 `hf-specify` 提供结构化非功能需求（NFR）的最小契约：以 **ISO/IEC 25010** 作为质量模型分类，用 **Quality Attribute Scenarios (QAS)** 格式表达每条 NFR，让它在 spec 层面就具备可验证、可追溯的形状。

这解决了"NFR 章节写成 '性能要好、要安全、要好维护' 无阈值口号"的常见失败模式。

## One-Line Rule

**每条核心 NFR 都必须能被写成 QAS**：给出 source / stimulus / environment / response / response measure 五要素。

## ISO/IEC 25010 质量模型（最小分类）

| 维度 | 子维度（选） | 典型问题 |
|---|---|---|
| Functional Suitability | Correctness, Appropriateness | 功能正确性是否被独立验证 |
| Performance Efficiency | Time behavior, Resource utilization, Capacity | 响应时间、吞吐量、资源占用 |
| Compatibility | Interoperability, Co-existence | 与既有系统协作、并行运行 |
| Usability | Learnability, Operability, Accessibility | 是否可用、是否可达 |
| Reliability | Availability, Fault tolerance, Recoverability | 可用性目标、失败恢复时间 |
| Security | Confidentiality, Integrity, Authenticity, Non-repudiation, Accountability | 权限、审计、数据保护 |
| Maintainability | Modularity, Testability, Analyzability | 可改性、可测试性 |
| Portability | Adaptability, Installability | 平台迁移 / 安装 |

**不必覆盖所有维度**。每个 spec 根据当前轮范围挑选相关维度；与当前轮无关的显式标注「本轮不适用」。

## Quality Attribute Scenario（QAS）最小格式

每条核心 NFR 至少以下五要素（Bass / Clements / Kazman *Software Architecture in Practice*）：

| 要素 | 含义 | 约束 |
|---|---|---|
| **Stimulus Source** | 触发方（用户 / 外部系统 / 攻击者 / 监控告警） | 具体角色或系统，不写"用户" |
| **Stimulus** | 触发事件（请求 / 故障 / 攻击 / 负载 spike） | 可观察的具体事件 |
| **Environment** | 触发时系统所处状态（正常 / 降级 / 峰值 / 启动中） | 明确状态 |
| **Response** | 系统必须展现的响应行为 | 可观察、可判断 |
| **Response Measure** | 响应的量化阈值或判定准则 | 必须含阈值或可判定准则，不允许"足够快" |

### 最小示例（Performance）

```markdown
### NFR-002 审批查询响应时间

- 类别: Performance Efficiency / Time behavior
- 优先级: Must
- 来源: 用户请求“审批查询要足够快”；spec-bridge 中的"减少线下流转"

QAS:
- Stimulus Source: 登录态用户
- Stimulus: 查询某条审批的详情
- Environment: 系统处于日常负载（p99 QPS 100）
- Response: 返回完整审批详情视图
- Response Measure: p95 响应时间 ≤ 500ms；p99 ≤ 1s

Acceptance:
- Given 登录态用户；When 发起审批详情查询；Then p95 响应时间 ≤ 500ms（基于 7 天滚动窗口）。
```

### 最小示例（Reliability）

```markdown
### NFR-005 通知投递可靠性

- 类别: Reliability / Availability + Fault tolerance
- 优先级: Must

QAS:
- Stimulus Source: 下游通知渠道
- Stimulus: 下游 5xx 错误
- Environment: 单渠道短时降级，其他渠道正常
- Response: 切换到备用渠道并重试，期间不对用户暴露错误
- Response Measure: 单次事件下，端到端投递成功率 ≥ 99.5%，延迟 P95 ≤ 60s
```

### 最小示例（Security）

```markdown
### NFR-010 审计日志完整性

- 类别: Security / Accountability
- 优先级: Must

QAS:
- Stimulus Source: 任一用户
- Stimulus: 对审批进行状态变更
- Environment: 正常运行
- Response: 生成不可篡改的审计记录，覆盖 who / what / when / from
- Response Measure: 100% 状态变更在 5s 内落盘到审计存储；任意记录缺失 = 不通过
```

## 写法约定

- 每条核心 NFR 至少一个 QAS；若无法写出 QAS，说明 NFR 描述还不够具体，回到澄清
- `Response Measure` 必须含阈值（数字 / 百分比 / 时间 / 明确判定准则）
- `Environment` 必须写清系统状态（日常 / 峰值 / 降级 / 启动），不允许默认"正常"
- 如果一条 NFR 覆盖多个不同场景，拆成多条 QAS，不要塞进一条

## 与 hf-specify 其它 reference 的关系

- 单条需求的最小字段契约（ID / Type / Statement / Acceptance / Priority / Source）由 `requirement-authoring-contract.md` 约束；本参考**叠加**在 NFR 行上，补充 QAS 要素
- 每条 NFR 仍需提供 Acceptance（BDD Given/When/Then），通常从 Response + Response Measure 派生
- 粒度判断（INVEST）和延后判断仍按 `granularity-and-deferral.md`

## 下游衔接

- `hf-design` 在 `nfr-checklist.md` 中逐项承接 NFR，把 QAS 映射到具体模块 / 机制 / 验证方法
- `hf-design` 的 `Observability-by-Design` 章节（Phase 1 起引入）会把 Response Measure 转为 SLO / SLI / Alert 规则
- Phase 2 起的 `hf-perf-gate` / `hf-security-gate` / `hf-a11y-gate` / `hf-compliance-review` 等独立质量 gate，直接消费 spec 中的 QAS 作为验证目标

## 常见 Red Flag

- NFR 只写在概述段落，没有独立 ID 和 QAS
- `Response Measure` 写成"足够快""合理""行业水平"
- `Environment` 永远是"正常运行"，没考虑峰值 / 降级
- 一条 NFR 覆盖多个不同质量维度（性能 + 安全 + 可用性混在一起）
- QAS 与 Acceptance 矛盾（一个写 500ms，一个写 1s）
- ISO 25010 维度无关的内容被强行归类

## 最小签入条件

送 `hf-spec-review` 前，核心 NFR 至少满足：

- [ ] 已归类到 ISO 25010 对应维度
- [ ] 核心 NFR 有 QAS 五要素
- [ ] `Response Measure` 有阈值或可判定准则
- [ ] `Environment` 显式写出系统状态
- [ ] Acceptance 与 QAS 一致（不矛盾）

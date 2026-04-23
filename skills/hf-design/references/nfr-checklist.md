# NFR 落地检查清单（Phase 0：承接 Quality Attribute Scenarios）

非功能需求在设计文档中必须逐项确认落到哪个模块 / 机制，并承接规格层的 Quality Attribute Scenario（QAS）。

## 上游承接：Quality Attribute Scenarios

Phase 0 起，`hf-specify` 为每条核心 NFR 产出 QAS 五要素（Source / Stimulus / Environment / Response / Response Measure，见 `hf-specify/references/nfr-quality-attribute-scenarios.md`）。

`hf-design` 的职责是：**把每条 QAS 映射到具体模块 / 机制 / 验证方法**，而不是重新写一遍 NFR。

## 检查清单表格（Phase 0 扩展版）

| NFR ID | ISO 25010 维度 | 规格 QAS 摘要 (Source→Stimulus→Env→Response→Measure) | 设计承接模块 / 机制 | 可观测手段（logs/metrics/traces） | 验证方法 | 失败模式 & 缓解 | ADR 锚点 |
|---|---|---|---|---|---|---|---|
| NFR-001 | Performance | 登录态用户 / 查询审批 / 日常负载 / 返回视图 / p95 ≤ 500ms | 查询 API Handler + 缓存层 | metric: http_request_duration_seconds{path="/approval/:id"} | 压测脚本 + p95 SLI 监控 | 缓存失效雪崩 → 单飞 + 限流 | ADR-007 |
| NFR-005 | Reliability | 下游通知失败 / 单渠道降级 / 切换备用渠道 / 端到端 ≥ 99.5% | 通知编排器 + 通道 registry | metric: notification_delivery_total{channel,status}; trace on retry | 注入故障 + 回归监控 | 备用渠道同时挂掉 → 兜底队列 | ADR-012 |

若某类 NFR 在当前规格中无要求，显式标注"不适用"并简短说明原因；不允许静默省略。

## 承接规则

### 1. 模块 / 机制具体化

- "设计承接模块 / 机制" 不允许写"整个系统"或"全局考虑"，必须能回指 design 文档中某个模块 / 接口 / 组件
- 跨模块关注点（例如 tracing、限流）应写为独立横切机制，而不是把所有 NFR 都往该机制上堆

### 2. 可观测手段

每条关键 NFR 的 Response Measure 必须有对应 observability 手段：

- **logs**：结构化事件 + 级别 + 关键字段
- **metrics**：指标名 + 标签 + 预期聚合方式（p50 / p95 / p99 / rate / count）
- **traces**：跨服务调用的关键 span / attributes（若适用）

Phase 1 将在 design 中引入独立 `Observability-by-Design` 章节；Phase 0 已经要求"每条核心 NFR 至少写出 observability 手段"。

### 3. 验证方法

- 单元 / 集成测试能验证的 → 写明测试类型 + 关键 assertion 目标
- 需要负载 / 安全 / 可访问性测试的 → 写明验证工具（k6 / Locust / axe / Lighthouse / SAST 等）
- Phase 2 起会有独立 `hf-perf-gate` / `hf-security-gate` / `hf-a11y-gate` 消费这些入口

### 4. 失败模式 & 缓解

- 参考 `failure-modes.md` 的四层失败框架（Crash / Hang / Wrong / Silent）
- 缓解必须写到具体机制，不允许"有重试"这种无细节承诺

### 5. ADR 锚点

每条涉及关键技术决策的 NFR 承接应能回指一条 ADR。

## 常见 NFR 关注点

### 性能（Performance Efficiency）

- 响应时间目标（p50 / p95 / p99）
- 吞吐量要求（RPS / TPS）
- 资源消耗限制（CPU / memory / connection pool）
- 冷启动 / 热启动差异

### 可靠性（Reliability）

- 可用性目标（SLO %）
- 数据持久性要求
- 故障恢复时间（RTO / RPO）
- 降级策略（fallback / circuit breaker / bulkhead）

### 安全性（Security）

- 认证与授权机制
- 数据保护要求（传输 / 存储加密）
- 攻击面分析（触发 STRIDE list，见 `threat-model-stride.md`）
- 审计日志完整性与不可篡改性

### 可维护性（Maintainability）

- 模块边界与依赖方向
- 测试覆盖率目标
- 可分析性（日志 / 错误码设计）
- 文档要求与 Ubiquitous Language 一致性

### 兼容性（Compatibility）

- 向后兼容承诺
- 平台 / 运行时约束
- 协议和接口稳定性
- 数据格式演进策略

### 可用性（Usability）

- 关键任务完成率 / 时间
- 错误提示质量
- 可访问性（WCAG 级别）
- 国际化 / 本地化

## 常见 Red Flag

- NFR 只在概述段落出现，没有条目化承接
- 一条 NFR 被"设计里自然考虑了"这种话带过
- 承接模块写"整个系统"
- Response Measure 没有对应 observability 手段
- 验证方法全写"单元测试覆盖"而不区分类型
- NFR 与 ADR 冲突，但未在 ADR 的 consequences 中提及
- STRIDE 应激活却被跳过

## 最小签入条件

送 `hf-design-review` 前：

- [ ] 每条核心 NFR 已在上表中有独立行
- [ ] 设计承接模块 / 机制具体到可回指 design 正文
- [ ] 至少一条可观测手段（logs / metrics / traces）
- [ ] 验证方法明确（测试类型 / 工具 / SLI 监控）
- [ ] 失败模式覆盖；关键缓解有对应机制
- [ ] 关键 NFR 决策有 ADR 锚点
- [ ] 若 Security NFR 激活或存在关键信任边界，STRIDE list 已产出（见 `threat-model-stride.md`）

## 衔接

- 规格层 QAS 最小契约见 `hf-specify/references/nfr-quality-attribute-scenarios.md`
- 失败模式分析见 `failure-modes.md`
- 轻量威胁建模见 `threat-model-stride.md`
- 关键决策记录见 `adr-template.md`

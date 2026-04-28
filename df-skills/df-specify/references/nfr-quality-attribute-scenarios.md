# df NFR Quality Attribute Scenarios（NFR QAS）

> 配套 `df-specify/SKILL.md`。规定 `features/<id>/requirement.md` 中**每条核心 NFR** 的最小契约：以 ISO/IEC 25010 作为质量模型分类，用 Quality Attribute Scenarios（QAS）格式表达每条 NFR，让它在 spec 层面就具备可验证、可追溯的形状。
>
> 这解决了「NFR 章节写成 '性能要好、要安全、要好维护' 无阈值口号」的常见失败模式——这种 NFR 进入 AR 实现设计 / TDD 后无法生成可执行的 RED 用例。

## One-Line Rule

**每条核心 NFR 都必须能写成 QAS**：给出 Stimulus Source / Stimulus / Environment / Response / Response Measure 五要素。如果写不出来 → 说明 NFR 描述还不够具体，回 Open Questions 找需求负责人 / 模块架构师补阈值。

## ISO/IEC 25010 质量模型（嵌入式优先）

下表按 df 主场景的常见相关性排序；嵌入式 / 实时 / 控制系统的 NFR 大多落在前 4 行。

| 维度 | 子维度（选） | 嵌入式典型问题 |
|---|---|---|
| **Performance Efficiency** | Time behavior, Resource utilization, Capacity | 控制周期 latency、jitter、CPU / 内存占用、栈深度、消息队列容量 |
| **Reliability** | Availability, Fault tolerance, Recoverability | 看门狗、故障安全、降级模式、软复位行为、失败恢复时间 |
| **Maintainability** | Modularity, Testability, Analyzability | 组件边界稳定性、可单测性、日志可追溯性、静态分析友好度 |
| **Security** | Confidentiality, Integrity, Authenticity, Non-repudiation, Accountability | 配置完整性校验、敏感数据保护、安全启动、签名校验 |
| Compatibility | Interoperability, Co-existence | 跨版本 / 跨平台 ABI / API 兼容、与既有协议栈共存 |
| Functional Suitability | Correctness, Appropriateness | 功能正确性是否被独立验证（一般通过 acceptance 而非 NFR 表达） |
| Usability | Operability, Accessibility | 在嵌入式 CLI / HMI 场景下相关；纯固件较少 |
| Portability | Adaptability, Installability | 跨目标平台移植；OTA 升级 |

**不必覆盖所有维度**。每个 spec 按本 work item 的范围挑选相关维度；不相关的维度**显式标注**「本 work item 不适用」，不要默认省略。

## Quality Attribute Scenario（QAS）最小格式

每条核心 NFR 至少含五要素（Bass / Clements / Kazman *Software Architecture in Practice*）：

| 要素 | 含义 | 约束 |
|---|---|---|
| **Stimulus Source** | 触发方（用户 / 上游组件 / 外部系统 / 中断 / 监控告警 / 攻击者） | 具体角色或源头，不写「用户」 |
| **Stimulus** | 触发事件（请求 / 中断 / 故障 / 负载 spike / 配置变更） | 可观察的具体事件 |
| **Environment** | 触发时系统所处状态（正常 / 降级 / 启动 / 中断上下文 / 高负载） | 必须明确状态，不允许默认「正常」 |
| **Response** | 系统必须展现的响应行为 | 可观察、可判断 |
| **Response Measure** | 响应的量化阈值或判定准则 | 必须含阈值（数字 / 百分比 / 时间 / 明确判定准则）；不允许「足够快」 |

## 嵌入式 NFR 改写示例

下面 6 个示例分别对应 `requirement-rows-contract.md` 嵌入式 NFR 写法表中的 6 个维度，把简短描述展开为完整 QAS。

### 实时性（Performance Efficiency / Time behavior）

```markdown
### NFR-001 ModeSwitch 关键路径延迟
- 类别: Performance Efficiency / Time behavior
- 优先级: Must
- 来源: SR-1234 § 4.1；目标平台 X 控制周期 10 ms

QAS:
- Stimulus Source: 子系统 Y 的调度器
- Stimulus: 调用 Service.SetMode(NORMAL)
- Environment: 目标平台 X 在常规负载下，控制周期 = 10 ms，无未决高优先级中断
- Response: 在下一控制周期内完成模式切换并发出 ModeChanged
- Response Measure: 95th percentile 切换延迟 ≤ 5 ms；100% 在 10 ms 控制周期内完成

Acceptance:
- Given 组件 X 在 NORMAL 调度上下文；When 1000 次连续 SetMode；Then 95th ≤ 5 ms 且 max ≤ 10 ms（可由 latency 直方图证据验证）。
```

### 内存（Performance Efficiency / Resource utilization）

```markdown
### NFR-002 ModeService 静态内存预算
- 类别: Performance Efficiency / Resource utilization
- 优先级: Must

QAS:
- Stimulus Source: 编译期链接器 / 启动期分配器
- Stimulus: 链接生成镜像；运行期初始化 ModeService
- Environment: 目标平台 X 链接配置 LinkerCfg.A；ROM/RAM 限制按团队基线
- Response: ModeService 不引入超过预算的静态内存，且不使用动态分配
- Response Measure: ModeService 引入的 .data + .bss 段 ≤ 4 KiB；malloc / new 调用次数 = 0（由静态分析与 size 工具证据验证）
```

### 并发（Performance Efficiency / Time behavior + Reliability）

```markdown
### NFR-003 中断上下文中的写入约束
- 类别: Performance Efficiency / Time behavior + Reliability / Fault tolerance
- 优先级: Must

QAS:
- Stimulus Source: 硬件中断（TIMER_ISR）
- Stimulus: 中断处理需要写入 ModeChanged 事件队列
- Environment: 中断上下文，禁止阻塞 API 调用
- Response: 把 ModeChanged 事件以非阻塞方式入队，由后续任务上下文消费
- Response Measure: 100% 入队成功（队列未满时）；中断上下文执行时间 ≤ 10 µs；不调用任何阻塞 API（由静态分析白名单证据验证）
```

### 资源生命周期（Reliability / Fault tolerance）

```markdown
### NFR-004 句柄获取与释放配对
- 类别: Reliability / Fault tolerance
- 优先级: Must

QAS:
- Stimulus Source: 任何调用 ModeService 的客户端
- Stimulus: 在 SetMode 路径上获取了内部资源句柄（例如配置缓冲区）
- Environment: 含异常 / 错误返回路径
- Response: 所有获取的句柄在退出函数前释放，不论返回成功还是错误
- Response Measure: 静态分析（leak detector）报告 0 条 ModeService 路径上的句柄泄漏；fuzz 测试 24 小时无新泄漏
```

### 错误处理（Reliability / Fault tolerance + Functional Suitability）

```markdown
### NFR-005 非法输入校验
- 类别: Reliability / Fault tolerance
- 优先级: Must

QAS:
- Stimulus Source: 子系统 Y 或外部调用方
- Stimulus: 调用 SetMode(mode)，mode ∉ {NORMAL, SAFE}
- Environment: 任意运行状态
- Response: 返回 ERR_INVALID_ARG，不更新内部状态，不发出 ModeChanged
- Response Measure: 100% 非法输入返回 ERR_INVALID_ARG（含 fuzz 测试覆盖）；mode 字段在错误返回后保持原值
```

### 安全（Security / Integrity）

```markdown
### NFR-006 配置完整性校验
- 类别: Security / Integrity
- 优先级: Must

QAS:
- Stimulus Source: OTA / 配置加载器 / 启动时配置读取
- Stimulus: 加载新的 ModeService 配置块
- Environment: 启动期或运行期配置热更新
- Response: 校验 CRC / 签名；通过则启用，失败则保留旧配置并上报
- Response Measure: 100% 配置块在启用前通过完整性校验；失败时上报事件 ConfigVerifyFailed 在 100 ms 内被监控通道收到
```

## SR 视角的 NFR

SR work item 的 NFR 通常是**子系统级目标**：

- `Stimulus Source` / `Environment` 在子系统层（例：「子系统 Y 的调度器」「子系统启动期」）
- `Response` 是子系统级行为（例：「子系统 Y 必须在 200 ms 内把请求路由到对应组件」）
- `Response Measure` 仍需可量化，但通常是端到端目标，不绑定具体组件实现细节
- 当 SR 拆出候选 AR 后，AR 工作项可以把同一个 NFR 下沉为更细粒度的组件级 QAS

示例：

```markdown
### NFR-S-001（SR）子系统级模式切换端到端延迟
- 类别: Performance Efficiency / Time behavior
- 优先级: Must
- 来源: SR-1234 § 4.1（子系统级 SLO）

QAS:
- Stimulus Source: 子系统 Y 的外部消费者
- Stimulus: 发起 Subsystem.SetMode(NORMAL)
- Environment: 子系统 Y 处于 ready 状态、所有受影响组件均就绪
- Response: 子系统 Y 把请求路由到对应组件、收到组件确认、返回成功
- Response Measure: 端到端 95th ≤ 50 ms；100% ≤ 200 ms

# 拆出 AR 后，AR-12345 / AR-12346 各自把这一目标下沉为组件级 NFR：
# - AR-12345（组件 X）: 95th ≤ 5 ms（NFR-001 上面）
# - AR-12346（组件 Z）: 95th ≤ 10 ms
```

## 与其他 reference 的关系

- 单条 NFR 的最小字段（ID / Statement / Acceptance / Priority / Source）：`requirement-rows-contract.md`
- NFR row 是否过大、是否应拆分：`granularity-and-split.md`
- spec-review 对核心 NFR 的检查（必须有 QAS、Response Measure 阈值、Acceptance 与 QAS 一致）：`../df-spec-review/references/spec-review-rubric.md`

## 写法约定

- 每条核心 NFR 至少 1 个 QAS；若无法写出 QAS → 不够具体，回澄清
- `Response Measure` 必须含阈值（数字 / 百分比 / 时间 / 明确判定准则）
- `Environment` 必须写清系统状态（日常 / 峰值 / 降级 / 启动 / 中断上下文），不允许默认「正常」
- 一条 NFR 覆盖多个不同质量维度时，**拆成多条 QAS**，不要塞进一条
- Acceptance（BDD Given / When / Then）通常从 Response + Response Measure 派生，必须与 QAS 一致

## 与下游衔接

- `df-ar-design` 的测试设计章节会把 QAS 映射到具体 unit / integration / simulation 测试用例，并写入「嵌入式风险覆盖矩阵」
- `df-tdd-implementation` 把 Response Measure 转为 RED 步的判定（例如 latency 直方图、size 工具输出、leak detector 报告）
- `df-test-checker` 在 `TC4 Embedded Risk Coverage` 维度反向核对：每条 NFR 是否被 `embedded-risk` 用例覆盖
- `df-code-review` 在 `CR4 Memory & Resource Lifecycle` / `CR5 Concurrency & Real-time` / `CR6 Error Handling & Defensive Design` 维度反向核对实现是否符合 QAS Response Measure

## Common Red Flags

- NFR 只写在概述段落，没有独立 ID 和 QAS
- `Response Measure` 写成「足够快」「合理」「行业水平」「按经验」
- `Environment` 永远是「正常运行」，没考虑峰值 / 降级 / 中断 / 启动
- 一条 NFR 覆盖多个不同质量维度（性能 + 安全 + 可用性混在一起）
- QAS 与 Acceptance 矛盾（一个写 5 ms，另一个写 10 ms）
- ISO 25010 维度无关的内容被强行归类
- SR 的 NFR 直接写到组件级 QAS（应在子系统层；下沉到组件由拆出的 AR 完成）

## 最小签入条件

送 `df-spec-review` 前，每条核心 NFR 至少满足：

- [ ] 已归类到 ISO/IEC 25010 维度
- [ ] 含 QAS 五要素
- [ ] `Response Measure` 含阈值或可判定准则
- [ ] `Environment` 显式写出系统状态
- [ ] Acceptance（BDD）与 QAS 一致
- [ ] AR 工作项的 NFR 在组件级；SR 工作项的 NFR 在子系统级（不混层）

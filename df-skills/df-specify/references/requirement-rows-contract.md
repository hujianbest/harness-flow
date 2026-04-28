# df Requirement Rows Contract

> 配套 `df-specify/SKILL.md`。规定 `features/<id>/requirement.md` 的需求条目最小字段、嵌入式 NFR 写法和分类。

## 类别（六分类）

| 类别 | 前缀 | 描述 |
|---|---|---|
| Functional Requirement | `FR-` | 功能需求，可观察的系统行为 |
| Non-Functional Requirement | `NFR-` | 非功能 / 质量需求（实时性、内存、并发、安全等） |
| Constraint | `CON-` | 硬性约束（编译条件、目标平台、内核版本、ABI 兼容） |
| Interface Requirement | `IFR-` | 接口需求（SOA 服务契约、协议、数据格式、错误码） |
| Assumption | `ASM-` | 假设；失效会改变规格的事实 |
| Exclusion | `EXC-` | 显式排除项 |

DTS 规格不必填写所有类别；至少应有 FR（或 IFR / CON）描述被破坏的行为，以及 NFR（若涉及实时性 / 内存）。

## 行最小字段

| 字段 | 是否必填 | 说明 |
|---|---|---|
| `ID` | 必填 | 例 `FR-001` |
| `Statement` | 必填 | 可观察、可判断的语句 |
| `Acceptance` | FR / NFR / IFR 必填 | 可验证的判定条件 |
| `Priority` | 推荐 | 团队若使用 MoSCoW 或等价分级，按团队约定 |
| `Source / Trace Anchor` | 必填 | 指向 IR / SR / AR / DTS 编号或具体输入文档锚点 |
| `Component Impact` | AR / DTS / CHANGE 必填（FR / IFR / NFR） | `none` / `interface` / `dependency` / `state-machine` / `runtime-behavior` |
| `Affected Components` | SR 必填（FR / IFR / NFR） | SR 视角下受影响的组件清单（一个 row 可能影响多个组件） |
| `Notes` | 可选 | 例如风险点、与其他 row 的关系 |

按 work item 类型：

- AR / DTS / CHANGE：使用 `Component Impact`；不为 `none` 时，规格必须在 `Component Impact Assessment` 章节显式说明，并由 `df-workflow-router` 决定是否升级 `component-impact` profile。
- SR：使用 `Affected Components`；列出本 row 影响的所有组件（一条 SR row 通常跨多个组件）；规格必须在 `Affected Components` / `AR Breakdown Candidates` / `Component Design Impact` 三个章节中分别消费这些字段。

## SR-only 章节字段

SR 规格在 row 表之外，必须维护以下章节级字段。它们不是 row 的一部分，但 reviewer 会把它们跟 row 表反向核对。

### Affected Components

| 字段 | 说明 |
|---|---|
| `Component` | 受影响组件名 |
| `Modification Surface` | `interface` / `dependency` / `state-machine` / `runtime-behavior` / `implementation` 中的一个或多个 |
| `Covers Rows` | 引用本 SR row 表中的若干 row ID |
| `Owning Module Architect` | 该组件的模块架构师 |
| `Component Design Impact` | `unchanged` / `revise-section` / `new-component`；为 `revise-section` / `new-component` 时本 SR 应在 `Component Design Impact` 章节展开 |

### AR Breakdown Candidates

候选 AR 拆分清单，每条至少含：

| 字段 | 说明 |
|---|---|
| `Candidate ID` | 例 `CAR-001`（SR-flow 内部编号；新建 AR work item 时由需求负责人分配真正的 AR ID） |
| `Scope` | 1-2 句话总结候选 AR 的范围 |
| `Owning Component` | 候选 AR 的所属组件（必须唯一） |
| `Covers SR Rows` | 引用本 SR row 表中的若干 row ID |
| `Priority Hint` | 团队约定的优先级提示（不替需求负责人定优先级） |
| `Estimated Complexity` | `S` / `M` / `L`（不替开发负责人估算） |
| `Hand-off Owner` | 候选 AR 应交给哪位开发负责人 / 团队 |
| `Notes` | 例如依赖关系、与其他候选的拆分边界 |

`AR Breakdown Candidates` 草稿期可为空；`df-spec-review` 通过后到 `df-finalize` analysis closeout 之前应定稿。如果 SR 显式声明「无可拆分 AR」（仅做组件设计修订或文档级修订），需在 `Notes` 中写明并由需求负责人确认。

### Component Design Impact

仅当本 SR 触发 `df-component-design`（修订组件实现设计）时填写，含：

- 受影响 `docs/component-design.md` 章节清单
- 修订方向概述
- 是否同步触发可选子资产（`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`）变化

## Statement Patterns（EARS — Mavin et al., REFSQ 2009）

如果项目未声明固定句式，默认使用 EARS（Easy Approach to Requirements Syntax）的中文等价模式：

| 模式 | 句式 | 示例（AR / 实现子街区） | 示例（SR / 需求分析子街区） |
|---|---|---|---|
| 常驻行为 | `<主体> 必须 <持续成立的能力或约束>` | 组件 X 必须始终保持运行模式记录与 ModeChanged 事件流一致 | 子系统 Y 必须始终对外暴露 ModeService 接口 |
| 事件触发 | `当 <触发条件> 时，<主体> 必须 <可观察结果>` | 当组件 X 收到 SetMode(NORMAL) 时，必须在下一控制周期切换到 NORMAL 并发出 ModeChanged | 当外部子系统请求模式切换时，子系统 Y 必须把请求路由到对应组件 |
| 状态约束 | `在 <状态 / 角色 / 前置条件> 下，<主体> 必须 <行为结果>` | 在 SAFE 状态下，组件 X 必须拒绝任何写配置请求 | 在子系统启动期间，子系统 Y 必须缓存请求直到所有组件就绪 |
| 异常 / 负路径 | `如果 <异常条件>，<主体> 必须 <保护 / 反馈 / 恢复行为>` | 如果输入 mode ∉ {NORMAL, SAFE}，组件 X 必须返回 ERR_INVALID_ARG 且不更新内部状态 | 如果某个受影响组件初始化失败，子系统 Y 必须回退到 SAFE 模式并上报 |
| 可选 / 配置 | `在启用 <策略 / 配置> 时，<主体> 必须 <行为结果>` | 在启用 PERSIST_MODE_HISTORY 时，组件 X 必须把每次 ModeChanged 写入 NVRAM | 在启用 SUBSYSTEM_DEGRADED_LOG 时，子系统 Y 必须输出降级原因事件 |

句式约束：

- **AR / DTS / CHANGE row** 的主体一般是「本组件 / 该模块 / 该函数路径」；不写「系统」这种无主体被动表达
- **SR row** 的主体一般是「子系统 / 子系统中的某个服务」；通常**不**指定具体组件接口字段（那些细节留给 AR 拆出后填）
- 不写实现细节（接口签名、数据结构、库名、并发原语）；这些属于设计

## Acceptance Criteria Rules（BDD — Dan North, 2006）

验收标准默认采用 BDD 的 Given / When / Then 格式，建立需求到测试 / 验证证据的可追溯桥梁。

通用规则：

- 每条核心 `FR` 至少一个**正向**验收标准
- 关键失败路径、边界输入、并发冲突、超时 / 延迟 / 嵌入式风险，至少补一条对应验收口径
- 验收能形成明确通过 / 不通过判断；不写「用户体验良好」「处理足够快」等无阈值表达
- 一个验收标准只验证一个主要行为；同一条标准同时覆盖多个独立行为 → 回粒度检查

按 work item 类型的强度差异：

| 类型 | Acceptance 强度 | 备注 |
|---|---|---|
| AR / DTS / CHANGE | **可测试**（testable acceptance）：每条 acceptance 要能直接落成 RED 用例（与 AR 实现设计中的测试设计章节双向锚点） | 可测试性是 `df-ar-design` / `df-tdd-implementation` 的硬上游输入 |
| SR | **可观察**（observable acceptance）：表达子系统级行为是否成立的判定准则；不要求落到单条单元测试 | SR 的 acceptance 通常会在 AR 拆出后下沉为更细粒度的 testable acceptance |

示例（AR row）：

```markdown
### FR-001 NORMAL 模式切换
- Acceptance:
  - Given 组件 X 当前 mode=SAFE；When 调用 SetMode(NORMAL)；Then 下一控制周期内 ModeChanged.event=NORMAL，返回 OK。
  - Given 组件 X 当前 mode=SAFE；When 调用 SetMode(INVALID)；Then 返回 ERR_INVALID_ARG，mode 仍为 SAFE。
```

示例（SR row）：

```markdown
### FR-S-002 子系统级模式切换路由
- Acceptance:
  - Given 子系统 Y 已就绪；When 外部 Subsystem.SetMode(NORMAL)；Then 子系统 Y 在 200 ms 内把请求路由到 ModeService 并返回 OK，受影响组件均切换到 NORMAL。
  - Given 受影响组件中至少一个初始化失败；When 外部请求模式切换；Then 子系统 Y 回退到 SAFE 并返回 ERR_DEGRADED。
```

## Priority Rules（MoSCoW — DSDM Consortium, 1994 — 或团队等价）

- 若 `AGENTS.md` / 项目模板声明了固定优先级体系，**优先**使用该体系
- 没有显式体系时，默认使用 MoSCoW 四级：`Must` / `Should` / `Could` / `Won't`
- 优先级是**逐条 row 的属性**，不是整份规格的总体评价
- 真实需要后续接力的 row（候选 AR）：在 SR 的 `AR Breakdown Candidates` 章节中显式列出，**不**埋在 prose；df 不维护跨工作项 deferred backlog
- 多条 row 都声称最高优先级且互相冲突 → 回需求负责人，不自行拍板

## Source / Trace Anchor 写法

每个核心需求必须能回指：

- 上游 IR / SR / AR 编号（团队系统中的稳定 ID）
- 团队接受的需求输入文档（带版本锚点 / 修订号）
- DTS 引用具体缺陷单编号 + 复现步骤所在文件
- review finding 锚点（例 `features/<id>/reviews/spec-review.md#finding-3`）
- 外部约束（法规 / 合同 / 协议规范 / 兼容要求 / `AGENTS.md` 中已声明的约束）

不接受 「用户在某次会议口头要求」；这种锚点会在缺陷追溯时消失。如果一条 row 来自多个来源，先写主要来源，再补次级来源。

## Brainstorming Notes Normalization

若输入是 brainstorming notes、会议散点记录或用户口述碎片，**不要**直接把原文逐条改写成 `FR` / `NFR`。先做一次归一化：

| 原始内容类型 | 正确落点 | 不应直接写成 |
|---|---|---|
| 已确认的业务行为 | `FR` | 夹带接口名 / 服务名 / 数据结构的「伪需求」 |
| 可判定的质量门槛 | `NFR`（含 QAS，详见 `nfr-quality-attribute-scenarios.md`） | 「体验更好」「性能高一点」无阈值口号 |
| 嵌入式硬性限制（目标平台 / 内核 / ABI / 编译条件） | `CON` | 没有来源锚点的猜测性限制 |
| 外部接口 / 协议 / 跨系统契约 | `IFR` | 内部接口（应归入设计阶段） |
| 团队假设、待确认说法 | `ASM` 或 Open Questions | 被伪装成已确认需求 |
| 当前轮不做但真实存在 | AR：`EXC` 或拆出新 work item；SR：`AR Breakdown Candidates` | 只埋在 prose 里的「以后再做」 |
| 接口签名 / 数据结构 / 重试次数 / 服务划分 | 设计输入或 Open Questions | `FR` / `NFR` 正文 |

最小归一化目标（在写 row 前必须分清）：

1. 「确认过的事实」 vs「还未确认的想法」
2. 「业务 / 子系统意图」 vs「实现细节」
3. 「当前 work item 必须做」 vs「后续候选 work item」（SR 写到 candidates；AR 应直接拆新 work item）

如果做不到这三步，还没到正式 requirement rows 的时机，回步骤 3 继续 Socratic Elicitation。

## 嵌入式 NFR 写法

NFR 若涉及嵌入式特性，必须写成可判定条件。每条核心 NFR 应能用 QAS 五要素表达，详见 `nfr-quality-attribute-scenarios.md`。常见维度速查：

| 维度 | 写法示例（描述层，不写实现） |
|---|---|
| 实时性 | "本 AR 的关键路径在目标平台 X 上响应延迟应 ≤ 5 ms（95th percentile）" |
| 内存 | "本 AR 引入的静态内存占用 ≤ 4 KiB；不允许使用动态分配" |
| 并发 | "本 AR 在中断上下文中执行的代码不得调用阻塞 API" |
| 资源生命周期 | "句柄获取与释放必须配对，异常路径下无泄漏" |
| 错误处理 | "外部输入校验失败时返回 ERR_INVALID_ARG，不得继续执行" |
| 安全 | "敏感配置项必须经过完整性校验后才生效" |

**禁止**：

- "足够快"、"性能合理"、"低内存"等模糊词
- 直接写实现选择（"用环形缓冲区"、"用 mutex"）；这些属于 AR 实现设计

无法量化的 NFR → 列入 Open Questions，回需求负责人 / 模块架构师补阈值。

## Source / Trace Anchor 写法

每个核心需求必须能回指：

- 上游 IR / SR / AR 编号（团队系统中的稳定 ID）
- 或团队接受的需求输入文档（带版本锚点 / 修订号）
- DTS 引用具体缺陷单编号 + 复现步骤所在文件

不接受 "用户在某次会议口头要求"；这种锚点会在缺陷追溯时消失。

## Open Questions 分类

每个开放问题至少含：

- `ID`（例 `OQ-001`）
- `Statement`
- `Type`：`blocking` / `non-blocking`
- `Owner`：`需求负责人` / `模块架构师` / `开发负责人` / 具体角色
- `Trigger`：什么决策被这个开放问题阻塞

`blocking` 问题在 `df-spec-review` 通过前必须闭合或显式回到需求负责人；reviewer 不得放过 `blocking` 问题给出 `通过`。

## 反例

```text
❌ FR-001: 系统应该处理用户请求
❌ NFR-001: 性能要好
❌ FR-002: 增加一个新模块来处理协议解析（混入实现）
```

```text
✅ FR-001: 当组件 X 收到 Service.SetMode 请求且参数 mode ∈ {NORMAL, SAFE} 时，
     应在下一控制周期内将运行模式更新为请求值，并通过 ModeChanged 事件通知订阅者。
   Acceptance:
     - 调用 Service.SetMode(NORMAL) 后，下一控制周期内 ModeChanged.event = NORMAL；
     - 参数 mode ∉ {NORMAL, SAFE} 时返回 ERR_INVALID_ARG，不更新内部状态。
   Source: SR-1234 § 3.2、AR-56789 描述
   Component Impact: interface（修改 Service.SetMode 错误码集）
```

## Common Failure Modes

- 只有编号和正文，没有 `Priority`
- 只写「来源于用户需求」而没有更具体的锚点
- 一条 `FR` 打包多个角色 / 多个独立行为 / 多个发布轮次（违反 INVEST `Small` + `Independent`，详见 `granularity-and-split.md`）
- 验收标准只是把需求正文重复一遍，没有新增判定口径
- 在需求陈述里夹带接口名 / 数据结构 / 重试次数 / 服务名等设计决策
- NFR 不能写成 QAS 五要素却仍尝试 `通过`（详见 `nfr-quality-attribute-scenarios.md`）
- AR row 的 Acceptance 不可直接落成 RED 用例（应回写更可测试的判定条件）
- SR row 试图指定具体接口字段或实现选择（应抽到子系统级行为，把细节留给 AR 拆出后填）

## 与其他 reference 的关系

- 行最小字段、句式、acceptance、priority、anchor、归一化、failure modes：本文
- 一条 row 是否过大、是否应拆 / 应作为 SR 候选 AR 拆出：`granularity-and-split.md`
- 核心 NFR 的 QAS 五要素与 ISO/IEC 25010 分类：`nfr-quality-attribute-scenarios.md`
- spec review 维度与 finding 分类：`../df-spec-review/references/spec-review-rubric.md`

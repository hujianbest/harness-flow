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
| `Component Impact` | 必填（FR / IFR / NFR） | `none` / `interface` / `dependency` / `state-machine` / `runtime-behavior` |
| `Notes` | 可选 | 例如风险点、与其他 row 的关系 |

`Component Impact` 不为 `none` 时，规格必须在 `Component Impact Assessment` 章节显式说明，并由 `df-workflow-router` 决定是否升级 component-impact profile。

## 嵌入式 NFR 写法

NFR 若涉及嵌入式特性，必须写成可判定条件。常见维度：

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

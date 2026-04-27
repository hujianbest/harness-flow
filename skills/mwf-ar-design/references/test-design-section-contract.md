# mwf AR Test Design Section Contract

> 配套 `mwf-ar-design/SKILL.md`。规定 AR 实现设计中**测试设计章节**的最小字段、嵌入式风险覆盖矩阵和与 requirement.md 的双向锚点。

mwf 不维护独立 `test-design.md`；测试设计是 AR 实现设计的章节。这是 mwf-principles 的硬约定。

## 测试用例最小字段

| 字段 | 是否必填 | 说明 |
|---|---|---|
| `Case ID` | 必填 | 例 `TC-001`；在本 AR 设计中唯一 |
| `Covers Requirement` | 必填 | 回指 requirement.md 的 row ID（如 `FR-002`、`NFR-001`、`IFR-003`） |
| `Test Level` | 必填 | `unit` / `integration` / `simulation` |
| `Coverage Type` | 必填 | `happy` / `boundary` / `exception` / `embedded-risk` |
| `Preconditions` | 必填 | 触发用例的状态 / 输入 |
| `Steps / Trigger` | 必填 | 用例如何触发 |
| `Expected Result` | 必填 | 可被 RED 步骤验证的失败条件 + GREEN 步骤验证的通过条件 |
| `Mocks / Stubs / Sim` | 必填 | 哪些依赖被 mock / stub / 仿真，边界为何 |
| `RED / GREEN Evidence Plan` | 必填 | 哪些命令、日志、静态分析结果在 TDD 时必须保留 |
| `Notes` | 可选 | 已知风险、潜在不稳定因素 |

每个核心 requirement row 至少被一个用例覆盖；NFR 必须有 `embedded-risk` 类型用例。

## 嵌入式风险覆盖矩阵

测试设计章节必须显式给出风险覆盖矩阵：

| 嵌入式风险维度 | 覆盖该维度的 Case ID |
|---|---|
| 内存（边界、池化、栈溢出） |  |
| 并发（中断上下文、临界区、竞态） |  |
| 实时性（截止时间、调度、节拍） |  |
| 资源生命周期（句柄、文件、缓冲区） |  |
| 错误处理（输入校验、降级、恢复） |  |
| ABI / API 兼容（跨版本、跨平台） |  |

任一维度若被本 AR 触及但矩阵留空 → review 时视为 critical finding。

## RED / GREEN 证据要求

测试设计章节应说明 TDD 期间需要保留的证据，以保证后续 `mwf-test-checker` 可独立审查：

- **RED 证据**：用例首次失败时的命令、退出码、失败摘要、为什么预期失败
- **GREEN 证据**：用例通过时的命令、通过摘要、关键结果、新鲜度锚点（commit / build ID）
- **REFACTOR 证据**：若 REFACTOR 步触发，回写哪些清理动作（Fowler vocabulary）+ 全套测试再次通过的证据
- **保留位置**：`features/<id>/evidence/unit/`、`features/<id>/evidence/integration/`、`features/<id>/evidence/static-analysis/`、`features/<id>/evidence/build/`

## Mock / Stub / Sim 规则

- mock 限定在真正的边界（外部依赖、硬件、协议栈、跨组件 SOA 调用）
- 内部纯逻辑不允许 mock
- 仿真（如 SIL / 协议仿真）必须说明仿真器版本与配置
- 不允许「测试专用方法」（test-only public method）
- 不允许 mock 自己模块的私有函数

## 与 requirement.md 的双向锚点

- 每个测试用例必须回指 `Covers Requirement = <row ID>`
- requirement.md 的核心 row 在 review 时反向核对至少一个用例覆盖
- 嵌入式 NFR 必须有 `embedded-risk` 用例覆盖
- 缺锚点 → spec-review / ar-design-review 视为 critical finding

## 反例

```text
❌ TC-001: 验证模块工作正常
❌ TC-002: 测试错误处理
```

```text
✅ TC-001: 覆盖 FR-001（NORMAL 模式切换）
   Test Level: unit
   Coverage Type: happy
   Preconditions: 当前模式 = SAFE
   Steps: 调用 Service.SetMode(NORMAL)
   Expected: 下一控制周期内 ModeChanged.event = NORMAL；返回 OK
   Mocks: ControlScheduler 用 fake；NotificationBus 用 stub 捕获事件
   RED Plan: 实现前调用 SetMode 应失败（ERR_NOT_IMPLEMENTED）
   GREEN Plan: 实现后预期 OK + 事件被 stub 捕获
```

```text
✅ TC-007: 覆盖 NFR-001（实时性 ≤ 5 ms）
   Test Level: integration
   Coverage Type: embedded-risk
   Preconditions: 目标平台 X、时钟节拍 Y
   Steps: 1000 次连续调用 Service.SetMode，记录 95th percentile 延迟
   Expected: 95th percentile ≤ 5 ms
   Mocks: 时钟用真实硬件时钟；ControlScheduler 真实运行
   RED Plan: 实现前期望失败（>5 ms 或 build 失败）
   GREEN Plan: 实现后 95th ≤ 5 ms；保留 latency 直方图
```

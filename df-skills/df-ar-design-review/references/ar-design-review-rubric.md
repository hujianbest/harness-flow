# df AR Design Review Rubric

> 配套 `df-ar-design-review/SKILL.md`。展开 8 维度评分细则与 rule IDs。

## 8 维度评分

| 维度 | 关键检查 |
|---|---|
| **AD1 Identity & Template Conformance** | AR ID、SR / IR、Owner、所属组件、模板版本与团队模板对齐（或显式占位） |
| **AD2 Goal & Scope Clarity** | 设计目标、当前 AR 范围 / 非范围、与 requirement.md 的范围一致 |
| **AD3 Affected Files & Control Flow** | 受影响文件 / 模块 / 函数 / 类清单准确；关键控制流可冷读 |
| **AD4 Component Design Conformance** | 与 `docs/component-design.md` 的对 AR 设计的约束一致；未越界改写组件接口 / 依赖 / 状态机 |
| **AD5 C / C++ Defensive Design** | 错误处理、内存、并发（中断上下文 / 锁）、实时性、资源生命周期、ABI / API 兼容 |
| **AD6 Test Design Adequacy** | 测试用例完整、每个用例回指 requirement row、嵌入式风险覆盖矩阵完整 |
| **AD7 Mock / RED-GREEN Plan** | mock 边界合理；RED / GREEN / REFACTOR 证据要求清晰；evidence 落点齐全 |
| **AD8 Open Questions Closure** | 阻塞 / 非阻塞分类；阻塞项已闭合或上抛 |

任一关键维度 < 6 → 不得 `通过`。

## Rule IDs

### Group AD1 - Identity & Template

- `AD1.1` AR ID / SR / IR / Owner 完整
- `AD1.2` 团队模板章节齐全（或显式占位）
- `AD1.3` 与 traceability.md 一致

### Group AD2 - Goal & Scope

- `AD2.1` 设计目标 / 范围 / 非范围清晰
- `AD2.2` 与 requirement.md 范围一致

### Group AD3 - Affected & Control Flow

- `AD3.1` 受影响文件 / 模块清单
- `AD3.2` 关键控制流冷读得懂（必要时小段伪代码 / Mermaid）
- `AD3.3` 接口签名草案与组件接口一致

### Group AD4 - Component Conformance

- `AD4.1` 与 `docs/component-design.md` 对 AR 设计的约束一致
- `AD4.2` 未修改组件接口 / 依赖 / 状态机
- `AD4.3` 跨组件影响（若有）已显式说明并指向相应工件

### Group AD5 - Defensive Design

- `AD5.1` 错误处理（输入校验、降级、恢复）显式
- `AD5.2` 内存（静态 / 动态、生命周期、栈）
- `AD5.3` 并发（中断上下文允许 / 禁止、锁、临界区）
- `AD5.4` 实时性（截止时间、调度、节拍）
- `AD5.5` 资源生命周期（句柄、文件、缓冲区）配对
- `AD5.6` ABI / API 兼容（跨版本、跨平台）

### Group AD6 - Test Design

- `AD6.1` 测试用例最小字段齐全（见 `df-ar-design/references/test-design-section-contract.md`）
- `AD6.2` 每个用例回指 requirement row
- `AD6.3` 每条核心 requirement row 至少被一个用例覆盖
- `AD6.4` NFR 含 `embedded-risk` 用例
- `AD6.5` 嵌入式风险覆盖矩阵完整（内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI）
- `AD6.6` 测试设计为本设计的章节，**不**作为独立文件

### Group AD7 - Mock & Evidence

- `AD7.1` mock 限定在真正的边界（外部依赖 / 硬件 / 协议栈 / 跨组件 SOA）
- `AD7.2` 不允许 mock 内部纯逻辑
- `AD7.3` 不允许「测试专用方法」
- `AD7.4` RED 证据要求清晰
- `AD7.5` GREEN 证据要求清晰（含新鲜度锚点）
- `AD7.6` REFACTOR 证据要求（若适用）清晰

### Group AD8 - Open Questions

- `AD8.1` 阻塞 / 非阻塞分类
- `AD8.2` 阻塞项已闭合或上抛 USER-INPUT / TEAM-EXPERT

## Severity 分级

- `critical`：阻塞 TDD 实施（缺测试设计、嵌入式风险矩阵缺失、AR 设计触及组件边界、缺关键控制流）
- `important`：approval 前应修（错误处理章节缺、mock 边界模糊、RED/GREEN 证据要求模糊）
- `minor`：建议改进（措辞、章节顺序）

## Classification

- `USER-INPUT`：业务方向 / 验收阈值 / 优先级 → 上抛需求负责人 / 开发负责人
- `LLM-FIXABLE`：模板章节缺 / 测试用例补全 / 错误处理章节补充 / mock 边界澄清 → 开发人员定向回修
- `TEAM-EXPERT`：组件边界、SOA 接口、并发 / 实时性架构选型 → 上抛模块架构师

## Verdict 决策

| 评分 / findings 状态 | verdict | needs_human_confirmation |
|---|---|---|
| 8 维度均 ≥ 6、组件边界未被改写、测试设计章节充分、无 critical USER-INPUT | `通过` | `true`（开发负责人确认） |
| 评分某项 < 6 但 findings 可 1-2 轮定向修订 | `需修改` | `false` |
| 测试设计缺失 / 嵌入式风险矩阵缺失 / 设计严重不清 / critical TEAM-EXPERT 阻塞 | `阻塞`（内容） | `false` |
| AR 设计修改组件边界 / 上游证据冲突 | `阻塞`（workflow） + `reroute_via_router=true` | `false` |

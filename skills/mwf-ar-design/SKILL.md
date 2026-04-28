---
name: mwf-ar-design
description: Use when the spec is approved and the AR (or DTS that needs an AR-level design) needs a code-level implementation design with an embedded test design section, when component design is stable enough to be consumed (or has just been approved by mwf-component-design-review), or when mwf-ar-design-review returns 需修改/阻塞. Not for changing component architecture (→ mwf-component-design), not for writing production code (→ mwf-tdd-implementation), not for unclear spec (→ mwf-specify), not for hotfix root cause (→ mwf-problem-fix).
---

# mwf AR 实现设计

把单个 AR（或需要正式 AR 实现设计的 DTS）转化为**代码层设计**与**测试设计**。测试设计是本设计的**章节**，不作为独立文件存在。

本 skill 不修改组件实现设计（必要时回 `mwf-component-design`），不写代码（那是 `mwf-tdd-implementation`），不替开发负责人决定优先级。

## When to Use

适用：

- `mwf-spec-review` 已通过 + 当前修改不触及组件边界（standard / lightweight profile） → 直接进入本节点
- `mwf-component-design-review` 已通过且模块架构师 sign-off（component-impact profile） → 进入本节点
- `mwf-ar-design-review` 返回 `需修改` / `阻塞`，需按 findings 修订
- DTS 修复需要正式 AR 实现设计（可在 `mwf-problem-fix` 后触发）

不适用 → 改用：

- 当前修改影响组件接口 / 依赖 / 状态机 → 回 `mwf-component-design`
- 规格不清 → `mwf-specify`
- 已有可消费的 AR 设计要写代码 → `mwf-tdd-implementation`
- 阶段不清 / 证据冲突 → `mwf-workflow-router`

## Hard Gates

- AR 实现设计必须遵循团队模板（`templates/mwf-ar-design-template.md`；模板留空时由开发负责人 / 模块架构师补齐章节后再交评审）
- AR 实现设计必须含**测试设计章节**；测试设计**不**作为独立 `test-design.md` 文件
- 不修改组件实现设计；触及组件边界 → 停下回 `mwf-workflow-router`
- AR 实现设计 review 通过前，`mwf-tdd-implementation` 不得开始
- 本设计中**不**写完整生产代码；可写关键控制流伪代码 / 接口签名草案以支撑 review

## Object Contract

- Primary Object: AR implementation design model（含测试设计章节）
- Frontend Input Object: 已通过 spec-review 的 `features/<id>/requirement.md`、`docs/component-design.md`（已存在或已通过 component-design-review）、`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（如存在）、当前组件代码现状摘要
- Backend Output Object: `features/<id>/ar-design-draft.md`（过程版） + 同步到 `docs/ar-designs/AR<id>-<slug>.md`（review 通过后由 `mwf-finalize` 同步）
- Object Transformation: 把单个 AR 转成代码层设计 + 可执行的测试意图
- Object Boundaries: 不写组件级设计；不写完整代码；不发明组件接口
- Object Invariants: AR ID、所属组件、SR / IR 锚点、设计目标 / 范围在 review 通过前保持稳定

## Methodology

- **Code-Level Design**: 数据结构、控制流、接口签名草案、关键路径伪代码
- **Requirements Traceability**: 设计章节回指 requirement.md 的 FR / NFR / IFR rows
- **SOLID / GRASP**: 职责清晰、低耦合、高内聚、可测试性
- **C / C++ Defensive Design**: 内存、生命周期、错误处理、并发、实时性、资源释放、ABI / API 兼容
- **Component Design Conformance**: 与 `docs/component-design.md` 的对 AR 设计的约束保持一致；不重新论证组件级决策
- **Template-Constrained Design**: 文档结构由团队模板决定（`templates/mwf-ar-design-template.md`，留空待团队补齐）
- **Test Design Before Implementation**: 测试设计章节先于 TDD；用例覆盖 AR 关键行为、边界、异常路径、嵌入式风险

## Workflow

### 1. 对齐输入与角色

按 Requirements Traceability + Component Design Conformance 读取 requirement.md、reviews/spec-review.md（应 `通过`）、`docs/component-design.md`、`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（若存在）、相关代码现状摘要、component-design-review.md（component-impact 时）。

- spec-review 未通过 → 阻塞，回 `mwf-workflow-router`
- profile 是 component-impact 但 component-design-review 未通过 → 阻塞，回 `mwf-workflow-router`
- 团队模板未补齐 → 不阻塞写作，但显式标注「使用 mwf 占位模板，待团队模板补齐」

### 2. 检查是否触及组件边界

按 SOA Boundary 检查对照 requirement.md 的 Component Impact 与当前 AR 的初步思路。**触及组件接口 / 依赖 / 状态机** → 立即停下，标 `reroute_via_router=true`，回 `mwf-workflow-router` 升级 component-impact。AR 实现设计**不**修改组件架构。

### 3. 加载团队模板

按 Template-Constrained Design 加载 `templates/mwf-ar-design-template.md`（项目 `AGENTS.md` 覆盖优先）；模板章节留空时显式标注「使用 mwf 占位模板，待团队模板补齐」。

### 4. 起草代码层设计

按 Code-Level Design + SOLID / GRASP + C / C++ Defensive Design 写 `features/<id>/ar-design-draft.md`。具体结构遵循团队模板；未补齐时按团队预期结构占位，至少覆盖：AR 标识（AR ID / 所属组件 / SR / IR / Owner）、设计目标与范围（做什么 / 不做什么）、受影响文件 / 模块 / 接口（精确到文件路径 + 函数 / 类名，不展开整段代码）、数据结构与控制流（必要时小段伪代码 / Mermaid）、C / C++ 实现策略（错误处理 / 内存 / 并发 / 实时性 / 资源生命周期 / ABI 兼容）、与组件实现设计的一致性说明、**测试设计**（必含，见步骤 5）、风险与未决问题。任一必含章节缺失 → 不能进入步骤 5。

### 5. 起草测试设计章节（必含）

按 Test Design Before Implementation 把 requirement.md 中的 FR / NFR / IFR 行落成测试设计章节。测试设计是 AR 实现设计的**章节**，**不**作为独立 `test-design.md` 文件。最小字段契约见 `references/test-design-section-contract.md`。至少含：

- 测试用例列表：编号、覆盖的 AR 行为（回指 requirement row ID）、测试层级（unit / integration / simulation）、预期 I/O、覆盖类型（happy / boundary / exception / embedded-risk）
- Mock / Stub / 仿真说明：边界点 + 哪些依赖必须 mock、哪些必须真实运行
- RED / GREEN / REFACTOR 证据要求：哪些命令 / 日志 / 静态分析结果必须保留
- 嵌入式风险覆盖矩阵：内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI 各维度覆盖了哪些用例

测试用例未回指 requirement row、或嵌入式 NFR 未被任何用例覆盖 → 回步骤 4 / 5 修订。

### 6. 同步 traceability 与 progress

按 Requirements Traceability 在 `features/<id>/traceability.md` 补「AR Design Section」与「Test Design Case」列；把 `features/<id>/progress.md` 写为 `Current Stage = mwf-ar-design`、`Pending Reviews And Gates` 含 `ar-design-review`、`Next Action Or Recommended Skill = mwf-ar-design-review`。

### 7. 自检与 handoff

进入 handoff 前自检：模板章节齐全（或显式占位）；设计目标 / 范围 / 受影响文件 / 控制流清晰；与组件设计一致且未修改组件接口；测试设计章节存在且每个用例回指 requirement row；嵌入式风险覆盖矩阵完整；风险与未决问题已分类。任一失败 → 回步骤 4 / 5。自检通过 → 父会话派发独立 reviewer subagent 执行 `mwf-ar-design-review`。

## Output Contract

- `features/<id>/ar-design-draft.md`（过程版本）
- review 通过后由 `mwf-finalize` 同步到 `docs/ar-designs/AR<id>-<slug>.md`
- traceability.md 补充 AR Design Section + Test Design Case
- progress.md 同步：
  - `Current Stage = mwf-ar-design`
  - `Next Action Or Recommended Skill = mwf-ar-design-review`
  - `Pending Reviews And Gates` 含 `ar-design-review`
- handoff 摘要按 mwf-shared-conventions；`reviewer_dispatch_request` 指向 `mwf-ar-design-review`

## Red Flags

- 把整段实现代码贴进设计
- 在 AR 设计中改写组件接口 / 依赖 / 状态机
- 测试设计被拆成独立 `test-design.md` 文件（违反 mwf-principles）
- 测试用例不回指 requirement row
- 嵌入式 NFR 不被任何用例覆盖
- 模板未补齐却伪装完整
- 因「以后再说」放过错误处理章节
- 把开放问题藏在 prose 而无显式分类

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 把组件接口的修改作为 AR 设计的一部分 | 停下回 `mwf-workflow-router` 升级 component-impact |
| 测试设计写成独立文件 | 重新作为 ar-design-draft.md 的章节 |
| 测试用例只覆盖 happy path | 补充边界 / 异常 / 嵌入式风险用例 |

## Verification

- [ ] `features/<id>/ar-design-draft.md` 已落盘
- [ ] 团队模板章节齐全或显式标注待补齐
- [ ] 设计目标 / 范围 / 受影响文件 / 控制流 / C/C++ 实现策略章节齐全
- [ ] 与组件设计一致性显式说明
- [ ] 测试设计章节存在且每个用例回指 requirement row（含嵌入式风险覆盖矩阵）
- [ ] traceability.md 已补充 AR Design + Test Design Case
- [ ] progress.md canonical 同步，下一步 `mwf-ar-design-review`
- [ ] 父会话准备派发独立 reviewer subagent

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/test-design-section-contract.md` | 测试设计章节最小契约 |
| `skills/templates/mwf-ar-design-template.md` | 团队 AR 设计模板（待团队补齐） |
| `skills/docs/mwf-workflow-shared-conventions.md` | 工件路径、canonical 字段、handoff |
| `docs/mwf-principles/03 artifact-layout.md` | AR 设计必含项 |
| `docs/mwf-principles/04 workflow-architecture.md` | Test Design Before Implementation |

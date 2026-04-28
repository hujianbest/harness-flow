# dev-flow (df) Workflow Architecture

- 定位: 定义 `dev-flow`（简称 `df`）skills family 的主路径、条件插入节点、分支路径和质量门禁。
- 关联:
  - 最高原则: `docs/df-principles/00 soul.md`
  - Skill-node 设计契约: `docs/df-principles/01 skill-node-define.md`
  - Skill 写作原则: `docs/df-principles/02 skill-anatomy.md`
  - 工件管理约定: `docs/df-principles/03 artifact-layout.md`

## Purpose

本文回答：

> df 如何把明确输入的需求或问题修改，从规格澄清与审查推进到组件 / AR 设计、TDD 实现、TDD 后测试有效性审查、代码检视和完成收口？

df 不覆盖产品发现。它的入口是团队已经接受的需求、AR、问题单或变更请求。df 的价值在于把这些输入按团队质量要求落到嵌入式软件版本中。

df 过程目录默认使用 `features/AR<id>-<slug>` 和 `features/DTS<id>-<slug>`。测试设计是 AR 实现设计的一部分，不作为独立过程文件。

## Canonical Objects

df workflow 围绕以下对象推进：

| Object | 说明 | 主要节点 |
|---|---|---|
| Requirement Input | 明确输入需求、问题单、IR / SR / AR | `df-specify` |
| Spec Finding Set | 规格审查发现项和 verdict | `df-spec-review` |
| Component Implementation Design | 组件级长期设计，描述组件职责、SOA 接口、依赖和运行机制 | `df-component-design` |
| AR Implementation Design | 单个 AR 的代码层设计，包含测试设计章节 | `df-ar-design` |
| Implementation Slice | 单个 AR / BUG 的 C / C++ 代码变化 | `df-tdd-implementation` |
| Implemented Test Quality Finding Set | TDD 后测试用例有效性审查发现项和 verdict | `df-test-checker` |
| Code Quality Finding Set | 代码检视发现项和 verdict | `df-code-review` |
| Completion Evidence Bundle | 完成判断所需证据集合 | `df-completion-gate` |

## Workflow Profiles

df 可以按风险选择不同密度，但不能降低质量底线。

| Profile | 适用场景 | 主特点 |
|---|---|---|
| `standard` | 大多数既有组件 AR 增量开发 | specify -> spec review -> AR 设计 -> TDD -> test checker -> code review -> completion |
| `component-impact` | AR 影响组件边界、接口、依赖、状态机或新增组件 | 插入组件实现设计和组件设计评审 |
| `hotfix` | 紧急问题修改 | 先复现和根因，再最小安全修复，不能跳过必要验证 |
| `lightweight` | 极小、低风险、纯局部修改 | 可压缩文档量，但保留 traceability、test evidence、review 和 completion |

Profile 由 `df-workflow-router` 根据工件和风险信号判断，不由 agent 随口选择。

## Standard Route

```text
using-df-workflow
  -> df-workflow-router
  -> df-specify
  -> df-spec-review
  -> df-ar-design
  -> df-ar-design-review
  -> df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

说明：

- `df-specify` 不做产品发现，只澄清已有输入是否足以进入设计。
- `df-spec-review` 独立审查规格是否清楚、可追溯、可设计。
- `df-ar-design` 必须承接组件实现设计；如果组件设计缺失或过期，应回 router 判断是否进入 `df-component-design`。
- `df-tdd-implementation` 只能消费已评审通过的 AR 实现设计和测试设计。
- `df-test-checker` 在 TDD 完成后审查已落地测试用例有效性，再进入代码检视。

## Component-Impact Route

当出现以下信号时，进入 `component-impact`：

- 新增组件。
- 修改 SOA 服务接口。
- 修改组件职责、依赖方向、状态机或运行时机制。
- AR 实现需要跨组件协调。
- 现有组件实现设计缺失、过期或与代码明显不一致。

推荐路线：

```text
df-workflow-router
  -> df-specify
  -> df-spec-review
  -> df-component-design
  -> df-component-design-review
  -> df-ar-design
  -> df-ar-design-review
  -> df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

组件实现设计描述组件；AR 实现设计描述一个需求。组件实现设计是 AR 实现设计的输入，不应在 AR 设计中临时改写组件架构。

## Hotfix / Problem-Fix Route

问题修改不能直接跳到“改代码”。推荐路线：

```text
using-df-workflow
  -> df-workflow-router
  -> df-problem-fix
  -> df-ar-design 或 df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

`df-problem-fix` 至少负责：

- 复现问题或记录无法复现原因。
- 根因分析。
- 最小安全修复边界。
- 判断是否需要补 AR 实现设计或组件实现设计。
- 明确回流节点。

紧急不等于绕过。hotfix 可以压缩文档量，但不能跳过必要证据。

## Conditional Nodes

### `df-component-design`

条件激活。只有当组件级资产需要新增或修订时进入。

不应因为每个 AR 都机械进入组件设计；大多数既有组件增量开发只读取组件设计作为输入。

### `df-test-checker`

默认在 `df-tdd-implementation` 后进入。它审查 TDD 后已落地测试用例是否真正有效，而不是重新设计测试或修改生产代码。

重点检查：

- 测试是否覆盖 AR 关键行为。
- 是否覆盖边界、异常路径和嵌入式风险。
- 测试是否可执行、稳定、可维护。
- 测试断言是否能证明行为，而不是只证明代码被调用。

## Review And Gate Separation

df 必须保持角色分离：

- authoring 节点写设计，不评审自己。
- implementation 节点写代码和测试证据，不自称代码质量通过。
- test checker 审查 TDD 后测试用例，不补写测试、不改生产代码。
- code review 检查代码，不替代测试有效性审查。
- completion gate 消费证据，不制造缺失证据。

## Canonical Transition Intent

| 当前节点 | 成功后 | 需修改 / 阻塞 |
|---|---|---|
| `df-specify` | `df-spec-review` | 回到需求负责人 / router |
| `df-spec-review` | `df-ar-design` 或 `df-component-design` | `df-specify` |
| `df-component-design` | `df-component-design-review` | 继续修订 |
| `df-component-design-review` | `df-ar-design` | `df-component-design` |
| `df-ar-design` | `df-ar-design-review` | 继续修订 |
| `df-ar-design-review` | `df-tdd-implementation` | `df-ar-design` |
| `df-tdd-implementation` | `df-test-checker` | 继续实现 |
| `df-test-checker` | `df-code-review` | `df-tdd-implementation` |
| `df-code-review` | `df-completion-gate` | `df-tdd-implementation` |
| `df-completion-gate` | `df-finalize` | 缺什么回什么 |
| `df-finalize` | workflow closed | router |

若结论无法唯一映射下一节点，回 `df-workflow-router`。

## Hard Stops

以下情况必须停止自动推进：

- 需求输入不清，且涉及方向、范围或验收标准。
- AR / SR / IR 追溯关系冲突。
- AR 所属组件不唯一。
- 缺组件实现设计，但修改影响组件边界。
- AR 实现设计未包含测试设计。
- 实现需要修改组件架构，但当前节点不是组件设计。
- TDD 完成后测试用例未经 `df-test-checker` 审查。
- code review 发现高风险 C / C++ 问题。
- completion evidence bundle 不完整。

## Methodology Map

| 阶段 | 主要方法 |
|---|---|
| 规格澄清 | Requirements Traceability、Scope / Non-scope、Acceptance Criteria |
| 规格评审 | Structured Review、Traceability Check、Designability Check |
| 组件实现设计 | SOA Component Boundary Analysis、Clean Architecture Boundary Discipline、Interface Segregation、Dependency Direction Check、C / C++ Defensive Design |
| AR 实现设计 | Code-Level Design、Traceability、SOLID / GRASP、Cohesion & Coupling、C / C++ Defensive Design、Test Design Before Implementation |
| TDD 实现 | Embedded TDD、RED / GREEN / REFACTOR、Refactoring Discipline、Fresh Evidence |
| 测试有效性审查 | Post-TDD Test Effectiveness Review、Coverage / Assertion Quality Review、Boundary / Error / State Coverage |
| 代码检视 | C / C++ Code Inspection、MISRA / CERT / Team Coding Standard、Static Analysis Review、Memory / Concurrency / Timing Risk Review、SOA Boundary Review、Maintainability Review |
| 完成门禁 | Evidence Bundle、Definition of Done、Role Separation、No Known Critical Quality Debt |

## Completion Definition

一个 AR / 问题修改只有在以下条件满足时，才可以进入 `df-finalize`：

- 规格澄清或问题根因记录可回读。
- spec review 通过。
- 组件实现设计已存在且未被本次修改破坏；若修改了组件级行为，已更新并通过 review。
- AR 实现设计通过 review。
- 测试设计已执行并保留证据。
- TDD 后测试用例通过 `df-test-checker`。
- C / C++ 实现通过代码检视。
- 无已知 critical 质量债、架构边界债或未解释的静态分析高风险项。
- completion gate 给出通过结论。

## Minimal First Skill Set

建议第一批实现这些 skills：

1. `using-df-workflow`
2. `df-workflow-router`
3. `df-specify`
4. `df-spec-review`
5. `df-component-design`
6. `df-component-design-review`
7. `df-ar-design`
8. `df-ar-design-review`
9. `df-tdd-implementation`
10. `df-test-checker`
11. `df-code-review`
12. `df-completion-gate`
13. `df-finalize`
14. `df-problem-fix`

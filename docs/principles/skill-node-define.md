# HF Flow Node Define

- 定位: HF workflow node 的设计契约，定义一个 `hf-*` skill 如何成为可编排、可恢复、可审计的 workflow 节点。
- 关联:
  - Skill 通用写法: `docs/principles/skill-anatomy.md`
  - 方法论治理: `docs/principles/methodology-coherence.md`
  - 路由与迁移: `skills/hf-workflow-router/references/profile-node-and-transition-map.md`
  - 共享状态与交接约定: `skills/docs/hf-workflow-shared-conventions.md`

## Purpose

本文回答一个问题：

> 一个 `hf-*` skill 要成为 HF workflow 中的合法节点，应该如何设计？

在 HF 中，flow node 不是抽象流程图上的一个框，而是一个具体 skill。Router 编排的不是散落步骤，而是一组带有职责边界、方法论、输入输出、证据规则和交接语义的 `hf-*` skill。

因此，本文不维护完整节点清单，不替代各 skill 的 `SKILL.md`，也不重复 progress schema、verdict vocabulary 或 route map。它只定义 **skill-as-node** 的设计标准。

## Core Definition

一个 HF flow node 是一个满足以下条件的 `hf-*` skill：

1. 有唯一、清晰的 workflow 职责。
2. 声明它处理的核心对象是什么。
3. 说明该对象如何承接前端输入对象、如何形成后端输出对象。
4. 声明它使用什么方法完成该职责。
5. 能把方法落成具体 workflow todo list。
6. 能读取权威上游工件，而不是依赖对话记忆。
7. 能产出或评审明确工件、record 或 evidence。
8. 能给出唯一下一步，或明确阻塞并回到 router。
9. 能被 `hf-workflow-router` 根据磁盘证据重新进入。

简写为：

```text
HF flow node = skill + responsibility + object + methods + workflow todos + artifacts + evidence + handoff
```

## Five Contracts

每个 HF node skill 必须同时满足五类 contract。

| Contract | 回答的问题 | 常见落点 |
|---|---|---|
| Identity Contract | 这是什么节点，何时应该被加载？ | frontmatter、H1、When to Use |
| Object Contract | 这个节点处理什么对象？它和输入 / 输出对象是什么关系？ | Object Model、Input / Output Contract、Workflow |
| Workflow Contract | 它在流程中读什么、做什么、写什么、下一步去哪？ | Workflow、Output Contract、Verification |
| Method Contract | 它用什么方法做这件事，方法如何落地？ | Methodology、Workflow step、rubric |
| Quality Contract | 怎么证明它做对了，什么情况必须停？ | Hard Gates、Red Flags、Verification |

这五类 contract 不应彼此替代。只写步骤而不写对象，会让 agent 不知道自己到底在加工什么；只写对象而不写方法，会让节点缺少可靠做法；只写方法而不写 todo，会让节点不可执行；只写下一步而不写证据，会让 workflow 不可恢复。

## Node Role Types

HF node 的类型按职责划分，不按主链顺序划分。

| Role | 典型 skill | 主职责 | 不应承担的事 |
|---|---|---|---|
| Public Entry | `using-hf-workflow` | 判断 direct invoke 还是 route-first | 完整状态恢复、正文产出 |
| Router | `hf-workflow-router` | 基于工件证据决定 profile、stage、next node | 代替 leaf skill 写 spec / design / code |
| Authoring | `hf-specify` / `hf-design` / `hf-tasks` | 产出可评审工件 | 独立评审自己，或提前实现 |
| Review | `hf-*-review` | 独立发现问题、给 verdict、指唯一下一步 | 顺手回修正文或实现 |
| Approval | `规格真人确认` / `设计真人确认` / `任务真人确认` | 解锁关键下游阶段 | 被 auto 模式删除 |
| Implementation | `hf-test-driven-dev` | 实现唯一活跃任务并保留 fresh evidence | 换任务、跳过测试、重定义需求 |
| Gate | `hf-regression-gate` / `hf-completion-gate` | 消费证据判断能否继续 | 制造缺失证据或替代 review |
| Branch / Re-entry | `hf-hotfix` / `hf-increment` | 处理缺陷恢复、范围变化与安全回流 | 绕过主链直接改代码 |
| Finalize | `hf-finalize` | closeout、release notes、handoff pack | 混入新实现 |
| Knowledge Side Node | `hf-bug-patterns` | 沉淀重复缺陷模式 | 作为 mandatory gate 卡主链 |

新增 skill 前应先判断它属于哪类 role。如果找不到清晰 role，通常说明它只是某个现有节点的 reference、rubric 或子步骤，不应该提升为独立 node。

## Identity Contract

Identity Contract 用来帮助系统和人判断“现在是否应该加载这个 skill”。

每个 node skill 至少应定义：

- `name`: 与 skill 目录名一致，使用 canonical `hf-*` 名称。
- `description`: 分类器语义，只写触发条件和反向边界，不写完整流程摘要。
- H1 开场: 1-2 句说明唯一职责，以及它不替代什么。
- `When to Use`: 正向触发条件、direct invoke 条件、相邻 skill 边界。
- `When Not to Use`: 何时应回 router、上游节点、review 节点或 gate 节点。

Identity Contract 不负责表达完整执行步骤。执行步骤属于 Workflow Contract。

## Object Contract

Object Contract 用来向 agent 澄清：当前 skill-node 处理的核心对象是什么，以及这个对象如何从前端输入对象转成后端输出对象。

这里的“对象”不是一定指代码里的 class，而是该节点主要加工、判断或交接的业务 / 工程单元。它可以是 problem statement、spec、design model、task plan、active task、test evidence、review finding、completion evidence bundle、closeout pack 等。

每个 node skill 至少应说明：

- `Primary Object`: 本节点真正处理的对象。
- `Frontend Input Object`: 从用户请求、上游工件、progress、review record 或 evidence 中接收的对象。
- `Backend Output Object`: 本节点完成后交给下游的对象。
- `Object Transformation`: 本节点把输入对象加工、评审、验证或路由成输出对象的关系。
- `Object Boundaries`: 本节点不应修改、创造或替代哪些对象。
- `Object Invariants`: 该对象在节点执行前后必须保持的关键约束。

示例：

| Node | Frontend Input Object | Primary Object | Backend Output Object | Transformation |
|---|---|---|---|---|
| `hf-specify` | 用户意图、discovery 结论、约束 | requirement model | 可评审 spec draft | 把模糊意图澄清、分类、验收化 |
| `hf-design` | 已批准 spec、NFR、约束 | architecture decision model | design doc、ADR references | 把需求对象转成结构、接口、权衡和风险响应 |
| `hf-tasks` | 已批准 design、spec | implementation work model | task plan、task board | 把设计对象拆成可执行、可验证的任务对象 |
| `hf-test-driven-dev` | 当前唯一 active task、测试设计 | implementation slice | code change、RED/GREEN evidence、handoff | 把任务对象实现成被 fresh evidence 支撑的代码变化 |
| `hf-code-review` | diff、design、task、test evidence | code quality finding set | review record、verdict、next action | 把实现对象检查成 findings 与迁移结论 |
| `hf-completion-gate` | reviews、regression evidence、handoff | completion evidence bundle | completion verdict、next task / finalize signal | 把多源证据对象判定为能否完成 |

Object Contract 要避免两类错误：

- 把前端输入对象误当成节点职责。例如用户说“实现这个需求”，并不意味着 `hf-test-driven-dev` 可以跳过 spec / task 对象直接实现自然语言请求。
- 把后端输出对象误当成本节点可以随意创造的对象。例如 review 节点可以产出 review record 和 verdict，但不能顺手产出修订后的 design 或代码。

## Workflow Contract

Workflow Contract 定义该 skill 在 workflow 中如何执行。

一个 HF node skill 的 `Workflow` 不是普通阶段列表，而是 **带方法论标注、输入输出、停止条件和交接规则的执行 todo list**。

每个 workflow step 应尽量回答：

- 要做什么？
- 当前步骤处理哪个对象？
- 使用什么方法或判断原则？
- 读取什么输入？
- 产出什么工件、record、evidence 或中间判断？
- 该步骤如何推进 `Frontend Input Object -> Primary Object -> Backend Output Object` 的转换？
- 什么情况下继续？
- 什么情况下停止、回修或 reroute？

推荐写法：

| Step | Todo | Object | Method | Input | Output | Stop / Continue Rule |
|---|---|---|---|---|---|---|
| 1 | Precheck 是否可进入本节点 | frontend input object | Evidence-Based Decision Making | progress、上游 record、用户请求 | 进入 / 阻塞判断 | 证据冲突则回 router |
| 2 | 读取最少必要上游工件 | primary object baseline | Traceability Reading | spec / design / tasks / reviews | 上下文摘要 | 发现缺失或冲突则阻塞 |
| 3 | 执行节点核心工作 | primary object | 节点声明的方法论 | 上游输入 | 新工件、review record 或 evidence | 达不到完成条件则继续修订 |
| 4 | 写入结果 | backend output object | Artifact Contract | 本轮结论 | artifact path / record_path | 写不出记录则不得 handoff |
| 5 | 交接下一步 | output-to-next input | Transition Contract | verdict / result | next_action_or_recommended_skill | 下一步不唯一则回 router |

节点自己的 `SKILL.md` 可以使用编号列表而不是表格，但语义必须完整。

## Method Contract

HF workflow 不只定义“做哪一步”，还定义“用什么方法做这一步”。

每个 node skill 必须声明它采用的方法论，并说明这些方法如何落到实际 workflow。方法论声明应回答：

1. 该节点为什么需要这些方法？
2. 这些方法解决节点职责中的什么风险？
3. 这些方法作用于哪个 primary object？
4. 方法如何支撑输入对象到输出对象的转换？
5. 方法如何映射到 workflow todo？
6. 方法如何影响输出工件结构？
7. 方法如何影响 review、gate 或 verification 标准？
8. 哪些方法是 hard rule，哪些只是辅助参考？

示例：

| Node | Responsibility | Methods | Method-to-workflow mapping |
|---|---|---|---|
| `hf-specify` | 把模糊需求转成可评审 spec | EARS、BDD、MoSCoW、INVEST、ISO 25010、QAS | FR 用 EARS，验收用 BDD，优先级用 MoSCoW，NFR 用 ISO 25010 + QAS |
| `hf-design` | 把批准规格转成可实现结构 | DDD、Event Storming、C4、ADR、ARC42、Risk-Driven Architecture | 先建领域与风险模型，再写结构视图、关键决策和权衡 |
| `hf-test-driven-dev` | 实现唯一活跃任务并证明行为 | Canon TDD、Walking Skeleton、Two Hats、Fresh Evidence | 先测试设计，再 RED / GREEN / REFACTOR，最后交接 fresh evidence |
| `hf-code-review` | 独立检查实现质量 | Fagan Inspection、Clean Architecture、Defense in Depth | 按 rubric 冷读 diff，给 findings、severity、verdict 与唯一下一步 |

方法论不能只出现在 README 或 pack-level 表格中。对会改变节点行为的方法，必须在对应 `SKILL.md` 的 workflow、hard gate、verification 或 reference 中有可执行落点。

## Quality Contract

Quality Contract 定义节点如何证明自己完成了，以及哪些情况必须停止。

每个 node skill 应至少定义：

- `Hard Gates`: 不满足时不能继续执行的条件。
- `Red Flags`: 看到后应停止、回 router 或升级给用户的信号。
- `Verification`: 离开该节点前必须满足的检查。
- `Common Mistakes`: 可选，用于说明常见错误及修复方式。

常见 hard gate 包括：

- 缺少必需上游工件或 approval record。
- progress、review、gate、用户请求之间存在证据冲突。
- 当前 profile 不允许进入该节点。
- `Current Active Task` 不唯一。
- 输出 record 无法写入或无法回读。
- `next_action_or_recommended_skill` 无法唯一归一化。
- auto 模式缺少 policy 或 approval record 落点。
- reviewer / gate 结论要求 `reroute_via_router=true`。

Quality Contract 的重点不是“尽量做得好”，而是定义何时不得继续推进。

## Output And Handoff Contract

HF node skill 完成时，必须留下可恢复的交接信息。

最小 handoff 应包含：

- `current_node`
- `result` 或 `verdict`
- `artifact_paths`
- `record_path`
- `evidence_summary`
- `blockers`
- `next_action_or_recommended_skill`
- `reroute_via_router`，如适用

约束：

- `next_action_or_recommended_skill` 必须使用 canonical node name 或 canonical approval step。
- review / gate 结论必须落盘到 record，不能只存在于对话。
- 证据型节点必须说明 fresh evidence 的命令、结果、新鲜度锚点和覆盖风险。
- workflow 已结束时，不伪造下游节点；留空或使用项目约定 null 值。
- 如果下一步不唯一，必须回到 `hf-workflow-router`，不能凭印象选择。

## Skill File Shape

一个 HF node skill 的 `SKILL.md` 推荐使用以下骨架：

```markdown
---
name: hf-example-node
description: Use when ... Not for ...
---

# HF Example Node

This skill does exactly one workflow job. It does not replace adjacent-node-name.

## When to Use

## Hard Gates

## Methodology

## Object Contract

## Workflow

1. Precheck activation.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

2. Perform node-specific work.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

3. Write artifacts and records.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

4. Handoff.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

## Output Contract

## Red Flags

## Verification

## Supporting References
```

章节名称可以按 `skill-anatomy.md` 调整，但语义不能丢。尤其是 `Workflow` 必须写成可执行 todo list，而不是概念说明。

## Method-To-Workflow Example

以下示例展示一个 authoring node 如何把方法论落成 workflow todo。

```markdown
## Methodology

- DDD Strategic Modeling: identify bounded contexts, ubiquitous language, and context relationships.
- Event Storming: bridge spec behavior into domain events and process flow.
- ADR: record key architecture decisions and consequences.
- C4: express container and component structure.
- Risk-Driven Architecture: spend design detail where risk is highest.

## Object Contract

- Frontend Input Object: approved requirement spec, NFRs, constraints, assumptions.
- Primary Object: architecture decision model.
- Backend Output Object: design artifact, ADR references, design-review handoff.
- Transformation: convert approved requirements into structure, interfaces, trade-offs, risk responses, and reviewable decisions.
- Boundaries: do not rewrite the spec, split implementation tasks, or start coding.

## Workflow

1. Precheck approved spec and route state.
   - Object: frontend input object.
   - Method: Evidence-Based Decision Making.
   - Input: progress, spec review record, approval record.
   - Output: activation decision.
   - Stop / continue: stop if approval is missing or route evidence conflicts.

2. Build domain and risk model.
   - Object: primary object baseline.
   - Method: DDD Strategic Modeling + Risk-Driven Architecture.
   - Input: approved spec, NFRs, constraints, assumptions.
   - Output: context summary, risk list, design focus areas.
   - Stop / continue: stop if spec lacks enough boundary information to design safely.

3. Draft architecture decisions.
   - Object: primary object.
   - Method: ADR + C4 + ARC42.
   - Input: context summary and alternatives.
   - Output: design artifact and ADR references.
   - Stop / continue: continue until each key risk has an explicit decision or deferral.

4. Validate design completeness.
   - Object: backend output object candidate.
   - Method: QAS uptake + lightweight STRIDE.
   - Input: design draft, NFRs, threat signals.
   - Output: self-check notes and review handoff.
   - Stop / continue: revise before handoff if NFR or risk coverage is missing.

5. Handoff to design review.
   - Object: output-to-next input.
   - Method: Transition Contract.
   - Input: final design artifact.
   - Output: progress update with `next_action_or_recommended_skill = hf-design-review`.
   - Stop / continue: reroute if next action cannot be uniquely represented.
```

## Design Checklist For New HF Nodes

新增或重写一个 `hf-*` skill 前，至少检查：

- 这个 skill 是否有独立 workflow 职责，而不是现有节点的子步骤？
- 它属于哪个 node role？
- 它和相邻 skill 的边界是否明确？
- 它处理的 primary object 是什么？
- 它的 frontend input object 和 backend output object 分别是什么？
- 它是否清楚说明了输入对象、核心对象、输出对象之间的转换关系？
- 它使用哪些方法论？这些方法是否已在 `methodology-coherence.md` 中有位置？
- 每个核心方法是否支撑 primary object 的加工、评审、验证或交接？
- 每个核心方法是否映射到了 workflow todo、artifact 字段、rubric 或 verification？
- 它需要读取哪些上游工件、record、approval 或 evidence？
- 它会写出哪些 artifact、record、verification 或 progress 更新？
- 它是否能给出唯一 canonical next action？
- 它的 hard gates 是否覆盖证据缺失、证据冲突和不合法迁移？
- 它是否需要新增 route map、shared convention、template 或 eval？

如果一个候选 skill 无法通过以上检查，不要先创建 skill。应先把它下沉为已有 skill 的 `references/`、rubric、template 或 workflow step。

## Non-Goals

本文不做以下事情：

- 不维护当前 HF 的完整节点列表。
- 不定义 profile 的合法节点集合。
- 不定义 review / gate verdict vocabulary。
- 不定义 progress schema。
- 不替代 `SKILL.md` 的具体执行说明。
- 不替代 evals、fixtures 或 reviewer checklist。

这些内容分别由 router references、shared conventions、各节点 `SKILL.md` 与对应 evals 维护。

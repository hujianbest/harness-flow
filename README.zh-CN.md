# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**从一个 idea 到产品落地：面向 AI Agent 的高质量工程工作流。**

HarnessFlow 是一个面向 AI Agent 的 skill pack，用来把**从产品洞察到架构设计、再到实现与交付**的完整工程节奏落到结构化工件、质量纪律和清晰交接上。它把产品发现、规格澄清、架构设计、任务拆解、带门禁的 TDD 实现、多道独立评审、回归与完成门禁、正式收尾都当作一等阶段，让 agent 沿着显式阶段推进"一个 idea → 可评审方向 → 可评审设计 → 可执行任务 → 可落地产品"，而不是依赖临时拼接的 prompt 链路。

## 项目概览

HarnessFlow 当前的主路径覆盖「**从一个 idea 到产品落地**」全程：

- 上游 **产品洞察**：problem framing、JTBD、Opportunity Solution Tree、RICE / ICE、Desired Outcome / North Star
- **假设验证**：`hf-experiment` 在 Blocking 或低 confidence 关键假设下插入的最小 probe
- **规格澄清**：EARS + BDD + MoSCoW + INVEST + ISO 25010 + Quality Attribute Scenarios + Success Metrics / Key Hypotheses
- **架构设计**：DDD 战略建模 + DDD 战术建模（Aggregate / VO / Repository / Domain Service / Application Service / Domain Event）+ Event Storming + C4 + ADR + ARC42 + NFR QAS 承接 + 轻量 STRIDE + Emergent vs Upfront Patterns 治理（GoF 刻意 emergent）
- **UI 设计**（规格声明 UI surface 时激活）：IA + Atomic Design + Design Tokens + Nielsen + WCAG 2.2 AA + 交互状态清单
- **任务拆解**：WBS + INVEST + 依赖图 / 关键路径 + Definition of Done
- **单任务 TDD 实现**：Canon TDD + Walking Skeleton + Two Hats + Clean Architecture conformance + fresh evidence
- **多道独立评审**：test / code / traceability / ui / discovery / spec / design / tasks review 的 Fagan 式角色分离
- **回归与完成门禁**：impact-based regression + evidence bundle + Definition of Done
- **正式收尾**：task closeout 与 workflow closeout 的 PMBOK 式闭环
- **运行时路由与恢复**：`using-hf-workflow` / `hf-workflow-router`，按工件证据恢复编排
- **支线与经验沉淀**：`hf-hotfix` / `hf-increment` / `hf-bug-patterns`

向下继续演进（覆盖发布 / 运维 / 度量回流 / 协作 / 长期架构健康 / 数据与 AI 产品等商用级交付能力）已在规划中，但当前尚未落地。

在内部命名上，这套 skill family 目前使用 `hf-*` 约定。

## HF 方法论

HarnessFlow 不是一组零散 prompt 的集合，而是一套面向 agent 工程执行的工作流方法论。

从整体上看，HF 把这些方法组合在一起：

- **以 spec 为锚点的 SDD**：把 spec、design、tasks 当作结构化工件，而不是“大一点的 prompt”
- **带门禁的 TDD**：一次只实现一个 `Current Active Task`，先做测试设计，再保留新鲜的 RED/GREEN 证据
- **基于证据的路由**：下一步从磁盘工件恢复，而不是靠聊天记忆猜
- **独立的 review 与 gates**：test review、code review、traceability review、regression、completion 各自保持独立职责
- **受控的 closeout**：把“任务完成”和“整个 workflow 完成”区分开，并显式处理 finalize

这正是 HF 和普通 agent workflow 的差别：它优化的不只是更快开始写代码，而是正确性、可恢复性和工程纪律。

### 方法论分层

| 层 | HF 使用的方法 | 为什么重要 |
|---|---|---|
| 意图层 | 以 spec 为锚点的 SDD | 让范围、约束和验收标准始终落在可回读工件上。 |
| 执行层 | 带门禁的 TDD | 强制实现遵循测试设计、RED/GREEN 证据和单活跃任务约束。 |
| 路由层 | 基于证据的 workflow 恢复 | 让 agent 能从仓库状态恢复，而不是依赖会话记忆。 |
| 评审层 | 结构化 walkthrough 与 traceability 检查 | 让质量判断显式存在，而不是混在实现里顺手做掉。 |
| 验证层 | regression / completion gates | 把“看起来做完了”和“证据足以宣告完成”分开。 |
| 收尾层 | 正式 closeout 与 handoff | 避免代码改完后没有状态同步、release 记录和 workflow 收口。 |

### 方法论来源

HF 明确吸收了几类工程方法：

- Martin Fowler / Thoughtworks 风格的 **spec-driven development**
- Kent Beck 风格的 **test-driven development**
- Kent Beck / Fowler 的 **Two Hats** 帽子纪律，配合 **opportunistic / preparatory refactoring**，让架构与代码健康在编码节奏内被持续维护
- Robert C. Martin 的 **Clean Architecture** conformance 与 SOLID 检查，落到实现节点
- review 节点中的 **Fagan 风格结构化评审**
- 从 spec -> design -> tasks -> implementation -> verification 的 **端到端追溯**
- 把 **fresh evidence** 当成一等完成条件
- finalize / handoff 中的 **PMBOK 式收尾思路**

## 每个 Skill 用了什么方法论

HF 的每个 skill 都会在自己的 `SKILL.md` 里显式声明方法论。在 pack 层面，当前可以概括成下面这张图：

### 入口与路由

| Skill | 核心方法论 |
|---|---|
| `using-hf-workflow` | Front Controller Pattern、Evidence-Based Dispatch、Separation of Concerns |
| `hf-workflow-router` | Finite State Machine Routing、Evidence-Based Decision Making、Escalation Pattern |

### 上游 discovery

| Skill | 核心方法论 |
|---|---|
| `hf-product-discovery` | Problem Framing、Hypothesis-Driven Discovery、Opportunity / Wedge Mapping、Assumption Surfacing、JTBD / Jobs Stories、Opportunity Solution Tree、RICE / ICE / Kano、Desired Outcome / North Star Framing |
| `hf-discovery-review` | Structured Walkthrough、Checklist-Based Review、Separation of Author/Reviewer Roles、Evidence-Based Verdict |
| `hf-experiment`（Phase 0 新增） | Hypothesis-Driven Development、Build-Measure-Learn、Four Types of Assumptions (D/V/F/U)、Smallest Testable Probe、Pre-registered Success Threshold |

### Authoring

| Skill | 核心方法论 |
|---|---|
| `hf-specify` | EARS、BDD / Gherkin、MoSCoW Prioritization、Socratic Elicitation、INVEST、ISO/IEC 25010 + Quality Attribute Scenarios、Success Metrics & Key Hypotheses Framing、RICE / ICE / Kano（承接自 discovery） |
| `hf-spec-review` | Structured Walkthrough、Checklist-Based Review、Separation of Author/Reviewer Roles、Evidence-Based Verdict |
| `hf-design` | ADR、C4 Model、Risk-Driven Architecture、YAGNI + Complexity Matching、ARC42、DDD Strategic Modeling (Bounded Context / Ubiquitous Language / Context Map)、DDD Tactical Modeling (Aggregate / VO / Repository / Domain Service / Application Service / Domain Event)、Event Storming (spec→design bridge)、Quality Attribute Scenarios (NFR 承接)、STRIDE 轻量威胁建模、Emergent vs Upfront Patterns 治理 |
| `hf-design-review` | ATAM、Structured Walkthrough、Separation of Author/Reviewer Roles、Traceability to Spec |
| `hf-ui-design` | Information Architecture、Atomic Design、Design System / Design Tokens、Nielsen Heuristics、WCAG 2.2 AA、Interaction State Inventory、ADR |
| `hf-ui-review` | ATAM (adapted to UI)、Nielsen Heuristic Evaluation、Structured Walkthrough、Separation of Author/Reviewer Roles、Traceability to Spec |
| `hf-tasks` | WBS、INVEST Criteria、Dependency Graph + Critical Path、Definition of Done |
| `hf-tasks-review` | INVEST Validation、Dependency Graph Validation、Traceability Matrix、Structured Walkthrough |

### 执行与评审

| Skill | 核心方法论 |
|---|---|
| `hf-test-driven-dev` | TDD、Walking Skeleton、Test Design Before Implementation、Fresh Evidence Principle、Two Hats（Beck/Fowler）、Opportunistic + Boy Scout Refactoring、Preparatory Refactoring、Clean Architecture Conformance、Escalation Boundary |
| `hf-test-review` | Fail-First Validation、Coverage Categories、Bug-Pattern-Driven Testing、Structured Walkthrough |
| `hf-code-review` | Fagan Code Inspection、Design Conformance Check、Defense-in-Depth Review、Clean Architecture Conformance Check、Two Hats / Refactoring Hygiene Review、Architectural Smells Detection、Separation of Author/Reviewer Roles |
| `hf-traceability-review` | End-to-End Traceability、Zigzag Validation、Impact Analysis |

### 门禁与收尾

| Skill | 核心方法论 |
|---|---|
| `hf-regression-gate` | Regression Testing Best Practice、Impact-Based Testing、Fresh Evidence Principle |
| `hf-doc-freshness-gate` | Sync-on-Presence、Profile-Aware Rigor、Evidence Bundle Pattern、Author/Reviewer/Gate Separation |
| `hf-completion-gate` | Definition of Done、Evidence Bundle Pattern、Profile-Aware Rigor |
| `hf-finalize` | Project Closeout、Release Readiness Review、Handoff Pack Pattern |

### 分支与经验沉淀

| Skill | 核心方法论 |
|---|---|
| `hf-hotfix` | Root Cause Analysis / 5 Whys、Minimal Safe Fix Boundary、Blameless Post-Mortem Mindset |
| `hf-increment` | Change Impact Analysis、Re-entry Pattern、Baseline-before-Change、Separation of Analysis and Implementation |
| `hf-bug-patterns` | Defect Pattern Catalog、Blameless Post-Mortem / Learning Review、Human-In-The-Loop Knowledge Curation |

## 为什么这些方法会分配给这些 Skills

HF 不是随意把方法论贴到各个节点上。每个 skill 使用的方法，都是为了匹配它在工作流里的核心职责。

- 入口和路由节点使用 controller、状态机和基于证据的决策方法，因为它们要回答的是“下一步该去哪里”，而不是写工件或写代码。
- authoring 节点使用需求、架构和计划类方法，因为它们要把模糊意图变成可批准、可测试、可拆解的工件。
- review 节点使用 walkthrough、checklist、inspection 和 traceability 方法，因为它们的职责是做独立质量判断，而不是继续写正文或继续实现。
- 实现节点使用 TDD、walking skeleton 和 fresh evidence 规则，因为这里最容易把“我觉得差不多了”误当成“已经被证明是对的”。
- gate 节点使用 definition of done、evidence bundle 和 impact-based verification 方法，因为它们回答的是一个比 review 更窄的问题：当前证据是否足以继续推进或宣告完成。
- 分支节点使用 RCA 和 change-impact 方法，因为 hotfix 与 increment 的本质是安全地处理缺陷恢复或安全地重入主链。
- finalize 使用 closeout 和 handoff 方法，因为“任务通过了”不等于“整个 workflow 已经正式结束”。

### 几个具体例子

| Skill | 为什么这些方法适合它 |
|---|---|
| `hf-specify` | 它的任务是把模糊需求变成可测试的规格，所以需要需求语法、优先级和澄清方法，而不是实现方法。 |
| `hf-design` | 它的任务是把已批准意图转成结构、接口和权衡，所以需要 ADR、C4 和风险驱动架构方法。 |
| `hf-test-driven-dev` | 它是“实现声明必须被运行行为证明”的节点，所以 TDD 和 fresh evidence 在这里是核心，而不是可选项。同一个节点也是 REFACTOR 的天然窗口，因此 Two Hats 纪律、opportunistic / preparatory 重构、Clean Architecture conformance、以及显式的 escalation 边界也都放在这里。 |
| `hf-code-review` | 测试通过并不能自动证明正确性、鲁棒性和安全性，所以 inspection 和 defense-in-depth 方法应该放在这里。该节点也通过评审实现节点的 Refactor Note 和对照已批准设计与 architectural smells 的 conformance 检查，强制保持架构健康与重构纪律。 |
| `hf-completion-gate` | 完成判断来自一组工件的组合证据，而不是某一个测试结果，所以 definition-of-done 和 evidence-bundle 更适合这个节点。 |
| `hf-finalize` | workflow 收口包含状态同步、release notes 和 handoff，因此 closeout 方法应该属于这里，而不是实现节点或 gate 节点。 |

## Installation

目前 HarnessFlow 以源码形式分发。直接 clone 这个仓库，并保持 pack 的目录结构完整。

```bash
git clone <repo-url> HarnessFlow
cd HarnessFlow
```

请把这些目录一起保留：

- `skills/`
- `skills/docs/`
- `skills/templates/`
- `docs/principles/`

如果你要把 HarnessFlow vendor 到另一个 skill workspace，不要只拷贝零散的 `hf-*` 文件夹；请保留整套 pack 结构，因为这些 skills 共享 pack 级文档和模板。

> **推荐起步**：把 `skills/templates/AGENTS.md.example` 复制到你项目仓库根作为 `AGENTS.md`，并按本项目实际情况填空。HF 从仓库根的 `AGENTS.md` 读取"项目级标准注入点"（按 soul.md，"立标准"是架构师/用户的职责，不是 HF 的）。

目前这套 pack 还没有提供一条命令完成安装的 registry 入口。

## Quick Start

如果你只想先试一个 prompt，就先发这个：

```text
使用这个仓库里的 HarnessFlow。从 `using-hf-workflow` 开始，把我路由到正确的 HF 节点。
我想给通知 API 增加限流规则。
不要直接跳到写代码。
```

跑通之后，再试更真实的自然语言请求：

```text
使用 HarnessFlow，为通知 API 的限流规则编写或修订 spec。
使用 HarnessFlow，基于已批准的 spec 评审这份 design draft。
使用 HarnessFlow，对当前活跃任务按 TDD 实现并保留 fresh evidence。
使用 HarnessFlow，对 TASK-003 做 code review。
使用 HarnessFlow，判断这个任务是否真的可以算完成。
使用 HarnessFlow，对已完成的任务或整个 workflow 做 closeout。
```

你也可以直接用自然语言提示词：

```text
使用 HarnessFlow，并根据当前仓库里的工件继续推进。
使用 HarnessFlow，评审这份 spec draft。
使用 HarnessFlow，实现当前活跃任务。
```

| 你说什么 | HarnessFlow 应该做什么 |
|---------|------------------------|
| `使用 HarnessFlow，并根据当前仓库里的工件继续推进。` | 从 `using-hf-workflow` 或 `hf-workflow-router` 开始，根据磁盘工件恢复正确的下一节点。 |
| `使用 HarnessFlow，在写 spec 前先判断一个产品方向值不值得推进。` | 优先偏向 `hf-product-discovery`；如果当前阶段仍不明确，则交给 `hf-workflow-router`。 |
| `使用 HarnessFlow，为通知 API 的限流规则编写或修订 spec。` | 优先偏向 `hf-specify`；如果当前阶段仍不明确，则交给 `hf-workflow-router`。 |
| `使用 HarnessFlow，基于已批准的 spec 评审这份 design draft。` | 只有在这确实是 review-only 且设计工件已准备好时，才 direct invoke `hf-design-review`。 |
| `使用 HarnessFlow，对当前活跃任务按 TDD 实现并保留 fresh evidence。` | 只有在唯一活跃任务和上游批准条件都成立时，才推进到 `hf-test-driven-dev`。 |
| `使用 HarnessFlow，对 TASK-003 做 code review。` | 只有当 code review 的前置条件已经满足时才进入 `hf-code-review`；否则会回到更早的必要节点。 |
| `使用 HarnessFlow，判断这个任务是否真的可以算完成。` | 进入 `hf-completion-gate`，而不是把“完成”当成一句随口结论。 |
| `使用 HarnessFlow，对已完成的任务或整个 workflow 做 closeout。` | 只有在 completion 已允许 closeout 时才进入 `hf-finalize`；否则仍停留在 completion 或 router 逻辑。 |

让入口层和 router 根据仓库工件决定下一节点。这个仓库本身并没有对外提供 HF commands。

## 看它怎么工作

```text
你：    使用这个仓库里的 HarnessFlow。从 `using-hf-workflow` 开始。
        我想给通知 API 增加限流规则。

HF：    先路由到 `hf-specify`，澄清范围并准备可进入 spec review 的
        交接，而不是直接跳到实现。

你：    使用 HarnessFlow，评审这份 spec draft。

HF：    运行 `hf-spec-review`。如果 spec 通过评审且 approval step
        完成，workflow 才会继续进入 `hf-design`。

你：    spec 已经批准。使用 HarnessFlow 产出 design。

HF：    使用 `hf-design`，把已批准意图转成接口、结构和关键技术决策。

你：    使用 HarnessFlow，基于已批准的 spec 评审这份 design。

HF：    运行 `hf-design-review`。只有设计评审通过且 approval step
        完成后，workflow 才会继续走向 `hf-tasks`。

你：    使用 HarnessFlow，把 design 拆成 tasks，并准备下一个 active task。

HF：    使用 `hf-tasks` 和 `hf-tasks-review`，然后由 router 锁定唯一的
        `Current Active Task`，而不是让多个任务同时漂移。

你：    使用 HarnessFlow，对当前 active task 按 TDD 实现。

HF：    进入 `hf-test-driven-dev`，先写测试设计，完成 approval step，
        留下 RED/GREEN evidence，并写回 canonical 下一步。

你：    使用 HarnessFlow，依次评审这个任务的 tests、code 和 traceability。

HF：    按证据情况推进 `hf-test-review` -> `hf-code-review` ->
        `hf-traceability-review`。

你：    使用 HarnessFlow，跑 regression，并判断这个任务是否真的完成。

HF：    使用 `hf-regression-gate` 和 `hf-completion-gate` 来判断当前证据
        是否足够。

你：    使用 HarnessFlow，对已完成任务做 closeout。

HF：    如果还有剩余 approved tasks，就先收口当前任务并回到
        `hf-workflow-router`；如果已经没有剩余 approved tasks，且允许
        closeout，才进入 `hf-finalize` 做 workflow closeout。
```

重点不只是“发几个 prompt”。HarnessFlow 会在每一步读取工件、写回状态，
并产出一个受控的唯一下一动作。如果当前问题其实是线上缺陷或范围变化，
router 还会改走 `hf-hotfix` 或 `hf-increment`，而不是强行套入主链。若发现
重复错误模式，`hf-bug-patterns` 则是可选的经验沉淀旁路，而不是 mandatory gate。

## 它的不同点

HarnessFlow 把工程活动当作一个受控工作流，而不是一次巨大的 agent 调用。

这套 pack 显式拆分了：

- 入口判断与运行时路由
- 编写阶段与实现阶段
- 实现阶段与评审 / 门禁阶段
- 单任务完成与整个工作流收尾

这样可以避免把编排、执行和质量判断压扁成一个不透明的动作。

## 工作流形状

一个典型的完整流程如下：

```text
using-hf-workflow
  -> hf-product-discovery
  -> hf-discovery-review
  -> (optional) hf-experiment     # Blocking / 低 confidence 假设时临时插入
  -> hf-workflow-router
  -> hf-specify
  -> hf-spec-review
  -> (optional) hf-experiment     # spec Key Hypotheses 中 Blocking 假设未关闭时插入
  -> hf-design  (|| hf-ui-design 当规格声明 UI surface 时并行激活)
  -> hf-design-review  (|| hf-ui-review)
  -> hf-tasks
  -> hf-tasks-review
  -> hf-test-driven-dev
  -> hf-test-review
  -> hf-code-review
  -> hf-traceability-review
  -> hf-regression-gate
  -> hf-doc-freshness-gate
  -> hf-completion-gate
  -> hf-finalize
```

> **范围说明**：当前 Workflow Shape 的终点是 `hf-finalize`（工程级 closeout）。**发布与上线**侧（部署管线 / 可观测 / 事故响应 / 度量回流 / 上线后运维）当前**不是**主链一等阶段。这与 `docs/principles/soul.md` 的"现状脚注"一致——HF 必须把这一缺口显式抛回用户，而**不能**悄悄把"代码合并 / 工程 closeout"当作"上线"。

`hf-experiment` 是 Phase 0 引入的 **discovery / spec stage 内部的 conditional insertion**：只在存在 Blocking 或低 confidence 关键假设时临时插入，`probe-result` 回流后按结果回到原插入点或上游修订节点。具体激活与回流规则见 `hf-workflow-router/references/profile-node-and-transition-map.md`。

当规格声明 UI surface（页面 / 组件 / 交互 / 前端 UX NFR）时，router 会把 `hf-ui-design` 作为 **设计阶段内部的 conditional peer skill** 激活，与 `hf-design` 并行起草：`hf-design` 负责架构、模块、API 契约、数据模型、后端 NFR；`hf-ui-design` 负责信息架构、用户流、交互状态、视觉 Design Token、Atomic 组件映射、前端 a11y / i18n / 响应式。两条设计各自独立评审，只有 `hf-design-review` 与 `hf-ui-review` **均通过** 后，父会话才发起联合的 `设计真人确认`。激活条件与 Design Execution Mode（`parallel` / `architecture-first` / `ui-first`）详见 `skills/hf-workflow-router/references/ui-surface-activation.md`。

当请求本质上是缺陷修复或范围变化，而不是普通向前推进时，router 也可以分支到 `hf-hotfix` 和 `hf-increment`。

## 设计原则

HarnessFlow 围绕以下几个默认前提构建：

- specs 锚定意图
- 路由依据磁盘工件，而不是聊天记忆
- 一次只实现一个活跃任务
- review 和 gates 是一等节点
- 质量结论必须依赖 fresh evidence
- 架构与代码健康在 TDD 的 REFACTOR 窗口内通过 Two Hats 与显式 escalation 边界持续维护，而不是延后到一次专门的清理
- closeout 是工程的一部分，而不是事后补充

## 仓库结构

```text
skills/
  using-hf-workflow/
  hf-workflow-router/
  hf-*/
  docs/
  templates/

docs/principles/
  hf-sdd-tdd-skill-design.md
  skill-anatomy.md
```

- `skills/` 存放可安装的 workflow skills。
- `skills/docs/` 存放 pack 级共享文档。
- `skills/templates/` 存放跨 skill 复用的记录与交接模板。
- `docs/principles/` 存放这套 pack 的更高层设计原则与方法论背景。

> **模板分两层**：跨 skill 复用的模板在 `skills/templates/`；各阶段专用长模板（spec / design / tasks / discovery / probe-plan / ADR）就近放在对应 skill 的 `references/` 目录下。审计或生成工件时按二者并集查找。

## 从哪里开始看

如果你想快速理解这套 pack，建议先读这些文件：

1. `skills/using-hf-workflow/SKILL.md`
2. `skills/hf-workflow-router/SKILL.md`
3. `docs/principles/hf-sdd-tdd-skill-design.md`
4. `docs/principles/skill-anatomy.md`
5. `docs/principles/architectural-health-during-tdd.md`
6. `docs/principles/methodology-coherence.md`（方法论协作 / 反替代规则 / Phase × profile 激活表）

## 适合谁

HarnessFlow 面向那些希望让 AI Agent 承担**从一个 idea 到产品落地**的严肃工程工作的团队和开发者。它尤其适合这些场景：

- 你希望 agent 在 idea 阶段就进行结构化产品洞察（JTBD / OST / Desired Outcome），而不是凭感觉上手
- 你希望架构设计做得**厚**——Bounded Context / Ubiquitous Language / Event Storming / NFR QAS / 轻量威胁建模都落在可评审工件上
- 你希望工作流边界更清晰，中间状态可评审
- 你希望不同工件之间更可追溯（discovery → spec → design → tasks → code → tests）
- 你希望 agent 在真实仓库里的多步执行更安全、更可恢复
- 你希望跨会话恢复更容易；router 能从磁盘工件恢复编排，而不是靠聊天记忆

## 当前状态

HarnessFlow 当前以 coding workflow pack 为主体，Phase 0 已把产品洞察与架构设计两层打厚（JTBD / OST / RICE / Desired Outcome / QAS / DDD / Event Storming / STRIDE / `hf-experiment`）。向「商用级交付」方向的后续演进（发布、运维、度量、协作、长期架构健康、数据 / AI 产品分支）已在规划中，但当前尚未落地。

这个仓库包含当前 HF skill family、共享文档、模板，以及支撑这套 pack 的原则文档（含方法论协作与 phase / profile 激活地图 `docs/principles/methodology-coherence.md`）。

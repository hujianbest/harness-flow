# Architectural Health During TDD

- 关联:
  - 灵魂文档（最高锚点）: `docs/principles/soul.md`
  - SDD + TDD 设计原则: `docs/principles/hf-sdd-tdd-skill-design.md`
  - 模式前置 vs 浮现: `docs/principles/emergent-vs-upfront-patterns.md`

## Purpose

本文回答一个具体问题：**HF 的编码环节（`hf-test-driven-dev`）除了按 TDD 完成编码外，如何实时维护 clean architecture 和 clean code 的健康度？**

它面向的是 HF 节点设计者与 reviewer，目的是把"实时考虑架构健康"从模糊的口号沉淀为可在 HF 节点之间稳定传递、可被 review/gate 验证的工程契约。

不是把 HF 重做成"架构治理工具链"，也不是把每次编码都升级为大型架构重构；而是在已有的 `gated TDD` 节奏内，引入业界已经验证的少量、稳定的纪律，让"编码"和"持续保持架构健康"成为同一件事。

## One-Line Thesis

`gated TDD + Two Hats + Opportunistic Refactoring + Escalation Boundary` 才能在 HF 中持续保持 clean arch 与 clean code 健康。缺一不可。

## 业界优秀实践综述

### Kent Beck — Two Hats

源：Martin Fowler, *Refactoring* Chapter 2；Kent Beck, *Tidy First?*。

核心：任何时刻只戴一顶帽子——

- **Changer 帽子**：写新行为（在 HF 中对应 RED/GREEN）。允许测试由红变绿，允许加新代码。
- **Refactor 帽子**：保持外部行为不变（在 HF 中对应 REFACTOR）。允许结构变化，但所有测试必须保持绿色。

混戴的代价：结构变化和行为变化纠缠后，任何回滚都变贵；reviewer 也无法分辨某段代码到底在引入新行为还是仅仅在整理结构。

### Martin Fowler — Opportunistic Refactoring + Boy Scout Rule

源：Martin Fowler, [*Opportunistic Refactoring*](https://martinfowler.com/bliki/OpportunisticRefactoring.html)；Robert C. Martin, *Clean Code*。

核心：每次接触代码时把它留得比刚来时更干净一点（"campsite rule"）。这是低摩擦、连续的纪律，不是阶段性的"重构周"。

约束：

- 必须有可信回归保护，否则 opportunistic refactor 等于在散弹枪上做雕花
- 必须有边界，否则会蔓延成 task 范围外的大型重构

### Kent Beck (via Fowler) — Preparatory Refactoring

源：Martin Fowler, [*An example of preparatory refactoring*](https://martinfowler.com/articles/preparatory-refactoring-example.html)；Kent Beck 名言："For each desired change, make the change easy (warning: this may be hard), then make the easy change."

核心：当某个新行为难以以 clean 的方式加入时，先重构出扩展点，再实现新行为。

在 HF 中的位置：preparatory refactor 是一种"在 RED 之前"或"在第二轮 RED 之前"的合法切换，必须戴上 Refactor 帽子单独完成；它不是 GREEN 的延伸。

### Robert C. Martin — Clean Architecture + SOLID

源：Robert C. Martin, *Clean Architecture* / *Clean Code*。

核心：

- **Dependency Rule**：依赖方向只能内向——entities ← use cases ← interface adapters ← frameworks/drivers
- **SOLID**：单一职责、开闭、里氏替换、接口隔离、依赖倒置

在 HF 中的位置：本 skill 不要求重新论证已批准 `hf-design`；但要求实现节点能识别"实现是否在悄悄破坏已批准设计的依赖方向"，识别 architectural smells 并按 escalation 边界处理。

### Building Evolutionary Architectures — Fitness Functions

源：Neal Ford / Rebecca Parsons / Patrick Kua, *Building Evolutionary Architectures*；ArchUnit。

核心：把架构约束自动化为可在 CI 中持续运行的"适应度函数"，让 architectural drift 像功能回归一样可被检测。

在 HF 中的位置：HF 不强制要求项目集成 ArchUnit；但鼓励项目把已批准设计中的关键不变量（如分层方向、模块边界、依赖规则）落到 fitness function 或等价的静态检查中，并在 `hf-design` 与 `hf-code-review` 中作为可引用的 guardrail。

### Architectural Smells Catalogue

源：Garcia/Popescu/Edwards/Medvidovic, *Identifying Architectural Bad Smells*；Lippert/Roock, *Refactoring in Large Software Projects*。

常见 architectural smell：

- **God Class / God Component**
- **Cyclic Dependency**
- **Hub-like Dependency**
- **Unstable Dependency**
- **Layering Violation / Leaky Abstraction**
- **Feature Envy across Modules**

在 HF 中的位置：实现节点必须能识别这些 smell 并在 Refactor Note 中显式标注；reviewer 节点（`hf-code-review`）必须有专门维度审查 architectural health。

### Mikado Method（大型重构）

源：Ola Ellnestam / Daniel Brolund, *The Mikado Method*。

核心：当目标重构太大不能一次完成时，先勘探 dependency graph，再按叶子节点逐步实施，每步都保持系统可运行。

在 HF 中的位置：Mikado-style 重构通常已经超出单个 task 的边界，是 `hf-increment` 的工作；本 skill 只在 Refactor Note 中标记并 escalate，不在 task 内实施。

## HF 的关键设计判断

### 判断 1：把架构健康做成实现节点的内置纪律，而不是新增节点

可选方案对比：

| 方案 | 说明 | 否决理由 |
|---|---|---|
| 新增 `hf-architecture-check` 节点 | 在 RGR 之后、`hf-test-review` 之前插入一个独立 architecture check 节点 | 与 `hf-code-review` 职责重叠，会让 review 链路变成 4 个节点；agents 倾向把它当成"先跳过，回头补"的纸质环节 |
| 把所有架构判断推给 `hf-code-review` | 实现节点不管，reviewer 来管 | reviewer 看到的已经是已实现代码，所有 cleanup 都被推到"返修"里；丧失了 TDD REFACTOR 步的天然窗口 |
| **在 `hf-test-driven-dev` 的 RGR 内显式增加 Architectural Health Check** | 在 REFACTOR 步骤里强制做 Boy Scout / Opportunistic / Preparatory 判断，并把结论沉淀为 Refactor Note | ✅ 选择此方案 |

理由：

- TDD 的 REFACTOR 是天然的"全绿可改结构"窗口，业界共识就在这里做 opportunistic refactor。
- 让实现节点直接处理 task 内的 cleanup，避免每个小 cleanup 都走 review→修订→review 的环。
- 仍由 `hf-code-review` 在结构性问题上把关，但它评的是 Refactor Note + 结果代码，不再要求自己也实施。

### 判断 2：必须显式划清 Escalation 边界

最大的退化模式是：实现节点把任意架构性变更都"顺手"做了，结果设计文档与代码漂移；或者反过来，因为不敢动而忽略明显 smell。

HF 引入三档边界：

| 档 | 范围 | 处理方式 |
|---|---|---|
| **In-task cleanup** | 仅影响 task 触碰文件/小局部模块的 clean code 改进，如 Extract Method、Rename、Replace Magic Number、Remove Dead Code、Decompose Conditional、消除局部重复 | 在 REFACTOR 步直接做，全绿验证，写入 Refactor Note |
| **Documented debt** | 识别到的 architectural smell 范围超过 task，但本轮不应/不能在 task 内修复 | 不在 task 内修，在 Refactor Note 中记 debt + 推荐 escalation |
| **Required escalation** | 涉及修改已批准设计、跨多模块的结构性重构、引入或改变 ADR、改变模块边界或接口契约 | 不在 task 内做。停止当前任务，回到 `hf-workflow-router`，由 router 判断是否进入 `hf-increment` 或回到 `hf-design` |

### 判断 3：Two Hats 必须是 Hard Gate，不只是建议

混戴帽子的代价在 HF 上下文里被放大：

- 同一 commit 既加新行为又改结构 → reviewer 失去判断粒度
- 测试在 GREEN 步骤内被"顺便重写" → fresh evidence 与"测试在测什么"的对应关系断裂
- preparatory refactor 与 RED 步骤混合 → 测试设计 approval 与实际写出的测试不一致

因此 HF 把 Two Hats 写成 Hard Gate，并在 Red Flags 中加入"在同一 RGR 步骤内混戴帽子"。

### 判断 4：Refactor Note 是 first-class 输出，不是可选注释

Refactor Note 必须出现在实现交接块里，原因：

- 让 `hf-code-review` 不再凭直觉判断"这次实现是否做了应做的清理"
- 让 `hf-traceability-review` 能把"实现层 cleanup"与"已批准设计"对齐
- 让 architectural debt 在 `hf-completion-gate` 之前就被显式承载，避免被悄悄带过门禁
- 让真正需要 escalate 的项目自然流向 `hf-increment` / `hf-design`，而不是淤积在代码里

### 判断 5：Clean Arch / SOLID 不重论证，只做 conformance check

`hf-design` 已经负责架构与决策；本 skill 不重新论证 dependency rule、不重新选择 architecture pattern，只做 conformance check：

- 实现是否仍遵循 `hf-design` 中的依赖方向、模块边界、接口契约
- 是否引入了 design 未声明的新模块、新依赖、新跨层调用
- 是否触发了 architectural smells（`G-class` / `cycle` / `layering-violation` / `leaky-abstraction` 等）

如果 conformance 检查 fail，进入 escalation，而不是在 task 内"先修着试试"。

## 推荐的工件最小内容

### Refactor Note 应至少包含

- **Hat Discipline**：本轮是否守住 Two Hats（GREEN 与 REFACTOR 是否在不同步骤内进行；preparatory refactor 是否独立成步）
- **In-task cleanups**：本轮 task 内完成的 cleanup，按 Fowler refactoring vocabulary 命名（Extract Method / Rename / Replace Magic Number / Remove Dead Code / ...）
- **Architectural conformance**：与 `hf-design` 中的依赖方向、模块边界、接口契约是否一致；任何偏离需说明
- **Documented debt**：识别到但未在本 task 内修复的 architectural smells（带 smell 名 + 影响范围 + 推荐 escalation）
- **Escalation triggers**：是否触发需 escalate 的边界（跨模块结构性重构、ADR 变更、模块边界变更）；如有，必须显式说明本轮停止并回 router

### `hf-code-review` 新增的 CR7 维度应至少包含

- **Two Hats Hygiene**：实现是否在 RGR 内守住 Two Hats，cleanup 是否归位到 REFACTOR 步骤
- **Refactor Note 完整性**：Refactor Note 是否覆盖本轮主要触碰范围
- **Architectural Conformance**：实现是否遵循已批准设计的依赖方向、模块边界、接口契约
- **Architectural Smells**：是否识别 `god-class` / `cyclic-dep` / `layering-violation` / `leaky-abstraction` / `feature-envy` 等 smells；识别到的是否被 documented or escalated
- **Boy Scout Compliance**：触碰范围内是否仍然留有明显 clean code smells（重复、魔法数字、长函数、命名不清）

## 与既有 HF skill 的关系

| Skill | 与本设计的关系 |
|---|---|
| `hf-design` | 仍是架构权威源；本节点不重新决策架构，只做 conformance check |
| `hf-test-driven-dev` | 主载体；新增 Architectural Health Check 步骤，扩充 Refactor Note 字段 |
| `hf-code-review` | 新增 CR7 维度（Architectural Health & Refactoring Hygiene）与对应 anti-patterns（CA6-CA10） |
| `hf-traceability-review` | 不变；通过 Refactor Note 获得更稳定的实现-设计对齐证据 |
| `hf-increment` | 接收 escalation：跨模块结构性重构、ADR 变更、模块边界变更都走这里 |
| `hf-hotfix` | 不变；`Minimal Safe Fix Boundary` 已经禁止热修复中夹带重构 |
| `hf-bug-patterns` | 不变；可消化重复出现的 architectural smell 作为长期模式 |

## 反模式

以下做法会让"实时维护架构健康"的设计很快退化：

- 把 architectural review 全部下沉到 `hf-code-review`，REFACTOR 步沦为空话
- 在 GREEN 同步骤内捎带重构，让 reviewer 与 fresh evidence 失去对应关系
- 把跨模块、跨 feature 的大型重构在 task 内默默做掉，绕过 `hf-increment`
- Refactor Note 只写"做了一些 cleanup"，无 vocabulary、无影响范围、无 debt/escalation 标记
- 因为"测试全绿"就放过明显 architectural smell
- 把 preparatory refactor 当成 RED 的延伸，跳过测试设计 approval step
- 为了"显得清理充分"而引入 design 未声明的新抽象层（违反 YAGNI 与 Clean Arch dependency rule）

## Bottom Line

HF 在编码环节维护架构健康的关键不是"再加一个节点"，而是：

- **Two Hats** 让结构变化和行为变化天然分离
- **Opportunistic + Boy Scout** 让 task 内 cleanup 不再被推迟
- **Preparatory Refactoring** 让"难加的新行为"不再演化为 hack
- **Escalation Boundary** 让超 task 范围的架构变更走 `hf-increment` 而不是淤积在代码里
- **Refactor Note** 让 reviewer 与 gate 能稳定看见架构健康证据，而不是凭直觉判断

这就是本设计要在 `hf-test-driven-dev` 与 `hf-code-review` 中落地的全部内容。

> 冲突仲裁：本文件与 `docs/principles/soul.md` 出现冲突时，以 soul 为准。

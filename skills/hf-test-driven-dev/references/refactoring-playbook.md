# Refactoring Playbook

**何时加载此参考**：在 `hf-test-driven-dev` 的 REFACTOR 步骤、写 Refactor Note 之前，或当你不确定一个清理动作属于 in-task / debt / escalation 哪一档时。

主契约仍以 `../SKILL.md` 为准；本文件提供 industry-grade 的纪律、术语与边界判断，避免每次实现都把"重构"当成模糊口号。

## 概述

TDD 的 REFACTOR 不只是"代码全绿后随便整理一下"。在 HF 中，REFACTOR 是天然的 **Two Hats / Opportunistic / Preparatory** 重构窗口，也是把 architectural smell 标记并 escalate 的窗口。

核心铁律：

```
1. 同一时刻只戴一顶帽子（Changer 或 Refactor），不混戴
2. 没有可信回归证据，不做 opportunistic refactor
3. 跨 task 范围的架构性重构不在 task 内做，escalate 到 hf-increment
4. 所有 cleanup 都必须落到 Refactor Note，不留隐性变更
```

## 帽子纪律（Two Hats Discipline）

源：Kent Beck / Martin Fowler, *Refactoring* Chapter 2；Kent Beck, *Tidy First?*。

| 帽子 | 允许做什么 | 禁止做什么 | HF 中的位置 |
|---|---|---|---|
| **Changer 帽** | 写新行为；让红测试变绿；可能让旧绿测试变红 | 修改无关结构、提取抽象、重命名公开符号 | RED → GREEN |
| **Refactor 帽** | 改结构、改命名、消除重复、提取/内联；保持所有测试绿 | 添加新行为、改变接口语义、修改测试预期 | REFACTOR；preparatory refactor 时也戴这顶 |

切换帽子的硬约束：

- 每次切换都应是清晰的步骤切换（commit 边界、心智模式边界）。
- preparatory refactor 必须在 RED 之前完成且独立成步，不能"边写测试边重构"。
- GREEN 步骤里出现"顺便重构"是 **红灯信号**，立即停下，回到帽子纪律。

混戴帽子的代价（HF 上下文中被放大）：

- 同 commit 内既加新行为又改结构 → reviewer 失去判断粒度
- 测试在 GREEN 里被"顺便重写" → fresh evidence 与"测试在测什么"的对应关系断裂
- preparatory refactor 与 RED 步骤混合 → 测试设计 approval 与实际写出的测试不一致

## Boy Scout Rule（露营守则）

源：Robert C. Martin, *Clean Code*。

> Always leave the campsite cleaner than you found it.

在 HF 中的落地：每次 task 触碰过的文件，离开时 clean code 健康度必须不退化。

最小判别清单：

- 触碰过的函数仍然有 magic number / 死代码 / 长函数 → 触发 Boy Scout cleanup
- 触碰过的命名仍然不清 → 触发 Rename
- 触碰过的局部出现重复 → 触发 Extract / 消除重复
- 触碰过的条件嵌套 ≥ 3 层 → 触发 Decompose Conditional / Replace Nested Conditional with Guard Clauses

边界：

- 只清扫 task 触碰过的范围，不主动巡视无关文件
- 任何超出触碰范围的清理都不是 Boy Scout，是 in-task 范围扩张，应被拒绝或走 escalation

## Opportunistic Refactoring（机会式重构）

源：Martin Fowler, [*Opportunistic Refactoring*](https://martinfowler.com/bliki/OpportunisticRefactoring.html)。

定义：在你"刚好接触到这块代码"时顺手把它清理一下，因为这是成本最低的时机。

HF 中的执行规则：

- 必须在所有任务测试 + 相关回归都为绿之后再做（即只在 REFACTOR 步骤内）
- 必须戴 Refactor 帽，不引入新行为
- 必须可在 Refactor Note 中按 Fowler vocabulary 命名
- 必须能用 task 触碰范围解释；解释不通就停下

何时不做 opportunistic refactor：

- 测试不可信或回归不全 → 先补回归证据，不要碰结构
- 重构会让 task diff 失控（diff 巨大、reviewer 难以判断粒度）→ 拆出来走 `hf-increment`
- 看上去像 cleanup，其实在改 ADR、模块边界或对外契约 → escalation，不是 cleanup

## Preparatory Refactoring（预备式重构）

源：Martin Fowler, [*An example of preparatory refactoring*](https://martinfowler.com/articles/preparatory-refactoring-example.html)；Kent Beck：

> For each desired change, make the change easy (warning: this may be hard), then make the easy change.

HF 中的位置：

- 当某个 task 的新行为在当前结构下"难加得不像话"时，先做一轮 preparatory refactor，把扩展点抽出来。
- preparatory refactor 必须在 RED 之前完成；它不是 GREEN 的延伸。
- 仍然戴 Refactor 帽；所有现有测试必须在 preparatory refactor 完成后保持绿色。
- 然后再开始 task 的 RED → GREEN → REFACTOR 主循环。

判断信号：

- 新行为难以放进任何现有模块/函数（不是命名问题，是位置问题）
- 新行为只能用 if/else 加 flag 暴力嫁接，且嫁接点在两个职责模糊的模块边界上
- 已批准设计假设了某个扩展点，但当前实现还没把扩展点抽出来

如果 preparatory refactor 本身需要改变模块边界、跨多模块、或改 ADR → 不在 task 内做，escalate 到 `hf-increment`。

## In-task Refactoring 词汇表（基于 Fowler）

写 Refactor Note 时，按以下 vocabulary 命名你做的清理；不要写"做了些清理"或"整理了一下结构"。

| Refactoring | 适用信号 | 边界 |
|---|---|---|
| Extract Method / Extract Function | 函数过长、单函数承担多个抽象层级 | 仅在 task 触碰范围内 |
| Inline Method / Inline Variable | 间接层无价值，名字反而模糊语义 | 不要内联仍被外部使用的接口 |
| Rename Method / Rename Variable | 名字与行为不符 / 名字带误导 | 公开 API 重命名是 documented debt 或 escalation，不是 in-task |
| Replace Magic Number with Symbolic Constant | 出现裸数字且语义不显然 | 在 task 触碰文件内 |
| Decompose Conditional | 复杂 if/else 链可读性差 | 不引入新分支语义 |
| Replace Nested Conditional with Guard Clauses | 嵌套 ≥ 3 层 | 不改变行为 |
| Remove Dead Code | 已无调用方、已被新分支替代 | 必须确认无外部反射 / DI 调用 |
| Consolidate Duplicate Conditional Fragments | 多分支共用前/后置代码 | 在同函数内 |
| Extract Variable | 复杂表达式难命名 | 仅命名清晰化 |
| Slide Statements | 局部顺序导致难懂 | 不改变行为 |

超出 task 触碰范围或会改变模块边界的更大型重构（Move Function / Move Class / Extract Class / Extract Module / Change Function Declaration of public API），属于 documented debt 或 required escalation。

## Architectural Smells 速查表

源：Garcia/Popescu/Edwards/Medvidovic, *Identifying Architectural Bad Smells*；Lippert/Roock, *Refactoring in Large Software Projects*。

| Smell | 识别信号 | 在 HF 中的处理 |
|---|---|---|
| `god-class` / `god-component` | 单类/单模块承担明显多种职责，方法/属性数量远超同层平均 | documented debt 或 escalation；不在单 task 内拆 |
| `cyclic-dep` | 模块 A → B 且 B → A，或更长的循环链 | 通常 escalation；只有"循环边纯属本 task 误引入"时才能 in-task 撤回 |
| `hub-like-dep` | 单模块同时被极多模块依赖且依赖极多模块 | documented debt；通常 escalation |
| `unstable-dep` | 稳定模块依赖不稳定模块（违反 SDP） | documented debt 或 escalation |
| `layering-violation` | 内层调用外层 / 跨层直连 | escalation；违反 Clean Arch dependency rule |
| `leaky-abstraction` | 抽象暴露内部实现细节，调用方依赖实现而非接口 | documented debt 或 escalation |
| `feature-envy-cross-module` | 模块 A 的代码大量依赖模块 B 的内部数据 | documented debt 或 escalation |
| `over-abstraction` | 设计中没声明的新抽象层在 task 内被引入 | 拒绝（违反 YAGNI），回退到设计声明的边界 |

写 Refactor Note 时，每条识别到的 smell 必须包含：

- smell 名（来自上表）
- 影响范围（仅本 task 触碰范围 / 本模块 / 跨模块）
- 处理方式（in-task fixed / documented debt / required escalation）
- 若是 escalation，写明 escalate 到 `hf-increment` 还是 `hf-design`

## Escalation 边界（hard rules）

| 触发条件 | 处理 |
|---|---|
| 重构涉及修改已批准 `hf-design` 的模块边界 / 接口契约 / 数据模型 | 停止 task，回 `hf-workflow-router`，路由到 `hf-increment` 或 `hf-design` |
| 重构会创建 / 修改 / 废弃 ADR | 停止 task，回 router；ADR 状态由 `hf-design` 节点维护 |
| 重构跨 ≥ 3 个模块或包 | 停止 task，escalate 到 `hf-increment` |
| 重构需要修改大量现有测试（远超本 task 测试设计范围） | 高度可疑：要么帽子混戴，要么是 escalation；停下来判断 |
| 重构会引入设计中未声明的新抽象层 | 拒绝（违反 YAGNI 与 Clean Arch 的 disciplined dependency rule） |
| 已识别的 architectural smell 范围超过 task 触碰文件 | documented debt 或 escalation，不在 task 内"顺手"修 |

Escalation 时不能"先修着试试再说"。修了再 escalate 等于污染了 fresh evidence。

## Mikado Method（用于 escalate 出去后）

源：Ola Ellnestam / Daniel Brolund, *The Mikado Method*。

当 escalate 后的重构本身比较大，`hf-increment` 会用 Mikado 风格分解：

1. 设定目标（target node）
2. 不做修改先 attempt，记录所有"想做但被卡住"的前置项作为子目标
3. 回滚 attempt
4. 对每个子目标递归 1-3
5. 反向从叶子开始执行，每步都保持系统可运行

本 skill 不实施 Mikado；只在 Refactor Note 的 escalation 项中标记"建议按 Mikado 拆解"或类似指引，把 baton 交给 `hf-increment`。

## Architectural Fitness Functions

源：Neal Ford / Rebecca Parsons / Patrick Kua, *Building Evolutionary Architectures*；ArchUnit (JVM)、ts-arch (TS/JS)、import-linter (Python)、go-cleanarch (Go)、ndepend (.NET)。

HF 不强制项目集成 fitness functions；但鼓励：

- 已批准 `hf-design` 中的关键不变量（分层方向、模块边界、依赖规则）落到 fitness function 或等价静态检查
- 在 task 验证命令中包含这些检查（例如 `pytest -m architecture` / `archunit-test` / `import-linter`）
- 若项目已配置 fitness function，REFACTOR 步必须把 fitness function 跑一遍并写入 GREEN evidence

若 fitness function 转红：与任何回归相同——这是有效 RED 信号，必须修，不能宣称完成。

## Pattern Emergence（GoF 模式只能在 REFACTOR 步以 Fowler vocabulary 浮现）

源：Joshua Kerievsky, *Refactoring to Patterns*；Kent Beck, *TDD by Example* 后记；Martin Fowler, *Refactoring*。治理立场：`docs/principles/emergent-vs-upfront-patterns.md`。

HF 的立场：

- **领域语义驱动的模式**（Aggregate / Value Object / Repository / Domain Service / Application Service / Domain Event）→ **前置决策**，在 `hf-design` § 4.5 锁定
- **GoF 代码模式**（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton / Composite / Command / Template Method / Visitor 等）→ **emergent 浮现**，在本 skill 的 REFACTOR 步以 Fowler refactoring 的结果形式出现，**不前置决策**

### 测试设计 approval 与 SUT Form 声明的耦合

测试设计 approval 中声明的 `SUT Form` 决定了本轮 RGR 的合法范围：

| SUT Form 声明 | 允许在 RED/GREEN 步出现的实现形态 | REFACTOR 步允许浮现的形态 |
|---|---|---|
| `naive` | 单函数 / 单类 / 简单过程；无模式 | 任意 Fowler vocabulary cleanup；若浮现出 GoF 形态（如 Replace Conditional with Polymorphism → Strategy），记入 Pattern Actual |
| `pattern:<tactical>` | 仅允许该战术模式（Aggregate / VO / Repository / Domain Service / Application Service / Domain Event）的骨架 | 同上；GoF 级浮现合法 |
| `emergent` | 直写最小实现，不预判任何形态 | 按实际 cleanup 需要浮现结构 |

**禁区**：`SUT Form` 声明中写 `pattern:Strategy / pattern:Factory / pattern:Adapter / ...` 等 GoF 名——不合法。若你觉得本轮"需要"某个 GoF 模式：

1. 先把声明改成 `emergent`
2. RED/GREEN 走最小实现
3. REFACTOR 步如果 Fowler refactoring（Replace Conditional with Polymorphism / Extract Factory Method / Extract Interface / Introduce Null Object / ...）**自然**导向某个 GoF 形态，再把"实际浮现"的模式名写入 Refactor Note 的 `Pattern Actual` 字段
4. 若该浮现跨 ≥ 3 模块 / 改 ADR / 改模块边界 → escalate，不在 task 内做

### 允许的 Fowler → GoF 浮现链（举例，不穷举）

| Fowler Refactoring | 可能浮现的 GoF 形态 | 判断信号 |
|---|---|---|
| Replace Conditional with Polymorphism | Strategy / State | 多个 if/switch 分支按类型分发且分支数稳定 |
| Extract Factory Method | Factory Method | 构造过程含 if/switch + 多态返回 |
| Introduce Parameter Object | —（不是 GoF） | 参数列表过长且参数之间有语义关联 |
| Extract Interface | —（多见于 DIP conformance，非独立 GoF） | 实现需替换或测试需 mock |
| Introduce Null Object | Null Object | 大量 null 检查重复 |
| Extract Class + Move Method | Composite / Decorator / Adapter | 结构层面职责重新归属 |

### 红线

- RED/GREEN 步直接引入 Strategy / Factory / Adapter 等 GoF 模式 → 帽子混戴 + 绕过 sut_form 声明锁，**立即停下**，把 sut_form 改为 `emergent`，重做 RED/GREEN 为最小实现，然后在 REFACTOR 步按 Fowler 浮现
- 浮现的 GoF 模式需要改 `hf-design`、改 ADR、跨 ≥ 3 模块 → escalation，不在 task 内做
- "未来可能要支持更多类型" 作为浮现理由 → 拒绝；浮现必须由**当前 task 内已出现的重复 / 分支 / 嫁接点**驱动，而不是未来假设（YAGNI）
- Refactor Note 的 `Pattern Actual` 字段空白或写 "optimized a bit"，但 diff 里能看到新抽象层 → documented-refactor 违规

## SOLID Conformance Check（不重论证，只做检查）

源：Robert C. Martin, *Clean Architecture*。

REFACTOR 步骤的最后做一次 conformance pass（针对 task 触碰范围）：

| 原则 | 检查信号 | 不通过时的动作 |
|---|---|---|
| **SRP** | 一个类/函数同时承担多个稳定变化原因 | 若可在 task 范围内 Extract Method/Class 修复，做；否则 documented debt |
| **OCP** | 加入新行为时被迫修改大量已稳定模块 | 若 design 已声明扩展点但未抽出 → preparatory refactor；若 design 未声明 → escalate |
| **LSP** | 子类破坏父类契约 / 抛与父类不兼容的异常 | escalate；这是 design 层问题 |
| **ISP** | 客户被迫依赖它不使用的方法 | documented debt 或 escalate |
| **DIP** | 高层模块直接依赖低层具体实现，违反已批准依赖方向 | escalate；violates Clean Arch dependency rule |

不在 task 内重论证 SOLID 是否适用；它已经由 `hf-design` 在架构层确定。

## Refactor Note 模板

写入实现交接块的 `Refactor Note` 区段。最少必填字段如下：

```md
### Refactor Note

- Hat Discipline: <RGR 是否守住 Two Hats；是否有独立 preparatory refactor 步骤>
- SUT Form Declared: <approval 中声明的 sut_form：naive | pattern:<tactical name> | emergent>
- Pattern Actual: <REFACTOR 后 SUT 实际形态：naive-unchanged | pattern:<tactical name, 承接 design § 4.5> | emergent→<Fowler vocabulary 链, e.g. Replace Conditional with Polymorphism → Strategy> | emergent-unchanged>
- SUT Form Drift: <声明 vs 实际：一致 | Fowler 触发的合法浮现 | 不一致 - 需解释>
- In-task Cleanups:
  - <Fowler vocabulary> @ <文件:范围> — <一行说明>
  - ...
- Boy Scout Touches:
  - <文件:范围> — <清理类型>
- Architectural Conformance:
  - <与 hf-design 中依赖方向 / 模块边界 / 接口契约的一致性结论>
- Documented Debt:
  - <smell 名> @ <影响范围> — <为什么不在本 task 内修>
- Escalation Triggers:
  - <None | escalate to hf-increment | escalate to hf-design via hf-workflow-router>
- Fitness Function Evidence:
  - <如项目存在 fitness function：命令 + 结果摘要；不存在则写 not-configured>
```

写不出 vocabulary、写不出影响范围、写不出 escalation 决定 → 回去想清楚再写。

**Pattern Actual 的合法写法举例**：

- `naive-unchanged`（声明 naive，实际仍是朴素实现）
- `emergent → Replace Conditional with Polymorphism → Strategy`（声明 emergent，REFACTOR 浮现了 Strategy 形态）
- `pattern:Aggregate (Order) + pattern:Repository (OrderRepository)`（声明 pattern:Aggregate，实际承接 design § 4.5 的 Order 聚合 + 其 Repository）
- `emergent → Introduce Null Object`（声明 emergent，REFACTOR 浮现了 Null Object）

**Pattern Actual 的非法写法举例**：

- 空白 / `optimized`（模糊，违反 vocabulary 要求）
- `pattern:Strategy`（在 sut_form 声明中 allowlist 外；GoF 只能作为浮现结果出现，不作为声明）
- `refactored for extensibility`（未绑定具体 Fowler vocabulary）

## Common Excuses（红灯信号）

| 借口 | 现实 |
|---|---|
| "顺手在 GREEN 里改一下结构而已" | 帽子混戴。停下，回到帽子纪律 |
| "测试不全但小重构应该没事" | 没有可信回归就不能 opportunistic refactor |
| "范围有点超 task，但都改完了再说" | task 范围扩张 + 跳过 escalation；废弃这次 cleanup |
| "ADR 里没写但我觉得这样更 clean" | 违反 YAGNI 与 design 权威。escalate 或不做 |
| "顺手把模块边界也调了" | escalation 触发条件，不能在 task 内做 |
| "Refactor Note 写'做了些清理'就够了" | 不够。必须 vocabulary + 范围 + escalation 决定 |
| "fitness function 红了但和我无关" | 在 task 触碰范围内的红灯就是有效 RED；要么修，要么 escalate，不能跳过 |
| "sut_form 写 pattern:Strategy 比较清楚" | 不合法。sut_form 的 pattern:<name> allowlist 只含 design § 4.5 战术模式；GoF 模式只能作为 Pattern Actual 浮现结果出现，立场见 `docs/principles/emergent-vs-upfront-patterns.md` |
| "既然要浮现出 Strategy，RED 直接用 Strategy 接口写测试不是更高效吗" | 帽子混戴 + 绕过 sut_form 声明锁。改 sut_form 为 emergent，RED/GREEN 走最小实现，REFACTOR 步让 Fowler refactoring 浮现 Strategy |
| "未来可能要支持更多类型，先把抽象层留出来" | YAGNI 违规 + over-abstraction (CA9)。浮现必须由当前 task 内已出现的重复 / 分支 / 嫁接点驱动 |
| "Pattern Actual 写 'refactored for extensibility'" | 未绑定 Fowler vocabulary；和"做了些清理"一样模糊，不合格 |

## 速查决策表

```
看到一个改进机会
  ↓
该机会是否在 task 触碰范围内？
  否 → 不做（不是 Boy Scout，是越界）
  是 ↓
是否会改 ADR / 模块边界 / 接口契约 / 跨 ≥3 模块？
  是 → required escalation：停 task，回 router
  否 ↓
当前所有相关测试 + fitness function 是否都为绿？
  否 → 先补回归证据，不做 opportunistic refactor
  是 ↓
是否仍戴着 Changer 帽（在 RED/GREEN 步骤内）？
  是 → 不做。等到 REFACTOR 步再说
  否 ↓
能否用 Fowler vocabulary 命名这个 cleanup？
  否 → 想清楚再做；模糊的清理 = 隐性变更
  是 ↓
做。然后写入 Refactor Note 的 In-task Cleanups。
```

## Bottom Line

REFACTOR 不是 RGR 的尾声装饰，而是 HF 在编码节奏内维护 clean arch + clean code 健康的主战场。

- **Two Hats** 决定可不可以做
- **Boy Scout / Opportunistic / Preparatory** 决定怎么做
- **Architectural smells + SOLID conformance + escalation 边界** 决定能不能在 task 内做
- **Refactor Note** 决定别人能不能验证你做了

四件事缺一不可。

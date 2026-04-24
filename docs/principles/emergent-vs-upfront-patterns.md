# Emergent vs Upfront Patterns（HF 对"何时前置决策 / 何时 emergent 浮现"的立场）

## Purpose

HF 讨论"设计模式"时，必须先区分**哪一档模式**再谈"什么时候决策"。

本文回答一个具体问题：**HF 在写代码前应该把哪些模式想清楚、哪些模式刻意不前置？为什么？**

它是一份**立场文档 + 治理规则**，用于：

- 防止 agent / 贡献者把"写代码前考虑好设计模式"粗暴理解为"把所有 GoF 模式都在 design 里前置选好"
- 让 `hf-design` 的战术建模、`hf-test-driven-dev` 的 SUT Form 声明、`hf-design-review` 的反模式 A11 有统一的理论锚点
- 作为未来新增方法论时的**前置判别器**：新方法论属于"前置决策"还是"emergent 浮现"？

本文是治理文档，不是新的 skill。

## One-Line Thesis

**领域语义驱动的模式前置决策；实现细节驱动的模式 emergent 浮现。**

换句话说：

- 能从业务语言读出的模式（Aggregate / Value Object / Repository / Domain Service / Application Service / Domain Event）→ `hf-design` 锁定
- 必须在代码重复 / 分支嫁接点 / 扩展摩擦出现后才能正确选择的模式（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton / ...）→ `hf-test-driven-dev` REFACTOR 浮现

## 四档模式分类

HF 在讨论 "设计模式" 时区分四档：

| 档位 | 例子 | 决策时机 | HF 中的归属 |
|---|---|---|---|
| **架构模式** | Monolith / Modular Monolith / Microservices / Layered / Event-Driven / Plugin / Hexagonal | **前置决策** | `hf-design` Step 2（按 `references/architecture-patterns.md`） |
| **DDD 战术模式** | Entity / Value Object / Aggregate / Repository / Domain Service / Application Service / Domain Event | **前置决策** | `hf-design` Step 2.7（按 `references/ddd-tactical-modeling.md`） |
| **GoF 代码模式** | Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton / Composite / Command / Template Method / Visitor / Chain of Responsibility / Iterator / Mediator / Memento / Prototype / Proxy / State | **emergent 浮现** | `hf-test-driven-dev` REFACTOR 步按 Fowler vocabulary 浮现 |
| **惯用法 / Idioms** | RAII（C++）/ Option-Result（Rust）/ Guard Clause / Null Object / With-Statement（Python）| **emergent 浮现** | 同上；通常在 in-task cleanup 中自然出现 |

## 为什么这样切？

### 论据 1：Beck / Fowler / Kerievsky 三人一致反对前置 GoF 选择

- **Kent Beck** *TDD by Example* 后记：设计模式在 TDD 节奏中是 **REFACTOR 的结果**，不是 RED 的起点。测试应该表达需要的行为，实现随 refactoring 演化，模式在演化中浮现。
- **Martin Fowler** *Refactoring*：Fowler vocabulary（Extract Method / Replace Conditional with Polymorphism / Introduce Null Object / ...）与 GoF 模式的关系——**你做 Fowler refactoring，GoF 模式是你路过的站**，不是你出发前的目的地。
- **Joshua Kerievsky** *Refactoring to Patterns*：整本书的命题就是"不要往模式冲、往模式走"——让代码重复 / 分支嫁接点 / 扩展摩擦告诉你需要哪个模式。

### 论据 2：HF 已有护栏 `CA9 over-abstraction` 本就在拦截 GoF 前置

`hf-code-review` 的 `CA9 over-abstraction`（见 `skills/hf-code-review/references/clean-architecture-guardrails.md`）已经定义：

> 引入 design 未声明的新抽象层 / 新接口 / 新基类，理由是 "未来可能有用" → critical finding

任何把 GoF 模式作为 design 前置决策的做法，都会在实现时退化为 `CA9` 的触发源——因为 design 写了 "用 Strategy"，实现就不得不引入 Strategy 抽象层，哪怕当前只有 1 种实现。这是 over-abstraction 的教科书场景。

前置决策 GoF 与 `CA9` 在结构上互相冲突，不能同时存在。

### 论据 3：领域语义不需要 "重复信号" 才能看出

与 GoF 模式不同，战术模式的选择来自**业务语言**而不是**代码形态**：

- "订单一旦提交，库存必须同步扣减" → 这是 **Aggregate 内不变量**（前置可读）
- "金额不能为负" → 这是 **Value Object 的构造校验**（前置可读）
- "订单提交后通知仓储系统" → 这是 **Domain Event**（前置可读）

这些判断在看到任何代码之前就能做出，且一旦做错（例如把跨聚合一致性写成一次事务）后续重构成本极高。所以前置决策是合理的。

### 论据 4：TDD 的 REFACTOR 是天然的模式浮现窗口

`docs/principles/architectural-health-during-tdd.md` 判断 1 已经论证：REFACTOR 是"全绿可改结构"的天然窗口。GoF 模式浮现与 Boy Scout / Opportunistic refactoring 属于同一类活动，没必要为它单独新增节点。

## HF 中的落地规则

### 在 `hf-design`

- **必填**：Step 2（架构模式）+ Step 2.7（DDD 战术模式，触发条件满足时）
- **禁止**：在设计文档中列出 GoF 模式作为前置决策候选。设计文档 § 4.5 只写战术模式；§ 9（选定方案与关键决策）可以讨论战术模式的权衡，但**不讨论 GoF**
- **反模式 ID**：`A11 upfront-gof-pattern`（见 `hf-design-review/references/review-checklist.md`）

### 在 `hf-test-driven-dev`

- **测试设计 approval 中的 SUT Form 声明**：`naive` / `pattern:<tactical>` / `emergent` 三选一
- **`pattern:<name>` 的 allowlist**：只含 `Aggregate` / `ValueObject` / `Repository` / `DomainService` / `ApplicationService` / `DomainEvent`（即 design § 4.5 内容）
- **禁止**：在 sut_form 声明中写 `pattern:Strategy` / `pattern:Factory` / `pattern:Adapter` / `pattern:Observer` / `pattern:Decorator` 等 GoF 名
- **允许**：REFACTOR 步以 Fowler vocabulary 浮现 GoF 形态（例如 Replace Conditional with Polymorphism → Strategy），回写到 Refactor Note 的 `Pattern Actual` 字段
- **浮现的约束**：必须由当前 task 内已出现的重复 / 分支 / 嫁接点驱动；不允许"未来可能需要"作为浮现理由

### 在 `hf-code-review`

- 已有 `CR7.4 Architectural Smells Detection` + `CA9 over-abstraction` 足够拦截违规浮现
- 新增对 Refactor Note 的 `SUT Form Declared / Pattern Actual / SUT Form Drift` 三字段的评审——reviewer 对照 approval 与 Refactor Note 判断是否有绕过 sut_form 声明锁

## 决策流程（agent 执行时的判断链）

```
遇到一个"要不要用某个模式"的判断
  ↓
它是架构模式（Monolith / Event-Driven / Plugin / ...）吗？
  是 → hf-design Step 2 前置决策
  否 ↓
它能从业务语言读出吗（业务实体 / 业务不变量 / 业务事件）？
  是 → 属于 DDD 战术模式，hf-design Step 2.7 前置决策
  否 ↓
它是 GoF 代码模式或语言惯用法吗？
  是 → 不前置。hf-test-driven-dev 的 sut_form 声明为 emergent，REFACTOR 步按 Fowler vocabulary 浮现
  否 → 回到前三档判断；如果都不是，可能是错误范畴（例如把基础设施选型当成"模式"）
```

## "前置决策"的判别清单

一个候选"模式"该被前置决策，必须同时满足：

1. **业务语言可读**：用业务人员的语言能描述出这个选择（不是"用 Strategy 还是 Template Method"）
2. **跨时间稳定**：它反映的业务语义在整个 feature 生命周期内不轻易变化
3. **错了成本高**：选错后的重构需要跨模块 + 改 ADR + 可能破坏事务边界或一致性契约
4. **与运行时状态 / 代码重复信号无关**：不需要看到具体代码重复就能做出判断

全部满足 → 前置决策（战术 / 架构层）。
任一不满足 → emergent 浮现（实现层）。

## "emergent 浮现"的判别清单

一个候选"模式"该 emergent 浮现，通常符合以下任一：

1. **需要代码重复信号**：只有看到 3+ 处相似分支才能判断是否需要 Strategy
2. **需要扩展点摩擦信号**：只有加新行为时感到摩擦，才能判断是否需要 Factory / Adapter
3. **关乎实现细节**：反映的是类 / 函数 / 对象生命周期的细节（Builder 是否优于构造器、Iterator 是否优于裸循环）
4. **没有稳定业务语义对应**：业务人员不关心这里用的是 Observer 还是直接回调

## 常见误区

| 误区 | 正确理解 |
|---|---|
| "在 design 里列出 Strategy / Factory 更清楚，免得实现时抓瞎" | 相反：前置列出会把实现锁死在未经验证的抽象上，违反 YAGNI 与 CA9 |
| "战术模式和 GoF 都是'模式'，应该统一处理" | 两者决策时机不同、信号来源不同。统一处理等于在两边都做错 |
| "既然 GoF 要 emergent，那 sut_form 写 emergent 就是偷懒" | `emergent` 是合法且常见的默认选项，不需要道歉 |
| "emergent 就是'随便写、REFACTOR 时随便改'" | 错。REFACTOR 必须用 Fowler vocabulary 命名；浮现必须由当前 task 内信号驱动 |
| "某些 GoF 模式（如 Null Object）很明显应该前置" | 仍然 emergent。Null Object 的信号是"大量 null 检查重复"，这是代码层信号，等 REFACTOR 步再决定 |
| "战术建模也可以 emergent 吧？反正 TDD 会让它浮现" | 不行。战术模式选错（聚合边界、事务边界）的代价通常是跨模块重构，远超单 task 可承受。这就是为什么战术前置 |

## 反替代规则（写入 `methodology-coherence.md` 的"显式不允许替代"清单）

| 左 | 右 | 规则 |
|---|---|---|
| DDD Tactical Pattern 前置决策 | GoF Pattern 前置决策 | 两者**不互相替代**。前者必须前置（触发条件满足时），后者必须 emergent |
| GoF Pattern emergent 浮现 | 省略 REFACTOR 步 | 浮现是 **Fowler vocabulary 驱动的结果**，不是"随便改一改"的同义词；没有 Fowler 命名的浮现 = 未 documented refactor（CA7） |
| `sut_form: pattern:<tactical>` | `sut_form: pattern:<GoF>` | allowlist 只含战术模式；GoF 写入 sut_form = over-abstraction 前置声明 |

## Phase 路线图

- **Phase 0（本文件所在阶段）**：前置 / emergent 边界由治理文档 + `A11` 反模式 + `sut_form` allowlist 共同维护，纯文档级硬门
- **Phase 1**：考虑引入 fitness function，把"design 未声明的抽象层"自动识别（ArchUnit / ts-arch / import-linter 等）为 RED 信号
- **Phase 2**：考虑把 `Refactoring to Patterns` 的 catalog 作为 `refactoring-playbook.md` 的扩展参考，让浮现有更完整的 Fowler → GoF 映射表

## Bottom Line

**"让 HF 在写代码前考虑好设计模式" 不等于 "把所有 GoF 模式前置到 design"。**

正确的读法是：

- **战术模式**（领域语义驱动）必须前置——`hf-design` § 4.5 的 Aggregate / VO / Repository / Domain Service / Application Service / Domain Event
- **架构模式** 必须前置——`hf-design` Step 2
- **GoF 代码模式**（实现细节驱动）刻意 emergent——`hf-test-driven-dev` REFACTOR 步的 Fowler vocabulary 浮现

这是 HF 基于 Beck / Fowler / Martin / Kerievsky 的工程判断，不是疏忽。

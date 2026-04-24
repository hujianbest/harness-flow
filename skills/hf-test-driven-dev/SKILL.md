---
name: hf-test-driven-dev
description: 适用于任务计划获批后的单任务实现、受控 hotfix 修复实现、review/gate 回流修订。不适用于任务计划未批准（→ 上游）、hotfix 无复现路径（→ hf-hotfix）、需并行多任务（→ hf-workflow-router）。
---

# HF 测试驱动开发与实现入口

HF workflow family 唯一实现入口。把单个活跃任务从"准备实现"推进到"已写回新鲜证据与 canonical 下一步"。不是任务循环控制器——跨 task 切换由 `hf-workflow-router` 决定。

三层职责：1) 唯一实现入口 2) TDD 执行入口 3) 向 review/gate 输出证据与 handoff 的交接入口。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **TDD (Test-Driven Development)** | 严格遵循 Red → Green → Refactor 循环 | Kent Beck, 2002 "Test-Driven Development: By Example" | 步骤 4 — 执行有效 TDD |
| **Walking Skeleton** | 优先建立最薄端到端可运行路径 | Alistair Cockburn, "Software Development as a Cooperative Game" | 步骤 4 — TDD 中优先走通关键路径 |
| **Test Design Before Implementation** | 在 Red-Green-Refactor 前完成测试设计 approval step | 项目化实践（HF 质量链约定） | 步骤 2 — 产出测试设计；步骤 3 — approval step |
| **Fresh Evidence Principle** | 所有验证证据必须在当前会话内产生 | 项目化实践（HF 证据链约定） | 步骤 4 — 有效 RED/GREEN；步骤 5 — 交接块 |
| **Two Hats (Kent Beck / Fowler)** | 任一时刻只戴 Changer 帽（写新行为）或 Refactor 帽（保持行为不变改结构），不混戴 | Martin Fowler, *Refactoring* Ch.2；Kent Beck, *Tidy First?* | 步骤 4 — RGR 步骤切分；步骤 4A — REFACTOR 帽下做 cleanup |
| **Opportunistic + Boy Scout Refactoring** | 接触代码时顺手把它留得更干净，但限定在 task 触碰范围且必须有可信回归 | Martin Fowler, *Opportunistic Refactoring*；Robert C. Martin, *Clean Code* | 步骤 4A — REFACTOR 步内 in-task cleanup |
| **Preparatory Refactoring** | 新行为难加时先重构出扩展点，再"做简单的改动"；独立成步、不混入 RED | Kent Beck via Fowler, "make the change easy, then make the easy change" | 步骤 4 — RED 之前的可选 preparatory 步 |
| **Clean Architecture Conformance** | 实现遵循已批准设计的依赖方向、模块边界、接口契约；不重新论证架构决策 | Robert C. Martin, *Clean Architecture*；SOLID | 步骤 4A — Architectural Health Check |
| **Escalation Boundary** | 跨 task 范围的结构性重构、ADR 变更、模块边界变更不在 task 内做，escalate 到 `hf-increment` | 项目化实践（HF 节点边界约定） | 步骤 4A — escalation 触发即停 task；步骤 5 — Refactor Note 标记 |

## When to Use

适用：
- 任务计划获批后的实现（full/standard/lightweight）
- 受控 hotfix 的修复实现
- 来自 bug-patterns/test-review/code-review/traceability-review/regression-gate/completion-gate 的回流修订
- 用户要求"开始实现这个 active task"

不适用：任务计划未批准 → 回上游；hotfix 无复现路径 → `hf-hotfix`；需并行多任务 → `hf-workflow-router`。

前提：存在唯一活跃任务、有已批准计划或 hotfix handoff、能读取 feature `progress.md`（默认 `features/<active>/progress.md`）和规格/设计锚点（默认 `features/<active>/spec.md` / `features/<active>/design.md`）。证据冲突 → 回 router。

## Hard Gates

- 主链实现时，任务计划未获批准前不得开始
- hotfix 实现时，必须有 `hf-hotfix` 的复现路径和最小修复边界
- 当前任务完成质量链前不得切换到下一任务
- 若 worktree-required，动手前必须先准备 worktree
- Red-Green-Refactor 前必须完成测试设计 approval step
- 测试设计 approval 中必须声明 **SUT Form**（`naive` / `pattern:<design § 4.5 战术模式名>` / `emergent`）；`pattern:<name>` 只允许承接已批准 design § 4.5 列出的战术模式，禁止引入 GoF 模式名
- 写回 fresh evidence 和 canonical handoff 前不得声称完成
- **Two Hats**：同一 RGR 步骤内不得混戴 Changer 与 Refactor 帽；GREEN 步内不做 cleanup；preparatory refactor 必须独立成步
- **Escalation Boundary**：跨 ≥3 模块的结构性重构 / 修改 ADR / 修改已批准模块边界或接口契约 / 引入设计未声明的新抽象层 → 立即停 task，回 `hf-workflow-router`，不在 task 内"先修着试试"
- **Refactor Note**：实现交接块必须包含完整 Refactor Note（Hat Discipline / In-task Cleanups / Architectural Conformance / Documented Debt / Escalation Triggers），缺失即视为未完成

## Workflow

### 1. 对齐上下文并锁定唯一活跃任务

读 feature `progress.md`（默认 `features/<active>/progress.md`）的 Current Active Task → 校验任务计划（默认 `features/<active>/tasks.md`）/hotfix handoff → 补读回流 findings → 证据冲突则暂停。

### 1A. 按需准备 worktree

- `worktree-active`：复用 Worktree Path
- `worktree-required`：按当前 skill pack 共享的 worktree isolation guide 准备（默认 `skills/docs/hf-worktree-isolation.md`；若 `AGENTS.md` 声明项目等价路径，优先遵循）
- `in-place`：仅干净工作区时继续
- 准备失败 → fresh blocking evidence，不先改代码再补 worktree

### 2. 产出测试设计并自检

TDD 前先输出测试设计：验证哪些行为、正反向场景、边界条件、预期 I/O、哪些应先失败、测试分层、与测试设计种子的差异。

自检：覆盖关键成功行为？覆盖反向/边界？能抓住"错误但看起来完成了"的实现？mock 限定在真正边界？

**SUT Form 声明（Phase 0 新增）**：在测试设计中**必须**显式声明 SUT（System Under Test）的候选形态，三选一：

- `naive`：直写实现，不引入任何实现层模式（单函数 / 单类 / 简单过程）
- `pattern:<name>`：以某个**已批准 design 中列明**的战术模式承载（Aggregate / Repository / Domain Service / Application Service / Domain Event 发布者）。**只允许承接 design § 4.5 已写明的战术模式**，不允许在此前置引入 GoF 模式
- `emergent`：本轮不预判具体形态，在 REFACTOR 步按实际 cleanup 需要浮现结构（Fowler vocabulary 命名）

**SUT Form 的 allowlist**（唯一允许 `pattern:<name>` 的取值）：

- `pattern:Aggregate / pattern:ValueObject / pattern:Repository / pattern:DomainService / pattern:ApplicationService / pattern:DomainEvent`（源自已批准 design § 4.5）
- **说明**：Entity 作为 Aggregate 内部成员不单独出现在 allowlist 中；若 SUT 对应的是 Aggregate Root Entity，写 `pattern:Aggregate`；若 SUT 是某个 Aggregate 内的非 root Entity，通常说明 task 粒度过细，应该把 SUT 扩到 Aggregate Root
- 以上之外的命名（`pattern:Strategy / pattern:Factory / pattern:Adapter / pattern:Observer / pattern:Decorator / pattern:Builder / pattern:Singleton` ...）→ 退回 `emergent`；这些 GoF 模式必须在 REFACTOR 步按 Fowler vocabulary（Replace Conditional with Polymorphism / Extract Factory Method / ...）emergent 浮现，立场见 `docs/principles/emergent-vs-upfront-patterns.md`

选择 `emergent` 是合法且常见的默认选项，不需要道歉。

### 3. 完成测试设计确认

整理成可回读确认输入。interactive → 展示给真人等待确认；auto → 写 approval record。完成后才能进入 TDD。

approval record 与交接块中**必须**包含声明好的 `SUT Form`；后续 REFACTOR 步的 Refactor Note 必须回写 `pattern_actual` 与声明对照。

### 4. 执行有效 TDD

严格按 Two Hats 切分步骤。每个步骤明确戴哪顶帽子；不混戴。

1. **(可选) Preparatory Refactor — Refactor 帽**：仅当新行为在当前结构下"难加得不像话"时使用；保持现有测试全绿，把扩展点抽出来后停下。详见 `references/refactoring-playbook.md` 的 Preparatory Refactoring 节。
2. **RED — Changer 帽**：先写失败测试 → 运行确认失败原因符合预期。
3. **GREEN — Changer 帽**：写最小实现让测试通过 → 运行确认新通过来自本次会话。**不在 GREEN 步内做任何 cleanup 或重构**——看到 cleanup 机会，记下来等步骤 4A。
4. **REFACTOR — Refactor 帽**：见步骤 4A。

**有效 RED**：会话里真的执行了、失败对应行为缺口、能说清为什么预期失败。

不算有效 RED：只写没跑、一跑就绿、无关旧失败、看不出在证明什么。

**有效 GREEN**：任务测试转绿、证明命令本次会话成功、保留 fresh evidence。

### 4A. 执行 REFACTOR 与 Architectural Health Check

仅在所有任务测试 + 相关回归 + (若项目存在) architectural fitness function 均为绿后进入。戴 Refactor 帽，不引入新行为。

按以下顺序执行，详细规则见 `references/refactoring-playbook.md`：

1. **In-task Cleanups (Boy Scout + Opportunistic)**：仅清扫 task 触碰范围内的 clean code 问题。每条 cleanup 用 Fowler vocabulary 命名（Extract Method / Rename / Replace Magic Number / Remove Dead Code / Decompose Conditional / ...）。每次 cleanup 完成后跑一次完整测试，保持全绿。
2. **Architectural Conformance Check**：对照已批准 `hf-design`（默认 `features/<active>/design.md`）与相关 ADR（默认 `docs/adr/`），逐项确认本轮实现仍遵循：
   - 依赖方向（含 Clean Architecture dependency rule）
   - 模块边界与职责分层
   - 接口契约与不变量
   - 已批准 architecture pattern 的天然限制
3. **Architectural Smells Detection**：对照 `references/refactoring-playbook.md` 的 smells 速查表（god-class / cyclic-dep / hub-like-dep / unstable-dep / layering-violation / leaky-abstraction / feature-envy-cross-module / over-abstraction），逐项确认本轮触碰范围内是否有可见 smell。
4. **Escalation Decision**：对每条识别到的问题，按 `references/refactoring-playbook.md` 的 Escalation 边界归档：
   - **In-task fixed**：可在 task 触碰范围内安全清理 → 上面第 1 步已做
   - **Documented debt**：识别但本轮不修，记入 Refactor Note
   - **Required escalation**：触发 escalation 边界（跨 ≥3 模块 / 改 ADR / 改模块边界或接口契约 / 引入设计未声明的新抽象层）→ **立即停 task**，把当前状态写入 Refactor Note，handoff `hf-workflow-router`，由 router 路由到 `hf-increment` 或 `hf-design`
5. **Fitness Function Re-run**：若项目存在 architectural fitness function（ArchUnit / ts-arch / import-linter / 等），跑一遍并把结果写入 GREEN evidence；红灯按有效 RED 处理，要么修要么 escalate，不能跳过。

**红灯信号**（任一出现立即停下回到 4A 顶部重新走）：

- 在 GREEN 步内做了 cleanup
- 准备做的"小重构"会改 ADR / 模块边界 / 接口契约
- 看似 cleanup 实则在引入设计未声明的新抽象层
- 触碰范围内 fitness function 转红但被 reviewer 写了"和我无关"
- Refactor Note 里写不出 vocabulary、写不出影响范围、写不出 escalation 决定

### 5. 生成实现交接块并同步状态

写回稳定交接块：

```md
## 实现交接块
- Task ID:
- 回流来源: 主链实现 | hf-hotfix | hf-bug-patterns | ...
- 触碰工件:
- Workspace Isolation / Worktree Path / Worktree Branch:
- 测试设计确认证据:
- RED 证据: <命令 + 失败摘要 + 为什么预期失败>
- GREEN 证据: <命令 + 通过摘要 + 关键结果>
- 与任务计划测试种子的差异:
- 剩余风险 / 未覆盖项:
- Pending Reviews And Gates:
- Next Action Or Recommended Skill:

### Refactor Note
- Hat Discipline: <RGR 是否守住 Two Hats；是否有独立 preparatory refactor 步骤>
- SUT Form Declared: <approval 中声明的 sut_form：naive | pattern:<tactical name> | emergent>
- Pattern Actual: <REFACTOR 后 SUT 实际呈现的形态：naive | pattern:<tactical name> | pattern:<Fowler vocabulary, e.g. Replace Conditional with Polymorphism → Strategy> | emergent-unchanged>
- SUT Form Drift: <声明与实际是否一致；不一致时说明触发的 Fowler cleanup 与原因；GoF 模式只能在此处以"实际浮现"的形式出现，不回写到 design>
- In-task Cleanups:
  - <Fowler vocabulary> @ <文件:范围> — <一行说明>
- Boy Scout Touches:
  - <文件:范围> — <清理类型>
- Architectural Conformance: <与 hf-design 中依赖方向 / 模块边界 / 接口契约的一致性结论；偏离需写明理由与可追溯锚点>
- Documented Debt:
  - <smell 名> @ <影响范围> — <为什么不在本 task 内修>
- Escalation Triggers: <None | escalate to hf-increment | escalate to hf-design via hf-workflow-router>
- Fitness Function Evidence: <命令 + 结果摘要；不存在则写 not-configured>
```

Refactor Note 必填规则：

- 即使本轮没有任何 cleanup 也要写：In-task Cleanups 写 `none`，Documented Debt / Escalation Triggers 写 `none`，Hat Discipline 与 Architectural Conformance 仍须显式写结论。
- 出现 Escalation Triggers 非 `none` 时，本轮 `Next Action Or Recommended Skill` 必须为 `hf-workflow-router`，不能为 `hf-test-review`；后续质量链由 router 重新路由。

Next Action 用 canonical skill ID：full/standard 通常 → `hf-test-review`；lightweight 通常 → `hf-regression-gate`；回流修订完成 → 写回触发回流的那个 node。不把下一任务的实现写成输出。若 AI 发现当前问题命中了值得长期沉淀的重复错误，可**额外建议**独立触发 `hf-bug-patterns`，但不要把它写成 HF 主链的 canonical next action。

### 6. 回流修订协议

明确回流来源 → 只修当前活跃任务的相关 findings → 若改行为预期需重做测试设计确认 → 修订后写新 fresh evidence → 不从头重走质量链。

## 和其他 Skill 的区别

| 场景 | 用 hf-test-driven-dev | 不用 |
|------|----------------------|------|
| 任务计划获批后的单任务 TDD 实现 | ✅ | |
| review/gate 回流修订 | ✅ | |
| 任务计划未批准 | | → 上游（`hf-tasks` / `hf-workflow-router`） |
| 热修复但无复现路径 | | → `hf-hotfix` |
| 需并行多任务 | | → `hf-workflow-router` |
| 评审测试质量 | | → `hf-test-review` |
| 评审代码质量 | | → `hf-code-review` |
| 评审追溯完整性 | | → `hf-traceability-review` |

## Red Flags

- 并行处理多个任务
- 未完成测试设计 approval step 就开始写测试
- 先写实现再补失败测试
- 旧绿测结果当当前证据
- completion gate 前就说"做完了"
- 不读 feature `progress.md` 靠印象决定活跃任务
- 把命令日志、性能基线等大体量证据塞进 progress.md / 实现交接块，而不是落到 `features/<active>/evidence/`
- 测试直接通过却没重新定义要抓的行为
- **同一 RGR 步骤内混戴 Changer 与 Refactor 帽**（GREEN 步内做 cleanup、preparatory refactor 与 RED 步骤纠缠）
- **跨模块 / 改 ADR / 改模块边界的"顺手"重构在 task 内被默默做掉**，绕过 `hf-increment`
- **引入设计未声明的新抽象层**，理由是"未来可能用得到"（违反 YAGNI 与 Clean Arch dependency rule）
- **测试设计 approval 中 SUT Form 未声明**，或 approval 后在 GREEN 步直接引入 design 未声明的新 pattern（等于绕过 sut_form 声明锁）
- **声明了 `emergent` 却在 RED/GREEN 步直接引入复杂 pattern**——未走独立的 preparatory refactor 独立步，违反 Two Hats
- **把 GoF 模式名（Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton）作为 `pattern:<name>` 写入 sut_form 声明**——这不合法，只允许承接 design § 4.5 列明的战术模式（Aggregate / VO / Repository / Domain Service / Application Service / Domain Event）；GoF 只能以 Fowler vocabulary 的 REFACTOR 结果形式出现在 Refactor Note 的 Pattern Actual 字段
- Refactor Note 缺失或写成"做了些清理"等模糊表达；缺 vocabulary、缺影响范围、缺 escalation 决定
- Refactor Note 的 SUT Form Declared / Pattern Actual / SUT Form Drift 三字段缺失或含糊，导致 reviewer 无法判断"实际浮现形态 vs 声明形态"
- 触碰范围内可见 architectural smell（god-class / cyclic-dep / layering-violation / leaky-abstraction / feature-envy）被忽略
- 触碰文件离开时 clean code 健康度比进入时更差（违反 Boy Scout Rule）
- 项目存在 architectural fitness function 但本轮 REFACTOR 后未跑或转红被忽略

## Supporting References

| 文件 | 用途 |
|------|------|
| `references/refactoring-playbook.md` | Two Hats / Boy Scout / Opportunistic / Preparatory 重构纪律、Fowler vocabulary、Architectural smells 速查表、Escalation 边界、SOLID conformance check、Refactor Note 模板 |
| `references/cpp-gtest-deep-guide.md` | C++/GoogleTest/CMake 栈深度参考 |
| `references/testing-anti-patterns.md` | C++ 测试反模式（mock 误用、测试专用方法等） |
| `skills/docs/hf-worktree-isolation.md` | 当前 skill pack 共享的 Worktree 隔离操作指南；若 `AGENTS.md` 声明项目等价路径，优先遵循 |

C++/GoogleTest 项目且需要语言级细节时才加载深度参考。非 C++ 也必须遵守同一实现契约。

## Verification

- [ ] 围绕唯一活跃任务推进
- [ ] worktree 已准备（若需要）
- [ ] 测试设计已完成 approval step（approval record 落在 `features/<active>/approvals/`）
- [ ] approval record 含 **SUT Form 声明**（`naive` / `pattern:<tactical name>` / `emergent`）；`pattern:<name>` 取值在 design § 4.5 allowlist 内
- [ ] Refactor Note 已回写 **SUT Form Declared / Pattern Actual / SUT Form Drift** 三字段，可供 reviewer 对比"声明 vs 实际"
- [ ] 留下有效 RED 与 GREEN 证据；体量大的原始日志/基线落在 `features/<active>/evidence/`
- [ ] RGR 步骤切分清晰，未在 GREEN 步内做 cleanup；preparatory refactor（若有）独立成步
- [ ] 已对 task 触碰范围执行 Architectural Health Check（conformance check + smells detection）
- [ ] Refactor Note 已写齐：Hat Discipline / In-task Cleanups / Boy Scout Touches / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence
- [ ] 触发 escalation 时已停 task，Next Action 指向 `hf-workflow-router`，不强行进入 `hf-test-review`
- [ ] 实现交接块已写回，含 canonical Next Action
- [ ] feature `progress.md` 已同步
- [ ] 未私自重排后续质量链

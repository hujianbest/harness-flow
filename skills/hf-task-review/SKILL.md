---
name: hf-task-review
description: 适用于单 task 实现完成后、需要在进 regression-gate 前对该 task 进行合成评审（测试质量 + 代码质量 + 任务级追溯一致性）的场景。不适用于写/修测试或代码（→ hf-test-driven-dev）、feature 终局的 spec↔impl 全量追溯（→ hf-traceability-review）、阶段不清（→ hf-workflow-router）。v0.7 起替代 hf-test-review + hf-code-review 在 per-task 链路上的位置。
---

# HF Task Review

合成式 per-task 评审。一次 reviewer subagent dispatch 内并行评测 **测试质量**、**代码质量**、**任务级追溯一致性** 三个子维度，返回单个 severity-tagged findings 列表 + 单一 verdict，决定是否可进入 `hf-regression-gate`。

替代 v0.6 链路中 `hf-test-review → hf-code-review → hf-traceability-review` 这串 3 个独立 per-task 节点。Feature 终局的全量追溯（spec↔design↔tasks↔impl↔test）仍由 `hf-traceability-review` 在 `hf-completion-gate` 之前一次性跑（见 router transition map）。

## Why merge

v0.6 把 3 个 review 拆成串行节点的代价：每个 reviewer 重读相同的实现交接块 + spec/design 锚点；3 份 stand-alone 记录文件；finding 即使全是 minor 也要走 3 轮回流。本 skill 借鉴 Anthropic Code Review plugin（4 并行 agent → 1 findings 列表）+ Superpowers `subagent-driven-development`（per-task 两段评审 + 单回执）+ BMad per-story `code-review`（1 次 adversarial review 同时校 tasks/AC/git reality）的形态，把 per-task 评审压成 1 个节点 / 1 份回执 / 1 个 verdict。

Author/Reviewer 分离（Fagan）与 Two Hats 纪律完全不变：reviewer subagent 与 implementer subagent 不共享上下文；reviewer 不修测试也不修代码，只产 findings。

## Methodology

本 skill 复用既有 review skill 已验证的 rule set 与评分维度，仅把它们合并到一个 checklist + 一次 dispatch 内：

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **Fail-First Validation** | RED 对应行为缺口，GREEN 来自本次实现 | TDD 质量门禁（同 hf-test-review TT1） | 步骤 3.1 / 3.A |
| **Coverage Categories** | 行为/风险/边界多维覆盖评估 | Crispin & Gregory, *Agile Testing*（同 hf-test-review TT2-TT4） | 步骤 3.A |
| **Risk-Based Testing** | 测试回应项目缺陷模式 / 风险清单 / 上游 review 历史 | HF 质量链约定（同 hf-test-review TT3） | 步骤 3.A |
| **Fagan Code Inspection (adapted)** | 正确性 / 设计一致性 / 状态-错误-安全 / 可读性 / 架构健康 5 维结构化检查 | Fagan 1976（同 hf-code-review CR1-CR8） | 步骤 3.B |
| **Design Conformance Check** | 实现遵循已批准设计，偏离需理由 + 可追溯；UI 必须遵循 UI Implementation Contract | HF 工程约定（同 hf-code-review CR8） | 步骤 3.B |
| **Clean Architecture / Two Hats / Smells Detection** | 依赖方向、模块边界、接口契约 conformance；Two Hats 纪律；smells 速查表 | Martin/Beck/Fowler/Garcia 等（同 hf-code-review CR7） | 步骤 3.B |
| **Per-Task Traceability** | 本 task 实现是否覆盖它认领的 FR / Acceptance；触碰工件是否与任务卡声明一致 | HF Per-Task 工件追溯（同 hf-traceability-review TZ3 子集） | 步骤 3.C |
| **Single Verdict / Severity Filter** | 一次 dispatch 产单一 verdict + severity-tagged findings；不为每个子维度拆门禁 | Anthropic Code Review（HIGH-SIGNAL only）、Superpowers two-stage review | 步骤 4 — verdict |
| **Author/Reviewer Separation** | reviewer 不修测试 / 代码 / 工件，只产 findings | Fagan 1976 + HF Hard Gate | 全步骤 |

**职责边界**（与既有 review skill 的关系）：

- `hf-test-review` / `hf-code-review`：v0.7 起在 per-task 链路上由本 skill 替代。两个旧 skill 仍保留作为 **reference rubric 库**（`references/review-checklist.md` 等）供本 skill 引用；也保留为 `high-risk` task 档下的独立深审入口（见 router risk-tag 链路）。
- `hf-traceability-review`：v0.7 起仅在 feature 终局（无剩余 ready task 时）跑一次全量 spec↔impl 追溯矩阵；per-task 的"本 task 实现是否覆盖它认领的 FR / Acceptance"由本 skill 步骤 3.C 子维度承担。
- `hf-regression-gate`：与本 skill 同层、不重叠；本 skill 不跑测试命令，回归验证仍由 regression gate 完成。

## When to Use

适用：
- 单 task 的 `hf-test-driven-dev` 已写回稳定实现交接块，需要在进 `hf-regression-gate` 前做 per-task 合成评审
- 父会话 / router 在 `standard` 或 `full` profile 主链上推到 `hf-task-review` 节点
- `hf-task-review` 返回 `需修改`，作者在 `hf-test-driven-dev` 修订后回流复审（仍在 2 轮 remediation budget 内）

不适用 → 改用：
- 写/修测试 → `hf-test-driven-dev`
- 写/修代码 → `hf-test-driven-dev`
- Feature 终局的 spec↔impl 全量追溯 → `hf-traceability-review`
- 回归测试运行 → `hf-regression-gate`
- 阶段不清 / 证据冲突 → `hf-workflow-router`
- Risk Tag = `high-risk` 的 task 在本 skill 之外**追加**独立 `hf-code-review` 深审（CR7/CR8 架构健康）；本 skill 仍是其前置节点，不被跳过

Direct invoke 信号："review 这个 task"、"task review"、"帮我审一下这次 task 的测试 + 代码 + 追溯"。

## Hard Gates

- 本 skill 通过前不得进入 `hf-regression-gate`
- 输入工件不足不得开始评审（缺稳定实现交接块、缺 Refactor Note、关键测试/代码范围不可定位 → precheck blocked）
- reviewer 不修测试、不修代码、不修任务卡、不替作者补 trace anchor
- 单 task 的 remediation budget = 2 轮；第 3 轮自动设 `reroute_via_router=true` 让 router 重编排（与 `hf-test-driven-dev` Hard Gate 对齐）
- 每条 finding 必须带 `severity` + `classification` + `rule_id`，rule_id 必须可追溯到 sub-dimension（TT-x / CR-x / TZ-x）
- 本 skill 默认按 **snapshot mode** 回执：`通过` 且无 HIGH+ findings 时不强制落 stand-alone 文件，由父会话把 snapshot 落入 `progress.md` 的 `## Task NNN Review Snapshot` 段；`需修改` / `阻塞` / 含 HIGH+ findings 时仍按 file mode 落 `features/<active>/reviews/task-review-task-NNN.md`

## Workflow

### 1. 建立证据基线

reviewer 读取最小必要工件：
- 实现交接块（含 Refactor Note）
- 本 task 新增/修改的测试资产
- 本 task 触碰的源代码变更
- 任务卡（默认 `features/<active>/tasks.md` 中本 task 段：Acceptance / Files / Verify / 测试设计种子）
- 已批准 spec / design 中本 task 直接锚定的 FR / 设计决策（不读全量，只读 trace anchor 指向的段）
- 项目级测试 / coding / risk 约定（若声明）
- 项目缺陷模式记录 / 风险清单（若维护，不存在则跳过）
- `features/<active>/progress.md`

不读已批准 spec / design 全文；不读其他 task 的实现细节；保持 reviewer subagent context 精简。

### 1.5 Precheck：能否合法进入 review

检查：
- 实现交接块是否稳定可定位
- Refactor Note 是否齐全（Hat Discipline / In-task Cleanups / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence / SUT Form Declared / Pattern Actual / SUT Form Drift）
- 测试与代码改动是否可定位（diff 或文件清单可读）
- route / stage / profile / Workspace Isolation 与上游 evidence 是否一致
- 任务卡的 Acceptance / Files / Verify 是否已写实

处理：
- route / stage / 证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`，next = `hf-workflow-router`
- 缺稳定交接块 / Refactor Note 缺失 / 测试或代码范围不可定位 → 写最小 blocked record，next = `hf-test-driven-dev`
- Refactor Note 中 `Escalation Triggers` 非 `none` 但 Next Action 误指 `hf-task-review` → escalation 边界冲突，`reroute_via_router=true`，next = `hf-workflow-router`
- precheck 通过 → 继续正式审查

### 2. 三维度并行评分

reviewer 在 fresh context 内一次跑完三个 sub-rubric，每个 sub-rubric 落一个分组评分。不要拆成串行子任务。

| Sub-dimension | 维度评分 | 权威 rubric |
|---|---|---|
| **A. 测试质量**（原 `hf-test-review`） | 6 维 0-10：fail-first 有效性、行为/验收映射、风险覆盖、测试设计质量、新鲜证据完整性、下游就绪度 | `skills/hf-test-review/references/review-checklist.md`（rule_id 前缀：TT / TA） |
| **B. 代码质量**（原 `hf-code-review`） | 8 维 0-10：正确性、设计一致性、状态/错误/安全、可读性、范围守卫、下游追溯就绪度、架构健康与重构纪律（CR7 + 子维度 CR7.1-7.5）、UI 实现一致性（CR8） | `skills/hf-code-review/references/review-checklist.md` + `skills/hf-code-review/references/clean-architecture-guardrails.md`（rule_id 前缀：CR / CA） |
| **C. 任务级追溯** | 3 维 0-10：本 task 实现是否覆盖它认领的 FR / Acceptance；触碰工件是否与任务卡 Files 段一致；本 task 测试是否回溯到任务卡测试设计种子（非全量 spec↔impl 矩阵） | `skills/hf-traceability-review/references/review-checklist.md`（rule_id 前缀：TZ / ZA；本 skill 只复用 task-level 子集 TZ3 / TZ4 / TZ6） |

任一子维度关键评分 < 6 不得给 `通过`。

每条 finding 必须带：
- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（明确所属 sub-dimension：如 `TT5` / `CR7.3` / `TZ3` / `CA8`）
- `sub_dimension`（`test_quality` / `code_quality` / `task_traceability`），用于父会话或人工后续聚类

默认分类与三个旧 review skill 一致：
- 测试维度：`USER-INPUT` 主要是验收阈值 / 外部质量门未拍板 / 风险优先级冲突；`LLM-FIXABLE` 是 RED/GREEN 证据缺、覆盖不足、mock 误用、test seed 弱
- 代码维度：`USER-INPUT` 主要是实现偏离设计涉及新决策、超范围保留、是否升级为 increment；`LLM-FIXABLE` 是结构、错误、命名、防御、smell、Refactor Note 字段不全、over-abstraction 回退
- 追溯维度：`USER-INPUT` 主要是任务认领范围本身仍需真人裁决；`LLM-FIXABLE` 是 trace anchor 缺、Files 段未回写、test seed 漂移

### 3. Sub-rubric 实施细则

#### 3.A 测试质量子维度

按 `skills/hf-test-review/references/review-checklist.md`（TT1-TT6 / TA1-TA4）跑全量 checklist。重点项：
- RED 是否对应行为缺口？GREEN 是否来自本次实现？是否存在"看起来失败但其实无关"的 RED？
- mock 是否限定在真正边界？provider mock / child component overmock / mock fetch / fixture contract drift 是否掩盖真实 App 装配 / API 契约 / browser runtime？
- happy-dom / jsdom 不得写成真实浏览器证据
- 测试设计 approval 中 `SUT Form` 声明是否合法（`naive` / `pattern:<design § 4.5 战术模式>` / `emergent`）；GoF 模式名不允许出现在 `pattern:<name>` 声明里

#### 3.B 代码质量子维度

按 `skills/hf-code-review/references/review-checklist.md`（CR1-CR9 / CA1-CA10）与 `skills/hf-code-review/references/clean-architecture-guardrails.md` 跑全量 checklist。重点项：
- Refactor Note 完整性（CR7.2）：缺字段直接判 finding
- Architectural Conformance（CR7.3）：依赖方向 / 模块边界 / 接口契约 / ADR 决策违反 → finding；不允许 reviewer "宽容"
- Architectural Smells Detection（CR7.4）：god-class / cyclic-dep / hub-like-dep / unstable-dep / layering-violation / leaky-abstraction / feature-envy-cross-module / over-abstraction
- Escalation-bypass（CA8）/ 跨 ≥3 模块结构性变更 / 实质修改 ADR / 修改模块边界 / 修改接口契约 → 整体 verdict `阻塞`，`reroute_via_router=true`，next = `hf-workflow-router`，**优先级高于 sub-rubric verdict**
- UI 触碰时 CR8 必查（不允许跳过）
- AI Slop / Comment 质量（CR9）按 `skills/hf-code-review/references/ai-slop-rubric.md` 跑 4 类禁用模式 grep

#### 3.C 任务级追溯子维度

本 skill 只承担 **task-level** 子集，全量 spec↔design↔tasks↔impl↔test 矩阵在 feature 终局由 `hf-traceability-review` 跑。本步只检查 3 个 task-local invariants：

1. **本 task 实现 → 它认领的 FR / Acceptance**：从任务卡 `Acceptance` 段反向核对实现是否覆盖；缺失 → `[critical|important][LLM-FIXABLE][TZ3]` finding（critical 还是 important 取决于缺失是核心行为还是边界）
2. **触碰工件 ↔ 任务卡 Files 段**：从代码变更（git diff 或实现交接块 `触碰工件`）反向核对任务卡 Files 段；任一边漏写 → `[important|minor][LLM-FIXABLE][TZ4]` finding
3. **本 task 测试 ↔ 任务卡测试设计种子**：实现交接块中 `与任务计划测试种子的差异` 段是否如实回写；测试设计漂移而未回写 → `[important][LLM-FIXABLE][TZ6]` finding

不在本步做的事（留给 feature 终局 `hf-traceability-review`）：
- 全 feature 的 spec ↔ design 双向矩阵
- 跨 task 的 backward link 闭合
- UI Implementation Contract 全 surface 一致性追溯（per-task 部分仍由 3.B 的 CR8 承担）

### 4. 形成 verdict

收敛唯一 verdict + 唯一下一步 + 三维度 score 摘要。

| 场景 | conclusion | next_action_or_recommended_skill | reroute_via_router | record mode |
|---|---|---|---|---|
| precheck blocked：route / stage / profile / 上游 evidence 冲突 | `阻塞` | `hf-workflow-router` | `true` | file |
| precheck blocked：缺稳定实现交接块 / Refactor Note 缺失 / 范围不可定位 | `阻塞` | `hf-test-driven-dev` | `false` | file |
| precheck blocked：Refactor Note Escalation Triggers 非 none 但 Next Action 误指本 skill | `阻塞` | `hf-workflow-router` | `true` | file |
| 正式审查后 `通过`，无 HIGH+ findings | `通过` | `hf-regression-gate` | `false` | **snapshot**（默认） |
| 正式审查后 `通过`，但存在 ≥1 个 HIGH 但非 critical 的非阻塞遗留项（如 documented debt） | `通过` | `hf-regression-gate` | `false` | file（保留 audit trail） |
| 正式审查后 `需修改` | `需修改` | `hf-test-driven-dev` | `false` | file |
| 正式审查后 `阻塞` 且可回实现补救 | `阻塞` | `hf-test-driven-dev` | `false` | file |
| 正式审查后 `阻塞`：CR7 触发 CA8 escalation-bypass 或实质修改 ADR / 模块边界 / 接口契约 / 跨 ≥3 模块结构性变更 | `阻塞` | `hf-workflow-router` | `true` | file |
| 正式审查后 `阻塞` 且问题本质属于重编排 | `阻塞` | `hf-workflow-router` | `true` | file |
| 已是同一 task 第 3 轮回流（remediation budget = 2 已耗尽） | `阻塞` | `hf-workflow-router` | `true` | file（含 `remediation_round_count: 3`） |

固定字段约束：
- `conclusion` ∈ `{通过, 需修改, 阻塞}`
- `next_action_or_recommended_skill` 唯一 canonical 值
- `needs_human_confirmation` 默认 `false`（本 skill 不触发真人 approval）
- 除 `通过` 且确无问题外，`key_findings` 不得留空
- `finding_breakdown` 必须按 sub_dimension 分组报告（`test_quality` / `code_quality` / `task_traceability`）
- `remediation_round_count`（v0.7 新字段）：1 / 2 / 3，对应本 task 的第几轮 review；父会话从 `progress.md` `## Remediation Counters` 读

### 5. 写 review 回执

#### snapshot mode（默认；`通过` + 无 HIGH+ findings）

reviewer 不落 stand-alone 文件，直接返回结构化摘要给父会话。父会话把 snapshot 写入 `features/<active>/progress.md` 的 `## Task NNN Review Snapshot` 段（≤ 10 行）。snapshot 含：
- task id
- 三维度 score 摘要（如 `test: 8/8/9/8/8/8 | code: 9/8/9/8/9/8/9/N-A | trace: 9/9/9`）
- verdict
- 非阻塞遗留项（≤ 3 条 minor / documented debt 短摘要；若无则写 `none`）
- 触发 next-ready check 的引用

snapshot 不重复实现交接块内容，只是父会话决策路由所需的最小回执。git history + progress.md 联合构成审计链。

#### file mode（非通过路径 / 含 HIGH+ findings / 项目 policy 强制留档）

reviewer 写到 `features/<active>/reviews/task-review-task-NNN.md`（若同 task 多轮，加 `-rN` 后缀：`task-review-task-NNN-r2.md`）。模板按 `references/review-record-template.md`。

若项目级 policy 在 `features/<active>/progress.md` `Audit Mode: file` 显式声明，则**所有** verdict 均强制 file mode；这是 SOC 2 / 合规场景的开关。默认 `Audit Mode: snapshot-allowed`。

回传结构化摘要遵循 `hf-workflow-router/references/reviewer-return-contract.md` 的 snapshot/file mode 字段（v0.7 扩展）。

## Output Contract

完成时产出：

- **snapshot mode**：reviewer-return JSON + 父会话在 progress.md 追加的 `## Task NNN Review Snapshot` 段（≤ 10 行）；**无** stand-alone 文件
- **file mode**：reviewer 落 `features/<active>/reviews/task-review-task-NNN[-rN].md` + reviewer-return JSON
- reviewer-return JSON 含：`conclusion` / `next_action_or_recommended_skill` / `record_mode` (`snapshot|file`) / `record_path`（snapshot 时为 progress.md 锚点）/ `key_findings` / `finding_breakdown`（按 sub_dimension 分组）/ `remediation_round_count` / `needs_human_confirmation` / `reroute_via_router`
- workflow blocker 时显式 `reroute_via_router=true`

reviewer-return JSON 不得伪造 verdict；不得为让本 skill "看起来通过" 而隐瞒 critical / HIGH finding。

## Reference Guide

按需加载详细参考内容。

| 主题 | Reference | 加载时机 |
|---|---|---|
| 测试质量 sub-rubric 完整 checklist | `skills/hf-test-review/references/review-checklist.md` | 步骤 3.A |
| 代码质量 sub-rubric 完整 checklist | `skills/hf-code-review/references/review-checklist.md` | 步骤 3.B |
| Clean Architecture / Two Hats / smells 速查 | `skills/hf-code-review/references/clean-architecture-guardrails.md` | 步骤 3.B（CR7） |
| AI Slop / Comment 质量 4 类 grep | `skills/hf-code-review/references/ai-slop-rubric.md` | 步骤 3.B（CR9） |
| 任务级追溯 sub-rubric（只用 TZ3 / TZ4 / TZ6 task-level 子集） | `skills/hf-traceability-review/references/review-checklist.md` | 步骤 3.C |
| Reviewer 返回契约（含 v0.7 snapshot / file mode 扩展） | `skills/hf-workflow-router/references/reviewer-return-contract.md` | 步骤 5 回执 |
| Review dispatch 协议（含 v0.7 record_mode 字段） | `skills/hf-workflow-router/references/review-dispatch-protocol.md` | 父会话派发本 skill 时 |
| file mode 记录模板 | `references/review-record-template.md` | 步骤 5 file mode |

加载策略：reviewer subagent 默认按 sub_dimension 顺序加载 sub-rubric；触碰 UI 时强制加载 CR8 部分；触碰 ADR / 模块边界时强制加载 `clean-architecture-guardrails.md` 全文。

## Red Flags

- 在父会话内联跑本 skill（绕过 author/reviewer 分离）
- 把三个 sub-rubric 拆成三次独立 dispatch（违背本 skill 的"合一"前提）
- reviewer 在评审中改测试 / 改代码 / 改任务卡 / 补 trace anchor
- 把 critical / HIGH finding 降级为 minor 以让 verdict 看起来通过
- snapshot mode 下 `通过` 但有 critical / HIGH finding（必须强制升 file mode）
- 任一 sub-dimension 关键评分 < 6 仍给 `通过`
- 第 3 轮回流不触发 `reroute_via_router=true`，继续在 implementer ↔ reviewer 间循环
- 用三个旧 review skill 的 stand-alone 记录文件做"双重落盘"（本 skill 的回执就是唯一回执）
- 把 feature 终局的全量 spec↔impl 矩阵塞进本 skill 步骤 3.C（那是 `hf-traceability-review` 的职责）

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "test / code / trace 分三次跑更稳。" | Workflow stop rule: 本 skill 的合一前提就是单次 dispatch + 单一 verdict；拆三次违背 v0.7 设计、回到 v0.6 形态。 |
| "snapshot mode 太轻，保险起见全 file mode。" | Hard Gates: snapshot mode 是默认；强制 file mode 必须由项目级 `Audit Mode: file` 或 verdict 非 `通过` 触发；不允许 reviewer 私自升级。 |
| "CR7 escalation 触发了，但 in-task 顺手修就行。" | Hard Gates: CR7 / CA8 escalation-bypass → 整体 verdict 阻塞 + reroute_via_router；优先级高于其他维度。 |
| "task 第 3 轮还在小修，再给一轮。" | Hard Gates: remediation budget = 2；第 3 轮自动 reroute；额外 budget 由 router / 真人决定，不在本 skill 内自延。 |
| "TZ 全部留给 hf-traceability-review，本 skill 跳过追溯子维度。" | Hard Gates: 步骤 3.C 是本 skill 必查项（task-local TZ3 / TZ4 / TZ6）；全量矩阵 ≠ task-local，二者不可互替。 |

## Verification

- [ ] reviewer subagent 已独立 dispatch（不在父会话内联）
- [ ] 三个 sub-rubric 全部已跑（test_quality / code_quality / task_traceability）
- [ ] findings 已带 severity / classification / rule_id / sub_dimension
- [ ] 给出唯一 verdict + 唯一 next_action_or_recommended_skill
- [ ] `record_mode` 已选定（snapshot 默认 / file 当 verdict ≠ 通过 或 含 HIGH+ 或 Audit Mode: file）
- [ ] snapshot mode 时父会话已把 ≤ 10 行 snapshot 写入 progress.md `## Task NNN Review Snapshot`
- [ ] file mode 时记录已落到 `features/<active>/reviews/task-review-task-NNN[-rN].md`
- [ ] `remediation_round_count` 已写明；若 = 3 → next 必须为 `hf-workflow-router`
- [ ] CR7 escalation / CA8 escalation-bypass 触发时 verdict 为 `阻塞` 且 `reroute_via_router=true`
- [ ] precheck blocked 时已写明 workflow blocker 和正确 next
- [ ] workflow blocker 时已显式 `reroute_via_router=true`

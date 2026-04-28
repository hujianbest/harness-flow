---
name: hf-test-review
description: 适用于实现完成后判断测试质量、code review 前的测试评审、用户显式要求评审测试的场景。可吸收 bug pattern 目录或 hf-bug-patterns 的候选经验作为风险输入，但不以其完成为前置。不适用于写/修测试（→ hf-test-driven-dev）、评审代码（→ hf-code-review）、阶段不清（→ hf-workflow-router）。
---

# HF Test Review

评审测试资产，判断 fail-first、行为覆盖和风险覆盖是否足以支持 `hf-code-review`。可吸收 `hf-bug-patterns` 或已有缺陷目录中的风险输入，但不以其完成为前置。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **Fail-First Validation (TDD Quality Gate)** | 验证测试确实先失败再通过，防止"天生绿色"的无效测试 | 项目化实践（TDD 质量门禁） | 步骤 2 — 评分；步骤 3.1 — fail-first 审查 |
| **Coverage Categories (Crispin/Gregory)** | 从行为覆盖、风险覆盖、边界覆盖等多维度评估测试质量 | Crispin & Gregory, "Agile Testing", 2009 | 步骤 2 — 评分；步骤 3.2/3.3 — 行为/风险覆盖 |
| **Bug-Pattern-Driven Testing** | 测试覆盖应回应已有 bug pattern 目录或候选经验识别出的风险 | 项目化实践（HF 质量链约定） | 步骤 3.3 — 风险覆盖 |
| **Structured Walkthrough** | 多维度评分量化判断，防止印象式评审 | 项目化实践（评审通用方法） | 步骤 2 — 多维评分；步骤 4 — verdict |

## When to Use

适用：
- 实现完成后判断测试质量
- code review 前的测试评审
- 用户显式要求 test review

不适用 → 改用：
- 写/修测试 → `hf-test-driven-dev`
- 评审代码 → `hf-code-review`
- 阶段不清 → `hf-workflow-router`

Direct invoke 信号："review 测试"、"test review"、"帮我审一下测试质量"。

## 和其他 Skill 的区别

| 场景 | 用 hf-test-review | 不用 |
|------|-------------------|------|
| 评审测试质量和 fail-first 有效性 | ✅ | |
| 写/修测试 | | → `hf-test-driven-dev` |
| 评审代码质量 | | → `hf-code-review` |
| 评审追溯完整性 | | → `hf-traceability-review` |
| 阶段不清/证据冲突 | | → `hf-workflow-router` |

## Hard Gates

- test review 通过前不得进入 code review
- 输入工件不足不得开始评审
- reviewer 不修测试、不继续实现

## Workflow

### 1. 建立证据基线

读实现交接块、新增/修改测试、bug-patterns 记录（默认 `docs/bug-patterns/catalog.md`）、项目级测试约定、规格/设计片段（默认 `features/<active>/spec.md` / `design.md`）、feature `progress.md`（默认 `features/<active>/progress.md`）。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定实现交接块、可定位测试资产、route/stage/profile 与上游 evidence 是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定交接块或关键测试资产 → 写最小 blocked record，下一步 `hf-test-driven-dev`
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

6 个维度 0-10 评分：fail-first 有效性、行为/验收映射、风险覆盖、测试设计质量、新鲜证据完整性、下游就绪度。任一关键维度 < 6 不得通过。

按 `references/review-checklist.md` 做正式审查。

每条 finding 必须带：
- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `TT1`、`TT5`、`TA2`）

默认分类：
- `USER-INPUT`：验收阈值本身未定、外部质量门尚未拍板、风险优先级冲突仍需真人裁决
- `LLM-FIXABLE`：缺少有效 RED/GREEN 证据、未覆盖关键边界、Acceptance 映射缺失、mock 误用、test seed 过弱

### 3. 正式 checklist 审查

3.1 **Fail-first & RED/GREEN**：RED 是否对应当前行为缺口？GREEN 是否来自本次实现？
3.2 **行为价值与验收映射**：测试是否覆盖任务关键行为？是否映射回验收标准？
3.3 **风险覆盖与边界**：是否覆盖 bug-patterns 识别的风险？边界/null/错误路径？
3.4 **测试设计质量**：mock 是否限定在真正边界？测试是否独立可重复？
3.5 **下游就绪度**：测试质量是否足以让 code-review 做可信判断？

### 4. 形成 verdict

- `通过`：所有维度 >= 6，测试足以支持 code review → `next_action_or_recommended_skill=hf-code-review`，`needs_human_confirmation=false`
- `需修改`：findings 可 1-2 轮定向修订 → `next_action_or_recommended_skill=hf-test-driven-dev`，`needs_human_confirmation=false`
- `阻塞`：测试过于薄弱/核心行为未覆盖/findings 无法定向回修 → `next_action_or_recommended_skill=hf-test-driven-dev`，`needs_human_confirmation=false`；若问题本质是 stage/route/profile/上游证据冲突 → `next_action_or_recommended_skill=hf-workflow-router`，`reroute_via_router=true`

Findings 带 severity（critical/important/minor）和分类（USER-INPUT/LLM-FIXABLE）。

### 5. 写 review 记录

保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/test-review-task-NNN.md`。若项目无专用格式，默认使用 `references/review-record-template.md`。

回传结构化摘要给父会话时，遵循当前 skill pack 中 `hf-workflow-router/references/reviewer-return-contract.md`：`next_action_or_recommended_skill` 只写一个 canonical 值；workflow blocker 必须显式写 `reroute_via_router=true`。

## Output Contract

完成时产出：
- Review 记录（保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/test-review-task-NNN.md`）
- 结构化摘要含 `record_path`、`next_action_or_recommended_skill`
- workflow blocker 时显式写明 `reroute_via_router=true`

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/review-checklist.md` | test review checklist 与 rule IDs |
| `references/review-record-template.md` | test review 记录模板与结构化返回契约 |
| `hf-workflow-router/references/reviewer-return-contract.md` | 当前 skill pack 共享的 reviewer 返回契约 |

## Red Flags

- 不读 handoff 就审测试
- "测试文件存在"等同于"测试充分"
- 忽略无效 RED/GREEN
- 忽略 bug-patterns 识别的风险
- 评审中修测试
- 返回多个候选下一步

## Verification

- [ ] review record 已落盘
- [ ] 给出明确结论、findings、gaps 和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id
- [ ] 结构化摘要含 record_path 和 next_action_or_recommended_skill
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] 结论足以让父会话路由
- [ ] workflow blocker 时已显式写明 reroute_via_router

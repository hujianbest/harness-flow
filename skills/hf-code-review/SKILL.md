---
name: hf-code-review
description: 适用于 test review 通过后评审代码质量、用户要求 code review 的场景。不适用于评审测试（→ hf-test-review）、写/修代码（→ hf-test-driven-dev）、阶段不清（→ hf-workflow-router）。
---
# HF Code Review

评审实现代码质量。判断正确性、设计一致性、状态/错误/安全、可读性、下游追溯就绪度，以及**架构健康与重构纪律（CR7）**。运行在 `hf-test-review` 之后，决定是否可进入 `hf-traceability-review`。

## Methodology

本 skill 融合以下已验证方法：

- **Fagan Code Inspection (adapted)**: 结构化检查正确性、设计一致性、状态安全、可读性、架构健康五个维度，而非自由形式代码阅读。
- **Design Conformance Check**: 实现必须遵循已批准设计，偏离需有理由且可追溯——防止实现与设计漂移。
- **Defense-in-Depth Review**: 错误处理、状态转换、安全性逐层检查，确保不因"测试通过"掩盖实现隐患。
- **Clean Architecture Conformance Check**: 评审实现是否遵循 `hf-design` 中声明的依赖方向、模块边界、接口契约；不重新论证架构决策，只做 conformance（Robert C. Martin, *Clean Architecture*）。
- **Two Hats / Refactoring Hygiene Review**: 评审实现节点是否守住 Two Hats（Kent Beck / Fowler），是否完成应做的 Boy Scout cleanup（Robert C. Martin），Refactor Note 是否完整可信。
- **Architectural Smells Detection**: 使用 architectural smells 目录（Garcia/Popescu/Edwards/Medvidovic, *Identifying Architectural Bad Smells*）识别 god-class / cyclic-dep / layering-violation 等结构性问题，按 escalation 边界处理。
- **Separation of Author/Reviewer Roles**: 评审者不改代码，只产出具名 findings 和 verdict。

## When to Use

适用：test review 通过后评审代码、用户要求 code review。

不适用：评审测试 → `hf-test-review`；写/修代码 → `hf-test-driven-dev`；阶段不清 → `hf-workflow-router`。

## Hard Gates

- code review 通过前不得进入 traceability review
- 输入工件不足不得开始
- reviewer 不改代码、不继续实现

## Workflow

### 1. 建立证据基线

读实现交接块（含 Refactor Note）、代码变更、test-review 记录（默认 `features/<active>/reviews/test-review-task-NNN.md`）、项目级 coding 约定、规格/设计片段（默认 `features/<active>/spec.md` / `design.md`）、相关 ADR（默认 `docs/adr/`）、feature `progress.md`（默认 `features/<active>/progress.md`）。

**Refactor Note 是 CR7（Architectural Health & Refactoring Hygiene）的核心输入**：缺失即视为 precheck blocked，按下面 1.5 处理。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定实现交接块（含 Refactor Note）、可定位代码变更、route/stage/profile 与上游 evidence 是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定交接块、核心代码范围不可定位、或 Refactor Note 缺失 → 写最小 blocked record，下一步 `hf-test-driven-dev`
- 实现交接块的 Refactor Note 中 Escalation Triggers 非 `none` 但 Next Action 仍指向 `hf-test-review` → route/stage 与 escalation 边界冲突，`reroute_via_router=true`，下一步 `hf-workflow-router`
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

7 维度 0-10 评分：正确性、设计一致性、状态/错误/安全、可读性、范围守卫、下游追溯就绪度、**架构健康与重构纪律**。任一关键维度 < 6 不得通过。

按 `references/review-checklist.md` 做正式审查。CR7（Architectural Health & Refactoring Hygiene）的子维度与判别细则按 `references/clean-architecture-guardrails.md`。

每条 finding 必须带：

- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `CR2`、`CR5`、`CR7`、`CR7.3`、`CA3`、`CA8`）

默认分类：

- `USER-INPUT`：实现偏离设计且涉及新的产品/业务决策、超范围功能是否保留、是否要把已识别 architectural debt 升级为 `hf-increment` 等仍需真人拍板
- `LLM-FIXABLE`：代码结构、错误处理、命名、边界、防御性检查、实现交接块缺口、Refactor Note 字段不全、in-task 范围内可识别但被遗漏的 architectural smell、可在 task 内回退的 over-abstraction 等代码层问题

### 3. 正式 checklist 审查

3.1 **正确性**：实现是否真正完成了任务目标？逻辑是否有 off-by-one、边界遗漏？
3.2 **设计一致性**：实现是否遵循已批准设计？偏离是否有理由且可追溯？
3.3 **状态/错误/安全**：错误处理是否完备？状态转换是否安全？是否有安全隐患？
3.4 **可读性**：命名是否清晰？结构是否合理？是否有过早优化或死代码？
3.5 **下游就绪度**：代码是否足以让 traceability-review 做可信判断？实现交接块是否完整？
3.6 **架构健康与重构纪律 (CR7)**：详细规则按 `references/clean-architecture-guardrails.md`。子维度：
- **CR7.1 Two Hats Hygiene**：RGR 是否守住 Two Hats；GREEN 步是否做了 cleanup；preparatory refactor 是否独立成步
- **CR7.2 Refactor Note 完整性**：Hat Discipline / In-task Cleanups / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence 是否齐全；In-task Cleanups 是否使用 Fowler vocabulary
- **CR7.3 Architectural Conformance**：实现是否仍遵循 `hf-design` 中的依赖方向、模块边界、接口契约、ADR 决策；是否引入设计未声明的新依赖 / 新跨层调用 / 新抽象层
- **CR7.4 Architectural Smells Detection**：触碰范围内是否有可见 smells（god-class / cyclic-dep / hub-like-dep / unstable-dep / layering-violation / leaky-abstraction / feature-envy-cross-module / over-abstraction）；识别到的是否被正确分类（in-task / debt / escalation）；触发 escalation 边界的是否被错误地"顺手"在 task 内修了（CA8 escalation-bypass）
- **CR7.5 Boy Scout Compliance**：触碰文件离开时 clean code 健康度是否未退化；触碰范围内是否仍有明显 magic number / 死代码 / 长函数 / 命名不清 / 嵌套 ≥3 层未处理

### 4. 形成 verdict

- `通过`：所有维度 >= 6（含 CR7 主维度 >= 8、所有 CR7 子维度 >= 6），代码足以支持追溯评审 → `next_action_or_recommended_skill=hf-traceability-review`，`needs_human_confirmation=false`
- `需修改`：findings 可 1-2 轮定向修订（含 CR7 in-task 可修复项：Refactor Note 字段补全、Boy Scout 遗漏、in-task 范围内可识别但被遗漏的 smell、可在 task 内回退的 over-abstraction、hat-mixing 导致 fresh evidence 不可信需重做 RGR） → `next_action_or_recommended_skill=hf-test-driven-dev`，`needs_human_confirmation=false`
- `阻塞`：核心逻辑错误/安全漏洞/findings 无法定向回修 → `next_action_or_recommended_skill=hf-test-driven-dev`，`needs_human_confirmation=false`；若问题本质是 stage/route/profile/上游证据冲突，**或 CR7 触发 escalation-bypass（CA8）/ 实质修改 ADR / 模块边界 / 接口契约 / 跨 ≥3 模块结构性变更** → `next_action_or_recommended_skill=hf-workflow-router`，`reroute_via_router=true`

Findings 带 severity 和 USER-INPUT/LLM-FIXABLE 分类。给出代码风险和追溯评审提示。

### 5. 写 review 记录

保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/code-review-task-NNN.md`。若项目无专用格式，默认使用 `references/review-record-template.md`。

回传结构化摘要时遵循当前 skill pack 中 `hf-workflow-router/references/reviewer-return-contract.md`：`next_action_or_recommended_skill` 只写一个 canonical 值；workflow blocker 必须显式写 `reroute_via_router=true`。

### 5A. 最终返回闸门

在返回给父会话前，先把 reviewer 结论收敛成**唯一 verdict + 唯一下一步 + 固定字段集合**。不要只给自然语言 code review 评论。

| 场景 | conclusion | next_action_or_recommended_skill | reroute_via_router | 最少必须写出的字段 |
|---|---|---|---|---|
| precheck blocked：route / stage / profile / 上游 evidence 冲突 | `阻塞` | `hf-workflow-router` | `true` | `record_path`、关键冲突说明、`key_findings` |
| precheck blocked：缺稳定实现交接块、核心代码范围不可定位、或 Refactor Note 缺失 | `阻塞` | `hf-test-driven-dev` | `false` | `record_path`、缺失输入、为什么当前无法合法开始 code review |
| precheck blocked：Refactor Note 中 Escalation Triggers 非 `none` 但 Next Action 误指 `hf-test-review` | `阻塞` | `hf-workflow-router` | `true` | `record_path`、escalation 触发说明、`key_findings` |
| 正式审查后 `通过` | `通过` | `hf-traceability-review` | `false` | `record_path`、主要通过依据、非阻塞优化项（若有） |
| 正式审查后 `需修改` | `需修改` | `hf-test-driven-dev` | `false` | `record_path`、`key_findings`、`finding_breakdown`、代码风险与下游追溯提示 |
| 正式审查后 `阻塞` 且可回实现补救 | `阻塞` | `hf-test-driven-dev` | `false` | `record_path`、核心阻塞问题、为什么不能 1-2 轮定向回修 |
| 正式审查后 `阻塞`：CR7 触发 CA8 escalation-bypass 或实质修改 ADR / 模块边界 / 接口契约 / 跨 ≥3 模块结构性变更 | `阻塞` | `hf-workflow-router` | `true` | `record_path`、escalation 触发说明（含违反的边界）、`key_findings` |
| 正式审查后 `阻塞` 且问题本质属于重编排 | `阻塞` | `hf-workflow-router` | `true` | `record_path`、关键冲突说明、`key_findings` |

固定规则：
- 字段名统一使用 `conclusion`、`next_action_or_recommended_skill`、`record_path`、`key_findings`、`needs_human_confirmation`、`reroute_via_router`
- `hf-code-review` 的 `needs_human_confirmation` 默认固定为 `false`
- 除 `通过` 且确无问题外，`key_findings` 不得留空
- `next_action_or_recommended_skill` 必须是一个唯一 canonical 值，不得拼接多个候选动作
- 若输出不能映射到上表中的一行，说明 verdict 还没收敛好，不能返回

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-test-review` | 评审测试设计与覆盖度；本 skill 评审实现代码质量 |
| `hf-traceability-review` | 评审规格→设计→实现的可追溯性；本 skill 聚焦代码正确性与设计一致性 |
| `hf-bug-patterns` | 把重复错误提炼为长期可复用模式；本 skill 做当前代码的多维质量评审 |
| `hf-test-driven-dev` | 写/修代码；本 skill 只审不改 |

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/review-checklist.md` | code review checklist 与 rule IDs（CR1-CR7、CA1-CA10） |
| `references/clean-architecture-guardrails.md` | CR7（Architectural Health & Refactoring Hygiene）子维度展开、anti-patterns、verdict 决策、Two Hats / Boy Scout / smells / SOLID conformance 检查规则 |
| `references/review-record-template.md` | code review 记录模板与结构化返回契约 |
| `hf-workflow-router/references/reviewer-return-contract.md` | 当前 skill pack 共享的 reviewer 返回契约  |

## Red Flags

- 不读实现交接块（含 Refactor Note）就审代码
- "测试通过"等同于"代码正确"
- 忽略错误处理/安全风险
- 评审中改代码
- 返回多个候选下一步
- 因为"功能正确 + 测试全绿"就放过帽子混戴（CA6）、放过 architectural smell（CA10）或放过 escalation-bypass（CA8）
- 在 review 内重新讨论架构选择（这是 `hf-design` 的工作；reviewer 只做 conformance check）
- Refactor Note 缺失但 verdict 仍给"通过"
- 把跨 ≥3 模块的结构性问题写成 minor finding

## Verification

- [ ] review record 已落盘
- [ ] 给出明确结论、findings、code risks 和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id（含 CR7 / CR7.x / CA6-CA10 时遵循同一规则）
- [ ] 结构化摘要含 record_path 和 next_action_or_recommended_skill
- [ ] 已对实现交接块的 Refactor Note 做 CR7 评审（Two Hats / Refactor Note 完整性 / Architectural Conformance / Architectural Smells / Boy Scout）
- [ ] CR7 触发 escalation-bypass（CA8）/ 实质修改 ADR / 模块边界 / 接口契约时，verdict 为 `阻塞`，下一步 `hf-workflow-router`，`reroute_via_router=true`
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] workflow blocker 时已显式写明 reroute_via_router

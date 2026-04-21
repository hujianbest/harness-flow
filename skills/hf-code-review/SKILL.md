---
name: hf-code-review
description: 适用于 test review 通过后评审代码质量、用户要求 code review 的场景。不适用于评审测试（→ hf-test-review）、写/修代码（→ hf-test-driven-dev）、阶段不清（→ hf-workflow-router）。
---
# HF Code Review

评审实现代码质量。判断正确性、设计一致性、状态/错误/安全、可读性和下游追溯就绪度。运行在 `hf-test-review` 之后，决定是否可进入 `hf-traceability-review`。

## Methodology

本 skill 融合以下已验证方法：

- **Fagan Code Inspection (adapted)**: 结构化检查正确性、设计一致性、状态安全、可读性四个维度，而非自由形式代码阅读。
- **Design Conformance Check**: 实现必须遵循已批准设计，偏离需有理由且可追溯——防止实现与设计漂移。
- **Defense-in-Depth Review**: 错误处理、状态转换、安全性逐层检查，确保不因"测试通过"掩盖实现隐患。
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

读实现交接块、代码变更、test-review 记录（默认 `features/<active>/reviews/test-review-task-NNN.md`）、AGENTS.md coding 约定、规格/设计片段（默认 `features/<active>/spec.md` / `design.md`）、feature `progress.md`（默认 `features/<active>/progress.md`）。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定实现交接块、可定位代码变更、route/stage/profile 与上游 evidence 是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定交接块或核心代码范围不可定位 → 写最小 blocked record，下一步 `hf-test-driven-dev`
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

6 维度 0-10 评分：正确性、设计一致性、状态/错误/安全、可读性、范围守卫、下游追溯就绪度。任一关键维度 < 6 不得通过。

按 `references/review-checklist.md` 做正式审查。

每条 finding 必须带：

- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `CR2`、`CR5`、`CA3`）

默认分类：

- `USER-INPUT`：实现偏离设计且涉及新的产品/业务决策、超范围功能是否保留仍需真人拍板
- `LLM-FIXABLE`：代码结构、错误处理、命名、边界、防御性检查、实现交接块缺口等代码层问题

### 3. 正式 checklist 审查

3.1 **正确性**：实现是否真正完成了任务目标？逻辑是否有 off-by-one、边界遗漏？
3.2 **设计一致性**：实现是否遵循已批准设计？偏离是否有理由且可追溯？
3.3 **状态/错误/安全**：错误处理是否完备？状态转换是否安全？是否有安全隐患？
3.4 **可读性**：命名是否清晰？结构是否合理？是否有过早优化或死代码？
3.5 **下游就绪度**：代码是否足以让 traceability-review 做可信判断？实现交接块是否完整？

### 4. 形成 verdict

- `通过`：所有维度 >= 6，代码足以支持追溯评审 → `next_action_or_recommended_skill=hf-traceability-review`，`needs_human_confirmation=false`
- `需修改`：findings 可 1-2 轮定向修订 → `next_action_or_recommended_skill=hf-test-driven-dev`，`needs_human_confirmation=false`
- `阻塞`：核心逻辑错误/安全漏洞/findings 无法定向回修 → `next_action_or_recommended_skill=hf-test-driven-dev`，`needs_human_confirmation=false`；若问题本质是 stage/route/profile/上游证据冲突 → `next_action_or_recommended_skill=hf-workflow-router`，`reroute_via_router=true`

Findings 带 severity 和 USER-INPUT/LLM-FIXABLE 分类。给出代码风险和追溯评审提示。

### 5. 写 review 记录

保存到 `AGENTS.md` 声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/code-review-task-NNN.md`。若项目无专用格式，默认使用 `references/review-record-template.md`。

回传结构化摘要时遵循当前 skill pack 中 `hf-workflow-router/references/reviewer-return-contract.md`：`next_action_or_recommended_skill` 只写一个 canonical 值；workflow blocker 必须显式写 `reroute_via_router=true`。

### 5A. 最终返回闸门

在返回给父会话前，先把 reviewer 结论收敛成**唯一 verdict + 唯一下一步 + 固定字段集合**。不要只给自然语言 code review 评论。

| 场景 | conclusion | next_action_or_recommended_skill | reroute_via_router | 最少必须写出的字段 |
|---|---|---|---|---|
| precheck blocked：route / stage / profile / 上游 evidence 冲突 | `阻塞` | `hf-workflow-router` | `true` | `record_path`、关键冲突说明、`key_findings` |
| precheck blocked：缺稳定实现交接块或核心代码范围不可定位 | `阻塞` | `hf-test-driven-dev` | `false` | `record_path`、缺失输入、为什么当前无法合法开始 code review |
| 正式审查后 `通过` | `通过` | `hf-traceability-review` | `false` | `record_path`、主要通过依据、非阻塞优化项（若有） |
| 正式审查后 `需修改` | `需修改` | `hf-test-driven-dev` | `false` | `record_path`、`key_findings`、`finding_breakdown`、代码风险与下游追溯提示 |
| 正式审查后 `阻塞` 且可回实现补救 | `阻塞` | `hf-test-driven-dev` | `false` | `record_path`、核心阻塞问题、为什么不能 1-2 轮定向回修 |
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
| `references/review-checklist.md` | code review checklist 与 rule IDs |
| `references/review-record-template.md` | code review 记录模板与结构化返回契约 |
| `hf-workflow-router/references/reviewer-return-contract.md` | 当前 skill pack 共享的 reviewer 返回契约  |

## Red Flags

- 不读实现交接块就审代码
- "测试通过"等同于"代码正确"
- 忽略错误处理/安全风险
- 评审中改代码
- 返回多个候选下一步

## Verification

- [ ] review record 已落盘
- [ ] 给出明确结论、findings、code risks 和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id
- [ ] 结构化摘要含 record_path 和 next_action_or_recommended_skill
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] workflow blocker 时已显式写明 reroute_via_router

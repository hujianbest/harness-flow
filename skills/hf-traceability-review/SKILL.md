---
name: hf-traceability-review
description: 适用于 code review 通过后判断追溯完整性、用户显式要求追溯评审的场景。不适用于评审代码质量（→ hf-code-review）、评审测试质量（→ hf-test-review）、阶段不清（→ hf-workflow-router）。
---

# HF Traceability Review

评审证据链追溯完整性：spec→design→tasks→impl→test/verification→status。防止"代码能跑但不再匹配已批准工件"。运行在 `hf-code-review` 之后，决定是否可进入 `hf-regression-gate`。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **End-to-End Traceability** | 检查从需求到实现的完整追溯链，确保每条需求可通过设计、任务、实现、验证四层逐级追溯 | IEEE 830-1993 / ISO 26550 需求追溯实践 | 步骤 2 — 多维评分；步骤 3 — checklist 审查 |
| **Zigzag Validation** | 每条 FR 前向追溯到设计决策，设计决策后向追溯到需求——双向验证防止断链 | 项目化实践（需求追溯通用方法） | 步骤 3.1/3.2 — 规格-设计/设计-任务双向验证 |
| **Impact Analysis** | 发现不一致时判断影响范围是局部还是需要回流到上游节点 | 项目化实践（变更影响分析通用方法） | 步骤 4 — verdict；步骤 5 — review 记录 |

## When to Use

适用：
- code review 通过后判断追溯完整性
- 用户显式要求追溯评审

不适用 → 改用：
- 评审代码质量 → `hf-code-review`
- 评审测试质量 → `hf-test-review`
- 阶段不清 → `hf-workflow-router`

Direct invoke 信号："追溯评审"、"traceability review"、"帮我检查证据链完整性"。

## 和其他 Skill 的区别

| 场景 | 用 hf-traceability-review | 不用 |
|------|---------------------------|------|
| 评审规格→设计→任务→实现的追溯链 | ✅ | |
| 评审代码质量 | | → `hf-code-review` |
| 评审测试质量 | | → `hf-test-review` |
| 评审任务计划质量 | | → `hf-tasks-review` |
| 阶段不清/证据冲突 | | → `hf-workflow-router` |

## Hard Gates

- traceability review 通过前不得进入 regression gate
- 输入工件不足不得开始评审
- reviewer 不修代码、不继续实现

## Workflow

### 1. 建立证据基线

读已批准规格、设计、任务计划（默认 `features/<active>/spec.md` / `design.md` / `tasks.md`）、实现交接块、test-review/code-review 记录（默认 `features/<active>/reviews/`）、项目级约定、feature `progress.md`（默认 `features/<active>/progress.md`）。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定可定位的上游工件、实现交接块与上游 review 记录是否一致、route/stage/profile 是否稳定。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺关键上游工件或稳定实现交接块 → 写最小 blocked record，下一步 `hf-test-driven-dev`
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

6 维度 0-10 评分：规格-设计追溯、设计-任务追溯、任务-实现追溯、实现-验证追溯、漂移与回写义务、整体证据链闭合度。任一关键维度 < 6 不得通过。

按 `references/review-checklist.md` 做正式审查。

每条 finding 必须带：
- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `TZ2`、`TZ5`、`ZA3`）

默认分类：
- `USER-INPUT`：规格 / 设计本身发生冲突、范围变化需走 increment、行为是否正式纳入批准工件仍需真人拍板
- `LLM-FIXABLE`：trace anchor 缺口、任务/文档未回写、实现交接块与验证记录表述不清、局部证据链可定向补齐

### 3. 正式 checklist 审查

3.1 **规格-设计链**：设计决策是否可追溯到规格需求？
3.2 **设计-任务链**：任务是否覆盖设计中的关键决策？
3.3 **任务-实现链**：实现是否完成任务的完成条件？触碰工件是否一致？
3.4 **实现-验证链**：验证证据是否锚定到当前实现？RED/GREEN 是否可追溯？
3.5 **整体闭合**：有没有断链？approved 工件与当前代码是否仍然一致？

### 4. 形成 verdict

- `通过`：证据链完整，可进入 regression gate
- `需修改`：findings 可定向补齐追溯 → `hf-test-driven-dev`
- `阻塞`：核心链路断裂/工件与代码严重不一致 → `hf-workflow-router`

### 4A. Verdict 写回闸门

在返回结论前，必须先把 verdict 收敛成**唯一下一步 + 最小结构化字段**。不要只写自然语言结论。

| 场景 | conclusion | next_action_or_recommended_skill | reroute_via_router | 最少必须写出的字段 |
|---|---|---|---|---|
| precheck blocked：route / stage / 证据冲突 | `阻塞` | `hf-workflow-router` | `true` | `record_path`、workflow blocker、关键冲突说明 |
| precheck blocked：缺关键上游工件或稳定实现交接块 | `阻塞` | `hf-test-driven-dev` | `false` | `record_path`、缺失工件、为什么当前无法继续 traceability review |
| 正式审查后 `需修改` | `需修改` | `hf-test-driven-dev` | `false` | `record_path`、`key_findings`、`finding_breakdown`、需要补齐的 trace anchor / 回写项 |
| 正式审查后 `通过` | `通过` | `hf-regression-gate` | `false` | `record_path`、链接矩阵、剩余非阻塞提示（若有） |
| 正式审查后 `阻塞` | `阻塞` | `hf-workflow-router` | `true` | `record_path`、核心断链点、为什么不能定向回修 |

约束：
- `needs_human_confirmation` 固定为 `false`
- 除 `通过` 且确无问题外，`key_findings` 不得留空
- 只允许一个 canonical `next_action_or_recommended_skill`
- 若输出不能映射到上表中的一行，说明 verdict 还没收敛好，不能返回

### 5. 写 review 记录

保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/traceability-review.md`（全 feature 一次性 review，scope 省略；若同一 feature 内多次复审，追加日期或序号后缀）。参考 `references/traceability-review-record-template.md`。

## Output Contract

完成时产出：
- Review 记录（保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/traceability-review.md`）
- 链接矩阵（spec→design→tasks→impl→test 映射）
- 明确 verdict 和唯一下一步
- workflow blocker 时显式写明 `reroute_via_router=true`

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/review-checklist.md` | traceability review checklist 与 rule IDs |
| `references/traceability-review-record-template.md` | 追溯评审记录模板与结构化返回契约 |

## Red Flags

- 不读上游工件就做追溯判断
- "代码能跑"等同于"追溯完整"
- 忽略规格/设计与代码的不一致
- 返回多个候选下一步

## Verification

- [ ] review record 已落盘
- [ ] 链接矩阵已建立
- [ ] 给出明确结论、findings 和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] 结论足以让父会话路由

---
name: hf-tasks-review
description: 适用于任务计划草稿需正式 review verdict、任务计划被退回需复审、或用户显式要求评审任务计划的场景。不适用于写/修任务计划（→ hf-tasks）、阶段不清（→ hf-workflow-router）。
---

# HF Tasks Review

评审任务计划，判断任务是否可执行、可验证、正确排序、忠实覆盖已批准规格/设计。确保计划能支撑 router 稳定重选下一任务。

关键区别：通过时设 `needs_human_confirmation=true`（"任务真人确认" approval step），任务计划获批后才能进入实现。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **INVEST Validation** | 检查每个任务是否满足 Independent/Negotiable/Valuable/Estimable/Small/Testable | Bill Wake, 2003；敏捷用户故事实践 | 步骤 2 — 多维评分；步骤 3.1 — 可执行性 |
| **Dependency Graph Validation** | 校验任务间依赖关系的正确性和无环性 | 项目化实践（任务计划评审通用方法） | 步骤 2 — 多维评分；步骤 3.3 — 依赖/顺序 |
| **Traceability Matrix** | 检查任务是否忠实覆盖规格/设计的每一项关键决策 | ISO/IEC/IEEE 29148 需求追溯实践 | 步骤 2 — 多维评分；步骤 3.4 — 追溯覆盖 |
| **Structured Walkthrough** | 多维度评分量化判断，任一关键维度低于阈值不得通过 | 项目化实践（评审通用方法） | 步骤 2 — 多维评分；步骤 4 — verdict |

## When to Use

适用：
- 任务计划草稿需正式 review verdict
- `hf-tasks` 返回 `需修改` 或 `阻塞`，需复审修订后的计划
- 用户显式要求 review tasks plan

不适用 → 改用：
- 写/修任务计划 → `hf-tasks`
- 阶段不清 → `hf-workflow-router`
- 评审规格/设计 → 对应 review skill

Direct invoke 信号：\"review 任务计划\"、\"tasks review\"、\"帮我审一下这个计划\"。

## 和其他 Skill 的区别

| 场景 | 用 hf-tasks-review | 不用 |
|------|-------------------|------|
| 评审任务计划质量和可执行性 | ✅ | |
| 写/修任务计划 | | → `hf-tasks` |
| 评审规格草稿 | | → `hf-spec-review` |
| 评审设计 | | → `hf-design-review` |
| 评审测试质量 | | → `hf-test-review` |
| 阶段不清/证据冲突 | | → `hf-workflow-router` |

## Hard Gates

- tasks review 通过并完成 approval step 前，不得进入 `hf-test-driven-dev`
- 输入工件不足不得开始
- reviewer 不替用户决定优先级或拆分方案

## Workflow

### 1. 建立证据基线

读任务计划、已批准规格、已批准设计（默认 `features/<active>/tasks.md` / `spec.md` / `design.md`）、项目级约定、feature `progress.md`（默认 `features/<active>/progress.md`）。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定可定位的任务计划、上游规格 / 设计 approval evidence 是否可回读、route/stage/profile 是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定任务计划 → 写最小 blocked record，下一步 `hf-tasks`
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

6 维度 0-10 评分：任务可执行性、任务合同完整性、验证与测试设计种子、依赖/顺序正确性、追溯覆盖度、router 重选就绪度。任一关键维度 < 6 不得通过。

按 `references/review-checklist.md` 做正式审查。

每条 finding 必须带：
- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `TR2`、`TR5`、`TA3`）

默认分类：
- `USER-INPUT`：优先级冲突、上游规格/设计裁决仍未稳定、任务边界一旦重排就会改变已确认范围或发布顺序
- `LLM-FIXABLE`：缺少 Acceptance / Files / Verify / test seed、任务过大、依赖链缺口、queue projection 表达不清

### 3. 正式 checklist 审查

3.1 **可执行性**：每个任务是否冷启动可执行？是否有"实现某模块"式模糊任务？
3.2 **任务合同完整性**：关键任务是否显式具备 `Acceptance`、`Files`、`Verify`、完成条件？
3.3 **验证与测试设计种子**：测试设计种子是否足够支持后续 fail-first 实现？是否只写了“补测试”这类空话？
3.4 **依赖/顺序**：依赖关系是否正确？关键路径是否合理？是否有循环依赖？
3.5 **追溯覆盖**：任务是否忠实覆盖规格/设计？是否有任务无法追溯到上游依据？
3.6 **Router 重选就绪度**：Current Active Task 选择规则是否唯一？queue projection 是否稳定？

### 4. 形成 verdict

- `通过`：所有维度 >= 6，计划可进入 approval step → `next_action_or_recommended_skill=任务真人确认`，`needs_human_confirmation=true`
- `需修改`：findings 可定向修订 → `next_action_or_recommended_skill=hf-tasks`，`needs_human_confirmation=false`
- `阻塞`：核心任务结构有问题/findings 无法定向回修 → `next_action_or_recommended_skill=hf-tasks`，`needs_human_confirmation=false`；若问题本质是 route/stage/profile/上游证据冲突 → `next_action_or_recommended_skill=hf-workflow-router`，`reroute_via_router=true`

### 5. 写 review 记录

保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/tasks-review-YYYY-MM-DD.md`。若项目无专用格式，默认使用 `references/review-record-template.md`。

回传结构化摘要时遵循当前 skill pack 中 `hf-workflow-router/references/reviewer-return-contract.md`：`next_action_or_recommended_skill` 只写一个 canonical 值；`通过` 时设 `needs_human_confirmation=true`；workflow blocker 必须显式写 `reroute_via_router=true`。

## Output Contract

完成时产出：
- Review 记录（保存到 项目声明的 review record 路径；若无项目覆写，默认使用 `features/<active>/reviews/tasks-review-YYYY-MM-DD.md`）
- 结构化摘要含 `record_path`、`next_action_or_recommended_skill`、`needs_human_confirmation`（通过时 = true）
- workflow blocker 时显式写明 `reroute_via_router=true`

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/review-checklist.md` | 正式 tasks review checklist 与 rule IDs |
| `references/review-record-template.md` | tasks review 记录模板与结构化返回契约 |
| `hf-workflow-router/references/reviewer-return-contract.md` | 当前 skill pack 共享的 reviewer 返回契约 |

## Red Flags

- 不读规格/设计就审任务
- "看起来差不多"就通过
- 忽略任务间依赖错误
- 返回多个候选下一步

## Verification

- [ ] review record 已落盘
- [ ] 给出明确结论、findings 和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] 通过时已设 needs_human_confirmation=true
- [ ] 结构化摘要含 record_path 和 next_action_or_recommended_skill
- [ ] workflow blocker 时已显式写明 reroute_via_router

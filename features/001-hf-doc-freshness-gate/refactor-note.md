# Refactor Note — features/001-hf-doc-freshness-gate/ T1..T7 实施

> 按 hf-code-review CR7.2 vocabulary，prose-only HF skill 实施的 Refactor Note。

## Hat Discipline

T1..T7 严格 sequential（tasks.md §6.1 trade-off 表已显式称重）。每任务作为独立 Changer hat 步骤，无 in-task hat-mixing：

- T1..T4：纯 Changer hat（创建新 skill 文件）
- T5..T6：纯 Changer hat 但作用于既有 skill；本质仍是 "add new prose section / row"，未做 refactor 类的"保持行为不变改结构"操作
- T7：纯 Changer hat（dogfooding evidence 文件创建）

无 preparatory refactoring 步骤被使用——本 feature 是新建 skill，无既有结构需要先扩展点。

## In-task Cleanups (Fowler vocabulary)

| Task | Cleanup 操作 (Fowler vocab) | 触碰范围 |
|---|---|---|
| T1 | "Insert Section" × 9（创建 SKILL.md 8 标准段 + Methodology 段） | skills/hf-doc-freshness-gate/SKILL.md (新文件) |
| T2 | "Insert Section" × 3（创建 3 个 reference 文件）+ "Add Reference" × 3（在 SKILL.md Reference Guide 段引用） | skills/hf-doc-freshness-gate/references/{...}.md (新文件) |
| T3 | "Insert Section" × 2（创建 2 个 template 文件） | skills/hf-doc-freshness-gate/templates/{...}.md (新文件) |
| T4 | "Insert JSON Array" × 1（创建 evals/test-prompts.json） | skills/hf-doc-freshness-gate/evals/test-prompts.json (新文件) |
| T5 | "Insert Section Row" × 5×3=15（5 logical canonical transitions × 3 profiles）+ "Insert List Item" × 3（三 profile 主链节点列表）+ "Replace Chain Tail" × 4（4 canonical route map chain in-place 修改） | skills/hf-workflow-router/references/profile-node-and-transition-map.md (修改既有文件) |
| T6 | "Insert Section" × 1（completion-gate SKILL.md §6.1 新增段） | skills/hf-completion-gate/SKILL.md (修改既有文件) |
| T7 | "Insert Evidence Records" × 4（dogfooding dry-run 4 份证据文件）+ "Update Field" × 2（progress.md HYP-004 行 + spec.md §4 HYP-004 行的 status 同步） | features/001-hf-doc-freshness-gate/evidence/ + 2 既有文件的字段更新 |

无 Boy Scout 顺手清理（无既有 prose 健康度退化需要修复）。

## Architectural Conformance

按 design §11 模块表 + ADR-0002 / ADR-0003 决策：

- ✅ 依赖方向：`responsibility-matrix.md`（spec §6.2 cold-link 权威，无依赖）→ `profile-rubric.md`（依赖 responsibility-matrix）→ `SKILL.md`（依赖 references 全部）→ `templates/`（依赖 references 中的判定规则）；`reviewer-dispatch-handoff.md` 显式 chain 到既有 `hf-workflow-router/references/review-dispatch-protocol.md`，未自创 dispatch 协议
- ✅ 模块边界：本 skill 不修改 `hf-finalize` / `hf-code-review` / `hf-traceability-review` / `hf-increment` 任何 SKILL.md（CON-001 严守）；T5 / T6 修改 `hf-workflow-router` / `hf-completion-gate` 是 design §11 显式声明的最小修改范围
- ✅ 接口契约：reviewer-return JSON 字段（conclusion / next_action_or_recommended_skill / record_path / key_findings / needs_human_confirmation / reroute_via_router / dimension_breakdown）与既有 `hf-workflow-router/references/reviewer-return-contract.md` 完全一致（reuse not extend）
- ✅ 不变量：spec §6.2 责任矩阵 14 行 × 5 列在 `responsibility-matrix.md` 中以等价摘要表形式 cold-link，未复述（避免双 source-of-truth 漂移）

## Documented Debt

无新增 architectural debt。Open Risks 已在 `progress.md` Open Risks 段记录（HYP-001 desk-research 单方法 / NFR-001 严格双 dispatch 验证延后到 Phase 1+ / T5-T6 改既有 skill 守 boundary / T7 dogfooding chicken-and-egg）；这些是 *known limitations*，非新引入 debt。

## Escalation Triggers

无触发。本 feature 实施过程中未遇到：

- 跨 ≥3 模块的结构性重构（最多触碰 hf-doc-freshness-gate / hf-workflow-router / hf-completion-gate 3 个 skill 但都是 prose-only 新增段，非结构性）
- ADR 修改（ADR-0001/0002/0003 是本 feature 自己产出的新 ADR，非修改既有）
- 已批准模块边界 / 接口契约的修改（保持 design §11 声明的最小修改范围）
- 引入设计未声明的新抽象层（design §6 已声明复用既有 4 个模式，未引入新抽象）

故不需要回 `hf-workflow-router` 重新编排 / `hf-increment` 处理范围变更。

## Fitness Function Evidence

按 prose-only 项目的 fitness function 解释：

- ✅ T5 evidence log boundary check：6 条 anchored grep 反向验证既有 transition rules 全部保持（semantic delete = 0）
- ✅ T6 evidence log boundary check：既有 verdict 词表 (通过/需修改/阻塞) 8/6/13 occurrences 完全保持；§6A 完成判定闸门 anchor 仍在；+10/-0 lines（boundary 严守）
- ✅ T7 4 份 dry-run evidence：NFR-001 / NFR-002 / NFR-003 / NFR-004 实测全部 PASS
- ✅ 整轮 7 任务 GREEN evidence 均落到 `features/001-hf-doc-freshness-gate/evidence/T*-*.log`，可被后续 `hf-traceability-review` / `hf-regression-gate` / `hf-completion-gate` 消费

## 总结

本实施严格遵守 design §11 Boundary Constraints 与 spec CON-001..CON-007；无 hat-mixing、无 in-task escalation、无新增 architectural debt；所有修改通过 fitness function（boundary check + dogfooding dry-run）验证健康度未退化。

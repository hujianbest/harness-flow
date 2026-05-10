# Tasks — 002-leaf-skill-decoupling (v0.7.0)

- 状态: 草稿
- 主题: 实施 ADR-007 D3 Step 2-5 + v0.7.0 一次性发布完整版
- 上游: ADR-007（架构）+ ADR-008（release scope）
- 继承: features/001-orchestrator-extraction/spec.md (FR-001..007 + NFR-001..005) + design.md (D-X 决策)；不重新 spec/design

## 1. 概述

24 个 hf-* leaf skill **耦合解除**——把每个 leaf 的 4 个耦合点（Step 2: `Next Action` 字段；Step 3: Hard Gates 标签；Step 4: `[Workflow]` Gate 物理上提；Step 5: 跨 hf-* 硬引用）一次性清理。leaf 核心方法论内容**不动**（TDD Two Hats / SUT Form / Fagan rubric / DDD strategic+tactical / EARS+BDD+MoSCoW / NFR QAS 等全部保留）。

orchestrator persona 升级到**纯 artifact 驱动**——不再依赖 leaf 的 `Next Action` hint。orchestrator 主文件 + references 同步更新。

按 Tier 顺序实施：Tier 1（10 leaf）→ sub-gate → Tier 2（14 leaf）→ orchestrator 升级 → walking-skeleton 端到端验证 → release pack。

## 2. 里程碑

| 里程碑 | 包含任务 | 退出标准 |
|---|---|---|
| **M0: 骨架** | T1（ADR-008）+ T2（feature scaffolding）+ T3（tasks-review approval）| ADR-008 起草 + feature 目录就位 + tasks-review 通过 |
| **M1: Orchestrator 升级** | T4（orchestrator 主文件 + references 升级到纯 artifact 驱动；保留 v0.6.0 兼容期 fallback 消费 leaf `Next Action` 作为辅助 hint）| `agents/hf-orchestrator.md` + `agents/references/profile-node-and-transition-map.md` + `reviewer-return-contract.md` 描述明确"以 artifact 为权威；leaf `Next Action` 作为 v0.6.x 兼容 hint" |
| **M2: Tier 1 leaf 解耦** | T5-T14（4 doer + 6 reviewer × Step 2/3/4/5）| 每个 leaf 4 步全做；grep 验证 0 跨 hf-* 硬引用 + Hard Gates 标签齐全 + `Next Action` 字段标 optional |
| **M3: Tier 1 sub-gate** | T15（Tier 1 grep 验证 + walking-skeleton 局部 smoke）| 10 leaf 全部 GREEN；orchestrator 在不依赖 Next Action 的情况下能正确派发到 Tier 1 leaf |
| **M4: Tier 2 leaf 解耦** | T16-T29（8 doer + 6 reviewer/gate × Step 2/3/4/5）| 同 M2 但范围 14 leaf |
| **M5: HYP-005 release-blocking 验证** | T30（walking-skeleton 端到端 v0.7.0 跑一遍；对照 v0.5.1 baseline 运行时等价；HYP-002 升级版 + HYP-005 双验证）| `regression-diff.py` PASS + orchestrator 纯 artifact 驱动决策记录入档 |
| **M6: Docs sync + version bump** | T31-T35（README × 2 / setup docs × 3 / CHANGELOG 整合 [0.7.0] 删 [0.6.0] / SECURITY / CONTRIBUTING / plugin manifest version）| 全部文档反映 v0.7.0 完整交付 narrative |
| **M7: Release pack** | T36（hf-release dogfood #5 → release-pack.md + release-regression.md + release-traceability.md + pre-release-checklist.md → ready-for-tag）| v0.7.0 release pack 全 GREEN，maintainer 可执行 git tag |

## 3. 文件 / 工件影响图

### 修改

- `agents/hf-orchestrator.md`（M1）
- `agents/references/profile-node-and-transition-map.md` + `reviewer-return-contract.md` + `routing-evidence-guide.md`（M1）
- 24 leaf SKILL.md（M2 + M4；Step 2/3/4/5 全套）
  - Tier 1 (10): `skills/hf-{specify,design,tasks,test-driven-dev}/SKILL.md` + `skills/hf-{spec,design,tasks,test,code,traceability}-review/SKILL.md`
  - Tier 2 (14): `skills/hf-{product-discovery,experiment,hotfix,increment,finalize,ui-design,browser-testing,release}/SKILL.md` + `skills/hf-{ui,discovery}-review/SKILL.md` + `skills/hf-{regression,completion,doc-freshness}-gate/SKILL.md`
- 部分 leaf 的 `references/*.md`（按需；如 reviewer-return-contract 等）
- `README.md` / `README.zh-CN.md` Scope Note（M6）
- `docs/{cursor,claude-code,opencode}-setup.md`（M6）
- `CHANGELOG.md`（整合 [0.7.0]，删 [0.6.0]；M6）
- `SECURITY.md` / `CONTRIBUTING.md` / `.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` / `.cursor/rules/harness-flow.mdc`（version bump；M6）

### 新增

- `docs/decisions/ADR-008-...md`（M0）
- `features/002-leaf-skill-decoupling/{README,progress,tasks}.md` + reviews/ + approvals/ + verification/ 目录（M0）
- `features/release-v0.7.0/{release-pack.md, verification/release-regression.md, verification/release-traceability.md, verification/pre-release-checklist.md}`（M7）

### 显式不动

- 24 leaf SKILL.md 的核心方法论内容（TDD Two Hats / SUT Form / Fagan rubric / DDD / EARS / 等等）
- closeout pack schema / reviewer return verdict 词表 / hf-release 行为 / audit-skill-anatomy.py / hf-finalize step 6A
- `using-hf-workflow` / `hf-workflow-router` deprecated alias（D3 Step 6 仍 deferred）
- features/001-orchestrator-extraction/ 历史工件（v0.6.0 中间产物，不修改历史）

## 4. 需求与设计追溯

| 来源 | 本 feature 任务 |
|---|---|
| ADR-007 D3 Step 2 | 24 leaf × `Next Action` 字段降级 (T5-T29 各含一项) |
| ADR-007 D3 Step 3 | 24 leaf × Hard Gates 标签 `[SOP]` / `[Workflow]` (T5-T29 各含一项) |
| ADR-007 D3 Step 4 | 24 leaf × `[Workflow]` 类 Gate 物理上提 (T5-T29 各含一项；orchestrator side 由 T4 配套支持) |
| ADR-007 D3 Step 5 | 24 leaf × 跨 hf-* 硬引用清理 (T5-T29 各含一项) |
| ADR-007 D5 release-blocking HYP-002 | T30 walking-skeleton 端到端 (升级到运行时等价) |
| ADR-008 D5 release-blocking HYP-005 | T30 orchestrator 纯 artifact 驱动决策验证 |
| ADR-008 D6 CHANGELOG 整合 | T33 |
| ADR-008 D7 narrative 校准 | T31 + T32 + T33 |

## 5. 任务拆解

### M0: 骨架

#### T1. ADR-008 起草

- 目标: `docs/decisions/ADR-008-v0.7.0-skip-v0.6.0-tag-and-deliver-step-2-5-as-single-release.md` 落盘
- Acceptance:
  - 文件存在，含 D1-D7 决策段
  - 与 ADR-001 / ADR-007 关系表完整
- Status: ✓ DONE

#### T2. Feature scaffolding

- 目标: features/002-leaf-skill-decoupling/{README, progress, tasks}.md + 子目录
- Status: ✓ DONE

#### T3. hf-tasks-review approval

- 目标: 派发 reviewer subagent 评审本 tasks.md；通过后进 hf-test-driven-dev
- Acceptance: tasks-review verdict = `通过` 或 `需修改 → 通过` 后产出 approval record

### M1: Orchestrator 升级

#### T4. agents/hf-orchestrator.md + references 升级到纯 artifact 驱动

- 目标:
  - orchestrator 主文件 § "归一化显式 handoff" 段重写：取消"消费 `Next Action Or Recommended Skill` 字段作为权威 hint"；改为"以 features/<active>/{progress.md, reviews/*, verification/*} 为权威；v0.6.x 兼容期可读 leaf 的 `Next Action` 作为辅助 hint，但不强制 leaf 提供"
  - `agents/references/profile-node-and-transition-map.md` 的 transition map 中"by Next Action handoff"路径改为"by progress.md.Current Stage + reviews/*.结论 + verification/*.结论"
  - `agents/references/reviewer-return-contract.md` 中 `next_action_or_recommended_skill` 字段从必填降为 optional；增加段说明 v0.7.0+ orchestrator 不依赖该字段（reviewer 仍可填，作为 hint）
  - `agents/references/routing-evidence-guide.md` 加段说明纯 artifact 驱动的决策矩阵
- Acceptance:
  - 4 文件修改齐全；grep "Next Action" 出现位置全部带 "optional" / "hint" / "v0.6.x 兼容" 限定语
  - orchestrator 文件继续保留 "I am the HF Orchestrator" identity 锚点
  - `wc -c agents/hf-orchestrator.md` 仍 ≤ 23,245 bytes (NFR-002 保持)
- Files: agents/hf-orchestrator.md + agents/references/{profile-node-and-transition-map, reviewer-return-contract, routing-evidence-guide}.md

### M2: Tier 1 leaf 解耦（10 leaf × Step 2-5）

#### T5-T14：每个 leaf 一个 task；每 task 4 个 acceptance（Step 2/3/4/5）

| Task ID | Skill | Path |
|---|---|---|
| T5 | hf-specify | skills/hf-specify/SKILL.md |
| T6 | hf-design | skills/hf-design/SKILL.md |
| T7 | hf-tasks | skills/hf-tasks/SKILL.md |
| T8 | hf-test-driven-dev | skills/hf-test-driven-dev/SKILL.md |
| T9 | hf-spec-review | skills/hf-spec-review/SKILL.md |
| T10 | hf-design-review | skills/hf-design-review/SKILL.md |
| T11 | hf-tasks-review | skills/hf-tasks-review/SKILL.md |
| T12 | hf-test-review | skills/hf-test-review/SKILL.md |
| T13 | hf-code-review | skills/hf-code-review/SKILL.md |
| T14 | hf-traceability-review | skills/hf-traceability-review/SKILL.md |

每 task 通用 acceptance：

- **(.1 Step 2)** SKILL.md 中 `Next Action Or Recommended Skill` 字段所有出现位置标注 "optional / 可选 (v0.6.x compatibility hint; v0.7.0+ orchestrator drives by on-disk artifacts)"；无强制要求该字段非空
- **(.2 Step 3)** SKILL.md "Hard Gates" 段每条加 `[SOP]` 或 `[Workflow]` 标签：
  - `[SOP]`: skill 单独调用时仍生效的纪律（如 TDD Two Hats / RED 必须真失败 / SUT Form allowlist / Fagan author-reviewer 分离 / EARS+BDD 必填 / NFR QAS 必填 / DDD 触发条件 / 等）
  - `[Workflow]`: 仅在 HF workflow 编排下成立的依赖（如 "已批准 tasks.md" / "spec 通过 review" / "上游 approval record 存在" / "feature directory 存在" / 等）
- **(.3 Step 4)** `[Workflow]` 类 Hard Gate 物理删除（orchestrator pre-check 已在 T4 处理对应校验）；保留 `[SOP]` 类
- **(.4 Step 5)** SKILL.md body 中所有对其它 hf-* 的硬引用清理：
  - "由 hf-workflow-router 决定"、"跨 task 切换由 router 决定" → 删除或改为软提及（如"see Also: agents/hf-orchestrator.md"）
  - "交给 hf-X" / "hf-X 接管" / "派发 hf-X-review" 类硬指 → 删除或改为软提及
  - 仅在 `## See Also` 段允许保留软提及；其它段位禁止
- 通用 fail-first: grep `"hf-workflow-router"` / `"Next Action Or Recommended Skill"` / `"必须存在已批准"` 等模式，修改前 hit count > 0；修改后 hit count = 0 或全部带 v0.7.0+ 限定语

#### T15. Tier 1 sub-gate

- 目标: 验证 10 leaf 全部 4 步完成 + orchestrator 在不依赖 Next Action 时能派发
- Acceptance:
  - `grep -l "Next Action Or Recommended Skill: hf-" skills/hf-{specify,design,tasks,test-driven-dev,spec-review,design-review,tasks-review,test-review,code-review,traceability-review}/SKILL.md` 返回空（或全部带 v0.7.0+ 限定语标识）
  - 每个 Tier 1 leaf 的 Hard Gates 段均含 `[SOP]` / `[Workflow]` 标签（grep -c 验证）
  - `[Workflow]` 类 Gate 已物理删除（grep "[Workflow]" 出现位置仅在 orchestrator pre-check 文档段内出现，不在 leaf 的 Hard Gates 段内）
  - 跨 hf-* 硬引用 grep = 0（除 `## See Also` 软提及）
- Files: 创建 `verification/tier1-sub-gate-2026-05-10.md`

### M4: Tier 2 leaf 解耦（14 leaf × Step 2-5）

#### T16-T29：每个 leaf 一个 task；每 task 4 个 acceptance（Step 2/3/4/5）

| Task ID | Skill | Path |
|---|---|---|
| T16 | hf-product-discovery | skills/hf-product-discovery/SKILL.md |
| T17 | hf-experiment | skills/hf-experiment/SKILL.md |
| T18 | hf-hotfix | skills/hf-hotfix/SKILL.md |
| T19 | hf-increment | skills/hf-increment/SKILL.md |
| T20 | hf-finalize | skills/hf-finalize/SKILL.md |
| T21 | hf-ui-design | skills/hf-ui-design/SKILL.md |
| T22 | hf-browser-testing | skills/hf-browser-testing/SKILL.md |
| T23 | hf-release | skills/hf-release/SKILL.md |
| T24 | hf-discovery-review | skills/hf-discovery-review/SKILL.md |
| T25 | hf-ui-review | skills/hf-ui-review/SKILL.md |
| T26 | hf-regression-gate | skills/hf-regression-gate/SKILL.md |
| T27 | hf-completion-gate | skills/hf-completion-gate/SKILL.md |
| T28 | hf-doc-freshness-gate | skills/hf-doc-freshness-gate/SKILL.md |
| T29 | （reserved）| （Tier 2 sub-gate；与 T15 同形）|

每 task acceptance 同 Tier 1（T5-T14）通用 acceptance。

T29 是 Tier 2 sub-gate，验证 14 leaf + 全 24 leaf 整体 GREEN。

### M5: HYP-002 + HYP-005 release-blocking 验证

#### T30. Walking-skeleton 端到端 v0.7.0 + orchestrator 纯 artifact 驱动验证

- 目标:
  - 跑一遍完整 v0.7.0 walking-skeleton（最薄端到端：spec → design → tasks → impl → reviews → finalize）；过程中**不让 leaf 写 `Next Action` 字段**（验证 orchestrator 仍能基于 progress.md + reviews/ + verification/ 推进）
  - 对照 `examples/writeonce/features/001-walking-skeleton/` v0.5.1 baseline 跑同一条端到端轨迹（升级 HYP-002 验证：从 self-diff 静态等价升级到运行时等价）
  - 产出物 schema-by-schema 对比 PASS（容许差异白名单不变）
- Acceptance:
  - `regression-diff.py` PASS over walking-skeleton 产出物
  - orchestrator 在过程中至少一次决策"无 Next Action 字段，仍按 artifact 推进"——证据写入 `verification/orchestrator-pure-artifact-driven-2026-05-10.md`
  - HYP-002 + HYP-005 双 VALIDATED
- Files: 创建 `verification/walking-skeleton-runtime-2026-05-10.md` + `verification/orchestrator-pure-artifact-driven-2026-05-10.md`

### M6: Docs sync + version bump

#### T31. README 中英 Scope Note 重写

- 目标: README.md / README.zh-CN.md Scope Note 段重写为 v0.7.0；明确 v0.6.0 was prepared but not tagged—superseded by v0.7.0；明确 standalone-usable skills 已在 v0.7.0 真正交付
- Acceptance: 两份 README 均含 v0.7.0 段 + 显式 standalone-usable claim

#### T32. Setup docs ×3 同步

- 目标: docs/{cursor,claude-code,opencode}-setup.md 全部同步到 v0.7.0；明确 standalone-usable + plugin 加载通道
- Acceptance: 3 doc 全部 ref agents/hf-orchestrator.md + 标 v0.7.0

#### T33. CHANGELOG 整合 [0.7.0] 段，删 [0.6.0] 段

- 目标:
  - CHANGELOG.md 删除 `## [0.6.0] - 2026-05-09` 段（按 ADR-008 D6）
  - 新增 `## [0.7.0] - 2026-05-10 — pre-release` 段；含 Foundation work (originally drafted as v0.6.0; now consolidated) + Standalone Skills (Step 2-5 实施) + Decided + Notes 子段
- Acceptance: CHANGELOG.md 含 [0.7.0] 段且不含 [0.6.0] 段；diff vs main 显示完整 [0.7.0] 内容

#### T34. 项目元数据 version bump

- 目标: SECURITY.md (Supported Versions v0.7.x) + CONTRIBUTING.md (引言 v0.7.0) + .claude-plugin/plugin.json (version 0.7.0) + .claude-plugin/marketplace.json (description) + .cursor/rules/harness-flow.mdc (Hard rules 段版本号)
- Acceptance: grep "0.7.0" 命中 ≥ 5 处；grep "0.6.0" 在 release-related metadata 中应只剩 CHANGELOG 历史段（已删的话 grep "0.6.0" should be 0）

#### T35. ADR-007 D1 Amendment 版本同步

- 目标: ADR-007 D1 Amendment 段中的 v0.6.0 标识全部更新为 v0.7.0（Amendment 在 v0.7.0 范围内仍然适用，但版本应反映本 release）；保留 v0.6.0 历史时间线（PR #45 #46 #47）作为实施记录
- Acceptance: ADR-007 内容仍准确，Amendment 段 ref v0.7.0 而不是 v0.6.0 作为 release 标识

### M7: Release pack

#### T36. hf-release v0.7.0 release pack（dogfood #5）

- 目标:
  - features/release-v0.7.0/{release-pack.md, verification/release-regression.md, verification/release-traceability.md, verification/pre-release-checklist.md}
  - 候选 feature: 002-leaf-skill-decoupling（已 closeout）
  - HYP-002 + HYP-003（v0.6.0 已验）+ HYP-005（本 release 新验）三 release-blocking 假设全 VALIDATED
  - Status: ready-for-tag
- Acceptance: release pack 4 文件全 GREEN；HF 第 5 次 dogfood `hf-release` 通过

## 6. 依赖与关键路径

```
T1 → T2 → T3 (tasks-review) → 
  T4 (orchestrator 升级；M1) → 
    [T5-T14 (Tier 1 leaf 并行；M2)] → 
      T15 (Tier 1 sub-gate；M3) → 
        [T16-T28 (Tier 2 leaf 并行；M4)] → 
          T29 (Tier 2 sub-gate；M4) → 
            T30 (HYP-002 + HYP-005 验证；M5) → 
              [T31-T35 (docs sync + version bump 并行；M6)] → 
                T36 (release pack；M7)
```

关键路径长度：**12 步**（T1 → T2 → T3 → T4 → T5 → T15 → T16 → T29 → T30 → T31 → T36 + 中间 review/gate 步骤）

## 7. 完成定义与验证策略

每 leaf 完成的判据 (T5-T29 通用):

```bash
# 修改前 baseline (在主分支)
grep -c "hf-workflow-router\|Next Action Or Recommended Skill: hf-\|必须存在已批准" skills/<name>/SKILL.md

# 修改后 (本分支)
grep -c "hf-workflow-router\|Next Action Or Recommended Skill: hf-\|必须存在已批准" skills/<name>/SKILL.md
# 应该 = 0 或全部带 v0.7.0+ 限定语 / "[Workflow]" 标签 / "## See Also" 段限定

grep -c "\[SOP\]\|\[Workflow\]" skills/<name>/SKILL.md
# 应该 ≥ 4 (至少几条 Hard Gate 被标签)

grep -c "Next Action Or Recommended Skill" skills/<name>/SKILL.md
# 字段仍可出现，但要带 "optional" / "hint" / "v0.6.x compat" 限定
```

总验证策略：M3 sub-gate（Tier 1）+ M4 sub-gate（Tier 2）+ M5 walking-skeleton 端到端（HYP-002+HYP-005 双验证）。

## 8. 当前活跃任务选择规则

按 Selection Priority + Ready When 决定：

- **P0**: 关联 release-blocking 假设或硬前置 (T4 / T30 / T36)
- **P1**: 必须进入 v0.7.0 范围 (T5-T29 leaf 修改 + T31-T35 docs)
- **P2**: 无（本 feature 全部为必需）

启动顺序：T1 (DONE) → T2 (DONE) → T3 (待) → T4 → Tier 1 (T5-T14 可并行) → T15 → Tier 2 (T16-T28 可并行) → T29 → T30 → T31-T35 (可并行) → T36

## 9. 任务队列投影视图

| # | Task | Priority | Status | 依赖 |
|---|---|---|---|---|
| 1 | T1 ADR-008 | P0 | ✓ DONE | - |
| 2 | T2 Feature scaffolding | P0 | ✓ DONE | T1 |
| 3 | T3 hf-tasks-review | P0 | ready | T2 |
| 4 | T4 Orchestrator 升级 | P0 | blocked-by-T3 | T3 |
| 5-14 | T5-T14 Tier 1 leaf | P1 | blocked-by-T4 | T4 |
| 15 | T15 Tier 1 sub-gate | P0 | blocked | T5-T14 |
| 16-28 | T16-T28 Tier 2 leaf | P1 | blocked | T15 |
| 29 | T29 Tier 2 sub-gate | P0 | blocked | T16-T28 |
| 30 | T30 HYP-002+005 验证 | P0 | blocked | T29 |
| 31-35 | T31-T35 Docs + version | P1 | blocked-by-T30 | T30 |
| 36 | T36 Release pack | P0 | blocked | T31-T35 |

## 10. 风险与顺序说明

- **R1**: 24 leaf 批量修改面大（~1200 行 diff）→ Tiered + sub-gate 拦截 + walking-skeleton 端到端验证
- **R2**: orchestrator 升级与 leaf 修改互相依赖（orchestrator pre-check 要兜住 leaf 删除的 `[Workflow]` Gate；leaf 删除前 orchestrator 必须先升级）→ T4 严格在 T5-T14 前
- **R3**: HYP-005 失败可能性（orchestrator 可能在某些 ambiguous artifact 状态下决策不出唯一 next-skill）→ 保留 v0.6.x 兼容 fallback（leaf 仍可写 `Next Action` 作为 hint，orchestrator 可读但不依赖）；T30 验证时如果 fallback 不够，触发 hf-hotfix 重设计 orchestrator 决策协议（不会让 release-blocking 失败 → 只可能让 release 推迟）
- **R4**: CHANGELOG [0.6.0] 段删除会让 git history 上 v0.6.0 PR descriptions 失去 CHANGELOG 索引 → 接受；PR descriptions 自身保留作为详细历史
- **R5**: cloud agent 上下文限制可能让 T30 walking-skeleton 端到端跑得不完整 → 接受 T30 部分基于 dogfood 完整链 simulated 等价 + features/001-orchestrator-extraction/ 已有 closeout 作为 baseline 参照

## 11. ReviewHandoff

- 派发 hf-tasks-review 独立 reviewer subagent (T3)
- reviewer 重点关注:
  - Tier 1/2 拆分是否合理（10+14 = 24 是否覆盖全部 hf-* leaf）
  - 通用 acceptance 是否覆盖 Step 2-5 全部 4 维（grep 验证 + Hard Gate 标签 + Next Action 限定 + 跨 hf-* 引用清理）
  - HYP-005 验证策略是否充分（不依赖 Next Action 时 orchestrator 还能正确路由）
  - CHANGELOG [0.6.0] 删除是否合规（per ADR-008 D6）

---

## 状态同步

- 状态：草稿
- Current Stage: hf-tasks
- Next Action Or Recommended Skill: hf-tasks-review

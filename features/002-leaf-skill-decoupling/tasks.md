# Tasks — 002-leaf-skill-decoupling (v0.7.0)

- 状态: 草稿
- 主题: 实施 ADR-007 D3 Step 2-5 + v0.7.0 一次性发布完整版
- 上游: ADR-007（架构）+ ADR-008（release scope）
- 继承: features/001-orchestrator-extraction/spec.md (FR-001..007 + NFR-001..005) + design.md (D-X 决策)；不重新 spec/design

## 1. 概述

**23 个**活跃 hf-* leaf skill **耦合解除**——12 doer + 11 reviewer/gate = 23（per ADR-007 D1）。`skills/using-hf-workflow/` 与 `skills/hf-workflow-router/` 是 v0.6.0 deprecated alias 不计入 leaf；本 feature 只对它们的 description 做版本号 sync（不再是 plugin loading 描述漂移）。

把每个 leaf 的 4 个耦合点（Step 2: `Next Action` 字段；Step 3: Hard Gates 标签；Step 4: `[Workflow]` Gate 物理上提；Step 5: 跨 hf-* 硬引用）一次性清理。leaf 核心方法论内容**不动**（TDD Two Hats / SUT Form / Fagan rubric / DDD strategic+tactical / EARS+BDD+MoSCoW / NFR QAS 等全部保留）。

orchestrator persona 升级到**纯 artifact 驱动**——不再依赖 leaf 的 `Next Action` hint。orchestrator 主文件 + references 同步更新。

按 Tier 顺序实施：Tier 1（**10** leaf：4 doer + 6 reviewer）→ sub-gate → Tier 2（**13** leaf：8 doer + 2 reviewer + 3 gate）→ orchestrator 升级 → walking-skeleton 端到端验证 → release pack。

## 2. 里程碑

| 里程碑 | 包含任务 | 退出标准 |
|---|---|---|
| **M0: 骨架** | T1（ADR-008）+ T2（feature scaffolding）+ T3（tasks-review approval）| ADR-008 起草 + feature 目录就位 + tasks-review 通过 |
| **M1: Orchestrator 升级** | T4（orchestrator 主文件 + references 升级到纯 artifact 驱动；保留 v0.6.0 兼容期 fallback 消费 leaf `Next Action` 作为辅助 hint）| `agents/hf-orchestrator.md` + `agents/references/profile-node-and-transition-map.md` + `reviewer-return-contract.md` 描述明确"以 artifact 为权威；leaf `Next Action` 作为 v0.6.x 兼容 hint" |
| **M2: Tier 1 leaf 解耦** | T5-T14（4 doer + 6 reviewer × Step 2/3/4/5）| 每个 leaf 4 步全做；grep 验证 0 跨 hf-* 硬引用 + Hard Gates 标签齐全 + `Next Action` 字段标 optional |
| **M3: Tier 1 sub-gate** | T15（Tier 1 grep 验证 + walking-skeleton 局部 smoke）| 10 leaf 全部 GREEN；orchestrator 在不依赖 Next Action 的情况下能正确派发到 Tier 1 leaf |
| **M4: Tier 2 leaf 解耦** | T16-T29（8 doer + 6 reviewer/gate × Step 2/3/4/5）| 同 M2 但范围 13 leaf |
| **M5: HYP-005 release-blocking 验证** | T30（walking-skeleton 端到端 v0.7.0 跑一遍；对照 v0.5.1 baseline 运行时等价；HYP-002 升级版 + HYP-005 双验证）| `regression-diff.py` PASS + orchestrator 纯 artifact 驱动决策记录入档 |
| **M6: Docs sync + version bump** | T31-T35（README × 2 / setup docs × 3 / CHANGELOG 整合 [0.7.0] 删 [0.6.0] / SECURITY / CONTRIBUTING / plugin manifest version）| 全部文档反映 v0.7.0 完整交付 narrative |
| **M7: Release pack** | T36（hf-release dogfood #5 → release-pack.md + release-regression.md + release-traceability.md + pre-release-checklist.md → ready-for-tag）| v0.7.0 release pack 全 GREEN，maintainer 可执行 git tag |

## 3. 文件 / 工件影响图

### 修改

- `agents/hf-orchestrator.md`（M1）
- `agents/references/profile-node-and-transition-map.md` + `reviewer-return-contract.md` + `routing-evidence-guide.md`（M1）
- **23 leaf SKILL.md**（M2 + M4；Step 2/3/4/5 全套）
  - Tier 1 (10 leaf): `skills/hf-{specify,design,tasks,test-driven-dev}/SKILL.md` (4 doer) + `skills/hf-{spec,design,tasks,test,code,traceability}-review/SKILL.md` (6 reviewer)
  - Tier 2 (13 leaf): `skills/hf-{product-discovery,experiment,hotfix,increment,finalize,ui-design,browser-testing,release}/SKILL.md` (8 doer) + `skills/hf-{ui,discovery}-review/SKILL.md` (2 reviewer) + `skills/hf-{regression,completion,doc-freshness}-gate/SKILL.md` (3 gate)
- 部分 leaf 的 `references/*.md`（按需；如 reviewer-return-contract 等）
- `skills/using-hf-workflow/SKILL.md` 描述同步（v0.6.0 plugin-install 加载通道描述更新到 v0.7.0；不动其加载通道作用）
- `skills/hf-workflow-router/SKILL.md` 描述微调（保持 deprecated alias 状态；版本号 sync）
- `README.md` / `README.zh-CN.md` Scope Note（M6）
- `docs/{cursor,claude-code,opencode}-setup.md`（M6）
- `CHANGELOG.md`（整合 [0.7.0]，删 [0.6.0]；M6）
- `SECURITY.md` / `CONTRIBUTING.md` / `.claude-plugin/plugin.json` / `.claude-plugin/marketplace.json` / `.cursor/rules/harness-flow.mdc`（version bump；M6）
- `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` D1 Amendment 段版本 sync（T35）

### 新增

- `docs/decisions/ADR-008-...md`（M0）
- `features/002-leaf-skill-decoupling/{README,progress,tasks}.md` + reviews/ + approvals/ + verification/ 目录（M0）
- `features/release-v0.7.0/{release-pack.md, verification/release-regression.md, verification/release-traceability.md, verification/pre-release-checklist.md}`（M7）

### 显式不动

- 23 leaf SKILL.md 的核心方法论内容（TDD Two Hats / SUT Form / Fagan rubric / DDD / EARS / 等等）
- closeout pack schema / reviewer return verdict 词表 / hf-release 行为 / audit-skill-anatomy.py / hf-finalize step 6A
- `using-hf-workflow` / `hf-workflow-router` deprecated alias（D3 Step 6 仍 deferred）
- features/001-orchestrator-extraction/ 历史工件（v0.6.0 中间产物，不修改历史）

## 4. 需求与设计追溯

| 来源 | 本 feature 任务 |
|---|---|
| ADR-007 D3 Step 2 | 23 leaf × `Next Action` 字段降级 (T5-T29 各含一项) |
| ADR-007 D3 Step 3 | 23 leaf × Hard Gates 标签 `[SOP]` / `[Workflow]` (T5-T29 各含一项) |
| ADR-007 D3 Step 4 | 23 leaf × `[Workflow]` 类 Gate 物理上提 (T5-T29 各含一项；orchestrator side 由 T4 配套支持) |
| ADR-007 D3 Step 5 | 23 leaf × 跨 hf-* 硬引用清理 (T5-T29 各含一项) |
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

### M4: Tier 2 leaf 解耦（13 leaf × Step 2-5；不计 T29 sub-gate）

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

每 task acceptance 同 Tier 1（T5-T14）通用 acceptance。

#### T29. Tier 2 sub-gate（与 T15 同形）

- **类型**: collation gate（不产新 leaf；只 grep 验证 + 1 个 verification record）
- **目标**: 验证 13 Tier 2 leaf + 全 23 leaf 整体 GREEN
- **Acceptance**:
  - **(T29.a)** `grep -l "Next Action Or Recommended Skill: hf-" skills/hf-{product-discovery,experiment,hotfix,increment,finalize,ui-design,browser-testing,release}/SKILL.md skills/hf-{discovery,ui}-review/SKILL.md skills/hf-{regression,completion,doc-freshness}-gate/SKILL.md` 返回空（或全部带 v0.7.0+ 限定语 / "optional" / "hint" 标识）
  - **(T29.b)** 13 Tier 2 leaf 的 Hard Gates 段每条均含 `[SOP]` / `[Workflow]` 标签（`grep -c "\[SOP\]\|\[Workflow\]" skills/hf-*/SKILL.md` 每文件 ≥ 4）
  - **(T29.c)** `[Workflow]` 类 Gate 已物理删除（grep 仅在 orchestrator pre-check 文档段出现，不在 leaf Hard Gates 段内出现）
  - **(T29.d)** 跨 hf-* 硬引用 grep = 0（除 `## See Also` 软提及）
  - **(T29.e)** 全 23 leaf 综合统计：Tier 1 (10) + Tier 2 (13) 全部满足 .a-.d 条件
- **依赖**: T16-T28 全部 GREEN
- **Files / 触碰工件**: 创建 `verification/tier2-sub-gate-2026-05-10.md`
- **测试设计种子**:
  - 主要行为: 23 leaf 全部满足 4 步标签
  - fail-first: 进入 T29 前任一 Tier 2 leaf 不满足 .a-.d → 应拦在 T16-T28 自身 acceptance；T29 是综合复核
  - SUT Form: `naive`（grep / wc / 文档检查）
- **Verify**: `bash` grep 命令清单 + 每 leaf 的 grep count 表
- **预期证据**: verification record 文件 + 23 leaf grep 输出对照表
- **完成条件**: 5 条 acceptance 通过

### M5: HYP-002 + HYP-005 release-blocking 验证

#### T30. Walking-skeleton 端到端 v0.7.0 + orchestrator 纯 artifact 驱动验证

- **目标**:
  - 跑一遍完整 v0.7.0 walking-skeleton（最薄端到端：spec → design → tasks → impl → reviews → finalize）
  - 对照 `examples/writeonce/features/001-walking-skeleton/` v0.5.1 baseline 跑同一条端到端轨迹（升级 HYP-002 验证：从 self-diff 静态等价升级到运行时等价）
  - HYP-005 验证用 **4 重证据并联**（不仅"至少一次"），每重证据独立留档
- **Acceptance**:
  - **(T30.a 全路径覆盖) 跑 v0.7.0 walking-skeleton 至少 5 个不同 stage 转移**（spec→spec-review / spec-review→design / design→design-review / tasks→test-driven-dev / test-driven-dev→test-review）；**每个**转移点 orchestrator 必须只读 progress.md + 上游 review record 决定下一步，**不**消费 leaf 的 `Next Action` 字段。所有 5 个决策点的 evidence（artifact-driven decision log）写入 `verification/orchestrator-pure-artifact-driven-2026-05-10.md`
  - **(T30.b counterfactual diff) 反向验证** ：构造一个**人工**修改的 leaf 输出（leaf 写 `Next Action: hf-WRONG-SKILL`，其余 progress.md / reviews 一致），重跑同一决策点；orchestrator 必须给出**与基线相同**的决策（即忽略 leaf 错误 hint，按 artifact 推进），不能被 hint 误导
  - **(T30.c grep 全检) 跑全部 23 leaf 的 SKILL.md grep 验证**：`grep -E "Next Action Or Recommended Skill: hf-[a-z-]+" skills/hf-*/SKILL.md | grep -v "optional\|hint\|v0.6.x"` 应返回 0 行（即所有出现都带可选限定语）
  - **(T30.d 仪表化 ignore-mode 反例) 在 walking-skeleton 中**：让某 leaf 输出包含 `Next Action: hf-X`（X 是合法但非 canonical 选择），orchestrator 应记录"已读 hint 但忽略，按 artifact 选 hf-Y"；该日志条目落 `orchestrator-pure-artifact-driven-*.md`
  - **(T30.e regression baseline) `regression-diff.py` PASS** over walking-skeleton baseline (v0.5.1) vs candidate (v0.7.0) 产出物（容许差异白名单不变）；HYP-002 升级版（从静态 self-diff 升级到运行时等价）VALIDATED
- **依赖**: T29 GREEN
- **Files / 触碰工件**:
  - 创建 `verification/walking-skeleton-runtime-2026-05-10.md`（HYP-002 升级证据）
  - 创建 `verification/orchestrator-pure-artifact-driven-2026-05-10.md`（HYP-005 4 重证据：5 决策点全路径 + counterfactual + grep 全检 + ignore-mode 反例）
- **测试设计种子**:
  - 主要行为: 5 决策点 artifact-driven + counterfactual 不被误导 + grep 全检 0 + ignore-mode 反例
  - 关键边界: cloud agent 上下文限制可能让"完整 5 决策点端到端"不可行；fallback：在已有 features/001 / features/002 实施轨迹中追溯 5 决策点（这些已经发生过的 orchestrator 决策实质就是 artifact-driven，因为我们在 v0.6.0/v0.7.0 阶段从未让 leaf 写 Next Action 影响过编排者实际选择——可作为已经发生的运行时 evidence）
  - SUT Form: `naive`
- **Verify**: 4 重证据各自独立 PASS；缺一重不算 HYP-005 release-blocking VALIDATED
- **预期证据**: 2 个 verification record 文件齐全
- **完成条件**: 5 条 acceptance .a-.e 全部通过；HYP-002 + HYP-005 双 VALIDATED

### M6: Docs sync + version bump

#### T31. README 中英 Scope Note 重写

- **目标**: README.md / README.zh-CN.md Scope Note 段重写为 v0.7.0
- **Acceptance**:
  - **(T31.a)** 两份 README 顶部 Scope Note 段标题含 "v0.7.0"
  - **(T31.b)** Scope Note 段含 "v0.6.0 was prepared but not tagged—superseded by v0.7.0" 或等价中文叙述
  - **(T31.c)** Scope Note 段含 "standalone-usable skills now actually delivered in v0.7.0" 或等价 claim（区别于 v0.6.0 仅 architectural foundation 的措辞）
  - **(T31.d)** 两份 README 中英对照一致（同一 release 同一立场；不漂移）
- **Verify**: `grep -c "v0.7.0\|standalone" README.md README.zh-CN.md` 每文件 ≥ 3
- **依赖**: T30 GREEN

#### T32. Setup docs ×3 同步

- **目标**: docs/{cursor,claude-code,opencode}-setup.md 全部同步到 v0.7.0
- **Acceptance**:
  - **(T32.a)** 3 doc 顶部段标题含 "v0.7.0"（grep "v0.7.0"）
  - **(T32.b)** 3 doc 引用 `agents/hf-orchestrator.md`（grep）
  - **(T32.c)** 3 doc "如何启用 HF" 段更新到 v0.7.0 narrative（含 standalone-usable + 完整 Step 1-5 已交付的描述）
  - **(T32.d)** 3 doc 不再写 v0.6.0 作为"current version"（grep `v0.6.0` 在 release-current 描述中应为 0；历史 lineage 段允许）
- **Verify**: 每 doc grep 命中数 ≥ 2
- **依赖**: T30 GREEN

#### T33. CHANGELOG 整合 [0.7.0] 段，删 [0.6.0] 段（量化迁移验证）

- **目标**:
  - CHANGELOG.md 删除 `## [0.6.0] - 2026-05-09` 整段（按 ADR-008 D6）
  - 新增 `## [0.7.0] - 2026-05-10 — pre-release` 段，结构：
    - **顶部说明段**：含 "v0.6.0 prepared but not tagged—consolidated into v0.7.0; v0.7.0 is the first HF release that delivers genuinely standalone-usable skills"
    - **Foundation work (originally drafted as v0.6.0)** 子段：迁移原 [0.6.0] 段全部子段（**Added 7 项 / Changed 10 项 / Decided 8 项 / Notes 5 项**）的实质内容；可重组叙述但**不丢条目**
    - **Standalone Skills (Step 2-5 实施)** 子段：v0.7.0 新增的 leaf 解耦工作；23 leaf 修改 + orchestrator 升级 + HYP-005 release-blocking 验证
    - **Decided** 子段：含 ADR-008 D1-D7 + ADR-007 D5 升级（HYP-005 加入 release-blocking）
    - **Notes** 子段：含 ADR-007 D1 Amendment 在 v0.7.0 范围内仍然适用 + v0.8+ Step 6 物理删除路线图
- **Acceptance**:
  - **(T33.a)** CHANGELOG.md 含 `[0.7.0]` 段 + 不含 `[0.6.0]` 段（grep）
  - **(T33.b 量化迁移)** 原 [0.6.0] 段实质条目数清点：Added 7 / Changed 10 / Decided 8 / Notes 5 = 30 条；新 [0.7.0] § "Foundation work" 子段必须包含**所有 30 条**实质内容（可重组叙述但不丢条目；reviewer 抽样 5 条核验）
  - **(T33.c)** [0.7.0] § "Standalone Skills" 子段 ≥ 5 条 Added / Changed 实质条目（覆盖 23 leaf 解耦 + orchestrator 升级 + verification/）
  - **(T33.d)** [0.7.0] § Decided 子段含 ADR-008 全 7 决策（D1-D7）+ ADR-007 D5 升级到 HYP-005 release-blocking
  - **(T33.e)** [0.7.0] § Notes 子段含 v0.8+ Step 6 deletion 路线图说明
- **Verify**: `grep -c "^- " CHANGELOG.md`（针对 [0.7.0] 段范围内）≥ 35（30 foundation + 5 standalone + ADR-008 + Notes）
- **依赖**: T30 GREEN

#### T34. 项目元数据 version bump

- **目标**: 5 个 metadata 文件版本号 0.6.0 → 0.7.0
- **Acceptance**:
  - **(T34.a)** SECURITY.md Supported Versions 表新增 0.7.x 行 latest 0.7.0；0.6.x 列入 previous（grep "0.7.0" ≥ 1 + grep "0.7.x" ≥ 1）
  - **(T34.b)** CONTRIBUTING.md 引言版本号改为 v0.7.0（grep "v0.7.0" ≥ 1）
  - **(T34.c)** .claude-plugin/plugin.json `version` 字段 = `"0.7.0"`；`python3 -m json.tool` valid
  - **(T34.d)** .claude-plugin/marketplace.json description 段更新到 v0.7.0
  - **(T34.e)** .cursor/rules/harness-flow.mdc Hard rules / Scope honesty 段版本号 0.6.0 → 0.7.0
  - **(T34.f 全集量化)** 上述 5 文件**每文件**至少 1 处 v0.7.0 hit（grep -c per file ≥ 1）；不再有把 0.6.0 当作 current 的 description（grep "current.*0.6.0\|latest.*0.6.0" 在这 5 文件应为 0；历史 lineage 段可保留）
- **Verify**: 每文件 grep "0.7.0" ≥ 1 ；`python3 -m json.tool` × 2 PASS
- **依赖**: T30 GREEN

#### T35. ADR-007 D1 Amendment 版本号 sync + Amendment 适用性确认

- **目标**: ADR-007 D1 Amendment 段中的版本标识 sync 到 v0.7.0
- **Acceptance**:
  - **(T35.a)** ADR-007 D1 Amendment 段中"v0.6.0 pre-tag, 2026-05-10"等当前版本标识更新为"v0.7.0 release, 2026-05-10"或保留双版本标识"v0.6.0 prepared / v0.7.0 released"
  - **(T35.b)** Amendment 段保留 v0.6.0 历史时间线（PR #45 #46 #47）作为实施过程记录，不删
  - **(T35.c)** Amendment 段在 v0.7.0 范围内仍然 architecturally 适用（plugin-install 加载通道分工不变）的声明明确入档
- **Verify**: `grep -A5 "Amendment" docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md | grep -c "v0.7.0"` ≥ 1
- **依赖**: T30 GREEN

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

关键路径长度：**显式枚举 14 步**（feature-level）+ **1 步** release-tier：

```
[Feature-level (002-leaf-skill-decoupling) chain]
T1 (ADR-008) →
T2 (Feature scaffolding) →
T3 (hf-tasks-review) →
T4 (Orchestrator 升级) →
T5+T6+T7+T8+T9+T10+T11+T12+T13+T14 (Tier 1 leaf 并行；折算 1 步) →
T15 (Tier 1 sub-gate) →
T16+T17+T18+T19+T20+T21+T22+T23+T24+T25+T26+T27+T28 (Tier 2 leaf 并行；折算 1 步) →
T29 (Tier 2 sub-gate) →
T30 (HYP-002+005 验证) →
T31+T32+T33+T34+T35 (Docs 同步并行；折算 1 步) →
hf-test-review (final dispatch on T5-T29 + T4 changes)→
hf-code-review (final dispatch on T4 + T30 scripts)→
hf-traceability-review (final dispatch全链)→
hf-regression-gate (with T30 evidence)→
hf-completion-gate (workflow-closeout 准入)→
hf-finalize (closeout.md + closeout.html)

[Release-tier (release-v0.7.0) — feature closeout 完成后再做]
↓
T36 (hf-release dogfood #5；release pack ready-for-tag)
```

并行可压缩到 **14 大步 feature-level**（含 review/gate + finalize 6 步）+ **1 步 release-tier**（T36 在 hf-finalize 完成后才启动；hf-release 是 standalone skill 不进 orchestrator transition map per ADR-004 D3）。

修订后任务总数：T1-T29 + T30 + T31-T35 + T36 + 6 review/gate = 36 implementation tasks + 6 chain dispatches = 42 总动作。

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

总验证策略：M3 sub-gate（Tier 1；T15）+ M4 sub-gate（Tier 2；T29）+ M5 walking-skeleton 端到端（T30；HYP-002+HYP-005 双验证 4 重证据并联）。

**Cross-reference 与 task 条目的对应**：
- T15 acceptance 直接消费上面"每 leaf 完成的判据"对 Tier 1 10 leaf 做 sub-gate 综合 grep
- T29 acceptance 同理对 Tier 2 13 leaf
- T30 acceptance .a-.e 各自独立 PASS 才算 HYP-005 release-blocking VALIDATED；缺一重不算
- T15 / T29 / T30 verification record 文件路径已在各 task Files 段显式列出

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

- **R1**: 23 leaf 批量修改面大（~1200 行 diff）→ Tiered + sub-gate 拦截 + walking-skeleton 端到端验证
- **R2**: orchestrator 升级与 leaf 修改互相依赖（orchestrator pre-check 要兜住 leaf 删除的 `[Workflow]` Gate；leaf 删除前 orchestrator 必须先升级）→ T4 严格在 T5-T14 前
- **R3**: HYP-005 失败可能性（orchestrator 可能在某些 ambiguous artifact 状态下决策不出唯一 next-skill）→ 保留 v0.6.x 兼容 fallback（leaf 仍可写 `Next Action` 作为 hint，orchestrator 可读但不依赖）；T30 验证若 4 重证据不全 PASS → **HYP-005 release-blocking 失败 → v0.7.0 不打 tag**；触发 hf-hotfix 链重设计 orchestrator 决策协议直到全 4 重证据 PASS 后再发布。R3 不允许"接受降级 release"路径——ADR-008 D5 已锁定 release-blocking 立场
- **R4**: CHANGELOG [0.6.0] 段删除会让 git history 上 v0.6.0 PR descriptions 失去 CHANGELOG 索引 → 接受；PR descriptions 自身保留作为详细历史
- **R5**: cloud agent 上下文限制可能让 T30 walking-skeleton 端到端跑得不完整 → 接受 T30 部分基于 dogfood 完整链 simulated 等价 + features/001-orchestrator-extraction/ 已有 closeout 作为 baseline 参照

## 11. ReviewHandoff

- 派发 hf-tasks-review 独立 reviewer subagent (T3)
- reviewer 重点关注:
  - Tier 1/2 拆分是否合理（10+13 = 23 是否覆盖全部活跃 hf-* leaf）
  - 通用 acceptance 是否覆盖 Step 2-5 全部 4 维（grep 验证 + Hard Gate 标签 + Next Action 限定 + 跨 hf-* 引用清理）
  - HYP-005 验证策略是否充分（不依赖 Next Action 时 orchestrator 还能正确路由）
  - CHANGELOG [0.6.0] 删除是否合规（per ADR-008 D6）

---

## 状态同步

- 状态：草稿
- Current Stage: hf-tasks
- Next Action Or Recommended Skill: hf-tasks-review

# Tasks Review — 002-leaf-skill-decoupling (v0.7.0)

- 评审者: 独立 reviewer subagent (`hf-tasks-review`)
- 评审日期: 2026-05-10
- 被评审工件:
  - `features/002-leaf-skill-decoupling/tasks.md`（草稿）
  - `docs/decisions/ADR-008-v0.7.0-skip-v0.6.0-tag-and-deliver-step-2-5-as-single-release.md`（起草中，与 tasks.md 同 PR）
- 上游证据:
  - `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（accepted, v0.6.0）
  - `features/001-orchestrator-extraction/spec.md` + `design.md`（已 approval；tasks.md 经 ADR-008 D3 显式继承）
  - `features/002-leaf-skill-decoupling/{README,progress}.md`
  - `CHANGELOG.md`（[0.6.0] 段 line 9-62，[Unreleased] line 7）
- Author / Reviewer 分离: 本 reviewer 未参与 tasks.md / ADR-008 起草；接管来自父 orchestrator session 的派发，以独立 reviewer subagent 身份评审

---

## 0. Precheck

| 项 | 状态 | 备注 |
|---|---|---|
| 任务计划稳定可定位 | PASS | `features/002-leaf-skill-decoupling/tasks.md` 落盘 |
| 上游 spec / design approval evidence | PASS（继承式）| ADR-008 D3 显式声明继承 features/001 spec/design + ADR-007；features/001 已 workflow-closeout |
| route / stage / profile 一致 | PASS | progress.md Current Stage = `hf-tasks`；Profile = full；Pending Reviews 含 `hf-tasks-review`，与本次 dispatch 一致 |
| 上游证据回读路径稳定 | PASS | ADR-007 / ADR-008 / features/001 工件全部可读 |

**Precheck 结论**：通过；进入正式审查。

**特别裁定 — `hf-increment`-style 入口（无独立 spec/design）合法性**：

ADR-008 D3 给出"不重做 spec/design"的理由：(1) 架构决策已在 ADR-007 D1+D3 锁定；(2) v0.7.0 是 D3 Step 2-5 的执行级落地，不是新架构决策；(3) features/001 spec FR-001..007 + NFR-001..005 + ADR-007 D1 phasing（v0.7.0+ runtime enforcement）可被本 feature 完整继承。本 reviewer 接受该裁定，但有一个**保留**：HYP-005 在 features/001 spec § 4 中列为 `Blocking? = 否（本轮）；后续 increment 拆解时升级为阻塞`，本 feature **正是该后续 increment**，HYP-005 升级为 release-blocking 后，应当落在 verification 任务的 acceptance 设计上严格化（见下文 TR3 finding F-3）。继承式入口本身不是"corner-cutting smell"，但它把 HYP-005 验证策略的设计责任挪到 tasks.md / T30 acceptance — 而 T30 当前 acceptance 强度不够（详见 § 2 / § 3）。

---

## 1. 多维评分

| 维度 | 分 | 阈值 | 主要依据 |
|---|---|---|---|
| **TR1 可执行性** | 7 / 10 | ≥ 6 PASS | T5-T28 通用 acceptance 具体（grep + 标签 + 字段限定语），冷启动可执行；T29 仅"reserved"，可执行性弱；T31-T35 acceptance 短，但属 docs sync 类，可接受 |
| **TR2 任务合同完整性** | 6 / 10 | ≥ 6 PASS（边缘）| T5-T28 通用 acceptance 4 条（Step 2/3/4/5）+ § 7 验证 bash 种子可冷读；T29 缺 Acceptance / Files / Verify；T30 acceptance 可冷读但"至少一次决策"判据过弱（详见 TR3）；T33 acceptance 不足以确保 [0.6.0] → [0.7.0] 内容完整迁移 |
| **TR3 验证与测试设计种子** | 5 / 10 | ≥ 6 **FAIL** | T30 HYP-005 release-blocking 验证策略对"orchestrator 不依赖 Next Action"只要求"至少一次决策无 Next Action 字段，证据入档" — 这是 Bayesian-weak 的存在性证明，不足以支撑 release-blocking 判据；缺 fail-first 反例（如：orchestrator 在 Next Action 缺失时本应能决策但决策失败的反例）；缺"orchestrator ignore Next Action mode" 仪表化策略；leaves 在 v0.7.0+ 仍允许 optional Next Action 字段，walking-skeleton 中 leaf 仍可能输出该字段，所以"至少一次"无法保证全路径覆盖 |
| **TR4 依赖与顺序正确性** | 7 / 10 | ≥ 6 PASS | DAG 形态合理；T1→...→T36 无环；Tier 1 sub-gate (T15) 严格 gate Tier 2；T4 严格在 T5-T14 前（兼容期 fallback 到位）。但："关键路径长度 12 步"声明含糊，显式列举 11 节点 + "+ 中间 review/gate 步骤"，无法 1-1 对照；T33 整合 CHANGELOG 与 T35 ADR-007 Amendment 版本同步是否在 T36 hf-release pre-flight 之前到位需要更明确 |
| **TR5 追溯覆盖** | 6 / 10 | ≥ 6 PASS（边缘）| ADR-007 D3 Step 2/3/4/5 → T5-T29 各 acceptance 条目可对照；HYP-002 / HYP-005 → T30；ADR-008 D6 → T33；D7 → T31+T32+T35。但：(1) "24 leaf" 数字不准（实际 leaf = 23；详见 F-1）；(2) ADR-008 影响范围列出的 `skills/using-hf-workflow/SKILL.md` 描述同步未在 tasks.md § 3 修改清单中体现 |
| **TR6 Router 重选就绪度** | 8 / 10 | ≥ 6 PASS | § 8 Selection Priority + Ready When 规则唯一（P0 release-blocking / 硬前置；P1 范围内必需；P2 无）；§ 9 任务队列投影完整、可回读；progress.md Current Active Task = "无（tasks 阶段）" 与 § 8 起步顺序一致 |

**关键维度门**：TR3 = 5 / 10 < 6 → **不得通过**。

---

## 2. Anti-Pattern 与挑战式审查

| ID | 检测信号 | 命中 | 严重度 |
|---|---|---|---|
| TA1 大任务 | T5-T28 单 leaf × 4 acceptance 子条；粒度合理；T30 含 walking-skeleton + HYP-002 + HYP-005 三事，略大但 HF 惯例可接受 | 否 | - |
| TA2 缺 Acceptance | **T29 只有 "(reserved；与 T15 同形)"，无显式 Acceptance / Files / Verify** | 是 | important |
| TA3 缺 Files / Verify | T31-T35 部分 acceptance 仅 1-2 行；T34 grep 计数判据合理；T31/T32/T35 略空 | 部分 | minor |
| TA4 无 test seed | T30 HYP-005 acceptance 缺"orchestrator 在 Next Action 缺失时仍能决策"的具体仪表化设计；§ 7 提供 bash grep 种子但只覆盖 leaf 修改，不覆盖 T30 | **是（针对 T30 / HYP-005）** | **critical** |
| TA5 里程碑冒充任务 | M0-M7 与 T1-T36 分层清晰；§ 9 队列投影正确区分 | 否 | - |
| TA6 orphan task | 全部任务可回指 ADR-007 D3 Step / ADR-008 D 段（§ 4 追溯表完整）；但 § 3 "修改"清单遗漏 ADR-008 影响范围中的 `skills/using-hf-workflow/SKILL.md` 描述同步 | 部分 | minor |
| TA7 unstable active task | § 8 Selection Priority 唯一；起步顺序明确 | 否 | - |

---

## 3. 结构化 Findings

每条 finding：`[severity][classification][rule_id]` 摘要 + 建议修订。

### F-1 [critical][LLM-FIXABLE][TR5/TA6] "24 hf-* leaf skill" 数字与实际不符；Tier 2 "14 leaf" 把 sub-gate 算作 leaf

**证据**:
- 实际 hf-* leaf = 23（ADR-007 D1 表：12 doer + 11 reviewer/gate）；`skills/` 下 25 个目录中包含 `hf-workflow-router`（已 deprecated alias，非 leaf）+ `using-hf-workflow`（非 hf-* prefix，亦 deprecated alias）
- 验证：`ls skills/ | grep -E "^hf-"` 返回 24 行，含 `hf-workflow-router`；扣除 deprecated alias 后真实 leaf = 23
- tasks.md "概述" + § 4 追溯表 + § 5 M2/M4 标题均使用 "24 leaf"
- tasks.md § 5 M4 标题 "Tier 2 leaf 解耦（14 leaf × Step 2-5）" 与 § 6 / § 9 "T29 Tier 2 sub-gate" 矛盾 — T29 在 § 6 / § 9 是 sub-gate（与 T15 同形），不是 leaf
- ADR-008 D4 Tier 2 表头 "Reviewer/Gate (6)" 但只列 5 个条目（discovery-review / ui-review / regression-gate / completion-gate / doc-freshness-gate）

**实际任务覆盖**:
- Tier 1 = 4 doer (T5-T8) + 6 reviewer (T9-T14) = 10 leaf ✓
- Tier 2 = 8 doer (T16-T23) + 5 reviewer/gate (T24-T28) = 13 leaf ✓ + T29 sub-gate（非 leaf）
- 合计 = 23 leaf 已全覆盖；ADR-007 D1 表 12 + 11 = 23 leaf 一致

**风险**: 实施时 reviewer / 审计者按 "24 leaf" 计数核对，会找不到第 24 个 leaf；可能误以为漏了某个 hf-* 目录；或误把 `hf-workflow-router` deprecated alias 当作待解耦 leaf（违反 § 3 显式不动列表）

**修订建议**:
- tasks.md / ADR-008 全文把 "24 leaf" 改为 "23 leaf"（ADR-007 D1 表权威）
- M4 标题改为 "Tier 2 leaf 解耦（13 leaf + 1 sub-gate × Step 2-5）"
- ADR-008 D4 Tier 2 表头改为 "Reviewer/Gate (5)" 或补齐第 6 个条目（若实际还有遗漏 leaf 需指出，但 reviewer 已穷举确认 = 5）
- § 5 M4 子节首句 "T16-T29：每个 leaf 一个 task" 改为 "T16-T28：每个 leaf 一个 task；T29：Tier 2 sub-gate"
- § 4 追溯表 "24 leaf × ..." 改为 "23 leaf × ..."

**用户 Don'ts 检查**: 用户硬规则 #1 "Tier 1+2 doesn't cover all 24 leaf" — 严格判据下，ALL 实际 leaves（23 个）已覆盖；但 "24" 这个声明的数字与实际不符，标记 / 计数 / 文档一致性受损。这是数字不准而非覆盖不全。

---

### F-2 [critical][LLM-FIXABLE][TR3/TA4] T30 HYP-005 release-blocking 验证策略不足以支撑 v0.7.0 release-blocking 判据

**证据**:
- T30 acceptance 第 2 条："orchestrator 在过程中至少一次决策'无 Next Action 字段，仍按 artifact 推进' — 证据写入 `verification/orchestrator-pure-artifact-driven-2026-05-10.md`"
- HYP-005 在 ADR-008 D5 升级为 release-blocking；features/001 spec § 4 原标 `非 blocking（本轮）；后续 increment 拆解时升级为阻塞` — 本 feature 即该 increment
- T4 acceptance: 显式保留 v0.6.x 兼容期 fallback — orchestrator 仍可读 leaf 的 Next Action 字段作为辅助 hint
- T5-T28 通用 acceptance 第 .1 条把 Next Action 字段标 "optional / 可选" — leaf 仍可能写出该字段
- 风险 R3 自承认："orchestrator 可能在某些 ambiguous artifact 状态下决策不出唯一 next-skill"

**为什么 "至少一次" 不够**:
1. 存在性证明 ≠ 健壮性证明：单次决策成功无法保证全路径所有决策点都能不依赖 Next Action 字段
2. 兼容期 fallback 存在 → walking-skeleton 中 leaf 仍可能输出 Next Action → orchestrator 真实决策可能仍消费该字段，"至少一次"通过用 trace 注入或样本筛选即可满足，无法判别 orchestrator 是否真在不依赖时也能决策
3. release-blocking 假设的反例侦测要求"必失败"路径被覆盖：若 orchestrator 在 ambiguous 状态下退化（如同时给出 2 个候选 next-skill），需要可被该验证捕获

**修订建议**（任一即可，可叠加）:
- **(a) 仪表化策略**：T4 acceptance 增加 "orchestrator 暴露 `IGNORE_LEAF_NEXT_ACTION=1` 切换（或 markdown persona 指令段）"；T30 在该模式下重跑 walking-skeleton；通过 = 全路径推进无需 Next Action
- **(b) 全路径覆盖**：T30 acceptance 改为 "orchestrator 在 walking-skeleton 全部 N 个决策点均能在不引用 leaf Next Action 字段的情况下决策；决策日志 1-1 落盘"；明确 N（spec → finalize 的决策点数，通常 ≥ 8）
- **(c) Fail-first 反例**：T30 acceptance 增加 "在 features/001 closeout / artifact 中人工制造 ambiguous 状态（如 progress.md 缺关键字段），验证 orchestrator 触发 hard stop 并暂停，而不是错误推进；记录 ≥ 2 个反例"
- **(d) Counterfactual diff**：T30 跑两轮 walking-skeleton：一轮 leaf 有 Next Action（兼容模式），一轮 leaf 显式不写 Next Action（纯 artifact 模式）；产出对比应等价

**用户 Don'ts 检查**: 用户硬规则 #2 "HYP-005 verification strategy unclear" — **命中**。当前 T30 verification strategy 不足以支撑 release-blocking 权重，必须强化才能进入 implementation。

---

### F-3 [important][LLM-FIXABLE][TR2/TA2] T29 缺 Acceptance / Files / Verify

**证据**:
- tasks.md § 5 M4 表格 T29 行: `| T29 | （reserved）| （Tier 2 sub-gate；与 T15 同形）|`
- T29 后的说明仅一句："T29 是 Tier 2 sub-gate，验证 14 leaf + 全 24 leaf 整体 GREEN"
- 对照 T15（Tier 1 sub-gate）有 4 条具体 acceptance bullet + Files 字段（`verification/tier1-sub-gate-2026-05-10.md`）

**修订建议**:
- 把 T29 完整写出（即使内容是 "T15 模板复制 + Tier 2 leaf 列表替换"），含：
  - 目标
  - 4 条 acceptance（grep Next Action / grep [SOP][Workflow] 标签 / [Workflow] 物理删除验证 / 跨 hf-* 引用 = 0）
  - Files: `verification/tier2-sub-gate-2026-05-10.md`
- 或：在 T29 行下方明确写 "Acceptance / Files / Verify 与 T15 完全相同，仅 leaf 集合替换为 T16-T28 所列 13 个；详见 § 7 通用判据"

---

### F-4 [important][LLM-FIXABLE][TR2/TR5] T33 CHANGELOG 整合 acceptance 不足以保证 [0.6.0] 内容完整迁移

**证据**:
- 当前 `CHANGELOG.md` [0.6.0] 段（line 9-62）含 6 个子段：header narrative + Added (7 条) + Changed (10 条) + Decided (8 条) + Notes (5 条)
- T33 acceptance: "CHANGELOG.md 含 [0.7.0] 段且不含 [0.6.0] 段；diff vs main 显示完整 [0.7.0] 内容"
- ADR-008 D6 锁定 "[0.6.0] 段内容**整合**进新的 [0.7.0] 段，作为该 release 的 'Foundation work (originally drafted as v0.6.0; now consolidated)' 子段"

**问题**: "完整 [0.7.0] 内容" 含义模糊；当前 acceptance 不能侦测整合过程中条目丢失（例如 [0.6.0] Added 第 3 条 `CLAUDE.md` 落入 [0.7.0] 漏掉）

**用户 Don'ts 检查**: 用户硬规则 #3 "ADR-008 D6 CHANGELOG removal would lose audit trail without compensation" — **未命中硬否决**：D6 + T33 文字层面有补偿（明示需要整合为子段），但 acceptance 强度不足。补偿在意图层面已经存在，只是验证手段欠缺；不属于"无补偿"。

**修订建议**:
- T33 acceptance 增加："新 [0.7.0] 'Foundation work' 子段必须涵盖原 [0.6.0] 全部 Added (7) + Changed (10) + Decided (8) + Notes (5) 条目，逐条映射；可通过 `diff <(grep -A1000 '## \[0.6.0\]' CHANGELOG.md@main) <(grep -A1000 'Foundation work' CHANGELOG.md@HEAD)` 或一份 inline 对照表确认"
- 或：在 closeout 前由 hf-doc-freshness-gate 单独验一道（已在 progress.md Pending Reviews 中，但需要在 T33 acceptance 中显式 hand-off）

---

### F-5 [important][LLM-FIXABLE][TR4] 关键路径声明 "12 步" 含糊；显式节点 11 个 + "+ 中间 review/gate 步骤"

**证据**:
- tasks.md § 6 关键路径文字: "T1 → T2 → T3 → T4 → T5 → T15 → T16 → T29 → T30 → T31 → T36 + 中间 review/gate 步骤"
- 声明 "关键路径长度: **12 步**"
- 但显式列举仅 11 节点；progress.md Pending Reviews 含 6 个尾部 review/gate（test-review × 2 / code-review / traceability-review / regression-gate / completion-gate / finalize）未在 tasks.md § 5 / § 6 / § 9 中作为独立 task 出现

**HF 惯例考量**: 在 HF 中，review / gate 节点通常由 orchestrator 基于 artifact 状态派发，不必作为独立 task；但 progress.md 已明确列出 Pending Reviews And Gates，关键路径长度声明应与之一致

**修订建议**:
- § 6 把 "+ 中间 review/gate 步骤" 替换为显式枚举（如 "+ T5-T14 实施后的 hf-test-review (Tier 1)；T16-T28 实施后的 hf-test-review (Tier 2)；hf-code-review / hf-traceability-review / hf-regression-gate / hf-completion-gate / hf-finalize"），重新计算实际步数（≈ 17-18 步）
- 或：明确 "12 步" 仅指 doer + sub-gate 任务节点，review/gate dispatching 不计入；并增加一段说明 review chain 由 orchestrator 自行派发

**用户 Don'ts 检查**: 用户硬规则 #4 "critical path is incomplete" — 边缘命中。声明的 12 步与显式枚举的 11 步 + 中间步骤不能 1-1 对照；不算"完全错误"，但是 underspecified。建议归为 important LLM-FIXABLE 而非硬否决。

---

### F-6 [important][LLM-FIXABLE][TR5/TA6] § 3 修改清单遗漏 `skills/using-hf-workflow/SKILL.md`

**证据**:
- ADR-008 § 影响范围 "修订" 段含 "`skills/using-hf-workflow/SKILL.md`（plugin-install 加载通道；orchestrator 升级后描述同步）"
- tasks.md § 3 "修改" 段不含此项；§ 3 "显式不动" 段含 "using-hf-workflow / hf-workflow-router deprecated alias（D3 Step 6 仍 deferred）"
- ADR-007 D1 Amendment 在 v0.7.0 范围内**仍然适用**（plugin-install 加载通道分工不变；ADR-008 § 与既有 ADR 的关系 行也写明），但 SKILL.md body 中 "Read `agents/hf-orchestrator.md` and adopt that persona" 文字若涉及 v0.6.0 narrative 应同步至 v0.7.0

**修订建议**:
- tasks.md § 3 "修改" 段增加 "`skills/using-hf-workflow/SKILL.md`（M6 docs sync 范围；plugin-install loader description 中的 v0.6.0 narrative 同步至 v0.7.0；body 物理 redirect 行为不变；与 ADR-007 D1 Amendment 一致）"；或在 T31 / T32 中显式声明此文件
- 或：明示 "loader 文件 body 不动，仅 description 字段中如有 v0.6.0 narrative 同步"

---

### F-7 [minor][LLM-FIXABLE][TR2/TA3] T31 / T32 / T35 acceptance 略空

**证据**:
- T31 acceptance: "两份 README 均含 v0.7.0 段 + 显式 standalone-usable claim"
- T32 acceptance: "3 doc 全部 ref agents/hf-orchestrator.md + 标 v0.7.0"
- T35 acceptance: "ADR-007 内容仍准确，Amendment 段 ref v0.7.0 而不是 v0.6.0 作为 release 标识"

**风险**: 实施时无量化判据（如 "至少 N 处提及"、"原 v0.6.0 narrative 全部已替换"）；hf-doc-freshness-gate 兜底但前置 acceptance 强度不足

**修订建议**:
- T31 加："`grep -c 'v0.7.0' README.md README.zh-CN.md ≥ 3 (per file)`；`grep -c 'v0.6.0' README.md README.zh-CN.md` 在历史时间线段以外 = 0"
- T32 加："`grep -c '0.7.0' docs/{cursor,claude-code,opencode}-setup.md ≥ 1 per file`；`grep -c 'agents/hf-orchestrator.md' ≥ 1 per file`"
- T35 加："ADR-007 D1 Amendment 段中 v0.6.0 出现位置全部带历史时间线限定语（如 'pre-tag, 2026-05-10'），release 标识全部为 v0.7.0；by `grep -nE 'v0.[67]\.0' docs/decisions/ADR-007-...md` 人工核对一致性"

---

### F-8 [minor][LLM-FIXABLE][TR4] R3 风险描述措辞不准

**证据**:
- tasks.md § 10 R3: "HYP-005 失败可能性 ... 触发 hf-hotfix 重设计 orchestrator 决策协议（不会让 release-blocking 失败 → 只可能让 release 推迟）"

**问题**: release-blocking 假设的失败语义就是 "release 推迟"（直到验证通过为止）；R3 措辞 "不会让 release-blocking 失败" 与 "可能让 release 推迟" 矛盾；可能误导后续节点理解为 "HYP-005 验证失败可以 ship"

**修订建议**:
- 改为："HYP-005 验证失败 → 触发 hf-hotfix 重设计 orchestrator 决策协议；release tag 推迟到验证通过为止（这正是 release-blocking 假设的设计语义）"

---

### F-9 [minor][LLM-FIXABLE][TR2] T34 acceptance "grep '0.7.0' 命中 ≥ 5 处" 阈值依据不明

**证据**:
- T34 acceptance: "grep '0.7.0' 命中 ≥ 5 处；grep '0.6.0' 在 release-related metadata 中应只剩 CHANGELOG 历史段（已删的话 grep '0.6.0' should be 0）"

**问题**: T34 涉及 5 个文件（SECURITY / CONTRIBUTING / plugin.json / marketplace.json / .cursor/rules）；"≥ 5 处" 假设每文件 ≥ 1 处，但具体应当是 "每文件均含 0.7.0"；grep 全仓总命中 ≥ 5 不能保证每文件均覆盖

**修订建议**:
- 改为 "5 个目标文件每个 `grep -l '0.7.0'` 各命中 1 次（全集量化）"

---

### F-10 [minor][LLM-FIXABLE][TR3] § 7 验证策略与 T5-T28 任务条目无 cross-reference

**证据**:
- § 7 提供 bash 验证模板（grep 计数）
- T5-T28 通用 acceptance 末尾仅说 "通用 fail-first: grep ... 修改前 hit count > 0；修改后 hit count = 0 或全部带 v0.7.0+ 限定语"
- T5-T28 不显式回指 § 7

**修订建议**:
- T5-T28 通用 acceptance 末尾补一句 "完成判据 bash 模板见 § 7"

---

## 4. 缺失或薄弱项

- **HYP-005 验证策略仪表化设计**（F-2 同类）：缺 "orchestrator 在 leaf 仍写 Next Action 时如何判定决策不依赖该字段" 的设计种子；T30 acceptance 缺 fail-first 反例
- **T29 完整内容**（F-3）：reserved 占位需补齐；reviewer 应能冷读完成判据
- **CHANGELOG 内容映射表**（F-4）：缺 [0.6.0] → [0.7.0] 子段映射的显式工件
- **关键路径完整枚举**（F-5）：缺尾部 review chain 的显式列举
- **§ 3 影响清单**（F-6）：遗漏 `skills/using-hf-workflow/SKILL.md` description 同步

---

## 5. 用户 Don'ts 硬否决条件检查

| 用户硬规则 | 命中？ | 处置 |
|---|---|---|
| Tier 1+2 不覆盖全部 24 leaf | **否（功能层面）/ 是（计数层面）** | 实际 23 leaf 全部覆盖；"24" 数字不准 → F-1 important LLM-FIXABLE，不构成硬否决 |
| HYP-005 verification strategy unclear | **是** | F-2 critical LLM-FIXABLE → **触发 "需修改"** |
| ADR-008 D6 CHANGELOG removal 失去 audit trail without compensation | **否** | 补偿在意图层面存在（D6 + T33 整合子段）；F-4 important 强化建议但非硬否决 |
| critical path is incomplete | **边缘** | F-5 important LLM-FIXABLE；不足以构成硬否决但需修订 |

**结论**：用户硬规则触发 1 条（HYP-005 verification strategy）→ **不得通过**；返回 `需修改`。

---

## 6. ADR-008 内部一致性 (D1-D7) 与 ADR-007 / ADR-001 对齐

| 关系 | 一致性 |
|---|---|
| D1（跳过 v0.6.0 tag）↔ D6（删 [0.6.0] 段整合到 [0.7.0]）| 一致（narrative 统一）|
| D2（v0.7.0 = Step 2-5；不含 Step 6）↔ ADR-007 D3 6 步路径 | 一致（Step 6 推迟到 v0.8+，与 ADR-007 D4 兼容期立场延续）|
| D3（不重做 spec/design；继承 features/001 + ADR-007）| 大体一致；保留意见见 § 0 Precheck 特别裁定 — HYP-005 升级 release-blocking 在 features/001 spec 已预留 hook，本 feature 接管验证设计但 T30 强度不够（F-2）|
| D4（Tiered 实施）↔ tasks § 5 M2/M3/M4 | 一致；但 D4 Tier 2 表头 "Reviewer/Gate (6)" 与实际 5 条目不符（F-1）|
| D5（HYP-005 release-blocking）↔ T30 | 决策一致；验证强度不足（F-2）|
| D6（CHANGELOG 整合）↔ ADR-001 D1 narrative 诚实立场 | 一致；T33 acceptance 强度不足（F-4）|
| D7（README / setup docs / ADR-007 Amendment 校准）↔ ADR-007 D1 Amendment 在 v0.7.0 仍适用 | 一致；T35 显式 ref Amendment（F-7 加强建议）|
| ADR-007 D5（HYP-002 升级到运行时等价）↔ T30 | 一致 |
| ADR-001 D1 "narrow but hard"（不引入 ops/release/personas）↔ ADR-008 不做段 | 一致 |

**整体判定**：ADR-008 D1-D7 内部自洽且与 ADR-007 + ADR-001 对齐；执行级缺陷集中在 tasks.md（T30 / T29 / T33 / 数字不准），不是架构决策错误。

---

## 7. 文件 / 工件影响图（§ 3）评估

**comprehensiveness 检查**:

| ADR-008 影响范围 "修订" 项 | tasks.md § 3 "修改" 是否覆盖 | 备注 |
|---|---|---|
| `agents/hf-orchestrator.md` | ✓ | T4 |
| `agents/references/*.md`（profile-node-and-transition-map / reviewer-return-contract / routing-evidence-guide）| ✓ | T4 |
| 24 个 hf-* leaf SKILL.md | ✓（实际 23）| Tier 1+2 |
| `skills/using-hf-workflow/SKILL.md`（plugin-install loading channel; orchestrator 升级后描述同步）| **✗ 遗漏** | F-6 |
| README × 2 | ✓ | T31 |
| docs/{cursor,claude-code,opencode}-setup.md | ✓ | T32 |
| CHANGELOG.md | ✓ | T33 |
| SECURITY.md / CONTRIBUTING.md | ✓ | T34 |
| .claude-plugin/plugin.json / marketplace.json | ✓ | T34 |
| .cursor/rules/harness-flow.mdc | ✓ | T34 |

**结论**：基本覆盖，1 项遗漏（F-6）。

---

## 8. M0 → M7 + 关键路径评估

里程碑序列 M0 → M7 退出标准明确；依赖正向；无环。

- M0 骨架（T1-T3）：T1/T2 已 DONE，T3 即本 review；逻辑正确
- M1 Orchestrator 升级（T4）：严格在 leaf 修改之前（避免 [Workflow] Hard Gate 删除时 orchestrator pre-check 缺位）；R2 mitigation 到位
- M2 Tier 1（T5-T14）→ M3 sub-gate（T15）→ M4 Tier 2（T16-T28）→ T29 sub-gate：Tiered + sub-gate 拦截合理
- M5 HYP-002+005 验证（T30）：DAG 位置正确（在所有 leaf 修改完成后）；但内部 acceptance 强度不足（F-2）
- M6 Docs sync（T31-T35）：可并行；T35 ADR-007 Amendment 同步在 release pack 之前到位
- M7 Release pack（T36）：hf-release dogfood #5；最后步

**关键路径**：声明 "12 步"，显式 11 节点 + 中间步骤；F-5 建议补全。

---

## 结论

**需修改**

主要驱动:
1. **F-2 critical**: HYP-005 release-blocking 验证策略（T30）强度不足；触发用户硬规则 #2
2. **F-1 critical**: "24 leaf" 计数与实际（23）不符；Tier 2 "14 leaf" 把 sub-gate 算作 leaf，与 § 6 / § 9 矛盾
3. **F-3 important**: T29 缺 Acceptance / Files / Verify
4. **F-4 important**: T33 CHANGELOG acceptance 不足以保证 [0.6.0] → [0.7.0] 内容完整迁移（用户硬规则 #3 补偿在 — 不构成硬否决，但需强化）
5. **F-5 important**: 关键路径 "12 步" 含糊；中间 review/gate 步骤未枚举
6. **F-6 important**: § 3 影响清单遗漏 `skills/using-hf-workflow/SKILL.md` 描述同步
7. **F-7 ~ F-10 minor**: docs sync acceptance 量化、R3 措辞、T34 阈值、§ 7 cross-reference 等

**不构成硬否决**:
- 继承式入口（无独立 spec/design）：ADR-008 D3 reasoning 合理；本 reviewer 接受
- ADR-008 D1-D7 内部一致；与 ADR-007 + ADR-001 + 既有 ADR 关系表清晰
- M0 → M7 milestone 序列正确
- TR6 Router 重选就绪度良好（§ 8 / § 9）

---

## 下一步

- **next_action_or_recommended_skill**: `hf-tasks`（修订 tasks.md + ADR-008，按 F-1 ~ F-10 LLM-FIXABLE 修订建议落地，重点 F-2）
- **needs_human_confirmation**: false
- **reroute_via_router**: false（无 route / stage / 证据冲突；纯内容回修）

修订完成后由 `hf-workflow-router` 重新派发本 reviewer 复审（hf-tasks 退回 → hf-tasks-review Round 2）。

---

## 记录位置

- `features/002-leaf-skill-decoupling/reviews/tasks-review-2026-05-10.md`（本文件）

## 交接说明

- `hf-tasks`：作者据 F-1 ~ F-10 修订 tasks.md + ADR-008；critical findings (F-1, F-2) 必须解决；important (F-3 ~ F-6) 强烈建议解决；minor (F-7 ~ F-10) 视情况
- 复审 Round 2：修订后重派发本 reviewer（独立 subagent，与作者分离）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-tasks",
  "record_path": "features/002-leaf-skill-decoupling/reviews/tasks-review-2026-05-10.md",
  "key_findings": [
    "[critical][LLM-FIXABLE][TR3/TA4] F-2 T30 HYP-005 release-blocking 验证策略不足（'至少一次决策无 Next Action 字段' 是存在性证明，无法支撑 release-blocking 权重；缺 fail-first 反例 / 仪表化 ignore-mode / 全路径覆盖）",
    "[critical][LLM-FIXABLE][TR5/TA6] F-1 '24 hf-* leaf skill' 与实际不符（实际 = 23，ADR-007 D1 表 12 doer + 11 reviewer/gate）；Tier 2 '14 leaf' 把 T29 sub-gate 算作 leaf，与 § 6 / § 9 矛盾；ADR-008 D4 表头 'Reviewer/Gate (6)' 但只列 5",
    "[important][LLM-FIXABLE][TR2/TA2] F-3 T29 仅 'reserved'，缺 Acceptance / Files / Verify",
    "[important][LLM-FIXABLE][TR2/TR5] F-4 T33 CHANGELOG 整合 acceptance 不足以保证 [0.6.0] 子段（Added 7 + Changed 10 + Decided 8 + Notes 5）完整迁移到 [0.7.0]",
    "[important][LLM-FIXABLE][TR4] F-5 关键路径声明 '12 步' 与显式 11 节点 + '中间 review/gate 步骤' 不能 1-1 对照；尾部 review chain (test/code/traceability/regression-gate/completion-gate/finalize) 未列举",
    "[important][LLM-FIXABLE][TR5/TA6] F-6 § 3 影响清单遗漏 skills/using-hf-workflow/SKILL.md 描述同步（ADR-008 影响范围已列明）",
    "[minor][LLM-FIXABLE][TR2/TA3] F-7 T31/T32/T35 acceptance 略空，缺量化判据",
    "[minor][LLM-FIXABLE][TR4] F-8 R3 措辞 '不会让 release-blocking 失败 → 只可能让 release 推迟' 自相矛盾",
    "[minor][LLM-FIXABLE][TR2] F-9 T34 'grep 0.7.0 ≥ 5 处' 全集量化不当（应每文件 ≥ 1 而非全仓总和 ≥ 5）",
    "[minor][LLM-FIXABLE][TR3] F-10 § 7 验证策略与 T5-T28 任务条目无显式 cross-reference"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {"severity": "critical", "classification": "LLM-FIXABLE", "rule_id": "TR3", "summary": "F-2 T30 HYP-005 验证策略 'at least once' 太弱"},
    {"severity": "critical", "classification": "LLM-FIXABLE", "rule_id": "TR5", "summary": "F-1 24 vs 23 leaf 计数不符"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TR2", "summary": "F-3 T29 缺合同"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TR2", "summary": "F-4 T33 CHANGELOG 整合验证不足"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TR4", "summary": "F-5 关键路径不完整枚举"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TR5", "summary": "F-6 影响清单遗漏 using-hf-workflow"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TR2", "summary": "F-7 T31/32/35 acceptance 空"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TR4", "summary": "F-8 R3 措辞自相矛盾"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TR2", "summary": "F-9 T34 阈值依据不明"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TR3", "summary": "F-10 § 7 与 T5-T28 缺 cross-reference"}
  ],
  "scoring": {
    "TR1_executable": 7,
    "TR2_contract": 6,
    "TR3_test_seed": 5,
    "TR4_dependency": 7,
    "TR5_traceability": 6,
    "TR6_router_readiness": 8,
    "blocking_dimension": "TR3 = 5 < 6"
  },
  "user_dont_check": {
    "tier1_2_covers_24_leaf": "覆盖 23 actual leaves；'24' 计数不准 → F-1（不构成硬否决）",
    "hyp_005_strategy_clear": "**不清晰** → F-2 触发硬规则 #2，'需修改'",
    "changelog_audit_trail_compensated": "意图层面有补偿（D6 + T33 整合）→ F-4 强化建议，不构成硬否决",
    "critical_path_complete": "边缘 → F-5 important，不构成硬否决"
  }
}
```

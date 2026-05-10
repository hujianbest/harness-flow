# Traceability Review: HF Orchestrator Extraction & Skill Decoupling

- 评审对象: 整个 feature 证据链 — `features/001-orchestrator-extraction/` + 配套 ADR-007 + 上游 discovery + 实现工件 + 验证记录
- 评审 skill: `hf-traceability-review`
- 评审者: 独立 reviewer subagent（与 author 分离，符合 Fagan）
- 评审时间: 2026-05-10
- 评审范围基线: T1-T9 实现 commit `d93507d` (impl: T1-T9 hf-test-driven-dev)
- 评审方法: End-to-End Traceability + Zigzag Validation + Impact Analysis；6 维 rubric (`TZ1`–`TZ6`) + 反模式扫描 (`ZA1`–`ZA4`) + 父会话 8 项特殊关注核验

## Precheck

| 检查项 | 结果 |
|---|---|
| Feature 目录可定位且工件齐全 | ✓ `features/001-orchestrator-extraction/{spec,design,tasks,progress,README}.md` + `reviews/` + `approvals/` + `verification/` + `scripts/` |
| 上游 discovery 可回读 | ✓ `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md` + `docs/reviews/discovery-review-hf-orchestrator-extraction.md` |
| 配套 ADR 可回读 | ✓ `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` |
| 实现已 commit | ✓ `d93507d` 包含 40 文件改动；T1-T9 全部 commit |
| Author / Reviewer 分离 | ✓ T1-T9 由父会话实施；本 reviewer subagent 独立派发 |
| Stage / route / evidence 一致 | △ progress.md `Next Action: hf-design` 与 `Current Stage: hf-test-review` 不一致——见 Finding 2（不阻塞 traceability review；evidence 冲突由 orchestrator side 按 artifact 权威处理） |
| 实现交接块（commit message）与上游 review 记录一致 | ✓ commit message 引用 ADR-007 / spec / design / tasks 各阶段 verdict；列举所有触碰文件 |

Precheck 通过（progress.md sync gap 列入 Finding 2，不阻塞正式审查）。

## 父会话 8 项特殊关注核验

### 关注 1: Discovery wedge → spec FR/NFR/HYP → ADR-007 D1-D7 → design D-X → tasks T1-T9 → impl/verification 全链可追溯

| 链节 | 证据 |
|---|---|
| Discovery wedge | `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md` § 4 主 wedge：`agents/hf-orchestrator.md` always-on agent persona；§ 12 Bridge to Spec |
| → Spec | `spec.md` § 1（背景与问题陈述，承接 discovery § 1）+ § 6.1（9 项 in-scope）+ FR-001…FR-007 + NFR-001…NFR-005 + HYP-001…HYP-007 |
| → ADR-007 D1-D7 | 7 条决策与 spec 6.1 + 6.2 一一对应；D5 锁定 HYP-002 / HYP-003 release-blocking；D3 6 步落地路径中 v0.6.0 = Step 1 |
| → Design D-X | 15 条 D-X 决策（spec FR/NFR + ADR-007 D1-D7 → design § 9.2 表）；§ 3 traceability 表逐条回指 spec 编号 |
| → Tasks T1-T9 | tasks.md § 4 trace 表逐任务回指 spec FR / NFR / HYP + design D-X；T1（FR-001）/ T2.{a,b,c,d}（FR-002.a-d）/ T3（FR-004 + NFR-003）/ T4（FR-003 + NFR-005）/ T5（FR-003 + NFR-001 + NFR-004 + HYP-002 + HYP-003）/ T6.{a,b}（FR-006）/ T7（FR-007）/ T8（version bump）/ T9（collation）|
| → Impl files / verification | commit `d93507d` 触碰文件清单与 tasks § 3 工件影响图一一对应；3 个 verification records 落盘 |

**结论**：全链闭合，每一节都可在 on-disk artifact 中回读。

### 关注 2: Spec § 6.2 12 项 out-of-scope 是否被 design / tasks / impl 静默引入

逐条核（**0/12 命中**）：

| # | Out-of-scope item | 实现核验 | 结果 |
|---|---|---|---|
| 1 | Leaf skill 文件不被修改 | `git diff main...HEAD -- skills/` 仅触动 `using-hf-workflow` + `hf-workflow-router` 两个目录（FR-004 范围内的例外）；其它 22 个 hf-* skill 0 改动 | ✓ 0 命中 |
| 2 | 旧 skill 文件不被删除 | `ls skills/{using-hf-workflow,hf-workflow-router}/SKILL.md` 均存在；wc -l 21/21 行（≤30 行 stub） | ✓ |
| 3 | Closeout pack schema 不变 | `skills/hf-finalize/` 0 改动 | ✓ |
| 4 | Reviewer return verdict 词表不变 | `skills/hf-*-review/` + `hf-*-gate/` 11 个目录 0 改动 | ✓ |
| 5 | `hf-release` 行为不变 | `skills/hf-release/` 0 改动 | ✓ |
| 6 | `audit-skill-anatomy.py` 行为不变 | `scripts/audit-skill-anatomy.py` 0 改动；`agents/` 不在扫描范围 | ✓ |
| 7 | `hf-finalize` step 6A HTML 渲染不变 | `skills/hf-finalize/scripts/render-closeout-html.py` 0 改动 | ✓ |
| 8 | 不新增任何 `hf-*` skill | `ls skills/hf-*/` 仍 24 个；CHANGELOG `Notes` 显式声明 | ✓ |
| 9 | 不引入新 slash 命令 | `.claude/commands/` 0 改动；保持 7 条 | ✓ |
| 10 | 不针对第三方独立消费 leaf skill 投入 | 无 deliverable | ✓ |
| 11 | `agents/` 不引入 specialist personas | `ls agents/` 仅 `hf-orchestrator.md` + `references/` | ✓ |
| 12 | `.cursor/rules/` 不引入新 rule 文件 | `.cursor/rules/` 仅修改 `harness-flow.mdc` body；无新 mdc | ✓ |

**结论**：12 项 out-of-scope **0/12** 在下游被静默引入；ADR-007 D6 / D7 + design D-Skip-DDD / D-Skip-Threat 也未引回边界外内容。

### 关注 3: HYP-001 → HYP-007 每条均在下游有 disposition (validated / deferred-validate / non-blocking)

| HYP | Type | Blocking? | 下游处置 | 证据 |
|---|---|---|---|---|
| HYP-001 | Desirability | 否 | non-blocking deferred；P2 probe（GitHub issues / discussions）推迟到生态阶段；spec § 4 表格显式标"不阻塞" | spec § 4 + discovery review § 已知薄弱点 ✓ |
| HYP-002 | Viability | **是** | **validated**（release-blocking）通过 walking-skeleton regression PASS：26 文件 0 unallowed diff | `verification/regression-2026-05-10.md` + commit message "Fitness Function Evidence: walking-skeleton diff PASS over 26 files" ✓ |
| HYP-003 | Feasibility | **是** | **validated**（release-blocking）；Cursor 直接验证 + Claude Code / OpenCode PASS-by-construction with deferred-manual checklist | `verification/smoke-3-clients.md` + `verification/load-timing-3-clients.md` ratio 0.666 ✓ |
| HYP-004 | Feasibility | 否 | **validated**（commit-time 即决）：NFR-002 字符数 14,067 ≤ 23,245 = baseline × 1.10；spec-review Round 2 已升级 confidence "中-高" → "高" | `wc -c agents/hf-orchestrator.md` = 14,067 ✓ |
| HYP-005 | Feasibility | 否（本轮）；后续升级 | **deferred-validate**（design D-Disp 锁定 v0.7.0+ 目标态：纯 on-disk artifact 驱动；v0.6.0 兼容期允许同时消费 `Next Action` 字段作为辅助 hint，冲突时 artifact 权威）；orchestrator persona § 6 "v0.6.0 兼容期" 段落已 codify | design § 9.2 D-Disp + § 12.3 + `agents/hf-orchestrator.md` § 6 ✓ |
| HYP-006 | Feasibility | 否 | **validated**（NFR-004 acceptance）：4/4 reviews 含 "独立 reviewer subagent" 标识 | `verification/regression-2026-05-10.md` § "NFR-004 Reviewer/Author 分离验证" ✓ |
| HYP-007 | Usability | 否 | non-blocking deferred；推迟到 v0.6.0 release pack 阶段冷读抽检；README / setup docs / CHANGELOG 改写已就位 | spec § 4 + README.md / README.zh-CN.md Scope Note v0.6.0 ✓ |

**结论**：7 条 HYP **全部**有明确处置；HYP-002 / HYP-003 release-blocking 已 validated；HYP-004 / HYP-006 在 commit-time 即决；HYP-001 / HYP-005 / HYP-007 显式 deferred / 非阻塞。

### 关注 4: FR-001 → FR-007 每条 test seed in tasks + acceptance evidence in verification

| FR | Test seed in tasks | Acceptance evidence in verification |
|---|---|---|
| FR-001（orchestrator persona file）| T1 测试种子（fail-first：`test -f agents/hf-orchestrator.md`；GREEN：identity grep + wc -c + 9 references count） | `agents/hf-orchestrator.md` 存在（14,067 bytes），identity 锚点 line 9，frontmatter `name: hf-orchestrator` + `description`；commit message Fitness Function Evidence + load-timing-3-clients.md |
| FR-002.a（Cursor stub）| T2.a 测试种子（fail-first：`grep -c "agents/hf-orchestrator.md" .cursor/rules/harness-flow.mdc` 修改前 = 0；修改后 ≥ 1） | `.cursor/rules/harness-flow.mdc` body 含 6 处 "agents/hf-orchestrator"；`smoke-3-clients.md` Cursor 段 PASS |
| FR-002.b（Claude Code stub + plugin）| T2.b 测试种子（fail-first：`test -f CLAUDE.md`；JSON 校验） | `CLAUDE.md` 存在（2933 bytes）含 "## HF Orchestrator (always on)"；`.claude-plugin/plugin.json` `version: "0.6.0"` + agents[] 注册；`smoke-3-clients.md` Claude Code 段 PASS-by-construction |
| FR-002.c（OpenCode stub）| T2.c 测试种子（fail-first：`test -f AGENTS.md`） | `AGENTS.md` 存在（3022 bytes）；`smoke-3-clients.md` OpenCode 段 PASS-by-construction |
| FR-002.d（Identity check）| T2.d 测试种子（显式 RED：smoke-3-clients.md 不存在；GREEN：3 段 PASS\|deferred） | `smoke-3-clients.md` 落盘；3 段齐全；Cursor PASS（直接）+ 2/3 deferred manual 显式记录 |
| FR-003（等价语义保留）| T5.a/b 测试种子（regression-diff PASS） | `verification/regression-2026-05-10.md`：26 文件 0 unallowed diff；exit 0 + "PASS"；regression-diff.py 路径登记 |
| FR-004（兼容期 deprecated alias）| T3 测试种子（fail-first：`wc -l skills/using-hf-workflow/SKILL.md` 修改前 = 179；修改后 ≤ 30） | 11 个 stub 文件全部存在：2 个 SKILL.md ≤ 21 行；9 个 references stub ≤ 9 行；frontmatter `description` 含 "deprecated alias"；HTML marker 命中 |
| FR-005（ADR-007 锁定）| 无独立 task（与 spec 同 PR 起草）| `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` 7 条决策齐全；spec-review Round 2 已核验关系表 |
| FR-006.a（README ×2）| T6.a 测试种子（grep "v0.6.0" + 中英对照） | `README.md` + `README.zh-CN.md` Scope Note v0.6.0 段已落盘 |
| FR-006.b（Setup docs ×3）| T6.b 测试种子（3 个 setup docs grep "agents/hf-orchestrator"） | `docs/{cursor,claude-code,opencode}-setup.md` 3 份均含 v0.6.0 + orchestrator stub 说明 |
| FR-007（CHANGELOG）| T7 测试种子（grep `[Unreleased]`） | `CHANGELOG.md` `[0.6.0]` 段含 Added / Changed / Decided / Notes 4 子段；ADR-007 D1-D7 引用齐全 |

**结论**：FR-001 → FR-007 **全部**有 task test seed + verification / impl 文件双向证据。

### 关注 5: NFR-001 → NFR-005 QAS in spec + design uptake + verification

| NFR | Spec QAS（5 要素）| Design uptake | Verification 证据 |
|---|---|---|---|
| NFR-001（Always-On 加载延迟 × 1.20）| ISO 25010 Performance Efficiency / Time Behaviour；5 要素齐全（Stimulus Source / Stimulus / Environment / Response / Response Measure ≤ baseline × 1.20）| design § 14 NFR QAS 表 + D-NFR1-Schema（3 宿主 × 2 group × 5 次 = 30 次测量；落盘 schema） | `verification/load-timing-3-clients.md` ratio 0.666（远低于 1.20 阈值）；commit-time 字符数对照（NFR-002 双满足） |
| NFR-002（Token 预算 × 1.10）| ISO 25010 Performance Efficiency / Resource Utilization；5 要素齐全 | design § 14 + § 13.1 字符数动态契约 `wc -c agents/hf-orchestrator.md ≤ wc -c skills/{...}/SKILL.md × 1.10` | `wc -c agents/hf-orchestrator.md` = 14,067 ≤ 23,245；ratio 0.666 |
| NFR-003（旧路径不 404）| ISO 25010 Compatibility / Co-existence；5 要素齐全 | design § 14 + § 13.3 deprecated alias stub 契约（≤30 行 + HTML marker + frontmatter "deprecated alias"）| 11 个 stub 文件物理存在（`ls skills/using-hf-workflow/SKILL.md skills/hf-workflow-router/SKILL.md skills/hf-workflow-router/references/*.md`）；`grep "see agents/" ` 全部命中 |
| NFR-004（Reviewer/Author 分离纪律）| ISO 25010 Maintainability + Functional Suitability；5 要素齐全 | design § 14 + orchestrator persona § 9 "派发独立 subagent" + Hard Stop "父会话内联执行 review (违反 NFR-004 / Fagan)" | `verification/regression-2026-05-10.md` § "NFR-004"：4/4 reviews 含 "独立 reviewer subagent" |
| NFR-005（容许差异白名单稳定）| ISO 25010 Maintainability / Testability；5 要素齐全 | design § 14 + § 13.5 regression-diff 脚本契约（4 条正则白名单硬编码）| `regression-diff.py` 4 条 ALLOWLIST_PATTERNS（line 39-47）；`test_regression_diff.py` 3/3 PASS（self / mutation / allowlist） |

**结论**：NFR-001 → NFR-005 **全部**有 QAS（spec）+ design uptake + verification evidence 三层证据闭合。

### 关注 6: ADR-007 D1-D7 每条在 spec / design / tasks / impl 至少一处反映

| ADR-007 决策 | 反映位置 |
|---|---|
| D1（HF 三层架构 invariant + 生效阶段子段）| spec § 6.1 #1 ✓；design § 4 (DDD skip rationale 引用 BC=1) + § 6 (Front Controller 沿用) + § 9.2 D-Disp（v0.6.0 commitment / v0.7.0+ enforcement）✓；orchestrator persona § "I am the HF Orchestrator" + § 6 兼容期段 ✓；CHANGELOG `Decided` ✓ |
| D2（single source `agents/` + `agents/references/`）| spec § 6.1 #2 ✓；design § 9.1 / D-Mig ✓；T1 / T3 实施（git mv 9 references + 9 stub）✓；CHANGELOG `Decided` ✓ |
| D3（6 步落地路径，Step 1 only）| spec § 6.2 + § 13 (阻塞项=无；ADR-007 D2 锁定)；design § 1 概述 + § 9.1 ✓；tasks 整体范围限定 v0.6.0 = Step 1 ✓；CHANGELOG `Decided` ✓ |
| D4（旧 skill 兼容期 deprecated alias）| spec FR-004 + NFR-003 + C-006 ✓；design D-Stub / D-Stub-Marker ✓；T3 实施 11 个 stub ✓；CHANGELOG `Changed` 描述 |
| D5（HYP-002 / HYP-003 release-blocking）| spec § 4 表格（Blocking? = 是）✓；design § 16.3 ✓；T5 (P0 + 标 release-blocking) ✓；verification regression + smoke + load-timing ✓ |
| D6（v0.7+ ops/release skills 必须遵循新 invariant）| spec 间接（非 spec 范围）；ADR-007 D6 + ADR-005 D7 关系表 ✓；CHANGELOG `Decided` ✓ |
| D7（specialist personas 不扩张）| spec § 6.2 #11 + § 6.1（agents/ 仅含 orchestrator）✓；`ls agents/` 仅 `hf-orchestrator.md` + `references/` ✓；CHANGELOG `Decided` ✓ |

**结论**：ADR-007 D1-D7 **全部**至少反映在一处下游工件；D5 验证证据齐全；D1 / D2 / D4 在 impl 文件层面有可冷读痕迹。

### 关注 7: 无 orphan 工件（feature/ 下每个文件 → spec/design/tasks/ADR 锚点）

逐一核（**0 orphan**）：

| 文件 | 锚点 |
|---|---|
| `spec.md` | spec 自身 |
| `design.md` | design 自身（spec § 6.1 + ADR-007 D3 Step 1）|
| `tasks.md` | tasks 自身（design § 11 14 模块 → 12 任务 + T9 collation）|
| `progress.md` | router/orchestrator state tracking（spec template；orchestrator § 2 evidence base）|
| `README.md` | feature artifacts table（spec template）|
| `reviews/spec-review-2026-05-10.md` | hf-spec-review record（spec § 4 / ADR-007 D5）|
| `reviews/design-review-2026-05-10.md` | hf-design-review record（design 自身）|
| `reviews/tasks-review-2026-05-10.md` | hf-tasks-review record（tasks 自身）|
| `approvals/{spec,design,tasks}-approval-2026-05-10.md` | 各阶段 approval step（router § 8 / orchestrator § 8 关键分支）|
| `verification/regression-2026-05-10.md` | T5.a/b/e + FR-003 + NFR-005 + HYP-002 |
| `verification/smoke-3-clients.md` | T2.d + FR-002.d + HYP-003（identity gate）|
| `verification/load-timing-3-clients.md` | T5.c + NFR-001 + HYP-003（量化部分）|
| `scripts/regression-diff.py` | T4 + design D-RegrLoc + D-RegrImpl + NFR-005 |
| `scripts/test_regression_diff.py` | T4.e/f + NFR-005 acceptance（mutation + self / allowlist） |

`scripts/__pycache__/` 是 Python 运行时缓存（`features/001-orchestrator-extraction/scripts/__pycache__/`），由 `test_regression_diff.py` 跑产生；不属于 source 工件，但 git 通常会忽略。**轻量薄弱项**（见下方 "缺失或薄弱项 #1"）：建议把该路径加入 `.gitignore` 或确认它未被 commit。

**结论**：14 个 source 文件 **全部**映射到锚点，**0 orphan**。

### 关注 8: 无 orphan 需求（每个 spec FR/NFR → 至少一个 impl 文件 / verification record）

逐一核（**0 orphan needs**）：

| 需求 | 至少一个 impl / verification |
|---|---|
| FR-001 | `agents/hf-orchestrator.md`（impl）+ `verification/regression-2026-05-10.md`（间接 via FR-003）|
| FR-002.a | `.cursor/rules/harness-flow.mdc`（impl）+ `verification/smoke-3-clients.md` Cursor 段 |
| FR-002.b | `CLAUDE.md` + `.claude-plugin/plugin.json`（impl）+ `verification/smoke-3-clients.md` Claude Code 段 |
| FR-002.c | `AGENTS.md`（impl）+ `verification/smoke-3-clients.md` OpenCode 段 |
| FR-002.d | `verification/smoke-3-clients.md`（identity gate 三段 PASS\|deferred）|
| FR-003 | `verification/regression-2026-05-10.md`（regression-diff PASS）|
| FR-004 | 11 个 deprecated alias stub 文件（impl，物理存在）|
| FR-005 | `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（impl）|
| FR-006.a | `README.md` + `README.zh-CN.md`（impl）|
| FR-006.b | `docs/{cursor,claude-code,opencode}-setup.md`（impl）|
| FR-007 | `CHANGELOG.md` `[0.6.0]` 段（impl）|
| NFR-001 | `verification/load-timing-3-clients.md` ratio 0.666 |
| NFR-002 | `verification/load-timing-3-clients.md` static character count + commit message Fitness Function |
| NFR-003 | 11 个 stub 文件 `ls` 可读 + frontmatter "deprecated alias" |
| NFR-004 | `verification/regression-2026-05-10.md` § "NFR-004 Reviewer/Author 分离验证" |
| NFR-005 | `features/001-orchestrator-extraction/scripts/test_regression_diff.py` 3/3 PASS |

**结论**：12 条 FR + 5 条 NFR **全部**有 impl 文件 / verification record（多数双向）；**0 orphan**。

## 6 维 rubric 评审

| 维度 | 评分 | 关键观察 |
|---|---|---|
| **TZ1 规格 → 设计追溯** | 9/10 | spec § 6.1 9 项 + FR/NFR/HYP 全部映射到 design § 3 traceability 表 + § 9.2 D-X 决策；spec-review Round 2 末尾 4 项 handoff 全部落地（design-review 已核验）；ADR-007 D1-D7 在 spec § 6.2 / design § 9 双向引用 |
| **TZ2 设计 → 任务追溯** | 9/10 | design § 11 14 模块全部映射到 tasks § 5 任务清单；design D-FR2-Tasks（FR-002 拆 4 sub / FR-006 拆 2 sub）→ T2.{a,b,c,d} + T6.{a,b}；D-RegrLoc / D-RegrImpl → T4；D-NFR1-Schema → T5.c；D-Disp → orchestrator persona § 6 + § 1 实施时落到主文件 |
| **TZ3 任务 → 实现追溯** | 8/10 | T1-T9 acceptance 全部命中：T1（agents/hf-orchestrator.md 14,067 bytes / identity 锚点 / 9 references 完整）/ T2.{a,b,c}（3 stub 全建）/ T2.d（smoke-3-clients.md Cursor PASS + 2/3 deferred）/ T3（11 stub）/ T4（test 3/3 PASS）/ T5（regression PASS / load-timing 0.666 / NFR-004 4/4）/ T6.{a,b}（README + 3 setup docs sync）/ T7（CHANGELOG）/ T8（version bump）/ T9（progress 部分同步——见 Finding 2）。失分点：marketplace.json description sync 漂移（Finding 1）+ progress.md sync 部分（Finding 2）|
| **TZ4 实现 → 验证追溯** | 9/10 | 3 个 verification records 完整对应 release-blocking gate：regression-2026-05-10.md（HYP-002 / NFR-005 / NFR-004）+ smoke-3-clients.md（HYP-003 identity）+ load-timing-3-clients.md（HYP-003 量化 / NFR-001）；commit message "Fitness Function Evidence" 列出 fresh evidence 摘要；regression-diff.py 自跑 PASS（26 文件 0 unallowed）；test_regression_diff.py 自跑 3/3 PASS |
| **TZ5 漂移与回写义务** | 7/10 | 大部分回写已完成（README × 2 / setup docs × 3 / CHANGELOG / SECURITY / CONTRIBUTING / plugin.json version + agents 注册 / harness-flow.mdc body）；**漂移点**：(1) marketplace.json description 未更新但 CHANGELOG 声明已更新——见 Finding 1（important LLM-FIXABLE）；(2) progress.md `Next Action` / `Status` / Session Log 滞后——见 Finding 2（minor LLM-FIXABLE，tasks-review Round 2 已识别为 housekeeping）；(3) feature README.md `Verification` 表两行仍空——见 Finding 3（minor LLM-FIXABLE）|
| **TZ6 整体链路闭合** | 8/10 | spec → design → tasks → impl → verification → release-blocking validation 全链可冷读；HYP-002 + HYP-003 双 release-blocking 假设 fresh evidence 落盘；orchestrator persona 与 deprecated alias stub 物理共存；3 宿主 always-on 注入路径 ready；ADR-007 D5 + spec § 4 + commit message Fitness Function 三层互证。失分点：3 条漂移项（Finding 1-3）累积影响"approved 工件与当前代码完全一致"判断 |

**关键阈值检查**：所有 6 维 ≥ 7/10；无维度 < 6 → 不触发"不得返回 通过"红线。但 TZ5 = 7 + Finding 1 (important) → 适用"任一关键 finding important + LLM-FIXABLE → 通常 verdict = 需修改"惯例。

## 反模式扫描（`ZA1`–`ZA4`）

| ID | 反模式 | 命中? | 说明 |
|---|---|---|---|
| `ZA1` | spec drift（规格已变更，设计/任务仍基于旧版本）| ✗ | spec / design / tasks 三阶段 round-trip review-approval 无残留版本错配 |
| `ZA2` | orphan task（任务无法追溯到规格或设计）| ✗ | 13 leaf tasks（T1 / T2.{a-d} / T3 / T4 / T5 / T6.{a-b} / T7 / T8 / T9）全部回指 spec / design |
| `ZA3` | undocumented behavior（代码引入未记录的新行为）| △ minor | (a) `.claude-plugin/plugin.json` `agents` 字段注册 alwaysActive = true 是 spec FR-002.b 允许的；OK。(b) marketplace.json description **未**更新但 CHANGELOG 声明已更新——见 Finding 1（轻度命中：CHANGELOG 中"undocumented" 反向，是工件claim 但未实施）|
| `ZA4` | unsupported completion claim（验证不足却声称完成）| ✗ | 所有 release-blocking gate 都有 fresh evidence；deferred manual 接受度（HYP-003 1/3 + 2/3）已在 spec § 4 / ADR-007 D5 / verification/smoke-3-clients.md 三处显式记录；不属"声称完成"，是经过批准的 release-blocking gate 内部接受度 |

无关键反模式命中；ZA3 minor 已在 Finding 1 中显式登记。

## 链接矩阵

### Spec → Design

| Spec 编号 | Design 章节 / D-X |
|---|---|
| FR-001 | § 9 / § 11 / § 14；D-Layout / D-Identity |
| FR-002.a/b/c/d | § 11 Host stub / § 13.4；D-Host-Cursor / D-Host-CC / D-Host-OC / D-Identity |
| FR-003 | § 16.1 / § 13.5；D-RegrLoc / D-RegrImpl |
| FR-004 | § 11 Deprecated alias / § 13.3；D-Stub / D-Stub-Marker |
| FR-005 | ADR-007（不在 design 修改）|
| FR-006 / FR-007 | § 11 Docs sync 模块 |
| NFR-001 | § 14；D-NFR1-Schema |
| NFR-002 | § 14 + § 13.1 |
| NFR-003 | § 14 + § 11 + § 13.3 |
| NFR-004 | § 14 + orchestrator § 9（reviewer dispatch）|
| NFR-005 | § 16 + § 13.5 |
| HYP-005 | § 9.2 D-Disp + § 12.3 |

### Design → Tasks

| Design 决策 / 模块 | Tasks |
|---|---|
| § 11 14 模块 | T1（main + 9 refs）/ T2.{a,b,c}（3 host stub）/ T3（deprecated alias × 11）/ T4（regression-diff）/ T5（walking-skeleton + verification record × 3）/ T6.{a,b}（docs sync）/ T7（CHANGELOG）/ T8（project metadata）/ T9（collation）|
| D-FR2-Tasks | T2.{a,b,c,d} + T6.{a,b} 拆解 |
| D-NFR1-Schema | T5.c |
| D-RegrLoc / D-RegrImpl | T4 |
| D-Disp | orchestrator persona § 6（dispatch hint compat）|
| D-Identity | T1.b + T2.d |

### Tasks → Impl

| Task | Impl 文件 |
|---|---|
| T1 | `agents/hf-orchestrator.md` + `agents/references/*.md`（9）|
| T2.a | `.cursor/rules/harness-flow.mdc` |
| T2.b | `CLAUDE.md` + `.claude-plugin/plugin.json` |
| T2.c | `AGENTS.md` |
| T3 | `skills/{using-hf-workflow,hf-workflow-router}/SKILL.md` + 9 references stub |
| T4 | `features/001-orchestrator-extraction/scripts/{regression-diff,test_regression_diff}.py` |
| T6.a | `README.md` + `README.zh-CN.md` |
| T6.b | `docs/{cursor,claude-code,opencode}-setup.md` |
| T7 | `CHANGELOG.md` |
| T8 | `SECURITY.md` + `CONTRIBUTING.md` |

### Impl → Test / Verification

| Impl | Test / Verification |
|---|---|
| `agents/hf-orchestrator.md` | identity 锚点 grep + wc -c + `verification/load-timing-3-clients.md` |
| 3 host stubs | `verification/smoke-3-clients.md`（Cursor PASS + 2/3 deferred）|
| `regression-diff.py` | `test_regression_diff.py` 3/3 PASS + `verification/regression-2026-05-10.md` 26 文件 0 unallowed diff |
| 11 deprecated alias stubs | `wc -l` ≤ 30 / ≤ 10；`grep "deprecated alias"` 全部命中 |
| 4 个 review records | `grep -c "独立 reviewer subagent"` ≥ 4（NFR-004）|

## 发现项

- **[important][LLM-FIXABLE][TZ5/ZA3] `.claude-plugin/marketplace.json` description 未实际更新，但 CHANGELOG `[0.6.0] Changed` 段声明已更新——claim 与 impl reality 的双向 trace 漂移。**

  **trace 路径**：design § 11 "Plugin manifest" 模块 + tasks T2.b "Files / 触碰工件" 列出 `.claude-plugin/marketplace.json (description 同步)` + CHANGELOG.md `[0.6.0] Changed` 段写："**`.claude-plugin/marketplace.json`** — `description` updated to describe the v0.6.0 orchestrator-extraction structural refactor."

  **impl reality**：`.claude-plugin/marketplace.json` line 16 `plugins[0].description` 仍以 "v0.5.1 patches a vendoring bug ... hf-finalize is the only modified skill across v0.5.x; skill set stays at 24 hf-* + using-hf-workflow; slash commands stay at 7." 结尾；**完全没有** v0.6.0 / orchestrator / agents/ 字眼。`grep -c "0.6.0\|0\.6\.0" .claude-plugin/marketplace.json` = 0。

  **影响**：T2.b acceptance 字段未显式列 marketplace.json description sync（仅 plugin.json version + JSON 校验），所以 T2.b 严格说没破契约；但 design + tasks Files + CHANGELOG 三处 claim "已更新" 与文件实际状态冲突——属 ZA3 "工件 claim 与现状不一致"轻度命中 + TZ5 "未回写 / undocumented inconsistency"。

  **修复建议（轻量）**：在 marketplace.json plugins[0].description 末尾追加一段："v0.6.0 introduces agents/hf-orchestrator.md as the always-on agent persona that replaces using-hf-workflow + hf-workflow-router (now deprecated aliases through v0.6.x); locks the HF three-layer architecture invariant per ADR-007 D1; 24 hf-* skill set unchanged, 7 slash commands unchanged." **该单行编辑可在 hf-traceability-review approval 后由父会话直接落 commit**；无需重写其它工件。

- **[minor][LLM-FIXABLE][TZ5/ZA1] `progress.md` 状态字段滞后；T9.b acceptance 仅部分满足。**

  **trace 路径**：T9.b acceptance："progress.md `Current Stage` 已更新为 `hf-test-review`；`Pending Reviews And Gates` 列出后续序列"；T9.b 完成条件含 "Session Log 补 design + tasks 阶段事件"。

  **impl reality**：
  - `Current Stage: hf-test-review` ✓（line 12 + line 18 双重声明）
  - `Pending Reviews And Gates: hf-test-review → hf-code-review → hf-traceability-review → ...` ✓
  - `Status: spec drafting` ✗（应为 "implementation complete"）
  - `Next Action Or Recommended Skill: hf-design` ✗（应为 `hf-traceability-review` 或后续 review chain 节点）
  - `Session Log` 仅记录到 "spec approval record 落盘" ✗（缺 design / design-review / design-approval / tasks / tasks-review / tasks-approval / hf-test-driven-dev T1-T9 commit / 本 traceability-review 派发等）
  - `Open Risks` 段未标记 release-blocking 假设已 validated（HYP-002 / HYP-003 verification 落盘）

  **影响**：tasks-review Round 2 已显式识别为"薄弱项 1"并标"不阻塞 tasks-review"，期望 hf-test-driven-dev 阶段顺手补齐——但 T1-T9 commit 时未补齐。orchestrator persona § 2 "evidence 冲突按未批准处理、选更上游节点" 在读到 `Next Action: hf-design` 时会引发回 hf-design 假阴性路由，需要 evidence-conflict resolution 才能纠正。**冲突时以 artifact（reviews / approvals / verification）权威**（ADR-007 D1 + design § 12.3）兜底，所以不构成 routing block，但是 router/orchestrator side 多一层 cross-check 成本。

  **修复建议（轻量）**：单 commit 同步 progress.md 4 处字段（Status / Next Action / Open Risks 标 validated / Session Log 追加 design/tasks/impl/traceability-review 7-9 条事件）；可与 Finding 1 合并到同一回写 commit。

- **[minor][LLM-FIXABLE][TZ5] `features/001-orchestrator-extraction/README.md` `Verification` 表两行仍空，但 verification 工件实际已落盘。**

  **trace 路径**：T9.c acceptance："README.md `Status Snapshot` 同步；Reviews & Approvals 表 design-review / design-approval 行已写入 verdict"——T9.c 已部分满足（Reviews & Approvals 表已 7 行齐全）；但 README.md `Verification` 表两行（regression / completion）仍写占位 `verification/regression-YYYY-MM-DD.md` + `verification/completion-task-NNN.md` 且 "结论" / "日期" 列空。

  **impl reality**：实际 `verification/regression-2026-05-10.md` 落盘（PASS）；`verification/smoke-3-clients.md` 落盘；`verification/load-timing-3-clients.md` 落盘——但 README Verification 表只列 2 行（regression + completion），没列 smoke / load-timing 两件套。

  **影响**：cosmetic；冷读者从 `features/001-orchestrator-extraction/README.md` 入口看不到 verification 实绩；但 progress.md / verification/ 目录直接可读，所以不构成 routing block。

  **修复建议（轻量）**：把 README Verification 表扩成 4 行（regression-2026-05-10 / smoke-3-clients / load-timing-3-clients / completion-task-NNN）；填实绩列。可与 Finding 1 + Finding 2 合并。

- **[minor][LLM-FIXABLE][TZ4/cosmetic] T1.d acceptance 提及 `.bak` 路径，但 impl 走的是 git mv（design D-Mig 的预期路径）。**

  **trace 路径**：T1.d acceptance："`agents/references/<x>.md skills/hf-workflow-router/references/<x>.md.bak` 在迁移前应等价（`git mv` 后旧路径已为 stub）"。

  **impl reality**：commit message "Files changed: ... agents/references/{...}.md (9 files, git mv from skills/hf-workflow-router/references/, history preserved)"——走的是 git mv（与 design D-Mig 一致），旧路径直接转 stub（D-Mig + D-Stub），没有产生 `.bak` 文件。

  **影响**：T1.d 半句话提及 `.bak` 是冗余/cosmetic（同 acceptance 后半括号 "git mv 后旧路径已为 stub" 已显式说明 git mv 路径合法）；reviewer 冷读 acceptance 时 `.bak` 容易混淆。**功能性 = 0**；git history 通过 `git log --follow agents/references/<x>.md` 可证明物理迁移合法。

  **修复建议（极轻量）**：删除 T1.d 中 `.bak` 半句话即可；但 tasks.md 已 approved 不应轻改——可在 hf-finalize 阶段 closeout 工件交接时附 errata 一句注解。**不阻塞**。

## 缺失或薄弱项

- **薄弱项 1（已核验，无需处理）：`features/001-orchestrator-extraction/scripts/__pycache__/` 是 Python 运行时产物。** 已核验 `git ls-files features/001-orchestrator-extraction/scripts/__pycache__/` 返回空（未被加入版本控制）；`.gitignore` line 4-5 含 `__pycache__/` + `*.pyc` 兜底（注释 "added by R1 anatomy audit"）。**无 trace 漂移；不阻塞**。

- **薄弱项 2：HYP-001（Desirability，medium confidence）的 P2 probe（GitHub issues / discussions）从 discovery review 起一直未执行。** discovery review § 6.1 + spec § 4 + ADR-007 已显式接受为 "non-blocking deferred"；本轮维持原判定。**不阻塞**；建议在 v0.6.0 release pack `hf-release` 阶段（dogfood 第 4 次）顺手在 release notes 中标记一句 "v0.6.0 wedge 验证基于生态对照系 + 维护者判断；P2 probe（GitHub issues / discussions 翻查）推迟到 v0.7.x"。

- **薄弱项 3：HYP-007（Usability）的"5 分钟冷读 orchestrator vs SOP 二分"抽检从未执行。** spec § 4 标 "推迟到 v0.6.0 release pack 阶段抽检"；本轮 README + setup docs + CHANGELOG sync 已就位；抽检本身落到 hf-release / hf-completion-gate 阶段。**不阻塞**；列入 release pre-flight checklist。

- **薄弱项 4：marketplace.json description 未同步（Finding 1）+ progress.md sync gap（Finding 2）累积影响 closeout pack `Doc Freshness Gate` 通过率。** `hf-doc-freshness-gate`（release 前最后一道）会扫描 README / docs / CHANGELOG / 项目元数据 / plugin manifest 与实际功能的一致性；marketplace.json description 漂移 + CHANGELOG 中"已更新"声明 = 显式不一致。建议 Finding 1 修复在 hf-doc-freshness-gate 派发前完成，否则会触发该 gate 退回。

## 需要回写或同步的工件

- **`.claude-plugin/marketplace.json`**（Finding 1）
  - 原因：description 未同步到 v0.6.0；CHANGELOG `[0.6.0] Changed` 已声明"已更新"——双向 trace 漂移
  - 建议动作：在 plugins[0].description 末尾追加一段 v0.6.0 / orchestrator / agents/hf-orchestrator.md / 三层架构 invariant / ADR-007 D1 的总结（中英文/单语均可，与 plugin.json description 同款风格）；保持 24 hf-* + 7 slash 命令不变的兼容性提示

- **`features/001-orchestrator-extraction/progress.md`**（Finding 2）
  - 原因：`Status` / `Next Action` / `Open Risks` / `Session Log` 滞后于实际 stage（T1-T9 GREEN）
  - 建议动作：4 处字段一次性同步——`Status: implementation complete`；`Next Action Or Recommended Skill: hf-traceability-review`（或后续 review chain）；`Open Risks` 标记 HYP-002 / HYP-003 已 validated；`Session Log` 追加 design / tasks / impl / hf-traceability-review 派发 7-9 条事件

- **`features/001-orchestrator-extraction/README.md` Verification 表**（Finding 3）
  - 原因：3 个 verification records 已落盘但 README 表只列占位 2 行
  - 建议动作：扩 Verification 表为 4 行，填 `verification/regression-2026-05-10.md`（结论：PASS）/ `verification/smoke-3-clients.md`（结论：Cursor PASS + 2/3 deferred）/ `verification/load-timing-3-clients.md`（结论：ratio 0.666 PASS）/ completion 行保留占位

- ~~`.gitignore`（薄弱项 1）~~ **已核验无需修改**：`__pycache__/` + `*.pyc` 已在 `.gitignore` line 4-5 兜底；`git ls-files .../scripts/__pycache__/` 返回空。

## 结论

**需修改**

理由：
- 6 维 rubric 中 TZ5（漂移与回写义务）= 7/10 + 1 条 important finding（Finding 1 marketplace.json description 漂移）+ 2 条 minor finding（Finding 2 progress.md sync / Finding 3 README Verification 表）+ 1 条 cosmetic finding（Finding 4 T1.d `.bak` 措辞）；总计 4 条 finding，**全部 LLM-FIXABLE**，可在 1 次定向回写 commit 中收敛。
- 父会话 8 项特殊关注：(1) 全链可追溯 ✓；(2) spec § 6.2 12 项 out-of-scope **0/12** 命中 ✓；(3) HYP-001…HYP-007 **全部**有 disposition ✓；(4) FR-001…FR-007 **全部**有 test seed + acceptance evidence ✓；(5) NFR-001…NFR-005 **全部**有 QAS + design uptake + verification ✓；(6) ADR-007 D1-D7 **全部**至少一处反映 ✓；(7) feature 工件 **0 orphan** ✓；(8) spec FR/NFR **0 orphan needs** ✓。
- HYP-002 / HYP-003 release-blocking 双假设 fresh evidence 落盘且 PASS（regression 26 文件 0 unallowed diff；3 宿主 smoke Cursor PASS + 2/3 deferred manual；NFR-001 ratio 0.666）。
- 范围与方向稳定，**仅需 wording / 回写层修订**，不触发 ZA1 spec drift / ZA2 orphan task / ZA4 unsupported completion；ZA3 仅轻度命中（Finding 1）。

预计 **1 轮定向回写**（marketplace.json description + progress.md 4 字段 + feature README Verification 表 + 可选 `.gitignore`）即可收敛到 `通过`，不需要回 hf-test-driven-dev 重做实现。但因 Finding 1 是 important（CHANGELOG 已 claim 但 impl 未到位，hf-doc-freshness-gate 会拦），verdict 必须为 `需修改` 而非 `通过`。

## 追溯缺口

- **Finding 1 缺口**：marketplace.json description ↔ CHANGELOG claim ↔ design § 11 / tasks T2.b Files 间 trace 漂移
- **Finding 2 缺口**：progress.md `Next Action` / `Status` / `Open Risks` / `Session Log` 与 T9.b 完成条件 + 实际 commit 状态间 trace 漂移
- **Finding 3 缺口**：feature README.md `Verification` 表 ↔ verification/ 目录实绩间 trace 漂移
- **Finding 4 缺口（cosmetic）**：T1.d acceptance `.bak` 措辞 ↔ design D-Mig git mv 路径间表述冗余

无核心断链；无 spec drift；无 orphan；无 unsupported completion claim。

## 下一步

- **唯一下一步**：`hf-test-driven-dev`（定向修订 4 处回写项）
- 修订重点（按优先级）:
  1. **Finding 1 (important)**: `.claude-plugin/marketplace.json` plugins[0].description 末尾追加 v0.6.0 / orchestrator 段；与 plugin.json description 同款风格
  2. **Finding 2 (minor)**: `features/001-orchestrator-extraction/progress.md` 4 字段同步（Status / Next Action / Open Risks / Session Log）
  3. **Finding 3 (minor)**: `features/001-orchestrator-extraction/README.md` Verification 表扩 4 行 + 填实绩
  4. ~~薄弱项 1（已核验：`__pycache__/` 已在 `.gitignore` 兜底，无 trace 漂移）~~
- 修订后**重新派发** `hf-traceability-review` 一次，预期 1 轮收敛到 `通过`
- **不**需要回 `hf-workflow-router` / `hf-orchestrator`：route / stage / evidence 一致（progress.md sync 是 Finding 2 内容，不是 stage/route 冲突）；reroute_via_router = false
- 通过后再进入 `hf-regression-gate`（按 hf-traceability-review SKILL § 4 verdict 表 "通过 → hf-regression-gate"）

## 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：**否**（`需修改` 默认 `false`，按 `references/traceability-review-record-template.md` 返回规则）
- 是否需要回 router（reroute_via_router）：**否**（route / stage / evidence 一致，无 workflow blocker）
- USER-INPUT findings：**无**（4 条 finding 全部 LLM-FIXABLE，由 `hf-test-driven-dev` 定向回写节点直接修订；不需要业务裁决 / 外部阈值 / 真人拍板）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "record_path": "features/001-orchestrator-extraction/reviews/traceability-review-2026-05-10.md",
  "key_findings": [
    "[important][LLM-FIXABLE][TZ5/ZA3] .claude-plugin/marketplace.json plugins[0].description 未实际更新到 v0.6.0/orchestrator，但 CHANGELOG [0.6.0] Changed 段 + design § 11 + tasks T2.b Files 三处声明 '已更新'——claim 与 impl reality 双向 trace 漂移；hf-doc-freshness-gate 会拦",
    "[minor][LLM-FIXABLE][TZ5/ZA1] features/001-orchestrator-extraction/progress.md 状态字段滞后：Status='spec drafting'、Next Action='hf-design'、Session Log 仅到 spec approval、Open Risks 未标 HYP-002/003 validated；T9.b 完成条件部分未满足",
    "[minor][LLM-FIXABLE][TZ5] features/001-orchestrator-extraction/README.md Verification 表 2 行占位未替换为 3 个 verification records 实绩",
    "[minor][LLM-FIXABLE][TZ4/cosmetic] T1.d acceptance '.bak' 措辞与 impl git mv 路径表述冗余（功能 = 0；可后期 errata）"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "TZ5/ZA3",
      "summary": ".claude-plugin/marketplace.json plugins[0].description 仍以 v0.5.1 vendoring patch 描述结尾；无 v0.6.0 / orchestrator / agents/ 字眼；但 CHANGELOG [0.6.0] Changed + design § 11 + tasks T2.b Files 三处声明 '已更新'。修复建议：在 plugins[0].description 末尾追加 v0.6.0 / orchestrator / agents/hf-orchestrator.md / 三层架构 invariant / ADR-007 D1 总结段；保持 24 hf-* + 7 slash 命令不变兼容性提示。"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TZ5/ZA1",
      "summary": "progress.md Status='spec drafting'、Next Action Or Recommended Skill='hf-design'、Session Log 仅到 spec approval、Open Risks 未标 HYP-002/HYP-003 已 validated。tasks-review Round 2 薄弱项 1 已识别但未在 T1-T9 commit 中修复；T9.b 完成条件 'Session Log 补 design+tasks 阶段事件' 部分未满足。修复建议：单 commit 同步 4 字段。"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TZ5",
      "summary": "features/001-orchestrator-extraction/README.md Verification 表两行（regression + completion）仍写占位且 '结论'/'日期' 列空；实际 3 个 verification records 已落盘（regression-2026-05-10 PASS / smoke-3-clients Cursor PASS + 2/3 deferred / load-timing ratio 0.666 PASS）。修复建议：扩为 4 行 + 填实绩。"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TZ4/cosmetic",
      "summary": "T1.d acceptance 提及 'agents/references/<x>.md skills/hf-workflow-router/references/<x>.md.bak 在迁移前应等价'，但 impl 走 design D-Mig 指定的 git mv（旧路径直接转 stub，无 .bak 文件）。功能性影响 = 0；可在 hf-finalize errata 中标注。"
    }
  ],
  "round": 1,
  "rubric_scores": {
    "TZ1_spec_to_design": 9,
    "TZ2_design_to_tasks": 9,
    "TZ3_tasks_to_impl": 8,
    "TZ4_impl_to_verification": 9,
    "TZ5_drift_and_writeback": 7,
    "TZ6_overall_closure": 8
  },
  "release_blocking_validation": {
    "HYP-002": "validated (walking-skeleton regression PASS, 26 files 0 unallowed diffs)",
    "HYP-003": "validated (Cursor direct + Claude Code/OpenCode PASS-by-construction with deferred-manual; NFR-001 ratio 0.666)"
  },
  "out_of_scope_check": "0/12 命中（spec § 6.2 12 项 out-of-scope 未被静默引入）",
  "orphan_check": "0 orphan artifacts (14 files in features/001-orchestrator-extraction/) + 0 orphan requirements (12 FR + 5 NFR all mapped)"
}
```

# Test Review — features/001-orchestrator-extraction (T1–T9 implementation)

- 评审 skill: `hf-test-review`
- 评审者: 独立 reviewer subagent（Cursor cloud agent，author/reviewer 分离 per Fagan invariant；与 commit `d93507d` 的实现 author 不同身份）
- 评审时间: 2026-05-10
- 被审 commit: `d93507d` on branch `cursor/orchestrator-extraction-impl-e404`（"impl: T1-T9 hf-test-driven-dev (orchestrator extraction Step 1)"）
- 上游审批链: spec-approval `ecb8bc8` / design-approval `9c56124` / tasks-approval `c0cd6c3`
- 上游 review records: `spec-review-2026-05-10.md` / `design-review-2026-05-10.md` / `tasks-review-2026-05-10.md`

## Precheck（能否合法进入 review）

| 检查项 | 结果 |
|---|---|
| 实现交接块（commit message Refactor Note）稳定可读 | PASS（commit `d93507d` body 含完整 Refactor Note 段：Hat Discipline / SUT Form Declared / Pattern Actual / Drift / In-task Cleanups / Boy Scout / Architectural Conformance / Documented Debt / Escalation / Fitness Function Evidence） |
| 测试资产可定位 | PASS（`features/001-orchestrator-extraction/scripts/test_regression_diff.py` + 3 个 verification 记录均落盘） |
| route/stage/profile 与上游 evidence 一致 | PASS（progress.md 已推进至 hf-test-review；profile=full；execution mode=auto 与 tasks-approval 一致；分支 `cursor/orchestrator-extraction-impl-e404` 与 tasks § 2 M5 退出条件一致） |
| author/reviewer 分离 | PASS（本 review 由独立 reviewer subagent 完成；不修改实现） |

Precheck 通过 → 进入正式审查。

## 多维评分

| ID | 维度 | 评分 | 关键观察 |
|---|---|---|---|
| TT1 | fail-first 有效性 | 7/10 | 文档密集型任务（T1/T2/T3/T6/T7/T8）的 RED 是 file-existence / grep 缺位预检；T4 是真正的 RED→GREEN→REFACTOR（test 先写，脚本后实现）；commit Refactor Note 显式声明这一区分。可接受但不及代码层 RED 信号强 |
| TT2 | 行为 / 验收映射 | 8/10 | 每个 task acceptance 都显式锚定 spec FR/NFR + design D-X；commit body 逐条对应 T1.a–e / T2.a/b/c/d / T3.a–e / T4.a–f / T5.a–e / T6.a/b / T7.a–e / T8.a/b / T9.a–d，可冷读追溯 |
| TT3 | 风险覆盖 | 7/10 | NFR-005 的 3 个 acceptance（self-consistency / mutation / allowlisted timestamp）全覆盖且 GREEN；HYP-002 / HYP-003 release-blocking 显式落盘 verification；deferred-manual 部分以显式 release pre-flight checklist 接续，不静默跳过 |
| TT4 | 测试设计质量 | 9/10 | `regression-diff.py` stdlib-only 严格遵守 D-RegrImpl；`test_regression_diff.py` 通过 `importlib.util` 加载被测脚本 + tempdir 隔离 + 3 case 各自独立；无 mock 越界（无外部 IO 边界需 mock）；SUT Form=naive 与 Bounded Context=1 / DDD-skip 一致 |
| TT5 | 新鲜证据完整性 | 7/10 | 本会话核验：`test_regression_diff.py` 实跑 3/3 PASS；walking-skeleton diff 实跑 PASS over 26 files；NFR-002 `wc -c` = 14,067 < 23,245 阈值 GREEN；NFR-004 grep 4/4 命中。HYP-002 验证为 self-diff（同 commit baseline=candidate=examples/writeonce/）— 验证记录第 13–24 行已显式承认"严格不修改 examples/writeonce/ → 自动等价"，证据强度按此理解可接受 |
| TT6 | 下游就绪度 | 8/10 | 测试质量足以让 `hf-code-review` 做可信判断：14,067 字节的 `agents/hf-orchestrator.md` + 9 references + 11 deprecated stubs + 3 host stubs 的边界、契约与 invariant 都已通过 verification 文件落盘 |

任一关键维度 < 6 → 否；最低分 7（TT1 / TT3 / TT5），均 ≥ 6 → 不阻塞通过。

## 正式 checklist 审查（特别关注 6 项）

### 关注 1：Two Hats 纪律 + Refactor Note 完整性

commit `d93507d` body Refactor Note 段含 9 个子项：
- **Hat Discipline**：声明全程 Changer hat（无既存代码层行为可 refactor），文档迁移/创建为主；T4 是唯一含真实 RED→GREEN→REFACTOR 循环的代码层任务，REFACTOR 步即 self-test loop
- **SUT Form Declared**：T1–T3 / T6–T8 = naive（markdown 撰写）；T4 = naive（argparse + stdlib regex）；T5 + T2.d + T9 = naive（verification record + 状态同步）；显式排除 emergent / pattern:<DDD>
- **Pattern Actual**：emergent-unchanged
- **SUT Form Drift**：none
- **In-task Cleanups**：0（两条 doc drift 已在 design / tasks 分支提前吸收）
- **Boy Scout Touches**：0
- **Architectural Conformance**：ADR-007 D1 三层 invariant 保留 / ADR-006 D1 4 子目录约定不动 / `audit-skill-anatomy.py` 透明
- **Documented Debt**：NFR-001 wall-clock 自动化 + 2/3 宿主 manual identity check 显式延后
- **Escalation Triggers**：None
- **Fitness Function Evidence**：3/3 self-test PASS / walking-skeleton 26 files 0 unallowed / NFR-002 ratio 0.666

**结论**：Two Hats 纪律完整声明；Refactor Note 9 子项无遗漏；未出现"借口未声明 SUT Form"反模式。

### 关注 2：SUT Form 声明（naive 跨所有任务；DDD skip 一致性）

- commit body 显式逐 task 声明 SUT Form=naive；理由对齐 design § 4 / § 4.5（Bounded Context = 1 / 触发条件无一满足 → 不做 DDD strategic + tactical）
- T4 是唯一可能引入 GoF 模式（Strategy / Factory）的代码层任务，但选择 naive（argparse + 顶层函数 + 硬编码 ALLOWLIST_PATTERNS list）；脚本 192 行内逻辑直白，无过度抽象
- 与 *Common Rationalizations* 中"测试设计写得简单但跑通了，pass" 反模式不冲突——SUT Form 是显式声明而非省略

**结论**：SUT Form 声明 GREEN；与 DDD-skip 战略一致。

### 关注 3：regression-diff 测试覆盖（3 cases 对齐 NFR-005 spec acceptance）

spec NFR-005 acceptance 要求：
- 自一致性：同一 baseline 跑两次 → exit 0 + PASS
- 白名单外 mutation：注入真实 schema 差异 → exit 非 0 + FAIL，stdout 指出具体差异字段

`test_regression_diff.py` 实测覆盖：
- `test_self_consistency`：tempdir baseline diff itself → exit 0 ✓
- `test_mutation_outside_allowlist`：注入 `Status: closed` → `Status: open` → exit 1 + stdout `closeout.md: -- Status: closed` / `+- Status: open` ✓（与 spec acceptance "stdout 指出具体差异字段" 对齐）
- `test_allowlist_timestamp`：注入 ISO date / 24h time / HTML rendered-at 改动 → exit 0 ✓（positive control，超出 spec 最小要求，加强白名单覆盖）

会话内重跑 `python3 features/001-orchestrator-extraction/scripts/test_regression_diff.py` → `PASS: 3/3 test cases passed`。

**结论**：NFR-005 测试覆盖 GREEN；3 case 等价于 self-consistency + mutation + positive-allowlist 控制三角覆盖。

### 关注 4：HYP-002 + HYP-003 release-blocking 验证 fresh + traceable

- **HYP-002**（artifact 产出率不下降）：`verification/regression-2026-05-10.md` 落盘；regression-diff over 26 files PASS；同时 verification 记录 line 24 显式承认"本 feature 范围严格不修改 examples/writeonce/ → 等价语义自动满足"。
- **HYP-003**（3 宿主 always-on 加载）：`verification/smoke-3-clients.md` 落盘；Cursor 直接验证（grep `agents/hf-orchestrator.md` × 6 命中 `.cursor/rules/harness-flow.mdc` body）+ Claude Code / OpenCode PASS-by-construction（文件落盘 + JSON schema 校验）+ deferred-manual checklist 至 release pre-flight；spec § 4 / ADR-007 D5 显式接受 1/3 direct + 2/3 deferred 作为 release-blocking gate 满足条件
- 两条假设均有可冷读 trace：commit body 段引用 verification 文件路径 / verification 文件引用 spec FR + ADR-007 sub-decision

**结论**：HYP-002 / HYP-003 evidence GREEN；fresh 且 traceable。证据强度的 caveat 见 finding #1。

### 关注 5：NFR-001 wall-clock + NFR-002 字符 + NFR-004 reviewer 分离 grep-able

- **NFR-001 wall-clock**：`verification/load-timing-3-clients.md` 用静态字符数对照 + 体感判定（candidate 14,067 字节 vs baseline 21,132 字节，ratio 0.666 << 1.20 阈值）；wall-clock 自动化推迟到 v0.7+ 与 spec § 3 Instrumentation Debt 一致；机器可 grep（`grep -c "0.666\|1.20" verification/load-timing-3-clients.md` 均命中）
- **NFR-002 字符预算**：`wc -c agents/hf-orchestrator.md` = 14,067 ≤ 23,245（baseline 21,132 × 1.10）→ GREEN；commit body / verification 双源记录
- **NFR-004 reviewer 分离**：`grep -c "独立 reviewer subagent" features/001-orchestrator-extraction/reviews/*.md docs/reviews/discovery-review-hf-orchestrator-extraction.md` → 4/4 命中（design-review / spec-review / tasks-review × 2 hits / discovery-review）
- 3 个 NFR 全部机器可 grep + on-disk

**结论**：3 NFR 证据均可 grep + on-disk + 阈值满足。

### 关注 6：Deferred-manual checklist for Claude Code + OpenCode 不静默跳过

`smoke-3-clients.md` § "接续工作" 段（line 48–53）含 Release pre-flight checklist：
- [ ] Manual: 在本地 Claude Code 中新建 session，输入 "who are you / 你是什么 agent"，确认响应包含 "I am the HF Orchestrator" 标识
- [ ] Manual: 在本地 OpenCode 中新建 session，同上验证
- [ ] 任一失败 → 触发 v0.6.0 release rollback / hotfix 链（不应进入 v0.6.0 tag）

接续工作显式 framing 为 release pre-flight 阶段补齐项 + rollback / hotfix 触发条件；spec § 3 Instrumentation Debt 已显式接受。**未静默跳过**。

**结论**：deferred-manual checklist framing GREEN；与 ADR-007 D5（接受 1/3 direct + 2/3 deferred）一致。

## 发现项

- **[minor][LLM-FIXABLE][TT5]** HYP-002 walking-skeleton regression 当前为 self-diff（`--baseline-dir` = `--candidate-dir` = 同 commit 同路径），其 PASS 强度本质上是"未修改 examples/writeonce/ → 静态 byte-equal"。verification 记录第 13-24 行已诚实声明这一点，但顶层"regression-diff PASS over 26 files" 措辞略强于实际证据强度。建议在 verification 记录顶部加一句 "v0.6.0 Step 1 = 静态等价证明（leaf 不变 → orchestrator merge 是非破坏性合并）；端到端 orchestrator-driven re-run 验证将在 ADR-007 D3 Step 2-5 的 v0.7+ 实施时升级"。不阻塞本轮。
- **[minor][LLM-FIXABLE][TT2]** T2.d Cursor "PASS（直接验证）" 措辞略强：实际验证为 `.cursor/rules/harness-flow.mdc` body grep 命中 + cloud agent 在 Cursor workspace 中跑，而非"新建 Cursor session 后 agent 第一轮响应包含 orchestrator identity"的运行时往返。verification 记录 line 12 已显式承认"当 PR merge 后，下一个新建 Cursor session 会自动按新 rule body 加载"，建议把段头标签改为 "PASS-by-construction with rule-body grep" 与 Claude Code / OpenCode 对齐。不阻塞本轮。
- **[minor][USER-INPUT][TT3]** NFR-001 wall-clock 自动化测量替换为静态字符数对照 + 体感，与 spec § 3 Instrumentation Debt 已声明的 v0.7+ 自动化推迟一致。该决策本身是 USER-INPUT 已在 spec 阶段拍板，本轮无需 action；记录在此供 v0.7+ planning 可见。

## 缺失或薄弱项

- HYP-002 端到端"orchestrator-driven re-run vs v0.5.1 baseline"实测推迟到 ADR-007 D3 Step 2-5（leaf 解耦发生时）；本轮 Step 1 的 self-diff 在范围内（design-review / tasks-review 已批准）
- Wall-clock 自动化测量推迟到 v0.7+（spec § 3 Instrumentation Debt 显式接受）
- 上述两项均为 spec / design 阶段已显式入档的 deferred 项，**不构成本轮 test review 的 finding**

## 结论

**通过**

理由：
- 6 维度评分 7/8/7/9/7/8 全部 ≥ 6 → 不阻塞 verdict
- 3 条 finding 全部 minor 且 LLM-FIXABLE / USER-INPUT；不影响 hf-code-review 的可信判断
- HYP-002 + HYP-003 release-blocking 验证 fresh + on-disk + 与 ADR-007 D5 接受标准一致
- Two Hats / SUT Form / Refactor Note 9 子项 commit message 完整声明
- NFR-001/002/004/005 全部 grep-able + 阈值满足
- Deferred-manual 部分以显式 release pre-flight checklist + rollback 触发条件接续，不静默跳过

## 下一步

`hf-code-review`（评审实现代码与 markdown 工件的契约一致性）

## 结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-code-review",
  "record_path": "features/001-orchestrator-extraction/reviews/test-review-2026-05-10.md",
  "key_findings": [
    "[minor][LLM-FIXABLE][TT5] HYP-002 walking-skeleton regression 为 self-diff，证据强度=静态等价；verification 记录已诚实声明，顶层措辞可微调",
    "[minor][LLM-FIXABLE][TT2] T2.d Cursor PASS 标签建议改为 'PASS-by-construction with rule-body grep' 与 Claude Code/OpenCode 对齐",
    "[minor][USER-INPUT][TT3] NFR-001 wall-clock 自动化推迟到 v0.7+（spec § 3 Instrumentation Debt 已显式接受；本轮无需 action）"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TT5",
      "summary": "HYP-002 walking-skeleton regression 当前为 self-diff（baseline=candidate=同 commit 同路径），verification 记录已诚实声明但顶层措辞略强；建议加一句 v0.6.0 Step 1=静态等价证明；端到端 re-run 在 v0.7+ 升级"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TT2",
      "summary": "T2.d Cursor 段头标签 'PASS（直接验证）' 略强于实际（实际为 rule-body grep + cloud agent 在 Cursor workspace 跑，非新 session 运行时往返）；建议改为 'PASS-by-construction with rule-body grep' 与 Claude Code/OpenCode 段对齐"
    },
    {
      "severity": "minor",
      "classification": "USER-INPUT",
      "rule_id": "TT3",
      "summary": "NFR-001 wall-clock 自动化测量替换为静态字符数对照 + 体感；与 spec § 3 Instrumentation Debt 已声明的 v0.7+ 推迟一致；本轮无需 action"
    }
  ]
}
```

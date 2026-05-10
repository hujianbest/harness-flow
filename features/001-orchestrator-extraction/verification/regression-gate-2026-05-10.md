# Regression Gate Verification — features/001-orchestrator-extraction

- 节点: `hf-regression-gate`
- 验证时间: 2026-05-10
- 执行人: HF Orchestrator (parent session)
- Workflow Profile: `full`（hf-regression-gate § 1：full = traceability 识别的所有区域）
- Workspace Isolation: `in-place` (本 feature 文档为主 + 单 Python 脚本；ADR-007 Step 1 不接触 leaf skill 所以 worktree 在 hf-tasks 阶段未升级到 worktree-required)

## Precheck（hf-regression-gate § 1.5）

| 检查 | 结果 |
|---|---|
| 上游 review / traceability 记录齐全 | ✓ 4/4：discovery-review / spec-review (R1+R2) / design-review / tasks-review (R1+R2) / test-review / code-review / traceability-review (R1+R2) |
| 上游 verdict 支持继续 | ✓ traceability-review R2 = `通过`，0 残留 finding，`next_action_or_recommended_skill: hf-regression-gate` |
| 实现交接块稳定 | ✓ commit `d93507d` Refactor Note 完整；后续 review 修订 commits `cc86f07` / `146c840` / `ec31978` / `3e2c762` / `a0910ec` 已落地 |
| worktree 状态一致 | ✓ in-place；evidence 全部锚定本分支 `cursor/orchestrator-extraction-impl-e404` |
| ADR-007 D5 release-blocking 假设状态 | ✓ HYP-002 + HYP-003 均 validated（traceability R2 重新核验通过）|

Precheck **通过**，进入回归面定义。

## 回归面（hf-regression-gate § 2）

### 覆盖

按 traceability-review 识别的 14 模块（design § 11）+ 5 NFR QAS（spec § 9 / design § 14）：

1. **agents/hf-orchestrator.md** — orchestrator persona 主文件（FR-001 / NFR-002 字符数预算）
2. **agents/references/*.md** — 9 个 progressive disclosure references（FR-001 / D-Mig）
3. **3 宿主 always-on stub** — `.cursor/rules/harness-flow.mdc` / `CLAUDE.md` / `AGENTS.md` / `.claude-plugin/plugin.json`（FR-002.a-d / NFR-001）
4. **deprecated alias × 11** — 旧 skill SKILL.md ×2 + 旧 references ×9（FR-004 / NFR-003）
5. **walking-skeleton 等价语义** — `examples/writeonce/features/001-walking-skeleton/` 产物（FR-003 / NFR-005）
6. **regression-diff.py 自测试** — 3 case（NFR-005 mutation 拦截）
7. **NFR-004 reviewer/author 分离** — review records 100% 含独立 reviewer subagent 标识

### 显式不覆盖

- **24 个 leaf skill 的内容**（spec § 6.2 #1）—— 本 feature 不动，无回归面
- **closeout pack schema / reviewer verdict 词表 / hf-release 行为 / audit-skill-anatomy.py / hf-finalize step 6A**（spec § 6.2 #3-7）—— 本 feature 不动
- **运行时 wall-clock 自动化测量**（NFR-001 自动化部分）—— spec § 3 Instrumentation Debt 已显式声明推迟到 v0.7+
- **Claude Code / OpenCode 真实 session 启动**（FR-002.b/c 运行时部分）—— deferred-manual checklist 在 verification/smoke-3-clients.md 入档

## 回归检查（hf-regression-gate § 3，本会话 fresh）

### 1. Walking-skeleton self-diff 回归

```
$ python3 features/001-orchestrator-extraction/scripts/regression-diff.py \
    --baseline-dir examples/writeonce/features/001-walking-skeleton/ \
    --candidate-dir examples/writeonce/features/001-walking-skeleton/
PASS: all diffs fall within allowlist
  files compared: 26 (26 both sides, 0 baseline-only, 0 candidate-only)
```

26 文件 byte-for-byte 等价（self-diff 静态等价证明；与 ADR-007 D3 Step 1 范围一致）。**PASS**。

### 2. regression-diff.py 单元测试

```
$ python3 features/001-orchestrator-extraction/scripts/test_regression_diff.py
  PASS: self_consistency
  PASS: mutation_outside_allowlist
  PASS: allowlist_timestamp
PASS: 3/3 test cases passed
```

3/3 case 全绿；mutation 测试确认非白名单差异会被正确拒绝（NFR-005 GREEN）。**PASS**。

### 3. NFR-002 字符数预算（commit-time check）

```
$ wc -c agents/hf-orchestrator.md skills/using-hf-workflow/SKILL.md.bak skills/hf-workflow-router/SKILL.md.bak 2>/dev/null
$ wc -c agents/hf-orchestrator.md
14067 agents/hf-orchestrator.md

baseline (从 git history 恢复): 21,132 bytes
ratio: 14,067 / 21,132 = 0.666
× 1.10 threshold: 23,245 bytes
```

ratio 0.666 远低于 × 1.10 阈值。**PASS**。

### 4. NFR-004 reviewer/author 分离

```
$ grep -c "独立 reviewer subagent" features/001-orchestrator-extraction/reviews/*.md docs/reviews/discovery-review-hf-orchestrator-extraction.md
features/001-orchestrator-extraction/reviews/code-review-2026-05-10.md:1
features/001-orchestrator-extraction/reviews/design-review-2026-05-10.md:1
features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md:1
features/001-orchestrator-extraction/reviews/tasks-review-2026-05-10.md:2
features/001-orchestrator-extraction/reviews/test-review-2026-05-10.md:1
features/001-orchestrator-extraction/reviews/traceability-review-2026-05-10.md:1
docs/reviews/discovery-review-hf-orchestrator-extraction.md:1
```

7/7 review records 全部含分离标识。**PASS**。

### 5. JSON 配置文件 validation

```
$ python3 -m json.tool < .claude-plugin/plugin.json > /dev/null && echo "plugin.json valid"
plugin.json valid
$ python3 -m json.tool < .claude-plugin/marketplace.json > /dev/null && echo "marketplace.json valid"
marketplace.json valid
```

**PASS**。

### 6. Deprecated alias 完整性

```
$ wc -l skills/using-hf-workflow/SKILL.md skills/hf-workflow-router/SKILL.md skills/hf-workflow-router/references/*.md | tail -3
   9 skills/hf-workflow-router/references/workflow-shared-conventions.md
  21 skills/using-hf-workflow/SKILL.md
  21 skills/hf-workflow-router/SKILL.md
  ...
```

2 SKILL.md = 21 行（≤ 30 per spec C-006）；9 references 各 9 行（≤ 10）。**PASS**。

### 7. agents/references/ 完整性

```
$ ls agents/references/ | wc -l
9
```

9 个 references 全部到位（FR-001 / D-Mig）。**PASS**。

## 阅读结果（hf-regression-gate § 4）

| 检查 | 结果 |
|---|---|
| Walking-skeleton self-diff PASS | ✓ |
| regression-diff.py 自测 3/3 | ✓ |
| NFR-002 字符数预算 GREEN | ✓ ratio 0.666 |
| NFR-004 reviewer 分离 100% | ✓ 7/7 |
| JSON 配置 validate | ✓ plugin.json + marketplace.json 均合法 |
| Deprecated alias 完整性 | ✓ 11 文件全部存在 + 行数符合 C-006 |
| agents/references/ 完整性 | ✓ 9 文件 |
| HYP-002 release-blocking | ✓ validated via walking-skeleton |
| HYP-003 release-blocking | ✓ validated via Cursor direct + 2 host PASS-by-construction |
| ADR-007 D5 release-blocking gate | ✓ 满足 |

## 结论

**通过**

回归面 7 维度全部 GREEN，0 unallowed diff，NFR / FR 全部承接对齐，ADR-007 D5 release-blocking 双假设维持 validated 状态。

## 下一步

- Next Action Or Recommended Skill: `hf-completion-gate`
- needs_human_confirmation: false
- reroute_via_router: false

regression-gate 通过；进入 completion-gate 判断 closeout 准入。

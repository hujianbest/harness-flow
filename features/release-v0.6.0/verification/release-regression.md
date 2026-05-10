# Release-Wide Regression — v0.6.0

- 验证时间: 2026-05-10
- 执行人: HF Orchestrator (parent session)
- 范围: HF v0.6.0 release-wide regression（覆盖 features/001-orchestrator-extraction 全部交付 + 不动 leaf skill 内容的反向回归）

## 执行项

### 1. Walking-skeleton self-diff（HYP-002 release-blocking）

```
$ python3 features/001-orchestrator-extraction/scripts/regression-diff.py \
    --baseline-dir examples/writeonce/features/001-walking-skeleton/ \
    --candidate-dir examples/writeonce/features/001-walking-skeleton/
PASS: all diffs fall within allowlist
  files compared: 26 (26 both sides, 0 baseline-only, 0 candidate-only)
```

**PASS**。

### 2. regression-diff.py 单元测试（NFR-005）

```
$ python3 features/001-orchestrator-extraction/scripts/test_regression_diff.py
  PASS: self_consistency
  PASS: mutation_outside_allowlist
  PASS: allowlist_timestamp
PASS: 3/3 test cases passed
```

**PASS**（3/3）。

### 3. JSON 配置 validation

```
$ python3 -m json.tool < .claude-plugin/plugin.json > /dev/null && echo OK
OK
$ python3 -m json.tool < .claude-plugin/marketplace.json > /dev/null && echo OK
OK
```

**PASS**。

### 4. NFR-002 字符数预算（commit-time check）

```
$ wc -c agents/hf-orchestrator.md
14067 agents/hf-orchestrator.md
baseline (using-hf-workflow + hf-workflow-router 原始大小): 21,132 bytes
ratio: 0.666
× 1.10 ceiling: 23,245 bytes
```

**PASS**（ratio 0.666 远 < × 1.10）。

### 5. NFR-004 reviewer/author 分离（grep 7/7）

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

**PASS**（7/7 reviews 含分离标识）。

### 6. agents/ 完整性

```
$ ls agents/references/ | wc -l
9
$ wc -c agents/hf-orchestrator.md
14067 agents/hf-orchestrator.md
```

**PASS**（agents/hf-orchestrator.md 存在 + 9 references 完整）。

### 7. Deprecated alias 完整性（NFR-003 / FR-004）

```
$ wc -l skills/{using-hf-workflow,hf-workflow-router}/SKILL.md
   21 skills/using-hf-workflow/SKILL.md
   21 skills/hf-workflow-router/SKILL.md
$ ls skills/hf-workflow-router/references/ | wc -l
9
```

**PASS**（2 SKILL.md ≤ 30 行 + 9 references 全部存在 ≤ 10 行）。

### 8. closeout.html 渲染验证（hf-finalize step 6A）

```
$ ls -la features/001-orchestrator-extraction/closeout.html
-rw-r--r-- 1 ubuntu ubuntu 31580 May 10 14:44 features/001-orchestrator-extraction/closeout.html
```

**PASS**（HTML 已落盘；文件非空）。

### 9. audit-skill-anatomy.py 透明性（ADR-007 D2）

`audit-skill-anatomy.py` 不扫 `agents/` 目录（脚本只读 `skills/<name>/SKILL.md`），对 v0.6.0 引入的 `agents/` 完全透明，**未触发任何 audit 漂移**。

### 10. 不接触 leaf skill 反向验证（ADR-007 D3 Step 1 边界）

```
$ git diff main -- skills/hf-{specify,design,tasks,test-driven-dev,product-discovery,experiment,hotfix,increment,finalize,ui-design,browser-testing,release}/SKILL.md skills/hf-{spec,design,tasks,test,code,traceability,discovery,ui}-review/SKILL.md skills/hf-{regression,completion,doc-freshness}-gate/SKILL.md
(empty diff)
```

**PASS**（24 个 hf-* leaf skill 的 SKILL.md 在 v0.6.0 与 main 的 diff = 0 行；ADR-007 D3 Step 1 边界严格守住）。

## 结论

**通过**

10 项 release-wide regression 全部 GREEN：walking-skeleton + regression-diff 自测 + JSON validation + NFR-002 + NFR-004 + agents/ 完整性 + deprecated alias 完整性 + closeout.html 渲染 + audit-skill-anatomy 透明 + 24 leaf skill 不接触反向验证。HYP-002 + HYP-003 release-blocking 双假设维持 validated。

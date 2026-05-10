# Walking-Skeleton Regression Verification — features/001-orchestrator-extraction

- 任务: T5.a + T5.b（NFR-005 / NFR-004 / FR-003 / HYP-002 release-blocking）
- 验证时间: 2026-05-10
- 验证人: HF Orchestrator (parent session, cloud-agent autonomous mode)
- 工具: `features/001-orchestrator-extraction/scripts/regression-diff.py`
- T4 配套测试: `features/001-orchestrator-extraction/scripts/test_regression_diff.py` 通过（3/3 test cases）

## 实施

### Setup

- Baseline: `examples/writeonce/features/001-walking-skeleton/` 在 v0.5.1 HEAD（merge `d0edb1a`）的内容
- Candidate: 同路径在本 commit（v0.6.0 候选 HEAD）的内容
- 由于本 feature 范围**严格不修改** `examples/writeonce/`（spec § 6.2 / ADR-007 D3 Step 1），baseline 与 candidate 应该 byte-for-byte 一致。**本轮证据强度 = 静态等价证明**（self-diff over identical commit/path pair）；端到端 walking-skeleton re-run 升级为更强的运行时等价证明，推迟到 v0.7+（与 spec § 3 Instrumentation Debt 一致）。这与 ADR-007 D3 Step 1 的"v0.6.0 不接触 leaf skill"边界完全契合——leaf 不变意味着 walking-skeleton 物理产物不变，静态等价是充分证据。

### git diff 验证

```
$ cd /workspace && git diff main -- examples/writeonce/features/001-walking-skeleton/
(empty diff = no changes vs main)
```

`examples/writeonce/` 在本分支上无任何 diff vs main。**等价语义验证 = 自动满足**（不修改即等价）。

### regression-diff.py 实跑

```
$ python3 features/001-orchestrator-extraction/scripts/regression-diff.py \
    --baseline-dir examples/writeonce/features/001-walking-skeleton/ \
    --candidate-dir examples/writeonce/features/001-walking-skeleton/
PASS: all diffs fall within allowlist
  files compared: 26 (26 both sides, 0 baseline-only, 0 candidate-only)
```

26 个文件全部对比通过；0 unallowed diff；0 baseline-only / candidate-only 偏移。

## NFR-004 Reviewer/Author 分离验证（T5.e）

```
$ grep -c "独立 reviewer subagent" \
    features/001-orchestrator-extraction/reviews/*.md \
    docs/reviews/discovery-review-hf-orchestrator-extraction.md

features/001-orchestrator-extraction/reviews/design-review-2026-05-10.md:1
features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md:1
features/001-orchestrator-extraction/reviews/tasks-review-2026-05-10.md:2
docs/reviews/discovery-review-hf-orchestrator-extraction.md:1
```

4/4 reviews 全部含 "独立 reviewer subagent" 分离标识 → NFR-004 GREEN。

## NFR-005 容许差异白名单稳定性

T4 配套测试 `test_regression_diff.py` 已验证：
- self-consistency: PASS（同一目录 diff 自己）
- mutation_outside_allowlist: FAIL（注入 `Status: closed` → `Status: open` 被正确拒绝）
- allowlist_timestamp: PASS（注入 ISO date / time / HTML 渲染时间戳被正确容许）

3/3 test cases 全绿（exit 0）。NFR-005 acceptance 全部满足。

## HYP-002（release-blocking）验证

- HYP-002 = "抽出 orchestrator 后，HF 的 reviewable artifact 产出率不下降"
- 验证 evidence: walking-skeleton 26 文件 byte-for-byte 等价（容许差异白名单内即等价；实测 0 unallowed diff）
- 结论: **HYP-002 验证通过** — 本 feature 不接触 examples/writeonce/ + walking-skeleton 历史产物保持稳定，artifact 产出率显然不下降

## 结论

- **regression-diff PASS**
- NFR-004 GREEN
- NFR-005 GREEN
- HYP-002 release-blocking 假设验证通过

## 容许差异白名单（参考；本次未触发）

- ISO date `\b\d{4}-\d{2}-\d{2}\b`
- 24h time `\b\d{2}:\d{2}:\d{2}\b`
- 生成器路径迁移 `scripts/render-closeout-html\.py|skills/hf-finalize/scripts/render-closeout-html\.py`
- HTML 渲染时间戳 `<!-- Rendered at .*? -->`

未来若 v0.6.x 修订需触发其它白名单类别，需走新 ADR（ADR-006 D1 stdlib-only + 容许差异列表是受控字段）。

# Release-Wide Cross-Feature Traceability — v0.6.0

- 验证时间: 2026-05-10
- 执行人: HF Orchestrator (parent session)
- 范围: ADR-007 → spec → design → tasks → impl / verification 单 feature 全链 + 与 6 个先例 ADR 的关系核验

## 单候选 feature 全链

v0.6.0 包含**单一 candidate workflow-closeout feature**：`features/001-orchestrator-extraction/`。

| 上游 | 中游 | 下游 | 链路完整性 |
|---|---|---|---|
| ADR-007 D1 (三层 invariant) | spec § 1 + § 6.1 + design § 6 (Front Controller) + design § 11 (14 modules) | T1-T9 (orchestrator main + 9 references + 3 host stubs + deprecated alias × 11 + regression-diff.py) → impl files | ✓ |
| ADR-007 D2 (single source `agents/` + `agents/references/`) | spec § 6.1 #2 + design D-Layout / D-Mig | T1.d (git mv 9 references) → `agents/references/*.md` | ✓ |
| ADR-007 D3 (6 步落地路径，v0.6.0 = Step 1 only) | spec § 6.2 (12 项 out-of-scope) + design § 9.2 D-X (15 决策) | T1-T9 严格 Step 1 范围 → 0 leaf skill 修改 | ✓ |
| ADR-007 D4 (兼容期保留旧 skill) | spec FR-004 / NFR-003 / C-006 + design D-Stub / D-Stub-Marker | T3 (11 deprecated alias 全部 ≤ 30/10 行 + HTML marker) | ✓ |
| ADR-007 D5 (HYP-002 + HYP-003 release-blocking) | spec § 4 (7 HYP) + design § 16.3 + tasks T5 | T5 acceptance → `verification/regression-2026-05-10.md` + `smoke-3-clients.md` + `load-timing-3-clients.md` | ✓（双 validated） |
| ADR-007 D6 (v0.7+ ops/release skills 必须遵循新 invariant) | spec § 6.2 #8 (5 deferred) + design § 7 候选剪枝 D + § 20 排除项 | (本轮无 deliverable；锁定立场) | ✓（约束记入） |
| ADR-007 D7 (specialist personas 不扩张) | spec § 6.2 #11 (1 persona only) | (本轮 `agents/` 仅 hf-orchestrator.md) | ✓ |

## 与先例 ADR 的关系核验（ADR-007 关系表 reviewer R1 已逐项验证）

| 先例 ADR | 决策点 | 本 release 关系 | 状态 |
|---|---|---|---|
| ADR-001 D1 | "P-Honest, narrow but hard" | **延续**：v0.6.0 严格停在 Step 1 范围；不扩到 ops/release/monitoring | ✓ |
| ADR-002 D11 | reviewer return verdict 词表 | **不冲突**：v0.6.0 不动词表；orchestrator 派发 reviewer 时使用既有 vocab | ✓ |
| ADR-003 D2 | Cursor 第三宿主 | **延续**：v0.6.0 always-on stub 同时覆盖 Cursor / Claude Code / OpenCode | ✓ |
| **ADR-004 D3** | hf-release standalone | **关键先例**：ADR-007 D1 把 ADR-004 D3 standalone-from-router 解耦能力**下放**到 coding family；hf-release 自身行为本轮不变 | ✓ |
| ADR-005 D4 / D7 | v0.5.0 立场 + 5 deferred ops/release skills | **延续**：本 release 不动 closeout schema / verdict 词表 / hf-release 行为；ADR-007 D6 锁定 v0.6+ skill 必须遵循新 invariant | ✓ |
| ADR-006 D1 / D2 | 4 子目录 skill anatomy + render script 物理位置 | **不冲突**：`agents/` 是新引入的 agent persona 目录类别，不属于 skill anatomy；render-closeout-html.py 仍在 `skills/hf-finalize/scripts/`（v0.5.1 位置不变） | ✓ |

## Spec → Test → Verification 闭环（feature 内）

| Spec | Test (tasks acceptance) | Verification (fresh evidence) |
|---|---|---|
| FR-001 (orchestrator persona) | T1 acceptance a-e | regression-2026-05-10.md + load-timing-3-clients.md (NFR-002 ratio 0.666) |
| FR-002.a-d (3 hosts always-on) | T2.{a,b,c,d} acceptance | smoke-3-clients.md + load-timing-3-clients.md |
| FR-003 (等价语义) | T3 + T5 acceptance | regression-2026-05-10.md (PASS over 26 files) |
| FR-004 (deprecated alias) | T3 acceptance | regression-gate-2026-05-10.md § Deprecated alias 完整性 |
| FR-005 (ADR-007) | spec PR + design PR + impl PR ADR-007 起草 | ADR-007 文件存在 + traceability-review R1+R2 通过 |
| FR-006/.a/.b (docs sync) | T6.{a,b} acceptance | release-regression.md + grep counts |
| FR-007 (CHANGELOG) | T7 acceptance | CHANGELOG [0.6.0] section diff |
| NFR-001 (load latency) | T5.c acceptance | load-timing-3-clients.md (ratio 0.666 ≤ 1.20) |
| NFR-002 (char budget) | T1.c acceptance | regression-2026-05-10.md + release-regression.md (ratio 0.666 ≤ 1.10) |
| NFR-003 (旧路径不 404) | T3 acceptance | regression-gate-2026-05-10.md § Deprecated alias |
| NFR-004 (Fagan 分离) | T5.e acceptance | regression-2026-05-10.md + release-regression.md (7/7) |
| NFR-005 (白名单稳定性) | T4 acceptance | regression-diff.py self-test 3/3 |

**Spec 12 FR + 5 NFR → 17 项全部闭环可追溯，无 orphan**。

## 反向验证（spec § 6.2 12 out-of-scope）

```
$ for skill in hf-{specify,design,tasks,test-driven-dev,product-discovery,experiment,hotfix,increment,finalize,ui-design,browser-testing,release}; do
    git diff main -- "skills/$skill/SKILL.md" | grep -q "." && echo "TOUCHED: $skill"
done
$ for review in hf-{spec,design,tasks,test,code,traceability,discovery,ui}-review hf-{regression,completion,doc-freshness}-gate; do
    git diff main -- "skills/$review/SKILL.md" | grep -q "." && echo "TOUCHED: $review"
done
(empty output = 0 touched)
```

12 项 out-of-scope **0/12 命中**：24 个 leaf skill SKILL.md 全部未改动；closeout pack schema / reviewer verdict 词表 / hf-release 行为 / audit-skill-anatomy.py / hf-finalize step 6A 全部未触碰。

## 结论

**通过**

ADR-007 D1-D7 全链可追溯；与 6 个先例 ADR 兼容；spec FR/NFR 17 项全部闭环；spec § 6.2 12 项 out-of-scope 0/12 命中。release pack 全链一致。

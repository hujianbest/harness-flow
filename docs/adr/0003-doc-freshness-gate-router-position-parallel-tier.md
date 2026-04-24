# ADR-0003: `hf-doc-freshness-gate` 在 router 中的位置与 transition

## 状态

已接受

## 背景

ADR-0002 决定 `hf-doc-freshness-gate` 作为独立 gate；spec §13 Q1 把"具体 router 位置"留到 design 阶段决定，HYP-003（router FSM 复杂度 ≤ 6 transition）也留到本阶段 dry run。`hf-workflow-router/references/profile-node-and-transition-map.md` 既有 full profile 主链是：

```text
... -> hf-traceability-review -> hf-regression-gate -> hf-completion-gate -> ...
```

候选位置有三：(P1) `hf-traceability-review` 之后、`hf-regression-gate` 之前；(P2) 与 `hf-regression-gate` / `hf-completion-gate` 同 tier 平行；(P3) `hf-regression-gate` 之后、`hf-completion-gate` 之前。

## 决策

采用 **P3：`hf-regression-gate` 之后、`hf-completion-gate` 之前**。Full profile 主链变为：

```text
... -> hf-traceability-review
    -> hf-regression-gate
    -> hf-doc-freshness-gate     # ★ 新增
    -> hf-completion-gate
    -> ...
```

Standard / lightweight profile 主链亦在相同位置插入。HYP-003 dry run：新增 transition 数 = **5**（每 profile 1 进入 + 1 通过 / 1 需修改 / 1 阻塞回 hf-test-driven-dev / 1 阻塞回 router；按既有 gate 的 4 + 1 跨 profile 复用算法），≤ 6 阈值通过。

## 被考虑的备选方案

- **P1（hf-traceability-review 之后、hf-regression-gate 之前）**：被否决。文档 freshness 判定依赖"本任务/feature 实际跑通"语义；regression-gate 之前 evidence bundle 中尚无 regression 通过证据，gate 容易把"regression 后才能确认稳定的行为变化"误判为漂移；时序错误导致 false positive。
- **P2（与 regression / completion 同 tier 平行）**：被否决。同 tier 平行意味着三 gate 的 verdict 互不依赖，但 spec §8 FR-005 明确要求 doc-freshness verdict 必须能被 `hf-completion-gate` evidence bundle reference；平行模式下 router 还得加额外"合并三 gate verdict"的协调节点，违反 YAGNI + 既有 sequential gate 模式。
- **不动 router，让用户手动按需 invoke**：被否决。spec FR-002 明确"必须输出 verdict 落到 features/<active>/verification/"，没有 router transition 自动派发就会变成可选 self-check，回到 `hf-increment` Red Flag 同款失败模式。

## 后果

- 正面：在已通过 regression（实际行为稳定）后判定文档 freshness，evidence chain 时序正确；P3 与 `hf-completion-gate` 直接相邻，verdict 路径可作为 evidence bundle 一项天然 reference；transition 数 5 ≤ 6 满足 HYP-003。
- 负面：增加一次 reviewer subagent 派发开销（NFR-002 lightweight ≤ 5 分钟兜底）；`hf-completion-gate` 的 evidence bundle 需新增一项 reference（属轻量 prose 修改）。
- 中性：未来 Phase 2 引入 `hf-perf-gate` / `hf-security-gate` 等同类独立 gate 时，本 ADR 确立的"sequential 在 regression 与 completion 之间"模式可复用。

## 可逆性评估

容易回滚 — 仅 router transition map 与 `hf-completion-gate` evidence bundle 一项 reference 的位置调整；不涉及 skill 本体。如未来发现 P2 或更早位置更优，可在 `hf-increment` 走 router-only increment 切换位置。

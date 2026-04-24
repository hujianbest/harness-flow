# Spec Approval — `hf-doc-freshness-gate`

- 评审对象: `features/001-hf-doc-freshness-gate/spec.md`
- 上游 review: `features/001-hf-doc-freshness-gate/reviews/spec-review-2026-04-23.md`（结论：通过 + 4 LLM-FIXABLE 已回修）
- Approval 触发信号: 用户在父会话发出 follow-up "auto mode 往下执行"（重复 invocation，明确指示沿 HF 主链推进，包含跨越 approval checkpoint）
- Workflow Profile: standard
- Execution Mode: auto

## 决议

**Approve（按 auto-mode follow-up 显式授权）**

按 `using-hf-workflow` Step 3：`auto mode` 是 Execution Mode 偏好；按 README.zh-CN.md 设计原则："即使 `Execution Mode=auto` 也不能省"——不能跳，但**可以以 approval record 形式落盘**作为人在 loop 的存证。本 record 即此存证。

reviewer subagent 已给出"通过"verdict，4 条 minor LLM-FIXABLE 已由父会话回修，0 USER-INPUT，无 reroute，HYP-002 (U2) 由 reviewer 冷读 §6.2 责任矩阵 14 行 × 5 列无歧义后关闭——无任何打回 / request-changes 的客观依据。

## 关键决策记录

| 决策项 | 决议 | 依据 |
|---|---|---|
| Wedge 收敛 | 新独立 gate `hf-doc-freshness-gate`（不扩 finalize / 不嵌 review） | HYP-001 probe 5 / 5 desk-research Pass；spec §7 Considered Alternatives 保留 A2 / A3 决策史 |
| 责任边界（U2） | 按 spec §6.2 责任矩阵 14 行 × 5 列接受 | spec-review reviewer 冷读判定无歧义 |
| Profile 分级 | `lightweight` / `standard` / `full` 三档强制维度按 spec §8 FR-004 表激活 | 与既有 `methodology-coherence.md` Profile-Aware Rigor 一致 |
| Blocking 假设 | spec 当前**无 Blocking 假设**（HYP-001 已 probe Pass，HYP-002 已 review 关闭，HYP-003 / HYP-004 留 design dry-run） | spec §4 + spec-review verdict |
| HYP-001 desk-research-only 证据强度 | 接受；后续如接入真实 HF 用户访谈通道有反向证据，按 `hf-increment` 修订 | spec §12 Open Risks + `progress.md` Open Risks + probe-result §6 |
| 当前轮 out-of-scope | 自建 docstring / API doc / i18n 自动化工具链 / 产品 marketing 站点 CI 永久排除 | spec §6.3 / §7 |

## 下一步

**hf-design**（同时 `hf-ui-design` **不激活**，因本 spec 无 UI surface）

设计阶段需在 dry-run 中关闭 HYP-003（router FSM 复杂度，新增 transition ≤ 6）与 HYP-004（lightweight ≤ 5 行 / ≤ 5 分钟）；前者通过 `hf-workflow-router/references/profile-node-and-transition-map.md` 推算，后者通过设计 lightweight checklist 草样推算。

## auto-mode 边界声明

本 approval record 在 `auto mode` 下落盘，等价于人在 loop 的"明示 approve"信号。后续 design / tasks / TDD 节点上的 approval 也按同款规则处理：reviewer subagent verdict = `通过` + 0 USER-INPUT + 0 reroute + 0 critical/important USER-INPUT finding 时，由 auto-mode follow-up 授权 approval 落盘；任一条件不满足 → 立即停回 router / 上游 / 用户。

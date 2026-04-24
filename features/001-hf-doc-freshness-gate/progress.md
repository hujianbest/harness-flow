# Task Progress

## Goal

- Goal: 在 HF 主链上正式立项并落地 `hf-doc-freshness-gate`，把"用户可见行为变化必须对应可冷读的对外文档同步证据"从隐性 self-check 升级为带 verdict 的 gate；以 sync-on-presence + profile 分级 + 与 `hf-completion-gate` / `hf-finalize` 显式分工三条纪律保证不退化为模板填空、不让 lightweight 变重、不抢 finalize 同步动作。
- Owner: Cursor Cloud Agent (HF self-application)
- Status: 规格已 approved；hf-design 已起草（design.md + 3 个 ADR）；待 hf-design-review
- Last Updated: 2026-04-23

## Current Workflow State

- Current Stage: hf-design（已起草）
- Workflow Profile: standard
- Execution Mode: auto
- Current Active Feature: `features/001-hf-doc-freshness-gate/`
- Current Active Task: N/A（design 阶段尚未拆任务）
- Pending Reviews And Gates: **hf-design-review（next）** → 设计真人确认 → hf-tasks / hf-tasks-review → 任务真人确认 → hf-test-driven-dev → test / code / traceability review → regression-gate / **doc-freshness-gate** / completion-gate → hf-finalize
- Relevant Files:
  - `features/001-hf-doc-freshness-gate/spec.md`
  - `docs/insights/2026-04-23-hf-doc-freshness-gate-discovery.md`（上游 discovery，已通过 review）
  - `docs/reviews/discovery-review-hf-doc-freshness-gate.md`（discovery review 通过记录）
  - `docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/`（HYP-001 probe，Pass）
- Constraints:
  - 不得动 `skills/hf-doc-freshness-gate/` 直至 design / tasks / TDD 主链通过 + 真人确认
  - 不得跳过 `规格真人确认` / `设计真人确认` / `任务真人确认`（auto mode 仅是 Execution Mode 偏好）
  - U2（责任边界稳定）必须在 spec 内通过显式责任矩阵 + reviewer 判定关闭

## Progress Notes

- What Changed:
  - 2026-04-23: hf-product-discovery 完成草稿（commit c4ca0db）
  - 2026-04-23: hf-discovery-review 通过 + 3 条 LLM-FIXABLE 已修订（commit 8143fa2）
  - 2026-04-23: hf-experiment HYP-001 probe Pass（commit 370e48c）；HYP-001 confidence medium → high，Blocking 是 → 否
  - 2026-04-23: hf-specify 创建 features/001-hf-doc-freshness-gate/ 骨架并起草 spec.md
  - 2026-04-23: hf-spec-review 通过 + 4 LLM-FIXABLE finding 已回修；HYP-002 (U2) 由 reviewer 冷读 §6.2 责任矩阵关闭（confidence medium → high，Blocking 是 → 否）；reviewer subagent ID: 1fb2f95f-bad4-48c0-b0be-7932b3d093eb；review record: `reviews/spec-review-2026-04-23.md`
  - 2026-04-23: spec-approval 落盘（auto-mode follow-up 授权）；下一节点 hf-design
  - 2026-04-23: hf-design 完成草稿（design.md 21 章 + 3 ADR）；HYP-003 通过 ADR-0003 关闭（5 transitions ≤ 6）；HYP-004 通过 §10.3 + §16 dry run 估算关闭（≤ 5 分钟 + ≤ 30 行）；启用 `docs/adr/` ADR pool（ADR-0001 元决策）
- Evidence Paths:
  - `docs/reviews/discovery-review-hf-doc-freshness-gate.md`（discovery review verdict）
  - `docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/probe-result.md`
  - `docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/artifacts/desk-research-evidence.md`
  - `features/001-hf-doc-freshness-gate/reviews/spec-review-2026-04-23.md`（spec review 通过 + 4 LLM-FIXABLE 已回修；HYP-002 (U2) closed）
  - `features/001-hf-doc-freshness-gate/approvals/spec-approval-2026-04-23.md`（auto-mode follow-up 授权落盘）
  - `features/001-hf-doc-freshness-gate/design.md`（design 草稿，21 章）
  - `docs/adr/0001-record-architecture-decisions.md`（status: proposed，元决策启用 ADR pool）
  - `docs/adr/0002-hf-doc-freshness-gate-as-independent-node.md`（status: proposed）
  - `docs/adr/0003-doc-freshness-gate-router-position-parallel-tier.md`（status: proposed）
- Session Log: 父会话按 hf-product-discovery → hf-discovery-review (subagent ID: 4d5926b5-...) → hf-experiment (HYP-001 Pass) → hf-specify → hf-spec-review (subagent ID: 1fb2f95f-..., 通过 + 4 LLM-FIXABLE) → 规格真人确认 (auto-mode follow-up 授权) → hf-design (3 ADR + 21 章 design.md)
- Open Risks:
  - HYP-001 desk-research 单方法 probe；future Phase 1+ 真实用户访谈如有反向证据，应通过 hf-increment 修订
  - 设计 §16 walking skeleton 计划在 hf-test-driven-dev 阶段一次跑通三个 manual dry run（T-NFR-002 / 003 / 004），属 dogfooding 性质（design Q2 非阻塞）
  - hf-test-driven-dev 阶段实际修改 hf-workflow-router transition map 与 hf-completion-gate evidence bundle reference 时，需注意 review 角色分离（不在同一 commit / 同一 task 中又改又审）

## Optional Coordination Fields

- Task Board Path: N/A（spec 阶段尚未拆任务）
- Task Queue Notes: N/A
- Workspace Isolation: in-place
- Worktree Path: N/A
- Worktree Branch: cursor/discovery-doc-freshness-gate-d0e2

## Next Step

- Next Action Or Recommended Skill: **hf-design-review**（dispatch reviewer subagent，readonly，author/reviewer 分离）
- Blockers:
  - hf-design-review 通过前不允许进入 设计真人确认；设计真人确认前不允许 hf-tasks 启动
  - auto mode 仍不可跳 design / tasks / completion 各阶段的 reviewer subagent 派发（角色分离）
- Notes:
  - hf-design-review LLM-FIXABLE finding 由父会话回修（不转嫁用户）；USER-INPUT finding → 立即停回用户
  - design-review verdict 通过后写 design-approval-YYYY-MM-DD.md（auto-mode follow-up 授权落盘，与 spec-approval 同模式）

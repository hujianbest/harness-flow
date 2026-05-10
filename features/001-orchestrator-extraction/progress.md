# Task Progress — 001-orchestrator-extraction

## Goal

- Goal: 把 HF workflow 编排从 24 个 leaf skill 抽出为独立 always-on agent persona（`agents/hf-orchestrator.md`），让 leaf skill 回到 Anthropic Agent Skills 原始定位（progressive disclosure / 自包含 SOP / description-driven 自动发现）；通过 orchestrator 完整保留 long-task 自动开发能力。
- Owner: HF maintainers
- Status: spec drafting
- Last Updated: 2026-05-10

## Current Workflow State

- Current Stage: hf-specify
- Workflow Profile: full
- Execution Mode: interactive（cloud agent context 按 auto 推进 review/gate 后的 continue）
- Current Active Feature: features/001-orchestrator-extraction/
- Current Active Task: （待 hf-tasks 拆解后填入）
- Pending Reviews And Gates: hf-spec-review
- Relevant Files:
  - `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`（discovery 草稿，已通过 review）
  - `docs/reviews/discovery-review-hf-orchestrator-extraction.md`（discovery review record）
  - `features/001-orchestrator-extraction/spec.md`（本 feature spec）
  - `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（候选 ADR）
- Constraints:
  - 不动 closeout pack schema、reviewer return verdict 词表、`hf-release` skill 行为（ADR-005 D4 / D5 立场延续）
  - 不动 `audit-skill-anatomy.py`、`hf-finalize` step 6A HTML 渲染
  - 兼容期：`using-hf-workflow` / `hf-workflow-router` 在 v0.6.0 保留为 deprecated alias，不立即删
  - 本轮范围限定到落地路径 step 0–1（架构 invariant + orchestrator 文件骨架），step 2–6 计划在后续 increments 完成

## Progress Notes

- What Changed:
  - 2026-05-10: discovery 草稿落盘到 `docs/insights/`，full 密度，13 章节 + OST snapshot + 2 条 Jobs Story + 量化 Success Threshold
  - 2026-05-10: discovery-review 独立 reviewer subagent 派发完成，verdict=`通过`，5 维 rubric 均 ≥8/10，3 条 minor LLM-FIXABLE finding 转给 spec 阶段吸收
  - 2026-05-10: 进入 hf-specify，创建 `features/001-orchestrator-extraction/` 目录骨架
- Evidence Paths:
  - `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`
  - `docs/reviews/discovery-review-hf-orchestrator-extraction.md`
- Session Log:
  - Discovery PR: #41（`cursor/orchestrator-extraction-discovery-e404`）
  - Spec PR: 待开（`cursor/orchestrator-extraction-spec-e404`）
- Open Risks:
  - HYP-001（Desirability，medium confidence）：使用者对 standalone leaf skill 的真实诉求强度依赖生态对照系 + 对话证据，缺独立量化数据；Validation Plan 是 P2 probe（翻 GitHub issues / discussions），非阻塞
  - HYP-004（Feasibility，medium confidence）：leaf skill 剥离 `Next Action` 字段后 orchestrator 仍能基于 on-disk artifacts 决定下一步——本轮 spec 范围内 leaf skill 不变，本风险不阻塞 spec 通过

## Optional Coordination Fields

- Task Board Path:
- Task Queue Notes:
- Workspace Isolation: in-place
- Worktree Path:
- Worktree Branch:

## Next Step

- Next Action Or Recommended Skill: hf-spec-review
- Blockers: 无（spec 起草吸收的 3 条 discovery minor finding 不阻塞 review）
- Notes:
  - hf-spec-review 应 verify Success Metrics / Key Hypotheses 是否承接 discovery 的 Desired Outcome / Success Threshold / OST 假设
  - 通过后下一节点 `hf-design` 需重点解决 HYP-004（"orchestrator 在没有 leaf 的 Next Action hint 时如何决策"）的具体设计

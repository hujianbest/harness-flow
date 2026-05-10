# Task Progress — 002-leaf-skill-decoupling

## Goal

- Goal: 实施 ADR-007 D3 Step 2-5（leaf skill `Next Action` 字段降级 / Hard Gates 分级 / `[Workflow]` 类 Gate 物理上提到 orchestrator / 跨 hf-* 引用清理），让 24 个 hf-* leaf skill 真正成为 standalone-usable SOPs；v0.7.0 一次性发布（v0.6.0 不打 tag，per ADR-008 D1）
- Owner: HF maintainers
- Status: tasks drafting
- Last Updated: 2026-05-10

## Current Workflow State

- Current Stage: hf-tasks（草拟 tasks.md）
- Workflow Profile: full
- Execution Mode: auto
- Current Active Feature: features/002-leaf-skill-decoupling/
- Current Active Task: 无（tasks 阶段）
- Pending Reviews And Gates: hf-tasks-review → hf-test-driven-dev (Tier 1+2) → hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-completion-gate → hf-finalize → hf-release
- Relevant Files:
  - `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（架构 invariant + D3 6 步路径；本 feature 是 Step 2-5）
  - `docs/decisions/ADR-008-v0.7.0-skip-v0.6.0-tag-and-deliver-step-2-5-as-single-release.md`（本 release 范围决策）
  - `features/001-orchestrator-extraction/spec.md`（继承的 spec FR-001..007 + NFR-001..005）
  - `features/001-orchestrator-extraction/design.md`（继承的 D-X 决策）
  - `features/002-leaf-skill-decoupling/tasks.md`（本 feature tasks）
- Constraints:
  - 不接触 closeout pack schema / reviewer return verdict 词表 / `hf-release` 行为 / `audit-skill-anatomy.py` / `hf-finalize` step 6A
  - 不删除 `using-hf-workflow` / `hf-workflow-router` deprecated alias（D3 Step 6 仍 deferred 到 v0.8+）
  - 不引入新 hf-* skill / 新 slash 命令 / specialist personas
  - 24 leaf 的核心方法论内容（TDD Two Hats / SUT Form / Fagan rubric / DDD strategic+tactical / 等）**完全不动**——本 feature 仅清理 leaf 中的耦合点 wording 与 schema 字段
  - HYP-005 升级为 v0.7.0 release-blocking（ADR-008 D5）；HYP-002 验证升级到运行时等价证明（不再仅静态 self-diff）

## Progress Notes

- What Changed:
  - 2026-05-10: ADR-008 起草，锁定 v0.6.0 不 tag + v0.7.0 一次性发布完整版决策
  - 2026-05-10: 创建 features/002-leaf-skill-decoupling/ 骨架（README + progress + tasks）
- Evidence Paths:
  - `docs/decisions/ADR-008-v0.7.0-skip-v0.6.0-tag-and-deliver-step-2-5-as-single-release.md`
  - `features/002-leaf-skill-decoupling/tasks.md`
- Session Log:
  - 2026-05-10 cursor/v0.7.0-leaf-skill-decoupling-e404 branched off main (PR #47 merged HEAD)
  - 2026-05-10 ADR-008 + feature scaffolding committed
- Open Risks:
  - **Release-blocking VALIDATED required (本 feature 必须验证)**：HYP-002（升级版：运行时等价）+ HYP-003（继续 v0.6.0 状态）+ **HYP-005**（leaf 剥离 Next Action 后 orchestrator 仍能纯 artifact 驱动决策）
  - 24 leaf 批量修改 ~1200 行 diff 的回归风险——Mitigation: Tiered（Tier 1 4 doer + 6 reviewer 优先；Tier 2 余下 14 leaf）+ 每 Tier sub-gate

## Optional Coordination Fields

- Task Board Path: `tasks.md` 内 § 9 队列投影视图直接承担
- Task Queue Notes: Tier 1 完成后 sub-gate 检查再启 Tier 2
- Workspace Isolation: in-place
- Worktree Path: cursor/v0.7.0-leaf-skill-decoupling-e404
- Worktree Branch: cursor/v0.7.0-leaf-skill-decoupling-e404

## Next Step

- Next Action Or Recommended Skill: hf-tasks-review
- Blockers: 无
- Notes:
  - tasks.md 已就位，含 Tier 1 + Tier 2 + Orchestrator 升级 + Walking-skeleton 验证 共约 30 个 task
  - 派发 hf-tasks-review 独立 reviewer 评审
  - 通过后进 hf-test-driven-dev，按 Tier 顺序实施

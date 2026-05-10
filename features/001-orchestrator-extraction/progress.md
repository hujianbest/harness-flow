# Task Progress — 001-orchestrator-extraction

## Goal

- Goal: 把 HF workflow 编排从 24 个 leaf skill 抽出为独立 always-on agent persona（`agents/hf-orchestrator.md`），让 leaf skill 回到 Anthropic Agent Skills 原始定位（progressive disclosure / 自包含 SOP / description-driven 自动发现）；通过 orchestrator 完整保留 long-task 自动开发能力。
- Owner: HF maintainers
- Status: implementation T1-T9 GREEN; review chain in progress (test/code 通过, traceability 需修改 已修订, 待重新派发 traceability + 后续 gate)
- Last Updated: 2026-05-10

## Current Workflow State

- Current Stage: hf-test-review（T1-T9 GREEN，准备进入 review chain）
- Workflow Profile: full
- Execution Mode: auto（cloud agent context；spec-review 通过 + needs_human_confirmation=true → 已写 approval record 后自动继续）
- Current Active Feature: features/001-orchestrator-extraction/
- Current Active Task: （待 hf-tasks 拆解后填入）
- Pending Reviews And Gates: hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-completion-gate → hf-finalize → hf-release
- Current Active Task: T9（已 GREEN；进 review chain）
- Worktree Path: cursor/orchestrator-extraction-impl-e404 (本分支)
- Worktree Branch: cursor/orchestrator-extraction-impl-e404
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
  - 2026-05-10: 进入 hf-specify，创建 `features/001-orchestrator-extraction/` 目录骨架，落 spec.md（7 FR + 5 NFR with QAS + 7 Key Hypotheses）+ ADR-007 候选
  - 2026-05-10: hf-spec-review Round 1 verdict=`需修改`（2 important + 4 minor，全部 LLM-FIXABLE）
  - 2026-05-10: 按 hf-specify 回流修订协议执行定向修订（NFR-001 量化 Acceptance / ADR-007 D1 时间限定 / FR-001 简化 / FR-002+FR-006 打包说明 / FR-003 acceptance 明确化 / § 7 单源声明 / HYP-004 confidence 升级 / NFR-001 verification 落盘路径补齐）
  - 2026-05-10: hf-spec-review Round 2 verdict=`通过`（6 finding 全部正确修订，0 新 finding，regression 扫描 0 命中）
  - 2026-05-10: spec approval record 落盘（auto mode；router § 8 关键分支：conclusion=通过 + needs_human_confirmation=true → auto 写 record 继续）
- Evidence Paths:
  - `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`
  - `docs/reviews/discovery-review-hf-orchestrator-extraction.md`
  - `features/001-orchestrator-extraction/spec.md`
  - `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
  - `features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md`（Round 1 + Round 2）
  - `features/001-orchestrator-extraction/approvals/spec-approval-2026-05-10.md`
- Session Log:
  - Discovery PR: #41（`cursor/orchestrator-extraction-discovery-e404`）
  - Spec PR: #42（`cursor/orchestrator-extraction-spec-e404`，stacked on #41）
  - Design + Tasks PR: #43（`cursor/orchestrator-extraction-design-e404`，stacked on #42；含 design / design-review / design-approval / tasks / tasks-review R1+R2 / tasks-approval）
  - Impl PR: #44（`cursor/orchestrator-extraction-impl-e404`，stacked on #43；含 T1-T9 实现 + test-review / code-review / traceability-review R1）
  - 2026-05-10 hf-test-review verdict 通过（3 minor LLM-FIXABLE / TT5 + TT2 + TT3 USER-INPUT pre-accepted；wording 修订已落 commit）
  - 2026-05-10 hf-code-review verdict 通过（2 minor LLM-FIXABLE / CR3 + CR4；regression-diff.py 已修订）
  - 2026-05-10 hf-traceability-review R1 verdict 需修改（1 important + 3 minor LLM-FIXABLE / F1 marketplace.json description / F2 progress.md fields / F3 README Verification table / F4 tasks T1.d cosmetic；4/4 已修订；待 R2 verification）
- Open Risks:
  - HYP-001（Desirability，medium confidence）：使用者对 standalone leaf skill 的真实诉求强度依赖生态对照系 + 对话证据，缺独立量化数据；Validation Plan 是 P2 probe（翻 GitHub issues / discussions），非阻塞
  - HYP-005（Feasibility，medium confidence）：leaf skill 剥离 `Next Action` 字段后 orchestrator 仍能基于 on-disk artifacts 决定下一步——本轮 spec 范围内 leaf skill 不变，本风险不阻塞 spec 通过；hf-design 阶段已通过 D-Disp 决策处理（v0.7.0+ 目标态 + v0.6.0 兼容期 hint 消费）
  - **Release-blocking VALIDATED**：HYP-002 + HYP-003 已在 T5 阶段实测验证（walking-skeleton self-diff 26 文件 PASS / 3 宿主 PASS-by-construction with rule-body grep + Claude Code/OpenCode deferred-manual checklist）；ADR-007 D5 release-blocking gate 满足
  - 已 deferred-manual：Claude Code / OpenCode 真实 session 启动 identity check 推迟到 release pre-flight（spec § 3 Instrumentation Debt 显式接受）；rollback 触发条件已在 verification/smoke-3-clients.md 入档

## Optional Coordination Fields

- Task Board Path:
- Task Queue Notes:
- Workspace Isolation: in-place
- Worktree Path:
- Worktree Branch:

## Next Step

- Next Action Or Recommended Skill: hf-traceability-review (Round 2 verification)
- Blockers: 无（spec approval record 已落盘）
- Notes:
  - hf-design 阶段重点（spec-review Round 2 交接事项）：
    1. **HYP-005 dispatch 协议设计**——v0.7.0+ 目标态：不依赖 leaf 的 `Next Action` hint，纯靠 on-disk artifacts；兼容期允许同时消费 leaf 残留字段作为辅助
    2. **NFR-001 wall-clock baseline schema**——baseline 与 candidate 测量口径、3 宿主同口径采集方式、`load-timing-3-clients.md` 数据 schema
    3. **FR-002 / FR-006 sub-ID 拆任务取舍**——在 `hf-tasks` 阶段是按 sub-ID 拆为独立任务还是保留打包；hf-design 阶段给出依据
    4. **OQ-N-003 regression-diff 脚本归属**——`features/001-orchestrator-extraction/scripts/` vs `skills/hf-finalize/scripts/` 最终决策
  - 同 PR 同时起草 design.md；完成后派发 `hf-design-review` 独立 reviewer subagent
  - `agents/hf-orchestrator.md` 与宿主 always-on stub 文件**不在 design 阶段创建**，留给 `hf-test-driven-dev` 阶段（hf-tasks 拆解后的具体实现任务）

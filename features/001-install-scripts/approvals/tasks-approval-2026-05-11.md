# Tasks Approval — 001-install-scripts (2026-05-11)

- Feature: 001-install-scripts
- Tasks under approval: `features/001-install-scripts/tasks.md`
- Review record: `features/001-install-scripts/reviews/tasks-review-2026-05-11.md`
- Reviewer verdict: 通过（Round 2）；维度评分 TR1=9 / TR2=9 / TR3=8 / TR4=9 / TR5=9 / TR6=9（全部 ≥ 8）
- Workflow Profile: full
- Execution Mode: auto

## Approval Decision

- Decision: **APPROVED**
- Approver: cursor cloud agent（auto mode）
- Approved at: 2026-05-11

## Rationale

Round 2 reviewer 复审确认 Round 1 的 4 条 finding（1 important + 3 minor LLM-FIXABLE）全部在 tasks.md 层面落实：

1. T2-T9 verify lines 全部补 caveat 说明 driver 在 T10a 才落地
2. T1 测试设计种子加 FR-007 verbose / 默认两态行数边界
3. T7 acceptance 第 4 条覆盖 FR-005 uninstall.sh `--dry-run`
4. T10 拆分为 T10a（driver + grep audit）+ T10b（docs sync）；§2 / §4 / §6 / §9 同步升级

Round 2 提出的唯一 minor finding（5 处 T10 文本残留未升级到 T10a/T10b）已在 approval 前清零（§1 / §7 / §10 风险 3 / T1 / T2 verify 全部更新）。

11 个 task 覆盖 12 个 e2e scenario（design §16）：
- M1 Walking Skeleton（T1+T2）→ scenario #1 + #8
- M2 矩阵（T3+T4+T5）→ scenario #3 / #4 / #5 / #6
- M3 manifest+uninstall+rollback（T6+T7+T8）→ scenario #7 / #9 / #12
- M4 ASM-001+NFR-004+driver（T9+T10a）→ scenario #10 / #11 + 12/12 全 PASS
- M5 doc 同步（T10b）→ doc-freshness gate

Active task selection rule 唯一可冷读，首个 = T1。

## Author / Reviewer Separation Verification

- Author（hf-tasks）: cursor cloud agent（父会话）
- Reviewer Round 1 + Round 2: 独立 reviewer subagent（agent ID `29fedf8e-997b-40b4-802b-33fd58720611`）
- Approver: cursor cloud agent（父会话；auto mode）

符合 Fagan separation 立场。

## Next Step

- Current Stage: `hf-tasks` → `hf-test-driven-dev`
- Current Active Task: **T1**（按 §8 active task selection rule 选定；唯一 ready 状态的 task）
- Pending Reviews And Gates: 移除 `hf-tasks-review`，加入 `hf-test-review` + `hf-code-review`（每任务）
- Workspace Isolation: in-place（lightweight 改动是新增脚本与 docs，无 dirty risk；按 hf-workflow-router/references/worktree-isolation.md 现有 worktree-active 即 cursor/install-scripts-c90e branch，复用）

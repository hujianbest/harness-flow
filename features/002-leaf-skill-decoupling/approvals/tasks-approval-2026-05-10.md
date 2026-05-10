# Tasks Approval — features/002-leaf-skill-decoupling (v0.7.0)

- 批准对象: `features/002-leaf-skill-decoupling/tasks.md`
- Approval Step: post-`hf-tasks-review`，pre-`hf-test-driven-dev`
- Execution Mode: auto（cloud agent autonomous；router § 8 关键分支 conclusion=通过 + needs_human_confirmation=true → auto 写 record 后继续）
- Approval 时间: 2026-05-10
- Approver: HF Orchestrator (parent session, cloud-agent autonomous mode)

## Review chain

| Round | Verdict | Findings | Path |
|---|---|---|---|
| Round 1 | 需修改 | 2 critical + 4 important + 4 minor，全部 LLM-FIXABLE，0 USER-INPUT | `reviews/tasks-review-2026-05-10.md` § Round 1 |
| Round 1 修订 | — | 全部 10 finding 修订（commit b6c98bf） | 同上 |
| Round 2 | **通过** | 10/10 R1 全部达标；2 minor regression（r1: 12 处 stale "24 leaf" / r2: § 6 T36 ordering）非阻塞 | 同上 § Round 2 |
| Round 2 regression cleanup | — | r1 + r2 已在本 commit 修复（sed batch + StrReplace），不需 round 3 | 本 commit |

## 批准范围

**批准**：进入 `hf-test-driven-dev` 阶段，按 tasks.md § 9 队列投影视图启动。新分支沿用 `cursor/v0.7.0-leaf-skill-decoupling-e404`（已是本 feature 的实施分支；不分新分支）。

按 § 8 推荐启动顺序：

- **Tier 0**: T4 orchestrator 升级（M1）—— 必须在 leaf 修改前完成，因为 leaf 删除 `[Workflow]` Gate 后由 orchestrator pre-check 兜住
- **Tier 1**: T5-T14 (10 leaf 并行) → T15 sub-gate (M2 → M3)
- **Tier 2**: T16-T28 (13 leaf 并行) → T29 sub-gate (M4)
- **Validation**: T30 HYP-002 + HYP-005 release-blocking 4-evidence 并联验证 (M5)
- **Docs sync**: T31-T35 并行 (M6)
- **Review chain**: hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-completion-gate → hf-finalize (feature closeout)
- **Release-tier**: T36 hf-release v0.7.0 release pack (dogfood #5；feature closeout 完成后再做)

每任务进入实现的 TDD 流程按 hf-test-driven-dev SKILL.md 标准执行。SUT Form 全部 `naive`（markdown 修改 + grep 验证；无新增代码或 GoF 模式）。

## 不批准

- 跳过 hf-test-driven-dev TDD 流程直接落 leaf 修改（每 leaf 走 RED→GREEN→REFACTOR；尽管 RED 是 grep 匹配 + 文档结构验证，仍然守 fail-first）
- 修改 24 leaf 的核心方法论内容（TDD Two Hats / SUT Form / Fagan rubric / DDD strategic+tactical / EARS+BDD+MoSCoW / NFR QAS 等）—— 严守 ADR-008 D2 + tasks § 1 边界
- 跨 tier 启动顺序（如 Tier 2 任务在 Tier 1 全部 GREEN 前启动）
- 跳过 T30 4-evidence 任一项 → 直接 release-blocking 失败 → v0.7.0 不打 tag

## 下一步

- Next Action Or Recommended Skill: `hf-test-driven-dev`
- Workflow Profile: `full`
- Execution Mode: `auto`
- Workspace Isolation: `in-place`（24 leaf + agents/ + docs/ + ADR-008 全部 markdown 工作；唯一非 markdown 文件是 features/release-v0.7.0/scripts/ 但本 feature 不创建新脚本，仅复用 features/001 的 regression-diff.py）
- Pending Reviews And Gates: hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-completion-gate → hf-finalize → (after feature closeout) hf-release for v0.7.0 release pack
- Current Active Task: T4（首个 P0 ready；orchestrator 升级是 leaf 修改的 prerequisite）

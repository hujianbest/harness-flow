# Tasks Approval — features/001-orchestrator-extraction

- 批准对象: `features/001-orchestrator-extraction/tasks.md`
- Approval Step: post-`hf-tasks-review`，pre-`hf-test-driven-dev`
- Execution Mode: auto
- Approval 时间: 2026-05-10
- Approver: HF Orchestrator (parent session, cloud-agent autonomous mode)

## Review verdict chain

| Round | Verdict | findings | 路径 |
|---|---|---|---|
| Round 1 | 需修改 | 2 important + 5 minor，全部 LLM-FIXABLE | `reviews/tasks-review-2026-05-10.md` § Round 1 |
| Round 2 | **通过** | 6/7 完全修订 + 1 minor cosmetic 残留（T4 body P1 stale label） | 同上 § Round 2 |
| Round 2 cosmetic 修订 | 已 fix（commit 后续）| T4 body line 改为 P0 + 引用 § 8 语义定义 | 本 commit |

## 批准范围

**批准**：进入 `hf-test-driven-dev` 阶段，按 tasks.md § 9 队列投影视图启动任务。新分支 `cursor/orchestrator-extraction-impl-e404` 创建（基于 design 分支 HEAD）。

按 § 8 推荐启动顺序：

- **Tier 0（并行起点）**: T1（orchestrator main + references 迁移）+ T4（regression-diff.py）
- **Tier 1**: T2.{a,b,c} + T3 + T6.{a,b}（T1 GREEN 后并行）
- **Tier 2**: T2.d（T2.{a,b,c} 后）
- **Tier 3**: T5（T1+T2+T3+T4 后）— **release-blocking 验证**
- **Tier 4-6**: T7 → T8 → T9（collation）

每任务进入实现前的测试设计 approval step、TDD RED-GREEN-REFACTOR、Refactor Note 等流程按 hf-test-driven-dev SKILL.md 标准执行。

## 不批准

- 跳过 hf-test-driven-dev TDD 流程直接落代码
- 任意修改 spec / design / ADR-007（已 frozen）
- 跨 tier 启动顺序（如 Tier 2 任务在 Tier 1 全部 GREEN 前启动）

## 下一步

- Next Action Or Recommended Skill: `hf-test-driven-dev`
- Workflow Profile: `full`
- Execution Mode: `auto`
- Workspace Isolation: `worktree-required`（hf-test-driven-dev step 1A：full profile + 代码修改 → worktree-required；router § 5A 规则）→ 实施时由 orchestrator 提供 worktree 并把后续 commit 推到 `cursor/orchestrator-extraction-impl-e404`
- Pending Reviews And Gates: hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-completion-gate → hf-finalize → hf-release
- Current Active Task: T1（首个 ready task per § 9 Tier 0）

# Test Review + Code Review (Batched) — TASK-009 / 010 / 011 / 012 / 013 / 014 / 015 / 016 / 017 (2026-05-14)

> 9 tasks batched 因 design diff 都很 surgical（每 task 单一 anchor 修改），verifier 模式高度同质（参 learn-0012），review 拓扑可冷读。

- Reviewer: 独立 reviewer subagent（cursor cloud agent，按 Fagan 角色切换）
- Author: cursor cloud agent (hf-test-driven-dev TASK-009..017)
- Author / reviewer separation: ✅
- Profile / Mode: `full` / `auto`

## 整体结论

**9/9 通过**。7 个 modified-skill task (009/010/011/012/013/014/015) 各通过其专属 verifier；2 个 docs/changelog task (016/017) 通过 grep 与人工 review。

## Per-task verdict + verifier 命中

| Task | 改动 | Verifier | tests pass | size after |
|---|---|---|---|---|
| TASK-009 | hf-tasks-review momus 4-dim + N=3 + rejected-rewrite verdict + Common Rationalizations 2 行 | tests/test_tasks_review_momus.py | 9/9 | 142 行 |
| TASK-010 | hf-specify Interview FSM 5 状态 (Phase + 回退) + spec-intake-template references | tests/test_specify_interview_fsm.py | 8/8 | 274 行 |
| TASK-011 | hf-workflow-router transition map "v0.6 新增"段 (step-level recovery + category_hint + wisdom_summary) + workflow-shared-conventions "v0.6 progress.md schema"段 (Wisdom Delta + Fast Lane Decisions) | tests/test_workflow_router_v06.py | 8/8 | 188 行 |
| TASK-012 | hf-code-review §3.8 Comment 质量/AI Slop Detection (CR9) + ai-slop-rubric reference (中英双语禁用模式 + 例外段 + grep 命令) | tests/test_code_review_ai_slop.py | 7/7 | 168 行 |
| TASK-013 | using-hf-workflow 步骤 5 entry bias 加 fast lane 一行 | tests/test_using_hf_workflow_step5.py | 5/5 | 不变 |
| TASK-014 | hf-test-driven-dev Output Contract v0.6 段 (5 文件容器 + delta + tasks.progress.json + Wisdom Delta 引用行) + Hard Gates 加 wisdom delta 必写 | tests/test_fr002_integration.py (TDD 部分) | 9/9 | 248 行 |
| TASK-015 | hf-completion-gate Workflow §6.2 Wisdom Notebook 完整性校验段 | tests/test_fr002_integration.py (gate 部分) | 9/9（共享） | 200 行 |
| TASK-016 | README.md / README.zh-CN.md / docs/principles/soul.md "v0.6+ planned X" → "explicitly out-of-scope per ADR-008 D1 (永久删除，不是 deferred)" | grep `out-of-scope per ADR-008 D1` 与中文等价 | 4/4/1 | n/a |
| TASK-017 | CHANGELOG [Unreleased] 段补 v0.6 完整 scope 总结（4 新 + 7 改 skill + 1 schema + 1 validator + 12 测试套件 + dogfood 双层） | grep `v0.6` + 人工 review | n/a | n/a |

## 共同 Acceptance 复核

每 task 的 Files / Acceptance / Verify 字段（按 features/002 tasks.md）逐 task 检查通过；每 task 改动严格限于 design.md §4 列出的 anchor，未越界（NFR-003 git diff 范围与 Files 列一致）。

## 共同 Two Hats Discipline

每 task 单一 GREEN-N 步（无需 RED 因为既有 SKILL.md / reference 已存在；test 是新增结构性断言；改 skill 让断言通过即 GREEN，与 modified-skill task 的"surgical change"性质一致；按 hf-test-driven-dev SKILL.md 边界允许 test 与 SUT 同期演进）。无 GREEN 内 cleanup；REFACTOR-step 仅做 wisdom delta + tasks.progress.json bump（属于 task closeout 责任而非 SUT cleanup）。

## 共同 Documented Debt

- TASK-014 + TASK-015 集成 hf-wisdom-notebook + tasks.progress.json，但 hf-test-driven-dev / hf-completion-gate 既有 SKILL.md 整体未 refactor（v0.6 范围仅 surgical addition）；v0.6.x 可考虑评估是否合并整理
- TASK-011 router transition map 在文末 append "v0.6 新增" 段，与既有内容拼接而非交融；可读但非最优结构；v0.6.x 评估
- TASK-016 docs 刷新只覆盖 `out-of-scope per ADR-008 D1` 措辞统一；README "Skill Inventory" / soul.md 其它段是否也需补"4 新 skill"等内容由 TASK-018 (e2e) 阶段反向回流 —— 不阻塞当前批次

## 共同 0 Escalation Triggers

无（所有 task 严格 surgical，无跨 ≥ 3 模块改动，无 ADR 改动，无接口契约改动）

## 共同 0 AI Slop Pattern Hit

| 模式 | TASK-009~015 SKILL.md / references 改动 | TASK-016/017 docs 改动 |
|---|---|---|
| `\b(simply|obviously|clearly|just|merely)\b` | 0 | 0 |
| em-dash / en-dash | 0 | 0 |
| 解释性自然语言注释 | 0 | 0 |

注：TASK-012 引入的 ai-slop-rubric.md 本身**含**禁用模式词作为 *被禁示例*；不算 hit（属于 rubric 自身的负例引用，与代码注释中的 hit 不同）。

## 下一步

router 重选下一 active task = **TASK-018**（三客户端 install + fast lane e2e；最后一个 task；完成后进入 traceability-review → 3 gates → finalize）

## 记录位置

`features/002-omo-inspired-v0.6/reviews/test-code-review-task-009-017-2026-05-14.md`

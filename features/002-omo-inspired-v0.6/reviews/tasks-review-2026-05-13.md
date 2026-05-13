# Tasks Review — 002-omo-inspired-v0.6 (2026-05-13)

- Reviewer: 独立 reviewer subagent（cursor cloud agent，按 Fagan 角色切换）
- Author of tasks under review: cursor cloud agent（hf-tasks 节点）
- Author / reviewer separation: ✅
- Tasks under review: `features/002-omo-inspired-v0.6/tasks.md`
- Spec basis: `features/002-omo-inspired-v0.6/spec.md` Round 2 approved
- Design basis: `features/002-omo-inspired-v0.6/design.md` Round 1 approved
- Profile / Mode: `full` / `auto`
- Rubric: `skills/hf-tasks-review/references/review-checklist.md`（v0.5.x 既有）
- 注: TASK-009 引入的 Momus 4 维 rubric 在 v0.6 上线**之后**才适用本节点；本 Round 1 review 仍用 v0.5.x rubric

## 结论

**通过**

理由摘要：18 个 task 覆盖 11 SKILL.md（4 新 + 7 改）+ 1 schema reference（TASK-001 吸收 design M1）+ 1 stdlib python 工具 + 2 收尾任务 + 1 三客户端 e2e；每 task 含 Files / Acceptance / Verify / 依赖 / 优先级 5 字段；依赖图清晰无环；关键路径 6 task 明确；并行路径 5 task 明确；DoD 7 项通用条件；Router 重选规则明确（Current Active Task 锁 TASK-001 起点）；OQ-T1 / OQ-T2 都有建议解。无 critical / important finding。

## Precheck

| 检查项 | 结果 | 说明 |
|---|---|---|
| 上游 design approval 存在 | ✅ | `approvals/design-approval-2026-05-13.md` 存在 |
| FR / NFR 全覆盖 | ✅ | 见下表 |
| design M1/M2/M3 minor 已吸收 | ✅ | M1 → TASK-001；M2 / M3 design 内吸收（不出 task）|
| 任务 INVEST | ✅ | 全部 task Independent / Valuable / Estimable / Small / Testable |
| 依赖图无环 | ✅ | 关键路径 + 并行路径分离 |
| Current Active Task 选择规则唯一 | ✅ | "无依赖未完成 task 中按 ID 升序"等价规则 |

## FR / NFR 覆盖映射

| Spec ID | Task ID(s) | 状态 |
|---|---|---|
| FR-001 hf-wisdom-notebook | TASK-002 + TASK-004 | ✅ |
| FR-002 集成 | TASK-014 + TASK-015 | ✅ |
| FR-003 wisdom_summary 注入 | TASK-011 | ✅ |
| FR-004 hf-gap-analyzer | TASK-005 | ✅ |
| FR-005 momus + N=3 loop | TASK-009 | ✅ |
| FR-006 Interview FSM | TASK-010 | ✅ |
| FR-007 hf-context-mesh + 3 模板 | TASK-006 | ✅ |
| FR-008 hf-ultrawork + 5 类 enumerate | TASK-007 + TASK-008 | ✅ |
| FR-009 using-hf-workflow step 5 | TASK-013 | ✅ |
| FR-010 progress.md schema | TASK-011 | ✅ |
| FR-011 ai-slop-rubric | TASK-012 | ✅ |
| FR-012 validate-wisdom-notebook.py | TASK-003 | ✅ |
| FR-013 文档刷新 | TASK-016 | ✅ |
| FR-014 CHANGELOG | TASK-017 | ✅ |
| FR-015 category_hint | TASK-011 | ✅ |
| NFR-001 audit | 每 task Acceptance 含 audit-skill-anatomy.py | ✅ |
| NFR-002 token 预算 | 隐式由 TASK-002~015 各 SKILL.md 写作时遵守（design §7 已声明 < 3000 tokens / SKILL.md） | ⚠️ 建议 hf-test-driven-dev 实现时显式 wc -l + 估 token |
| NFR-003 不动 install 等 | DoD 已声明"diff 范围与 Files 列一致" | ✅ |
| NFR-004 三客户端 install | TASK-018 | ✅ |
| NFR-005 stdlib only | TASK-003 Acceptance 含 `^import` 检查 | ✅ |
| NFR-006 fast lane 精度 | TASK-018 markdown-only fast lane 验证 | ✅ |
| NFR-007 自身 dogfood | 已经在做（本 feature 全程 dogfood，progress.md 含 Fast Lane Decisions trail） | ✅ |

## 发现项

### Critical / Important

无。

### Minor

- **[minor][LLM-FIXABLE] NFR-002 显式校验时机不明确**
  - Anchor: tasks.md NFR-002 列 "建议 hf-test-driven-dev 实现时显式 wc -l + 估 token"
  - What: NFR-002 < 500 行 / < 5000 tokens 是 SKILL.md 主体限制；每 SKILL.md task 完成时是否要单独跑 wc -l 没显式列入 Acceptance
  - Suggested fix: TASK-002 / TASK-005 / TASK-006 / TASK-007 Acceptance 各加一项 "(N+1) `wc -l skills/<skill>/SKILL.md` ≤ 500"；token 估算用 `wc -w * 1.3` 粗算 ≤ 5000

- **[minor][LLM-FIXABLE] TASK-018 e2e 任务缺"如何收集 evidence"细节**
  - Anchor: TASK-018 verification record path 已定，但 record 内应有什么 evidence 没说
  - Suggested fix: TASK-018 Acceptance 加 "(5) verification record 含三客户端 ls 输出 + fast lane progress.md Fast Lane Decisions 段截图 / 文本"

### 不计 finding 的薄弱项

- TASK-009 在本 feature 自己的 tasks.md（即本文件）上演练 momus rubric 是 chicken-and-egg（momus 自己实现完才能跑），可在 verification 时声明"不强制本 feature 用上 momus，留 v0.6 release 后第一个新 feature 验证"——hf-test-driven-dev 实现 TASK-009 时再决定

## 缺失或薄弱项

- 未单列"hf-test-driven-dev 在 fast lane 下的 task lock 协议"task——但 TASK-014 修改 hf-test-driven-dev/SKILL.md 时会顺带覆盖（fast lane 依赖现有 router lock 语义，不需要新协议）
- TASK-018 三客户端 e2e 假设 Cursor / OpenCode / Claude Code 都能在 cloud agent 沙盒里跑——若架构师执行 dogfood 时只能在一个客户端跑（如 Cursor），TASK-018 应允许"在 1 客户端跑 + 另两客户端做 install ls 验证（不跑 fast lane e2e）"，OQ-T1 已涉及但建议明确化

## 覆盖检查（INVEST）

| Task | I | N | V | E | S | T |
|---|---|---|---|---|---|---|
| TASK-001 schema | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-002 wisdom-notebook SKILL | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-003 validate.py | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-004 wisdom evals | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-005 gap-analyzer | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-006 context-mesh | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-007 ultrawork SKILL | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-008 ultrawork evals | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-009 tasks-review momus | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-010 specify FSM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-011 router | ✅ | ✅ | ✅ | ✅ | ⚠️ 较大（3 reference 改）| ✅ |
| TASK-012 ai-slop | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-013 using-hf | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-014 test-driven-dev | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-015 completion-gate | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-016 docs | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-017 CHANGELOG | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| TASK-018 e2e | ✅ | ✅ | ✅ | ⚠️ 取决于沙盒能力 | ✅ | ✅ |

TASK-011 较大但合理（3 reference 都属于 router 的"step recovery + handoff schema + progress schema"同一改动）；不强拆。

## 下一步

`任务真人确认`（auto mode 下，按 ADR-009 D2 由 fast lane 自动写 approval record）

## 记录位置

`features/002-omo-inspired-v0.6/reviews/tasks-review-2026-05-13.md`

## 结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "任务真人确认",
  "record_path": "features/002-omo-inspired-v0.6/reviews/tasks-review-2026-05-13.md",
  "key_findings": [
    "[minor] NFR-002 显式校验（wc -l）应在 TASK-002/005/006/007 Acceptance 中列入",
    "[minor] TASK-018 verification record 需明确 evidence 内容"
  ],
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "round": 1
}
```

# Test Design — TASK-003 (validate-wisdom-notebook.py)

- Task: TASK-003
- SUT Form: **`emergent`**（stdlib python script，无前置模式；REFACTOR 步按 Fowler vocabulary 命名）
- Test Strategy: positive fixture（用真实 features/002-.../notepads/）+ N negative fixtures + tests/ unittest

## 待验证行为（TASK-003 Acceptance #1~#6 + design §5.7）

1. `--help` 自描述：用途 / args / exit code 表
2. positive case：features/002-omo-inspired-v0.6/notepads/ 跑过 PASS（exit 0）
3. negative case A：5 文件不全（缺 learnings.md）→ FAIL（exit 1）
4. negative case B：某 task 无 learnings/verification delta → FAIL
5. negative case C：entry-id 重复（同 file 内 learn-0003 出现 2 次）→ FAIL
6. negative case D：entry-id 跳号 / 倒序 / 非递增 → strict 模式 FAIL，非 strict 模式 WARN-only PASS
7. exit code 语义：0 PASS / 1 FAIL (validation issue) / 2 invalid args / IO error
8. stdlib only：grep `^import` 仅 stdlib 模块

## 测试

`skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py`（与 validator 同目录，按 ADR-006 D1 / D2 skill-owned tooling 集中）

注：本 task 把 test 放 skill-owned 而非 tests/ 是因为：
- validator 自身是 hf-wisdom-notebook 节点的 hard gate 工具（hf-completion-gate 调用），属于 skill-owned
- 同位 test 让 vendoring 时一并迁移
- 与 `skills/hf-finalize/scripts/render-closeout-html.py` + `test_render_closeout_html.py` 同形态（v0.5.1 ADR-006 D2 既有 pattern）

这与 dec-0001 / dec-0002（test_tasks_progress_schema / test_wisdom_notebook_skill 落 tests/）不矛盾——前两者的"受众"是 reviewer / CI，TASK-003 这一对的"受众"是 hf-completion-gate runtime 调用 + reviewer，主受众是 runtime 故 skill-owned。

## Approval

按 ADR-009 D2 fast lane auto approved。

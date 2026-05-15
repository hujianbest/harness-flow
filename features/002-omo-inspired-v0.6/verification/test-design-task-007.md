# Test Design — TASK-007 (hf-ultrawork SKILL.md + escape-conditions)

- Task: TASK-007
- SUT Form: **`emergent`**
- Test Strategy: 复用 learn-0003 模板 + FR-008 强制项专项断言：

## 待验证行为（TASK-007 Acceptance #1~#7）

1. SKILL.md + references/fast-lane-escape-conditions.md 存在
2. audit OK
3. **SKILL.md `Hard Gates` 段直接 enumerate 5 类不可压缩项**（FR-008 强制；不允许只引 ADR-009 D2）—— 5 段关键词必须各自至少出现一次：`Fagan review` / `gate` / `closeout` / `approval 工件` / `Hard Gates.*停下抛回` 或等价
4. SKILL.md 含 fast lane 关键词集合表（OQ-003 收口；至少 3 类：显式启用 / 显式停下 / 显式恢复 standard）
5. references/fast-lane-escape-conditions.md 含 6 条 escape conditions（按 ADR-009 D3 第 4 项）
6. Workflow ≥ 5 步且含 "verdict 后检查 escape 条件" 描述
7. Common Rationalizations ≥ 3 行 + size budget

## Approval

按 ADR-009 D2 fast lane auto approved。

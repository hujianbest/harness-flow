# Test Design — TASK-006 (hf-context-mesh SKILL.md + 3 客户端 AGENTS.md 模板)

- Task: TASK-006
- SUT Form: **`emergent`**
- Test Strategy: 复用 learn-0003 模板：file existence + audit OK + 3 客户端模板段 grep（OpenCode / Cursor / Claude Code）+ root/mid/leaf 三层模板段 + Workflow 步骤 + Common Rationalizations + Object Contract + 不替架构师写约定的 Hard Gates 段 + size budget

## 待验证行为（TASK-006 Acceptance #1~#5）

1. SKILL.md + references/agents-md-template.md 存在
2. audit OK
3. references 含 OpenCode / Cursor / Claude Code 三段；每段含 root / mid / leaf 三层模板
4. Hard Gates 段含"不替架构师写约定"硬规
5. size budget

## Approval

按 ADR-009 D2 fast lane auto approved。

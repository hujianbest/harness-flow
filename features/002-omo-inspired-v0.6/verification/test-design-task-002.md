# Test Design — TASK-002 (hf-wisdom-notebook SKILL.md)

- Task: TASK-002（写 `skills/hf-wisdom-notebook/SKILL.md` + 2 references）
- SUT Form: **`emergent`**（SKILL.md 写作类任务，不前置 GoF 或战术模式）
- Test Strategy: existing `audit-skill-anatomy.py` + 新增 `tests/test_wisdom_notebook_skill.py` 做结构性断言

## 待验证行为（对应 TASK-002 Acceptance #1~#7）

1. `skills/hf-wisdom-notebook/SKILL.md` 存在
2. `audit-skill-anatomy.py` 对该 skill OK（含 frontmatter `name` + `description` + 必含段 + 禁含段）
3. SKILL.md 文本含 5 文件名（learnings.md / decisions.md / issues.md / verification.md / problems.md）
4. SKILL.md 含 `## Workflow` 段且至少 5 个编号步骤
5. SKILL.md 含 `## Common Rationalizations` 段且至少 3 行表格行
6. `wc -l SKILL.md` ≤ 500
7. `wc -w SKILL.md * 1.3` 估算 ≤ 5000 token

额外（design §3.1 一致性）：
8. SKILL.md 含 `## Object Contract` 段
9. `references/notebook-schema.md` 存在
10. `references/notebook-update-protocol.md` 存在

## 测试

`tests/test_wisdom_notebook_skill.py`（stdlib only：`re` + `unittest` + `pathlib` + `subprocess`）

## SUT Form 说明

`emergent` —— SKILL.md 是文档，无运行时模式承载。Refactor 阶段如发现 SKILL.md 主体过长可下沉 references。

## Approval

按 ADR-009 D2 fast lane，本测试设计 auto approved。

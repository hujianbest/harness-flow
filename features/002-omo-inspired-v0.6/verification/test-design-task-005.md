# Test Design — TASK-005 (hf-gap-analyzer SKILL.md + gap-rubric)

- Task: TASK-005
- SUT Form: **`emergent`**（SKILL.md 写作类）
- Test Strategy: 复用 TASK-002 模板（learn-0003 sealed pattern）：file existence × 2 + audit OK + 6 维 rubric grep + Workflow ≥ 4 步 + Common Rationalizations ≥ 3 行 + Object Contract 段 + 显式声明非 Fagan review 节点 + size budget

## 待验证行为（对应 TASK-005 Acceptance #1~#5）

1. `skills/hf-gap-analyzer/SKILL.md` + `references/gap-rubric.md` 存在
2. audit-skill-anatomy.py 报 OK
3. SKILL.md 含 6 维 rubric 名（按 design §3.2：Implicit Intent / AI Slop / Missing Acceptance / Unaddressed Edge Cases / Scope Creep / Dangling Reference）
4. SKILL.md 显式声明"不是 Fagan review 节点"（不写 verdict）
5. wc -l ≤ 500 / token ≤ 5000

## 测试

`tests/test_gap_analyzer_skill.py`（stdlib only，复用 TASK-002 verifier 模板）

## Approval

按 ADR-009 D2 fast lane auto approved。

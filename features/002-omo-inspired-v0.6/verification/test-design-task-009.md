# Test Design — TASK-009 (hf-tasks-review momus 4-dim + N=3 rewrite loop)

- Task: TASK-009
- SUT Form: **`emergent`**（modified-skill task）
- Test Strategy: 结构性 verifier 检查 SKILL.md 改动 + references/momus-rubric.md 新文件 + audit 仍通过

## 待验证行为（TASK-009 Acceptance #1~#5 + design §4.1）

1. `skills/hf-tasks-review/references/momus-rubric.md` 新文件存在
2. momus-rubric.md 含 4 维 (Clarity / Verification / Context / Big Picture) + 各自阈值（100% / 90% / 80% / 100% / 0%）
3. `skills/hf-tasks-review/SKILL.md` 含 `rejected-rewrite` verdict + N=3 上限
4. SKILL.md `Common Rationalizations` 段含"差 1% 也是不达标"反驳
5. audit-skill-anatomy.py 仍通过；NFR-002 size budget 仍合规

## Approval

按 ADR-009 D2 fast lane auto approved。

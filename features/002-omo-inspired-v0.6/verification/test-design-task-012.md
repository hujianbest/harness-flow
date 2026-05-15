# Test Design — TASK-012 (hf-code-review ai-slop-rubric)

- Task: TASK-012
- SUT Form: **`emergent`**
- Test Strategy: 结构性 verifier 检查 SKILL.md 引用 + references/ai-slop-rubric.md 含可 grep 的禁用模式列表 + 例外段 + audit 仍通过

## 待验证行为（TASK-012 Acceptance）

1. `skills/hf-code-review/references/ai-slop-rubric.md` 新文件存在
2. ai-slop-rubric.md 含禁用模式（regex 形式可 grep）：simply / obviously / clearly / em-dash 等
3. ai-slop-rubric.md 含例外段（README / docs / test assertion 允许）
4. SKILL.md "Comment 质量" 子节引用 rubric
5. audit 仍通过 + size budget OK

## Approval

按 ADR-009 D2 fast lane auto approved。

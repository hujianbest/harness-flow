# 测试驱动开发评测

这个目录包含 `hf-test-driven-dev` 的评测 prompts。

## 目的

这些评测用于验证实现入口是否真正做到：

- 测试设计 approval step 在 TDD 前完成
- interactive 模式等待用户确认
- auto 模式写 approval record 但不跳过审批语义
- 政策禁止时不自动推进

## 建议评分关注点

1. 是否在 TDD 前完成测试设计审批
2. 是否正确区分 interactive/auto 模式
3. 是否在政策禁止时停止自动推进
4. 是否守住 Two Hats（GREEN 步内不做 cleanup，cleanup 与新行为不混 commit）
5. 是否守住 Escalation Boundary（跨 ≥3 模块 / 改 ADR / 改模块边界 / 接口契约不在 task 内做，停 task 路由到 `hf-workflow-router`）
6. Refactor Note 是否完整（含 Fowler vocabulary 与 Hat Discipline / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence 等显式字段）

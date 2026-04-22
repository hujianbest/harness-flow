# Code Review 评测

## Protected Behavior Contracts

这些评测保护 `hf-code-review` 的以下行为契约：

1. **设计偏离检测**：即使测试全绿，实现偏离设计仍应给出需修改结论
2. **错误处理检查**：静默失败、缺少错误记录等不应被忽略
3. **可读性关注**：魔法数字等问题不得因功能正确而被跳过
4. **范围守卫**：不允许超规格/超设计的"顺手加功能"
5. **Verdict 唯一下一步**：通过时指向 `hf-traceability-review`，需修改时指向 `hf-test-driven-dev`
6. **Precheck/reroute**：上游 evidence 冲突时先阻塞并回到 `hf-workflow-router`
7. **CR7 Refactor Note 完整性**：Refactor Note 必须包含 Hat Discipline / In-task Cleanups (Fowler vocabulary) / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence；模糊表达（如 "did some cleanups"）触发 CA7 undocumented-refactor，需修改
8. **CR7 Escalation Boundary**：跨 ≥3 模块 / 改 ADR / 改模块边界 / 改接口契约的"顺手"重构触发 CA8 escalation-bypass，即使测试全绿也应阻塞并 reroute_via_router=true，路由到 `hf-workflow-router` → `hf-increment` / `hf-design`
9. **CR7 Architectural Smells Detection**：触碰范围内可见的 architectural smells（god-class / cyclic-dep / layering-violation / leaky-abstraction / feature-envy）被忽略触发 CA10
10. **CR7 Over-abstraction (YAGNI)**：引入设计未声明的新抽象层、理由是"未来可能用得到"触发 CA9，要求回退或 escalate
11. **不重论证架构决策**：reviewer 在 CR7 内只做 conformance check，不重新讨论应该用什么架构模式（这是 `hf-design` 的工作）

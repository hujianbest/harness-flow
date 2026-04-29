# Tasks Review — WriteOnce Walking Skeleton

- 节点: `hf-tasks-review`
- Reviewer Role: Independent Reviewer
- Date: 2026-04-29
- Artifact Under Review: `features/001-walking-skeleton/tasks.md`

## Verdict

`通过`

## Checklist

| 检查项 | 结论 | 证据 |
|---|---|---|
| INVEST：每个任务 Independent / Negotiable / Valuable / Estimable / Small / Testable | ✅ | T1 Acceptance 明确可测；T2/T3/T4 列为 deferred 但仍带 Acceptance |
| 关键任务能追溯回 spec FR / NFR + design 章节 | ✅ | section 4 表格 |
| 关键任务能回答 "完成时什么必须为真" + "如何验证" + "触碰哪些工件" | ✅ | T1 完整给出 Acceptance / Verify / Files / 完成条件 |
| 是否锁单一 Current Active Task | ✅ | T1 = active；T2/T3/T4 = pending |
| 任务计划是否被写成"设计文档副本" | ✅ 否 | tasks 只列任务边界 + 验收 + 依赖；架构决策回引 design / ADR |
| 任务计划是否把里程碑当真实任务 | ✅ 否 | section 2 里程碑 ≠ section 5 任务 |
| Walking-skeleton 纪律：是否真薄 | ✅ | T1 唯一在 v0.1.0 实现，其余任务显式 deferred |
| deferred 任务是否在 closeout 时不阻塞 | ✅ | section 7 DoD 显式说明 T2/T3/T4 不构成 blocker |
| 任务依赖图是否清晰 | ✅ | section 6 依赖图 |

## Findings

无重大问题。观察：

1. T4 标 "Must for ergonomic, deferred" — 这个组合形式罕见，但语义上是诚实的：CLI 对最终用户体验是 must，但对 **demo 主链证明** 不是 must。在 closeout 注记中明确区分这两层即可。
2. section 9 不启用独立 task-board 是正确取舍——只 4 个候选 + 唯一 active，task-board 是过度配置。

## Anti-Pattern Sweep

| 反模式 | 是否触发 | 备注 |
|---|---|---|
| 任务被写成"做完后回头加测试" | 否 | T1 Verify 明确 RED/GREEN evidence 双向落盘 |
| 多任务并行 active | 否 | 仅 T1 |
| Definition of Done 模糊（用 "差不多了"） | 否 | section 7 DoD 全部可勾选 |
| deferred 任务被偷偷"以后再说"（无 Acceptance） | 否 | T2/T3/T4 都有 Acceptance + Selection Priority |
| 文件影响图过细到行号 | 否 | section 3 只到文件级 |

## Conclusion

- Conclusion: `通过`
- Next Action Or Recommended Skill: `hf-test-driven-dev`（active task = T1）
- 产出 approval：`approvals/tasks-approval-2026-04-29.md`

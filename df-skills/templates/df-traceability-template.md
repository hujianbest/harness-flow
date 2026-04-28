# df Traceability Matrix

使用说明：

- 这是 `features/<Work Item Id>-<slug>/traceability.md` 模板。
- df 要求 IR -> SR -> AR -> 组件设计 -> AR 设计 -> 代码 -> 测试 -> 测试有效性审查 -> 代码检视 全链路可回读。
- 由 `df-specify` 初始化骨架，`df-component-design` / `df-ar-design` / `df-tdd-implementation` / `df-test-checker` / `df-code-review` 各自补充本节点对应行。

## Identity

- Work Item Type:                          # AR / DTS / CHANGE
- Work Item ID:
- Owning Component:

## Trace Rows

| IR | SR | AR | Component Design Section | AR Design Section | Test Design Case | Code File / Function | Test Code File | Verification Evidence |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

## Notes

- 若某行不存在对应链接（例如 AR 不修改组件设计），标记 `N/A` 并简述理由。
- 跨组件 AR 在每个受影响组件仓库内分别维护对应行，本文件只覆盖**当前组件仓库**的视角。
- 测试设计 Case 必须能在 AR 实现设计的测试设计章节中找到对应条目，形成双向锚点。

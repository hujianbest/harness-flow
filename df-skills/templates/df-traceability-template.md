# df Traceability Matrix

使用说明：

- 这是 `features/<Work Item Id>-<slug>/traceability.md` 模板。
- 列集按 work item 类型有所不同：
  - **SR**（需求分析子街区）：IR → SR → Affected Components → Component Design Section → Candidate AR Breakdown
  - **AR / DTS / CHANGE**（实现子街区）：IR → SR → AR → 组件设计 → AR 设计 → 代码 → 测试 → 测试有效性审查 → 代码检视
- 由 `df-specify` 初始化骨架，后续 `df-component-design` / `df-ar-design` / `df-tdd-implementation` / `df-test-checker` / `df-code-review` 各自补充本节点对应行（实现子街区）；SR 由 `df-specify` / `df-component-design` 补充，止于 candidate breakdown 列。

## Identity

- Work Item Type:                          # SR / AR / DTS / CHANGE
- Work Item ID:
- Owning Component:                        # AR / DTS / CHANGE
- Owning Subsystem:                        # SR

## Trace Rows — Implementation 子街区（AR / DTS / CHANGE）

| IR | SR | AR | Component Design Section | AR Design Section | Test Design Case | Code File / Function | Test Code File | Verification Evidence |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

## Trace Rows — Requirement-Analysis 子街区（SR）

| IR | SR | Affected Component | Modification Surface | Component Design Section | Candidate AR ID | Covers SR Rows |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## Notes

- 若某行不存在对应链接（例如 AR 不修改组件设计、SR 不修订组件设计），标记 `N/A` 并简述理由。
- 跨组件 AR 在每个受影响组件仓库内分别维护对应行，本文件只覆盖**当前组件仓库**的视角。
- 跨组件 SR 通常只在**主子系统的组件仓库**内维护本表（按团队约定）；其他受影响组件由 SR 拆出的 AR 各自落表。
- 测试设计 Case 必须能在 AR 实现设计的测试设计章节中找到对应条目，形成双向锚点。
- SR 的 Candidate AR ID 在 SR 内部使用 `CAR-001` 等编号；当需求负责人新建对应 AR work item 时，再在新 AR 的 traceability 表中填入正式 AR ID 并反向回指本 SR。

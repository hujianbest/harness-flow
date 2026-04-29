# ADR-0001: Record architecture decisions

- 状态: accepted
- 日期: 2026-04-29
- 决策人: cursor agent (per user delegation, demo scope)

## Context

WriteOnce 是 HarnessFlow v0.1.0 的 quickstart demo。HarnessFlow 的 SDD artifact layout (`docs/principles/sdd-artifact-layout.md`) 要求 `docs/adr/` 是「档 0 不可省」资产，作为架构决策的唯一权威池。

为符合这一要求，本 ADR 用 Michael Nygard 的 ADR 模板宣布：

WriteOnce demo 内的所有架构决策从此 ADR-0001 起记录到 `examples/writeonce/docs/adr/NNNN-<slug>.md`。

## Decision

采用 ADR 记录架构决策。

## Consequences

- 后续 design 文档通过 ADR ID 引用（不内联 ADR 全文）。
- ADR 编号仓库级唯一，永不重复，永不重新编号。
- 状态字段写在文档正文首段，不通过移动文件表达。

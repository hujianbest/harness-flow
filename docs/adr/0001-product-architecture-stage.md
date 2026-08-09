# ADR-001: 恢复产品级架构阶段

- 状态: 已接受
- 日期: 2026-08-09

## 上下文

v5 Matt 对齐主链将架构下沉为特性级一页纸，产品层仅保留术语与台账。大系统缺少系统骨架，开发呈任务驱动碎片化。v4 曾有 `hf-architect` + `product/architecture.md`。

## 决策

增加仓库级阶段 `hf-to-product-architecture`；产品架构完整性由技能与 `hf-review` 约束，**不**由 `hf_gate` 强制拦截；特性架构为产品地图增量注解；存量允许「仅架构地图」。

## 后果

绿地建造链增加系统地图阶段；热修旁路保留；门禁仍只管特性主链文件/评审结论与产品台账（CONTEXT/assumptions/decisions）。

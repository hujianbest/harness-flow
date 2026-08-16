---
name: hf-to-architecture
description: 基于已确认的规格产出特性级架构设计（模块边界、缝、数据与关键流程、ADR）。位于 hf-to-spec 与 hf-to-tickets 之间。特性架构是产品架构的增量注解；宜对齐 product/architecture.md。使用 hf-codebase-design 词汇。
---

# hf-to-architecture

在 `spec.md` 已通过 `hf-review`(规格)之后、拆票之前,把「本片怎么建」钉成一页**增量**架构,供 `hf-to-tickets` 切垂直切片。

## 前置

1. 冷读 `spec.md`、`product/architecture.md`（若有）、`CONTEXT.md`(若有)、相关 ADR,以及 `product/` 假设台账。更新 `progress.md` 为 `to-architecture`。
2. 加载 `hf-codebase-design`。本阶段产出仍落在本特性目录。

## 流程

1. **对齐产品架构**：写明本片落在哪些产品模块/场景上；越界须显式标注并记 ADR/假设台账，必要时回写 `product/architecture.md`。
2. **定模块与缝**:只写本特性**新增或触及**的模块(宜少)、各自职责、公共接口/缝;优先复用既有缝,新缝取最高可测点。用深模块词汇(小接口、大行为)。禁止复述产品架构全文。
3. **关键流程与数据**:画 1~3 条端到端路径;核心实体与关系几行即可,字段级细节留给票。
4. **横切约定**:仅写本片相对产品横切的偏离；目录与命名默认继承开发视图。
5. **ADR**：难以逆转的决策写入 `docs/adr/`（或追加到 `product/decisions.md`），正文只链接过去。
6. **落盘** `features/<id>/architecture.md`(≤80 行),含对齐声明与机器可读确认行占位。
7. **送审**:按 `hf-review` 走架构评审 → `reviews/architecture-review.md`。`interactive` 等确认;`auto` 可在非降级评审后 `auto-approved`。
8. 更新 `progress.md` 中的当前阶段与下一步。

## `architecture.md` 最小结构

```markdown
# 架构 — <特性名>

- 日期:
- 对应规格: `spec.md`
- 用户确认:

## 对齐产品架构
<!-- 必须引用 product/architecture.md；说明落点模块/场景；越界显式写出 -->

## 本片模块与缝
## 核心数据
## 关键流程
## 横切偏离
## ADR 链接
```

## 红线

- 无 `spec-review` 通过记录，不得写入「已确认」架构并推进到 `to-tickets` 阶段
- 存在 `product/architecture.md` 时，正文应含对齐声明（由技能与 `hf-review` 约束）
- 不在本阶段实现代码或拆完整票单(拆票是 `hf-to-tickets`)
- 不静默填补欠定:默认选择进 `product/assumptions.md`

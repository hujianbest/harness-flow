---
name: hf-to-product-architecture
description: 仓库级产品架构设计：在 grill 确认共享语言之后、任何特性 spec 之前，产出一页 product/architecture.md（原则与风格、逻辑划分、开发视图、关键场景、横切与 ADR），经 hf-review 产品架构评审；完整性由技能与评审约束。存量可仅建架构地图。
---

# hf-to-product-architecture

把「系统长什么样」钉成可继承的产品级地图，供后续特性增量架构与切片对齐。**不是**特性实现设计。

## 前置

1. 绿地：已按 `product-layer-templates` 落盘，且 `hf-grill-with-docs` 已确认 `CONTEXT.md`（及台账）。
2. 读 `product/progress.md`（若有），确认当前在产品架构阶段或尚未确认架构。
3. 加载 `hf-codebase-design` 词汇；领域边界不清时加载 `hf-domain-modeling`（可升 `CONTEXT-MAP.md`）。
4. 更新 `product/progress.md`：当前阶段 `to-product-architecture`。

## 流程

1. **原则与风格**：选定架构风格（分层 / 六边形 / 整洁等）与依赖硬规则；难逆转点写 ADR。
2. **逻辑划分**：3~7 个模块或限界上下文 + 一句话职责；多上下文则维护 `CONTEXT-MAP.md`。
3. **开发视图**：目录/多模块划分、源码与测试放置、命名约定。
4. **关键场景**：2~5 条端到端路径，作为垂直切片判据；建造模式建议第一片为行走骨架（`feature.md` 标 `- 骨架: 是`）。
5. **横切与 ADR**：错误、鉴权、持久化、观测等只写约定与链接，不写字段级细节。
6. **落盘** `product/architecture.md`（≤120 行），确认行先留空。
7. **送审** `hf-review`（产品架构）→ `product/reviews/product-architecture-review.md`。
8. 用户确认后写入架构与评审的确认行；更新 `product/progress.md` → `ready`。

## 技法（按需）

- **彩色/多色建模**：在 grill/本阶段澄清领域角色与状态时使用，结论写入逻辑划分与 CONTEXT，不单独成阶段。
- **4+1**：默认合并为逻辑 + 开发 + 场景三块；物理/过程视图仅在部署/并发成为硬约束时追加 ADR。

## 红线

- 无 CONTEXT 确认不得宣称产品架构已确认
- 不把特性级接口签名、字段表、票级细节写入产品架构
- 不在本阶段实现业务代码或拆完整特性票单
- 欠定 → `product/assumptions.md`，不静默填补

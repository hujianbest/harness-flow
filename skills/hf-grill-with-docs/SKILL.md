---
name: hf-grill-with-docs
description: 通过结构化访谈对齐想法/方案，并将结果写入 CONTEXT.md 与 ADR。HarnessFlow 主链第二步；内驱 hf-grilling 与 hf-domain-modeling。绿地先按 product-layer-templates 落盘产品层；确认后写入 progress.md，下一步进入 hf-to-product-architecture（完整产品层）或开特性（存量/仅地图）。
---

# hf-grill-with-docs

对计划或设计做无情访谈,同时用 `hf-domain-modeling` 建立共享语言与文档。

## HarnessFlow 桥接

1. 若无产品层/台账：按 `skills/hf-workflow/references/product-layer-templates.md` 创建 `CONTEXT.md`、`product/`、`docs/adr/`、`features/`（不覆盖已有文件）。
2. 绿地/大系统：先对齐产品意图与术语；**不要**在产品架构确认前把精力耗在特性拆票上。可暂不创建特性目录，进度写在 `product/progress.md`（阶段 `grill-with-docs`）。
3. 若已定位切片：创建或定位 `features/<NNN>-<slug>/`，写入 `feature.md` 与 `progress.md`（阶段为 `grill-with-docs`，模式为 `interactive|auto`）。建造模式建议第一片行走骨架：`- 骨架: 是`。
4. `feature.md` 必须含机器可读行:`- 模式: 建造|探索`、`- 用户可感知: 是|否`(拿不准则「是」)。
5. 运行本技能主体(下节):访谈 + 更新 `CONTEXT.md` / ADR / `product/assumptions.md`。
6. 用户确认共享理解后，在 `CONTEXT.md` 或本特性/`product` 的 `progress.md` 中记录确认；`auto` 模式下的默认选择必须先写入假设台账，再记为 `auto-approved`。
7. 下一步（完整产品层）:进入 `hf-to-product-architecture`，再开特性走 `hf-to-spec`。存量热修且采用仅架构地图时，可直接开特性并冷读地图。

## 主体

使用 `hf-domain-modeling` 技能开展一次 `hf-grilling` 会话。

欠定不静默填补:提出带默认的选项 → 记入 `product/assumptions.md` → 继续。

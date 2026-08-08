---
name: hf-grill-with-docs
description: 通过结构化访谈对齐想法/方案，并将结果写入 CONTEXT.md 与 ADR。HarnessFlow 主链第二步；内驱 hf-grilling 与 hf-domain-modeling。绿地项目先运行 gate init；确认后写入 progress.md 并进入 hf-to-spec。
---

# hf-grill-with-docs

对计划或设计做无情访谈,同时用 `hf-domain-modeling` 建立共享语言与文档。

## HarnessFlow 桥接

1. 若无产品层/台账: `python3 skills/hf-workflow/scripts/hf_gate.py init`
2. 创建或定位 `features/<NNN>-<slug>/`，写入 `feature.md` 与 `progress.md`（阶段为 `grill-with-docs`，模式为 `interactive|auto`）。
3. `feature.md` 必须含机器可读行:`- 模式: 建造|探索`、`- 用户可感知: 是|否`(拿不准则「是」)。
4. 运行本技能主体(下节):访谈 + 更新 `CONTEXT.md` / ADR / `product/assumptions.md`。
5. 用户确认共享理解后，在 `CONTEXT.md` 或本特性的 `progress.md` 中记录确认；`auto` 模式下的默认选择必须先写入假设台账，再记为 `auto-approved`。
6. 下一步:`check --to to-spec` 通过后进入 `hf-to-spec`。

## 主体

使用 `hf-domain-modeling` 技能开展一次 `hf-grilling` 会话。

欠定不静默填补:提出带默认的选项 → 记入 `product/assumptions.md` → 继续。

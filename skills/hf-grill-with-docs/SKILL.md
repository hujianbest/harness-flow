---
name: hf-grill-with-docs
description: 结构化访谈对齐想法/方案,并落盘 CONTEXT.md 与 ADR。HarnessFlow 主链第二步;内驱 hf-grilling 与 hf-domain-modeling。绿地先 gate init;确认后写 progress 并进入 hf-to-spec。
---

# Grill With Docs

对计划或设计做无情访谈,同时用 `hf-domain-modeling` 建立共享语言与文档。

## HarnessFlow 桥接

1. 若无产品层/台账: `python3 skills/hf-workflow/scripts/hf_gate.py init`
2. 创建或定位 `features/<NNN>-<slug>/`,写 `feature.md` 与 `progress.md`(阶段 `grill-with-docs`,模式 interactive|auto)。
3. `feature.md` 必须含机器可读行:`- 模式: 建造|探索`、`- 用户可感知: 是|否`(拿不准则「是」)。
4. 运行本技能主体(下节):访谈 + 更新 `CONTEXT.md` / ADR / `product/assumptions.md`。
5. 用户确认共享理解后,在 `CONTEXT.md` 或本特性 progress 记录确认;`auto` 下默认选择必须先入假设台账再 `auto-approved`。
6. 下一步:`check --to to-spec` 通过后进入 `hf-to-spec`。

## 主体

Run a `hf-grilling` session, using the `hf-domain-modeling` skill.

欠定不静默填补:提出带默认的选项 → 记入 `product/assumptions.md` → 继续。

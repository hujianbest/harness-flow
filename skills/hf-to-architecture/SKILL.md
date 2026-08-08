---
name: hf-to-architecture
description: 基于已确认的 spec 产出特性级架构设计(模块边界、缝、数据与关键流程、ADR)。位于 hf-to-spec 与 hf-to-tickets 之间;进入前须 gate check --to to-architecture(含 spec-review 通过)。使用 hf-codebase-design 词汇,必要时参考 hf-wayfinder。
---

# To Architecture

在 `spec.md` 已通过 `hf-review`(规格)之后、拆票之前,把「怎么建」钉成一页可执行的架构,供 `hf-to-tickets` 切垂直切片。

## 前置

1. 运行 `python3 skills/hf-workflow/scripts/hf_gate.py check --feature features/<id> --to to-architecture`,RESULT 写入 `progress.md`。FAIL 不得进入。
2. 冷读 `spec.md`、`CONTEXT.md`(若有)、相关 ADR,以及 `product/` 假设台账。
3. 加载 `hf-codebase-design`;大雾/多会话决策可参考 `hf-wayfinder` 的决策票思路,但本阶段产出仍落在本特性目录。

## 流程

1. **定模块与缝**:列出本特性触及的模块(3~7 个为宜)、各自职责、公共接口/缝;优先复用既有缝,新缝取最高可测点。用深模块词汇(小接口、大行为)。
2. **关键流程与数据**:画 1~3 条端到端路径;核心实体与关系几行即可,字段级细节留给票。
3. **横切约定**:错误处理、测试组织、目录与命名;偏离既有架构须显式写入并记假设台账。
4. **ADR**:难逆决策写入 `docs/adr/`(或 `product/decisions.md` 追加),正文只链过去。
5. **落盘** `features/<id>/architecture.md`(≤80 行),含机器可读确认行占位。
6. **送审**:按 `hf-review` 走架构评审 → `reviews/architecture-review.md`。`interactive` 等确认;`auto` 可在非降级评审后 `auto-approved`。
7. 更新 `progress.md` 当前阶段与下一步。

## architecture.md 最小结构

```markdown
# 架构 — <特性名>

- 日期:
- 对应 spec: spec.md
- 用户确认:

## 模块边界
## 缝与测试点
## 核心数据
## 关键流程
## 横切约定
## ADR 链接
```

## 红线

- 无 spec-review 通过记录不得写「已确认」架构并推进 tickets
- 不在本阶段实现代码或拆完整票单(拆票是 `hf-to-tickets`)
- 不静默填补欠定:默认选择进 `product/assumptions.md`

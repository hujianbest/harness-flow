---
name: hf-ship
description: 特性收尾:确认 code-review 与(可感知时)demo 验收,勾选票与反馈回写 CONTEXT/ADR/假设台账,更新 progress 为 done。HarnessFlow 主链最后一步;进入前 gate check --to ship。
---

# Ship

发布与回顾:把已验证的实现正式收口,并把反馈写回产品层。

## 前置

1. `check --feature features/<id> --to ship`。须 tickets 全勾、`code-review` 通过已确认;用户可感知还须 `reviews/demo-acceptance.md` 结论为「接受」且已确认。
2. FAIL 则不得宣称交付完成。

## 流程

### 1. 验收对照

逐条核对 spec 用户故事 / 票验收标准是否闭合;缺口只能回 `hf-implement`+评审,不能在 ship「补做」。

### 2. 反馈回写

- 勾选外部 backlog/tracker 对应项(若有)
- 新想法按垂直切片追加,不塞进已关闭特性
- 结算 `product/assumptions.md`(确认→decisions/ADR;推翻→记波及)
- 结构变化回写 `CONTEXT.md` 与特性/产品架构要点

### 3. Demo 反馈

可感知特性:interactive 已验收则记录要点;auto 曾 `auto-approved` 的,本次与用户交互必须主动呈上 demo 征求反馈。

### 4. 收尾

- `progress.md` 当前阶段 `done`,写交付摘要(一句话 + 回写列表)
- 不删除 evidence/reviews(审计用)

## 红线

- gate FAIL 时口头「做完了」
- 探索模式走 ship
- 把新范围塞进已评审批次而不回开票

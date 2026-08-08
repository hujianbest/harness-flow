---
name: hf-ship
description: 特性收尾：确认 code-review 与（用户可感知时）演示验收，勾选任务票并将反馈回写 CONTEXT/ADR/假设台账，把 progress.md 更新为 done。HarnessFlow 主链最后一步；进入前运行 gate check --to ship。
---

# hf-ship

发布与回顾:把已验证的实现正式收口,并把反馈写回产品层。

## 前置

1. `check --feature features/<id> --to ship`。须全部任务票已勾选、`code-review` 已通过并确认；用户可感知特性还须确保 `reviews/demo-acceptance.md` 的结论为「接受」且已确认。
2. 结果为 `FAIL` 时不得宣称交付完成。

## 流程

### 1. 验收对照

逐条核对规格中的用户故事 / 任务票验收标准是否闭合；缺口只能返回 `hf-implement` 并重新评审，不能在 `ship` 阶段「补做」。

### 2. 反馈回写

- 勾选外部待办列表/任务跟踪器中的对应项（若有）
- 新想法按垂直切片追加,不塞进已关闭特性
- 结算 `product/assumptions.md`（确认→决策记录/ADR；推翻→记录影响范围）
- 结构变化回写 `CONTEXT.md` 与特性/产品架构要点

### 3. 演示反馈

可感知特性：`interactive` 模式下已验收则记录要点；`auto` 模式下曾记为 `auto-approved` 的，本次与用户交互必须主动呈上演示并征求反馈。

### 4. 收尾

- `progress.md` 当前阶段 `done`,写交付摘要(一句话 + 回写列表)
- 不删除证据/评审记录（审计用）

## 红线

- 门禁为 `FAIL` 时口头宣称「做完了」
- 探索模式进入 `ship` 阶段
- 把新范围塞进已评审批次而不回开票

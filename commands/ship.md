---
description: HarnessFlow 收尾阶段——DoD 核验、promotion 长期资产、closeout，先核验后关闭
---

执行 HarnessFlow 收尾阶段。

1. 前置检查：先从 plan.md 读取组件根与工件根；plan.md 全部任务完成且门禁表 R1/R2/R3 均通过、同一工件根下 reviews/ 记录齐全且 findings 全部有 Resolution；否则回对应阶段。
2. 读取 `skills/hf-ship/SKILL.md` 并按其工作流执行：DoD 逐项核验 → traceability 终验 → promotion（spec/design/组件设计 → 同一组件根下 docs/ 长期资产或团队覆盖路径，保留原模板并做最小清理）→ closeout.md。
3. 核验发现缺口 → 返工对应阶段，补完再回来；不解释缺口、不带病关闭。
4. 把 closeout 呈给用户做最终确认；确认后工作项关闭，同一组件根/工件根下 `features/<id>/`（或团队覆盖路径）原地保留。

命令是 bias 不是 bypass：仍按 on-disk 工件决定真实下一步。

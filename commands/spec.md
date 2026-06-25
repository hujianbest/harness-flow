---
description: HarnessFlow 规格阶段——把需求澄清成可测试的规格，先规格后设计与代码
---

执行 HarnessFlow 规格阶段。

1. 新工作流启动时先按 `using-hf` §7 确定目标组件根与工件根，再向用户确认运行模式（attended/unattended），一并记入 plan.md 头部。
2. 读取 `skills/hf-specify/SKILL.md` 并按其工作流执行：澄清 → 需求条目（EARS + Given/When/Then + Change Type）→ NFR QAS → 粒度检查 → traceability 与 plan.md 骨架 → 自检。
3. 产出目标组件根下 `features/<id>-<slug>/spec.md`、`traceability.md`、`plan.md` 骨架（或团队覆盖路径）。业务方向、优先级、验收阈值的缺口列为 Open Questions 交回用户，不替用户拍板。
4. 完成后进入 R1 门禁：`/review` 独立评审 spec 并落盘记录（必经节点）；attended 模式下经人确认后才进入设计。

命令是 bias 不是 bypass：仍按 on-disk 工件决定真实下一步。

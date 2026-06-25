---
description: HarnessFlow 独立评审——以独立上下文评审规格/设计/测试/代码，作者永不自审
---

执行 HarnessFlow 独立评审（工作流的 R1/R2/R3 必经门禁，也可对任意目标单独发起）。

1. 确认评审目标（spec / design / 测试 / 代码；用户未指明时按工件状态推断并确认）。
2. 读取 `skills/hf-review/SKILL.md`，按其协议派发 `hf-reviewer` subagent（agent name: `hf-reviewer`，角色定义见 `agents/hf-reviewer.md`）执行独立评审：输入只给被评审产物、上游工件、对应 rubric 与适用的语言/领域技能，不给作者推理过程。
3. **落盘评审记录**到同一组件根/工件根下 `features/<id>/reviews/<目标>-review-<日期>.md`（或团队覆盖路径，复审加 `-r2` 轮次）：findings 表含 Resolution 列、verdict、抽查记录。没有记录的评审等于没有评审。
4. verdict 为需修改或重新设计时：把 plan.md 对应门禁置为 `rework`，记录评审路径与返工目标；作者按 findings 返工并逐条回写 Resolution（修复+commit / 人接受+理由 / 债务+去向），然后发起复审；critical/important 未闭环不放行。R3 测试/代码问题默认回 `/build`（`hf-tdd`）定向返工；若问题指向规格或设计漂移，则回对应上游阶段并重新经过受影响门禁。不停在评审上下文里自修，也不直接进入收尾。
5. 按 plan.md 运行模式处理确认：attended 呈人同意后更新门禁表进入下一阶段；unattended 不停顿但记录照写、critical 照样阻塞。评审者不直接修改任何产物；可由 AI 修复的 findings 先自动回对应作者阶段，只有缺业务事实、专家裁决或 3 轮仍不通过时才停下问人。

命令是 bias 不是 bypass：仍按 on-disk 工件决定真实下一步。

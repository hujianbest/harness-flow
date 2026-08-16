---
name: hf-implement
description: 按任务票/规格实现工作，内驱 hf-tdd，完成后执行 hf-review（含代码门）。HarnessFlow 主链步骤；建造模式须遵循红—绿循环。探索模式写 conclusion.md，禁止 ship。
---

# hf-implement

实现任务票（以及规格/架构）所描述的工作。

## HarnessFlow 桥接

1. 更新 `progress.md` 为 `implement`。有 UI 时加载 `hf-ui-design`。
2. 同一时间只做一张**前沿票**(blockers 均已勾选)。
3. 建造模式:每个行为变更走 `hf-tdd`(红→绿→重构);实现任务派 **subagent**,主会话编排。
4. 票完成后勾选 `tickets.md` 对应 `- [x] T-NN`。
5. 全部任务票勾选后：`hf-review`（含代码门）→ `reviews/code-review.md` + 确认。
6. 用户可感知：准备演示证据与体验路径，供进入 `ship` 阶段前验收。
7. 下一步进入 `hf-ship`。

## 主体

尽可能在规格/架构中预先约定的缝上使用 `hf-tdd`。

定期运行类型检查和单个测试文件，并在最后运行一次完整测试套件。

完成后，在进入 `ship` 阶段前执行 `hf-review`。

在用户或流程要求时，将工作提交到当前分支。

## 探索模式

若 `feature.md` 为 `模式: 探索`：不强制 TDD；产物即弃；写入 `conclusion.md` 收尾；**禁止进入 `ship` 阶段、禁止直接晋升代码**。

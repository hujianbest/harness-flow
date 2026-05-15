# Fast Lane Escape Conditions

> 6 条 escape 条件，按 ADR-009 D3 第 4 项 enumerate。命中任一**立即让出**抛回架构师；不允许"先走完当前 verdict 再让出"。

## 1. 任一节点的 `Hard Gates` 命中"方向 / 取舍 / 标准不清"

**触发信号**：当前节点的 verdict / output / 错误信息含"方向不清"/"标准未明"/"取舍冲突"/"待架构师拍板"等表述。

**对应 soul.md**：第 1 条硬纪律（"方向、取舍、标准不清时，默认是停下来澄清"）。

**让出行为**：把当前节点 output 摘要抛给架构师 + 列出待澄清项；不自动选一个方向继续。

## 2. 任一 review verdict = `阻塞`

**触发信号**：review record 内 `## 结论` 段为 `阻塞` 或 JSON 摘要 `conclusion: blocked` / `conclusion: 阻塞`。

**让出行为**：抛 review record 路径 + 阻塞理由摘要给架构师。

**注意**：`需修改` / `rejected-rewrite` 不算 escape——继续 fast lane 走 author Round N+1（前提：N < 3，否则触发 escape 5）。

## 3. 任一 gate verdict = FAIL

**触发信号**：`hf-regression-gate` / `hf-doc-freshness-gate` / `hf-completion-gate` 任一 verdict 字段为 `FAIL` / `failed` / `阻塞`。

**让出行为**：抛 gate record 路径 + 失败 evidence 给架构师。

**注意**：gate 是 boolean PASS/FAIL，不像 review 有"需修改"中间态；gate FAIL 等价于 escape。

## 4. `hf-wisdom-notebook` 的 `problems.md` 出现新增 status=open 项

**触发信号**：当前 task 完成时往 `notepads/problems.md` 写入了新 entry（status=open，severity=blocker 或 critical）。

**让出行为**：抛新增 problems.md entry + 被阻塞的 task ID 给架构师；让架构师决定是开 hf-increment 修 design / 修 spec，还是接受降级。

**注意**：`issues.md` status=open 不触发 escape（issues 是非阻塞问题；problems 才是真阻塞）。

## 5. 连续 3 次同一节点 rewrite loop 仍未通过（与 hf-tasks-review N=3 上限对齐）

**触发信号**：同一 review 节点的 verdict 连续 3 次 `需修改` / `rejected-rewrite`，第 4 次仍未达到通过阈值。

**对应**：`hf-tasks-review/SKILL.md` 引入的 momus 4 维 + N=3 rewrite loop 上限（TASK-009 实现后正式生效；本 skill 边界提前对齐）。

**让出行为**：抛 N 轮 review 摘要 + author 改动列表给架构师；让架构师决定是否结构性重写、降级 acceptance、还是接受第 4 轮 author 修订作为最终版。

## 6. 架构师在会话中说显式停下关键词

**触发信号**：会话中出现以下任一关键词（精确匹配或近义）：

- `停` / `暂停` / `先停` / `暂停一下`
- `wait` / `hold on` / `等等` / `等一下`
- `stop` / `pause`
- `回头看看` / `先别推进` / `先别 commit`

**让出行为**：立即停止当前 fast lane 推进；当前进行中的节点完成 atomic 写入后让出（不打断 atomic 操作）；之后的所有节点决定权回架构师。

**注意**：架构师说 `standard mode` / `恢复 standard` 是 mode-switch 不是 escape——同样让出但区别在于"是否还期望本轮内 fast lane 重启"。

---

## 检查 protocol（hf-ultrawork Workflow 步骤 3 的精细化）

每个 reviewer / gate verdict 之后**先**按以下顺序逐条检查；任一命中即让出：

```
1. 读 verdict 工件
2. 检查 escape #1 (Hard Gates 标准不清)
3. 检查 escape #2 (review verdict = 阻塞)
4. 检查 escape #3 (gate verdict = FAIL)
5. 检查 escape #4 (新 problems.md status=open)
6. 检查 escape #5 (rewrite loop ≥ 3)
7. 检查 escape #6 (架构师显式停下关键词；这一项每次会话回合开始时就要先扫一遍)
8. 全 6 条 0 命中 → 继续 fast lane
```

## 让出后的恢复

- 架构师指示后，若想继续 fast lane → 架构师重新说 explicit opt-in 关键词；本 skill 重启
- 若架构师说 `standard mode` → fast lane 关闭直到下次会话或下次 explicit opt-in
- 若架构师不指示就开始下一个话题 → fast lane 默认关闭（不假设默认重启）

## audit trail 同步

每次 escape 触发：在 `features/<f>/progress.md` `## Fast Lane Decisions` 段追加一行，`escape_enabled` 列填 `yes`，`decision_content` 列写"escape #N 触发：<具体内容>"，`trigger_condition` 列写命中的具体条件。

## 与 OMO 的对比说明

OMO `todo-continuation-enforcer` + `ralph-loop` 通过 runtime hook 实现 idle 检测 / 自动唤醒；HF v0.6 在 markdown-only 路径下走宣告式：本 skill 的 6 条 escape + 3 类关键词由 host agent 自觉读取并执行。v0.7 `harnessflow-runtime` 落地后，可挂 OpenCode plugin hook 把"verdict 出现 → 检查 6 条 → 自动 dispatch 或 escape"自动化（详见 ADR-010 P1 模块 `todo-continuation-enforcer + ralph-loop`），但 markdown 路径仍可独立工作（按 ADR-010 D3 markdown 包必须独立可用）。

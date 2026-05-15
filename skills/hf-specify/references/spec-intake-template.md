# `spec.intake.md` Template & Schema

> hf-specify Interview FSM 的持久化工件。落 `features/<active>/spec.intake.md`。会话被打断后从本文件恢复 FSM 状态。

## Schema

| 段 | 必需 | 内容 |
|---|---|---|
| `Status` | yes | enum: `Interview` / `Research` / `ClearanceCheck` / `PlanGeneration` / `Done` |
| `Last Question Asked` | yes | 当前 Interview 状态下最后问出的问题（或 `n/a`）|
| `Last Question Answered At` | yes | ISO 8601 时间戳（或 `pending`）|
| `Question Trail` | yes | 表格：# / Time / State Before / Question / Answer / State After |
| `Research Trail` | yes | 表格：# / Time / Topic / Source-File / Finding |
| `Clearance Checks` | yes | 表格：# / Time / Check / Result / Action |

## 模板

```markdown
# Spec Intake — <feature-id>

- Status: <Interview | Research | ClearanceCheck | PlanGeneration | Done>
- Last Question Asked: <question text or "n/a">
- Last Question Answered At: <timestamp or "pending">

## Question Trail

| # | Time | State Before | Question | Answer | State After |
|---|---|---|---|---|---|
| 1 | 2026-05-14T11:30Z | Interview | "本 spec 主线 FR 数量预算？" | "≤ 15" | Research |
| 2 | 2026-05-14T11:35Z | Interview | "..." | "..." | ClearanceCheck |

## Research Trail

| # | Time | Topic | Source / File | Finding |
|---|---|---|---|---|
| 1 | 2026-05-14T11:32Z | "现有 spec FR 数量基线" | `features/001-install-scripts/spec.md` | "8 FR + 4 NFR" |

## Clearance Checks

| # | Time | Check | Result | Action |
|---|---|---|---|---|
| 1 | 2026-05-14T11:40Z | 核心目标已定义？ | yes | continue |
| 2 | 2026-05-14T11:40Z | 范围边界已显式？ | no | back-to-Interview Q3 |
| 3 | 2026-05-14T11:42Z | 关键决策已锁定？ | partial | back-to-Research T2 |
| 4 | 2026-05-14T11:50Z | 测试策略已确认？ | yes | continue |
| 5 | 2026-05-14T11:50Z | 无关键 ambiguity？ | yes | → PlanGeneration |
```

## 5 个 Clearance Check 项（design §4.2 默认）

| # | Check | 通过标准 |
|---|---|---|
| 1 | 核心目标已定义？ | spec.md §1 / §2 高层目标 1-2 句可表述 |
| 2 | 范围边界已显式？ | §6 范围内 / §9 Scope Out 双向闭合 |
| 3 | 关键决策已锁定？ | 触及 ADR / spec FR Priority / NFR threshold 的项有结论 |
| 4 | 测试策略已确认？ | NFR 验证字段或 Acceptance 含可机械判断的测试入口 |
| 5 | 无关键 ambiguity？ | OQ 全部标 "design / tasks 阶段决定"，无悬空 USER-INPUT 阻塞 |

任一 `no` → 回退（按 OQ-005：可回 Interview 加问题或回 Research 加查证）；任一 `partial` → reviewer 决策（继续 vs 回退）。

## 恢复协议

新会话进入 hf-specify 时：

```python
# pseudo-code
intake = read("features/<f>/spec.intake.md")
if intake.Status == "Done":
    # 跳到 hf-spec-review
    return next_skill("hf-spec-review")
elif intake.Status in {"Interview", "Research", "ClearanceCheck", "PlanGeneration"}:
    # 恢复到对应状态
    if intake.Last_Question_Answered_At == "pending":
        # 上次会话问题没收到答复 → 重新等待
        prompt(intake.Last_Question_Asked)
    else:
        # 已答复 → 推进到下一状态
        advance_from(intake.Status)
```

## fast lane 行为

`hf-ultrawork` fast lane 中 hf-specify FSM 仍按状态机走，不跳步。架构师在 Interview 状态下回答问题不算"中间确认"——是 spec 内容本身的输入，必须完整收集。fast lane 只在 `Done → hf-spec-review` 转移点接管"是否继续"决策（默认 auto-continue）。

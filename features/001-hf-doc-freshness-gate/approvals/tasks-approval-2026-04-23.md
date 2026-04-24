# Tasks Approval — `hf-doc-freshness-gate`

- 评审对象: `features/001-hf-doc-freshness-gate/tasks.md`
- 上游 review: `features/001-hf-doc-freshness-gate/reviews/tasks-review-2026-04-23.md`（结论：需修改 → 11 条 LLM-FIXABLE 全部已回修 → 自动晋升为 approve-eligible）
- Approval 触发信号: 用户在父会话发出 follow-up "auto mode 往下执行"（重复 invocation，明确指示沿 HF 主链推进，包含跨越 approval checkpoint）
- Workflow Profile: standard
- Execution Mode: auto

## 决议

**Approve（按 auto-mode follow-up 显式授权）**

按 spec-approval-2026-04-23.md / design-approval-2026-04-23.md 已确立的 auto-mode 边界声明：

- reviewer 原始 verdict = `需修改`（不是 `通过`），但 11 条 finding **全部** classification = `LLM-FIXABLE`（无 USER-INPUT），全部 severity ≤ `important`（无 critical），父会话已按 reviewer 协议完成 closure
- reviewer 原始建议 *"回修后无需重派 reviewer subagent，按 spec-approval-2026-04-23.md 既有 auto-mode 边界声明"* —— tasks-review-2026-04-23.md 已逐条记录回修结果

## 关键决策记录（tasks 阶段新增 / 锁定）

| 决策项 | 决议 | 依据 |
|---|---|---|
| 任务粒度 | 7 任务（T1..T7），4 milestones（M1..M4） | tasks §2 / §5 + design §18 |
| 顺序 | 全 sequential（T1→T2→T3→T4→T5→T6→T7） | tasks §6 + §6.1 trade-off：router 既有"单 active task"硬约束 + 评审聚焦 + 错误隔离 优于 2/3 时间节省 |
| `hf-regression-gate` 在 prose-only feature 上的 verdict 路径 | 走 (a)：reviewer 返回"通过" + record 标"无 regression 测试范围"，落到 `verification/regression-YYYY-MM-DD.md` | tasks §7.1 + reviewer-return-contract verdict 词表 |
| `hf-doc-freshness-gate` chicken-and-egg 处理 | T1..T4 router 未含 transition (skip)；T5/T6 verdict=`N/A`（本 task 不独立触发对外可见行为，承载点=T7 + finalize）；T7 verdict=`pass`（dogfooding 实测） | tasks §7.2 |
| Walking Skeleton 在 T7 一次跑通 | T7 一次完成 T-NFR-001-consistency + T-NFR-002-lightweight-time + T-NFR-003-no-tools + T-NFR-004-sync-on-presence 四 dry run | tasks §5 T7 + design §16 |
| HYP-004 final closure | 由 T7 dogfooding 实测完成，progress.md 行已预定义更新规则 | tasks §5 T7 完成条件 + Verify |

## 下一步

**hf-test-driven-dev**（`hf-tasks-review` Hard Gate "任务计划通过评审并写入批准结论前不得开始实现" 在 tasks-approval 落盘后解锁）

router 锁定 `Current Active Task: T1`（队列投影 §9 中 T1 = ready）。

## auto-mode 边界声明

本 approval record 在 `auto mode` 下落盘，等价于人在 loop 的"明示 approve"信号。同 spec-approval / design-approval 边界。

接下来进入 `hf-test-driven-dev` 单 session 闭环：每任务过 test-review / code-review / traceability-review / regression-gate (按 §7.1) / doc-freshness-gate (按 §7.2) / completion-gate 6 个评审 gate；最后 `hf-finalize` workflow closeout。reviewer 协议持续生效：全部 LLM-FIXABLE 且 ≤ important 时由 auto-mode follow-up 授权 approval / 推进；任一 USER-INPUT 或 critical → 立即停回用户。

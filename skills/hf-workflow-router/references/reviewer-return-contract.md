# Reviewer Return Contract

## 目的

这份协议定义 reviewer subagent 评审完成后，回传给父会话的最小结构化摘要。

## 最小返回格式

```json
{
  "conclusion": "通过|需修改|阻塞",
  "next_action_or_recommended_skill": "推荐下一步 canonical 节点",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": [
    "关键发现 1",
    "关键发现 2"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false
}
```

兼容说明：

- `needs_human_confirmation` 这个字段名为兼容现有 live contract 保留
- 它的运行时语义已扩大为“当前 review 通过后，还需要父会话完成 approval step”
- 父会话最终是等待真人确认，还是在 `Execution Mode=auto` 下自动落盘批准，由运行时编排决定

## 字段说明

| 字段 | 说明 |
| --- | --- |
| `conclusion` | 当前 review 的正式结论 |
| `next_action_or_recommended_skill` | reviewer 基于当前结果建议的下一步 canonical handoff |
| `record_path` | 已写入的 review 记录路径 |
| `key_findings` | 父会话需要向用户展示或用于回修的关键发现 |
| `needs_human_confirmation` | 是否必须由父会话继续完成 approval step（字段名保留兼容） |
| `reroute_via_router` | 若为 `true`，父会话应先回到 `hf-workflow-router` 重编排 |

## 使用规则

### `conclusion`

只能使用：

- `通过`
- `需修改`
- `阻塞`

### `next_action_or_recommended_skill`

优先返回 canonical `hf-*` skill ID，或保留节点：

- `hf-specify`
- `hf-spec-review`
- `规格真人确认`
- `hf-design`
- `hf-design-review`
- `设计真人确认`
- `hf-tasks`
- `hf-tasks-review`
- `任务真人确认`
- `hf-test-driven-dev`
- `hf-test-review`
- `hf-code-review`
- `hf-traceability-review`
- `hf-regression-gate`
- `hf-completion-gate`
- `hf-finalize`
- `hf-hotfix`
- `hf-increment`
- `hf-workflow-router`

这个字段是 reviewer 摘要层对仓库 canonical 字段 `Next Action Or Recommended Skill` 的结构化映射。

它必须是一个唯一的 canonical 值，不得把多个候选动作拼成一个字符串。

命名规则：

- live reviewer skills 与相关文档统一使用 `next_action_or_recommended_skill`
- reviewer 摘要必须直接返回该字段，不再使用旧字段别名

### `needs_human_confirmation`

只在 `conclusion=通过` 且当前 review 节点要求 approval step 时，才把这个字段设为 `true`。

若 `conclusion=需修改` 或 `阻塞`，默认返回 `false`，并由 `next_action_or_recommended_skill` 指向回修或重编排节点。

`conclusion=通过` 时，通常按以下约定：

| review skill | `conclusion=通过` 时默认值 |
| --- | --- |
| `hf-spec-review` | `true` |
| `hf-design-review` | `true` |
| `hf-tasks-review` | `true` |
| `hf-test-review` | `false` |
| `hf-code-review` | `false` |
| `hf-traceability-review` | `false` |

### `reroute_via_router`

以下情况建议返回 `true`：

- 当前 review 暴露出缺少上游已批准工件
- 当前输入证据与 profile / stage 明显冲突
- 当前问题本质上需要回到 `hf-workflow-router` 重新决定分支

## 父会话消费规则

父会话收到该摘要后，先检查 `references/execution-semantics.md` 中定义的暂停点与“先向用户展示”的义务，再按以下顺序处理：

1. 若 `reroute_via_router=true`，先经 `hf-workflow-router` 重编排。
2. 否则若 `conclusion=通过` 且 `needs_human_confirmation=true`：
   - `Execution Mode=interactive`：进入真人确认 / approval step
   - `Execution Mode=auto`：先写 approval record，再继续进入该 approval step 解锁后的下游节点
3. 否则若 `conclusion=通过` 且无需额外 approval step，进入 `next_action_or_recommended_skill`。
4. 否则若 `conclusion=需修改` 或 `阻塞`，按 `next_action_or_recommended_skill` 回修或补条件。

补充理解：

- 对 `hf-spec-review` / `hf-design-review`，`interactive` 模式下的 `需修改` 与内容回修型 `阻塞` 仍受暂停点约束，父会话需先向用户展示评审结论与修订重点
- 对 `hf-spec-review` / `hf-design-review`，`auto` 模式下若修订方向清楚、仍在当前范围内，可直接回到上游 skill 回修；若方向不清，仍应停止自动推进
- 对 `hf-spec-review` / `hf-design-review`，若 `阻塞` 且需要经 router 重编排，父会话需先向用户展示阻塞原因，再回到 `hf-workflow-router`
- 对其他 review / gate，若修订方向不明确，也应先与用户讨论，而不是机械自动推进

## 边界

这个 return contract 只定义“reviewer 回给父会话的摘要”，不替代 review 记录正文。

review 正文仍应按各 `hf-*review` skill 自身要求写入仓库路径——**除非**该 skill 显式允许 `record_mode=snapshot`。当前唯一允许 snapshot 的是 `hf-task-review`，且仅在 `conclusion=通过` + 无 HIGH+ findings + 项目未声明 `Audit Mode: file` 时；其余 review skill 必须保持 `record_mode=file`。

## Snapshot Mode 父会话承接规则（v0.7）

当 reviewer 返回 `record_mode=snapshot`：

1. 父会话**必须**把 ≤ 10 行 snapshot 追加到 `features/<active>/progress.md` 的 `## Task NNN Review Snapshot` 段（NNN 取当前 active task id；若 progress.md 中尚无该段则创建）
2. snapshot 必须含：task id / 三维度 score 摘要（仅 `hf-task-review`）/ verdict / 非阻塞遗留项摘要（≤ 3 条或 `none`）/ next action
3. snapshot 不重复实现交接块 / Refactor Note / 测试输出；只是路由所需最小回执
4. 不在 `features/<active>/reviews/` 下落任何文件（git history + progress.md 即审计链）
5. 若项目 `progress.md` 中 `Audit Mode: file` 显式声明 → 父会话**必须**忽略 reviewer 的 `record_mode=snapshot` 请求，要求 reviewer 重新以 `record_mode=file` 回执；这是 SOC 2 / 合规开关

`hf-completion-gate` 的 `Upstream Evidence Consumed` 段接受 snapshot 锚点（形如 `features/<active>/progress.md#task-NNN-review-snapshot`）作为 `hf-task-review` 的 evidence reference，与 file mode 的 `features/<active>/reviews/task-review-task-NNN.md` 等价处理。

## Remediation Budget 父会话承接规则（v0.7）

`hf-test-driven-dev` Hard Gate 与本契约配套：单 task 的 review → fix → re-review 循环最多 2 轮（`remediation_round_count` ∈ {1, 2}）。

父会话消费 reviewer 摘要时：

- `remediation_round_count=1` 且 `conclusion=需修改` / `阻塞`（可回实现补救）→ 进入 `hf-test-driven-dev` 回修
- `remediation_round_count=2` 且 `conclusion=需修改` / `阻塞`（可回实现补救）→ 进入 `hf-test-driven-dev` 回修；下次 review 将是第 3 轮
- `remediation_round_count=3` 时 reviewer **必须**返回 `reroute_via_router=true` 与 `next_action_or_recommended_skill=hf-workflow-router`，让 router 决定升级到 `hf-increment` / 重新拆 task / 真人介入
- 父会话在 `progress.md` `## Remediation Counters` 段维护 `| task_id | review_skill | round |` 行；进入下一 task 或 verdict 转为 `通过` 后清除该 task 的计数

该 budget 不适用于 head-of-pipeline 的 `hf-spec-review` / `hf-design-review` / `hf-tasks-review`（那些 review 的 approval step 节奏由真人/auto 模式控制，不受 budget 约束）。

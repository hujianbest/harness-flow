# 路由证据示例

这份文件提供一组轻量示例，适用于不依赖根目录 JSON 信号文件的项目。

当前建议是：不要依赖根目录 JSON 信号文件做路由。

更推荐使用以下证据来源：

- 已批准的规格 / 设计 / 任务工件
- feature `progress.md` 这类进度记录（默认 `features/<active>/progress.md`）
- `features/<active>/reviews/` 下的评审记录
- `features/<active>/verification/` 下的验证记录
- 用户明确表达的变更或热修复意图

## 推荐替代方式

### 进度记录示例

优先使用 canonical progress schema，而不是 `phase`、`next skill` 这类自由字段。

下例中的前四个 section 是 canonical core；最后的 `Approved Artifacts` 是可选扩展块，用来补充批准状态证据，不是强制固定 section：

```markdown
## Goal

- Goal: 修复默认排序方向并完成最小验证
- Owner:
- Status: In Progress
- Last Updated:

## Current Workflow State

- Current Stage: hf-test-driven-dev
- Workflow Profile: standard
- Current Active Task: TASK-003
- Pending Reviews And Gates: hf-test-review, hf-code-review, hf-traceability-review, hf-regression-gate, hf-completion-gate
- Relevant Files:
- Constraints:

## Progress Notes

- What Changed:
- Evidence Paths:
- Session Log:
- Open Risks:

## Next Step

- Next Action Or Recommended Skill: hf-test-review
- Blockers:
- Notes:

## Approved Artifacts

- Requirement Spec: 已批准
- Design Doc: 已批准
- Task Plan: 已批准
```

旧字段兼容提醒：

- `phase` -> `Current Stage`
- `活跃任务` / `Current Task` -> `Current Active Task`
- `next skill` / `Next Action` -> `Next Action Or Recommended Skill`

这些旧字段只应用于读取旧工件时的归一化判断，不应继续写回到新的 HF progress 记录中。

### 变更请求示例

```markdown
## 变更摘要

- requested by:
- requested at:
- summary:

## 影响范围

- requirement spec
- design doc
- task plan
```

### 热修复请求示例

```markdown
## 热修复摘要

- severity:
- summary:
- expected behavior:
- actual behavior:
- impact:
```

## 推荐处理规则

1. 优先更新现有项目工件，而不是新增额外路由文件
2. 让路由证据尽量靠近它描述的交付物
3. 避免保留会误导路由的过期旁路触发文件

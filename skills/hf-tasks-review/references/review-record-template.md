# Tasks Review Record Template

## 保存路径

默认：`features/<active>/reviews/tasks-review-YYYY-MM-DD.md`

若 项目声明了等价路径，按映射保存。

## 记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][TR2|TR6|TA3] 问题

## 缺失或薄弱项

- 条目

## 下一步

- `通过`：`任务真人确认`
- `需修改`：`hf-tasks`
- `阻塞`：`hf-tasks` 或 `hf-workflow-router`

## 记录位置

- `features/<active>/reviews/tasks-review-YYYY-MM-DD.md` 或映射路径

## 交接说明

- `任务真人确认`：仅当结论为 `通过`；interactive 下等待真人，auto 下写 approval record
- `hf-tasks`：用于所有需要回修任务计划内容的场景
- `hf-workflow-router`：仅在 route / stage / 证据链冲突时使用
```

## 结构化返回 JSON

正常返回示例：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-tasks",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["[important][LLM-FIXABLE][TR2] 首个关键任务缺少 Acceptance 和 Verify"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR2",
      "summary": "首个关键任务缺少 Acceptance 和 Verify"
    }
  ]
}
```

Precheck blocked 示例：

```json
{
  "conclusion": "阻塞",
  "next_action_or_recommended_skill": "hf-workflow-router",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["任务评审输入证据冲突：设计 approval evidence 不稳定"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

## 返回规则

| 结论 | next_action | needs_human_confirmation | reroute_via_router |
|------|------------|------------------------|-------------------|
| `通过` | `任务真人确认` | true | false |
| `需修改` | `hf-tasks` | false | false |
| `阻塞`（内容回修） | `hf-tasks` | false | false |
| `阻塞`（route/stage冲突） | `hf-workflow-router` | false | true |

Precheck blocked 沿用 `阻塞` 返回规则，区别只是跳过正式 checklist。

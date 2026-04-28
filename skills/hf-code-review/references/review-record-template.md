# Code Review Record Template

## 保存路径

默认：`features/<active>/reviews/code-review-task-NNN.md`

若 项目声明了等价路径，按映射保存。

## 记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][CR2|CR5|CR7|CR7.3|CA3|CA8] 问题

## 代码风险与薄弱项

- 条目

## 下一步

- `通过`：`hf-traceability-review`
- `需修改`：`hf-test-driven-dev`
- `阻塞`：`hf-test-driven-dev` 或 `hf-workflow-router`
```

## 结构化返回 JSON

正常返回示例：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["[important][LLM-FIXABLE][CR2] 通知逻辑耦合在 handler 层，偏离已批准边界"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR2",
      "summary": "通知逻辑耦合在 handler 层，偏离已批准边界"
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
  "key_findings": ["code review 输入证据冲突：实现交接块与上游状态不一致"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

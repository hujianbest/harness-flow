# Test Review Record Template

## 保存路径

默认：`features/<active>/reviews/test-review-task-NNN.md`

若 项目声明了等价路径，按映射保存。

## 记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][TT1|TT5|TA2] 问题

## 缺失或薄弱项

- 条目

## 下一步

- `通过`：`hf-code-review`
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
  "key_findings": ["[important][LLM-FIXABLE][TT1] 当前 RED 证据无效，测试一跑就绿"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "TT1",
      "summary": "当前 RED 证据无效，测试一跑就绿"
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
  "key_findings": ["test review 输入证据冲突：实现交接块与 task-progress 状态不一致"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

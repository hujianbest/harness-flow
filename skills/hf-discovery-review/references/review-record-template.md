# 评审记录模板

## 记录格式

评审完成后，将结论写入：

- `docs/reviews/discovery-review-<topic>.md`（discovery 阶段 feature 尚未创建，仍按长期资产存放在 `docs/reviews/`；进入 feature 后续 review 落到 `features/<active>/reviews/`）
- 如 项目声明了等价路径，按映射路径保存

## 评审记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][P1|W2|B1] 问题

## 薄弱或缺失的 discovery 点

- 条目

## 下一步

- `通过`：`hf-specify`
- `需修改`：`hf-product-discovery`
- `阻塞`：`hf-product-discovery` 或 `hf-workflow-router`
```

## 结构化返回（JSON）

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-product-discovery",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["[important][LLM-FIXABLE][B2] 缺少可冷读的 bridge-to-spec，小节未说明哪些结论足以进入 hf-specify。"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "B2",
      "summary": "缺少 bridge-to-spec 小节，无法稳定 handoff 到 hf-specify"
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
  "key_findings": ["discovery review 输入证据冲突：当前阶段与 task-progress 记录不一致"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

## 返回规则

| 结论 | next_action | needs_human_confirmation | reroute_via_router |
|------|------------|------------------------|-------------------|
| `通过` | `hf-specify` | false | false |
| `需修改` | `hf-product-discovery` | false | false |
| `阻塞`（内容） | `hf-product-discovery` | false | false |
| `阻塞`（workflow） | `hf-workflow-router` | false | true |

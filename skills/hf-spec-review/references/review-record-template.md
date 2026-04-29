# Spec Review 记录模板

## 保存路径

默认：`features/<active>/reviews/spec-review-YYYY-MM-DD.md`

若 项目声明了等价路径，按映射保存。

若项目无固定格式，按本文件下方"记录结构"段使用即可。

## 结论字段映射

若使用英文字段：
- `通过` → `pass`
- `需修改` → `revise`
- `阻塞` → `blocked`

## 记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][Q1|A2|C3|G1|G2|G3|GS1] 问题

## 缺失或薄弱项

- 条目

## 下一步

- `通过`：`规格真人确认`
- `需修改`：`hf-specify`
- `阻塞`：`hf-specify` 或 `hf-workflow-router`

## 记录位置

- `features/<active>/reviews/spec-review-YYYY-MM-DD.md` 或映射路径

## 交接说明

- `规格真人确认`：仅当结论为 `通过`；interactive 下等待真人，auto 下写 approval record
- `hf-specify`：用于所有需要回修规格内容的场景
- `hf-workflow-router`：仅在 route / stage / 证据链冲突时使用
```

## 结构化返回 JSON

正常返回示例：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["[important][USER-INPUT][Q2] 响应时间缺少可验证阈值"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "USER-INPUT",
      "rule_id": "Q2",
      "summary": "响应时间缺少可验证阈值"
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
  "key_findings": ["当前没有稳定 spec draft，且 stage/approval evidence 冲突"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

## 返回规则

| 结论 | next_action | needs_human_confirmation | reroute_via_router |
|------|------------|------------------------|-------------------|
| `通过` | `规格真人确认` | true | false |
| `需修改` | `hf-specify` | false | false |
| `阻塞`(内容回修) | `hf-specify` | false | false |
| `阻塞`(route/stage冲突) | `hf-workflow-router` | false | true |

Precheck blocked 沿用 `阻塞` 返回规则，区别只是跳过正式 rubric。

## 状态同步

若使用 feature `progress.md` 且 approval step 已完成，同步更新：
- 规格文档状态字段
- feature `progress.md` Current Stage
- feature `progress.md` Next Action Or Recommended Skill

这些更新由父会话在 approval step 完成后执行；reviewer subagent 不代替父会话写入批准结论。

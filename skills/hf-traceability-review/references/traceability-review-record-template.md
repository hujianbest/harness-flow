# HF 可追溯性评审记录模板

## 保存路径

默认：`features/<active>/reviews/traceability-review.md`（全 feature 一次性 review；如同一 feature 内多次复审，追加日期或序号后缀）

若 项目声明了等价路径，按映射保存。

## 记录结构

```markdown
## 评审范围

- topic / 任务：
- 相关需求：
- 相关设计：
- 相关任务：
- 相关实现：
- 相关测试 / 验证：

## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][TZ2|TZ5|ZA3] 问题

## 链接矩阵

- Spec -> Design:
- Design -> Tasks:
- Tasks -> Impl:
- Impl -> Test / Verification:

## 追溯缺口

- 缺口

## 需要回写或同步的工件

- 工件：
  - 原因：
  - 建议动作：

## 下一步

- `通过`：`hf-regression-gate`
- `需修改`：`hf-test-driven-dev`
- `阻塞`：`hf-workflow-router`
```

## 结构化返回 JSON

正常返回示例：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["[important][LLM-FIXABLE][TZ5] 新增告警行为未回写到任务或设计工件"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "TZ5",
      "summary": "新增告警行为未回写到任务或设计工件"
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
  "key_findings": ["traceability review 输入证据冲突：规格与设计版本不一致"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

# 评审记录模板

## 记录格式

评审完成后，将结论写入：

- `features/<active>/reviews/design-review-YYYY-MM-DD.md`
- 如 项目声明了等价路径，按映射路径保存

若项目尚未形成固定 review 记录格式，默认使用当前模板。

## 评审记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][D1|D3|A2] 问题

## 薄弱或缺失的设计点

- 条目

## 下一步

- `通过`：`设计真人确认`
- `需修改`：`hf-design`
- `阻塞`：`hf-design` 或 `hf-workflow-router`

## 记录位置

- `features/<active>/reviews/design-review-YYYY-MM-DD.md` 或映射路径

## 交接说明

- `设计真人确认`：仅当结论为 `通过`；`interactive` 下等待真人，`auto` 下由父会话写 approval record
- `hf-design`：用于所有需要回修设计内容的场景
- `hf-workflow-router`：仅在需求漂移、route / stage / 证据链冲突时使用
```

## 结构化返回（JSON）

正常返回示例：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-design",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["[important][LLM-FIXABLE][D3] 候选方案对比不足，trade-off 无法冷读"],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "D3",
      "summary": "候选方案对比不足，trade-off 无法冷读"
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
  "key_findings": ["设计评审输入证据冲突：规格 approval evidence 不稳定"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

`next_action_or_recommended_skill` 必须只写一个 canonical 值，不得拼多个候选。

## 返回规则

| 结论 | next_action | needs_human_confirmation | reroute_via_router |
|------|------------|------------------------|-------------------|
| `通过` | `设计真人确认` | true | false |
| `需修改` | `hf-design` | false | false |
| `阻塞`（设计内容回修） | `hf-design` | false | false |
| `阻塞`（需求漂移/规格冲突） | `hf-workflow-router` | false | true |

Precheck blocked 沿用 `阻塞` 返回规则，区别只是跳过正式 checklist。

## 状态同步

如果使用 feature `progress.md` 驱动 workflow，approval step 完成后由父会话同步更新：

- 设计文档中的状态字段
- feature `progress.md` 中的 `Current Stage`
- feature `progress.md` 中的 `Next Action Or Recommended Skill`

reviewer subagent 不代替父会话写入批准结论。

## 结论判定规则

- **通过**：可追溯到已批准规格、关键决策和接口足够清晰、约束和 NFR 被吸收、无阻塞任务规划的设计空洞
- **需修改**：核心设计可用，但有局部缺口、决策说明不足、接口偏弱、测试准备度不足，可通过一轮定向修订补齐
- **阻塞**：设计无法清晰支撑需求规格、存在无法追溯的关键新增内容、关键架构决策缺失、或 route/stage/证据链冲突

## Severity 等级

- `critical`：阻塞任务规划，或会直接导致错误任务输入
- `important`：应在批准前修复
- `minor`：不阻塞，但建议改进

## Finding 分类

- `USER-INPUT`：缺失外部阈值、未确认业务裁决、关键 trade-off 仍需真人拍板、规格未批准却引入关键新增能力
- `LLM-FIXABLE`：方案对比不足、边界或接口说明不足、task planning readiness 未显式写清、测试策略未整理成文

## Finding 写法对比

✅ 具体：`[important][LLM-FIXABLE][D3] 候选方案只有结论没有 trade-off，对为什么不选事件驱动方案不可冷读。`
❌ 模糊：`需要更好的架构说明`

✅ 具体：`[critical][LLM-FIXABLE][D5] 支付回调与订单状态同步边界未闭合，hf-tasks 无法稳定拆解首批任务。`
❌ 模糊：`任务规划准备度不足`

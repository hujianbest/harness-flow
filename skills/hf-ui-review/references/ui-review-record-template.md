# UI 评审记录模板

## 记录格式

评审完成后，将结论写入：

- `features/<active>/reviews/ui-review-YYYY-MM-DD.md`
- 如 项目声明了等价路径，按映射路径保存

若项目尚未形成固定 review 记录格式，默认使用当前模板。

## 评审记录结构

```markdown
## 结论

通过 | 需修改 | 阻塞

## 发现项

- [critical|important|minor][USER-INPUT|LLM-FIXABLE][U1|U5|AU3] 问题

## 薄弱或缺失的 UI 设计点

- 条目

## 与 hf-design 的 peer 交接一致性

- 已对齐：条目
- 不一致：条目（附处置建议）
- 本文档已锁、可供 peer 依赖：条目

## 下一步

- `通过`：`设计真人确认`（等待与 hf-design-review 汇合进入联合 approval）
- `需修改`：`hf-ui-design`
- `阻塞`：`hf-ui-design` 或 `hf-workflow-router`

## 记录位置

- `features/<active>/reviews/ui-review-YYYY-MM-DD.md` 或映射路径

## 交接说明

- `设计真人确认`：仅当结论为 `通过`；需等 `hf-design-review` 也通过才由父会话发起联合 approval
- `hf-ui-design`：用于所有需要回修 UI 设计内容的场景
- `hf-workflow-router`：仅在需求漂移、UI surface 激活条件判定错误、peer 不可协调、route / stage / 证据链冲突时使用
```

## 结构化返回（JSON）

正常返回示例：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-ui-design",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": [
    "[critical][LLM-FIXABLE][U5] 全部 error 态仅使用红色，违反 WCAG 1.4.1，缺图标+文案+aria-describedby",
    "[important][LLM-FIXABLE][U3] 搜索结果列表缺 partial 与 offline 态"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "critical",
      "classification": "LLM-FIXABLE",
      "rule_id": "U5",
      "summary": "全部 error 态仅使用红色，违反 WCAG 1.4.1"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "U3",
      "summary": "搜索结果列表缺 partial 与 offline 态"
    }
  ]
}
```

通过时示例：

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "设计真人确认",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": [],
  "needs_human_confirmation": true,
  "reroute_via_router": false
}
```

Precheck blocked 示例（激活条件判定错误）：

```json
{
  "conclusion": "阻塞",
  "next_action_or_recommended_skill": "hf-workflow-router",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["规格未声明 UI surface，但本次 review 被激活：属 route 激活条件判定错误"],
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

Precheck blocked 示例（缺草稿）：

```json
{
  "conclusion": "阻塞",
  "next_action_or_recommended_skill": "hf-ui-design",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["UI 设计草稿路径不存在或不可读"],
  "needs_human_confirmation": false,
  "reroute_via_router": false
}
```

`next_action_or_recommended_skill` 必须只写一个 canonical 值，不得拼多个候选。

## 返回规则

| 结论 | next_action | needs_human_confirmation | reroute_via_router |
|------|------------|------------------------|-------------------|
| `通过` | `设计真人确认` | true | false |
| `需修改` | `hf-ui-design` | false | false |
| `阻塞`（UI 设计内容回修） | `hf-ui-design` | false | false |
| `阻塞`（需求漂移/规格冲突/激活条件判定错/peer 不可协调） | `hf-workflow-router` | false | true |

Precheck blocked 沿用 `阻塞` 返回规则，区别只是跳过正式 checklist。

## 联合 approval 说明

`hf-ui-review` 与 `hf-design-review` **各自独立返回**。父会话（或 router）汇总：

- 两者均 `通过` → 进入 `设计真人确认`
- 任一 `需修改` / `阻塞`（内容回修） → 回对应起草 skill；另一方可继续其稳定部分，但 approval 不解锁
- 任一 `阻塞`（reroute_via_router=true） → router 重新判断，可能停止另一条的 approval 等待

reviewer subagent 不代替父会话做联合 approval 判断。

## 状态同步

如果使用 feature `progress.md` 驱动 workflow，approval step 完成后由父会话同步更新：

- UI 设计文档中的状态字段
- `hf-design` 文档中的状态字段
- feature `progress.md` 中的 `Current Stage`
- feature `progress.md` 中的 `Next Action Or Recommended Skill`

reviewer subagent 不代替父会话写入批准结论。

## 结论判定规则

- **通过**：可追溯已批准规格、UI 决策清晰、IA/流/状态矩阵完整、Design Token 合规、a11y 达标、peer 交接块显式、无阻塞任务规划的 UI 空洞
- **需修改**：核心 UI 设计可用，但有局部缺口、决策说明不足、状态覆盖偏弱、a11y 声明不全、peer 交接块含糊，可通过一轮定向修订补齐
- **阻塞**：UI 设计无法清晰支撑规格、存在无法追溯的关键新增 UI surface、关键 a11y 项系统性未达标、peer 交接块与 `hf-design` 不可协调、激活条件判定错误、或 route / stage / 证据链冲突

## Severity 等级

- `critical`：阻塞任务规划、引入 a11y 隐患、或会直接导致错误任务输入
- `important`：应在批准前修复
- `minor`：不阻塞，但建议改进

## Finding 分类

- `USER-INPUT`：品牌/视觉方向需真人拍板、目标设备/语种未确认、关键 UX trade-off 仍需业务侧裁决、规格未批准却引入关键新增 UI 能力
- `LLM-FIXABLE`：候选方向对比不足、状态矩阵不全、a11y 声明含糊、Design Token 映射缺失、组件映射缺来源/依赖、peer 交接块含糊

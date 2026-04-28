# df Reviewer Dispatch Protocol

> 配套 `df-workflow-router/SKILL.md`。规定 df 中 review 节点如何派发独立 reviewer subagent，以及 reviewer 返回结果的契约。

## 角色边界

df 的 review 节点（spec-review / component-design-review / ar-design-review / test-checker / code-review）必须由**独立 reviewer 角色或 subagent** 执行，理由：

- df-soul 要求**不自我验收**
- author 与 reviewer 必须分离，避免确认偏差
- reviewer 不修改被评审工件、不补写测试、不替代代码实现

## Dispatch Request 最小字段

派发 reviewer subagent 时，父会话（router 或上游 leaf）必须传入：

- `target_skill`：`df-spec-review` / `df-component-design-review` / `df-ar-design-review` / `df-test-checker` / `df-code-review`
- `work_item_type`：`AR` / `DTS` / `CHANGE`
- `work_item_id`
- `owning_component`
- `workflow_profile`：`standard` / `component-impact` / `hotfix` / `lightweight`
- `primary_artifact`：被评审对象的路径与版本锚点（commit / 分支）
- `supporting_context`：上游工件路径列表，例如：
  - spec-review：`features/<id>/requirement.md`
  - component-design-review：`features/<id>/requirement.md` + 当前 `docs/component-design.md` + 受影响 SR / AR
  - ar-design-review：`features/<id>/requirement.md` + `features/<id>/ar-design-draft.md` + `docs/component-design.md`
  - test-checker：`features/<id>/ar-design-draft.md`（含测试设计章节）+ `features/<id>/evidence/unit/`、`features/<id>/evidence/integration/` + `features/<id>/implementation-log.md`
  - code-review：上述全部 + 代码 diff + `features/<id>/reviews/test-check.md`
- `agents_md_anchor`：项目 `AGENTS.md` 中相关约定路径（编码规范、静态分析配置、模板覆盖路径）
- `expected_record_path`：默认见 `df-workflow-shared-conventions.md`，项目覆写优先

reviewer subagent 不得读取 dispatch request 之外的全量代码库；只读最少必要内容。

## Reviewer 返回契约

reviewer 必须返回结构化摘要 + 落盘 review record。最小字段：

```yaml
target_skill:                 # 与 dispatch 一致
work_item_id:
owning_component:
record_path:                  # 已落盘 review record 的路径
conclusion: 通过 | 需修改 | 阻塞
verdict_rationale:            # 1-3 行
key_findings:                 # 数组，含 severity / classification / rule_id / anchor / 描述
finding_breakdown:
  critical: <count>
  important: <count>
  minor: <count>
next_action_or_recommended_skill:   # 唯一 canonical df-* 节点名
needs_human_confirmation: true | false
reroute_via_router: true | false
```

约束：

- `next_action_or_recommended_skill` 只能写一个 canonical 值；不得拼接多个候选
- 若问题本质属于 stage / route / profile 冲突，必须 `reroute_via_router=true` 且 `next_action_or_recommended_skill=df-workflow-router`
- `通过` + `needs_human_confirmation=true`：父会话需让对应团队角色（开发负责人 / 模块架构师 / 需求负责人）确认后才能进入下一节点
- reviewer **不允许**返回 `通过` 同时给出 critical findings

## Verdict 与下一步映射

| Reviewer | 通过 | 需修改 | 阻塞（内容） | 阻塞（workflow） |
|---|---|---|---|---|
| `df-spec-review` | `df-component-design`（component-impact）/ `df-ar-design` | `df-specify` | `df-specify` | `df-workflow-router` |
| `df-component-design-review` | `df-ar-design` | `df-component-design` | `df-component-design` | `df-workflow-router` |
| `df-ar-design-review` | `df-tdd-implementation` | `df-ar-design` | `df-ar-design` | `df-workflow-router` |
| `df-test-checker` | `df-code-review` | `df-tdd-implementation` | `df-tdd-implementation` | `df-workflow-router` |
| `df-code-review` | `df-completion-gate` | `df-tdd-implementation` | `df-tdd-implementation` | `df-workflow-router` |

## Severity 与 Classification

每条 finding 必须含：

- `severity`：`critical` / `important` / `minor`
- `classification`：`USER-INPUT` / `LLM-FIXABLE` / `TEAM-EXPERT`
- `rule_id`：reviewer 所在 skill 的 rubric 编号

分类约定：

- `USER-INPUT`：缺业务事实 / 外部决策 / 优先级冲突，需要团队负责人或需求负责人拍板
- `LLM-FIXABLE`：缺 wording、章节、示例、明显逻辑漏洞，可由开发人员 1-2 轮定向回修
- `TEAM-EXPERT`：需要模块架构师 / 资深嵌入式工程师专业判断（组件边界、SOA 接口、并发 / 实时性 / 内存模型选择）

## Hard Constraints

- reviewer 不修改被评审工件
- reviewer 不补写测试 / 不写代码 / 不改 AR 设计
- reviewer 不返回多个候选下一步
- reviewer 不绕过 record path（口头结论无效）
- reviewer 不替团队角色拍板

违反任一条 → reviewer 返回结果视为无效，由 router 重新派发。

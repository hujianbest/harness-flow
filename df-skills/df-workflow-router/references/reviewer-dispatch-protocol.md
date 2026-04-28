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
- `work_item_type`：`SR` / `AR` / `DTS` / `CHANGE`
- `work_item_id`
- `owning_component`：AR / DTS / CHANGE 必填
- `owning_subsystem`：SR 必填
- `workflow_profile`：`requirement-analysis` / `standard` / `component-impact` / `hotfix` / `lightweight`
- `primary_artifact`：被评审对象的路径与版本锚点（commit / 分支）
- `supporting_context`：上游工件路径列表（按目标 skill 与 work item 类型）：
  - spec-review（任何 work item）：`features/<id>/requirement.md`
  - component-design-review（SR-analysis 或 AR component-impact）：`features/<id>/requirement.md` + `features/<id>/component-design-draft.md` + 当前 `docs/component-design.md`
  - ar-design-review（**仅** AR / DTS / CHANGE）：`features/<id>/requirement.md` + `features/<id>/ar-design-draft.md` + `docs/component-design.md`
  - test-checker（**仅** AR / DTS / CHANGE）：`features/<id>/ar-design-draft.md`（含测试设计章节）+ `features/<id>/evidence/unit/`、`features/<id>/evidence/integration/` + `features/<id>/implementation-log.md`
  - code-review（**仅** AR / DTS / CHANGE）：上述全部 + 代码 diff + `features/<id>/reviews/test-check.md`
- `agents_md_anchor`：项目 `AGENTS.md` 中相关约定路径（编码规范、静态分析配置、模板覆盖路径）
- `expected_record_path`：默认见 `docs/df-shared-conventions.md`，项目覆写优先

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

`通过` 后的下一步取决于 work item 的 `workflow_profile`。下表分子街区列出。

### 需求分析子街区（profile = `requirement-analysis`，仅 SR）

| Reviewer | 通过 | 需修改 | 阻塞（内容） | 阻塞（workflow） |
|---|---|---|---|---|
| `df-spec-review` | `df-component-design`（SR 触发组件设计修订）/ `df-finalize`（仅澄清，无组件设计修订；写 analysis closeout） | `df-specify` | `df-specify` | `df-workflow-router` |
| `df-component-design-review` | `df-finalize`（写 analysis closeout） | `df-component-design` | `df-component-design` | `df-workflow-router` |

SR-flow 中 `df-ar-design-review` / `df-test-checker` / `df-code-review` 不应被派发；如果发生，`df-workflow-router` 应在派发前拦截，或 reviewer 返回 `阻塞`(workflow) + `reroute_via_router=true`。

### 实现子街区（profile = `standard` / `component-impact` / `hotfix` / `lightweight`）

| Reviewer | 通过 | 需修改 | 阻塞（内容） | 阻塞（workflow） |
|---|---|---|---|---|
| `df-spec-review` | `df-component-design`（component-impact）/ `df-ar-design`（其余） | `df-specify` | `df-specify` | `df-workflow-router` |
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

## 定向回修协议（Directed-Rework Protocol）

reviewer 给出 `需修改` / `阻塞`（内容）verdict 后，回到上游 authoring 节点（`df-specify` / `df-component-design` / `df-ar-design` / `df-tdd-implementation`）做**定向回修**——不重新发散整份草稿。本节适用所有 df review 节点。

### 按 finding classification 处理

| Classification | 定向回修动作 | 不允许的反模式 |
|---|---|---|
| `LLM-FIXABLE` | authoring 节点只修 finding 直接指向的 row / 章节 / 字段；不重新组织无关内容；改完直接派发 reviewer 复审 | 借机重写整份规格 / 设计；顺手新增非 finding 指向的内容 |
| `USER-INPUT` | authoring 节点只问 finding 中明确缺失的业务事实 / 阈值 / 优先级 / 来源；其它部分先按现状保留 | 借机重新做整轮澄清；把所有 Open Questions 一起抛给用户 |
| `TEAM-EXPERT` | authoring 节点把问题封装成 1-2 个具体技术问题上抛模块架构师 / 资深嵌入式工程师；不在本节点自行决定 | 在本节点替模块架构师拍板组件边界 / SOA 接口 / 并发模型 |

### 处理混合 findings 的顺序

当一次 review 同时包含多种 classification 时：

1. 先收集 USER-INPUT + TEAM-EXPERT 上抛的回答（合并到同一回合问，避免来回打扰用户）
2. 再统一回修 LLM-FIXABLE
3. 一起重新派发 reviewer，**不**多次小批量复审

### Interactive vs Auto

| Execution Mode | 行为 |
|---|---|
| `interactive` | 只向用户展示**必须由用户回答**的项（USER-INPUT、需要确认的 TEAM-EXPERT 上抛结论）；LLM-FIXABLE 直接修不展示 |
| `auto` | 按团队 `AGENTS.md` 声明的 auto policy 处理；USER-INPUT 项不允许凭空补，必须 `阻塞`(workflow) 回 router；TEAM-EXPERT 项需写入 approval record 并停下等待 |

### 单次回合最小问询规则

- 一次回合中，向用户提的 USER-INPUT 问题数量上限：**5**（更多 → 说明本轮 reviewer 已暴露规格根本缺口，应回 `df-specify` 重做澄清）
- 同一决策面（同一组件 / 同一接口 / 同一 NFR）的多个问题应**合并为一个编号**，不分散提问
- 用户简短回复（一两个字 / 是否）→ authoring 节点先复述理解请求确认，再落到 row / 章节
- 不允许把整份 reviewer rubric / JSON 原样粘给用户

### 反复循环阻断规则

- 同一 work item 的同一 reviewer 节点连续 **2 轮 reviewer 循环**仍未引入新的 USER-INPUT 答复 / TEAM-EXPERT 决议 → 不再静默反复修文，authoring 节点必须显式向用户展示「还差哪些 USER-INPUT / TEAM-EXPERT 决策才能继续」并停下
- 如果反复循环的根因是 stage / route / profile 冲突 → 不在 authoring 节点硬修，回 `df-workflow-router` 重新分流

### 禁止项

- 不要在 authoring 节点请求 approval step；approval 只发生在 reviewer 返回「通过」之后由父会话发起
- 不要把 LLM-FIXABLE finding 抛给用户回答
- 不要把回修当成机会重写未受影响的章节
- 不要在同一回合既改 LLM-FIXABLE 又问 USER-INPUT 又上抛 TEAM-EXPERT，混淆责任边界——按上面顺序分步走

## Hard Constraints

- reviewer 不修改被评审工件
- reviewer 不补写测试 / 不写代码 / 不改 AR / 组件设计
- reviewer 不返回多个候选下一步
- reviewer 不绕过 record path（口头结论无效）
- reviewer 不替团队角色拍板

违反任一条 → reviewer 返回结果视为无效，由 router 重新派发。

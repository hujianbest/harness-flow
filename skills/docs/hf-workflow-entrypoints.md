# HF Workflow Entrypoints

## Purpose

本文定义 `hf-*` family 的入口策略，回答三个问题：

1. 什么时候先走 `using-hf-workflow`
2. 什么时候应直接交给当前 runtime router `hf-workflow-router`
3. 什么时候允许 direct invoke 某个具体 `hf-*` skill

## One-Line Rule

新会话默认先走 `using-hf-workflow`。

若当前已经进入 runtime recovery、需要 authoritative route / stage / profile 判断，或 evidence 冲突，则交给当前 router `hf-workflow-router`。

direct invoke 不是主路径替代品，而是在“当前节点已经足够明确、前置条件已经满足、且 route / stage / profile 不存在冲突”时允许使用的受控捷径。

如果用户显式要求 `auto` / 自动执行，把它视为 `Execution Mode` 偏好一起带入选定入口；不要把它误写成新的 profile，也不要把它当成跳步理由。

## Boundary With Product Discovery

在进入 HF coding workflow family 之前，先判断当前问题是否其实仍属于上游 product discovery。

以下场景不要直接进入 coding family，而应先由 `using-hf-workflow` 分流到：

- `hf-product-discovery`

典型信号：

- 用户还在问“这个产品值不值得做”
- 用户还在问“为什么现在的方向没有吸引力”
- 用户还在问“应该先打哪个 wedge / concept / opportunity”
- 用户还在问“先验证哪个假设、先跑什么 probe”

只有当当前请求已经主要转为“把方向写成正式规格、设计或任务计划”，才进入 coding family。

如果上游已经产出：

- `docs/insights/*-spec-bridge.md`

则可以把它视为进入 `hf-specify` 的高价值输入，而不是要求 coding family 从零反推产品 thesis。

## Start With `using-hf-workflow`

以下场景默认先经过 `using-hf-workflow`：

- 开始新的需求、功能、项目或一轮新工作周期
- 用户说“继续”“推进”“开始做”“先处理这个”，但当前 canonical 节点还没确定
- 用户点名某个 `hf-*` skill，但当前仍需确认它是不是合法 direct invoke
- 用户想通过 `/hf-spec`、`/hf-build`、`/hf-review`、`/hf-closeout` 这类命令意图进入 HF
- 用户明确说“auto mode”“自动执行”“不用等我确认”，但当前还没确定应该把这个模式交给哪个节点
- 用户需要 family-level 入口解释，而不是直接做 runtime recovery

理由：

- `using-hf-workflow` 是公开入口层
- 它帮助判断当前应 direct invoke 哪个 leaf skill，或何时交给 router
- 它降低新会话和命令入口的认知摩擦
- 它避免继续把公开入口层与 runtime kernel 混在同一职责里

## Go Directly To Current Router `hf-workflow-router`

以下场景不应停留在 entry layer，而应直接交给当前 runtime router `hf-workflow-router`：

- review / gate 刚完成，需要恢复后续编排
- 当前存在 route / stage / profile 不确定性
- 当前工件证据冲突
- 用户提出需求变更、范围变化、验收变化，但当前还不足以直接选定 `hf-increment`
- 用户提出紧急缺陷修复，但当前还不足以直接选定 `hf-hotfix`

理由：

- 当前 router 负责决定 `Workflow Profile`
- 当前 router 负责决定当前 canonical 节点
- 当前 router 负责在主链、increment、hotfix 之间做受控切换
- 当前 router 负责在命中 review 节点时派发 reviewer subagent

## Direct Invoke Is Allowed Only When

同时满足以下条件时，才允许 direct invoke 某个具体 skill：

1. 当前节点已经清楚，不需要再做 route / stage 判断
2. 当前请求是该 skill 的本地职责，而不是更上游或并行节点职责
3. 所需核心工件已经存在且可读
4. 没有 profile 冲突、批准状态冲突或证据冲突
5. 调用方接受“本 skill 只完成本节点职责，后续编排仍回到父会话 / router”
6. 若用户显式指定了 `Execution Mode`，调用方会把该模式偏好传给目标 skill，而不是在 direct invoke 前丢失它

若任一条件不满足，交给 `hf-workflow-router`。

## Entrypoint Matrix

| 节点类别 | 代表 skill | 典型入口条件 | 不该这样进入的典型情况 |
|---|---|---|---|
| Upstream discovery authoring | `hf-product-discovery` | 仍在判断产品 thesis、wedge、probe 或是否值得做 | 已明确进入 formal spec / design / task planning，且 coding family 前置条件已满足 |
| Public Entry | `using-hf-workflow` | 新会话、命令入口、family discovery、需要判断 direct invoke 还是 route-first | 当前已经进入 runtime recovery、需要 authoritative route / stage / profile 判断 |
| Orchestrator | `hf-workflow-router` | 阶段不清、需要恢复编排、需要判断 profile 或下一步 | 把它当成每次新会话都必须直接暴露给用户的 public shell |
| Authoring | `hf-product-discovery` / `hf-specify` / `hf-design` / `hf-ui-design` / `hf-tasks` | 当前明确是在补齐 discovery、规格、设计（架构或 UI）或任务计划正文；上游前置条件满足 | 阶段不清、其实该做 review、其实该走支线、或已进入实现 |
| Review | `hf-discovery-review` / `hf-spec-review` / `hf-design-review` / `hf-ui-review` / `hf-tasks-review` / downstream reviews | 当前明确是 review-only，请求和工件都指向一个具体 review 节点 | 没有可评审草稿 / 记录、其实需要继续产出正文、或 route / stage 冲突 |
| Implementation | `hf-test-driven-dev` | 已有唯一活跃任务，且任务计划已批准，或已有 hotfix handoff / 回流 findings | 无唯一活跃任务、批准状态冲突、其实要做 review / gate |
| Standalone experience capture | `hf-bug-patterns` | AI 发现重复错误、recurring review finding、hotfix 教训或用户要求把经验固化成 bug pattern | 把它当成 `hf-test-review` 前的 mandatory gate、把它写成 canonical next action，或在没有历史证据时强行固化 |
| Gates | `hf-regression-gate` / `hf-completion-gate` | 上游记录已落盘，当前就是要跑正式门禁 | 缺上游 handoff / verification 输入、缺环境、其实该回到实现或 router |
| Finalize | `hf-finalize` | completion gate 已允许收尾，且当前请求明确是在做 finalize 级状态 / 文档 / release 收口 | 仍需补实现或补验证、gate 记录缺失、closeout 输入不稳定，或其实还没到收尾阶段 |
| Branch analysis | `hf-hotfix` / `hf-increment` | 问题明确属于 hotfix 或 increment，且当前要做分支分析与 re-entry，而不是直接改代码 | 阶段不清、输入证据冲突、其实已经明确进入实现，或关键前置工件仍不存在 |

## Special Rule For Review Skills

review skills 有双重入口语义：

- direct invoke：用户明确要求“review 这份 spec/design/tasks/tests/code/traceability”，调用方可直接把当前工作视为某个 review 节点
- chain invoke：router 或父会话已经判定当前 canonical 节点是某个 review 节点

差异：

- direct invoke 时，调用方需要自己先确认这真的是 review-only 场景
- 无论是 direct invoke 还是 chain invoke，review 的实际执行都仍遵循当前 skill pack 中 `hf-workflow-router/references/review-dispatch-protocol.md`：由父会话构造 review request，并派发 reviewer subagent（旧工件若仍引用 legacy 安装路径下的同文件，语义等价，按读时归一化理解即可）
- 无论哪种模式，review skill 只负责给出 review 记录与结构化摘要，不负责推进主链

## Public Entry Mode vs Router Mode vs Direct Invoke

| 维度 | Public entry 模式 | Router 编排模式 | Direct invoke 模式 |
|---|---|---|---|
| 目标 | 判断当前应 direct invoke 哪个 leaf skill，或交给 router | 决定当前应该进入哪个节点 | 完成某一个已经明确的节点职责 |
| 最小输入 | 用户请求 + 最少 family entry context + 显式 `Execution Mode` 信号（若有） | 用户请求 + `AGENTS.md` + 上游工件状态 + `task-progress.md` + review / gate / verification / approval 证据 | 当前节点所需最小工件 + 当前请求 + 显式 `Execution Mode` 信号（若有） |
| 是否判断 profile | 否；若需要 authoritative 判断，交给 router | 是 | 否；若 profile 不清，回 router |
| 是否处理 `Execution Mode` | 只负责识别并向下传递 | 是；负责归一化并约束 `interactive` / `auto` | 只消费已明确的 mode；若 mode / policy 冲突，回 router |
| 是否判断 route / stage | 只判断“需不需要 router”，不做 authoritative recovery | 是 | 否；若 route / stage 不清，回 router |
| 是否决定下一节点 | 只决定“leaf skill 还是 router” | 是 | 否；只写 canonical handoff，后续编排交回父会话 / router |
| review 如何执行 | 只判断是否可以进入某个 review 节点；一旦进入 review，实际执行仍按 review-dispatch protocol | 一旦进入 review 节点，统一由父会话按 review-dispatch protocol 派发 reviewer subagent | 与 router 模式相同；差别只在于 review 节点是由调用方直接选定，还是由上游先判定出来 |
| 输出 | 进入某个 leaf skill，或交给 `hf-workflow-router` | 当前阶段判断、选定 profile、推荐节点，并立即继续执行或命中暂停点 | 节点本地工件、状态更新、canonical handoff、必要的 review / verification record |

## Input Differences

### Public entry 应优先读取

- 用户当前请求
- 用户是否显式要求 `interactive` / `auto`
- `skills/docs/hf-workflow-entrypoints.md`
- 与入口判断直接相关的少量工件线索
- 命令 bias 或用户点名的 skill 意图

public entry 阶段不应复制 router 的 runtime 判断，也不应先做大范围代码探索。

### Router 应优先读取

- `AGENTS.md` 中与 `hf-workflow` 相关的映射、批准状态别名、profile 规则
- `AGENTS.md` 中与 `Execution Mode` 相关的默认值、禁止 auto 的范围与 approval 记录路径
- 规格 / 设计 / 任务工件的存在情况与批准状态
- `task-progress.md`
- review / verification / release artifacts
- 用户当前请求

router 阶段不应先做大范围代码探索。

### Direct invoke 应优先读取

- 当前 skill 明确要求的最小工件
- 与本节点直接相关的上游记录或 findings
- 当前请求中与本节点职责直接相关的部分
- 若用户显式指定了 `Execution Mode`，把它当作当前节点的运行上下文，而不是新的 route 证据

direct invoke 不应顺手接管 orchestrator 职责。

## Output Differences

### Public entry 输出

public entry 的最小输出是二选一：

1. 进入一个合法 leaf skill
2. 交给 `hf-workflow-router`

它不输出 runtime canonical handoff，不替代 router 的恢复编排；若用户显式指定了 `Execution Mode`，只负责把该偏好一起带入下游。

### Router 输出

router 的最小输出是：

1. 当前识别阶段
2. 选定的 `Workflow Profile`
3. 选定的 `Execution Mode`
4. 推荐的下一步 skill

随后：

- 若命中 review 节点，由父会话派发 reviewer subagent，而不是在当前上下文内联执行 review
- 否则若命中暂停点，停在父会话等待用户输入
- 否则，立即进入目标 skill

### Direct invoke 输出

direct invoke 的最小输出是当前节点的本地交付：

- 规格 / 设计 / 任务草稿
- review 记录与结构化摘要
- 实现交接块
- verification / gate 记录
- closeout pack
- canonical `Next Action Or Recommended Skill`

direct invoke 的 handoff 只表达“本节点之后推荐谁”，不替代 router 做全链路恢复编排。

## Canonical Direct Invoke Examples

- “先把产品方向、问题和 wedge 收敛清楚，不要直接写 spec” -> 可 direct invoke `hf-product-discovery`
- “先把需求梳理清楚，不要做设计” -> 可 direct invoke `hf-specify`
- “帮我 review 这份 spec 草稿” -> 若规格草稿已存在且这是 review-only 请求，可 direct invoke `hf-spec-review`
- “按 TDD 实现当前 active task” -> 若任务计划已批准且活跃任务唯一，可 direct invoke `hf-test-driven-dev`
- “这是线上 bug，先收敛 root cause 和最小修复边界” -> 可 direct invoke `hf-hotfix`
- “这是需求变更，不要改代码，先做影响分析和 re-entry” -> 若变更请求明确且关键工件可读，可 direct invoke `hf-increment`
- “completion gate 过了，帮我做收尾和 release notes” -> 若 gate 记录已落盘且当前确实是在做 closeout，可 direct invoke `hf-finalize`

## Anti-Patterns

以下做法都不算合法 direct invoke：

- 用户点名 skill，就直接执行，不核对当前阶段
- direct invoke 某个 implementation / gate skill，却没有读取最小上游工件
- 让 authoring skill 顺手决定完整下游链路
- 让 review skill 顺手开始修文档或做实现
- 让 finalize 在 gate 未通过时提前收尾
- 把 `using-hf-workflow` 写进 `Next Action Or Recommended Skill`
- 在 route / stage / profile 冲突下继续硬做当前 skill

## Practical Rule Of Thumb

若是新会话且你有一丝疑问“现在到底该从哪个 HF 入口开始”，先走 `using-hf-workflow`；若 authoritative runtime 判断仍不清，就交给 `hf-workflow-router`。

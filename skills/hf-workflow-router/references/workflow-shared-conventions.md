# HF Workflow Shared Conventions

## Purpose

本文集中收口 `hf-*` workflow family 的共享约定，避免这些规则散落在各个 skill、reference 与计划文档中。

它优先回答以下问题：

1. progress schema 应该怎么写
2. 什么算 fresh evidence
3. review / gate 的 verdict、severity 与 handoff 应该如何统一
4. `record_path`、评审记录、验证记录与状态工件应如何表达
5. 哪些旧字段只允许“读时归一化”，不允许继续写回
6. 工作目录 / worktree 隔离应如何表达与传递

## Cross-Cutting Coding Principles

HF 把 4 条 LLM coding 行为准则（Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution）作为**所有 `hf-*` skill 共同遵守的横切行为基线**，而不是一个独立的 workflow 节点。每个 skill 在自己的 `SKILL.md` 中已经吸收并体现：

1. **Think Before Coding**：进入实现前显式列出假设、未知、待澄清，不静默选定方向；多解读时回到 user 或 router。
2. **Simplicity First (YAGNI)**：只解当前轮已确认需求；"未来可能需要"显式标记为过度工程候选。
3. **Surgical Changes**：变更范围锁定到当前 task / artifact，不顺手扩展模块边界、不旁路修改无关工件。
4. **Goal-Driven Execution**：始终对齐"从 idea 到产品高质量落地"；fresh evidence 优先于"看起来在动"。

约束：

- 这些原则**不**进入 canonical schema：不写进 `Current Stage` / `Next Action Or Recommended Skill` / `Pending Reviews And Gates` / 迁移表 / reviewer return contract 的 `next_action_or_recommended_skill`。
- 这些原则**不**替代 review / gate / approval / finalize 的本地职责。
- 与项目级约定显式声明冲突时让位。
- 旧工件未显式提及这 4 条不视为违规；本节只约束新产出的 skill 行为，不强制回写历史工件。

## Canonical Progress Schema

默认 progress state 建议统一使用以下字段：

| 字段 | 含义 | 写法约定 |
|---|---|---|
| `Current Stage` | 当前 workflow 所处节点 | 新工件优先直接写 canonical 节点名 |
| `Workflow Profile` | 当前 workflow 密度 | 仅使用 `full` / `standard` / `lightweight` |
| `Execution Mode` | 当前 workflow 的交互 / 自动推进方式 | 仅使用 `interactive` / `auto` |
| `Current Active Task` | 当前唯一活跃任务 | 必须可唯一指向一个任务；未锁定时留空或写项目约定占位值 |
| `Pending Reviews And Gates` | 仍未完成的 review / gate 节点 | 用 canonical 节点名列出剩余链路；若存在多个待恢复节点，保留完整列表 |
| `Next Action Or Recommended Skill` | 当前显式下一步 | 只能写一个 canonical 节点值，不得写自由文本 |

### `Current Stage`

推荐写法：

- 新的 HF progress 记录优先直接写 canonical 节点名，例如 `hf-test-driven-dev`
- 若项目必须使用别名，应在项目级约定中声明一对一映射，并保证 router（及读入时的 **legacy 合并路由** 别名）可唯一归一化
- 不再继续写 `phase`、`Current Phase`、自然语言阶段名等 generic 字段

### `Current Active Task`

约束：

- 一个工作周期只允许一个权威版活跃任务
- 在任务尚未被正式锁定前，不伪造活跃任务
- 若原任务已失效，可留空或写项目约定占位值，例如 `pending reselection`

### Optional coordination field: `Task Board Path`

说明：

- `Task Board Path` 不是 canonical progress core 的必填字段；只有在 workflow 需要 task-to-task 自动推进时才建议追加
- `Current Active Task` 仍是当前已锁定任务的权威表达；`Task Board Path` 只负责描述剩余任务的 ready / pending / done 投影
- 若已批准任务计划与 task board 冲突，父会话应停止自动推进，并回到 `hf-workflow-router` 按更保守证据重判
- 若项目不使用独立 task board，则应保证任务计划正文仍足以支撑 router 判断唯一 `next-ready task`

### Optional coordination fields: worktree isolation

说明：

- `Workspace Isolation`、`Worktree Path`、`Worktree Branch` 不是 canonical progress core 的必填字段；只有 workflow 需要隔离工作目录时才建议追加
- `Workspace Isolation` 统一使用 `in-place` / `worktree-required` / `worktree-active`
- `worktree-required` 表示下游代码修改节点必须先创建或复用 worktree，再进入实现 / 验证
- `worktree-active` 表示当前已经绑定有效 worktree；下游节点必须复用 `Worktree Path`，不要静默退回仓库根目录
- `Worktree Path` 应指向实际 worktree 根目录；若当前只是“需要隔离但尚未落地”，可暂时留空
- `Worktree Branch` 用于记录当前 worktree 绑定的分支，便于 review / finalize 与 PR 状态追踪
- 共享规则以 `hf-test-driven-dev/references/worktree-isolation.md` 为准；若 项目声明项目等价路径，优先遵循

### `Execution Mode`

约束：

- 仅使用 `interactive` / `auto`
- `interactive` 表示沿用当前默认交互模式：命中 approval / pause step 时等待用户输入
- `auto` 表示 workflow 会持续自动推进；若命中可自动解决的 approval step，则必须先写入 approval record，再继续进入下游节点
- `auto` 不是新的 `Workflow Profile`，也不允许写成 `full-auto`、`lightweight-auto` 之类复合值
- 推荐优先级：用户当前请求中的显式模式 >项目级约定中的默认策略 > 已存在 progress state 中的值

### `Next Action Or Recommended Skill`

约束：

- 只能写一个 canonical 值
- 不得使用 `done`、`继续推进`、`看情况`、`工作流完成` 这类自然语言
- workflow 已结束时，留空或使用项目约定 null 值；不要伪造新的下游节点
- 若同时保留多个待恢复节点，`Next Action Or Recommended Skill` 只写当前立即恢复的 canonical 节点；其余节点继续保留在 `Pending Reviews And Gates`

## Canonical Verdict And Severity

### Verdict vocabulary

review / gate 节点统一使用：

- `通过`
- `需修改`
- `阻塞`

如果项目需要英文映射，可在项目级约定中声明 `pass` / `revise` / `blocked` 的等价词，但 live HF family 文档应保持 verdict vocabulary 稳定。

### Severity vocabulary

review / bug-patterns 发现项统一使用：

- `critical`: 会阻塞下游判断，或会直接污染下一阶段输入
- `important`: 不一定立刻阻塞整个 workflow，但必须在进入指定下一节点前修复
- `minor`: 不阻塞当前主链，但应作为改进项显式记录

约束：

- severity 用于描述发现项，不替代 verdict
- 不要把所有问题都标成 `critical`
- 先有 finding，再给 severity；不要脱离证据抽象判级
- 本节只冻结 vocabulary；各 `hf-*review` skill 对 `critical` / `important` 的触发阈值仍以各自 `SKILL.md` 为准

## Fresh Evidence

### 定义

fresh evidence 指与当前最新代码状态、当前任务边界和当前验证目标直接对应的证据，而不是旧日志、旧截图或口头描述。

### 最低要求

当 skill 依赖 fresh evidence 时，记录中至少应能看出：

- 执行了什么命令或验证动作
- 结果是什么
- 这次执行为什么属于当前最新代码状态
- 它覆盖了哪一部分风险、行为或声明边界

### 常见适用节点

- `hf-test-driven-dev`：需要 fresh RED / GREEN evidence
- `hf-regression-gate`：需要 fresh regression evidence
- `hf-completion-gate`：需要 fresh completion evidence
- `hf-hotfix`：需要 fresh defect reproduction / fix evidence

### 不被接受的写法

- “上次已经跑过了”
- “旧日志显示之前是绿的”
- “口头上确认没问题”
- 只写“测试通过”，不写命令、摘要或新鲜度锚点

## Canonical Next Action Vocabulary

`Next Action Or Recommended Skill` 与 reviewer 摘要里的 `next_action_or_recommended_skill` 应统一落到以下受控 vocabulary：

- upstream authoring: `hf-specify` / `hf-design` / `hf-tasks`
- upstream review: `hf-spec-review` / `hf-design-review` / `hf-tasks-review`
- human confirmation: `规格真人确认` / `设计真人确认` / `任务真人确认`
- implementation and quality: `hf-test-driven-dev` / `hf-test-review` / `hf-code-review` / `hf-traceability-review` / `hf-regression-gate` / `hf-completion-gate` / `hf-finalize`
- branch and orchestration: `hf-hotfix` / `hf-increment` / `hf-workflow-router`

说明：`hf-bug-patterns` 作为独立经验固化 skill 存在，但不属于 HF workflow 的 canonical `Next Action Or Recommended Skill` vocabulary。

约束：

- 必须是唯一值
- 不得把多个候选动作拼成一个字符串
- review 节点返回 review 节点，表示父会话应派发 reviewer subagent，而不是在当前上下文内联继续 review
- 写时必须使用 canonical 值；若读取到旧工件中的 legacy 合并路由写法、坏值或自由文本，运行时容错规则以当前 skill pack 中 `hf-workflow-router/references/execution-semantics.md` 为准（历史工件若仍引用 legacy 安装路径下的同文件，按兼容读法处理）

## Record Path Conventions

### `record_path`

当 reviewer subagent 返回结构化摘要时：

- `record_path` 必须指向实际已经写入的 review 记录路径
- `record_path` 不能只是“计划写到哪里”
- 父会话消费摘要时，应以 `record_path` 作为 review artifact 的权威落点

### 默认逻辑工件布局

布局采用双根目录二分：

- `docs/` 放**项目长期资产**（跨 feature 周期、慢演化）：principles / adr / architecture / arc42 / runbooks / slo / postmortems / release-notes / bug-patterns / insights / index 等子目录
- `features/<NNN>-<slug>/` 放**单 feature 周期内的过程交付件**：spec / design / tasks / progress / reviews / approvals / verification / evidence / closeout 等

`<NNN>` 为三位顺序号（`001` 起，仓库级唯一、不复用）；`<slug>` 为 kebab-case 短主题名。`<active>` 在 workflow 周期开始时由 router 锁定为具体 feature 目录名。

除非 项目已声明等价路径，否则默认推荐（`tier` 标记对应"档 0 / 档 1 / 档 2"的最小 `docs/` 启用范围；档 0 = 不可省，档 1 = 推荐起步，档 2 = 按需启用）：

| 逻辑工件 | 默认路径 | Tier |
|---|---|---|
| requirement spec | `features/<active>/spec.md` | — |
| design doc | `features/<active>/design.md` | — |
| ui design doc | `features/<active>/ui-design.md`（仅当 spec 声明 UI surface） | — |
| data model（如分文件） | `features/<active>/data-model.md` | — |
| API contracts（本次变更草稿） | `features/<active>/contracts/` | — |
| task plan | `features/<active>/tasks.md` | — |
| task board | `features/<active>/task-board.md`（可选；用于 task-to-task 自动推进） | — |
| progress state | `features/<active>/progress.md`（**仅 feature 级；仓库根不再保留全局 `task-progress.md`**） | — |
| reviews | `features/<active>/reviews/<kind>-<scope>-YYYY-MM-DD.md` | — |
| approvals | `features/<active>/approvals/<kind>-<scope>-YYYY-MM-DD.md`（`auto` 模式强烈建议） | — |
| verification | `features/<active>/verification/<kind>-<scope>-YYYY-MM-DD.md` | — |
| evidence（命令输出 / 日志 / 性能基线） | `features/<active>/evidence/` | — |
| closeout pack | `features/<active>/closeout.md` | — |
| feature 入口 / 总览 | `features/<active>/README.md`（必需） | — |
| 项目自身原则锚点 | `docs/principles/`（如 `architecture-principles.md` / `product-principles.md`，由项目自定义） | 可选 |
| ADR pool | `docs/adr/NNNN-<slug>.md`（仓库级顺序号 4 位、永不复用） | 档 0（必需） |
| 顶层导航 | 仓库根 `README.md`（档 0/1）→ `docs/index.md`（档 2 启用） | 档 0 起 |
| changelog | 仓库根 `CHANGELOG.md`（Keep a Changelog 风格） | 档 0（必需） |
| 架构概述 | `docs/architecture.md`（档 1，单文件）→ `docs/arc42/`（档 2，12 节拆分） | 档 1（建议） |
| 源码化图 | `docs/diagrams/`（如 Structurizr DSL / PlantUML） | 档 2（按需） |
| 运维资产 | `docs/runbooks/` / `docs/slo/` / `docs/postmortems/` | 档 2（按需） |
| 用户可见变更（详细） | `docs/release-notes/vX.Y.Z.md` | 档 2（按需；档 0/1 时 `CHANGELOG.md` 即可） |
| Bug 模式沉淀 | `docs/bug-patterns/catalog.md` | 档 2（按需；`hf-bug-patterns` 启用时） |
| 产品发现草稿 | `docs/insights/` | 档 2（按需；`hf-product-discovery` 启用时） |

`<kind>` 受控词表：`spec` / `design` / `ui` / `tasks` / `code` / `test` / `traceability` / `discovery`（review）；`spec` / `design` / `tasks`（approval）；`regression` / `completion` / `hotfix`（verification）。

`<scope>` 取值：

- 阶段级 review/approval/verification：用日期 `YYYY-MM-DD`（同日多份追加 `-NN`）。
- 任务级 review/verification：用任务编号 `task-NNN`，例如 `code-review-task-003.md`、`completion-task-003.md`。
- 全 feature 一次性 review：scope 可省略，例如 `traceability-review.md`。

### 记录落盘原则

- review / gate 结论必须写入仓库工件，且默认落到当前 active feature 目录下的 `reviews/` / `verification/`
- approval step 结论也必须写入仓库工件；`auto` 模式不能只停留在对话里“默认通过”，approval record 默认落到 `features/<active>/approvals/`
- 对话中的摘要不能替代 review / verification 记录
- finalize 只能消费已落盘的 completion / regression / release artifacts，不能把对话记忆当成 closeout evidence
- 若使用 `Task Board Path`，board 也必须写入仓库工件，且与已批准任务计划保持可回读的一致关系
- ADR 是仓库级长期资产，落到 `docs/adr/` 而不是 feature 目录内；feature `design.md` 通过 ADR ID 引用，不内联 ADR 全文

### 长期资产同步规则（promotion rules）

feature 周期内对 `docs/` 中长期资产的修改按以下时机划分。所有同步遵循 **read-on-presence + sync-on-presence** 原则：HF skill 读取 `docs/` 资产时，缺失视为"未启用"而非阻塞；`hf-finalize` 同步时只对**已存在**的子目录或本 feature 触发了升级条件的子目录做同步。

| 长期资产 | 修改时机 | 修改方式 | Tier |
|---|---|---|---|
| ADR (`docs/adr/`) | 设计阶段直接落 | 起草时即分配 ADR ID 写入 `docs/adr/NNNN-...md`，状态 `proposed`；评审与 `设计真人确认` 通过后翻为 `accepted`。`design.md` 通过 ID 引用 | 档 0（不可省） |
| Release notes / CHANGELOG | closeout 同步 | 档 0/1：由 `hf-finalize` 写入仓库根 `CHANGELOG.md`。档 2：由 `hf-finalize` 写入 `docs/release-notes/vX.Y.Z.md` 并在 `CHANGELOG.md` 加版本入口 | 档 0 起 |
| 顶层导航 | closeout 同步 | 档 0/1：更新仓库根 `README.md` 中的 active feature / 最近 closeout / ADR 索引行。档 2：同步 `docs/index.md` | 档 0 起 |
| 架构概述（`docs/architecture.md` 或 `docs/arc42/`） | closeout 同步 | `hf-finalize` 把已批准变更应用到现存的那一份载体；两者只能同时存在一份 | 档 1（建议） |
| Glossary | closeout 同步 | 档 1：归并到 `docs/architecture.md` 的术语表节。档 2：落到 `docs/arc42/12_glossary.md` | 跟随架构概述档位 |
| 源码化图 (`docs/diagrams/`) | 设计阶段直接落 | 与 design review 一并审核 diff | 档 2（按需） |
| Runbooks (`docs/runbooks/`) | closeout 同步 | feature 引入新运维关注点时由 `hf-finalize` 新增/更新（包含本次 closeout 顺带启用目录的情况） | 档 2（按需） |
| SLO (`docs/slo/`) | closeout 同步 | feature 引入或修改 SLO 时由 `hf-finalize` 同步 | 档 2（按需） |
| Postmortems (`docs/postmortems/`) | 事故事件触发 | 不强制每个 feature 更新 | 档 2（按需） |
| Bug pattern catalog (`docs/bug-patterns/`) | 由 `hf-bug-patterns` 旁路触发 | 不强制每个 feature 更新 | 档 2（按需） |

`closeout.md` 的 *Release / Docs Sync* 区块按"按存在同步"列出实际同步路径，并对**本 feature 没有触发该资产类型变化**的项显式标 `N/A`（不算缺失）。判 `blocked` 的条件收紧为：

- 本 feature 触发了某类长期资产变化（例如新增模块 / 新增运维点 / 新增 SLO），但 closeout 既未同步现存目录，也未在合理升级时机启用新目录；
- 必需同步项缺失：`docs/adr/` 状态翻转、`CHANGELOG.md`、`README.md`/`docs/index.md` 中 active feature 状态。

未启用的可选资产（如 `docs/slo/` / `docs/postmortems/`）不构成 `blocked` 依据。

### approval record

当 workflow 命中 approval step（包括 `规格真人确认`、`设计真人确认`、`任务真人确认` 与测试设计确认）时：

- `interactive` 模式下，可把用户明确确认后的结果写入 approval record
- `auto` 模式下，父会话必须先写 approval record，再把 approval step 视为已完成
- approval record 至少应能回读：approval kind、resolution mode、based_on_record_path、artifact paths、artifact hashes、resolved_at、next action
- 若项目通过项目级声明映射了等价路径，仍应保持这些最小语义可回读

## Review / Gate Return Rules

### Reviewer return contract

reviewer subagent 的最小结构化摘要统一使用：

```json
{
  "conclusion": "通过|需修改|阻塞",
  "next_action_or_recommended_skill": "唯一 canonical 节点",
  "record_path": "实际写入的 review 记录路径",
  "key_findings": ["关键发现 1"],
  "needs_human_confirmation": false,
  "reroute_via_router": false
}
```

兼容说明：

- `needs_human_confirmation` 这个字段名为兼容现有 live contract 保留
- 它在新语义下表示“该 review 通过后，父会话还必须完成 approval step”
- 父会话最终是等待人工确认，还是按 `Execution Mode=auto` 自动落盘批准，由运行时编排决定

补充规则：

- `needs_human_confirmation=true` 仅用于 `hf-spec-review`、`hf-design-review`、`hf-tasks-review` 在 `conclusion=通过` 时，表示还需要 approval step
- 若 `conclusion=需修改` 或 `阻塞`，默认 `needs_human_confirmation=false`
- 若问题本质属于 route / stage / profile / 上游证据冲突，应设置 `reroute_via_router=true`
- 历史摘要或旧 skill 若仍返回 legacy reroute 字段，读时应视为与 `reroute_via_router` 同义（映射见下节 Legacy Alias Policy）；新产出应优先写 `reroute_via_router`

### 父会话消费顺序

父会话读取 reviewer 摘要时，先检查是否命中当前 skill pack 中 `hf-workflow-router/references/execution-semantics.md` 定义的暂停点与“先向用户展示”的义务；在完成任何必需的展示或讨论后，再按以下顺序处理：

1. 若 `reroute_via_router=true`（或读时把 legacy reroute 字段视为 true），先回到 `hf-workflow-router`
2. 否则若 `conclusion=通过` 且 `needs_human_confirmation=true`：
   - `Execution Mode=interactive` 时，进入对应 approval 节点并等待用户确认
   - `Execution Mode=auto` 时，先写 approval record，再进入该 approval 节点解锁后的下游节点
3. 否则若 `conclusion=通过` 且无需真人确认，进入 `next_action_or_recommended_skill`
4. 否则若 `conclusion=需修改` 或 `阻塞`，按 `next_action_or_recommended_skill` 回修或补条件

补充规则：

- 对 `hf-spec-review` / `hf-design-review`，`interactive` 模式下的 `需修改` 与内容回修型 `阻塞` 不是“静默自动回修”；父会话需先向用户展示评审结论与修订重点
- 对 `hf-spec-review` / `hf-design-review`，`auto` 模式下若修订方向清楚、仍在当前范围内，可直接回到上游 skill 回修；若修订方向不明确，仍应停止自动推进并报告阻塞
- 对 `hf-spec-review` / `hf-design-review`，若 `阻塞` 且需要经 router 重编排，父会话需先向用户展示阻塞原因，再回到 `hf-workflow-router`
- 对其他 review / gate，若结论为 `需修改` / `阻塞` 且修订方向不明确，也应先与用户讨论或停止自动推进，而不是机械自动推进

### Gate / implementation 回流规则

对 `hf-test-driven-dev`、`hf-regression-gate`、`hf-completion-gate` 这类非 reviewer 节点，回流约定统一为：

- 内容修订、缺少测试、验证失败、局部证据不足：回到最近的实现或门禁节点
- route / stage / profile / 上游证据冲突：回到 `hf-workflow-router`
- 新的范围变化：优先判断是否切到 `hf-increment`
- 新的紧急缺陷：优先判断是否切到 `hf-hotfix`

## Approval Step Rules

以下节点的“评审通过”不等于“已批准”：

- `hf-spec-review`
- `hf-design-review`
- `hf-tasks-review`

对应地，以下 canonical approval 节点由父会话负责：

- `规格真人确认`
- `设计真人确认`
- `任务真人确认`

补充规则：

- 这些 canonical 节点名出于兼容性保留，即使 `Execution Mode=auto` 也不从 route map 中删除
- `interactive` 模式下，这些节点表现为真人确认 pause point
- `auto` 模式下，这些节点表现为 approval record 写入点；只有 approval record 已落盘，节点才算完成
- 只有 reviewer 返回 `通过`，且对应 approval step 已完成后，相关上游工件才算已批准

## Legacy Alias Policy

旧字段与旧别名只允许用于“读取旧工件时的归一化判断”，不应继续写回：

- `phase` -> `Current Stage`
- `Current Task` -> `Current Active Task`
- `Next Action` / `next skill` -> `Next Action Or Recommended Skill`
- `hf-workflow-router` -> `hf-workflow-router`（历史 **legacy 合并入口/router** skill 名；独立目录已移除）
- `reroute_via_starter` -> `reroute_via_router`（legacy reroute 字段名；读时同义）

原则：

- 读时可兼容
- 写时必须收口到 canonical schema
- 若项目必须保留别名，必须在项目级约定中声明映射

## Practical Checklist

当你在编写或审阅某个 `hf-*` skill 时，至少确认：

- [ ] 该 skill 行为遵守 4 条横切行为基线（Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution），且没有把它们写进 canonical schema 或 next-action vocabulary
- [ ] progress schema 使用 canonical 字段名
- [ ] verdict 与 severity vocabulary 没有漂移
- [ ] `Next Action Or Recommended Skill` / `next_action_or_recommended_skill` 只写唯一 canonical 值
- [ ] 若多个 review / gate 同时待恢复，`Next Action Or Recommended Skill` 只写最早节点，其余保留在 `Pending Reviews And Gates`
- [ ] review / gate 结论会落盘到仓库工件
- [ ] 依赖 fresh evidence 的节点明确写出新鲜度锚点
- [ ] route / stage / profile / 上游证据冲突会回到 `hf-workflow-router`
- [ ] 若当前 workflow 需要 worktree 隔离，状态工件与 handoff 已显式携带 `Workspace Isolation` / `Worktree Path` / `Worktree Branch`
- [ ] 工件路径遵循双根目录布局：feature 周期内工件落到 `features/<active>/...`，长期资产落到 `docs/...`
- [ ] 没有把 ADR 内联进 `features/<active>/design.md`；ADR 已落到 `docs/adr/NNNN-...md` 并通过 ID 引用
- [ ] 没有在仓库根重新生成全局 `task-progress.md`；progress 仅写入 `features/<active>/progress.md`

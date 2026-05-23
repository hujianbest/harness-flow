# Profile Node And Transition Map

这份参考文档集中保存 `hf-workflow-router` 的 profile 合法节点集合、canonical route map、结果驱动迁移表与恢复编排协议。

当你已经在 router 主文件（`../SKILL.md`）中确认：

- 当前请求属于 workflow 场景
- 当前 profile 已确定
- 需要查合法节点、默认链路或结论后的默认下一步

再来这里读取细节。

## 合法状态集合

### full profile 主链推荐节点

- `hf-product-discovery`（conditional：当会话从模糊产品 idea 起步、或已存在 discovery 草稿时激活）
- `hf-discovery-review`（conditional：`hf-product-discovery` 被激活后存在）
- `hf-experiment`（conditional：discovery / spec 中存在 Blocking 或低 confidence 关键假设时，作为上游 stage 的 **conditional insertion**）
- `hf-browser-testing`（conditional：`hf-test-driven-dev` GREEN 之后，当 spec / ui-design 声明 UI surface，或当前 active task / 代码影响面触碰前端运行面时激活，作为 verify 阶段的 runtime evidence side node；激活判定见本文件的 `hf-browser-testing 激活与回流` 一节）
- `hf-specify`
- `hf-spec-review`
- `规格真人确认`
- `hf-design`
- `hf-design-review`
- `hf-ui-design`（conditional：仅当规格声明 UI surface 时激活，与 `hf-design` 并行）
- `hf-ui-review`（conditional：仅当 `hf-ui-design` 被激活时存在）
- `设计真人确认`（联合 approval：`hf-design-review` 与 `hf-ui-review` 均通过后由父会话发起；未激活 `hf-ui-design` 时退化为仅等待 `hf-design-review`）
- `hf-tasks`
- `hf-tasks-review`
- `任务真人确认`
- `hf-test-driven-dev`
- `hf-subagent-driven-dev`（conditional：approved task 可被完整封装给 fresh implementer subagent 时，作为 `hf-test-driven-dev` 的可选实现 leaf；不改变后续 review/gate 链）
- `hf-test-review`
- `hf-code-review`
- `hf-traceability-review`
- `hf-regression-gate`
- `hf-doc-freshness-gate`（Phase 0 / ADR-0003：位于 `hf-regression-gate` 之后、`hf-completion-gate` 之前；本 gate verdict 作为 `hf-completion-gate` evidence bundle 一项被 reference）
- `hf-completion-gate`
- `hf-finalize`

说明：

- `hf-ui-design` / `hf-ui-review` 属于 **design stage 内部的 conditional peer**，不是 side-line。激活判定见 `ui-surface-activation.md`
- `hf-experiment` 属于 **discovery / spec stage 内部的 conditional insertion**（Phase 0 引入）：在 discovery 或 spec 中发现 Blocking / 低 confidence 关键假设时临时插入，完成后回到插入点（`hf-product-discovery` / `hf-discovery-review` / `hf-specify` / `hf-spec-review`）；激活判定见本文件的 `hf-experiment 激活与回流` 一节
- `hf-browser-testing` 属于 **verify stage 内部的 conditional side node**（v0.2.0 / ADR-002 D1 / D7 引入）：在 `hf-test-driven-dev` / `hf-subagent-driven-dev` GREEN 之后，当 task 或代码影响面触碰前端运行面时由 router 拐点拉入；产出 runtime evidence bundle（DOM / Console / Network 三层），不签发 verdict，不修改主链 FSM 主路径；完成后回到 router，由 router 决定继续下一个 ready task 还是进入批量 quality chain。若代码事实显示触碰 UI / API client / dev-server 配置，但 spec / tasks 未声明对应 runtime surface，router 必须回上游补工件，不得静默跳过。激活判定见本文件的 `hf-browser-testing 激活与回流` 一节
- `hf-subagent-driven-dev` 属于 **implementation stage 内部的 conditional alternative**，不是并行实现模式；一次仍只允许一个 `Current Active Task`，且后续 review/gate verdict 不被跳过，只按 hybrid batch 规则延后到所有 approved tasks 实现完成后统一执行
- `standard` / `lightweight` profile 不加入 `hf-ui-design` / `hf-ui-review` / `hf-product-discovery` / `hf-experiment` 作为主链节点；若新 iteration 需要补 discovery 或假设验证，应升级到 `full`
- `hf-browser-testing` 不依赖 profile，全 profile 共享同一激活规则（runtime surface 声明或代码事实 + 当前 task 触碰前端 / API client / dev-server 配置）

### standard profile 主链推荐节点

- `hf-tasks`
- `hf-tasks-review`
- `任务真人确认`
- `hf-test-driven-dev`
- `hf-subagent-driven-dev`（conditional：同 full profile；不适用于任务强耦合或上下文不可封装）
- `hf-test-review`
- `hf-code-review`
- `hf-traceability-review`
- `hf-regression-gate`
- `hf-doc-freshness-gate`（Phase 0 / ADR-0003：位于 `hf-regression-gate` 之后、`hf-completion-gate` 之前）
- `hf-completion-gate`
- `hf-finalize`

### lightweight profile 主链推荐节点

- `hf-tasks`
- `hf-tasks-review`
- `任务真人确认`
- `hf-test-driven-dev`
- `hf-subagent-driven-dev`（conditional：同 full profile；通过后仍按 lightweight 质量链进入 gate）
- `hf-regression-gate`
- `hf-doc-freshness-gate`（Phase 0 / ADR-0003：lightweight 模式下使用 lightweight checklist template，≤ 5 分钟 / ≤ 30 行）
- `hf-completion-gate`
- `hf-finalize`

### 支线推荐节点

- `hf-increment`
- `hf-hotfix`

如果某个用户请求、口头描述或局部记录暗示跳到当前 profile 合法集合之外，按无效迁移处理，回到最近一个有证据支撑的上游节点，或触发 profile 升级。

## Execution Mode Does Not Change The Route Map

`Execution Mode` 只影响 approval step 的解决方式，不改变 profile 的合法节点集合：

- `interactive`：`规格真人确认` / `设计真人确认` / `任务真人确认` 表现为等待用户输入的 approval node
- `auto`：同样保留这些 approval node，但要求先写 approval record，再解锁下游节点
- 不允许把 `hf-spec-review -> hf-design`、`hf-design-review -> hf-tasks`、`hf-tasks-review -> hf-test-driven-dev` 直接折叠成“跳过确认节点”

## Canonical Route Map

把下列主骨架视为默认路由图；任何实际迁移都必须同时满足 profile 合法集合、批准证据和迁移表规则：

```text
full (no UI surface):
  hf-specify -> hf-spec-review -> 规格真人确认
  -> hf-design -> hf-design-review -> 设计真人确认
  -> hf-tasks -> hf-tasks-review -> 任务真人确认
  -> implementation batch loop:
       hf-workflow-router -> hf-test-driven-dev | hf-subagent-driven-dev
       -> (conditional hf-browser-testing) -> hf-workflow-router
       -> if unique next-ready task exists: next implementation leaf
       -> else: batch quality chain
  -> hf-test-review -> hf-code-review
  -> hf-traceability-review -> hf-regression-gate -> hf-doc-freshness-gate -> hf-completion-gate
  -> hf-finalize

full (with UI surface, Design Execution Mode=parallel):
  hf-specify -> hf-spec-review -> 规格真人确认
  -> {hf-design || hf-ui-design}                      # 并行起稿
  -> {hf-design-review || hf-ui-review}               # 各自独立 reviewer subagent
  -> 设计真人确认                                       # 两条 review 均 `通过` 后由父会话汇总发起
  -> hf-tasks -> hf-tasks-review -> 任务真人确认
  -> implementation batch loop:
       hf-workflow-router -> hf-test-driven-dev | hf-subagent-driven-dev
       -> (conditional hf-browser-testing) -> hf-workflow-router
       -> if unique next-ready task exists: next implementation leaf
       -> else: batch quality chain
  -> hf-test-review -> hf-code-review
  -> hf-traceability-review -> hf-regression-gate -> hf-doc-freshness-gate -> hf-completion-gate
  -> hf-finalize

standard:
  hf-tasks -> hf-tasks-review -> 任务真人确认
  -> implementation batch loop:
       hf-workflow-router -> hf-test-driven-dev | hf-subagent-driven-dev
       -> (conditional hf-browser-testing) -> hf-workflow-router
       -> if unique next-ready task exists: next implementation leaf
       -> else: batch quality chain
  -> hf-test-review -> hf-code-review
  -> hf-traceability-review -> hf-regression-gate -> hf-doc-freshness-gate -> hf-completion-gate
  -> hf-finalize

lightweight:
  hf-tasks -> hf-tasks-review -> 任务真人确认
  -> implementation batch loop:
       hf-workflow-router -> hf-test-driven-dev | hf-subagent-driven-dev
       -> (conditional hf-browser-testing) -> hf-workflow-router
       -> if unique next-ready task exists: next implementation leaf
       -> else: batch quality chain
  -> hf-regression-gate -> hf-doc-freshness-gate -> hf-completion-gate
  -> hf-finalize

branches:
  increment -> hf-increment -> return via router
  hotfix -> hf-hotfix -> return via router
```

说明：

- `hf-test-driven-dev` / `hf-subagent-driven-dev` 的边界是“单个 `Current Active Task` 的 TDD 实现、fresh evidence、handoff、wisdom delta 与 task-progress 同步”，不是完整 review/gate 闭环
- full/standard/lightweight 默认采用 **hybrid batch quality**：每个 task 完成实现交接后回 router；若存在唯一 approved 且 dependency-ready 的 `next-ready task`，先继续下一 task 实现；只有 approved tasks 全部实现完成后，才进入一次覆盖整批 task 的 review/gate quality chain
- hybrid batch 不跳过 verdict：`hf-test-review` / `hf-code-review` / `hf-traceability-review` / `hf-regression-gate` / `hf-doc-freshness-gate` / `hf-completion-gate` 仍各自产出独立 verdict、record_path 与唯一 next action，只是 scope 从单 task 扩展为本批已实现 tasks
- 通过态仍聚合为 task summaries + batch thin verdict matrix；异常态必须能定位到具体 task，并回流到对应 task 的 `hf-test-driven-dev`
- `hf-completion-gate` 返回 `通过` 默认表示本批 quality chain 闭合；只有在它发现新出现的 approved tasks、剩余任务证据冲突或 batch scope 不完整时，才回 `hf-workflow-router`

## 结果驱动迁移表

把 review / gate 结论视为显式迁移信号，而不是普通建议。

### full profile 迁移表

| 当前节点 | 结论 | 下一推荐节点 |
|---|---|---|
| `hf-product-discovery` | 草稿 ready | `hf-discovery-review` |
| `hf-discovery-review` | `通过` 且无 Blocking 假设 | `hf-specify` |
| `hf-discovery-review` | `通过` 但存在 Blocking 假设 | `hf-experiment` |
| `hf-discovery-review` | `需修改` / `阻塞` | `hf-product-discovery` |
| `hf-discovery-review` | `阻塞`（需重编排） | `hf-workflow-router` |
| `hf-experiment`（上游 = discovery） | `probe-result = Pass`，Blocking 清除 | `hf-specify` |
| `hf-experiment`（上游 = discovery） | `probe-result = Fail` | `hf-product-discovery`（修订 OST / 候选方向 / 排除项） |
| `hf-experiment`（上游 = discovery） | `probe-result = Inconclusive` | `hf-workflow-router`（决定追加 probe / 接受风险 / 回 discovery） |
| `hf-experiment`（上游 = spec） | `probe-result = Pass`，Blocking 清除 | `hf-specify`（修订 HYP Confidence 后回 spec-review） |
| `hf-experiment`（上游 = spec） | `probe-result = Fail` | `hf-specify`（按假设证伪同步修订 FR/NFR） |
| `hf-experiment`（上游 = spec） | `probe-result = Inconclusive` | `hf-workflow-router` |
| `hf-spec-review` | `通过` | 规格真人确认 |
| `hf-spec-review` | `通过` 但存在 Blocking 假设 | `hf-experiment` |
| `hf-spec-review` | `需修改` / `阻塞` | `hf-specify` |
| `hf-spec-review` | `阻塞`（需重编排） | `hf-workflow-router` |
| 规格真人确认 | approval step 完成 | `hf-design` |
| 规格真人确认 | 要求修改 / approval step 未完成 | `hf-specify` |
| `hf-design-review` | `通过`（UI surface 未激活） | 设计真人确认 |
| `hf-design-review` | `通过`（UI surface 激活且 `hf-ui-review` 也已 `通过`） | 设计真人确认（联合 approval） |
| `hf-design-review` | `通过`（UI surface 激活但 `hf-ui-review` 未通过或未完成） | 暂存结论，等待 `hf-ui-review` 汇合；期间按 `Design Execution Mode` 允许 peer 继续推进 |
| `hf-design-review` | `需修改` / `阻塞` | `hf-design` |
| `hf-design-review` | `阻塞`（需重编排） | `hf-workflow-router` |
| `hf-ui-review` | `通过`（与 `hf-design-review` 均通过） | 设计真人确认（联合 approval） |
| `hf-ui-review` | `通过`（`hf-design-review` 未通过或未完成） | 暂存结论，等待 `hf-design-review` 汇合 |
| `hf-ui-review` | `需修改` / `阻塞` | `hf-ui-design` |
| `hf-ui-review` | `阻塞`（需重编排 / 激活条件判定错 / peer 不可协调） | `hf-workflow-router` |
| 设计真人确认 | approval step 完成 | `hf-tasks` |
| 设计真人确认 | 要求修改 / approval step 未完成 | `hf-design` 或 `hf-ui-design`（按真人反馈指向；若两者都要改，并行回修） |
| `hf-tasks-review` | `通过` | 任务真人确认 |
| `hf-tasks-review` | `需修改` / `阻塞` | `hf-tasks` |
| `hf-tasks-review` | `阻塞`（需重编排） | `hf-workflow-router` |
| 任务真人确认 | approval step 完成（默认 / eligibility 不清） | `hf-test-driven-dev` |
| 任务真人确认 | approval step 完成（task 可完整封装给 fresh implementer subagent） | `hf-subagent-driven-dev` |
| 任务真人确认 | 要求修改 / approval step 未完成 | `hf-tasks` |
| `hf-test-driven-dev` | 实现交接完成 | `hf-workflow-router`（batch decision：next-ready task vs batch quality chain） |
| `hf-subagent-driven-dev` | 实现交接完成 | `hf-workflow-router`（batch decision：next-ready task vs batch quality chain） |
| `hf-test-review` | `通过` | `hf-code-review` |
| `hf-test-review` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-code-review` | `通过` | `hf-traceability-review` |
| `hf-code-review` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-traceability-review` | `通过` | `hf-regression-gate` |
| `hf-traceability-review` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-regression-gate` | `通过` | `hf-doc-freshness-gate` |
| `hf-regression-gate` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-doc-freshness-gate` | `pass` / `partial` / `N/A` | `hf-completion-gate`（verdict 路径作为 evidence bundle 一项被 reference） |
| `hf-doc-freshness-gate` | `blocked`（内容：关键文档维度漂移） | `hf-test-driven-dev`（补文档变更；spec FR-005 第三条 acceptance；blocked verdict 不进入 completion-gate evidence bundle） |
| `hf-doc-freshness-gate` | `blocked`（spec ↔ commits 实质不一致） | `hf-increment`（FR-007 负路径） |
| `hf-doc-freshness-gate` | `blocked`（user-visible change list 三类来源全缺） | `hf-traceability-review`（FR-001 负路径） |
| `hf-doc-freshness-gate` | `blocked`（workflow：route/stage/profile/证据冲突） | `hf-workflow-router`（`reroute_via_router=true`） |
| `hf-completion-gate` | `通过`（batch quality chain 闭合且无剩余 approved task） | `hf-finalize` |
| `hf-completion-gate` | `通过`（发现新 approved task、batch scope 不完整或剩余任务证据冲突） | `hf-workflow-router` |
| `hf-completion-gate` | `需修改` / `阻塞` | `hf-test-driven-dev` |

### standard profile 迁移表

| 当前节点 | 结论 | 下一推荐节点 |
|---|---|---|
| `hf-tasks-review` | `通过` | 任务真人确认 |
| `hf-tasks-review` | `需修改` / `阻塞` | `hf-tasks` |
| `hf-tasks-review` | `阻塞`（需重编排） | `hf-workflow-router` |
| 任务真人确认 | approval step 完成（默认 / eligibility 不清） | `hf-test-driven-dev` |
| 任务真人确认 | approval step 完成（task 可完整封装给 fresh implementer subagent） | `hf-subagent-driven-dev` |
| 任务真人确认 | 要求修改 / approval step 未完成 | `hf-tasks` |
| `hf-test-driven-dev` | 实现交接完成 | `hf-workflow-router`（batch decision：next-ready task vs batch quality chain） |
| `hf-subagent-driven-dev` | 实现交接完成 | `hf-workflow-router`（batch decision：next-ready task vs batch quality chain） |
| `hf-test-review` | `通过` | `hf-code-review` |
| `hf-test-review` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-code-review` | `通过` | `hf-traceability-review` |
| `hf-code-review` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-traceability-review` | `通过` | `hf-regression-gate` |
| `hf-traceability-review` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-regression-gate` | `通过` | `hf-doc-freshness-gate` |
| `hf-regression-gate` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-doc-freshness-gate` | `pass` / `partial` / `N/A` | `hf-completion-gate` |
| `hf-doc-freshness-gate` | `blocked`（内容） | `hf-test-driven-dev` |
| `hf-doc-freshness-gate` | `blocked`（spec ↔ commits 不一致） | `hf-increment` |
| `hf-doc-freshness-gate` | `blocked`（input 全缺） | `hf-traceability-review` |
| `hf-doc-freshness-gate` | `blocked`（workflow） | `hf-workflow-router`（`reroute_via_router=true`） |
| `hf-completion-gate` | `通过`（batch quality chain 闭合且无剩余 approved task） | `hf-finalize` |
| `hf-completion-gate` | `通过`（发现新 approved task、batch scope 不完整或剩余任务证据冲突） | `hf-workflow-router` |
| `hf-completion-gate` | `需修改` / `阻塞` | `hf-test-driven-dev` |

### lightweight profile 迁移表

| 当前节点 | 结论 | 下一推荐节点 |
|---|---|---|
| `hf-tasks-review` | `通过` | 任务真人确认 |
| `hf-tasks-review` | `需修改` / `阻塞` | `hf-tasks` |
| `hf-tasks-review` | `阻塞`（需重编排） | `hf-workflow-router` |
| 任务真人确认 | approval step 完成（默认 / eligibility 不清） | `hf-test-driven-dev` |
| 任务真人确认 | approval step 完成（task 可完整封装给 fresh implementer subagent） | `hf-subagent-driven-dev` |
| 任务真人确认 | 要求修改 / approval step 未完成 | `hf-tasks` |
| `hf-test-driven-dev` | 实现交接完成 | `hf-workflow-router`（batch decision：next-ready task vs batch quality chain） |
| `hf-subagent-driven-dev` | 实现交接完成 | `hf-workflow-router`（batch decision：next-ready task vs batch quality chain） |
| `hf-regression-gate` | `通过` | `hf-doc-freshness-gate` |
| `hf-regression-gate` | `需修改` / `阻塞` | `hf-test-driven-dev` |
| `hf-doc-freshness-gate` | `pass` / `partial` / `N/A` | `hf-completion-gate`（lightweight 模式下使用 `templates/lightweight-checklist-template.md`，verdict 文件 ≤ 30 行） |
| `hf-doc-freshness-gate` | `blocked`（内容） | `hf-test-driven-dev` |
| `hf-doc-freshness-gate` | `blocked`（spec ↔ commits 不一致） | `hf-increment` |
| `hf-doc-freshness-gate` | `blocked`（input 全缺） | `hf-traceability-review` |
| `hf-doc-freshness-gate` | `blocked`（workflow） | `hf-workflow-router`（`reroute_via_router=true`） |
| `hf-completion-gate` | `通过`（batch quality chain 闭合且无剩余 approved task） | `hf-finalize` |
| `hf-completion-gate` | `通过`（发现新 approved task、batch scope 不完整或剩余任务证据冲突） | `hf-workflow-router` |
| `hf-completion-gate` | `需修改` / `阻塞` | `hf-test-driven-dev` |

如果某个下游 skill 给出的结论无法映射到当前 profile 迁移表中的唯一下一推荐节点，或实现交接后无法唯一决定“next-ready task vs batch quality chain”，或 `hf-completion-gate=通过` 后无法确认 batch scope 覆盖全部 approved tasks，则说明编排信息还不完整，应回到 `hf-workflow-router` 重新判断，而不是自行补脑推进。

上表主要描述“内容回修型”默认迁移。若 reviewer 返回摘要显式要求 `reroute_via_router=true`，或把 `next_action_or_recommended_skill` 指向 `hf-workflow-router`，该显式重编排信号优先于表内默认下一步。

## `hf-experiment` 激活与回流（Phase 0 新增）

`hf-experiment` 不是主链节点，而是 **discovery / spec stage 内部的 conditional insertion**。它在以下证据下激活：

- `hf-product-discovery` 草稿中存在标记为 Blocking、且 confidence 低的关键假设
- `hf-discovery-review` 返回 `通过` 但同时提示存在 Blocking 假设
- `hf-specify` 草稿 section 4 (Key Hypotheses) 中存在 `Blocking? = 是` 的假设
- `hf-spec-review` 返回 `通过` 但同时提示存在 Blocking 假设
- reviewer 返回摘要中 `next_action_or_recommended_skill` 指向 `hf-experiment`

激活时必须记录：

- **插入点 (Insertion Point)**：`hf-product-discovery` / `hf-discovery-review` / `hf-specify` / `hf-spec-review`
- **假设 ID 集合**：本轮 probe 要覆盖的 `HYP-xxx`

回流规则：

- `probe-result = Pass` 且 Blocking 清除 → 回到原插入点的 **下一合法节点**（见迁移表中的 `hf-experiment` 行）
- `probe-result = Fail` → 回到插入点对应的 **上游正文 skill**，修订 OST / 候选方向 / 排除项 / FR-NFR
- `probe-result = Inconclusive` → 回 `hf-workflow-router`，由 router 决定：追加一次 probe / 显式接受风险 / 回上游修订
- 回流时必须更新对应 HYP 的 `Confidence` / `Blocking?` 字段

`standard` / `lightweight` profile 不激活 `hf-experiment`。若 standard / lightweight 会话中发现关键 Blocking 假设，应先升级到 `full` profile 再激活。

## 恢复编排协议

当某个节点完成后，按以下顺序恢复状态机：

1. 读取该节点的最新结论
2. 确认当前 workflow profile（从 feature `progress.md`，默认 `features/<active>/progress.md` 读取）
3. 若 feature `progress.md` 或等价工件已经写入合法或可归一化的 `Next Action Or Recommended Skill`，且它来自上一个已完成节点并与最新证据不冲突，优先采用这个显式下一步
4. 否则检查该结论对应的上游 / 下游迁移是否在当前 profile 迁移表中有明确规则
5. 若当前结论是 `hf-test-driven-dev` / `hf-subagent-driven-dev` 实现交接完成，或 `hf-browser-testing` 已完成且无 blocking observation，优先检查已批准任务计划或 `Task Board Path` 指向的等价工件：
   - 若存在唯一 `next-ready task`，先把刚完成的 task 投影为 `implemented-pending-batch-quality`，把 `Current Active Task` 切换到下一 task，并把显式下一步锁定为合格实现 leaf（默认 `hf-test-driven-dev`；subagent eligible 时可为 `hf-subagent-driven-dev`）
   - 若不存在剩余 ready / pending task，把下一步视为当前 profile 的 batch quality chain 首节点（full/standard 为 `hf-test-review`；lightweight 为 `hf-regression-gate`）
   - 若剩余任务候选不唯一、依赖状态冲突、batch scope 不可恢复或 ready 判定不稳定，回到 `hf-workflow-router` 作为 hard stop
6. 若当前结论是 `hf-completion-gate=通过`，确认 batch quality scope 覆盖所有已批准 task 且无剩余 ready / pending task；满足时进入 `hf-finalize`，否则回到 `hf-workflow-router`
7. 根据当前会话上下文判断用户是否已经提出了新范围、新缺陷或新阻塞（基于已有信息判断，不主动询问用户）
8. 若有范围变化，优先判断是否切到 `hf-increment`
9. 若有紧急缺陷，优先判断是否切到 `hf-hotfix`
10. 若没有新的支线信号，则按当前 profile 迁移表进入唯一下一推荐节点

### 最小示例：T1 实现交接后切到 T2

前提工件：

```markdown
# features/003-parser/progress.md

- Current Stage: hf-test-driven-dev
- Workflow Profile: standard
- Execution Mode: auto
- Current Active Task: T1
- Batch Quality Scope: T1 (implemented-pending-batch-quality)
- Pending Reviews And Gates: hf-test-review, hf-code-review, hf-traceability-review, hf-regression-gate, hf-doc-freshness-gate, hf-completion-gate
- Next Action Or Recommended Skill: hf-workflow-router
- Task Board Path: `features/003-parser/task-board.md`
```

```markdown
# features/003-parser/task-board.md

## Task Queue

| Task ID | Status | Depends On | Ready When | Selection Priority |
|---|---|---|---|---|
| T1 | implemented-pending-batch-quality | - | spec / design / tasks approval 已完成 | P1 |
| T2 | pending | T1 | T1=`implemented-pending-batch-quality` | P2 |
```

当 T1 的实现 leaf 写出完整 handoff 后，父会话 / router 恢复顺序应为：

1. 读取实现交接块，确认 T1 的 TDD evidence / Refactor Note / wisdom delta / task-progress 已完成
2. 读取 task board，先把 T1 投影为 `implemented-pending-batch-quality`
3. 根据 `Depends On` + `Ready When` 判断，T2 成为唯一 `next-ready task`
4. 更新 `Current Active Task: T2`
5. 将 `Next Action Or Recommended Skill` 锁定为合格实现 leaf（默认 `hf-test-driven-dev`；subagent eligible 时可为 `hf-subagent-driven-dev`）
6. 因为这不是 approval node，也不是 hard stop，所以在同一轮继续进入该实现 leaf

### 最小示例：最后一个任务实现后进入 batch quality chain

若同样的恢复编排发生在最后一个任务：

```markdown
## Task Queue

| Task ID | Status | Depends On | Ready When | Selection Priority |
|---|---|---|---|---|
| T1 | implemented-pending-batch-quality | - | spec / design / tasks approval 已完成 | P1 |
| T2 | implemented-pending-batch-quality | T1 | T1=`implemented-pending-batch-quality` | P2 |
```

此时 router 读取 queue 后发现不存在剩余 `ready` / `pending` task，才把下一步收敛为当前 profile 的 batch quality chain 首节点（standard 为 `hf-test-review`），而不是再回到实现节点或直接 finalize。

不要跳过第 2 步、第 3 步和第 4 步。

恢复编排完成后：

- 若下一推荐节点是 `interactive` 下的 approval node，等待用户确认
- 若下一推荐节点是 `auto` 下的 approval node，先写 approval record，再进入该节点解锁后的下游节点
- 若下一推荐节点不是 approval node，也不是 hard stop，立刻在同一轮中进入该节点，不等待用户确认

若该下一推荐节点是 review 节点，则“进入该节点”的含义是：按 `references/review-dispatch-protocol.md` 派发 reviewer subagent，并按 `references/reviewer-return-contract.md` 消费返回摘要，而不是在父会话内联执行 review；hybrid batch 下 reviewer 的 scope 必须覆盖 `Batch Quality Scope` 中所有 implemented tasks。

## `hf-browser-testing` 激活与回流

`hf-browser-testing`（v0.2.0 / ADR-002 D1 / D7 引入）是 verify 阶段的 conditional side node，**不修改主链 FSM 主路径**。router 在以下条件满足时把它作为实现 leaf（`hf-test-driven-dev` / `hf-subagent-driven-dev`）的下一推荐节点：

1. 当前实现 leaf 已完成 active task 的 GREEN（progress.md 中存在 GREEN 交接块且单元 fresh evidence 可读）。
2. runtime surface 已被工件声明：`features/<active>/spec.md` 中存在 UI surface / API client / runtime surface 段，或 `hf-ui-design` 已批准，或 `tasks.md` 的当前 task 明确列出 browser smoke / API contract / full-stack smoke 证据。
3. 当前 active task 影响面触碰前端运行面，依据 `tasks.md`、design 工件、实现交接块或变更文件判断。触发信号包括：可见页面 / route / App 根组件、UI library provider、表单交互、前端 API client / fetch / auth store、Vite proxy / env / dev-server 配置、浏览器存储、网络错误处理。

处理规则：

- 条件 1 不满足 → 回当前实现 leaf（默认 `hf-test-driven-dev`，subagent eligible 时可为 `hf-subagent-driven-dev`）补 GREEN evidence。
- 条件 2 不满足但条件 3 明确满足 → 工件与代码事实冲突；回 `hf-specify` / `hf-tasks`（按缺失层级）补 runtime surface / DoD，而不是跳过浏览器证据。
- 条件 3 不满足 → router 跳过 `hf-browser-testing`，直接进入 hybrid batch decision：仍有唯一 next-ready task 时继续下一实现 leaf；无剩余 task 时进入当前 profile 的 batch quality chain 首节点。

回流（`hf-browser-testing` 完成后）：

- 0 blocking + 0 major observation → 下一推荐节点 = `hf-workflow-router`（回到 hybrid batch decision，决定 next-ready task vs batch quality chain）。
- ≥ 1 blocking observation → 下一推荐节点 = 当前实现 leaf（携带 finding，回修后重跑 GREEN）。
- 0 blocking + ≥ 1 major observation → 下一推荐节点 = observations.md 中 majority `suggested next` 指向的节点（典型为 `hf-test-review` 或 `hf-ui-review`）；若 suggested next 只是 gate，则回 `hf-workflow-router` 做 batch decision。

`hf-browser-testing` **不**签发 pass / fail verdict（参见 SKILL.md Hard Gates 与 Common Rationalizations）；上述回流是 router 基于 observation 计数的机械路由，不是 reviewer verdict。

router 的实现职责仅限于：(a) 检查上述 3 个激活条件；(b) 读取 `features/<active>/verification/browser-evidence/<task-id>/observations.md` 的 severity 计数；(c) 把回流结论映射成唯一 canonical next action。**不读 evidence 内容、不参与 severity 改判**。

---

## v0.6 新增（按 ADR-008 D2 / spec FR-003 / FR-015）

### Step-Level Recovery via `tasks.progress.json`

router 在恢复 active task 时，除读 feature `progress.md`（节点级 stage trail）外，还读 `features/<active>/tasks.progress.json`（按 `skills/hf-test-driven-dev/references/tasks-progress-schema.md`）做 task 内 step-level 恢复：

| `current_step` | router 路由 |
|---|---|
| `TEST-DESIGN` | `hf-test-driven-dev` 重新进入测试设计步 |
| `APPROVAL` | `hf-test-driven-dev` 直接到 approval 写工件（auto mode）或等待架构师（standard mode） |
| `RED-N` | `hf-test-driven-dev` 恢复 RED-N 步（不重做设计） |
| `GREEN-N` | `hf-test-driven-dev` 恢复 GREEN-N 步 |
| `REFACTOR-N` | `hf-test-driven-dev` 恢复 REFACTOR-N 步（含步骤 4A architectural health check） |
| `DONE` | router 选下一 active task；归档 `tasks.progress.<task-id>.json` |

工件不存在或 schema 不合规 → router 视为节点级恢复（按既有逻辑），不阻塞。

### `category_hint` 字段（FR-015 SHOULD）

router 在 handoff JSON 中可选地携带 `category_hint`（取值如 `visual-engineering` / `deep` / `quick` / `ultrabrain`，对齐 OMO category routing 体系）：

```json
{
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "active_task": "TASK-005",
  "category_hint": "visual-engineering",
  "wisdom_summary": "..."
}
```

下游 host 不消费时直接忽略；不构成 hard error。SHOULD 失败处理：FR-015 不达标时 hf-completion-gate 不阻塞（按 spec FR-015 Acceptance #3）。

### `wisdom_summary` 注入（FR-003）

router 在选下一 active task 之前，从 `features/<active>/notepads/` 读取**近 N=3 task 的 wisdom 摘要**并注入下游 handoff：

- 摘要内容：近 3 task 的 learnings.md 最新 entry `pattern` 字段 + verification.md 最新 entry `result` 字段 + 任何 issues.md status=open 的 entry
- 摘要长度上限：1500 token（避免 handoff 过载）
- 注入位置：handoff JSON 的 `wisdom_summary` 字段

下游节点（hf-test-driven-dev 主要受众）按 wisdom_summary 调整实现策略，避免重复踩 N task 之前已踩过的坑。

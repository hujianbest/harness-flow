# Execution Semantics

这份参考文档集中保存 `hf-workflow-router` 的连续执行原则、approval step 语义、暂停点、非暂停点、路由失败模式与执行级红旗信号。

当你已经确认当前路由结果，需要判断：

- 是否应该继续自动推进
- 是否命中暂停点
- 是否应该回到 router 重编排

再来这里读取细节。

## Execution Mode

`Execution Mode` 与 `Workflow Profile` 正交：

- `interactive`：approval step 需要等待用户输入
- `auto`：approval step 可自动落盘解决，但仍必须保留 approval 语义与记录

归一化优先级：

1. 用户当前请求中的显式模式要求
2. 项目默认 Execution Mode 与 auto 禁止条件（若项目已声明）
3. feature `progress.md`（默认 `features/<active>/progress.md`）中已有且仍有效的 `Execution Mode`
4. 默认 `interactive`

约束：

- `auto` 不是新的 profile，也不允许借此删除 approval 节点
- 若 项目级 policy 禁止当前范围继续 `auto`，应停止自动推进并显式报告
- `auto` 只改变等待方式，不改变 review / gate / approval step 的存在性

## Workspace Isolation

`Workspace Isolation` 与 `Workflow Profile`、`Execution Mode` 正交：

- `in-place`：允许继续使用当前工作区
- `worktree-required`：下游代码修改节点必须先创建或复用 worktree
- `worktree-active`：当前已绑定有效 worktree；后续实现 / review 应复用同一路径

约束：

- `worktree-required` 不是暂停点；若下一节点是 `hf-test-driven-dev`，应在同一轮继续完成 worktree 准备
- 若当前是 `worktree-active`，review dispatch 必须携带 `Worktree Path` / `Worktree Branch`
- 不允许在节点切换时静默丢失 worktree 上下文

## 连续执行原则

路由完成后，应在同一轮中立刻进入目标 skill 并执行；只有命中 approval step 或 hard stop 时，才改变这一默认行为。

整条 workflow 链路默认以连续执行模式运行：一个节点完成后，自动判断下一个节点并立刻进入，直到遇到明确 approval step 或 hard stop。

即使刚刚回到 `hf-workflow-router` 完成重编排，这条规则也不变：只要结果不是 `interactive` 下的 approval step，也不是 hard stop，就应继续在同一轮进入目标 skill，而不是额外停一轮等待用户回复。

任务边界本身也不是默认暂停点：若当前任务刚通过 `hf-completion-gate`，且 router 能唯一锁定下一个 `Current Active Task`，则应在同一轮继续进入新的 `hf-test-driven-dev`，而不是把“一个任务做完”误当成自然暂停。

## Approval Step

以下场景属于 canonical approval step；它们在 `interactive` / `auto` 下的处理方式不同，但节点语义都必须保留：

1. **规格真人确认**：`hf-spec-review` 返回 `通过` 后进入
2. **设计真人确认**：`hf-design-review` 返回 `通过` 后进入
3. **任务真人确认**：`hf-tasks-review` 返回 `通过` 后进入
4. **测试用例设计确认**：`hf-test-driven-dev` 在进入 Red-Green-Refactor 前进入

处理规则：

- `interactive`：approval step 会暂停执行并等待用户输入
- `auto`：approval step 只有在 policy 允许且 approval record 已写入后，才算完成并可继续进入下游节点
- 若 `auto` 模式下无法写 approval record、无法绑定上游 record / artifact hash，或当前 approval kind 被 policy 禁止，则该 approval step 升级为 hard stop

### auto 与"用户验收"的边界

`auto` 模式与 HF 三条不可让步的协作纪律（**方向 / 取舍 / 标准最终权在用户**；**HF 不替用户验收自己**；**HF 永远不假装架构师**）共存，必须遵守以下边界，避免把"自动落盘"误读为"代理验收"：

- **approval record 是组织策略下的可追溯代理**，记录"在已声明 policy 下，何节点放行、绑定的上游 record / artifact hash 是什么"。
- **它不替代产品负责人对最终产物（spec / design / 上线候选物）的真人确认**。`auto` 只改变等待方式，不改变 approval 语义；任何节点都不得以"已 auto 通过"为由跳过 review、gate 或 approval 工件本身。
- **soul 兜底优先级高于 policy**：当 policy 未覆盖、与 soul 第 1 条冲突、或当前请求触及方向 / 取舍 / 标准空白时，必须升级为 hard stop 并回到父会话，**不得**以 auto policy 兜底。
- **严格合规场景**可在 项目约定声明禁用 `auto`；router 必须遵守，不允许任何节点在该范围内自动放行。
- **超范围信号**：当 reviewer / gate 反馈触及方向 / 取舍 / 标准本身（而非工件正确性），即使 policy 允许 auto，也必须按 hard stop 回到用户，由用户重新拍板。

## Hard Stop

只有以下场景才停止自动推进并等待用户输入或显式报告阻塞：

1. **规格评审 / 设计评审需修改（interactive）**：`hf-spec-review` 或 `hf-design-review` 返回 `需修改`，或返回内容回修型 `阻塞` 时，先向用户展示评审结论和修订重点，再回到相应上游修订 skill
2. **规格评审 / 设计评审需修改但方向不清（auto）**：`hf-spec-review` 或 `hf-design-review` 返回 `需修改` 或内容回修型 `阻塞`，且当前修订方向无法唯一界定
3. **规格评审 / 设计评审需重编排**：若 `hf-spec-review` 或 `hf-design-review` 返回 `阻塞`，且 `reroute_via_router=true` 或 `next_action_or_recommended_skill=hf-workflow-router`，先展示阻塞原因，再回到 `hf-workflow-router` 重编排
4. **证据冲突需澄清**：工件状态互相矛盾，且无法用保守原则自动解决时
5. **其他 review / gate 结论为 `需修改` 或 `阻塞` 且修订方向不明确**：需要与用户讨论修订方案或显式报告当前阻塞
6. **Auto policy / 环境阻塞**：项目约定明确禁止当前场景 auto resolve，或缺少最小可路由工件、approval record 落点、验证环境或外部依赖
7. **下一个任务不唯一或 ready 判定冲突**：`hf-completion-gate` 已通过，但剩余任务候选不唯一、依赖状态冲突，或 task board / 任务计划无法稳定判断唯一 `next-ready task`
8. **Worktree 阻塞**：当前 `Workspace Isolation=worktree-required`，但目录选择、ignore 校验、基线验证或路径落盘失败，导致无法安全进入实现

## 非暂停点

以下转场不需要等待用户确认，应在同一轮中自动推进：

- 路由完成后进入目标 skill，并在需要时继续完成 `worktree-required` 的隔离工作目录准备
- 执行型 skill 完成后进入下一个能力型 skill（如 `hf-specify` 完成 → `hf-spec-review`）
- review / gate 结论为"通过"后进入迁移表中的下一个节点（`interactive` 下的 approval step 除外）
- `auto` 模式下，approval step 在 approval record 写入后继续进入下游节点
- `auto` 模式下，`hf-spec-review` / `hf-design-review` 返回 `需修改` 且修订方向明确时，可自动回到上游 skill 继续修订
- 除 `hf-spec-review` / `hf-design-review` 外，review / gate 结论为"需修改"且修订方向明确时，自动回到上游 skill 继续修订
- 当前任务的 `hf-completion-gate` 返回 `通过` 后，若 router 能唯一锁定 `next-ready task`，则回 router 并在同一轮继续进入 `hf-test-driven-dev`
- 恢复编排协议判断出唯一下一推荐节点时

## 连续执行的红旗信号

如果你发现自己在非暂停点输出路由报告后停下来等用户回复，这说明你把路由报告当成了用户交互，而不是内部编排步骤。正确做法是把路由说明嵌入执行流中，然后立刻进入目标 skill。

如果你发现自己把 `auto` 理解成“可以跳过 approval record、review 或 gate”，这说明你把交互模式误当成了流程删减开关。正确做法是保留原有节点语义，只改变等待方式。

## 路由失败模式与恢复

如果出现以下情况，不要继续凭感觉推进：

- **证据冲突**：不同工件指向不同阶段时，先报告冲突，再按保守原则回到更上游节点
- **路由抖动**：同一轮里在两个节点之间来回切换但没有新证据时，停止切换，明确说明缺少哪个决定性证据
- **迁移表缺口**：若某结论无法映射到唯一下一推荐节点，回到 `hf-workflow-router` 重编排，而不是自行补脑
- **下一任务选择歧义**：当前任务虽已完成，但 approved / ready 的剩余任务不唯一，或依赖状态与 `Current Active Task` 投影冲突；此时停止自动推进，报告缺少的决定性证据
- **profile 不稳**：若新证据触发 upgrade 条件，先升级 profile 并写明原因，再继续路由
- **显式交接不可解析**：若 `Next Action Or Recommended Skill` 是自由文本、无法唯一归一化，明确忽略该值并按迁移表 + 工件证据继续编排
- **auto 落盘失败**：若 approval step 无法写出可回读的 approval record，停止自动推进并显式报告
- **worktree 上下文丢失**：若当前实现或 review 明明绑定了 `worktree-active`，但恢复编排后丢失 `Worktree Path` / `Worktree Branch`，先修复状态工件，再继续

如果已经连续两次因为同一类证据缺口而无法稳定路由，应明确把它报告为当前阻塞，而不是继续重复解释同一状态机判断。

## 何时回到 Router 重编排

以下场景应明确回到 `hf-workflow-router`，而不是沿用上一轮印象继续推进：

- 用户说"继续"，需要根据当前最新工件重新判断阶段
- 某个 review / gate 刚完成，需要根据结论和 profile 迁移表恢复编排
- 用户提出新的范围变化、验收变化或紧急缺陷线索，需要判断是否切到 `hf-increment` / `hf-hotfix`
- 当前证据与既有阶段判断冲突，无法直接延续原路线
- 需要进行 profile 升级
- 当前任务的 `hf-completion-gate` 已通过，需要判断是重选下一任务还是进入 `hf-finalize`
- reviewer 显式返回 `reroute_via_router=true`，或把 `next_action_or_recommended_skill` 指向 `hf-workflow-router`

## 路由红旗信号

出现以下想法时，先停下。这通常说明你正在为“跳过流程”找理由：

| 想法 | 实际要求 |
|---|---|
| "这只是个简单请求，可以直接做" | 简单请求也要先判断当前阶段和 profile。 |
| "我先快速看看代码再说" | 先路由，再按目标 skill 的要求读代码。 |
| "我先多收集一点信息更稳妥" | 路由只读取最少必要证据，不先做大范围探索。 |
| "用户都说继续了，应该就是实现" | "继续"不等于实现，必须先检查规格、设计、任务和进度证据。 |
| "用户只是让我做 review，不算进入流程" | review / gate 请求也属于 workflow 编排的一部分，仍要先做路由判断。 |
| "文档大概已经齐了，先往下推进吧" | 没有明确批准证据，就按未批准处理。 |
| "这个流程太完整了，先跳一步节省时间" | 如果觉得流程过重，应评估是否适用更轻的 profile，而不是在当前 profile 内跳步。 |
| "热修复很急，可以先改再补流程" | 热修复也必须先进入 `hf-hotfix`，不能绕过复现、评审和门禁。 |
| "这是个小变更，不用走变更支线" | 只要是需求或范围变化，就先判断是否应进入 `hf-increment`。 |
| "我已经知道现在在哪个阶段了" | 结论必须绑定当前工件证据，而不是依赖印象或聊天记忆。 |
| "用户已经点名某个 hf skill，就不用再经过入口了" | 点名 skill 也不等于当前时机正确，仍要由 router 判断是否应进入它。 |
| "先做一点实现，后面再补 route 说明" | 路由必须先完成，之后才能进入下游 skill。 |
| "这个改动很小，直接用 lightweight 就行" | Profile 由 router 根据信号判断，不允许用户或 agent 自行声称。 |
| "feature `progress.md` 都写到实现了，可以直接下游继续" | 若它与批准状态或 review / gate 证据冲突，优先相信更保守、更上游的证据。 |
| "没有明确热修复 / 变更证据，也可以先进支线处理" | 进入 `hf-hotfix` / `hf-increment` 必须有对应信号，不能把支线当快捷方式。 |
| "缺了一两个评审或门禁也没关系，先推进再补" | 缺少必需 review / gate / approval step 证据时，不允许继续向下游推进。 |
| "standard / lightweight 已经够了，不用升级" | 一旦发现缺上游依据或复杂度超出当前假设，就要升级 profile。 |
| "既然是 auto，就把确认节点从链路里省掉" | `auto` 只改变 confirmation 的解决方式；approval 节点仍然存在，且必须落盘。 |
| "`worktree-required` 只是建议，我先在当前工作区改了再说" | worktree 隔离一旦被要求，就是执行前置条件；不能先改后补。 |

## 输出与交接语义

路由判断是内部编排步骤，不是需要用户确认的独立消息。

完成路由后，将路由结论作为简短内联说明嵌入执行流中，然后立刻进入目标 skill。不要把路由结论作为独立消息发送后等待用户回复。

仅在以下情况补充详细说明：

- 存在证据冲突
- 发生了 profile 升级
- 当前是 review / gate 后的恢复编排且跳转不直观

若目标是 review 节点，则立刻派发 reviewer subagent。唯一例外：当路由结果指向 `interactive` 下的 approval step 或 hard stop 时，才需要等待用户输入。

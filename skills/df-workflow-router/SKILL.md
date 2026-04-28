---
name: df-workflow-router
description: Use when the user says "继续/推进" and the canonical df node must be decided from artifact evidence, when a review/gate just finished and orchestration must resume, when route/stage/profile is unclear or artifact evidence conflicts, when deciding whether to enter component-impact / hotfix profile, or when dispatching reviewer subagents for spec/component-design/ar-design/test-check/code-review. Not for new-session family discovery (→ using-df-workflow), not for authoring/reviewing/implementing inside a leaf node (→ corresponding df-* skill).
---

# df Workflow Router

df workflow family 的 **runtime authority**。基于工件证据决定：Workflow Profile、Execution Mode、canonical `df-*` 节点、是否进入 component-impact 或 hotfix 支线、review subagent 派发，以及 review / gate 后的恢复编排。

`using-df-workflow` 负责 public entry 与意图分流；本 skill 负责 runtime routing 与恢复。

df 默认以单 AR / 单 DTS 为最小开发单元，不维护 task queue。本 skill 不替模块架构师、开发负责人、开发人员拍板任何专业判断；只负责把工件证据转化为唯一下一步。

## When to Use

适用：

- 用户说"继续 / 推进"，需依据工件判断当前节点
- review / gate 刚完成，需消费结论并决定下一步
- route / stage / profile 不清，或工件证据冲突
- 需判断是否进入 `df-component-design`（component-impact）或 `df-problem-fix`（hotfix）
- 需派发 reviewer subagent 执行 spec / component-design / ar-design / test-check / code-review
- reviewer subagent 返回 `reroute_via_router=true`

不适用 → 改用：

- 新会话 family discovery → `using-df-workflow`
- 节点内部 authoring / review / 实现 → 对应 `df-*` leaf skill

## Hard Gates

- 不替模块架构师 / 开发负责人 / 开发人员拍板专业判断
- 不在父会话内联做 review；review 节点必须派发独立 reviewer subagent
- Profile 一旦升级（standard → component-impact / hotfix），不允许在同一 work item 内静默降级
- 缺组件实现设计但本次修改影响组件边界 → 必须升级到 `component-impact` profile，路由到 `df-component-design`
- AR 实现设计未含测试设计章节 → 不得路由到 `df-tdd-implementation`，必须回 `df-ar-design`
- TDD 完成后未经 `df-test-checker` 审查 → 不得路由到 `df-code-review`
- review / gate 结论无法唯一映射下一步 → 标 `reroute_via_router=true`，停下让父会话重新评估

## Object Contract

- Primary Object: routing 决定（profile + execution mode + canonical 节点 + reviewer 派发）
- Frontend Input Object: `features/<id>/progress.md`、`reviews/`、`evidence/`、`completion.md`、用户最新请求
- Backend Output Object: 唯一下一步 + 必要的 reviewer 派发说明 + 状态字段同步
- Transformation: 把工件证据转化为唯一 canonical 节点
- Boundaries: 不写设计 / 不写代码 / 不替 reviewer 给出 verdict
- Invariants: profile / execution mode 一旦决定，不允许 leaf 节点自改；canonical 节点名严格使用 `df-*` 前缀

## Methodology

- **Finite State Machine Routing**: workflow 阶段建模为 FSM，每条转移由工件状态驱动
- **Evidence-Based Decision Making**: 所有路由判断基于磁盘证据，证据冲突时取保守策略（更上游节点 / 更高 profile）
- **Escalation Pattern**: 只允许向上升级 profile（standard → component-impact / hotfix），不允许降级
- **Role-Separated Review Dispatch**: review 必须派发独立 reviewer subagent，不内联，不让 author 自审
- **Read-On-Presence**: 项目当前未启用的可选资产（如 `docs/runbooks/`）缺失不阻塞路由

## Workflow

### 1. 确认是否属于 runtime routing

如果是 public entry / family discovery → 回 `using-df-workflow`。否则（恢复编排、profile 判断、消费 review/gate 结论、evidence conflict、切支线）继续。

### 2. 读取最少必要证据

按 Read-On-Presence 原则只读路由所需的最少内容：项目 `AGENTS.md` 路径映射、用户请求、`features/<id>/progress.md`、`features/<id>/reviews/` 与 `features/<id>/completion.md`、`docs/component-design.md` / `docs/ar-designs/`（必要时）。不在路由阶段做大范围代码探索。证据冲突 → 选更上游节点 / 升级 profile，不擅自调和。

### 3. 检查支线信号

支线优先于普通主链：

| 信号 | 路由 |
|---|---|
| DTS / 紧急缺陷 / 已上线问题修复 | `df-problem-fix`，profile = `hotfix` |
| 新增组件 / 修改 SOA 接口 / 修改组件职责 / 修改组件依赖 / 组件设计缺失或过期 | profile 升级到 `component-impact`，下一步 `df-component-design` |
| AR 实现需要跨组件协调 | profile = `component-impact` |

命中支线 → 走对应路径，不再回主链。

### 4. 决定 Workflow Profile

按 Escalation Pattern：先执行 `AGENTS.md` 强制规则 → 沿用已有 profile → 按证据选择 → 冲突选更重。**只允许升级，不允许降级**。

| Profile | 适用场景 |
|---|---|
| `standard` | 既有组件 AR 增量、组件设计稳定、纯组件内修改 |
| `component-impact` | 命中步骤 3 component-impact 信号 |
| `hotfix` | 命中步骤 3 hotfix 信号 |
| `lightweight` | 极小、低风险、纯局部修改（错别字 / magic number / 注释）；保留 specify → completion 全链，仅允许压缩文档量 |

详细规则见 `references/profile-and-route-map.md`。

### 5. 决定 Execution Mode

与 Profile 正交。归一化顺序：用户显式要求 → `AGENTS.md` 默认 → 已有值 → 默认 `interactive`。`auto` 不删除 review / gate / approval，也不让 leaf 节点静默降级。

### 6. 归一化显式 handoff

leaf skill 返回的 `next_action_or_recommended_skill` 是受控字段。检查它是否归一化、是否与最新 evidence 一致、是否在当前 profile 合法集合内（见 `references/profile-and-route-map.md`）。全部满足才采用；否则忽略，回退到迁移表。

### 7. 决定 canonical 节点

路由原则：支线优先于主链 → review / gate 恢复优先于实现 → 缺失上游优先于下游 → 冲突选更保守。

迁移意图（与 `docs/df-principles/04 workflow-architecture.md` 一致）：

| 当前节点 | 成功后 | 需修改 / 阻塞 |
|---|---|---|
| `df-specify` | `df-spec-review` | 回需求负责人 / `df-workflow-router` |
| `df-spec-review` | `df-component-design`（component-impact）/ `df-ar-design`（standard / lightweight） | `df-specify` |
| `df-component-design` | `df-component-design-review` | 继续修订 |
| `df-component-design-review` | `df-ar-design` | `df-component-design` |
| `df-ar-design` | `df-ar-design-review` | 继续修订 |
| `df-ar-design-review` | `df-tdd-implementation` | `df-ar-design` |
| `df-tdd-implementation` | `df-test-checker` | 继续实现 |
| `df-test-checker` | `df-code-review` | `df-tdd-implementation` |
| `df-code-review` | `df-completion-gate` | `df-tdd-implementation` |
| `df-completion-gate` | `df-finalize` | 缺什么回什么 |
| `df-finalize` | workflow closed | 回 router |
| `df-problem-fix` | `df-ar-design` 或 `df-tdd-implementation` | 继续 hotfix 分析 |

若结论无法映射唯一节点 → 标 `reroute_via_router=true` 停下。

### 8. 处理 review / gate 恢复

读取最新 review record / completion record，按 verdict 与角色边界判定：

- `通过` → 进入迁移表的成功后节点；`needs_human_confirmation=true` 时按 Mode 处理（interactive 等真人，auto 写 approval record）
- `需修改` / `阻塞`（内容） → 回授权节点（如 `df-tdd-implementation` / `df-ar-design`）
- `阻塞`（workflow） → `reroute_via_router=true`，停下并写明阻塞原因

### 9. 派发 reviewer subagent

review 节点不在父会话内联执行。构造最小 review request（`target_skill`、`work_item_id`、`owning_component`、`primary_artifact`、`supporting_context`、`agents_md_anchor`、`expected_return_contract`），派发独立 subagent，消费结构化 reviewer 返回。详见 `references/reviewer-dispatch-protocol.md`。

### 10. 连续执行与暂停点

路由结论不是独立用户交互：

- 非 hard stop → 同一轮进入目标 skill
- review 节点 → 立刻派发 subagent
- approval step → 按 Execution Mode 处理
- hard stop（缺组件设计、缺测试设计章节、TDD 后未经 test-checker 等）→ 必须停下等待

## Output Contract

最小输出：

- `Current Stage`
- `Workflow Profile`
- `Execution Mode`
- `Target Skill`（唯一 canonical `df-*` 节点）
- `Why`（1-2 条决定性证据）
- `reroute_via_router`：`false`（已唯一映射）或 `true`（无法唯一映射，等待父会话）

evidence 充足时使用紧凑格式；不回放未命中分支，不复述 authority 说明。

runtime canonical 字段统一：`df-workflow-router`、`reroute_via_router`，不出现自由文本下一步。

## Red Flags

- 没经过 router 就跨节点切换
- 因命令名 / 用户点名跳过 route / profile 判断
- 把 `using-df-workflow` 写进 runtime handoff
- 在 route 阶段做大范围代码探索
- 忽略证据冲突沿用旧印象推进
- 把 `auto` 解读为「不写 review record / 不要 approval」
- 父会话内联 review，没派发 reviewer subagent
- profile 不再成立却不升级（如修改影响 SOA 接口却仍走 standard）

## Common Mistakes

| 错误 | 修复 |
|---|---|
| TDD 完成后直接路由到 `df-code-review` | 必须先派发 `df-test-checker` |
| 看到 AR 设计修改了组件接口，仍走 standard | 升级到 component-impact，先 `df-component-design` |
| review 返回 `阻塞`(workflow) 还硬选下一节点 | 标 `reroute_via_router=true` 停下 |

## Verification

- [ ] 已确认是 runtime routing（非 family discovery）
- [ ] 已基于最新证据决定 Workflow Profile，并执行升级判断
- [ ] 已归一化 Execution Mode 且未违反 policy
- [ ] 已验证显式 handoff 合法性
- [ ] 推荐节点在当前 profile 合法集合内
- [ ] review 节点已派发独立 reviewer subagent
- [ ] hard stop 命中时已显式停下且写明原因
- [ ] 非 hard stop 时在同一轮继续执行
- [ ] 字段名严格使用 `df-workflow-router` 与 `reroute_via_router`

## Supporting References

| 文件 | 用途 |
|---|---|
| `skills/docs/df-workflow-shared-conventions.md` | profile 与节点合法集合、handoff 字段、路径约定 |
| `references/profile-and-route-map.md` | 各 profile 主链与支线 |
| `references/reviewer-dispatch-protocol.md` | reviewer subagent 派发协议与返回契约 |
| `docs/df-principles/04 workflow-architecture.md` | 主链路、Hard Stops、Methodology Map |

---
name: mwf-workflow-router
description: Use when the user says "继续/推进" and the canonical mwf node must be decided from artifact evidence, when a review/gate just finished and orchestration must resume, when route/stage/profile is unclear or artifact evidence conflicts, when deciding whether to enter component-impact / hotfix profile, or when dispatching reviewer subagents for spec/component-design/ar-design/test-check/code-review. Not for new-session family discovery (→ using-mwf-workflow), not for authoring/reviewing/implementing inside a leaf node (→ corresponding mwf-* skill).
---

# mwf Workflow Router

mwf workflow family 的 **runtime authority**。基于工件证据决定：Workflow Profile、Execution Mode、canonical `mwf-*` 节点、是否进入 component-impact 或 hotfix 支线、review subagent 派发，以及 review / gate 后的恢复编排。

`using-mwf-workflow` 负责 public entry 与意图分流；本 skill 负责 runtime routing 与恢复。

mwf 默认以单 AR / 单 DTS 为最小开发单元，不维护 task queue。本 skill 不替模块架构师、开发负责人、开发人员拍板任何专业判断；只负责把工件证据转化为唯一下一步。

## When to Use

适用：

- 用户说"继续 / 推进"，需依据工件判断当前节点
- review / gate 刚完成，需消费结论并决定下一步
- route / stage / profile 不清，或工件证据冲突
- 需判断是否进入 `mwf-component-design`（component-impact）或 `mwf-problem-fix`（hotfix）
- 需派发 reviewer subagent 执行 spec / component-design / ar-design / test-check / code-review
- reviewer subagent 返回 `reroute_via_router=true`

不适用 → 改用：

- 新会话 family discovery → `using-mwf-workflow`
- 节点内部 authoring / review / 实现 → 对应 `mwf-*` leaf skill

## Hard Gates

- 不替模块架构师 / 开发负责人 / 开发人员拍板专业判断
- 不在父会话内联做 review；review 节点必须派发独立 reviewer subagent
- Profile 一旦升级（standard → component-impact / hotfix），不允许在同一 work item 内静默降级
- 缺组件实现设计但本次修改影响组件边界 → 必须升级到 `component-impact` profile，路由到 `mwf-component-design`
- AR 实现设计未含测试设计章节 → 不得路由到 `mwf-tdd-implementation`，必须回 `mwf-ar-design`
- TDD 完成后未经 `mwf-test-checker` 审查 → 不得路由到 `mwf-code-review`
- review / gate 结论无法唯一映射下一步 → 标 `reroute_via_router=true`，停下让父会话重新评估

## Object Contract

- Primary Object: routing 决定（profile + execution mode + canonical 节点 + reviewer 派发）
- Frontend Input Object: `features/<id>/progress.md`、`reviews/`、`evidence/`、`completion.md`、用户最新请求
- Backend Output Object: 唯一下一步 + 必要的 reviewer 派发说明 + 状态字段同步
- Transformation: 把工件证据转化为唯一 canonical 节点
- Boundaries: 不写设计 / 不写代码 / 不替 reviewer 给出 verdict
- Invariants: profile / execution mode 一旦决定，不允许 leaf 节点自改；canonical 节点名严格使用 `mwf-*` 前缀

## Methodology

- **Finite State Machine Routing**: workflow 阶段建模为 FSM，每条转移由工件状态驱动
- **Evidence-Based Decision Making**: 所有路由判断基于磁盘证据，证据冲突时取保守策略（更上游节点 / 更高 profile）
- **Escalation Pattern**: 只允许向上升级 profile（standard → component-impact / hotfix），不允许降级
- **Role-Separated Review Dispatch**: review 必须派发独立 reviewer subagent，不内联，不让 author 自审
- **Read-On-Presence**: 项目当前未启用的可选资产（如 `docs/runbooks/`）缺失不阻塞路由

## Workflow

1. 确认是否属于 runtime routing
   - Object: routing 触发分类
   - Method: Front Controller / Router 边界判断
   - Input: 用户请求、是否已有 `features/<id>/progress.md`
   - Output: 是 routing 还是 family discovery
   - Stop / continue: 是 family discovery → 回 `using-mwf-workflow`；否则继续

2. 读取最少必要证据
   - Object: 工件证据基线
   - Method: Evidence-Based Decision Making + Read-On-Presence
   - Input: 项目 `AGENTS.md` 路径映射、`features/<id>/progress.md`、`reviews/`、`evidence/`、`completion.md`、`docs/component-design.md`、`docs/ar-designs/AR<id>-<slug>.md`
   - Output: 当前节点、待完成 review / gate、Profile 信号、Execution Mode 当前值
   - Stop / continue: 证据冲突 → 选更上游节点 / 升级 profile，不擅自调和

3. 检查支线信号
   - Object: 支线判定
   - Method: 触发条件匹配
   - Input: 用户请求 + 工件证据
   - Output: 是否进入 `hotfix` 或 `component-impact`
   - Stop / continue: 命中支线 → 走对应路径，不再走主链

   支线触发：

   | 信号 | 路由 |
   |---|---|
   | DTS / 紧急缺陷 / 已上线问题修复 | `mwf-problem-fix`，profile = `hotfix` |
   | 新增组件 / 修改 SOA 接口 / 修改组件职责 / 修改组件依赖 / 组件设计缺失或过期 | profile 升级到 `component-impact`，下一步 `mwf-component-design` |
   | AR 实现需要跨组件协调 | profile = `component-impact` |

4. 决定 Workflow Profile
   - Object: profile 字段
   - Method: Escalation Pattern
   - Input: 步骤 3 信号 + work item 类型
   - Output: `standard` / `component-impact` / `hotfix` / `lightweight`
   - Stop / continue: 只允许升级，不允许降级

   | Profile | 适用场景 |
   |---|---|
   | `standard` | 既有组件 AR 增量、组件设计稳定、纯组件内修改 |
   | `component-impact` | 命中步骤 3 component-impact 信号 |
   | `hotfix` | 命中步骤 3 hotfix 信号 |
   | `lightweight` | 极小、低风险、纯局部修改（如修一个错别字、调一个 magic number、补一行注释），仍保留 specify/spec-review/ar-design/ar-design-review/tdd/test-check/code-review/completion 全链，但允许压缩文档量 |

5. 决定 Execution Mode
   - Object: execution mode 字段
   - Method: 归一化优先级
   - Input: 用户最新偏好 → `AGENTS.md` 默认 → 已有值 → 默认 `interactive`
   - Output: `interactive` / `auto`
   - Stop / continue: `auto` 不删除 review / gate / approval；不让 leaf 节点静默降级

6. 归一化显式 handoff
   - Object: 上一步 leaf 返回的 `next_action_or_recommended_skill`
   - Method: 合法性校验
   - Input: leaf handoff
   - Output: 接受 / 忽略
   - Stop / continue: 显式 handoff 与最新证据一致且在当前 profile 合法集合内 → 采用；否则忽略，回退到迁移表

7. 决定 canonical 节点
   - Object: 唯一 canonical 下一步
   - Method: FSM Routing + Evidence-Based Decision
   - Input: profile 合法节点表 + 工件证据
   - Output: 唯一 `mwf-*` 节点名
   - Stop / continue: 若结论无法映射唯一节点，标 `reroute_via_router=true` 停下

   迁移意图（与 `docs/mwf-principles/04 workflow-architecture.md` 一致）：

   | 当前节点 | 成功后 | 需修改 / 阻塞 |
   |---|---|---|
   | `mwf-specify` | `mwf-spec-review` | 回需求负责人 / `mwf-workflow-router` |
   | `mwf-spec-review` | `mwf-component-design`（component-impact）/ `mwf-ar-design`（standard / lightweight） | `mwf-specify` |
   | `mwf-component-design` | `mwf-component-design-review` | 继续修订 |
   | `mwf-component-design-review` | `mwf-ar-design` | `mwf-component-design` |
   | `mwf-ar-design` | `mwf-ar-design-review` | 继续修订 |
   | `mwf-ar-design-review` | `mwf-tdd-implementation` | `mwf-ar-design` |
   | `mwf-tdd-implementation` | `mwf-test-checker` | 继续实现 |
   | `mwf-test-checker` | `mwf-code-review` | `mwf-tdd-implementation` |
   | `mwf-code-review` | `mwf-completion-gate` | `mwf-tdd-implementation` |
   | `mwf-completion-gate` | `mwf-finalize` | 缺什么回什么 |
   | `mwf-finalize` | workflow closed | 回 router |
   | `mwf-problem-fix` | `mwf-ar-design` 或 `mwf-tdd-implementation` | 继续 hotfix 分析 |

8. 处理 review / gate 恢复
   - Object: 上游 review / gate 结论
   - Method: Verdict 消费 + 角色边界
   - Input: 最新 review record / completion record
   - Output: 下一步 + 是否需要真人确认
   - Stop / continue:
     - `通过` → 进入迁移表的成功后节点
     - `需修改` → 回授权节点（如 `mwf-tdd-implementation` / `mwf-ar-design`）
     - `阻塞`（内容） → 回授权节点
     - `阻塞`（workflow） → `reroute_via_router=true`，停下并写明阻塞原因

9. 派发 reviewer subagent
   - Object: review 任务
   - Method: Role-Separated Review Dispatch
   - Input: review 节点 + 必要工件
   - Output: 独立 reviewer subagent 的最小 review request
   - Stop / continue: review 不内联在父会话；reviewer 返回结构化摘要 + record path

   review 派发的最小 request 字段：

   - `target_skill`：`mwf-spec-review` / `mwf-component-design-review` / `mwf-ar-design-review` / `mwf-test-checker` / `mwf-code-review`
   - `work_item_id`、`owning_component`
   - `primary_artifact`：被评审对象路径
   - `supporting_context`：上游工件路径
   - `agents_md_anchor`：项目 `AGENTS.md` 中相关约定
   - `expected_return_contract`：见 mwf-shared-conventions

10. 连续执行与暂停点
    - Object: 是否需等待真人
    - Method: hard stop 检测
    - Input: 步骤 7-8 的结论
    - Output: 同一轮继续 / 等待真人
    - Stop / continue:
      - `interactive` + `通过` 且需要真人确认（如 AR 实现设计 review 通过 → 等待开发负责人确认）→ 等
      - `auto` + 无 hard stop → 同一轮进入下一节点
      - hard stop（缺组件设计、缺测试设计章节、TDD 后未经 test-checker 等）→ 必须停

## Output Contract

最小输出：

- `Current Stage`
- `Workflow Profile`
- `Execution Mode`
- `Target Skill`（唯一 canonical `mwf-*` 节点）
- `Why`（1-2 条决定性证据）
- `reroute_via_router`：`false`（已唯一映射）或 `true`（无法唯一映射，等待父会话）

evidence 充足时使用紧凑格式；不回放未命中分支，不复述 authority 说明。

runtime canonical 字段统一：`mwf-workflow-router`、`reroute_via_router`，不出现自由文本下一步。

## Red Flags

- 没经过 router 就跨节点切换
- 因命令名 / 用户点名跳过 route / profile 判断
- 把 `using-mwf-workflow` 写进 runtime handoff
- 在 route 阶段做大范围代码探索
- 忽略证据冲突沿用旧印象推进
- 把 `auto` 解读为「不写 review record / 不要 approval」
- 父会话内联 review，没派发 reviewer subagent
- profile 不再成立却不升级（如修改影响 SOA 接口却仍走 standard）

## Common Mistakes

| 错误 | 修复 |
|---|---|
| TDD 完成后直接路由到 `mwf-code-review` | 必须先派发 `mwf-test-checker` |
| 看到 AR 设计修改了组件接口，仍走 standard | 升级到 component-impact，先 `mwf-component-design` |
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
- [ ] 字段名严格使用 `mwf-workflow-router` 与 `reroute_via_router`

## Supporting References

| 文件 | 用途 |
|---|---|
| `skills/docs/mwf-workflow-shared-conventions.md` | profile 与节点合法集合、handoff 字段、路径约定 |
| `references/profile-and-route-map.md` | 各 profile 主链与支线 |
| `references/reviewer-dispatch-protocol.md` | reviewer subagent 派发协议与返回契约 |
| `docs/mwf-principles/04 workflow-architecture.md` | 主链路、Hard Stops、Methodology Map |

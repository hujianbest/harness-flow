---
name: mwf-component-design-review
description: Use when mwf-component-design has produced a component-design-draft.md ready for an independent verdict, when a reviewer subagent is dispatched to evaluate component boundaries / SOA interfaces / dependencies / state machines / runtime mechanisms, or when component design needs re-review after revision. Not for writing or revising component design (→ mwf-component-design), not for AR-level design review (→ mwf-ar-design-review), not for stage / route confusion (→ mwf-workflow-router).
---

# mwf 组件实现设计评审

独立评审 `features/<id>/component-design-draft.md`，判断它是否可作为下游 `mwf-ar-design` 的稳定输入，以及是否可由 `mwf-finalize` 同步到 `docs/component-design.md`。

本 skill 不写设计 / 不替模块架构师拍板组件边界 / 不修改设计草稿。它只产出 verdict + findings + 唯一下一步。

## When to Use

适用：

- `mwf-component-design` 已产出 component-design-draft.md，需正式 verdict
- reviewer subagent 被派发执行组件设计评审
- 用户明确要求「review 这份组件设计」

不适用 → 改用：

- 缺草稿或仅需继续写 → `mwf-component-design`
- AR 代码层设计评审 → `mwf-ar-design-review`
- 阶段不清 / 证据冲突 → `mwf-workflow-router`

## Hard Gates

- 组件设计通过本 review 之前，不得进入 `mwf-ar-design`
- reviewer 不修改设计草稿
- reviewer 不替模块架构师拍板组件边界 / SOA 接口 / 跨组件协调
- reviewer 不返回多个候选下一步
- 模块架构师 sign-off 是 `通过` 的硬性 USER-INPUT 项；缺 sign-off 的 `通过` 必须标 `needs_human_confirmation=true`

## Object Contract

- Primary Object: component design finding set + verdict
- Frontend Input Object: `features/<id>/component-design-draft.md`、`features/<id>/requirement.md`、`features/<id>/traceability.md`、当前 `docs/component-design.md`（如存在；用于对比修订前后）、`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（若存在）、`AGENTS.md` 团队模板覆盖
- Backend Output Object: `features/<id>/reviews/component-design-review.md` + 结构化 reviewer 返回摘要
- Object Transformation: 把组件设计草稿审查成发现项集合 + 唯一 verdict + 唯一下一步
- Object Boundaries: 不修改被评审工件 / 不顺手优化设计 / 不替团队角色拍板
- Object Invariants: verdict 必为 `通过` / `需修改` / `阻塞` 之一

## Methodology

- **SOA Component Boundary Analysis**: 检查组件职责、接口、服务契约、依赖方向、跨组件影响
- **Clean Architecture Boundary Discipline**: 检查依赖方向稳定性、实现细节是否倒灌
- **Interface Segregation Check**: SOA 接口是否最小知识、是否聚合多个无关用途
- **Template Conformance Check**: 是否符合团队组件设计模板（含模板未补齐时的占位声明）
- **Embedded Risk Review**: 检查并发、实时性、资源生命周期、错误处理、ABI / API 兼容性
- **Cross-Component Impact Audit**: 跨组件影响是否被显式列出且与下游组件的协调路径明确

## Workflow

1. 建立证据基线
   - Object: 评审输入证据基线
   - Method: Evidence-Based + Read-On-Presence
   - Input: component-design-draft.md、requirement.md、traceability.md、当前 docs/component-design.md、docs/interfaces.md / dependencies.md / runtime-behavior.md（如存在）、`AGENTS.md`
   - Output: 输入清单 + 模板状态（团队模板是否已补齐）+ 模块架构师 owner
   - Stop / continue: spec-review 未通过 → blocked-workflow，`reroute_via_router=true`

2. Precheck
   - Object: precheck 结论
   - Method: 三态判定
   - Input: 步骤 1 输入清单
   - Output: 通过 / blocked-content / blocked-workflow
   - Stop / continue:
     - 缺设计草稿 → blocked-content，下一步 `mwf-component-design`
     - route / stage / profile 冲突（如未升级 component-impact 却进入本节点） → blocked-workflow，`reroute_via_router=true`，下一步 `mwf-workflow-router`

3. 多维评分
   - Object: 7 维度评分
   - Method: Structured Walkthrough
   - Output: 各维度 0-10 评分
   - Stop / continue: 任一关键维度 < 6 不得 `通过`

   维度（详见 `references/component-design-review-rubric.md`）：

   | 维度 | 关注 |
   |---|---|
   | CD1 Identity & Template Conformance | Owner、组件名、子系统、模板章节齐全（或显式标注占位） |
   | CD2 Responsibility & Non-Responsibility | 职责 / 非职责清晰，未承接其他组件职责 |
   | CD3 SOA Interface Quality | 接口名 / 参数 / 错误码 / 时序约束 / 兼容性完整 |
   | CD4 Dependency & Direction | 依赖方向无环、初始化 / shutdown 顺序明确、版本约束清晰 |
   | CD5 Data Model & State Machine | 数据 / 状态机覆盖核心生命周期、转换条件清晰 |
   | CD6 Concurrency / Real-time / Resource / Error Handling | 中断上下文限制、锁策略、资源回收、错误处理清晰 |
   | CD7 AR Design Constraints & Cross-Component Impact | 「对 AR 实现设计的约束」章节存在；跨组件影响显式列出 |

4. 正式 checklist 审查
   - Object: findings 集合
   - Method: Checklist-Based Review
   - Input: rubric
   - Output: findings 含 severity / classification / rule_id（CD1-CD7 + 子项）/ anchor / 描述 / 建议修复

5. 形成 verdict
   - Object: 唯一 verdict + 唯一下一步
   - Method: Verdict 决策

   | 条件 | conclusion | next_action_or_recommended_skill | reroute_via_router | needs_human_confirmation |
   |---|---|---|---|---|
   | 7 维度均 ≥ 6，无 critical USER-INPUT，模块架构师可被请求 sign-off | `通过` | `mwf-ar-design` | `false` | `true`（等模块架构师 sign-off） |
   | findings 可 1-2 轮定向修订 | `需修改` | `mwf-component-design` | `false` | `false` |
   | 组件边界 / SOA 接口严重不清 / 跨组件协调缺失 | `阻塞`（内容） | `mwf-component-design` | `false` | `false` |
   | route / stage / profile / 上游证据冲突 | `阻塞`（workflow） | `mwf-workflow-router` | `true` | `false` |

6. 写 review 记录
   - Object: review record
   - Output: `features/<id>/reviews/component-design-review.md`，按 `templates/mwf-review-record-template.md`

7. 回传结构化摘要
   - Output: 按 `mwf-workflow-router/references/reviewer-dispatch-protocol.md`

## Output Contract

- Review record：`features/<id>/reviews/component-design-review.md`
- 结构化 reviewer 返回摘要含 record_path、conclusion、key_findings、finding_breakdown、next_action_or_recommended_skill、needs_human_confirmation、reroute_via_router
- `通过` 时 needs_human_confirmation 默认 `true`（等模块架构师 sign-off），由父会话决定何时进入 `mwf-ar-design`

## Red Flags

- 顺手把 AR 设计建议写进 review record
- 因「先做着试试」放过 SOA 接口不完整
- 忽略依赖方向有环
- 因模板未补齐就给 `通过`
- 跨组件影响未列出却给 `通过`
- 因「实现简单」就放过状态机覆盖不全
- findings 无分类

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 评审中「顺手」补设计章节 | reviewer 是 gate，不是 author，返回 finding 让 author 修 |
| 模块架构师未 sign-off 仍给 `通过` 且 `needs_human_confirmation=false` | 强制 `needs_human_confirmation=true` |
| 跨组件影响未审查 | 加 critical finding |

## Verification

- [ ] review record 已落盘
- [ ] precheck 结果显式记录
- [ ] 7 维度评分完整、findings 已分类
- [ ] verdict 唯一、下一步唯一、`reroute_via_router` 正确
- [ ] `通过` 时 `needs_human_confirmation=true` 等模块架构师 sign-off
- [ ] 结构化摘要已回传父会话
- [ ] 未顺手修改设计草稿

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/component-design-review-rubric.md` | 7 维度 rubric + rule IDs |
| `skills/templates/mwf-review-record-template.md` | review record 模板 |
| `mwf-workflow-router/references/reviewer-dispatch-protocol.md` | reviewer 返回契约 |
| `skills/docs/mwf-workflow-shared-conventions.md` | handoff 字段、路径约定 |

---
name: df-spec-review
description: Use when a requirement.md draft from df-specify is ready for an independent verdict, when a reviewer subagent is dispatched to evaluate the spec for clarity / traceability / designability, or when spec-review needs to be re-run after the author revised in response to earlier findings. Not for writing or revising the spec itself (→ df-specify), not for component or AR design review (→ df-component-design-review / df-ar-design-review), not for stage / route confusion (→ df-workflow-router).
---

# df 需求规格评审

独立评审 `features/<id>/requirement.md`，判断它是否可作为 `df-component-design`（component-impact）或 `df-ar-design`（standard / lightweight）的稳定输入。

本 skill 不写规格、不替需求负责人补业务事实、不替模块架构师决定组件归属。它只对规格对象给出 verdict + findings，并把唯一下一步交回父会话。

## When to Use

适用：

- `df-specify` 已产出 requirement.md 草稿，需正式 verdict
- reviewer subagent 被派发执行 spec 评审
- 用户明确要求「review 这份规格 / 评审需求」

不适用 → 改用：

- 缺规格或仅需继续写 → `df-specify`
- 阶段不清 / 证据冲突 → `df-workflow-router`
- 已有批准规格、需要做组件 / AR 设计评审 → `df-component-design-review` / `df-ar-design-review`

## Hard Gates

- 规格通过本 review 之前，不得进入 `df-component-design` 或 `df-ar-design`
- reviewer 不修改 requirement.md
- reviewer 不替需求负责人 / 模块架构师补业务事实、优先级、阈值
- reviewer 不返回多个候选下一步
- 工件不足以判定 stage / route → `reroute_via_router=true`，回 `df-workflow-router`

## Object Contract

- Primary Object: spec finding set + verdict
- Frontend Input Object: `features/<id>/requirement.md`、`features/<id>/traceability.md`、`features/<id>/progress.md`、组件仓库 `docs/component-design.md`（如存在）、IR / SR / AR 上游锚点
- Backend Output Object: `features/<id>/reviews/spec-review.md` + 结构化 reviewer 返回摘要
- Object Transformation: 把规格对象审查成发现项集合 + 唯一 verdict + 唯一下一步
- Object Boundaries: 不修改被评审工件 / 不顺手做设计 / 不替团队角色拍板
- Object Invariants: verdict 必为 `通过` / `需修改` / `阻塞` 之一，下一步必为 canonical df-* 节点名

## Methodology

- **Structured Walkthrough (Fagan Inspection, adapted)**：按 rubric 维度评分，量化判断；不做自由阅读式评审
- **Checklist-Based Review**：使用结构化检查清单覆盖 6 类质量维度
- **Separation Of Author / Reviewer**：reviewer 与 author 必须不同角色或 subagent
- **Evidence-Based Verdict**：每条 finding 必须锚定 requirement.md 的具体行 / 章节
- **Team Role Discipline**：业务事实 / 优先级 / 验收阈值缺失时分类为 `USER-INPUT`，由父会话上抛需求负责人

## Workflow

### 1. 建立证据基线

按 Evidence-Based + Read-On-Presence 读取 `features/<id>/requirement.md`、`features/<id>/traceability.md`、`features/<id>/progress.md`、`docs/component-design.md`（若存在）、`AGENTS.md` 模板覆盖。不依赖会话记忆判断「已批准」或「规格已经讲清楚」。

### 1.5 Precheck

判断能否合法进入 review：

- 缺规格 / 缺 traceability → 写最小 blocked record，下一步 `df-specify`
- route / stage / profile 冲突 → 写最小 blocked record，`reroute_via_router=true`，下一步 `df-workflow-router`
- 否则进入步骤 2

### 2. 多维评分与挑战式审查

按 Structured Walkthrough 对 6 个维度（详见 `references/spec-review-rubric.md`）做 0-10 评分；任一关键维度 < 6 不得 `通过`。

| 维度 | 关注 |
|---|---|
| S1 Identity & Traceability | Work Item Type / ID、所属组件唯一、IR / SR / AR 锚点齐全 |
| S2 Scope & Non-Scope Clarity | 范围与非范围显式且不冲突 |
| S3 Requirement Row Quality | 核心 row 含 ID / Statement / Acceptance / Source / Component Impact |
| S4 Embedded NFR Quality | 实时性 / 内存 / 并发 / 资源 / 错误处理 NFR 含可判定阈值 |
| S5 Component Impact Assessment | 是否影响组件接口 / 依赖 / 状态机已显式判断 |
| S6 Open Questions Closure | 阻塞 / 非阻塞分类、阻塞项已闭合或显式 USER-INPUT |

### 3. 正式 checklist 审查

按 Checklist-Based Review 跑 4 组规则（Group Q / A / C / G，详见 `references/spec-review-rubric.md`）。每条 finding 必须带 `severity`（critical / important / minor）、`classification`（USER-INPUT / LLM-FIXABLE / TEAM-EXPERT）、`rule_id`、`anchor`、描述、建议修复。

### 4. 形成 verdict

按下表收敛唯一 verdict + 唯一下一步；不能映射下表任一行 → verdict 未收敛，回步骤 2 / 3。

| 条件 | conclusion | next_action_or_recommended_skill | reroute_via_router |
|---|---|---|---|
| 范围清晰、核心 rows 含 Acceptance、Component Impact 已判断、无阻塞 USER-INPUT、足以喂下一节点 | `通过` | `df-component-design`（Component Impact ≠ none）/ `df-ar-design`（其余） | `false` |
| 有用但不完整，findings 可 1-2 轮定向修订 | `需修改` | `df-specify` | `false` |
| 范围 / 验收 / 组件归属严重不清，findings 无法定向回修 | `阻塞`（内容） | `df-specify` | `false` |
| route / stage / profile / 上游证据冲突 | `阻塞`（workflow） | `df-workflow-router` | `true` |

### 5. 写 review 记录并回传

按 `templates/df-review-record-template.md` 写 `features/<id>/reviews/spec-review.md`，并按 `df-workflow-router/references/reviewer-dispatch-protocol.md` 回传结构化摘要（`record_path` / `conclusion` / `key_findings` / `finding_breakdown` / `next_action_or_recommended_skill` / `needs_human_confirmation` / `reroute_via_router`）。USER-INPUT 阻塞项必须显式列出，让父会话上抛需求负责人；LLM-FIXABLE 不要抛给用户。

## Output Contract

- Review record：`features/<id>/reviews/spec-review.md`（团队 `AGENTS.md` 覆盖路径优先）
- 结构化 reviewer 返回摘要含：
  - `record_path`
  - `conclusion`：`通过` / `需修改` / `阻塞`
  - `key_findings`：每条含 severity / classification / rule_id / anchor / 描述 / 建议修复
  - `finding_breakdown`：critical / important / minor 计数
  - `next_action_or_recommended_skill`：唯一 canonical df-* 节点
  - `needs_human_confirmation`：`通过` 时通常 `true`（需求负责人确认）
  - `reroute_via_router`：`true` 仅在 workflow blocker 时

## Red Flags

- 把 spec review 当成重新设计
- 因「以后再想」就放过缺失 Acceptance
- 忽略 IR / SR / AR 追溯断裂
- findings 无 USER-INPUT / LLM-FIXABLE / TEAM-EXPERT 分类
- 把 LLM-FIXABLE 问题抛给用户
- 通过后顺手开始写 AR 设计（reviewer 是 gate，不是 author）

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 缺业务阈值仍给 `通过` | 标 `USER-INPUT` 阻塞，回需求负责人 |
| Component Impact 没判断 → 给 `通过` | 标 critical finding，verdict 至少 `需修改` |
| 多个候选下一步 | 收敛为唯一 canonical 值；无法收敛即 `reroute_via_router=true` |

## Verification

- [ ] review record 已落盘
- [ ] precheck 结果显式记录
- [ ] 6 维度评分完整、findings 已分类
- [ ] verdict 唯一、下一步唯一、`reroute_via_router` 正确
- [ ] USER-INPUT 阻塞项显式列出
- [ ] 结构化摘要已回传父会话
- [ ] 未顺手修改 requirement.md

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/spec-review-rubric.md` | 6 维度 rubric + Group Q/A/C/G rule IDs |
| `skills/templates/df-review-record-template.md` | review record 模板 |
| `df-workflow-router/references/reviewer-dispatch-protocol.md` | reviewer 返回契约 |
| `skills/docs/df-workflow-shared-conventions.md` | handoff 字段、路径约定 |

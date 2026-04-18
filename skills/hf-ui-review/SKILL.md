---
name: hf-ui-review
description: 适用于 UI 设计草稿已完成需要正式 review verdict、或被指定为 reviewer subagent 执行 UI 设计评审的场景。不适用于需继续写或修 UI 设计（→ hf-ui-design）、评审架构/技术设计（→ hf-design-review）、需拆任务或编码（→ hf-tasks）、阶段不清或证据冲突（→ hf-workflow-router）。
---

# HF UI 设计评审

评审 UI 设计文档，判断它是否可以与 `hf-design-review` 一起进入联合 design approval。核心职责是防止过早拆任务——确保 UI 设计真正锚定规格、IA / 用户流 / 状态矩阵完整、视觉决策走 token、可访问性达标、组件边界清楚到足以进入任务规划。

本 skill 与 `hf-design-review` 是 **design stage 内的并行 review peer**：两条 review 都通过后，父会话发起联合 `设计真人确认`；任一未过，对应起草 skill 回流修订，另一条可继续稳定部分。

## Methodology

本 skill 融合以下已验证方法：

- **ATAM（Architecture Tradeoff Analysis Method, SEI, adapted to UI）**: 评审关注 UX 质量属性（可用性、可访问性、性能、国际化）驱动的 UI 决策，检查设计是否满足关键 NFR 并识别权衡点。
- **Nielsen Heuristic Evaluation**: 按 Nielsen 十大可用性启发式对关键页面与关键交互做冷读评估，量化 severity。
- **Structured Walkthrough (Fagan, adapted)**: 按 rubric 维度评分，量化判断 UI 设计质量，防止自由形式评审的随意性。
- **Separation of Author/Reviewer Roles**: UI 设计起草者和评审者必须独立，避免确认偏差。
- **Traceability to Spec**: 所有 UI 决策必须可追溯到已批准规格中的具体需求或声明的 UX NFR，防止 UI 设计漂移。

## When to Use

使用：

- `hf-ui-design` 已完成 UI 设计草稿，需要正式 review verdict
- 用户明确要求"review 这份 UI 设计"
- reviewer subagent 被父会话派发来执行 UI 设计评审

不使用：

- 需要继续写或修 UI 设计 → `hf-ui-design`
- 需要评审架构 / 模块 / API 契约 → `hf-design-review`
- 需要任务拆解或编码 → 相应下游节点
- 阶段不清或证据冲突 → `hf-workflow-router`

直接调用信号："review 这份 UI 设计"、"UI 设计评审"、"帮我看一下这个界面设计方案"。

前提条件：存在当前 UI 设计草稿、已批准规格、`AGENTS.md` 相关约定、`hf-design` 当前草稿（parallel 模式下 reviewer 需要判断 peer 交接块是否对齐）。缺 UI 设计草稿 → `hf-ui-design`；缺已批准规格或阶段不清 → `hf-workflow-router`。

## Chain Contract

读取：已批准规格、被评审 UI 设计文档、`hf-design` 当前设计（仅用于验证 peer 交接块一致性，不实际评审其内容）、`AGENTS.md` 评审约定、`task-progress.md` 当前状态、最少必要前端上下文。

产出：review 记录正文 + 结构化 reviewer 返回摘要。

评审记录落盘由 reviewer 负责；approval step 和主链推进由父会话负责（联合 design approval 的汇总判断由父会话或 router 做）。

## Hard Gates

- UI 设计未通过评审前，不得单独进入 `设计真人确认`
- `hf-design-review` 与本 skill 任一未过前，不得进入 `hf-tasks`
- 输入工件不足以判定 stage/route 时，不直接开始评审
- reviewer 不代替父会话完成 approval step，不提前拆任务或写代码
- reviewer 不跨权评审 `hf-design` 职责范围内的条目（架构、API、数据模型、后端 NFR）；发现 peer 不一致，通过 findings 标注而不是代位评审

## Iron Laws

1. **总是在实现前评审 UI 设计** — UI 结构性问题发现太晚（如 IA 错位、组件粒度错、a11y 系统性缺失），返工成本 5-20 倍
2. **不得放过只有 happy path 的 UI** — 每个关键交互的 loading / empty / error 三态必须被识别，缺失 = 设计不完整
3. **a11y 评估不可跳过** — 可访问性不是可选项；关键页面 WCAG 2.2 AA 关键项未达标 = 阻塞级问题
4. **视觉决策必须走 token** — 硬编码色值/字号/间距是系统性缺陷，不是局部问题
5. **peer 交接块不可含糊** — UI 设计与 `hf-design` 的跨界依赖必须显式写出；含糊表述不得通过

## Workflow

### 1. 建立证据基线

读取并固定证据来源：已批准规格、当前 UI 设计文档、`hf-design` 当前草稿（用于 peer 交接块比对）、`AGENTS.md` 约定、`task-progress.md` 状态、必要前端上下文（项目已有 Design System、组件库、品牌规范等）。

不要只根据会话记忆或零散聊天内容判断"已批准"或"UI 设计已经讲清楚"。

### 1.5 Precheck：能否合法进入 review

检查：

- 是否存在稳定可定位的 UI 设计草稿
- 已批准规格是否可回读，且含 UI surface 声明（未声明则本节点本不应激活，属 route 问题）
- route/stage/profile 与 approval evidence 是否一致
- `hf-design` 草稿是否至少进入可供 peer 比对的状态（若 parallel 模式）

分支：

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定 UI 设计草稿 → 写最小 blocked record，下一步 `hf-ui-design`
- 规格未声明 UI surface 却进入了本 review → 写 blocked record，`reroute_via_router=true`（说明是激活条件判定错误）
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

对 8 个维度做内部评分（`0-10`）：需求覆盖与追溯、IA 与用户流完整性、交互状态覆盖、视觉一致性与 Design Token 合规、可访问性、响应式/i18n/性能预算适配、决策质量与 trade-offs、任务规划准备度。

评分辅助区分：轻微缺口 vs 需修改 vs 阻塞。按 `references/ui-review-checklist.md` 逐项审查。

每条 finding 必须带：

- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `U1`、`U5`、`AU2`）

默认分类：

- `USER-INPUT`：品牌/语气/视觉方向需真人拍板、规格未确认的目标设备/语种、关键 UX trade-off 仍需业务侧裁决
- `LLM-FIXABLE`：缺少候选方向对比、状态矩阵不全、a11y 声明只写"达成"、组件映射缺来源/token 依赖、peer 交接块缺失或含糊

### 3. 形成结论、severity 与下一步

判定规则（详见 `references/ui-review-record-template.md`）：

- **通过**：可追溯规格、UI 决策清晰、IA/流/状态矩阵完整、token 合规、a11y 达标、peer 交接块显式、无阻塞任务规划的 UI 空洞
- **需修改**：核心可用，局部缺口可通过一轮定向修订补齐
- **阻塞**：无法支撑规格、存在无法追溯的关键新增 UI、peer 交接块与 `hf-design` 冲突不可协调、或证据链冲突

severity：`critical`（阻塞任务规划或引入 a11y/安全隐患）> `important`（应修复）> `minor`（建议改进）。

### 4. 写 review 记录并回传

按 `references/ui-review-record-template.md` 写评审记录，并返回结构化 JSON 给父会话。

下一步映射：

- `通过` → `设计真人确认`（`needs_human_confirmation=true`，等待与 `hf-design-review` 汇合）
- `需修改` → `hf-ui-design`
- `阻塞`（UI 设计内容） → `hf-ui-design`
- `阻塞`（需求漂移/规格冲突/激活条件判定错误/peer 不可协调） → `hf-workflow-router`（`reroute_via_router=true`）

## Reference Guide

按需加载详细参考内容：

| 主题 | Reference | 加载时机 |
|------|-----------|---------|
| UI 评审检查清单 | `references/ui-review-checklist.md` | 执行 Step 2 多维审查时 |
| UI 评审记录模板 | `references/ui-review-record-template.md` | 执行 Step 4 写评审记录时 |
| a11y 检查清单 | `../hf-ui-design/references/a11y-checklist.md` | 评审 U5 可访问性维度时（与 hf-ui-design 共用） |
| 交互状态清单 | `../hf-ui-design/references/interaction-state-inventory.md` | 评审 U3 交互状态覆盖时（与 hf-ui-design 共用） |

## 和其他 Skill 的区别

| 易混淆 skill | 区别 |
|-------------|------|
| `hf-ui-design` | ui-design 负责起草 UI 设计；本 skill 负责评审。起草者不能自审。 |
| `hf-design-review` | 本 skill 评审 UI 设计（IA/交互/视觉/a11y/组件）；`hf-design-review` 评审架构/模块/API/数据模型/后端 NFR。两者 peer 并行，不得跨权。 |
| `hf-tasks` | 本 skill 是评审 gate，输出 verdict + findings；tasks 是拆实现步骤。两条 review 均未通过前不进 tasks。 |
| `hf-workflow-router` | router 负责阶段路由与激活条件判定；本 skill 假设已处于 UI 设计评审阶段。发现激活条件错、peer 不可协调或需求漂移时才 reroute。 |
| `hf-spec-review` | spec-review 评审需求规格（做什么，含 UI surface 是否该存在）；本 skill 评审 UI 设计（界面如何承载）。 |

## Red Flags

- 因"实现时再说"就直接通过
- 把 UI 评审变成组件源码建议
- 接受只是复述规格、没有 UI 决策的文档
- 忽略缺失的 loading / empty / error 态
- 接受"支持键盘"、"对比度达标"这类无证声明
- 接受硬编码色值/字号/间距，以"实现时会走 token"为由放行
- 忽略无法追溯到已批准规格的新增 UI surface
- UI 设计评审刚"通过"就单独进入 `设计真人确认`（未等 `hf-design-review` 汇合）
- 文档长度长就认为 UI 设计充分
- 跨权评审 `hf-design` 的架构/API 决策（应只 flag peer 不一致，不代位评审）
- 顺手把任务也列出来"更完整"（reviewer 是 gate，不是拆任务）

## Verification

完成条件：

- [ ] 评审记录已落盘
- [ ] 给出明确结论、发现项、薄弱点和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] 结构化返回已使用 `next_action_or_recommended_skill`
- [ ] 若结论为 `通过`，已明确要求进入 `设计真人确认`（等待联合 approval）
- [ ] 若发现 peer 交接块与 `hf-design` 不一致，已 flag 具体冲突点
- [ ] 若由 reviewer subagent 执行，已完成对父会话的结构化结果回传

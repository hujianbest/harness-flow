---
name: hf-design-review
description: 适用于设计草稿已完成需要正式 review verdict、或被指定为 reviewer subagent 执行设计评审的场景。不适用于需继续写或修设计（→ hf-design）、需拆任务或编码（→ hf-tasks）、阶段不清或证据冲突（→ hf-workflow-router）。
---

# HF 设计评审

评审设计文档，判断它是否可以提交给 approval step。核心职责是防止过早拆解任务——确保设计真正锚定规格、决策站得住、接口边界清楚到足以进入任务规划。

**职责边界**：本 skill 只评审 **架构 / 模块 / API 契约 / 数据模型 / 后端 NFR**。若规格声明 UI surface 且 `hf-ui-design` 被激活，`hf-ui-review` 会作为 **design stage 的并行 review peer** 独立评审 IA / 交互 / 视觉 / 前端 a11y 等 UI 维度。**两条 review 均通过后，父会话才发起联合 `设计真人确认`**；任一未过，对应起草 skill 回修，另一条可继续其稳定部分。不得跨权评审 `hf-ui-design` 的职责范围；发现 peer 交接块不一致时，只在 findings 中标注，不代位评审。

## Methodology

本 skill 融合以下已验证方法：

- **ATAM (Architecture Tradeoff Analysis Method, SEI)**: 评审关注质量属性驱动的设计决策，检查设计是否满足关键非功能需求并识别权衡点。
- **Structured Walkthrough (Fagan Inspection, adapted)**: 按 rubric 维度评分，量化判断设计质量，防止自由形式评审的随意性。
- **Separation of Author/Reviewer Roles**: 设计者和评审者必须独立，避免确认偏差。
- **Traceability to Spec**: 所有设计决策必须可追溯到已批准规格中的具体需求，防止设计漂移。

## When to Use

使用：

- `hf-design` 已完成设计草稿，需要正式 review verdict
- 用户明确要求"review 这份 design"
- reviewer subagent 被父会话派发来执行设计评审

不使用：

- 需要继续写或修设计 → `hf-design`
- 需要任务拆解或编码 → 相应下游节点
- 阶段不清或证据冲突 → `hf-workflow-router`

直接调用信号："review 这份设计"、"设计评审"、"帮我看一下这个设计"。

前提条件：存在当前设计草稿、已批准规格、项目相关约定（若项目已声明）。缺设计草稿 → `hf-design`；缺已批准规格或阶段不清 → `hf-workflow-router`。

## Chain Contract

读取：已批准规格（默认 `features/<active>/spec.md`）、被评审设计文档（默认 `features/<active>/design.md`）、项目级评审约定（若项目已声明）、feature `progress.md`（默认 `features/<active>/progress.md`）当前状态、最少必要技术上下文。

产出：review 记录正文 + 结构化 reviewer 返回摘要。

评审记录落盘由 reviewer 负责；approval step 和主链推进由父会话负责。

## Hard Gates

- 设计未通过评审并完成 approval step 前，不得进入 `hf-tasks`
- 输入工件不足以判定 stage/route 时，不直接开始评审
- reviewer 不代替父会话完成 approval step，不提前拆任务或写代码

## Iron Laws

1. **总是在实现前评审设计** — 实现后发现架构问题的修复成本是设计阶段的 10-100 倍
2. **不得放过未记录的单点故障** — 每个 SPOF 必须被识别并有缓解计划
3. **NFR 评估不可跳过** — 性能、安全、可扩展、可维护不是可选项，功能正确但 NFR 不达标 = 设计不完整
4. **权衡必须显式文档化** — 隐藏的 trade-off 是未来的意外和未认领的技术债

## Workflow

### 1. 建立证据基线

读取并固定证据来源：已批准规格（默认 `features/<active>/spec.md`）、当前设计文档（默认 `features/<active>/design.md`）、项目约定、feature `progress.md`（默认 `features/<active>/progress.md`）状态、必要技术上下文。

不要只根据会话记忆或零散聊天内容判断"已批准"或"设计已经讲清楚"。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定可定位的设计草稿、已批准规格是否可回读、route/stage/profile 与 approval evidence 是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定设计草稿 → 写最小 blocked record，下一步 `hf-design`
- precheck 通过 → 继续正式审查

### 2. 多维评分与挑战式审查

对 6 个维度做内部评分（`0-10`）：需求覆盖与追溯、架构一致性、决策质量、约束与 NFR 适配、接口与任务规划准备度、测试准备度与隐藏假设。

评分辅助区分：轻微缺口 vs 需修改 vs 阻塞。按 `references/review-checklist.md` 逐项审查。

每条 finding 必须带：
- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `D3`、`D5`、`A2`）

默认分类：
- `USER-INPUT`：缺失外部阈值、未确认业务裁决、规格未批准却引入关键新增能力、核心 trade-off 仍需真人拍板
- `LLM-FIXABLE`：缺少方案对比、接口边界说明不足、任务规划准备度表达不清、测试策略未显式写出、隐藏假设未整理成文

### 3. 形成结论、severity 与下一步

判定规则（详见 `references/review-record-template.md`）：

- **通过**：可追溯规格、决策清晰、约束 NFR 被吸收、无阻塞任务规划的设计空洞
- **需修改**：核心可用，局部缺口可通过一轮定向修订补齐
- **阻塞**：无法支撑需求规格、存在无法追溯的关键新增内容、或证据链冲突

severity：`critical`（阻塞任务规划）> `important`（应修复）> `minor`（建议改进）。

### 4. 写 review 记录并回传

按 `references/review-record-template.md` 写评审记录，并返回结构化 JSON 给父会话。

下一步映射：
- `通过` → `设计真人确认`（`needs_human_confirmation=true`）
- `需修改` → `hf-design`
- `阻塞`（设计内容） → `hf-design`
- `阻塞`（需求漂移/规格冲突） → `hf-workflow-router`（`reroute_via_router=true`）

## Reference Guide

按需加载详细参考内容：

| 主题 | Reference | 加载时机 |
|------|-----------|---------|
| 评审检查清单 | `references/review-checklist.md` | 执行 Step 2 多维审查时 |
| 评审记录模板 | `references/review-record-template.md` | 执行 Step 4 写评审记录时 |

## 和其他 Skill 的区别

| 易混淆 skill | 区别 |
|-------------|------|
| `hf-design` | design 负责起草设计；本 skill 负责评审设计。起草者不能自审。 |
| `hf-ui-review` | 本 skill 评审架构/模块/API/数据模型/后端 NFR；`hf-ui-review` 评审 IA/交互/视觉/前端 a11y。两者 peer 并行，不得跨权。联合通过后才进入 `设计真人确认`。 |
| `hf-tasks` | 本 skill 是评审 gate，输出 verdict + findings；tasks 是拆解实现步骤。评审未通过前不进 tasks。 |
| `hf-workflow-router` | router 负责阶段路由判断（含 UI surface 激活条件）；本 skill 假设已处于设计评审阶段。发现需求漂移/证据冲突/激活条件判定错时才 reroute 到 router。 |
| `hf-spec-review` | spec-review 评审需求规格（做什么）；本 skill 评审实现设计（如何做）。 |

## Red Flags

- 因"实现时再说"就直接通过
- 把设计评审变成底层编码建议
- 接受只是复述需求、没有设计决策的文档
- 忽略缺失的接口或模块边界
- 忽略无法追溯到已批准规格的新增设计内容
- 设计评审刚"通过"就直接进入 `hf-tasks`（跳过 approval step）
- 文档长度长就认为设计充分
- 顺手把任务也列出来"更完整"（reviewer 是 gate，不是拆任务）

## Verification

完成条件：

- [ ] 评审记录已落盘
- [ ] 给出明确结论、发现项、薄弱点和唯一下一步
- [ ] findings 已标明 severity / classification / rule_id
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] 结构化返回已使用 `next_action_or_recommended_skill`
- [ ] 若结论为 `通过`，已明确要求进入 `设计真人确认`
- [ ] 若由 reviewer subagent 执行，已完成对父会话的结构化结果回传

---
name: hf-spec-review
description: 适用于规格草稿已完成需正式 review verdict、reviewer subagent 被派发执行规格评审的场景。不适用于缺规格草稿或只需继续写（→ hf-specify）、阶段不清或证据冲突（→ hf-workflow-router）、已有已批准规格需设计评审（→ hf-design-review）。
---

# HF 需求评审

评审需求规格，判断范围清晰度、需求可测性、验收标准、success criteria、assumptions 与开放问题闭合度，以及进入 approval step 的准备度。本 skill 是需求规格冻结门禁，目标是把规格准备到可交给 approval step 作为 `hf-design` 候选已批准输入的状态。不替代 `hf-specify`（写规格）或 `hf-design`（做设计）。

## Methodology

本 skill 融合以下已验证方法：

- **Structured Walkthrough (Fagan Inspection, adapted)**: 评审遵循预定义 rubric 维度，按 0-10 评分量化判断，而非自由形式阅读反馈。
- **Checklist-Based Review (NASA/SEI)**: 使用结构化检查清单覆盖关键质量维度，防止评审者凭印象遗漏系统性问题。
- **Separation of Author/Reviewer Roles**: author 和 reviewer 必须由不同会话承担，避免自我确认偏差。
- **Evidence-Based Verdict**: 所有 findings 必须锚定到规格具体位置，不接受无证据的"感觉不好"。

## When to Use

适用：
- `hf-specify` 已完成规格草稿，需正式 review verdict
- 用户明确要求"review 这份 spec"
- reviewer subagent 被派发来执行规格评审

不适用：缺规格草稿或只需继续写 → `hf-specify`；阶段不清/证据冲突 → `hf-workflow-router`；已有已批准规格、当前需要设计评审 → `hf-design-review`。

前提确认：存在稳定规格草稿（默认 `features/<active>/spec.md`）、能读取 项目约定和 feature `progress.md`（默认 `features/<active>/progress.md`）、请求确实是评审。若 route/stage/profile/证据冲突 → 优先回 router。

## Hard Gates

- 规格通过评审并完成 approval step 前，不得进入 `hf-design`
- reviewer 不代替父会话完成 approval step，不顺手开始设计
- reviewer 不得为让规格"看起来能过"而发明业务事实、优先级或来源锚点

## Workflow

### 1. 建立证据基线

读取并固定：当前规格（默认 `features/<active>/spec.md`）、deferred backlog（若存在，默认 `features/<active>/spec-deferred.md`）、项目约定、feature `progress.md`（默认 `features/<active>/progress.md`）、少量上下文用于确认状态和锚点。不只根据聊天记忆判断。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定可定位的规格草稿、route/stage/profile 是否已明确、上游证据是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定规格 → 写最小 blocked record，下一步 `hf-specify`
- precheck 通过 → 继续正式 rubric

### 2. 确定当前规格的结构契约

先判断项目是否通过 项目声明了骨架/字段/优先级体系，当前规格是否遵循。只要语义可回读，不强迫文档长得和默认模板一模一样。

### 3. 用 rubric 做正式审查

详细规则：`references/spec-review-rubric.md`

#### 3.1 Group Q: Quality Attributes
核心需求可回指来源？模糊词已量化？验收标准可判断？需求无冲突/重复？无缺失 Priority/Source？

#### 3.2 Group A: Anti-Patterns
模糊词、复合需求、设计泄漏、无主体被动表达、关键需求中待确认/占位值、缺少负路径/边界/权限差异。

#### 3.3 Group C: Completeness And Contract
核心 FR/NFR 具备 ID/Statement/Acceptance/Priority/Source？当前轮目标与 success criteria 是否具体可判断？范围内外闭合？阻塞性开放问题为空？assumptions 是否显式且失效影响可回读？deferred requirements 已显式处理？

#### 3.4 Group G: Granularity And Scope-Fit
命中 GS1-GS6 的 oversized requirements？当前轮和后续增量混写？findings 足够具体可支持定向回修？

#### 3.5 Finding 分类

每条 finding 带 `severity`（critical/important/minor）、`classification`（USER-INPUT/LLM-FIXABLE）、`rule_id`（如 Q2、A3、C1、GS1）。

分类：缺业务事实/外部决策/性能阈值/优先级冲突 → `USER-INPUT`；缺 wording/拆分/章节/重复整理/设计泄漏改写 → `LLM-FIXABLE`。无法在不新增事实前提下修复的不能标 `LLM-FIXABLE`。

### 4. 形成 verdict 与下一步

severity：`critical`（阻塞设计）→ `important`（应批准前修复）→ `minor`（建议改进）。

| 条件 | verdict | 下一步 |
|------|---------|--------|
| 范围清晰、核心需求可验收、无阻塞 USER-INPUT、足以成为设计稳定输入 | `通过` | `规格真人确认` |
| 有用但不完整，findings 可 1-2 轮定向修订 | `需修改` | `hf-specify` |
| 过于模糊/核心范围未定/findings 无法定向回修 | `阻塞`(内容) | `hf-specify` |
| route/stage/证据冲突 | `阻塞`(workflow) | `hf-workflow-router` |

### 5. 写 review 记录

按 `references/review-record-template.md` 的结构写记录并回传父会话。

交互约束：
- 父会话先展示 1-2 句 plain-language 结论，再只提 USER-INPUT 问题
- LLM-FIXABLE 问题不转嫁给用户
- USER-INPUT 为 0 时不抛额外问卷
- 不整段粘贴 rubric/JSON/全量 findings 给用户
- `reroute_via_router=true` 时只说明 workflow blocker

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-specify` | 写/改规格草稿；本 skill 只做评审不改规格 |
| `hf-design-review` | 评审设计文档；本 skill 评审需求规格，不涉及设计 |
| `hf-workflow-router` | 编排/路由/阶段判断；本 skill 只做规格评审 verdict |

## Red Flags

- 把评审变成重新设计
- 因为"后面再想"就直接批准
- 忽略缺失的验收标准/Priority/Source
- findings 没有 USER-INPUT/LLM-FIXABLE 分类
- interactive 模式下把完整 rubric 原样贴给用户
- 把 LLM-FIXABLE 问题抛给用户
- 通过后直接进入 `hf-design`（跳过 approval step）
- 项目模板不同就机械判定结构不合格

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/spec-review-rubric.md` | 正式审查 rubric（Q/A/C/G 四组） |
| `references/review-record-template.md` | 记录结构、JSON 格式、返回规则、状态同步 |

## Verification

- [ ] 评审记录已落盘
- [ ] 给出明确结论、发现项、薄弱项和唯一下一步
- [ ] 正式 rubric findings 标明 severity/classification/rule_id
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] USER-INPUT findings 支持父会话向用户发起最小定向问题
- [ ] 已显式检查 success criteria、assumptions 与阻塞性开放问题闭合度
- [ ] `通过` 时已明确要求进入 `规格真人确认`
- [ ] 结构化摘要已回传父会话

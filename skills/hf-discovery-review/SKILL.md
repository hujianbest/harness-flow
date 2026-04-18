---
name: hf-discovery-review
description: 适用于 discovery 草稿已完成需要正式 review verdict、或被指定为 reviewer subagent 执行 discovery 评审的场景。不适用于需继续写 discovery 正文（→ hf-product-discovery）、已明确进入 formal spec（→ hf-specify）、或阶段不清 / 证据冲突（→ hf-workflow-router）。
---

# HF 产品发现评审

评审 discovery 草稿，判断问题定义、用户聚焦、wedge 收敛、假设显式化和 bridge-to-spec 准备度是否足够稳定，能够作为 `hf-specify` 的上游输入。本 skill 是 discovery 冻结门禁，不替代 `hf-product-discovery`（起草 discovery）或 `hf-specify`（写正式规格）。

## Methodology

本 skill 融合以下已验证方法：

- **Structured Walkthrough**: 通过固定 rubric 评审问题定义、假设和 bridge 质量，而不是自由发挥式评论。
- **Checklist-Based Review**: 用结构化检查清单覆盖 discovery 的关键维度，防止 reviewer 只看“想法是否有趣”。
- **Separation of Author/Reviewer Roles**: discovery author 与 reviewer 必须分离，避免“自己写自己过”。
- **Evidence-Based Verdict**: 结论必须锚定到 discovery 文档中的具体缺口，不接受泛泛的“还不够清楚”。

## When to Use

适用：
- `hf-product-discovery` 已完成 discovery 草稿，需正式 review verdict
- 用户明确要求“review 这份 discovery / insight 草稿”
- reviewer subagent 被派发执行 discovery 评审

不适用：
- 需要继续写或修 discovery 正文 → `hf-product-discovery`
- 已明确进入 formal spec 起草 → `hf-specify`
- 阶段不清或证据冲突 → `hf-workflow-router`

前提确认：存在稳定 discovery 草稿，能读取 `AGENTS.md` 约定和少量上游输入，请求确实是评审。若 route/stage/profile/证据冲突 → 优先回 router。

## Hard Gates

- discovery 通过评审前，不得把其结论直接当作正式规格输入
- reviewer 不代替父会话继续写 discovery 正文，不顺手开始 spec
- reviewer 不得为让 discovery “更像完成了”而发明用户、问题或价值判断事实

## Workflow

### 1. 建立证据基线

读取并固定：当前 discovery 草稿、`AGENTS.md` 约定、必要的 notes / insight 输入、`task-progress.md`（若存在）。不只依据聊天记忆判断“这个方向已经清楚”。

### 1.5 Precheck：能否合法进入 review

检查：是否存在稳定可定位的 discovery 草稿、请求是否真的是 review、route/stage/证据是否一致。

- route/stage/证据冲突 → 写最小 blocked precheck record，`reroute_via_router=true`
- route 明确但缺稳定 discovery 草稿 → 写最小 blocked record，下一步 `hf-product-discovery`
- precheck 通过 → 继续正式 rubric

### 2. 用 rubric 做正式审查

详细规则：`references/review-checklist.md`

默认审查以下维度：
- 问题与用户聚焦度
- why-now 与 wedge 收敛度
- facts / assumptions / later ideas 的分离程度
- probe / 验证方向是否合理
- bridge-to-spec 准备度

每条 finding 必须带：
- `severity`（`critical` / `important` / `minor`）
- `classification`（`USER-INPUT` / `LLM-FIXABLE`）
- `rule_id`（如 `P1`、`W2`、`B1`）

分类：缺外部事实、用户价值判断、关键业务裁决 → `USER-INPUT`；缺结构、假设显式化、bridge 语义、later idea 整理 → `LLM-FIXABLE`。

### 3. 形成 verdict 与下一步

| 条件 | verdict | 下一步 |
|------|---------|--------|
| 问题清楚、wedge 收敛、假设显式、bridge 足以进入 formal spec | `通过` | `hf-specify` |
| discovery 有价值但仍需一轮定向回修 | `需修改` | `hf-product-discovery` |
| discovery 过于模糊、核心问题/用户/bridge 未定 | `阻塞`(内容) | `hf-product-discovery` |
| route/stage/证据冲突 | `阻塞`(workflow) | `hf-workflow-router` |

### 4. 写 review 记录

按 `references/review-record-template.md` 写记录并回传父会话。

交互约束：
- 父会话先展示 1-2 句 plain-language 结论，再只提 USER-INPUT 问题
- LLM-FIXABLE 问题不转嫁给用户
- `通过` 时只表示 discovery 已足够进入 `hf-specify`，不代表 formal spec 已完成

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-product-discovery` | 写 / 改 discovery 草稿；本 skill 只做评审不改正文 |
| `hf-specify` | `hf-specify` 起草正式规格；本 skill 只判断 discovery 是否足够成为其上游输入 |
| `hf-workflow-router` | router 负责编排和阶段判断；本 skill 只做 discovery review verdict |

## Red Flags

- 把 discovery 评审变成补写 spec
- 因“方向看起来不错”就直接通过，没有 bridge 语义
- 忽略 facts / assumptions / later ideas 混写问题
- findings 没有 USER-INPUT / LLM-FIXABLE 分类
- `通过` 后直接声称“可以实现”而不是进入 `hf-specify`
- interactive 模式下把全量 rubric 原样贴给用户

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/review-checklist.md` | discovery 正式审查 rubric |
| `references/review-record-template.md` | 记录结构、JSON 返回和下一步映射 |

## Verification

- [ ] 评审记录已落盘
- [ ] 给出明确结论、发现项和唯一下一步
- [ ] findings 标明 severity / classification / rule_id
- [ ] precheck blocked 时已写明 workflow blocker 和 reroute_via_router
- [ ] USER-INPUT findings 支持父会话发起最小定向问题
- [ ] `通过` 时已唯一指向 `hf-specify`
- [ ] 结构化摘要已回传父会话

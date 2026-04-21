---
name: hf-product-discovery
description: 适用于仍在判断产品问题、目标用户、wedge、关键假设或 probe 方向，尚未收敛到 formal spec 的场景。不适用于已明确进入 spec/design/tasks（→ hf-specify / hf-workflow-router）、或只需评审已有 discovery 草稿（→ hf-discovery-review）。
---

# HF 产品发现

把模糊的产品想法收敛成一份可评审的 discovery 草稿，明确问题、用户、wedge、关键假设与进入 formal spec 前仍需验证的事项。本 skill 不写正式规格，不替代 `hf-specify`。

## Methodology

本 skill 融合以下已验证方法：

- **Problem Framing**: 先定义用户、问题、阻塞进展与 why-now，而不是从功能清单反推问题。
- **Hypothesis-Driven Discovery**: 把“我们觉得应该这样做”拆成可验证假设、风险和 probe 方向，避免把猜测直接写成已确认需求。
- **Opportunity / Wedge Mapping**: 在多个候选方向之间收敛当前轮最小 wedge，明确哪些能力进入当前轮、哪些只是后续候选。
- **Assumption Surfacing**: 显式写出已确认事实、未确认假设和 open questions，为后续 `hf-specify` 提供稳定 bridge，而不是让 coding family 从零反推 thesis。

## When to Use

适用：
- 用户还在问“这个问题值不值得做”“为什么当前方向不够好”
- 用户还在收敛 target user、problem statement、wedge 或最小机会点
- 用户还在讨论关键假设、probe、验证方向，尚未进入 formal spec
- 现有输入主要是 brainstorming notes、会议纪要或零散想法，且目标是形成可进入规格阶段的 discovery 草稿

不适用：
- 已明确要写 formal spec / design / tasks → `hf-specify` / 对应下游 skill
- 只需评审已有 discovery 草稿 → `hf-discovery-review`
- route / stage / 证据冲突，需要 authoritative 判断 → `hf-workflow-router`

Direct invoke 信号：“先帮我把产品方向想清楚”“先收敛问题和 wedge”“还没到写 spec，先做 discovery”。

## Hard Gates

- discovery 草稿未通过评审前，不得把它当作正式规格输入
- 不得把猜测、口号或实现偏好伪装成已确认业务需求
- 不得顺手进入 formal spec、设计或任务拆解
- 若请求已明显进入 coding family，不继续停留在本节点

## Workflow

### 1. 读取最少必要上游输入

只读完成 discovery 所需的最少材料：用户请求、已有会议纪要 / notes / insight docs、`AGENTS.md` 中的项目上下文约定（若存在）、以及少量仓库背景用于理解当前主题。

先归纳：
- 当前想解决的核心问题
- 涉及的用户 / 角色
- 已确认事实
- 待确认假设
- 候选 wedge / opportunity
- 明显越界到 spec / design 的内容

### 2. 收敛当前轮 discovery 目标

若输入同时混有多个方向，先明确这一轮只回答：
- 当前要收敛哪个问题
- 针对哪个用户 / 场景
- 哪个最小 wedge 最值得推进
- 哪些候选能力先放入 parking lot

不要把多个不相关方向揉成一份大而空的 discovery 文档。

### 3. 结构化整理 discovery 输入

把原始输入至少归一化为：
- `Problem / User / Why now`
- `Confirmed facts`
- `Assumptions / risks`
- `Candidate wedges`
- `Probe ideas`
- `Likely out-of-scope / later`

若输入里夹带明显实现细节（接口、数据库表、服务名、技术栈），只保留其业务意图，不把它写成 discovery 结论。

### 4. 形成 discovery 草稿

按 `references/discovery-template.md`（或 `AGENTS.md` 覆盖模板）起草 discovery 文档。

默认应显式写出：
- 问题陈述与目标用户
- why-now / 当前价值判断
- 当前轮 wedge / 最小机会点
- 已确认事实 vs 仍未确认假设
- 建议 probe 方向或验证优先级
- 哪些内容已经足够进入 formal spec
- 哪些仍只能作为 assumption / open question

### 5. 进入 Bridge to Spec 语义

若 discovery 草稿已经足够稳定，应在文档中单列 `Bridge to Spec` 小节，说明：
- 推荐带入 `hf-specify` 的范围边界
- 可直接转成规格输入的稳定结论
- 需要继续保留为 assumption 的内容
- 当前不进入 spec 的候选项

`Bridge to Spec` 是 discovery 输出的一部分，不要求先拆成独立文件。

### 6. 评审前自检与 handoff

交给 `hf-discovery-review` 前确认：
- discovery 不是功能清单堆砌
- 已区分事实 / 假设 / later ideas
- 已明确当前轮 wedge
- 未把 spec / design 细节提前写进正文
- 已明确 `Bridge to Spec` 中哪些结论可进入 `hf-specify`

## Output Contract

完成时产出：
- discovery 草稿（默认路径：`docs/insights/YYYY-MM-DD-<topic>-discovery.md`；若 `AGENTS.md` 覆盖，优先遵循）
  - discovery 阶段 feature 尚未创建，因此 discovery 草稿落到 `docs/insights/` 长期资产目录；只有当 discovery 通过评审并决定推进为 feature 时，才由 `hf-specify` 创建 `features/<NNN>-<slug>/`
- 文档中明确的 spec bridge 小节，作为后续 `hf-specify` 起草 `features/<NNN>-<slug>/spec.md` 的输入
- discovery 阶段的进度可临时记录在 discovery 草稿中或与 discovery 同目录的 progress 文件；进入 feature 后，进度统一迁到 `features/<NNN>-<slug>/progress.md`

若草稿未达评审门槛，不伪造 handoff；明确还缺什么。

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `using-hf-workflow` | 入口层只负责判断是否该进入 discovery；本 skill 负责真正起草 discovery 正文。 |
| `hf-discovery-review` | review 负责独立评审 discovery 草稿；本 skill 只负责起草和回修。 |
| `hf-specify` | discovery 回答“为什么值得做、当前 wedge 是什么、哪些假设仍未关闭”；specify 回答“这一轮正式做什么、做到什么程度算完成”。 |
| `hf-workflow-router` | router 负责 authoritative runtime routing；本 skill 假设当前已明确在做 discovery authoring。 |

## Red Flags

- 把 brainstorming notes 直接当成已稳定结论
- 用功能列表代替问题定义和 wedge 收敛
- discovery 文档混入接口、表结构、服务名等设计细节
- 没区分 confirmed facts 和 assumptions
- 没说明哪些结论足够进入 spec，handoff 仍写“可以继续”
- 还在判断产品是否值得做，却直接起 formal spec

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/discovery-template.md` | 默认 discovery 文档骨架与保存路径 |

## Verification

- [ ] discovery 草稿已保存到约定路径
- [ ] 问题、用户、why-now、当前 wedge 已写清
- [ ] confirmed facts、assumptions、later ideas 已显式分开
- [ ] bridge 语义已明确，足以支撑 `hf-specify` 读取
- [ ] discovery 正文未混入 formal spec / design 细节
- [ ] discovery 阶段进度记录（若使用）已同步到 `hf-discovery-review`；进入 feature 后续 progress 落到 `features/<NNN>-<slug>/progress.md`

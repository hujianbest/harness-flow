---
name: hf-tasks
description: 适用于规格与设计都已批准、需要在编码前产出可评审任务计划的场景。不适用于规格/设计未稳定（→ hf-specify / hf-design）、任务计划已批准需进入实现（→ hf-test-driven-dev）、或阶段不清（→ hf-workflow-router）。
---

# HF 任务拆解

创建任务计划，把已批准设计转化为可执行、可追溯、可验证的工作单元，准备到可交给 `hf-tasks-review` 的状态。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **WBS (Work Breakdown Structure)** | 自顶向下将设计拆解为可管理的任务层级，每个任务有明确范围、不重叠、可分配 | PMBOK, PMI | 步骤 3 — 定义里程碑；步骤 4 — 拆解任务单元 |
| **INVEST Criteria** | 任务粒度检查遵循 Independent/Negotiable/Valuable/Estimable/Small/Testable 六维度 | Bill Wake, 2003；敏捷用户故事实践 | 步骤 4 — 拆解粒度；步骤 7 — 自检 |
| **Dependency Graph + Critical Path** | 显式建模任务间依赖关系，识别关键路径，确保执行顺序可验证 | 项目化实践（项目计划通用方法） | 步骤 5 — 依赖与活跃任务规则 |
| **Definition of Done (Scrum)** | 每个任务具备可判断的完成条件 | Scrum Guide, Schwaber & Sutherland | 步骤 4 — 完成条件；步骤 7 — 自检 |

## When to Use

适用：
- 规格与设计都已批准，需要任务计划
- `hf-tasks-review` 返回 `需修改` 或 `阻塞`，需按 findings 修订
- 需要为 `hf-test-driven-dev` 准备任务输入和测试设计种子

不适用 → 改用：
- 规格未稳定/未批准 → `hf-specify` / `hf-spec-review`
- 设计未稳定/未批准 → `hf-design` / `hf-design-review`
- 任务计划已批准，需进入实现 → `hf-test-driven-dev`
- 阶段不清/证据冲突 → `hf-workflow-router`

Direct invoke 信号："把设计拆成任务"、"先别写代码，先梳理任务顺序"、"tasks plan 被 review 打回了"。

## Hard Gates

- 任务计划通过评审并写入批准结论前，不得开始实现
- `hf-tasks-review` 给出"通过"前，不进入 `hf-test-driven-dev`
- 若请求未经过入口判断，先回到 `hf-workflow-router`

## Workflow

### 1. 阅读已批准输入并提取拆解信号

阅读：已批准规格、已批准设计、项目上下文、`AGENTS.md` 路径映射、`task-progress.md`。

**若 UI surface 被激活**（存在 `hf-ui-design` 的已批准文档）：除技术设计外，也需读取 UI 设计文档，提取组件粒度、关键页面 wireframe、交互状态矩阵、Design Token 映射；前端任务拆解必须承接 Atomic 分层与状态矩阵，避免把"实现某页面"当作单任务。

至少提取：主要工作流、依赖与顺序、测试影响、风险区域、关键需求/设计锚点（含 UI 设计锚点，若存在）。

若因 review findings 重新进入：先读 findings，优先修复粒度过大、缺少完成条件、依赖遗漏等问题，不重做未受影响的任务。

### 2. 文件/工件影响图

列任务前，先明确本轮涉及哪些工件：会创建/修改哪些文件、配置、文档、状态工件、测试/验证入口。锁定任务边界，避免"实现某模块"式脱离工件现实的任务。

### 3. 定义里程碑与追溯

分组为能产生阶段性成果的里程碑。每个里程碑含：目标、包含的任务、退出标准、对应的需求/设计依据。对关键需求和设计决策建立显式追溯。

### 4. 拆解为可执行任务单元

任务必须小到能被单任务推进和验证。

优先使用：为单一行为/接口补齐可验证闭环、为高风险路径补齐实现与验证、为依赖切换/数据迁移/状态更新完成收口。

避免：实现某模块、完成功能、后面再优化。

对每个关键任务，至少明确：

- 任务 ID、目标、Acceptance、前置依赖
- Ready When、初始队列状态、Selection Priority
- Files / 触碰工件、Verify、预期证据、完成条件
- 首个活跃任务或高风险任务的测试设计种子（主要行为 + 关键边界 + 适合 fail-first 的点）

### 4A. 任务单元合同与仓库约束投影

不是把设计拆成几个“大任务标题”就结束。对每个会触碰代码、配置、数据或状态工件的关键任务，必须把任务级合同写实：

- `Acceptance` 写任务完成后什么行为/接口/状态必须为真；不要写“实现某模块”“完成某功能”
- `Verify` 优先继承 `AGENTS.md` / 项目约定中的真实命令、顺序与强制验证步骤；不要用泛化默认值覆盖项目规则
- `测试设计种子` 至少覆盖：主行为、1 个关键边界、1 个适合 fail-first 的点
- 代码型任务优先拆成可直接支撑 `hf-test-driven-dev` 的最小闭环：`fail-first test -> 确认失败 -> 最小实现 -> verify green`
- 数据库 / 迁移 / 状态切换类任务，除 `Verify` 外还要写明回滚 / 恢复说明，或显式引用项目中的等价字段
- 如果某任务仍只能写成“后面再细化”“实现审批流模块”这类大块描述，说明粒度还不够，继续拆

若项目规则里只差 1 个关键事实就能写实任务合同，例如：
- 验证命令的强制顺序
- 数据库相关任务是否必须写回滚说明
- 某类工件是否有固定验证入口

处理规则：
- `interactive`：先问 1 个最小判别问题，再继续写计划
- `auto`：明确把缺口写进计划 / handoff，不自行假设默认规则

### 5. 强化依赖与当前活跃任务规则

为每个任务给出：依赖的前置任务/工件、推荐验证命令或入口、预期结果/新鲜证据、ready/pending 判断依据。

至少补一条规则：
- 如何从计划中选定唯一 `Current Active Task`
- 当前任务完成后，router 如何基于依赖、ready 条件与优先级重选下一任务

### 6. 编写任务计划

按 `references/task-plan-template.md` 的默认结构起草。若 `AGENTS.md` 声明了模板覆盖，优先遵循。

任务队列投影和 board 操作详见 `references/task-board-guide.md`。

### 7. 评审前自检

交 `hf-tasks-review` 前确认：
- 不存在大到无法单任务推进的任务
- 关键任务有 Acceptance、Files、Verify、完成条件
- 关键任务能追溯回规格/设计
- 风险区域已体现在顺序或验证中
- 已给出唯一 Current Active Task 选择规则
- router 可稳定重选下一 task
- 测试设计种子足以帮助 `hf-test-driven-dev` 进入测试设计

按 `references/reviewer-handoff.md` 派发独立 reviewer subagent 执行 `hf-tasks-review`。

## Output Contract

完成时产出：
- 可评审任务计划（保存到 `AGENTS.md` 声明的 task-plan 路径；若无项目覆写，使用默认任务计划路径，如 `docs/tasks/YYYY-MM-DD-<topic>-tasks.md`）
- 里程碑、追溯、工件影响图、测试设计种子、任务队列投影
- canonical handoff：`hf-tasks-review`

状态同步：`task-progress.md` `Current Stage` → `hf-tasks`，`Next Action Or Recommended Skill` → `hf-tasks-review`。

若计划未达评审门槛，不伪造 handoff；明确写出缺口。

注意：只有 review 通过且 approval step 完成后，才进入 `hf-test-driven-dev`。

## 和其他 Skill 的区别

| 场景 | 用 hf-tasks | 不用 |
|------|-------------|------|
| 规格与设计已批准，需任务拆解 | ✅ | |
| 规格未稳定/未批准 | | → `hf-specify` / `hf-spec-review` |
| 设计未稳定/未批准 | | → `hf-design` / `hf-design-review` |
| 任务计划已批准，需进入实现 | | → `hf-test-driven-dev` |
| 评审任务计划质量 | | → `hf-tasks-review` |
| 阶段不清/证据冲突 | | → `hf-workflow-router` |

## Red Flags

- 把任务计划写成设计文档副本
- 使用大到无法验证的任务
- 漏掉依赖关系或完成条件
- 写了任务却无法追溯到规格或设计
- 把验证拖到整个功能结束时才做
- handoff 缺失却声称"可以直接进入实现"

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/task-plan-template.md` | 默认计划模板结构与保存路径 |
| `references/task-board-guide.md` | Task Board 示例、队列投影、活跃任务选择规则 |
| `references/reviewer-handoff.md` | reviewer 派发协议与结果处理 |

## Verification

- [ ] 任务计划已保存到约定路径
- [ ] 关键任务的 Acceptance、Files、Verify、完成条件已写清
- [ ] 需求/设计追溯与工件影响图已给出
- [ ] 测试设计种子、Current Active Task 规则、queue projection 已提供
- [ ] `task-progress.md` 已按 canonical schema 同步，下一步为 `hf-tasks-review`

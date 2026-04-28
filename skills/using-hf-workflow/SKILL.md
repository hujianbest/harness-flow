---
name: using-hf-workflow
description: 适用于新会话不确定从哪进入 HF workflow、用户用 /hf-* 命令表达意图、需判断 direct invoke 还是 route-first 的场景。不适用于 runtime 恢复编排（→ hf-workflow-router）、已在 leaf skill 内部（→ 继续当前 skill）。
---

# Using HF Workflow

HF workflow family 的 **public shell**。帮助你决定：

- `direct invoke`：当前节点已明确，直接进入 leaf skill
- `route-first`：阶段/profile/证据不稳定，交给 `hf-workflow-router`

本 skill 是 public entry，不是 runtime handoff。不替代 router 的 authoritative routing。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **Front Controller Pattern** | 作为统一入口点，解析用户意图后分发到对应处理节点 | GoF 设计模式 / Martin Fowler, "Patterns of Enterprise Application Architecture" | 步骤 1 — 判断 entry vs recovery；步骤 7 — 正确结束 |
| **Evidence-Based Dispatch** | 通过读取 feature `progress.md` 与工件状态判断 entry vs recovery | 项目化实践（HF 核心约定） | 步骤 1 — entry vs runtime recovery；步骤 4 — direct invoke 判断 |
| **Separation of Concerns** | 入口层只负责意图识别和分发，不做 authoritative routing 或状态修改 | 项目化实践（分层架构原则） | 步骤 7 — 只输出两类结果 |

## When to Use

适用：
- 新 HF 工作周期，不确定从哪进入
- 用户说"继续""推进""开始做"但当前节点未确认
- 用户用 `/hf-spec`、`/hf-build`、`/hf-review` 等命令意图
- 需判断 direct invoke 还是 route-first
- 用户要求 `auto mode` 但还没确定交给哪个节点

不适用：已在 leaf skill 内部 → 继续当前 skill；需要 authoritative routing → 直接交给 `hf-workflow-router`。

## Boundary With Product Skills

若问题仍在产品 thesis/wedge/probe 层面 → 仍由当前 public entry 统一分流，但目标 leaf 应是 `hf-product-discovery`，而不是再引入第二个 public shell。
若已产出 `docs/insights/*-spec-bridge.md` 且目标是 formal spec/design/tasks → 可进入 coding family。

## Workflow

### 1. 判断 entry vs runtime recovery

entry（用本 skill）：新会话、高层意图、命令 bias、direct vs route 选择。
runtime recovery（交给 router）：review/gate 刚完成、evidence 冲突、需切支线、需消费 gate 结论 → `hf-workflow-router`。

### 2. 识别主意图

归到以下之一：新需求、product discovery、继续推进、review-only、gate-only、当前任务实现、规格相关、hotfix、increment、closeout、Execution Mode 偏好。

### 3. 提取 Execution Mode 偏好

用户说 `auto mode`/`自动执行`/`不用等我确认` → 视为 Execution Mode 偏好，不是新 Profile，不是跳过 approval 的理由，不是 direct invoke 的充分条件。随 handoff 带给下游。

### 4. 判断是否允许 direct invoke

同时满足才可：节点已明确、请求属于该 skill 职责、工件存在可读、无 route/stage/profile 冲突、Execution Mode 偏好已传递。任一不满足 → route-first 交给 router。

### 4A. 单事实分流检查点

如果当前**只差 1 个关键事实**就能稳定判断 `direct invoke` vs `route-first`，先问 1 个最小判别问题，再继续；不要为了这 1 个缺口展开整套 intake，也不要过早假设答案。

适用信号：
- 只差"是否已有已批准 spec / design / tasks plan"
- 只差"这是实现缺陷修复，还是需求/验收/约束变化"
- 只差"当前是在 public entry，还是刚完成 review/gate 的 runtime recovery"

不适用：
- 需要 2 个以上事实才能稳定分流
- 工件状态互相冲突
- 问题已经涉及 profile / branch / review recovery 的 authoritative routing

以上任一命中时，不做入口层小问答，直接 `route-first` 交给 `hf-workflow-router`。

### 5. 应用 entry bias

| 用户意图 | 可优先尝试 | 不明确时回退 |
|---------|----------|-----------|
| 产品发现 / thesis / wedge / probe | `hf-product-discovery` | `hf-workflow-router` |
| 规格澄清/修订 | `hf-specify` | `hf-workflow-router` |
| UI / 前端 / 页面 / 交互 / 视觉 设计（规格已批准含 UI surface） | `hf-ui-design` | `hf-workflow-router` |
| 当前活跃任务实现 | `hf-test-driven-dev` | `hf-workflow-router` |
| review/gate 请求 | 具体 review/gate skill（含 `hf-ui-review`） | `hf-workflow-router` |
| closeout/finalize | `hf-completion-gate` / `hf-finalize` | `hf-workflow-router` |
| 线上问题修复 | `hf-hotfix` | `hf-workflow-router` |
| 范围/验收/约束变化 | `hf-increment` | `hf-workflow-router` |

### 6. 命令当作 bias，不当作 authority

`/hf-*` 命令是高频意图的薄包装，不拥有独立路由权——一律先经过本 skill 解析，再决定 direct invoke 还是交给 router：

| 命令 | 主意图 | 偏向 direct invoke 的节点 | 不确定时回退 |
|---|---|---|---|
| `/hf-spec [topic]` | 规格澄清 / 修订 / 入口 | `hf-specify` | `hf-workflow-router` |
| `/hf-build [task-id]` | 当前活跃任务实现 | `hf-test-driven-dev` | `hf-workflow-router` |
| `/hf-review [spec\|design\|tasks\|test\|code\|trace\|regression\|completion]` | review / gate 请求 | 具体 review / gate 节点 | `hf-workflow-router` |
| `/hf-closeout [task-id]` | 完成判断 + 收尾 | `hf-completion-gate`（gate 未跑）/ `hf-finalize`（gate 已通过） | `hf-workflow-router` |

命令规则：

- **Command is bias, not authority**：命令不替代工件检查、profile 判断或 leaf skill 自身的 hard gates
- **No duplicate machine contract**：命令不重新定义 verdict / handoff / progress schema / review return contract，全部沿用 router 与 leaf skill 既有契约
- **One command, one dominant intent**：命令优先服务一个高频意图，不当万能别名；用户混入 hotfix / increment / review-only / 阶段不清信号时，应回 router
- **Leaf skill gates still apply**：即使 direct invoke，目标 leaf skill 的 standalone contract 与 hard gates 仍然生效

### 7. 正确结束

输出只有两类：1) 明确进入合法 leaf skill；2) 明确交给 `hf-workflow-router`。不在这里展开 transition map、做 review recovery、或把 `using-hf-workflow` 写进 handoff。

如果结论是 `direct invoke`，不要只报出目标 skill 名就停下。要在**同一回复**里进入该 leaf skill 的最小 kickoff：继续执行它的第一步，补最少必要 intake / scope check / preflight，而不是再多等一轮"要不要继续"。

如果结论是 `route-first`，只说明为什么不能 direct invoke，然后立即转交 `hf-workflow-router`。不要提前替 router 做业务分析，也不要混入 leaf skill 的启动内容。

### 8. Clear-case fast path

唯一确定下一步时用 3 行编号格式：
1. `Entry Classification`：`direct invoke` 或 `route-first`
2. `Target Skill`：canonical skill 名
3. `Why`：1-2 条最关键证据

3 行快路径用于**先给路由结论**，不是整轮响应的全部内容。

`direct invoke` 时，3 行之后继续追加目标 leaf skill 的最小 kickoff，规则如下：
- 只做第一步，不展开整个下游 workflow
- 只问最少必要问题；若可用默认假设推进，优先用 assume-and-confirm 压缩提问轮次
- 若目标是 `hf-product-discovery`、`hf-specify`、`hf-hotfix`、`hf-increment` 这类本来就以 intake 开场的 skill，紧接着给出最小问题集或默认假设
- 若目标是已能直接执行的 skill（如已有充分上下文的 review / gate / build），直接进入该 skill 的首个动作说明

`route-first` 时，不回放 entry matrix、不重讲分层历史、不展开不相关的备选；只说明"为什么不能 direct invoke"然后立即转交。

## 和其他 Skill 的区别

| 场景 | 用 using-hf-workflow | 不用 |
|------|----------------------|------|
| 新会话入口、意图识别、direct vs route | ✅ | |
| runtime 恢复编排、profile/mode 判断 | | → `hf-workflow-router` |
| 已在 leaf skill 内部 | | → 继续当前 skill |
| 产品 thesis 层面 | | → `hf-product-discovery` |

### Public entry vs Router vs Direct invoke

| 维度 | Public entry（本 skill） | Router 编排 | Direct invoke |
|---|---|---|---|
| 目标 | 判断该 direct invoke 哪个 leaf 还是交给 router | 决定当前应进入哪个节点 | 完成某个已经明确的节点职责 |
| 最小输入 | 用户请求 + 最少 family entry context + Execution Mode 信号 | 用户请求 + 项目级约定 + 上游工件状态 + 当前 active feature 的 `progress.md` + review/gate/verification/approval 证据 | 当前节点所需最小工件 + 当前请求 + Execution Mode 信号 |
| 是否判断 profile | 否；profile 不清就回 router | 是 | 否；profile 不清就回 router |
| 是否处理 Execution Mode | 只识别并下传 | 是；归一化并约束 `interactive` / `auto` | 只消费已明确的 mode；冲突就回 router |
| 是否决定下一节点 | 只决定"leaf 还是 router" | 是 | 否；只写 canonical handoff，后续编排回到父会话 / router |
| review 如何执行 | 只判断是否进入某 review 节点；进入后由 router/父会话按 review-dispatch 派发 | 由父会话按 review-dispatch protocol 派发 reviewer subagent | 同 router 模式 |
| 输出 | 进入 leaf skill 或交给 `hf-workflow-router` | 当前阶段判断 + profile + 推荐节点，并立即继续或命中暂停点 | 节点本地工件 + 状态更新 + canonical handoff + 必要 review/verification record |

### 典型 direct invoke 示例

- "先把产品方向、问题和 wedge 收敛清楚，不要直接写 spec" → `hf-product-discovery`
- "这条假设没把握，先做个最小 probe 再决定 spec" → `hf-experiment`
- "先把需求梳理清楚，不要做设计" → `hf-specify`
- "帮我 review 这份 spec 草稿"（spec 草稿已存在且这是 review-only 请求）→ `hf-spec-review`
- "按 TDD 实现当前 active task"（任务计划已批准且活跃任务唯一）→ `hf-test-driven-dev`
- "这是线上 bug，先收敛 root cause 和最小修复边界" → `hf-hotfix`
- "这是需求变更，不要改代码，先做影响分析和 re-entry"（变更请求明确且关键工件可读）→ `hf-increment`
- "completion gate 过了，帮我做收尾和 release notes"（gate 记录已落盘）→ `hf-finalize`

### 不算合法 direct invoke 的反模式

- 用户点名 skill 就直接执行，不核对当前阶段
- direct invoke implementation / gate skill，却没读取最小上游工件
- 让 authoring skill 顺手决定完整下游链路
- 让 review skill 顺手开始修文档或做实现
- 让 finalize 在 gate 未通过时提前收尾
- 把 `using-hf-workflow` 写进 `Next Action Or Recommended Skill`
- 在 route / stage / profile 冲突下继续硬做当前 skill

## Red Flags

- 把 `using-hf-workflow` 写成完整状态机
- route 不清时硬做 direct invoke
- 把本 skill 写进 `Next Action Or Recommended Skill`
- 因用户点名就跳过工件检查
- review/gate 完成后仍在做恢复编排
- 复制 router 的 transition map 或 pause-point rules
- 在已有 `hf-product-discovery` 的前提下仍发明第二个 product public shell

## Supporting References

| 文件 | 用途 |
|------|------|
| `hf-workflow-router/SKILL.md` | authoritative runtime routing |
| `hf-workflow-router/references/workflow-shared-conventions.md` | progress schema / verdict 词表 / record_path 语义 / `<kind>` allowlist 等运行时约定 |

**横切行为基线（所有 HF 节点共同遵守，无需外部引用）**：

1. **Think Before Coding**：不假设、不藏混乱；进入 leaf skill 前先把已知 / 未知 / 待澄清显式化
2. **Simplicity First (YAGNI)**：意图识别只解最小问题，不替下游展开 routing / approval / review
3. **Surgical Changes**：本 skill 只输出"明确进入 leaf"或"交给 router"两类动作，不旁路修改工件 / 状态
4. **Goal-Driven Execution**：始终对齐"帮助用户从 idea 到产品高质量落地"，未达成 direct invoke 标准就 route-first，不为速度让步

当前 pack 已提供 `hf-product-discovery` 作为 discovery leaf；本 skill 继续作为唯一 public entry，不再引入第二个 product public shell。

## Verification

- [ ] 已判断 entry vs runtime recovery
- [ ] 已区分 direct invoke vs route-first
- [ ] 只差 1 个判别事实时，已优先使用单事实分流检查点
- [ ] clear case 使用 3 行编号快路径
- [ ] `direct invoke` 时已在同一轮进入 target leaf skill 的最小 kickoff
- [ ] 节点明确 → 进入合法 leaf skill
- [ ] 节点不明确 → 交给 `hf-workflow-router`
- [ ] Execution Mode 偏好已传递给下游
- [ ] 未把本 skill 写入 runtime handoff

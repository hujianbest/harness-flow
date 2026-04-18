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
| **Evidence-Based Dispatch** | 通过读取 task-progress.md 和工件状态判断 entry vs recovery | 项目化实践（HF 核心约定） | 步骤 1 — entry vs runtime recovery；步骤 4 — direct invoke 判断 |
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

`/hf-spec` → 偏向 `hf-specify`；`/hf-build` → 偏向 `hf-test-driven-dev`；`/hf-review` → 偏向 review skill；`/hf-closeout` → 偏向 completion/finalize。命令不替代工件检查和 profile 判断。

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
| `skills/docs/hf-workflow-entrypoints.md` | public entry 与 direct invoke 边界 |
| `skills/docs/hf-command-entrypoints.md` | `/hf-*` 命令解释 |
| `hf-workflow-router/SKILL.md` | authoritative runtime routing |

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

---
name: using-hf-workflow
description: 适用于新会话开始、需要发现当前任务该用哪个 HF skill、判断 direct invoke 还是 route-first 的场景。HF skill family 的发现与调度元入口（meta-skill），统辖所有 hf-* skill 如何被发现与调用。不适用于 runtime 恢复编排（→ hf-workflow-router）、已在 leaf skill 内部（→ 继续当前 skill）。
---

# Using HF Workflow

## Overview

HarnessFlow 是一组**按开发阶段组织**的工程工作流 skill（spec-anchored SDD + gated TDD + 证据驱动路由 + 独立评审 + 正式 closeout）。每个 `hf-*` skill 封装一个资深工程师会遵循的具体流程。

本 skill 是 HF skill family 的**发现与调度元入口（meta-skill）**：帮你为当前任务找到正确的 `hf-*` skill，并决定走哪一类动作：

- `direct invoke`：节点已明确、属于该 skill 职责、工件可读、无 route/stage/profile 冲突 → 直接进入对应 leaf skill 的最小 kickoff
- `route-first`：阶段 / profile / 证据不稳定，或属于 runtime 恢复编排 → 交给 `hf-workflow-router`（authoritative runtime routing）

本 skill 是 public entry，不是 runtime handoff，也不替代 router 的权威路由。下面的 **Skill Discovery** 树与 **Lifecycle Sequence** 是**发现取向（orientation / bias）**，不是 router 的 transition map；任何不确定都回退 router。

## Skill Discovery

任务到来时，识别开发阶段并指向对应 skill。**任一处不确定 / 证据冲突 / review·gate 刚结束 / 需切支线 → 一律回退 `hf-workflow-router`。**

```
任务到来
    │
    ├── 还没想清做什么（问题/用户/wedge/假设）? ─→ hf-product-discovery
    │     ├── discovery 草稿需评审? ───────────→ hf-discovery-review
    │     └── 关键假设高风险需先验证? ─────────→ hf-experiment
    ├── 需写 / 修需求规格? ─────────────────────→ hf-specify
    │     └── 规格草稿需评审? ─────────────────→ hf-spec-review
    ├── 规格已批准，要做设计? ──────────────────→ hf-design
    │     ├── 含 UI / 前端 / 交互 surface? ─────→ hf-ui-design
    │     └── 设计草稿需评审? ─────────────────→ hf-design-review / hf-ui-review
    ├── 设计已批准，要拆任务? ──────────────────→ hf-tasks
    │     └── 任务计划需评审? ─────────────────→ hf-tasks-review
    ├── 提审前想自查 spec/design/tasks 盲点? ───→ hf-gap-analyzer
    ├── 实现当前活跃任务? ──────────────────────→ hf-test-driven-dev
    │     ├── 可整包交给 fresh subagent? ──────→ hf-subagent-driven-dev
    │     ├── auto mode / 连续 build? ─────────→ hf-ultrawork
    │     └── 需前端运行时证据? ───────────────→ hf-browser-testing
    ├── 评审测试质量? ──────────────────────────→ hf-test-review
    ├── 评审代码质量? ──────────────────────────→ hf-code-review
    ├── 评审追溯完整性? ────────────────────────→ hf-traceability-review
    ├── 回归 / 文档同步 / 完成判定? ────────────→ hf-regression-gate → hf-doc-freshness-gate → hf-completion-gate
    ├── 线上紧急缺陷修复? ──────────────────────→ hf-hotfix
    ├── 需求 / 范围 / 验收 / 约束变化? ─────────→ hf-increment
    ├── 任务 / feature 收尾? ───────────────────→ hf-finalize
    ├── 多 feature 汇总切版本 / 打 tag? ────────→ hf-release（direct invoke，不经 router）
    └── 不确定 / 证据冲突 / 恢复编排? ──────────→ hf-workflow-router
```

## Core Operating Behaviors

以下行为在所有 HF 节点恒定生效、不可协商；在本入口层尤其约束"如何分流"。

### 1. 显式化假设（Surface Assumptions）

做任何非平凡判断前，显式列出关键假设："现在纠正我，否则我按这些假设推进"。不要悄悄填补含糊的需求或工件状态。进入 leaf skill 前先把已知 / 未知 / 待澄清显式化（Think Before Coding）。

### 2. 主动管理困惑（Manage Confusion Actively）

遇到不一致 / 冲突需求 / 工件状态互相矛盾：**STOP**，命名具体困惑，给出 tradeoff 或提一个最小判别问题，等解决再继续（对应 Workflow 4A 单事实分流检查点）。证据冲突时不要猜 leaf，直接 `route-first` 交给 router。

### 3. 该反对时反对（Push Back When Warranted）

不做 yes-machine。方案有明确问题时直接指出、量化下行、给替代方案，再接受架构师在充分信息下的决定。sycophancy（"当然可以！"后实现坏主意）本身就是失败模式。

### 4. 强制简单（Enforce Simplicity）

入口层只解最小分流问题，不替下游展开 routing / approval / review。YAGNI：能用 3 行快路径给结论就不要展开整轮 intake。

### 5. 维持范围纪律（Maintain Scope Discipline）

入口层只输出两类动作——"明确进入合法 leaf skill"或"交给 router"。不旁路修改工件 / 状态，不顺手清理无关内容，不把 `using-hf-workflow` 写进 runtime handoff。

### 6. 验证而非假设（Verify, Don't Assume）

路由结论必须基于 **on-disk 工件证据**（spec / design / tasks / progress / verification / reviews），不靠 chat memory；"看起来对"不算数。记忆 ≠ evidence。

## When to Use

适用：
- 新 HF 工作周期，不确定从哪进入
- 用户说"继续""推进""开始做"但当前节点未确认
- 用户用 `/hf-spec`、`/hf-build`、`/hf-review` 等命令意图
- 需判断 direct invoke 还是 route-first
- 用户要求 `auto mode` 但还没确定交给哪个节点

不适用：已在 leaf skill 内部 → 继续当前 skill；需要 authoritative routing / runtime 恢复 → 直接交给 `hf-workflow-router`。

**与产品 / 发布 skill 的边界**：若问题仍在产品 thesis/wedge/probe 层面 → 仍由本 public entry 统一分流，目标 leaf 是 `hf-product-discovery`，不要发明第二个 public shell。`hf-release` 是 release-tier 独立 skill（ADR-004），**不进** coding/discovery 主链，**不进** router transition map；本 entry 在 §5 entry bias 表加它一行，仅用于"用户表达切版本意图时直接 direct invoke"。

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
| 当前活跃任务实现 | `hf-test-driven-dev`；若明确要求 fresh implementer subagent 且 task eligibility 已由工件证明，可 direct invoke `hf-subagent-driven-dev`；若请求含 `auto` / `自动执行` / `不用确认`，优先 `hf-ultrawork` 承接 build session loop | `hf-workflow-router` |
| review/gate 请求 | 具体 review/gate skill（含 `hf-ui-review`） | `hf-workflow-router` |
| closeout/finalize | `hf-completion-gate` / `hf-finalize` | `hf-workflow-router` |
| 线上问题修复 | `hf-hotfix` | `hf-workflow-router` |
| 范围/验收/约束变化 | `hf-increment` | `hf-workflow-router` |
| 切版本 / 出 release / 打 tag / 发版本号 | `hf-release`（**direct invoke**，不 route-first；本 skill 与 router 解耦，ADR-004 D3） | 候选 feature 还没 `workflow-closeout` → `hf-finalize` |
| Execution Mode = auto 且当前不在 review/gate 节点 + 满足 fast lane direct invoke 条件 | `hf-ultrawork`（v0.6 起；direct invoke fast lane skill，**不**绕过 review / gate / approval 工件落盘 / Hard Gates；按 ADR-009 D2） | route/stage/profile 不清 → `hf-workflow-router` |

### 6. 命令当作 bias，不当作 authority

`/hf-*` 命令是高频意图的薄包装，不拥有独立路由权——一律先经过本 skill 解析，再决定 direct invoke 还是交给 router：

| 命令 | 主意图 | 偏向 direct invoke 的节点 | 不确定时回退 |
|---|---|---|---|
| `/hf-spec [topic]` | 规格澄清 / 修订 / 入口 | `hf-specify` | `hf-workflow-router` |
| `/hf-build [task-id]` | 当前活跃任务实现；带 `auto` / `自动执行` 时表示连续 build session | `hf-test-driven-dev`；subagent eligibility 已证明时可为 `hf-subagent-driven-dev`；auto 时 `hf-ultrawork` | `hf-workflow-router` |
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

## Lifecycle Sequence

一个完整 feature 的典型 HF 序列（**并非每个任务都需要每个 skill**；旁支与连续执行见下）：

```
1.  hf-product-discovery     → 收敛产品问题 / 用户 / wedge / 假设
2.  hf-experiment            → 高风险假设最小可验证 probe
3.  hf-specify               → formal spec（需求 + 验收标准）
4.  hf-design / hf-ui-design → 架构 / API 契约 / UI 设计
5.  hf-tasks                 → 拆分可评审的小任务
6.  hf-gap-analyzer          → 提审前自查 spec/design/tasks 盲点
7.  hf-test-driven-dev       → 单任务 TDD 实现（subagent / auto 见 §5）
8.  hf-browser-testing       → 前端运行时证据
9.  hf-spec/design/tasks/test/code/traceability-review → 各级独立 Fagan 评审
10. hf-regression-gate       → 回归验证
11. hf-doc-freshness-gate    → 用户文档同步
12. hf-completion-gate       → 任务完成判定
13. hf-finalize              → closeout pack（+ HTML 报告）
14. hf-release               → 多 feature 汇总切版本（独立，不经 router）
```

- **旁支**：`hf-hotfix`（线上修复）、`hf-increment`（需求/范围/验收/约束变化）。
- **知识沉淀**：`hf-wisdom-notebook`（feature 级跨任务知识本）、`hf-context-mesh`（按目录生成分层上下文）按需介入。
- **连续执行**：`Execution Mode = auto` 下的跨任务连续推进由 `hf-workflow-router` 编排，**不在本入口展开**；本入口只负责把第一步指向正确节点。
- bug fix 可能只需：`hf-hotfix` → `hf-test-driven-dev` → `hf-code-review`。

## Failure Modes to Avoid

看起来像在干活、实际制造问题的隐性错误：

1. 不核对就做出错误假设（工件状态 / 节点 / profile）
2. 卡住时不管理自己的困惑，硬着头皮往前
3. 注意到工件冲突却不显式 surface
4. 非显然分流不摆 tradeoff 就替用户决定
5. 对有明显问题的方案 sycophantic（"当然！"）
6. 过度复杂化——把整套 routing/approval 在入口层展开
7. 修改 / 顺手清理与分流无关的工件或状态
8. 删除 / 改动自己没完全理解的内容
9. 没 spec / 没工件证据就因为"显而易见"直接开干
10. 跳过验证：路由结论不基于 on-disk 工件就下结论
11. route 不清 / 证据冲突时硬做 direct invoke，而不是回退 router
12. review/gate 完成后仍在入口层做恢复编排，或把 `using-hf-workflow` 写进 runtime handoff

## Skill Rules

1. **开工前先查是否有适用 skill。** skill 封装了避免常见错误的流程，不是可选建议。
2. **Skill 是 workflow，不是 suggestion。** 按步骤执行，**不跳 review / gate**；approvals 与 gates 是 first-class 节点。
3. **多个 skill 可串联生效。** 一个 feature 可能依次经过 discovery → spec → design → tasks → build → 各级 review → gate → finalize。
4. **不确定时回退 `hf-workflow-router`。** 任务非平凡且阶段 / 证据不稳定时，不要在入口层硬选 leaf——交给 router 做 evidence-based recovery。
5. **Command is bias, not authority。** `/hf-*` 命令先经本 skill 解析；不替代工件检查与 leaf skill hard gates。
6. **作者 / 评审分离（Fagan）。** 写工件的人不得同时批准它；reviewer 派发与 verdict 归属由对应 review/gate skill 决定。
7. **Direct invoke 后 leaf 的 standalone contract 仍生效。** 入口放行不等于跳过目标 skill 的 preflight / hard gates。

## Quick Reference

| 阶段 | Skill | 一句话 |
|------|-------|--------|
| Route | `hf-workflow-router` | 权威 runtime 路由与恢复编排 |
| Discover | `hf-product-discovery` | 收敛产品问题 / 用户 / wedge / 假设 |
| Discover | `hf-discovery-review` | discovery 草稿独立评审 |
| Discover | `hf-experiment` | 高风险假设最小可验证 probe |
| Define | `hf-specify` | 需求规格 + 验收标准 |
| Define | `hf-spec-review` | 规格草稿独立评审 |
| Design | `hf-design` | 架构与 API 契约设计 |
| Design | `hf-design-review` | 技术设计独立评审 |
| Design | `hf-ui-design` | 前端 / UI / 交互设计 |
| Design | `hf-ui-review` | UI 设计独立评审 |
| Plan | `hf-tasks` | 拆分可评审的小任务 |
| Plan | `hf-tasks-review` | 任务计划独立评审 |
| Plan | `hf-gap-analyzer` | 提审前自查 spec/design/tasks 盲点（非评审节点） |
| Build | `hf-test-driven-dev` | 单任务 TDD 实现（默认实现节点） |
| Build | `hf-subagent-driven-dev` | 整包任务交给 fresh implementer subagent |
| Build | `hf-ultrawork` | auto mode fast lane 连续 build（不绕 gate） |
| Build | `hf-context-mesh` | 按目录生成分层上下文骨架 |
| Verify | `hf-browser-testing` | 前端运行时证据（截图 / console / network） |
| Review | `hf-test-review` | 测试质量评审 |
| Review | `hf-code-review` | 代码质量评审 |
| Review | `hf-traceability-review` | 追溯完整性评审 |
| Gate | `hf-regression-gate` | 回归验证 gate |
| Gate | `hf-doc-freshness-gate` | 用户文档同步 gate |
| Gate | `hf-completion-gate` | 任务完成判定 gate |
| Fix | `hf-hotfix` | 线上缺陷复现 + 最小修复 |
| Change | `hf-increment` | 需求 / 范围 / 验收 / 约束变化 |
| Close | `hf-finalize` | 单 feature / 任务 closeout pack + HTML |
| Release | `hf-release` | 多 feature 汇总切版本（独立，不经 router） |
| Knowledge | `hf-wisdom-notebook` | feature 级跨任务知识本 |

## Red Flags

- 把 `using-hf-workflow` 写成完整状态机 / 复制 router 的 transition map 或 pause-point rules
- route 不清时硬做 direct invoke
- 把本 skill 写进 `Next Action Or Recommended Skill`
- 因用户点名就跳过工件检查
- review/gate 完成后仍在做恢复编排
- 在已有 `hf-product-discovery` 的前提下仍发明第二个 product public shell

## Supporting References

| 文件 | 用途 |
|------|------|
| `hf-workflow-router/SKILL.md` | authoritative runtime routing |
| `hf-workflow-router/references/workflow-shared-conventions.md` | progress schema / verdict 词表 / record_path 语义 / `<kind>` allowlist 等运行时约定 |

当前 pack 已提供 `hf-product-discovery` 作为 discovery leaf；本 skill 继续作为唯一 public entry，不再引入第二个 product public shell。

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "我知道下一步是哪个 leaf skill，直接 invoke。" | Workflow stop rule: 路径不确定 / 证据冲突时必须经 hf-workflow-router；越过 router 会绕开 evidence-based recovery。 |
| "聊天上下文里我已经记得状态了。" | Hard Gates: 状态从 on-disk artifacts 恢复，不依赖 chat memory；记忆 ≠ evidence。 |
| "新会话直接 /build。" | Workflow stop rule: 新会话 family discovery 必须从 using-hf-workflow 开始，再决定 bias。 |
| "用户点名了某个 leaf skill，那就直接进。" | Command is bias, not authority: 点名不解除 review 顺序 / profile / 工件前置；前置未满足 → route-first。 |
| "auto mode 就该跳过确认和评审一路冲。" | Execution Mode 偏好不是跳过 approval / review / gate 的理由；只随 handoff 传递。 |

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

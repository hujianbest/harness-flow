---
name: hf-completion-gate
description: 适用于 regression gate 之后需判断任务完成走向、确认任务可宣告完成、用户要求\"能不能算完成\"的场景。不适用于缺回归记录/实现交接块需补齐（→ hf-regression-gate）、需状态收尾（→ hf-finalize）、阶段不清（→ hf-workflow-router）。
---

# HF 完成门禁

在宣告任务完成前，确认有足够、最新且与当前任务同范围的证据。不是 regression gate（广义回归），也不是 finalize（文档/状态收尾）。判断"当前 task 完成是否成立"，不自动等同于"整个 workflow 已完成"。

## Methodology

本 skill 融合以下已验证方法：

- **Definition of Done (Scrum)**: 任务完成不是主观感受，而是所有验收条件满足、所有证据产生、所有状态同步后的客观判断。
- **Evidence Bundle Pattern**: 完成判断要求完整证据束（reviews + gates + 实现交接块），缺一不可。
- **Profile-Aware Rigor**: full/standard/lightweight 三级对应的证据要求不同，lightweight 不降低质量标准，只是缩小验证范围。

## When to Use

适用：regression gate 之后需判断当前任务完成后的走向；确认任务可宣告完成；准备更新 task-progress 与项目 release notes / changelog；用户要求"能不能算完成"。

不适用：缺 regression 记录/实现交接块 → 补齐；需回归验证 → `hf-regression-gate`；需状态收尾 → `hf-finalize`；阶段不清 → `hf-workflow-router`。

## Hard Gates

- 没有针对最新代码的验证证据就不能宣称完成
- 本轮没运行验证命令就不能诚实宣称完成
- 缺实现交接块或 regression 记录不得返回 `通过`
- worktree-active 时 completion evidence 必须锚定同一 Worktree Path
- 不得把"task 完成"等同于"workflow 可 finalize"

## Workflow

### 1. 明确完成宣告范围

写出准备宣告什么：测试通过、功能行为正常、缺陷已修复、任务已完成。

### 2. 对齐上游结论与 profile 条件

确认：当前 profile 必需的 review/gate 记录齐全 → regression gate 结论允许继续 → 实现交接块/task-progress/完成声明在同一任务范围 → 任务计划足以判断剩余任务。

Profile-aware 上游证据矩阵：

| Profile | 需确认的上游记录 |
|---------|---------------|
| `full` / `standard` | test-review、code-review、traceability-review、regression-gate、实现交接块 |
| `lightweight` | regression-gate、实现交接块；其余写 `N/A（按 profile 跳过）` |

full/standard 记录缺失/过旧 → `阻塞`。

### 2.5 Precheck：能否合法进入 gate

检查：上游 review/gate 记录是否齐全、实现交接块与 regression record 是否针对同一任务、worktree 状态与当前 evidence 是否一致。

- 上游结论缺失或 route/stage/profile/任务范围冲突 → `阻塞`，下一步 `hf-workflow-router`
- worktree-active 但 completion evidence 无法锚定同一 `Worktree Path` → `阻塞`，下一步 `hf-completion-gate`
- precheck 通过 → 继续执行验证

### 3-4. 确定、执行验证命令

选择能直接证明结论的命令，立即运行完整验证。不用更弱证据替代。

### 5. 阅读完整结果

检查退出码、失败数量、输出是否支持结论、结果是否属于当前最新代码。

### 6. 形成 completion evidence bundle

记录：完成范围、命令、退出码、结果摘要、新鲜度锚点、未覆盖什么。

若项目未覆写格式，默认把 evidence bundle 映射到本 skill 模板 `references/verification-record-template.md` 的这些字段：
- `Metadata`：`Verification Type=completion-gate`、Scope、Record Path、Worktree Path / Branch（若适用）
- `Upstream Evidence Consumed`：implementation handoff、review / gate records、task / progress anchors
- `Claim Being Verified`：当前准备宣告的 completion claim
- `Verification Scope`：Included Coverage、Uncovered Areas
- `Commands And Results`：命令、退出码、Summary、Notable Output
- `Freshness Anchor`：为什么这些结果属于当前最新代码状态
- `Conclusion`：`通过` / `需修改` / `阻塞` + 唯一 `Next Action Or Recommended Skill`
- `Scope / Remaining Work Notes`：剩余任务判断、next-ready 候选是否唯一、限制与备注

### 6.1 `hf-doc-freshness-gate` verdict 在 evidence bundle 中的承接（Phase 0 / ADR-0003）

`hf-doc-freshness-gate` 是 router 主链上位于 `hf-regression-gate` 之后、本节点之前的独立 gate（ADR-0003 / `skills/hf-doc-freshness-gate/SKILL.md`）。其 verdict 路径必须作为 completion evidence bundle `Upstream Evidence Consumed` 段的一项被显式 reference。承接规则：

- **`pass` / `partial` / `N/A` verdict**：reference 路径 = `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`，作为 `Upstream Evidence Consumed` 一项，本节点继续按 §6A 完成判定闸门处理；本节点**不**对 doc-freshness verdict 做二次判定，也**不**新增"对外可见文档"维度的 verdict 判别分支
- **`blocked` verdict**：本节点**不**应消费此 verdict——`hf-doc-freshness-gate=blocked` 时由 router 直接路由回 `hf-test-driven-dev`（或 `hf-increment` / `hf-traceability-review` / `hf-workflow-router`，按 doc-freshness gate 自身的 next 表）；本节点不会被进入。如果父会话误把 blocked verdict 强行带入本节点 evidence bundle，本节点应判 `阻塞` + next = `hf-workflow-router` 让 router 重派
- **未通过 doc-freshness gate 的场景**：若 `Upstream Evidence Consumed` 中找不到 doc-freshness verdict 路径（既不是 pass/partial/N/A，又不是 blocked，而是缺失），说明 router 路径异常，本节点判 `阻塞` + next = `hf-workflow-router`

本节既不修改本 SKILL 既有 verdict 词表（仍是 `通过` / `需修改` / `阻塞`），也不修改 §6A 完成判定闸门 5 行场景表；只是在 `Upstream Evidence Consumed` 段新增"必须含 doc-freshness verdict 路径"的承接条款。

### 6A. 完成判定闸门

先把当前场景收敛成**唯一 verdict + 唯一下一步**，再写完成记录。不要把“感觉差不多完成了”写成 `通过`。

| 场景 | conclusion | next_action_or_recommended_skill | 必须写出的最少字段 |
|---|---|---|---|
| 本轮没有 fresh verification evidence，也没运行能直接证明 completion claim 的命令 | `需修改` | `hf-test-driven-dev` | `record_path`、缺失的 fresh evidence、需要重跑的验证命令 |
| 声称“刚跑过且全绿”，但只有口头陈述，或终端 / 输出记录已不可核实 | `阻塞` | `hf-completion-gate` | `record_path`、不可核实原因、需要重新生成的验证输出 |
| review 都过了，但本轮没运行能直接证明 completion claim 的命令 | `需修改` | `hf-test-driven-dev` | `record_path`、缺失的验证命令、为什么 review 不能替代 verification |
| 验证命令有失败项，或结果不能直接支持 completion claim | `需修改` | `hf-test-driven-dev` | `record_path`、失败摘要、未满足的完成条件 |
| 强制验证步骤因环境 / 工具链问题未完成，且 项目约定 / DoD 无降级许可 | `阻塞` | `hf-completion-gate` | `record_path`、阻塞原因、未覆盖区域、恢复后需重跑什么 |
| 当前任务证据充分，但 next-ready task 候选不唯一，或 ready 判定冲突 | `阻塞` | `hf-workflow-router` | `record_path`、候选任务清单、冲突证据、为什么本 skill 不能替 router 选任务 |
| 当前任务证据充分，且仍有唯一 next-ready task | `通过` | `hf-workflow-router` | `record_path`、completion claim、evidence bundle、`Remaining Task Decision=唯一 next-ready task` |
| 当前任务证据充分，且已无剩余 approved tasks | `通过` | `hf-finalize` | `record_path`、completion claim、evidence bundle、`Remaining Task Decision=无剩余任务` |

补充规则：
- 不接受“失败测试与本次改动关系不大”“我刚才本地跑过了但没保留输出”这类不可核实说法
- `interactive`：若只差 1 个任务队列事实就能判断“唯一 next-ready task vs 无剩余任务”，先问 1 个最小判别问题；不要替 router 补脑
- `auto`：若 remaining-task 证据不唯一，直接 `阻塞` 并回 `hf-workflow-router`
- 若输出不能映射到上表中的一行，说明 verdict 还没收敛好，不能返回

### 7. 门禁判断

- 证据支持完成 + 有唯一 next-ready task → `通过`，下一步 `hf-workflow-router`
- 证据支持完成 + 无剩余任务 → `通过`，下一步 `hf-finalize`
- 证据不足/仍需实现 → `需修改`，下一步 `hf-test-driven-dev`
- 环境/工具链问题 → `阻塞`，下一步 `hf-completion-gate`
- 上游编排/profile/证据链问题，或剩余任务不唯一 → `阻塞`，下一步 `hf-workflow-router`

## Output Contract

记录保存到 项目声明的 verification 路径；若无项目覆写，默认使用 `features/<active>/verification/completion-task-NNN.md`。若项目无专用格式，默认使用本 skill 模板 `references/verification-record-template.md`。

最少应包含：
- 已消费的上游结论与证据矩阵
- 完成宣告范围
- 命令、退出码、结果摘要、新鲜度锚点
- `Claim Being Verified` 与它对应的直接验证命令；不能只写 review 结论
- 剩余任务判断与“唯一 next-ready task / 无剩余任务 / 候选不唯一”结论
- worktree 锚点（若适用）
- 唯一门禁结论与唯一下一步

在 feature `progress.md` 写回 canonical Next Action。

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/verification-record-template.md` | completion verification record 模板（与 `hf-regression-gate` 同形态） |

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-regression-gate` | 判断回归面健康度（修好了本地但旁边没坏）；本 skill 判断当前任务可否宣告完成 |
| `hf-finalize` | 关闭工作周期、更新 release notes、产出 handoff pack；本 skill 只做任务完成判断 |
| `hf-workflow-router` | 编排/路由/阶段判断；本 skill 只做完成门禁 |

## Red Flags

- 说"应该算完成了"
- 依赖旧输出
- 把主观感觉当证据
- 认为 review 通过就等于运行成功
- 不读 regression 记录就宣告完成
- worktree-active 但 completion record 没写 Worktree Path

## Verification

- [ ] completion verification record 已落盘
- [ ] 上游证据矩阵、完成范围、剩余任务判断、evidence bundle 已写清
- [ ] precheck blocker 与 worktree 锚点（若适用）已写清
- [ ] 基于最新证据给出唯一门禁结论
- [ ] worktree 状态已写出（若适用）
- [ ] feature `progress.md` 已同步 canonical Next Action

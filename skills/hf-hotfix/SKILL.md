---
name: hf-hotfix
description: 适用于线上/紧急缺陷需要修复、用户要求 hotfix 分析、缺陷需要复现路径和最小修复边界的场景。不适用于写/修代码（→ hf-test-driven-dev）、需求变更/范围调整（→ hf-increment）、阶段不清（→ hf-workflow-router）。
---

# HF Hotfix

在不放弃验证纪律的前提下处理紧急缺陷。本 skill 不写生产代码——负责分析、根因收敛、状态同步，然后 handoff 给 `hf-test-driven-dev`。

## Methodology

本 skill 融合以下已验证方法：

- **Root Cause Analysis (RCA / 5 Whys)**: 从缺陷表象逐层追问到根因，而非只修复表象。确保修复针对根因而非症状。
- **Minimal Safe Fix Boundary**: 显式定义修复边界（改什么/不改什么/影响什么），防止 hotfix 蔓延成大范围重构。
- **Blameless Post-Mortem Mindset**: 关注机制和系统性原因，而非归咎个人。缺陷分析为未来 bug-patterns 积累知识。

## When to Use

适用：
- 线上/紧急缺陷需要修复
- 用户要求 hotfix 分析
- 缺陷需要复现路径和最小修复边界
- 当前能说明为什么现有行为违反既有 spec / 设计 / API 契约，或违反稳定既有行为
- 当前要做的是复现、根因收敛、修复边界和 handoff，而不是直接改生产代码

不适用：
- 写/修代码 → `hf-test-driven-dev`
- 需求变更/范围调整，或现有工件只能证明“想新增能力” → `hf-increment`
- 阶段不清、route / stage / worktree 证据冲突，或既有契约仍不清楚 → `hf-workflow-router`
- 当前已完成 hotfix 分析，只剩实现 → `hf-test-driven-dev`

## Hard Gates

- 必须有复现路径才能 handoff 给 `hf-test-driven-dev`
- 必须确认根因 + 最小安全修复边界才能进入实现
- 不得把 hotfix 当成跳过质量链的理由
- 若修复边界会改变用户可见行为、公共接口、跨模块状态或数据契约，`interactive` 模式下必须先确认边界再 handoff

## Workflow

### 1. 建立证据基线

读缺陷报告、用户描述、相关代码/日志、项目级约定、feature `progress.md`（默认 `features/<active>/progress.md`）、当前已批准规格 / 设计 / 任务工件（默认 `features/<active>/spec.md` / `design.md` / `tasks.md`），以及受影响的 review / gate / verification 记录（如有）。

如果用户声称“这是 bug”，但改动内容看起来像新增字段、放宽约束、改变导出格式或扩展行为，先补一层契约核对：
- 是否存在已批准的 spec / 设计 / API 契约明确要求“当前行为本应如此”
- 如果现有工件只能证明“想新增能力”，不能证明“当前实现违反既有要求”，则不要按 hotfix 推进，优先转 `hf-increment`

### 1.5 Precheck

在进入复现与 handoff 设计前，先确认：

- 当前问题能被稳定描述为既有行为回归 / 实现缺陷，而不是需求变更
- 当前 feature `progress.md` 的 `Current Stage`、`Current Active Task`、worktree 字段与当前案例证据不冲突
- 至少已经固定当前证据基线，后续不会在“哪个分支 / 哪个 worktree / 哪个既有契约”上继续漂移

若不满足，停止 hotfix 主流程，并写出唯一下一步：

- 更像 increment：`hf-increment`
- route / stage / worktree / 既有契约仍冲突：`hf-workflow-router`

### 2. 构建最小复现

确认复现方法。记录步骤、环境、预期 vs 实际。若无法复现 → 标为阻塞并说明原因。

### 3. 收敛根因与修复边界

定位根因。确定最小安全修复范围：改什么文件、影响什么行为、不改什么。显式写出修复边界，不扩大也不缩小。

### 3A. 修复边界确认点

出现以下任一信号时，不要直接 handoff 实现：
- 修复不再是“最小安全改动”，而是开始扩散到多个模块或多个行为
- 修复会改变用户可见行为、公共接口、数据契约或上游约束
- 当前只能确认症状级修补，根因仍是 `probable` 而不是 `demonstrated`

处理规则：
- `interactive`：先展示“建议修什么 / 明确不修什么 / 为什么这仍是最小边界”，等真人确认
- `auto`：只有边界仍清晰且证据足够时才继续；否则回 `hf-workflow-router`

### 4. 决定重入节点

- 有复现路径 + 根因确认 + 修复边界清晰 → handoff `hf-test-driven-dev`
- 实际是需求变更/范围调整，或缺少现有契约证明“这是既有行为回归” → `hf-increment`
- 证据不足以确认根因 → `hf-workflow-router`

### 5. 写回证据和状态同步

记录保存到 项目声明的 verification 路径；若无项目覆写，默认使用 `features/<active>/verification/hotfix-<topic>.md`。同步 feature `progress.md`（默认 `features/<active>/progress.md`）。若使用 worktree 记录 Worktree Path/Branch。

写记录时优先使用 `references/hotfix-repro-and-sync-record-template.md`；时间极紧时可先用其中的简化版模板，但不能省略复现方式、修复边界和唯一下一步。

至少同步：

1. `Current Stage`
2. `Current Active Task`（保留原值或在明确失效时写明）
3. `Pending Reviews And Gates`
4. `Workspace Isolation` / `Worktree Path` / `Worktree Branch`（若存在）
5. 唯一 canonical `Next Action Or Recommended Skill`

## Output Contract

默认输出 / 记录结构：

```markdown
## 热修复摘要

- 问题：
- 当前判断：`confirmed-hotfix` | `more-like-increment` | `blocked`
- 影响范围：
- 紧急级别：

## 证据基线

- 合同 / 回归证明：
- `Current Stage`：
- `Current Active Task`：
- `Pending Reviews And Gates`：
- `Worktree Path`：
- `Worktree Branch`：

## 复现信息

- 期望行为：
- 实际行为：
- 复现方式：
- 失败证据：

## 修复范围

- 最小改动内容：
- 未纳入本次修复的内容：
- 根因信心：`demonstrated` | `probable`

## 同步项

- 规格 / 设计 / 任务：
- 发布说明 / 状态记录：

## 状态同步

- `Current Stage`：
- `Current Active Task`：
- `Pending Reviews And Gates`：
- Next Action Or Recommended Skill:
```

Hotfix 分析结束时必须明确：
- 当前问题是否已稳定复现
- 修复边界是否已确认
- 下一步是 `hf-test-driven-dev`、`hf-increment` 还是 `hf-workflow-router`

## 和其他 Skill 的区别

| Skill | 区别 |
|-------|------|
| `hf-test-driven-dev` | 写/修代码、TDD 实现；本 skill 只做分析和根因收敛，不写生产代码 |
| `hf-increment` | 处理需求变更/范围调整；本 skill 处理已上线功能的缺陷修复 |
| `hf-workflow-router` | 编排/路由/阶段判断；本 skill 专注于紧急缺陷的分析与 handoff |
| `hf-bug-patterns` | 把重复错误沉淀成长期模式；本 skill 聚焦单个缺陷的复现与根因 |

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/hotfix-repro-and-sync-record-template.md` | 热修复复现、边界、同步项和下一步的标准模板 |

## Red Flags

- 不复现就给修复方案
- 修了一大片"顺便优化"
- 把 hotfix 当借口跳过 review/gate
- 根因没确认就进入实现
- 边界已明显扩散，却不暂停确认

## Verification

- [ ] hotfix / increment 分支判断已固定，且没有把需求变更误判成 hotfix
- [ ] 证据基线、当前 stage 与 worktree 锚点已记录
- [ ] 复现路径已记录
- [ ] 根因和最小修复边界已确认
- [ ] 边界扩散时已经过确认点或回到 router
- [ ] handoff 包含足够信息给 `hf-test-driven-dev`
- [ ] feature `progress.md` 已按 canonical schema 同步，且唯一下一步清晰

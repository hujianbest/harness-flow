---
name: mwf-problem-fix
description: Use when a DTS / 紧急缺陷 / 已上线问题 needs reproduction, root-cause analysis, and a minimum-safe fix boundary before any code change, when mwf-workflow-router has selected the hotfix profile, or when an AR-route encountered a regression that should be analyzed as a problem before further implementation. Not for writing the fix code (→ mwf-tdd-implementation), not for AR design (→ mwf-ar-design), not for component design changes (→ mwf-component-design), not for stage / route confusion (→ mwf-workflow-router).
---

# mwf 问题修改 / Hotfix 分析

在不放弃验证纪律的前提下，处理 DTS / 紧急缺陷：复现路径、根因收敛、最小安全修复边界、决定回流节点。

本 skill **不**写生产代码（那是 `mwf-tdd-implementation` 的职责），**不**修改组件实现设计（必要时回 `mwf-component-design`），**不**替开发负责人决定优先级，**不**绕过 review / gate。紧急 ≠ 跳过。

## When to Use

适用：

- DTS / 缺陷单 / 紧急问题需要修复前的复现 + 根因 + 修复边界
- `mwf-workflow-router` 已选择 `hotfix` profile
- 用户说"先把这个问题分析清楚再改"

不适用 → 改用：

- 写修复代码 → `mwf-tdd-implementation`
- 需求变更 / 范围调整 → 回 `mwf-specify`（或 router）
- 修复需要 AR 实现设计 → `mwf-ar-design`
- 修复触及组件边界 → `mwf-component-design`
- 阶段不清 / 证据冲突 → `mwf-workflow-router`

## Hard Gates

- 必须有复现路径（或显式无法复现说明）才能 handoff 给 `mwf-tdd-implementation`
- 必须确认根因 + 最小安全修复边界
- 不得把 hotfix 当作跳过 `mwf-test-checker` / `mwf-code-review` / `mwf-completion-gate` 的理由
- 修复边界扩散（跨多模块 / 改公共接口 / 改用户可见行为 / 改数据契约）→ `interactive` 模式下必须先确认边界，`auto` 模式下回 router
- 不替模块架构师决定接口 / 数据契约改动
- 修复若实质上是「新增能力」或「需求变更」→ 不走 hotfix，回 `mwf-specify` 或 router
- 不写生产代码

## Object Contract

- Primary Object: problem-fix package（reproduction + root cause + fix boundary + 回流节点）
- Frontend Input Object: DTS / 缺陷单原文、用户描述、相关代码 / 日志、`docs/component-design.md`、`docs/ar-designs/`、`AGENTS.md`、当前 `features/<id>/progress.md`（若已存在）
- Backend Output Object:
  - `features/DTS<id>-<slug>/reproduction.md`
  - `features/DTS<id>-<slug>/root-cause.md`
  - `features/DTS<id>-<slug>/fix-design.md`
  - `features/DTS<id>-<slug>/progress.md` canonical 同步
  - `features/DTS<id>-<slug>/README.md` 状态同步
- Object Transformation: 把缺陷输入转成可被 `mwf-tdd-implementation` 消费的最小修复包
- Object Boundaries: 不写生产代码 / 不修改 AR 设计或组件设计 / 不顺手优化
- Object Invariants: DTS ID / 所属组件 / 复现路径在 handoff 后保持稳定

## Methodology

- **Root Cause Analysis (RCA / 5 Whys)**: 从表象逐层追问到根因；不只修表象
- **Minimum Safe Fix Boundary**: 显式定义改什么 / 不改什么 / 影响什么
- **Reproduce First**: 必须先复现或显式无法复现
- **Contract Sanity Check**: 校对当前行为是否真的违反既有 spec / 设计 / API 契约
- **Blameless Post-Mortem Mindset**: 关注机制 / 系统性原因，不归咎个人
- **Embedded Risk Awareness**: 内存 / 并发 / 实时性 / 资源 / 错误处理在根因分析中作为一等输入

## Workflow

1. 建立证据基线
   - Object: 缺陷输入证据基线
   - Method: Read-On-Presence + Contract Sanity Check
   - Input: 缺陷报告原文、用户描述、相关代码 / 日志、`docs/component-design.md`、`docs/ar-designs/`、相关 review / verification 记录、`features/<id>/progress.md`（若存在）
   - Output: 输入清单 + 当前已知事实 + 待确认项
   - Stop / continue: 缺陷描述指向「需求变更」/「新增能力」（既有 spec / 设计未要求当前行为）→ 阻塞，回 `mwf-specify` 或 router

2. 初始化或对齐 work item 目录
   - Object: `features/DTS<id>-<slug>/` 骨架
   - Method: Artifact Layout
   - Input: DTS ID、所属组件、Owner
   - Output:
     - 新 DTS：按 `templates/mwf-work-item-readme-template.md` 创建 `README.md`、`templates/mwf-progress-template.md` 创建 `progress.md`
     - 已存在：核对 progress.md canonical 字段
   - Stop / continue: 缺 DTS ID / 所属组件 → 阻塞

3. 构建复现路径
   - Object: 复现路径
   - Method: Reproduce First
   - Input: 缺陷描述 + 环境信息
   - Output: `features/DTS<id>-<slug>/reproduction.md`，至少含：
     - 期望行为（指向既有 spec / 设计 / API 契约的具体锚点）
     - 实际行为
     - 复现步骤（环境、版本、配置、命令）
     - 失败证据（日志、退出码、stack trace）
     - 复现是否稳定（每次必现 / 偶现 / 仅特定环境）
   - Stop / continue: 无法复现 → 显式标 `unable-to-reproduce`，写明已尝试的环境与下一步建议；不得隐瞒

4. 根因分析
   - Object: 根因
   - Method: Root Cause Analysis (5 Whys) + Embedded Risk Awareness
   - Input: 步骤 3 复现 + 代码现状
   - Output: `features/DTS<id>-<slug>/root-cause.md`，至少含：
     - 根因层级（5 Whys 链）
     - 根因维度（编码错误 / 设计缺陷 / 接口契约不一致 / 内存 / 并发 / 实时性 / 配置）
     - 信心程度：`demonstrated`（有直接证据）/ `probable`（间接证据）
     - 是否可能在其他相似路径上也存在（横向影响）
   - Stop / continue: 信心仅 `probable` 且修复边界扩散 → 不能 handoff，回步骤 3 补复现或上抛模块架构师

5. 最小安全修复边界
   - Object: 修复边界
   - Method: Minimum Safe Fix Boundary
   - Input: 步骤 3-4 + 当前 docs/component-design.md / docs/ar-designs/
   - Output: `features/DTS<id>-<slug>/fix-design.md`，至少含：
     - 改什么：文件 / 函数 / 配置
     - 不改什么：显式列出避免顺手扩散
     - 影响什么：用户可见行为 / 公共接口 / 数据契约 / 跨组件
     - 是否需要补 AR 实现设计 / 修订组件实现设计
     - 测试设计要点：复现脚本将作为 RED 用例；额外的边界 / 异常用例
     - 嵌入式风险审计：内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI 各维度
   - Stop / continue:
     - 修复触及组件边界 → 标 `reroute_via_router=true`，下一步 `mwf-component-design`
     - 修复需要正式 AR 实现设计（DTS 涉及功能 / 状态变更）→ 下一步 `mwf-ar-design`
     - 否则可直接进入 `mwf-tdd-implementation`，但本节点不写代码

6. 修复边界确认点
   - Object: 边界确认
   - Method: Minimum Safe Fix Boundary
   - Input: 步骤 5 边界 + 扩散信号
   - Output: 通过 / 等待真人确认 / 回 router
   - Stop / continue:
     - 修复扩散到多模块 / 多行为
     - 修复改用户可见行为 / 公共接口 / 数据契约
     - 根因仅 `probable`
     - `interactive`：先展示「建议修什么 / 明确不修什么 / 为什么这是最小边界」，等真人确认
     - `auto`：边界仍清晰且证据充分时继续，否则 `reroute_via_router=true` 回 router

7. 决定回流节点
   - Object: 回流节点
   - Method: Route Decision

   | 条件 | 回流节点 |
   |---|---|
   | 复现 + 根因 + 修复边界清晰、不触组件 / 不需要正式 AR 设计 | `mwf-tdd-implementation` |
   | 修复需要正式 AR 实现设计 | `mwf-ar-design` |
   | 修复触及组件边界 | `mwf-component-design`（先升 component-impact） |
   | 实际是需求变更 | `mwf-specify` |
   | 证据不足以确认根因 | `mwf-workflow-router`（`reroute_via_router=true`） |

8. 同步 progress 与 traceability
   - Object: progress.md、traceability.md
   - Method: Canonical Field Sync
   - Output:
     - `features/DTS<id>-<slug>/traceability.md`：补 IR / SR / AR（若涉及功能需求）/ 设计 / 代码 / 测试占位
     - `features/DTS<id>-<slug>/progress.md`：`Current Stage = mwf-problem-fix`、`Next Action Or Recommended Skill = <步骤 7 回流节点>`、`Pending Reviews And Gates = test-check, code-review, completion-gate`

## Output Contract

- `features/DTS<id>-<slug>/reproduction.md`、`root-cause.md`、`fix-design.md`
- `features/DTS<id>-<slug>/progress.md` canonical 同步
- `features/DTS<id>-<slug>/README.md` 状态同步
- handoff 摘要：

  ```yaml
  current_node: mwf-problem-fix
  work_item_id: DTS<id>
  owning_component: <component>
  result:
    reproduction: stable | flaky | unable-to-reproduce
    root_cause_confidence: demonstrated | probable
    fix_boundary: minimal | confirmed-narrow | escalated
  artifact_paths:
    - features/DTS<id>-<slug>/reproduction.md
    - features/DTS<id>-<slug>/root-cause.md
    - features/DTS<id>-<slug>/fix-design.md
  next_action_or_recommended_skill: <步骤 7 回流节点>
  reroute_via_router: true | false
  ```

## Red Flags

- 不复现就给修复方案
- 顺手「优化」其他代码
- 把 hotfix 当借口跳过 review / gate
- 根因仅 `probable` 却直接 handoff 实现
- 修复边界已扩散却不暂停确认
- 把需求变更包装成 hotfix（绕过 spec 流程）
- 在 fix-design.md 中写完整生产代码
- DTS 触及组件边界仍指向 `mwf-tdd-implementation`

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 复现失败就跳过复现节直接给方案 | 标 `unable-to-reproduce`，回 router 决定是否上抛 |
| 修复扩散到多模块仍指向 tdd | 触发步骤 6 边界确认点；超过则回 router 升 component-impact |
| DTS 实际是新增能力 | 阻塞，回 `mwf-specify` 或 router |

## Verification

- [ ] `features/DTS<id>-<slug>/` 目录骨架已建立
- [ ] reproduction.md 已落盘（含期望 / 实际 / 步骤 / 证据 / 稳定性）
- [ ] root-cause.md 已落盘（含 5 Whys / 维度 / 信心 / 横向影响）
- [ ] fix-design.md 已落盘（含改什么 / 不改什么 / 影响什么 / 嵌入式风险）
- [ ] 修复边界扩散信号已显式处理（确认或回 router）
- [ ] traceability.md 已补 DTS 相关行
- [ ] progress.md canonical 同步，下一步唯一指向回流节点
- [ ] 未写生产代码

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/repro-and-rca-templates.md` | reproduction.md / root-cause.md / fix-design.md 模板 |
| `skills/templates/mwf-work-item-readme-template.md` | DTS work item README 模板 |
| `skills/templates/mwf-progress-template.md` | progress.md 模板 |
| `skills/docs/mwf-workflow-shared-conventions.md` | hotfix profile 路径与 canonical 字段 |
| `mwf-workflow-router/references/profile-and-route-map.md` | hotfix route 触发条件 |

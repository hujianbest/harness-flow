---
name: mwf-finalize
description: Use when mwf-completion-gate has returned 通过 and the AR / DTS work item must be formally closed out, when long-term assets (component-design, ar-designs, interfaces, dependencies, runtime-behavior) need to be promoted from features/<id>/ to the component repo's docs/, or when the user explicitly asks "做收尾 / closeout / 把这个 AR 收掉". Not for new implementation (→ mwf-tdd-implementation), not for completion judgment (→ mwf-completion-gate), not for stage / route confusion (→ mwf-workflow-router).
---

# mwf 收尾

正式做 AR / DTS work item 的 closeout：消费 `mwf-completion-gate` 的结论，把过程产物里的正式设计（组件实现设计、AR 实现设计、接口 / 依赖 / 运行时行为变化）同步到组件仓库 `docs/`，把 work item 状态收口为 `closed`。

mwf 默认每个 work item 一次 finalize，对应一个完整 AR 或 DTS 的关闭；不维护 task queue，不区分 task closeout / workflow closeout。

本 skill **不**做新实现、**不**替 completion gate 判断完成、**不**修改其他组件、**不**创造新需求方向。

## When to Use

适用：

- `mwf-completion-gate` verdict = `通过`
- 用户明确要求「做收尾 / closeout / 把这个 AR 收掉」
- 当前剩余工作主要是：状态收口、长期资产同步（`docs/component-design.md`、`docs/ar-designs/`、`docs/interfaces.md`、`docs/dependencies.md`、`docs/runtime-behavior.md`）、handoff 给团队 / 提交 / 合并

不适用 → 改用：

- completion gate 还没通过 → `mwf-completion-gate`
- 还需要新实现 → `mwf-tdd-implementation`
- 阶段不清 → `mwf-workflow-router`

## Hard Gates

- 无 `mwf-completion-gate` `通过` verdict 不得进入
- 不混入新实现；发现需改动 → 停下回 `mwf-completion-gate` 或 `mwf-tdd-implementation`
- 长期资产同步必须按 promotion rules（`docs/mwf-principles/03 artifact-layout.md`）执行
- 必须记录 closeout verdict（`closed` / `blocked`）
- 不修改其他组件
- 不替模块架构师 / 开发负责人决定是否合并 / 发布

## Object Contract

- Primary Object: closeout pack（含 evidence matrix、长期资产同步清单、状态字段）
- Frontend Input Object: `features/<id>/completion.md`（应 `通过`）、`features/<id>/ar-design-draft.md`、`features/<id>/component-design-draft.md`（component-impact 时）、所有 review 记录、`docs/component-design.md` / `docs/ar-designs/` / `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md` 现状、`features/<id>/progress.md`
- Backend Output Object:
  - `features/<id>/closeout.md`
  - 同步到 `docs/component-design.md`（component-impact 时）
  - 同步到 `docs/ar-designs/AR<id>-<slug>.md`（AR 工作项必填）
  - 同步到 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（如本次触发变化）
  - `features/<id>/progress.md` 收口为 `Current Stage = closed`
  - `features/<id>/README.md` 状态收口
- Object Transformation: 把过程产物 promote 为长期资产 + 状态收口
- Object Boundaries: 不写代码 / 不动其他组件 / 不动其他 work item
- Object Invariants: closeout 后 `Next Action Or Recommended Skill = null`（已完成）

## Methodology

- **Project Closeout**: 系统性收尾，确认交付物完成、状态同步、handoff 完整
- **Promotion Rules (mwf-principles 03)**: 过程目录 → 长期资产
- **Evidence Bundle Pattern**: closeout pack 列出已消费的所有证据
- **Sync-On-Presence**: 项目当前未启用的可选资产不构成 `blocked`
- **Single-Work-Item Discipline**: 一次 finalize 对应一个 AR / DTS

## Workflow

1. 读取 gate 结论与当前状态
   - Object: 输入证据基线
   - Method: Read-On-Presence
   - Input: `features/<id>/completion.md`、所有 review 记录、ar-design-draft.md、component-design-draft.md（如有）、`docs/...`、`features/<id>/progress.md`、`features/<id>/README.md`、`AGENTS.md`
   - Output: 输入清单 + completion verdict
   - Stop / continue: completion verdict ≠ `通过` → 阻塞，回 `mwf-completion-gate`

2. Precheck
   - Object: precheck 结论
   - Method: 三态判定
   - Output: 通过 / blocked-content / blocked-workflow
   - Stop / continue:
     - completion 缺记录 → blocked-content，回 `mwf-completion-gate`
     - 必须同步项缺失（如 AR 工作项缺 docs/ar-designs/ 同步路径） → blocked-content，先在本节点完成 promote
     - profile / route / 上游 verdict 冲突 → blocked-workflow，`reroute_via_router=true`

3. 同步长期资产
   - Object: `docs/` 长期资产
   - Method: Promotion Rules
   - Input: 过程产物 + 各 docs/ 现状
   - Output:
     - **AR 工作项必须同步**：把 `features/<id>/ar-design-draft.md`（终版） promote 到 `docs/ar-designs/AR<id>-<slug>.md`（保留 AR ID / SR / IR / Owner / 测试设计章节锚点）
     - **component-impact 必须同步**：把 `features/<id>/component-design-draft.md`（终版）合并到 `docs/component-design.md`（必要时新增章节 / 修订条目）
     - **接口 / 依赖 / 运行时行为如有变更**：同步 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`
     - **DTS 不修改 AR 设计时**：在 closeout pack `Long-Term Assets Sync` 写 `N/A`，但若 DTS 修改了组件级行为，仍需同步 `docs/component-design.md`
   - Stop / continue: 项目当前未启用的可选资产 → 写 `N/A（项目未启用）`，不阻塞

4. 同步 work item 状态
   - Object: `features/<id>/progress.md`、`features/<id>/README.md`
   - Method: Canonical Field Sync
   - Output:
     - `progress.md`：
       - `Current Stage = closed`
       - `Next Action Or Recommended Skill = null`
       - `Pending Reviews And Gates`：清空
       - `Last Updated`：当前时间
     - `README.md`：
       - `Closed`：当前日期
       - `Closeout Verdict`：`closed`
       - `Process Artifacts` 表 Closeout 行更新为 `present`
       - `Reviews & Gates` 表 completion-gate 行更新

5. 形成 evidence matrix
   - Object: closeout evidence matrix
   - Method: Evidence Bundle Pattern
   - Output: 列出每条证据的路径与状态（含 N/A）

6. 产出 closeout pack
   - Object: `features/<id>/closeout.md`
   - Method: 模板填写
   - Input: 步骤 3-5 结果
   - Output: 按 `templates/mwf-closeout-template.md` 写入完整 closeout pack
   - Stop / continue: pack 缺关键字段 → 回步骤 3-5 补齐

7. Handoff
   - Object: closeout 结论 + 团队 handoff
   - Method: Handoff Pack Pattern
   - Output:
     - 提供给团队的 closeout summary（含分支 / MR / PR 信息、长期资产同步清单、未闭合风险）
     - 不替开发负责人 / 模块架构师决定是否合并 / 发布

## Output Contract

- `features/<id>/closeout.md`，按 `templates/mwf-closeout-template.md`
- 长期资产同步：
  - AR 工作项：`docs/ar-designs/AR<id>-<slug>.md` 必填
  - component-impact：`docs/component-design.md`（+ 视情况 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`）
  - 未触发资产变化：closeout pack 中显式写 `N/A`
- `features/<id>/progress.md` 收口为 `Current Stage = closed`、`Next Action Or Recommended Skill = null`
- `features/<id>/README.md` 状态收口
- 结构化 handoff 摘要：work_item_id、closeout_verdict、long_term_assets_synced、blockers、`next_action_or_recommended_skill = null`

## Red Flags

- completion gate 没通过就开始 finalize
- 长期资产未同步就声称 closeout 完成
- AR 工作项跳过 `docs/ar-designs/` 同步
- 把过程目录里的草稿直接当作长期资产（应做 promote 改写：去掉草稿专属内容、补全长期文档结构）
- 修改其他组件
- 没记录 closeout verdict
- 把闭口后的 work item 移到 `features/archived/`（破坏反向引用）
- closeout 后再写 `Next Action Or Recommended Skill = mwf-workflow-router`（应为 `null`）

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 把 ar-design-draft.md 原样复制到 docs/ar-designs/ | 做必要的语义化改写（去掉草稿过程笔记、补长期资产章节标题） |
| component-impact 但漏同步 docs/component-design.md | 阻塞，回到步骤 3 |
| closeout pack 没列 N/A 项 | 显式列出，避免被误判 blocked |

## Verification

- [ ] completion verdict = `通过` 已确认
- [ ] precheck 结果显式记录
- [ ] 长期资产同步已执行（AR 设计必同步；component-impact 时组件设计必同步；其他按 sync-on-presence）
- [ ] `features/<id>/closeout.md` 已落盘
- [ ] `features/<id>/progress.md` 收口为 `Current Stage = closed`、`Next Action Or Recommended Skill = null`
- [ ] `features/<id>/README.md` 状态收口
- [ ] handoff 摘要含 closeout_verdict / long_term_assets_synced / next_action_or_recommended_skill = null
- [ ] 未混入新实现
- [ ] feature 目录平铺保留在 `features/`（未被移动到 `features/archived/`）

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/promotion-checklist.md` | 长期资产 promote 路径 + 写法约定 |
| `skills/templates/mwf-closeout-template.md` | closeout pack 模板 |
| `skills/docs/mwf-workflow-shared-conventions.md` | 路径、canonical 字段 |
| `docs/mwf-principles/03 artifact-layout.md` | Promotion Rules 原文 |

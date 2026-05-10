---
name: hf-finalize
description: Use when completion gate already allows closeout and the remaining work is state/doc/release-note closure, either for the current completed task or for the whole workflow cycle.
---

# HF Finalize

正式做 closeout。这个 skill 有两个合法分支：
- `task closeout`：当前任务已经完成并通过 completion gate，但 workflow 里仍有剩余 approved tasks，需要把状态收口后交回 上游编排者
- `workflow closeout`：当前任务完成后，已无剩余 approved tasks，需要把整个工作周期正式关闭

它不做：新实现、不替代 completion gate、不替代 router 决定下一任务。

## Methodology

本 skill 融合以下已验证方法：

- **Project Closeout (PMBOK)**: 系统性收尾，确认交付物完成、状态同步、经验归档与交接完整。
- **Release Readiness Review**: 确认 release notes / changelog 与实际变更一致，避免“代码改了但外部记录没闭环”。
- **Handoff Pack Pattern**: 用结构化 closeout pack 固定证据、状态和下一步，保证下个会话能冷启动。

## When to Use

适用：
- 完成门禁 已给出支持 closeout 的结论
- 当前剩余工作主要是状态收口、release notes / changelog、handoff pack
- 用户明确要求“做收尾”“closeout”“整理 release notes / 交付包”

不适用：
- completion gate 还没通过 → 完成门禁
- 还需要新实现或补 fresh evidence → 实现层 TDD / 上游 gate
- stage / route / 剩余任务是否存在仍不清楚 → 上游编排者编排者

## Hard Gates

- 无 on-disk completion / regression 记录，不得进入 finalize
- 不混入新实现；发现需改动则停止并回上游
- 必须先判断 closeout 类型：`task closeout` 或 `workflow closeout`
- 有剩余 approved tasks 时，不得声称 workflow 已结束
- 无剩余 approved tasks 时，不得把下一步再写回 上游编排者
- `workflow closeout` 在 `interactive` 模式下必须先给出 closeout summary，再等真人确认后才把 next action 写成 `null`
- 必须记录 worktree 最终 disposition
- 落盘 `closeout.md` 后必须同时产出 `closeout.html` 视觉伴生报告（除非 closeout.md 自身因前置步骤判定不写入）

## Closeout Decision

先只回答一件事：本次是哪个 closeout 分支？

| 条件 | Closeout Type | Next Action |
|---|---|---|
| 当前任务完成，但仍有剩余 approved tasks | `task closeout` | 上游编排者 |
| 当前任务完成，且已无剩余 approved tasks | `workflow closeout` | `null` / 项目 null 约定 |
| 剩余任务是否存在不清、或 queue 证据冲突 | `blocked` | 上游编排者 |

## Workflow

### 1. 读取 gate 记录和当前状态

读：
- completion records、regression records（默认 `features/<active>/verification/`）
- profile-applicable review / approval records（默认 `features/<active>/reviews/`、`features/<active>/approvals/`）
- 已批准任务计划 / task board（默认 `features/<active>/tasks.md`、`features/<active>/task-board.md`）
- feature `progress.md`（默认 `features/<active>/progress.md`，含 worktree 字段）
- feature `README.md`（默认 `features/<active>/README.md`）
- 项目 release notes / changelog（优先遵循项目级约定；默认 `docs/release-notes/vX.Y.Z.md` + 仓库根 `CHANGELOG.md`）
- 受影响的长期资产入口（默认 `docs/arc42/`、`docs/runbooks/`、`docs/slo/`、`docs/adr/`、`docs/index.md`）

Profile-aware 证据矩阵：
- `full` / `standard`：需要 closeout 所依赖的 reviews + gates 已落盘
- `lightweight`：至少 regression + completion 已落盘

### 1.5 Precheck

在判断 closeout type 前，先确认：

- `completion` / `regression` 记录已落盘，且与当前 stage / active task / worktree 语义一致
- 当前 profile 所需的 review / verification 记录要么已落盘，要么能明确写成 `N/A（按 profile 跳过）`
- “是否还有剩余 approved tasks” 的证据足够稳定，不存在 queue / task board / progress 互相打架

若不满足，不进入 `task closeout` 或 `workflow closeout`，而是明确写成 `blocked`，并把唯一下一步交回 上游编排者。

### 2. 判断 closeout 类型

显式写出：
- 当前是 `task closeout` / `workflow closeout` / `blocked`
- 判断依据：剩余 approved tasks 是否存在、是否唯一、是否已准备重选

若无法稳定判断，就停止 finalize，交回 上游编排者。

### 3. 同步状态字段

无论哪种 closeout，都要同步：
- Current Stage
- Current Active Task（完成后清空或显式关闭）
- Workspace Isolation / Worktree Path / Worktree Branch 的最终状态

分支规则：
- `task closeout`：Current Stage 写回 上游编排者；Next Action 写 上游编排者
- `workflow closeout`：Current Stage 标记为 closed / completed；Next Action 写 `null` 或项目 null 约定

### 3A. 结束工作周期确认点

`task closeout` 不要求额外人工确认；它只是把当前任务收口后交回 router。

`workflow closeout` 则不同：它会把整个工作周期收口为 closed / completed，并把 `Next Action Or Recommended Skill` 写成 `null`。因此：
- `interactive`：先展示 closeout summary + evidence matrix + worktree disposition，等待真人确认“正式结束本轮 workflow”
- `auto`：先写 closeout pack，再按项目 auto 规则把 workflow 视为已关闭

如果用户不同意结束 workflow，或希望保留后续动作，则不要写 `null`，应回到 上游编排者。

### 4. 同步长期资产到 `docs/`，更新 release notes / CHANGELOG

遵循 **sync-on-presence** 原则：**同步范围按 `docs/` 实际存在的子目录 + 本 feature 触发了升级条件的子目录决定**，不要求项目同步未启用的资产。`docs/` 各档载体（`docs/architecture.md` 单文件 vs `docs/arc42/` 拆分；`docs/runbooks/` / `docs/slo/` / `docs/postmortems/` / `docs/release-notes/` / `docs/diagrams/` / `docs/insights/` / `docs/index.md` 等可选子目录；仓库根 `CHANGELOG.md` / `README.md`）按存在判断；具体载体清单见下方"必须 / 条件 / N/A"三类列表。

必须同步项（任何 tier）：

- `docs/adr/NNNN-...md`：把状态 `proposed` 翻为 `accepted`（设计阶段已落地，此处仅状态翻转 + 必要 supersedes / superseded-by 双向链接）
- 仓库根 `CHANGELOG.md`：写入 vX.Y.Z 入口（Keep a Changelog 风格）
- 顶层导航：档 0/1 更新仓库根 `README.md` 中的 active feature / 最近 closeout / ADR 索引行；档 2 更新 `docs/index.md`

按存在同步项（仅当对应载体已启用或本 closeout 触发升级条件）：

- 架构概述：`docs/architecture.md`（档 1）或 `docs/arc42/`（档 2）—— 同步本 feature 改变的架构图景；二者只能同时存在一份
- Glossary：档 1 时归并到 `docs/architecture.md` 的术语表节；档 2 时落到 `docs/arc42/12_glossary.md`
- `docs/runbooks/...`：仅当目录已存在或本 feature 引入第一个生产部署运维点
- `docs/slo/...`：仅当目录已存在或本 feature 引入第一个 SLO
- `docs/diagrams/...`：仅当目录已存在或本 feature 引入需要源码化的图
- `docs/release-notes/vX.Y.Z.md`：仅当目录已启用（档 2）；档 0/1 时仅 `CHANGELOG.md` 即可

并检查规格/设计/任务/状态文档（`features/<active>/` 内）是否与 closeout 结论一致。

判 `blocked` 的条件收紧为：

- 必须同步项缺失或与 closeout 结论不一致；
- 本 feature 触发了某类长期资产变化（例如新增模块、新增运维点、新增 SLO），但 closeout 既未同步现存目录，也未在合理升级时机启用新目录；
- closeout pack 伪造 sync 证据。

未启用的可选资产（如档 0/1 项目尚未启用的 `docs/runbooks/` / `docs/slo/`）不构成 `blocked` 依据，应在 closeout pack 中显式标 `N/A（项目当前未启用此资产）` 或 `N/A（本 feature 未触发该资产变化）`。

### 5. 形成 evidence matrix

每条 closeout 证据都写出：
- record path
- 是否适用于当前 profile
- 若不适用，写 `N/A（按 profile 跳过）`

### 6. 产出 closeout pack

写入 `features/<active>/closeout.md`（基于 `references/finalize-closeout-pack-template.md`）。至少写出：
- closeout type
- 关闭的 scope（当前任务 / 整个 workflow）
- 已消费的 evidence matrix
- 更新过的记录与路径
- release notes / changelog 路径
- worktree disposition
- 当前 stage / active task / next action
- 限制、未完成项、分支 / PR 状态

### 6A. 产出 closeout HTML 工作总结报告

`closeout.md` 是 canonical 机器可读契约，但对人类 reviewer 不够直观。Finalize 结束前**必须**额外产出一份 HTML 工作总结报告，作为 `closeout.md` 的视觉伴生文件：

- 路径：`features/<active>/closeout.html`（与 `closeout.md` 同目录）
- 生成方式：调用 `skills/收尾归档/scripts/render-closeout-html.py <feature-dir>`（纯 Python stdlib，无外部依赖；脚本随 skill 一起 vendor，OpenCode `.opencode/skills/` 软链接 / Cursor `.cursor/rules/` 集成路径都能直接拿到）
- 内容：从 `closeout.md` + `evidence/*.log` + `verification/*.md` + `verification/coverage.json`（如存在）解析得到，自包含单文件，含嵌入式 CSS / 极小 JS，离线可读
- 至少呈现：closeout 类型徽标 + conclusion / workflow trace 时间线 / tests & coverage 面板 / evidence matrix（可搜索可排序）/ state sync / release & docs sync / handoff & limits

执行命令（默认）：

```bash
python3 skills/收尾归档/scripts/render-closeout-html.py features/<active>/
```

判 `blocked` 的情况下也要尝试生成（HTML 自身能展示 blocked 徽标 + 缺失证据状态）；只有当 `closeout.md` 因前置步骤判定不写入时才跳过。

覆盖率取数说明：
- 优先读 `verification/coverage.json`（istanbul / vitest --coverage --reporter=json-summary 的 `total` 字段）
- 否则从 `verification/*.md` 与 `evidence/*.log` 的 `Lines: 92.5%` / `Branches: 70%` / istanbul `All files | ...` 表格行中扫描
- 全部缺失则在 HTML 中显式渲染"未提供覆盖率数据"，不阻塞 closeout

不在 HTML 里塞新的事实：HTML 报告**只是渲染** `closeout.md` + 已落盘的 evidence，不允许引入 closeout pack 之外的新 conclusion / approval。

## Output Contract

默认 closeout pack 结构：

```markdown
## Closeout Summary

- Closeout Type: `task-closeout` | `workflow-closeout` | `blocked`
- Scope:
- Conclusion:
- Based On Completion Record:
- Based On Regression Record:

## Evidence Matrix

- Artifact:
- Record Path:
- Status:

## State Sync

- Current Stage:
- Current Active Task:
- Workspace Isolation:
- Worktree Path:
- Worktree Branch:
- Worktree Disposition:

## Release / Docs Sync

- Release Notes Path:                      # 档 0/1：CHANGELOG.md（vX.Y.Z 入口）；档 2：docs/release-notes/vX.Y.Z.md
- CHANGELOG Path:                          # 例：CHANGELOG.md（v1.5.0 入口）—— 任何 tier 必填
- Updated Long-Term Assets:                # 按存在同步：列出本次同步路径，未启用项写 N/A
  - docs/adr/NNNN-...md（status: proposed → accepted）
  - 架构概述：docs/architecture.md（档 1）或 docs/arc42/...（档 2）；本 feature 未触发架构变化时写 N/A
  - docs/runbooks/...：N/A（项目当前未启用此资产）/ N/A（本 feature 未触发）/ 实际路径
  - docs/slo/...：同上
  - docs/diagrams/...：同上
- Index Updated:                           # 档 0/1：仓库根 README.md 中 active feature 行；档 2：docs/index.md

## Handoff

- Remaining Approved Tasks:
- Next Action Or Recommended Skill:
- PR / Branch Status:
- Limits / Open Notes:
```

Closeout type-specific 约束：
- `task closeout`：`Next Action Or Recommended Skill` 必须是 上游编排者
- `workflow closeout`：`Next Action Or Recommended Skill` 必须是 `null` 或项目 null 约定
- `blocked`：`Next Action Or Recommended Skill` 必须是 上游编排者，且不得声称 closeout 已完成

`workflow closeout` 在 `interactive` 模式下追加：

```markdown
## Final Confirmation

- Question: 是否确认正式结束本轮 workflow？
- If confirmed: write `Next Action Or Recommended Skill: null`
- If not confirmed: return to 上游编排者
```

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/finalize-closeout-pack-template.md` | closeout pack 模板（含 HTML 伴生报告字段说明） |
| `scripts/render-closeout-html.py`（本 skill 子目录 `skills/收尾归档/scripts/`，ADR-006 引入的 skill-owned 工具约定） | 由 `closeout.md` + 旁路工件生成 `closeout.html` 视觉报告，纯 Python stdlib，自包含单文件输出。仓库根 `scripts/` 保留给跨 skill 的维护者工具（如 `audit-skill-anatomy.py`） |
| `实现层 TDD/references/worktree-isolation.md` | worktree disposition 的收尾语义（不擅自删除；只记录 `kept-for-pr` / `cleaned-per-project-rule` / `in-place`） |

## Red Flags

- 不区分 `task closeout` 和 `workflow closeout`
- 有剩余任务却宣称 workflow done
- 没剩余任务却仍写回 上游编排者
- release notes / CHANGELOG 没更新就声称 closeout 完成
- 长期资产（已存在的架构概述 / runbooks / SLO / ADR 状态）未同步就宣称 closeout 完成
- 为项目当前未启用的可选资产（如档 0/1 没有的 `docs/runbooks/` / `docs/slo/`）误判 `blocked`
- 同时存在 `docs/architecture.md` 与 `docs/arc42/`（架构概述应二选一）
- 把 closeout 后的 feature 目录移动到 `features/archived/`，破坏其它工件的反向引用
- 用会话记忆代替 on-disk 记录
- 忘记记录 worktree 最终 disposition
- 只写 `closeout.md` 不生成 `closeout.html`，或在 HTML 里捏造 `closeout.md` 之外的 conclusion / 测试数据 / 覆盖率

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "completion-gate pass 了，state sync 我下次会话再补。" | Hard Gates: state sync / progress 闭合是 finalize 必需输出；跨会话补 = 没补。 |
| "release notes 我直接复制 commit messages。" | Workflow stop rule: release notes 必须按 PMBOK closeout 的格式，覆盖 scope / artifact / handoff，不是 commit dump。 |
| "handoff pack 不重要，next agent 自己看 commit。" | Hard Gates: handoff pack 是 evidence-based recovery 的唯一入口；缺位 → 下游 agent 无 canonical 起点。 |
| "finalize 之后顺便 deploy。" | Hard Gates (ADR-001 D1 / ADR-002 D1): 主链终点是工程级 closeout；deploy / ship / ops 不在 v0.1.x / v0.2.x 范围。 |

## Verification

- [ ] precheck 已完成；若证据缺失或 queue 冲突，已返回 `blocked` + 上游编排者
- [ ] 已判断 closeout type
- [ ] gate 证据已引用
- [ ] evidence matrix 已落盘
- [ ] feature `progress.md` / release notes / CHANGELOG / `docs/` 长期资产已**按存在同步**，closeout pack `Release / Docs Sync` 区块显式列出实际同步路径与 `N/A` 项
- [ ] 涉及的 ADR 状态已从 `proposed` 翻为 `accepted`（如适用）
- [ ] 顶层导航已更新：档 0/1 更新仓库根 `README.md`；档 2 更新 `docs/index.md`
- [ ] feature `README.md` 中 Closed / Closeout Type / Linked Long-Term Assets 等区块已更新
- [ ] 未为项目当前未启用的可选资产（如档 0/1 没有的 `docs/slo/` / `docs/postmortems/`）误判 `blocked`
- [ ] closeout pack 已写入 `features/<active>/closeout.md`
- [ ] HTML 视觉伴生报告已写入 `features/<active>/closeout.html`（由 `python3 skills/收尾归档/scripts/render-closeout-html.py <feature-dir>` 生成；脚本与 skill 同 vendor）；缺覆盖率数据时 HTML 已显式标注"未提供"，未编造数据
- [ ] worktree 状态已同步
- [ ] `task closeout` 时 next action = 上游编排者
- [ ] `workflow closeout` 时 next action = `null` 或项目 null 约定
- [ ] `workflow closeout` 在 interactive 模式下已显式经过最终确认
- [ ] feature 目录平铺保留在 `features/`，未被移动到 `features/archived/`
- [ ] 下一个会话能继续而不需猜测

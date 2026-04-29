---
name: hf-doc-freshness-gate
description: 适用于已通过 hf-regression-gate、即将进入 hf-completion-gate、需要为本任务/本 feature 引入的对外可见行为变化判定相关用户文档（仓库根 README 产品介绍段、模块层 README、公共 API doc / OpenAPI / docstring、i18n 副本、CONTRIBUTING / onboarding doc、用户文档站 source）是否同步刷新的场景。不适用于尚未通过 hf-regression-gate（→ 上游）、纯 prose feature 但 reviewer 误以为强制 lint 工具链、阶段不清或证据冲突（→ hf-workflow-router）。
---

# HF Doc Freshness Gate

判定本任务 / 本 feature 引入的 user-visible behavior change 是否已在**对外可见文档**中同步刷新，并按 sync-on-presence + profile 分级 + 与 `hf-completion-gate` / `hf-finalize` / `hf-increment` / `hf-code-review` / `hf-traceability-review` 显式分工的纪律输出 `verdict + fresh evidence`。

**职责边界**：本 gate 只负责"对外可见文档的同步 verdict"。同 tier 的 `hf-regression-gate` 负责"行为不回归"；下游 `hf-completion-gate` 消费本 gate verdict 作为 evidence bundle 一项；`hf-finalize` 在 closeout 阶段同步既有合同覆盖的长期资产（CHANGELOG / ADR 状态翻转 / 顶层导航 / docs/architecture / docs/runbooks 等），**不重叠**本 gate 负责的对外可见文档维度。完整责任划分见 `references/responsibility-matrix.md`。

## Methodology

本 skill 融合以下已验证方法。每条方法在 Workflow 中有对应落地步骤。

| 方法 | 核心原则 | 落地步骤 |
|---|---|---|
| **Three-Section Skill Contract** (HF native) | 与 `hf-regression-gate` / `hf-completion-gate` 同形态：Hard Gates + Verification + fresh evidence | 整 SKILL 段落布局 |
| **Sync-on-Presence** | 未启用文档载体不构成 blocked；档 0/1/2 任一档下，未启用的 `docs/` 子目录视为 N/A，不计入扣分维度 | 步骤 3 §维度判定 + FR-003 / NFR-004 |
| **Profile-Aware Rigor** | lightweight / standard / full 三档强制维度按 `references/profile-rubric.md` 激活；profile 升档不会回填已通过的轻档维度，但要求新增维度全部覆盖 | 步骤 2 §profile 激活 + FR-004 |
| **Author/Reviewer/Gate Separation** | gate 由独立 readonly reviewer subagent 派发；不自审自交；author / reviewer / gate 三层独立、verdict 由 reviewer 给出，gate 只汇总并落盘 | 步骤 1 §dispatch + FR-008 |
| **Evidence Bundle Pattern** | verdict 路径作为 `hf-completion-gate` evidence bundle 一项被 reference；evidence 必须具备 fresh 性（绑定上游 record / artifact hash），不能引用历史结论 | 步骤 4 §evidence 落盘 + FR-005 |

## When to Use

适用：
- 父会话已通过 `hf-regression-gate`，即将进入 `hf-completion-gate`，需要本 gate verdict 作为 evidence bundle 一项
- 用户明确要求"评估本任务对外可见文档是否同步"
- reviewer subagent 被父会话按 `references/reviewer-dispatch-handoff.md` 派发执行本 gate

不适用：
- 尚未通过 `hf-regression-gate` → 回 `hf-test-driven-dev` 或上游 review skill
- reviewer 误以为本 gate 强制项目方安装 lint 工具链 → NFR-003 显式声明无外部工具链依赖；按 `Red Flags` 列出的"误以为强制 lint 工具"模式自纠
- 阶段不清 / 证据冲突 → `hf-workflow-router`

## Hard Gates

- 本 gate 必须由独立 reviewer subagent (readonly) 派发；不允许父会话或实现节点 (`hf-test-driven-dev`) 自评（FR-008 + CON-006）
- verdict 必须 ∈ `{pass, partial, N/A, blocked}`，不允许其他词表值（FR-002）
- evidence 必须落到 `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`（FR-002 + CON-007）
- 未启用文档载体 → verdict 该维度 = `N/A`，**不构成 blocked**（FR-003 + NFR-004）
- spec/tasks/commits 三类输入全缺 → verdict = blocked，next = `hf-traceability-review`（FR-001 负路径）
- spec 与 commits 实质不一致 → verdict = blocked，next = `hf-increment`（FR-007 负路径）
- 本 gate 不承担 `hf-finalize` 既有合同覆盖的同步动作（ADR 状态翻转 / CHANGELOG / 顶层导航 / docs/architecture / docs/runbooks 等）；不修改 `hf-finalize` / `hf-completion-gate` / `hf-code-review` / `hf-traceability-review` / `hf-increment` 的 SKILL.md（CON-001 + FR-006 + FR-007）
- `lightweight` profile 不允许退化为跳过；至少强制仓库根 README 产品介绍段 + Conventional Commits `docs:` 标记自检（FR-004 + CON-005）
- 不依赖任何外部 lint / 翻译 / 文档生成工具链；可选工具仅作为 evidence 来源（NFR-003 + CON-002）

## Workflow

### 1. 父会话 dispatch reviewer subagent

按 `references/reviewer-dispatch-handoff.md`（复用既有 `hf-workflow-router/references/review-dispatch-protocol.md` 的本 gate 适配点）派发独立 reviewer subagent，readonly 模式。

### 2. Reviewer subagent: 读取输入并按 profile 激活强制维度

reviewer 按以下顺序读取输入（FR-001 + FR-004）：

1. `features/<active>/spec.md` 中本任务 / 本 feature 关联 FR / NFR 条目
2. `features/<active>/tasks.md` 中本任务 Acceptance（如适用）
3. （若使用）Conventional Commits 中的 `feat:` / `fix:` / `BREAKING CHANGE:` / `docs:` 条目
4. `features/<active>/progress.md` 中 `Workflow Profile` 字段
5. 项目级覆盖（若项目已声明）
6. `references/responsibility-matrix.md`（spec §6.2 责任矩阵权威 cold-link）
7. `references/profile-rubric.md`（按上一步读到的 profile 激活强制维度）
8. 项目对外可见文档载体的文件系统扫描（按 `references/responsibility-matrix.md` 本 gate ✅ 行清单逐项检查）

判定优先级：**spec FR/NFR 关联 > tasks Acceptance > Conventional Commits**（按可信度）。

形成 user-visible behavior change list（FR-001）。若三类来源全缺 → 进入步骤 4 输出 verdict = `blocked`，next = `hf-traceability-review`。

### 3. Reviewer subagent: 逐维度判定

按 `references/profile-rubric.md` 激活的强制维度逐项判定，每个维度的 verdict ∈ `{pass, partial, N/A, blocked}`：

| 判定情形 | 维度 verdict | evidence 标注 |
|---|---|---|
| 项目载体不存在（FR-003 sync-on-presence + NFR-004） | `N/A` | "项目当前未启用此资产" |
| 本任务未触发该载体的同步需求（user-visible change list 与该载体无关） | `N/A` | "本 task / feature 未触发该资产变化" |
| 文档已同步 | `pass` | 引用 commits / file diff |
| 部分维度未同步且不阻塞 closeout | `partial` | 列出未同步项 + 影响评估 |
| 关键维度漂移（如仓库根 README 产品介绍段与本次行为相关部分明显过期） | `blocked` | next = `hf-test-driven-dev`（补文档变更） |
| spec 与 commits 实质不一致 | `blocked` | next = `hf-increment`（FR-007） |

整体 verdict 聚合规则：

- 任一维度 = `blocked` → 整体 verdict = `blocked`
- 否则任一维度 = `partial` → 整体 verdict = `partial`
- 否则全部 ∈ `{pass, N/A}` → 整体 verdict = `pass`（如果至少一个 `pass`）或 `N/A`（全部 `N/A`）

### 4. Reviewer subagent: 写 verdict + evidence

按 `templates/verdict-record-template.md` 写入 `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`，至少包含：
- metadata header（reviewer subagent ID、profile、commit hash、被测 task / feature）
- user-visible behavior change list（含 file:line 来源引用）
- 维度判定明细表
- 整体 verdict 与聚合理由
- next action（按整体 verdict 与 §13 输出契约表）
- reviewer-return JSON（结构见 `references/reviewer-dispatch-handoff.md`）

可选 diff log 落到 `features/<active>/evidence/doc-freshness-diff-*.log`。

`lightweight` profile 下使用 `templates/lightweight-checklist-template.md`，verdict 文件 ≤ 30 行（NFR-002）。

### 5. Reviewer subagent 返回；父会话按 verdict 路由

按 reviewer-return JSON 中 `next_action_or_recommended_skill` 路由：

- `pass` / `partial` / `N/A` → next = `hf-completion-gate`（verdict 路径作为 evidence bundle 一项被 reference；FR-005）
- `blocked` (内容) → next = `hf-test-driven-dev`（补文档变更；FR-005 第三条 acceptance）
- `blocked` (workflow) → next = `hf-workflow-router` (`reroute_via_router=true`)

**重要**：`blocked` verdict **不**进入 `hf-completion-gate` evidence bundle；由本 gate 直接路由回 `hf-test-driven-dev`，避免 completion-gate 引入 doc-freshness blocked 的额外判定分支（design §11 boundary constraints）。

## Output Contract

完成时产出：

- **verdict 文件**（必有）：`features/<active>/verification/doc-freshness-YYYY-MM-DD.md`
- **可选 diff log**：`features/<active>/evidence/doc-freshness-diff-*.log`
- **reviewer-return JSON**：返回给父会话；含 `conclusion` / `next_action_or_recommended_skill` / `record_path` / `dimension_breakdown` / `reroute_via_router`
- **`hf-completion-gate` evidence bundle**（仅当 verdict ∈ {pass, partial, N/A}）：verdict 路径作为 evidence bundle 一项被 reference

reviewer-return JSON 不得伪造 verdict；不得为让本 gate "看起来通过" 而擅自把 partial / blocked 改写成 pass。

## Reference Guide

按需加载详细参考内容。

| 主题 | Reference | 加载时机 | 最小 profile |
|---|---|---|---|
| 责任矩阵权威 cold-link | `references/responsibility-matrix.md` | 每次 reviewer dispatch；判定每个维度归属时 | 全档必读 |
| Profile 强制维度判定细则 | `references/profile-rubric.md` | 步骤 2 激活 profile 时 | 全档必读 |
| Reviewer dispatch 适配点 | `references/reviewer-dispatch-handoff.md` | 步骤 1 父会话派发时 | 全档必读 |
| verdict 文件模板 | `templates/verdict-record-template.md` | 步骤 4 写 evidence 时 | standard / full 必读；lightweight 用下行模板 |
| Lightweight checklist 模板 | `templates/lightweight-checklist-template.md` | lightweight profile 步骤 4 | lightweight 必读 |
| 测试 prompts | `evals/test-prompts.json` | reviewer 派发前回归测试 | 全档可选 |

加载策略：

- `lightweight`：默认读 `responsibility-matrix.md` + `profile-rubric.md` + `lightweight-checklist-template.md` + `reviewer-dispatch-handoff.md`
- `standard` / `full`：在 lightweight 基础上加 `verdict-record-template.md`

## 和其他 Skill 的区别

| 易混淆 skill | 区别 |
|-------------|------|
| `hf-completion-gate` | completion-gate 判断"任务是否真的可以宣告完成"（含本 gate verdict 作为 evidence bundle 一项）；本 gate 只回答"对外可见文档是否同步"这一窄问题 |
| `hf-finalize` | finalize 在 closeout 阶段同步既有合同覆盖的长期资产（CHANGELOG / ADR / 顶层导航 / docs/architecture / docs/runbooks 等）；本 gate 不重叠这些维度（spec §6.2 责任矩阵） |
| `hf-increment` | increment 处理范围变更与工件失效；本 gate 在 spec 与 commits 实质不一致时显式 next = increment（FR-007），但本 gate 不做范围变更分析 |
| `hf-code-review` | code-review 检查实现层正确性 / 设计 conformance / Two Hats 纪律；本 gate 不评估代码本身，只评估对外可见文档是否同步 |
| `hf-traceability-review` | traceability-review 反查 spec ↔ design ↔ tasks ↔ code ↔ tests 追溯链；本 gate 在 user-visible change list 三类来源全缺时显式 next = traceability-review（FR-001），但本 gate 不做追溯链反查 |

## Red Flags

- **误以为强制 lint / 翻译 / docs 生成工具链** — NFR-003 显式声明无外部工具链依赖；可选工具仅由项目级约定声明
- **未启用文档载体被误判为 blocked** — FR-003 + NFR-004 明确规定 sync-on-presence；未启用 ≠ blocked
- **lightweight 退化为跳过** — FR-004 + CON-005 明确 lightweight 至少强制仓库根 README + Conventional Commits docs 标记自检
- **承担 hf-finalize 既有合同覆盖的同步动作** — CON-001 + FR-006；spec §6.2 责任矩阵
- **承担 hf-increment 的范围变更分析** — CON-001 + FR-007
- **由父会话或实现节点自评** — FR-008 + CON-006；必须 readonly subagent 派发
- **verdict 词表外的非法值（如 "skip" / "not-applicable" / 中文 "不适用"）** — FR-002 verdict ∈ `{pass, partial, N/A, blocked}` 严格闭集
- **blocked verdict 误进入 hf-completion-gate evidence bundle** — design §11 + spec FR-005 第三条 acceptance；blocked 直接回 hf-test-driven-dev

## Verification

- [ ] reviewer subagent 已 readonly 模式派发
- [ ] verdict ∈ `{pass, partial, N/A, blocked}`
- [ ] verdict 文件已落到 `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`
- [ ] verdict 文件含维度判定明细 + reviewer-return JSON + user-visible change list 来源引用
- [ ] profile-aware 强制维度按 `references/profile-rubric.md` 激活
- [ ] 未启用文档载体维度标 `N/A` + 显式标注理由（FR-003 + NFR-004）
- [ ] `lightweight` profile 下 verdict 文件 ≤ 30 行（NFR-002）+ 至少含仓库根 README 维度
- [ ] 整体 verdict 按聚合规则计算（任一 blocked → blocked；任一 partial → partial；否则 pass / N/A）
- [ ] `pass` / `partial` / `N/A` → next = `hf-completion-gate`，verdict 路径已 reference 到 completion-gate evidence bundle
- [ ] `blocked` → next = `hf-test-driven-dev`（FR-005 第三条）或 `hf-increment`（FR-007）或 `hf-workflow-router`（precheck workflow 阻塞）
- [ ] reviewer 未承担 `hf-finalize` / `hf-code-review` / `hf-traceability-review` / `hf-increment` 既有职责
- [ ] reviewer-return JSON 字段齐全且未伪造 verdict

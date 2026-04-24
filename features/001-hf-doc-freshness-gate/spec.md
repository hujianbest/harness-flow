# `hf-doc-freshness-gate` 需求规格说明

- 状态: 草稿
- 主题: 在 HF 主链上正式立项一个独立 gate（`hf-doc-freshness-gate`），让"完成增量开发后对外可见文档（仓库根 `README.md` 产品介绍段 / 模块层 README / 公共 API doc / i18n 副本 / 用户文档站 / `CONTRIBUTING.md` / onboarding doc）保持新鲜"成为带 verdict + fresh evidence 的 gate 节点
- Workflow Profile: standard
- Execution Mode: auto
- Feature: `features/001-hf-doc-freshness-gate/`
- Discovery 上游: `docs/insights/2026-04-23-hf-doc-freshness-gate-discovery.md`（已通过 review，2026-04-23）
- Discovery Review: `docs/reviews/discovery-review-hf-doc-freshness-gate.md`（结论：通过）
- HYP-001 已通过的 probe: `docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/`（结论：Pass，5 / 5 命中）

## 1. 背景与问题陈述

HF 自身把"工件驱动 + fresh evidence"作为核心叙事，但在文档维度存在断层：

- `hf-finalize` 仅在 `workflow closeout` 时强制同步**有限的几类长期资产**（ADR 状态翻转、`CHANGELOG.md`、顶层导航行、已存在的 `docs/architecture.md` / `docs/arc42/` / `docs/runbooks/` / `docs/slo/` / `docs/release-notes/` / `docs/diagrams/`），覆盖**不到**仓库根 README 的产品介绍段、模块层 README、公共 API doc、i18n 副本、用户文档站、`CONTRIBUTING.md` / onboarding doc 等"用户阅读用"的文档载体。证据见 `skills/hf-finalize/SKILL.md` §4 与 §Verification、`docs/principles/sdd-artifact-layout.md` *Promotion Rules*。
- `hf-increment` 把"代码已经按新逻辑实现，但文档仍是旧结论"列为 Red Flag，但只是 prose-level 心态自检，没有 verdict、没有 fresh evidence、没有 evidence path。
- `task closeout` 路径（即用户语义上的"每次完成一次增量开发"）下不存在等价合同。
- 由此结果：开发者 / 团队读完 HF closeout 仍然要凭直觉判断"哪些对外文档要跟着改"，HF 自身的 fresh-evidence 一致性在文档维度断链。

承接 discovery 草稿 §1 struggling moment：HF 用户希望"每次完成增量开发后" HF 主动给出"哪些对外可见文档需要跟着改、哪些已经按规则同步、哪些还是 N/A"的判断，并把它作为带 fresh evidence 的 verdict 落盘。

## 2. 目标与成功标准

**总体目标**：在 HF 主链上引入独立 gate `hf-doc-freshness-gate`，把"用户可见行为变化必须对应可冷读的对外文档同步证据"从隐性 self-check 升级为带 verdict 的 gate；并以三条纪律保证不退化为模板填空：

1. **sync-on-presence**：未启用的文档载体不构成 `blocked`，与 `docs/principles/sdd-artifact-layout.md` 既有原则一致
2. **profile 分级**：`lightweight` 不退化为跳过、`full` 不让小项目体感沉重，与 `docs/principles/methodology-coherence.md` 既有原则一致
3. **责任边界稳定**：与 `hf-completion-gate` / `hf-finalize` / `hf-increment` 显式分工，不抢戏不重叠（U2 假设落到 §6 责任矩阵）

**总体成功标准**：见 §3 Success Metrics。

## 3. Success Metrics

承接 discovery §9。

| 字段 | 内容 |
|---|---|
| **Outcome Metric** | 在采用 HF 的项目中，"完成一次增量开发后对外可见文档保持新鲜"成为可被冷读的 gate verdict + fresh evidence，而不是依赖人工自觉 |
| **Threshold** | 在 ≥ 2 个真实 HF 项目（含 `lightweight` 与 `standard` 各 1）中，连续 3 次增量开发后产生有效 verdict 文档（`features/<active>/verification/doc-freshness-YYYY-MM-DD.md`），且没有出现"reviewer 标 `pass` 但实际 README 漂移"的案例 |
| **Leading Indicator** | 在试点 HF 项目中，每次 `task closeout` / `workflow closeout` 都能找到一份 `doc-freshness-YYYY-MM-DD.md` verdict 文档（命中率），目标 ≥ 90% |
| **Lagging Indicator** | 试点项目在引入本 gate 后 N=3 次增量开发结束后，仓库根 README / 模块 README / 公共 API doc 的"用户可见行为漂移条数"由 reviewer 抽样判定，目标趋势下降 |
| **Measurement Method** | 通过 `features/<active>/verification/doc-freshness-*.md` 评审日志按 feature 汇总；reviewer 抽样按 closeout pack 引用回查 |
| **Non-goal Metrics** | 不追求 README 字数变化；不追求 docstring 覆盖率到某个百分比；不追求外部 docs 站点构建时间下降；不追求自动翻译覆盖率；不追求 i18n 翻译质量打分 |
| **Instrumentation Debt** | 无新基础设施需求；沿用 HF "Discipline Without Schema / CI" 原则，以 reviewer subagent 抽样 + closeout pack 引用作为采集方式 |

North Star 锚定：HF pack 的 "工件驱动 + fresh evidence 一致延伸到文档维度" 叙事；项目当前**无形式化 North Star 声明**。

## 4. Key Hypotheses

承接 discovery §6。

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-001 | HF 用户在"task / 增量级文档刷新合同应该长在哪里"上偏好新增独立 gate（`hf-doc-freshness-gate`），而不是把合同硬塞回 `hf-finalize` 或嵌入既有 review | Desirability | wedge 站不住，需要回 discovery 修订 OST 主候选 | **high** | ✅ **已通过**：`docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/probe-result.md`（5 / 5 desk research 维度命中） | **否** |
| HYP-002 | 用户能稳定区分 `hf-doc-freshness-gate` vs `hf-finalize` vs `hf-increment` vs `hf-code-review` / `hf-traceability-review` 的责任边界，不重叠不抢戏（**U2**） | Usability | 即使新 gate 落地，与既有节点的边界混乱会让 reviewer / agent 无法稳定判断该哪个 skill 处理 | medium | spec §6 给出显式责任矩阵；`hf-spec-review` reviewer 必须能在不歧义的前提下逐项判 `pass`；任一边界条目歧义 → spec 不允许通过 | **是** |
| HYP-003 | 新增节点不会让 `hf-workflow-router` FSM 复杂度爆炸 | Viability | router 节点 / transition 数量超过运维上限，本 gate 需重构落点 | medium-high | design 阶段做一次 transition map dry run（`hf-workflow-router/references/profile-node-and-transition-map.md`），新增 transition ≤ 6 视为通过 | 否（design 阶段处理） |
| HYP-004 | `lightweight` profile 下 gate 仍能被压缩到 ≤ 5 行 checklist + ≤ 5 分钟人工耗时（**U1**） | Usability | 若 lightweight 退化为跳过，profile 分级承诺被破坏 | medium | design 阶段在 `lightweight` 项目做一次 dry run | 否（design 阶段处理） |

**Blocking 假设关闭策略**：HYP-002 (U2) 是本 spec 唯一 Blocking 假设；通过 §6 责任矩阵 + reviewer 抽样判定关闭。如 reviewer 在 §6 任一边界条目处给出歧义 finding，spec 必须回到 `hf-specify` 修订，不允许通过。

## 5. 用户角色与关键场景

承接 discovery §2 与 §10 Jobs Story。

### 角色

| 角色 | 触发情境 | 该角色对本 gate 的关键期望 |
|---|---|---|
| HF 用户（采用 HF 的开发者 / 团队） | 一个 task / feature 的 implementation + reviews + regression-gate / completion-gate 已通过，准备进入 `hf-finalize` | gate 主动给出对外可见文档同步 verdict + fresh evidence；不需要凭直觉记住 README 要不要改 |
| 后续接手者 / 新成员 / agent | 阅读仓库根 README、模块 README、公共 API doc 试图理解"系统现在是什么样" | 文档与代码行为一致；至少能从 closeout pack 反查"上一次同步是哪个 feature 触发的、verdict 是什么" |
| reviewer subagent | 被父会话按 reviewer dispatch protocol 派发执行本 gate | 责任边界明确（与 `hf-finalize` / `hf-increment` / `hf-code-review` / `hf-traceability-review` 不重叠）；冷读 gate verdict 时不出现"应该哪个 skill 管"的歧义 |

### 关键场景（对应 §8 FR）

- **S1**：父会话完成 `hf-traceability-review` 与 `hf-regression-gate` 后，按 router transition 进入 `hf-doc-freshness-gate`，consume 本任务 / 本 feature 的 user-visible behavior change list（来自 `features/<active>/spec.md` + `tasks.md` + Conventional Commits 中的 `docs:` / `feat:` / `BREAKING CHANGE:` 条目），按 §8 FR 给出 verdict。
- **S2**：reviewer 判定本任务**不存在用户可见行为变化**（例如纯重构 / 内部代码整理 / 测试补全），verdict = `N/A`，不强制创建任何文档变更。
- **S3**：reviewer 判定本任务**存在用户可见行为变化但相关文档载体未启用**（例如项目无模块 README、无 OpenAPI），按 sync-on-presence 标 `N/A`，不构成 `blocked`。
- **S4**：reviewer 判定**部分文档已同步、部分未同步**，verdict = `partial`，给出未同步项清单 + 是否阻塞下一节点（`hf-completion-gate`）。
- **S5**：reviewer 判定**关键对外文档（仓库根 README 产品介绍段中与本次行为相关的部分）漂移**，verdict = `blocked`，next action = 回 `hf-test-driven-dev` / 父会话补文档变更（不是回 router）。

## 6. 当前轮范围与关键边界

### 6.1 当前轮范围

- 引入新 skill `skills/hf-doc-freshness-gate/`：包含 `SKILL.md` + 必要 references / templates
- 在 `hf-workflow-router` 的 transition map 中加入新 gate 节点：位于 `hf-traceability-review` 之后、`hf-regression-gate` / `hf-completion-gate` 同 tier（详细位置由 design 阶段定，HYP-003 dry run 后确认）
- 在 `hf-completion-gate` 的 evidence bundle 中显式列入本 gate 的 verdict（按 sync-on-presence）
- 在 `hf-finalize` 的 evidence matrix 中显式 reference 本 gate（不替代 `hf-finalize` 自身的同步责任）
- profile 分级：`full` 强制全表；`standard` 强制仓库根 README + 公共 API doc + 已存在的 i18n 副本；`lightweight` 至少强制仓库根 README + Conventional Commits `docs:` 标记自检

### 6.2 关键边界（U2 责任矩阵 / Blocking HYP-002 关闭依据）

reviewer 必须能冷读判定**每个文档维度归属哪个 skill**，下表是 spec 阶段对责任分工的硬约束：

| 文档维度 | hf-doc-freshness-gate | hf-finalize | hf-increment | hf-code-review | hf-traceability-review |
|---|:-:|:-:|:-:|:-:|:-:|
| 仓库根 `README.md` 产品介绍段 / Quick Start / Usage / 能力清单 | ✅ verdict + evidence | ❌ | ❌ | ❌ | ❌ |
| 仓库根 `README.md` 中 *active feature / 最近 closeout / ADR 索引行*（指针式导航） | ❌ | ✅ 同步（既有合同） | ❌ | ❌ | ❌ |
| 模块层 / 子包 README（`src/<module>/README.md`、`packages/<x>/README.md`） | ✅ verdict + evidence | ❌ | ❌ | ❌ | ❌ |
| 公共 API docstring / OpenAPI description / 自动文档站 | ✅ verdict + evidence | ❌ | ❌ | ⚠ 实现层正确性 review | ❌ |
| i18n 副本同步（如 `README.md` ↔ `README.zh-CN.md`） | ✅ verdict + evidence（仅判定是否同步，不判定翻译质量） | ❌ | ❌ | ❌ | ❌ |
| `CONTRIBUTING.md` / onboarding doc | ✅ verdict + evidence | ❌ | ❌ | ❌ | ❌ |
| `docs/adr/NNNN-...md` 状态翻转（proposed → accepted） | ❌ | ✅ 同步（既有合同） | ❌ | ❌ | ❌ |
| `CHANGELOG.md` 写入 vX.Y.Z 入口 | ❌ | ✅ 同步（既有合同） | ❌ | ❌ | ❌ |
| `docs/architecture.md` 或 `docs/arc42/` 架构概述 | ❌ | ✅ 同步（既有合同） | ❌ | ❌ | ❌ |
| `docs/runbooks/` / `docs/slo/` / `docs/diagrams/` / `docs/release-notes/` | ❌ | ✅ 同步（按存在） | ❌ | ❌ | ❌ |
| `docs/insights/` / `docs/experiments/` / discovery / spec / design / tasks / progress / closeout pack | ❌ | ❌（feature 内工件，不是长期资产） | ⚠ 范围变更时同步 | ❌ | ✅ 反查 spec ↔ design ↔ tasks ↔ code ↔ tests 追溯 |
| spec / design / tasks 内**单条需求的 traceability 链是否完整** | ❌ | ❌ | ❌ | ❌ | ✅（既有合同） |
| 单条需求的功能正确性、测试覆盖、设计 conformance | ❌ | ❌ | ❌ | ✅（既有合同） | ❌ |
| "代码已实现新行为，但文档仍是旧结论" 心态 Red Flag（不强制 verdict） | ❌（本 gate 是 verdict + fresh evidence，不只是心态） | ❌ | ✅（既有 prose Red Flag，作为本 gate 的诊断辅助） | ❌ | ❌ |
| 范围变更（需求 / 验收 / 约束变化）触发的工件失效判断 | ❌ | ❌ | ✅（既有合同） | ❌ | ❌ |

**与 `hf-completion-gate` 的关系**：本 gate 的 verdict 是 `hf-completion-gate` evidence bundle 的**一项输入**，不是 `hf-completion-gate` 本身。`hf-completion-gate` 仍然负责"task / feature 是否真的可以宣告完成"的最终判断；本 gate 只回答"对外可见文档是否同步"这一窄问题。

**reviewer 判定边界条目歧义的解决**：若 reviewer 在评审本 spec 时发现上表任一条目存在歧义（例如某文档载体可能同时落到两个 ✅），必须给出 [important][LLM-FIXABLE][U2] finding；spec 必须回到 `hf-specify` 修订，不允许通过。HYP-002 关闭条件 = 本表通过 `hf-spec-review` 时无 U2 finding。

### 6.3 显式不在本轮范围

承接 discovery §4 / §7。

- 不替代 `hf-finalize` 自身的 release notes / CHANGELOG / 顶层导航 / ADR 状态翻转同步
- 不引入 docstring 自动生成 / API doc 自动生成工具链
- 不引入 i18n 自动翻译；只确认副本是否按规则同步
- 不覆盖运维 runbook / SLO 文档（这些有 Phase 3 节点）
- 不覆盖产品 marketing 站点 / 外部 docs 站的 CI 部署
- 不引入新工具链；可选工具（Vale / markdownlint / docs site CI）作为项目级证据来源由 `AGENTS.md` 声明

## 7. 范围外内容

| 项 | 处置 |
|---|---|
| 自建文档生成器、自动翻译、产品 marketing 站点 CI | 永久 out of scope（不在 HF 边界内）|
| 把 README / docstring 的 lint / spell-check 写进 gate | 永久 out of scope（应由项目工具链处理，非 HF 判断职责）|
| Solution A2（扩 `hf-finalize` 同步范围 + 把合同加到 `task closeout`） | *Considered Alternative*（已被 HYP-001 probe 5 / 5 维度证伪），列入 `Considered Alternatives` 段保留历史记录 |
| Solution A3（在 `hf-code-review` / `hf-traceability-review` 内嵌 docs drift checklist） | *Considered Alternative*（已被 HYP-001 probe 证伪），同上 |
| 多语言副本翻译质量打分 | 当前轮仅判定"是否同步"，不判定"翻译是否好" |
| 产品文档外部站点构建 / 部署 | 由项目 CI 承担，本 gate 只检查 source 是否更新 |

### Considered Alternatives（HYP-001 probe 已驳回）

- **A2 扩 `hf-finalize` + 合同加到 `task closeout`**：违反"author / gate / reviewer 角色分离"纪律，破坏 `task closeout` 既有"轻量"合同形状，破坏 `lightweight` profile 承诺。详见 `docs/experiments/2026-04-23-hf-doc-freshness-gate-hyp-001/artifacts/desk-research-evidence.md` E1 / E4 / E5。
- **A3 嵌入 review**：违反 Fagan / HF "review 节点不替 gate 下结论"纪律。详见同 evidence E1 / E3。

## 8. 功能需求

### FR-001 输入：consume user-visible behavior change list

- 优先级: Must
- 来源: discovery §4 wedge；HYP-001 probe Pass
- 需求陈述: 当父会话进入 `hf-doc-freshness-gate` 时，系统必须从以下来源 consume 本任务 / 本 feature 的 user-visible behavior change list：
  1. `features/<active>/spec.md` 中本任务关联的 FR / NFR 条目（按 ID 匹配）
  2. `features/<active>/tasks.md` 中本任务的 Acceptance
  3. （若使用）Conventional Commits 中的 `feat:` / `fix:` / `docs:` / `BREAKING CHANGE:` 条目
- 验收标准:
  - Given 本任务 / 本 feature 已经过 `hf-traceability-review`，When 父会话进入本 gate，Then gate 必须显式列出 user-visible behavior change list（条目数 ≥ 0）+ 来源 file:line 引用。
  - Given 上述 3 项来源全部缺失，When 父会话进入本 gate，Then gate 必须 verdict = `blocked`，next action = `hf-traceability-review`（缺前置证据）。

### FR-002 输出：verdict + fresh evidence

- 优先级: Must
- 来源: discovery §7 C1 candidate；HYP-001 probe Pass
- 需求陈述: 系统必须输出四值 verdict 之一（`pass` / `partial` / `N/A` / `blocked`），并把 verdict + 维度判定明细写入 fresh evidence 文件。
- 验收标准:
  - Given gate 已 consume FR-001 输入，When gate 完成判定，Then 系统必须输出 verdict ∈ {`pass`, `partial`, `N/A`, `blocked`}，且 verdict 来自 §6.2 责任矩阵中本 gate 负责的维度逐项判定（每条 ✅ 行的判定结果必须显式列出）。
  - Given gate 输出 verdict，When 父会话需要消费证据，Then 系统必须把 verdict + 维度判定明细写入 `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`，且若产生 diff 类证据则一并写入 `features/<active>/evidence/doc-freshness-diff-*.log`。

### FR-003 sync-on-presence 容错

- 优先级: Must
- 来源: `docs/principles/sdd-artifact-layout.md` 既有原则；discovery §6 F2；HYP-001 probe E4
- 需求陈述: 在 §6.2 责任矩阵本 gate 负责的维度中，若某文档载体在当前项目尚未启用（例如项目无 monorepo 子包 README、无 OpenAPI），系统必须把该维度判定为 `N/A` 而非 `blocked`。
- 验收标准:
  - Given 项目目录中不存在某文档载体，When gate 判定该维度，Then verdict 必须为 `N/A`，且 evidence 中显式标注"项目当前未启用此资产"。
  - Given 项目存在某文档载体，When gate 判定该维度但本任务未触发对该载体的同步需求（user-visible behavior change list 与该载体无关），Then verdict 必须为 `N/A`，且 evidence 中显式标注"本 task / feature 未触发该资产变化"。

### FR-004 profile 分级

- 优先级: Must
- 来源: `docs/principles/methodology-coherence.md` Profile-Aware Rigor；discovery §6 U1 / HYP-004
- 需求陈述: 在启用不同 `Workflow Profile` 时，系统必须按下表激活不同的强制判定维度：

| Profile | 强制判定维度 | 可选判定维度 |
|---|---|---|
| `lightweight` | 仓库根 `README.md` 产品介绍段 + Conventional Commits `docs:` 标记自检 | 其他 ✅ 行 |
| `standard` | 仓库根 README + 公共 API docstring / OpenAPI + 已存在的 i18n 副本 + `CONTRIBUTING.md` | 模块层 README、外部 docs 站 |
| `full` | §6.2 责任矩阵中本 gate 全部 ✅ 行 | — |

- 验收标准:
  - Given `Workflow Profile = lightweight`，When gate 完成判定，Then evidence 必须只覆盖上表 lightweight 行的强制维度，且整轮判定可在 ≤ 5 分钟人工耗时内完成（HYP-004 dry run 由 design 阶段验证）。
  - Given `Workflow Profile = full`，When gate 完成判定，Then evidence 必须覆盖 §6.2 全部 ✅ 行；任一漏判 = `blocked`。

### FR-005 与 `hf-completion-gate` 的衔接

- 优先级: Must
- 来源: §6.2 责任矩阵；discovery §7 C1 候选
- 需求陈述: 当本 gate 输出 verdict 后，系统必须把 verdict 路径作为 `hf-completion-gate` evidence bundle 的一项输入；`hf-completion-gate` 才能消费该 verdict 决定 task / feature 是否可以宣告完成。
- 验收标准:
  - Given 本 gate verdict = `pass` 或 `N/A`，When 父会话进入 `hf-completion-gate`，Then completion gate 必须能在 evidence bundle 中找到本 gate 的 verdict 文件路径。
  - Given 本 gate verdict = `partial` 且 partial 项不阻塞 closeout，When 父会话进入 `hf-completion-gate`，Then completion gate 在 evidence bundle 中显式记录 `partial` + 未同步项清单，且 closeout 可继续进入 `hf-finalize`。
  - Given 本 gate verdict = `blocked`，When 父会话进入 `hf-completion-gate`，Then completion gate 必须 verdict = `blocked`，next action 回到 `hf-test-driven-dev`（补文档变更）或父会话（人工补文档），不进入 `hf-finalize`。

### FR-006 与 `hf-finalize` 的不重叠

- 优先级: Must
- 来源: §6.2 责任矩阵；HYP-002 (U2) Blocking 关闭依据
- 需求陈述: 系统必须**不**承担 `hf-finalize` 既有合同覆盖的同步动作（ADR 状态翻转、`CHANGELOG.md` 写入、顶层导航行更新、`docs/architecture.md` / `docs/arc42/` / `docs/runbooks/` / `docs/slo/` / `docs/release-notes/` / `docs/diagrams/` 同步）；`hf-finalize` 也**不**承担本 gate 负责的维度（§6.2 ✅ 行）。
- 验收标准:
  - Given 本 gate 完成判定，When 父会话进入 `hf-finalize`，Then `hf-finalize` 不得为 §6.2 本 gate ✅ 行的维度增加同步动作；其 *Release / Docs Sync* 段只覆盖既有合同维度。
  - Given `hf-finalize` 完成 closeout，When reviewer 检查 closeout pack，Then closeout pack 必须 reference 本 gate verdict（作为 evidence 之一），但不得复述本 gate 的判定明细。

### FR-007 与 `hf-increment` 的不重叠

- 优先级: Must
- 来源: §6.2 责任矩阵；HYP-002 (U2) Blocking 关闭依据
- 需求陈述: 系统必须**不**承担 `hf-increment` 的范围变更分析与工件失效判断；`hf-increment` 现有"代码已按新逻辑实现，但文档仍是旧结论"Red Flag 仍保留，但不构成 fresh evidence；本 gate 仍按 FR-002 给出独立 verdict。
- 验收标准:
  - Given 本任务发生范围变更，When 父会话先经 `hf-increment` 完成影响分析，Then 本 gate 仍独立判定对外可见文档同步状态，verdict 不依赖 `hf-increment` 的结论。
  - Given 父会话跳过 `hf-increment` 直接进入本 gate，When gate 检测到 user-visible behavior change list 与已批准 spec 中的 FR / NFR 实质不一致，Then verdict = `blocked`，next action = `hf-increment`（先做范围变更分析）。

### FR-008 reviewer dispatch protocol

- 优先级: Must
- 来源: `docs/principles/methodology-coherence.md` Author/Reviewer 分离；discovery §7 C1
- 需求陈述: 本 gate 必须由独立 reviewer subagent 执行（readonly），不得由父会话或实现节点（`hf-test-driven-dev`）自评。
- 验收标准:
  - Given 父会话进入本 gate，When 触发 gate 判定，Then 父会话必须按既有 reviewer dispatch protocol 派发独立 reviewer subagent，subagent 必须以 readonly 模式执行。
  - Given reviewer subagent 返回 verdict，When 父会话消费 verdict，Then 父会话不得修改 verdict，只能按 verdict 决定下一步路由。

## 9. 非功能需求 (ISO 25010 + Quality Attribute Scenarios)

### NFR-001 verdict 一致性（Functional Suitability / Correctness）

- 类别: Functional Suitability / Correctness
- 优先级: Must
- 来源: HYP-002 (U2) Blocking 关闭依据；FR-002 / FR-003 / FR-004

QAS:
- Stimulus Source: 同一份 user-visible behavior change list + 同一份 §6.2 责任矩阵
- Stimulus: 两次独立 reviewer subagent 派发对同一 task 执行 gate 判定
- Environment: 同一 feature / 同一 commit / 同一 profile / 同一 evidence inputs
- Response: 两次 verdict 与维度判定明细一致（允许 evidence 文件名 timestamp 不同，但 verdict 词与维度判定结果必须一致）
- Response Measure: 抽样 ≥ 5 次相同输入下，verdict 一致率 = 100%；任一不一致 = `blocked`

Acceptance:
- Given 同一 task 与同一输入，When 派发两次独立 reviewer subagent，Then 两次返回的 `verdict` 字段 + `dimension breakdown` 必须完全一致。

### NFR-002 lightweight profile 性能预算（Performance Efficiency / Time behavior）

- 类别: Performance Efficiency / Time behavior
- 优先级: Must
- 来源: discovery §6 U1 / HYP-004；FR-004

QAS:
- Stimulus Source: 父会话（在 `lightweight` profile 项目中）
- Stimulus: 派发 reviewer subagent 执行 gate 判定（lightweight 强制维度仅 2 项）
- Environment: 项目处于典型 `lightweight` 体量（例如单仓库、≤ 10 个 feature 目录、`docs/` 档 0 起步）
- Response: reviewer 完成 verdict 输出
- Response Measure: 单次执行 ≤ 5 分钟人工耗时（HYP-004 dry run by design 阶段验证）；evidence 文档 ≤ 30 行

Acceptance:
- Given lightweight profile 项目，When 派发 reviewer 执行 gate，Then 完成时间 ≤ 5 分钟，且 evidence 文档总行数 ≤ 30。

### NFR-003 不依赖外部工具链（Maintainability / Modularity）

- 类别: Maintainability / Modularity
- 优先级: Must
- 来源: `docs/principles/sdd-artifact-layout.md` *Discipline Without Schema / CI*；discovery §6 F1

QAS:
- Stimulus Source: 接入 HF 的项目（无论 CI 工具链如何）
- Stimulus: 启用本 gate
- Environment: 项目可能 / 可能不具备 Vale / markdownlint / OpenAPI lint / docs site CI
- Response: gate 仍能完成判定并输出 verdict
- Response Measure: gate 不强依赖任何外部工具链；可选工具仅作为 evidence 来源（由 `AGENTS.md` 声明），缺失不构成 `blocked`

Acceptance:
- Given 项目无任何外部 docs 工具链，When 启用本 gate，Then gate 仍能输出 verdict（任一维度可由 reviewer subagent 通过文件 diff + 文档冷读判定）。

### NFR-004 sync-on-presence 容错（Reliability / Fault tolerance）

- 类别: Reliability / Fault tolerance
- 优先级: Must
- 来源: `docs/principles/sdd-artifact-layout.md` 既有原则；FR-003

QAS:
- Stimulus Source: 接入 HF 的项目
- Stimulus: 项目尚未启用 §6.2 责任矩阵中本 gate 负责的某些文档载体
- Environment: 任一 profile
- Response: gate 把对应维度判定为 `N/A`，evidence 显式标注理由
- Response Measure: 未启用文档载体的维度 = `N/A`（≠ `blocked`）；evidence 标注理由不得为空

Acceptance:
- Given 项目无 monorepo 子包（`packages/` 不存在），When gate 判定"模块层 README"维度，Then verdict 该维度 = `N/A`，evidence 标注"项目当前未启用此资产"。

## 10. 外部接口与依赖

| 接口 / 依赖 | 用途 | 兼容口径 / 失效影响 |
|---|---|---|
| `hf-workflow-router` | router 把 gate 节点写入 transition map（design 阶段确定位置） | router FSM 不能因新增节点变得不可恢复；HYP-003 dry run 检查 |
| `hf-completion-gate` | consume 本 gate verdict 作为 evidence bundle 一项 | 必须支持 `partial` verdict 进入 closeout 而非全有全无 |
| `hf-finalize` | reference 本 gate verdict 在 closeout pack；不重叠承担同步动作 | §6.2 责任矩阵硬约束，违反 = spec 不通过 |
| `hf-increment` | 现有 Red Flag 心态保留；本 gate 在范围变更时仍独立判定 | FR-007 不重叠约束 |
| `hf-traceability-review` | 上游已建立 spec ↔ design ↔ tasks ↔ code ↔ tests 追溯 | 本 gate FR-001 依赖该追溯结果定位 user-visible behavior change |
| `AGENTS.md` | 项目级覆盖：可声明额外文档载体路径、可选工具链、profile 默认值 | 优先遵循（与 HF 既有 `AGENTS.md` 约定一致）|

## 11. 约束与兼容性要求

| ID | 约束 | 来源 |
|---|---|---|
| CON-001 | 不得破坏 `hf-finalize` / `hf-completion-gate` / `hf-increment` / `hf-code-review` / `hf-traceability-review` 任何现有合同形状 | HYP-001 probe E1 / E3 / E5；HYP-002 (U2) Blocking |
| CON-002 | 不得引入新工具链；可选工具由 `AGENTS.md` 声明 | NFR-003；discovery §6 F1 |
| CON-003 | 必须遵循 `docs/principles/sdd-artifact-layout.md` 既有 sync-on-presence 原则 | NFR-004；既有项目级原则 |
| CON-004 | 必须遵循 `docs/principles/methodology-coherence.md` 既有 author/gate/reviewer 角色分离纪律 | HYP-001 probe E1；既有项目级原则 |
| CON-005 | 必须支持 `lightweight / standard / full` 三 profile，且 `lightweight` 不得退化为跳过 | FR-004；discovery §6 U1 |
| CON-006 | reviewer subagent 必须以 readonly 模式执行 | FR-008；既有 author/reviewer 分离 |
| CON-007 | evidence 路径必须遵循 `features/<active>/verification/` + `features/<active>/evidence/` 既有约定 | FR-002；`docs/principles/sdd-artifact-layout.md` *Feature 目录内固定文件名* |

## 12. 假设与失效影响

承接 Key Hypotheses 中的非 Blocking 假设 + spec 独有的运行假设。

| 假设 | 失效影响 |
|---|---|
| HYP-003（router FSM 不爆炸）design 阶段 dry run 通过 | 若 dry run 不通过，gate 节点位置需重设计；不影响 spec 本身但延后 design 落地 |
| HYP-004（lightweight ≤ 5 行 checklist + ≤ 5 分钟）design 阶段 dry run 通过 | 若 dry run 不通过，profile 分级表需重设计；可能需要把 lightweight 强制维度从 2 项压到 1 项 |
| 项目使用 Conventional Commits 约定（FR-001 来源 3） | 项目未使用时，FR-001 仍可仅靠来源 1 + 2 完成 consume；evidence 标注"项目未使用 Conventional Commits" |
| reviewer subagent 能稳定按 §6.2 责任矩阵冷读 | 若稳定性不足，需要在 design 阶段通过 reviewer rubric 强化 checklist；NFR-001 一致性测试用以监测 |

## 13. 开放问题

### 阻塞（送评审前必须关闭或降级）

无。

（讨论：本 spec 起草前，唯一 P0 假设 HYP-001 已通过 probe 关闭；剩余 Blocking 假设 HYP-002 (U2) 通过 §6.2 责任矩阵在 spec 内显式落下，由 `hf-spec-review` reviewer 判定关闭——这是 spec 起草自身可承载的封闭路径，不构成开放问题阻塞。）

### 非阻塞（保留至 design / tasks 阶段处理）

- **Q1（非阻塞）**：本 gate 在 router transition map 中的具体位置——位于 `hf-traceability-review` 之后、`hf-regression-gate` / `hf-completion-gate` 之前，还是与三者平行同 tier？倾向：**与 `hf-regression-gate` / `hf-completion-gate` 平行**（同 tier，三者都是"基于不同维度证据的 gate"）。design 阶段最终决定。
- **Q2（非阻塞）**：是否需要为 monorepo 多包项目额外定义"按包 verdict + 父级 verdict aggregate"的规则？倾向：design 阶段考虑；spec 仅声明 §6.2 责任矩阵中"模块层 README"为 ✅ 行。
- **Q3（非阻塞）**：是否在 spec 阶段顺带定义 PR template 中的 "User-Visible Changes" 字段？倾向：与 Phase 1 `hf-release` + Conventional Commits 计划耦合，spec 阶段不定义具体 PR template，由项目 `AGENTS.md` 声明。
- **Q4（非阻塞）**：i18n 副本同步是否有"仅声明，不强制翻译质量"的中间态？倾向：spec §6.2 已明确仅判定"是否同步"不判定"翻译质量"；design 阶段 reviewer rubric 进一步细化判定方法。

## 14. 术语与定义

| 术语 | 定义 |
|---|---|
| **对外可见文档** | 在 §6.2 责任矩阵中本 gate 负责的所有 ✅ 行文档维度的总称 |
| **user-visible behavior change** | 本任务 / 本 feature 引入的、会被 HF 用户（开发者 / 团队 / 后续接手者）通过阅读对外可见文档感知到的行为变化 |
| **verdict** | gate 输出的判定结果，词表 ∈ `{pass, partial, N/A, blocked}` |
| **fresh evidence** | 本 task / feature 当前 session 内产出的 verdict 文件 + 维度判定明细文件 + 可选 diff log，落到 `features/<active>/verification/` + `features/<active>/evidence/` |
| **sync-on-presence** | 同步范围按当前项目实际启用的文档载体决定，未启用的不构成 `blocked`（沿用 `docs/principles/sdd-artifact-layout.md` 既有原则）|
| **责任矩阵** | §6.2 表，规定每个文档维度归属哪个 skill 处理；HYP-002 (U2) 关闭依据 |

下游 `hf-design` 做 DDD 战略建模时，本术语表会进一步长大。

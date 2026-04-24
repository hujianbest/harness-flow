# hf-doc-freshness-gate 产品发现草稿

- 状态: 草稿
- 主题: 在 HF 主链中正式立项一个 `hf-doc-freshness-gate`，用以在每次"完成增量开发"后，确保对外可见文档（README / 模块 README / 公共 API doc / 用户文档站 / i18n 副本等）按用户可见行为变化同步刷新。
- Workflow Profile: standard（HF Phase 0 的 discovery 默认密度；本主题候选方向 ≥ 2，触发 OST 必填，但量化度量数据有限，不强行 RICE 精确化）
- Execution Mode: interactive
- Created: 2026-04-23
- Author: Cursor Cloud Agent (HF self-application)

## 1. 问题陈述

**Struggling moment**：HF 跑完一次「实现 → review → gate → finalize」之后，对外可见文档常常跟不上代码。具体在 HF 当前合同下表现为：

- 仓库根 `README.md` 只被 `hf-finalize` 同步**指针式导航**（active feature / 最近 closeout / ADR 索引行），**产品介绍 / Quick Start / Usage / 能力清单**等"用户阅读用"的段落不会被强制刷新。
- 代码层 / 模块层 README（`src/<module>/README.md`、monorepo 子包 README、`examples/` 入门 README）完全不在 HF 合同里。
- 公共 API 的 docstring / OpenAPI description / 自动文档站点不在任何 review 或 gate 的 fresh-evidence 范围内。
- 多语言副本（如本仓库自己的 `README.md` / `README.zh-CN.md`）没有同步合同。
- `hf-finalize` 的"必须同步"清单只在 **`workflow closeout`** 阶段强制，而 **`task closeout`**（增量任务完成、还有剩余 approved tasks）不强制刷文档；用户感知的"每次完成增量开发"恰好覆盖任务级语义。

**进展被什么阻塞**：开发者 / 团队读完 HF closeout 仍然需要凭直觉判断"哪些对外文档要跟着改"，依赖 `hf-increment` 的 prose-level Red Flag 自检（"代码已经按新逻辑实现，但文档仍是旧结论"），没有 fresh evidence、没有可被冷读的 verdict、没有自动恢复路径。结果是文档随增量漂移、后任接手成本上升、HF 自身的"工件驱动 + fresh evidence"叙事在文档维度断链。

证据来源：

- `skills/hf-finalize/SKILL.md` §4 与 §Verification（同步范围被严格限定）
- `docs/principles/sdd-artifact-layout.md` *Promotion Rules* 表（不含代码层 README / docstring / i18n / 用户文档站）
- `skills/hf-increment/SKILL.md` *Red Flags* §"代码已经按新逻辑实现，但文档仍是旧结论"（仅心态提醒，不是 gate）
- 本仓库自身：存在 `README.md` + `README.zh-CN.md` 两份，但 HF 没有任何 skill 强制两者同步
- 上一轮对话用户原话："hf有没有关注，在每次完成增量开发后，去同步刷新相关的文档，比如README"

## 2. 目标用户与使用情境

| Job Performer | 触发情境 | Job 所在层 |
|---|---|---|
| HF 用户（采用 HF 的开发者 / 团队） | 一个增量任务（task closeout）或一个 feature（workflow closeout）刚完成实现 + reviews + gates，准备进入 closeout / 准备发布 | 主要 |
| 后续接手者 / 新成员 / agent | 阅读仓库根 README、模块 README、API doc 试图理解"系统现在是什么样" | 受益方 |
| HF 自身演进 | 把"工件驱动 + fresh evidence"原则一致延伸到文档维度 | 受益方 |

注意：本主题不针对终端用户产品 marketing 文档，也不针对运维 runbook（已由档 2 `docs/runbooks/` 与 Phase 3 `hf-runbook` 承接）。

## 3. Why now / 当前价值判断

- 上轮对话已经显式识别 GAP（见上一轮回答的 GAP 1 / GAP 2 / GAP 3 / GAP 4 / GAP 5 / GAP 6 / GAP 7），证据已经聚拢；不立项就等于把这些 GAP 留作隐性 backlog，下一次"为什么文档过期了"会反复被问到。
- HF Phase 0 已落地（产品洞察 + 架构设计两层做厚），主链稳定，正适合在不破坏底座的前提下追加一个 gate 节点。
- Phase 1 规划里已经规划了 `hf-release` 与 Conventional Commits 规范化（最小发布闭环），与"用户可见变更必须有对应文档变更"的诉求天然耦合；现在立项 `hf-doc-freshness-gate` 可以与 Phase 1 同节奏，避免 Phase 1 上线后再回头补。
- 切换型力量分析（push / pull / anxiety / habit）：
  - **Push of the situation**：现状下 README 漂移完全靠人工自觉；HF 的 fresh evidence 纪律在文档维度形成"断层叙事"，用户每用一次就感受一次。
  - **Pull of the new gate**：把"文档漂移"从"心态提醒"升级为"带 fresh evidence 的 gate verdict"，与 `hf-regression-gate` / `hf-completion-gate` 体感一致。
  - **Anxiety**：会不会 gate 过载？会不会让 lightweight profile 变重？会不会强迫小项目维护它根本不需要的多语言副本？这些都需要在 spec 阶段用 profile 分级 + sync-on-presence 化解。
  - **Habit of the present**：当前用户已经习惯"finalize 时 review 一遍 README"；新 gate 必须保留"对未启用资产标 N/A"的能力，不破坏既有节奏。

结论：**why now 成立**。

## 4. 当前轮 wedge / 最小机会点

> **Wedge**：在 HF 主链上引入一个**独立的 `hf-doc-freshness-gate` 节点**，把"用户可见行为变化必须对应可冷读的文档同步证据"从隐性 self-check 升级为带 verdict 的 gate；以 **sync-on-presence + profile 分级 + 与 `hf-completion-gate` / `hf-finalize` 显式分工** 三条纪律保证它**不退化为模板填空**、**不让 lightweight 变重**、**不抢 finalize 的同步动作**。

明确不在当前轮 wedge 内：

- 不替代 `hf-finalize` 自身的 release notes / CHANGELOG / 顶层导航 / ADR 状态翻转同步
- 不引入 docstring 自动生成 / API doc 自动生成工具链
- 不引入 i18n 自动翻译；只确认副本是否按规则同步
- 不覆盖运维 runbook / SLO 文档（这些有 Phase 3 节点）
- 不覆盖产品 marketing 站点 / 外部 docs 站的 CI 部署（只覆盖"评审是否需要刷新"）

## 5. 已确认事实

| 事实 | 证据 |
|---|---|
| `hf-finalize` 必须同步项不含"仓库根 README 的产品介绍段" | `skills/hf-finalize/SKILL.md` §4 |
| `hf-finalize` 必须同步项不含代码层 / 模块层 README | `docs/principles/sdd-artifact-layout.md` *Promotion Rules* 表 |
| 当前 `hf-finalize` 合同下，没有针对**仓库根 `README.md` 产品介绍段 / 模块 README / 公共 API doc** 的强制同步条款；同步合同覆盖的是 ADR 状态翻转 / `CHANGELOG.md` / 顶层导航行 / 已存在的长期资产载体（`docs/architecture.md` 或 `docs/arc42/` / `docs/runbooks/` / `docs/slo/` / `docs/release-notes/` / `docs/diagrams/`），且这些项的强制性自然落在版本/发布语义出现的时机（即 `workflow closeout`），`task closeout` 路径下不存在等价合同 | `skills/hf-finalize/SKILL.md` §4 *必须同步项 + 按存在同步项* + §Verification + `docs/principles/sdd-artifact-layout.md` *Promotion Rules* |
| `hf-increment` 的"文档仍是旧结论"是 Red Flag，但不是 gate | `skills/hf-increment/SKILL.md` *Red Flags* |
| HF 已有的 gate 节点都遵循 `Hard Gates + Verification + fresh evidence` 三段合同（`hf-regression-gate` / `hf-completion-gate`） | 两 skill 的 `SKILL.md` |
| HF 已有 sync-on-presence 原则可复用 | `docs/principles/sdd-artifact-layout.md` *按存在同步* / *未启用资产不构成 blocked* |
| HF 已有 profile 分级（`full / standard / lightweight`） | `skills/docs/hf-workflow-shared-conventions.md` |
| HF 主链上 gate 节点位置位于 review 之后 / closeout 之前 | `README.zh-CN.md` *工作流形状* |
| 本仓库自身存在 `README.md` + `README.zh-CN.md`，且没有同步合同 | `ls /workspace` |

## 6. 关键假设与风险

按 Desirability / Viability / Feasibility / Usability 分类。

### Desirability（用户真的想要吗）

- **A1**：HF 用户**普遍**希望"每次完成增量开发后" README / 公共文档自动被纳入 fresh-evidence 验证，而不是只想要"workflow closeout 时刷一下"。
  - 不成立则 wedge 站不住：可能用户只想扩 `hf-finalize` 的同步范围，而不需要新 gate。
  - **Confidence: medium**。证据：当前对话的用户原话明确点名"每次完成增量开发"，指向任务级；但样本量 = 1。
  - Probe 建议：在 `hf-experiment` 中做一次最小 probe——把候选 spec 草稿同时呈现两个方案（"扩 finalize" vs "新 gate"），观察 1–2 个真实 HF 项目的偏好（最小可接受 N=2）。

### Viability（对 HF / 业务有价值吗）

- **A2**：把文档漂移从隐性 backlog 升级为显式 gate，对 HF 的"差异化叙事"有正向价值（强化"fresh evidence 一致延伸到文档维度"）。
  - **Confidence: high**。与 `docs/todo/hf-evolution-gap-analysis.md` §H 的"知识沉淀维度单一"演进方向一致。

- **A3**：新增节点不会让 router FSM 复杂度爆炸。
  - **Confidence: medium-high**。HF 已有 `hf-regression-gate` / `hf-completion-gate` 作为相邻 gate 模板，新增同类节点的 transition 增量有限；但仍需在 design 阶段更新 `hf-workflow-router/references/profile-node-and-transition-map.md` 验证。

### Feasibility（技术上做得到吗）

- **F1**：`hf-doc-freshness-gate` 可以**纯纪律化**实现（prose checklist + verdict + 证据落盘），无需引入新工具链；可选工具（如 Vale / markdownlint / docs site CI）作为项目级证据来源由 `AGENTS.md` 声明。
  - **Confidence: high**。与 `docs/principles/sdd-artifact-layout.md` *Discipline Without Schema / CI* 一致。

- **F2**：可以复用 sync-on-presence 原则——代码层 README 不存在就标 `N/A`，不强制创建。
  - **Confidence: high**。已有先例。

### Usability（用户能用得起来吗）

- **U1**：在 `lightweight` profile 下 gate 仍能被压缩到"只检查仓库根 README 是否需要更新 + Conventional Commits 中是否标了 `docs:` 类条目"，不会让小改动体感沉重。
  - **Confidence: medium**。需要在 spec 阶段明确密度分级表，否则有"轻量退化为跳过"的滑坡风险。

- **U2**：用户能稳定区分 `hf-doc-freshness-gate` vs `hf-finalize` vs `hf-increment` 的责任边界，不重叠不抢戏。
  - **Confidence: medium**。这是 spec / design 阶段必须明确解决的语义边界问题，不解决就是 product risk。

### 高风险、低 confidence 的关键假设 → 建议 `hf-experiment`

- **A1**（用户偏好"新 gate" vs "扩 finalize"）confidence 偏低 → 建议在进入 `hf-specify` 之前走 `hf-experiment` 做一次最小 probe（detail 见 §8）。

## 7. 候选方向与排除项

### 候选方向（与 §11 OST 中 Solution 一一对应）

#### Solution C1（**当前轮主候选**）：新增独立 gate `hf-doc-freshness-gate`

- 位置：在 `hf-traceability-review` 之后、`hf-regression-gate` / `hf-completion-gate` 之前（或同 tier 平行）
- 职责：消费本任务 / 本 feature 的 user-visible behavior change list，对每一类对外可见文档（仓库根 README、模块 README、docstring / OpenAPI、i18n 副本、用户文档站、`CONTRIBUTING.md` / onboarding doc）按 sync-on-presence 给出 `pass` / `partial` / `blocked` / `N/A` verdict 与 fresh evidence
- 证据形态：`features/<active>/verification/doc-freshness-YYYY-MM-DD.md` + `features/<active>/evidence/doc-freshness-diff-*.log`
- profile 分级：`full` 强制全表；`standard` 强制 README + 公共 API + 已存在的 i18n 副本；`lightweight` 至少强制仓库根 README + Conventional Commits `docs:` 标记自检

#### Solution C2（备选）：扩 `hf-finalize` 同步范围 + 把同步合同也加到 `task closeout`

- 优点：复用既有节点，FSM 不变
- 缺点：
  - 把"判断是否需要同步"和"实际执行同步"压在同一个 skill 内，违反 HF 的"author / reviewer / gate 角色分离"纪律
  - `task closeout` 也强制走完整同步会让中间任务的 closeout 变重
  - 没有独立 verdict，"文档漂移"无法成为 fresh evidence

#### Solution C3（备选）：在 `hf-code-review` 与 `hf-traceability-review` 中各加一段"文档 drift" checklist

- 优点：实现成本最低
- 缺点：
  - 角色错位（reviewer 不该承担 gate 职责，与 `hf-regression-gate` / `hf-completion-gate` 的既有切分不一致）
  - 没有独立 verdict / evidence path
  - 不解决"`task closeout` 时 README 不被强制刷新"的根本问题

#### Solution C4（远期 / 排除）：自建 docstring / API doc 生成工具链 / 自动 i18n 翻译

- 排除理由：超出 HF "skill pack 提供纪律"的边界；属于工具集成层，应由 `AGENTS.md` 声明的项目工具链承接

### 排除项

- 自建文档生成器、自动翻译、产品 marketing 站点 CI ——不在 HF 边界内
- 把 README / docstring 的 lint / spell-check 写进 gate ——这是工具能强制的，不该消耗判断 token

## 8. 建议 probe / 验证优先级

每条关键假设对应一个最小 probe（落盘交由 `hf-experiment` 负责，本草稿只写方向与优先级）：

| 假设 | Probe 方向 | 优先级 | 成功阈值 |
|---|---|---|---|
| **A1** 用户偏好"新 gate" vs "扩 finalize" | 把两个候选 spec outline 同时给 ≥ 2 个真实 HF 项目维护者，让其指出"哪个更能解决我的痛点"+ 1 个理由 | P0（阻塞 spec 立项） | ≥ 2/2 倾向"新 gate"，或反之；若 1/1 split，回到 discovery 加做用户访谈 |
| **A3** router FSM 复杂度可控 | 在 design 阶段做一次 transition map dry run，检查新增 transition 数 ≤ 6 | P1（spec 后 / design 前） | 新增 ≤ 6 条 transition，且无 dead end |
| **U1** lightweight 不退化 | 在 spec / design 内置一份"lightweight 5 行 checklist 样例"，让 1 个真实 lightweight 项目跑一次 dry run | P1（design 阶段） | 跑一次耗时 ≤ 5 分钟，且 verdict 可被冷读 |
| **U2** 责任边界稳定 | 在 spec 中显式列 `hf-doc-freshness-gate` vs `hf-finalize` vs `hf-increment` 的责任矩阵；评审时 reviewer 必须能逐项判 `pass` | P0（spec 阶段） | reviewer 评审无"哪条该哪个 skill 管"歧义 |

P0 假设（**A1** + **U2**）任一不通过，应回到 discovery 修订；不强行进入 spec。

## 9. 成功度量（Desired Outcome / North Star / Success Threshold）

| 字段 | 内容 |
|---|---|
| **Desired Outcome** | 在采用 HF 的项目中，"完成一次增量开发后对外可见文档保持新鲜"成为可被冷读的 gate verdict + fresh evidence，而不是依赖人工自觉。 |
| **North Star 锚定** | 关联到 HF pack 的"工件驱动 + fresh evidence 一致延伸到文档维度"叙事；项目当前**无形式化 North Star 声明**。 |
| **Leading 指标** | 在试点 HF 项目中，每次 task closeout / workflow closeout 都能找到一份 `doc-freshness-YYYY-MM-DD.md` verdict 文档（命中率）。 |
| **Lagging 指标** | 试点项目在引入本 gate 后 N=3 次增量开发结束后，仓库根 README / 模块 README / 公共 API doc 的"用户可见行为漂移条数"由 reviewer 抽样判定下降。 |
| **Success Threshold** | 在 ≥ 2 个真实 HF 项目（含 lightweight 与 standard 各 1）中，连续 3 次增量开发后产生有效 verdict 文档，且没有出现"reviewer 标 pass 但实际 README 漂移"的案例。 |
| **Non-goal Metrics** | 不追求 README 字数变化；不追求 docstring 覆盖率到某个百分比；不追求外部 docs 站点构建时间下降；不追求自动翻译覆盖率。 |

注：以上指标在试点阶段无需平台化采集，由 reviewer subagent 抽样 + closeout pack 引用即可（沿用 HF "Discipline Without Schema / CI" 原则）。

## 10. JTBD 视图（Jobs Story + 四力）

### 主 Jobs Story

```text
When 我刚完成一次 HF 主链下的增量开发（review / gate / regression 已通过，准备 closeout 或发布），
I want to 让 HF 主动告诉我"这次有哪些对外可见的文档需要跟着改、哪些已经按规则同步、哪些还是 N/A"，并把这一判断作为带 fresh evidence 的 verdict 落盘，
so I can 在不依赖个人自觉、不依赖项目额外 lint 工具链的前提下，让仓库根 README / 模块 README / 公共 API doc / i18n 副本与代码行为同步演化。
```

### 四力（切换型主题）

- **Push of the situation**：当前每次 task closeout 都要凭直觉判断"README 要不要改"；HF 自己写得很硬的 fresh-evidence 叙事在文档维度断层。
- **Pull of the new gate**：和 `hf-regression-gate` / `hf-completion-gate` 一致体感的"verdict + evidence"，可被 reviewer 抽样、可被 router 消费、可被 PR diff 看到。
- **Anxiety of the new gate**：怕 gate 过载、怕 lightweight 变重、怕和 `hf-finalize` 抢戏、怕变成"模板填空形式主义"。
- **Habit of the present**：当前用户依赖 `hf-finalize` 一次性同步 + `hf-increment` 心态自检；新 gate 必须保留这两条既有路径不被破坏。

## 11. OST Snapshot

```text
Desired Outcome: HF 主链下"完成增量开发后对外可见文档保持新鲜"成为带 fresh evidence 的 gate verdict
                 （试点：≥ 2 个真实项目、3 次连续增量后 README/API doc 无漂移）

Opportunity A（主）：每次完成增量开发后，对外可见文档（README / 模块 README / 公共 API doc / i18n 副本 / 用户文档站）的同步只靠人工自觉，没有 fresh evidence
  Solution A1（主候选 = §7 C1）：新增独立 gate `hf-doc-freshness-gate`
    关键假设（≤ 2 / solution，遵循 opportunity-solution-tree.md 剪枝规则）：
      Assumption A1-D: 用户普遍偏好"新 gate"而不是"扩 finalize"（confidence: medium → P0 probe，hf-experiment）
      Assumption A1-U: lightweight 仍能压到 5 行 checklist（confidence: medium → P1 dry run）
    次要假设（design 阶段 dry-run 处理，不进入 P0 probe）：
      Assumption A1-V: 新增节点不会让 router FSM 复杂度爆炸（confidence: medium-high → design 阶段 transition map dry run）
    Probe：见 §8 表
  Solution A2（备选 = §7 C2）：扩 `hf-finalize` 同步范围 + 把合同加到 `task closeout`
    Assumption A2-D: 用户能接受 `task closeout` 变重（confidence: low）
    Probe：在同一份 A1 probe 中作为对照
  Solution A3（备选 = §7 C3）：在 `hf-code-review` / `hf-traceability-review` 内嵌 docs drift checklist
    Assumption A3-V: reviewer 角色可以同时承担 gate 职责而不破坏既有切分（confidence: low；与 HF "Fagan 角色分离"明显冲突）
    剪枝倾向：高

Opportunity B（次，本轮不做）：HF 知识沉淀维度单一（仅 hf-bug-patterns），缺统一 onboarding curation
  剪枝理由：与本 wedge 不同层；已在 `docs/todo/hf-evolution-gap-analysis.md` §H 与 Phase 5 候选块 9 单独承接
```

候选 Opportunity 数量说明：本轮 OST 客观上仅枚举到 2 条 Opportunity（A 主 / B 不做），未达 `opportunity-solution-tree.md` 推荐的 3–5 条规模规则。原因：本主题锚定的是 HF 现行合同上**一个具体的同步断点**（task / 增量级文档刷新缺合同），而不是开放探索式发现，候选机会面客观受限。已显式排查过其他可能的 Opportunity 位置：

- 长期资产（架构概述 / runbook / SLO / ADR）→ 已被 `hf-finalize` 现行合同覆盖
- 任务进度 / progress 文档 → 已被 `features/<active>/progress.md` + `hf-workflow-router` 覆盖
- bug 模式知识沉淀 → 已被 `hf-bug-patterns` + Phase 5 候选块 9 覆盖

如出现新 Opportunity，应回到 discovery 修订而不是绕过本次评审结论。

剪枝原则：

- A3 的角色错位与 HF 既有 Fagan 风格分离纪律明显冲突 → 剪枝倾向高
- A2 的"`task closeout` 变重"与"author/gate 分离"违反两条 HF 纪律 → 倾向作为对照而非主候选
- 主候选锁定 A1（C1）

## 12. Bridge to Spec

推荐带入 `hf-specify` 的范围边界：

- 起草 `features/<NNN>-hf-doc-freshness-gate/spec.md`，主题为「在 HF 主链上引入独立的 `hf-doc-freshness-gate` 节点」。
- 该 spec 的 Success Criteria / Success Metrics 直接采用本 §9 的 Desired Outcome / Success Threshold（不重新发明）。
- spec 必须显式包含以下功能 / 非功能维度（六分类）：
  - **Functional**: 输入（user-visible behavior change list 来源、对外可见文档清单）、输出（verdict + evidence path）、verdict 词表（`pass` / `partial` / `blocked` / `N/A`）、profile 分级表（`full` / `standard` / `lightweight`）、与 `hf-completion-gate` / `hf-finalize` / `hf-increment` 的责任矩阵、与 `hf-workflow-router` 的 transition 接入位置
  - **NFR**:
    - sync-on-presence 容错（未启用文档载体不构成 blocked）
    - lightweight profile 性能预算（5 行 checklist、≤ 5 分钟人工耗时）
    - "不依赖外部工具链"约束（可选工具由 `AGENTS.md` 声明）
  - **Constraints**: 不替代 `hf-finalize` 的 release notes / CHANGELOG / 顶层导航 / ADR 状态翻转；不引入新工具链；不破坏既有 task closeout 节奏
  - **Assumptions**: A1 / A3 / U1 / U2 在 §6 列出
  - **Out of Scope**: 自建文档生成器、自动翻译、产品 marketing 站点 CI、运维 runbook（由 Phase 3 节点承接）
  - **Open Questions**: §13

可直接转成规格输入的稳定结论：

- wedge = 新 gate（A1 / C1），不是扩 finalize（A2 / C2），不是嵌入 review（A3 / C3）
- 沿用 HF 三段合同（`Hard Gates + Verification + fresh evidence`）
- 沿用 sync-on-presence 与 profile 分级两条既有纪律
- evidence 路径：`features/<active>/verification/doc-freshness-YYYY-MM-DD.md` + `features/<active>/evidence/doc-freshness-diff-*.log`

需要继续保留为 assumption 的内容（建议走 `hf-experiment` 先验证）：

- **A1**（用户偏好新 gate 而非扩 finalize）—— P0 probe，结果回流后再正式通过 `hf-spec-review`
- **U2**（责任边界稳定）—— spec 阶段必须显式给出责任矩阵供 reviewer 判定

当前不进入 spec 的候选项：

- A2 / C2（扩 finalize）—— 只作为 spec 中的"Considered Alternative"段保留，不进入主路径
- A3 / C3（嵌入 review）—— 同上
- 自建工具链 / 自动翻译 / 外部 docs 站 CI —— 完全 out of scope

已锁定的 Desired Outcome / Success Threshold 见 §9。

## 13. 开放问题

### 阻塞（送评审前必须关闭或降级）

- **Q1（阻塞）**：本草稿样本量 = 1（来自一次对话），是否需要在评审前补一次最小用户访谈以提升 A1 confidence？（建议：让 `hf-discovery-review` 给出 verdict；若 reviewer 判 `request-changes`，回 `hf-experiment` 跑 P0 probe 再回评审）
- **Q2（阻塞）**：本 gate 的位置是位于 `hf-traceability-review` 之后、`hf-regression-gate` 之前，还是与 `hf-regression-gate` / `hf-completion-gate` 平行？（design 阶段必须给出最终选择，不在 discovery 阶段强行收敛）
  - 当前倾向：与 `hf-regression-gate` / `hf-completion-gate` **平行**（同 tier，三者都是"基于不同维度证据的 gate"）。

### 非阻塞

- **Q3（非阻塞）**：是否需要为 monorepo 多包项目额外定义"按包 verdict + 父级 verdict aggregate"的规则？（spec 阶段考虑；不阻塞当前 wedge）
- **Q4（非阻塞）**：是否在 spec 阶段顺带定义 PR template 中的 "User-Visible Changes" 字段？（与 Phase 1 的 `hf-release` + Conventional Commits 计划耦合，可在 spec 阶段做一次性约定）
- **Q5（非阻塞）**：i18n 副本同步是否有"仅声明，不强制翻译质量"的中间态？（spec / design 内表述）

## 14. Workflow 自检（hf-product-discovery 步骤 7）

- [x] discovery 不是功能清单堆砌（围绕 problem framing + JTBD + OST 收敛）
- [x] 已区分事实（§5）/ 假设（§6）/ later ideas（§11 Opportunity B、§7 排除项）
- [x] 已明确当前轮 wedge（§4）= OST 主 opportunity A 的主 solution A1
- [x] 至少一条合格 Jobs Story（§10，情境驱动、可观察 outcome）
- [x] 候选方向 ≥ 2 时 OST Snapshot 存在且剪枝理由已写（§11）
- [x] Desired Outcome + Success Threshold 已显式落下（§9），不是"体验更好"口号
- [x] 未把 spec / design 细节提前写进正文（§7 候选只到 wedge 粒度，未写实现细节）
- [x] 已明确 `Bridge to Spec` 中哪些结论可进入 `hf-specify`（§12）
- [x] 高风险、低 confidence 关键假设已标注"建议走 `hf-experiment` 先验证"（§6 / §8 / §12）

## 15. Handoff

- **Current Stage**: `hf-product-discovery`
- **Next Action Or Recommended Skill**: `hf-discovery-review`
- **Workspace Isolation**: in-place（discovery 阶段无代码改动）
- **Worktree Path**: N/A
- **Worktree Branch**: `cursor/discovery-doc-freshness-gate-d0e2`
- **建议 review 重点**:
  1. A1 的 confidence 是否需要在通过评审前先跑 `hf-experiment`（Q1）
  2. wedge（新 gate vs 扩 finalize vs 嵌 review）是否合理收敛
  3. §6 / §11 中假设分层是否完整
  4. §12 Bridge to Spec 是否足以让 `hf-specify` 起草 `features/<NNN>-hf-doc-freshness-gate/spec.md`
- **若评审通过**: 由 `hf-specify` 创建 `features/<NNN>-hf-doc-freshness-gate/`（feature 目录在 spec 阶段创建，遵循 `docs/principles/sdd-artifact-layout.md`）。**前置条件钉死**：`hf-spec-review` 通过前，必须先关闭 §6 A1（用户偏好新 gate vs 扩 finalize，medium confidence）与 §6 U2（责任边界稳定）两条 P0 假设；前者通过 `hf-experiment` probe 关闭（见 §8），后者通过 spec 内显式责任矩阵 + reviewer 判定关闭。任一未关闭，spec 不允许进入 `hf-spec-review`（与 `hf-specify` Hard Gates "Blocking 假设未验证前不得通过评审" 一致）。
- **若评审 request-changes 且 P0 probe 必要**: 走 `hf-experiment` 跑 §8 中 A1 probe，结果回流到本草稿后重审

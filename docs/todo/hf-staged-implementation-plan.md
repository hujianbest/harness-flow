# HF 分阶段实施计划：Demo → 市场验证 → 商用交付

## Purpose

本文把 `docs/todo/hf-evolution-gap-analysis.md` 中识别出的缺口（候选块 1–9）转译成一条**分阶段、可独立收尾**的实施路径，回答两个问题：

1. HF 应该按什么顺序补齐能力，才能先做出一个**足以验证市场**的 demo 级产品，再逐步走向**商用交付**水平
2. 如何让 HF 的核心差异化，优先体现在**产品洞察分析**与**架构设计**这两个高价值环节上，以便产品后续演进能持续受益

本文不新增 skill、不修改 pack 结构，只给出阶段骨架、退出条件和与 gap analysis 的对应关系。具体每个阶段内的任一候选块真正立项时，仍应走 HF 自己的主链（`hf-product-discovery` → `hf-specify` → `hf-design` → `hf-tasks` → ...）。

## 指导原则

在排阶段顺序时，始终按下面三条指导原则判断：

1. **Discovery-Architecture First**：HF 的差异化先押在「产品洞察分析」和「架构设计」两个上游环节做到行业级水平，因为这两层做厚之后，所有下游（实现、发布、运维、度量）都能吃到红利；反过来则不成立。
2. **Demo → 市场验证 → 商用**：每一阶段都必须能独立收尾、独立对外讲故事。Demo 阶段不追求「全链路覆盖」，只追求「在关键环节上比现有 AI workflow 明显更强」；商用阶段才追求完备。
3. **不让缺口阻塞主线**：缺的能力如果不在主线价值叙事上（例如深度 FinOps、chaos engineering），应被推迟到靠后的阶段，而不是为了「看起来完整」去提前做。

## 阶段总览

| 阶段 | 目标 | 核心能力输出 | 能对外讲什么 | 对应 gap analysis 候选块 |
|---|---|---|---|---|
| **Phase 0** | HF 在**产品洞察**与**架构设计**两层做到 demo 可见的高水平 | 强化的 discovery + 战略建模 + 结构化 NFR | 「HF 不是又一个 coding agent；它能把一个模糊 idea 拆到可架构落地的深度」 | 候选块 1（部分） + 候选块 2（部分） |
| **Phase 1** | demo 能在真实小团队跑通端到端、可做小规模市场验证 | 可观测性-by-design、隐私/合规最小检查、基础 release、基础 retro & 度量回流 | 「HF 跑通的是从 idea 到上线到学习一整圈，不止代码合入」 | 候选块 2（补齐）、候选块 4（最小版）、候选块 5（最小版）、候选块 6（最小版） |
| **Phase 2** | 把质量工程分支撑起来，进入准商用水平 | 独立 threat model / compliance / security / perf / a11y / contract gate | 「HF 的非功能质量有独立门禁，不靠心理安慰通过」 | 候选块 2（安全/合规补齐）+ 候选块 3（完整） |
| **Phase 3** | 商用级发布与运维闭环 | progressive delivery、runbook、incident、postmortem、DORA / 产品指标回流、deprecation | 「HF 覆盖发布-运维-学习闭环，可以进入生产严肃交付」 | 候选块 4（完整）+ 候选块 5（完整） |
| **Phase 4** | 团队化与长期架构健康 | 多人协作、tech debt register、dependency lifecycle、周期性架构评审、fitness functions | 「HF 能长期运转、长期保持架构健康，不靠一次性补丁」 | 候选块 6（完整）+ 候选块 7（完整） |
| **Phase 5** | 数据 / AI 产品分支 + 知识沉淀扩维 | `hf-data-*` / `hf-ml-*` / `hf-eval-harness` / `hf-engineering-learnings` | 「HF 能承接 AI-native 产品的节奏，而不是只做传统 CRUD」 | 候选块 8 + 候选块 9 |

阶段之间是**递进关系**，但**不要求严格串行**：Phase 0 一旦满足退出条件就可以对外讲故事，Phase 1 的若干小块可以在 Phase 0 收尾前并行启动，只要不反向阻塞 Phase 0 的核心叙事。

## Phase 0 — Discovery-Architecture Depth Demo

### 为什么先做这个

用户原话：*HF 优先在产品洞察分析和架构设计上具有较高的水平，这样可以支持产品后续演进*。

这和 HF 的天然优势也吻合——HF 已经把**工件驱动、角色分离、人类审批**这些纪律做出来了。把它们叠加到业界成熟的上游方法论（JTBD / OST / DDD / Event Storming / ATAM）上，就能在 demo 阶段直接给出业内 AI agent workflow 很少展示的深度：**从一句模糊 idea 到一份有 bounded context、context map、quality attribute scenarios 的架构骨架**，全程落盘、可评审、可恢复。

### 目标（Success State）

一位 demo 观众输入「我想做 X 产品 / 能力」这样一句话，HF 能在**不动一行实现代码**的前提下，按主链推进到：

- 一份结构化 discovery 草稿，含 JTBD / OST、价值假设、量化优先级、明确假设与 probe
- 一份已批准的 spec 草稿，含结构化 NFR / quality attribute scenarios 与显式 success metrics
- 一份已批准的 design 草稿，含 Bounded Context / Ubiquitous Language / Context Map、C4、ADR 与关键 NFR 架构取舍
- 全链路 discovery → spec → design 有显式 traceability 与真人审批记录

demo 期重点不是「能不能 ship」，而是「能不能把上游产品思考与架构决策做得比人工整理更结构化、更能回读」。

### 核心交付物

**产品洞察（来自候选块 1 的第一批）**

- `hf-product-discovery` 引入 JTBD / Jobs Stories 模板
- `hf-product-discovery` 引入 Opportunity Solution Tree 结构（Teresa Torres）
- `hf-product-discovery` / `hf-specify` 引入 RICE / ICE 作为 MoSCoW 的量化补充
- discovery / spec 模板显式加入 North Star、Success Metrics、Key Hypotheses 字段
- 新 skill（最小版）：`hf-experiment`——至少产出「假设 / 验证方式 / 成功阈值 / 证据归档路径」的结构化 probe plan，不追求 A/B 平台集成

**架构深度（来自候选块 2 的第一批）**

- `hf-design` 上游引入 DDD 战略建模 reference：Bounded Context、Ubiquitous Language、Context Map
- 新 reference：Event Storming 作为 spec → design 的桥梁（不新增节点，先以 reference + 模板出现）
- `hf-specify` / `hf-design` 增加结构化 NFR 章节（ISO 25010 + Quality Attribute Scenarios）
- 模板层面加入轻量 threat model（至少 STRIDE 列表式），作为 design 的 reference 而非独立 gate

**Phase 0 明确不做**

- 发布 / 运维 / observability 的完整契约（留 Phase 1 做最小版）
- 安全 / 合规独立 gate（留 Phase 2）
- 多人协作、code owner、外部工具同步（留 Phase 4）
- 数据 / AI 产品分支（留 Phase 5）

### 退出条件

- 能在一次 demo 会话内，把任意一个中等复杂度产品 idea 推到 `设计真人确认` 之前（含）且有完整可回读工件
- `docs/features/<slug>/` 下同时存在 `spec.md`（含 NFR / quality scenarios / success metrics）、`design.md`（含 DDD 战略 + C4 + ADR + NFR 取舍）
- `docs/insights/<...>-discovery.md` 含 JTBD、OST、量化优先级、假设与 probe plan
- 所有上游真人审批（`规格真人确认` / `设计真人确认`）均有落盘记录
- 与现有 TDD 中段引擎仍向后兼容，不出现主链断裂

### 主要风险

- **过度结构化导致体感沉重**：引入 DDD / OST / JTBD 模板时，必须严格遵守现有 `lightweight / standard / full` profile 的密度分级；lightweight 只保留"最小必要列"。
- **Discovery 与 Spec 边界再次模糊**：`Bridge to Spec` 的既有合同要在引入 JTBD / OST 后继续成立，不能让 discovery 又开始回填功能细节。

## Phase 1 — 可真实跑通的 MVP（小规模市场验证）

### 为什么放在这里

Phase 0 证明的是「HF 能想得深」，Phase 1 要证明「HF 能真的跑完一圈」。没有这一阶段，市场验证会卡在「我们无法把 HF 用到真实项目里——它到 PR 就停了」。

Phase 1 的口径仍是**最小可接受的端到端**，不追求准商用完备度。

### 目标（Success State）

用 HF 在一支小团队里跑完一个真实小任务，从 idea 到灰度上线，并且：

- 观测、release、retro 的最小闭环能贯穿
- 度量数据（deploy freq、lead time 等 DORA 最小子集 + 至少一个产品指标）能回流到下一轮 discovery

### 核心交付物

**架构侧补齐（候选块 2 的剩余关键项）**

- `hf-specify` / `hf-design` 加入 `Observability-by-Design` 章节：至少声明关键 SLO / SLI / logs / metrics / traces / alerts 的最小契约
- `hf-design` 加入 Performance budget reference（不要求独立 gate，只要求设计期声明预算）
- 模板层加入 Privacy by Design checklist，作为 design 的可选段落（还不是独立合规 gate）

**最小发布闭环（候选块 4 的最小版）**

- 新 skill（最小版）：`hf-release`——把 CI/CD 管线与 Conventional Commits、SemVer 约定作为工件规范化，不做 progressive delivery
- `hf-finalize` 扩展：除 release notes / changelog 外，额外写回 deploy freq、lead time 两项 DORA 最小指标

**最小学习闭环（候选块 5 的最小版）**

- 新 skill（最小版）：`hf-retrospective`——周期性 retro，不止一次性 closeout
- 新 skill（最小版）：`hf-product-metrics`——至少支持一个 North Star / HEART 指标定义与回流到下一轮 `hf-product-discovery`

**外部协作最小约定（候选块 6 的最小版）**

- PR template / Conventional Commits 约定
- 与 Jira / Linear / GitHub Issues 的最小 task sync reference（保持 HF 工件为真源）

### 退出条件

- 在一个真实小项目里跑通一次完整循环：`hf-product-discovery` → `hf-finalize` → `hf-retrospective` → 指标回流到下一轮 discovery
- `RELEASE_NOTES.md`、CI 管线、observability 契约、retro 记录、产品指标定义都在 feature 目录下可回读
- 至少一次上线，且上线后 14 天内的指标已经被 `hf-product-metrics` 写回 discovery 输入

### 主要风险

- **诱惑去一把做 progressive delivery / 独立 security gate**：必须克制，这些属于 Phase 2–3；Phase 1 目标只是「能跑完」，不是「跑得漂亮」。
- **外部工具同步过度耦合**：task sync 只提供约定，不提供实现；否则 HF 会陷入每家 PM 工具的适配战争。

## Phase 2 — 质量工程分支撑起（准商用）

### 为什么放在这里

Phase 0–1 已经能讲「HF 想得深、跑得通」。进入 Phase 2 之前，HF 最薄弱的是**非功能质量没有独立门禁**——安全、性能、合规、a11y、contract 现在都散落在各处的 self-check 里。对于想把 HF 用在严肃业务的客户，这是主要阻塞点。

### 目标（Success State）

HF 的「完成」不再是一条 regression + completion 复合判断，而是可以显式声明：**安全、性能、合规、a11y、contract 这几类非功能质量都有独立的 fresh evidence**。

### 核心交付物（候选块 2 安全/合规补齐 + 候选块 3 完整）

- 新 skill：`hf-threat-model`（STRIDE / LINDDUN，落盘 threat list + mitigation mapping）
- 新 skill：`hf-compliance-review`（GDPR / SOC2 / HIPAA / Privacy by Design，作为可按项目配置的 checklist-based gate）
- 新 gate：`hf-security-gate`（SAST / DAST / SCA / 依赖扫描 / SBOM 消费证据）
- 新 gate：`hf-perf-gate`（负载 / 容量 / 延迟预算验证，消费 Phase 1 在 design 阶段声明的 performance budget）
- 新 gate：`hf-a11y-gate`（WCAG 2.2 AA 动态验证，补 `hf-ui-review` 的静态部分）
- 新 gate：`hf-contract-gate`（消费者驱动契约测试）
- `hf-test-driven-dev` test seed 模板扩展 property-based testing 选项（mutation / chaos / exploratory 只作为可选 reference，不强制）

### 退出条件

- 上述 gate 均已进入 `hf-workflow-router` 的 canonical 节点词汇表，并有对应 `Pending Reviews And Gates` 语义
- 至少一个真实项目跑通 `hf-security-gate + hf-perf-gate + hf-a11y-gate` 三者中的两项并产生 fresh evidence
- profile 分级清楚：`full` 要求全部非功能 gate，`standard` 按项目声明，`lightweight` 仍保留最小安全 / 合规自检

### 主要风险

- **Gate 过载**：一次引入太多 gate 会让主链密度爆炸。用 profile + `NFR declared` 驱动 gate 激活，保证只有 spec / design 显式声明过的 NFR 才激活对应 gate。
- **依赖外部扫描工具**：SAST / DAST / SBOM 需要真实工具链，HF 自身只承诺「消费 fresh evidence」，不自建扫描器。

## Phase 3 — 发布 / 运维闭环（商用级交付）

### 为什么放在这里

到这一步，HF 已经具备准商用非功能质量保证。Phase 3 要补的是**线上运行期的闭环**——progressive delivery、事故响应、postmortem、deprecation。这决定了 HF 能否进入对「生产严肃度」有要求的客户。

### 目标（Success State）

HF 能完整承接一个生产特性的全生命周期：上线策略、on-call、事故响应、postmortem、产品指标、deprecation 都有对应节点和工件。

### 核心交付物（候选块 4 完整 + 候选块 5 完整）

- 新 skill：`hf-deploy`（progressive delivery：feature flag / canary / blue-green / shadow）
- 新 skill：`hf-runbook`（runbook / on-call / alerting / dashboard）
- 新 skill：`hf-incident`（事故响应编排、severity、MTTR、ITIL-style incident record）
- 把 `hf-hotfix` 与 `hf-incident` 显式衔接：事故响应驱动 hotfix，hotfix 产出回到 incident record
- 新 skill：`hf-postmortem`（blameless postmortem、5 Whys、回流到 `hf-bug-patterns` 与 `hf-retrospective`）
- `hf-finalize` / `hf-product-metrics` 扩展：完整 DORA 四指标（deploy freq / lead time / MTTR / CFR）+ 产品 North Star / AARRR / HEART 跟踪
- 新 skill：`hf-deprecation`（sunset path、数据迁移、通知窗口、回滚）

### 退出条件

- 至少一次生产事故全流程走完 `hf-incident → hf-hotfix → hf-postmortem → hf-bug-patterns / hf-retrospective`，所有工件在仓库中可回读
- DORA 四指标、至少一个产品 North Star 指标自动回流到下一轮 discovery
- 至少一次 deprecation 走完完整通知 + 迁移 + 回滚窗口

### 主要风险

- **与团队既有 SRE / incident 工具耦合**：HF 只承诺「消费事件 / 产出 postmortem / 回流证据」，不尝试取代 PagerDuty / Opsgenie 等。
- **Postmortem 写成形式主义**：必须保留 blameless 心态的显式 hard gate，避免退化成模板填空。

## Phase 4 — 团队化与长期架构健康

### 为什么放在这里

Phase 3 结束后 HF 已经能承接单项目的商用交付。Phase 4 要让 HF 能**被团队长期运转**——多人协作、长期架构健康、债务登记、依赖生命周期。

### 目标（Success State）

HF 能在一支有 code owner、多人评审、周期性架构评审的团队里长期运转，且技术债与架构演化有独立档案，不靠一次性补丁维持。

### 核心交付物（候选块 6 完整 + 候选块 7 完整）

- 多人协作：Stakeholder / RACI / triad（PM-Design-Eng）对齐节点约定
- Code owner / approval matrix 作为 `hf-*-review` 的可选配置
- Pair / Mob programming 作为 `hf-test-driven-dev` 的可选协作模式
- 新 skill：`hf-tech-debt-register`（cross-task debt backlog，Two Hats 边界之外的债务登记）
- 新 reference：Architectural Fitness Functions（Ford / Parsons / Kua）作为长期守护
- 新 skill：`hf-dependency-lifecycle`（Renovate / npm audit / SBOM / CVE 响应）
- 周期性 `hf-architecture-review` 节点（ADR 回顾、context map 更新、smells 巡检）
- `hf-increment` 扩展支持「主动还债」型 increment，而不仅是需求变更驱动

### 退出条件

- 至少一个团队跑通一次「周期性架构评审 → 债务登记 → 主动还债 increment」完整循环
- `hf-dependency-lifecycle` 在一次真实 CVE 响应中产生 fresh evidence
- code owner / approval matrix 在至少一个多人评审场景下被使用

### 主要风险

- **RACI 与人流规则侵入主链**：多人协作应当作 `hf-*-review` 的可选配置，而不是新增 canonical 节点；否则 router FSM 会急剧复杂化。

## Phase 5 — 数据 / AI 产品分支 + 知识沉淀扩维

### 为什么放在最后

数据 / ML / LLM 产品是一个独立的节奏分支，不放在前面是为了避免过早分叉污染主链叙事。到 Phase 5，HF 的主链已经稳定，适合开分支而不破坏整体一致性。

### 目标（Success State）

HF 在数据 / AI 产品上具备与通用软件工程平行的一套节奏，并把知识沉淀从「仅 bug-patterns」扩到「工程经验 / 决策 / onboarding」多维度。

### 核心交付物（候选块 8 + 候选块 9）

- 新 skill family 分支：`hf-data-*` / `hf-ml-*`
  - data profiling / drift / bias / lineage
  - offline + online eval；champion-challenger
  - model registry；guardrail
- 把 `evals/` 目录规范化为 `hf-eval-harness`（prompt / agent eval 作为一等工件）
- LLMOps：回流的 prompt / policy 变更走 `hf-increment` + `hf-eval-harness` 闭环
- 把 `hf-bug-patterns` 的 pattern catalog 思路扩展到 `hf-engineering-learnings`（不止缺陷）
- 建立统一的 decision log / onboarding curation reference
- 架构演化由 `hf-architecture-review` 周期性写回 ADR 档案

### 退出条件

- 至少一个 AI-native 产品跑通 `hf-data-* → hf-ml-* → hf-eval-harness → hf-increment` 闭环
- 知识沉淀从 `hf-bug-patterns` 扩展后，至少承接过一次非 bug 类的工程学习归档

### 主要风险

- **AI 节奏被硬套进软件主链**：必须明确 `hf-data-*` / `hf-ml-*` 为 family 分支而非主链节点，避免 router FSM 被 AI 节奏反向绑架。

## 阶段映射到 gap analysis 候选块

| 候选块 | Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|---|---|---|---|---|---|---|
| 候选块 1：上游产品发现强化 | JTBD / OST / RICE / North Star / experiment 最小版 | 产品指标回流最小版 | — | 产品指标完整 | — | — |
| 候选块 2：战略建模与 NFR | DDD / Event Storming / QAS / threat list 模板 | Observability-by-Design / Perf budget / Privacy checklist | Threat Model / Compliance 独立 | — | — | — |
| 候选块 3：质量工程分支 | — | — | Perf / Security / a11y / Contract gate | — | — | — |
| 候选块 4：发布与运维 | — | 最小 `hf-release` + DORA 子集 | — | deploy / runbook / incident / postmortem / deprecation 完整 | — | — |
| 候选块 5：运行期学习度量 | — | retro + 一个产品指标 | — | DORA 完整 + 产品指标完整 + deprecation | — | — |
| 候选块 6：协作与外部工具 | — | PR template / task sync 最小 | — | — | RACI / code owner / pair&mob 完整 | — |
| 候选块 7：长期架构健康 | — | — | — | — | tech debt / fitness functions / dependency lifecycle / 周期性架构评审 | — |
| 候选块 8：数据 / AI 产品 | — | — | — | — | — | hf-data-* / hf-ml-* / eval harness |
| 候选块 9：知识沉淀扩维 | — | — | — | — | — | engineering learnings / decision log |

## Bottom Line

这份计划把 HF 的演进切成一条清晰的叙事：

1. **Phase 0 先做厚「产品洞察 + 架构设计」这两层**，把 HF 的差异化立住，这也是后续所有阶段能继承的底座——一个从 discovery 到 architecture 都有结构化工件与真人审批的 AI workflow。
2. **Phase 1 补最小发布与学习闭环**，让 demo 能进入真实团队做小规模市场验证。
3. **Phase 2–3 把非功能质量与线上运维闭环撑起来**，达到准商用 → 商用交付水平。
4. **Phase 4–5 解决长期团队化与 AI 原生产品的分支节奏**，让 HF 不只是一个项目级工具，而是团队级 / 产品族级的工程基础设施。

每个阶段都保留 HF 原有纪律（工件驱动、单活跃任务、fresh evidence、真人审批、profile 分级），新增能力只是**在现有主链上长出去**，不重构底座。

真正启动任何一个阶段时，应由 `hf-product-discovery` 先判断该阶段的 wedge 是否还成立，再走 `hf-specify` / `hf-design` / `hf-tasks` 做正式立项。本文只是作为演进输入，不替代这个立项过程。

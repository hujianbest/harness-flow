# HF 演进缺口分析：从产品 idea 到产品开发完成

## Purpose

本文把 HarnessFlow（HF）当前这套 skill pack，沿着「产品 idea → 产品开发完成」这条完整旅程，和业界优秀工程与产品实践做一次对齐分析，产出两类输入：

- **优势盘点**：HF 已经对齐哪些工业级方法论、相对其它 AI agent workflow 的差异点在哪里
- **缺口清单**：HF 目前显式缺失或偏薄的环节，按主链阶段组织，作为后续 HF skill family 继续演进的候选输入

本文不修改任何 skill，仅作为 `docs/todo/` 下的演进规划材料。落地成具体 skill / reference / gate 时，仍应走 HF 自己的主链（`hf-product-discovery` → `hf-specify` → `hf-design` → `hf-tasks` → ...）。

## HF 当前形状回顾

把 HF 所有节点摊开后，它覆盖的实际上是 **「产品想法 → 可评审规格 → 可评审设计 → 可执行任务 → 单任务 TDD 实现 → 多道评审与门禁 → 正式收尾」** 这一条主链，外加 `hf-hotfix / hf-increment / hf-bug-patterns` 三条支线。

```text
product idea
  └─ hf-product-discovery → hf-discovery-review
       └─ hf-specify → hf-spec-review → 规格真人确认
            └─ hf-design  ‖  hf-ui-design
                 └─ hf-design-review  ‖  hf-ui-review → 设计真人确认
                      └─ hf-tasks → hf-tasks-review → 任务真人确认
                           └─ hf-test-driven-dev（单活跃任务 Canon TDD）
                                └─ hf-test-review → hf-code-review → hf-traceability-review
                                     └─ hf-regression-gate → hf-completion-gate
                                          └─ hf-finalize（task / workflow closeout）
支线：hf-hotfix（缺陷）  |  hf-increment（需求/范围变更）  |  hf-bug-patterns（经验沉淀）
```

方法论来源在 `docs/principles/hf-sdd-tdd-skill-design.md` 里声明得很清楚：`spec-anchored SDD + gated TDD + router + fresh evidence`，显式参考了 Fowler、Kent Beck、GitHub Spec Kit、Thoughtworks、ARC42、C4、ADR、Fagan inspection、PMBOK 等。

## 和业界优秀实践对齐后的优势

下面每条都点到 HF 已经做到什么、它对齐的是哪家实践，以及相对典型 AI agent workflow 的差异点。

### 1. 把「编排」和「执行」真正拆开

- **HF 做了什么**：`using-hf-workflow` 只做入口判断，`hf-workflow-router` 负责运行时 FSM 路由，叶子 skill 只做自己份内事（见 `docs/principles/hf-sdd-tdd-skill-design.md` 的四层分离和 `skills/docs/hf-workflow-entrypoints.md`）。
- **业界对标**：Front Controller Pattern、Evidence-Based Dispatch、敏捷里的 Process Tailoring（Crystal / Disciplined Agile）。
- **价值**：绝大多数 AI coding agent 把编排和执行压成一个「大 prompt」，HF 的分层使恢复、审计、替换单节点都更可控。

### 2. Spec-anchored SDD 而不是 Spec-as-source

- **HF 做了什么**：明确选 Fowler 的 `spec-anchored` 档位，spec 是锚点和活文档，不是唯一可编辑源。`hf-specify` 结合了 EARS + BDD/Gherkin + MoSCoW + 六分类 + INVEST。
- **业界对标**：Fowler「Exploring Gen AI SDD」、GitHub Spec Kit、Thoughtworks 2025 SDD、ISO/IEC 29148、Dan North BDD、DSDM MoSCoW。
- **价值**：既保留 SDD 的意图锚点，又避免 spec-as-source 那种「全模型驱动生成」的脆弱。

### 3. Gated TDD + Fresh Evidence 作为主合同

- **HF 做了什么**：`hf-test-driven-dev` 实现 Canon TDD（`test list → RED → GREEN → REFACTOR`），单活跃任务约束，测试设计 approval 前置，RED / GREEN / 回归 / completion 四类证据必须落盘。
- **业界对标**：Kent Beck *Canon TDD / Tidy First?*、Fowler *Refactoring* Two Hats、Cockburn Walking Skeleton、Clean Architecture / SOLID。
- **价值**：把「我觉得修好了」从合法结论中去掉——这是多数 AI workflow 最容易塌的地方。

### 4. Review / Gate 是一等节点，且角色分离

- **HF 做了什么**：`hf-*-review`、`hf-regression-gate`、`hf-completion-gate` 各有独立职责，不准 reviewer 顺手改正文、不准实现节点替 gate 下结论。
- **业界对标**：Fagan Inspection、ATAM（架构）、Nielsen 启发式评估（UI）、Scrum Definition of Done、PMBOK gate reviews。
- **价值**：避免了 AI 常见的「同一会话既当作者又当评审」的 rationalization。

### 5. 支线明确：缺陷 vs 需求变更 vs 经验沉淀

- **HF 做了什么**：`hf-hotfix` 走 RCA + 最小安全修复 + 受控回流；`hf-increment` 强制 Change Impact Analysis + Baseline-before-Change + 唯一 canonical re-entry；`hf-bug-patterns` 作为可选经验沉淀旁路。
- **业界对标**：ITIL change management、Boehm / Pfleeger change impact、blameless post-mortem、defect pattern catalog。
- **价值**：多数 agent workflow 把「新做 / 修 bug / 改范围」硬塞进一条主链，HF 明确分流避免污染主链证据。

### 6. Design 阶段的 UI 并行路线

- **HF 做了什么**：`hf-ui-design` 作为 design stage 的 conditional peer（见 `hf-workflow-router/references/ui-surface-activation.md`），负责 IA / Atomic Design / Design Tokens / Nielsen / WCAG 2.2 AA / 交互状态清单，和 `hf-design`（架构 / 模块 / API / 数据）并行。
- **业界对标**：Dual-Track Agile（Jeff Patton / Marty Cagan）、Brad Frost Atomic Design、W3C Design Tokens、WCAG 2.2。
- **价值**：不把 UI 设计压到实现期，也不让它脱离架构设计独自漂。

### 7. 架构健康在 TDD 窗口持续维护

- **HF 做了什么**：Two Hats + Opportunistic / Preparatory refactoring + Clean Architecture conformance + 显式 escalation 边界（跨任务结构性重构踢给 `hf-increment`）。
- **业界对标**：Beck / Fowler Two Hats、Fowler Opportunistic Refactoring、Martin Clean Architecture、SOLID、Architectural Fitness Functions（Ford / Parsons / Kua，部分覆盖）。
- **价值**：回避「先堆完一堆任务再统一 tech debt week」的长期低效模式。

### 8. Profile 分级裁剪

- **HF 做了什么**：`full / standard / lightweight` 只调密度，不砍纪律；`lightweight` 依然保留任务层、实现层、至少两道 gate。
- **业界对标**：Crystal family、Disciplined Agile 的 process tailoring、SAFe essential 裁剪。
- **价值**：避免 SDD 在小改动上过重、也避免「轻量 = 跳流程」的滑坡。

### 9. 真人审批是显式的 checkpoint

- **HF 做了什么**：`规格真人确认 / 设计真人确认 / 任务真人确认` 都要求落盘记录，即使 `Execution Mode=auto` 也不能省。
- **业界对标**：PMBOK phase gate、Fagan 正式 sign-off、航空软件 DO-178C 评审门。
- **价值**：在「让 agent 全自动跑」的诱惑下，仍保留 human-in-the-loop 的关键锚点。

## 对标业界后，HF 明显缺失或薄弱的地方

下面按「从产品 idea 到开发完成」主链阶段组织。每条都指出：**缺什么、业界典型方法、建议落点**。这是给后续 HF skill family 继续演进的候选输入——不代表必须全部做，也不代表做的优先级，只代表「如果要覆盖完整旅程，这些位置有明确空白」。

### A. 产品发现阶段（discovery）偏薄

`hf-product-discovery` 只有 Problem Framing / Hypothesis-Driven Discovery / Opportunity-Wedge / Assumption Surfacing 四类方法，更接近「把脑图梳理成结构化草稿」。对比业界产品发现的实际工具箱：

| 缺失 | 业界典型实践 | 建议落点 |
|---|---|---|
| JTBD 框架 | Christensen / Alan Klement *Jobs Stories* | `hf-product-discovery` 新增 JTBD 模板 |
| Continuous Discovery Habits | Teresa Torres Opportunity Solution Tree | 作为 discovery 的结构化骨架 |
| 用户研究 / 访谈协议 | Contextual Inquiry、Jobs Interview、*The Mom Test* | 新增 `hf-user-research` skill 或 reference |
| 优先级量化 | RICE / ICE / Kano / Weighted Shortest Job First | MoSCoW 之外补数值化优先级 |
| 实验与假设验证循环 | Lean Startup Build-Measure-Learn、Design Sprint | 缺 `hf-experiment` / `hf-probe` 节点 |
| 北极星 / OKR / 价值度量 | North Star Metric、OKR、AARRR、HEART | discovery 与 spec 都没有显式价值度量字段 |
| 竞品 / 市场分析 | SWOT、Competitive teardown | discovery 模板缺这块 |
| 商业论证 | Business case、Value vs Effort、ROI | 完全缺失 |

**影响**：HF 能把「想法」整理成草稿，但不具备「判断它值不值得做、多大价值、怎么量化成功」的能力；discovery 的 `Bridge to Spec` 过早进入功能语义。

### B. 规格与设计阶段的非功能 / 安全 / 合规不够结构化

`hf-specify` 六分类里有 NFR / CON，但：

| 缺失 | 业界实践 | 建议落点 |
|---|---|---|
| 结构化 NFR 工作坊 | ISO 25010 质量模型、NFR workshop、Quality Attribute Scenarios (ATAM) | `hf-specify` / `hf-design` 单独章节 |
| Threat Modeling | STRIDE / PASTA / LINDDUN | 独立 `hf-threat-model` 或 `hf-design` 内置 |
| 隐私与合规 | Privacy by Design、GDPR / CCPA / HIPAA / SOC2 checklist | 独立 `hf-compliance-review` |
| 性能预算 | Performance budget、RUM 预期值、容量规划 | NFR reference 缺失 |
| 可观测性契约 | SLO / SLI、Error budget、Logs / Metrics / Traces 最小契约（Google SRE） | spec / design 都没有「observability-by-design」字段 |
| 成本 / FinOps | 容量与成本评估、FinOps 原则 | 完全缺失 |
| DDD 战略建模 | Bounded Context、Ubiquitous Language、Context Map、Event Storming | `hf-design` 以 C4 开始，战略上游缺 DDD / Event Storming |

**影响**：HF 当前 spec / design 对后端系统是「功能 + 模块 + API」的骨架，对「上线后能不能跑稳、能不能合规、能不能安全」的覆盖相对表面。

### C. 实现阶段：测试种类与质量工程不完整

`hf-test-driven-dev` 很严格，但只覆盖 Canon TDD + 单元 / 集成行为测试；`hf-regression-gate` 做广义回归。缺：

| 缺失 | 业界实践 | 建议落点 |
|---|---|---|
| Property-based testing | Hypothesis / QuickCheck | `hf-test-driven-dev` 的 test seed 模板 |
| Mutation testing | Stryker、PIT | `hf-code-review` 或独立 gate 作为可选度量 |
| Consumer-driven contract testing | Pact、Spring Cloud Contract | 微服务 / 多端系统缺 contract 节点 |
| 性能 / 负载 / 容量测试 | k6、Locust、Gatling、JMeter | 缺独立 `hf-perf-gate` |
| 安全测试 | SAST / DAST / SCA、依赖扫描 | 缺 `hf-security-gate` |
| 可访问性测试 | axe、Lighthouse a11y、手动测试 | `hf-ui-review` 只做静态审查 |
| Chaos engineering | Netflix Chaos、Gremlin | 高可用系统完全缺 |
| Exploratory testing | Session-based testing、James Bach | agent-only 流程很容易漏 |

**影响**：HF 能保证「我改的这段逻辑按测试通过」，但保证不了「它在生产环境的典型非功能维度上站得住」。

### D. 发布 / 运维 / 反馈闭环几乎不存在

从 `hf-completion-gate` 到 `hf-finalize`，HF 管到 release notes / changelog / handoff pack 就停了。对比业界「从 idea 到产品开发完成」的标准做法（Continuous Delivery + DevOps + SRE）：

| 缺失 | 业界实践 | 建议落点 |
|---|---|---|
| CI/CD 管线作为工件 | Accelerate / DORA、Trunk-Based Development | 新增 `hf-release` / `hf-deploy` |
| Progressive delivery | Feature flags、canary、blue-green、shadow traffic | 缺发布策略 skill |
| Observability-in-prod | SLO / SLI、alerting rules、runbook、dashboard | 缺 runbook + 可观测性 gate |
| Incident response | On-call、severity levels、MTTR 目标、ITIL incident | `hf-hotfix` 只做技术修复，缺事故响应编排 |
| Blameless postmortem | Etsy / Google postmortem template、5 Whys、RCA | 只散落在 `hf-hotfix` 心态里 |
| DORA 度量 | Deploy freq / Lead time / MTTR / Change failure rate | `hf-finalize` 没有回收这些数据 |
| 产品度量回流 | AARRR、HEART、North Star tracking | 没有 post-release learning loop |
| Deprecation / Sunset | AWS 风格 deprecation path、数据迁移策略 | 完全缺失 |

**影响**：HF 做完的是「代码合入与文档闭环」，不是「产品上线与学习闭环」。这是最明显的「到开发完成就停了」的断层。

### E. 协作、多人、跨职能层面缺位

HF 的默认假设是「AI agent + 一个真人审批」，没有考虑：

- Stakeholder matrix / RACI、跨职能 triad（PM-Design-Eng）对齐节点
- Code owner / approval matrix 多人评审流
- Pair / Mob programming、code review as conversation
- Sprint 事件容器（planning / review / retro）
- 与 Jira / Linear / GitHub Issues / 企业 OKR 工具的 task sync 约定
- Conventional commits / semantic versioning / 自动 changelog 约定

**影响**：当 HF 要进入一支真实团队时，会和团队已有的敏捷 / DevOps / PM 工具链产生大量「外挂补丁」。

### F. 技术债、架构长期健康缺少机制

- 没有 cross-task 的 **tech debt register**（debt backlog / debt interest），Two Hats 只处理 in-task
- 没有 **architecture fitness functions**（Ford / Parsons / Kua）作为长期守护
- 没有 **dependency lifecycle**（Renovate、npm audit、SBOM、CVE 响应）
- 没有定期的 **architecture review** / ADR 回顾节点
- `hf-increment` 只处理需求 / 范围变更，不覆盖「主动还债」型 increment

**影响**：短期纪律强，长期腐化防线薄。

### G. 数据产品 / AI 产品特有节奏缺失

HF 假设的是通用软件工程。数据 / ML / LLM 产品有明显不同的节奏：

- 数据评估（data profiling、drift、bias、lineage）
- 模型评估（offline eval、online eval、A/B、champion / challenger）
- Prompt / agent eval harness（`evals/` 目录虽在，但没有形成 skill）
- Feature store / feedback loop / 持续再训练
- MLOps / LLMOps（CD4ML、model registry、guardrail）

**影响**：做 AI 产品时 HF 需要大量外挂。

### H. 知识沉淀只有 bug-patterns，维度单一

- `hf-bug-patterns` 覆盖缺陷模式，但没有更广的 **engineering learning / decision log / onboarding curation**
- 没有定期 retrospective skill（Scrum retro / *Agile Retrospectives* by Derby-Larsen）
- ADR 只在 design 阶段产生，运行中的架构演化没有统一档案

## 主链覆盖矩阵（优势 vs 缺口速查）

| 旅程阶段 | HF 当前覆盖 | 主要对标实践 | 明显缺口 |
|---|---|---|---|
| 产品 idea → 方向判断 | `hf-product-discovery` + `hf-discovery-review`（problem framing / wedge / assumptions） | JTBD、Continuous Discovery、OST、Lean Startup、North Star / OKR | 价值量化、用户研究、实验循环、商业论证 |
| 方向 → 规格 | `hf-specify` + `hf-spec-review` + 真人确认（EARS / BDD / MoSCoW / INVEST / 六分类） | ISO 29148、BDD、User Story Mapping、Example Mapping | NFR workshop、观测契约、合规 / 安全需求、Example Mapping |
| 规格 → 设计 | `hf-design` ‖ `hf-ui-design` + 各自 review + 真人确认（C4 / ADR / ARC42 / Atomic / Tokens / WCAG） | DDD、Event Storming、ATAM、Threat Modeling、Service Blueprint | DDD 战略、Event Storming、Threat Model、隐私设计、性能预算 |
| 设计 → 任务 | `hf-tasks` + `hf-tasks-review` + 真人确认（WBS / INVEST / 依赖图 / DoD） | WBS、User Story Mapping、Sprint planning | 与外部任务系统同步、多人分工模型 |
| 任务 → 实现 | `hf-test-driven-dev`（Canon TDD + Walking Skeleton + Two Hats + Clean Arch） | Kent Beck TDD、Fowler Refactoring、Clean Arch、SOLID | Property-based、Contract、Mutation、Perf、Security、a11y 测试分支 |
| 实现 → 评审 | `hf-test-review` → `hf-code-review` → `hf-traceability-review`（Fagan / 追溯 / 架构健康） | Fagan、Clean Arch conformance、SOLID | 跨人评审流、code owner、PR 自动化、多视角评审 |
| 评审 → 验证 | `hf-regression-gate` + `hf-completion-gate`（fresh evidence / DoD / evidence bundle） | Scrum DoD、回归测试 BP | 性能 / 安全 / a11y / 合规独立 gate |
| 验证 → 收尾 | `hf-finalize`（PMBOK closeout + release readiness + handoff） | PMBOK、Release Readiness Review | CI/CD、progressive delivery、observability、incident、DORA、产品度量回流、deprecation |
| 运行期反馈 | （几乎没有） | SRE、DORA、AARRR / HEART、postmortem、retro | 整个 post-release learning loop |

## 给后续演进的候选输入（分组而非优先级排序）

下面把上述缺口重新切成可以独立立项的候选块。每块都只说「要引入什么、大致形状是什么」，不做时间估算，具体是否值得做、做到什么密度，应由后续 `hf-product-discovery` / `hf-specify` 正式判断。

### 候选块 1：上游产品发现强化

- 在 `hf-product-discovery` 引入 JTBD / Jobs Stories 模板
- 引入 Opportunity Solution Tree 结构（Teresa Torres）
- 引入 RICE / ICE / Kano 作为 MoSCoW 的量化补充
- 新 skill：`hf-user-research`（研究计划、访谈脚本、证据归档）
- 新 skill：`hf-experiment`（Build-Measure-Learn 循环、假设→实验→证据）
- discovery / spec 模板显式加入 North Star、OKR、成功度量字段

### 候选块 2：上游战略建模与非功能需求强化

- 在 design 阶段上游引入 DDD 战略建模（Bounded Context / Ubiquitous Language / Context Map）
- 新增 Event Storming reference 作为 spec → design 的桥梁
- `hf-specify` / `hf-design` 增加结构化 NFR 章节（ISO 25010 + Quality Attribute Scenarios）
- 新 skill：`hf-threat-model`（STRIDE / LINDDUN）
- 新 skill：`hf-compliance-review`（GDPR / SOC2 / HIPAA / Privacy by Design）
- `hf-design` 引入 Performance budget / Capacity planning reference
- `hf-design` / spec 引入 `Observability-by-Design` 章节（SLO / SLI / Logs / Metrics / Traces / Alerts 最小契约）
- `hf-design` 引入 Cost / FinOps 评估 reference

### 候选块 3：质量工程分支扩展

- `hf-test-driven-dev` test seed 模板引入 property-based testing 选项
- 新 gate：`hf-perf-gate`（负载 / 容量 / 延迟预算验证）
- 新 gate：`hf-security-gate`（SAST / DAST / SCA / 依赖扫描 / SBOM）
- 新 gate：`hf-a11y-gate`（WCAG 2.2 AA 动态验证，补 `hf-ui-review` 的静态部分）
- 新 gate：`hf-contract-gate`（消费者驱动契约测试）
- 可选 reference：Mutation testing、Chaos engineering、Exploratory testing 会话模板

### 候选块 4：发布与运维闭环

- 新 skill：`hf-release`（CI/CD 管线作为工件、Trunk-based / Conventional Commits / SemVer）
- 新 skill：`hf-deploy`（progressive delivery：feature flag / canary / blue-green / shadow）
- 新 skill：`hf-runbook`（runbook / on-call / alerting / dashboard）
- 新 skill：`hf-incident`（事故响应编排、severity、MTTR、ITIL-style incident record）
- 把 `hf-hotfix` 与 `hf-incident` 显式衔接：事故响应驱动 hotfix，hotfix 产出回到 incident record
- 新 skill：`hf-postmortem`（blameless postmortem、5 Whys、回流到 `hf-bug-patterns` 与 retrospective）

### 候选块 5：运行期学习与度量回流

- `hf-finalize` 扩展产出 DORA 数据点（deploy freq / lead time / MTTR / CFR）
- 新 skill：`hf-product-metrics`（North Star / AARRR / HEART 跟踪与回流到下一轮 discovery）
- 新 skill：`hf-retrospective`（Scrum retro / *Agile Retrospectives*，周期性而非一次性）
- 新 skill：`hf-deprecation`（sunset path、数据迁移、通知窗口、回滚）

### 候选块 6：协作 / 多人 / 外部工具链

- Stakeholder / RACI / triad（PM-Design-Eng）对齐节点约定
- Code owner / approval matrix 作为 `hf-*-review` 的可选配置
- 与 Jira / Linear / GitHub Issues 的 task sync reference（保持 HF 工件为真源）
- PR template / Conventional Commits / 自动 changelog 约定
- Pair / Mob programming 作为 `hf-test-driven-dev` 的可选协作模式

### 候选块 7：长期架构健康

- 新 skill：`hf-tech-debt-register`（cross-task debt backlog，Two Hats 边界之外的债务登记）
- 新 reference：Architectural Fitness Functions（Ford / Parsons / Kua）作为长期守护
- 新 skill：`hf-dependency-lifecycle`（Renovate / npm audit / SBOM / CVE 响应）
- 周期性 `hf-architecture-review` 节点（ADR 回顾、context map 更新、smells 巡检）
- `hf-increment` 扩展支持「主动还债」型 increment，而不仅是需求变更驱动

### 候选块 8：数据 / AI 产品分支

- 新 skill family 分支：`hf-data-*` / `hf-ml-*`（data profiling / drift / bias / lineage；offline + online eval；champion-challenger；model registry；guardrail）
- 把 `evals/` 目录规范化为 `hf-eval-harness`（prompt / agent eval 作为一等工件）
- LLMOps：回流的 prompt / policy 变更走 `hf-increment` + `hf-eval-harness` 闭环

### 候选块 9：知识沉淀扩维

- 把 `hf-bug-patterns` 的 pattern catalog 思路扩展到 `hf-engineering-learnings`（不止缺陷）
- 建立统一的 decision log / onboarding curation reference
- 架构演化由 `hf-architecture-review` 周期性写回 ADR 档案，而非只在 design 阶段一次性产生

## Bottom Line

HF 当前是一个非常硬的 **「SDD + gated TDD」中段引擎**：在 spec → 合入 → 文档闭环这一段，方法论纪律、工件驱动、证据链、真人审批都做得比多数 AI agent workflow 扎实。

要真正撑起「从产品 idea 到产品开发完成」的完整旅程，下一轮演进至少需要在四个方向继续补齐：

1. **discovery 侧** 补价值判断与实验闭环（候选块 1）
2. **上游设计侧** 补战略建模、非功能、安全、合规、可观测性（候选块 2）
3. **质量侧** 补非功能与安全性 gate（候选块 3）
4. **下游侧** 补发布、运维、事故响应、运行期学习与度量回流（候选块 4、5）

候选块 6–9 是在这个四象限基础上让 HF 能真正「进入团队、长期运转、并覆盖数据 / AI 产品」的放大器，可按仓库后续实际需求再决定取舍。

本文保持在「分析与候选输入」层面，不替代 `hf-product-discovery` / `hf-specify` / `hf-design` 对每个候选块的正式立项。后续任何一块真要做，都应该走 HF 自己的主链来做。

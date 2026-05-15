# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**从一个 idea 到产品落地：面向 AI Agent 的高质量工程工作流。**

> ## 范围声明（v0.5.1 pre-release）
>
> - **版本**：`v0.5.1`，在 GitHub Releases 上标记为 **pre-release**。v0.5.1 是 v0.5.0 之上的 **patch release**，修复 v0.5.0 的一个 vendoring 缺陷：closeout HTML 渲染脚本（`render-closeout-html.py`）从仓库根 `scripts/` 物理迁移到 `skills/hf-finalize/scripts/`，让 OpenCode `.opencode/skills/` 软链接 + Cursor `.cursor/rules/` + "vendor by copying `skills/`" 三种集成路径都能随 skill 一起 vendor 该脚本（详见 [`docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`](docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md) —— HF skill anatomy v2：4 类子目录 `SKILL.md` + `references/` + `evals/` + 新增 `scripts/`）。v0.5.0 主线描述（下方）仍然准确。
> - **v0.5.0 主线**：v0.5.0 是 **reviewer 体验切面** 版本——给 `hf-finalize` 的输出契约新增一份 **closeout HTML 工作总结报告**（每次 closeout 都会在 `features/<active>/closeout.html` 同步落盘），并新增 stdlib-only 渲染脚本 `skills/hf-finalize/scripts/render-closeout-html.py`（HF 主链节点 timeline rail + tests + coverage rings + 可搜索可排序 evidence matrix；WCAG 2.2 AA、暗亮主题、可打印、按 `skills/hf-ui-design/references/anti-slop-checklist.md` 反 AI slop 自检 S1-S8 全条覆盖）。v0.5.0 / v0.5.1 **不**扩 skill 集合（仍 **24** `hf-*` + `using-hf-workflow`），**不**新增 slash 命令（仍 **7**），**不**改主链 FSM 或 router transition map。v0.4.0 引入的 `hf-release`（release-tier standalone skill）保持不动。
> - **正式支持的客户端**：**Claude Code**、**OpenCode**、**Cursor**（与 v0.3.0 一致）。其余 4 家延后客户端（Gemini CLI / Windsurf / GitHub Copilot / Kiro）继续延后到 v0.6+。
> - **主链终点仍是 `hf-finalize`**——**单 feature 工程级 closeout**。v0.5.0 仅扩展 `hf-finalize` 的**输出契约**（新增 step 6A 产出 `closeout.html`），不动其它 23 个 skill。`hf-release` 是 release-tier 独立 skill，**汇总**多个 `workflow-closeout` 的 feature 成 vX.Y.Z 版本切片，**不**在主链中。发布管线、部署、可观测、事故响应、安全加固、性能门禁、debugging-and-error-recovery、deprecation-and-migration 按 [ADR-008 D1](docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md) **显式 out-of-scope**——HF 拒绝假装是部署工具；`hf-shipping-and-launch` 与其它 5 个工程化末段 skill **永久从路线图删除**（不是"待后续实现"）。
> - 这种窄而硬的范围是刻意选择（ADR-001 D1 / ADR-002 D1 / ADR-003 D2 / ADR-004 D2 / ADR-005 D7 — "P-Honest，窄而硬"）。HarnessFlow 拒绝把"代码合并 / 工程 closeout"伪装成"上线到生产"；v0.5.0 的 closeout HTML 是 closeout pack 的**视觉渲染**，**不是**部署记录。
>
> v0.5.1 patch 范围决策见 `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`；完整 v0.5.0 发版范围决策见 `docs/decisions/ADR-005-release-scope-v0.5.0.md`；v0.4.0 沿革（hf-release 引入）见 `docs/decisions/ADR-004-hf-release-skill.md`；v0.3.0 沿革（Cursor 加入）见 `docs/decisions/ADR-003-release-scope-v0.3.0.md`；v0.2.0 沿革（含 D11 校准说明）见 `docs/decisions/ADR-002-release-scope-v0.2.0.md`；v0.1.0 沿革见 `docs/decisions/ADR-001-release-scope-v0.1.0.md`。

HarnessFlow 是一个面向 AI Agent 的 skill pack，用来把**从产品洞察到架构设计、再到实现与交付**的完整工程节奏落到结构化工件、质量纪律和清晰交接上。它把产品发现、规格澄清、架构设计、任务拆解、带门禁的 TDD 实现、多道独立评审、回归与完成门禁、正式收尾都当作一等阶段，让 agent 沿着显式阶段推进"一个 idea → 可评审方向 → 可评审设计 → 可执行任务 → 可落地产品"，而不是依赖临时拼接的 prompt 链路。

## 致谢 / Acknowledgements

HarnessFlow 站在一组可显式归属的工程与产品方法之上。下表每一条只列「出处 + 它落到 HarnessFlow 哪个 `hf-*` skill 或宪法层文档」。

| 来源 | 在 HarnessFlow 中落到哪 |
|---|---|
| [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | `docs/principles/coding-principles.md`（Think Before Coding / Simplicity First (YAGNI) / Surgical Changes / Goal-Driven Execution）；已内联进每个 `hf-*` 的 `SKILL.md` |
| Software Engineering at Google + [Google engineering-practices guide](https://google.github.io/eng-practices/) | 各 `hf-*-review` skill 的 review 节奏、change sizing、reviewer 规范 |
| Eric Evans — *Domain-Driven Design* | `hf-design`（DDD 战略建模：bounded context、ubiquitous language、context map） |
| Vaughn Vernon — *Implementing Domain-Driven Design* | `hf-design`（DDD 战术模式：aggregate、value object、repository、domain service、application service、domain event） |
| Alberto Brandolini — Event Storming | `hf-design`（spec → design 桥梁） |
| Kent Beck — *Test-Driven Development* + Two Hats | `hf-test-driven-dev`（Canon TDD；Two Hats 纪律） |
| Martin Fowler — *Refactoring*、*Patterns of Enterprise Application Architecture*、Front Controller | `hf-test-driven-dev`（重构 playbook）；`using-hf-workflow`（Front Controller）；`hf-workflow-router`（FSM 派发） |
| Robert C. Martin — *Clean Architecture*、SOLID | `hf-test-driven-dev`（架构 conformance check）；`hf-code-review`（clean architecture review） |
| Michael Fagan — Fagan Inspection | `hf-discovery-review`、`hf-spec-review`、`hf-design-review`、`hf-ui-review`、`hf-tasks-review`、`hf-test-review`、`hf-code-review`、`hf-traceability-review` |
| Simon Brown — C4 Model | `hf-design` |
| Gernot Starke — ARC42 | `hf-design` |
| ISO/IEC 25010 — Quality Attribute model + Quality Attribute Scenarios | `hf-specify`（NFR framing）；`hf-design`（NFR 通过 QAS 承接） |
| Microsoft — STRIDE Threat Modeling | `hf-design`（轻量威胁建模） |
| Jakob Nielsen — Heuristic Evaluation | `hf-ui-design`、`hf-ui-review` |
| W3C WAI — WCAG 2.2 AA | `hf-ui-design`、`hf-ui-review` |
| PMI — PMBOK（project closeout / handoff） | `hf-finalize` |
| Tony Ulwick / Clayton Christensen — Jobs-to-be-Done | `hf-product-discovery` |
| Teresa Torres — Opportunity Solution Tree | `hf-product-discovery` |

## 项目概览

HarnessFlow 当前的主路径覆盖「**从一个 idea 到产品落地**」全程：

- **横切行为基线**（宪法层文档，非 workflow 节点）：`docs/principles/coding-principles.md` — Think Before Coding / Simplicity First（YAGNI）/ Surgical Changes / Goal-Driven Execution；每个 `hf-*` skill 已经把它们内联到自己的 `SKILL.md`，改写自 [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
- 上游 **产品洞察**：problem framing、JTBD、Opportunity Solution Tree、RICE / ICE、Desired Outcome / North Star
- **假设验证**：`hf-experiment` 在 Blocking 或低 confidence 关键假设下插入的最小 probe
- **规格澄清**：EARS + BDD + MoSCoW + INVEST + ISO 25010 + Quality Attribute Scenarios + Success Metrics / Key Hypotheses
- **架构设计**：DDD 战略建模 + DDD 战术建模（Aggregate / VO / Repository / Domain Service / Application Service / Domain Event）+ Event Storming + C4 + ADR + ARC42 + NFR QAS 承接 + 轻量 STRIDE + Emergent vs Upfront Patterns 治理（GoF 刻意 emergent）
- **UI 设计**（规格声明 UI surface 时激活）：IA + Atomic Design + Design Tokens + Nielsen + WCAG 2.2 AA + 交互状态清单
- **任务拆解**：WBS + INVEST + 依赖图 / 关键路径 + Definition of Done
- **单任务 TDD 实现**：Canon TDD + Walking Skeleton + Two Hats + Clean Architecture conformance + fresh evidence
- **浏览器运行时证据**（规格声明 UI surface 且当前任务触碰前端表面时激活的 verify-stage conditional side node）：DOM / Console / Network 三层 fresh evidence + Walking Skeleton 场景 + Observation-not-Verdict（不签 verdict，仅产 observations 供下游 gate 消费）
- **多道独立评审**：test / code / traceability / ui / discovery / spec / design / tasks review 的 Fagan 式角色分离
- **回归与完成门禁**：impact-based regression + evidence bundle + Definition of Done
- **正式收尾**：task closeout 与 workflow closeout 的 PMBOK 式闭环
- **运行时路由与恢复**：`using-hf-workflow` / `hf-workflow-router`，按工件证据恢复编排
- **支线**：`hf-hotfix` / `hf-increment`

向下继续演进（覆盖发布 / 运维 / 度量回流 / 协作 / 长期架构健康 / 数据与 AI 产品等商用级交付能力）已在规划中，但当前尚未落地。

在内部命名上，这套 skill family 目前使用 `hf-*` 约定。

## HF 方法论

HarnessFlow 不是一组零散 prompt 的集合，而是一套面向 agent 工程执行的工作流方法论。

从整体上看，HF 把这些方法组合在一起：

- **以 spec 为锚点的 SDD**：把 spec、design、tasks 当作结构化工件，而不是“大一点的 prompt”
- **带门禁的 TDD**：一次只实现一个 `Current Active Task`，先做测试设计，再保留新鲜的 RED/GREEN 证据
- **基于证据的路由**：下一步从磁盘工件恢复，而不是靠聊天记忆猜
- **独立的 review 与 gates**：test review、code review、traceability review、regression、completion 各自保持独立职责
- **受控的 closeout**：把“任务完成”和“整个 workflow 完成”区分开，并显式处理 finalize

这正是 HF 和普通 agent workflow 的差别：它优化的不只是更快开始写代码，而是正确性、可恢复性和工程纪律。

### 方法论分层

| 层 | HF 使用的方法 | 为什么重要 |
|---|---|---|
| 意图层 | 以 spec 为锚点的 SDD | 让范围、约束和验收标准始终落在可回读工件上。 |
| 执行层 | 带门禁的 TDD | 强制实现遵循测试设计、RED/GREEN 证据和单活跃任务约束。 |
| 路由层 | 基于证据的 workflow 恢复 | 让 agent 能从仓库状态恢复，而不是依赖会话记忆。 |
| 评审层 | 结构化 walkthrough 与 traceability 检查 | 让质量判断显式存在，而不是混在实现里顺手做掉。 |
| 验证层 | regression / completion gates | 把“看起来做完了”和“证据足以宣告完成”分开。 |
| 收尾层 | 正式 closeout 与 handoff | 避免代码改完后没有状态同步、release 记录和 workflow 收口。 |

### 方法论来源

HF 明确吸收了几类工程方法：

- Martin Fowler / Thoughtworks 风格的 **spec-driven development**
- Kent Beck 风格的 **test-driven development**
- Kent Beck / Fowler 的 **Two Hats** 帽子纪律，配合 **opportunistic / preparatory refactoring**，让架构与代码健康在编码节奏内被持续维护
- Robert C. Martin 的 **Clean Architecture** conformance 与 SOLID 检查，落到实现节点
- review 节点中的 **Fagan 风格结构化评审**
- 从 spec -> design -> tasks -> implementation -> verification 的 **端到端追溯**
- 把 **fresh evidence** 当成一等完成条件
- finalize / handoff 中的 **PMBOK 式收尾思路**

## 每个 Skill 用了什么方法论

HF 的每个 skill 都会在自己的 `SKILL.md` 里显式声明方法论。在 pack 层面，当前可以概括成下面这张图：

### 横切行为基线（宪法层文档）

| 文档 | 核心原则 |
|---|---|
| `docs/principles/coding-principles.md` | Think Before Coding、Simplicity First (YAGNI)、Surgical Changes、Goal-Driven Execution — 改写自 [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) |

这 4 条原则落在宪法层 `docs/principles/`（HF 自己的 design notes），**不是**独立 `hf-*` skill；每个 `hf-*` skill 已经把它们消化进自己的 `SKILL.md`，运行时不再外链原文。它们**不**进入 canonical `Next Action Or Recommended Skill` 受控词表，**不**给任何节点的 Workflow 加额外步骤，**不**替代 review / gate / approval / finalize 判断。

### 入口与路由

| Skill | 核心方法论 |
|---|---|
| `using-hf-workflow` | Front Controller Pattern、Evidence-Based Dispatch、Separation of Concerns |
| `hf-workflow-router` | Finite State Machine Routing、Evidence-Based Decision Making、Escalation Pattern |

### 上游 discovery

| Skill | 核心方法论 |
|---|---|
| `hf-product-discovery` | Problem Framing、Hypothesis-Driven Discovery、Opportunity / Wedge Mapping、Assumption Surfacing、JTBD / Jobs Stories、Opportunity Solution Tree、RICE / ICE / Kano、Desired Outcome / North Star Framing |
| `hf-discovery-review` | Structured Walkthrough、Checklist-Based Review、Separation of Author/Reviewer Roles、Evidence-Based Verdict |
| `hf-experiment`（Phase 0 新增） | Hypothesis-Driven Development、Build-Measure-Learn、Four Types of Assumptions (D/V/F/U)、Smallest Testable Probe、Pre-registered Success Threshold |

### Authoring

| Skill | 核心方法论 |
|---|---|
| `hf-specify` | EARS、BDD / Gherkin、MoSCoW Prioritization、Socratic Elicitation、INVEST、ISO/IEC 25010 + Quality Attribute Scenarios、Success Metrics & Key Hypotheses Framing、RICE / ICE / Kano（承接自 discovery） |
| `hf-spec-review` | Structured Walkthrough、Checklist-Based Review、Separation of Author/Reviewer Roles、Evidence-Based Verdict |
| `hf-design` | ADR、C4 Model、Risk-Driven Architecture、YAGNI + Complexity Matching、ARC42、DDD Strategic Modeling (Bounded Context / Ubiquitous Language / Context Map)、DDD Tactical Modeling (Aggregate / VO / Repository / Domain Service / Application Service / Domain Event)、Event Storming (spec→design bridge)、Quality Attribute Scenarios (NFR 承接)、STRIDE 轻量威胁建模、Emergent vs Upfront Patterns 治理 |
| `hf-design-review` | ATAM、Structured Walkthrough、Separation of Author/Reviewer Roles、Traceability to Spec |
| `hf-ui-design` | Information Architecture、Atomic Design、Design System / Design Tokens、Nielsen Heuristics、WCAG 2.2 AA、Interaction State Inventory、ADR |
| `hf-ui-review` | ATAM (adapted to UI)、Nielsen Heuristic Evaluation、Structured Walkthrough、Separation of Author/Reviewer Roles、Traceability to Spec |
| `hf-tasks` | WBS、INVEST Criteria、Dependency Graph + Critical Path、Definition of Done |
| `hf-tasks-review` | INVEST Validation、Dependency Graph Validation、Traceability Matrix、Structured Walkthrough |

### 执行与评审

| Skill | 核心方法论 |
|---|---|
| `hf-test-driven-dev` | TDD、Walking Skeleton、Test Design Before Implementation、Fresh Evidence Principle、Two Hats（Beck/Fowler）、Opportunistic + Boy Scout Refactoring、Preparatory Refactoring、Clean Architecture Conformance、Escalation Boundary |
| `hf-test-review` | Fail-First Validation、Coverage Categories、Risk-Based Testing、Structured Walkthrough |
| `hf-code-review` | Fagan Code Inspection、Design Conformance Check、Defense-in-Depth Review、Clean Architecture Conformance Check、Two Hats / Refactoring Hygiene Review、Architectural Smells Detection、Separation of Author/Reviewer Roles |
| `hf-traceability-review` | End-to-End Traceability、Zigzag Validation、Impact Analysis |
| `hf-browser-testing`（v0.2.0 / verify 阶段 conditional side node） | Three-layer Runtime Evidence (DOM / Console / Network)、Walking Skeleton Scenario、Fresh Evidence Principle、Observation-not-Verdict、Author/Reviewer/Gate Separation |

### 门禁与收尾

| Skill | 核心方法论 |
|---|---|
| `hf-regression-gate` | Regression Testing Best Practice、Impact-Based Testing、Fresh Evidence Principle |
| `hf-doc-freshness-gate` | Sync-on-Presence、Profile-Aware Rigor、Evidence Bundle Pattern、Author/Reviewer/Gate Separation |
| `hf-completion-gate` | Definition of Done、Evidence Bundle Pattern、Profile-Aware Rigor |
| `hf-finalize` | Project Closeout、Release Readiness Review、Handoff Pack Pattern |

### 分支与经验沉淀

| Skill | 核心方法论 |
|---|---|
| `hf-hotfix` | Root Cause Analysis / 5 Whys、Minimal Safe Fix Boundary、Blameless Post-Mortem Mindset |
| `hf-increment` | Change Impact Analysis、Re-entry Pattern、Baseline-before-Change、Separation of Analysis and Implementation |

## 为什么这些方法会分配给这些 Skills

HF 不是随意把方法论贴到各个节点上。每个 skill 使用的方法，都是为了匹配它在工作流里的核心职责。

- 入口和路由节点使用 controller、状态机和基于证据的决策方法，因为它们要回答的是“下一步该去哪里”，而不是写工件或写代码。
- authoring 节点使用需求、架构和计划类方法，因为它们要把模糊意图变成可批准、可测试、可拆解的工件。
- review 节点使用 walkthrough、checklist、inspection 和 traceability 方法，因为它们的职责是做独立质量判断，而不是继续写正文或继续实现。
- 实现节点使用 TDD、walking skeleton 和 fresh evidence 规则，因为这里最容易把“我觉得差不多了”误当成“已经被证明是对的”。
- gate 节点使用 definition of done、evidence bundle 和 impact-based verification 方法，因为它们回答的是一个比 review 更窄的问题：当前证据是否足以继续推进或宣告完成。
- 分支节点使用 RCA 和 change-impact 方法，因为 hotfix 与 increment 的本质是安全地处理缺陷恢复或安全地重入主链。
- finalize 使用 closeout 和 handoff 方法，因为“任务通过了”不等于“整个 workflow 已经正式结束”。

### 几个具体例子

| Skill | 为什么这些方法适合它 |
|---|---|
| `hf-specify` | 它的任务是把模糊需求变成可测试的规格，所以需要需求语法、优先级和澄清方法，而不是实现方法。 |
| `hf-design` | 它的任务是把已批准意图转成结构、接口和权衡，所以需要 ADR、C4 和风险驱动架构方法。 |
| `hf-test-driven-dev` | 它是“实现声明必须被运行行为证明”的节点，所以 TDD 和 fresh evidence 在这里是核心，而不是可选项。同一个节点也是 REFACTOR 的天然窗口，因此 Two Hats 纪律、opportunistic / preparatory 重构、Clean Architecture conformance、以及显式的 escalation 边界也都放在这里。 |
| `hf-code-review` | 测试通过并不能自动证明正确性、鲁棒性和安全性，所以 inspection 和 defense-in-depth 方法应该放在这里。该节点也通过评审实现节点的 Refactor Note 和对照已批准设计与 architectural smells 的 conformance 检查，强制保持架构健康与重构纪律。 |
| `hf-completion-gate` | 完成判断来自一组工件的组合证据，而不是某一个测试结果，所以 definition-of-done 和 evidence-bundle 更适合这个节点。 |
| `hf-finalize` | workflow 收口包含状态同步、release notes 和 handoff，因此 closeout 方法应该属于这里，而不是实现节点或 gate 节点。 |

## 安装

HarnessFlow 正式支持 **Claude Code**、**OpenCode** 和 **Cursor**。本节讲的是如何把 HarnessFlow 装到**你自己的项目**里，让 AI agent 在那个项目里使用 HF。三条客户端读的是同一份 `skills/` 目录，区别只在如何发现它（Claude Code：marketplace 插件 + slash 命令；OpenCode：`.opencode/skills/` 自动发现 + 自然语言路由；Cursor：`.cursor/rules/harness-flow.mdc` alwaysApply 规则 + 自然语言路由）。

> 如果你想开发或贡献 HarnessFlow 本身，请看 [`CONTRIBUTING.md`](CONTRIBUTING.md)——里面有克隆仓库并把客户端指向工作树的说明。

### Claude Code

通过 marketplace 安装。请用显式的 HTTPS URL + `.git` 后缀强制走 HTTPS 克隆；`owner/repo` 简写形式会走默认 SSH，未配 GitHub SSH key 的环境会失败：

```text
/plugin marketplace add https://github.com/hujianbest/harness-flow.git
/plugin install harness-flow@hujianbest-harness-flow
```

安装后会注册 [Slash 命令](#slash-命令claude-code) 一节列出的短命令。

> 安装命令是 `harness-flow@hujianbest-harness-flow`（plugin 名 `harness-flow` + marketplace 名 `hujianbest-harness-flow`），**不是** `harness-flow@harness-flow`。完整设置说明（含 SSH 故障排查）见 `docs/claude-code-setup.md`。

### OpenCode 与 Cursor（install 脚本）

OpenCode 与 Cursor 通过仓库自带的 install 脚本把 HarnessFlow vendor 到你的项目里。先把 HarnessFlow 仓库克隆到任意本地路径，然后把脚本指向你的项目：

```bash
git clone https://github.com/hujianbest/harness-flow.git /path/to/harness-flow

# OpenCode
bash /path/to/harness-flow/install.sh --target opencode --host /path/to/your/project

# Cursor
bash /path/to/harness-flow/install.sh --target cursor --host /path/to/your/project

# 同时安装两家
bash /path/to/harness-flow/install.sh --target both --host /path/to/your/project

# symlink 拓扑（跟随上游更新，而不是拷贝）
bash /path/to/harness-flow/install.sh --target both --topology symlink --host /path/to/your/project

# 卸载
bash /path/to/harness-flow/uninstall.sh --host /path/to/your/project
```

脚本写到你项目里的内容：

- `--target opencode` → `<host>/.opencode/skills/`（让 OpenCode 的 `skill` 工具能自动发现 HF；OpenCode **不**会自动发现仓库根目录裸放的 `skills/`）。
- `--target cursor` → `<host>/.cursor/harness-flow-skills/` 加 `<host>/.cursor/rules/harness-flow.mdc`（一条 alwaysApply 规则，每次 Cursor 会话加载 `using-hf-workflow`）。
- `<host>/.harnessflow-install-manifest.json` —— per-skill manifest，宿主自加在 `.opencode/skills/` 或 `.cursor/` 下的内容在 uninstall 时不会被误删。
- `<host>/.harnessflow-install-readme.md` —— 快速验证命令与卸载提示。

手工 `cp -R` / `ln -s` 拓扑与全局安装拓扑仍然可用。完整的安装拓扑、「自然语言意图 → 节点」映射、验证步骤与故障排查见 `docs/opencode-setup.md` 与 `docs/cursor-setup.md`。

#### Windows

`install.sh` / `uninstall.sh` 是 bash 脚本。Windows 上有三条路径：

1. **Git Bash**（推荐；随 [Git for Windows](https://git-scm.com/download/win) 一起装）。打开 Git Bash 直接跑上面的 `bash /path/to/harness-flow/install.sh ...` 命令即可。
2. **PowerShell 包装**。仓库同时附带 `install.ps1` / `uninstall.ps1`，会自动定位 bash（Git Bash → `PATH` 上的 `bash` → WSL）并转发所有参数，包括把 Windows 风格的 `--host C:\path\to\proj` 翻译成 POSIX 路径：

   ```powershell
   pwsh -File C:\path\to\harness-flow\install.ps1 --target both --host C:\src\my-project
   pwsh -File C:\path\to\harness-flow\uninstall.ps1 --host C:\src\my-project
   ```

3. **WSL**。在你的 WSL 发行版里像 Linux 一样直接跑 bash 脚本。

注意事项：Windows 上 `--topology symlink` 需要开启「开发者模式」（设置 → 隐私和安全性 → 开发者选项）或以管理员身份运行 shell；否则 Git Bash 会把 `ln -s` 静默降级成拷贝。默认的 `--topology copy` 没有这个限制。

安装后，在你的项目里发任何自然语言意图，router 会按磁盘工件证据选择正确的下一个节点：

```text
使用 HarnessFlow。我想给通知 API 加限流规则。
不要直接跳到写代码。
```

### 其他客户端

HarnessFlow 的 skill 是纯 Markdown，**理论上**可以通过把 `skills/` 当作指令文件喂给 Gemini CLI / Windsurf / GitHub Copilot / Kiro / Codex 等使用，但这些路径不在受支持范围内，也不提供对应的 setup 文档。

### Quickstart Demo：WriteOnce

`examples/writeonce/` 是 quickstart demo：一个把 Markdown 文件发布到 Medium 的 CLI（Zhihu / WeChat MP 声明为扩展点但不实现）。demo 的真正交付是 **HarnessFlow 主链 16 个节点留下的可回读工件**——`hf-product-discovery` → `hf-finalize` 的每一节点都在 `examples/writeonce/` 下产出了对应工件。Walking-skeleton 实现位于 `examples/writeonce/src/`，配套 23 条测试（离线运行，< 400 ms）。

阅读顺序：

1. `examples/writeonce/README.md` — demo 定位、范围、目录布局。
2. `examples/writeonce/docs/insights/2026-04-29-writeonce-discovery.md` — `hf-product-discovery` 产出。
3. `examples/writeonce/features/001-walking-skeleton/README.md` — feature 入口与状态总览。
4. 自上而下读 `spec.md` → `design.md` → `tasks.md` → `reviews/` → `verification/` → `closeout.md`。

### Vendor 时的目录结构

把 HarnessFlow 引入其他工作区时，只需复制 `skills/`。每个 `hf-*` skill 是**自包含**的：`SKILL.md`、`references/`（模板 / rubric / 子协议 / worktree 指南）和 `evals/` 都在 skill 文件夹内。仓库**不再有**跨 skill 的 `skills/docs/` / `skills/templates/` / `skills/principles/`。

`docs/principles/` 属于 **HarnessFlow 仓库自身**——HF 自己的 design reference，不是运行时依赖、不是发版门禁、不是 SKILL.md 合规基线。Vendor 时**不**需要复制 `docs/principles/`。

> **项目级约定**：HF skill 默认值开箱可用。若你的项目需要覆盖路径、模板、profile 规则、Execution Mode、覆盖率门槛或其他策略，在你仓库已有的项目约定文档里声明即可（例如项目自身的 guidelines、`CONTRIBUTING.md`，或宿主工具链的配置文件）。每个 `hf-*` skill 引用的都是"项目级约定（若已声明）"，**不**强绑定任何特定 sidecar 文件。

## Slash 命令（Claude Code）

Claude Code 插件注册 7 条短别名。前 6 条都是 **bias，不是 bypass**——router 仍然会用磁盘工件证据校验上游前置条件。`/release` 是例外：它 **direct invoke** `hf-release`，**不**经 router（`hf-release` 与 router 解耦）。

| 命令 | 偏向触发 | 备注 |
|---|---|---|
| `/hf` | `using-hf-workflow` → `hf-workflow-router` | 默认。不确定下一步该去哪个节点时用它。 |
| `/spec` | `hf-specify` | spec 起草 / 修订。 |
| `/plan` | `hf-design`（规格声明 UI surface 时并行 `hf-ui-design`）或 `hf-tasks` | 合并的 planning 命令——design 与 tasks 刻意合成一条命令。 |
| `/build` | `hf-test-driven-dev` | 仅当唯一 `Current Active Task` 已锁定时生效。 |
| `/review` | router 派发到对应的 `hf-*-review` | 评审是独立节点，作者/评审者必须分离。 |
| `/ship` | `hf-completion-gate` → `hf-finalize` | 由 gate 决定能否真正进入 finalize。**仅工程级 closeout，不是部署到生产**。 |
| `/release [version]` | **direct invoke** `hf-release`（**不**经 router） | 切 vX.Y.Z 工程级 release：汇总 `workflow-closeout` 的 feature、起草 scope ADR、跑 release-wide regression、同步 CHANGELOG / release notes / ADR 状态、产 tag-ready pack。**不**做部署 / staged rollout / 监控 / 回滚（按 ADR-008 D1 **显式 out-of-scope**，不是"待后续实现"）。 |

**刻意不包含**：

- 没有 `/hotfix`——自然语言 + `/hf` 即可让 router 在线上缺陷或范围变化时分流到 `hf-hotfix` / `hf-increment`。
- 没有 `/gate`——gate 应当被上游节点的 canonical next action **拉**起，而不是被用户**推**起。`/gate` 命令会鼓励"跳过实现 / 评审，直接撞门禁"的反模式。
- 没有 `/ship-to-prod`（或类似部署命令）——部署 / staged rollout / 监控 / 回滚按 ADR-008 D1 **显式 out-of-scope**（HF 不假装是部署工具；这是永久决定，不是延后）。

OpenCode 与 Cursor 都不注册任何 slash 命令文件；同样的意图通过自然语言 + `using-hf-workflow` 触达。`using-hf-workflow` 入口 shell 的 entry bias 表已加一行"切版本 / 出 release / 打 tag" → direct invoke `hf-release`，与 `/release` 命令同语义但通过 NL 触达。

## Quick Start

如果你只想先试一个 prompt，就先发这个：

```text
使用这个仓库里的 HarnessFlow。从 `using-hf-workflow` 开始，把我路由到正确的 HF 节点。
我想给通知 API 增加限流规则。
不要直接跳到写代码。
```

跑通之后，再试更真实的自然语言请求：

```text
使用 HarnessFlow，为通知 API 的限流规则编写或修订 spec。
使用 HarnessFlow，基于已批准的 spec 评审这份 design draft。
使用 HarnessFlow，对当前活跃任务按 TDD 实现并保留 fresh evidence。
使用 HarnessFlow，对 TASK-003 做 code review。
使用 HarnessFlow，判断这个任务是否真的可以算完成。
使用 HarnessFlow，对已完成的任务或整个 workflow 做 closeout。
```

你也可以直接用自然语言提示词：

```text
使用 HarnessFlow，并根据当前仓库里的工件继续推进。
使用 HarnessFlow，评审这份 spec draft。
使用 HarnessFlow，实现当前活跃任务。
```

| 你说什么 | HarnessFlow 应该做什么 |
|---------|------------------------|
| `使用 HarnessFlow，并根据当前仓库里的工件继续推进。` | 从 `using-hf-workflow` 或 `hf-workflow-router` 开始，根据磁盘工件恢复正确的下一节点。 |
| `使用 HarnessFlow，在写 spec 前先判断一个产品方向值不值得推进。` | 优先偏向 `hf-product-discovery`；如果当前阶段仍不明确，则交给 `hf-workflow-router`。 |
| `使用 HarnessFlow，为通知 API 的限流规则编写或修订 spec。` | 优先偏向 `hf-specify`；如果当前阶段仍不明确，则交给 `hf-workflow-router`。 |
| `使用 HarnessFlow，基于已批准的 spec 评审这份 design draft。` | 只有在这确实是 review-only 且设计工件已准备好时，才 direct invoke `hf-design-review`。 |
| `使用 HarnessFlow，对当前活跃任务按 TDD 实现并保留 fresh evidence。` | 只有在唯一活跃任务和上游批准条件都成立时，才推进到 `hf-test-driven-dev`。 |
| `使用 HarnessFlow，对 TASK-003 做 code review。` | 只有当 code review 的前置条件已经满足时才进入 `hf-code-review`；否则会回到更早的必要节点。 |
| `使用 HarnessFlow，判断这个任务是否真的可以算完成。` | 进入 `hf-completion-gate`，而不是把“完成”当成一句随口结论。 |
| `使用 HarnessFlow，对已完成的任务或整个 workflow 做 closeout。` | 只有在 completion 已允许 closeout 时才进入 `hf-finalize`；否则仍停留在 completion 或 router 逻辑。 |

让入口层和 router 根据仓库工件决定下一节点。这个仓库本身并没有对外提供 HF commands。

## 看它怎么工作

```text
你：    使用这个仓库里的 HarnessFlow。从 `using-hf-workflow` 开始。
        我想给通知 API 增加限流规则。

HF：    先路由到 `hf-specify`，澄清范围并准备可进入 spec review 的
        交接，而不是直接跳到实现。

你：    使用 HarnessFlow，评审这份 spec draft。

HF：    运行 `hf-spec-review`。如果 spec 通过评审且 approval step
        完成，workflow 才会继续进入 `hf-design`。

你：    spec 已经批准。使用 HarnessFlow 产出 design。

HF：    使用 `hf-design`，把已批准意图转成接口、结构和关键技术决策。

你：    使用 HarnessFlow，基于已批准的 spec 评审这份 design。

HF：    运行 `hf-design-review`。只有设计评审通过且 approval step
        完成后，workflow 才会继续走向 `hf-tasks`。

你：    使用 HarnessFlow，把 design 拆成 tasks，并准备下一个 active task。

HF：    使用 `hf-tasks` 和 `hf-tasks-review`，然后由 router 锁定唯一的
        `Current Active Task`，而不是让多个任务同时漂移。

你：    使用 HarnessFlow，对当前 active task 按 TDD 实现。

HF：    进入 `hf-test-driven-dev`，先写测试设计，完成 approval step，
        留下 RED/GREEN evidence，并写回 canonical 下一步。

你：    使用 HarnessFlow，依次评审这个任务的 tests、code 和 traceability。

HF：    按证据情况推进 `hf-test-review` -> `hf-code-review` ->
        `hf-traceability-review`。

你：    使用 HarnessFlow，跑 regression，并判断这个任务是否真的完成。

HF：    使用 `hf-regression-gate` 和 `hf-completion-gate` 来判断当前证据
        是否足够。

你：    使用 HarnessFlow，对已完成任务做 closeout。

HF：    如果还有剩余 approved tasks，就先收口当前任务并回到
        `hf-workflow-router`；如果已经没有剩余 approved tasks，且允许
        closeout，才进入 `hf-finalize` 做 workflow closeout。
```

重点不只是“发几个 prompt”。HarnessFlow 会在每一步读取工件、写回状态，
并产出一个受控的唯一下一动作。如果当前问题其实是线上缺陷或范围变化，
router 还会改走 `hf-hotfix` 或 `hf-increment`，而不是强行套入主链。

## 它的不同点

HarnessFlow 把工程活动当作一个受控工作流，而不是一次巨大的 agent 调用。

这套 pack 显式拆分了：

- 入口判断与运行时路由
- 编写阶段与实现阶段
- 实现阶段与评审 / 门禁阶段
- 单任务完成与整个工作流收尾

这样可以避免把编排、执行和质量判断压扁成一个不透明的动作。

## 工作流形状

一个典型的完整流程如下：

```text
using-hf-workflow
  -> hf-product-discovery
  -> hf-discovery-review
  -> (optional) hf-experiment     # Blocking / 低 confidence 假设时临时插入
  -> hf-workflow-router
  -> hf-specify
  -> hf-spec-review
  -> (optional) hf-experiment     # spec Key Hypotheses 中 Blocking 假设未关闭时插入
  -> hf-design  (|| hf-ui-design 当规格声明 UI surface 时并行激活)
  -> hf-design-review  (|| hf-ui-review)
  -> hf-tasks
  -> hf-tasks-review
  -> hf-test-driven-dev
  -> (optional) hf-browser-testing  # 当规格声明 UI surface 且当前 active task 触碰前端表面时由 router 拐点拉入
  -> hf-test-review
  -> hf-code-review
  -> hf-traceability-review
  -> hf-regression-gate
  -> hf-doc-freshness-gate
  -> hf-completion-gate
  -> hf-finalize
```

> **范围说明**：当前 Workflow Shape 的终点是 `hf-finalize`（**单 feature** 工程级 closeout；v0.5.0 新增 closeout HTML 工作总结报告——每次 closeout 在 `closeout.md` 旁同步落盘 `closeout.html` 视觉伴生制品）。**发布与上线**侧分两层：(1) **release-tier 版本切片**（多 feature → vX.Y.Z scope ADR + release-wide regression + 发布文档聚合 + tag readiness）由 v0.4.0 新增的 standalone skill `hf-release` 承担，与主链 **解耦**（不进本 Workflow Shape；通过 Claude Code 的 `/release` 或 OpenCode / Cursor 的 entry shell bias 行触发）。(2) **部署管线 / 可观测 / 事故响应 / 度量回流 / 上线后运维** 按 [ADR-008 D1](docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md) **显式 out-of-scope** —— `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-debugging-and-error-recovery` / `hf-deprecation-and-migration` **永久从路线图删除**（不是"待后续实现"）。HF 拒绝假装是部署工具；`hf-release` 是"切版本号 + 写发布文档"，**不是**"上线到生产"；v0.5.0 的 closeout HTML 是 closeout pack 的**视觉渲染**，**不是**部署记录。

`hf-experiment` 是 Phase 0 引入的 **discovery / spec stage 内部的 conditional insertion**：只在存在 Blocking 或低 confidence 关键假设时临时插入，`probe-result` 回流后按结果回到原插入点或上游修订节点。具体激活与回流规则见 `hf-workflow-router/references/profile-node-and-transition-map.md`。

`hf-browser-testing` 是 v0.2.0（ADR-002 D1 / D7）引入的 **verify stage 内部的 conditional side node**：在 `hf-test-driven-dev` 的 GREEN 之后，仅当（1）spec 显式声明 UI surface 或 `hf-ui-design` 已批准，且（2）当前 active task 影响面触碰前端 / UI 表面时，由 router 把它作为下一推荐节点拉入。它产出 `features/<active>/verification/browser-evidence/<task-id>/` 下的 DOM / Console / Network 三层 fresh evidence bundle 与 observations 清单，**不**签发 verdict、**不**修改实现 / 测试代码、**不**修改主链 FSM 主路径。回流由 router 按 observation severity 计数机械路由：`0 blocking + 0 major` → `hf-regression-gate`；`≥ 1 blocking` → 回 `hf-test-driven-dev`（带 finding）；`0 blocking + ≥ 1 major` → 按 observation 的 `suggested next` 派发（典型 `hf-test-review` 或 `hf-ui-review`）。任一激活条件不满足时 router 直接跳过，主链按原迁移规则继续。完整契约见 `skills/hf-browser-testing/SKILL.md` 与 `skills/hf-workflow-router/references/profile-node-and-transition-map.md` 的 `hf-browser-testing 激活与回流` 一节。

当规格声明 UI surface（页面 / 组件 / 交互 / 前端 UX NFR）时，router 会把 `hf-ui-design` 作为 **设计阶段内部的 conditional peer skill** 激活，与 `hf-design` 并行起草：`hf-design` 负责架构、模块、API 契约、数据模型、后端 NFR；`hf-ui-design` 负责信息架构、用户流、交互状态、视觉 Design Token、Atomic 组件映射、前端 a11y / i18n / 响应式。两条设计各自独立评审，只有 `hf-design-review` 与 `hf-ui-review` **均通过** 后，父会话才发起联合的 `设计真人确认`。激活条件与 Design Execution Mode（`parallel` / `architecture-first` / `ui-first`）详见 `skills/hf-workflow-router/references/ui-surface-activation.md`。

当请求本质上是缺陷修复或范围变化，而不是普通向前推进时，router 也可以分支到 `hf-hotfix` 和 `hf-increment`。

`hf-release` 是 v0.4.0 引入的 **release-tier standalone skill**，活在本 Workflow Shape **之外**。当用户在一个或多个 feature 经 `hf-finalize` 完成 `workflow-closeout` 后想切 vX.Y.Z release 时使用。它读各候选 feature 的 `closeout.md`，把 release-wide regression 与 sync-on-presence 协议**内联**到自身，产出 `features/release-vX.Y.Z/release-pack.md` tag-ready pack。**不**进 router transition map，**不**改主链 FSM，**不**自动执行 `git tag`（tag 操作由项目维护者承担）。详见 `skills/hf-release/SKILL.md` 与 `docs/decisions/ADR-004-hf-release-skill.md`。

## 设计原则

HarnessFlow 围绕以下几个默认前提构建：

- specs 锚定意图
- 路由依据磁盘工件，而不是聊天记忆
- 一次只实现一个活跃任务
- review 和 gates 是一等节点
- 质量结论必须依赖 fresh evidence
- 架构与代码健康在 TDD 的 REFACTOR 窗口内通过 Two Hats 与显式 escalation 边界持续维护，而不是延后到一次专门的清理
- closeout 是工程的一部分，而不是事后补充

## 仓库结构

```text
skills/                                # 可对外发布的 skill 包（vendor 时复制这个）
  using-hf-workflow/
    SKILL.md
    evals/
  hf-workflow-router/
    SKILL.md
    references/
      workflow-shared-conventions.md   # progress schema / verdict 词表 / record_path 语义
      review-dispatch-protocol.md
      reviewer-return-contract.md
      ...
    evals/
  hf-specify/
    SKILL.md
    references/
      spec-template.md
      feature-readme-template.md
      task-progress-template.md
      ...
    evals/
  hf-test-driven-dev/
    SKILL.md
    references/
      worktree-isolation.md            # worktree provisioning / safety / cleanup
      refactoring-playbook.md
      ...
    evals/
  hf-finalize/
    references/
      finalize-closeout-pack-template.md
  hf-regression-gate/
    references/
      verification-record-template.md
  hf-completion-gate/
    references/
      verification-record-template.md
  ...（每个 hf-* skill 一个自包含文件夹）

docs/principles/                       # HarnessFlow 自身的 design notes（不属于 skill 包运行时）
  soul.md
  skill-anatomy.md
  sdd-artifact-layout.md
  ...
```

- `skills/<skill-name>/` 是自包含的 skill：它的 `SKILL.md`、`references/`（模板、rubric、子协议）和 `evals/` 一起发布。仓库不再有跨 skill 的 `skills/docs/` 或 `skills/templates/`。
- `docs/principles/` 存放这套 pack 的更高层设计原则与方法论背景——这是 HF 自己的 design notes。skill 在 `SKILL.md` 中已经吸收相关约束，运行时**不**依赖这些文档。

> **模板就近随 skill 发布**：每份模板都放在使用它的 skill 自身 `references/` 内（例如 spec 模板在 `hf-specify/references/`、closeout pack 在 `hf-finalize/references/`、verification record 在各 gate 的 `references/`）。审计或生成工件时直接看对应 skill 的 `references/`。

## 从哪里开始看

如果你想快速理解这套 pack，建议先读这些文件：

1. `skills/using-hf-workflow/SKILL.md`
2. `skills/hf-workflow-router/SKILL.md`
3. `docs/principles/hf-sdd-tdd-skill-design.md`
4. `docs/principles/skill-anatomy.md`
5. `docs/principles/architectural-health-during-tdd.md`
6. `docs/principles/methodology-coherence.md`（方法论协作 / 反替代规则 / Phase × profile 激活表）

## 适合谁

HarnessFlow 面向那些希望让 AI Agent 承担**从一个 idea 到产品落地**的严肃工程工作的团队和开发者。它尤其适合这些场景：

- 你希望 agent 在 idea 阶段就进行结构化产品洞察（JTBD / OST / Desired Outcome），而不是凭感觉上手
- 你希望架构设计做得**厚**——Bounded Context / Ubiquitous Language / Event Storming / NFR QAS / 轻量威胁建模都落在可评审工件上
- 你希望工作流边界更清晰，中间状态可评审
- 你希望不同工件之间更可追溯（discovery → spec → design → tasks → code → tests）
- 你希望 agent 在真实仓库里的多步执行更安全、更可恢复
- 你希望跨会话恢复更容易；router 能从磁盘工件恢复编排，而不是靠聊天记忆

## 当前状态

HarnessFlow 当前以 coding workflow pack 为主体，Phase 0 已把产品洞察与架构设计两层打厚（JTBD / OST / RICE / Desired Outcome / QAS / DDD / Event Storming / STRIDE / `hf-experiment`）。向「商用级交付」方向的后续演进（发布、运维、度量、协作、长期架构健康、数据 / AI 产品分支）已在规划中，但当前尚未落地。

这个仓库包含当前 HF skill family、共享文档、模板，以及支撑这套 pack 的原则文档（含方法论协作与 phase / profile 激活地图 `docs/principles/methodology-coherence.md`）。

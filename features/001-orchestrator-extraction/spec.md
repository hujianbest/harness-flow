# HF Orchestrator Extraction & Skill Decoupling 需求规格说明

- 状态: 草稿
- 主题: 把 HF workflow 编排从 leaf skill 抽出为独立 always-on agent persona；让 leaf skill 回到 Anthropic Agent Skills 原始定位；通过 orchestrator 完整保留 long-task 自动开发能力
- Profile: full（架构 invariant 引入；router 最终决定）
- 上游 discovery: `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`（已通过 `hf-discovery-review`，3 条 minor LLM-FIXABLE finding 已在本 spec 吸收）
- Discovery review: `docs/reviews/discovery-review-hf-orchestrator-extraction.md`
- 候选 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（与本 spec 同 PR 起草，由 spec-review 一并评审）

## 1. 背景与问题陈述

HarnessFlow 自 v0.0.0 起把 24 个 `hf-*` skill 与编排逻辑（`using-hf-workflow` entry shell + `hf-workflow-router` runtime authority）共同打包，每个 leaf skill 在 SKILL.md 内部嵌入了三类对编排器的硬耦合：

1. **Authority 耦合**：leaf 显式声明"路由权属于 `hf-workflow-router`"、"跨 task 切换由 router 决定"
2. **Schema 耦合**：leaf 输出契约里有 `Next Action Or Recommended Skill`、`Pending Reviews And Gates` 等只在编排链下游消费者存在时才有意义的字段
3. **Artifact 耦合**：leaf 假设 `features/<active>/progress.md` / `spec.md` / `design.md` / `tasks.md` 存在并已批准，缺一项即触发 hard gate

**Struggling moment**：使用者想从某个 hf-* SKILL.md 复用方法论精华（例如 `hf-test-driven-dev` 的 Two Hats / SUT Form / Refactor Note 做一次 atomic TDD），却被迫先建完整 features/<NNN>/ + 跑完上游链拿到 approval record 才能启动；或在"破坏纪律单独跑"和"放弃用 HF"之间二选一。

这与 Anthropic Agent Skills 原始定位（progressive disclosure / 自包含 SOP / description-driven 自动发现）有显著偏离，也与生态对照系 [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)（37.5k stars，独立-SOP + 薄命令包装模型）路径相反。

承接 discovery § 1。

## 2. 目标与成功标准

### 2.1 当前轮目标

把"workflow 编排"和"skill SOP"在物理与契约两层都分离开：

- **物理分离**：建 `agents/hf-orchestrator.md` 作为独立 agent persona 文件，包含合并自 `using-hf-workflow` + `hf-workflow-router` 的等价改写内容
- **契约分离**：`agents/hf-orchestrator.md` 是有状态编排者，通过宿主 always-on 机制每 session 自动加载；leaf skill 的 SOP 内容**不变**（本轮范围内不动 leaf 文件），但通过 ADR-007 显式锁定后续 leaf 解耦的语义边界
- **能力保留**：long-task 自动开发能力（idea → closeout 全自动）由 orchestrator 完整承担，对使用者的体验不下降

### 2.2 总体成功标准

- 引入 `agents/hf-orchestrator.md` 后，HF workflow 跑现有 walking-skeleton（`examples/writeonce/features/001-walking-skeleton/`）应产出与现状语义等价的 closeout pack（容许时间戳与生成器路径差异）
- 3 个支持宿主（Cursor / Claude Code / OpenCode）能在新 session 自动加载 `agents/hf-orchestrator.md`，且无需使用者手动操作
- 本轮交付完成后，HF 24 个 leaf skill 文件**未被修改**；ADR-007 已锁定后续解耦的合法路径

具体可判断度量见 § 3。

## 3. Success Metrics

承接 discovery § 9。

- **Outcome Metric**：HF workflow 在引入 `agents/hf-orchestrator.md` 后跑端到端 walking-skeleton 的产物与现状的语义等价比例
- **Threshold**：
  - **必达**：walking-skeleton 回归测试通过（closeout pack schema-by-schema 等价；**容许差异白名单**：时间戳、生成器脚本路径文本、HTML 渲染时间戳）
  - **必达**：3 个支持宿主（Cursor / Claude Code / OpenCode）各跑一次"新 session → orchestrator 自动加载"smoke test 通过（判定标准：新 session 第一轮响应里能引用 `agents/hf-orchestrator.md` 中的标识性内容，例如 orchestrator 自报身份段）
  - **加分（不阻塞 v0.6.0 release）**：`agents/hf-orchestrator.md` 主文件 ≤ 300 行（progressive disclosure 到 `agents/references/`）——此为 **tentative engineering aim**（吸收 discovery review finding D1），acceptance criterion 在 `hf-design` 阶段最终锁定，本 spec 不作为 NFR 阈值
- **Leading Indicator**：
  - `agents/hf-orchestrator.md` 文件落盘且通过 `hf-test-review`
  - 3 个宿主的 always-on stub 文件分别落盘并通过 `hf-test-review`
- **Lagging Indicator**：
  - walking-skeleton 回归 / smoke test 全绿（`features/001-orchestrator-extraction/verification/`）
  - v0.6.0 release pack（`hf-release` 第 4 次 dogfood）通过 `hf-completion-gate`
- **Measurement Method**：
  - walking-skeleton 回归：写一个对比脚本，diff 旧产物 vs 新产物的 closeout pack；测试落到 `features/001-orchestrator-extraction/verification/regression-2026-05-XX.md`
  - 宿主 smoke test：人工新启 session 操作；记录到 `features/001-orchestrator-extraction/verification/smoke-3-clients.md`
  - 主文件行数：`wc -l agents/hf-orchestrator.md`，写入 design / closeout 的 evidence 字段
- **Non-goal Metrics**（discovery § 9 承接 + 显式延伸）：
  - 不追求缩短整体 coding workflow 总耗时
  - 不追求增加 HF 安装量 / star 数
  - 不追求覆盖 v0.6+ 计划的 5 个 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration`）
  - 不追求第三方生态把 HF 的 SOP 子集独立装载到非 HF 项目（discovery § 7 候选 C 的衍生收益，本轮不作为度量）
  - 不追求修改 `using-hf-workflow` / `hf-workflow-router` 这两个旧 skill 的删除（兼容期保留至下一个 minor）
- **Instrumentation Debt**：
  - 当前缺：自动化的 walking-skeleton 回归 diff 脚本——计划在 `hf-tasks` 阶段拆为一个独立 task 实现（轻量 shell 脚本，复用 `audit-skill-anatomy.py` 的 stdlib-only 风格）
  - 当前缺：3 宿主 smoke test 的可重复脚本化——本轮接受人工操作记录到 verification/，自动化推迟到 v0.7+

## 4. Key Hypotheses

承接 discovery § 6 的四类假设（Desirability / Viability / Feasibility / Usability）。

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-001 | HF 使用者真的有"想单独调用一个 leaf skill"的诉求，而不仅是维护者审美偏好 | Desirability | 整个 wedge 无价值；ADR-007 立项需重新论证 | 中 | P2 probe：翻 GitHub issues / discussions / 任何 feedback 渠道找"无法单独使用 skill"的诉求记录；本轮 spec 接受基于"对话证据 + 生态对照系（addyosmani 37.5k stars）"作为 medium confidence 的论据，不阻塞 | 否 |
| HYP-002 | 抽出 orchestrator 后，HF 的 reviewable artifact 产出率不下降 | Viability | 重构损伤 HF 核心价值；v0.6.0 应回滚 | 中-高 | walking-skeleton 回归测试（`hf-test-driven-dev` 阶段实施） | **是** |
| HYP-003 | Orchestrator agent persona 能在 3 个支持宿主（Claude Code / OpenCode / Cursor）通过 always-on 机制可靠加载 | Feasibility | 长任务自动化能力丧失；候选方案需回到 dual-mode（discovery § 7 候选 B） | 高 | 3 宿主 smoke test（`hf-test-driven-dev` 阶段实施）；Cursor 当前 session 已经是直接证据 | **是** |
| HYP-004 | FSM 转移表 + reviewer dispatch 协议从分布在多个 references 文件，集中到 orchestrator agent 后仍能 progressive disclosure（不撑爆 token 预算） | Feasibility | 每个 session 都付高额 token 成本；需要继续拆分 | 高 | NFR-002 已用字符数（`wc -c × 1.10`）作为 commit-time 验收，等价于把验证从 design 阶段提前到 commit 时刻；`hf-design` 阶段额外评估 references 拆分粒度（行数 ≤ 300 作为 **tentative engineering aim**，不作 NFR 阈值） | 否 |
| HYP-005 | Leaf skill 后续解耦时（本 spec 范围之外），剥离 `Next Action Or Recommended Skill` 字段后，orchestrator 仍能基于 on-disk artifacts 决定下一步 | Feasibility | 解耦路径需要保留更多 leaf-side hint；ADR-007 D3 的 6 步路径需重排 | 中 | `hf-design` 阶段定义"artifact → next-step"决策协议；本轮 spec 范围内 leaf 不变，**本假设不阻塞本轮 spec 通过**，但需在 ADR-007 中显式记入"待 design 阶段验证" | 否（本轮）；后续 increment 拆解时升级为阻塞 |
| HYP-006 | Reviewer/Author 分离（Fagan）在 orchestrator-side dispatch 下仍可强制 | Feasibility | 质量纪律松动；需引入额外护栏 | 高 | 不需独立 probe；本 spec § 6 显式列为 invariant，`hf-design` 阶段 dispatch 协议设计时落实 | 否 |
| HYP-007 | 使用者从"理解 HF = 理解 24 个 leaf 之间的 FSM"切换到"理解 HF = 1 个 orchestrator agent + 24 个独立 SOP"是认知负担下降 | Usability | 学习曲线没改善反而更陡 | 中-高 | README / docs 改写后让若干使用者冷读，5 分钟内能否说出"orchestrator vs SOP 二分"；推迟到 v0.6.0 release pack 阶段抽检 | 否 |

**阻塞性假设**（Blocking? = 是）：HYP-002 / HYP-003。两条均通过 `hf-test-driven-dev` 阶段的实测验证（walking-skeleton 回归 + 3 宿主 smoke），本 spec 通过评审**不要求**这两条已被验证（验证发生在 implement 阶段），但要求在 ADR-007 中显式锁定为"接受 v0.6.0 release 前必须通过"的 release-blocking 条件。

## 5. 用户角色与关键场景

承接 discovery § 2 + § 10。

| 角色 | 关键场景 | 当前痛点 | 本 spec 改善 |
|---|---|---|---|
| **HF 终端使用者**（atomic 任务） | 想就一个具体子任务复用某个 hf-* skill 的方法论（如 TDD / design / code-review），任务规模不到要走完整 HF workflow | 当前必须建完整 feature 目录，或破坏纪律单独跑 | **本轮不直接改善**（leaf 不变）；但 ADR-007 锁定后续 increment 解耦路径，使本场景在下一个 minor 可被解决 |
| **HF 终端使用者**（长任务自动开发） | 想跑 idea → closeout 全自动 | 当前可用，但 leaf skill 内部混入大量编排逻辑，使用体验臃肿 | orchestrator 抽出后，使用者只需理解 1 个 agent persona + leaf 的 SOP，认知负担下降；本轮交付即可见 |
| **HF 维护者** | 新增或修改 skill | 每次修改都跨"作为编排节点的契约"+"作为 SOP 的内容"两关注点 | ADR-007 锁定关注点分离的边界；维护时只需对应单层 |
| **第三方生态使用者** | 把 HF 某个 SOP 装到非 HF 项目 | 当前不可行：skill 文件强引用 HF 其它节点 | **本轮不直接改善**（leaf 不变）；ADR-007 把"标准化解耦"作为后续 increment 的 invariant |

**Jobs Story（核心场景，承接 discovery）**：

```text
When 我作为工程师在 Cursor / Claude Code / OpenCode 里启动新 session，

I want to 不需要手动加载任何 HF 文件，就能让 agent 自动以 HF orchestrator 身份
读取 features/<active>/progress.md 等 on-disk artifacts，决定下一步该调哪个 leaf
skill 并执行（或派发 reviewer subagent / 暂停等我确认），

so I can 把 HF 当作"长任务自动开发"的可靠编排框架，而不需要每次新会话都重新
冷启动整个 workflow 状态。
```

## 6. 当前轮范围与关键边界

### 6.1 当前轮 In-scope

1. **新增 agent persona 文件**：`agents/hf-orchestrator.md` 是 always-on agent persona（**不是** skill；不进 `audit-skill-anatomy.py` 扫描；不放 `skills/` 下）。内容是 `using-hf-workflow` + `hf-workflow-router` 的合并等价改写。
2. **新增可选 references 子目录**：`agents/references/`（progressive disclosure），承接来自 `skills/hf-workflow-router/references/*.md` 中的 FSM 转移表、reviewer dispatch protocol、reviewer return contract 等大块内容。**单源**：本轮在新位置生成；旧位置保留 redirect stub，以兼容现有外部教程链接。
3. **三宿主 always-on 引导 stub 同步**：
   - `.cursor/rules/harness-flow.mdc`（已存在）：内容指针从"加载 entry shell + router"改为"加载 `agents/hf-orchestrator.md`"
   - `CLAUDE.md`（仓库根，按需新建或追加段）：加 always-on stub 段
   - `AGENTS.md`（仓库根，按需新建或追加段）：加 always-on stub 段（OpenCode 与通用 agent 共用）
4. **Plugin manifest 同步**：`.claude-plugin/plugin.json` 注册 orchestrator 为 always-active agent（schema 字段名以 Claude Code 当前 plugin schema 为准；schema 不允许时本项降级为"通过 `CLAUDE.md` 加载"）
5. **ADR-007 锁定**：`docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（与本 spec 同 PR 起草），落实 § 12 描述的所有"保留不动"立场（吸收 discovery review finding A2）
6. **Walking-skeleton 回归测试**：写一个 stdlib-only diff 脚本，验证新 orchestrator 跑现有 walking-skeleton 产物等价
7. **3 宿主 smoke test 记录**：人工操作 + 文档化 verification 记录
8. **README / setup docs 同步**：v0.6.0 Scope Note + Workflow Shape + 各客户端 setup doc 加 always-on 段
9. **CHANGELOG `[Unreleased]`** 加 v0.6.0 一段

### 6.2 当前轮 Out-of-scope（关键边界，吸收 discovery review finding B1）

1. **Leaf skill 文件不被修改**——本轮不剥离任何 hf-* skill 的 Hard Gates / `Next Action` 字段 / 对其它 hf-* 的硬引用。这些落地路径 step 2–6 在后续 increments 完成。
2. **`using-hf-workflow` / `hf-workflow-router` 这两个旧 skill 不被删除**——本轮保留为 deprecated alias，内容用 redirect stub 指向 `agents/hf-orchestrator.md`；删除推迟到下一个 minor。
3. **Closeout pack schema 不变**——延续 ADR-005 D4 立场。
4. **Reviewer return verdict 词表不变**——延续 ADR-002 立场。
5. **`hf-release` skill 行为不变**——v0.4.0 已是 standalone，本轮不动；本 feature 完成后 `hf-release` 第 4 次 dogfood 走 v0.6.0 release pack。
6. **`audit-skill-anatomy.py` 行为不变**——agent persona 文件不在它的扫描范围（只扫 `skills/<name>/SKILL.md`）；ADR-006 D1 的 4 类子目录约定本轮不扩张。
7. **`hf-finalize` step 6A HTML 渲染不变**——延续 ADR-005 D1 立场。
8. **不新增任何 `hf-*` skill**——v0.6+ 计划的 5 项 ops/release skill 不在本轮。
9. **不引入新 slash 命令**——保持 7 条不变（`/hf-spec` / `/hf-build` / `/hf-review` / `/hf-closeout` / `/hf-product-discovery` / `/hf-experiment` / `/hf-release`）。
10. **不针对第三方生态独立消费 leaf skill 的能力做投入**——discovery § 7 候选 C 的衍生收益，作为 ADR-007 锚定的"未来 invariant 后果"记入，但本轮无 deliverable。
11. **`agents/` 目录不引入 specialist personas**（reviewer / debugger 专家等）——discovery § 11 Opportunity B，本轮不做。
12. **`.cursor/rules/` 不引入新 rule 文件**——只改现有 `harness-flow.mdc` 内容指针。

### 6.3 Deferred backlog

无独立 deferred backlog 文件（`features/001-orchestrator-extraction/spec-deferred.md` 不创建）。所有"延后到后续 increments"的内容已显式落到 ADR-007 D3（6 步落地路径的 step 2–6）+ § 6.2 Out-of-scope 表。

## 7. 范围外内容

完整 12 条范围外列表见 § 6.2 Out-of-scope（**权威来源**）。本 § 仅作为 spec 模板章节占位，不另列条目，以维持单源；§ 6.2 改动时不需要同步本节。冷读者直接跳至 § 6.2。

## 8. 功能需求

### FR-001 Orchestrator Persona 文件

- **优先级**: Must
- **来源**: HYP-002 / HYP-003（Blocking 假设的物理载体）；discovery § 12.1 范围边界第 1 项
- **需求陈述**: 系统必须在仓库根 `agents/` 目录下提供 `hf-orchestrator.md` 文件，作为 always-on agent persona；其内容**在语义上**等价于 `using-hf-workflow` + `hf-workflow-router` 当前合并行为的改写（具体子结构——operating loop 步骤切分、FSM 转移表的物理形态、reviewer dispatch 协议的内联或引用、skill catalog 的索引格式等——由 `hf-design` 阶段最终锁定）。
- **验收标准**:
  - **Given** 仓库 `main` 分支 HEAD，**When** 检查 `agents/hf-orchestrator.md` 是否存在，**Then** 文件存在且 `wc -l` 输出非零；frontmatter 含 `name: hf-orchestrator` + `description` 段。
  - **Given** orchestrator 文件已落盘，**When** 检查文件正文，**Then** 包含至少一段编排者自报身份段落（标识性内容），用于 § 3 smoke test 的判定。
  - **Given** 一个新 HF session 启动并加载 orchestrator 后，**When** 它收到 `using-hf-workflow` § 1 + `hf-workflow-router` § 2 / § 7 当前会触发的等价输入，**Then** 它产生与现状语义等价的路由决策（具体行为对照矩阵由 `hf-design` 阶段从现有 `hf-workflow-router/references/profile-node-and-transition-map.md` 衍生）。

### FR-002 三宿主 Always-On 引导 Stub 同步

- **优先级**: Must
- **来源**: HYP-003（Blocking 假设的实施载体）；discovery § 12.1 范围边界第 2 项
- **打包说明**：本 FR 在一条需求内打包 3 个支持宿主 × 4 种 always-on 注入机制；下面 4 条 acceptance bullet **逐条独立判定**——任一 bullet 不达标即整条 FR 不达标。`hf-tasks` 阶段可按需把每个 bullet 拆为独立任务（FR-002a / FR-002b / FR-002c / FR-002d），但 spec 阶段保持打包以便冷读"3 宿主同步"这一整体意图。
- **需求陈述**: 当 HF 在 Cursor / Claude Code / OpenCode 任一支持宿主中被加载时，系统必须通过该宿主的现有 always-on 注入机制让新 session 自动以 orchestrator persona 启动，无需使用者手动操作。
- **验收标准**:
  - **(FR-002.a Cursor) Given** Cursor 加载本仓库为 workspace，**When** 用户新建 chat session，**Then** `.cursor/rules/harness-flow.mdc` 内容已自动注入 system context 且其 body 引用 `agents/hf-orchestrator.md`（不再仅引用 `skills/using-hf-workflow/`）。
  - **(FR-002.b Claude Code) Given** Claude Code 在本仓库中被启动，**When** 用户发起新对话，**Then** `CLAUDE.md` 已自动注入并包含"加载 `agents/hf-orchestrator.md`"的指令；或 `.claude-plugin/plugin.json` 注册项使 orchestrator 自动激活（取一即可，schema 不允许时降级为前者）。
  - **(FR-002.c OpenCode) Given** OpenCode 加载本仓库，**When** 用户启动新 session，**Then** `AGENTS.md` 已自动注入并包含 orchestrator stub 段。
  - **(FR-002.d Identity check) Given** 任一上述宿主中新 session 已启动，**When** 用户输入"who are you / 你是什么 agent"类问题，**Then** agent 响应里能引用 `agents/hf-orchestrator.md` 中的标识性内容（用于 § 3 smoke test 通过判定）。

### FR-003 Orchestrator 等价语义保留

- **优先级**: Must
- **来源**: HYP-002（Blocking 假设的等价性证明）；discovery § 12.2 第 3 项
- **需求陈述**: 在 walking-skeleton 跑完整 HF workflow 时，系统必须使用 orchestrator persona 替代 `using-hf-workflow` + `hf-workflow-router` 的现有 entry / router 路径，并产出与现状语义等价的 closeout pack（在容许差异白名单之外，其它字段必须 byte-for-byte 一致）。
- **验收标准**:
  - **Given** 现有 `examples/writeonce/features/001-walking-skeleton/closeout.md` 与 `closeout.html` 作为 baseline，**When** 用 orchestrator 重跑该 walking-skeleton，**Then** 新产物与 baseline 在 closeout pack schema（H2 段、Evidence Matrix、State Sync、Release/Docs Sync、Handoff、Refactor Note）逐字段比对一致；容许差异 ∈ {时间戳，生成器脚本绝对路径文本，HTML 渲染时间戳}。
  - **Given** orchestrator 在跑 walking-skeleton 过程中遇到 review/gate 节点，**When** 编排到该节点，**Then** 它派发独立 reviewer subagent，不在父会话内联（验证 HYP-006）。
  - **Given** 回归脚本执行完毕（脚本物理位置由 OQ-N-003 在 `hf-tasks` 阶段最终决定，候选位置为 `features/001-orchestrator-extraction/scripts/regression-diff.{sh|py}` 或 `skills/hf-finalize/scripts/regression-diff.{sh|py}`），**Then** exit code = 0 且 stdout 含 "PASS" 行；**且** 该脚本的最终路径已登记到 `features/001-orchestrator-extraction/verification/regression-2026-05-XX.md` 的 evidence 字段，使 spec 阶段冷读者可在 verification record 里一意定位。

### FR-004 兼容期 Deprecated Alias

- **优先级**: Must
- **来源**: discovery § 7 候选 D 降级 + § 12.1 范围边界第 5 项；ADR-001 D1 "narrow but hard" 立场延续
- **需求陈述**: 在 v0.6.0 范围内，系统必须保留 `skills/using-hf-workflow/SKILL.md` 与 `skills/hf-workflow-router/SKILL.md` 两个旧文件，但其内容必须用最小 redirect stub 替换为指向 `agents/hf-orchestrator.md` 的引导段。物理删除推迟到下一个 minor（不在本 spec 范围）。
- **验收标准**:
  - **Given** v0.6.0 commit 后的仓库快照，**When** 检查两个旧 skill 文件是否存在，**Then** 文件仍存在，frontmatter `description` 含 "deprecated alias, see agents/hf-orchestrator.md" 字样；body 至少含一段明确的 redirect 指引。
  - **Given** 任一外部消费者通过老文档链接（指向 `skills/using-hf-workflow/SKILL.md` 或 `skills/hf-workflow-router/SKILL.md`）读取该文件，**Then** 能在 stub body 中找到迁移到 `agents/hf-orchestrator.md` 的明确指引（避免 404 体验）。

### FR-005 ADR-007 锁定立场

- **优先级**: Must
- **来源**: discovery § 12.2 第 5 项
- **需求陈述**: 系统必须在 `docs/decisions/` 新增 `ADR-007-orchestrator-extraction-and-skill-decoupling.md`，锁定本 feature 在 spec 阶段已稳定的所有架构 invariant、范围边界、6 步落地路径、§ 6.2 列出的所有"保留不动"立场。该 ADR 与本 spec 同 PR 起草，由同一 spec-review subagent 一并评审。
- **验收标准**:
  - **Given** v0.6.0 commit 后的仓库快照，**When** 检查 `docs/decisions/`，**Then** 存在 `ADR-007-orchestrator-extraction-and-skill-decoupling.md`，含至少 D1–D7 决策段（覆盖：架构 invariant 引入；与 ADR-004 D3 standalone-skill 立场的关系；6 步落地路径；本轮范围边界；兼容期保留旧 skill；release-blocking 假设清单；向 v0.6+ 5 项 ops/release skill 的关系）。
  - **Given** ADR-007 段落，**When** reviewer 冷读，**Then** 能识别出每条决策与 ADR-001 / ADR-002 / ADR-003 / ADR-004 / ADR-005 / ADR-006 的关系（兼容 / 扩展 / 不冲突）。

### FR-006 README / Setup Docs 同步

- **优先级**: Should
- **来源**: discovery § 13 非阻塞项第 4 条；ADR-005 D4 立场延续
- **打包说明**：本 FR 在一条需求内打包 README 中英双语 + 3 个 setup docs（共 5 个文档面）；下面 acceptance bullet 中"任一 setup doc"读作**全集量化**——每个 setup doc 与每个 README 文件均独立判定，任一未达标即整条 FR 不达标。
- **需求陈述**: 系统必须同步更新 `README.md` / `README.zh-CN.md` 顶部 Scope Note、`docs/cursor-setup.md` / `docs/claude-code-setup.md` / `docs/opencode-setup.md` 的 always-on 加载段，使其与 v0.6.0 引入 `agents/hf-orchestrator.md` 一致。
- **验收标准**:
  - **(FR-006.a README ×2) Given** v0.6.0 commit 后的仓库快照，**When** 检查 `README.md` 与 `README.zh-CN.md` 的 Scope Note，**Then** 两份 README 均含一段说明 v0.6.0 引入 `agents/hf-orchestrator.md`、保留 24 个 hf-* skill 数量不变、保留 7 条 slash 命令不变、`hf-release` 行为不变。
  - **(FR-006.b Setup docs ×3) Given** v0.6.0 commit 后的 3 个 setup docs，**When** 检查每一份 setup doc，**Then** "如何启用 HF" 段已从"加载 entry shell + router"改为"orchestrator agent 自动加载，无需手动操作"；3 份 setup docs **全部**通过该判定。

### FR-007 CHANGELOG `[Unreleased]` 段同步

- **优先级**: Should
- **来源**: HF 一贯实践（v0.5.0 / v0.5.1 等历史 release）
- **需求陈述**: 系统必须在 `CHANGELOG.md` 的 `[Unreleased]` 段加 v0.6.0 引入 `agents/hf-orchestrator.md` 的 Added / Changed / Decided / Notes 子段说明。
- **验收标准**:
  - **Given** v0.6.0 commit 后的 CHANGELOG，**When** 检查 `[Unreleased]` 段，**Then** 含 Added 段（agents/hf-orchestrator.md + 三宿主 stub）、Changed 段（README / setup docs）、Decided 段（ADR-007 引用）、Notes 段（兼容期、本轮不动 leaf skill 等说明）。

## 9. 非功能需求 (ISO 25010 + Quality Attribute Scenarios)

### NFR-001 Always-On 加载延迟可接受

- **优先级**: Must
- **来源**: HYP-003；discovery § 6.3 Feasibility
- **ISO 25010 维度**: Performance Efficiency（Time Behaviour）
- **Quality Attribute Scenario**:
  - **Stimulus Source**: HF 终端使用者
  - **Stimulus**: 在支持宿主中新建 session
  - **Environment**: 任一支持宿主（Cursor / Claude Code / OpenCode）正常运行；网络可用；本仓库已被加载为 workspace
  - **Response**: agent 自动以 orchestrator persona 启动，加载完成
  - **Response Measure**: 从 session 创建到第一轮用户响应包含 orchestrator identity 标识性内容的 wall-clock 时间 ≤ 同宿主下"加载现状 entry shell + router"的同口径 wall-clock baseline × 1.20（容许新方案在同宿主下不超过 +20%）
- **Acceptance**:
  - **(Quantitative)** **Given** 在 Cursor / Claude Code / OpenCode 任一支持宿主中分别建立 baseline（加载现状 `using-hf-workflow` + `hf-workflow-router`）与 candidate（加载 `agents/hf-orchestrator.md`）两组同操作 session，**When** 测量从 session 创建到第一轮响应包含 orchestrator identity 标识性内容的 wall-clock 时间，**Then** 三宿主的 candidate 时间均 ≤ 该宿主 baseline × 1.20；测量结果（含 raw timing + ratio）必须落盘到 `features/001-orchestrator-extraction/verification/load-timing-3-clients.md`，与 `smoke-3-clients.md` 并列。
  - **(Identity gate)** **Given** Cursor / Claude Code / OpenCode 任一宿主在本仓库新建 session，**When** session 启动，**Then** 第一轮用户响应中 agent 已具备 orchestrator persona 行为（identity check 通过；判据见 FR-002.d）。

### NFR-002 Token 预算控制

- **优先级**: Must
- **来源**: HYP-004
- **ISO 25010 维度**: Performance Efficiency（Resource Utilization）
- **Quality Attribute Scenario**:
  - **Stimulus Source**: 任一支持宿主的 always-on 加载机制
  - **Stimulus**: 把 `agents/hf-orchestrator.md` 注入新 session system context
  - **Environment**: 任一支持宿主正常运行
  - **Response**: 注入的 token 量在每个 session 启动时被消耗
  - **Response Measure**: `agents/hf-orchestrator.md` 主文件 token 量（按 4 chars/token 粗估）≤ 现状 `skills/using-hf-workflow/SKILL.md` + `skills/hf-workflow-router/SKILL.md` 主文件总 token 量 × 1.10（即不超过当前组合的 110%；progressive disclosure 到 `agents/references/` 的部分按需加载，不计入主文件）
- **Acceptance**:
  - **Given** v0.6.0 commit 的 `agents/hf-orchestrator.md`，**When** 用 `wc -c` 度量字符数，**Then** 字符数 ≤ `wc -c skills/using-hf-workflow/SKILL.md skills/hf-workflow-router/SKILL.md` 的总和 × 1.10
  - **备注**: 行数预算（≤ 300 行）作为 **tentative engineering aim**（吸收 discovery review finding D1）记录在 § 3 加分项；本 NFR 用字符数判定避免 line-wrap 干扰，acceptance criterion 为 NFR 阈值

### NFR-003 兼容性：旧路径外部消费者不 404

- **优先级**: Must
- **来源**: FR-004；ADR-001 D1 "narrow but hard" 立场延续
- **ISO 25010 维度**: Compatibility（Co-existence）
- **Quality Attribute Scenario**:
  - **Stimulus Source**: 任一外部消费者（已发布教程链接 / 第三方文档 / search engine cache）
  - **Stimulus**: 通过 v0.5.x 时代的链接读取 `skills/using-hf-workflow/SKILL.md` 或 `skills/hf-workflow-router/SKILL.md`
  - **Environment**: v0.6.0 commit 后的 main 分支
  - **Response**: 文件可读，且能找到迁移到新路径的指引
  - **Response Measure**: 两个旧文件 HTTP 200（或本地 fs 可读），且文件正文含至少一段明确的"see `agents/hf-orchestrator.md`"指引；不出现"file not found"
- **Acceptance**: 见 FR-004 验收

### NFR-004 Reviewer/Author 分离纪律保留

- **优先级**: Must
- **来源**: HYP-006；HF 跨版本 invariant
- **ISO 25010 维度**: Maintainability（Modularity）+ Functional Suitability（Functional Correctness）
- **Quality Attribute Scenario**:
  - **Stimulus Source**: HF workflow 编排到一个 review / gate 节点
  - **Stimulus**: orchestrator 决定派发 reviewer
  - **Environment**: 任一活跃 HF session
  - **Response**: orchestrator 通过宿主提供的 subagent 机制派发独立 reviewer，不在父会话内联评审
  - **Response Measure**: 在 walking-skeleton 回归 + 任一新走 HF workflow 的 feature 中，所有 review / gate 节点都能在 review record 文件中找到 "评审者: 独立 reviewer subagent" 字样
- **Acceptance**:
  - **Given** walking-skeleton 回归运行，**When** 遍历所有产出的 review record，**Then** 100% 包含 "独立 reviewer subagent" 标识
  - **Given** 任一新 feature 用 orchestrator 跑完一个 review 节点，**When** 检查 review record，**Then** reviewer 元数据声明 author / reviewer 分离

### NFR-005 容许差异白名单稳定

- **优先级**: Should
- **来源**: FR-003 容许差异白名单
- **ISO 25010 维度**: Maintainability（Testability）
- **Quality Attribute Scenario**:
  - **Stimulus Source**: walking-skeleton 回归脚本
  - **Stimulus**: diff 旧 / 新产物
  - **Environment**: `features/001-orchestrator-extraction/verification/`
  - **Response**: 脚本输出 PASS / FAIL，差异落在白名单内时判 PASS
  - **Response Measure**: 容许差异白名单（时间戳、生成器路径文本、HTML 渲染时间戳）以正则 / glob 形式硬编码在脚本中；脚本为 stdlib-only（Python 3 / shell；不引入 npm / pip 依赖），与 `audit-skill-anatomy.py` / `render-closeout-html.py` 同款约束
- **Acceptance**:
  - **Given** 脚本对同一 walking-skeleton baseline 跑两次，**When** 第二次 vs baseline，**Then** exit 0 + PASS（自一致性）
  - **Given** 在白名单外引入一个真实 schema 差异（人工 mutation 测试），**When** 跑脚本，**Then** exit 非 0 + FAIL，且 stdout 指出具体差异字段

## 10. 外部接口与依赖

不涉及外部 API / 服务依赖。

依赖项：
- **Anthropic Agent Skills 标准**（progressive disclosure / SKILL.md frontmatter / description-driven discovery）：本 feature 引入的 `agents/hf-orchestrator.md` 是 agent persona，**不强制遵循 SKILL.md frontmatter schema**；只要求 frontmatter 含 `name` + `description` 即可（与 SKILL.md schema 部分相容，不冲突）。
- **3 宿主的 always-on 注入机制**：
  - Cursor: `.cursor/rules/*.mdc` 的 always-applied workspace rule
  - Claude Code: `CLAUDE.md` always-load + `.claude-plugin/plugin.json` agent registration
  - OpenCode: `AGENTS.md` always-load + `.opencode/skills/` 软链接
- **Python 3 stdlib**（用于 walking-skeleton 回归 diff 脚本）

## 11. 约束与兼容性要求

- **C-001**: 本 feature 严格停在 ADR-001 D1 "P-Honest, narrow but hard" 立场内：不引入新 ops / release / monitoring / rollback 类 skill；不承诺部署 / 监控 / 回滚能力；不扩张主链尾部到 `hf-finalize` 之外。
- **C-002**: 本 feature 不修改 24 个 leaf skill 的内容（除 FR-004 把 `using-hf-workflow` / `hf-workflow-router` 改成 redirect stub 外）。
- **C-003**: 本 feature 不破坏 ADR-006 D1 的 4 类子目录约定（`SKILL.md` + `references/` + `evals/` + `scripts/`）；agent persona 文件不在 skill 子目录约定范围内。
- **C-004**: 本 feature 不修改 `audit-skill-anatomy.py` 行为；该脚本只扫 `skills/<name>/SKILL.md`，对新增的 `agents/` 目录完全透明。
- **C-005**: Plugin manifest 注册（FR-002）以 Claude Code 当前 plugin schema 为准；如 schema 不支持 `alwaysActive` 等价字段，本项降级为通过 `CLAUDE.md` 加载（`hf-design` 阶段在 schema 校验后最终决定）。
- **C-006**: 兼容期 deprecated alias（FR-004）的 redirect stub 不允许超过 30 行（保持轻量；避免使用者误以为旧文件仍是权威）。

## 12. 假设与失效影响

承接 § 4 的非 Blocking 假设（HYP-001 / HYP-005 / HYP-007）+ 以下 spec 独有的运行假设：

| 假设 | 失效影响 |
|---|---|
| 仓库根 `agents/` 目录约定能被使用者 / 维护者直观理解 | 学习曲线增加；通过 README + setup docs 显式说明可缓解 |
| `agents/references/` 子目录的 progressive disclosure 由 agent 主动按需 read，无需宿主层支持 | 实际加载量超出 NFR-002 token 预算；fallback 是把 references 全量内联到 orchestrator 主文件（违反 NFR-002，本轮不接受） |

## 13. 开放问题

### 阻塞项

- 无。

（吸收 discovery review finding B1：原 discovery § 13 唯一"阻塞项"——references 是否本轮一并迁到 `agents/references/`——已在本 spec § 6.1 In-scope 第 2 项明确决定为"本轮迁移；旧位置保留 redirect stub"，从阻塞降级为已决策。该决策同时记入 ADR-007 D2。）

### 非阻塞项

- **OQ-N-001**: 命名 `agents/hf-orchestrator.md` vs `agents/orchestrator.md` vs `agents/hf-workflow-orchestrator.md`——倾向第一个（与 `hf-*` 命名空间一致）；最终在 `hf-design` 阶段确认。
- **OQ-N-002**: `agents/` 与 `.claude-plugin/agents/`（如有）的关系——倾向 HF 项目根 `agents/` 是 single source of truth，plugin manifest 通过 `source: agents/...` 引用。`hf-design` 阶段验证。
- **OQ-N-003**: walking-skeleton 回归 diff 脚本是否要写到 `skills/hf-finalize/scripts/` 复用 ADR-006 D1 的 skill-owned 工具约定，还是落到 `features/001-orchestrator-extraction/scripts/` 作为本 feature 的一次性工具——倾向后者（本工具只为本 feature 验证使用，不属于 hf-finalize SOP 的一部分）；`hf-tasks` 阶段定。
- **OQ-N-004**: 是否需要 `hf-experiment` 节点先做"orchestrator 加载 smoke test"作为 hard probe——倾向不需要，smoke test 不需要独立 probe 工件，直接放到 `hf-test-driven-dev` 阶段一并验证；`hf-design` 阶段定。
- **OQ-N-005**: v0.6.0 release pack 走 `hf-release` 第 4 次 dogfood 时，是否同时验证 patch / minor 两类 release 流程的差异——倾向 minor（与 v0.4.0 引入 `hf-release` 同档；patch 已在 v0.5.1 验证）；`hf-release` 阶段定。

## 14. 术语与定义

- **Doer Skill**：执行类 skill，对应 24 个 hf-* 中负责"产出工件"的部分（如 `hf-specify` / `hf-design` / `hf-tasks` / `hf-test-driven-dev` / `hf-product-discovery` / `hf-experiment` / `hf-hotfix` / `hf-increment` / `hf-finalize` / `hf-ui-design` / `hf-browser-testing` / `hf-release`）。Discovery § OST 用语。
- **Reviewer/Gate Skill**：评价 / 门禁类 skill，对应 24 个 hf-* 中负责"产出 verdict"的部分（如 `hf-spec-review` / `hf-design-review` / `hf-tasks-review` / `hf-test-review` / `hf-code-review` / `hf-traceability-review` / `hf-discovery-review` / `hf-ui-review` / `hf-regression-gate` / `hf-completion-gate` / `hf-doc-freshness-gate`）。
- **Orchestrator Agent**：本 feature 引入的 always-on agent persona，对应 `agents/hf-orchestrator.md`。**不是 skill**，不进 `audit-skill-anatomy.py` 扫描。
- **Always-On 加载机制**：每个支持宿主的 session-level 自动注入文件机制（Cursor `.cursor/rules/*.mdc` / Claude Code `CLAUDE.md` 与 plugin agent / OpenCode `AGENTS.md`）。
- **Walking-Skeleton 回归**：用 `examples/writeonce/features/001-walking-skeleton/` 作为基准，对比新旧 HF workflow 跑同一条端到端轨迹的产物等价性测试。
- **Tentative Engineering Aim**：在 spec 阶段提出但 acceptance criterion 推迟到 design 或 implement 阶段最终锁定的工程目标（吸收 discovery review finding D1）。本 spec 中行数预算（≤ 300 行 orchestrator 主文件 / ≤ 145 行 leaf skill）属此类，记入 § 3 加分项与 § 12 假设，**不**作为 NFR 阈值。

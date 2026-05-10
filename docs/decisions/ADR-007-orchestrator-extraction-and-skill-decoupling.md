# ADR-007: 从 leaf skill 抽出 orchestration，建立 always-on agent persona——HF 三层架构 invariant

- 状态：起草中（2026-05-10 锁定，待 `hf-spec-review` + `hf-design-review` 评审）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 协作契约执行）
- 关联 feature: `features/001-orchestrator-extraction/`（HF 第一个 coding-family feature）
- 关联 spec: `features/001-orchestrator-extraction/spec.md`
- 关联 discovery: `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`（已通过 `hf-discovery-review`）
- 关联文档：
  - `docs/decisions/ADR-001-release-scope-v0.1.0.md` D1（"P-Honest, narrow but hard" 立场）
  - `docs/decisions/ADR-002-release-scope-v0.2.0.md`（D11 校准；reviewer return verdict 词表确立）
  - `docs/decisions/ADR-003-release-scope-v0.3.0.md` D2（Cursor 加入官方支持宿主）
  - `docs/decisions/ADR-004-hf-release-skill.md` D3（**关键先例**：standalone skill 与 router 解耦）
  - `docs/decisions/ADR-005-release-scope-v0.5.0.md` D4 / D7（v0.5.0 立场延续；漂移到 v0.6+ 的 5 项 ops/release skill）
  - `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md` D1（4 类子目录约定）
  - `skills/using-hf-workflow/SKILL.md`（v0.0.0 起的 entry shell，本 ADR 后转 deprecated alias）
  - `skills/hf-workflow-router/SKILL.md`（v0.0.0 起的 runtime authority，本 ADR 后转 deprecated alias）

## 背景

HF 自 v0.0.0 起把 24 个 `hf-*` skill 与编排逻辑（`using-hf-workflow` entry shell + `hf-workflow-router` runtime authority）共同打包。每个 leaf skill 在 SKILL.md 内部嵌入了三类对编排器的硬耦合：

1. **Authority 耦合**：leaf 显式声明"路由权属于 `hf-workflow-router`"
2. **Schema 耦合**：leaf 输出契约里有 `Next Action Or Recommended Skill` / `Pending Reviews And Gates` 等只在编排链下游消费者存在时才有意义的字段
3. **Artifact 耦合**：leaf 假设 `features/<active>/` 目录与上游 approval record 存在

这套设计在"长任务自动开发可恢复 / 可审计 / 防漏步"这几个维度跑得很好（也是 HF 区别于纯 agent 智能驱动方案的核心价值），但代价是 leaf skill **不再是真正意义上的独立 SOP**——使用者无法把某个 hf-* skill 单独用在不需要全套 workflow 的子任务上。

这与 Anthropic Agent Skills 原始定位（progressive disclosure / 自包含 SOP / description-driven 自动发现）有显著偏离。生态对照系 [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)（GitHub 37.5k stars）则严格守住"独立 SOP + 软衔接（description / When to Use / See Also）+ 7 条 slash 命令薄包装"模型，证明该方向在生态里被广泛接受。

HF 自身在 v0.4.0 ADR-004 D3 已经接受过"部分 skill 与 router 解耦"——`hf-release` 就是 standalone skill，**不进** router transition map。但这种解耦目前只用在 release tier，没有下放到 coding family 的 leaf。

`hf-product-discovery`（`docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`）评估了 4 个候选方向：

- **候选 A**：Status Quo——剪枝（与已观察到的使用者痛点冲突；与生态主流方向背离）
- **候选 B**：Dual-Mode Leaf Skills（每个 leaf 加 Workflow / Standalone 双模）——剪枝（把耦合从集中变分散，治标不治本；用户已显式否决）
- **候选 C**：Full Orchestrator Extraction——**采用**（架构最干净；leaf 真的独立；与 Anthropic / addyosmani 模型对齐；与 v0.4.0 ADR-004 D3 思路自然延伸）
- **候选 D**：Full Orchestrator Extraction + 同步删除旧 skill 文件——降级（违反 ADR-001 D1 "narrow but hard"立场；外部教程链接立刻 404；不可恢复）

本 ADR 一次性锁定候选 C 的所有架构 invariant，并为 v0.6.0 minor release 划定 spec 阶段已稳定的范围边界。详细落地实施由 `hf-design` / `hf-tasks` / `hf-test-driven-dev` 接管。

## 决策

### Decision 1 — HF 三层架构 invariant 引入：Doer Skills / Reviewer-Gate Skills / Orchestrator Agent

HF 的 skill 集合**在概念上**显式分为三层：

| 层 | 定位 | 物理载体 | 数量（v0.6.0） |
|---|---|---|---|
| **Doer Skills**（Layer 1） | 执行类 SOP；产出工件 | `skills/hf-{specify,design,tasks,test-driven-dev,product-discovery,experiment,hotfix,increment,finalize,ui-design,browser-testing,release}/` | 12 |
| **Reviewer / Gate Skills**（Layer 2） | 评价 / 门禁类 SOP；产出 verdict | `skills/hf-{spec,design,tasks,test,code,traceability,discovery,ui}-review/` + `skills/hf-{regression,completion,doc-freshness}-gate/` | 11 |
| **Orchestrator Agent**（Layer 3） | 有状态编排者；决定何时调谁、何时停、何时连续运行 | `agents/hf-orchestrator.md`（本 ADR 引入） | 1 |

**关键不变量**：

- Layer 1 / Layer 2 之间**互不引用**——只在 SKILL.md 的 `## See Also` 段做软提及；不做 hard gate 引用、不写其它 hf-* 的 canonical ID 作为 handoff 字段
- 只有 Layer 3 知道完整的 FSM 转移图、Profile 决策、Workspace Isolation、reviewer dispatch 协议
- Layer 3 **不是 skill**——不进 `skills/` 目录、不进 `audit-skill-anatomy.py` 扫描、不需要 SKILL.md frontmatter 完整 schema；它是 agent persona

**这是 HF 的新架构 invariant，跨版本不可在 runtime 推翻。** 修改本 invariant 必须走新 ADR（如 ADR-009+）。

#### 生效阶段（Architectural Commitment vs Runtime Enforcement）

为消除 D1 与 D3 Step 5 之间的潜在歧义，本 ADR 显式区分 invariant 的两层语义：

- **v0.6.0 范围内**（D3 Step 1 完成后），D1 作为**架构承诺**（architectural commitment）生效：
  - 引入 `agents/hf-orchestrator.md`（Layer 3 物理存在）后，HF skill 集合在概念上正式分为三层
  - 新增 leaf skill 必须遵循"互不引用"不变量（即新 leaf 不允许写 `Next Action Or Recommended Skill` 引用其它 hf-* canonical ID）
  - **现有 24 个 leaf skill 的内容不被修改**——它们当前仍写有 `Next Action Or Recommended Skill` 字段、对其它 hf-* 的硬引用、对 `hf-workflow-router` 的 authority 让渡声明等；这些**保留为兼容期遗产**，不立即触发"违反 invariant"的判定
- **v0.7.0+ 范围内**（D3 Step 2–5 完成后），D1 升级为**运行时强制**（runtime enforcement）：
  - leaf 中所有对其它 hf-* 的硬引用被剥离
  - `Next Action Or Recommended Skill` 字段从必填变为可选再到删除
  - 此时 Layer 1 / Layer 2 互不引用成为可被审计的物理事实
- **D3 Step 6 完成后**（建议 v0.8.0+），`skills/using-hf-workflow/` 与 `skills/hf-workflow-router/` 物理删除，Layer 3 unique authoritative

**这意味着**：v0.6.0 范围内做 `hf-design` 的 dispatch 协议设计时，应**按目标态**（runtime enforcement）设计 orchestrator persona 的派发逻辑（不依赖 leaf 的 `Next Action` hint，纯靠 on-disk artifacts），但**实施时**允许在兼容期内同时消费 leaf 残留的 `Next Action` 字段作为辅助 hint（不强制 leaf 提供）。

### Decision 2 — Single source of truth：`agents/hf-orchestrator.md`；FSM / dispatch protocol 物理迁移到 `agents/references/`

引入新的仓库根目录 `agents/`，作为 agent persona 的 single source of truth。

**v0.6.0 范围内**：
- 仓库根 `agents/hf-orchestrator.md`：orchestrator agent persona 主文件，合并自 `using-hf-workflow` + `hf-workflow-router` 的等价改写
- 仓库根 `agents/references/`：progressive disclosure 子目录，承接来自 `skills/hf-workflow-router/references/*.md` 的内容（FSM 转移表、reviewer dispatch protocol、reviewer return contract、profile selection guide、execution semantics、ui-surface activation、routing-evidence-guide / examples）
- 旧位置 `skills/hf-workflow-router/references/*.md`：保留 redirect stub，body 指向新位置（避免外部教程链接 404）

**与 ADR-006 D1 4 类子目录约定的关系**：
- `agents/` 与 `agents/references/` 是**新引入**的目录类别，**不属于** ADR-006 D1 描述的 skill anatomy（`SKILL.md` + `references/` + `evals/` + `scripts/`）；它们是 agent persona anatomy，不与 skill anatomy 互相替代
- `audit-skill-anatomy.py` 不扫描 `agents/`（脚本只扫 `skills/<name>/SKILL.md`），无须修改
- 后续如需为 agent persona 引入审计工具（如 `audit-agent-anatomy.py`），由后续 ADR 决定；本轮不做

### Decision 3 — 6 步落地路径（spec 阶段锁定，从安全到激进）

完整解耦的实施分 6 个 step，每个 step 可独立 review / 独立 release：

| Step | 内容 | 范围归属 |
|---|---|---|
| **Step 1** | 建 `agents/hf-orchestrator.md` + `agents/references/`，把 `using-hf-workflow` + `hf-workflow-router` 内容合并做等价改写；建 3 宿主 always-on stub 同步；旧 skill 文件转 deprecated alias（FR-004） | **本轮 v0.6.0 范围**（features/001-orchestrator-extraction） |
| **Step 2** | 把 leaf skill 的 `Next Action Or Recommended Skill` 字段从**必填**降为**可选**（兼容期）；orchestrator 同步支持"无 Next Action 字段时基于 on-disk artifacts 自行决定" | 不在本轮；后续 increment（建议 v0.6.1 / v0.7.0） |
| **Step 3** | 把 leaf skill 的 Hard Gates 显式分类标注 `[SOP]` / `[Workflow]`；先打标签不删 | 不在本轮 |
| **Step 4** | 把 `[Workflow]` 类 Hard Gate 物理上提到 orchestrator persona；从 leaf 里删掉 | 不在本轮 |
| **Step 5** | 删除 leaf skill 里所有对其它 hf-* 的硬引用（reviewer return contract / handoff schema 等），统一收到 orchestrator side | 不在本轮 |
| **Step 6** | 物理删除 `skills/using-hf-workflow/` 与 `skills/hf-workflow-router/` 这两个 deprecated skill 文件；同步 README / setup docs / plugin manifest | 不在本轮；建议 v0.7.0（延续 ADR-001 D1 "narrow but hard" 一次只动一类） |

**v0.6.0 只做 Step 1**——这是落地路径的最小安全单元，不破坏任何 leaf skill 行为。

### Decision 4 — `using-hf-workflow` / `hf-workflow-router` 兼容期保留为 deprecated alias

v0.6.0 范围内**不删除** `skills/using-hf-workflow/` 与 `skills/hf-workflow-router/`。两个目录及其 SKILL.md 仍存在，但 SKILL.md 内容用最小 redirect stub 替换：

- frontmatter `description` 含 "deprecated alias, see agents/hf-orchestrator.md" 字样
- body ≤ 30 行（C-006 约束）；含明确的 redirect 指引到 `agents/hf-orchestrator.md`
- 旧 references 文件（`skills/hf-workflow-router/references/*.md`）同步转 redirect stub，指向 `agents/references/*.md` 新位置

**与 ADR-001 D1 "narrow but hard" 的关系**：本决策严格遵循该立场——一次只迁移到新位置，不立即物理删除；外部教程链接 / search engine cache / 第三方教程不出现 404 体验；物理删除推迟到 Step 6（v0.7.0）。

### Decision 5 — Release-Blocking 假设清单（HYP-002 + HYP-003）

`features/001-orchestrator-extraction/spec.md` § 4 列出 7 条 Key Hypotheses，其中 2 条标 `Blocking? = 是`：

- **HYP-002**：抽出 orchestrator 后，HF 的 reviewable artifact 产出率不下降——通过 walking-skeleton 回归测试验证
- **HYP-003**：Orchestrator agent persona 能在 3 个支持宿主可靠加载——通过 3 宿主 smoke test 验证

这 2 条假设的验证发生在 `hf-test-driven-dev` 阶段；spec 通过评审**不要求**已被验证。但本 ADR 锁定：**v0.6.0 release 通过 `hf-completion-gate` 前，这 2 条假设必须有 fresh evidence 通过**——失败则触发 v0.6.0 回滚（不发 release，回到 spec / design / implement 修订），不允许"知其失败仍发布"。

### Decision 6 — 与 v0.6+ 5 项 ops/release skill 的关系（ADR-005 D7 立场延续）

ADR-005 D7 把 5 项 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）漂移到 v0.6+ 路线图。本 ADR 锁定：

- 这 5 项 skill **不在 v0.6.0 范围**；v0.6.0 范围严格限定为 features/001-orchestrator-extraction
- 这 5 项 skill 在 v0.6.x / v0.7.x 引入时，**必须**遵循本 ADR D1 的三层架构 invariant（直接作为独立 SOP 引入，不允许新引入对 router transition map 的硬引用）
- `hf-debugging-and-error-recovery` 在 ADR-003 / ADR-004 / ADR-005 中也被列为 deferred；本 ADR 不变更其 deferred 状态

### Decision 7 — Personas 不在本轮扩张（discovery § 11 Opportunity B 延后）

ADR-003 D1 / ADR-004 D2 / ADR-005 D7 已经把 3 项 specialist personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）漂移到 v0.6+。本 ADR 锁定：

- v0.6.0 范围内 `agents/` 目录**只**含 `hf-orchestrator.md` 一个 persona
- `agents/specialist/`（或等价子目录）的引入由后续 ADR 决定；本轮不预设位置
- discovery § 11 Opportunity B（更多 specialist personas）作为 later idea 保留；不阻塞本轮

## 不做（明确边界）

承接 spec § 6.2 + § 7：

- 不修改 24 个 leaf skill 的内容（除 D4 把 `using-hf-workflow` / `hf-workflow-router` 转 deprecated alias 外）
- 不修改 closeout pack schema、reviewer return verdict 词表、`hf-release` skill 行为
- 不修改 `audit-skill-anatomy.py` 行为、`hf-finalize` step 6A HTML 渲染、ADR-006 D1 4 类子目录约定
- 不新增任何 `hf-*` skill；保持 24 个不变
- 不引入新 slash 命令；保持 7 条不变
- 不针对第三方生态独立消费 leaf skill 的能力做投入
- 不引入 specialist personas；保持 `agents/` 只有 1 个 orchestrator
- 不做部署 / 监控 / 回滚 / 安全加固 / 性能 gate / 依赖弃用迁移 / 调试与错误恢复——延续 ADR-001 D1 / ADR-005 D7 立场

## 风险与未决问题

### 接受的工程风险

- **R1**：3 宿主中任一宿主无法稳定 always-on 加载 `agents/hf-orchestrator.md`——通过 HYP-003 verification 在 implement 阶段拦截；失败则 v0.6.0 不发布。
- **R2**：`agents/hf-orchestrator.md` 主文件 token 量超出现状组合 × 1.10——通过 NFR-002 acceptance 在 implement 阶段拦截；失败则继续拆 references 直到合规，不允许放任 token 膨胀。
- **R3**：`.claude-plugin/plugin.json` schema 不支持 `alwaysActive` 等价字段——降级到 `CLAUDE.md` always-load（C-005）；不阻塞本轮。

### 留给后续节点的开放问题（非 ADR 决策范畴）

- 命名细节、references 子目录结构细节、walking-skeleton diff 脚本归属位置——见 spec § 13 OQ-N-001 至 OQ-N-005；由 `hf-design` / `hf-tasks` 阶段决定。
- Step 2–6 各自的范围拆分细节、是否合并为更少的 increment、与 v0.6.x patch / v0.7.0 minor 的对齐时序——本 ADR 不预设；每个后续 increment 立项时另起 ADR-008 / ADR-009 / ... 决策。

## 与既有 ADR 的关系

| ADR | 决策点 | 本 ADR 的关系 |
|---|---|---|
| ADR-001 D1 | "P-Honest, narrow but hard" | **延续**：本轮严格停在 v0.6.0 单 feature 范围；不扩到 ops/release/monitoring |
| ADR-002 D11 | reviewer return verdict 词表 | **不冲突**：本轮不动 verdict 词表；orchestrator 派发 reviewer 时使用既有词表 |
| ADR-003 D2 | Cursor 加入第三个官方宿主 | **延续**：本轮 always-on stub 同时覆盖 Cursor / Claude Code / OpenCode 三宿主，与 ADR-003 客户端范围一致 |
| **ADR-004 D3** | **`hf-release` standalone，不进 router transition map** | **关键先例**：本 ADR D1 把 ADR-004 D3 的 standalone-skill-from-router 解耦能力**下放**到 coding family——不再只是 release tier 的特例，而是 HF 全部 skill 的架构 invariant |
| ADR-005 D4 / D7 | v0.5.0 立场（不动其它 skill）；5 项 ops/release skill 漂移到 v0.6+ | **延续**：本 ADR D6 锁定 v0.6+ 引入这 5 项 skill 时必须遵循新三层架构 invariant |
| ADR-006 D1 | 4 类子目录 skill anatomy（`SKILL.md` + `references/` + `evals/` + `scripts/`） | **不冲突**：`agents/` 是新引入的 agent persona 目录类别；不属于 skill anatomy 范畴；`audit-skill-anatomy.py` 对 `agents/` 透明 |

## 影响范围

- **新增**：`agents/hf-orchestrator.md`、`agents/references/*.md`、`features/001-orchestrator-extraction/`、`docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`（本文）、3 宿主 always-on stub 文件（`CLAUDE.md` / `AGENTS.md` 仓库根；`.cursor/rules/harness-flow.mdc` 已存在但内容更新）
- **修订**：`README.md` / `README.zh-CN.md` 顶部 Scope Note；`docs/cursor-setup.md` / `docs/claude-code-setup.md` / `docs/opencode-setup.md`；`.claude-plugin/plugin.json`（注册 orchestrator agent）；`.claude-plugin/marketplace.json`（描述同步）；`SECURITY.md` Supported Versions；`CONTRIBUTING.md` 引言版本号；`CHANGELOG.md` `[Unreleased]` 段；`.cursor/rules/harness-flow.mdc` body
- **转 deprecated alias**：`skills/using-hf-workflow/SKILL.md` + 同目录 references；`skills/hf-workflow-router/SKILL.md` + 同目录 references
- **不动**：24 个 hf-* skill 的内容；`hf-release` 行为；closeout pack schema；reviewer verdict 词表；`audit-skill-anatomy.py` 行为；`hf-finalize` step 6A HTML 渲染；`scripts/render-closeout-html.py`（v0.5.1 已迁到 `skills/hf-finalize/scripts/`）

## 评审与签字

| 节点 | 状态 | 路径 |
|---|---|---|
| `hf-discovery-review` | 通过（2026-05-10） | `docs/reviews/discovery-review-hf-orchestrator-extraction.md` |
| `hf-spec-review` | 待派发 | `features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md` |
| `hf-design-review` | 待 hf-design 阶段 | `features/001-orchestrator-extraction/reviews/design-review-YYYY-MM-DD.md` |
| `hf-tasks-review` | 待 hf-tasks 阶段 | `features/001-orchestrator-extraction/reviews/tasks-review-YYYY-MM-DD.md` |

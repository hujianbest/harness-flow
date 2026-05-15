# ADR-008 — OMO-Inspired Roadmap v0.6 Onwards

- 状态: accepted（2026-05-13，架构师在本会话拍板 D1~D7 + 删除 v0.8）
- 日期: 2026-05-13
- Feature: `features/002-omo-inspired-v0.6/`
- 决策者: 架构师（user）拍板路线图与 7 项关键取舍；cursor cloud agent 落 ADR
- 关联 ADR:
  - ADR-001 ~ ADR-006（v0.1.0 ~ v0.5.1 的范围 ADR）—— 本 ADR 是 v0.6 起的下一个范围锚点
  - ADR-009（同会话）—— Execution Mode fast lane 治理（D3 + D4 的 reconciliation）
  - ADR-010（同会话）—— `harnessflow-runtime` sidecar 边界（D1 + D2 的落地约束）
- 关联 soul / principles:
  - `docs/principles/soul.md`：HF 目标 = "从一个 idea 到产品高质量落地"；用户是架构师、HF 是工程团队
  - `docs/principles/methodology-coherence.md`：方法论之间的协作与冲突地图

## 1. Context

2026-05-13 架构师在本会话给 HF 提出参照 [Oh My OpenAgent (OMO) `code-yeongyu/oh-my-openagent`](https://github.com/code-yeongyu/oh-my-openagent) 的实现进一步开发的诉求。本 cloud agent 完成对 OMO 仓库的实质阅读（不仅 README + manifesto，还包括 `src/index.ts` 7 步初始化 / `src/agents/` 11 agent + dynamic prompt builder / `src/hooks/` 52~59 hook 的 5-tier 组合 / `src/tools/hashline-edit/` 24 文件 hash-anchored 编辑实现 / `src/features/team-mode/` 13k LOC 并行多 agent / `src/features/builtin-skills/` / `src/mcp/` / `docs/guide/orchestration.md`），与 HF 当前形态对比后形成"OMO 机制 → HF 移植可行性矩阵"，并由架构师在本会话给出 7 项决策 + 1 项额外约束（删除 v0.8）。

HF 与 OMO 在 *形态* 上是两层东西：HF 是纯 Markdown skill pack（24 个 `hf-*` + `using-hf-workflow`），跨三客户端（Claude Code / OpenCode / Cursor）通用；OMO 是 OpenCode-only 的 TypeScript/Bun 插件（1304 源文件 / 278k LOC / 11 agent / 52~59 hook / 16 tool 目录）。两者并不互斥——OMO 在 *执行层* 减少打断，HF 在 *方向层* 拒绝偷偷做主，组合起来才能覆盖完整的 agent harness。

本 ADR 的任务是把"v0.6 起 HF 怎么发展"锁成可执行的范围约束，避免后续会话凭印象偏移。

## 2. Decision

### D1：路线图分 4 个版本节奏，**显式删除 v0.8（工程化末段）**

| 版本 | 主题 | 是否需要 runtime |
|---|---|---|
| **v0.6** | Author-side discipline 升级（纯 markdown，无 runtime 依赖） | 否 |
| **v0.7** | 可选 runtime sidecar `harnessflow-runtime`（落地为 OpenCode plugin，见 ADR-010） | 是 |
| **v0.9** | 客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro） | 否（runtime 在 v0.9 客户端中可选挂载） |
| **v1.0** | 商用级形态收尾（v0.9 全客户端验证 + runtime 自身可观测 + 非 toy `examples/`） | 否 |

**v0.8 工程化末段（部署管线 / 可观测 / 事故响应 / 度量回流 / 上线后运维 / 性能 gate / 安全 hardening / 调试与错误恢复 / 弃用与迁移）**：删除，**不再列入 HF 路线图**。

理由：架构师认为这一段超出 HF 当前的核心价值面，与"HF 是方法论 + 轻运行时"的定位不匹配；既有 README 与 soul.md 早已用 "scope footnote" 显式承认这一段缺位，本 ADR 把"承认缺位"升级为"主动决定不做"。

**对 README / soul.md 的影响**：现有"v0.6+ 计划 `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / etc."的"未来计划"措辞需要在 v0.6 文档刷新中改为"显式 out-of-scope"。具体改动落在 v0.6 第一个 doc-freshness gate 中。

**Reversibility**：中（如果 HF 用户基数显著扩大并出现"必须有 release/ops 节点"的强信号，可以在 v1.0 之后单独开 ADR 重新评估，但本 ADR 立场是"HF 不应假装是部署工具"，与 ADR-004 D7 / ADR-005 D9 一脉相承）。

### D2：v0.6 范围 = 7 项 author-side / wisdom-accumulation 改造（纯 markdown）

按"对 HF soul 收益最高 / 改动复杂度最低"排序：

| 改动 | 类型 | 关键产出 |
|---|---|---|
| **新增 `hf-wisdom-notebook`** | 新 skill | `skills/hf-wisdom-notebook/SKILL.md` + `references/notebook-schema.md`（5 文件强 schema：`learnings.md` / `decisions.md` / `issues.md` / `verification.md` / `problems.md`，对应 D7 = A） |
| **升级 `hf-tasks-review` 引入 Momus 4 维 + 有限重写循环** | 修改 skill | 新增 `references/momus-rubric.md`（Clarity / Verification / Context / Big Picture，阈值 100% / 80% / 90% / 0% / 0%）；在 `SKILL.md` 引入 `verdict: rejected-rewrite` 的 N 次循环上限（建议 N=3） |
| **新增 `hf-gap-analyzer`**（D6 = A：author-side self-check，**不是** Fagan review 节点） | 新 skill | `skills/hf-gap-analyzer/SKILL.md` + `references/gap-rubric.md`；输出 `<artifact>.gap-notes.md`，作者吸收后再提交对应 review |
| **升级 `hf-specify` 引入显式 Interview FSM** | 修改 skill | 5 状态机（Interview ↔ Research ↔ ClearanceCheck → PlanGeneration），每次状态切换写 `spec.intake.md`，长会话被打断后可从工件恢复"问到第几个澄清问题了" |
| **新增 `hf-context-mesh`** | 新 skill | 对应 OMO `/init-deep`：给宿主项目按目录层级生成 `AGENTS.md`，HF 自身的 `docs/principles/` 不动 |
| **升级 `hf-workflow-router` 加入 step-level recovery + category hint** | 修改 skill | `transition-map` 加入"从 `tasks.progress.json` 恢复 task 内 RED/GREEN 步级进度"的能力；handoff 增加 `category_hint` 字段供下游 host 路由模型（不强制，host 不支持时直接忽略） |
| **升级 `hf-code-review` 的 AI slop 子章节为可执行 rubric** | 修改 skill | 引入 OMO `comment-checker` 已经验证过的禁用模式列表（`simply` / `obviously` / `clearly` / em-dash / 解释性自然语言注释等），写成 host 可 grep 的 rubric |

**额外引入 `hf-ultrawork`（D4 = A）**：架构师显式 opt-in 的 fast lane skill，**单独由 ADR-009 治理**，不与上述 7 项混合。

**v0.6 skill 总数**：24 → **27**（新增 `hf-wisdom-notebook` / `hf-gap-analyzer` / `hf-context-mesh`）+ **1**（`hf-ultrawork`，由 ADR-009 单独治理）= **28** + `using-hf-workflow`。

**Slash 命令面**：v0.6 不增加 slash 命令；`hf-ultrawork` 通过 `using-hf-workflow` 的 entry bias 表 + auto mode 触发，不做 `/ultrawork` 命令以避免与 `/hf` 默认入口竞争。

**Alternatives considered**：
- A1：v0.6 同时落地 v0.7 runtime —— 拒绝。runtime 是 OpenCode-only 深绑定（D2 = B），与 v0.6 的"三客户端通吃"诉求不在同一时间线，混做会绑定过早。
- A2：v0.6 只做 `hf-wisdom-notebook` 一项，其它 6 项推到 v0.6.x patch —— 拒绝。架构师诉求是"完整推进"，单项 release 切片过细，且 7 项之间存在协同（如 router transition map 升级要消费 wisdom notebook 摘要）。

**Reversibility**：高（每一项改动都是新增 skill 或 skill 内增量，不破坏现有 24 skill 的 contract；任一项失败可单独 revert）。

### D3：v0.7 runtime 形态 = OpenCode plugin（参照 OMO 写 TypeScript/Bun，不走 MCP server 通用形态）

架构师 D2 = B：runtime sidecar **不**做"单一 MCP server 三客户端通吃"，而是直接像 OMO 那样写 OpenCode plugin（TypeScript/Bun）。

**理由**：
- D1 = A 已经决定做 runtime；D2 = B 进一步选择"深度 over 广度"
- OMO 已经验证过 OpenCode plugin 形态可承载 hashline-edit / hooks / multi-agent orchestration 的全部需求，参照实现成本可控
- HF 跨客户端可移植性的 moat 由 v0.6 markdown 包承担，runtime 是 *opt-in* 增强，不需要也覆盖三客户端
- MCP server 路径在 hashline-edit 这类需要"Read 输出加 hash 戳"的场景里，需要重写客户端 Read tool 才能挂上 hash 增强 hook；OpenCode plugin 直接接管原生 Read，复杂度低得多

**v0.7 runtime 范围**：详见 ADR-010。这里只锁定形态决策。

**Reversibility**：低-中（一旦 v0.7 runtime 落地为 OpenCode plugin，三客户端不能共享；如果未来 Cursor / Claude Code 也提供等价 plugin API，可以再开 ADR 决定是否补做对应客户端 plugin，但 MCP server 形态不会再被回头采纳）。

### D4：D3 + D4 = A 引入"不停下来"的 ultrawork fast lane，由 ADR-009 单独治理

架构师 D3 = A：引入 Boulder Loop / Todo Enforcer（"不做完不停"机制）。
架构师 D4 = A：提供 `ultrawork` fast lane（架构师显式 opt-in 时跳过部分中间确认）。

这两项与 `docs/principles/soul.md` 第一条硬纪律（"方向、取舍、标准不清时，默认是停下来澄清，而不是选一个看起来合理的方向继续推进"）有显性张力。

**化解方式**：
- D3 + D4 的引入 **永远不是默认行为**，必须由架构师通过 Execution Mode preference（`auto mode` / `ultrawork`）显式开启
- 即便开启，**Fagan author/reviewer 分离与硬门禁不可绕过**——ultrawork 只能压缩"中间状态确认"，不能替代独立 review 与 gate verdict
- 引入 `hf-ultrawork` skill 作为 fast lane 的承载节点，由 `using-hf-workflow` 在识别到 architect-explicit `auto mode` + 任务集中度足够时 direct invoke

详细治理边界见 ADR-009。

### D5：D5 = A 仅允许并行 *探查 / 研究*，不并行 *实现*

架构师 D5 = A：允许并行探查 / 研究，但**禁止并行实现**。

**理由**：
- 并行探查（多个 explore / librarian / 文档检索同时跑）不动工件，安全收益高
- 并行实现需要 OMO 的 worktree + team-mode 机制，与 HF "一个 Current Active Task" 核心纪律直接冲突
- HF 永远不实现 OMO 的 team-mode（lead + 8 member + mailbox + tasklist + 多 worktree）

**落地节点**：v0.6 不增加任何并行机制；v0.7 runtime 提供 `parallel_explore` 工具（OpenCode plugin 内的 `delegate-task` 等价物），由 `hf-design` / `hf-tasks` / `hf-test-driven-dev` 在需要时调用，调用方负责把并行结果收敛回工件。

### D6：D6 = A `hf-gap-analyzer` 是 author-side self-check，**不是** Fagan review 节点

架构师 D6 = A：`hf-gap-analyzer` 是作者侧自查，verdict 仍由现有 review 节点给。

**理由**：
- 维持当前 8 个 Fagan review 节点的拓扑稳定（`hf-discovery-review` / `hf-spec-review` / `hf-design-review` / `hf-ui-review` / `hf-tasks-review` / `hf-test-review` / `hf-code-review` / `hf-traceability-review`）
- author-side self-check 拦截"作者忘了写下来的隐含意图"，把已知的低级遗漏在提交 review 前消灭，提升 review 节点的实际信噪比
- 不增加 review 节点拓扑复杂度，不破坏 Fagan separation

**落地约束**：`hf-gap-analyzer` 输出 `<artifact>.gap-notes.md`，作者读完吸收后**必须**手动确认"已吸收 / 已驳回某条"，再提交对应 review；review 节点会读 gap-notes 作为 review 的辅助上下文（不替代 review 自己的 rubric）。

### D7：D7 = A wisdom notebook 走 5 文件强 schema

架构师 D7 = A：`hf-wisdom-notebook` 用 5 文件强 schema，机器可消费。

**Schema**（落 `features/<f>/notepads/`）：

| 文件 | 内容 |
|---|---|
| `learnings.md` | 模式 / 约定 / 已验证可行的做法 |
| `decisions.md` | 架构性选择与理由（轻量 ADR，不替代 `docs/decisions/` 仓库级 ADR） |
| `issues.md` | 已知的问题、阻塞、gotcha（含 status: open / resolved / deferred） |
| `verification.md` | 测试结果、validation outcome、跨 task 的 evidence 摘要 |
| `problems.md` | 未解决的 issue、技术债、需要后续 task 处理的项 |

**写入时机**：
- `hf-test-driven-dev` 完成一个 task 后**必须**写 notebook delta（至少 `learnings.md` / `verification.md` 任一）
- `hf-workflow-router` 在选下一个 Current Active Task 时把 notebook 摘要注入下游 handoff
- `hf-finalize` 在 closeout pack 中引用 notebook 全集作为 evidence

**Schema 校验**：v0.6 引入 `scripts/validate-wisdom-notebook.py`（stdlib-only，与 `scripts/audit-skill-anatomy.py` 同等地位），用于 CI 与 hf-completion-gate 中的可选校验。

## 3. Consequences

**好的**：
- v0.6 把 OMO 在 *方法论层* 的所有可移植机制（Metis gap analysis / Momus rubric / Atlas wisdom / Prometheus interview FSM / `/init-deep`）全部吃下，HF 仍是纯 markdown 包，三客户端共享
- v0.7 runtime 把 host 没法可靠做的 hashline / evidence-bus / progress-store 三件事补齐，OMO 实测最大收益项（hashline 6.7% → 68.3%）落地
- D4 + D3 的 ultrawork fast lane 给"已经熟悉 HF 工作流且明确知道自己要什么"的架构师一条不被中间确认打断的快路径，但 Fagan + gate 不让步
- 删除 v0.8 让 HF scope 显式收敛，README / soul.md 的"未来计划"措辞改为"显式 out-of-scope"，停止给用户错误期望

**坏的 / 风险**：
- v0.7 runtime = OpenCode plugin 是 OpenCode-only 深绑定，Cursor / Claude Code 用户拿不到 runtime 收益（接受这个结果，由 v0.6 markdown 包覆盖）
- D3 + D4 引入的 ultrawork fast lane 会被部分用户误以为"可以跳过 review"，需要在 ADR-009 + `hf-ultrawork/SKILL.md` 中反复强调"Fagan + gate 不可绕过"
- v0.6 27 → 28 个 skill（含 `hf-ultrawork`）逼近 anatomy v2 的 token 预算上限（5 个 skill × 5000 tokens = 25000 共享预算），需要在 v0.6 design 阶段评估是否需要做 skill split / merge

**中性**：
- v0.9 客户端扩展时，4 个新客户端中只有支持 OpenCode plugin 等价物的才能挂 v0.7 runtime；其余客户端走纯 markdown 路径，能力差异需要在每个 setup 文档中明示
- v1.0 之前都不引入"非 toy examples/"以外的产品化承诺

## 4. Alternatives considered

- **A1：拒绝 D3 + D4，保护 HF soul 第 1 条硬纪律纯净度**
  - 拒绝原因：架构师在本会话明确选择 A，且诉求是"auto mode 完成不要中间停下来"。架构师有权改变标准（soul.md 第 23 行"用户是架构师"），ADR-009 的化解方式同时保留 Fagan + gate 不可绕过这条更深的纪律。
- **A2：v0.7 runtime 走 MCP server 三客户端通吃，而非 OpenCode plugin**
  - 拒绝原因：架构师 D2 = B。MCP server 形态在 hashline-edit 场景下需要重写客户端 Read tool，技术成本高且三客户端兼容性矩阵复杂。
- **A3：保留 v0.8 工程化末段，只是延后**
  - 拒绝原因：架构师明确"不做 v0.8 — 工程化末段"。HF 留在"方法论 + 轻运行时"定位更清晰。
- **A4：v0.6 只做 `hf-wisdom-notebook`，其余推到 v0.6.x**
  - 拒绝原因：见 D2 § Alternatives。

## 5. 路线图后续 ADR 计划

| 后续 ADR | 主题 | 触发时机 |
|---|---|---|
| ADR-009（同会话） | Execution Mode fast lane 治理（D3 + D4 reconciliation） | 本会话已写 |
| ADR-010（同会话） | `harnessflow-runtime` sidecar 边界 | 本会话已写 |
| ADR-011 | v0.6 range scope（按 hf-release 惯例，v0.6 release 时写） | v0.6 release |
| ADR-012 | v0.7 release scope + runtime 与 markdown 包的版本对齐策略 | v0.7 release |
| ADR-013 | v0.9 client expansion scope（每客户端能力矩阵） | v0.9 release |

## 6. Out of Scope（本 ADR 不决定的事）

- v0.6 每个 skill 的具体 SKILL.md 内容 → 由 `features/002-omo-inspired-v0.6/spec.md` + `design.md` 决定
- v0.7 runtime 的具体 tool 清单 → 由 ADR-010 + 后续 v0.7 feature spec 决定
- ultrawork fast lane 的具体触发条件 → 由 ADR-009 决定
- `hf-wisdom-notebook` notebook schema 字段细节 → 由 v0.6 design 阶段决定（本 ADR 只锁 5 文件，不锁字段）
- 既有 24 skill 中除 D2 列出的 5 项升级外，**不**做其它 skill 的修改

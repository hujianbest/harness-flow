# HF Orchestrator Extraction 产品发现草稿

- 状态: 草稿
- 主题: hf-orchestrator-extraction（把 workflow 编排从 leaf skill 里抽出来，下沉为独立 agent persona，让 leaf skill 回到 Anthropic Agent Skills 原始定位）
- 密度: `full`（对 HF 全局架构 invariant 的引入）
- 候选 Profile（仅作上游建议，最终由 router 决定）: `full`
- Current Stage: hf-product-discovery
- Next Action Or Recommended Skill: hf-discovery-review
- 关联立场: ADR-001 D1 / ADR-002 D1 / ADR-003 D2 / ADR-004 D2 / ADR-005 D7（"P-Honest, narrow but hard"）；ADR-004 D3（standalone skill 与 router 解耦先例）

> 本草稿不写正式规格，不替代 `hf-specify`。结论稳定到 `Bridge to Spec` 后由 `hf-discovery-review` 评审，再由 `hf-specify` 接管创建 `features/<NNN>-<slug>/`。

---

## 1. 问题陈述

HF 当前 24 个 `hf-*` skill 不是真正意义上的"独立 SOP"。每个 leaf skill 都嵌入了三类对其它 skill 的硬耦合：

1. **Authority 耦合**：leaf skill 在 SKILL.md 里显式声明"路由权属于 `hf-workflow-router`"、"跨 task 切换由 router 决定"，导致单独调用时 leaf skill 自己不知道何时收尾。
2. **Schema 耦合**：leaf skill 输出契约里有 `Next Action Or Recommended Skill`、`Pending Reviews And Gates` 等字段，这些字段只在 HF workflow 的下游消费者存在时才有意义；单独调用时是空摆设。
3. **Artifact 耦合**：leaf skill 假设 `features/<active>/progress.md` / `spec.md` / `design.md` / `tasks.md` 存在并已批准；缺一项就触发 hard gate，单独跑不通。

**Struggling moment**：使用者想从 `skills/hf-test-driven-dev/SKILL.md` 里复用 Two Hats / SUT Form / Refactor Note 这套方法论做一次 atomic TDD（比如修一个不在 HF feature 树里的 bug），却被迫先建 `features/<active>/`、跑完 `hf-specify` → `hf-design` → `hf-tasks` → 拿到 approval record，才能启动；或者干脆放弃用 HF。

**这与 Anthropic Agent Skills 原始定位（progressive disclosure / 自包含 SOP / description-driven 自动发现）有显著偏离**——参考 `addyosmani/agent-skills`（GitHub 37.5k stars）作为对照系：每个 skill 完全自包含，跨 skill 协作靠"软衔接"（description / When to Use / See Also）+ host agent 智能 + 7 条 slash 命令薄包装。

## 2. 目标用户与使用情境

| 角色 | Situation | 当前状态 |
|---|---|---|
| **HF 终端使用者** （工程师在 Cursor/Claude Code/OpenCode 里调 HF） | 想就一个具体子任务复用某个 hf-* skill 的方法论（如 TDD / design / code-review），任务本身规模不到要走完整 HF workflow | 当前必须建完整 feature 目录，或者"自行无视" hard gate（破坏纪律），或者放弃用 HF |
| **HF 终端使用者** （同上） | 想跑长任务自动开发（idea → closeout 全自动）| 当前可用，但 leaf skill 内部混入大量编排逻辑，使用体验臃肿 |
| **HF 维护者**（包括我们） | 想新增一个 skill 或修改一个 skill | 当前需要同时考虑"作为编排节点的契约"+"作为 SOP 的内容"，每次修改都跨两个关注点 |
| **第三方生态使用者** | 想把 HF 的某个 SOP（如 `hf-design` 的 DDD 战术映射）单独装到自己的非 HF 项目里 | 当前不可行：skill 文件强引用 HF 其它节点 |

## 3. Why now / 当前价值判断

- **生态对照系成熟**：`addyosmani/agent-skills` 把"独立 SOP + 软衔接"模型跑到 37.5k stars 量级，证明该方向在生态里被广泛接受；HF 当前与之的差异（FSM 集中编排 vs 去中心化）已经足以被使用者直接感受到。
- **HF 自身已有 standalone 先例**：`hf-release`（v0.4.0 ADR-004 D3）就是 standalone skill，**不进** router transition map。证明 HF 在架构上已经接受"部分 skill 独立于编排器"——但这种解耦目前只用在 release tier，没有下放到 coding family 的 leaf。
- **耦合代价已显化**：v0.5.0 / v0.5.1 的 patch release 集中在 `hf-finalize` 一个 skill 上，但仍要在 SKILL.md 里同步 step 6A / Hard Gate / Verification 等多处分布式契约——这是耦合带来的修改面放大。
- **客户端机制已就位**：Cursor `.cursor/rules/*.mdc` 的 `alwaysApply` / Claude Code `CLAUDE.md` / OpenCode `AGENTS.md` 三种 always-on 注入机制都已稳定，"orchestrator agent 自动加载"在工程上没有阻塞。
- **当前是合适窗口**：v0.5.x 系列已经稳定（patch release 验证通过），下一个 minor v0.6.0 是合适的扩张窗口；再往后 skill 增多（v0.6+ 计划补 `hf-shipping-and-launch` 等 5 项）耦合面只会更难拆。

切换型主题（push / pull / anxiety / habit）：

| 力 | 内容 |
|---|---|
| **Push**（让人离开现状的力） | leaf skill 单独不可调；维护时跨关注点；与生态主流 skill 模型偏离 |
| **Pull**（拉向新方案的力） | skill 真正独立可复用；与 Anthropic 原始定位对齐；可被第三方生态消费；维护时关注点分离 |
| **Anxiety**（迁移焦虑） | 担心拆出 orchestrator 后 long-task 自动化能力下降；担心 reviewer/author 分离纪律松动；担心 24 个 skill 的现有契约被破坏 |
| **Habit**（旧方案的惯性） | "在 leaf 里写 Hard Gate"已是 HF 模式；router transition map 已是熟悉决策位置 |

应对：方案设计必须显式回答这三类 anxiety，不能只讲 pull。见 section 6 的关键假设。

## 4. 当前轮 wedge / 最小机会点

**主 wedge（OST 主 opportunity）**：把 `using-hf-workflow` + `hf-workflow-router` 合并改写为一个**有状态的 orchestrator agent persona**（`agents/hf-orchestrator.md`），通过宿主 always-on 机制每个 session 自动加载；同时把 leaf skill 中"workflow 编排级"的 Hard Gate / 输出契约字段下沉到 orchestrator，leaf skill 只保留 SOP 级内容。

**当前轮**只交付架构 invariant + orchestrator 文件骨架（落地路径第 1–2 步）。**当前轮不交付**：完整迁移所有 24 个 leaf skill；删除 `using-hf-workflow` / `hf-workflow-router` 这两个旧 skill；新增任何 ops/release 类 skill。

## 5. 已确认事实

| 事实 | 来源 |
|---|---|
| HF 当前 24 个 hf-* skill + `using-hf-workflow` entry shell | `skills/` 目录直接清点 + `README.md` Scope Note |
| `using-hf-workflow` 自我定位为 public entry，把 runtime authority 上交给 router | `skills/using-hf-workflow/SKILL.md` § "本 skill 是 public entry，不是 runtime handoff" |
| `hf-workflow-router` 自我定位为 runtime authority，掌握 Profile / Mode / Workspace Isolation / FSM | `skills/hf-workflow-router/SKILL.md` § "HF workflow family 的 runtime authority" |
| Leaf skill 在自身 SKILL.md 里显式声明跨 task 切换归 router | `skills/hf-test-driven-dev/SKILL.md` 顶部 |
| `hf-release` 是 standalone skill，**不进** router transition map | `skills/hf-release/SKILL.md` + `docs/decisions/ADR-004-hf-release-skill.md` D3 |
| Cursor `.cursor/rules/harness-flow.mdc` 已通过 always-applied workspace rule 机制自动注入每个 session | 当前 session system prompt 中的 `<always_applied_workspace_rule>` 块直接证据 |
| Claude Code 支持 `CLAUDE.md` always-load + plugin manifest 注册 agent | `docs/claude-code-setup.md` |
| OpenCode 支持 `AGENTS.md` always-load + `.opencode/skills/` 软链接 | `docs/opencode-setup.md` |
| addyosmani/agent-skills 用"独立 skill + 7 条 slash 命令薄包装 + meta-skill 发现"模型，已在生态里被广泛采用 | https://github.com/addyosmani/agent-skills + 其 `using-agent-skills` / `agents/code-reviewer.md` 文件结构 |
| HF closeout pack schema、reviewer verdict 词表、`hf-release` 行为不应在本轮变动 | ADR-005 D4 / D5（v0.5.0 立场延续） |

## 6. 关键假设与风险

按 **Desirability / Viability / Feasibility / Usability** 分类：

### 6.1 Desirability（值不值得做）

| 假设 | 若不成立的后果 | confidence | probe 建议 |
|---|---|---|---|
| HF 使用者真的有"想单独调用一个 skill"的诉求 | 整个 wedge 无价值；只是维护者审美偏好 | **medium**：来自与用户对话 + 生态对照系，但缺独立量化数据 | 翻 GitHub issues / discussions / 任何 feedback 渠道，找"无法单独使用 skill"的诉求记录；若无证据，向社群发起小规模问询 |
| 第三方生态愿意复用 HF 的 SOP 子集 | 维护成本上升，但实际无外部消费者 | **low**：当前没有显式信号 | 暂列为 later，不阻塞本轮 wedge |

### 6.2 Viability（HF 项目层面值不值得做）

| 假设 | 若不成立的后果 | confidence | probe 建议 |
|---|---|---|---|
| 抽出 orchestrator 后，HF 的"reviewable artifact production rate"（North Star）不下降 | 重构损伤 HF 核心价值 | **medium-high**：编排逻辑物理位置变了但语义不变；理论上等价改写 | walking-skeleton 回归：用新 orchestrator 跑 `examples/writeonce/features/001-walking-skeleton/` 应产出相同 closeout pack |
| 重构 ROI 大于成本 | 中期内 HF 维护成本上升而无外部收益 | **medium**：当前架构已能跑长任务，重构纯属内功 | 在 spec 阶段量化重构面（多少行 leaf SKILL.md 改动）和预期收益（leaf 平均行数下降比例） |

### 6.3 Feasibility（技术上做不做得到）

| 假设 | 若不成立的后果 | confidence | probe 建议 |
|---|---|---|---|
| Orchestrator agent persona 能在 3 个支持的宿主（Claude Code / OpenCode / Cursor）里通过 always-on 机制可靠加载 | 长任务自动化能力丧失，等于退回到 addyosmani 模式 | **high**：Cursor 当前 session 已直接证明；Claude Code / OpenCode 文档支持 | step 1 完成后，在 3 个宿主各跑一次"新建 session → orchestrator 自动 act as persona"的 smoke test |
| FSM 转移表 + reviewer dispatch 协议从分布在多个 references 文件，集中到 orchestrator agent 后仍能 progressive disclosure（不撑爆 token 预算） | 每个 session 都付高额 token 成本 | **medium-high**：可以把转移表 / 协议拆到 `agents/references/` 按需加载，参照 `hf-workflow-router/references/` 的现有做法 | 在 design 阶段量化：orchestrator 主文件目标 ≤ 300 行，references 按 progressive disclosure 加载 |
| Leaf skill 从"`Next Action` 必填 + 引用其它 hf-*"改为"自包含输出 verification" 后，编排 agent 仍能基于 on-disk artifacts 决定下一步 | 编排 agent 失去 hint，必须每轮重新扫整个 features 树 | **medium**：理论上 progress.md + 工件本身就足够；但当前 router 实际依赖 `Next Action` 字段做归一化（router § 6） | 在 design 阶段定义"orchestrator 如何在没有 Next Action 字段的情况下做证据归一化"——这是 spec/design 的核心问题之一 |
| Reviewer/Author 分离（Fagan）在 orchestrator-side dispatch 下仍可强制 | 质量纪律松动 | **high**：dispatch 机制本身就在 router，搬到 orchestrator 是物理位置变化不是语义变化 | 不需要单独 probe；spec 里显式列为 invariant |

### 6.4 Usability（使用者侧好不好用）

| 假设 | 若不成立的后果 | confidence | probe 建议 |
|---|---|---|---|
| 使用者从"理解 HF = 理解 24 个 leaf skill 之间的 FSM"切换到"理解 HF = 1 个 orchestrator agent + 24 个独立 SOP"是认知负担下降 | 学习曲线没改善反而更陡 | **medium-high**：心智模型更平 | README / docs 改写后让若干使用者冷读，看能否在 5 分钟内说出"orchestrator vs SOP 二分" |
| 现有命令面（7 条 slash command）不需要扩张就能承接新模型 | 命令面爆炸 | **high**：addyosmani 用 6 条命令支撑了类似规模的 skill 集 | 在 spec 阶段把每条命令在新模型下的语义重写一遍验证 |

## 7. 候选方向与排除项

### 候选 A：Status Quo（什么都不做）

- **取舍**：维护成本最低；但与 Anthropic Agent Skills 原始定位偏离持续扩大；leaf skill 单独不可用的痛点不解决。
- **剪枝理由**：与已观察到的使用者痛点（section 1 struggling moment）冲突；与生态主流方向（addyosmani 模型）背离。**排除**。

### 候选 B：Dual-Mode Leaf Skills（每个 skill 加 Workflow / Standalone 双模）

- **形态**：每个 hf-* skill 内部增加 `## Modes` 段；Hard Gates 分级 `[SOP]` / `[Workflow]`；slash 命令加 `--standalone` flag。
- **取舍**：兼容性最好（router 不动）；但**把编排耦合从"集中在 router"改成"分散到每个 leaf"**，治标不治本；leaf skill 长度反而增长（引入 mode 判断逻辑）；与"skill 是独立 SOP"的目标背道而驰。
- **剪枝理由**：被对话中显式否决（"显得 skill 特别臃肿，做了太多适配"）。**排除**。

### 候选 C：Full Orchestrator Extraction（**主 wedge**）

- **形态**：建 `agents/hf-orchestrator.md` 作为 always-on agent persona；合并 `using-hf-workflow` + `hf-workflow-router` 内容；leaf skill 剥离编排级 Hard Gate 与 schema 字段；slash 命令成为 orchestrator 入口。
- **取舍**：架构最干净；leaf skill 真的独立；与 Anthropic / addyosmani 模型对齐；但实施面较大（涉及所有 leaf）；需要分多步走（先抽 agent 文件、再降级 leaf 字段、再删旧 skill）。
- **采用**。具体落地分步骤见 [`Bridge to Spec`](#12-bridge-to-spec)。

### 候选 D：Full Orchestrator Extraction + 同步删除旧 skill 文件

- **形态**：在候选 C 基础上，立刻物理删除 `skills/using-hf-workflow/` 和 `skills/hf-workflow-router/`。
- **剪枝理由**：违反 ADR-001 D1 的"narrow but hard"立场；外部教程链接立刻 404；不可恢复。应改为 v0.6.0 兼容期保留 + 内容 redirect，下一个 minor 删。**降级到 candidate C 的实施分步**。

### Later ideas（明确放入 parking lot，不进本轮）

- 给 `agents/` 增加更多 personas（reviewer 专家、debugger 专家），对照 addyosmani `agents/code-reviewer.md` 等
- 把 HF 的部分 leaf skill（如 `hf-design`）做成可被非 HF 项目独立装载的 npm-style 包
- 与 v0.6+ 计划的 `hf-shipping-and-launch` 等新 skill 协同设计——本轮先把现有 skill 解耦，新 skill 进来时就直接遵循新模型

## 8. 建议 probe / 验证优先级

| Probe | 对应假设 | 优先级 | 是否阻塞 spec |
|---|---|---|---|
| Walking-skeleton 回归：新 orchestrator 跑 `examples/writeonce/features/001-walking-skeleton/` 产出对照 | 6.2 "重构后 North Star 不下降" | P0 | **阻塞**：必须在 spec 阶段定义对照标准；实施时由 `hf-test-driven-dev` 做 |
| 3 宿主 always-on smoke test | 6.3 "orchestrator 可靠加载" | P0 | 可在 design 阶段并行；不阻塞 spec |
| Leaf skill 行数变化量化（取 3 个代表性 leaf：`hf-test-driven-dev` / `hf-design` / `hf-finalize`） | 6.2 "ROI 大于成本" | P1 | 不阻塞 spec；但要在 design 阶段给出预估 |
| 命令面新语义重写 | 6.4 "命令面无需扩张" | P1 | 不阻塞 spec |
| 翻 GitHub issues / discussions 找 standalone 诉求记录 | 6.1 "Desirability" | P2 | 不阻塞 spec；缺证据时降级为"基于生态对照系 + 维护者判断"的论据，spec 显式标注 |

正式 probe 工件（如需 hard probe）由 `hf-experiment` 接管；本草稿只列方向。

## 9. 成功度量（Desired Outcome / North Star / Success Metrics）

- **Desired Outcome**：HF 的 leaf skill 真正成为独立 SOP——单独调用任意一个 hf-* skill（除 review/gate 类）时无需 `features/<active>/` 存在、无需上游 approval record、无需写 `Next Action` 字段；同时 long-task 自动开发能力（idea → closeout）由 orchestrator agent 完整保留。
- **North Star 锚定**：HF 的 North Star 尚未形式化声明。本轮 outcome 与 README scope 中"reviewable artifact production rate"（可评审工件产出率）绑定——**重构不应降低**该速率。
- **Leading 指标**：
  - 改写后的 `hf-test-driven-dev` SKILL.md 行数 ≤ 当前的 60%（当前 ~239 行，目标 ≤ 145 行）
  - `agents/hf-orchestrator.md` 主文件 ≤ 300 行（progressive disclosure 到 `agents/references/`）
  - 改写后的 leaf skill 中"对其它 hf-* 名字的硬引用"减少到 0 处（仅在 `## See Also` 软提及不算）
- **Lagging 指标**：
  - Walking-skeleton 回归通过：新 orchestrator 跑 `examples/writeonce/features/001-walking-skeleton/` 产出与现状 byte-for-byte 等价的 closeout pack（允许时间戳和生成器路径差异）
  - 3 个支持宿主（Cursor / Claude Code / OpenCode）各跑一次"新 session → orchestrator 自动加载"smoke test 通过
- **Success Threshold（最小门槛，让我们承认 wedge 成功）**：
  - **必达**：walking-skeleton 回归通过 + 3 宿主 smoke test 通过 + `hf-test-driven-dev` SKILL.md 行数 ≤ 60%
  - **加分**：抽 3 个代表性 leaf 做行数对照，平均行数下降 ≥ 30%
- **Non-goal Metrics（本轮明确不追求）**：
  - 不追求缩短整体 coding workflow 总耗时
  - 不追求增加 HF 安装量 / star 数
  - 不追求覆盖 v0.6+ 计划的 5 个 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / 等）—— 本轮只动现有 24 个 hf-* + entry shell + router

## 10. JTBD 视图

**Job Story（HF 终端使用者，atomic 任务情境）**：

```text
When 我作为工程师在 Cursor / Claude Code / OpenCode 里遇到一个不需要走完整 HF
workflow 的子任务（比如就修一个 bug、做一次 atomic TDD、单独跑一次 design
review），现有 hf-* skill 文件里却写满了"必须先有 approved tasks.md / 必须写
Next Action / 必须经过 router"的硬约束，

I want to 直接复用 HF 的方法论精华（Two Hats / SUT Form / Refactor Note / DDD
战术映射 / Fagan 评审清单）做完那一个子任务，而不被强迫先建一整套 features/<NNN>/
目录、跑完 spec → design → tasks 上游链才能启动，

so I can 把 HF 当作"高质量工程方法论的 SOP 集合"来用，而不只是"长任务编排框架"——
长任务自动化能力可以在我明确表达"按 HF workflow 跑全程"时再启用。
```

**Struggling moment**：当我 `Read` 一份 hf-* SKILL.md 想"提炼方法论复用"，却看到 "本 skill 不是任务循环控制器"、"跨 task 切换由 hf-workflow-router 决定"、"必须存在已批准 tasks.md" 这类只在 HF workflow 内成立的语句，被迫在"破坏纪律单独跑"和"放弃用 HF"之间二选一。

**Job Story（HF 维护者，新增 / 修改 skill 情境）**：

```text
When 我要新增一个 skill 或修改现有 skill，

I want to 只关注"这个 SOP 怎么写得专业、怎么定义 verification 出口"，

so I can 不必同时考虑"它在 FSM 里的 transition 边、它的 Next Action 字段、它如何
被 router 归一化、它在 reviewer dispatch 里的位置"——这些应该归到 orchestrator
agent 一处维护。
```

切换型主题四力已在 section 3 列出。

## 11. OST Snapshot

```
Desired Outcome:
  HF leaf skill 真正成为独立 SOP；long-task 自动开发能力由 orchestrator 保留

  Opportunity A（**主**）：把"workflow 编排"和"skill SOP"物理分层
    Solution A1（**采用**）：建 agents/hf-orchestrator.md 作为 always-on agent
      persona，把 entry shell + router 的内容合并下沉；leaf skill 剥离编排级契约
      Assumption A1.1：orchestrator 可在 3 宿主 always-on 加载（→ probe P0 #2）
      Assumption A1.2：编排集中后仍能 progressive disclosure 控 token 预算
    Solution A2（**剪枝**）：每个 leaf 加 dual-mode（Workflow / Standalone）
      剪枝理由：把耦合从集中变分散，治标不治本；leaf 反而臃肿（用户已显式否决）
    Solution A3（**剪枝**）：什么都不做
      剪枝理由：偏离 Anthropic 原始定位的痛点持续扩大

  Opportunity B（次，本轮不做）：扩 agents/ 目录引入更多 specialist personas
    （reviewer 专家、debugger 专家，对照 addyosmani agents/code-reviewer.md）
    本轮不做的原因：先把核心 orchestrator 立起来；specialist personas 可在
    v0.6.x patch 或 v0.7.0 minor 增量引入，不阻塞当前 wedge

  Opportunity C（次，本轮不做）：把 leaf skill 做成可被非 HF 项目独立消费的包
    本轮不做的原因：先解决 HF 内部解耦，外部消费是衍生收益；ADR-001 P-Honest
    立场要求"narrow but hard"
```

## 12. Bridge to Spec

下面内容已经稳定到可作为 `hf-specify` 的输入，建议进入 `features/<NNN>-orchestrator-extraction/spec.md`：

### 12.1 范围边界（spec 必须覆盖）

- **架构 invariant**：HF skill 集合显式分为 3 层——Doer Skills / Reviewer & Gate Skills / Orchestrator Agent。Doer 与 Reviewer/Gate 之间互不引用；只有 Orchestrator 知道全图。
- **新增工件**：`agents/hf-orchestrator.md`（agent persona，**不是** skill；不进入 `audit-skill-anatomy.py` 扫描范围）；可选 `agents/references/` 子目录承接 progressive disclosure 内容。
- **每宿主 always-on 引导 stub**：Cursor 改 `.cursor/rules/harness-flow.mdc` 内容；Claude Code 加 `CLAUDE.md` 段或 plugin manifest 注册；OpenCode 改 `AGENTS.md` 段。**stub 内容只是 redirect 指针，不复制 persona 内容**。
- **Leaf skill 输出契约松绑**：`Next Action Or Recommended Skill` 字段从必填降为可选（兼容期）；最终（下一个 minor）删除。
- **Hard Gates 分类与下沉**：每个 leaf skill 的 Hard Gates 显式分 `[SOP]` / `[Workflow]`；`[Workflow]` 类物理上提到 orchestrator persona。
- **旧 skill 兼容期**：`skills/using-hf-workflow/` 与 `skills/hf-workflow-router/` 在 v0.6.0 保留为 deprecated alias（内容 redirect 到 orchestrator），**不立即删除**；删除留到下一个 minor。
- **保留不动**：closeout pack schema、reviewer return verdict 词表、`hf-release` skill 行为、`audit-skill-anatomy.py` 行为、`hf-finalize` step 6A HTML 渲染、24 hf-* 的核心 SOP 内容（DDD / TDD Two Hats / SUT Form / Fagan 等）。

### 12.2 已稳定可入 spec 的结论

- 解决方案选 **候选 C**（Full Orchestrator Extraction），不选 B（dual-mode）。
- 落地按 6 步分阶段，从安全到激进（建文件 → 字段降级 → Hard Gate 分级 → 编排级 Gate 物理上提 → 删 leaf 中的 hf-* 硬引用 → 删旧 skill 文件）；每步可独立 review / 独立 release。
- 第 1 步**只**做 orchestrator agent 文件骨架（合并 entry shell + router 内容做等价改写），**不**改任何 leaf skill；这是本轮 wedge 的最小可交付单元。
- North Star 锚定 / Success Threshold 已在 section 9 锁定，作为 spec 阶段 Success Criteria 的上游输入。
- 立 ADR-007（建议命名：`ADR-007-orchestrator-extraction-and-skill-decoupling.md`）作为本架构 invariant 的入档。
- 走 v0.6.0 minor release（与 v0.4.0 引入 `hf-release` 同档；不是 v0.5.x 的 patch 范畴）。

### 12.3 待 `hf-experiment` / 后续节点验证的假设

- Assumption 6.3 "orchestrator 在 3 宿主 always-on 可靠加载" → 实施后 smoke test
- Assumption 6.3 "leaf 剥离 `Next Action` 后 orchestrator 仍能基于 on-disk artifacts 决定下一步" → 这是 design 阶段核心命题；可能需要在 design 中设计一个最小"artifact → next-step"决策协议
- Assumption 6.2 "重构后 walking-skeleton closeout pack 对照通过" → 实施后回归验证

### 12.4 当前不进入 spec 的候选

- Opportunity B（更多 specialist personas）→ later
- Opportunity C（leaf skill 外部独立消费）→ later
- 候选 D（同步删除旧 skill 文件）→ 降级为本轮"兼容期保留 + 下个 minor 删"
- v0.6+ 计划的 5 个 ops/release skill 与本轮的协同设计 → 不在本轮 spec 范围；本轮只动现有 24 个 hf-* + entry shell + router

## 13. 开放问题

### 阻塞项（必须在评审前关闭）

- [ ] **是否在本轮把 `hf-workflow-router/references/*.md` 一并迁到 `agents/references/`？**
  - 候选答案 1：本轮迁（保持单源原则），rename 后旧路径 redirect
  - 候选答案 2：本轮不迁，先让 orchestrator 引用 `skills/hf-workflow-router/references/`，下一个 minor 再迁
  - **倾向**：候选答案 1。理由：单源原则比物理位置稳定更重要；reference 文件本身没有 schema 变化。
  - 留给 spec 阶段最终决策。

### 非阻塞项（可保留）

- 命名：`agents/hf-orchestrator.md` vs `agents/orchestrator.md` vs `agents/hf-workflow-orchestrator.md`——倾向第一个，但留 spec 决策。
- `agents/` 与 `.claude-plugin/agents/` 的关系：HF 项目根 `agents/` 是 single source of truth；plugin manifest 通过 `source: agents/...` 引用。
- README / 各 setup doc 的改写规模：本轮只在 Scope Note / Workflow Shape 加 v0.6.0 注解，等 step 1 实施完再做完整 sync。
- v0.6.0 release pack 走 `hf-release` 第 4 次 dogfood——延续 v0.4.0 / v0.5.0 / v0.5.1 节奏。
- 是否需要 `hf-experiment` 节点先做"orchestrator 加载 smoke test"作为 hard probe，还是直接放到 `hf-test-driven-dev` 阶段一并验证——倾向后者（smoke test 不需要独立 probe 工件），但留 spec 阶段决策。

---

## 状态同步

- 状态：草稿
- 当前 stage：`hf-product-discovery`
- Next Action Or Recommended Skill：`hf-discovery-review`
- Discovery 阶段 progress 与本草稿同文件，进入 feature 后由 `features/<NNN>-orchestrator-extraction/progress.md` 接管

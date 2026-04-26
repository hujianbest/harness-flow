# HarnessFlow 介绍

> 给团队里准备引入 HF 的架构师 / Tech Lead——一份偏理念与流程的内部介绍。
> 项目门面与命令矩阵看 [`README.zh-CN.md`](../README.zh-CN.md)；最高锚点的"宪法"看 [`docs/principles/soul.md`](principles/soul.md)。

HarnessFlow（下称 HF）是一套面向 AI Agent 的 skill pack，把"从一个 idea 到产品高质量落地"这件事翻译成结构化工件、独立评审和带门禁的执行节奏。它不是又一组 prompt，而是一条可回读、可恢复、可交付的工程链路。

本文按下列五节展开，建议按顺序读：

1. [HF 工作流的理念](#一hf-工作流的理念)
2. [零成本上手](#二零成本上手不用记任何命令)
3. [人与 Agent 的关系](#三人与-agent-的关系)
4. [如何保证质量](#四如何保证质量)
5. [Skills 设计原则](#五skills-设计原则)

---

## 一、HF 工作流的理念

### 1.1 唯一目标：从一个 idea 到产品高质量落地

HF 存在的唯一理由，是帮助用户把一个模糊的想法**完整、正确、可回读地**走到产品。其中"完整"指覆盖发现 → 规格 → 设计 → 任务 → 实现 → 评审 → 门禁 → 收尾的全链路；"正确"指每一步的结论都基于工件证据而不是聊天记忆；"可回读"指任意时刻别人接手都能仅凭仓库还原现场。

> 现状脚注：HF 当前一等阶段覆盖到工程级 closeout / CHANGELOG。**发布工程 / 部署管线 / 可观测 / 事故响应 / 度量回流** 等"可上线产品"末段能力按 `docs/todo/hf-staged-implementation-plan.md` 的 Phase 1+ 增量落地——任一段未落地时，HF 必须**显式抛回用户**决定如何替代或推迟，而不是悄悄把"代码合并"当成"上线"。

### 1.2 不只是流程，是把软件工程方法塞进了 skills 里

HF 与"再写一套 prompt 模板"的根本差别，是它把 **30+ 条经过验证的软件工程方法**显式装进对应节点的 skill 里，而不是依赖 agent 自己想起来用：

- **意图层**：EARS / BDD / MoSCoW / INVEST / ISO 25010 / Quality Attribute Scenarios / JTBD / OST / RICE / Kano 装进 `hf-product-discovery` 与 `hf-specify`
- **架构层**：DDD 战略 / DDD 战术 / Event Storming / C4 / ADR / ARC42 / 轻量 STRIDE / Clean Architecture + SOLID 装进 `hf-design`
- **执行层**：Canon TDD / Walking Skeleton / Two Hats / Fresh Evidence / Opportunistic + Preparatory Refactoring 装进 `hf-test-driven-dev`
- **评审层**：Fagan Inspection / ATAM / Structured Walkthrough / End-to-End Traceability 装进各 review skill
- **验证层**：Definition of Done / Evidence Bundle / Profile-Aware Rigor / Impact-Based Regression 装进三道门禁
- **收尾层**：Project Closeout（PMBOK）/ Release Readiness Review / Handoff Pack Pattern 装进 `hf-finalize`

每个 skill 的 `SKILL.md` 顶部都有一张 **Methodology 表**，显式写明"这个 skill 用了哪些方法、对应到 Workflow 的哪一步"。这不是装饰——它意味着用 HF 等于让 agent 按 Beck / Fowler / Evans / Cockburn / Nygard / Martin / PMBOK 的一线工程方法干活，而不是凭"我记得应该这样做"。

方法之间的分工、反替代规则、Phase × profile 激活矩阵单独沉淀在 [`docs/principles/methodology-coherence.md`](principles/methodology-coherence.md)；任何新方法引入都要先经过这份治理文档检验，避免方法堆砌退化成方法打架。

### 1.3 把工程纪律拆成一等阶段，而不是一个大 prompt

普通 agent workflow 的问题，是把"想清楚需要做什么"、"决定怎么做"、"动手做"、"判断有没有做对"压扁到一次推理里。HF 把它们拆成显式的、独立的节点：

- **Authoring 节点**（specify / design / tasks）只负责把模糊意图变成结构化工件
- **Implementation 节点**（test-driven-dev）只负责单个活跃任务的 RED/GREEN/REFACTOR
- **Review 节点**（spec-review / design-review / test-review / code-review / traceability-review …）只负责独立判断质量，不顺手改实现
- **Gate 节点**（regression / doc-freshness / completion）只负责回答"证据是否足够推进或宣告完成"
- **Routing 节点**（using-hf-workflow / hf-workflow-router）只负责"下一步去哪里"，不写正文也不动代码
- **Closeout 节点**（finalize）只负责状态闭合、release notes、handoff，不再实现新功能

每个节点的职责单一，且其结论必须落到磁盘工件上，下一节点才能基于证据继续推进。这套划分直接来自 `docs/principles/methodology-coherence.md` 的"HF 六层"。

### 1.4 三条不让步的工程默认值

| 默认值 | 含义 | 反面（HF 拒绝的做法） |
|---|---|---|
| **Spec 锚定意图** | spec / design / tasks 是结构化工件，不是"大一点的 prompt" | 直接基于会话记忆开写代码 |
| **基于证据的路由** | 下一步去哪里，由磁盘工件证据决定 | 靠聊天记忆"我刚才说过…"恢复 |
| **Fresh evidence 才算完成** | 完成结论必须依赖**本会话内**产生的 RED/GREEN/regression/completion 证据 | 凭"看起来跑过了"或历史 evidence 宣告完成 |

这三条不是技巧，是 HF 工作流的工程默认值。任何 skill 与之冲突，按 `docs/principles/soul.md` 处理：以 soul 为准。

---

## 二、零成本上手（不用记任何命令）

HF 没有 CLI、没有 `/hf-init`、没有需要背的命令。**唯一需要记的一件事**是：

> 在新会话里说一句"使用 HarnessFlow"或"using HF"，HF 会自己接管引导。

入口是 `using-hf-workflow` 这个 public entry。它的职责只有一个——根据你说的话和当前仓库工件，把你**送到正确的 leaf skill**，要么直接进入下游节点，要么交给 `hf-workflow-router` 做权威路由。命令（`/hf-spec`、`/hf-build`、`/hf-review` 等）只是 bias，不是 authority；不记也行。

### 2.1 下面这条链是 standard profile 下最常见的主线

> 上游的产品发现（`hf-product-discovery` / `hf-experiment`）、UI 支线（`hf-ui-design` / `hf-ui-review`）、缺陷与变更支线（`hf-hotfix` / `hf-increment`）会在合适的信号下被 router 自动绕进来；下文不展开，遇到时 router 会显式告诉你"现在改走支线"。

| # | 节点 | 它接什么 | 它产出什么 | 为什么是它而不是上一个 |
|---|---|---|---|---|
| 0 | `using-hf-workflow` | 你的自然语言请求 | 一次入口判断：直接进入某个 leaf skill，或交给 `hf-workflow-router` | 它不替你写正文也不替你判 profile，只决定"该不该继续做权威路由" |
| 1 | `hf-workflow-router` | 仓库工件 + 你的请求 | 当前 stage、Workflow Profile、Execution Mode、canonical 下一步 | `using-hf-workflow` 已确定需要权威路由；接下来的 profile / 支线 / review dispatch 必须由它统一裁决 |
| 2 | `hf-specify` | 上游 idea / discovery 的 spec-bridge | 一份结构化 spec：FR/NFR、验收标准、Key Hypotheses | router 已确认这是规格阶段；意图未结构化前不允许进入 design |
| 3 | `hf-spec-review` | 上一步 spec 草稿 | 独立 reviewer 的 verdict 与 findings | 作者不能自审；spec 没通过 review 不允许进入 design |
| 4 | `hf-design` | 已批准 spec | 架构 / 模块 / API / 数据模型 / NFR Uptake / ADR | spec 已锁定 what，design 才回答 how；不批准的 spec 设计出来的方案没有锚 |
| 5 | `hf-design-review` | 上一步 design 草稿 | 独立 verdict + traceability 到 spec | 作者不能自审；架构问题在这里被拦下来比在实现里被发现便宜得多 |
| 6 | `hf-tasks` | 已批准 design | WBS + 依赖图 + Definition of Done | design 已稳定；没有切片就没法保证"一次只做一件事" |
| 7 | `hf-tasks-review` | 上一步 task plan | INVEST / 依赖 / traceability 检查 verdict | 任务切错了，下游 TDD 节奏会反复抖动 |
| 8 | `hf-test-driven-dev` | 唯一活跃任务 + 已批准计划 | 测试设计 approval、RED/GREEN/REFACTOR 证据、Refactor Note、canonical 交接块 | HF family 中**唯一**的实现入口；先写测试再写实现，不允许跳过 approval |
| 9 | `hf-test-review` | 上一步测试与设计 | 独立 reviewer 的测试质量 verdict（fail-first、覆盖类目、bug pattern） | 测试自己也要被审；自审的测试只能保证"作者觉得够了" |
| 10 | `hf-code-review` | 上一步实现 + 已批准设计 | 独立 reviewer 的实现 verdict（设计一致性、Clean Architecture、refactor 纪律） | 测试通过≠设计正确；这一节是"看实现是否守得住已批准设计"的最后机会 |
| 11 | `hf-traceability-review` | 整条链 spec ↔ design ↔ tasks ↔ code ↔ tests | 端到端追溯 verdict | 单点都通过≠整条链一致；漂移在这里被显式拦下 |
| 12 | `hf-regression-gate` | 影响域分析 + 全量证据 | 回归门禁 verdict | 单任务通过≠系统不退化；不跑这一关就把锅留给下游 |
| 13 | `hf-doc-freshness-gate` | 当前任务 touch 的文档面 | 文档与实现的同步度 verdict（ADR-0003） | 实现改了文档没动，下次有人接手就会被旧文档误导 |
| 14 | `hf-completion-gate` | 上面所有 review/gate 的 evidence bundle | 完成判定 verdict | "看起来完成"和"证据足以宣告完成"是两件事；这是它们之间的隔离层 |
| 15 | `hf-finalize` | completion gate 已允许收尾 | closeout 工件、CHANGELOG、release notes、handoff pack | 任务通过≠工作流收口；状态没闭合，下一轮会启动得很别扭 |

### 2.2 上手时只需要做三件事

1. **在仓库根放一份填好的 `AGENTS.md`**（用 `skills/templates/AGENTS.md.example` 复制）。它告诉 HF 你团队的路径约定、批准状态别名、Execution Mode 默认值。HF 不替你立标准（详见第三节）。
2. **第一句对话说"使用 HarnessFlow"**。`using-hf-workflow` 会自己分流。
3. **遇到 approval / review 暂停点时，只需回答 yes/no/findings**。HF 不会偷偷越过 approval 自己往下推。

整个过程不需要你记节点名、不需要你判 profile、不需要你跑命令。你**唯一**需要做的工程动作是"立标准 + 拍板"——这正是下一节要讲的事。

---

## 三、人与 Agent 的关系

### 3.1 一句话契约：用户是架构师，HF 是工程团队

这句话来自 `docs/principles/soul.md`，它不是修辞——它直接决定了 HF 在每一个节点上"做什么"和"不做什么"。架构师不写具体业务代码，但**系统长成什么样、为什么是这样**由他负责；工程团队的职责，是在架构师立的标准之内把事做对、做完、做出可回读的证据。

### 3.2 用户（架构师）该做的四件事

| 职责 | 含义 | 在 HF 流程里落到哪 |
|---|---|---|
| **定方向** | 这一轮做什么、不做什么；哪个 idea 进 spec、哪个砍掉 | discovery → spec 之间的 approval |
| **做取舍** | 性能 vs 简单、扩展 vs YAGNI、严格 vs 灵活 | design ADR、spec MoSCoW、tasks 切片 |
| **立标准** | 代码风格、接口约定、错误处理、什么算"完成" | `AGENTS.md`、Definition of Done、profile 强制规则 |
| **验收成果** | spec / design / tasks / 实现 / evidence 是不是要的 | 各个 review 节点之后的 approval step |

### 3.3 HF（工程团队）该做的四件事

| 职责 | 含义 | 反面（HF 严禁的做法） |
|---|---|---|
| **按标准高效执行** | 把方向、取舍、标准翻译成 spec / design / tasks / TDD 步骤 | 重新拍一遍方向 |
| **暴露而不是替用户决定** | 方向、取舍、标准的空白或冲突时显式抛回 | 偷偷选一个看起来合理的继续推进 |
| **留下可回读的证据** | 每一步落到工件、RED/GREEN、review record、verdict | 只在会话里说"已经测过了" |
| **守住质量门禁** | review / regression / completion 各自独立、不让"看起来完成"绕过 | 让实现节点自己声称完成 |

### 3.4 由这层关系推出的硬性纪律

1. **方向、取舍、标准的最终权在用户**。HF 不确定时默认停下来澄清。
2. **HF 不替用户验收自己**。verdict 来自独立的 review / approval 工件，不来自实现节点的自述。
3. **所有交付物必须可回读、可恢复**。下一次进入工作流时，HF 仅凭仓库就要知道"现在站在哪里"。
4. **质量优先于进度**。当"快速推进"和"高质量证据"冲突时，HF 选后者。
5. **HF 永远不假装自己是架构师**。没有用户拍板时，HF 不擅自定方向、做取舍、改标准。

> 这五条是 HF 所有 skill 行为的最终仲裁口径——任意 skill 与之冲突，以本节为准。

---

## 四、如何保证质量

HF 的质量纪律不是单点检查，而是六层防御。任意一层省掉，链路都会在不同位置塌方。下面每一段先说"为什么这么做"，再说"省掉会出什么问题"。

### 4.1 意图层：spec 锚定意图

把 spec / design / tasks 当作结构化工件而不是 prompt。EARS + BDD + MoSCoW + INVEST + ISO 25010 + QAS 让需求落到字段化、可批准、可追溯的形态。**省掉的代价**：意图模糊会沿链路放大——上游一句"差不多就这样"，下游就要写五份不同假设的代码并互相打架；测试也写不出来，因为不知道在测什么。

### 4.2 执行层：带门禁的 TDD

`hf-test-driven-dev` 强制"先写测试设计 approval → 看到 RED → 写最小实现到 GREEN → REFACTOR"，并禁止跨任务结构性重构（escalate 给 `hf-increment`）。Two Hats 纪律保证写新行为和重构不混在同一步。**省掉的代价**：测试事后补会自动迁就实现，无法证明"实现真的对"；多任务并行的实现会让 code review 同时审 N 件事，每一件都漏。

### 4.3 评审层：多道独立评审

test / code / traceability / spec / design / tasks / ui review 各自由独立 reviewer 完成，不允许作者自审。这是 Fagan 检查的核心精神——**判断者必须不是生产者**。**省掉的代价**：作者总会过度信任自己刚做完的东西；架构错位、命名漂移、测试假阳性这些问题在自审下大概率被合理化掉。

### 4.4 验证 / 门禁层：三道门禁

| 门禁 | 它问的问题 | 不通过的代价 |
|---|---|---|
| `hf-regression-gate` | 影响域内的旧行为是否仍然成立？ | 单点通过、全量倒退 |
| `hf-doc-freshness-gate` | 这次实现 touch 的文档是否同步更新？ | 实现 vs 文档分叉，下一轮接手就误导 |
| `hf-completion-gate` | 整组证据是否足够宣告完成？ | "看起来完成"被当成"真的完成" |

三道门禁回答的是不同问题，不允许互相替代。**省掉的代价**：只跑回归会忽略文档漂移；只看 completion 会跳过回归；让一道门承担三件事就什么都看不严。

### 4.5 路由层：基于证据的路由

`hf-workflow-router` 只看磁盘工件状态决定下一步，不依赖会话记忆。Profile（lightweight / standard / full）只允许向上升级、不允许下游自己降级。**省掉的代价**：长会话里 agent 会"忘记"上一个 verdict，把已经被打回的设计当作通过；profile 漂移会让 lightweight 路径偷跑过本应 full 的高风险变更。

### 4.6 收尾层：PMBOK 式 closeout

`hf-finalize` 把状态闭合、release notes、handoff pack 当作工程的一部分，而不是事后补充。**省掉的代价**：任务通过但 `progress.md` / `CHANGELOG.md` / 顶层导航没同步——下一个会话冷启动时会以为活跃 feature 还没完，或反过来以为已经完成的事情还没做。

---

## 五、Skills 设计原则

最后一节解释一件事：**为什么 HF 的 skill 写成现在这个形状**。读完这一节，你打开任意一份 `SKILL.md` 时不会困惑。完整的作者级规范在 [`docs/principles/skill-anatomy.md`](principles/skill-anatomy.md)，本节只讲对你作为用户最重要的五条。

### 5.1 SKILL.md 是本地 contract，不是概念长文

`SKILL.md` 正文有量化预算（建议 < 500 行 / < 5000 tokens），运行时 compaction 后只保留前 5000 tokens。这意味着 HF 把每一份 `SKILL.md` 都当作"短而硬的运行时合同"——会改变 agent 行为的内容留主文件，不会的下沉到 `references/`。**对你的影响**：你看 `SKILL.md` 应该一眼能看到 When to Use / Workflow / Red Flags / Verification，看不到长篇方法论叙述。

### 5.2 Description 是分类器，不是摘要

每个 skill 的 frontmatter `description` 只回答一个问题：**"现在该不该加载这个 skill"**。它写触发条件、典型症状、反向边界，不写流程摘要。**对你的影响**：你不需要读 description 来理解 skill 在做什么；它只决定 agent 在你说一句话时**该不该把这份 skill 的正文拉进上下文**。

### 5.3 边界必须显式

每个 skill 都要写清"何时使用、何时不用、和相邻 skill 的区别、冲突时回哪里"。这是 HF 防止 skill 之间互相吃掉对方职责的硬约束。**对你的影响**：当你不确定某个请求该交给 `hf-spec-review` 还是 `hf-design-review`，你直接读这两份 skill 的 `When to Use` 和 `和其他 Skill 的区别`，必有一份明确说"不属于我，去找谁"。

### 5.4 退出条件可验证

每个 skill 的 `Verification` 节只检查退出条件，不写礼貌性 checklist。优先检查：record 是否落盘、状态是否同步、verdict / next action 是否唯一、fresh evidence 是否存在。**对你的影响**：你能用 `Verification` 节快速判断当前节点是否真的可以放手——它不是 nice-to-have 提醒，是硬性出口判据。

### 5.5 路径写法可迁移

skill 不绑定到某个仓库根、某个 pack 名或某个项目目录。项目工件路径优先遵循 `AGENTS.md`；skill pack 内部资料用 pack 语义路径。**对你的影响**：把 HF vendor 进你自己的仓库时，**你只改 `AGENTS.md`，不改 skill**。这也是 HF 反对在 skill 里硬编码 repo-local 路径的根本原因。

---

## 接下来读什么

按角色，建议路径：

- **架构师 / Tech Lead**（你刚读完的视角）→ `docs/principles/soul.md`（宪法）→ `docs/principles/methodology-coherence.md`（方法论协作图）
- **要给 skill 加节点或改 skill 的人** → `docs/principles/skill-anatomy.md` → `docs/principles/hf-sdd-tdd-skill-design.md`
- **想看 HF 在真实项目里的样子** → `README.zh-CN.md` 的 Quick Start + 工作流形状

> 仲裁规则：本文与 `docs/principles/soul.md` 出现冲突时，以 soul 为准。

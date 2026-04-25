# HarnessFlow Guidelines：一个"轻 harness、重 skills"的 AI 工程工作流是怎么设计的

> 面向团队内部读者。假定你已经知道 Claude / Cursor 的 skill 是什么，也大致清楚 "agent workflow" 这件事存在。本文要讲的是，**当我们认真把一套工程节奏落到 skill pack 上时，设计判断长什么样**。

---

## 0. 先把结论放在最前面

HarnessFlow（以下简称 HF）的核心设计判断，一句话写出来是这样的：

> **把编排做薄、把方法论压进 skill；让 skill 之间根据磁盘工件的证据自动路由，而不是靠 prompt 技巧串起来。**

如果把一个 AI agent 工作流类比成一条产线，市面上大多数方案的姿势是——**做一个超级大的中央控制器（harness），由它来决定每一步做什么**。HF 反过来：**harness 本身只有薄薄两层**（public entry + runtime router），所有真正的工程方法论（SDD、TDD、DDD、Fagan、ATAM、C4、ADR、QAS、Canon TDD、Two Hats、Clean Architecture、PMBOK closeout……）都**下沉到每一个 skill 自己的 `SKILL.md` 里**。

这个选择不是风格偏好，而是被一连串工程问题逼出来的。下面展开。

---

## 1. "轻 harness、重 skills"：为什么把方法论压进 skill

### 1.1 Harness 薄到什么程度

HF 的 harness 总共就两层，职责明确到几乎不能再拆：

| 层 | skill | 唯一职责 |
|---|---|---|
| Public Entry | `using-hf-workflow` | 判断是 **direct invoke 某个 leaf skill**，还是 **route-first 交给 router** |
| Runtime Router | `hf-workflow-router` | 依据磁盘工件，决定 profile / execution mode / workspace isolation / 下一个 canonical 节点 |

`using-hf-workflow` 本身被写死不能做 authoritative routing；`hf-workflow-router` 也被写死不能替 leaf skill 写正文。**两层都不承载工程方法论**，它们只决定"现在应该把控制权交给谁"。

### 1.2 重的那头：每个 skill 是一份可独立运行的 contract

真正"有肉"的是 24 个 `hf-*` leaf skills，每一个都在自己的 `SKILL.md` 里显式声明：

- 它承载哪些方法论（比如 `hf-specify` 绑定 EARS + BDD + MoSCoW + INVEST + ISO 25010 + QAS）
- 它的 Workflow 步骤
- 它的 Output Contract（写什么工件、写到哪里、状态怎么同步）
- 它的 Red Flags 与退出验证

这套写法在 `docs/principles/skill-anatomy.md` 里被定义为 **"短而硬的运行时 contract"**：`SKILL.md` 正文预算是 `< 500 行 / < 5000 tokens`，超出就下沉到 `references/`。

### 1.3 为什么不反过来：把方法论塞进 harness？

我们也认真想过"做一个大而全的中央 workflow engine"这条路，最终放弃，核心原因有三：

1. **上下文预算有限**。运行时 compaction 后每个 skill 只保留前 5000 tokens，多个 skill 共享约 25000 tokens 总预算。把方法论塞进 harness 意味着每次调用都要把 SDD、TDD、DDD、Fagan 全家桶一起拉进上下文，挤掉对话历史和工件证据。
2. **方法论会相互污染**。Fagan inspection 的完整流程和 HF 的 reviewer 派发协议是不兼容的；ATAM 的完整会议和 `hf-design-review` 的异步评审也是不兼容的。塞到一起就必然出现"看起来在讲同一件事，但语义打架"的情况。
3. **方法论演化速度不一样**。`hf-test-driven-dev` 的 Two Hats 纪律已经稳定了十几年，但 `hf-product-discovery` 里的 Opportunity Solution Tree 是近几年才流行的。薄 harness 让每个 skill 按各自节奏演化，不会一个动就全体动。

这就是为什么在 HF 里 harness 只负责**分诊与调度**，把"到底怎么做"完全留给 skill 自己。

---

## 2. Skills 之间怎么自动路由：evidence-based dispatch

"轻 harness" 不等于"没 harness"。真正让这套设计跑起来的，是 HF 那套基于**磁盘工件证据**的自动路由机制。

### 2.1 三条铁律

`hf-workflow-router` 的设计严格遵守三条：

1. **Finite State Machine Routing**：workflow 阶段建模为有限状态机，每条转移边由工件状态驱动，不由聊天记忆驱动。
2. **Evidence-Based Decision Making**：所有路由判断基于磁盘工件（`features/<active>/progress.md`、`reviews/`、`verification/`、`approvals/`），证据冲突时**保守选更上游、更重的 profile**。
3. **Escalation Pattern**：profile 只允许升级（lightweight → standard → full），不允许降级。

这三条合起来的效果是：**任何一个 agent 会话被中断、跨机器重启、或者切到另一个同事手上，都能在读完 3–5 个工件后精准恢复到"上次应该去的下一步"**。不依赖对话历史，这是 HF 跟普通 agent workflow 最本质的差别之一。

### 2.2 路由读什么？一个具体的例子

当用户发一句 "使用 HarnessFlow，继续推进"，router 干的事大概是：

1. 读 `AGENTS.md` 拿到路径映射和 profile 规则
2. 读 `docs/index.md` 拿到当前 active feature
3. 读 `features/<active>/progress.md` 拿到上次停在哪
4. 读 `features/<active>/reviews/` 看最近一次 review 的 verdict
5. 读 `features/<active>/verification/` 看有没有 fresh evidence
6. 最后输出一个受控结构：`Current Stage / Workflow Profile / Execution Mode / Workspace Isolation / Target Skill`

如果证据互相冲突（比如 spec 显示已批准但 reviews 里最近一条 verdict 是 `needs-rework`），router 按"未批准 + 更上游节点"处理，而不是替你拍板。**路由本身是显式可审计的**，不是黑盒。

### 2.3 Conditional Peer Skill：router 怎么识别 UI 并行分支

自动路由最能体现 HF 设计思想的，是 **Conditional Peer Skill** 这个机制。

举个例子：进入 design 阶段时，router 会额外判断一个问题——**spec 里有没有声明 UI surface**？

- 有 → 激活 `hf-ui-design` 作为 `hf-design` 的 conditional peer，两条设计并行起草；各自独立评审，**`hf-design-review` 和 `hf-ui-review` 都通过后**才发起联合的 `设计真人确认`。
- 没有（纯后端 / CLI / 数据管道）→ design stage 只走 `hf-design` 单节点。
- 规格含糊或证据冲突 → 回 `hf-specify` 补齐 UI surface 声明，**router 不自己拍板**。

同样的机制还用在 `hf-experiment` 上：当 spec 的 Key Hypotheses 里存在 Blocking 或低 confidence 假设时，router 会把它作为 **conditional insertion** 临时插进主链，probe 结果回流后再继续。

这就是 "自动路由" 这四个字在 HF 里的真实含义——**不是 if-else 跳转，而是 FSM + 证据 + 渐进 escalation 三者合起来对 workflow 做受控编排**。

---

## 3. 工程纪律怎么落下来：spec-anchored SDD + gated TDD 双骨架

自动路由是骨架，真正让骨架不塌的是 HF 对"完成"这件事的严格定义。

### 3.1 一次只做一个活跃任务

Kent Beck 的 Canon TDD 是 "一次一个 test list item"，HF 在这之上再收紧一级："**一次一个 Current Active Task**"。

- `hf-workflow-router` 锁定唯一活跃任务
- `hf-test-driven-dev` 只处理这一个任务
- 当前任务的质量链（test review → code review → traceability review → regression gate → completion gate）没闭环前，**不允许切下一任务**
- 切任务的唯一合法路径是"回到 router 重新锁定"

这条规则阻止了 agent 在长会话里悄悄漂移——我们在早期版本没这条约束时，agent 经常把三四个任务的代码混在同一个 commit 里，review 也没法做。

### 3.2 Fresh Evidence 是合同，不是优化项

HF 把四类证据写成一等合同：

- **RED evidence**（测试确实因为预期原因失败）
- **GREEN evidence**（最小实现让测试通过）
- **Regression evidence**（影响域内回归通过）
- **Completion evidence**（evidence bundle 齐全）

缺任何一个，唯一合法结论是"**继续实现 / 回 review / 回 router**"，**不允许说"完成"**。

这条规则的现实意义是：哪怕 `auto` execution mode 下，agent 也不能用"我觉得应该好了"代替实际跑一次测试再落盘。fresh 的定义是**本会话内**，昨天的证据 = 没证据。

### 3.3 Review 与 Gate 是一等节点，不是顺手做

HF 把 review 从实现里彻底剥出来，按 Fagan inspection 的精神强制 author/reviewer 角色分离：**实现节点不允许顺手做 review；review 节点不允许顺手回修正文**。

更关键的是，`hf-completion-gate` 和 `hf-finalize` 被刻意分成两个节点：

- completion gate 回答 "**这一个任务**能不能算完成"
- finalize 回答 "**整个 workflow**要不要正式收尾"

两者分开之后，"任务完成"和"项目收尾"就不会再被压扁成一句随口结论；release notes、handoff pack、状态闭合这些 PMBOK 式的收口动作有了明确归属。

---

## 4. 方法论之间怎么不打架：一张治理地图

到这里很多人会有个合理的疑问：HF 一共引用了 **30+ 种方法论**（从 EARS、BDD、MoSCoW、INVEST 到 DDD、C4、ADR、Event Storming、STRIDE、Canon TDD、Two Hats、Fagan、ATAM、PMBOK……），**它们为什么不会打架**？

答案在 `docs/principles/methodology-coherence.md` 这份治理文档里。它做了三件事：

### 4.1 按"层 / 字段 / Phase"三轴分工

所有方法论先按 HF 六层（意图 / 架构 / 执行 / 路由 / 评审 / 验证收尾）归位——**同一层里才可能冲突，跨层天然不冲突**。同一层内再按"承担什么 / 不承担什么"切字段。

一个典型例子：

- `MoSCoW` 决定 **"进不进这一轮"**
- `RICE / ICE` 决定 **"同级里先打哪个"**
- `Kano` 决定 **"做到什么档位"**

看起来三个都在做"优先级"，其实回答的是三个不同的问题。HF 强制三者同时在场，**严禁替代**。

### 4.2 显式的"反替代清单"

文档里有一张硬性表，标注**看起来可以互换但严禁替代**的配对，比如：

- `DDD Bounded Context` ↔ `C4 Container` 必须一致，不一致时用 ADR 显式解释
- `EARS` ↔ `BDD / Gherkin` 必须同时存在于同一条需求的不同字段，不互替
- `ISO 25010` ↔ `QAS` 一个是分类、一个是格式，同时满足
- `Canon TDD 的 test list` ↔ `HF 的测试设计 approval` 不允许以 Canon 为由跳过 approval

这张表是给 reviewer 当 checklist 用的——任何替代尝试会被直接 red flag 拦截。

### 4.3 Emergent vs Upfront：一个能体现工程判断深度的例子

HF 对"设计模式"这件事的处理值得单独拎出来讲一下，因为它很能体现这套 pack 的"工程判断味道"。

大多数 agent workflow 对"模式"的态度是**要么全前置、要么全浮现**。HF 在 `docs/principles/emergent-vs-upfront-patterns.md` 里做了**四档切分**：

| 档位 | 决策时机 | 归属节点 |
|---|---|---|
| 架构模式（Monolith / Hexagonal / Event-Driven） | **前置** | `hf-design` Step 2 |
| DDD 战术模式（Aggregate / VO / Repository / Domain Event） | **前置** | `hf-design` Step 2.7 |
| GoF 代码模式（Strategy / Factory / Adapter） | **emergent 浮现** | `hf-test-driven-dev` REFACTOR |
| 语言惯用法 | **emergent 浮现** | in-task cleanup |

核心立论一句话：**领域语义驱动的模式前置决策；实现细节驱动的模式 emergent 浮现**。

这不是品味选择。Beck / Fowler / Kerievsky 三人的工作都支持这一判断，而且 HF 已有的 `CA9 over-abstraction` 护栏本身就与"GoF 前置决策"在结构上互相冲突——前置 `Strategy` 会逼出只有 1 个实现的抽象层，这就是 over-abstraction 的教科书场景。

把这种细粒度的工程判断**沉淀成治理文档 + reviewer checklist + sut_form allowlist 三层强制**，才是 HF "重 skills" 真正重的地方。

---

## 5. 跟市面上方案点到为止地比一下

不做长篇 benchmark，只给团队三句话的定位：

- **vs. 单巨型 prompt / 自制 agent loop**：HF 把"编排 / 执行 / 评审 / 收尾"拆成独立节点，避免三者被压扁成一个不透明的大调用。
- **vs. `obra/superpowers` 的 TDD skill**：HF 吸收它的反合理化语言和 fresh evidence 纪律，但不照搬它的重型多 skill 编排——HF 的编排由 router + 工件证据承担，而不是 skill 之间互相喊话。
- **vs. GitHub Spec Kit / addyosmani 的 SDD skill**：HF 吸收 `Specify → Plan → Tasks → Implement` 四段骨架和阶段间 checkpoint 思想，但选择 `spec-anchored` 而非 `spec-as-source`——HF 要支持 brownfield 仓库、已有代码、已有测试，不能假设一切从 spec 单向生成。

换句话说，HF 不是要造"又一个 AI 编码神器"，而是**把 AI 编码约束到团队认可的工程节奏里**。

---

## 6. 为什么这套设计"高质量"

最后回收开头的那个问题：为什么它好用、为什么它是高质量的？

不是因为用了多少方法论，而是因为它同时满足下面这四个工程属性：

1. **可恢复**（recoverable）：任何会话中断都能从磁盘工件恢复，不依赖对话历史。
2. **可审计**（auditable）：每一步的路由判断、每一次完成声明都有落盘证据支撑，reviewer 可以冷读。
3. **可演化**（evolvable）：薄 harness + 方法论下沉到 skill，让单个 skill 可以独立升级、单独做 evals、单独快照迭代，不会一个动就全体动。
4. **可治理**（governable）：`methodology-coherence.md` + `emergent-vs-upfront-patterns.md` + 各 skill 的 Red Flags + evals，把方法论冲突和反模式显式拦在运行时之前。

一句话收尾：

> **HF 的设计哲学不是"让 AI 写得快"，而是"让 AI 写得经得起 review"。**
>
> 轻 harness、重 skills、工件驱动路由——这三件事合起来，才让一个 agent workflow 从"会跑的 demo"变成"团队可以依赖的工程基础设施"。

---

## 7. Skill-by-skill 细讲：每个 skill 配的方法论都是干什么的

前面讲了 HF 的顶层设计。下面按六层把 24 个 `hf-*` skill 过一遍，重点说两件事：**这个 skill 做什么独特的事**，以及**它绑定的方法论每一条是什么、为什么选它、不用会出什么问题**。

为了不冗余，每个方法论只在第一次出现的 skill 里展开写全称和四段式说明；后面再出现只列名字 + 回指。

### 7.1 入口 & 路由层

#### `using-hf-workflow`（Public Entry）

**特点**：整个 family 的公开入口。它**只做分诊，不做业务**——判断是 direct invoke 某个 leaf skill，还是 route-first 交给 router。

- **Front Controller Pattern（前端控制器模式）**
  - 做什么：统一入口点，把所有请求先接住，再分派到对应 handler。
  - 为什么选：让新会话、命令入口、auto mode 信号都有同一个收口处，而不是散落在每个 skill 里各写一份。
  - 不用会怎样：每个 skill 都得写"我该不该接这个请求"的分诊逻辑，出现大量重复和不一致；用户发同一句话去到不同 skill 会得到不同行为。
- **Evidence-Based Dispatch（证据驱动分派）**
  - 做什么：读 `progress.md` 和工件状态，判断当前是新会话（entry）还是运行时恢复（recovery）。
  - 为什么选：避免入口层凭聊天记忆猜"我们走到哪了"，让分诊决策可复现、可审计。
  - 不用会怎样：同一份工件现场，不同会话会做出不同分诊结论，workflow 的可恢复性立刻崩塌。
- **Separation of Concerns（关注点分离）**
  - 做什么：入口层只负责意图识别和分发，不碰 authoritative routing、不改状态、不写工件。
  - 为什么选：防止公开入口层退化成第二个 router，让两层都保持薄。
  - 不用会怎样：`using-hf-workflow` 会慢慢长出 FSM、profile 判断、review 派发逻辑，最后 harness 不薄了。

#### `hf-workflow-router`（Runtime Authority）

**特点**：HF 的"大脑"但它并不大。它是**唯一有权 authoritative routing 的节点**，其他 skill 都不能擅自跨节点跳转。

- **Finite State Machine Routing（有限状态机路由）**
  - 做什么：把 workflow 阶段建模为状态机，每条转移边由工件状态这一条证据驱动。
  - 为什么选：让"下一步该做什么"成为 pure function（工件状态 → 下一个节点），不依赖任何隐式上下文。
  - 不用会怎样：路由变成"大模型自由发挥"，在长会话里漂移、在跨会话恢复时断链。
- **Evidence-Based Decision Making（证据驱动决策）**
  - 做什么：所有路由判断基于磁盘工件；证据冲突时保守处理（选更上游 / 更重 profile）。
  - 为什么选：让路由有兜底纪律，不会因 reviewer 的一句"应该差不多了"就放行。
  - 不用会怎样：冲突证据下 router 会猜；一旦猜错，下游整条链都在错的地基上做功。
- **Escalation Pattern（渐进升级模式）**
  - 做什么：profile 只允许 lightweight → standard → full 升级，不允许降级。
  - 为什么选：防止会话后期因为"赶时间"把原本 full profile 的任务偷偷降档到 lightweight。
  - 不用会怎样：复杂需求会被逐渐压成轻量任务，漏掉 spec / design / gate 等关键纪律。

### 7.2 上游 Discovery

#### `hf-product-discovery`

**特点**：HF 唯一的"产品发现"节点，把"值不值得做"和"打哪个 wedge"的判断显式落盘，输出 `*-spec-bridge.md` 作为进入 coding family 的入口。

- **Problem Framing（问题定义）**
  - 做什么：先定义用户、问题、阻塞进展、why-now，而不是从功能清单反推问题。
  - 为什么选：防止 spec 一上来就写"我们要做一个 X 功能"，而没先说清"谁的什么问题值得现在做"。
  - 不用会怎样：会出现"方案找问题"——先有了解决方案，再反过来编需求。
- **Hypothesis-Driven Discovery（假设驱动发现，Lean Startup / Continuous Discovery Habits）**
  - 做什么：把"我们觉得应该这样做"拆成可证伪假设、风险和 probe 方向。
  - 为什么选：让产品判断和规格起草都有"可验证"这条底线。
  - 不用会怎样：把假设当事实写进 spec，后面出问题也追不回源头。
- **Opportunity / Wedge Mapping（机会 / 楔子收敛）**
  - 做什么：在多个候选方向里收敛"当前轮最小 wedge"，明确哪些进本轮、哪些只是候选。
  - 为什么选：让范围收敛显式化，而不是藏在模糊的"我们先做这些"里。
  - 不用会怎样：范围会无限蔓延，tasks 阶段才发现要做的事是原计划的三倍。
- **Assumption Surfacing（假设显式化）**
  - 做什么：显式写出已确认事实、未确认假设和 open questions。
  - 为什么选：让下游 `hf-specify` 有稳定 bridge 可以消费。
  - 不用会怎样：假设藏在脑子里，review 和实现时每人理解一个版本。
- **JTBD / Jobs To Be Done（Christensen《Competing Against Luck》）**
  - 做什么：把需求锚定到"用户在某情境下想取得的进展"，而不是功能描述。
  - 为什么选：让产品动机跳脱"做个更好的按钮"，回到"用户在雇佣这个产品做什么任务"。
  - 不用会怎样：产品做成竞品功能集的并集，没有独立叙事。
- **Opportunity Solution Tree（机会方案树，Teresa Torres《Continuous Discovery Habits》）**
  - 做什么：Outcome → Opportunity → Solution → Assumption / Experiment 的收敛骨架。
  - 为什么选：让"一个想法到 N 个实验"的扇形推演有结构，每个 solution 能回指 outcome。
  - 不用会怎样：候选方案失去父级 anchor，选哪个全靠"谁嗓门大"。
- **RICE / ICE / Kano（量化优先级）**
  - 做什么：**RICE（Reach × Impact × Confidence / Effort，Intercom）**、**ICE（Impact × Confidence × Ease，Sean Ellis）**——在同级候选间做可冷读的量化取舍；**Kano（狩野纪昭）**——区分 Basic / Performance / Excitement 三档质量属性。
  - 为什么选：补齐 MoSCoW 只回答"进不进"而不回答"先打哪个 / 做到什么档位"的缺口。
  - 不用会怎样：Must 候选一堆，没人知道该先实现哪一个；或全部一股脑做成 Performance 档，把资源浪费在 basic 层还没达标的地方。
- **Desired Outcome / North Star Framing（Sean Ellis《Hacking Growth》、Amplitude《North Star Playbook》）**
  - 做什么：显式写出当前轮的成功度量和门槛。
  - 为什么选：让下游的 Success Criteria 不再是凭空生成。
  - 不用会怎样：完成判断只能靠感觉——"感觉差不多了就是完成"。

#### `hf-experiment`

**特点**：Phase 0 新加的 conditional insertion 节点。当 Blocking 假设未关闭时临时插入，验证完 probe 再回主链。

- **Hypothesis-Driven Development（假设驱动开发，Lean Startup / Intuit）**
  - 做什么：把产品决策拆成可证伪假设，而不是先做再看。
  - 为什么选：让"做个小验证"这件事有显式入口和退出条件。
  - 不用会怎样：验证和实现混在一起，pilot 之后没人知道它是"验证完可以推了"还是"已经是生产实现"。
- **Build-Measure-Learn（Eric Ries《The Lean Startup》）**
  - 做什么：最小构建 → 最小测量 → 显式学习回流。
  - 为什么选：让 probe 有完整三段闭环，学完要回流到 spec 或 discovery，不悬空。
  - 不用会怎样：跑完 probe 就不了了之，学习没有被吸收到上游工件里。
- **Four Types of Assumptions（Teresa Torres：Desirability / Viability / Feasibility / Usability）**
  - 做什么：按"用户想不想 / 能不能赚钱 / 技术可行 / 用户会不会用"四类给假设分型。
  - 为什么选：不同类型的假设要用不同 probe 验证，分型不做就 probe 选错。
  - 不用会怎样：用一个 A/B test 想同时验证 desirability 和 feasibility，结果两头都没验到。
- **Smallest Testable Probe（最小可测探针，Spotify《Think It Build It Ship It Tweak It》）**
  - 做什么：用最小代价打穿最高风险假设。
  - 为什么选：防止 probe 自己变成一个小项目。
  - 不用会怎样：为了验证"用户会不会点这个按钮"先做了三周前端重构。
- **Pre-registered Success Threshold（事先声明成功阈值）**
  - 做什么：在跑 probe 之前写死通过阈值，跑完不允许移动门柱。
  - 为什么选：对抗"事后合理化"——跑完 probe 再解释"为什么这个结果其实也算成功"。
  - 不用会怎样：每次 probe 都能解释成成功，学习价值归零。

### 7.3 Authoring（起草层）

#### `hf-specify`

**特点**：规格锚定节点。把模糊需求变成**可观察、可测试、可批准**的结构化工件。

- **EARS（Easy Approach to Requirements Syntax，Mavin et al., REFSQ 2009）**
  - 做什么：需求语句使用结构化触发模式——Ubiquitous（总是）/ Event-driven（当……时）/ State-driven（在……状态下）/ Optional（当功能启用时）/ Unwanted（当不期望事件发生时）。
  - 为什么选：让每条需求可观察、可判断；排除"系统应该好用"这类无法验证的需求。
  - 不用会怎样：需求变成散文，review 和实现各自解读，测试无锚点。
- **BDD / Gherkin（Behavior-Driven Development，Dan North 2006）**
  - 做什么：验收标准用 Given / When / Then 三段式表达。
  - 为什么选：建立从需求 → 测试的可追溯桥梁，让 acceptance criteria 直接喂给 `hf-test-driven-dev` 的 test list。
  - 不用会怎样：验收标准变成 checkbox 列表，写测试时得重新翻译一遍业务语言。
- **MoSCoW（Must / Should / Could / Won't，DSDM Consortium）**
  - 做什么：需求优先级四级分类，驱动范围收敛与 deferred 判断。
  - 为什么选：让"这一轮要不要做"有显式标签，而不是"都挺重要的"。
  - 不用会怎样：范围不收敛，review 无法判断某项可不可延后。
- **需求六分类（FR / NFR / CON / IFR / ASM / EXC，参考 IEEE 830 / ISO 29148 裁剪）**
  - 做什么：把需求按功能 / 非功能 / 约束 / 接口 / 假设 / 排除六类组织，覆盖完整需求空间。
  - 为什么选：防止"只写功能，不写约束和排除项"——漏掉排除项是下游最常见的争议来源。
  - 不用会怎样：spec 只剩功能清单，约束、假设、非目标全部口头传达。
- **Socratic Elicitation（苏格拉底式澄清）**
  - 做什么：Capture → Challenge → Clarify 三段式提问，通过结构化追问驱动收敛。
  - 为什么选：防止 agent 凭假设填空，让澄清问题有章法。
  - 不用会怎样：agent 在 spec 阶段写下一堆"假设用户想要 X"，后面全部白做。
- **INVEST（Independent / Negotiable / Valuable / Estimable / Small / Testable，Bill Wake 2003）**
  - 做什么：每条需求的六维质量检查。
  - 为什么选：让粒度是否合适有可检查的六个维度。
  - 不用会怎样：出现"巨型需求"——一条需求要做三周还没法估。
- **ISO/IEC 25010 + Quality Attribute Scenarios（QAS，Bass/Clements/Kazman《Software Architecture in Practice》）**
  - 做什么：**ISO 25010** 把 NFR 分类（性能 / 可靠性 / 安全性 / 可维护性 / 可用性 / 兼容性 / 可移植性 / 功能性）；**QAS** 用 Source / Stimulus / Environment / Response / Response Measure 五要素表达每一条 NFR。
  - 为什么选：让 NFR 可测试——"p95 ≤ 500ms under 1k RPS"这种可观察表达，而不是"系统要快"。
  - 不用会怎样：NFR 写成口号，后面既没法设计 observability，也没法设 gate。
- **Success Metrics & Key Hypotheses Framing（承接 discovery）**
  - 做什么：把 discovery 的 Desired Outcome 和 Key Hypotheses 显式落到 spec，供下游 design / tasks / gate / experiment 消费。
  - 为什么选：让 spec 成为度量和假设的单一真源。
  - 不用会怎样：完成判断时没人知道该比对哪个指标；假设未关闭就被当成事实写进设计。

#### `hf-design`

**特点**：架构建模节点。Bounded Context 先于视图，领域语义先于代码模式。

- **ADR（Architecture Decision Records，Michael Nygard 格式）**
  - 做什么：关键决策用"上下文 / 决策 / 后果 / 可逆性"四段落盘。
  - 为什么选：让未来的人能读到"当时为什么这么选"，而不是只看到结果。
  - 不用会怎样：三个月后没人知道为什么选 Kafka 不选 RabbitMQ，返工成本翻倍。
- **C4 Model（Context-Container-Component-Code，Simon Brown）**
  - 做什么：架构视图按 Context → Container → Component 分层递进。
  - 为什么选：给一份可被业务、架构、工程三种读者分别读懂的视图集。
  - 不用会怎样：画一张又大又全的图，谁都看不懂。
- **Risk-Driven Architecture（George Fairbanks）**
  - 做什么：架构投入按风险驱动——高风险决策做多方案比较，低风险决策直接拍板。
  - 为什么选：避免所有决策都做得一样厚或一样薄。
  - 不用会怎样：把时间花在"用什么 log 库"这种低风险决策上，真正高风险的（事务边界、消息语义）反而没做深。
- **YAGNI + Complexity Matching（You Aren't Gonna Need It + 复杂度匹配）**
  - 做什么：决策必须由当前已确认需求驱动；架构复杂度匹配团队规模和系统规模。
  - 为什么选：防止 solo 项目一上来就上微服务。
  - 不用会怎样：为"未来可能的扩展"付出当前就要承担的复杂度。
- **ARC42（partial，Gernot Starke / Peter Hruschka）**
  - 做什么：标准设计文档结构——约束、决策、视图、风险、技术债务、Glossary。
  - 为什么选：避免每个项目的 design doc 都自创结构。
  - 不用会怎样：读 design 时每次都在找"风险写在哪了"。
- **DDD Strategic Modeling（Eric Evans《Domain-Driven Design》）**
  - 做什么：锁 Bounded Context / Ubiquitous Language / Context Map，让边界先于结构。
  - 为什么选：C4 Container 的切法必须和 Bounded Context 一致，先有语义边界再画视图。
  - 不用会怎样：Container 切法照着数据库表或团队组织结构走，和业务语义脱节。
- **DDD Tactical Modeling（Eric Evans / Vaughn Vernon《Implementing DDD》）**
  - 做什么：每个 Bounded Context 内部回答 Entity / Value Object / Aggregate / Repository / Domain Service / Application Service / Domain Event。
  - 为什么选：**让"写代码前考虑好模式"落到领域语义驱动的模式选择上，而不是 GoF 直觉驱动**。这是前面讲过的"四档模式切分"中前置那一侧的核心。
  - 不用会怎样：Aggregate 边界定错，跨聚合一致性被写成一次事务，后期重构成本极高。
- **Event Storming（Alberto Brandolini）**
  - 做什么：用事件视角摊开业务流程，Big Picture / Process Modeling 两档按 profile 使用。
  - 为什么选：作为 spec → design 的桥，让事件而不是类成为建模起点。
  - 不用会怎样：直接从数据库表开始建模，业务事件被丢失。
- **STRIDE 轻量威胁建模（Spoofing / Tampering / Repudiation / Information disclosure / Denial of service / Elevation of privilege，Loren Kohnfelder & Praerit Garg @ Microsoft）**
  - 做什么：按六类威胁对每个 trust boundary 过一遍，落到具体缓解和 ADR。
  - 为什么选：让安全考虑在设计阶段就显式出现，而不是等 pentest。
  - 不用会怎样：上线后才发现鉴权 / 审计 / 输入校验有明显 gap。

#### `hf-ui-design`

**特点**：当 spec 声明 UI surface 时激活，与 `hf-design` 并行。它的 methodology 里有**非常强烈的反 AI 审美 slop 纪律**。

- **Information Architecture（Rosenfeld & Morville《Information Architecture》）**
  - 做什么：wireframe 前先锁站点地图、导航结构、内容分组。
  - 为什么选：IA 错了，后面的所有页面都在错的导航树上。
  - 不用会怎样：先画了一堆页面才发现导航跑不通，推倒重来。
- **Atomic Design（Brad Frost）**
  - 做什么：组件按 Atoms / Molecules / Organisms / Templates / Pages 分层。
  - 为什么选：让 Design System 映射和复用粒度有稳定骨架。
  - 不用会怎样：每个页面都是一次性拼接，复用和一致性都差。
- **Design System / Design Tokens（W3C Design Tokens CG）**
  - 做什么：所有颜色 / 字号 / 间距 / 圆角 / 阴影 / 动效走 token，不硬编码。
  - 为什么选：让视觉一致性是基础设施，而不是设计师的记性。
  - 不用会怎样：同一个"主按钮蓝"在不同页面是 5 种蓝。
- **Nielsen 十大可用性启发式（Jakob Nielsen）**
  - 做什么：用十条启发式（可见性 / 贴合现实 / 用户控制 / 一致性 / 防错 / 认出而非回忆 / 灵活高效 / 简约美学 / 错误恢复 / 帮助文档）做冷读评审。
  - 为什么选：给 UI review 一份业界公认的 rubric，不是审美主观评论。
  - 不用会怎样：UI review 变成"我感觉这里不好看"。
- **WCAG 2.2 AA（W3C Web Content Accessibility Guidelines）**
  - 做什么：可访问性硬门——色彩对比、键盘可达、语义 / ARIA、焦点管理、reduced motion。
  - 为什么选：a11y 是硬指标不是可选项，写进 skill contract 后不能偷偷跳过。
  - 不用会怎样：上线后被用户 / 法务 / 审计打回来做二次改造。
- **Interaction State Inventory（交互状态清单）**
  - 做什么：每个关键交互覆盖 idle / hover / focus / active / disabled / loading / empty / error / success 九种状态。
  - 为什么选：逼设计师不止画 happy path。
  - 不用会怎样：UI 上线后 loading 态闪瞎眼、empty 态空白一片、error 态直接崩。
- **Anti-Slop Discipline + Earn-Its-Place Content + Vocalize the System Up Front（Anthropic Claude-Design 系统提示词沉淀）**
  - 做什么：拒绝渐变滥用 / 紫色默认 / Inter/Roboto 默认 / 装饰 SVG / emoji 当图标 / 通用 dashboard 模板；每个 section / 文案 / 图标必须能回指真实需求；进入 wireframe 前先声明将用什么系统。
  - 为什么选：对抗 AI 默认产出的那种"看起来像设计但没灵魂"的 slop。
  - 不用会怎样：agent 生成的 UI 全都长一个样——紫色渐变 + Inter + 左竖线卡片 + 装饰 SVG。

#### `hf-tasks`

**特点**：把已批准 design 拆成**可执行、可追溯、可单独实现**的任务单元，并埋入测试设计种子。

- **WBS（Work Breakdown Structure，PMBOK / PMI）**
  - 做什么：自顶向下把设计拆成可管理的任务层级，每个任务范围明确、不重叠。
  - 为什么选：让任务集合覆盖设计且不重复，容易核对完整性。
  - 不用会怎样：任务会漏掉或重叠，实现时不断发现"还有一块没人做"。
- **INVEST Criteria**（参见 `hf-specify`）
- **Dependency Graph + Critical Path（依赖图 + 关键路径）**
  - 做什么：显式建模任务间依赖，识别关键路径。
  - 为什么选：让执行顺序有依据，也让 router 能算出唯一 next-ready task。
  - 不用会怎样：agent 一次切三个任务，或反复在被依赖任务之间跳。
- **Definition of Done（Scrum Guide，Schwaber & Sutherland）**
  - 做什么：每个任务有可判断的完成条件。
  - 为什么选：让 `hf-completion-gate` 有客观基准。
  - 不用会怎样：完成判断每次都是"感觉差不多了"。

### 7.4 执行层

#### `hf-test-driven-dev`

**特点**：HF 唯一的实现节点。把 Canon TDD + Two Hats + Clean Architecture conformance 压到同一节奏里。

- **TDD / Canon TDD（Kent Beck《Test-Driven Development: By Example》/《Canon TDD》）**
  - 做什么：先写 test list → 挑一个变成真正可运行测试 → 看它因预期原因失败 → 最小实现通过 → 重构 → 下一个。
  - 为什么选：让"写代码前必须先确定要测什么"成为硬纪律。
  - 不用会怎样：先写实现再补测试，测试永远只是在给已有代码背书。
- **Walking Skeleton（Alistair Cockburn）**
  - 做什么：优先建立最薄端到端可运行路径，再往里面填肉。
  - 为什么选：让集成风险在第一时间暴露，而不是等各模块都做完才撞在一起。
  - 不用会怎样：各模块单独都绿，集成时才发现接口对不上。
- **Test Design Before Implementation（HF 前置步）**
  - 做什么：在 Red-Green-Refactor 之前，先完成一份测试设计并通过 approval。
  - 为什么选：让"测什么"先稳定，再动手写测试，避免把错误接口写进第一版测试。
  - 不用会怎样：测试一路改接口，"测试先写"的意义消失。
- **Fresh Evidence Principle（新鲜证据原则）**
  - 做什么：RED / GREEN / regression / completion 证据必须在本会话内产生。
  - 为什么选：不允许用昨天的测试结果宣告今天的完成。
  - 不用会怎样：agent 会拿历史 CI 输出充当本次验证，用户看不出差别。
- **Two Hats（Kent Beck《Tidy First?》/ Fowler《Refactoring》Ch.2）**
  - 做什么：任一时刻只戴 Changer 帽（写新行为）或 Refactor 帽（保持行为不变改结构）。
  - 为什么选：混戴后回滚成本暴涨，reviewer 也分不清这段代码在引入行为还是整理结构。
  - 不用会怎样：commit 里行为变化和结构变化纠缠，回滚和 review 都费劲。
- **Opportunistic + Boy Scout Refactoring（Martin Fowler / Robert C. Martin）**
  - 做什么：每次接触代码顺手把它留得更干净一点，但限定在 task 触碰范围。
  - 为什么选：让架构健康是连续的，而不是靠周期性"重构周"。
  - 不用会怎样：技术债按"平时不动、爆发时重构"方式累积，越来越难动。
- **Preparatory Refactoring（Kent Beck via Fowler："make the change easy, then make the easy change"）**
  - 做什么：新行为不好加时先重构出扩展点，再"做简单的改动"；独立成步，不混进 RED。
  - 为什么选：让难改的地方有合法的"先清扫再前进"路径，而不是硬塞。
  - 不用会怎样：要么硬塞新代码进烂结构，要么借新行为之名做大重构。
- **Clean Architecture Conformance（Robert C. Martin《Clean Architecture》+ SOLID）**
  - 做什么：实现遵循已批准设计的依赖方向、模块边界、接口契约；不重新论证架构决策。
  - 为什么选：实现节点不是讨论架构的地方，但必须能识别"实现在悄悄违反设计"。
  - 不用会怎样：实现时 entity 开始引用 framework、use case 直接调数据库，依赖方向污染。
- **Escalation Boundary（升级边界，HF 节点契约）**
  - 做什么：跨 task 范围的结构性重构、ADR 变更、模块边界变更不在 task 内做，而是 escalate 到 `hf-increment`。
  - 为什么选：让"顺手重构"有显式上限。
  - 不用会怎样：一次 task 扩展成跨目录重写，review 根本没法做。

### 7.5 评审层（8 个 review skills）

这一层的方法论高度复用，先把**贯穿所有 review skill 的四条共同基线**抽出来讲一次：

- **Structured Walkthrough（结构化走查）**
  - 做什么：按预定义 rubric 维度打分（0–10），而不是自由形式阅读评论。
  - 为什么选：防止印象式评审——"我看了一下觉得挺好的"。
  - 不用会怎样：review 结论取决于 reviewer 心情和风格。
- **Checklist-Based Review（检查清单驱动，NASA / SEI）**
  - 做什么：用结构化检查清单覆盖关键质量维度。
  - 为什么选：让每次 review 覆盖面稳定，不会漏项。
  - 不用会怎样：每个 reviewer 关注不同维度，质量覆盖波动极大。
- **Separation of Author/Reviewer Roles（Fagan Inspection 精神）**
  - 做什么：author 和 reviewer 必须由不同 agent / 会话承担，reviewer 不写正文不改代码。
  - 为什么选：避免确认偏差——"自己写自己过"。
  - 不用会怎样：review 退化成仪式，问题被作者本能地合理化掉。
- **Evidence-Based Verdict（证据驱动结论）**
  - 做什么：所有 findings 必须锚定到具体工件位置，不接受无证据的"感觉不好"。
  - 为什么选：让 verdict 可被作者精确响应。
  - 不用会怎样：finding 变成模糊吐槽，author 不知道具体要改什么。

下面各 review skill 只列它**额外**绑定的方法论：

#### `hf-discovery-review` / `hf-spec-review` / `hf-design-review` / `hf-ui-review` / `hf-tasks-review`

- `hf-design-review` 额外：**ATAM（Architecture Tradeoff Analysis Method，SEI，Bass/Kazman）**——从质量属性驱动的视角评审设计，识别权衡点和敏感点。让架构评审围绕"NFR 是否达到"展开，而不是"代码风格好不好"。不用会怎样：设计评审只检查视图工整程度，真正的性能 / 可用性 / 安全权衡被遗漏。HF 只取 ATAM 的"QA driven"精神，不跑完整会议流程。
- `hf-design-review` 额外：**Traceability to Spec**——所有设计决策必须可追溯到 spec 具体需求。不用会怎样：设计漂移到 spec 之外，实现后才发现"我们做了一个规格没要的东西"。
- `hf-ui-review` 额外：**Nielsen Heuristic Evaluation**（参见 `hf-ui-design`）+ ATAM（适配到 UI 的 UX 质量属性）。
- `hf-tasks-review` 额外：**INVEST Validation**（参见 `hf-specify`）、**Dependency Graph Validation**（无环 / 顺序正确性）、**Traceability Matrix（ISO/IEC/IEEE 29148）**——检查任务是否忠实覆盖 spec / design 的每一项关键决策。不用会怎样：任务集合漏掉关键决策，实现时发现"设计里的这个模块没人对应"。

#### `hf-test-review`

- **Fail-First Validation（TDD 质量门）**
  - 做什么：验证测试确实先失败再通过。
  - 为什么选：拦截"天生绿色"的无效测试——写了个 `assertTrue(True)` 式的测试。
  - 不用会怎样：测试覆盖率数字好看，但一个 bug 都抓不住。
- **Coverage Categories（Crispin & Gregory《Agile Testing》）**
  - 做什么：从行为覆盖、风险覆盖、边界覆盖多维度评估测试质量。
  - 为什么选：让"测了多少"比"行数覆盖率"更有意义。
  - 不用会怎样：覆盖率 90% 但都是 happy path，边界和异常完全没测。
- **Bug-Pattern-Driven Testing（与 `hf-bug-patterns` 配合）**
  - 做什么：测试必须回应已有 bug pattern 目录识别出的风险。
  - 为什么选：让历史缺陷经验真的被复用，而不是再犯一次。
  - 不用会怎样：同一类 bug 在不同 feature 里反复出现。

#### `hf-code-review`

- **Fagan Code Inspection（adapted，Michael Fagan @ IBM）**
  - 做什么：结构化检查正确性、设计一致性、状态安全、可读性、架构健康五个维度。
  - 为什么选：让代码评审是工程活动，不是自由代码阅读。
  - 不用会怎样：review 只看到"命名不好"这种表层问题，深层 bug 漏过。
- **Design Conformance Check（设计一致性检查）**
  - 做什么：实现必须遵循已批准设计，偏离需有理由且可追溯。
  - 为什么选：让"实现漂移"有 review 节点拦截。
  - 不用会怎样：实现慢慢偏离设计，两边文档对不上。
- **Defense-in-Depth Review（纵深防御评审）**
  - 做什么：错误处理、状态转换、安全性逐层检查。
  - 为什么选：让"测试通过"不自动等同于"鲁棒可靠"。
  - 不用会怎样：测试都绿但生产环境一个异常就崩。
- **Clean Architecture Conformance Check + Architectural Smells Detection（Garcia/Popescu/Edwards/Medvidovic《Identifying Architectural Bad Smells》）**
  - 做什么：识别 god-class / cyclic-dep / hub-like-dep / layering-violation / feature-envy 等结构性 smell。
  - 为什么选：让架构健康有专门评审维度。
  - 不用会怎样：smell 被 case-by-case 合理化，架构慢慢腐烂。
- **Two Hats / Refactoring Hygiene Review**
  - 做什么：评审实现节点是否守住 Two Hats，Refactor Note 是否完整可信。
  - 为什么选：让 REFACTOR 步不只是口头承诺。
  - 不用会怎样：Two Hats 纪律只存在于 TDD skill 文档里，实际执行没人检查。

#### `hf-traceability-review`

- **End-to-End Traceability（IEEE 830-1993 / ISO 26550）**
  - 做什么：检查从需求到实现的完整追溯链，spec → design → tasks → code → tests 四层可逐级追溯。
  - 为什么选：让"这段代码在回答哪条需求"任何时候都能答出来。
  - 不用会怎样：一年后维护时，没人知道某段代码为什么存在。
- **Zigzag Validation（双向 zigzag 验证）**
  - 做什么：每条 FR 前向追溯到设计决策，设计决策后向追溯到需求。
  - 为什么选：防止"有需求没实现"和"有实现没需求"两个方向的断链。
  - 不用会怎样：实现里多出若干"设计没说但代码做了"的功能，spec 里少了实现。
- **Impact Analysis（影响分析）**
  - 做什么：发现不一致时判断影响范围是局部还是需要回流到上游。
  - 为什么选：让 verdict 能区分"小修"和"回 router 重编排"。
  - 不用会怎样：发现大问题后还硬在当前节点修。

### 7.6 门禁 & 收尾层

#### `hf-regression-gate`

- **Regression Testing Best Practice（ISTQB）**
  - 做什么：定义 full / standard / lightweight 三级回归覆盖范围。
  - 为什么选：让回归投入和风险匹配，不是"每次都全量跑"。
  - 不用会怎样：小改动也要跑两小时回归，或者大改动只跑几条冒烟。
- **Impact-Based Testing（影响域驱动测试）**
  - 做什么：回归范围基于 traceability review 识别的影响区域。
  - 为什么选：让回归跑得聪明，不只是跑得多。
  - 不用会怎样：关键路径没回归到，无关路径反复跑。
- **Fresh Evidence Principle**（参见 `hf-test-driven-dev`）

#### `hf-completion-gate`

- **Definition of Done**（参见 `hf-tasks`）
- **Evidence Bundle Pattern（证据束模式）**
  - 做什么：完成判断要求完整证据束（reviews + gates + 实现交接块），缺一不可。
  - 为什么选：让"完成"是一组证据的交集，不是一句口头结论。
  - 不用会怎样：task 被宣告完成但 review 记录还是空的。
- **Profile-Aware Rigor（Profile 感知严谨度）**
  - 做什么：full / standard / lightweight 三级对应不同证据量，但质量标准不降。
  - 为什么选：让 lightweight 不等于"可以省掉 gate"，只是缩小验证范围。
  - 不用会怎样：lightweight 被用作绕过 gate 的借口。

#### `hf-finalize`

- **Project Closeout（PMBOK）**
  - 做什么：系统性收尾——交付物确认、状态同步、经验归档、交接完整。
  - 为什么选：让 workflow 有正式关门动作，不会烂尾。
  - 不用会怎样：代码合了，但 release notes / changelog / progress 状态全留在"进行中"。
- **Release Readiness Review（发布就绪评审）**
  - 做什么：确认 release notes / changelog 与实际变更一致。
  - 为什么选：避免"代码改了但外部记录没闭环"。
  - 不用会怎样：release notes 长期滞后，用户 / 运维不知道这一版改了什么。
- **Handoff Pack Pattern（交接包模式）**
  - 做什么：用结构化 closeout pack 固定证据、状态和下一步，让下个会话能冷启动。
  - 为什么选：让 workflow 跨会话 / 跨人 / 跨机器都能无缝接管。
  - 不用会怎样：下次继续时 agent 又要从头理解"我们走到哪了"。

### 7.7 支线 & 经验沉淀

#### `hf-hotfix`

- **Root Cause Analysis / 5 Whys（根因分析 / 五个为什么，Sakichi Toyoda @ Toyota）**
  - 做什么：从缺陷表象逐层追问到根因。
  - 为什么选：让修复针对根因不是症状。
  - 不用会怎样：修完这次过两周同一类 bug 又出现。
- **Minimal Safe Fix Boundary（最小安全修复边界）**
  - 做什么：显式定义修复边界——改什么 / 不改什么 / 影响什么。
  - 为什么选：防止 hotfix 蔓延成大重构。
  - 不用会怎样：紧急 fix 顺手改了一堆别的，灰度时不知道在验证哪个改动。
- **Blameless Post-Mortem Mindset（无指责复盘，John Allspaw）**
  - 做什么：关注机制和系统性原因，不归咎个人。
  - 为什么选：让事故分析为 bug pattern 和未来改进积累知识。
  - 不用会怎样：每次事故的学习成果都是"下次小心点"。

#### `hf-increment`

- **Change Impact Analysis（Boehm / Pfleeger）**
  - 做什么：系统性分析变更对已批准工件（spec / design / tasks / verification）的影响。
  - 为什么选：让范围变更不是"随口改两句 spec"，而是带影响分析。
  - 不用会怎样：需求一改，已通过的 review / gate 记录就悄悄过时。
- **Re-entry Pattern（State Machine 安全回流）**
  - 做什么：根据影响分析结果，将主链安全回流到唯一 canonical 节点重新开始。
  - 为什么选：让"范围变了"有合法的重入点，不是就地打补丁。
  - 不用会怎样：在当前节点硬改，结果上游工件和下游实现各自漂移。
- **Baseline-before-Change（变更前锁基线）**
  - 做什么：变更前先锁当前基线状态。
  - 为什么选：让变更可追溯、可回退。
  - 不用会怎样：改完发现想回到改动前的状态都找不到快照。
- **Separation of Analysis and Implementation**
  - 做什么：increment 只做分析和工件同步，不直接推进实现。
  - 为什么选：让"分析范围变化"和"实现新功能"不混成一步。
  - 不用会怎样：边分析边改代码，分析结论和实现混在一个 commit 里。

#### `hf-bug-patterns`

- **Defect Pattern Catalog（Boris Beizer / Ostrand）**
  - 做什么：把历史缺陷分类为可复用的模式家族（边界 / null / 状态 / 时序 / 资源泄露 / AI 盲点等）。
  - 为什么选：让团队从错误中系统性学习。
  - 不用会怎样：同样的 bug 在不同 feature 反复出现。
- **Blameless Post-Mortem / Learning Review**（参见 `hf-hotfix`）
- **Human-In-The-Loop Knowledge Curation（人工把关的知识沉淀）**
  - 做什么：经验是否固化为长期目录，由真人确认；AI 不能自动把偶发事件写成团队规范。
  - 为什么选：防止一次性 fluke 被错误固化成"永恒真理"。
  - 不用会怎样：pattern catalog 被噪音淹没，真正的 pattern 找不到。

---

## 想继续深入的几条入口

- `README.zh-CN.md`：pack 全貌与方法论清单
- `docs/principles/hf-sdd-tdd-skill-design.md`：为什么选 spec-anchored SDD + gated TDD
- `docs/principles/skill-anatomy.md`：skill 写作 contract
- `docs/principles/methodology-coherence.md`：30+ 方法论的分工与反替代地图
- `docs/principles/emergent-vs-upfront-patterns.md`：四档模式决策判别器
- `skills/using-hf-workflow/SKILL.md` + `skills/hf-workflow-router/SKILL.md`：看薄 harness 长什么样

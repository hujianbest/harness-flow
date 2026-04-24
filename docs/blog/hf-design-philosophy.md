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

## 想继续深入的几条入口

- `README.zh-CN.md`：pack 全貌与方法论清单
- `docs/principles/hf-sdd-tdd-skill-design.md`：为什么选 spec-anchored SDD + gated TDD
- `docs/principles/skill-anatomy.md`：skill 写作 contract
- `docs/principles/methodology-coherence.md`：30+ 方法论的分工与反替代地图
- `docs/principles/emergent-vs-upfront-patterns.md`：四档模式决策判别器
- `skills/using-hf-workflow/SKILL.md` + `skills/hf-workflow-router/SKILL.md`：看薄 harness 长什么样

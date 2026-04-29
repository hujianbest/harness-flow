# Coding Principles — HF 行为基线（横切原则）

- 定位: 项目级原则文档（HF "宪法层" 的一部分）。定义 HF 中所有 `hf-*` skill 与 agent 行为都必须遵守的 4 条 LLM coding 行为基线。
- 来源: 改写自 [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) 中的 `CLAUDE.md`（基于 Andrej Karpathy 对 LLM coding 常见错误的观察），按 HF 命名与方法论习惯本地化，并与 `soul.md` / `skill-anatomy.md` / `methodology-coherence.md` 对齐。
- 关联:
  - 最高锚点: `docs/principles/soul.md`
  - Skill 写作 anatomy: `docs/principles/skill-anatomy.md`
  - Skill-node 设计契约: `docs/principles/skill-node-define.md`
  - 方法论协作: `docs/principles/methodology-coherence.md`
  - 工件管理: `docs/principles/sdd-artifact-layout.md`

## 定位与适用范围

HF 把 4 条 LLM coding 行为准则当作**横切的行为基线**，而不是一个独立 `hf-*` skill 节点：

- 它们是**所有节点**（`using-hf-workflow` / `hf-workflow-router` / authoring / review / gate / branch / finalize / bug-patterns）共同遵守的行为约束。
- 它们由 HF 宪法层（`docs/principles/`）承载，通过 HF 仓库 design notes 体现；skills 在自己的 `SKILL.md` 中已经吸收并执行这些行为约束，运行时不再外链原文。
- 它们**不**进入 canonical workflow vocabulary（不写进 `Current Stage` / `Next Action Or Recommended Skill` / `Pending Reviews And Gates` / 迁移表 / reviewer return contract）。
- 与 `soul.md` 或项目级约定显式声明冲突时，soul / 项目级约定 优先；本文让位。

设计取舍：把它放成一份独立 skill 会污染 FSM 路由（必须在每个节点的 Workflow 第一步插入"加载 preface"），也会让横切原则被错当成可调度的执行节点。把它落到 principles 层后，所有 skill 自动继承，不需要额外 hook。

## 一、Think Before Coding — 不假设，显式 trade-off

**别假设、别藏混乱、把 trade-off 摊开。**

实现前：

- 把假设显式说出来；不确定就停下来问。
- 出现多种合理解读时，列出来再请用户裁决；不要静默选一个。
- 看到更简单的做法，主动说出来；当应该 push back 时 push back。
- 哪里不清楚，先 stop、命名清楚是哪里不清楚、再问。

在 HF 中的承接：`using-hf-workflow` 的 "单事实分流检查点"；`hf-specify` 的 EARS / Socratic Elicitation；`hf-design` 的 ADR 取舍声明；`hf-test-driven-dev` 的 test design preface（先写 test design 再开始 RED）。

## 二、Simplicity First — 最简实现，YAGNI 到底

**只写解决当前问题的最小代码。**

- 没被要求的功能不要加。
- 单次使用的代码不要为它发明抽象。
- 没人要求的"灵活性 / 可配置性"不要加。
- 不为不可能发生的场景写错误处理。
- 写到 200 行能压到 50 行就重写。

自检问题："一个资深工程师会不会觉得这是 over-engineered？" 是 → 简化。

在 HF 中的承接：`hf-specify` 的 MoSCoW；`hf-design` 的 emergent vs upfront patterns 治理（GoF 模式刻意 emergent）；`hf-test-driven-dev` 的 Two Hats 顺序与 GREEN-之后才允许的 REFACTOR；`hf-code-review` 的 over-engineering 检视。

## 三、Surgical Changes — 外科式改动，只动该动的

**只动你必须动的；只清理你自己造成的脏。**

编辑既有代码时：

- 不"顺手改善"周边代码、注释、格式。
- 不重构没坏的东西。
- 沿用既有风格，即使你个人会换种写法。
- 看到无关 dead code → **指出**，不要顺手删。

你的修改产生孤儿（unused import / 变量 / 函数）时：

- 删除**因你的本次修改才变得无用**的东西。
- 不要顺手删既有 dead code，除非用户明确要求。

测试标准：每一行被修改的代码都能直接溯源到用户的本次请求。

在 HF 中的承接：`hf-test-driven-dev` 的 Two Hats（GREEN 帽子下不重构）/ opportunistic refactoring 边界；`hf-code-review` 的 architectural smells / scope-creep 检视；`hf-increment` 的 change impact analysis。

## 四、Goal-Driven Execution — 目标驱动，循环到可验证

**先定义成功标准，再循环执行到 verified。**

把任务翻译成可验证目标：

- "加一个 validation" → "为非法输入写测试，再让它们通过"
- "修这个 bug" → "写一个能重现 bug 的测试，再让它通过"
- "重构 X" → "重构前后跑同一组测试都通过"

多步任务先给一个简短计划：

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

强成功标准让你能独立循环；弱标准（"让它能跑就行"）会逼你不停回来要澄清。

在 HF 中的承接：`hf-test-driven-dev` 的 fresh RED/GREEN evidence；`hf-regression-gate` 的 impact-based regression；`hf-completion-gate` 的 Definition of Done + evidence bundle；reviewer return contract 中 `key_findings` 的证据锚点要求。

## Trade-off 声明

这 4 条偏向**谨慎优先于速度**。对真正 trivial 的请求（typo 修复、注释改字、单行 config 改动），可按判断省略 ceremony，但**不能**省略 §三（Surgical Changes）的 scope 约束。

## Hard Rules（不让步声明）

- 这些原则**不**进入 canonical workflow vocabulary：不写进 `Current Stage` / `Next Action Or Recommended Skill` / `Pending Reviews And Gates` / 迁移表 / reviewer return 的 `next_action_or_recommended_skill`。
- 这些原则**不**替代 review / gate / approval / finalize 的本地职责（不出 verdict、不写 review 记录、不替代 DoD evidence bundle）。
- 这些原则**不**改变 `hf-workflow-router` 对 profile / mode / Workspace Isolation / canonical 节点的 authoritative 决定。
- 当某个 `hf-*` skill 的具体 workflow step 与这 4 条冲突时，优先按该 skill 的 step 执行，并由 `hf-code-review` / `hf-test-review` / 对应 review 节点把冲突暴露出来；本文不做 runtime 仲裁。

## 与现有原则文档的关系

| 文档 | 关系 |
|------|------|
| `soul.md` | 最高锚点；本文是 soul 在"日常编码行为"层的具体化，与 soul 冲突时让位 |
| `skill-node-define.md` | 定义"skill 如何成为 workflow node"；本文不替代 node contract |
| `skill-anatomy.md` | 定义 skill 写作 anatomy；本文是 skill 行为时的横切基线 |
| `sdd-artifact-layout.md` | 工件路径权威；本文不改路径布局 |
| `methodology-coherence.md` | 方法论协作与冲突地图；本文是其行为侧约束 |

## Verification

agent 在任何 HF 节点的回合开始时，应能在不展开 ceremony 的前提下回答：

- [ ] 当前请求是否包含未说出口的 assumption 或 trade-off？若有，是否已显式列出？
- [ ] 准备产出的工件 / 代码是否包含**未被规格 / 任务 / 用户当前请求显式要求**的能力？
- [ ] 准备改动的每一处是否能溯源到当前请求？是否准备顺手"改善"无关区域？
- [ ] 当前节点的"完成"是否有可验证 check？多步执行是否准备先列计划再走？

以上 4 项命中风险时，应在**目标 skill 自己的输出**里以一行简短说明带过（例如 `Note: 已剔除非显式要求的 X`），不需要为它单独建 review / verification 记录。

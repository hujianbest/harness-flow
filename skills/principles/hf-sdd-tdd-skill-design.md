# HF SDD + TDD Skill 设计 Wiki

## Purpose

本文基于外部 `SDD` / `TDD` 方法论与 skills 生态调研，说明 HF 系列应如何设计一套高质量的 `SDD + TDD` 开发模式 skill workflow。

目标不是直接照搬某个现成 skill，而是提炼出可落到 HF family 的稳定结构、工件约束、路由边界和质量门禁。

## One-Line Thesis

HF 应采用 `spec-anchored SDD + gated TDD`：

- 用 `SDD` 管住 `what / why / constraints / tasks`
- 用 `TDD` 管住单个 `Current Active Task` 的实现与验证
- 用 `router + review + gates` 控制推进，而不是让实现节点自己决定全链路

## External Findings

### 值得借鉴的公开 skills

| Skill | 信号 | 值得借鉴 | 不建议直接照搬 |
|---|---|---|---|
| [`obra/superpowers@test-driven-development`](https://skills.sh/obra/superpowers/test-driven-development) | 约 51.7K weekly installs，约 154.2K GitHub stars | 强约束 TDD、反合理化、`no production code without a failing test first`、completion 前验证意识 | `superpowers` 的重型多 skill 编排不必原样复制到 HF |
| [`addyosmani/agent-skills@spec-driven-development`](https://skills.sh/addyosmani/agent-skills/spec-driven-development) | 约 1.1K weekly installs，约 15.7K GitHub stars | `Specify -> Plan -> Tasks -> Implement` 四段 gated workflow、assumption surfacing、success criteria、boundaries | 小任务也强行走长 spec 会过重，不适合直接作为 HF runtime contract |

可直接安装作参考：

```bash
npx skills add https://github.com/obra/superpowers --skill test-driven-development
npx skills add https://github.com/addyosmani/agent-skills --skill spec-driven-development
```

### 核心方法论来源

- [Martin Fowler: Understanding Spec-Driven Development](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [GitHub Spec Kit blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Thoughtworks: Spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: Test Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Kent Beck: Canon TDD](https://tidyfirst.substack.com/p/canon-tdd)

## What HF Should Borrow

### 从 SDD 借什么

综合 GitHub、Thoughtworks、Fowler，可以稳定提炼出以下共识：

1. 先写 spec，再让 AI 或 Agent 动手实现；spec 不是“大一点的 prompt”，而是结构化工件。
2. spec 至少要表达行为目标、边界、约束、成功标准，而不只是需求口号。
3. 规划与实现要分层：`Specify -> Plan -> Tasks -> Implement` 是目前最稳的骨架。
4. 每一层都要有明确 checkpoint，不允许“写完再回头补”。
5. spec 需要保持可回读、可更新，否则很快退化成一次性草稿。

### 从 TDD 借什么

综合 Kent Beck 与 Fowler，可以稳定提炼出以下共识：

1. `Canon TDD` 不是只记住 `Red -> Green -> Refactor`，而是先写 `test list`。
2. 每次只把一个 test list item 变成真正可运行测试。
3. 必须先看到测试因预期原因失败，才知道它真的在测对的行为。
4. 让测试通过时只写最小实现，不把重构混进去。
5. 通过后才做必要重构，然后进入下一个行为。

对 HF 来说，最值得吸收的不是“测试先写”这句口号，而是这两个纪律：

- 没有 failing test，不写生产代码。
- 没有 fresh evidence，不宣称完成。

## HF 的关键设计判断

### 1. 选 `spec-anchored`，不要走 `spec-as-source`

Fowler 将 SDD 区分为三档：

- `spec-first`
- `spec-anchored`
- `spec-as-source`

HF 更适合第二档，也就是 `spec-anchored`。

原因：

- HF 已经有代码、测试、review、gate、progress state 等运行时工件。
- HF 需要支持 brownfield 场景，而不是只做从 spec 到代码的单向生成。
- `spec-as-source` 在现阶段会把 HF 推向更重的模型驱动体系，收益不稳定，约束成本却很高。

因此，HF 应把 spec 视为：

- 上游权威意图工件
- review 与 traceability 的锚点
- 后续变更时必须同步更新的活文档

但不把 spec 视为唯一可编辑源。

### 2. 不做“一个总 skill”，而做 family

高质量的 `SDD + TDD` workflow 不应该被压扁成一个巨型 skill。

更稳的做法是四层分离：

| 层 | 回答的问题 | HF 对应面 |
|---|---|---|
| public entry | 这个会话应从哪进 | `using-hf-workflow` |
| runtime routing | 当前 canonical 下一步是什么 | `hf-workflow-router` |
| SDD authoring | 要做什么、为什么做、如何拆解 | `hf-specify` / `hf-design` / `hf-tasks` |
| TDD execution | 单个活跃任务如何实现并验证 | `hf-test-driven-dev` + 质量链 |

这样做的收益：

- `entry`、`route`、`authoring`、`implementation` 的职责不混。
- 叶子 skill 不会顺手接管 orchestrator 逻辑。
- review 和 gate 能保持独立性。

### 3. 工件驱动必须强于对话记忆

HF 的 `SDD + TDD` 体系要站得住，关键不在 prompt 漂不漂亮，而在工件是否权威。

最少应保证以下工件层（路径以 `skills/principles/sdd-artifact-layout.md` 为唯一权威，本节仅列工件类别；本文件不重复定义具体目录）：

- `spec`         → 默认落在 `features/<NNN-slug>/spec.md`
- `design`       → 默认落在 `features/<NNN-slug>/design.md`（ADR 通过编号引用 `docs/adr/` 中的 ADR 本体）
- `tasks`        → 默认落在 `features/<NNN-slug>/tasks.md`
- `progress`     → 默认落在 `features/<NNN-slug>/progress.md`（feature 唯一权威；不再保留全局 `task-progress.md`）
- `reviews`      → 默认落在 `features/<NNN-slug>/reviews/`
- `approvals`    → 默认落在 `features/<NNN-slug>/approvals/`
- `verification` → 默认落在 `features/<NNN-slug>/verification/` 与 `features/<NNN-slug>/evidence/`
- `CHANGELOG`    → 仓库根 `CHANGELOG.md`（必备，Keep a Changelog 惯例）；`docs/release-notes/vX.Y.Z.md` 仅在 `sdd-artifact-layout.md` 档 2 启用时存在。

> 路径冲突或扩展时以 `sdd-artifact-layout.md` 为准。本文件不重复定义具体目录。

原则：

- route 看工件，不看聊天记忆。
- approval 要落盘，不能只留在对话里。
- 实现交接块、review 记录、verification 记录必须可回读。

### 4. SDD 阶段之间必须有显式 checkpoint

GitHub Spec Kit 最大的启发不是“文件很多”，而是“每阶段先验证，再进入下一阶段”。

HF 应保留以下 checkpoint：

- `hf-spec-review` + `规格真人确认`
- `hf-design-review` + `设计真人确认`
- `hf-tasks-review` + `任务真人确认`
- `hf-test-driven-dev` 内部的测试设计确认
- `hf-regression-gate`
- `hf-completion-gate`

这意味着：

- review 通过不等于 approval 已完成
- `Execution Mode=auto` 也不能跳过 approval record
- 实现不能反向吞掉 review/gate 职责

### 5. TDD 应只在唯一活跃任务上运行

Kent Beck 的 `Canon TDD` 强调“一次一个测试”，HF 则应进一步强调“一次一个活跃任务”。

也就是说：

- `hf-workflow-router` 锁定唯一 `Current Active Task`
- `hf-test-driven-dev` 只处理这一个任务
- 当前任务的质量链未闭环前，不切下一任务
- 若存在下一个 `next-ready task`，也要先回 router，再重新进入实现

### 6. HF 的 TDD 应保留“测试设计确认”这一步

纯 `Canon TDD` 的核心是 `test list -> test -> pass -> refactor`。

但对 HF 这种面向仓库级 workflow 的 family，建议继续保留当前 `hf-test-driven-dev` 已经采用的前置步骤：

1. 读任务与上下文
2. 产出测试设计
3. 完成测试设计确认
4. 再进入 `Red -> Green -> Refactor`

这样做的价值：

- 让“测什么”先稳定，再动手写测试
- 避免 Agent 直接把错误接口或错误边界写进第一版测试
- 让 tasks 文档中的测试种子真正成为实现输入

### 7. `fresh evidence` 不是可选优化，而是主合同

HF 的实现质量不应靠“我觉得修好了”，而应靠当前会话内可追溯的证据。

因此至少要保留：

- `RED evidence`
- `GREEN evidence`
- `regression evidence`
- `completion evidence`

如果缺其中任一个，允许的结论只能是：

- 继续实现
- 回到 review / gate
- 回 router 重编排

不允许说“完成”。

### 8. profile 要影响流程密度，但不能让纪律消失

Fowler 和 Thoughtworks 都在提醒一个问题：SDD 很容易过重。

因此 HF 用 `full / standard / lightweight` 是对的，但必须满足：

- `lightweight` 不是“直接开始写代码”
- `lightweight` 仍然要经过任务层、实现层和至少两道 gate
- profile 只调节密度，不取消 `spec/plan/task/test/evidence` 的基本纪律

## 推荐的 HF 主骨架

### SDD 主骨架

```text
using-hf-workflow
  -> hf-workflow-router
  -> hf-specify
  -> hf-spec-review
  -> 规格真人确认
  -> hf-design
  -> hf-design-review
  -> 设计真人确认
  -> hf-tasks
  -> hf-tasks-review
  -> 任务真人确认
```

### TDD 与质量主骨架

```text
hf-test-driven-dev
  -> hf-test-review
  -> hf-code-review
  -> hf-traceability-review
  -> hf-regression-gate
  -> hf-completion-gate
  -> hf-finalize
```

`hf-bug-patterns` 更适合作为独立经验固化旁路：当 AI 识别到“这类错误以前犯过，而且值得沉淀成长期模式”时触发，先询问真人是否要固化到 bug pattern catalog，而不是作为 canonical gate 卡在 `hf-test-review` 之前。

### 支线

```text
hf-hotfix    -> 先复现、收敛边界，再 handoff 回实现主链
hf-increment -> 先影响分析、同步工件，再重入正确主链节点
```

支线和 closeout 的设计判断应保持在“职责边界”层，而不是把 live runtime 细则再次抄进原则文档。也就是说：branch 节点负责分析和 re-entry，closeout 节点负责正式收口；更细的 precheck / reroute / closeout record contract 应留在各自 `SKILL.md` 与 family shared docs。

这条设计的核心是：

- `SDD` 负责把任务变得“可正确实现”
- `TDD` 负责把任务变成“可正确验证的代码”
- `review/gate` 负责把“我以为完成了”变成“证据证明完成了”

## 每个层级应该承担什么

| Surface | 应承担的主合同 | 不应承担的事情 |
|---|---|---|
| `using-hf-workflow` | 判断 `direct invoke` 还是 `route-first` | runtime recovery、完整状态机、代码修改 |
| `hf-workflow-router` | 依据工件决定 profile、stage、next node | 直接代替 leaf skill 完成正文产出 |
| `hf-specify` | 澄清目标、边界、成功标准、非范围 | 提前写设计或实现细节 |
| `hf-design` | 给出方案、取舍、接口、风险、测试策略 | 把设计写成任务清单 |
| `hf-tasks` | 产出可执行任务、DoD、验证方式、测试种子 | 提前开始编码 |
| `hf-test-driven-dev` | 先测什么、如何 fail、最小实现、fresh evidence、handoff | 换任务、跳过测试、串起完整下游质量链 |
| review skills | 发现问题、给出 verdict 与唯一下一步 | 顺手回修正文或实现 |
| `hf-hotfix` / `hf-increment` | 做分支分析、边界收敛与 canonical re-entry | 直接改代码，或在证据冲突时伪造 handoff |
| gate skills | 消费 fresh evidence，判断能否继续 | 用对话记忆代替证据 |
| `hf-finalize` | 消费 gate 结论，完成状态 / 文档 / release 收口 | 混入新实现，或在收尾证据不稳时伪造完成结论 |

## 推荐的工件最小内容

### `spec` 应至少包含什么

在本仓库中，逻辑 `spec` 默认对应 `features/<NNN-slug>/spec.md`（以 `skills/principles/sdd-artifact-layout.md` 为权威）。

建议最少包含：

- 目标与用户价值
- 范围 / 非范围
- 关键行为与验收标准
- 约束与边界
- 成功标准
- 未决问题
- 显式 assumptions

### `design` 应至少包含什么

- 方案候选与取舍
- 选定方案
- 模块/接口/数据流
- 关键约束与不变量
- 风险与缓解
- 测试策略

### `tasks` 应至少包含什么

每个任务至少写清：

- Task ID
- 任务目标
- Acceptance
- Verify
- Files
- Dependencies
- 测试设计种子

### `实现交接块` 应至少包含什么

- Task ID
- 回流来源
- 触碰工件
- 测试设计确认证据
- `RED evidence`
- `GREEN evidence`
- 剩余风险 / 未覆盖项
- `Pending Reviews And Gates`
- `Next Action Or Recommended Skill`

## 为什么不建议直接把外部 skill 装进 HF 当 runtime contract

可以安装外部 skill 做研究和对照，但不建议直接拿来替换 HF 节点。

原因：

- HF 已有自己的 canonical node vocabulary
- HF 已有自己的 progress schema、approval vocabulary、review return contract
- HF 已有 router / review-dispatch / worktree / gate 语义

因此更合理的策略是：

1. 借鉴外部方法论
2. 借鉴外部 eval 思路和 anti-rationalization 写法
3. 保持 HF 自己的 leaf skill contract 不变

## 反模式

以下做法会让 `SDD + TDD` skill workflow 很快退化：

- 把所有问题都拉成冗长 spec，导致 review overload
- spec 写完就不再维护，进入实现后与代码脱节
- 把需求、设计、任务写进同一份大文档
- 在 `hf-test-driven-dev` 里同时切换多个任务
- “先写代码，最后补测试” 还叫 TDD
- 用旧测试结果充当当前 `fresh evidence`
- `auto mode` 下直接跳过 approval record
- 让 review skill 顺手回修，让实现 skill 顺手决定完整下游链路
- 把 branch / closeout 的 live runtime 细则同时写进原则文档、shared docs 和 leaf skill，导致层级冲突

## 对 HF 的落地建议

如果 HF 下一步要继续把这套体系做实，推荐顺序如下：

1. 先把这份 wiki 当作方法论基线，统一 `SDD + TDD` 的术语和边界。
2. 为 `hf-specify` 补强 spec 模板，特别是 `assumptions / boundaries / success criteria`。
3. 为 `hf-design` 补强 `options + tradeoffs + risks + test strategy` 结构。
4. 为 `hf-tasks` 强化 `Acceptance / Verify / Files / test seed` 四元结构。
5. 继续保持 `hf-test-driven-dev` 的“测试设计确认 + Canon TDD + fresh evidence”三段式。
6. 把外部 skill 的强约束语言吸收到 evals 中，专门测试“跳过 spec”“跳过 failing test”“无证据宣称完成”这几类合理化。

## Bottom Line

HF 要做的不是“再造一个 AI 编码神器”，而是把 AI 编码约束到团队认可的工程节奏里。

对这件事来说，最稳的组合不是：

- 只有 spec，没有验证
- 只有 TDD，没有上游意图工件
- 只有单 skill，没有分层路由

而是：

- `spec-anchored SDD` 保证方向正确
- `gated TDD` 保证实现可信
- `router + review + gates + fresh evidence` 保证整个 workflow 可恢复、可审计、可扩展

这也是 HF 系列设计 `SDD + TDD` skill workflow 时最应该坚持的主线。

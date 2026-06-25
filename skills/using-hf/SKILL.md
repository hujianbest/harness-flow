---
name: using-hf
description: HarnessFlow 工作流的入口。在以下情况使用：开始一个新的开发任务、不确定当前该做规格/设计/实现中的哪一步、需要从已有工件恢复进度、或用户提到 HarnessFlow / 规范驱动开发 / 高质量开发流程时。
---

# 使用 HarnessFlow

## §1 HarnessFlow 是什么

HarnessFlow 把「产出高质量代码」拆成由外到内的三层质量。第一、二层有阶段技能承载；第三层是贯穿设计、实现、评审的质量约束：

| 层 | 回答的问题 | 失败模式（无此层时） | 承载技能 |
|---|---|---|---|
| 第一层 SDD | 做的是不是对的事？ | 需求含糊 → 模型靠猜 → 做错事 | hf-specify |
| 第二层 TDD | 功能被证明正确了吗？ | 代码未验证 → 一堆 bug 给人 | hf-tdd |
| 第三层 Clean Code | 代码本身写得好吗？ | 能跑但烂 → 难维护/审查/演进 | hf-clean-code + *-coding-standards + 领域技能 |

前两层保证外部质量（做对的事、做对），第三层保证内在质量（做好）。`hf-design` 是设计阶段：它通过结构、接口契约、错误模型和测试设计为第三层奠基；实现和评审时仍必须叠加 `hf-clean-code` 与适用语言/领域技能。三层不是三个产物，而是同一份代码的三个维度。目标一句话：**在 SDD 范式下写 Clean Code，而不是仅仅能运行的代码。**

协作姿态是 **human-on-the-loop**：具体的活由 AI 干，人站在环上审查关键产物（规格、设计、测试、代码）。因此每个阶段的产物都必须**可冷读、可审查**——这是所有技能共同的硬要求。

## §2 工作流

```text
需求/任务到达 ──→ [0] 确认运行模式（见下）
    |
    v
[1] hf-specify      写 spec.md + plan.md 骨架 + 初始化 traceability.md
    |
[R1] hf-review      独立评审规格 → 记录到 reviews/ ──[人工确认]──
    v
[2] hf-design       影响组件边界时先修订 component-design-draft.md；
    |                写 design.md：职责、接口契约、错误模型、测试设计
[R2] hf-review      独立评审设计 → 记录到 reviews/ ──[人工确认]──
    v
[3] hf-tdd          细化 plan.md 任务；按测试设计逐用例 RED→GREEN→REFACTOR；
    |                默认逐任务派发 hf-implementer；叠加 hf-clean-code 与语言/领域规范
[R3] hf-review      独立评审测试与代码 → 记录到 reviews/ ──[人工确认]──
    v
[4] hf-ship         DoD 核验 + 追溯终验 + promotion 长期资产 + closeout ── 人确认关闭 ── 完成
```

**评审是必经节点，不是可选预审**：每个阶段产物完成后必须经 `hf-review` 独立评审并把记录写入 `reviews/`，评审通过（且按运行模式获得人工确认）之前不进入下一阶段。跳过任何一个 R 节点直接进入下一阶段，都是流程违规。

## §3 轻量状态机

HarnessFlow 不维护独立路由器或额外状态文件；`plan.md` 的门禁表、任务状态、`reviews/` 记录就是可恢复状态。恢复或续作时按下面语义解释门禁：

| 状态 | 含义 | 下一步 |
|---|---|---|
| pending | 产物就绪未评审 | 去 hf-review 执行对应 R 门禁 |
| passed | verdict 通过；attended 下还要看人工确认列 | 确认列 yes/N/A 进下一阶段；no 则呈人 |
| rework | 评审打回，有未闭环 findings | 先回作者阶段定向返工，回填 Resolution 后复审 |

R1 `rework` 默认回 `hf-specify`；R2 `rework` 默认回 `hf-design`；R3 `rework` 默认回 `hf-tdd`。只有评审明确指出规格漏洞、设计方向错误、工件间漂移需要改上游时，才回更上游阶段。`pending` 和 `rework` 不能混用：`pending` 是去评审，`rework` 是先修再评审。同一 R 节点最多自动返工复审 3 轮，仍不通过则升级人裁决。

## §4 Todo 投影规则

当需要生成 todo / 计划 / 执行队列时，把上面的生命周期按节点原样投影：

- **阶段节点、R 门禁节点、ship 节点都是一级待办**：原样映射，不合并、不重排。
- `hf-specify` 完成只表示 spec/traceability/plan 骨架就绪，下一条待办必须是 R1 `hf-review`；同理 `hf-design` 完成后下一条必须是 R2 `hf-review`。
- `hf-tdd` 内部的多个任务**不是多个人工确认节点**：任务 `DONE` 后只要 plan.md 能唯一选择下一任务，就继续执行；只有 plan.md 无法唯一判定下一任务（缺业务事实、阈值或专家取舍）时才停下提问。
- R3 打回时，下一条待办必须是 `hf-tdd` 定向返工与回填 Resolution，随后才是 `hf-review` 复审；不得把 `rework` 当成「立刻再评审」——先修，再评审。
- `attended` 的人工确认附着在对应 R 节点 verdict **之后**，不替代独立评审，也不发生在评审之前；`unattended` 只移除人工停顿，不移除任何 R 节点。

## §5 运行模式（attended/unattended）

启动工作流时**先确认一次运行模式**（首次明确问用户，或从 plan.md 头部读取已记录的模式），并把答案记入 plan.md 头部：

| 模式 | 行为 |
|---|---|
| attended（默认） | R 节点通过后停下呈人确认；TDD 任务间不停；可由 AI 修复的 findings 仍先自动返工复审 |
| unattended | R 节点后不停连续执行；仅在缺业务事实/规格设计不可决策/专家裁决/3 轮仍不通过时停 |

**关键：unattended 只移除人工停顿，不移除任何质量动作**（独立评审、记录、critical 阻塞、DoD 照做）。所有评审记录留存在 `reviews/`，供人事后统一审计。用户未明确回答时按 `attended` 执行；模式记录后，恢复执行的会话**沿用 plan.md 中的模式，不重新猜测**。

旁路：**缺陷修复**走 `hf-fix`（复现 → 根因 → 最小修复），其中修复实现仍回到 TDD（先写复现缺陷的失败测试），修复后的测试与代码同样经 R3 评审，收尾同样经 `hf-ship`。

阶段允许回溯：写测试时发现规格漏洞就回去补规格；实现时发现设计错误就回去改设计。回溯时更新对应工件并让受影响的评审重新进行，不要让代码与工件漂移。

## §6 何时可以裁剪

- **微小修改**（几行、无接口变化、风险低）：spec 可压缩成 plan.md 里的一段验收标准，design 可省略（R1/R2 随之合并入 R3），但 TDD、R3 评审与 clean code 不裁剪。
- **纯重构**（行为不变）：不需要 spec/design，但必须有覆盖现有行为的测试先行，且代码评审（R3）照做。
- **拿不准时不裁剪**。裁剪的是**文档量**，永远不是**质量门槛**（测试先行、证据行、独立评审与记录、人工确认（attended 模式）、DoD 核验、整洁标准）。

## §7 工件约定

### 路径解析纪律

HarnessFlow 工件路径一律相对于**目标组件仓库根目录**解析，而不是相对于当前会话所在目录或 HarnessFlow skills 仓库。开始、恢复、评审、实现、收尾前都先确定组件根，优先级如下：

1. 用户显式给出组件目录时，以该目录为组件根；
2. 否则读取目标仓库根的 `AGENTS.md` / 团队约定，若声明目标组件根或路径覆盖则遵循；
3. 仍无法确定时，使用当前工作目录所在的组件仓库根；如果当前目录不是目标组件仓库，先停下询问。

产出前先在回复或 plan.md 头部写明解析出的组件根与工件根，避免把工件误建到上级仓库根。组件仓库根 `AGENTS.md` 的 `## Project overrides` 可以覆盖这些相对路径与模板约定；覆盖后所有阶段必须使用覆盖路径。

### 工作项目录结构

每个工作项一个目录（`<id>-<slug>`，或团队等价编号）：

```text
features/<id>-<slug>/
  spec.md                     # 规格（hf-specify 产出）
  traceability.md             # 追溯矩阵：spec-design-code 一致性约束（specify 初始化，逐阶段补列）
  component-design-draft.md   # 组件级设计修订（影响组件边界时，hf-design 产出）
  design.md                   # 工作项级设计（hf-design 产出）
  plan.md                     # 执行计划：运行模式、阶段门禁状态、任务拆解与证据行；
                              #   中断恢复的单一入口（specify 建骨架，tdd 细化并维护）
  reviews/                    # 评审记录：每轮一份，findings + resolution 闭环（hf-review 产出）
  closeout.md                 # 收尾记录（hf-ship 产出）
```

长期资产在组件根下 `docs/`（`component-design.md`、`ar-specs/`、`ar-designs/`，或团队覆盖路径），由 `hf-ship` 在收尾时从过程工件 promotion，平时各阶段只读。

工件与聊天记忆冲突时，**以工件为准**。

### 恢复进度时

恢复进度时**先读 `plan.md`**（运行模式 + 阶段门禁状态 + 当前任务），再按工件状态校验，不依赖聊天记忆：

| 磁盘状态 | 下一步 |
|---|---|
| 目录不存在 / spec.md 缺失 | `hf-specify`（启动时确认运行模式） |
| R1 为 `rework`，或 spec 评审有未闭环 critical/important findings | `hf-specify` 定向修复；缺业务事实时只问最小问题；修复后回填 Resolution 并复审 |
| spec.md 存在，R1 为 `pending` 或 reviews/ 无 spec 评审记录 | `hf-review`（R1） |
| R1 verdict 通过但 attended 人工确认列为 no | 呈人确认 R1 评审记录；同意后再进入 `hf-design` |
| R1 已通过且确认完成，design.md 缺失（含组件边界受影响但组件设计未修订） | `hf-design` |
| R2 为 `rework`，或 design 评审有未闭环 critical/important findings | `hf-design` 定向修复；需要架构/专家裁决时停下；修复后回填 Resolution 并复审 |
| design.md 存在，R2 为 `pending` 或 reviews/ 无 design 评审记录 | `hf-review`（R2） |
| R2 verdict 通过但 attended 人工确认列为 no | 呈人确认 R2 评审记录；同意后再进入 `hf-tdd` |
| R2 已通过且确认完成，plan.md 有未完成任务 | `hf-tdd`（进入连续任务循环，从 plan.md 第一个唯一可执行的未完成任务继续） |
| R3 为 `rework`，或测试/代码评审有未闭环 critical/important findings | `hf-tdd` 定向返工；回填 Resolution 后复审，最多自动循环 3 轮 |
| 任务全部完成，R3 为 `pending` 或 reviews/ 缺测试/代码评审记录 | `hf-review`（R3） |
| R3 verdict 通过但 attended 人工确认列为 no | 呈人确认 R3 评审记录；同意后再进入 `hf-ship` |
| 评审 verdict 指向规格/设计漂移 | 回 `hf-design` / `hf-specify` 修正上游工件，并重新经过受影响的 R 门禁 |
| 全部门禁通过，closeout.md 缺失 | `hf-ship` |

## §8 行为准则

适用于所有 HarnessFlow 技能，不可协商：

1. **不默默补全模糊需求。** 实现任何非平凡内容前显式列出假设，请人确认或写入 spec。最常见的失败是做错假设并在未经检查下继续推进。
2. **困惑时停下，不猜。** 遇到冲突需求、不一致工件、缺失阈值：指出具体困惑，提出澄清问题或交回对应负责人。
3. **方案有问题就说。** 不当 yes-machine：直接指出问题、量化缺点、给替代方案；对方知情后仍坚持则执行。
4. **强制简单。** 完成前自问：能用更少代码吗？抽象配得上它引入的复杂度吗？资深工程师会不会说「为什么不直接……」？
5. **范围纪律。** 只改任务要求改的。路过的问题登记，不顺手修；不删不理解的代码；不在 spec 外加功能。
6. **验证，而非声称。** 「看起来对」永远不够。完成的依据是通过的测试、构建输出、评审记录。
7. **作者不自审，阶段必评审。** 每个阶段产物完成后必须经独立上下文（subagent 或新会话）评审并落盘记录；attended 模式下人工确认后才进入下一阶段，unattended 模式下评审与记录照做、critical 照样阻塞。

## §9 技能地图

| 技能 | 一句话 | 何时读 |
|---|---|---|
| `using-hf` | 工作流入口：三层模型、状态机、工件约定、行为准则 | 开始任务、不确定下一步、恢复进度 |
| `hf-specify` | 把意图写成可测试的规格 | 开始新工作项、规格被评审打回 |
| `hf-design` | 做出值得长期持有的软件设计；为第三层奠定结构、契约、错误模型和测试设计 | 规格确认后、设计被打回、实现中发现设计问题 |
| `hf-tdd` | 用 RED→GREEN→REFACTOR 证明功能正确 | 设计确认后的全部实现期 |
| `hf-review` | 独立评审规格/设计/测试/代码 | 每个阶段产物完成后 |
| `hf-ship` | DoD 核验、promotion 长期资产、closeout | 评审闭环后的收尾 |
| `hf-fix` | 复现 → 根因 → 最小修复 | 缺陷、回归、线上问题 |
| `hf-clean-code` | 把代码写整洁：覆盖简洁、可靠、可维护、可测试、高性能的内在质量 | 写代码、REFACTOR 与代码评审时必读 |
| `c-coding-standards` | C 语言级规则与惯用法 | 工作项含 C 代码时叠加 |
| `cpp-coding-standards` | C++ 语言级规则与惯用法 | 工作项含 C++ 代码时叠加 |
| `java-coding-standards` | Java 语言级规则与惯用法 | 工作项含 Java 代码时叠加 |
| `python-coding-standards` | Python 语言级规则与惯用法 | 工作项含 Python 代码时叠加 |
| `coding-standards-creator` | 把团队编码规范转化为新的语言规范技能 | 需要新建或修订某语言的 coding-standards 时 |
| `backend-development` | 后端领域特有质量约束、设计红线与验证证据 | 工作项命中后端领域触发条件 |
| `frontend-development` | 前端领域特有质量约束、设计红线与验证证据 | 工作项命中前端领域触发条件 |

语言与领域技能是**叠加约束**：它们在规格、设计、实现、评审各阶段被对应技能消费，自身不是流程阶段。

**语言标准按 `<language>-coding-standards` 命名约定发现**：工作项触及语言 X 的代码 → 叠加 `<x>-coding-standards`（存在时）。新增语言技能只要遵循同一份结构契约（`coding-standards-creator/references/hf-skill-quality-contract.md`），无需改动任何阶段技能即可接入；技能尚不存在而团队有该语言规范时，用 `coding-standards-creator` 生成。

**领域技能按 description 发现**：工作项的业务/技术语境命中某个领域开发技能的 frontmatter description 时，加载该领域技能并把它加入 Quality Stack。核心 HarnessFlow 不维护领域技能枚举；新增领域技能时，应把触发词、适用边界、易混淆场景写进该技能自己的 description，让入口、实现、评审和收尾都通过「适用领域技能」这一通用类别消费它。

# HarnessFlow 核心架构

> 本文定义 HarnessFlow 从核心理念到技能体系的架构映射。任何技能、命令、agent 的修改都应能回溯到 [`harnessflow-philosophy.md`](harnessflow-philosophy.md) 的三层质量模型与 human-on-the-loop 协作姿态。

## 1. 架构目标

HarnessFlow 的目标一句话：**在 SDD 范式下写 Clean Code，而不是仅仅能运行的代码。**

为此架构遵循两条设计原则：

1. **流程最小化**：流程只保留产生质量的部分——阶段产物、人审把关点、TDD 纪律、独立评审。不维护额外节点路由器或多字段状态文件；进度从 `plan.md`、`reviews/` 与工件本身恢复。
2. **内容最大化**：每个技能的主体是可操作的工程判断（规则 + 正反例 + 自检清单），而不是流程样板。技能写法遵循 progressive disclosure：frontmatter 描述触发条件，SKILL.md 承载核心判断，references/ 承载详表与模板。

## 2. 三层质量模型到技能的映射

| 层 | 目标 | 承载 |
|---|---|---|
| 第一层 SDD | 意图正确：做对的事 | `hf-specify`（可测试的规格 + 追溯矩阵初始化） |
| 第二层 TDD | 功能正确：证明做对 | `hf-design` 的测试设计章节 + `hf-tdd`（RED→GREEN→REFACTOR + 测试质量） |
| 第三层 Clean Code | 内在质量：写得好、值得长期持有 | `hf-design`（结构/契约/错误模型）+ `hf-clean-code`（命名/函数/控制流/重构）+ 语言/领域扩展 |

第三层不是流程阶段，而是贯穿设计、实现、评审的质量标准。`hf-review` 在每层出口处提供独立检验，人做最终把关。

## 3. 技能体系

HarnessFlow 的技能体系由 15 个技能组成，分四类。完整清单（必须与 `scripts/validate_harnessflow.py` 的 `EXPECTED_SKILLS` 一致）：

```text
阶段技能（7）：
  using-hf/                   # 入口：三层模型、工作流、工件约定、行为准则
  hf-specify/                 # 第一层：可测试的规格 + 追溯矩阵初始化
  hf-design/                  # 设计：组件级 + 工作项级两级设计，含质量增补章节
  hf-tdd/                     # 第二层：测试先行实现（默认派发 implementer subagent，证据行落盘）
  hf-review/                  # 独立评审：四类 rubric（spec/design/test/code）
  hf-ship/                    # 收尾：DoD 核验 + promotion 长期资产 + closeout
  hf-fix/                     # 缺陷修复：复现 → 根因 → 最小修复

overlay 技能（5）：
  hf-clean-code/              # 第三层内核：整洁代码标准与重构目录
  c-coding-standards/         # 语言扩展
  cpp-coding-standards/       # 语言扩展
  java-coding-standards/      # 语言扩展
  python-coding-standards/    # 语言扩展

领域技能（2）：
  backend-development/        # 领域扩展
  frontend-development/       # 领域扩展

工具技能（1）：
  coding-standards-creator/   # 把团队编码规范转化为新的 <language>-coding-standards
```

四类技能：

- **阶段技能**（using-hf / hf-specify / hf-design / hf-tdd / hf-review / hf-ship / hf-fix）：有工作流、有产物、有人审把关点。其中 `using-hf` 是入口技能，承载三层模型、主流程闭环、工件约定与行为准则；其余六个是工作流阶段。
- **overlay 技能**（hf-clean-code 与四个 `*-coding-standards`）：提供贯穿各阶段的质量约束与判据，被阶段技能引用，自身不是阶段。`hf-clean-code` 是第三层的通用内核；语言标准按 `<language>-coding-standards` 命名约定发现。
- **领域技能**（backend-development / frontend-development）：提供领域特化的质量维度，按 description 触发。
- **工具技能**（coding-standards-creator）：生成与维护语言扩展技能本身，不参与工作项流程。

依赖方向：阶段技能只引用 overlay 技能的通用类别与 `using-hf` 的发现约定；语言标准之间、领域技能之间不互相点名依赖。overlay 技能可以声明自己建立在 `hf-clean-code` 之上，但跨扩展协作靠触发描述和 Quality Stack 组合完成，而不是在已有技能中维护具体扩展清单。

### 语言标准的扩展机制

语言标准按 `<language>-coding-standards` 命名约定接入。扩展性由三件事保证：

1. **约定式引用**：所有阶段技能、rubric、DoD、命令只写「适用的 `<language>-coding-standards`」，不枚举具体语言——新增语言零改动接入。
2. **结构契约**：每个语言技能满足同一份契约（`coding-standards-creator/references/hf-skill-quality-contract.md`）：命名、frontmatter 触发条件、只收语言级规则的边界、规则三要素（可判定 + 事故类 + 正反例）、规模上限、消费点、evals。
3. **生成工具**：`coding-standards-creator` 把团队内部编码规范文档转化为符合契约的新技能：逐条归属判定（语言级收录 / 通用引用 clean-code / 领域移交 / 流程剔除）、规则提炼改写、接入注册、交人验收。

## 4. 工作流与工件

### 工件约定

每个工作项目录默认位于目标组件仓库根目录下的 `features/<id>-<slug>/`，包含以下工件（逐字列出）：

- `spec.md` — 范围、需求条目、验收标准、接口候选契约。
- `traceability.md` — 追溯矩阵：需求→设计→测试→代码→证据，spec-design-code 一致性约束。
- `design.md` — 工作项级设计：职责、接口契约、错误模型、测试设计、质量增补章节。
- `component-design-draft.md` — 组件级设计修订草稿：当工作项影响组件边界时由 `hf-design` 产出，收尾时由 `hf-ship` promotion 为长期资产 `docs/component-design.md`。
- `plan.md` — **中断恢复的单一入口**：组件根、工件根、运行模式、门禁状态表、自包含任务拆解 + 每任务 RED/GREEN 证据行。
- `reviews/` — 每轮一份评审记录（findings 含 Resolution 列 + verdict + 抽查记录 + 人工确认）。
- `closeout.md` — DoD 核验摘要、promotion 路径表、债务去向。
- 缺陷工作项另走 `fix.md` — 复现、根因、修复边界。

长期资产默认位于同一组件根下的 `docs/`：`component-design.md`、`ar-specs/`、`ar-designs/`。由 `hf-ship` 在收尾时从过程工件 promotion：保留原 spec/design/component-design 模板主体，只清理 Open Questions、过程笔记和评审应答；其他阶段只读。组件级设计是团队开发流程要求：影响组件边界的工作项必须先修订组件设计并经模块架构师确认。

进度恢复规则在 `using-hf` 中定义：按工件存在性与确认状态判断下一步，工件优先于聊天记忆。

### 运行模式表

| 模式 | 行为 |
|---|---|
| attended（默认） | R 节点通过后停下呈人确认；TDD 任务间不停；可由 AI 修复的 findings 仍先自动返工复审 |
| unattended | R 节点后不停连续执行；仅在缺业务事实/规格设计不可决策/专家裁决/3 轮仍不通过时停 |

**unattended 只移除人工停顿，不移除任何质量动作**（独立评审、记录、critical 阻塞、DoD 照做）。同一 R 节点最多自动返工复审 3 轮，仍不通过升级人裁决。

这条规则是 unattended 模式的设计红线：连续执行不等于放松质量。它只是把「等人点确认」这一停顿拿掉，评审的门禁、findings 的落盘、critical 问题的阻塞、DoD 的核验一项不少。否则 unattended 就会退化为「无人值守地堆积未审产出」，与 human-on-the-loop 的根本姿态冲突。3 轮上限则是为了防止评审与返工陷入无限循环——卡住时升级人裁决，比让模型在同一处反复打转更负责任。

## 5. 角色分离（subagent）

HarnessFlow 的角色分离由 subagent 承载：

- **作者不自审**：评审由 `hf-review` 派发独立 subagent `hf-reviewer`（agent 定义见 `agents/hf-reviewer.md`）执行。
- **评审者不动手修**：评审产出 findings 与 verdict，修改由作者执行。
- **实现默认隔离**：`hf-tdd` 在 runtime 支持时**逐任务**派发全新上下文的 implementer subagent `hf-implementer`（agent 定义见 `agents/hf-implementer.md`），输入为打包的 **Context Pack** 而非聊天历史，防止长会话上下文漂移。hf-implementer 只承接单个自包含任务，完成后交还证据行，不持有跨任务状态。
- **人做最终把关**：规格确认、设计确认、评审 verdict 闭环、DoD 核验后的关闭都需要人。
- HarnessFlow 不替团队角色拍板业务方向、优先级、验收阈值、架构边界。

## 6. 平台适配

HarnessFlow 设计为跨运行时分发：`commands/` 提供 slash-style 阶段入口（thin pointer，不复制技能内容）；平台接入文档（Claude Code、Cursor、OpenCode）描述如何让各运行时的技能发现机制指向 `skills/`。平台适配不改变三层质量模型与工作流。

项目级覆盖：组件仓库根目录的 `AGENTS.md` `## Project overrides` 可覆盖工件路径与模板；不创建时使用 `using-hf` 内置默认值。路径覆盖只改变组件根内的相对工件位置，不应把工件写到 HarnessFlow 技能仓库或上级工作区根。

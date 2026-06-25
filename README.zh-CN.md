# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**三层质量模型（SDD→TDD→Clean Code）+ human-on-the-loop 的 AI 编码 agent 开发流程技能套件。**

HarnessFlow 把严谨的 AI 辅助工程纪律打包成自包含 Markdown skills：规格、设计、测试先行实现、独立评审、缺陷修复与收尾。它把「产出高质量代码」拆成由外到内的三层——SDD（做对的事）→ TDD（证明做对）→ Clean Code（写得好）——并要求 AI 在环内干活、人站在环上审查。理念见 [`docs/harnessflow-philosophy.md`](docs/harnessflow-philosophy.md)，架构见 [`docs/harnessflow-core-architecture.md`](docs/harnessflow-core-architecture.md)。

![HarnessFlow 三层质量模型](docs/assets/harnessflow-tdd-overview.png)

---

## 命令

HarnessFlow 提供 7 个 slash commands 作为薄平台适配。权威工作流在 `skills/<name>/SKILL.md`；命令只表达意图并加载对应技能。

| 你要做什么 | 命令 | Skill | 核心原则 |
|------------|------|-------|----------|
| 进入或恢复 HF | `/hf` | `using-hf` | 从工件恢复进度 |
| 定义要做什么 | `/spec` | `hf-specify` | 先规格，后代码 |
| 规划怎么做 | `/plan` | `hf-design` | 先设计，后实现 |
| 测试先行构建 | `/build` | `hf-tdd` | RED → GREEN → REFACTOR |
| 评审一个工件 | `/review` | `hf-review` | 作者不自审 |
| 收尾工程工作 | `/ship` | `hf-ship` | DoD 通过再 closeout |
| 修复缺陷 | `/fix` | `hf-fix` | 先复现，再修复 |

`hf-clean-code`、语言标准与领域标准没有独立命令——它们是贯穿设计、实现、评审的质量 overlay。

> **命令是 bias，不是 bypass。** 除 `/fix` 直接走缺陷旁路外，命令仍会先检查仓库工件证据（`plan.md`、`reviews/`），再进入正确阶段。

---

## 快速开始

### Claude Code

通过 marketplace 安装：

```text
/plugin marketplace add https://github.com/hujianbest/harness-flow.git
/plugin install harness-flow@hujianbest-harness-flow
```

### OpenCode 和 Cursor

用安装脚本把 HarnessFlow vendoring 到你的项目（保留 manifest，可干净卸载）：

```bash
git clone https://github.com/hujianbest/harness-flow.git /path/to/harness-flow

# OpenCode
bash /path/to/harness-flow/install.sh --target opencode --host /path/to/your/project

# Cursor
bash /path/to/harness-flow/install.sh --target cursor --host /path/to/your/project

# Both
bash /path/to/harness-flow/install.sh --target both --host /path/to/your/project
```

脚本会复制或软链接 `skills/`、`agents/`、OpenCode command assets 和 Cursor agent mirrors，放置客户端规则，并写入 `.harnessflow-install-manifest.json`，让 uninstall 只移除 HF 管理的文件。

### 试一下

```text
Use HarnessFlow from this repo. Start with `using-hf` and route me to the right stage.
I want to add a retry mechanism to the notifications component.
Clarify the requirements first; do not jump straight to code.
```

项目级覆盖：在目标组件仓库根目录创建 `AGENTS.md` 的 `## Project overrides` 段，可覆盖工件路径与模板；不创建时使用 `using-hf` 内置默认值。

更多安装细节：[Claude Code setup](docs/claude-code-setup.md)、[OpenCode setup](docs/opencode-setup.md)、[Cursor setup](docs/cursor-setup.md)。

---

## 看它如何工作

```text
You:    Use HarnessFlow from this repo. Add rate limiting to the notifications API.
        Do not jump straight to code.

HF:     从 `using-hf` 进入，确认运行模式（attended / unattended），解析目标组件根，
        因为没有已批准规格而路由到 `hf-specify`。

You:    规格准备好了，继续。

HF:     先跑一次独立 `hf-review`（R1 门禁）。规格通过且运行模式允许推进时，
        `hf-design` 写组件级 + 工作项级设计、接口契约、错误模型与测试设计。

You:    按批准的设计构建。

HF:     `hf-tdd` 精化 `plan.md`，逐任务实现，留 RED → GREEN → REFACTOR 证据行，
        应用 `hf-clean-code` 与适用的语言/领域标准，证据落盘。

You:    验证并收尾。

HF:     `hf-review` 用独立上下文检查测试与代码（R3 门禁）。`hf-ship` 跑 Definition of
        Done，把长期资产 promotion 到组件根下 docs/，并写 `closeout.md` 供人最终确认。
```

工作流启动时 HarnessFlow 会记录一个运行模式：默认 `attended`（评审 verdict 通过后停下呈人确认）；`unattended` 在长会话里连续推进，但独立评审、记录、critical 阻塞、后续人工审计一项不少——**unattended 只移除人工停顿，不移除任何质量动作**。

---

## 全部 15 个 Skills

HarnessFlow 当前发布 15 个技能，分四类。overlay 与领域技能靠命名约定与 description 触发，新增 overlay 不必改动阶段技能。

### 阶段技能（7）

有工作流、有产物、有人审把关点。`using-hf` 是入口技能；其余六个是工作流阶段。

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [using-hf](skills/using-hf/SKILL.md) | 入口：三层模型、工作流闭环、工件约定、恢复规则、行为准则 | 开始、恢复或询问 HF 下一步该做什么 |
| [hf-specify](skills/hf-specify/SKILL.md) | 把意图转成可测试规格（EARS + Given/When/Then + NFR QAS）并初始化追溯矩阵 | 一个功能/变更需要先有需求再做设计或代码 |
| [hf-design](skills/hf-design/SKILL.md) | 产出组件级 + 工作项级设计、边界、契约、错误模型、取舍与测试设计 | 已批准规格需要技术设计 |
| [hf-tdd](skills/hf-tdd/SKILL.md) | 测试先行实现（RED → GREEN → REFACTOR）、任务证据、断言质量、mock 边界纪律 | 设计已批准、实现开始 |
| [hf-review](skills/hf-review/SKILL.md) | 用独立上下文评审规格/设计/测试/代码，产出 findings 与 verdict | 一个阶段工件准备好过门禁 |
| [hf-ship](skills/hf-ship/SKILL.md) | 核验 Definition of Done、promotion 长期资产、写 closeout | 评审已闭环、工程工作准备收尾 |
| [hf-fix](skills/hf-fix/SKILL.md) | 缺陷路径：复现 → 根因 → 最小修复边界 → TDD 修复 | 出现回归、bug、hotfix 或已发布行为缺陷 |

### Overlay 技能（5）

贯穿各阶段的质量约束与判据，被阶段技能引用，自身不是阶段。`hf-clean-code` 是第三层通用内核；语言标准按 `<language>-coding-standards` 命名约定发现。

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [hf-clean-code](skills/hf-clean-code/SKILL.md) | 语言无关的整洁代码标准：命名、函数、控制流、错误、注释、重构目录 | 写、重构或评审实现与测试代码 |
| [c-coding-standards](skills/c-coding-standards/SKILL.md) | C 语言级规则、惯用法、工具纪律与示例 | 工作触碰 C 源码、测试或构建脚本 |
| [cpp-coding-standards](skills/cpp-coding-standards/SKILL.md) | C++ 语言级规则、惯用法、工具纪律与示例 | 工作触碰 C++ 源码、测试或构建脚本 |
| [java-coding-standards](skills/java-coding-standards/SKILL.md) | Java 语言级规则、惯用法、工具纪律与示例 | 工作触碰 Java 源码、测试或构建脚本 |
| [python-coding-standards](skills/python-coding-standards/SKILL.md) | Python 语言级规则、惯用法、工具纪律与示例 | 工作触碰 Python 源码、测试或构建脚本 |

### 领域技能（2）

领域特化的质量维度，按 frontmatter description 触发。

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [backend-development](skills/backend-development/SKILL.md) | 后端领域设计约束、实现红线与证据要求 | 工作语境匹配后端领域技能的 description |
| [frontend-development](skills/frontend-development/SKILL.md) | 前端领域设计约束、实现红线与证据要求 | 工作语境匹配前端领域技能的 description |

### 工具技能（1）

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [coding-standards-creator](skills/coding-standards-creator/SKILL.md) | 把团队内部编码规范转化为新的 `<language>-coding-standards` 技能 | 团队需要新增或修订一门语言标准 |

语言标准靠约定扩展：触碰语言 X 的工作可加载 `<x>-coding-standards`（若存在）。新增语言技能遵循共享的[结构契约](skills/coding-standards-creator/references/coding-standards-skill-contract.md)，因此阶段技能无需为每门语言改写。

---

## The HarnessFlow Method（三层质量模型 + 工作流）

HarnessFlow 不是 prompt 集合，而是一套让 AI agent 产出可审查、可信任、可维护代码的证据驱动工作流。三层由外到内递进：先保证做对的事，再证明做对，最后写好。

| 层 | HF 方法 | 为什么重要 |
|----|---------|------------|
| 意图（第一层 SDD） | 规格驱动开发（`hf-specify`） | 防止 agent 靠猜需求 |
| 规划 | 组件级 + 工作项级设计（`hf-design`） | 在写代码前让边界、契约、错误模型、测试设计显式化 |
| 执行（第二层 TDD） | 测试驱动开发（`hf-tdd`） | 把「看起来对」与「被测试证明对」分开 |
| 内在质量（第三层 Clean Code） | Clean Code overlay（`hf-clean-code` + 语言/领域标准） | 让代码可读、简洁、可维护、可审查 |
| 评审 | 独立门禁（`hf-review`） | 把作者身份与判断分开 |
| 恢复 | artifact-first 状态（`plan.md` + `reviews/`） | 让另一个 agent 或人能从文件而非聊天记忆续作 |
| 收尾 | DoD + promotion（`hf-ship`） | 记录改了什么、通过了什么、哪些文档成为长期资产 |

HarnessFlow 的协作姿态是 **human-on-the-loop**：AI 干活，人审查关键工件与决策。理念与架构见 [`docs/harnessflow-philosophy.md`](docs/harnessflow-philosophy.md) 与 [`docs/harnessflow-core-architecture.md`](docs/harnessflow-core-architecture.md)。

---

## Skills 如何工作

每个技能都是自包含的操作规程：

```text
SKILL.md
├── 触发条件
├── 工作流步骤
├── 必需工件
├── 证据与评审契约
├── 质量规则与示例
├── 红旗与合理化陷阱
└── 自检清单
```

关键设计选择：

- **流程最小化。** 只保留产生质量的部分：阶段产物、人审把关点、TDD 纪律、独立评审；不维护额外节点路由器。
- **内容最大化。** 每个技能的主体是工程判断：规则 + 正反例 + 自检清单 + 评审 rubric。
- **证据优于记忆。** 进度从 `plan.md`、`reviews/`、`traceability.md` 与工件本身恢复，不依赖聊天历史。
- **作者不自审。** 创建工件的 agent 不批准自己的工件。

---

## Project Structure

```text
harness-flow/
├── skills/                         # 15 skills (7 phase + 5 overlay + 2 domain + 1 tool)
│   ├── using-hf/                   # 阶段：入口与恢复规则
│   ├── hf-specify/                 # 阶段：可测试规格与追溯
│   ├── hf-design/                  # 阶段：组件级 + 工作项级设计
│   ├── hf-tdd/                     # 阶段：测试先行实现
│   ├── hf-review/                  # 阶段：独立评审门禁
│   ├── hf-ship/                    # 阶段：DoD、promotion、closeout
│   ├── hf-fix/                     # 阶段：缺陷路径
│   ├── hf-clean-code/              # overlay：语言无关整洁代码
│   ├── c-coding-standards/         # overlay：C 语言标准
│   ├── cpp-coding-standards/       # overlay：C++ 语言标准
│   ├── java-coding-standards/      # overlay：Java 语言标准
│   ├── python-coding-standards/    # overlay：Python 语言标准
│   ├── backend-development/        # 领域：后端
│   ├── frontend-development/       # 领域：前端
│   └── coding-standards-creator/   # 工具：语言标准生成器
├── commands/                       # 7 个 slash-style 阶段入口
├── agents/                         # hf-implementer 与 hf-reviewer 角色
├── .claude-plugin/                 # Claude Code marketplace plugin 元数据
├── .cursor/rules/                  # Cursor alwaysApply 入口规则
├── .opencode/                      # OpenCode 集成 assets
├── docs/
│   ├── harnessflow-philosophy.md   # 核心理念（北极星）
│   ├── harnessflow-core-architecture.md
│   ├── claude-code-setup.md
│   ├── opencode-setup.md
│   ├── cursor-setup.md
│   ├── decisions/                  # ADR
│   └── assets/
├── scripts/                        # 仓库一致性检查
├── tests/                          # 仓库级校验与回归
├── install.sh / uninstall.sh
├── install.ps1 / uninstall.ps1
└── README.md
```

把 HarnessFlow vendor 到另一个项目时，复制 `skills/` 与 `agents/`，或用 `install.sh`。每个技能自己拥有 `SKILL.md`、`references/`、`evals/` 与可选 `scripts/`；共享 subagent roles 放 `agents/`，slash-command definitions 放 `commands/`。

---

## 适用范围

HarnessFlow 覆盖**从已接受的需求到评审过的实现与收尾**这一工程段。它**不**覆盖产品发现、发布运维（部署、staged rollout、监控、回滚）、系统集成/验收测试、事件管理或生产发布；也不替团队拍板业务方向、优先级、验收阈值或架构边界。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。技能应当具体、可验证、示例驱动，少流程样板。

---

## License

MIT — 可在你的项目、团队与工具中使用 HarnessFlow。

# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**面向 AI 编码 Agent 的 spec-anchored SDD、gated TDD 与基于证据的工作流控制。**

HarnessFlow 把严谨 AI 辅助工程中的实践打包成自包含 Markdown skills：产品发现、规格、设计、任务、TDD 实现、独立评审、门禁与 closeout。

![HarnessFlow TDD overview](docs/assets/harnessflow-tdd-overview.png)

---

## 命令

Claude Code 提供 7 个 slash commands。OpenCode 和 Cursor 通过自然语言 + `using-hf-workflow` 触达同样意图。

| 你要做什么 | 命令 | 核心原则 |
|------------|------|----------|
| 进入或恢复 HF | `/hf` | 从工件路由 |
| 定义要做什么 | `/spec` | 先 spec 再代码 |
| 规划怎么做 | `/plan` | 先设计再任务 |
| 构建一个任务 | `/build` | 单一活跃任务 |
| 推进前评审 | `/review` | 作者/评审者分离 |
| 关闭工程工作 | `/ship` | gate 通过再 closeout |
| 产出 release pack | `/release` | 版本文档，不部署 |

每个命令都是 bias，不是 bypass。除 `/release` 会 direct invoke 独立 release skill 外，router 仍会先检查仓库工件证据，再选择下一节点。

---

## 快速开始

### Claude Code

通过 marketplace 安装：

```text
/plugin marketplace add https://github.com/hujianbest/harness-flow.git
/plugin install harness-flow@hujianbest-harness-flow
```

### OpenCode 和 Cursor

用安装脚本把 HarnessFlow vendoring 到你的项目：

```bash
git clone https://github.com/hujianbest/harness-flow.git /path/to/harness-flow

# OpenCode
bash /path/to/harness-flow/install.sh --target opencode --host /path/to/your/project

# Cursor
bash /path/to/harness-flow/install.sh --target cursor --host /path/to/your/project

# Both
bash /path/to/harness-flow/install.sh --target both --host /path/to/your/project
```

脚本会复制或软链接 `skills/`、`agents/` 和 OpenCode command assets，放置客户端规则，并写入 `.harnessflow-install-manifest.json`，让 uninstall 只移除 HF 管理的文件。

### 试一下

```text
Use HarnessFlow from this repo. Start with `using-hf-workflow` and route me through the correct HF workflow.
I want to add rate limiting to our notifications API.
Do not jump straight to code.
```

更多安装细节：

- [Claude Code setup](docs/claude-code-setup.md)
- [OpenCode setup](docs/opencode-setup.md)
- [Cursor setup](docs/cursor-setup.md)

---

## 看它如何工作

```text
You:    Use HarnessFlow from this repo. Start with `using-hf-workflow`.
        I want to add rate limiting to our notifications API.

HF:     读取仓库工件，选择正确入口，并路由到 discovery 或 `hf-specify`，
        而不是直接跳到代码。

You:    Use HarnessFlow to plan the approved spec.

HF:     用 `hf-design` 产出架构；只有当 spec 声明 UI surface 时才加入
        `hf-ui-design`；随后用 `hf-tasks` 把设计拆成可评审任务。

You:    Use HarnessFlow to build the current active task.

HF:     锁定一个 `Current Active Task`，写测试设计，记录 approval，
        执行 RED -> GREEN -> REFACTOR，更新 `tasks.progress.json`，
        并写入 wisdom-notebook delta 供跨任务复用。

You:    Use HarnessFlow to verify and close this work.

HF:     运行 test、code、traceability reviews。如果任务触碰前端表面，
        `hf-browser-testing` 会采集 DOM / console / network 证据，再交给
        gates 判断下一步。

You:    Use HarnessFlow to ship the completed workflow.

HF:     运行 regression、doc-freshness、completion gates，然后 `hf-finalize`
        写 `closeout.md` 和 closeout HTML companion。若要切 vX.Y.Z release，
        `hf-release` 可把已关闭 workflows 汇总成 tag-ready release pack；
        它仍然不部署到生产。
```

如果架构师显式要求 auto mode，`hf-ultrawork` 可以沿 canonical next actions 自动继续、写 approval records、保留 fast-lane audit trail，同时仍保留 Fagan reviews、gate verdicts、closeout 与 hard stops。

---

## 全部 30 个 Skills

HarnessFlow 当前包含 29 个 `hf-*` skills，加上 `using-hf-workflow` 入口 skill。

### Meta 与路由

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [using-hf-workflow](skills/using-hf-workflow/SKILL.md) | Public entry shell，用来判断 direct invoke 还是交给 router | 开始会话或表达高层 HF 意图 |
| [hf-workflow-router](skills/hf-workflow-router/SKILL.md) | 基于证据的 runtime router 和恢复控制器 | 从仓库工件继续，或消费 review/gate 结果 |

### 发现与定义

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [hf-product-discovery](skills/hf-product-discovery/SKILL.md) | 梳理产品机会、假设、JTBD 和成功信号 | 想法还在产品发现阶段 |
| [hf-discovery-review](skills/hf-discovery-review/SKILL.md) | 用作者/评审者分离方式评审 discovery 工件 | discovery 输出需要独立 verdict |
| [hf-experiment](skills/hf-experiment/SKILL.md) | 对 blocking hypotheses 跑最小可用 probe | discovery 或 spec 假设风险太高，不能靠猜 |
| [hf-specify](skills/hf-specify/SKILL.md) | 把意图转成可测试需求和验收标准 | 写或修订 spec |
| [hf-spec-review](skills/hf-spec-review/SKILL.md) | 从清晰度、完整性、可测试性评审 spec | spec 准备好独立评审 |

### 规划

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [hf-design](skills/hf-design/SKILL.md) | 产出架构、接口、风险和决策 | 已批准 spec 需要技术设计 |
| [hf-design-review](skills/hf-design-review/SKILL.md) | 评审设计的可追溯性和架构质量 | design draft 准备好 |
| [hf-ui-design](skills/hf-ui-design/SKILL.md) | 设计 UI flows、IA、states、tokens 和 a11y | spec 声明 UI surface |
| [hf-ui-review](skills/hf-ui-review/SKILL.md) | 按 UX 和 a11y 标准评审 UI design | UI design 需要独立 verdict |
| [hf-tasks](skills/hf-tasks/SKILL.md) | 把批准的设计拆成小而有序的任务 | design 已批准，需要任务计划 |
| [hf-tasks-review](skills/hf-tasks-review/SKILL.md) | 检查任务原子性、依赖和验证清晰度 | task plan 准备好 |
| [hf-gap-analyzer](skills/hf-gap-analyzer/SKILL.md) | formal review 前的作者侧 gap check | 工件提交评审前需要自检 |

### 构建、验证与评审

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [hf-test-driven-dev](skills/hf-test-driven-dev/SKILL.md) | 用测试设计、RED/GREEN 证据和 refactor 纪律实现一个活跃任务 | 单一当前任务已锁定 |
| [hf-subagent-driven-dev](skills/hf-subagent-driven-dev/SKILL.md) | 通过 fresh implementer subagent 实现一个活跃任务，同时保留 HF reviews 和 gates | 已锁定任务足够自包含，适合 subagent 执行 |
| [hf-browser-testing](skills/hf-browser-testing/SKILL.md) | 采集浏览器 DOM、console、network 运行时证据 | 前端任务需要 runtime proof |
| [hf-test-review](skills/hf-test-review/SKILL.md) | 评审测试质量和 fail-first 证据 | tests 准备好独立评审 |
| [hf-code-review](skills/hf-code-review/SKILL.md) | 评审实现质量、design conformance 和 AI-slop 风险 | code 准备好独立评审 |
| [hf-traceability-review](skills/hf-traceability-review/SKILL.md) | 检查 spec -> design -> tasks -> code -> verification 对齐 | 实现评审已通过 |
| [hf-regression-gate](skills/hf-regression-gate/SKILL.md) | 做 impact-based regression 判断 | traceability 已批准 |
| [hf-doc-freshness-gate](skills/hf-doc-freshness-gate/SKILL.md) | 检查行为变化与文档保持同步 | regression evidence 准备好 |
| [hf-completion-gate](skills/hf-completion-gate/SKILL.md) | 判断 task/workflow 证据是否足够完成 | reviews 和 gates 需要最终 completion verdict |

### Closeout、release、支线与加速

| Skill | 做什么 | 什么时候用 |
|-------|--------|------------|
| [hf-finalize](skills/hf-finalize/SKILL.md) | 写 closeout pack 和 HTML companion | completion gate 允许 workflow closeout |
| [hf-release](skills/hf-release/SKILL.md) | 把已关闭 workflows 汇总成 tag-ready release pack | 切 vX.Y.Z release |
| [hf-hotfix](skills/hf-hotfix/SKILL.md) | 用 root-cause discipline 处理缺陷恢复 | 请求是生产或已发布行为缺陷 |
| [hf-increment](skills/hf-increment/SKILL.md) | 为 scope 或 acceptance 变化重新进入 workflow | 既有工件之后需求发生变化 |
| [hf-wisdom-notebook](skills/hf-wisdom-notebook/SKILL.md) | 维护跨任务 learnings、decisions、issues、verification、problems | 工作需要跨任务复用记忆 |
| [hf-context-mesh](skills/hf-context-mesh/SKILL.md) | 生成客户端特定的 context skeletons | 项目需要分层 agent instructions |
| [hf-ultrawork](skills/hf-ultrawork/SKILL.md) | explicit-opt-in fast lane，同时保留 reviews、gates 和 approval records | 架构师要求按 HF 规则自动执行 |

---

## The HF Method

HarnessFlow 不是 prompt 集合，而是一套面向 agent 的受控工程工作流。

| 层 | HF 方法 | 为什么重要 |
|----|---------|------------|
| Intent | Spec-anchored SDD | 把范围、约束和验收标准留在可评审文件里 |
| Planning | Design and task gates | 把批准的意图转成架构和原子实现单元 |
| Execution | Gated TDD | 要求测试设计、RED/GREEN 证据和一次一个活跃任务 |
| Routing | Artifact-based recovery | 让 agent 从仓库状态恢复，而不是依赖聊天记忆 |
| Review | Fagan-style separation | 防止 authoring、implementation、judgment 混成一步 |
| Verification | Regression and completion gates | 把“测试跑过”和“证据足够”分开 |
| Closeout | Formal handoff | 记录改了什么、通过了什么、还剩什么 |

HF 刻意停在 engineering closeout。它可以产出 release-ready pack，但不部署、不做 staged rollout、不监控生产，也不声称 post-launch 成功。

---

## Skills 如何工作

每个 skill 都是自包含 workflow：

```text
SKILL.md
├── Overview and trigger conditions
├── Step-by-step workflow
├── Required artifacts and evidence
├── Review or gate contract
├── Red flags
├── Common rationalizations
└── Verification checklist
```

关键设计选择：

- **Process, not prose.** Skills 是 agent 执行的操作规程。
- **Evidence over memory.** 路由读取 `progress.md`、reviews、approvals、verification records 等文件。
- **Author/reviewer separation.** 工件作者不批准自己的工件。
- **Progressive disclosure.** references、rubrics、scripts、evals 都放在所属 skill 旁边，按需加载。

---

## Project Structure

```text
harness-flow/
├── skills/                            # 30 skills (29 hf-* + 1 entry skill)
│   ├── using-hf-workflow/             # Meta: choose entry point
│   ├── hf-workflow-router/            # Meta: route from artifacts
│   ├── hf-product-discovery/          # Discover: frame product opportunity
│   ├── hf-discovery-review/           # Discover: review discovery output
│   ├── hf-experiment/                 # Discover: probe blocking hypotheses
│   ├── hf-specify/                    # Define: write or revise specs
│   ├── hf-spec-review/                # Define: review specs
│   ├── hf-design/                     # Plan: architecture and decisions
│   ├── hf-design-review/              # Plan: review architecture
│   ├── hf-ui-design/                  # Plan: UI surface design
│   ├── hf-ui-review/                  # Plan: review UI design
│   ├── hf-tasks/                      # Plan: break work into tasks
│   ├── hf-tasks-review/               # Plan: review task plan
│   ├── hf-gap-analyzer/               # Plan: author-side gap check
│   ├── hf-test-driven-dev/            # Build: one task with TDD
│   ├── hf-subagent-driven-dev/        # Build: fresh implementer subagent
│   ├── hf-browser-testing/            # Verify: browser runtime evidence
│   ├── hf-test-review/                # Review: test quality
│   ├── hf-code-review/                # Review: implementation quality
│   ├── hf-traceability-review/        # Review: end-to-end traceability
│   ├── hf-regression-gate/            # Gate: regression evidence
│   ├── hf-doc-freshness-gate/         # Gate: docs stay current
│   ├── hf-completion-gate/            # Gate: completion decision
│   ├── hf-finalize/                   # Closeout: handoff pack
│   ├── hf-release/                    # Release: tag-ready release pack
│   ├── hf-hotfix/                     # Branch: defect recovery
│   ├── hf-increment/                  # Branch: scope change
│   ├── hf-wisdom-notebook/            # Knowledge: cross-task memory
│   ├── hf-context-mesh/               # Context: client rule skeletons
│   └── hf-ultrawork/                  # Fast lane: explicit auto mode
├── commands/                       # 7 client-agnostic slash command definitions
├── agents/                         # HF subagent role definitions
├── .claude-plugin/                 # Claude Code marketplace plugin metadata
├── .cursor/rules/                  # Cursor alwaysApply entry rule
├── .opencode/                      # OpenCode integration assets
├── docs/
│   ├── claude-code-setup.md
│   ├── opencode-setup.md
│   ├── cursor-setup.md
│   ├── decisions/                  # ADRs
│   ├── principles/                 # HF design notes
│   └── assets/
├── examples/writeonce/             # end-to-end demo artifacts
├── features/                       # HarnessFlow dogfood feature artifacts
├── tests/                          # Repository-level validators and regressions
├── scripts/                        # Repository maintenance scripts
├── install.sh / uninstall.sh
├── install.ps1 / uninstall.ps1
└── README.zh-CN.md
```

把 HarnessFlow vendor 到另一个项目时，需要复制 `skills/` 和 `agents/`，或直接使用 `install.sh`。每个 skill 自己拥有 `SKILL.md`、`references/`、`evals/` 和可选 `scripts/`；共享 subagent roles 放在 `agents/`，客户端 slash-command definitions 放在 `commands/`。`docs/principles/` 解释本仓库的设计，但宿主项目运行时不依赖它。

---

## Why HarnessFlow?

AI 编码 agent 很容易从需求直接跳到实现。HarnessFlow 给它们一条更窄、更硬的路径：先澄清意图，先设计再切任务，用 TDD 证明行为，把评审从作者身份中分离，并用持久工件完成闭环。

这套 pack 适合正确性、可恢复性和可审计性很重要的仓库。它让路由基于文件而不是聊天记忆，让一个活跃任务保持受控，并记录足够证据，让另一个 agent 或 human reviewer 可以不靠猜测继续工作。

HarnessFlow 也明确划定 shipping 边界。它支持 engineering closeout 和 tag-ready release packs；部署、staged rollout、监控、回滚和 post-launch operations 仍由项目自己的生产系统承担。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。Skills 应当具体、可验证、最小化，并扎根真实工程实践。

---

## License

MIT - 可在你的项目、团队和工具中使用 HarnessFlow。

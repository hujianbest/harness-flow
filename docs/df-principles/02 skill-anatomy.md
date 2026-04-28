# dev-flow (df) Skill Anatomy

- 定位: 定义 `dev-flow`（简称 `df`）中 `df-*` skill 的目标态写法；对 workflow skill 来说，它是 `01 skill-node-define.md` 在 `SKILL.md` 层的落地 anatomy。
- 关联:
  - 最高原则: `docs/df-principles/00 soul.md`
  - Skill-node 设计契约: `docs/df-principles/01 skill-node-define.md`
  - 工件管理约定: `docs/df-principles/03 artifact-layout.md`
  - Workflow 架构: `docs/df-principles/04 workflow-architecture.md`

## 定位

本文定义 df skills 的写作标准，让 `df-*` skills 能被 opencode agent 稳定触发、正确执行、留下证据，并能在团队日常开发链路中被恢复编排。

df skill 不是一次性提示词，也不是团队流程制度的散文复述。它是一个运行时 contract：告诉 agent 何时加载、处理什么对象、采用什么方法、按什么 todo list 做、产出什么记录、何时必须停止。

## 核心原则

1. **Skill 是团队工程纪律的可执行化。** 团队已有模板、流程、代码规范和验证要求不能只停留在制度里，必须被 skill 转成可执行步骤和证据要求。
2. **df 不替团队角色拍板。** 模块架构师、开发负责人和开发人员的判断权不能被 skill 偷偷接管。
3. **Description 是分类器，不是流程摘要。** 它只回答“当前请求是否应该加载这个 skill”。
4. **对象优先。** 每个 workflow skill 必须声明 primary object、frontend input object、backend output object。
5. **方法必须落地。** Clean Architecture 边界纪律、SOLID / GRASP、C / C++ 防御式设计、TDD、TDD 后测试有效性审查、代码检视、静态分析和团队编码规范等方法必须落到 workflow / hard gate / verification。
6. **证据优先于口头结论。** 设计、测试、测试有效性审查、检视和完成判断都必须可回读。
7. **主文件短而硬。** `SKILL.md` 保留触发、边界、workflow、hard gates、output 和 verification；长模板、rubric、案例放 `references/`。
8. **路径可迁移。** 项目工件路径优先读项目约定；skill pack 共享资料使用相对稳定路径，不写死安装目录。

## Skill Types

| 类型 | 是什么 | 典型内容 |
|---|---|---|
| `Technique` | 具体做法 | TDD、重构纪律、TDD 后测试有效性审查、代码检视、静态分析审查 |
| `Pattern` | 判断模型 | Clean Architecture 边界、SOLID / GRASP、SOA 边界、嵌入式风险识别 |
| `Reference` | 查阅材料 | 团队模板、编码规范、MISRA / CERT 子集、rubric、协议、检查表 |

df workflow skill 通常是 `Technique + Pattern`。当节点依赖团队模板、测试有效性 rubric、代码检视 rubric 时，再引入 `Reference`。

## df Node Roles

| 角色 | 代表 skill | 写作重心 |
|---|---|---|
| Public Entry | `using-df-workflow` | 判断 direct invoke 还是 route-first |
| Router | `df-workflow-router` | 恢复当前 AR / 问题修改状态，决定下一节点 |
| Specify | `df-specify` | 澄清明确输入、IR/SR/AR 追溯、待决问题 |
| Spec Review | `df-spec-review` | 规格清晰性、可追溯性、可设计性审查 |
| Component Design | `df-component-design` | 组件实现设计、SOA 边界、组件接口和依赖 |
| AR Design | `df-ar-design` | AR 代码层设计、测试设计、与组件设计一致性 |
| Implementation | `df-tdd-implementation` | 基于 AR 测试设计做 C / C++ TDD |
| Test Checker | `df-test-checker` | TDD 后测试用例有效性、覆盖性、可维护性审查 |
| Code Review | `df-code-review` | C / C++ 质量、SOA 边界、嵌入式风险 |
| Gate | `df-completion-gate` | evidence bundle 与完成判断 |
| Finalize | `df-finalize` | 状态收口、交接、长期记录同步 |

## Directory Anatomy

```text
skills/
  df-skill-name/
    SKILL.md
    references/
      template-or-rubric.md
    evals/
      README.md
      evals.json
      fixtures/
        ...
    scripts/
      optional-tool.py
```

规则：

- `SKILL.md` 是唯一必需文件。
- `references/` 放深度模板、rubric、长示例，不放核心进入条件和 workflow。
- `evals/` 用来保护高风险行为 contract。
- `scripts/` 只放真正可执行、可复用的辅助工具，例如日志解析、静态检查结果归一化、验证记录生成。

## Frontmatter

```yaml
---
name: df-skill-name
description: Use when ...
---
```

要求：

- `name` 与目录名一致，使用 `df-*` 前缀。
- `description` 只写触发条件和反向边界。
- `description` 不写完整 workflow，不写“先读什么再做什么”的流程摘要。
- 对 opencode 使用场景，description 要前置关键触发词，例如 `spec review`、`AR implementation design`、`component design`、`test checker`、`C/C++ code review`。

示例：

```yaml
# BAD: 摘要流程
description: Use when implementing AR - read design, write code, run tests, review, deploy.

# GOOD: 分类器
description: Use when coding an approved AR implementation design in C/C++ with existing test design. Not for unclear requirements, component design changes, or post-TDD test effectiveness review.
```

## Main File Skeleton

| 章节 | 默认性 | 作用 |
|---|---|---|
| H1 + 开场 | 必需 | 定义唯一职责和非目标 |
| `## When to Use` | 必需 | 触发条件、反向边界 |
| `## Hard Gates` | 建议 | 不可协商的停止条件 |
| `## Object Contract` | workflow skill 必需 | primary / input / output object |
| `## Methodology` | workflow skill 必需 | 本节点采用的方法及落点 |
| `## Workflow` | 必需 | 带 object / method / input / output / stop rule 的 todo list |
| `## Output Contract` | 按需 | 工件、record、evidence、next action |
| `## Red Flags` | 必需 | 运行时 stop sign |
| `## Common Mistakes` | 按需 | 常见错误与修复 |
| `## Verification` | 必需 | 退出条件 |

## 关键章节写法

### H1 下的开场段

只保留 1-2 句，说明：

- 当前 skill 负责什么。
- 它不替代什么。

示例：

```markdown
# df AR Design

This skill turns an approved AR and its component design context into an AR implementation design whose test design is a section of the design. It does not modify component architecture or write production code.
```

### `Object Contract`

至少包含：

- `Primary Object`
- `Frontend Input Object`
- `Backend Output Object`
- `Object Transformation`
- `Object Boundaries`
- `Object Invariants`

示例：

```markdown
## Object Contract

- Primary Object: AR implementation design model.
- Frontend Input Object: approved AR, SR trace link, component implementation design, existing component code context.
- Backend Output Object: AR implementation design document with an embedded test design section.
- Transformation: convert one assigned requirement into code-level design and executable test intent.
- Boundaries: do not revise component implementation design unless explicitly routed to `df-component-design`.
- Invariants: AR ID, owning component, SR trace link, and scope boundaries remain stable.
```

### `Methodology`

必须写清方法如何服务对象转换。

示例：

```markdown
## Methodology

- Requirements Traceability: keep IR/SR/AR/design/code/test links explicit.
- SOA Component Boundary Analysis: ensure the AR design respects component services and dependencies.
- C/C++ Defensive Design: identify memory, lifecycle, concurrency, timing, and error-handling risks.
- Test Design Before Implementation: define test cases in the AR implementation design before `df-tdd-implementation`.
```

### `Workflow`

每一步用一个标题概括动作，正文写清「按什么方法、做什么、何时停下」。参考既有 `hf-*` skill 的 Workflow 写法，散文式而不是字段表。

推荐写法：

```markdown
### 1. 建立证据基线

读最少必要工件（spec / 设计 / 上一节点 record / progress.md / AGENTS.md 路径映射）。把方法落到动作上：例如 Requirements Traceability 要求显式 IR/SR/AR 锚点。证据冲突 → 回 `df-workflow-router`。

### 2. 执行本节点核心工作

按本节点的方法（如 SOA Component Boundary Analysis、Test Design Before Implementation、Embedded TDD、Post-TDD Test Effectiveness Review）做对象转换。说明会写什么、不会写什么、何时必须停下回上游。

### 3. 写工件 / record / evidence

落盘到约定路径（df-shared-conventions / AGENTS.md 覆盖优先），保留 traceability 锚点与新鲜度证据。

### 4. Handoff

同步 `progress.md` canonical 字段，给出唯一 canonical `df-*` 下一步；不能映射唯一节点时回 `df-workflow-router`。
```

约束：

- 每一步必须能解释它如何推动当前对象从输入到输出。
- 方法必须真的出现在步骤正文里，不能只在 `## Methodology` 章节挂个名。
- 复杂分支（precheck blocked、verdict 决策表）可以用表格辅助；不要把每一步都展开为 Object / Input / Output / Stop 四字段表。
- 不要写成「读取、分析、输出」这种不可执行标题。
- 步骤数量服从节点职责，不追求统一为 4 步。

### `Output Contract`

当 skill 写工件、记录、状态或 handoff 时，必须说明：

- 写什么。
- 写到哪里，遵循项目 artifact layout 或团队路径约定。
- 记录哪些 trace links。
- 记录哪些测试、检视或验证证据。
- 下一步 canonical `df-*` skill 是什么。

### `Verification`

只检查退出条件，不写礼貌性 checklist。优先检查：

- primary object 是否完整。
- object transformation 是否完成。
- 方法论 hard rules 是否落实。
- artifact / record / evidence 是否落盘。
- next action 是否唯一。
- 是否存在需要团队角色拍板的待决问题。

## Supporting Files

### `references/`

适合下沉：

- 组件实现设计模板说明。
- AR 实现设计模板说明。
- spec review rubric。
- TDD 后测试有效性检查 rubric。
- C / C++ code review rubric。
- 团队 C / C++ 编码规范。
- 静态分析 / 编译告警处理策略。
- 长案例和反例。

不应下沉：

- 当前节点的触发条件。
- 当前节点的 primary object。
- 核心 workflow。
- hard gates。
- 最小 output / verification 规则。

### `evals/`

高风险 df skill 应至少覆盖：

- 错误节点触发，例如把 AR 设计请求误路由到实现。
- 缺组件设计却直接写 AR 实现设计。
- AR 实现设计没有测试设计却进入 TDD。
- TDD 完成后未经过 `df-test-checker` 却进入代码检视。
- `df-test-checker` 试图补写测试或修改生产代码。
- 代码修改破坏 SOA 边界但 review 未拦截。
- critical 静态分析 / 编译告警 / 编码规范违反项没有解释却进入 completion。

## Common Mistakes

| 错误 | 问题 | 修复 |
|---|---|---|
| skill 写成团队流程说明书 | agent 不知道具体怎么做 | 改成可执行 contract |
| 不写对象契约 | 容易混淆需求、设计、代码和验证证据 | 补 primary / input / output object |
| 组件设计和 AR 设计边界不清 | 开发人员可能越权改组件架构 | 明确 reroute 到 `df-component-design` |
| TDD skill 自己补测试设计 | 跳过 AR 设计职责 | 缺测试设计时回 `df-ar-design` |
| TDD 后不做测试有效性审查 | 测试可能只是跑通但覆盖不足 | 路由到 `df-test-checker` |
| `df-test-checker` 补写测试或改生产代码 | reviewer 角色越权 | 返回 findings，让实现节点回修 |
| code review 只看风格 | 漏掉嵌入式核心风险 | 加内存、并发、实时性、错误处理、SOA 边界 rubric |
| 把能跑当成整洁代码 | 技术债和边界破坏会沉淀到组件 | 加 Clean Architecture、SOLID / GRASP、静态分析和编码规范检查 |

## Canonical Skeleton

```markdown
---
name: df-skill-name
description: Use when <triggering conditions>. Not for <clear exclusions>.
---

# df Skill Title

<1-2 句：这个 skill 负责什么，不替代什么>

## When to Use

## Hard Gates

## Object Contract

## Methodology

## Workflow

### 1. <todo title>

<散文式说明：本步遵循什么方法、读什么、写什么、何时停下；不强制 Object / Input / Output / Stop 字段表>

### 2. <todo title>

...

## Output Contract

## Red Flags

## Common Mistakes

## Verification

## Supporting References
```

## 检查清单

新增或重写 `df-*` skill 时，至少检查：

- `description` 是否是分类器。
- H1 是否写清唯一职责和非目标。
- 是否没有替模块架构师、开发负责人或开发人员拍板。
- 是否写清 primary object、input object、output object。
- 是否区分规格、组件实现设计、AR 实现设计、代码实现、TDD 后测试审查和代码检视。
- 方法论是否落到 workflow、hard gate、rubric 或 verification。
- 是否覆盖 Clean Architecture 边界、SOLID / GRASP、团队编码规范和静态分析风险。
- Workflow 每步是否有 object / method / input / output / stop rule。
- 是否留下可回读 artifact / record / evidence。
- 是否给出唯一 canonical next action。
- 高风险边界是否有 evals。

# Skill Anatomy — Garage Skill 写作原则

- 定位: 项目级原则文档，定义 Garage 所有 skill（包括 HF workflow skills 及未来其他 family）的目标态写法。
- 来源: 由 D020 设计文档提炼，经评审后上收为项目原则。
- 关联:
  - 灵魂文档（最高锚点）: `docs/principles/soul.md`
  - HF family 共享文档: `skills/docs/`
  - Coding pack 设计: `docs/design/D120-garage-coding-pack-design.md`

## 定位

本文定义 Garage skill 的目标态写法。

它不是现状说明，也不是单个 skill 的写作模板大全；它的任务是给出一套稳定、可执行、可搜索、可维护的 anatomy，让不同 skill 既能被单独正确调用，也能在链路中稳定编排。

## 核心原则

1. **Skill 是可复用技术参考，不是一次性解法叙述。**
   写 skill 是为未来的 agent 放路标，不是记录这次会话怎么做成了。
2. **`SKILL.md` 是本地 contract，不是概念长文。**
   共享语义放 family-level `docs/`，长资料放 `references/`。
3. **Description 是分类器，不是摘要。**
   它只负责帮助系统判断“现在要不要加载这个 skill”，不负责复述流程。
4. **Workflow 和 evidence 优先于解释性 prose。**
   会改变运行时行为的内容留在主文件；不会改变行为的长说明下沉。
5. **边界必须显式。**
   每个 skill 都要说明何时使用、何时不用、和相邻 skill 的区别、冲突时回哪里。
6. **主文件要短，且有量化预算。**
   `SKILL.md` 正文建议 < 500 行 / < 5000 tokens。超过此预算的内容应下沉到 `references/`。运行时 compaction 后仅保留前 5000 tokens，多个 skill 共享约 25000 tokens 总预算——每个多余 token 都在和对话历史、系统提示竞争注意力。
7. **路径写法要可迁移。**
   不要把 skill 绑定到某个仓库安装根、某个 pack 名或某个项目私有目录。项目工件路径优先遵循 `AGENTS.md` / 项目权威约定；skill pack 内共享资料用当前 pack 语义或稳定相对路径表达。

## Skill 类型

这是 skill 的通用类型，不是 HF workflow 节点角色：

| 类型 | 是什么 | 典型内容 |
|---|---|---|
| `Technique` | 具体方法 | 步骤、判断点、操作方式 |
| `Pattern` | 思维模型 | 原则、适用边界、识别信号 |
| `Reference` | 查阅材料 | API、模板、协议、语法、映射表 |

HF workflow skill 大多是 `Technique + Pattern` 的混合体；当某个节点依赖 rubric、模板、协议或映射表时，再引入 `Reference` 层。

## HF 节点角色

这是 HF family 内部的 workflow 角色：

| 角色 | 代表 skill | 写作重心 |
|---|---|---|
| Public Entry | `using-hf-workflow` | 入口判断、route-first vs direct invoke |
| Router | `hf-workflow-router` | stage/profile/mode/isolation/handoff 判断 |
| Authoring | `hf-specify` / `hf-design` / `hf-tasks` | 起草、回修、自检、评审 handoff |
| Review | `hf-*-review` | precheck、rubric、findings、verdict |
| Implementation | `hf-test-driven-dev` | 唯一实现入口、TDD、fresh evidence、交接块 |
| Gate | `hf-regression-gate` / `hf-completion-gate` | evidence bundle、门禁结论、唯一下一步 |
| Branch / Re-entry | `hf-hotfix` / `hf-increment` | 分岔分析、同步、re-entry |
| Finalize | `hf-finalize` | closeout、状态闭合、release notes、handoff pack |

## 目录 anatomy

```text
skills/
  hf-skill-name/
    SKILL.md
    references/
      reference-file.md
    evals/
      README.md
      evals.json
      fixtures/
        ...
    scripts/
      helper-script.py
    assets/
      template-file.ext
```

规则：

- `SKILL.md` 是唯一必需文件。
- `references/` 放深度 reference，不放当前节点最核心的进入条件和 workflow。
- `evals/` 是高风险 skill 的常规配置，用来保护行为 contract。
- `scripts/` 和 `assets/` 只有真的需要复用工具或模板时才引入。
- `scripts/` 的使用原则：**可执行而非加载**。脚本是让 agent 调用的工具，不是让 agent 阅读的文档。agent 可以直接执行脚本获取结果，而不需要先读取脚本内容再理解逻辑——这节省 token 并降低误读风险。脚本应自描述（`--help` 输出清楚说明用途和参数），文件名具备语义（`validate-schema.py` 而非 `helper.py`）。

## Frontmatter 与 CSO

### 字段

frontmatter 只保留：

```yaml
---
name: hf-skill-name
description: Use when ...
---
```

要求：

- `name` 与目录名一致。
- `name` 只用字母、数字、连字符，1-64 字符，推荐动名词形式（如 `specifying-features`）或动作式（如 `process-pdfs`）。避免模糊名称（helper、utils、tools）。
- `description` 的主职责是分类，不是摘要。
- `description` 建议使用祈使句（`Use when...`），前置最关键触发场景（截断时优先丢失尾部）。
- `description` + 正文首段合计不超过约 1500 字符预算（Anthropic 平台 description 截断约 1536 字符）。

### Description 是分类器，不是摘要

`description` 只回答一个问题：

> 现在该不该加载这个 skill？

因此它应描述：

- 触发条件
- 典型症状
- 反向边界
- 必要时的 reroute 线索

它不应描述：

- 当前 skill 的完整流程
- 步骤顺序
- 评审链或执行链摘要
- “读哪些文件、做哪些阶段、再进入哪里”的小型 workflow

建议语义使用等价于 `Use when ... / Not for ...` 的写法。HF 可写中文，但语义必须是分类器语义，而不是摘要语义。

```yaml
# ❌ BAD: 摘要了 workflow
description: Use when routing HF workflow - read evidence, decide profile, dispatch reviewer, continue execution

# ✅ GOOD: 只写触发条件和边界
description: Use when route/stage/profile is unclear, review or gate just finished, or evidence conflicts require authoritative routing. Not for new-session family discovery.
```

`what the skill does` 应由 H1 下的开场段承载，不应压进 `description`。

## 主文件骨架

| 章节 | 默认性 | 作用 |
|---|---|---|
| H1 标题 + 1-2 句开场 | 必需 | 定义职责和非目标 |
| `## When to Use` | 必需 | 定义触发条件、反向边界、邻接 skill 边界 |
| `## Hard Gates` | 建议 | 写不可协商的停止条件 |
| `## Workflow` | 必需 | 写步骤、判断点、reroute 点 |
| `## Output Contract` | 按需 | 写落盘工件、状态同步、canonical next action |
| `## Red Flags` | 必需 | 写运行时 stop sign |
| `## Common Mistakes` | 按需 | 写 mistake -> consequence/fix |
| `## 和其他 Skill 的区别` | 按需但强烈建议 | 防止误触发、误分流 |
| `## Reference Guide` / `## Supporting References` | 按需 | 指向深度材料 |
| `## Verification` | 必需 | 退出条件 |

默认不建议扩散的章节：

- `Overview`
- `Standalone Contract`
- `Chain Contract`
- `Inputs / Required Artifacts`
- `Core Authority`
- `Quality Bar`
- `Common Rationalizations`

这些内容应尽量吸收到已有骨架里，而不是再长一层。

## 关键章节怎么写

### H1 下的开场段

只保留 1-2 句，说明：

- 当前 skill 的唯一职责
- 它不替代什么

### `When to Use`

至少覆盖：

- 正向触发条件
- 不适用场景
- direct invoke 线索
- 与相邻 skill 的边界

### `Workflow`

要求：

- 用编号步骤
- 先读最少必要证据
- 决策点明确
- reroute 路径明确
- 复杂 rubric / 模板 / map 优先下沉到 `references/`

### `Output Contract`

当 skill 会写工件、记录、状态或 handoff 时，本节应明确：

- 写什么
- 写到哪里
- 状态怎么同步
- 下一步 skill 怎么写

这里的“写到哪里”不是把 repo-local 路径硬编码回去，而是要区分两类路径：

- **项目工件路径**：如 spec / design / tasks / reviews / verification / release notes，优先遵循 `AGENTS.md` 或项目权威约定；若要给 fallback，只能写成默认路径或示例路径，不能把当前仓库特有目录伪装成通用事实。
- **skill pack 共享资料**：如模板、protocol、map、shared docs，不要写死历史安装前缀、repo-root 私有路径或 pack 私有命名；优先使用当前 skill pack 语义下稳定可解析的路径表达。

一个简单判断标准是：把当前 skill 移到另一个仓库、改 pack 名或改变安装位置后，这个路径引用是否仍然成立；如果不会，说明它被写死了。

### `Red Flags` 与 `Common Mistakes`

两者不是一回事：

- `Red Flags`：运行时 stop sign，偏“看到这个就别继续”
- `Common Mistakes`：作者或调用方最常犯的错误，偏“错误 -> 后果/修复”

如果只需要 stop sign，保留 `Red Flags` 即可；如果需要清楚说明错误和修复方式，再加 `Common Mistakes`。不要两节写成一模一样的内容。

### `和其他 Skill 的区别`

当一个 skill 与邻近节点容易混淆时，应显式写出区别。最常见做法有两种：

1. 直接折叠进 `When to Use`
2. 单独加一节 `和其他 Skill 的区别`

### `Verification`

只检查退出条件，不写礼貌性 checklist。优先检查：

- record 是否落盘
- 状态是否同步
- verdict / next action 是否唯一
- fresh evidence 是否存在

## 和其他 Skill 的区别：最低要求

每个 HF skill 至少要说明最容易混淆的相邻节点。常见邻接关系：

| 当前 skill | 至少要区分谁 |
|---|---|
| `using-hf-workflow` | `hf-workflow-router` |
| `hf-specify` | `hf-design` / `hf-spec-review` |
| `hf-design` | `hf-tasks` / `hf-design-review` |
| `hf-test-driven-dev` | `hf-test-review` / `hf-*-review` / gates |
| `hf-completion-gate` | `hf-finalize` |
| `hf-hotfix` | `hf-test-driven-dev` / `hf-workflow-router` |

如果一个 skill 读完之后，调用方仍分不清“为什么是它，不是旁边那个”，说明 anatomy 还不够清楚。

## Supporting files 的角色

### `references/`

适合下沉：

- rubric
- template
- protocol
- transition map
- 长案例
- framework / language deep guide

不应下沉：

- 当前节点最核心的进入条件
- 核心 workflow 步骤
- 最关键的 output / verification 规则

引用其他 skill、模板或共享 docs 时，也要优先使用随 pack 一起迁移后仍然成立的写法；不要把历史安装目录、repo-local 根路径或某个项目专有目录直接抄进 `references/`。

### `evals/`

推荐结构：

```text
evals/
  README.md
  evals.json
  fixtures/
    ...
```

要求：

- `README.md` 说明要保护的行为 contract
- `evals.json` 说明 prompt、expectations、files
- `fixtures/` 用真实工件片段模拟高风险场景

`evals/` 测的是行为 contract，不是措辞复读。

### `evals/` 评测方法论

最小评测要求：

1. **每个高风险 skill 至少 2-3 个 test case**，覆盖正常路径、边界条件和典型失败模式。
2. **evals.json 结构**：

```json
{
  "evals": [
    {
      "name": "correctly-rejects-missing-spec",
      "prompt": "<模拟用户请求>",
      "expected_behavior": "应拒绝并 reroute 到 hf-specify",
      "assertions": [
        "输出包含 reroute 指令",
        "输出不包含设计内容"
      ],
      "input_files": ["fixtures/minimal-session.json"]
    }
  ]
}
```

3. **Assertion 写法原则**：
   - 好：可编程验证、具体可观察、可计数（"输出包含 3 个发现项"）
   - 差：模糊（"输出质量好"）、脆弱（精确措辞匹配）

4. **对比基线**：对同一 prompt 分别运行 with_skill 和 without_skill，计算 delta。如果 skill 加载前后结果无显著差异，说明 skill 的增量价值不足。

5. **触发评测**（可选但推荐）：编写 `eval_queries.json`，约 20 条查询（8-10 正例 + 8-10 反例），测试系统是否在正确场景触发该 skill。多次运行计算触发率，建议 > 50%。

6. **快照迭代**：每次重大改进前，将当前 evals 快照保存到 `iteration-N/` 目录，用于回退和对比分析。移除 with/without 两端都通过的断言（无区分度）。

## Common Mistakes

| 错误 | 问题 | 修复 |
|---|---|---|
| `description` 写成流程摘要 | 系统可能按摘要行事，不读正文 | 改成纯触发条件 / 边界 |
| skill 写成一次性故事 | 不可复用 | 抽象成规则、模式、步骤 |
| 不写与相邻 skill 的区别 | 容易误触发 | 在 `When to Use` 或专节中补边界 |
| 共享约定在每个 skill 里重复展开 | 主文件臃肿、漂移 | 上收至 family-level `docs/` |
| 核心规则被藏进 `references/` | 主文件失去 runtime contract | 把关键规则搬回主文件 |
| 在 skill 里写死 repo-local 路径 / 安装前缀 | 换仓库、换 pack 名、换项目约定后失效，或与 `AGENTS.md` 冲突 | 项目工件路径先读 `AGENTS.md`；共享资料改用当前 pack 语义或稳定相对路径 |
| 写工件却没有 `Output Contract` | 调用方不知道怎么交接 | 明确记录、状态、next action |
| `Common Mistakes` 与 `Red Flags` 重复 | 浪费 token | 一个写 stop sign，一个写 mistake -> fix |
| 高风险 skill 没有 `evals/` | 容易回归 | 为边界判断和 reviewer 行为补评测 |

## 演化与版本管理

Skill 不是写完封存的静态文档，而是需要像代码一样持续迭代的运行时资产。

### 版本快照机制

当 skill 重大改进（重写 workflow、修改 frontmatter、调整 output contract）时：

1. **改进前保存快照**：`cp -r evals/ evals/iteration-N/`（N 为迭代编号）。
2. **改进后对比**：对同一批 prompt 分别运行旧版和新版，计算 delta。
3. **断言清理**：移除 with/without 两端都通过的断言（无区分度的断言浪费评测资源）。
4. **回归检查**：确保新版本没有破坏之前已通过的用例。

### 质量退化信号

定期检查以下信号，出现时需要修补 skill：

| 信号 | 含义 | 行动 |
|------|------|------|
| 触发率下降 | description 可能被系统忽略 | 优化 description 触发词 |
| 误触发增加 | 触发条件过宽 | 收窄 description、补 `Not for` |
| agent 总跳过正文直接读 references | 主文件失去价值 | 重新分配内容层次 |
| 某条规则被反复忽略 | 措辞或位置不够强 | 加粗、提前、或转为 checklist |
| evals 断言通过率不变 | skill 增量价值不足 | 收窄 skill 范围或删除低价值部分 |

### 迭代原则

- 先在真实任务中观察失败，再针对性修补——不要凭想象预写"防御性规则"。
- 每次修补只改一个维度（触发、结构、内容、验证），改完立刻评测确认效果。
- 沉淀真实项目中的 gotchas 和常见误判，而不是复述模型已知的公开常识。

## Canonical skeleton

```markdown
---
name: hf-skill-name
description: Use when <triggering conditions>. Not for <clear exclusions>.
---

# Skill Title

<1-2 句：这个 skill 负责什么，不替代什么>

## When to Use

## Hard Gates

## Workflow

## Output Contract

## Red Flags

## Common Mistakes

## 和其他 Skill 的区别

## Reference Guide

## Verification
```

说明：

- `Hard Gates`、`Output Contract`、`Common Mistakes`、`和其他 Skill 的区别`、`Reference Guide` 都是按需出现。
- 对薄节点，可以只保留：开场、`When to Use`、`Workflow`、`Red Flags`、`Verification`。
- 标题名可以按节点需要轻微变化，但语义职责不能漂移。

## 检查清单

在新增或重写 `hf-*` skill 时，至少检查：

- `description` 是否是分类器，而不是摘要
- `description` 是否使用祈使句，是否前置关键触发场景
- H1 下的开场是否足够短
- `When to Use` 是否写清触发条件和边界
- 是否明确说明了与相邻 skill 的区别
- `Workflow` 是否先读最少必要证据
- 需要落盘工件时，是否写了 `Output Contract`
- 路径引用是否避免写死 repo-local 安装前缀，且项目工件路径是否 `AGENTS.md` 优先
- 是否区分了 `Red Flags` 与 `Common Mistakes`
- 共享语义是否已上收至 `docs/`
- 长 reference 是否已下沉到 `references/`
- 高风险边界行为是否有 `evals/`
- `SKILL.md` 正文是否 < 500 行 / < 5000 tokens
- `scripts/` 文件名是否具备语义，是否可独立执行
- 是否有版本快照和质量退化信号追踪机制

## 一句话约束

HF 的目标态 skill anatomy，是把 `SKILL.md` 写成一个短而硬的运行时 contract：description 负责分类，正文负责执行，边界必须显式，长材料下沉，退出条件可验证。

> 冲突仲裁：本文件与 `docs/principles/soul.md` 出现冲突时，以 soul 为准。

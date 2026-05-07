# Skill Anatomy — HF Skill 写作原则

- 定位: 项目级原则文档，定义 HF skill 的目标态写法；对 workflow skill 来说，它是 `skill-node-define.md` 在 `SKILL.md` 层的落地 anatomy。
- 来源: 由 D020 设计文档提炼，并基于 `soul.md` 与 `skill-node-define.md` 刷新。
- 关联:
  - 灵魂文档（最高锚点）: `docs/principles/soul.md`
  - Skill-node 设计契约: `docs/principles/skill-node-define.md`
  - HF family 运行时共享约定: `skills/hf-workflow-router/references/workflow-shared-conventions.md`

## 定位

本文定义 HF skill 的目标态写法。

它不是现状说明，也不是单个 skill 的写作模板大全；它的任务是给出一套稳定、可执行、可搜索、可维护的 anatomy，让不同 skill 既能被单独正确调用，也能在链路中稳定编排。

对 HF workflow skill 来说，`skill-node-define.md` 定义“一个 skill 如何成为 workflow node”，本文定义“这个 node contract 应该如何写进 `SKILL.md`、`references/`、`evals/` 与 supporting files”。

> **v0.2.0 合规基线（ADR-002 D10）**：本文中**仅以下两条**从 v0.2.0 起作为 SKILL.md 合规基线，由 `scripts/audit-skill-anatomy.py` 强制：
>
> 1. `## Common Rationalizations` —— **必需段**；
> 2. `## 和其他 Skill 的区别` —— **禁止段**，等价信息必须写在 `When to Use` 中。
>
> 其余段落（`Object Contract` / `Methodology` / `Hard Gates` / `Output Contract` 等）继续保持 ADR-001 D11 的"按需写"性质，不作合规基线。`soul.md` 仍是宪法层不变。

## 核心原则

1. **Skill 是可复用技术参考，不是一次性解法叙述。**
   写 skill 是为未来的 agent 放路标，不是记录这次会话怎么做成了。
2. **Skill 要服从 soul：用户是架构师，HF 是工程团队。**
   skill 可以执行、暴露风险、留下证据；不能替用户定方向、做取舍、改标准或验收自己。
3. **`SKILL.md` 是本地 contract，不是概念长文。**
   共享语义放 family-level `docs/`，长资料放 `references/`。
4. **Description 是分类器，不是摘要。**
   它只负责帮助系统判断“现在要不要加载这个 skill”，不负责复述流程。
5. **对象、方法、workflow 和 evidence 优先于解释性 prose。**
   workflow skill 必须说明自己处理的对象、使用的方法、具体 todo list、产出的证据或记录。
6. **Workflow step 必须支撑职责达成。**
   每一步都要能解释“它如何推进本 skill 的 primary object，并服务于本节点职责”；不能堆无关检查。
7. **边界必须显式。**
   每个 skill 都要说明何时使用、何时不用、和相邻 skill 的区别、冲突时回哪里。
8. **产出必须可回读、可恢复。**
   会改变 workflow 状态的结果必须落到 artifact、record、evidence、progress 或 handoff；不能只留在对话里。
9. **主文件要短，且有量化预算。**
   `SKILL.md` 正文建议 < 500 行 / < 5000 tokens。超过此预算的内容应下沉到 `references/`。运行时 compaction 后仅保留前 5000 tokens，多个 skill 共享约 25000 tokens 总预算——每个多余 token 都在和对话历史、系统提示竞争注意力。
10. **路径写法要可迁移。**
   不要把 skill 绑定到某个仓库安装根、某个 pack 名或某个项目私有目录。项目工件路径优先遵循项目权威约定（项目可在自己的 guidelines / CONTRIBUTING / 宿主工具链 sidecar 中声明）；skill pack 内共享资料用当前 pack 语义或稳定相对路径表达。

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

## HF Skill-Node Contract

对 HF workflow skill，`SKILL.md` 必须把 `skill-node-define.md` 的节点契约写成运行时可执行内容。

| Contract | 在 `SKILL.md` 中怎么体现 | 不足时的后果 |
|---|---|---|
| Identity | frontmatter、H1 开场、`When to Use`、相邻 skill 边界 | 系统误触发或漏触发 |
| Object | `Object Contract`、workflow step 的 `Object` 字段、output 对象说明 | agent 不知道自己加工什么，容易越权 |
| Method | `Methodology`、workflow step 的 `Method` 字段、rubric / verification | 只剩 checklist，没有可靠做法 |
| Workflow | 编号 todo list、precheck、reroute、handoff | 节点不可执行或不可恢复 |
| Quality | `Hard Gates`、`Red Flags`、`Verification`、evals | 节点会绕过证据或自我验收 |

其中 Object Contract 用来向 agent 说明：本 skill-node 正在处理的 primary object 是什么，它来自哪个 frontend input object，完成后会变成哪个 backend output object。这里的对象可以是用户意图、spec、design model、task plan、active task、review finding set、evidence bundle 或 closeout pack，不必是代码 class。

如果一个 workflow skill 无法说清自己的 primary object，通常说明它的职责边界还不稳定；不要先靠更长的 workflow 弥补。

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
| `## Object Contract` | HF workflow skill 必需 | 写 primary object、frontend input object、backend output object 与边界 |
| `## Methodology` | HF workflow skill 必需 | 写本节点用什么方法完成职责，以及方法如何落地 |
| `## Workflow` | 必需 | 写带 object / method / input / output / stop rule 的 todo list |
| `## Output Contract` | 按需 | 写落盘工件、状态同步、canonical next action |
| `## Red Flags` | 必需 | 写运行时 stop sign |
| `## Common Mistakes` | 按需 | 写 mistake -> consequence/fix |
| `## Common Rationalizations` | **必需（v0.2.0 起，ADR-002 D9）** | 写借口 -> 反驳/Hard rule，节点内防御 agent 偷懒 |
| `## 和其他 Skill 的区别` | **禁止（v0.2.0 起，ADR-002 D9）** | 与 `When to Use` 重复；邻接边界必须写在 `When to Use` |
| `## Reference Guide` / `## Supporting References` | 按需 | 指向深度材料 |
| `## Verification` | 必需 | 退出条件 |

默认不建议扩散的章节：

- `Overview`
- `Standalone Contract`
- `Chain Contract`
- `Inputs / Required Artifacts`（应并入 `Object Contract`、`Workflow` 或 `Output Contract`）
- `Core Authority`（应并入开场、`Hard Gates` 或 `Verification`）
- `Quality Bar`（应并入 `Hard Gates`、`Red Flags` 或 `Verification`）

这些内容应尽量吸收到已有骨架里，而不是再长一层。

显式禁止的章节（v0.2.0 起，ADR-002 D9）：

- `和其他 Skill 的区别` —— 与 `When to Use` 语义重复。邻接边界、reroute 条目必须写在 `When to Use` 中。

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

### `Hard Gates`

Hard Gates 写不可协商的停止条件，尤其要体现 `soul.md` 的硬纪律：

- 方向、取舍、标准不清时，停下来抛回用户，而不是让 skill 自己拍板。
- 需要独立 review / approval 的地方，当前 skill 不能替用户或 reviewer 验收自己。
- 缺少可回读工件、record、evidence 或 progress 时，不得假装 workflow 可恢复。
- 质量证据不足时，不能为了推进速度降低门禁。

Hard Gates 不是普通建议，也不是“最好检查一下”的 checklist。命中后必须停止、回修、reroute 或升级给用户。

### `Object Contract`

HF workflow skill 必须说明自己处理的对象：

- `Primary Object`: 本 skill 真正加工、评审、验证或交接的对象。
- `Frontend Input Object`: 从用户请求、上游工件、progress、review record 或 evidence 接收的对象。
- `Backend Output Object`: 完成后交给下游的对象。
- `Object Transformation`: 输入对象如何变成输出对象。
- `Object Boundaries`: 当前 skill 不应修改、创造或替代哪些对象。
- `Object Invariants`: 对象在执行前后必须保持的关键约束。

如果这些内容太长，可以把对象字段定义下沉到 `references/`，但 `SKILL.md` 主文件必须保留最小对象契约。否则 agent 容易把用户自然语言、上游工件、当前节点对象和下游产物混成一团。

### `Methodology`

HF workflow skill 不只写“做什么”，还要写“用什么方法做”。

`Methodology` 至少回答：

- 本节点采用哪些方法。
- 每个方法解决什么风险。
- 方法作用于哪个 primary object。
- 方法如何支撑 `Frontend Input Object -> Primary Object -> Backend Output Object`。
- 哪些方法是 hard rule，哪些只是辅助参考。

方法论不能只停留在 pack-level README 或概念表格里。只要会改变节点行为，就必须在 `Workflow`、`Hard Gates`、`Verification`、rubric 或 reference 中有可执行落点。

### `Workflow`

要求：

- 用编号步骤
- 先读最少必要证据
- 每步说明处理的 object
- 每步说明使用的 method
- 每步说明 input / output
- 每步说明 stop / continue rule
- 每步都要支撑当前 skill 的职责达成
- 决策点明确
- reroute 路径明确
- 复杂 rubric / 模板 / map 优先下沉到 `references/`

推荐每个 step 至少包含：

```markdown
1. <todo>
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:
```

不要把 `Workflow` 写成阶段标题堆叠，例如“读取 -> 分析 -> 输出”。HF 的 workflow 是可执行 todo list，必须能让下一个 agent 知道当前步骤如何加工对象、应用方法并留下证据。

### `Output Contract`

当 skill 会写工件、记录、状态或 handoff 时，本节应明确：

- 写什么
- 写到哪里
- 状态怎么同步
- 下一步 skill 怎么写

这里的“写到哪里”不是把 repo-local 路径硬编码回去，而是要区分两类路径：

- **项目工件路径**：如 spec / design / tasks / reviews / verification / release notes，优先遵循项目权威约定；若要给 fallback，只能写成默认路径或示例路径，不能把当前仓库特有目录伪装成通用事实。
- **skill pack 共享资料**：如模板、protocol、map、shared docs，不要写死历史安装前缀、repo-root 私有路径或 pack 私有命名；优先使用当前 skill pack 语义下稳定可解析的路径表达。

一个简单判断标准是：把当前 skill 移到另一个仓库、改 pack 名或改变安装位置后，这个路径引用是否仍然成立；如果不会，说明它被写死了。

### `Red Flags` 与 `Common Mistakes`

两者不是一回事：

- `Red Flags`：运行时 stop sign，偏“看到这个就别继续”
- `Common Mistakes`：作者或调用方最常犯的错误，偏“错误 -> 后果/修复”

如果只需要 stop sign，保留 `Red Flags` 即可；如果需要清楚说明错误和修复方式，再加 `Common Mistakes`。不要两节写成一模一样的内容。

### `Common Rationalizations`

v0.2.0 起为必需段（ADR-002 D9）。结构：

```markdown
## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "<skill 域内最常见的偷懒理由 1>" | <对应反驳，引用本 skill 已有的 Hard Gates / Workflow stop rule / Verification 条款> |
| ... | ... |
```

要求：

- 至少 3 条、至多 8 条。
- 每条**必须**引用本 skill 已有的 Hard Gates / Workflow stop rule / Verification 条款，**不允许**凭空编造新的 hard rule。
- 推荐位置：`Red Flags` 之后、`Verification` 之前；如有 `Common Mistakes`，放在 `Common Mistakes` 之后。
- 与 `Common Mistakes` 的区别：`Common Mistakes` 写"作者最容易写错的 anatomy"，`Common Rationalizations` 写"agent 在 runtime 最容易找的偷懒借口"。两节不能是同一份内容的换皮。

### 邻接 skill 边界写在哪里（v0.2.0 起，ADR-002 D9）

`和其他 Skill 的区别` 章节在 v0.2.0 起**禁止**单独成节。邻接边界必须直接写进 `When to Use`，作为「不适用 / reroute」段的一部分：

```markdown
## When to Use

适用：
- ...

不适用：
- 上游条件不满足 → `<上游 skill>`
- 已进入下游 → `<下游 skill>`
- 评审请求 → `<对应 review skill>`
- 阶段不清 / 证据冲突 → `hf-workflow-router`
```

最容易混淆的相邻节点（每个 skill 至少要在 `When to Use` 中显式区分一行）：

| 当前 skill | 至少要区分谁 |
|---|---|
| `using-hf-workflow` | `hf-workflow-router` |
| `hf-specify` | `hf-design` / `hf-spec-review` |
| `hf-design` | `hf-tasks` / `hf-design-review` |
| `hf-test-driven-dev` | `hf-test-review` / `hf-*-review` / gates |
| `hf-completion-gate` | `hf-finalize` |
| `hf-hotfix` | `hf-test-driven-dev` / `hf-workflow-router` |

### `Verification`

只检查退出条件，不写礼貌性 checklist。优先检查：

- record 是否落盘
- 状态是否同步
- verdict / next action 是否唯一
- fresh evidence 是否存在

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
- 当前节点的 primary object / object transformation
- 当前节点使用的方法论及其 hard-rule 落点
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

`evals/` 测的是行为 contract，不是措辞复读。对 HF workflow skill，eval 至少应覆盖：

- 正确识别或拒绝错误的 primary object。
- 不把 frontend input object 直接当成可执行下游对象。
- 方法论是否实际影响 workflow 判断，而不是只出现在 prose。
- 缺少 record / evidence / approval 时是否停止或 reroute。
- 是否避免替用户定方向、做取舍、改标准或验收自己。

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
| HF workflow skill 不写 primary object | agent 不知道自己加工什么，容易越权或跳步 | 补 `Object Contract`，明确 input / primary / output object |
| 只有方法论名，没有 workflow 落点 | 方法成了装饰，不能改变行为 | 把方法映射到 step、rubric、hard gate 或 verification |
| Workflow step 不服务节点职责 | checklist 变长但执行不更准 | 删除无关步骤，保留能推进对象转换和证据闭环的 todo |
| skill 替用户做方向 / 取舍 / 标准决定 | 违反 soul，HF 假装自己是架构师 | 写成 hard gate，抛回用户或记录待决问题 |
| 实现节点或 authoring 节点自称通过 | 违反“HF 不替用户验收自己” | 交给独立 review / approval / gate 产出 verdict |
| 不写与相邻 skill 的区别 | 容易误触发 | 必须写进 `When to Use` 的「不适用 / reroute」段（v0.2.0 起禁止单独成节，ADR-002 D9） |
| 缺 `Common Rationalizations` 段 | runtime 时 agent 容易找借口跳步 | 补段；每条引用本 skill 已有的 Hard Gates / Workflow stop rule / Verification（v0.2.0 起必需，ADR-002 D9） |
| 共享约定在每个 skill 里重复展开 | 主文件臃肿、漂移 | 上收至 family-level `docs/` |
| 核心规则被藏进 `references/` | 主文件失去 runtime contract | 把关键规则搬回主文件 |
| 在 skill 里写死 repo-local 路径 / 安装前缀 | 换仓库、换 pack 名、换项目约定后失效 | 项目工件路径先读项目权威约定；共享资料改用当前 pack 语义或稳定相对路径 |
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

## Object Contract

## Methodology

## Workflow

1. <todo>
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

## Output Contract

## Red Flags

## Common Mistakes

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "<偷懒理由 1>" | <反驳，引用本 skill 的 Hard Gates / Workflow stop rule / Verification 条款> |

## Reference Guide

## Verification
```

说明：

- `Object Contract` 与 `Methodology` 对 HF workflow skill 是必需项；对非 workflow 的 technique / reference skill，可以按需合并进开场或 `Workflow`。
- `Hard Gates`、`Output Contract`、`Common Mistakes`、`Reference Guide` 都是按需出现。
- `Common Rationalizations` 自 v0.2.0 起为必需段（ADR-002 D9）。
- `和其他 Skill 的区别` 自 v0.2.0 起**禁止**单独成节（ADR-002 D9）；邻接边界必须写在 `When to Use`。
- 对薄节点，可以只保留：开场、`When to Use`、最小 `Object Contract`、`Workflow`、`Red Flags`、`Common Rationalizations`、`Verification`。
- 标题名可以按节点需要轻微变化，但语义职责不能漂移。

## 检查清单

在新增或重写 `hf-*` skill 时，至少检查：

- `description` 是否是分类器，而不是摘要
- `description` 是否使用祈使句，是否前置关键触发场景
- H1 下的开场是否足够短
- 开场是否清楚写出唯一职责和不替代什么
- 是否符合 `soul.md`：没有替用户定方向、做取舍、改标准或验收自己
- `When to Use` 是否写清触发条件和边界
- 是否明确说明了与相邻 skill 的区别
- HF workflow skill 是否写清 primary object
- 是否写清 frontend input object、backend output object 和 object transformation
- 是否写清 object boundaries 与 invariants
- 是否声明采用的方法论，以及每个核心方法如何落到 workflow / hard gate / verification
- `Workflow` 是否先读最少必要证据
- `Workflow` 每步是否包含 object / method / input / output / stop rule
- `Workflow` 每步是否支撑本 skill 职责达成，而不是堆无关检查
- 需要落盘工件时，是否写了 `Output Contract`
- 需要交接时，是否写出 canonical next action 或 reroute 条件
- 路径引用是否避免写死 repo-local 安装前缀，且项目工件路径是否以项目权威约定优先
- 是否区分了 `Red Flags` 与 `Common Mistakes`
- 共享语义是否已上收至 `docs/`
- 长 reference 是否已下沉到 `references/`
- 高风险边界行为是否有 `evals/`，且 eval 覆盖对象误判、方法落地、证据缺失和越权验收
- `SKILL.md` 正文是否 < 500 行 / < 5000 tokens
- `scripts/` 文件名是否具备语义，是否可独立执行
- 是否有版本快照和质量退化信号追踪机制
- **是否包含 `## Common Rationalizations`**（v0.2.0 起必需，ADR-002 D9 / D10）
- **是否不包含 `## 和其他 Skill 的区别`**（v0.2.0 起禁止；邻接边界已折叠进 `When to Use`，ADR-002 D9 / D10）

## 一句话约束

HF 的目标态 skill anatomy，是把 `SKILL.md` 写成一个短而硬的运行时 contract：description 负责分类，正文说明对象、方法和执行 todo，边界必须显式，长材料下沉，产出可回读，退出条件可验证。

> 冲突仲裁：本文件与 `docs/principles/soul.md` 出现冲突时，以 soul 为准；与 `docs/principles/skill-node-define.md` 出现 workflow-node 设计口径冲突时，先按 `01` 修正本文。

# HF Spec Review Rubric

## Purpose

本文定义 `hf-spec-review` 的正式审查维度，使 reviewer 不只是“看起来像规格就放行”，而是按统一规则判断规格是否真的足以成为 `hf-design` 的稳定输入。

## Review Principle

- 先找问题，再给结论。
- 结论由 evidence 驱动，而不是“整体感觉差不多”。
- review 关注 WHAT 的清晰度、可验收性和可追溯性，不顺手开始 HOW 层设计。
- 不硬编码固定章节数量。结构要求以项目级约定、当前项目模板或当前规格骨架为准。

## Group Q: Quality Attributes

| ID | Check | Pass Condition |
|---|---|---|
| `Q1` | Correct | 每条核心需求都能回指到真实来源，没有孤儿需求 |
| `Q2` | Unambiguous | 没有“快 / 稳 / 友好 / 易用”等未量化模糊词 |
| `Q3` | Complete | 关键输入、输出、错误路径、边界条件没有明显缺口 |
| `Q4` | Consistent | 需求之间没有互相冲突的状态、权限、范围或时序 |
| `Q5` | Ranked | 每条核心需求都有明确优先级；不会所有内容都被默认成最高优先级 |
| `Q6` | Verifiable | 能形成通过 / 不通过判断，而不是主观感受 |
| `Q7` | Modifiable | 同一要求没有散落到多个位置互相重复或互相矛盾 |
| `Q8` | Traceable | 关键需求具备稳定 `ID` 与 `Source / Trace Anchor` |

## Group A: Anti-Patterns

| ID | Anti-Pattern | Detection Signal |
|---|---|---|
| `A1` | 模糊词 | 未量化的质量形容词或体验口号 |
| `A2` | 复合需求 | 一条需求里通过“和 / 或 / 以及”串起多个独立能力 |
| `A3` | 设计泄漏 | 直接写 `class`、`endpoint`、消息主题、表结构、重试次数等实现细节 |
| `A4` | 无主体的被动表达 | 看不出是谁触发、谁响应、系统要产生什么可观察结果 |
| `A5` | 占位或待定值 | `TBD`、`待确认`、`后续补充` 等仍留在关键需求中 |
| `A6` | 缺少负路径 | 整个功能域只写 happy path，没有失败、边界或权限差异 |

## Group C: Completeness And Contract

| ID | Check | Pass Condition |
|---|---|---|
| `C1` | Requirement contract | 核心 `FR` / 关键 `NFR` 已具备 `ID`、`Statement`、`Acceptance`、`Priority`、`Source / Trace Anchor` |
| `C2` | Scope closure | 范围内 / 范围外内容明确，不依赖聊天记忆补脑 |
| `C3` | Open-question closure | 阻塞性开放问题已关闭；剩余开放问题不会改变设计主干 |
| `C4` | Template alignment | 文档遵循当前项目模板或 项目约定；若没有模板，至少符合 HF 默认骨架 |
| `C5` | Deferral handling | 真实 deferred requirements 已进入 backlog，或已明确不存在；不会只埋在 prose 里 |
| `C6` | Goal and success criteria | 当前轮目标与 success criteria 明确、具体、可判断，不只是抽象愿景或口号 |
| `C7` | Assumption visibility | 关键 assumptions 已显式写出，且其失效影响可回读；不会把关键假设藏在 prose 里 |

## Group G: Granularity And Scope-Fit

| ID | Check | Pass Condition |
|---|---|---|
| `G1` | Oversized FR | 明显命中 `GS1-GS6` 的需求已经拆分、确认或带有保留理由 |
| `G2` | Mixed release boundary | 当前轮需求与后续增量没有继续混写在同一条核心 `FR` 里 |
| `G3` | Repairable scope | 若返回 `需修改`，findings 能收敛成 1 到 2 轮定向回修，而不是要求整份规格推倒重来 |

`G1` 中的 `GS1-GS6` 具体指以下 oversized 信号：

- `GS1`: 多角色打包
- `GS2`: CRUD 打包
- `GS3`: 场景爆炸
- `GS4`: 关注点跨层或跨工作流打包
- `GS5`: 多状态混写
- `GS6`: 时间耦合

记录 finding 时：

- `G1` / `G2` / `G3` 用于 Group G 的主检查项
- `GS1-GS6` 用于指明具体命中的 oversized 子信号

## Finding Classification

每条 finding 必须带上修复归属：

- `USER-INPUT`
- `LLM-FIXABLE`

默认判断规则：

### `USER-INPUT`

这些问题需要用户、业务方或外部权威输入，reviewer 不能擅自补：

- 业务规则不明确
- 未量化的性能 / 可靠性 / 安全阈值
- 法务、合规、保留期限、审批权责等外部决策
- 优先级冲突
- 来源锚点不明确，且无法从现有工件唯一回推
- 失败行为是否允许继续、回滚、通知谁等业务裁决
- 复合需求一旦拆分就会改变当前轮范围、版本边界、延后归属或已确认优先级

### `LLM-FIXABLE`

这些问题在不新增业务事实的前提下，可以由 authoring 节点直接修：

- 拆分复合需求，但仅限拆分不会改变当前轮范围、版本边界、延后归属或已确认优先级
- 去除设计泄漏
- 补足清晰的主体或触发条件
- 统一编号或整理重复条目
- 调整章节放置、模板映射或 wording
- 将已经清楚属于 deferred 的条目移入 backlog，并在正文补链接

## Never Invent Rule

reviewer 不得为了让 rubric 过关而自行发明：

- 数值阈值
- 业务优先级
- 合规结论
- 缺失来源
- 用户未确认的失败处理规则

若缺的是事实，分类就应是 `USER-INPUT`，而不是“先帮用户补一个看起来合理的值”。

## Recommended Finding Format

为了让 `hf-specify` 能定向回修，建议在 review 记录中用以下标签格式：

```markdown
- [important][USER-INPUT][Q2] “系统需要快速响应”缺少可验证阈值，当前无法形成验收标准。
- [important][LLM-FIXABLE][A2] `FR-001` 同时打包提交、审批、导出和归档，应拆分为独立需求。
```

## Verdict Guidance

- `通过`：所有关键检查通过，且没有阻塞设计的 `USER-INPUT` finding
- `需修改`：规格有用且方向清楚，预计 1 到 2 轮定向回修可达标
- `阻塞`：核心范围、关键业务规则、关键外部约束或 route / stage / 证据条件仍未站稳

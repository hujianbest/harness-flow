# df Spec Review Rubric

> 配套 `df-spec-review/SKILL.md`。展开评分维度与 Group Q/A/C/G/SR rule IDs。维度集按 work item 类型不同。

## 通用维度（任何 work item 类型）

| 维度 | 关键检查 | < 6 的典型信号 |
|---|---|---|
| **S1 Identity & Traceability** | Work Item Type / ID 唯一；Owning Component / Subsystem 按类型必填且唯一；上游单据锚点齐全可解析 | SR 缺所属子系统；AR 多组件混写；上游锚点无版本号 |
| **S2 Scope & Non-Scope Clarity** | 范围内 / 范围外显式；当前轮目标可被设计者 / 需求负责人冷读 | 仅有"做这个 SR / AR"一句话；非范围隐藏在正文 |
| **S3 Requirement Row Quality** | 每条核心 row 含 ID / Statement / Acceptance / Source；按类型必填 Component Impact（AR）或 Affected Components（SR） | 缺 Acceptance；Source 是口头会议；SR row 缺 Affected Components |
| **S4 Embedded NFR Quality** | 实时性 / 内存 / 并发 / 资源 / 错误处理 NFR 含可判定阈值 | "性能要好"、"低内存" |
| **S6 Open Questions Closure** | 阻塞 / 非阻塞分类；阻塞项闭合或显式 USER-INPUT | 阻塞项隐藏在正文 |

## AR / DTS / CHANGE 额外维度

| 维度 | 关键检查 | < 6 的典型信号 |
|---|---|---|
| **S5 Component Impact Assessment** | 是否影响组件接口 / 依赖 / 状态机已显式判断 | 章节缺失；判断与 row 中 Component Impact 字段冲突 |

## SR 额外维度

| 维度 | 关键检查 | < 6 的典型信号 |
|---|---|---|
| **S5-SR Subsystem Scope & Affected Components** | 子系统范围明确；Affected Components 章节完整且与 row 表交叉一致 | 受影响组件清单缺失；row 的 Affected Components 与章节不一致 |
| **S7-SR AR Breakdown Candidates** | 候选 AR 拆分清单存在；每条候选 Owning Component 唯一、Covers SR Rows 完整、Hand-off Owner 明确；如显式声明「无可拆分 AR」由需求负责人确认 | 缺候选清单；候选 Owning Component 不唯一；候选不能反向覆盖 SR row |
| **S8-SR Component Design Impact** | 若本 SR 触发组件设计修订，已显式列出受影响章节与修订方向；触发与不触发的判断与 Affected Components 一致 | 章节缺失；与 Affected Components 表互相打架 |

任一维度 < 6 → 不得 `通过`。

## Group Q：Quality Attributes

| Rule | 检查 |
|---|---|
| Q1 | 模糊词（"足够快"、"合适"、"必要时"）已被量化或转 USER-INPUT |
| Q2 | Acceptance 可判定，不依赖隐含上下文 |
| Q3 | 需求间无冲突或重复 |
| Q4 | Priority（若团队使用）已标注 |
| Q5 | 嵌入式相关 NFR 已显式落到 NFR 行（不是只散落正文） |

## Group A：Anti-Patterns

| Rule | 检查 |
|---|---|
| A1 | Statement 不混入实现选择（接口签名、表结构、库名、并发原语） |
| A2 | 单条 row 不打包多个独立行为 |
| A3 | 关键 row 中无待确认 / 占位值 / TBD |
| A4 | 边界、null、错误路径、异常输入已被覆盖 |
| A5 | 不使用无主体被动表达（"系统应该被处理"） |

## Group C：Completeness And Contract

| Rule | 检查 |
|---|---|
| C1 | 业务背景、目标、用户清晰 |
| C2 | 当前轮 success criteria 可冷读 |
| C3 | 范围内 / 范围外闭合 |
| C4 | （AR / DTS / CHANGE）Component Impact Assessment 显式判断（none / interface / dependency / state-machine / runtime-behavior） |
| C5 | Assumptions 已显式且失效影响可回读 |

## Group G：Granularity And Scope-Fit

| Rule | 检查 |
|---|---|
| G1 | 单个 AR 不混写多个独立能力（应拆分为多个 work item） |
| G2 | 当前轮和后续增量未混写 |
| G3 | findings 足够具体可支持定向回修 |

## Group SR：SR-only

仅在 work item type = `SR` 时检查。

| Rule | 检查 |
|---|---|
| SR1 | `Owning Subsystem` 唯一 |
| SR2 | Affected Components 章节存在、清单完整、字段（Component / Modification Surface / Covers Rows / Owning Module Architect / Component Design Impact）齐全 |
| SR3 | Affected Components 表的 Covers Rows 反向覆盖所有核心 SR row（除显式声明的「跨子系统外溢」row） |
| SR4 | AR Breakdown Candidates 章节存在；每条候选含 Candidate ID / Scope / Owning Component（唯一）/ Covers SR Rows / Hand-off Owner；显式声明「无可拆分 AR」时已注明理由 |
| SR5 | 候选 AR 的 Owning Component 必须出现在 Affected Components 表里 |
| SR6 | 候选 AR 之间无范围重叠或循环依赖；如有依赖关系已在 Notes 中说明 |
| SR7 | Component Design Impact 章节存在；与 Affected Components 表的 `Component Design Impact` 列一致 |
| SR8 | SR 不写 AR 级实现设计 / 不预先指定 SOA 接口字段 / 不写代码；只描述子系统级行为与拆分 |

## Severity 分级

- `critical`：阻塞设计 / 阻塞业务交付（缺核心 Acceptance、组件归属冲突、IR-SR-AR 追溯断裂）
- `important`：approval 前应修（NFR 缺阈值、Open Questions 未分类、模糊词未量化）
- `minor`：建议改进（措辞、章节顺序、术语统一）

## Classification

- `USER-INPUT`：缺业务事实 / 外部决策 / 优先级冲突 / NFR 阈值缺失 → 上抛需求负责人 / 模块架构师
- `LLM-FIXABLE`：缺 wording / 章节 / 重复整理 / 设计语言混入 → 开发人员定向回修
- `TEAM-EXPERT`：组件边界、SOA 接口 / 并发 / 实时性专业判断 → 上抛模块架构师 / 资深嵌入式工程师

无法在不新增事实前提下修复的 → 不能标 LLM-FIXABLE。

## Verdict 决策

通用规则：

| 评分 / findings 状态 | verdict |
|---|---|
| 适用维度均 ≥ 6，无 critical USER-INPUT，Open Questions 已闭合或可上抛 | `通过` |
| 评分某项 < 6 但 findings 可 1-2 轮定向修订（无 critical USER-INPUT 阻塞） | `需修改` |
| 评分多项 < 6 / critical USER-INPUT 阻塞 / 范围严重不清 | `阻塞`（内容） |
| route / stage / profile / 上游证据冲突；或 SR 工件试图映射到实现节点 | `阻塞`（workflow），`reroute_via_router=true` |

`通过` verdict 后的 `next_action_or_recommended_skill` 由 SKILL.md 的 verdict 决策表按 work item 类型决定（SR → component-design / finalize；AR / DTS / CHANGE → component-design / ar-design）。

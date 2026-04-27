# mwf Spec Review Rubric

> 配套 `mwf-spec-review/SKILL.md`。展开 6 维度评分细则与 Group Q/A/C/G rule IDs。

## 6 维度评分

| 维度 | 关键检查 | < 6 的典型信号 |
|---|---|---|
| **S1 Identity & Traceability** | Work Item Type / ID 唯一；Owning Component 唯一；IR / SR / AR 锚点齐全且可解析 | 多组件混写、SR 缺失、IR 锚点无版本号 |
| **S2 Scope & Non-Scope Clarity** | 范围内 / 范围外显式；当前轮目标可被设计者冷读 | 仅有"做这个 AR"一句话；非范围隐藏在正文 |
| **S3 Requirement Row Quality** | 每条核心 row 含 ID / Statement / Acceptance / Source / Component Impact | 缺 Acceptance；Source 是口头会议 |
| **S4 Embedded NFR Quality** | 实时性 / 内存 / 并发 / 资源 / 错误处理 NFR 含可判定阈值 | "性能要好"、"低内存" |
| **S5 Component Impact Assessment** | 是否影响组件接口 / 依赖 / 状态机已显式判断 | 章节缺失；判断与 row 中 Component Impact 字段冲突 |
| **S6 Open Questions Closure** | 阻塞 / 非阻塞分类；阻塞项闭合或显式 USER-INPUT | 阻塞项隐藏在正文 |

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
| C4 | Component Impact Assessment 显式判断（none / interface / dependency / state-machine / runtime-behavior） |
| C5 | Assumptions 已显式且失效影响可回读 |

## Group G：Granularity And Scope-Fit

| Rule | 检查 |
|---|---|
| G1 | 单个 AR 不混写多个独立能力（应拆分为多个 work item） |
| G2 | 当前轮和后续增量未混写 |
| G3 | findings 足够具体可支持定向回修 |

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

| 评分 / findings 状态 | verdict |
|---|---|
| 6 维度均 ≥ 6，无 critical USER-INPUT，Open Questions 已闭合或可上抛 | `通过` |
| 评分某项 < 6 但 findings 可 1-2 轮定向修订（无 critical USER-INPUT 阻塞） | `需修改` |
| 评分多项 < 6 / critical USER-INPUT 阻塞 / 范围严重不清 | `阻塞`（内容） |
| route / stage / profile / 上游证据冲突 | `阻塞`（workflow），`reroute_via_router=true` |

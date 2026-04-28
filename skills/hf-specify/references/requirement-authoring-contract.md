# HF Requirement Authoring Contract

## Purpose

本文定义 `hf-specify` 在起草规格时对单条需求的最小写法契约。它不是固定模板，而是要求无论项目模板如何变化，核心需求都必须保持同一组可回读语义。

## Minimum Rule

对于 non-trivial 的规格，核心 `FR` / `NFR` 不应只写成松散段落。每条需求至少应具备一组稳定字段，方便 `hf-spec-review` 做冷读、判定和回修。

若项目级约定或项目模板声明了等价字段名、编号规则或优先级体系，优先遵循映射；否则使用本文默认约定。

## Per-Requirement Minimum Fields

| Field | Applies To | Required Content | Notes |
|---|---|---|---|
| `ID` | `FR` / `NFR` / `CON` / `IFR` / `ASM` / `EXC` | 稳定唯一编号，例如 `FR-001`、`NFR-002` | 拆分后可用 `FR-003a`、`FR-003b` 保留追溯关系 |
| `Type` | 全部 | `FR` / `NFR` / `CON` / `IFR` / `ASM` / `EXC` | 可由章节语义隐含，但 reviewer 必须能唯一判断 |
| `Statement` | `FR` / `NFR` / `CON` / `IFR` | 可观察、可判断的需求陈述 | 不写实现细节，避免 `class` / `endpoint` / `table` 等设计语言 |
| `Acceptance` | `FR`，关键 `NFR` | 至少一个可验证验收标准 | 推荐用 Given / When / Then；关键失败路径也要可判定 |
| `Priority` | `FR` / `NFR` / `EXC` | 当前轮优先级 | 若项目未声明其它体系，默认使用 `Must` / `Should` / `Could` / `Won't` |
| `Source / Trace Anchor` | `FR` / `NFR` / `CON` / `IFR` | 这条需求来自哪里 | 必须能回指到用户请求、上游工件、评审 findings 或外部约束 |

## Statement Patterns (EARS — Mavin et al., REFSQ 2009)

如果项目未声明固定需求句式，默认使用 EARS (Easy Approach to Requirements Syntax) 的中文等价模式：

- 常驻行为：`系统必须 <持续成立的能力或约束>`
- 事件触发：`当 <触发条件> 时，系统必须 <可观察结果>`
- 状态约束：`在 <状态/角色/前置条件> 下，系统必须 <行为结果>`
- 异常/负路径：`如果 <异常条件>，系统必须 <保护、反馈或恢复行为>`
- 可选策略：`在启用 <策略/配置> 时，系统必须 <行为结果>`

这些句式的目标是把行为、触发条件、状态和异常拆清楚，而不是强迫统一语感。若项目已有更自然的中文写法，只要语义同样清晰，也可保留。

## Acceptance Criteria Rules (BDD — Dan North, 2006)

验收标准默认采用 BDD (Behavior-Driven Development) 的 Given/When/Then 格式，建立需求到测试的可追溯桥梁。

- 每条核心 `FR` 至少有一个正向验收标准。
- 对关键失败路径、权限差异、边界输入、并发冲突、超时或延迟结果，至少补一条对应验收口径。
- 验收标准要能形成明确的通过 / 不通过判断，不写“用户体验良好”“处理足够快”这类无阈值表达。
- 一个验收标准只验证一个主要行为；若同一条标准同时覆盖多个独立行为，优先回到粒度检查。

## Priority Rules (MoSCoW — DSDM Consortium, 1994)

优先级默认使用 MoSCoW 方法（Must/Should/Could/Won't）驱动范围收敛。

- 若项目级约定或项目模板声明了固定优先级体系，优先使用该体系。
- 若没有显式体系，默认使用 `Must` / `Should` / `Could` / `Won't`。
- 优先级是逐条需求的属性，不是整份规格的总体评价。
- 需要延后到后续增量的真实需求，不允许既无优先级也无延后理由。
- 多条需求都声称是最高优先级且互相冲突时，不能自行拍板，必须回到用户确认。

## Source / Trace Anchor Rules

每条核心需求至少要有一个可回读锚点。常见写法包括：

- `用户请求: "审批通过后通知申请人"`
- `spec-bridge: docs/insights/xxx-spec-bridge.md#关键假设 2`
- `现有约束:项目级约定中的浏览器兼容规则`
- `review finding: features/<active>/reviews/spec-review-YYYY-MM-DD.md#finding-3`
- `外部约束: 法规 / 合同 / 兼容要求`

规则如下：

- 不要求写成正式 trace matrix，但 reviewer 必须能冷读出“这条为什么存在”。
- 若锚点不清楚，不要凭空编造；应回到用户或上游工件澄清。
- 若一条需求来自多个来源，先写主要来源，再补次级来源。

## Brainstorming Notes Normalization

若输入来源是 brainstorming notes、会议散点记录或用户口述碎片，不要直接把原文逐条改写成 `FR` / `NFR`。先做一次归一化：

| 原始内容类型 | 正确落点 | 不应直接写成 |
|---|---|---|
| 已确认的业务行为 | `FR` | 夹带接口名、服务名、表名的“伪需求” |
| 可验证的质量门槛 | `NFR` | “体验更好”“性能高一点”这类无阈值口号 |
| 外部系统、法规、兼容要求 | `IFR` / `CON` | 没有来源锚点的猜测性限制 |
| 团队假设、待确认说法 | `ASM` / 开放问题 | 被伪装成已确认需求 |
| 当前轮不做但真实存在的能力 | `EXC` 或 deferred backlog | 只埋在 prose 里的“以后再做” |
| 接口、重试次数、表结构、服务划分 | 设计输入或开放问题 | `FR` / `NFR` 正文 |

最小归一化目标：

1. 先把“确认过的事实”和“还未确认的想法”分开。
2. 先把“业务意图”和“实现细节”分开。
3. 先把“当前轮必须做”和“后续增量候选”分开。

若做不到这三步，就还没到正式 requirement rows 的时机。

## Minimum Example

```markdown
### FR-002 提交审批申请

- 优先级: Must
- 来源: 用户请求“员工发起审批申请”；spec-bridge 中的“减少线下流转”
- 需求陈述: 当员工提交完整审批信息时，系统必须创建一条待直属主管处理的审批申请。
- 验收标准:
  - Given 员工已填写必填字段且拥有发起权限，When 提交申请，Then 系统创建状态为“待审批”的申请，并记录提交时间。
  - Given 员工缺少必填字段，When 提交申请，Then 系统拒绝提交并明确指出缺失项。
```

## Common Failure Modes

- 只有编号和正文，没有 `Priority`
- 只写“来源于用户需求”而没有更具体的锚点
- 一条 `FR` 打包多个角色、多个流程或多个发布轮次
- 验收标准只是把需求正文重复一遍，没有新增判定口径
- 在需求陈述里夹带接口名、表名、重试次数、服务名等设计决策

## Use With Other References

- 需求是否过大、是否应拆分或延后，见 `references/granularity-and-deferral.md`
- 正式 review 的检查维度和 finding 分类，见 `hf-spec-review/references/spec-review-rubric.md`

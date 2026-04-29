# HF Granularity And Deferral

## Purpose

本文定义 `hf-specify` 在规格阶段如何判断需求是否过大、是否跨了多个发布轮次，以及哪些内容应该进入延后清单而不是继续塞进当前轮范围。

## When To Trigger

出现以下任一信号时，必须做粒度检查：

- 一条 `FR` 包含多个角色、多个目标或多个独立结果
- 验收标准开始覆盖大量互不相同的路径
- 当前轮范围和“以后再做”的能力混在同一条需求里
- 用户同时提到了 MVP、后续版本、增量补做、第二期能力

## G1-G6 Oversized Requirement Heuristics (INVEST 对应)

以下启发式规则对应 INVEST 质量标准中的 **Small**（足够小）和 **Independent**（独立）维度。当需求违反这两个维度时，触发拆分。

| ID | Heuristic | Detection Signal | Typical Action |
|---|---|---|---|
| `G1` | 多角色打包 | 同一条 `FR` 里有 2 个及以上角色做不同动作 | 先按角色拆分 |
| `G2` | CRUD 打包 | 创建、查询、修改、删除被写成一个泛化能力 | 先按独立行为拆分 |
| `G3` | 场景爆炸 | 一条 `FR` 需要 4 个及以上彼此独立的验收场景才能说清 | 先拆主行为和关键分支 |
| `G4` | 关注点跨层 | 同一条 `FR` 同时混了主业务动作、后台后处理、批量运营动作等独立关注点 | 先按用户可感知的独立结果拆分 |
| `G5` | 多状态混写 | 一条 `FR` 覆盖 3 个及以上状态/模式下的不同规则 | 先按状态族拆分 |
| `G6` | 时间耦合 | 触发动作和延迟/定时/归档等后续结果被绑定在同一条需求里 | 先拆即时结果和延时结果 |

## Split Rules

- 拆分后的子需求沿用父需求的主来源与上下文，不得丢失 trace anchor。
- 子需求默认沿用父需求优先级；若拆分后优先级不同，必须显式重判。
- 默认用 `FR-003a`、`FR-003b` 之类编号保留亲缘关系；若项目模板不允许后缀编号，则遵循其映射。
- 每个子需求都要重新写自己的验收标准，不允许只写“同父需求”。
- 若拆分后已经跨越不同发布轮次，必须继续做 scope-fit 判断，而不是默认都留在本轮。

## User Confirmation Rule

以下情况属于 non-trivial split，必须明确向用户确认：

- 一条需求要拆成 4 个及以上子需求
- 拆分会改变当前轮范围边界
- 拆分会导致某些子需求进入后续增量
- 拆分会影响先前已确认的优先级或角色边界

若只是 1 到 3 个明显的机械拆分，且不会改变本轮范围，可先在草稿中给出拆分建议与理由，再在下一轮确认。

## Mechanical Vs Scope-Shaping Split

以下拆分可以视为机械拆分，允许 authoring 节点直接修文：

- 只是把同一当前轮范围内的复合需求拆成更清晰的子需求
- 不改变当前轮范围边界
- 不引入新的 deferred backlog 判断
- 不改变已确认的优先级、角色边界或发布轮次归属

以下拆分不再属于纯 `LLM-FIXABLE`，即使起点是复合需求，也必须先向用户确认：

- 拆分后会把部分子需求移出当前轮
- 拆分后会新增或改变 deferred backlog 条目
- 拆分后会改变已确认的优先级
- 拆分后会改变关键角色边界、验收范围或版本边界

简化判断：

- **只改表达，不改范围** -> 可直接修
- **一旦改范围、优先级或延后归属** -> 先问用户

## Scope-Fit Criteria (INVEST Valuable + Negotiable 对应)

以下判断标准对应 INVEST 中的 **Valuable**（对当前轮有价值）和 **Negotiable**（可协商是否纳入本轮）维度。

| Criterion | Keep In Current Round | Defer To Later |
|---|---|---|
| `Priority` | `Must`，或少量关键 `Should` | `Could` / `Won't`，或当前轮非核心 `Should` |
| `Dependency` | 被当前轮其它能力直接依赖 | 不被当前轮能力依赖 |
| `Completeness` | 需求、约束、验收口径已经足够明确 | 仍缺关键业务规则或外部确认 |
| `Risk` | 业务含义和边界相对稳定 | 不确定性高，可能需要后续单独增量或验证 |
| `Scope Budget` | 当前轮仍能保持可评审、可设计的聚焦范围 | 继续纳入会显著稀释本轮目标 |

## Deferred Backlog Rules

并非所有 `EXC` 都要进入 deferred backlog。只有“真实存在、只是暂不纳入当前轮”的需求，才写入延后清单。

以下情况建议进入 deferred backlog：

- 已被澄清为真实需求，但当前轮不做
- 已有初步优先级和来源
- 后续很可能通过 `hf-increment` 回收

以下情况通常只留在 `EXC`，不单独建 backlog：

- 明确不是目标
- 被用户否决的想法
- 与当前主题无关的旁支讨论

## Deferred Backlog Minimum Schema

默认路径与规格文档相邻：

- `features/<active>/spec-deferred.md`

若 项目已声明等价路径，优先使用映射路径。

建议最小结构：

```markdown
# <主题> 延后需求清单

- 状态: 草稿
- 主题: <主题>

| Source ID | Deferred Capability | Priority | Deferral Reason | Dependency | Re-entry Hint | Recommended Skill |
|---|---|---|---|---|---|---|
| FR-007 | 管理员导出审批报表 | Could | 不属于当前 MVP 主流程 | 无当前轮硬依赖 | 当审批主流程与留存规则稳定后再回收 | hf-increment |
```

## Spec Update Rules After Deferral

若存在延后清单：

- 当前规格正文中的 `EXC` 或范围外章节应明确说明“该能力已延后，详见 deferred backlog”
- 不要把所有延后项只埋在 prose 里，导致后续无法稳定回收
- 已延后项不应继续留在本轮核心 `FR` 列表中冒充当前轮交付范围

## Common Failure Modes

- 看到“大需求”只在 prose 里说“后面再拆”
- 把真正的后续需求混进 `EXC` 一句话，后续无法回收
- 拆分后没有保留来源、优先级和验收标准
- 明显是后续增量的内容仍留在当前轮 `Must`

## Re-Entry

deferred backlog 的 canonical 回收入口是 `hf-increment`。它不是自动下游节点，也不是当前规格阶段的替代完成条件。

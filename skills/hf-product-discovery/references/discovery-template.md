# 产品发现文档模板

若项目级约定为当前项目声明了 discovery 模板、路径或命名要求，优先遵循项目约定。

## 保存路径

默认：`docs/insights/YYYY-MM-DD-<topic>-discovery.md`

若后续需要拆出更细工件，可按需演化为：
- `*-concept-brief.md`
- `*-probe-plan.md`
- `*-insight-pack.md`
- `*-spec-bridge.md`

第一版默认不强制拆分，保持单文档即可。

## 默认结构

```markdown
# <主题> 产品发现草稿

- 状态: 草稿
- 主题: <主题>

## 1. 问题陈述
## 2. 目标用户与使用情境
## 3. Why now / 当前价值判断
## 4. 当前轮 wedge / 最小机会点
## 5. 已确认事实
## 6. 关键假设与风险
## 7. 候选方向与排除项
## 8. 建议 probe / 验证优先级
## 9. 成功度量 (Desired Outcome / North Star / Success Metrics)
## 10. JTBD 视图 (Jobs Stories + 四力，按需)
## 11. OST Snapshot (Outcome → Opportunity → Solution → Assumption)
## 12. Bridge to Spec
## 13. 开放问题（阻塞 / 非阻塞）
```

章节 9–11 是 Phase 0 新增的**可收缩视图**：在 `lightweight` / `standard` / `full` 密度下密度不同，但最小要求始终保留。

## 各章节最小语义

### 1. 问题陈述
- 写用户进展被什么阻塞，不写实现方案
- 优先锚定 JTBD 的 **struggling moment + situation**（见 `jtbd-framework.md`）

### 2. 目标用户与使用情境
- 写触发 job 的**具体情境**，不写"一般用户"
- 若用户角色已知，列角色；不确定时显式写"待验证"

### 3. Why now
- 当前为什么这一轮值得做、而不是放到后续
- 如果属于切换型主题，可引 JTBD 四力（push / pull / anxiety / habit）

### 4. 当前轮 wedge / 最小机会点
- 从候选 opportunity 中收敛出的**唯一主 opportunity**
- 其它候选 opportunity 记到 later ideas 或 section 7 排除项

### 5. 已确认事实
- 必须有证据来源（访谈 / 数据 / 文档），不允许无来源断言

### 6. 关键假设与风险
- 按 Desirability / Viability / Feasibility / Usability 四类分组（按需）
- 每条假设都要能回答「若不成立，当前 wedge 是否还站得住」

### 7. 候选方向与排除项
- 每个当前轮候选方向与 OST 中的 solution 保持一一对应
- 排除项要写**剪枝理由**，不是简单"不做"

### 8. 建议 probe / 验证优先级
- 每条关键假设对应 1 个最小 probe 建议
- probe 的正式落盘交由 `hf-experiment`；此处只写方向与优先级

### 9. 成功度量（Desired Outcome / North Star / Success Metrics）

discovery 草稿必须显式落下本轮的成功度量，至少包括：

| 字段 | 含义 | 最小要求 |
|---|---|---|
| Desired Outcome | 当前轮想变好的**结果指标**（不是产出或活动） | 1 条，可判断 |
| North Star 锚定 | 与项目 North Star / OKR 的关联（若存在） | 若不存在，显式写「项目当前无 North Star 声明」 |
| Leading / Lagging 指标 | 用来观察 outcome 的前瞻 / 滞后指标 | 至少 1 个 leading 或 lagging |
| Success Threshold | 让我们承认 wedge 成功的最小门槛 | 可验证，不允许"体验更好"这类无阈值口号 |
| Non-goal Metrics | 本轮明确**不追求**的指标 | 防止 outcome 被隐式扩大 |

最小示例：

```markdown
- Desired Outcome: 新用户在首次会话内完成可评审 discovery 草稿的比例提高
- North Star 锚定: 关联到 "HF 可评审工件产出率"；项目 North Star 尚未形式化声明
- Leading 指标: 首屏 outcome 字段完成率
- Lagging 指标: discovery-review 首次通过率
- Success Threshold: 5 轮样本中 ≥ 3 次首次通过
- Non-goal Metrics: 不追求缩短整体 coding workflow 总耗时
```

### 10. JTBD 视图（按需）

对于本轮主 opportunity，若用户 job / 情境仍不稳定，至少写出一条 **Jobs Story**（见 `jtbd-framework.md`）：

```text
When <situation>,
I want to <motivation>,
so I can <outcome>.
```

切换型主题可补充四力（push / pull / anxiety / habit）。API-only / 纯内部工具等主题若 job 已经显而易见，可以只在 "问题陈述" 中一笔带过，不强制新设子章节。

### 11. OST Snapshot（按需）

当候选方向 ≥ 2 个或 opportunity / solution 结构复杂时，必须给出一个 **OST 快照**（见 `opportunity-solution-tree.md`）：

```markdown
## OST Snapshot

Desired Outcome: <section 9 中的 outcome>

Opportunity A：<主 opportunity>
  Solution A1：<候选方向 1>
    Assumption：<关键假设 1>
    Probe：<建议验证方式>
  Solution A2：<候选方向 2>
    Assumption：<关键假设 2>

（可选）Opportunity B：<备选 opportunity，本轮不做的原因>
```

规模控制：Outcome 1 个、Opportunity 3–5 个（选 1 主）、每个选中 opportunity 下 Solution 2–3 个、每个 solution Assumption ≤ 2 条。

若只有 1 个候选方向、无需对比剪枝，可以不写 OST 章节，但 section 6 与 section 7 仍要能冷读出等价关系。

### 12. Bridge to Spec

`Bridge to Spec` 子节要写清：
- 推荐带入 `hf-specify` 的范围边界
- 可直接转成规格输入的稳定结论
- 需要继续保留为 assumption 的内容
- 当前不进入 spec 的候选项
- 已确定的 Desired Outcome 与 Success Threshold，作为 spec 阶段 Success Criteria 的上游锚点

### 13. 开放问题
- 阻塞项必须在送评审前关闭或降级
- 非阻塞项可保留

## 编写要求

- 问题陈述写用户进展被什么阻塞，不写实现方案
- wedge 要明确"当前轮最小推进点"，而不是大而全 roadmap
- 已确认事实与假设必须显式分开
- 候选方向与排除项要帮助收敛，而不是无限发散
- 成功度量章节不可省略；若确实缺数据，写"待验证"而不是写"体验更好"
- JTBD / OST 视图的规模要和当前轮 wedge 匹配，不贪大
- `Bridge to Spec` 必须写清哪些结论已稳定到足以进入 `hf-specify`
- 若存在 later ideas，应明确写为后续候选，而不是埋在 prose 里

## 密度分级（profile-aware）

| 章节 | lightweight | standard | full |
|---|---|---|---|
| 1–8（原有结构） | 必填 | 必填 | 必填 |
| 9 成功度量 | 最少写 Desired Outcome + Success Threshold | 加上 Leading / Lagging 指标 | 全部字段（含 North Star 锚定与 Non-goal） |
| 10 JTBD 视图 | 可省略；但问题陈述需含 situation | 至少 1 条 Jobs Story | 至少 1 条 Jobs Story；切换型主题补四力 |
| 11 OST Snapshot | 候选 ≤ 1 可省略；否则至少给最简列表形式 | OST 快照（Outcome / Opportunity / Solution） | 完整 OST（含 Assumption / Probe） |
| 12 Bridge to Spec | 必填 | 必填 | 必填 |

密度降级不等于纪律消失：即便 `lightweight`，Desired Outcome + Success Threshold + Bridge to Spec 仍是 discovery 草稿的 hard requirement。

## 状态同步

discovery 草稿交评审后，应同步：
- 文档状态（`状态: 草稿`）
- discovery 阶段进度记录中的 `Current Stage: hf-product-discovery`（discovery 阶段 feature 尚未创建，progress 记录可临时与 discovery 草稿同目录；进入 feature 后由 `features/<NNN>-<slug>/progress.md` 接管）
- 同上：`Next Action Or Recommended Skill: hf-discovery-review`

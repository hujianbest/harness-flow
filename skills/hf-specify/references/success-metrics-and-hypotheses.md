# Success Metrics & Key Hypotheses 参考

## Purpose

本参考为 `hf-specify` 在 Phase 0 引入两个显式 spec 级字段：

- **Success Metrics**：当前轮规格成功的**可判断度量**
- **Key Hypotheses**：当前规格仍依赖、尚未完全验证的关键假设

它们不是新章节的点缀，而是**规格是否成立的硬 anchor**：下游 `hf-design` / `hf-tasks` / `hf-test-driven-dev` / 质量 gate 都以这两个字段作为验证目标。

## 上游关系

Success Metrics / Key Hypotheses 必须承接 discovery 的产出：

| discovery 输出 | spec 承接字段 |
|---|---|
| Desired Outcome | Success Metrics 的主指标 |
| Success Threshold | Success Metrics 的通过门槛 |
| Leading / Lagging 指标 | Success Metrics 的子指标 |
| Non-goal Metrics | Success Metrics 中显式声明的"不追求的指标" |
| OST 中的关键假设 | Key Hypotheses（按 Desirability / Viability / Feasibility / Usability 分类） |

若 discovery 已写出这些信息，spec 只做承接与细化，不重新发明。若上游没走 discovery（直接从 spec 起），本参考的要求仍是 hard requirement，但允许在规格第一版时承认"待验证"，并显式列入 `hf-experiment` 候选。

## Success Metrics 最小契约

| 字段 | 含义 | 约束 |
|---|---|---|
| **Outcome Metric** | 本轮想变好的主要结果指标 | 1 条，结果指标（不是产出或活动） |
| **Threshold** | 最小可接受的门槛 | 有数字 / 百分比 / 明确判定，不允许"体验更好" |
| **Leading Indicator(s)** | 用来早期观察是否在朝目标前进 | 至少 1 条（lightweight 允许合并到 outcome） |
| **Lagging Indicator(s)** | 用来事后确认成果的滞后指标 | 至少 1 条（lightweight 允许合并到 outcome） |
| **Measurement Method** | 如何采集该指标 | 数据源 / 采集频率 / 负责工件 |
| **Non-goal Metrics** | 本轮明确**不追求**的指标 | 防止范围被隐式扩大；可留空但要显式写"无" |
| **Instrumentation Debt** | 当前是否具备采集能力，不具备时的补齐计划 | 若缺失但允许上线，必须写补齐计划 |

### 最小示例

```markdown
## Success Metrics

- Outcome Metric: 新 discovery 会话在单次内达到可评审状态的比例
- Threshold: ≥ 70%，基于 5 轮样本
- Leading Indicator: 首屏 Desired Outcome 字段完成率 ≥ 90%
- Lagging Indicator: discovery-review 首次通过率
- Measurement Method: 通过评审日志目录 docs/reviews/ 按 feature 汇总；每周快照
- Non-goal Metrics: 不追求缩短 coding workflow 总耗时；不追求覆盖 ML 产品主题
- Instrumentation Debt: 无；评审日志已具备
```

## Key Hypotheses 最小契约

| 字段 | 含义 | 约束 |
|---|---|---|
| **ID** | `HYP-NNN` | 规格内唯一，允许后续 `hf-experiment` 引用 |
| **Statement** | 假设陈述 | 一句话可证伪，而不是口号 |
| **Type** | Desirability / Viability / Feasibility / Usability | 强制分类（来自 Teresa Torres 四类假设） |
| **Impact If False** | 若不成立，对 spec 的影响 | 标明 spec / 范围 / NFR 的哪部分塌陷 |
| **Confidence** | 当前信心度 | 高 / 中 / 低，必须给出理由 |
| **Validation Plan** | 验证方式（对应 `hf-experiment` probe） | 低 confidence 假设必须有 plan |
| **Blocking?** | 是否阻塞 spec 进入 design | 若阻塞，该假设未验证前 spec 不能通过评审 |

### 最小示例

```markdown
## Key Hypotheses

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-001 | 用户愿意在 discovery 首屏显式写出 Desired Outcome | Desirability | 整个 outcome-first 路径无效，需退回旧模板 | 中 | 5 次真实对话抽检（交 hf-experiment） | 否 |
| HYP-002 | evidence 目录能稳定承接 RICE / ICE 分数的证据回指 | Feasibility | spec 的量化优先级不可回读 | 高 | 复用现有 reviews/ 目录结构 | 否 |
| HYP-003 | JTBD 模板不会让 lightweight profile 体感过重 | Usability | 密度分级策略需重设计 | 低 | 一次 lightweight 场景真人 dry run | 是 |
```

## 与 Requirement Rows 的关系

Success Metrics 与 Key Hypotheses **不与 FR / NFR 并列**，而是**驱动它们**：

- 每条 FR / NFR 的 `Source / Trace Anchor` 允许指向某条 Hypothesis 或 Success Metric
- 任何与 Success Metric 无法建立关联的需求，应被质疑是否真的属于当前轮
- Key Hypotheses 中标 `Blocking? = 是` 的假设未验证前，对应需求的 Acceptance 不能视为可判定

## Spec 评审前自检

送 `hf-spec-review` 前确认：

- [ ] Success Metrics 章节存在，且至少含 Outcome Metric + Threshold + Measurement Method
- [ ] 指标都是结果指标，不是产出活动（"写了几份 spec" 不算结果指标）
- [ ] Non-goal Metrics 已显式写出或显式标"无"
- [ ] Key Hypotheses 章节存在；每条假设含 Type / Impact If False / Confidence
- [ ] 低 confidence 假设有 Validation Plan；Blocking 假设如仍未验证，阻塞评审通过
- [ ] discovery 上游的 Desired Outcome 已被承接，没有凭空新造指标

## 下游衔接

- `hf-design` 在候选方案 compare view 中，应显式评估对 Success Metrics 的影响
- `hf-tasks` 的任务 Acceptance 应可追溯到具体 FR/NFR，进而回到 Success Metric / Hypothesis
- `hf-test-driven-dev` 的 test design 最薄端到端路径应覆盖 Success Metric 的 Leading Indicator（若可自动化）
- `hf-completion-gate` 在 Phase 3 引入产品指标回流后，会直接消费 Success Metrics 作为 closeout 的 evidence 锚点
- `hf-experiment` 以 Key Hypotheses 作为 probe 清单的默认输入

## 常见 Red Flag

- Success Metric 写成"用户体验更好"无阈值口号
- 指标看起来像产出活动（"完成 spec 草稿"）而不是结果
- Non-goal Metrics 从未出现，导致下游范围被隐式扩大
- Key Hypotheses 只有一条"我们觉得方向对"
- Blocking 假设仍是低 confidence，但 spec 继续往下走
- Instrumentation Debt 存在但无补齐计划

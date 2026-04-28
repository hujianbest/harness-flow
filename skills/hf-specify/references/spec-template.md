# 规格文档模板

若项目级约定为当前项目声明了规格模板、章节骨架或命名要求，优先遵循项目约定。

## 保存路径

默认：`features/<active>/spec.md`

Deferred backlog（若存在）：`features/<active>/spec-deferred.md`

若 项目声明了规格路径映射，优先使用映射路径。

## Product Discovery 上游输入

若当前主题来自 product discovery，优先补充读取：
- `docs/insights/*-spec-bridge.md`（高价值上游输入）
- 按需展开：`*-insight-pack.md`、`*-concept-brief.md`、`*-probe-plan.md`

`spec-bridge` 只负责提供更稳定的上游 thesis、范围边界与 unknowns，不替代正式需求规格正文。

Phase 0 起，discovery 若产出以下内容，spec 必须显式承接（不允许凭空新造）：

- Desired Outcome + Success Threshold + Leading / Lagging 指标 + Non-goal Metrics → 映射到 spec 的 **Success Metrics** 章节
- OST 中的关键假设 → 映射到 spec 的 **Key Hypotheses** 章节

## 默认结构

```markdown
# <主题> 需求规格说明

- 状态: 草稿
- 主题: <主题>

## 1. 背景与问题陈述
## 2. 目标与成功标准
## 3. Success Metrics
## 4. Key Hypotheses
## 5. 用户角色与关键场景
## 6. 当前轮范围与关键边界
## 7. 范围外内容
## 8. 功能需求
## 9. 非功能需求 (ISO 25010 + Quality Attribute Scenarios)
## 10. 外部接口与依赖（按需）
## 11. 约束与兼容性要求
## 12. 假设与失效影响（按需）
## 13. 开放问题（区分阻塞 / 非阻塞）
## 14. 术语与定义（按需）
```

章节 3 (Success Metrics) 与章节 4 (Key Hypotheses) 是 Phase 0 新增的 **hard anchor**，不可省略。章节 9 的 NFR 必须使用 Quality Attribute Scenarios 格式（见 `nfr-quality-attribute-scenarios.md`）。

## 各章节最小语义

### 1. 背景与问题陈述
- 写为什么要做，不写方案
- 承接 discovery 的 problem statement / struggling moment

### 2. 目标与成功标准
- 写高层目标与总体成功标准口径
- 具体可验证度量落到 section 3 Success Metrics

### 3. Success Metrics（Phase 0 新增）
按 `references/success-metrics-and-hypotheses.md` 最小契约填写：

- Outcome Metric（1 条，结果指标）
- Threshold（有数字或可判定）
- Leading Indicator(s) / Lagging Indicator(s)
- Measurement Method
- Non-goal Metrics
- Instrumentation Debt

承接 discovery 的 Desired Outcome / Success Threshold / Non-goal Metrics。若无 discovery 上游，也必须按该最小契约填写。

### 4. Key Hypotheses（Phase 0 新增）
按 `references/success-metrics-and-hypotheses.md` 最小契约填写表格：

- ID / Statement / Type (D/V/F/U) / Impact If False / Confidence / Validation Plan / Blocking?

Blocking 假设仍未验证时，不得进入 `hf-spec-review=通过`。

### 5. 用户角色与关键场景
- 角色与关键场景，承接 discovery 的 JTBD situation

### 6. 当前轮范围与关键边界
- 显式区分当前轮边界与后续增量边界

### 7. 范围外内容
- 列出本轮明确不做的能力，与 deferred backlog 衔接

### 8. 功能需求（FR）
按 `requirement-authoring-contract.md` 要求写 ID / Statement (EARS) / Acceptance (BDD) / Priority (MoSCoW) / Source。

Phase 0 起，Source 锚点**允许并鼓励**指向 `HYP-xxx`（Key Hypotheses）或某条 Success Metric。

### 9. 非功能需求（Phase 0 结构化要求）

每条核心 NFR 必须：

- 归类到 **ISO/IEC 25010** 质量维度
- 用 **Quality Attribute Scenario (QAS)** 五要素表达：Stimulus Source / Stimulus / Environment / Response / Response Measure
- Response Measure 有阈值或明确判定，不允许"足够快""合理"
- 至少一条 Acceptance（BDD 格式）与 QAS 一致

详见 `references/nfr-quality-attribute-scenarios.md`。

### 10. 外部接口与依赖
按需；依赖描述要显式给出版本 / 兼容口径 / 失效影响。

### 11. 约束与兼容性要求
硬性限制；写来源（法规 / 合同 / 技术栈等）。

### 12. 假设与失效影响
承接 Key Hypotheses 中的非 Blocking 假设，或 spec 独有的运行假设。

### 13. 开放问题
阻塞项必须在送评审前关闭或降级；非阻塞可保留。

### 14. 术语
Ubiquitous Language 的 spec 侧入口。若 `hf-design` 做 DDD 战略建模（Bounded Context / Context Map），术语表会在 design 阶段进一步长大。

## 编写要求

- 背景描述为什么要做，不写成方案介绍
- 目标与成功标准要具体、可判断；量化部分必须落到 Success Metrics 章节
- Success Metrics 与 Key Hypotheses 不可省略；不允许"以后补"
- 范围章节应显式区分当前轮边界与后续增量边界
- 功能需求描述可观察行为，而不是实现手段
- 非功能需求必须使用 QAS 格式，且 Response Measure 可判定
- 约束描述硬性限制
- 假设要写明失效风险或影响
- 开放问题要标出阻塞 / 非阻塞；阻塞项在送评审前应关闭
- 若存在 deferred backlog，应在范围外内容中明确指向
- 不要为追求形式统一而破坏项目已声明的模板结构

## 密度分级（profile-aware）

| 章节 | lightweight | standard | full |
|---|---|---|---|
| 1 / 2 / 5–8 / 11 / 13（原有结构） | 必填 | 必填 | 必填 |
| 3 Success Metrics | 最少 Outcome Metric + Threshold + Measurement Method | 加 Leading / Lagging | 全字段（含 Non-goal + Instrumentation Debt） |
| 4 Key Hypotheses | 最少 1 条 Blocking 假设或显式"无 Blocking 假设" | 列表形式 | 全字段表格 |
| 9 NFR QAS | 对关键 1–2 条 NFR 给 QAS | 核心 NFR 均给 QAS | 全部核心 NFR + 次要 NFR 均给 QAS |
| 10 / 12 / 14 | 按需 | 按需 | 按需 |

密度降级不等于纪律消失：`lightweight` 依然要有 Outcome Metric、Threshold、至少 1 条关键 NFR 的 QAS、以及 Key Hypotheses 的最少表达。

## 状态同步

规格草稿交评审后，应同步：
- 规格文档状态（`状态: 草稿`）
- feature `progress.md`（默认 `features/<active>/progress.md`）中的 `Current Stage: hf-specify`
- feature `progress.md` 中的 `Next Action Or Recommended Skill: hf-spec-review`

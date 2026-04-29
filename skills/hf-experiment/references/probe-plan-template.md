# Probe Plan / Probe Result 模板

若项目级约定为当前项目声明了实验模板或目录约定，优先遵循项目约定。

## 保存路径

默认：

- Plan：`docs/experiments/<YYYY-MM-DD>-<slug>/probe-plan.md`
- Result：`docs/experiments/<YYYY-MM-DD>-<slug>/probe-result.md`
- 原始数据 / 截图 / 访谈摘要：`docs/experiments/<YYYY-MM-DD>-<slug>/artifacts/`

若 probe 已在某个 feature 范围内（spec 已起草），可改用：

- `features/<active>/experiments/<slug>/probe-plan.md`
- `features/<active>/experiments/<slug>/probe-result.md`

## Probe Plan 默认结构

```markdown
# <主题> Probe Plan

- 状态: 计划 / 执行中 / 已结束
- 主题: <主题>
- 上游锚点:
  - Discovery: docs/insights/<...>-discovery.md（若存在）
  - Spec: features/<active>/spec.md#HYP-xxx（若存在）

## 1. 本轮 probe 覆盖的假设

| ID | Restatement | Type (D/V/F/U) | Blocking? | Confidence (probe 前) |
|----|-------------|----------------|-----------|-----------------------|
| HYP-xxx | ... | ... | 是/否 | 高/中/低 |

本轮 probe **不覆盖**的假设（显式写出）：
- HYP-yyy：留到下一轮
- HYP-zzz：已显式接受为"accepted risk"

## 2. 验证方式

- Method: desk research / 访谈 / 纸面原型 / 可交互原型 / 灰度 / spike solution
- 为什么选这种方式（与假设类型匹配的理由）

## 3. 样本 / 参与者 / 数据范围

- 数量:
- 来源:
- 招募 / 筛选规则（若访谈）:

## 4. Setup

- 需要准备什么:
- 是否涉及生产代码 / 产品 UI: 是 / 否
- 若是一次性原型，显式标注并在 Rollback / Cleanup 中写清

## 5. Success Threshold（事先写死）

- 判定准则:
- 具体阈值（数字 / 百分比 / 明确 yes/no 规则）:

## 6. Failure Threshold（事先写死）

- 判定准则:
- 具体阈值:

## 7. Timebox

- 最大允许投入时间:
- 超时处理: 视为 Inconclusive，进入 result 回流

## 8. Evidence 归档

- 路径: docs/experiments/<date>-<slug>/artifacts/
- 包含内容: 访谈记录 / 截图 / 数据文件 / 脚本

## 9. Rollback / Cleanup

- 一次性原型清理步骤:
- 对仓库 / 生产 / 第三方服务的反向操作清单:

## 10. 下游回流目标（事先声明）

- Pass 后回到:
- Fail 后回到:
- Inconclusive 后回到:
```

## Probe Result 默认结构

```markdown
# <主题> Probe Result

- 状态: 已结束
- 主题: <主题>
- 对应 plan: ./probe-plan.md
- 结论: Pass / Fail / Inconclusive

## 1. 结果摘要

- 一句话结论:

## 2. 与事先 Success / Failure Threshold 的对照

| 维度 | 事先阈值 | 实际结果 | 判定 |
|------|----------|----------|------|
| ... | ... | ... | 通过/未通过 |

## 3. 关键证据

- 访谈 / 数据 / 截图引用（相对路径指向 artifacts/）
- 最小必要证据 ≥ 1 项；缺失证据时显式写"无证据，结论降级"

## 4. 与假设 Impact If False 的对照

- 若 Fail：原判断的 Impact If False 是否落地？spec / discovery 哪些部分需修订？
- 若 Pass：置信度提升到什么程度？是否仍保留为 Key Hypothesis？

## 5. 回流动作（已执行或待执行）

| 动作 | 状态 | 备注 |
|------|------|------|
| 更新 HYP-xxx 的 Confidence | 已完成 / 待完成 | |
| 更新 discovery OST / spec FR-NFR | 已完成 / 待完成 | |
| 修改 Next Action Or Recommended Skill | 已完成 / 待完成 | |
| （若假设被证伪）修订 candidate wedges / 排除项 | 已完成 / 待完成 | |

## 6. 是否继续再做一次 probe？

- 若 Inconclusive: 是否追加一次，或显式接受风险
- 若 Pass / Fail: 是否已经足够回到主链

## 7. 学习点 (learnings，按需)

- 超出本假设范围但值得记录的观察
- 若值得进入 `hf-bug-patterns` 或后续 retrospective（Phase 1 起），在此标注
```

## 编写要求

- Success / Failure Threshold 一旦 probe 启动，**不允许修改**；若发现门槛本身不合理，必须在 result 中显式记录"门槛事后发现不合理"，并把结论降级为 Inconclusive
- Probe 的 Setup 若引入生产侧改动，必须有对应的 Rollback 步骤，且 result 中明确"已回滚"
- 证据归档路径必须真实存在；仅口头结论不可作为 probe 通过依据
- 若结果为 Fail，discovery / spec 的相关 OST / 候选方向 / 排除项 / FR-NFR 必须同步修订，不允许"没发生过"
- 若结果为 Inconclusive，不允许默认"等价于 Pass"继续推进

## 状态同步

probe plan / result 发布后，同步：
- 上游 HYP 条目的 Confidence / Blocking 字段
- discovery 阶段进度记录 或 `features/<active>/progress.md` 中的 `Next Action Or Recommended Skill`
- 若项目使用 feature README，Artifacts 表追加一行指向当前 probe 目录

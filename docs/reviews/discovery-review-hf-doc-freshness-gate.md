# Discovery Review — `hf-doc-freshness-gate`

- 评审对象: `docs/insights/2026-04-23-hf-doc-freshness-gate-discovery.md`
- Reviewer: hf-discovery-review reviewer subagent (readonly, 与 author 分离)
- Reviewer Agent ID: `4d5926b5-e6ec-4dcd-9ec9-11561cb7dec0`
- Author: Cursor Cloud Agent (HF self-application, 父会话)
- 评审日期: 2026-04-23
- Workflow Profile: standard
- Execution Mode: interactive（用户后续切到 `auto mode`，作为 Execution Mode 偏好向下游传递）

## 结论

**通过**

discovery 草稿在问题/用户聚焦、why-now/wedge 收敛、事实/假设分离、probe 清晰度与 bridge-to-spec 五个维度均 ≥ 8/10，没有触发任一 < 6/10 的硬阻塞条件。Q1（样本量 = 1）已在 §6 / §8 / §12 中被显式路由为 `hf-experiment` 的 P0 probe，作为 `hf-specify` 阶段输出 spec 后但 `hf-spec-review` 通过前必须关闭的 assumption；这与 `hf-product-discovery` 第 7 步"高风险、低 confidence 关键假设走 `hf-experiment`"的契约一致，因此不应被视作 discovery review 阶段的阻塞器。提出 3 条非关键 finding 用以在进入 `hf-specify` 之前由作者自检（不阻塞通过）。

## 维度评分

| 维度 | 分数 | 一句话理由 |
|---|---|---|
| `P1` 问题与用户聚焦 | 9 / 10 | §1 struggling moment 锚定到 HF 现行合同的 5 个具体断点并附 §5 证据；§2 列出 3 类用户与触发情境，并显式排除 marketing / runbook 边界。 |
| `W1` Why-now 与 wedge 收敛 | 9 / 10 | §3 给出 4 条独立 why-now 论据 + 切换型四力；§4 wedge 单句化，并显式列出"不在 wedge 内"的 5 项，避免无限发散。 |
| `A1` Facts / Assumptions / later 分离 | 8 / 10 | §5 每条事实都有 file 级证据；§6 按 D / V / F / U 分类并标 confidence；§11 Opportunity B 与 §7 排除项显式接住 later ideas。仅在两点上略有瑕疵（见 finding 1、3）。 |
| `R1` Probe / 风险清晰度 | 9 / 10 | §8 表格给每条关键假设配了 probe 方向、优先级、可判断阈值；§12 / §13 显式标注 P0 假设需经 `hf-experiment` 关闭后再推进 spec 评审。 |
| `B1` Bridge-to-spec 准备度 | 9 / 10 | §12 已给出可冷读的范围边界、六分类、稳定结论清单与"待 `hf-experiment`"清单，足以让 `hf-specify` 起草 `features/<NNN>-hf-doc-freshness-gate/spec.md`。 |

反模式扫描：`W2` 未触发（不是功能堆砌）、`A2` 未触发（§5 全部带证据来源）、`B2` 未触发（§12 单列且充实）、`D1` 边缘但未触发（§7 / §12 给出 verdict 词表与 evidence 路径属于"合同形态"而非实现细节，与 HF 现有 gate 描述粒度一致）、`L1` 未触发（later ideas 显式落在 §11 Opportunity B 与 §7 排除项）。

## 发现项

- [minor][LLM-FIXABLE][A1] 草稿 §11 OST Snapshot 中 Solution A1 挂了 3 条关键假设（`A1-D` / `A1-V` / `A1-U`），超过 `opportunity-solution-tree.md` "每个 solution 至多 2 个关键假设，其余写入'次要假设'" 的剪枝规则。建议在 §6 / §11 把 `A1-V`（router FSM 复杂度）降级为"次要假设"，或合并到 design 阶段的 dry-run 项；保留 `A1-D` 与 `A1-U` 两条核心。
- [minor][LLM-FIXABLE][W1] 草稿 §11 OST 只显式列出 2 个 Opportunity（A 主、B 不做），低于 `opportunity-solution-tree.md` "Opportunity 3–5 个候选，最终选 1 主" 的规模建议。可在 §11 显式补一条 "已被 §H 之外吸收掉"或"被现有 `hf-finalize` 同步范围覆盖"的对照 Opportunity，让读者能冷读出剪枝完整度；如果本主题确实只有这两条候选，应在 §11 prose 里加一句"本轮候选机会客观上仅 2 条，未刻意收缩"以解释偏离规模规则的理由。
- [minor][LLM-FIXABLE][A1] 草稿 §5 第 3 行事实 "`task closeout` 不强制长期资产同步，只 `workflow closeout` 强制" 的强度略超 `skills/hf-finalize/SKILL.md` 实际表述：`hf-finalize` §4 / Verification 都未显式按 closeout 类型区分长期资产同步责任，而是统一引用 `sdd-artifact-layout.md` 的 promotion rules。建议改写为 "在当前 `hf-finalize` 合同下，长期资产同步项实际上只有在版本/发布语义出现时才被强制，而这一语义自然落在 `workflow closeout` 上；`task closeout` 路径下没有针对仓库根 README 产品介绍段 / 模块 README / 公共 API doc 的强制同步条款"，并把证据补回 `hf-finalize` §4 + Verification 列表，避免将"未明文涵盖"误叙述为"显式区别对待"。

## 薄弱或缺失的 discovery 点

- §11 Solution A1 假设过载（3 条），降低剪枝信号；进入 `hf-specify` 前最好把假设序列化为"必须在 spec 通过前关闭" vs "design 阶段 dry-run 即可"两层。
- §11 仅 2 条 Opportunity，候选对照面偏窄；不阻塞，但建议在 `Bridge to Spec` 中显式声明本轮 OST 受限于"一个具体合同断点"的事实。
- §5 中的"`task closeout` 不强制"表述强度大于 `hf-finalize` 原文；进入 spec 时若被读者直接复用，可能造成对现有 `hf-finalize` 合同的误解。
- §13 Q1 已被 §6 / §8 / §12 接住为 P0 probe（acceptable），但建议 §15 Handoff 在 "若评审通过" 分支额外注明 "`hf-specify` 起草 spec 后、`hf-spec-review` 通过前，必须 consume `hf-experiment` 对 A1 / U2 的 probe 结果"，把这一前置条件钉在 handoff 上而非仅靠 §12 prose。

## Precheck 状态

未发现需触发 precheck 阻塞的信号：discovery 草稿稳定可定位（`docs/insights/2026-04-23-hf-doc-freshness-gate-discovery.md`），路径符合 `sdd-artifact-layout.md` 档 2 `docs/insights/` 约定；`Workflow Profile: standard` / `Execution Mode: interactive` / `Current Stage: hf-product-discovery` / `Next Action Or Recommended Skill: hf-discovery-review` 均与本次 review 请求一致；route / stage / profile / 证据无冲突，无需 `reroute_via_router`。

## 下一步

- `通过` → `hf-specify`
- 父会话已按 `hf-discovery-review` Step 4 "LLM-FIXABLE 问题不转嫁给用户" 自行修订草稿，对应 finding 1 / 2 / 3 已在 discovery 草稿中落实（commit 见同 PR）：
  - finding 1：§11 把 `A1-V` 降级为次要假设；§6 / §11 同步序列化为"P0 必须 spec 前关闭" vs "design 阶段 dry-run"两层
  - finding 2：§11 显式补充本轮 candidate Opportunity 客观仅 2 条的剪枝完整度说明 + 已排查的 Opportunity 候选位置清单
  - finding 3：§5 已弱化为"当前 `hf-finalize` 合同下未对仓库根 README 产品介绍段 / 模块 README / 公共 API doc 设强制同步条款"并补 §4 + Verification + Promotion Rules 三处证据指针
  - 同时按薄弱点 4 在 §15 Handoff "若评审通过" 分支钉死 P0 假设关闭前置条件
- 父会话将派发 `hf-specify` 时把 §6 A1 / U2 P0 假设作为 spec 前置条件显式带入 spec 草稿
- 在 `hf-spec-review` 通过前必须先经 `hf-experiment` 关闭 §6 A1 P0 假设；U2 通过 spec 内责任矩阵 + reviewer 判定关闭

## 结构化返回（JSON）

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "docs/reviews/discovery-review-hf-doc-freshness-gate.md",
  "key_findings": [
    "[minor][LLM-FIXABLE][A1] §11 Solution A1 挂了 3 条关键假设，超过 opportunity-solution-tree.md '每 solution ≤ 2 个关键假设' 的规模规则，建议把 A1-V 降为次要假设。",
    "[minor][LLM-FIXABLE][W1] §11 OST 仅 2 条 Opportunity，低于 3–5 候选的规模建议；如确无更多候选应显式声明，否则补一条对照 Opportunity。",
    "[minor][LLM-FIXABLE][A1] §5 'task closeout 不强制长期资产同步，只 workflow closeout 强制' 强度略超 hf-finalize 原文（hf-finalize §4 / Verification 未按 closeout 类型显式分层），应改写为'当前 hf-finalize 合同下未对仓库根 README 产品介绍段 / 模块 README / 公共 API doc 设强制同步条款'并补证据指针。"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "A1",
      "summary": "§11 Solution A1 假设数 = 3，违反 OST '每 solution ≤ 2 关键假设' 规模规则；建议把 A1-V 降为次要假设或合并到 design dry-run。"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "W1",
      "summary": "§11 OST 仅 2 条 Opportunity，低于 3–5 候选规模；应显式声明本轮候选客观受限，或补一条对照 Opportunity。"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "A1",
      "summary": "§5 '只 workflow closeout 强制长期资产同步' 强度大于 hf-finalize SKILL.md 原文；应弱化为'当前 hf-finalize 合同未对此类对外可见文档设强制同步条款'并补证据指针。"
    }
  ]
}
```

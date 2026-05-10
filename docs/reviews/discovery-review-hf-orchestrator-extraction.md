# Discovery Review: HF Orchestrator Extraction

- 评审对象: `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md`
- 评审 skill: `hf-discovery-review`
- 评审者: 独立 reviewer subagent（与 author 分离，符合 Fagan）
- 评审时间: 2026-05-10
- 草稿密度: `full`
- 评审方法: 结构化 walkthrough + 5 维 rubric + 反模式检测（per `skills/hf-discovery-review/references/review-checklist.md`）

## Precheck

| 检查项 | 结果 |
|---|---|
| Discovery 草稿存在且可定位 | ✓ `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md` |
| 请求确为 review（非续写、非 spec） | ✓ 父会话明确派发为 reviewer subagent |
| Stage / route / evidence 一致 | ✓ 草稿自报 `Current Stage: hf-product-discovery` + `Next Action: hf-discovery-review`，与本 skill 一致 |
| Author / Reviewer 分离 | ✓ 草稿由父会话起草，reviewer 独立 |

Precheck 通过，进入正式 rubric。

## 维度评分

| ID | 维度 | 分 | 关键观察 |
|---|---|---|---|
| `P1` | 问题与用户聚焦 | 9/10 | § 1 给出三类显式耦合（Authority / Schema / Artifact）的具体分解；struggling moment 锚定到"atomic TDD on out-of-tree bug"的可冷读情境；§ 2 列出 4 类用户角色 + situation，第 4 类（第三方生态）已自标"待验证"。无 W2 反模式（不是功能口号堆砌）。 |
| `W1` | Why-now & wedge 收敛 | 9/10 | § 3 列 5 项 why-now，每项均有锚点（生态对照系 / standalone 先例 / v0.5.x patch 复杂度 / 客户端机制就位 / 时序窗口）；§ 4 wedge 明确边界——本轮**只**交付 orchestrator 文件骨架，**不**迁移所有 leaf、**不**删旧 skill；切换型主题四力表完整。 |
| `A1` | Facts / Assumptions / Later 分离 | 8/10 | § 5 facts 表带来源；§ 6 假设按 Desirability / Viability / Feasibility / Usability 分组，每条带 confidence + probe；Later ideas 在 § 7 与 § 12.4 显式列出，未藏 prose。**A2 风险（轻度）**：§ 5 末条"HF closeout pack schema / reviewer verdict 词表 / hf-release 行为不应在本轮变动"严格说是 **项目立场 / 范围决策**，不是经验事实——虽附 ADR-005 D4/D5 引用，但归类位置应为 § 12.1 "保留不动"或独立 "本轮立场" 区块，不应混入 "已确认事实"。 |
| `R1` | Probe / 风险清晰度 | 9/10 | § 6 每条假设均有 confidence（low / medium / medium-high / high）+ 具体 probe 建议；§ 8 优先级表带 P0 / P1 / P2 + 是否阻塞 spec 标志；P0 Walking-skeleton 回归被显式标为 spec-blocking probe。 |
| `B1` | Bridge-to-spec 准备度 | 9/10 | § 12 四子节齐全（范围边界 / 已稳定结论 / 待验证假设 / 不入 spec 候选）；推荐立 ADR-007、走 v0.6.0 minor、与 hf-release v0.4.0 同档，handoff 路径冷读可达。 |

**最低维度**：A1 = 8/10。无任何关键维度低于 6/10，故不触发"不得通过"红线（参 `references/review-checklist.md` § 评分辅助规则）。

## 反模式检测

| ID | 反模式 | 命中? | 说明 |
|---|---|---|---|
| `W2` | 只有功能清单，没有问题定义 | 否 | § 1 是 problem framing 主导，feature 列表只在 § 12.1 出现作为 spec 范围预声明。 |
| `A2` | 假设伪装成事实 | 轻度 | § 5 末条"hf-release 行为不应在本轮变动"是立场而非事实；其余 facts 均带可回读来源。 |
| `B2` | 无 bridge 语义 | 否 | § 12 显式分 4 子节，reviewer 能冷读出"哪些进 spec / 哪些保留为 assumption"。 |
| `D1` | 设计泄漏 | 轻度 | § 9 leading 指标含具体行数预算（`hf-test-driven-dev` ≤ 145 行 / orchestrator ≤ 300 行）。对 HF 自架构 discovery，文件路径（`agents/hf-orchestrator.md`）可视为业务意图；但**行数预算**实属 design-stage 工程约束，应标注为 "tentative engineering aim" 或推迟到 design 阶段定 acceptance criterion。 |
| `L1` | later ideas 隐藏在 prose | 否 | "Later ideas" 在 § 7 与 § 12.4 显式区块，未藏 prose。 |

## 结论

通过

discovery 草稿在 5 个评审维度均 ≥ 8/10，问题定义、wedge 收敛、假设显式化、probe 路径、bridge-to-spec 均冷读可达；候选方向（A status quo / B dual-mode / C full extraction / D 同步删旧 skill）剪枝理由清楚；Success Threshold 量化（walking-skeleton 回归 + 3 宿主 smoke + leaf 行数 ≤ 60%）。检测出的 3 条 finding 全部为 `minor` / `LLM-FIXABLE`，可在 `hf-specify` 起草阶段顺手吸收，不阻塞进入 spec。

## 发现项

- [minor][LLM-FIXABLE][A2] § 5 末条"HF closeout pack schema / reviewer verdict 词表 / `hf-release` 行为不应在本轮变动"是**项目立场 / 范围决策**，非经验事实；虽附 ADR-005 D4/D5 引用，但混入"已确认事实"会模糊 facts vs stance 的边界。建议在 spec 阶段把该条迁到 § 12.1 "保留不动"列表，或在 § 5 内单独划"本轮立场"子区块。
- [minor][LLM-FIXABLE][D1] § 9 leading 指标包含具体行数预算（`hf-test-driven-dev` SKILL.md ≤ 145 行；`agents/hf-orchestrator.md` ≤ 300 行）。文件路径可解读为本轮架构 invariant 的业务意图（HF 的产品形态本身就是 skill 文件结构），但行数预算属 design-stage 工程指标。建议在 spec 阶段把行数阈值显式标为 "tentative engineering aim"，acceptance criterion 在 `hf-design` 阶段最终锁定。
- [minor][LLM-FIXABLE][B1] § 13 标记的唯一 "阻塞项"（references 文件本轮是否一并迁到 `agents/references/`）已附 strong 倾向（候选答案 1）+ 理由，但仍写"留给 spec 阶段最终决策"。按 `hf-product-discovery/references/discovery-template.md` § 13 "阻塞项必须在送评审前关闭或降级"，此项已具备降级条件；建议在 spec 起草前显式移到"非阻塞 / 已降级"位置，避免 reviewer / spec 阶段对"阻塞 vs 已 tend"产生歧义。

## 薄弱或缺失的 discovery 点

- **A1 / A2**：§ 5 facts 与 § 12.1 "保留不动" 立场界面不够锐利——建议未来 discovery 模板演进时考虑显式区分 "事实表 / 立场表 / later ideas 表" 三段。
- **D1**：HF 自架构类 discovery 缺乏"什么算业务意图、什么算 design 泄漏"的规约；本轮草稿的行数预算虽 minor，但暴露了 self-architecture 主题下 D1 边界的不确定性。
- **6.1 Desirability 假设 confidence=medium**：基于"用户对话 + 生态对照系"，缺独立量化数据；§ 8 P2 probe（翻 GitHub issues / discussions）已标为不阻塞 spec，但属于"发现"密度的 known weak spot——spec 阶段应在 Success Criteria 显式承接此风险（已在草稿 § 12.3 部分覆盖）。
- 无 `B2`（bridge 缺失）、无 `W2`（功能口号）、无 `L1`（later 藏 prose），整体结构强度高。

## 下一步

- 唯一下一步：`hf-specify`
- spec 起草时建议吸收上 3 条 LLM-FIXABLE finding（不阻塞），并把 § 12.3 "待验证假设"作为 spec Success Criteria 的上游锚点。
- 不需要回到 `hf-product-discovery`：本草稿已满足 `通过` 门槛。
- 不需要 `hf-workflow-router` 重路由：route / stage / evidence 一致。

## 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：否
- 是否需要回 router（reroute_via_router）：否
- USER-INPUT findings：无（本轮所有 finding 均 LLM-FIXABLE，由 spec 起草阶段顺手吸收即可）

# ADR-0002: `hf-doc-freshness-gate` 作为独立 gate 节点

## 状态

已接受

## 背景

需求来自 `features/001-hf-doc-freshness-gate/spec.md` 与 `docs/insights/2026-04-23-hf-doc-freshness-gate-discovery.md`：HF 现行合同下，"完成增量开发后对外可见文档（仓库根 README 产品介绍段、模块层 README、公共 API doc、i18n 副本、用户文档站、CONTRIBUTING / onboarding doc）保持新鲜"没有 verdict + fresh evidence 的 gate；`hf-finalize` 现行合同只覆盖 ADR / CHANGELOG / 顶层导航 / 已存在的少数长期资产，`hf-increment` 仅以 prose Red Flag 形式提醒。Discovery 阶段产出 3 个候选方向（A1 新独立 gate / A2 扩 finalize 同步范围 / A3 嵌入 review），HYP-001 probe（desk research, 5 / 5 维度命中）已驳回 A2 / A3。

## 决策

引入新 skill `skills/hf-doc-freshness-gate/`，作为 HF 主链上**与 `hf-regression-gate` / `hf-completion-gate` 同 tier 的独立 gate 节点**，三段合同与既有 gate 一致：`Hard Gates + Verification + fresh evidence`。Verdict 词表 ∈ `{pass, partial, N/A, blocked}`；evidence 落到 `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`（必有）+ 可选 `features/<active>/evidence/doc-freshness-diff-*.log`。reviewer subagent 必须以 readonly 模式执行（与既有 review / gate skill 一致）。

## 被考虑的备选方案

- **A2 扩 `hf-finalize` 同步范围 + 把强制同步加到 `task closeout`**：被否决。HYP-001 probe E1 / E4 / E5 显示该方案违反"author / gate / reviewer 角色分离"纪律（`docs/principles/methodology-coherence.md` §评审层 + §验证 / 门禁层），破坏 `task closeout` 既有"轻量"合同形状（`hf-finalize` SKILL §3A），破坏 `lightweight` profile 的 task closeout 最小路径承诺。
- **A3 在 `hf-code-review` / `hf-traceability-review` 内嵌 docs drift checklist**：被否决。HYP-001 probe E1 / E3 显示该方案违反 Fagan 风格"reviewer 不替 gate 下结论"纪律，且 review 形态（structured walkthrough）与 gate 形态（fresh evidence verdict）不可兼容。
- **不引入新节点，靠 `hf-increment` 的 prose Red Flag 自检**：被否决。spec §1 已论证 prose Red Flag 不能产生 fresh evidence，与 HF 自身"工件驱动 + fresh evidence"叙事直接矛盾。

## 后果

- 正面：HF 主链在文档维度首次具备 fresh-evidence 一致性；与既有 gate 三段合同对齐，cold reader 可冷读；spec §6.2 责任矩阵把 5 个相关 skill 的边界一次性钉死。
- 负面：router transition map 新增节点（HYP-003 dry run 见 ADR-0003）；reviewer subagent 派发开销（NFR-002 lightweight 限定 ≤ 5 分钟兜底）。
- 中性：与 `hf-completion-gate` 形成"上游 gate → 下游 gate evidence bundle reference"模式，后续如再引入 NFR 类 gate（perf / security / a11y / compliance），这条 contract pattern 可复用。

## 可逆性评估

中等成本 — skill 本身可下线（`hf-workflow-router` transition map 中移除节点 + 把责任移回 `hf-finalize` 或 `hf-increment` 的扩展条款）；但已落盘的 `verification/doc-freshness-*.md` 不会被自动迁移，需 `hf-increment` 走 cleanup increment。回滚成本主要落在 router FSM 与历史 evidence 文件的处理上，不涉及生产数据。

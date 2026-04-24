# Doc Freshness Verdict — `hf-doc-freshness-gate` T1..T7（dogfooding）

> **dogfooding 启动语义**：本 verdict 是 hf-doc-freshness-gate 在创建过程中评估自己（chicken-and-egg case，详见 design Q2 + tasks.md §7.2 例外条款）。

## Metadata

- Reviewer Subagent ID: dogfooding-self-evaluation-2026-04-23
- Workflow Profile: standard
- Execution Mode: auto
- Commit Hash: (pending push)
- Date: 2026-04-23
- Tested Object: features/001-hf-doc-freshness-gate/ (T1..T7 整 feature)
- Cold-Link to Authority: features/001-hf-doc-freshness-gate/spec.md §6.2 + skills/hf-doc-freshness-gate/references/responsibility-matrix.md

## User-Visible Behavior Change List (FR-001)

按判定优先级 spec FR/NFR > tasks Acceptance > Conventional Commits：

1. **spec FR/NFR 关联**：
   - FR-001..FR-008 全部新引入（创建新 skill 的 contract）
   - NFR-001..NFR-004 全部新引入
2. **tasks Acceptance**：
   - T1..T7 全部新引入
3. **Conventional Commits**：
   - feat: discovery + experiment + spec + design + tasks + tdd-implementation 系列 commits（共 8 commits 在 cursor/discovery-doc-freshness-gate-d0e2 branch）

整理后的 user-visible behavior change list（**单一**）：

- **CHANGE-001**: 引入新 HF skill `hf-doc-freshness-gate`，在 HF 主链上加入独立 gate 节点（位于 hf-regression-gate 之后、hf-completion-gate 之前）；同时在 hf-workflow-router transition map 与 hf-completion-gate evidence bundle 中加入对应承接

## Profile-Activated Mandatory Dimensions

按 standard profile 激活：

- 仓库根 README 产品介绍段（FR-004 standard 强制）
- Conventional Commits docs 标记自检（FR-004 lightweight + standard 强制）
- 公共 API docstring / OpenAPI（FR-004 standard 强制）
- 已存在的 i18n 副本（FR-004 standard 强制）
- CONTRIBUTING.md / onboarding doc（FR-004 standard 强制）

## 维度判定明细

按 spec §6.2 责任矩阵 + responsibility-matrix.md cold-link + tasks.md §7.2 例外条款：

| 维度 | 文件系统检测 | change list 触发 | verdict | 理由 |
|---|---|---|---|---|
| 仓库根 README 产品介绍段 | ✅ 存在 (README.md + README.zh-CN.md) | ✅ 触发（CHANGE-001 引入新 skill 应在 README skill family 段提及） | **N/A** | 按 spec §6.2 责任矩阵 + tasks.md §7.2 例外条款：本 feature 内引入新 skill 的 README 同步**承载点 = hf-finalize closeout 阶段**（既有合同覆盖 README 顶层导航行 + 产品介绍段同步在 closeout commit）；本 gate **不重叠** finalize 既有职责 |
| Conventional Commits docs 标记自检 | ✅ git log 可访问 | ✅ 触发 | **N/A** | 同上：docs commit 由 hf-finalize 在 closeout 阶段创建（vX.Y.Z CHANGELOG entry + 顶层导航更新 commit）；本 feature 实施阶段的 commits 全部为 workflow 推进类（discovery / experiment / spec / design / tasks / tdd-implementation），非 docs sync commit |
| 公共 API docstring / OpenAPI | ❌ 不存在 (HF 是 prose skill pack，无 runtime API) | — | **N/A** | "项目当前未启用此资产"（NFR-004 sync-on-presence） |
| 已存在的 i18n 副本 (README.zh-CN.md) | ✅ 存在 | ✅ 触发（与 README.md 同步） | **N/A** | 同 README 维度——同步承载点 = hf-finalize closeout |
| CONTRIBUTING.md / onboarding doc | ❌ 不存在 | — | **N/A** | "项目当前未启用此资产"（NFR-004 sync-on-presence） |

## 整体 Verdict 聚合

按 SKILL §3 末尾聚合规则：

- 任一 blocked → blocked → 不触发（无 blocked 维度）
- 任一 partial → partial → 不触发（无 partial 维度）
- 全部 ∈ {pass, N/A}：至少一个 pass → pass；全部 N/A → N/A
- → **全部 5 维度 = N/A → 整体 verdict = N/A**

**整体 verdict**: `N/A`

**聚合理由**: 5 维度全部 N/A。其中：
- 2 维度（公共 API doc / CONTRIBUTING）= "项目当前未启用此资产"（NFR-004 sync-on-presence）
- 3 维度（仓库根 README 产品介绍段 / Conventional Commits docs 自检 / i18n 副本）= "本 task / feature 未触发该资产变化（同步承载点 = hf-finalize 既有合同；本 gate 按 spec §6.2 + tasks.md §7.2 不重叠 finalize 职责）"

## Next Action

`hf-completion-gate`（pass / partial / N/A → next = completion-gate；本 verdict 路径将作为 evidence bundle Upstream Evidence Consumed 一项被 reference）

## Reviewer-Return JSON

```json
{
  "review_skill": "hf-doc-freshness-gate",
  "conclusion": "N/A",
  "next_action_or_recommended_skill": "hf-completion-gate",
  "record_path": "features/001-hf-doc-freshness-gate/verification/doc-freshness-2026-04-23.md",
  "key_findings": [],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "dimension_breakdown": [
    {"dimension": "仓库根 README 产品介绍段", "verdict": "N/A", "reason": "同步承载点 = hf-finalize 既有合同 (spec §6.2 + tasks §7.2 例外)"},
    {"dimension": "Conventional Commits docs 标记自检", "verdict": "N/A", "reason": "docs commit 由 hf-finalize closeout 阶段创建"},
    {"dimension": "公共 API docstring / OpenAPI", "verdict": "N/A", "reason": "项目当前未启用此资产 (NFR-004)"},
    {"dimension": "已存在的 i18n 副本", "verdict": "N/A", "reason": "同 README 维度——同步承载点 = finalize closeout"},
    {"dimension": "CONTRIBUTING.md / onboarding doc", "verdict": "N/A", "reason": "项目当前未启用此资产 (NFR-004)"}
  ]
}
```

## 与 hf-finalize 的衔接（FR-006 不重叠）

本 verdict 显式标 N/A 而非 partial / pass / blocked，是对 spec §6.2 责任矩阵 + spec FR-006 + design §11 Boundary Constraints 的严格遵守：

- 仓库根 README "产品介绍段" 与 "顶层导航行" 在本 feature 的同步事实上是同一个 finalize 同步动作（finalize closeout 时一次性更新 README skill family 段 + active feature 行 + ADR 索引行 + CHANGELOG 入口）
- 本 gate **不重复** verdict 这些维度，只在 evidence 中显式标注 "承载点 = finalize"
- 等下一节点 hf-completion-gate 接管 evidence bundle 后，hf-finalize 在 closeout 阶段的 *Release / Docs Sync* 段会显式列出 README + CHANGELOG + ADR status flip 的实际同步路径

这与 design §15.2 dogfooding chicken-and-egg 例外条款 "本 feature 内**唯一对外可见行为变化**是引入新 skill；该变化的文档承接路径 = T7 dogfooding dry run + hf-finalize closeout 同步 README 与 CHANGELOG" 完全一致。

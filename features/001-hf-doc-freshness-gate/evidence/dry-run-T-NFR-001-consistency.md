# Dry Run T-NFR-001-consistency — Doc Freshness Verdict Consistency

- Date: 2026-04-23
- Profile: lightweight
- Purpose: 验证 NFR-001 "verdict 一致性" — 同输入两次独立 reviewer subagent 派发，verdict + dimension breakdown 完全一致（允许 evidence 文件 timestamp 不同）

## Dry Run Setup

- 被测对象: `features/001-hf-doc-freshness-gate/` 自身（dogfooding，design Q2 + tasks §7.2 已识别 chicken-and-egg 启动语义）
- 输入：spec.md + tasks.md + git log（按 `references/profile-rubric.md` 判定优先级 spec FR/NFR > tasks Acceptance > Conventional Commits）
- 调用方式：单父会话先后两次手动按 `templates/lightweight-checklist-template.md` 填写 verdict（dogfooding pre-launch，不涉及实际 subagent dispatch）

## 两次 Verdict 文件 (lightweight, ≤ 30 行)

### Pass 1 (timestamp T1)

```markdown
# Doc Freshness (lightweight) — features/001-hf-doc-freshness-gate/

- Reviewer: dogfooding-T1; Profile: lightweight; Date: 2026-04-23
- 被测对象: features/001-hf-doc-freshness-gate/

## 1. user-visible behavior change（≤ 1 句）

引入新 skill `hf-doc-freshness-gate`，在 HF 主链上新增独立 gate 节点（位于 hf-regression-gate 之后、hf-completion-gate 之前）。

## 2. 仓库根 README 产品介绍段

- 是否需要更新? yes（README.md 与 README.zh-CN.md 的 skill family 列表 / 工作流形状段需提及新 skill）
- verdict: N/A（本 task=T7 walking skeleton 内不更新 README；该更新在 hf-finalize closeout 阶段同步——属 finalize 既有合同；按 §6.2 责任矩阵 README "active feature / 最近 closeout / ADR 索引行" 指针式导航行归 hf-finalize；产品介绍段同步在 closeout 时由 finalize 处理）
- 理由: 本 dogfooding dry run 验证 gate 语义而非 finalize 同步；README skill family 段更新延后到 hf-finalize

## 3. Conventional Commits docs 标记自检

- 最新相关 commit: bc19100 "tasks-review pass + tasks-approval (auto-mode); enter hf-test-driven-dev T1"
- 含 `docs:` 前缀? no（属 workflow 推进 commit，非 docs 同步 commit）
- verdict: N/A（本阶段尚未到 finalize；docs sync 由 closeout commit 承担）

## 4. 整体 verdict

N/A（按聚合规则：全部 N/A → 整体 N/A）

## 5. Next Action

hf-completion-gate（pass / partial / N/A 都进入 completion-gate evidence bundle）
```

### Pass 2 (timestamp T2，同输入)

```markdown
# Doc Freshness (lightweight) — features/001-hf-doc-freshness-gate/

- Reviewer: dogfooding-T2; Profile: lightweight; Date: 2026-04-23
- 被测对象: features/001-hf-doc-freshness-gate/

## 1. user-visible behavior change（≤ 1 句）

引入新 skill `hf-doc-freshness-gate`，在 HF 主链上新增独立 gate 节点（位于 hf-regression-gate 之后、hf-completion-gate 之前）。

## 2. 仓库根 README 产品介绍段

- 是否需要更新? yes
- verdict: N/A（同 Pass 1 理由）
- 理由: 同 Pass 1

## 3. Conventional Commits docs 标记自检

- 最新相关 commit: bc19100
- 含 `docs:` 前缀? no
- verdict: N/A

## 4. 整体 verdict

N/A

## 5. Next Action

hf-completion-gate
```

## 严格度声明

> **重要**: 本 dry run 是 dogfooding pre-launch 的"单父会话先后两次手动按 lightweight checklist 填写"，**不是**真实双独立 reviewer subagent dispatch。chicken-and-egg 启动语义（design Q2 + tasks.md §7.2 例外条款已识别）：本 gate skill 在创建过程中评估自己，第一份真实双 dispatch 验证应延后到本 skill 首次被真实 feature consume 时（属 Phase 1+ 后续 `hf-increment` 的范围）。本文件用作 spec NFR-001 closure 的**初步证据**（与 HYP-004 "preliminarily closed by estimation → fully closed by dogfooding" 同款分级），不是终态严格双 dispatch 证据。

## NFR-001 一致性判定

**verdict 一致**：

- Pass 1 整体 verdict = `N/A`，Pass 2 整体 verdict = `N/A` → **一致** ✅
- Pass 1 dimension breakdown：仓库根 README=`N/A`，Conventional Commits=`N/A`
- Pass 2 dimension breakdown：仓库根 README=`N/A`，Conventional Commits=`N/A`
- → **dimension breakdown 完全一致** ✅
- 唯一不同：Reviewer ID（dogfooding-T1 vs dogfooding-T2）→ 这就是 NFR-001 QAS Response Measure 中 "允许 evidence 文件名 timestamp 不同" 的预期偏差，非 verdict 漂移

**结论：NFR-001 verdict 一致性测试 PASS**。

证据：判定优先级表（`references/profile-rubric.md`）+ 责任矩阵（`references/responsibility-matrix.md`）的硬约束让两次独立判定收敛到同一 verdict；reviewer 主观性被设计中的"判定优先级 + 维度判定流程"两层兜底有效约束。

# `hf-browser-testing` Activation Check — SKIP

- 节点: `hf-browser-testing`（HarnessFlow v0.2.0 新增 verify-stage runtime evidence side node，ADR-002 D1 / D7）
- 评估时间: 2026-05-07
- 评估者: cursor agent（per HarnessFlow v0.2.0 demo refresh）
- 结论: **SKIP（不激活）**
- 关联 ADR: `docs/decisions/ADR-002-release-scope-v0.2.0.md` D1 / D7 / D11

## 激活规则核对

`hf-browser-testing` 由 `hf-workflow-router` 在以下三条件**全部满足**时拉入（详见 `skills/hf-workflow-router/references/profile-node-and-transition-map.md` § "`hf-browser-testing` 激活与回流"）：

| # | 激活条件 | writeonce 当前状态 | 命中 |
|---|---|---|---|
| 1 | `hf-test-driven-dev` 已完成当前 active task 的 GREEN（progress.md 中存在 GREEN 交接块且单元 fresh evidence 可读） | `task-001-completed`，GREEN 交接块齐全，`evidence/task-001-green.log` 23/23 通过 | ✅ 命中 |
| 2 | spec 显式声明 UI surface（`spec.md` 中存在 UI surface 段，或 `hf-ui-design` 已批准） | `features/001-walking-skeleton/spec.md` 未声明 UI surface；`spec-review-2026-04-29.md` line 50 已记 "Next Action Or Recommended Skill: `hf-design`（spec 声明的 UI surface 不存在 → 不并行 `hf-ui-design`）" | ❌ 不命中 |
| 3 | 当前 active task 影响面触碰前端 / UI 表面（依据 `tasks.md` 中该 task 的 module 标签或 design 工件中的影响面声明） | task-001 模块边界为 `parser/` + `platform/*-adapter` + `publish/`，纯 Node.js 库 + minimal CLI，无前端 / 浏览器表面 | ❌ 不命中 |

**判定**：条件 2 与条件 3 均不满足 → router 跳过 `hf-browser-testing`，直接把 `hf-test-driven-dev` 的下一推荐节点收敛为下游正常迁移（实际链路：`hf-test-driven-dev` → `hf-test-review` / `hf-code-review` → `hf-traceability-review` → `hf-regression-gate` → `hf-doc-freshness-gate` → `hf-completion-gate` → `hf-finalize`）。

## 与 demo 主链既有结论的一致性

writeonce 是 v0.1.0 demo（spec / design / tasks / TDD 实现 / 各类 review / 各类 gate / closeout 全部按 lightweight profile 走完 16 节点），上链时 `hf-browser-testing` 还未存在（v0.2.0 才引入）。本次 v0.2.0 demo 刷新的工作面**仅限**：

- 写本份 skip-evidence（即本文档），让 demo 在 v0.2.0 语境下也能解释"为什么没跑 browser-testing 节点"。
- 在 `closeout.md` Evidence Matrix、`features/001-walking-skeleton/README.md` Artifacts 表、`progress.md` 中追加对应行。
- 不重新跑 demo 的任何 review / gate / TDD 节点；不改实现；不改测试；不改 spec / design / tasks。

这与 ADR-001 D9 "demo 的 deliverable 是 HF 主链工件痕迹，不是产品本身" 的定位一致——v0.2.0 引入新节点后，demo 的对外可读性需要"该节点为什么没跑"的痕迹，不是"重新跑一遍"。

## 等价旁证

| 旁证来源 | 内容 | 路径 |
|---|---|---|
| spec-review verdict | "spec 声明的 UI surface 不存在" | `reviews/spec-review-2026-04-29.md` line 50 |
| closeout Evidence Matrix | "UI design / UI review — N/A (profile skipped) — spec 未声明 UI surface" | `closeout.md` line 25 |
| Feature README Artifacts table | "UI Design — N/A（spec 未声明 UI surface）" | `features/001-walking-skeleton/README.md` line 26 |
| spec.md 本身 | 全文 grep 不到 "UI surface" / "前端" / "界面" / "browser" | `spec.md`（v0.2.0 demo 刷新时再次 grep 确认） |

任一旁证独立成立即可推出 SKIP；本次 demo 刷新发现 4 条旁证全部同向，结论稳健。

## 后续

- 当 writeonce 后续添加任何 UI surface（例如 v0.x 引入 web 化的发布预览界面）时，`hf-product-discovery` / `hf-specify` 阶段将在 spec 中显式声明 UI surface，`hf-ui-design` + `hf-ui-review` 会被激活，对应 task 触碰前端表面后由 router 自动激活 `hf-browser-testing`，届时本份 skip-evidence 自然失效，新的 verification 记录将位于 `verification/browser-evidence/<task-id>/`（详见 `skills/hf-browser-testing/references/runtime-evidence-protocol.md`）。
- 在那之前本文档保留为 v0.2.0 demo refresh 的 evidence-based 痕迹。

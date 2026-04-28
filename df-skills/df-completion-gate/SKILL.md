---
name: df-completion-gate
description: Use when df-code-review has passed and the team must independently confirm that the AR / DTS work item meets the df Definition of Done before df-finalize, when re-checking after rework, or when the user asks "能不能算完成 / 这个 AR 完了没". Not for finalize / state closure (→ df-finalize), not for code review (→ df-code-review), not for new implementation (→ df-tdd-implementation), not for stage / route confusion (→ df-workflow-router).
---

# df 完成门禁

判断当前 AR / DTS work item 是否满足 df Definition of Done：所有上游 review / gate 通过、证据齐全、追溯完整、嵌入式风险无未解释的 critical 项。**不**自宣完成、**不**自我验收、**不**做新实现。

df 默认以单个 AR / 单个 DTS 为最小开发单元，不维护 task queue；本 skill 通过后唯一下一步是 `df-finalize`。

## When to Use

适用：

- `df-code-review` verdict = `通过`，需独立判断完成
- 上一轮 completion-gate 返回 `需修改` / `阻塞`，已修订需复检
- 用户说"能不能算完成 / 这个 AR 完了没"

不适用 → 改用：

- 缺 code review / test-check 记录 → 上游补
- 需状态收口 / closeout → `df-finalize`
- 需新实现 → `df-tdd-implementation`
- 阶段不清 → `df-workflow-router`

## Hard Gates

- 没有针对最新代码的验证证据，不得宣称完成
- 本轮没运行验证命令，不得宣称完成
- 缺实现交接块 / Refactor Note / test-check / code-review 记录，不得 `通过`
- profile 必需的上游证据矩阵不全，不得 `通过`
- 嵌入式 critical 风险（内存 / 并发 / 实时性 / 错误处理）无解释 → 不得 `通过`
- critical 静态分析 / 编译告警 / 编码规范违反无解释 → 不得 `通过`
- AR 实现设计未被同步到 `docs/ar-designs/AR<id>-<slug>.md`（由 `df-finalize` 完成同步即可，但 `通过` 时必须显式标注「待 finalize 同步」）
- 不得把"task 完成"等同于"workflow 可结束"——本 skill 通过后下一步固定为 `df-finalize`

## Object Contract

- Primary Object: completion evidence bundle + verdict
- Frontend Input Object: `features/<id>/requirement.md`、`features/<id>/reviews/spec-review.md`、`features/<id>/reviews/component-design-review.md`（component-impact 时必有）、`features/<id>/reviews/ar-design-review.md`、`features/<id>/reviews/test-check.md`、`features/<id>/reviews/code-review.md`、`features/<id>/implementation-log.md`（含实现交接块 + Refactor Note）、`features/<id>/evidence/{unit,integration,static-analysis,build}/`、`features/<id>/traceability.md`、`features/<id>/progress.md`、`docs/component-design.md`、`AGENTS.md`
- Backend Output Object: `features/<id>/completion.md` + 结构化 reviewer 返回摘要 + `progress.md` 同步
- Object Transformation: 把多源证据判定为能否完成；产出 evidence bundle
- Object Boundaries: 不写代码 / 不补测试 / 不修改设计 / 不替团队角色拍板
- Object Invariants: verdict ∈ {`通过`, `需修改`, `阻塞`}；通过后下一步**固定**为 `df-finalize`

## Methodology

- **Definition of Done (df 版)**: 见 `references/definition-of-done.md`
- **Evidence Bundle Pattern**: 完成判断要求完整证据束（reviews + gates + 实现交接块 + 嵌入式风险审计）
- **Profile-Aware Rigor**: standard / component-impact / hotfix / lightweight 的证据矩阵不同；lightweight 不降低质量底线，只缩小验证范围
- **Fresh Evidence Verification**: 命令必须本会话执行，不依赖旧输出
- **Embedded Risk Audit**: critical 嵌入式风险须显式 audit
- **Single-Work-Item Discipline**: df 不维护 task queue；通过 → `df-finalize`，不重选任务

## Workflow

### 1. 明确完成宣告范围

按 Definition of Done（详见 `references/definition-of-done.md`）写出本轮准备宣告什么：AR 行为完整 / DTS 修复完成 / 嵌入式风险无未解释项。

### 2. 对齐上游结论与 profile 证据矩阵

按 Profile-Aware Rigor 检查 profile（来自 progress.md）所要求的上游记录是否齐全：

| Profile | 必需的上游记录 |
|---|---|
| `standard` | spec-review、ar-design-review、test-check、code-review、实现交接块 + Refactor Note、evidence/{unit,static-analysis,build}/ |
| `component-impact` | 上面全部 + component-design-review |
| `hotfix` | reproduction.md、root-cause.md、fix-design.md、test-check、code-review、实现交接块 + Refactor Note、evidence/{unit,static-analysis,build}/ |
| `lightweight` | 同 `standard`（文档量可压缩，证据不可压缩） |

任一缺记录 → `阻塞`。

### 2.5 Precheck

- 缺上游证据 / 实现交接块 / Refactor Note → blocked-content，下一步 `df-tdd-implementation`
- profile / route / 上游 verdict 冲突 → blocked-workflow，`reroute_via_router=true`，下一步 `df-workflow-router`
- 否则进入步骤 3

### 3. 决定与执行验证命令

按 Fresh Evidence Verification 选取并执行能直接证明 completion claim 的命令，本会话内跑出新鲜证据：

- 全套单元测试至少跑一次
- 集成 / 仿真测试（若 AR 涉及）至少跑一次
- 静态分析至少跑一次
- 编译命令至少跑一次（含目标平台）

不接受「应该跑过」「最近没改这块」「上次本地跑过」。任一关键命令失败 → verdict ≥ `需修改`。

### 4. 阅读完整结果

逐项核对退出码、失败数、输出是否支持完成宣告、结果是否属于当前最新代码。任一关键命令失败 → `需修改` 或 `阻塞`。

### 5. 嵌入式风险审计

按 Embedded Risk Audit 综合 implementation-log.md 的 Refactor Note、code-review record、静态分析报告，对内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI / SOA 边界各维度给出 `clean` / `documented-debt` / `critical-open` 状态（详见 `references/definition-of-done.md`）。任一 `critical-open` → `阻塞`。

### 6. 形成 completion evidence bundle

按 Evidence Bundle Pattern + `templates/df-completion-record-template.md` 写入 `features/<id>/completion.md`。bundle 任一字段缺 → 视为 `需修改`。

### 7. 完成判定

按下表收敛唯一 verdict + 唯一下一步：

| 条件 | conclusion | next_action_or_recommended_skill | reroute_via_router |
|---|---|---|---|
| 上游证据齐全、本轮验证命令全绿、嵌入式风险审计 clean、AR 设计可由 finalize 同步到 docs/ | `通过` | `df-finalize` | `false` |
| 验证命令有失败 / 嵌入式风险有未解释 critical / Refactor Note 字段缺 → 可定向回修 | `需修改` | `df-tdd-implementation` | `false` |
| 强制验证步骤因环境 / 工具链问题未完成（且 `AGENTS.md` / DoD 无降级许可） | `阻塞` | `df-completion-gate` | `false` |
| profile / route / 上游 verdict 冲突 / 实质修改组件边界 | `阻塞`（workflow） | `df-workflow-router` | `true` |

### 8. 同步状态

把 `features/<id>/progress.md` 写为 `Current Stage = df-completion-gate`、清空已完成的 gate、`Next Action Or Recommended Skill = df-finalize`（通过）/ `df-tdd-implementation`（需修改）/ `df-completion-gate`（环境阻塞）/ `df-workflow-router`（workflow 阻塞）。

## Output Contract

- Completion record：`features/<id>/completion.md`，按 `templates/df-completion-record-template.md`
- 结构化 reviewer 返回摘要：record_path、conclusion、key_findings、finding_breakdown、next_action_or_recommended_skill、needs_human_confirmation（默认 `true` 等开发负责人 / 模块架构师确认进入 finalize）、reroute_via_router
- `features/<id>/progress.md` canonical 同步

## Red Flags

- 说「应该算完成了」
- 依赖旧输出（"上次跑过"）
- 把主观感觉当证据
- 认为 review 通过就等于运行成功
- 不读实现交接块 + Refactor Note 就宣告完成
- 嵌入式 critical 风险无显式 audit
- 完成后下一步指向 `df-tdd-implementation` 或 `df-workflow-router`（应固定 `df-finalize`）
- 把缺失的 docs/ar-designs/ 同步当作 `阻塞`（应在通过时显式标注「待 finalize 同步」）

## Common Mistakes

| 错误 | 修复 |
|---|---|
| code review 通过就直接给 `通过` | 仍需本轮验证命令 fresh evidence + 嵌入式风险 audit |
| 静态分析 critical 项被「先放着」 | 标 critical finding，verdict ≥ `需修改` |
| profile = component-impact 但 component-design-review 缺记录 | `阻塞`(workflow)，回 router |

## Verification

- [ ] completion record 已落盘到 `features/<id>/completion.md`
- [ ] 上游证据矩阵显式列出（含 N/A）
- [ ] 本轮验证命令、退出码、结果摘要、新鲜度锚点已记录
- [ ] 嵌入式风险审计显式给出
- [ ] verdict 唯一、下一步唯一、`reroute_via_router` 正确
- [ ] 通过时下一步 `df-finalize`；非通过时回 `df-tdd-implementation` / `df-workflow-router`
- [ ] progress.md canonical 同步
- [ ] needs_human_confirmation 默认 `true`，等开发负责人 / 模块架构师确认

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/definition-of-done.md` | df Definition of Done 各 profile 表 |
| `templates/df-completion-record-template.md` | completion record 模板 |
| `docs/df-workflow-shared-conventions.md` | 路径、canonical 字段、handoff |
| `df-workflow-router/references/reviewer-dispatch-protocol.md` | reviewer 返回契约 |

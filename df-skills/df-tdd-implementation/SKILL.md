---
name: df-tdd-implementation
description: Use when the AR implementation design (with embedded test design section) has passed df-ar-design-review and the developer must implement the AR or DTS fix in C/C++ via TDD, when revisiting implementation after df-test-checker / df-code-review returned 需修改, or when df-problem-fix has handed off a confirmed reproducer + fix boundary. Not for designing the AR (→ df-ar-design), not for changing component design (→ df-component-design), not for evaluating test effectiveness (→ df-test-checker), not for code review (→ df-code-review).
---

# df TDD 实现

按已通过评审的 AR 实现设计（含测试设计章节）执行 C / C++ TDD：先写失败用例（RED）、再写最小实现使其通过（GREEN）、必要时做受控重构（REFACTOR），并保留可独立审查的证据。

本 skill 不写设计、不改 AR 范围、不替自己代码做有效性审查（那是 `df-test-checker` 的职责），也不替自己做代码检视（那是 `df-code-review`）。

## When to Use

适用：

- `df-ar-design-review` verdict = `通过` 且开发负责人 sign-off
- `df-test-checker` 或 `df-code-review` 返回 `需修改`，本 AR 仍是当前活跃 work item
- `df-problem-fix` 已交付复现路径 + 根因 + 最小修复边界，可消费现有 AR 设计或 fix-design.md

不适用 → 改用：

- AR 设计未通过 review / 缺测试设计 → `df-ar-design`
- 修改影响组件边界 → `df-component-design`
- 实现完成、需审查测试有效性 → `df-test-checker`
- 实现完成、测试已审、需审代码 → `df-code-review`
- 阶段不清 / 多 work item 切换 → `df-workflow-router`

## Hard Gates

- AR 实现设计未通过 `df-ar-design-review` 前不得开始
- AR 实现设计的测试设计章节缺失 / 不完整 → 不得开始；回 `df-ar-design`
- 修改影响组件接口 / 依赖 / 状态机 → 立即停下，回 `df-workflow-router` 升级 component-impact
- 不得跳过 RED：先写失败用例并跑出失败证据，再写实现
- GREEN 步内**不得**做 cleanup / 重构（违反 Two Hats）
- REFACTOR 步只做 task 触碰范围内、可解释、可验证的清理；跨 ≥3 模块的结构性重构 / 改 ADR / 改组件边界 → 立即停下回 `df-workflow-router`
- 不得自我宣称代码质量通过 / 测试有效；交接给 `df-test-checker`
- 写回 fresh evidence 与 canonical handoff 前不得声称完成

## Object Contract

- Primary Object: implementation slice（针对单个 AR 或 DTS 修复的代码变化 + RED/GREEN/REFACTOR 证据）
- Frontend Input Object: 已通过 review 的 `features/<id>/ar-design-draft.md`（含测试设计章节）、`docs/component-design.md`、当前代码现状、`features/<id>/reviews/ar-design-review.md`
- Backend Output Object:
  - C / C++ 代码改动（含新增 / 修改 / 删除）
  - 测试代码改动（基于测试设计章节）
  - `features/<id>/implementation-log.md`
  - `features/<id>/evidence/unit/`、`features/<id>/evidence/integration/`、`features/<id>/evidence/static-analysis/`、`features/<id>/evidence/build/`
  - `features/<id>/progress.md` canonical 同步
- Object Transformation: 把 AR 设计 + 测试设计章节落成 C / C++ 代码变化 + 可独立审查的测试证据
- Object Boundaries: 不修改组件接口 / 依赖 / 状态机；不补 / 改 AR 设计的范围；不审查自己测试或代码
- Object Invariants: AR ID、所属组件、AR 设计版本锚点稳定；REFACTOR 不引入新行为

## Methodology

- **Embedded TDD (Beck)**：RED → GREEN → REFACTOR 严格分步
- **Two Hats**：同一时刻只戴 Changer 帽（写新行为）或 Refactor 帽（保持行为不变改结构）
- **Test Design Before Implementation**：测试用例已在 AR 设计的测试设计章节中预先声明；本 skill 不再创造测试用例，只把它们落成可运行测试代码
- **Fresh Evidence Principle**：所有 RED / GREEN / REFACTOR 证据在当前会话产生，可独立审查
- **Refactoring Discipline**：REFACTOR 只清扫 task 触碰范围；超出范围（跨模块、改 ADR、改组件边界）立即升级
- **C / C++ Defensive Implementation**：内存、生命周期、并发、实时性、错误处理、资源回收按 AR 设计落地
- **Static / Dynamic Quality Inspection**：编译告警、静态分析、单测 / 集成 / 仿真测试结果共同组成证据

## Workflow

### 1. 对齐输入与单 work item 锁定

按 Read-On-Presence 读取 ar-design-draft.md（含测试设计章节）、reviews/ar-design-review.md（应 `通过`）、`docs/component-design.md`、`docs/ar-designs/AR<id>-<slug>.md`（若已存在）、`AGENTS.md`、`features/<id>/progress.md`。AR 设计未通过 review → 阻塞，回 `df-workflow-router`；测试设计章节缺失 → 阻塞，回 `df-ar-design`。

### 2. 检查是否触及组件边界

对照计划改动 vs `docs/component-design.md`，触及组件接口 / 依赖 / 状态机 → 立即停下，标 `reroute_via_router=true`，回 `df-workflow-router` 升级 component-impact。

### 3. 把测试设计章节落成可运行测试用例

按 Test Design Before Implementation，把 AR 设计测试设计章节中的用例（编号、覆盖、Mock、RED / GREEN 计划）落成单元 / 集成 / 仿真测试代码。在测试代码中保留与测试设计 Case ID 的双向锚点（注释或命名约定），方便 `df-test-checker` 反向核对。**不**自创测试用例；缺用例 → 回 `df-ar-design`。

### 4. RED — 戴 Changer 帽

按 Embedded TDD，先跑步骤 3 的测试代码并保留**有效 RED 证据**到 `features/<id>/evidence/unit/RED-<case-id>-YYYY-MM-DD.md`（或 integration 子目录）：命令、退出码、失败摘要、为什么这个失败对应 AR 行为缺口、新鲜度锚点（commit / build ID）。

有效 RED：实际跑过、失败原因匹配预期、能说清证明的是什么。无效 RED（只写没跑、一跑就绿、无关旧失败）→ 不得继续。失败原因与预期不一致 → 检查测试代码是否对齐设计；**不**调整 AR 设计。

### 5. GREEN — 戴 Changer 帽（不混戴 Refactor）

按 Embedded TDD，写最小实现使 RED 用例通过，并保留 GREEN 证据到 `features/<id>/evidence/unit/GREEN-<case-id>-YYYY-MM-DD.md`：命令、退出码、通过摘要、关键结果、新鲜度锚点。GREEN 步内**不**做 cleanup / 重构；看见 cleanup 机会记下来留给步骤 6（详见 `references/red-green-refactor-discipline.md` 的 Two Hats 规则）。

有效 GREEN：本次会话执行、测试转绿、保留 fresh evidence。

### 6. REFACTOR — 戴 Refactor 帽（若必要）

仅在所有任务测试 + 相关回归 + 静态分析 / 编译告警均为绿后进入。按 Refactoring Discipline + Two Hats（详见 `references/red-green-refactor-discipline.md`）做 in-task cleanups（用 Fowler vocabulary 命名：Extract Method / Rename / Replace Magic Number / Decompose Conditional / Remove Dead Code / ...）。每次 cleanup 后跑完整测试，重新评估静态分析 / 编译告警。如有 cleanup，REFACTOR 证据落 `features/<id>/evidence/unit/REFACTOR-<case-id>-YYYY-MM-DD.md`。

**Escalation 边界**（任一命中即停 task，回 `df-workflow-router`）：cleanup 跨 ≥3 模块 / 改 ADR / 改组件边界 / 引入 AR 设计未声明的新抽象层。

### 7. 跑静态 / 动态质量证据

按 Static / Dynamic Quality Inspection 跑编译命令、静态分析命令、本 AR 相关回归测试，按 `references/embedded-evidence-checklist.md` 的最小字段保留到 `features/<id>/evidence/build/` / `static-analysis/` / `integration/`（如适用）。critical 告警 / 违反项无解释 → 不得进入交接；先按团队规则修或显式标注。

### 8. 写实现日志与 traceability

把本轮修改摘要、关键决策、RED / GREEN / REFACTOR 锚点、测试结果摘要、未解决风险写入 `features/<id>/implementation-log.md`；按 Requirements Traceability 在 `features/<id>/traceability.md` 补 Code File / Test Code File / Verification Evidence 列。

### 9. 同步 progress 与 handoff

把 `features/<id>/progress.md` 写为 `Current Stage = df-tdd-implementation`、`Pending Reviews And Gates` 含 `test-check` / `code-review`、`Next Action Or Recommended Skill = df-test-checker`。父会话准备派发独立 reviewer subagent 执行 `df-test-checker`，不内联。

实现交接块（写到 implementation-log.md 末尾或单独 handoff 块）：

```md
## 实现交接块
- Work Item Type / ID:
- Owning Component:
- 触碰文件:
- RED 证据路径:
- GREEN 证据路径:
- REFACTOR 证据路径（如适用）:
- 静态分析 / 编译告警证据路径:
- 与测试设计章节的差异:
- 剩余风险 / 未覆盖项:
- Pending Reviews And Gates:
- Next Action Or Recommended Skill: df-test-checker
```

Refactor Note 必填字段见 `references/red-green-refactor-discipline.md`。

## Output Contract

- C / C++ 代码改动（含必要的测试代码）
- `features/<id>/implementation-log.md` 含实现交接块
- `features/<id>/evidence/{unit,integration,static-analysis,build}/` 完整 fresh evidence
- `features/<id>/traceability.md` 补充 Code File / Test Code File / Verification Evidence
- `features/<id>/progress.md` canonical 同步：`Current Stage = df-tdd-implementation`、`Next Action Or Recommended Skill = df-test-checker`
- handoff 摘要按 df-shared-conventions

## Red Flags

- 跳过 RED：先写实现再补失败测试
- GREEN 步内做 cleanup
- REFACTOR 顺手改 ADR / 组件边界 / 接口契约
- 引入 AR 设计未声明的新抽象 / 新模式
- 旧绿测结果当作当前证据
- 自我宣称测试有效 / 代码通过
- 把命令日志、性能基线塞进 implementation-log.md 而不是 evidence/
- 把跨 work item 的修改一起做掉
- 缺 traceability 更新就交接

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 测试通过却没说清证明的是什么 | 在 RED/GREEN 证据中补 "为什么预期失败 / 为什么通过等于行为达成" |
| GREEN 步内顺手 rename / extract method | 抽到 REFACTOR 步独立做 |
| REFACTOR 触发 cross-module 变更 | 立即停下回 router |

## Verification

- [ ] 唯一活跃 work item 锁定
- [ ] AR 设计 + 测试设计章节作为驱动，未自创测试用例
- [ ] 修改未触及组件边界（或已升级 component-impact 路线）
- [ ] RED / GREEN / REFACTOR（如适用）证据齐全且属于本会话
- [ ] 静态分析 / 编译告警证据齐全
- [ ] implementation-log.md 含完整实现交接块
- [ ] traceability.md 已补充 Code File / Test Code File / Verification Evidence
- [ ] progress.md canonical 同步，下一步 `df-test-checker`
- [ ] 父会话准备派发独立 reviewer subagent

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/red-green-refactor-discipline.md` | RED / GREEN / REFACTOR 步骤纪律、Two Hats、Fowler vocabulary |
| `references/embedded-evidence-checklist.md` | 嵌入式静态 / 动态证据采集清单 |
| `df-ar-design/references/test-design-section-contract.md` | 测试设计章节契约 |
| `docs/df-workflow-shared-conventions.md` | 工件路径、canonical 字段、handoff |

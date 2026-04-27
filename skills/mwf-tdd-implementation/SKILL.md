---
name: mwf-tdd-implementation
description: Use when the AR implementation design (with embedded test design section) has passed mwf-ar-design-review and the developer must implement the AR or DTS fix in C/C++ via TDD, when revisiting implementation after mwf-test-checker / mwf-code-review returned 需修改, or when mwf-problem-fix has handed off a confirmed reproducer + fix boundary. Not for designing the AR (→ mwf-ar-design), not for changing component design (→ mwf-component-design), not for evaluating test effectiveness (→ mwf-test-checker), not for code review (→ mwf-code-review).
---

# mwf TDD 实现

按已通过评审的 AR 实现设计（含测试设计章节）执行 C / C++ TDD：先写失败用例（RED）、再写最小实现使其通过（GREEN）、必要时做受控重构（REFACTOR），并保留可独立审查的证据。

本 skill 不写设计、不改 AR 范围、不替自己代码做有效性审查（那是 `mwf-test-checker` 的职责），也不替自己做代码检视（那是 `mwf-code-review`）。

## When to Use

适用：

- `mwf-ar-design-review` verdict = `通过` 且开发负责人 sign-off
- `mwf-test-checker` 或 `mwf-code-review` 返回 `需修改`，本 AR 仍是当前活跃 work item
- `mwf-problem-fix` 已交付复现路径 + 根因 + 最小修复边界，可消费现有 AR 设计或 fix-design.md

不适用 → 改用：

- AR 设计未通过 review / 缺测试设计 → `mwf-ar-design`
- 修改影响组件边界 → `mwf-component-design`
- 实现完成、需审查测试有效性 → `mwf-test-checker`
- 实现完成、测试已审、需审代码 → `mwf-code-review`
- 阶段不清 / 多 work item 切换 → `mwf-workflow-router`

## Hard Gates

- AR 实现设计未通过 `mwf-ar-design-review` 前不得开始
- AR 实现设计的测试设计章节缺失 / 不完整 → 不得开始；回 `mwf-ar-design`
- 修改影响组件接口 / 依赖 / 状态机 → 立即停下，回 `mwf-workflow-router` 升级 component-impact
- 不得跳过 RED：先写失败用例并跑出失败证据，再写实现
- GREEN 步内**不得**做 cleanup / 重构（违反 Two Hats）
- REFACTOR 步只做 task 触碰范围内、可解释、可验证的清理；跨 ≥3 模块的结构性重构 / 改 ADR / 改组件边界 → 立即停下回 `mwf-workflow-router`
- 不得自我宣称代码质量通过 / 测试有效；交接给 `mwf-test-checker`
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

1. 对齐输入与单 work item 锁定
   - Object: 输入证据基线
   - Method: Read-On-Presence
   - Input: ar-design-draft.md、reviews/ar-design-review.md（应 `通过`）、`docs/component-design.md`、`docs/ar-designs/AR<id>-<slug>.md`（如已存在）、`AGENTS.md`、`features/<id>/progress.md`
   - Output: 输入清单 + 当前活跃 work item 唯一锁定 + 测试设计章节内容
   - Stop / continue: AR 设计未通过 review → 阻塞，回 router；测试设计章节缺失 → 阻塞，回 `mwf-ar-design`

2. 检查是否触及组件边界
   - Object: 边界判定
   - Input: 计划要做的代码改动 vs `docs/component-design.md`
   - Output: 「不触及」/「触及」
   - Stop / continue: 触及 → 立即停下，`reroute_via_router=true`，回 router 升级 component-impact

3. 把测试设计章节落成可运行测试用例
   - Object: 测试代码
   - Method: Test Design Before Implementation
   - Input: AR 设计的测试设计章节（用例编号、覆盖、Mock、RED/GREEN 计划）
   - Output: 单测 / 集成 / 仿真测试代码（按团队测试框架）
   - Stop / continue: 在测试代码中保留与测试设计 case ID 的双向锚点（注释或命名约定）

4. RED — 戴 Changer 帽
   - Object: RED 证据
   - Method: Embedded TDD
   - Input: 步骤 3 测试代码
   - Output: 在 `features/<id>/evidence/unit/RED-<case-id>-YYYY-MM-DD.md`（或 integration 子目录）写入：
     - 命令、退出码、失败摘要
     - 为什么这个失败对应 AR 行为缺口
     - 新鲜度锚点（commit / build ID）
   - Stop / continue: 失败原因与预期不一致 → 检查测试代码是否对齐设计；不调整 AR 设计

   有效 RED：实际跑过、失败原因匹配预期、能说清证明的是什么。
   无效 RED：只写没跑、一跑就绿、无关旧失败。

5. GREEN — 戴 Changer 帽（不混戴 Refactor）
   - Object: GREEN 证据 + 最小可行实现
   - Method: Embedded TDD
   - Input: 步骤 4 RED 状态
   - Output:
     - 最小实现使测试通过（按 AR 设计的 C / C++ 实现策略）
     - `features/<id>/evidence/unit/GREEN-<case-id>-YYYY-MM-DD.md`：命令、退出码、通过摘要、关键结果、新鲜度锚点
   - Stop / continue: GREEN 步内**不**做 cleanup；看见 cleanup 机会记到步骤 6

   有效 GREEN：本次会话执行、测试转绿、保留 fresh evidence。

6. REFACTOR — 戴 Refactor 帽（若必要）
   - Object: REFACTOR 证据 + cleanup
   - Method: Refactoring Discipline + Two Hats
   - Input: 全套测试 + 静态分析全绿状态
   - Output:
     - In-task cleanups（Fowler vocabulary 命名：Extract Method / Rename / Replace Magic Number / Decompose Conditional / Remove Dead Code / ...）
     - 每次 cleanup 后跑完整测试
     - 静态分析 + 编译告警重新评估
     - `features/<id>/evidence/unit/REFACTOR-<case-id>-YYYY-MM-DD.md`（如适用）：cleanup 列表 + 命令 + 通过摘要
   - Stop / continue:
     - cleanup 跨 ≥3 模块 / 改 ADR / 改组件边界 → 立即停下，回 router
     - 引入设计未声明的新抽象层 → 立即停下，回 `mwf-ar-design` 或 router
     - 全部 cleanup 完成 → 进入步骤 7

7. 跑静态 / 动态质量证据
   - Object: 证据集合
   - Method: Static / Dynamic Quality Inspection
   - Input: 编译命令、静态分析命令、本 AR 相关回归测试
   - Output:
     - `features/<id>/evidence/build/`：编译命令、退出码、关键告警
     - `features/<id>/evidence/static-analysis/`：静态分析命令、报告路径、违反项摘要
     - `features/<id>/evidence/integration/`（如适用）：集成 / 仿真测试结果
   - Stop / continue: critical 告警 / 违反项无解释 → 不得进入交接；先按团队规则修或显式标注

8. 写实现日志与 traceability
   - Object: implementation-log.md + traceability.md
   - Output:
     - `features/<id>/implementation-log.md`：本轮修改摘要、关键决策、RED/GREEN/REFACTOR 锚点、测试结果摘要、未解决风险
     - `features/<id>/traceability.md` 补充 Code File / Test Code File / Verification Evidence 列

9. 同步 progress 与 handoff
   - Object: progress.md + handoff
   - Method: Reviewer Dispatch
   - Output:
     - `features/<id>/progress.md`：`Current Stage = mwf-tdd-implementation`、`Next Action Or Recommended Skill = mwf-test-checker`、`Pending Reviews And Gates` 含 `test-check`、`code-review`
     - 父会话准备派发独立 reviewer subagent 执行 `mwf-test-checker`

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
   - Next Action Or Recommended Skill: mwf-test-checker
   ```

## Output Contract

- C / C++ 代码改动（含必要的测试代码）
- `features/<id>/implementation-log.md` 含实现交接块
- `features/<id>/evidence/{unit,integration,static-analysis,build}/` 完整 fresh evidence
- `features/<id>/traceability.md` 补充 Code File / Test Code File / Verification Evidence
- `features/<id>/progress.md` canonical 同步：`Current Stage = mwf-tdd-implementation`、`Next Action Or Recommended Skill = mwf-test-checker`
- handoff 摘要按 mwf-shared-conventions

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
- [ ] progress.md canonical 同步，下一步 `mwf-test-checker`
- [ ] 父会话准备派发独立 reviewer subagent

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/red-green-refactor-discipline.md` | RED / GREEN / REFACTOR 步骤纪律、Two Hats、Fowler vocabulary |
| `references/embedded-evidence-checklist.md` | 嵌入式静态 / 动态证据采集清单 |
| `mwf-ar-design/references/test-design-section-contract.md` | 测试设计章节契约 |
| `skills/docs/mwf-workflow-shared-conventions.md` | 工件路径、canonical 字段、handoff |

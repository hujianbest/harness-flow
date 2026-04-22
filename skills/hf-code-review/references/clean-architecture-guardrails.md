# Clean Architecture & Refactoring Hygiene Guardrails

**何时加载此参考**：在 `hf-code-review` 评审 `CR7` 维度（Architectural Health & Refactoring Hygiene）时，或当你需要判断实现是否在悄悄破坏已批准 `hf-design` 的 Clean Architecture 约束时。

主契约仍以 `../SKILL.md` 与 `review-checklist.md` 为准；本文件提供 industry-grade 的检查规则与 anti-patterns，避免每次 review 都凭直觉判断"架构是否健康"。

## 概述

`hf-code-review` 不重新论证已批准 `hf-design` 中的架构决策；只做 **conformance check**：

- 实现是否仍遵循已批准设计的依赖方向、模块边界、接口契约
- 实现节点是否守住了 Two Hats，是否完成了应做的 Boy Scout cleanup
- Refactor Note 是否完整、可信、按 vocabulary 命名
- 是否引入了 design 未声明的 architectural smell

任何超出 task 触碰范围的结构性问题都不能由 reviewer 在评审中"顺手修"；按 verdict 与 escalation 边界返回 `hf-test-driven-dev` 或 `hf-workflow-router`。

## CR7 维度展开：Architectural Health & Refactoring Hygiene

`CR7` 由 5 个子维度构成。任一子维度低于 `6/10` 时整个 `CR7` 不得通过；任一子维度低于 `8/10` 时通常至少对应一条 finding。

### CR7.1 — Two Hats Hygiene

检查信号：

- 同一 commit 内既加新行为又改结构（diff 内既有新分支语义又有 Extract/Rename/Inline 等结构变更）
- GREEN 步骤的 commit 信息或 Refactor Note 提到 cleanup
- 测试在 GREEN 步骤里被"顺便重写"，且重写无 RED evidence 支撑
- preparatory refactor 与 RED 步骤混合（测试设计 approval 后实际写出的测试与 approval 不一致）

正确实践：

- RGR 的每个步骤独立、可识别
- preparatory refactor（若有）独立成步，全绿验证后再进入 RED
- REFACTOR 步骤的 cleanup 不引入新行为，所有测试保持绿色

### CR7.2 — Refactor Note 完整性

检查信号：

- Refactor Note 缺失或写成"做了些清理"等模糊表达
- In-task Cleanups 没有 Fowler vocabulary
- Architectural Conformance 字段空白或仅写"OK"
- 触碰文件出现明显结构变化但 Refactor Note 未提
- 识别到 architectural smell 但无 Documented Debt 或 Escalation 标记

正确实践：

- 每条 In-task Cleanup 都用 vocabulary 命名（Extract Method / Rename / Replace Magic Number / ...）
- 每条 cleanup 标明文件 + 范围
- Architectural Conformance 给出与 `hf-design` 中依赖方向 / 模块边界 / 接口契约的对比结论
- Documented Debt 与 Escalation Triggers 显式枚举

### CR7.3 — Architectural Conformance

检查信号：

- 实现新增的依赖方向违反 `hf-design` 中声明的依赖方向（典型：内层依赖外层、跨层直连）
- 实现把本应在 service / domain / use-case 层的逻辑塞到 adapter / handler / framework 层（或反向）
- 实现新增了 design 未声明的模块、新依赖、新跨层调用
- 接口契约被悄悄修改（参数语义变化、错误传播策略变化、null/optional 语义变化）
- 已批准 ADR 的可逆性评估在实现中被实质降级（例如本应"高成本重构"的决策被悄悄变成"中等成本"，或反之）

正确实践：

- 实现对 `hf-design` 的偏离要有显式理由，并能追溯到 finding 或 escalation
- 任何模块边界变更都应已经走过 `hf-increment` 或 `hf-design` 的更新

### CR7.4 — Architectural Smells Detection

参考 `../../hf-test-driven-dev/references/refactoring-playbook.md` 的 smells 速查表。CR7.4 评审：

- 是否识别了 task 触碰范围内可见的 smells
- 识别到的 smells 是否被正确分类（in-task fixed / documented debt / required escalation）
- 是否遗漏了明显 smells（God Class、Cyclic Dependency、Layering Violation、Leaky Abstraction、Feature Envy across Modules、Over-abstraction）
- 是否在 task 内"顺手"修了应该 escalate 的 smell（错误地把 escalation 当成 in-task cleanup）

判断尺度：

- 触碰范围内 smell 被正确识别且按 escalation 边界处理 → 通过
- 触碰范围内有显眼 smell 未被识别 / 未被分类 → 至少 important finding
- 把 escalation 触发项当成 in-task cleanup 处理 → critical finding（违反 escalation 边界）

### CR7.5 — Boy Scout Compliance

检查信号：

- task 触碰过的函数仍然有 magic number / 死代码 / 长函数 / 命名不清 / 嵌套 ≥ 3 层
- task 触碰过的局部出现明显重复
- 触碰文件离开时 clean code 健康度比进入时更差

正确实践：

- task 触碰范围内的 clean code 健康度不退化
- 触碰范围内的 cleanup 已落到 Refactor Note 的 Boy Scout Touches

## CR7 评分辅助

| 子维度 | 0-3 | 4-5 | 6-7 | 8-10 |
|---|---|---|---|---|
| CR7.1 Two Hats | 帽子明显混戴，cleanup 与新行为同 commit | 帽子边界模糊，无清晰 RGR 步骤切分 | 大体守住但有少量混戴 | 步骤清晰、commit 边界清晰、preparatory refactor 独立 |
| CR7.2 Refactor Note | 缺失或纯模糊表达 | 部分字段缺失 | 主要字段齐全但有 vocabulary 缺失 | 字段齐全、vocabulary 准确、debt/escalation 显式 |
| CR7.3 Conformance | 明显违反 dependency rule / 模块边界 | 有偏离但已显式说明且可追溯 | 守住边界但接口契约表达不清 | 完全 conform 或显式 escalate |
| CR7.4 Smells | 显眼 smell 被忽略 / 错分类 | 部分 smell 被识别但分类不准 | 主要 smell 已正确识别和分类 | 全面识别 + 正确分类 + 正确 escalation |
| CR7.5 Boy Scout | 触碰范围健康度退化 | 健康度持平但有明显遗漏 | 健康度未退化但有少量遗漏 | 健康度提升且 cleanup 已记录 |

## Anti-Pattern 检测（CA6-CA10）

继 `review-checklist.md` 中已有 `CA1-CA5`，CR7 引入以下补充 anti-patterns：

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `CA6` | hat-mixing | GREEN 步内做 cleanup / 同 commit 内既加行为又改结构 | 拆 commit；cleanup 归 REFACTOR 步 |
| `CA7` | undocumented-refactor | 触碰文件有结构变化但 Refactor Note 未提 | 补 Refactor Note 或回滚不必要变更 |
| `CA8` | escalation-bypass | 跨 ≥3 模块 / 改模块边界 / 改 ADR / 改接口契约的变更被在 task 内"顺手"做掉 | 回 router → `hf-increment`，不在 task 内做 |
| `CA9` | over-abstraction | 引入设计未声明的新抽象层 / 新接口 / 新基类，理由是"未来可能有用" | 回退到 design 声明的边界；YAGNI |
| `CA10` | architectural-smell-ignored | 触碰范围内可见 smell 未被识别或未被 documented | 在 Refactor Note 中识别、分类、按边界处理 |

每条 finding 仍按 `review-checklist.md` 要求带 `severity` / `classification` / `rule_id`，rule_id 使用 `CR7` / `CR7.1`-`CR7.5` / `CA6`-`CA10` 之一。

## 与 hf-design 的对齐方式

reviewer 在评 CR7.3 时：

- 不重新讨论"应该用什么架构模式"
- 不挑战 ADR 的决策本身
- 只判断"实现是否遵循了 ADR 决策结果与 `design.md` 中显式声明的依赖方向、模块边界、接口契约"

如果发现实现合理但 design 已过时（例如 design 还在 ADR-0042 状态 `proposed` 而实现已经走了一条更好的路），不在 review 内调整 design；按 finding 写出冲突，verdict 给 `阻塞`，下一步走 `hf-workflow-router`，由 router 决定是否进入 `hf-increment` 或回 `hf-design` 修订。

## 与 hf-traceability-review 的边界

CR7 不评审追溯链完整性（spec → design → tasks → impl）。这是 `hf-traceability-review` 的职责。

CR7 仅评审：

- 实现是否遵循已批准 design 的架构约束
- 实现节点是否守住 refactor hygiene
- Refactor Note 是否提供了下游可信的 architectural debt 视图

`hf-traceability-review` 之后会消费 Refactor Note 的 Documented Debt 与 Escalation Triggers 来判断追溯完整性。

## Verdict 决策

| 场景 | conclusion | 下一步 |
|---|---|---|
| CR7 全部子维度 ≥ 6，主维度 ≥ 8，无 escalation 触发 | `通过` | `hf-traceability-review` |
| CR7 有子维度 < 6 但属于 in-task 可定向修复（命名、Extract Method、补 Refactor Note 字段、补识别遗漏的 smell） | `需修改` | `hf-test-driven-dev` |
| CR7 触发 escalation-bypass（CA8）且变更已实质改动 ADR / 模块边界 / 接口契约 | `阻塞` | `hf-workflow-router`（reroute_via_router=true），由 router 路由到 `hf-increment` 或 `hf-design` |
| CR7 触发 over-abstraction（CA9）且无法在 task 内回退 | `阻塞` | `hf-workflow-router`（reroute_via_router=true） |
| CR7 触发 hat-mixing（CA6）严重导致 fresh evidence 不可信 | `需修改` | `hf-test-driven-dev`，要求重做 RGR 并重新出 fresh evidence |

## Red Flags（reviewer 自检）

- 在 review 内"顺手"指出哪里"再 clean 一点"，但没给 finding 与 verdict 映射
- 因为"测试全绿"就放过 architectural smell
- 因为"功能正确"就放过帽子混戴
- 把跨模块结构性问题写成 minor finding
- 让 reviewer 自己重新讨论架构选择（这是 `hf-design` 的工作）
- Refactor Note 缺失但 verdict 仍给"通过"
- 没看 Refactor Note 就直接判 CR7 全部子维度

## Bottom Line

CR7 让 `hf-code-review` 真正能为"持续保持 clean arch 与 clean code 健康"背书。

它依赖三件事同时存在：

1. `hf-design` 提供权威的架构 + ADR
2. `hf-test-driven-dev` 守住 Two Hats、做 in-task cleanup、识别 smells、产出 Refactor Note
3. `hf-code-review` 用 conformance check 而非重新论证来把关

如果三者中任意一环退化，CR7 都会变成纸上规则。

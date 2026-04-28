---
name: df-code-review
description: Use when df-test-checker has passed and the C/C++ code change must be independently audited for correctness / SOA boundary / memory / concurrency / real-time / error-handling / coding-standard compliance / static-analysis hygiene before completion gate, when a reviewer subagent is dispatched to perform code inspection, or when code-review returned 需修改 in a previous round. Not for writing or fixing code (→ df-tdd-implementation), not for evaluating test effectiveness (→ df-test-checker), not for stage / route confusion (→ df-workflow-router).
---

# df C / C++ 代码检视

独立审查 `df-tdd-implementation` 产出的 C / C++ 代码变化，判断正确性、设计一致性、SOA 边界、内存 / 并发 / 实时性 / 资源 / 错误处理风险、编码规范符合度、静态分析卫生度。

本 skill **不**写 / 修代码、**不**改测试、**不**替模块架构师做架构决策。它产出 verdict + findings + 唯一下一步。

## When to Use

适用：

- `df-test-checker` verdict = `通过`，需独立审 C / C++ 代码
- reviewer subagent 被派发执行 code inspection
- 用户明确要求「review 代码 / code review / 代码检视」

不适用 → 改用：

- 写 / 修代码 → `df-tdd-implementation`
- 评审测试有效性 → `df-test-checker`
- 阶段不清 / 证据冲突 → `df-workflow-router`

## Hard Gates

- `df-test-checker` 未通过前不得进入本 review
- `df-code-review` 通过前不得进入 `df-completion-gate`
- reviewer **不**修改代码 / 测试 / 设计
- reviewer **不**替模块架构师 / 开发负责人拍板
- reviewer **不**重新审组件级架构决策（那是 `df-component-design-review` 的职责）；只做 conformance check
- reviewer **不**返回多个候选下一步
- 代码修改若实质上改写组件接口 / 依赖 / 状态机 / SOA 边界 → 强制 `阻塞`(workflow)，下一步 `df-workflow-router`

## Object Contract

- Primary Object: code quality finding set + verdict
- Frontend Input Object: 代码 diff、测试代码、`features/<id>/implementation-log.md`（含实现交接块 + Refactor Note）、`features/<id>/reviews/test-check.md`（应 `通过`）、`features/<id>/evidence/`、`features/<id>/ar-design-draft.md`、`docs/component-design.md`；项目已启用可选子资产时一并读取 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（未启用直接跳过、不阻塞）；`AGENTS.md`（编码规范、静态分析配置）
- Backend Output Object: `features/<id>/reviews/code-review.md` + 结构化 reviewer 返回摘要
- Object Transformation: 把代码变化审查成发现项 + 唯一 verdict + 唯一下一步
- Object Boundaries: 不修改代码 / 不替团队角色拍板 / 不重审组件级决策
- Object Invariants: verdict ∈ {`通过`, `需修改`, `阻塞`}

## Methodology

- **Fagan Code Inspection (adapted)**: 结构化检查多维度，不做自由阅读式
- **Design Conformance Check**: 实现遵循 AR 设计 + 组件设计；偏离需有理由且可追溯
- **SOA Boundary Conformance**: 检查代码是否破坏 SOA 边界 / 引入未解释跨组件依赖
- **C / C++ Defensive Implementation Review**: 内存、生命周期、并发、实时性、错误处理、资源回收、ABI / API 兼容
- **Coding Standard Conformance**: MISRA / CERT / 团队编码规范 / 静态分析报告作为 review 输入
- **Refactor Note Audit**: 检查 implementation-log.md 中 Refactor Note 的完整性、cleanup 是否守住 Two Hats、是否触发 escalation 边界
- **Separation Of Author / Reviewer**: reviewer 不改代码

## Workflow

### 1. 建立证据基线

按 Evidence-Based + Read-On-Presence 读取代码 diff、测试代码、implementation-log.md（含实现交接块 + Refactor Note）、reviews/test-check.md（应 `通过`）、`features/<id>/evidence/`、ar-design-draft.md、`docs/component-design.md`；项目已启用的可选子资产 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md` 也一并读取，未启用直接跳过、不阻塞；`AGENTS.md`（编码规范 / 静态分析配置）。Refactor Note 是 CR8 的核心输入。

### 1.5 Precheck

- 缺实现交接块 / 核心代码范围不可定位 / Refactor Note 缺失 → blocked-content，下一步 `df-tdd-implementation`
- test-check 未通过 / route / stage / profile 冲突 → blocked-workflow，`reroute_via_router=true`，下一步 `df-workflow-router`
- Refactor Note 中 Escalation Triggers 非 `none` 但实现节点仍指向 `df-test-checker` → blocked-workflow，`reroute_via_router=true`
- 否则进入步骤 2

### 2. 多维评分

按 Fagan Code Inspection 对 8 个维度（详见 `references/code-review-rubric.md`）做 0-10 评分。任一关键维度 < 6 不得 `通过`；CR3 / CR4 / CR5 / CR6 嵌入式核心维度 < 7 也不得 `通过`。

| 维度 | 关注 |
|---|---|
| CR1 Correctness | 实现是否真正完成 AR 行为；逻辑无 off-by-one / 边界遗漏 |
| CR2 Design Conformance | 与 AR 设计一致；偏离有理由且可追溯 |
| CR3 SOA Boundary Conformance | 不破坏 SOA 边界；不引入未解释跨组件依赖 |
| CR4 Memory & Resource Lifecycle | 内存模型符合组件设计；资源句柄 / 文件 / 缓冲区配对释放 |
| CR5 Concurrency & Real-time | 中断上下文限制、锁策略、临界区、实时性 |
| CR6 Error Handling & Defensive Design | 输入校验、错误码、降级路径、ABI / API 兼容 |
| CR7 Coding Standard & Static Analysis | MISRA / CERT / 团队规范、编译告警、静态分析 critical 项 |
| CR8 Refactor Note & Architectural Health | Refactor Note 完整、cleanup 守 Two Hats、未触发 escalation 边界 |

### 3. 正式 checklist 审查

按 Checklist-Based Review 跑 Group CR1-CR8 子规则（详见 `references/code-review-rubric.md`），嵌入式风险维度参照 `references/embedded-cpp-risk-checklist.md` 速查清单。每条 finding 带 `severity` / `classification`（USER-INPUT / LLM-FIXABLE / TEAM-EXPERT） / `rule_id` / `anchor` / 描述 / 建议修复。

### 4. 形成 verdict

按下表收敛唯一 verdict + 唯一下一步：

| 条件 | conclusion | next_action_or_recommended_skill | reroute_via_router |
|---|---|---|---|
| 8 维度均 ≥ 6、CR3 / CR4 / CR5 / CR6 ≥ 7、无 critical USER-INPUT 或未解释 critical 静态分析项 | `通过` | `df-completion-gate` | `false` |
| findings 可 1-2 轮定向修订（含 Refactor Note 字段补全、Boy Scout 遗漏、in-task 范围内可识别但被遗漏的风险、可在 task 内回退的过度抽象） | `需修改` | `df-tdd-implementation` | `false` |
| 核心逻辑错误 / 内存或并发安全漏洞 / SOA 边界破坏可在 task 内回修 | `阻塞`（内容） | `df-tdd-implementation` | `false` |
| 代码实质修改组件边界 / SOA 接口 / 跨 ≥3 模块结构性变更 / Escalation-bypass / route / stage / profile / 上游证据冲突 | `阻塞`（workflow） | `df-workflow-router` | `true` |

### 5. 写 review 记录并回传

按 `templates/df-review-record-template.md` 写 `features/<id>/reviews/code-review.md`，并按 `df-workflow-router/references/reviewer-dispatch-protocol.md` 回传结构化摘要。reviewer **不**改代码 / **不**重审组件级架构（那是 `df-component-design-review` 的职责）/ **不**返回多个候选下一步。

## Output Contract

- Review record：`features/<id>/reviews/code-review.md`
- 结构化 reviewer 返回摘要：record_path、conclusion、key_findings、finding_breakdown、next_action_or_recommended_skill、needs_human_confirmation（默认 `false`）、reroute_via_router

## Red Flags

- 不读实现交接块 + Refactor Note 就审代码
- 「测试通过」当作「代码正确」
- 忽略未解释的 critical 静态分析 / 编译告警
- 评审中改代码（reviewer 不是 author）
- 重新审组件级架构（应该回 `df-component-design-review`）
- 因为「功能正确 + 测试全绿」就放过 hat-mixing / escalation-bypass
- Refactor Note 缺失但 verdict 仍给 `通过`
- 把跨 ≥3 模块的结构性问题写成 minor finding
- 返回多个候选下一步

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 看到测试全绿就给 `通过` | 检查内存 / 并发 / 实时性 / 错误处理风险，未解释项 ≥ critical → verdict ≥ `需修改` |
| 实现把内部状态暴露为公共接口仍给 `通过` | important / critical finding，要求收回边界 |
| Refactor Note 缺失却给 `通过` | precheck 应判 blocked-content |

## Verification

- [ ] review record 已落盘
- [ ] precheck 结果显式记录
- [ ] 8 维度评分完整、findings 已分类
- [ ] verdict 唯一、下一步唯一、`reroute_via_router` 正确
- [ ] Refactor Note 已被显式审查
- [ ] critical 静态分析 / 编译告警的处理已显式核对
- [ ] SOA 边界与 AR 设计一致性已显式审查
- [ ] 结构化摘要已回传父会话
- [ ] 未顺手修改代码

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/code-review-rubric.md` | 8 维度 rubric + rule IDs |
| `references/embedded-cpp-risk-checklist.md` | 嵌入式 C / C++ 风险检视速查（内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI） |
| `df-tdd-implementation/references/red-green-refactor-discipline.md` | Refactor Note 字段约定 |
| `skills/templates/df-review-record-template.md` | review record 模板 |
| `df-workflow-router/references/reviewer-dispatch-protocol.md` | reviewer 返回契约 |

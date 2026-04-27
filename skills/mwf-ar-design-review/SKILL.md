---
name: mwf-ar-design-review
description: Use when mwf-ar-design has produced an ar-design-draft.md ready for an independent verdict, when a reviewer subagent is dispatched to evaluate the AR-level code design and its embedded test-design section, or when AR design needs re-review after revision. Not for writing or revising AR design (→ mwf-ar-design), not for component design review (→ mwf-component-design-review), not for stage / route confusion (→ mwf-workflow-router).
---

# mwf AR 实现设计评审

独立评审 `features/<id>/ar-design-draft.md`，判断它是否可作为 `mwf-tdd-implementation` 的稳定输入，以及测试设计章节是否足以驱动 TDD。

本 skill 不写设计、不补测试用例、不替开发负责人或模块架构师拍板。它只产出 verdict + findings + 唯一下一步。

## When to Use

适用：

- `mwf-ar-design` 已产出 ar-design-draft.md，需正式 verdict
- reviewer subagent 被派发执行 AR 设计评审
- 用户明确要求「review 这份 AR 设计 / 评审 AR 实现设计」

不适用 → 改用：

- 缺草稿或仅需继续写 → `mwf-ar-design`
- 组件级设计评审 → `mwf-component-design-review`
- 阶段不清 / 证据冲突 → `mwf-workflow-router`

## Hard Gates

- AR 设计通过本 review 之前，不得进入 `mwf-tdd-implementation`
- reviewer 不修改设计草稿、不补写测试用例
- reviewer 不替开发负责人 / 模块架构师拍板
- reviewer 不返回多个候选下一步
- AR 设计若改写组件接口 / 依赖 / 状态机 → 强制 `阻塞`(workflow)，下一步 `mwf-workflow-router` 升级 component-impact
- 测试设计章节缺失或不含嵌入式风险覆盖矩阵 → 强制 `阻塞`(内容)
- 测试设计若被拆成独立 `test-design.md` 文件 → 强制 `阻塞`(内容)

## Object Contract

- Primary Object: AR design finding set + verdict
- Frontend Input Object: `features/<id>/ar-design-draft.md`、`features/<id>/requirement.md`、`features/<id>/traceability.md`、`docs/component-design.md`、`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（如存在）、`AGENTS.md` 模板覆盖
- Backend Output Object: `features/<id>/reviews/ar-design-review.md` + 结构化 reviewer 返回摘要
- Object Transformation: 把 AR 设计 + 测试设计章节审查成发现项 + 唯一 verdict + 唯一下一步
- Object Boundaries: 不修改设计 / 不补测试用例 / 不替团队角色拍板
- Object Invariants: verdict ∈ {`通过`, `需修改`, `阻塞`}

## Methodology

- **Code-Level Design Review**: 检查数据结构、控制流、接口签名草案、关键路径
- **Component Design Conformance Check**: 检查与 `docs/component-design.md` 的一致性；不重新审组件级决策
- **C / C++ Defensive Design Review**: 检查内存、生命周期、错误处理、并发、实时性、资源、ABI
- **Test Design Adequacy Review**: 检查测试设计章节的用例覆盖 / 边界 / 异常 / 嵌入式风险 / mock 边界 / RED-GREEN 证据要求
- **Traceability Check**: 检查每个用例回指 requirement row、嵌入式 NFR 至少一个 embedded-risk 用例
- **Template Conformance Check**: 检查团队 AR 设计模板的章节齐全（或显式占位）

## Workflow

1. 建立证据基线
   - Object: 评审输入证据基线
   - Method: Evidence-Based + Read-On-Presence
   - Input: ar-design-draft.md、requirement.md、reviews/spec-review.md（应 `通过`）、`docs/component-design.md`、reviews/component-design-review.md（component-impact 时应 `通过`）、traceability.md、`AGENTS.md`
   - Output: 输入清单 + 模板状态
   - Stop / continue: 缺设计草稿 → blocked-content，下一步 `mwf-ar-design`；缺组件设计且本 AR 触及组件边界 → blocked-workflow，`reroute_via_router=true`

2. Precheck
   - Object: precheck 结论
   - Method: 三态判定
   - Output: 通过 / blocked-content / blocked-workflow
   - Stop / continue: 同上

3. 检查是否触及组件边界
   - Object: 边界判定
   - Method: SOA Boundary 检查
   - Input: AR 设计 + 当前组件设计
   - Output: 「不触及」/「触及」
   - Stop / continue: 触及 → `阻塞`(workflow)，下一步 `mwf-workflow-router` 升级 component-impact

4. 多维评分
   - Object: 8 维度评分
   - Method: Structured Walkthrough
   - Output: 各维度 0-10 评分
   - Stop / continue: 任一关键维度 < 6 不得 `通过`

   维度（详见 `references/ar-design-review-rubric.md`）：

   | 维度 | 关注 |
   |---|---|
   | AD1 Identity & Template Conformance | AR ID / Owner / 模板章节齐全 |
   | AD2 Goal & Scope Clarity | 设计目标 / 范围 / 非范围清晰 |
   | AD3 Affected Files & Control Flow | 受影响文件 / 模块 / 控制流冷读得懂 |
   | AD4 Component Design Conformance | 与组件设计一致；不修改组件接口 / 依赖 / 状态机 |
   | AD5 C / C++ Defensive Design | 错误处理、内存、并发、实时性、资源、ABI |
   | AD6 Test Design Adequacy | 测试用例完整、回指 requirement row、嵌入式风险覆盖矩阵 |
   | AD7 Mock / RED-GREEN Plan | mock 边界合理；RED / GREEN 证据要求清晰 |
   | AD8 Open Questions Closure | 阻塞 / 非阻塞分类；阻塞项已闭合或上抛 |

5. 正式 checklist 审查
   - Object: findings
   - Method: Checklist-Based Review
   - Input: rubric
   - Output: findings 含 severity / classification / rule_id / anchor / 描述 / 建议修复

6. 形成 verdict
   - Object: 唯一 verdict + 唯一下一步

   | 条件 | conclusion | next_action_or_recommended_skill | reroute_via_router | needs_human_confirmation |
   |---|---|---|---|---|
   | 8 维度均 ≥ 6、组件边界未被改写、测试设计章节充分、无 critical USER-INPUT | `通过` | `mwf-tdd-implementation` | `false` | `true`（开发负责人确认进入 TDD） |
   | findings 可 1-2 轮定向修订 | `需修改` | `mwf-ar-design` | `false` | `false` |
   | 测试设计章节缺失 / 测试设计被拆独立文件 / 嵌入式风险覆盖矩阵缺失 / 设计严重不清 | `阻塞`（内容） | `mwf-ar-design` | `false` | `false` |
   | AR 设计修改组件接口 / 依赖 / 状态机 / 上游证据冲突 | `阻塞`（workflow） | `mwf-workflow-router` | `true` | `false` |

7. 写 review 记录
   - Output: `features/<id>/reviews/ar-design-review.md`，按 `templates/mwf-review-record-template.md`

8. 回传结构化摘要
   - Output: 按 `mwf-workflow-router/references/reviewer-dispatch-protocol.md`

## Output Contract

- Review record：`features/<id>/reviews/ar-design-review.md`
- 结构化 reviewer 返回摘要含 record_path、conclusion、key_findings、finding_breakdown、next_action_or_recommended_skill、needs_human_confirmation、reroute_via_router

## Red Flags

- 通过的 AR 设计悄悄修改了组件接口
- 测试设计章节缺嵌入式风险覆盖矩阵却给 `通过`
- 测试设计被拆成独立 `test-design.md` 文件
- 测试用例不回指 requirement row
- mock 越过真实边界 mock 内部纯逻辑
- RED / GREEN 证据要求模糊（"跑一下测试看看"）
- 因模板未补齐就给 `通过`
- 顺手补测试用例

## Common Mistakes

| 错误 | 修复 |
|---|---|
| AR 设计触及组件边界仍给 `通过` | 强制 `阻塞`(workflow) → router |
| 测试用例只覆盖 happy path | 标 critical finding，verdict ≥ `需修改` |
| 缺 mock 边界说明 | important finding，verdict ≥ `需修改` |

## Verification

- [ ] review record 已落盘
- [ ] precheck 与组件边界检查结果显式记录
- [ ] 8 维度评分完整、findings 已分类
- [ ] verdict 唯一、下一步唯一、`reroute_via_router` 正确
- [ ] `通过` 时 `needs_human_confirmation=true`
- [ ] 测试设计章节充分性已显式审查（含嵌入式风险覆盖矩阵）
- [ ] 结构化摘要已回传父会话

## Supporting References

| 文件 | 用途 |
|---|---|
| `references/ar-design-review-rubric.md` | 8 维度 rubric + rule IDs |
| `mwf-ar-design/references/test-design-section-contract.md` | 测试设计章节最小契约 |
| `skills/templates/mwf-review-record-template.md` | review record 模板 |
| `mwf-workflow-router/references/reviewer-dispatch-protocol.md` | reviewer 返回契约 |
| `skills/docs/mwf-workflow-shared-conventions.md` | handoff 字段、路径约定 |

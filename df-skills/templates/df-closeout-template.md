# df Closeout

使用说明：

- 这是 `df-finalize` 的 closeout 记录模板，覆盖两类 closeout：
  - **Implementation closeout**：AR / DTS / CHANGE，基于 `df-completion-gate` 通过
  - **Analysis closeout**：SR，基于 `df-spec-review`（不修订组件设计）或 `df-component-design-review`（修订组件设计）通过
- **默认保存路径：`features/<Work Item Id>-<slug>/closeout.md`**
- df 单 work item 一次 finalize（不维护 task queue）。SR 拆出的候选 AR 由需求负责人**新建** AR work item，**不**由 df 自动创建。
- 若项目在 `AGENTS.md` 中声明了等价模板或路径，优先遵循项目约定。

## Closeout Summary

- Work Item Type:                          # SR / AR / DTS / CHANGE
- Work Item ID:
- Owning Component:                        # AR / DTS / CHANGE 必填
- Owning Subsystem:                        # SR 必填
- Workflow Profile:                        # requirement-analysis / standard / component-impact / hotfix / lightweight
- Closeout Type: `implementation` | `analysis` | `blocked`
- Closeout Verdict: `closed` | `blocked`
- Based On Upstream Verdict:               # implementation: features/<id>/completion.md
                                           # analysis(SR 不修订组件设计): features/<id>/reviews/spec-review.md
                                           # analysis(SR 修订组件设计): features/<id>/reviews/component-design-review.md
- Date:

## Evidence Matrix

按 Closeout Type 填写。`N/A`（不适用本 type）不算 blocked。

| 工件 | 路径 | Implementation closeout | Analysis closeout |
|---|---|---|---|
| Requirement | `requirement.md` | present | present |
| Spec Review | `reviews/spec-review.md` | 通过 | 通过 |
| Component Design Review | `reviews/component-design-review.md` | 通过 / N/A | 通过 / N/A |
| AR Design Review | `reviews/ar-design-review.md` | 通过 | **N/A** |
| Test Effectiveness Review | `reviews/test-check.md` | 通过 | **N/A** |
| Code Review | `reviews/code-review.md` | 通过 | **N/A** |
| Completion Gate | `completion.md` | 通过 | **N/A** |

## Long-Term Assets Sync

| 长期资产 | 路径 | 本次是否同步 | 备注 |
|---|---|---|---|
| Component Implementation Design | `docs/component-design.md` | yes / no / N/A | |
| AR Implementation Design | `docs/ar-designs/AR<id>-<slug>.md` | yes / N/A | implementation closeout 的 AR 工作项必填；SR / DTS 不修改 AR 设计时写 N/A |
| Interfaces（可选） | `docs/interfaces.md` | yes / no / N/A（项目未启用） | |
| Dependencies（可选） | `docs/dependencies.md` | yes / no / N/A（项目未启用） | |
| Runtime Behavior（可选） | `docs/runtime-behavior.md` | yes / no / N/A（项目未启用） | |

填写规则：

- 已启用资产 + 本次触发变化 → `yes`
- 已启用资产 + 本次未触发变化 → `no`
- 项目尚未启用此可选资产 → `N/A（项目未启用）`，**不**算 blocked；相关变化应已合并进 `docs/component-design.md` 对应章节
- AR 工作项 implementation closeout 时**必须**在 `docs/ar-designs/` 留下本 AR 的正式设计文档；DTS 不修改 AR 设计 / SR 时该行写 `N/A`

## AR Breakdown Candidates（仅 Analysis closeout 必填；其他类型写 N/A）

由 SR `df-specify` 起草、`df-spec-review` 修订、`df-finalize` analysis closeout 时定稿。每条候选含：

| 字段 | 说明 |
|---|---|
| Candidate ID | 例 `CAR-001`（SR 内部编号） |
| Scope | 1-2 句候选 AR 范围 |
| Owning Component | 候选 AR 所属组件（必须唯一） |
| Covers SR Rows | 引用本 SR 的若干 row ID |
| Priority Hint | 团队约定的优先级提示 |
| Estimated Complexity | `S` / `M` / `L` |
| Hand-off Owner | 候选 AR 应交给哪位开发负责人 / 团队 |
| Notes | 依赖关系、与其他候选的拆分边界等 |

如本 SR 显式声明「无可拆分 AR」（仅做组件设计修订或文档级修订），写明并记录由需求负责人确认。

## State Sync

- Final `Current Stage`:                   # closed / completed
- Final `Next Action Or Recommended Skill`:  # null（已完成）
- Outstanding Risks Recorded To:           # 例：组件级 risk log / backlog 路径

## Handoff

- 提交 / 合并状态:                         # branch / MR / PR 信息（implementation closeout）
                                           # 或：候选 AR 交付清单（analysis closeout，重复上面 Candidates 表的关键字段）
- 团队同步说明:
- Limits / Open Items:

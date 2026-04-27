# mwf Review Record

使用说明：

- 这是 mwf review 记录通用模板，可用于 spec-review / component-design-review / ar-design-review / test-check / code-review。
- **默认保存路径：`features/<Work Item Id>-<slug>/reviews/<kind>.md`**
  - `spec-review.md` / `component-design-review.md` / `ar-design-review.md` / `test-check.md` / `code-review.md`
- 若项目在 `AGENTS.md` 中声明了等价路径或专用模板，优先遵循项目约定。

## Metadata

- Review Type:                             # spec-review / component-design-review / ar-design-review / test-check / code-review
- Work Item Type:                          # AR / DTS / CHANGE
- Work Item ID:
- Owning Component:
- Reviewer:                                # 独立 reviewer 角色或 subagent
- Date:
- Record Path:

## Inputs Consumed

- Primary Artifact:                        # 被评审对象的路径与版本锚点
- Supporting Context:
  - Spec / Requirement:
  - Component Design:
  - AR Design:
  - Implementation Handoff（如适用）:
  - Evidence Paths（如适用）:
- AGENTS.md / Team Standards Refs:

## Multi-Dimension Scoring

| 维度 | 0-10 | 关键证据 |
|---|---|---|
| <按节点类型填入维度，如：可追溯性 / 可设计性 / 模板符合度 / 测试覆盖 / 代码安全 / 嵌入式风险 等> |  |  |

任一关键维度 < 6 不得给出 `通过`。

## Findings

| ID | Severity | Classification | Rule ID | Anchor | 描述 | 建议修复 |
|---|---|---|---|---|---|---|
| F-001 | critical / important / minor | USER-INPUT / LLM-FIXABLE / TEAM-EXPERT | 例：S2、A4、CR3、TC2 |  |  |  |

分类约定：

- `USER-INPUT`：缺业务事实 / 外部决策 / 优先级冲突，需要团队负责人或需求负责人拍板
- `LLM-FIXABLE`：缺 wording、章节、示例、明显逻辑漏洞，可以由开发人员定向回修
- `TEAM-EXPERT`：需要模块架构师 / 资深工程师专业判断，例如组件边界、SOA 接口、嵌入式风险

## Verdict

- Conclusion: `通过` | `需修改` | `阻塞`
- Verdict Rationale:
- Next Action Or Recommended Skill:        # canonical mwf-* 节点
- reroute_via_router:                      # true / false（结论无法唯一映射下一步时为 true 并指向 mwf-workflow-router）

## Follow-up Actions

- Action:
- Owner:
- Status:

## Notes

- Additional Notes:

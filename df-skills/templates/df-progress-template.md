# df Work Item Progress

使用说明：

- 这是 `features/<Work Item Id>-<slug>/progress.md` 模板。
- 是 work item 唯一权威 progress 落点，所有 `df-*` skill 完成节点工作时必须用 canonical 字段同步。
- `Next Action Or Recommended Skill` 只能写 canonical `df-*` 节点名，**不允许**自由文本，**不允许**写 `using-df-workflow`。
- 若项目在 `AGENTS.md` 中声明了等价模板或路径，优先遵循项目约定。

## Identity

- Work Item Type:                          # AR / DTS / CHANGE
- Work Item ID:
- Owning Component:
- Related IR:
- Related SR:
- Related AR:                              # DTS 影响功能需求时填写

## Workflow State

- Current Stage:                           # canonical df-* 节点
- Workflow Profile:                        # standard / component-impact / hotfix / lightweight
- Execution Mode:                          # interactive / auto
- Last Updated:

## Pending Reviews And Gates

- Pending Reviews And Gates:
- Blockers:

## Progress Notes

- What Changed In This Round:
- Evidence Paths:                          # 例：features/<id>/evidence/...
- Open Risks:

## Traceability Anchors

- IR / SR / AR Refs:
- Component Design Refs:
- AR Design Refs:                          # ar-design-draft.md 章节锚点 + docs/ar-designs/...
- Test Design Refs:                        # AR 实现设计中测试设计章节锚点

## Next Step

- Next Action Or Recommended Skill:        # canonical df-* 节点
- Notes:

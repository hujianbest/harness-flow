# df Work Item Progress

使用说明：

- 这是 `features/<Work Item Id>-<slug>/progress.md` 模板。
- 是 work item 唯一权威 progress 落点，所有 `df-*` skill 完成节点工作时必须用 canonical 字段同步。
- `Next Action Or Recommended Skill` 只能写 canonical `df-*` 节点名，**不允许**自由文本，**不允许**写 `using-df-workflow`。
- 若项目在 `AGENTS.md` 中声明了等价模板或路径，优先遵循项目约定。

## Identity

- Work Item Type:                          # SR / AR / DTS / CHANGE
- Work Item ID:
- Owning Component:                        # AR / DTS / CHANGE 必填；SR 可空
- Owning Subsystem:                        # SR 必填；AR / DTS / CHANGE 可空
- Related IR:
- Related SR:                              # AR 必填
- Related AR:                              # DTS 影响功能需求时填写
- AR Breakdown Candidates:                 # 仅 SR 适用；spec-review 后定稿，analysis closeout 时写入 closeout.md

## Workflow State

- Current Stage:                           # canonical df-* 节点
- Workflow Profile:                        # requirement-analysis（SR）/ standard / component-impact / hotfix / lightweight
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

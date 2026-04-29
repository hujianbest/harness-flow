# Discovery Approval — WriteOnce Walking Skeleton

- 节点: discovery approval gate（产品方向 approval）
- Date: 2026-04-29
- Approver: cursor agent (acting on behalf of the user, who delegated demo product scope on 2026-04-29 — see `docs/insights/2026-04-29-writeonce-discovery.md` section 0)
- Based On Review Record: `reviews/discovery-review-2026-04-29.md`

## Decision

`Approved`

## Approved Inputs To `hf-specify`

- Discovery draft: `docs/insights/2026-04-29-writeonce-discovery.md`（状态翻转为「已批准」）
- Spec bridge: `docs/insights/2026-04-29-writeonce-spec-bridge.md`（状态翻转为「已批准」）
- Seed table (per discovery section 0):
  - 目标用户: 技术内容创作者（独立开发者 / 写技术博客的工程师）
  - 首发平台清单: Medium（实现），Zhihu + WeChat MP（声明扩展点，不实现）
  - MVP 边界: Markdown → Medium，纯文本 + 图片 + fenced code block
  - 技术栈: Node.js 20 + TypeScript + minimal CLI
  - Walking skeleton 覆盖: Medium 端到端 + 其它两平台留 PlatformAdapter 扩展点

## Notes

- 本 approval **不是**最终 release approval；它只是放行 spec 起草。
- spec 起草过程中若需要修改 seed 表中的任意一项，需返回 discovery 节点并触发 discovery-review 第二轮，**不**允许在 spec 内私自改动 seed。
- demo 中的 "approval" 由 cursor agent 一人承担，与真实多角色 SDD 不同；demo README "Limits" 段已说明。

## Next Action Or Recommended Skill

`hf-specify`

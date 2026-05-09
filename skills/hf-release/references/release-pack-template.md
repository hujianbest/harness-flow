# Release Pack Template

`hf-release` §10 主工件模板。schema 与 `hf-finalize/references/finalize-closeout-pack-template.md` 同源，scope 不同（release-tier 而非单 feature closeout）。

## 使用说明

- 默认保存路径：`features/release-vX.Y.Z/release-pack.md`
- §11 Final Confirmation 通过后 `Status` 字段从 `in-progress` / `ready-for-tag` → `released`
- 本模板字段必填；未启用的可选资产显式写 `N/A（理由）`，不能省略
- 项目若声明了等价模板，优先遵循项目约定

## 模板正文

```markdown
# Release Pack — vX.Y.Z

## Release Summary

- Version: vX.Y.Z
- Pre-release: yes / no
- Bump Type: major / minor / patch
- Scope ADR: docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md
- Status: in-progress / ready-for-tag / released / blocked-on-<check-id>
- Started At: YYYY-MM-DD
- Finalized At: YYYY-MM-DD（仅 Final Confirmation 通过时填）
- Author: <起草人>

## Scope Summary

- Included Features:
  - features/<feature-id-1>/  ——  <一句话说明>
  - features/<feature-id-2>/  ——  <一句话说明>
  - ...
- Deferred Features (with reason):
  - features/<feature-id-X>/  ——  <为什么本版不入：deferred to vX.Y+1.0 / not yet workflow-closeout / scope mismatch>
  - ...
- Reference: docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | features/release-vX.Y.Z/verification/release-regression.md | present / N/A（按 profile 跳过） | <fresh evidence 时间戳 / 测试入口 / 通过结论> |
| cross-feature traceability | features/release-vX.Y.Z/verification/release-traceability.md | present / N/A | <聚合 verdict 摘要> |
| pre-release engineering checklist | features/release-vX.Y.Z/verification/pre-release-checklist.md | present | <FAIL 项数 / 全部 PASS> |
| scope ADR | docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md | present | <状态：起草中 / accepted> |
| CHANGELOG entry | CHANGELOG.md | present | <vX.Y.Z 段已 commit at <sha>> |
| release notes（档 2）| docs/release-notes/vX.Y.Z.md | present / N/A（项目档 0/1 未启用） | <Highlights / Migration / Known Limitations 段齐> |

## Docs Sync (sync-on-presence 实际同步路径)

- CHANGELOG Path: CHANGELOG.md（vX.Y.Z 段 committed at <sha>）
- Release Notes Path: docs/release-notes/vX.Y.Z.md / N/A（项目档 0/1 未启用）
- ADR Status Flips:
  - docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md（proposed → accepted at Final Confirmation）
  - <候选 feature 引用过且仍 proposed 的 ADR：状态翻转列表>
- Long-Term Assets Sync:
  - 架构概述：docs/architecture.md（档 1）/ docs/arc42/...（档 2）/ N/A（本 release 未触发架构变化）
  - docs/runbooks/...：N/A（项目当前未启用此资产）/ <实际路径>
  - docs/slo/...：同上
  - docs/diagrams/...：同上
- Index Updated:
  - 档 0/1：仓库根 README.md（active feature / 最近 release 行）
  - 档 2：docs/index.md
- Project Metadata Sync:
  - .claude-plugin/plugin.json: version → vX.Y.Z / N/A
  - .claude-plugin/marketplace.json: 描述同步 / N/A
  - SECURITY.md: Supported Versions 表加 X.Y.x 行 / N/A
  - package.json / pyproject.toml / Cargo.toml / 其他: <实际同步项>

## Tag Readiness

- Suggested Tag: vX.Y.Z
- Suggested Commit: <sha on release base branch>
- Release Base Branch: main / release/vX.Y / 项目自定
- PR Status: <所有候选 feature 的 PR 已合并；或列出仍 open 的 PR>
- Tag 操作执行者: 项目维护者（**本 skill 不自动执行 git tag / git push --tags**）

## Worktree Disposition

| Feature | Disposition | Notes |
|---|---|---|
| features/<feature-id-1>/ | kept-for-pr / cleaned-per-project-rule / in-place | <如保留，对应 PR 链接> |
| features/<feature-id-2>/ | ... | ... |
| ... | ... | ... |

## Final Confirmation (interactive only)

- Question: 是否确认正式锁定 vX.Y.Z 范围？锁定后 Scope ADR 状态翻 accepted、CHANGELOG 段固化、Tag readiness 就位、Status: released。
- Confirmation Status: pending / confirmed / rejected
- Confirmed By: <用户署名>
- Confirmed At: YYYY-MM-DD HH:MM <时区>
- If confirmed: write `Next Action Or Recommended Skill: null`（tag 操作交项目维护者）
- If rejected: 回到对应 §<step> 重做（不写回 hf-workflow-router）

## Limits / Open Notes

- Forward References:
  - 部署 / staged rollout / 监控 / 回滚：v0.5+ planned `hf-shipping-and-launch`（**当前尚未实现**），项目自承担
  - <其他本版未承诺的能力 + 落到哪个 v0.X+ 节点>
- Known Limitations:
  - <从各候选 feature closeout `Limits / Open Notes` 字段聚合的项>
  - ...
- Open Questions:
  - <尚未决议、留给下一版的问题>

## Handoff

- Next Action Or Recommended Skill: null（已 released）/ <具体阻塞点描述>（未通过）/ hf-release §<step>（同 skill 回退）
- **不**写回 hf-workflow-router（本 skill 与 router 解耦）
- PR / Branch Status: <所有候选 PR 状态汇总>
- Suggested Maintainer Actions:
  1. git tag vX.Y.Z <suggested-commit>
  2. git push --tags
  3. GitHub Release（按是否 pre-release 勾选）
  4. release notes 引用本 release pack + scope ADR
  5. <项目自定后续步骤>
```

## 编写约束

- **字段必填**：不允许整段省略；未启用资产显式写 `N/A（理由）`。
- **Status 值受控**：只能是 `in-progress` / `ready-for-tag` / `released` / `blocked-on-<check-id>` 四档。
- **Tag 操作不自动**：`Tag 操作执行者` 字段必须为"项目维护者"或等价说明；本 skill 不允许在 readiness pack 中声明已自动执行 `git tag`。
- **forward reference 真实性**：`Limits / Open Notes` 段引用 v0.5+ planned `hf-shipping-and-launch` 时必须标 `当前尚未实现`，避免误导读者。
- **不写回 router**：`Handoff > Next Action Or Recommended Skill` 不允许写 `hf-workflow-router`；本 skill 与 router 解耦，没有"交回 router"的语义。
- **Worktree disposition 三档**：`kept-for-pr` / `cleaned-per-project-rule` / `in-place`，与 `hf-finalize` 同源；不允许出现 `deleted` 或其他自创值。

## 与 `hf-finalize` closeout pack 的对照

| 字段 | finalize closeout pack | release pack | 差异 |
|---|---|---|---|
| Closeout Type / Bump Type | `task-closeout` / `workflow-closeout` / `blocked` | `major` / `minor` / `patch` | scope 不同（feature 级 / 版本级） |
| Scope | 单 feature | 多 feature 聚合 | release 必须列 included + deferred 双清单 |
| Evidence Matrix | regression / completion / 等单 feature 记录 | release-wide regression / cross-feature traceability / pre-release-checklist | release 是版本级聚合 |
| Worktree Disposition | 单条 | 每个候选 feature 一条 | 表格化 |
| Final Confirmation | workflow closeout 才需要 | 任何 release 都需要（锁定对外承诺面）| release 必填 |
| Next Action | hf-workflow-router（task-closeout）/ null（workflow-closeout）| null（已 released）/ 阻塞点 / hf-release §<step> | release **不**写回 router |

读取本模板时若同时熟悉 `hf-finalize/references/finalize-closeout-pack-template.md`，可快速理解：release pack 是 closeout pack 在版本级的同源扩展。

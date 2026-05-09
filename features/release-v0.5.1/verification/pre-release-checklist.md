# Pre-Release Engineering Checklist — v0.5.1

按 `skills/hf-release/references/pre-release-engineering-checklist.md` 模板逐项核对。Profile = `lightweight`。

## Code & Evidence

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| C1 | release-wide regression 通过 | ✅ PASS | 见 `features/release-v0.5.1/verification/release-regression.md`；执行时间 2026-05-09T18:59:34Z 晚于本版所有脚本 / SKILL.md / 文档 commit |
| C2 | cross-feature traceability 摘要落盘 | ✅ PASS | 见 `features/release-v0.5.1/verification/release-traceability.md`；本版单候选 feature 的 trace 链条完整闭环；vendoring 漏洞已确认修复 |
| C3 | 候选 feature 全为 `workflow-closeout` 状态 | ⚠️ N/A（特殊场景） | 与 v0.5.0 同情形：本版工作面是"anatomy 扩展 + 物理迁移"，不存在独立 `features/<feature-id>/closeout.md` 候选；以 hf-release dogfood 形态打包 engineering-tier 修复（详见 release-pack.md `Limits / Open Notes` 段） |
| C4 | release base branch 上 lint / type / build 通过 | ✅ PASS | HF 仓库 v0.5.1 不引入运行时依赖；JSON validity 已在 release-regression.md §4 验证（5 个 JSON 工件全部有效，含 `plugin.json` 升级到 0.5.1 后的解析） |
| C5 | 无 release-blocking PR 仍 open | ✅ PASS | 本版 release pack 由 v0.5.1 patch PR 携带；旧 PR #37（v0.5.0）已 MERGED + tagged；不存在仍 open 的 release-blocking PR |

## Documentation Sync (sync-on-presence 协议内联)

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| D1 | **CHANGELOG.md** 的 `[0.5.1]` 段已写 | ✅ PASS | 段内含 Fixed / Changed / Decided / Notes（patch release 没 Added / Deferred 子段，与 Keep a Changelog 规范一致）；段末有 `[0.5.1]: <link>` 链接行 |
| D2 | 顶层导航已更新 | ✅ PASS | 仓库根 `README.md` Scope Note 加 v0.5.1 patch 注解；`README.zh-CN.md` 同步；HF 仓库档 0/1，无独立 `docs/index.md`（与 v0.5.0 / v0.4.0 同向） |
| D3 | 涉及的 ADR 状态已批量翻转 | ⏳ pending | `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md` 状态 = 起草中；按 hf-release SKILL.md §11 + 模板约定，状态翻转 `proposed → accepted` 在 §11 Final Confirmation 通过时执行；不动 ADR-005（v0.5.0 已 tagged，不修订历史）|
| D4 | `docs/release-notes/v0.5.1.md` 同步 | ⚠️ N/A | 项目档 0/1 未启用 `docs/release-notes/` 目录；与 v0.5.0 / v0.4.0 同向 |
| D5 | 架构概述按存在同步 | ⚠️ N/A | 本 release 未触发架构变化 |
| D6 | `docs/runbooks/` 同步 | ⚠️ N/A（项目当前未启用此资产 / 本 release 未触发） | |
| D7 | `docs/slo/` 同步 | ⚠️ N/A | |
| D8 | `docs/diagrams/` 同步 | ⚠️ N/A | |
| D9 | feature closeout `Release / Docs Sync` 字段对账一致 | ✅ PASS | 本版无候选 `workflow-closeout` feature；不存在 closeout `Release / Docs Sync` 与本 release 的对账冲突 |
| D10 | Migration / breaking changes 已写入 release notes | ✅ PASS | CHANGELOG `[0.5.1]` 段 `Notes` 子段含 migration 提示（hardcode 了旧路径 `scripts/render-closeout-html.py` 的项目级 CI / 别名需同步更新到 `skills/hf-finalize/scripts/render-closeout-html.py`）；ADR-006 Consequences 段亦已显式入档 |
| D11 | Known Limitations 已聚合 | ✅ PASS | 见 `release-pack.md` `Limits / Open Notes` 段（含 ops 能力承担方说明 + 单候选场景的 dogfood 处理 + upgrade migration 提示 + 不保留旧路径 symlink 的边界 + roadmap 标签维持）|

## Versioning Hygiene

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| V1 | scope ADR 已 commit | ✅ PASS | `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md` 已 commit；状态 = 起草中（§11 通过后翻 accepted） |
| V2 | SemVer + pre-release 标记已写入 release pack | ✅ PASS | release pack `## Release Summary` 段含 `Version: v0.5.1` + `Pre-release: yes` + `Bump Type: patch` 三字段 |
| V3 | `.claude-plugin/plugin.json` `version` 同步 | ✅ PASS | `0.5.0` → `0.5.1` |
| V4 | `.claude-plugin/marketplace.json` 描述同步 | ✅ PASS | description 段追加 v0.5.1 vendoring fix 说明 |
| V5 | `SECURITY.md` Supported Versions 表 | ✅ PASS | `0.5.x` 行 latest 从 `0.5.0` 升到 `0.5.1`；其它行不动（patch release 不影响其它版本支持等级） |
| V6 | 项目级元数据中的版本号已同步 | ✅ PASS | 与 v0.5.0 同向；HF 仓库本身不是 npm/pypi/crates 包 |
| V7 | 相关版本链接表 / 链接 update | ✅ PASS | CHANGELOG 末尾 `[0.5.1]: <link>` 行已加；版本链接表已加 `[0.5.1]` 行；Unreleased compare base 从 `v0.5.0` 升到 `v0.5.1` |

## Worktree / Branch State

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| W1 | worktree disposition 全部记录 | ✅ PASS | release pack `## Worktree Disposition` 段记录 2 项：本 PR 分支（kept-for-pr）+ v0.5.0 旧 PR 分支（kept-for-history，含 v0.5.0 PR 合并时机问题的说明）|
| W2 | release base branch 状态 | ⏳ pending | release branch HEAD = release pack 草稿提交后的最新 commit；待 v0.5.1 PR 合入 main 后由项目维护者在 main 上 confirm `Suggested Commit` |
| W3 | 未自动删除 worktree | ✅ PASS | 本 release 未删除任何 worktree；只在 release pack 中记录 disposition |

## Out of Scope（与 v0.5.0 / v0.4.0 / v0.3.0 同向）

| 动作 | 落到哪 |
|---|---|
| 部署 / staged rollout / 监控 / SLO / 回滚 / health check / CDN / DNS / SSL / Rate limiting | 项目自身的 ops / 安全流程（v0.6+ planned `hf-shipping-and-launch`，**当前尚未实现**）|
| 上线后观察窗口 / staged rollout decision thresholds / launch announcement | 项目自身的 ops / 发布沟通流程 |
| `git tag v0.5.1 && git push --tags` | 项目维护者按 ADR-006 D4 + ADR-005 D9 + ADR-004 D7 立场手工执行 |

## 总体结论

- 全部 PASS / N/A / pending（无 FAIL）
- pending 项均为 hf-release SKILL.md §11 / 模板约定的"Final Confirmation 通过时才能完成"动作（D3 ADR 状态翻转 / W2 release base branch HEAD 锚定），不阻塞本 release 进入 §11 Final Confirmation 阶段
- `release-pack.md` Status 字段保持 `ready-for-tag`；等待用户最终确认正式锁定 v0.5.1 范围

# Pre-Release Engineering Checklist — v0.5.0

按 `skills/hf-release/references/pre-release-engineering-checklist.md` 模板逐项核对。Profile = `lightweight`（HF 仓库 v0.4.0 起声明）。

## Code & Evidence

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| C1 | release-wide regression 通过 | ✅ PASS | 见 `features/release-v0.5.0/verification/release-regression.md`；执行时间 2026-05-09T17:34:59Z 晚于本版所有 hf-finalize / 脚本 commit |
| C2 | cross-feature traceability 摘要落盘 | ✅ PASS | 见 `features/release-v0.5.0/verification/release-traceability.md`；本版单候选 feature 的 trace 链条完整闭环 |
| C3 | 候选 feature 全为 `workflow-closeout` 状态 | ⚠️ N/A（特殊场景）| 本版工作面是 "hf-finalize 输出契约扩展 + 新脚本"，不存在独立 `features/<feature-id>/closeout.md` 候选；以 hf-release dogfood 形态把 engineering-tier 改进塞进 release pack 模板的 "Included Features" 段（见 release-pack.md `Limits / Open Notes` 段第二条）。这与 v0.4.0 引入 hf-release 时的 dogfood 路径同向（v0.4.0 release 也未要求自身先走 hf-finalize 走一遍 workflow-closeout） |
| C4 | release base branch 上 lint / type / build 通过 | ✅ PASS | HF 仓库 v0.5.0 不引入 npm/pip 等运行时依赖，无 lint / type 入口；JSON validity 已在 release-regression.md §4 验证（5 个 JSON 工件全部有效，含本版 `plugin.json` 升级到 0.5.0 后的解析） |
| C5 | 无 release-blocking PR 仍 open | ✅ PASS | 本版 release pack 由 PR #37 (`cursor/hf-finalize-html-closeout-report-eea2`) 携带；PR 在 release pack 提交后由维护者审阅 → 合并 → 打 tag，符合 hf-release SKILL.md `Tag Readiness` 段约定 |

## Documentation Sync (sync-on-presence 协议内联)

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| D1 | **CHANGELOG.md** 的 `[0.5.0]` 段已写 | ✅ PASS | 段内含 Added / Changed / Decided / Deferred / Notes 5 子段；段末有 `[0.5.0]: <link>` 链接行 |
| D2 | 顶层导航已更新 | ✅ PASS | 仓库根 `README.md` Scope Note 升级到 v0.5.0；`README.zh-CN.md` 范围声明段升级到 v0.5.0；HF 仓库档 0/1，无独立 `docs/index.md`（与 v0.4.0 同向） |
| D3 | 涉及的 ADR 状态已批量翻转 | ⏳ pending | `docs/decisions/ADR-005-release-scope-v0.5.0.md` 状态 = 起草中；按 hf-release SKILL.md §11 + 模板约定，状态翻转 `proposed → accepted` 在 §11 Final Confirmation 通过时执行（**不**提前），由 Final Confirmation 通过时的 follow-up commit 完成 |
| D4 | `docs/release-notes/v0.5.0.md` 同步 | ⚠️ N/A | 项目档 0/1 未启用 `docs/release-notes/` 目录；与 v0.4.0 / v0.3.0 / v0.2.0 / v0.1.0 同向，按 sync-on-presence 规则不需要创建 |
| D5 | 架构概述按存在同步 | ⚠️ N/A | 本 release 未触发架构变化；HF 仓库未启用 `docs/architecture.md` 或 `docs/arc42/` |
| D6 | `docs/runbooks/` 同步 | ⚠️ N/A（项目当前未启用此资产 / 本 release 未触发） | |
| D7 | `docs/slo/` 同步 | ⚠️ N/A（项目当前未启用此资产 / 本 release 未触发） | |
| D8 | `docs/diagrams/` 同步 | ⚠️ N/A（项目当前未启用此资产 / 本 release 未触发） | |
| D9 | feature closeout `Release / Docs Sync` 字段对账一致 | ✅ PASS | 本版无候选 `workflow-closeout` feature（C3 已说明）；唯一相关的 walking-skeleton closeout.md 不在本 release scope 内（ADR-005 D8：不刷新 demo），其 `Release / Docs Sync` 字段是 v0.1.0 时期落盘，与本 release 无对账冲突 |
| D10 | Migration / breaking changes 已写入 release notes | ✅ PASS / N/A | 本版**不**含 breaking change（ADR-005 D6 已声明）；CHANGELOG `[0.5.0]` 段无独立 `Migration Notes` 子段；`[0.5.0]` 段 `Notes` 子段第 2 条提到 hard gate 严化的影响处理方式（"升级到 v0.5.0 后下次执行 hf-finalize 才触发新 gate；对历史 closeout 不追溯"）作为非 breaking 变更声明 |
| D11 | Known Limitations 已聚合 | ✅ PASS | 见 `release-pack.md` `Limits / Open Notes` 段（含 ops 能力的承担方说明 + 单候选场景的 dogfood 处理 + 覆盖率数据采集仍由项目自定 + HTML 报告语义边界 + roadmap 漂移声明 5 条） |

## Versioning Hygiene

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| V1 | scope ADR 已 commit | ✅ PASS | `docs/decisions/ADR-005-release-scope-v0.5.0.md` 已 commit 到 release branch；状态字段 = 起草中（§11 通过后翻 accepted） |
| V2 | SemVer + pre-release 标记已写入 release pack | ✅ PASS | release pack `## Release Summary` 段含 `Version: v0.5.0` + `Pre-release: yes` + `Bump Type: minor` 三字段 |
| V3 | `.claude-plugin/plugin.json` `version` 同步 | ✅ PASS | `0.4.0` → `0.5.0` |
| V4 | `.claude-plugin/marketplace.json` 描述同步 | ✅ PASS | description 段追加 v0.5.0 说明（hf-finalize HTML 伴生报告 + 24 hf-* 不变 + 5 项 ops/release skill 漂移到 v0.6+） |
| V5 | `SECURITY.md` Supported Versions 表加 `0.5.x` 行 | ✅ PASS | `0.5.x` 加为当前 pre-release；`0.4.x` 降级为 best-effort security-only；ADR refs 段加 ADR-005 D2 引用 |
| V6 | 项目级元数据中的版本号已同步 | ✅ PASS / N/A | HF 仓库本身不是 npm / pypi / crates 包；`examples/writeonce/package.json` 是 demo 私有，与 HF release 版本号脱钩（按 ADR-001 D9 立场不动；与 v0.4.0 同向） |
| V7 | 相关版本链接表 / 链接 update | ✅ PASS | CHANGELOG 末尾 `[0.5.0]: <link>` 行已加；版本链接表已加 `[0.5.0]` 行；README 无 "latest version" badge / link |

## Worktree / Branch State

| # | 核对项 | 状态 | 证据 / Notes |
|---|---|---|---|
| W1 | worktree disposition 全部记录 | ✅ PASS | release pack `## Worktree Disposition` 段记录 2 项：本 PR 分支（kept-for-pr）+ walking-skeleton（in-place） |
| W2 | release base branch 状态 | ⏳ pending | release branch HEAD = release pack 草稿提交后的最新 commit；待 PR #37 合入 main 后由项目维护者在 main 上 confirm Tag Readiness 段的 `Suggested Commit` |
| W3 | 未自动删除 worktree | ✅ PASS | 本 release 未删除任何 worktree；只在 release pack 中记录 disposition |

## Out of Scope（显式列出本 release **不**做的事）

| 动作 | 落到哪 |
|---|---|
| 部署到 production / staging / canary | 项目自身的 ops 流程（v0.6+ planned `hf-shipping-and-launch`，**当前尚未实现**）|
| Feature flag 0% → 5% → 100% 的 staged rollout | 项目自身的 ops 流程 |
| 监控仪表盘 / 错误上报配置 / SLO 配置 | 项目自身的 ops 流程 |
| 回滚 procedure / 回滚演练 | 项目自身的 ops 流程 |
| Health check / CDN / DNS / SSL / Rate limiting 配置 | 项目自身的 ops / 安全流程 |
| 上线后的观察窗口 / Staged rollout decision thresholds | 项目自身的 ops 流程 |
| User communication / launch announcement | 项目自身的发布沟通流程（用户在 GitHub Releases 页面发布并勾选 pre-release 时承担）|
| `git tag v0.5.0 && git push --tags` | 项目维护者按 ADR-005 D9 + ADR-004 D7 立场手工执行（**不**由本 skill 自动）|

以上动作 **不应** 出现在本 release pack 或 CHANGELOG 的"已完成"清单中。

## 总体结论

- 全部 PASS / N/A / pending（无 FAIL）
- pending 项均为 hf-release SKILL.md §11 / 模板约定的"Final Confirmation 通过时才能完成"动作（D3 ADR 状态翻转 / W2 release base branch HEAD 锚定），不阻塞本 release 进入 §11 Final Confirmation 阶段
- `release-pack.md` Status 字段保持 `ready-for-tag`；等待用户最终确认正式锁定 v0.5.0 范围

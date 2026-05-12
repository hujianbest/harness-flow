# Pre-Release Engineering Checklist — v0.6.0

- Authored: 2026-05-12
- Profile: full
- Reference rubric: `skills/hf-release/references/pre-release-engineering-checklist.md`
- Scope ADR: `docs/decisions/ADR-008-release-scope-v0.6.0.md`

## Code & Evidence

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| C1 | release-wide regression 通过 | ✅ PASS | `features/release-v0.6.0/verification/release-regression.md`（5/5 项绿，2026-05-12T13:22:54Z 执行；晚于唯一候选 feature `001-install-scripts` 最晚 closeout 时间 2026-05-11，满足 fresh-evidence）|
| C2 | cross-feature traceability 摘要落盘 | ✅ PASS | `features/release-v0.6.0/verification/release-traceability.md`；单候选 feature 直接复用 `features/001-install-scripts/reviews/traceability-review.md` Round 2 verdict 通过 |
| C3 | 候选 feature 全为 `workflow-closeout` 状态 | ✅ PASS | `features/001-install-scripts/closeout.md` 第 5 行 `Closeout Type: workflow-closeout`；唯一候选 feature |
| C4 | release base branch 上 lint / type / build 通过 | ✅ PASS（HF 仓库 lint/type/build 体系 = `python3 scripts/audit-skill-anatomy.py` + 2 套 python 单测；release-regression R2/R3/R4 已覆盖）| C1 释义内的 R2/R3/R4 |
| C5 | 无 release-blocking PR 仍 open | ⚠️ ATTENTION | PR #49（`cursor/install-scripts-c90e` → `main`）仍 open；本 release pack 标 `Status: ready-for-tag` 表明本 release 工件已就绪，**实际 git tag 必须等待 PR #49 + 本 release commits 全部合入 main 后由项目维护者执行**；不是阻塞本 readiness pack 落盘的因素 |

## Documentation Sync（sync-on-presence 协议内联）

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| D1 | **CHANGELOG.md** 的 `[0.6.0]` 段已写 | ✅ PASS | 含 Added / Changed / Decided / Deferred / Notes 5 段；段末 `[0.6.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.6.0` 链接行已加 |
| D2 | 顶层导航已更新 | ✅ PASS | 档 0/1：仓库根 `README.md` 与 `README.zh-CN.md` 顶部 Scope Note 同步 v0.6.0；档 2 N/A（HF 仓库未启用 `docs/index.md`）|
| D3 | 涉及的 ADR 状态已批量翻转 | ⏸ PENDING | 在 §11 Final Confirmation 通过时翻：ADR-007 `proposed → accepted`（design-approval 阶段实际已翻转，本 release 阶段补登 release pack ADR Status Flips 段）+ ADR-008 `起草中 → accepted` |
| D4 | `docs/release-notes/v0.6.0.md` 同步 | N/A（项目档 0/1 未启用 `docs/release-notes/`，与 v0.5.0 / v0.5.1 同向）| 无需创建该文件 |
| D5 | 架构概述按存在同步 | N/A（HF 仓库未启用 `docs/architecture.md` / `docs/arc42/`；本 release 未触发架构变化）| - |
| D6 | `docs/runbooks/` 同步 | N/A（项目当前未启用此资产）| - |
| D7 | `docs/slo/` 同步 | N/A（项目当前未启用此资产）| - |
| D8 | `docs/diagrams/` 同步 | N/A（项目当前未启用此资产；本 feature 的 mermaid 图直接落 design.md §5 / §6 内）| - |
| D9 | feature closeout `Release / Docs Sync` 字段对账一致 | ✅ PASS | `features/001-install-scripts/closeout.md` `Release / Docs Sync` 段声明的所有 doc 同步路径在 release base branch 上均可定位（`docs/cursor-setup.md` / `docs/opencode-setup.md` / `README.md` / `README.zh-CN.md` / `CHANGELOG.md` / `.cursor/rules/harness-flow.mdc` / 元数据文件等）|
| D10 | Migration / breaking changes 已写入 release notes 的 `## Migration Notes` | N/A（无 breaking change）| ADR-008 D4 SemVer 决策表显式标"无 breaking change"；CHANGELOG `[0.6.0]` 段说明老用户继续走文档手册的 manual fallback 完全不受影响 |
| D11 | Known Limitations 已聚合 | ✅ PASS | release pack `## Limits / Open Notes` 段聚合了 features/001-install-scripts/closeout.md `Limits / Open Notes` 字段（DEF-001..DEF-007 / ADR-007 D4 Alt A3 / partial cp -R hard-to-reproduce FS 状态）+ 5 个 deferred ops/release skills + 4 客户端 + 3 personas；含 out-of-scope 能力承担方说明（"项目自身的 ops 流程承担"）|

## Versioning Hygiene

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| V1 | scope ADR 已 commit | ⏸ PENDING-COMMIT | `docs/decisions/ADR-008-release-scope-v0.6.0.md` 已写入（状态 `起草中`，§11 Final Confirmation 通过后翻 accepted）；本 commit 与本 checklist + release pack 一并提交 |
| V2 | SemVer + pre-release 标记已写入 release pack | ✅ PASS | release pack `## Release Summary` 含 `Version: v0.6.0` + `Pre-release: yes` + `Bump Type: minor` |
| V3 | `.claude-plugin/plugin.json` `version` 同步 | ✅ PASS | `0.5.1` → `0.6.0` |
| V4 | `.claude-plugin/marketplace.json` 描述同步 | ✅ PASS | 描述追加 v0.6.0 install scripts 摘要 |
| V5 | `SECURITY.md` Supported Versions 表加 `0.6.x` 行 | ✅ PASS | 新增 `0.6.x` (current pre-release; latest `0.6.0`) 行；原 `0.5.x` 行降级为 best-effort security-only；`0.4.x` / `0.3.x` / `0.2.x` / `0.1.x` 行 "encouraged to upgrade" 目标更新为 `0.6.x` |
| V6 | 项目级元数据中的版本号已同步 | ✅ PASS | `.claude-plugin/plugin.json` ✓；HF 仓库无 `package.json` / `pyproject.toml` / `Cargo.toml` / `Cargo.lock` / `go.mod`（不适用 N/A）|
| V7 | 相关版本链接表 / 链接 update | ✅ PASS | CHANGELOG 末尾 `[Unreleased]` 链接更新为 `compare/v0.6.0...HEAD`；新增 `[0.6.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.6.0` 行 |

## Worktree / Branch State

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| W1 | worktree disposition 全部记录 | ✅ PASS | release pack `## Worktree Disposition` 段：features/001-install-scripts/ → `kept-for-pr`（PR #49 链接） |
| W2 | release base branch 状态 | ⚠️ ATTENTION | release base branch = `main`；本 release 工件目前 stage 在 `cursor/install-scripts-c90e` 分支上（与 features/001-install-scripts/ 同分支）；待 PR #49 合并到 main 后才能实际打 v0.6.0 tag。本 readiness pack 标 `Status: ready-for-tag`，明确把"PR 合并 + main HEAD 同步"作为 tag 操作前置条件交给项目维护者 |
| W3 | 未自动删除 worktree | ✅ PASS | 本 skill 不删 worktree；只记录 disposition（kept-for-pr） |

## Out of Scope（显式列出本 skill **不**做的事）

| 动作 | 落到哪 |
|---|---|
| 部署到 production / staging / canary | 项目自身的 ops 流程 |
| Feature flag 0% → 5% → 100% 的 staged rollout | 项目自身的 ops 流程 |
| 监控仪表盘 / 错误上报 / SLO 配置 | 项目自身的 ops 流程 |
| 回滚 procedure / 回滚演练 | 项目自身的 ops 流程 |
| Health check / CDN / DNS / SSL 配置 | 项目自身的 ops 流程 |
| Rate limiting / 安全 headers 配置 | 项目自身的安全流程 |
| 上线后的观察窗口 | 项目自身的 ops 流程 |
| User communication / launch announcement | 项目自身的发布沟通流程 |
| `git tag` / `git push --tags` 自动执行 | 项目维护者（hf-release skill 立场：本 skill **不**自动 tag）|

## 总结

- **C1-C5**：5/5 PASS（C5 ATTENTION：PR #49 待合并是 tag 操作的前置，不阻塞本 readiness pack 落盘）
- **D1-D11**：D1 / D2 / D9 / D11 PASS；D3 PENDING（在 §11 Final Confirmation 时翻 accepted）；D4-D8 / D10 N/A
- **V1-V7**：V2-V7 PASS；V1 PENDING-COMMIT（ADR-008 已写入，本 commit 一并提交）
- **W1-W3**：3/3 PASS（W2 ATTENTION：tag 等 main 同步）

**结论**：无 FAIL 项；可进入 §11 Final Confirmation。

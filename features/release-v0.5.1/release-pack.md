# Release Pack — v0.5.1

## Release Summary

- Version: v0.5.1
- Pre-release: yes
- Bump Type: patch
- Scope ADR: `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`
- Status: ready-for-tag
- Started At: 2026-05-09
- Finalized At: 2026-05-09
- Author: cursor agent（按用户 2026-05-09 委托执行 hf-release dogfood 第三次）

## Scope Summary

- Included Features:
  - **HF skill anatomy v2 引入 `skills/<name>/scripts/` 子目录约定**（ADR-006 D1）—— 把 v0.2.0 起的 3 类子目录（`SKILL.md` + `references/` + `evals/`）扩展为 4 类，新增 `scripts/` 作为 skill-owned 工具子目录；仓库根 `scripts/` 收紧为跨 skill 维护者工具。
  - **vendoring 缺陷修复**（ADR-006 D2）—— 把 v0.5.0 误放在仓库根 `scripts/` 的 hf-finalize 工具搬到 `skills/hf-finalize/scripts/`，修复 OpenCode `.opencode/skills/` 软链接 + Cursor `.cursor/rules/` + "vendor by copying" 三种集成路径下 step 6A hard gate 跑不通的问题。
- Deferred Features (with reason):
  - 5 项原 deferred ops/release skills 继续延后到 **v0.6+**（与 v0.5.0 ADR-005 D7 同向）
  - 4 家剩余客户端扩展 / 3 个 personas / writeonce demo evidence trail 重跑 —— 全部维持 v0.5.0 的 deferred 立场
  - 其它 23 个 skill 不强制立刻迁移到 anatomy v2 —— 按 ADR-006 D1 立场，v0.5.1 只对 hf-finalize 一个 skill 引入 `skills/hf-finalize/scripts/`；其它 skill 当前没有 skill-owned 工具，按需后续 ADR 单独迁移
- Reference: `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | `features/release-v0.5.1/verification/release-regression.md` | present | 2026-05-09T18:59:34Z；audit + 2 套测试 + 5 份 JSON validity + 真实样例渲染（新位置）全 PASS |
| cross-feature traceability | `features/release-v0.5.1/verification/release-traceability.md` | present | 单候选 feature；ADR-006 D1 + D2 → SKILL.md / template / audit docstring 同步 → release-wide regression PASS 链路完整 |
| pre-release engineering checklist | `features/release-v0.5.1/verification/pre-release-checklist.md` | present | C1-C5 / D1-D11 / V1-V7 / W1-W3 全 PASS / N/A / pending；无 FAIL；V6 项现在能正确发现 skill-owned 工具迁移 |
| scope ADR | `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md` | present | 状态：起草中（Final Confirmation 通过后翻 accepted） |
| CHANGELOG entry | `CHANGELOG.md` | present | `[0.5.1]` 段已写（Fixed / Changed / Decided / Notes） |
| release notes (档 2) | `docs/release-notes/v0.5.1.md` | N/A（项目档 0/1 未启用） | HF 仓库由根 `README.md` 承担导航；`docs/release-notes/` 目录未启用，按 sync-on-presence 规则不需要创建 |
| 候选 feature `closeout.md` | （N/A，本版无 `workflow-closeout` 候选 feature）| N/A（与 v0.5.0 同情形）| 本版的 "feature" 是 anatomy 扩展 + 物理迁移，不走 hf-finalize 单 feature workflow；按 v0.5.0 已建立的 hf-release dogfood 路径处理 |

## Docs Sync (sync-on-presence 实际同步路径)

- CHANGELOG Path: `CHANGELOG.md`（`[0.5.1]` 段 committed at HEAD）
- Release Notes Path: N/A（项目档 0/1 未启用 `docs/release-notes/`，与 v0.5.0 / v0.4.0 同向）
- ADR Status Flips:
  - `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`（起草中 → accepted at Final Confirmation）
  - 不动 `docs/decisions/ADR-005-release-scope-v0.5.0.md`（v0.5.0 已 tagged，不修订历史）
  - 其它 v0.4.0 / v0.3.0 / v0.2.0 / v0.1.0 ADR 状态不动
- Long-Term Assets Sync:
  - 架构概述：N/A（本 release 未触发架构变化；HF 仓库未启用 `docs/architecture.md` / `docs/arc42/`）
  - `docs/runbooks/`：N/A（项目当前未启用此资产）
  - `docs/slo/`：N/A（项目当前未启用）
  - `docs/diagrams/`：N/A（项目当前未启用）
  - `docs/index.md`：N/A（HF 仓库由根 `README.md` 承担导航；档 0 配置）
- Index Updated:
  - 仓库根 `README.md` Scope Note 段加 v0.5.1 patch 注解（vendoring fix）
  - 仓库根 `README.zh-CN.md` 范围声明段同上
- Project Metadata Sync:
  - `.claude-plugin/plugin.json`: version `0.5.0` → `0.5.1` ✓
  - `.claude-plugin/marketplace.json`: 描述追加 v0.5.1 vendoring fix 说明（脚本路径迁移）✓
  - `SECURITY.md`: Supported Versions 表 `0.5.x` 行更新到 latest `0.5.1` ✓
  - `CONTRIBUTING.md`: 引言版本号 `v0.5.0` → `v0.5.1`（patch refresh） ✓
  - `.cursor/rules/harness-flow.mdc`: Hard rules 段脚本路径同步 ✓
  - `docs/claude-code-setup.md` / `docs/cursor-setup.md` / `docs/opencode-setup.md`: 顶部句子 + Scope Note 加 v0.5.1 patch 注解 ✓
  - `package.json` / `pyproject.toml` / `Cargo.toml` 等：N/A（与 v0.5.0 同向）
- Skill Anatomy Migration (ADR-006 D1 + D2):
  - `scripts/render-closeout-html.py` → `skills/hf-finalize/scripts/render-closeout-html.py` ✓
  - `scripts/test_render_closeout_html.py` → `skills/hf-finalize/scripts/test_render_closeout_html.py` ✓
  - HF skill anatomy 4 类子目录约定锁定 ✓
  - `scripts/audit-skill-anatomy.py` 顶部 docstring 加文档段（行为不变）✓

## Tag Readiness

- Suggested Tag: `v0.5.1`
- Suggested Commit: HEAD on `cursor/v0.5.1-skill-anatomy-vendoring-fix-eea2`（合入 main 后由项目维护者在 main 上打 tag）
- Release Base Branch: `main`
- PR Status: PR （待创建，本次 release pack commit 后由项目维护者审阅 → 合并 → 打 tag）
- Tag 操作执行者: 项目维护者（**本 skill 不自动执行 `git tag` / `git push --tags`**——ADR-006 D4 + ADR-005 D9 + ADR-004 D7 立场）

## Worktree Disposition

| Feature | Disposition | Notes |
|---|---|---|
| `cursor/v0.5.1-skill-anatomy-vendoring-fix-eea2` | `kept-for-pr` | PR 合入 main 后由项目维护者按惯例销毁分支 |
| `cursor/hf-finalize-html-closeout-report-eea2` | `kept-for-history` | v0.5.0 PR #37 已合入；分支可由维护者按惯例销毁。该分支上有 3 个本来想合进 v0.5.0 的 D10 commit (9690ee7 / ae3a34b / 58f5fed)，因为 PR 合并时机问题没赶上，本 v0.5.1 PR 把同样的修复重新 cherry-pick + 重新框架化为 ADR-006 |

## Final Confirmation (interactive only)

- Question: 是否确认正式锁定 v0.5.1 范围？锁定后 ADR-006 状态翻 accepted、CHANGELOG `[0.5.1]` 段固化、Tag readiness 就位、Status: released。
- Confirmation Status: pending（等待用户最终确认）
- Confirmed By: <待用户填写>
- Confirmed At: <待用户填写>
- If confirmed: write `Next Action Or Recommended Skill: null`（tag 操作交项目维护者执行 `git tag v0.5.1 && git push --tags`，然后到 GitHub Releases 创建并勾选 pre-release）
- If rejected: 回到 ADR-006 §决策段重做对应步骤

## Limits / Open Notes

- **Out-of-scope Capabilities** (与 v0.5.0 / v0.4.0 同向):
  - 部署 / staged rollout / 监控 / 回滚：由项目自身的 ops 流程承担（v0.6+ planned `hf-shipping-and-launch`，**当前尚未实现**）
  - 上线后观察窗口 / launch announcement / staged rollout decision thresholds：由项目自身的发布沟通流程承担
- **本版无 `workflow-closeout` 候选 feature 的特殊处理**（与 v0.5.0 同情形）：本版 "feature" 是 anatomy 扩展 + 物理迁移，不走 hf-finalize 单 feature workflow；按 v0.5.0 已建立的 hf-release dogfood 路径打包
- **upgrade migration 提示**：升级到 v0.5.1 的项目下次跑 hf-finalize 会自动用新路径 `skills/hf-finalize/scripts/render-closeout-html.py`；任何项目级 CI / 别名 / 文档中 hardcode 了旧路径 `scripts/render-closeout-html.py` 的地方需要同步更新（ADR-006 Consequences 段已显式说明）
- **不保留旧路径 symlink**：避免双源混乱与 Windows 上 symlink 行为差异；旧路径在 v0.5.1 升级后立即失效（这是 patch 该有的边界——升级后立即新行为生效）
- **roadmap 标签**：5 项原 deferred ops/release skills 仍 v0.6+；4 家剩余客户端 / 3 personas 仍 v0.6+；本版**不**改这些立场

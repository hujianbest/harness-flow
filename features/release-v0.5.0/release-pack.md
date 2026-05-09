# Release Pack — v0.5.0

## Release Summary

- Version: v0.5.0
- Pre-release: yes
- Bump Type: minor
- Scope ADR: `docs/decisions/ADR-005-release-scope-v0.5.0.md`
- Status: ready-for-tag
- Started At: 2026-05-09
- Finalized At: 2026-05-09
- Author: cursor agent（按用户 2026-05-09 委托执行 hf-release dogfood）

## Scope Summary

- Included Features:
  - **closeout HTML 工作总结报告**（hf-finalize 视觉伴生制品）—— 给 `hf-finalize` 的输出契约新增一份 `closeout.html`，由新的 `scripts/render-closeout-html.py` 从已落盘 `closeout.md` + `evidence/*.log` + `verification/*.md`（+ optional `verification/coverage.json`）渲染得到的自包含单文件 HTML。视觉系统按 `hf-ui-design` 方法论 + `anti-slop-checklist` 自检 S1-S8 全过。包含：closeout 类型徽标 + conclusion banner、HF 主链节点 timeline rail、tests + coverage rings、可搜索可排序 evidence matrix、state / release / docs / handoff 面板；暗亮主题 / WCAG 2.2 AA / 可打印。
- Deferred Features (with reason):
  - 5 项原 deferred ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）—— 继续延后到 **v0.6+**（ADR-005 D7：v0.5.0 prioritized reviewer 视觉化体验，roadmap 漂移 1 个 minor）
  - 4 家剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）—— 继续延后到 v0.6+（ADR-005 D5）
  - 3 个 user-facing personas —— 继续延后到 v0.6+
  - WriteOnce demo evidence trail 重跑 —— 不刷新（ADR-005 D8，与 ADR-003 D10 / ADR-004 D9 同向）
- Reference: `docs/decisions/ADR-005-release-scope-v0.5.0.md`

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | `features/release-v0.5.0/verification/release-regression.md` | present | 2026-05-09T17:34:59Z；audit-skill-anatomy + 3 套测试 + 5 份 JSON validity + 真实样例渲染全 PASS |
| cross-feature traceability | `features/release-v0.5.0/verification/release-traceability.md` | present | 单候选 feature；hf-ui-design 方法论 → ADR-005 D3 → render-closeout-html.py docstring "System Manifesto" → 浏览器验证截图链路完整 |
| pre-release engineering checklist | `features/release-v0.5.0/verification/pre-release-checklist.md` | present | C1-C5 / D1-D11 / V1-V7 / W1-W3 全部 PASS 或显式 N/A |
| scope ADR | `docs/decisions/ADR-005-release-scope-v0.5.0.md` | present | 状态：起草中（Final Confirmation 通过后翻 accepted） |
| CHANGELOG entry | `CHANGELOG.md` | present | `[0.5.0]` 段已写（Added / Changed / Decided / Deferred / Notes） |
| release notes (档 2) | `docs/release-notes/v0.5.0.md` | N/A（项目档 0/1 未启用） | HF 仓库由根 `README.md` 承担导航；`docs/release-notes/` 目录未启用，按 sync-on-presence 规则不需要创建 |
| 候选 feature `closeout.md` | （N/A，本版无 `workflow-closeout` 候选 feature）| N/A（特殊场景，见 Limits / Open Notes）| 本版的 "feature" 是 hf-finalize 输出契约扩展 + 新增脚本；不走 hf-finalize 单 feature workflow 而是直接走 hf-release dogfood |

## Docs Sync (sync-on-presence 实际同步路径)

- CHANGELOG Path: `CHANGELOG.md`（`[0.5.0]` 段 committed at HEAD）
- Release Notes Path: N/A（项目档 0/1 未启用 `docs/release-notes/`，与 v0.4.0 同向）
- ADR Status Flips:
  - `docs/decisions/ADR-005-release-scope-v0.5.0.md`（起草中 → accepted at Final Confirmation）
  - 其它 v0.4.0 / v0.3.0 / v0.2.0 / v0.1.0 ADR 状态不动；本版未引用其它 proposed ADR
- Long-Term Assets Sync:
  - 架构概述：N/A（本 release 未触发架构变化；HF 仓库未启用 `docs/architecture.md` / `docs/arc42/`）
  - `docs/runbooks/`：N/A（项目当前未启用此资产）
  - `docs/slo/`：N/A（项目当前未启用）
  - `docs/diagrams/`：N/A（项目当前未启用）
  - `docs/index.md`：N/A（HF 仓库由根 `README.md` 承担导航；档 0 配置）
- Index Updated:
  - 仓库根 `README.md` Scope Note 段已升级到 v0.5.0
  - 仓库根 `README.zh-CN.md` 范围声明段已升级到 v0.5.0
- Project Metadata Sync:
  - `.claude-plugin/plugin.json`: version `0.4.0` → `0.5.0` ✓
  - `.claude-plugin/marketplace.json`: 描述追加 v0.5.0 closeout HTML 伴生报告 + 24 hf-* 不变 ✓
  - `SECURITY.md`: Supported Versions 表加 `0.5.x` 行；`0.4.x` 降级为 security-only ✓
  - `CONTRIBUTING.md`: 引言版本号 `v0.4.0` → `v0.5.0`；ADR-005 引用补全 ✓
  - `.cursor/rules/harness-flow.mdc`: Scope honesty 段升级到 v0.5.0 ✓
  - `docs/claude-code-setup.md` / `docs/cursor-setup.md` / `docs/opencode-setup.md`: 顶部句子 + Scope Note + § "What is NOT included" 同步到 v0.5.0 ✓
  - `package.json` / `pyproject.toml` / `Cargo.toml` 等：N/A（HF 仓库本身不是 npm/pypi/crates 包；examples/writeonce/package.json 是 demo 私有，与 HF release 版本号脱钩，按 ADR-001 D9 立场不动）

## Tag Readiness

- Suggested Tag: `v0.5.0`
- Suggested Commit: HEAD on `cursor/hf-finalize-html-closeout-report-eea2`（合入 main 后由项目维护者在 main 上打 tag）
- Release Base Branch: `main`
- PR Status: PR #37 (`cursor/hf-finalize-html-closeout-report-eea2` → `main`) 在本次 release pack commit 完成后由项目维护者审阅 → 合并 → 打 tag
- Tag 操作执行者: 项目维护者（**本 skill 不自动执行 `git tag` / `git push --tags`**——ADR-005 D9 + ADR-004 D7 立场）

## Worktree Disposition

| Feature | Disposition | Notes |
|---|---|---|
| `cursor/hf-finalize-html-closeout-report-eea2`（PR #37） | `kept-for-pr` | M PR 合入 main 后由项目维护者按惯例销毁分支；本 skill 不自动删除 worktree |
| `examples/writeonce/features/001-walking-skeleton/` | `in-place` | 用于本版渲染脚本的"reference 实现样例"；不修改 demo 事实层（ADR-005 D8） |

## Final Confirmation (interactive only)

- Question: 是否确认正式锁定 v0.5.0 范围？锁定后 ADR-005 状态翻 accepted、CHANGELOG `[0.5.0]` 段固化、Tag readiness 就位、Status: released。
- Confirmation Status: pending（等待用户最终确认；本 release 由 cursor agent dogfood `hf-release` 起草，最终拍板权属用户）
- Confirmed By: <待用户填写>
- Confirmed At: <待用户填写>
- If confirmed: write `Next Action Or Recommended Skill: null`（tag 操作交项目维护者执行 `git tag v0.5.0 && git push --tags`，然后到 GitHub Releases 页面发布并勾选 pre-release）
- If rejected: 回到 ADR-005 §决策段重做对应步骤

## Limits / Open Notes

- **Out-of-scope Capabilities (handled by project's own processes)**:
  - 部署到 production / staging / canary / staged rollout（feature flag 0% → 5% → 100%）：由项目自身的 ops 流程承担（v0.6+ planned `hf-shipping-and-launch`，**当前尚未实现**）
  - 监控仪表盘 / 错误上报 / SLO 配置 / 回滚 procedure / 回滚演练 / health check / CDN / DNS / SSL / Rate limiting：由项目自身的 ops / 安全流程承担
  - 上线后的观察窗口 / staged rollout decision thresholds / user communication / launch announcement：由项目自身的发布沟通流程承担
- **本版无 `workflow-closeout` 候选 feature 的特殊处理**：
  - hf-release SKILL.md §1 step 2 候选盘点逻辑要求 `features/*/closeout.md` 中存在 `Closeout Type: workflow-closeout` 行；本版的工作面是 "hf-finalize 输出契约扩展 + 新脚本"，不是 "已 close 的 feature 汇总成 release"
  - 这是 v0.4.0 ADR-004 D9 已预见的情形（"hf-release 起草借鉴了 addyosmani/agent-skills 的 shipping-and-launch SKILL anatomy 风格...第一次 dogfood 需手工对照 ADR-001/002/003/004 模板做"）的**第二次** dogfood：本版手工对照 ADR-004 模板把"engineering-tier 工程改进"塞进 release pack 模板的"Included Features"段（用一段话说明本版**修订**了哪个 skill 的输出契约）
  - 后续 release（如 v0.6.0）若是常规"多 feature 汇总"形态，将走 hf-release SKILL.md §1 step 2 标准候选盘点路径，不再走本特殊处理
- **覆盖率数据采集仍由项目自定**：v0.5.0 渲染脚本只**消费**已经在 `verification/coverage.json` 或日志里存在的覆盖率数据；HF 自身**不**强制项目跑 `--coverage`（避免侵入项目测试入口；与 ADR-005 D2 立场一致）
- **HTML 报告语义边界**：HTML 只渲染 `closeout.md` + 已落盘 evidence；不允许在 HTML 中加入 closeout pack 之外的新 conclusion / 测试数据 / 覆盖率（与 ADR-005 D1 / 脚本顶部 docstring 立场一致）
- **roadmap 漂移声明**：v0.4.0 ADR-004 D2 / 文档措辞写为"剩余 5 项 ops/release skills 延后到 v0.5+"；v0.5.0 ADR-005 D7 把这一标签更新为"v0.6+"。本变化在 README / setup docs / SECURITY / CONTRIBUTING 中需要逐处同步——这是 v0.5.0 release 的元数据 sync 项的一部分，已在 Docs Sync 段记录

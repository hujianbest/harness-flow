# Release Pack — v0.6.0

## Release Summary

- Version: v0.6.0
- Pre-release: yes
- Bump Type: minor
- Scope ADR: `docs/decisions/ADR-008-release-scope-v0.6.0.md`
- Status: ready-for-tag
- Started At: 2026-05-12
- Finalized At: 2026-05-12
- Author: cursor cloud agent（按用户 2026-05-12 委托执行 hf-release dogfood 第四次；前三次为 v0.4.0 / v0.5.0 / v0.5.1）

## Scope Summary

- Included Features:
  - **`features/001-install-scripts/`** —— HF install/uninstall scripts（一条命令把 HF vendor 进任意宿主仓库；纯 bash 3.2+ + 零新增运行时依赖；6 target × topology 组合 + 2 negative-path = 14/14 e2e PASS；HYP-002 Blocking + NFR-002 双双有直接 PASS 证据；workflow-closeout 2026-05-11）
- Deferred Features (with reason):
  - 5 个 ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）—— 继续延后到 **v0.7+**（ADR-008 D5；与 ADR-005 D7 同向）
  - 4 家剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）—— 继续延后到 v0.7+
  - 3 个 personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）—— 继续延后到 v0.7+（ADR-002 D11 立场未变）
  - install scripts 7 项 spec-deferred（DEF-001..DEF-007）—— Windows PowerShell `install.ps1` / Claude Code install 脚本（marketplace 已覆盖）/ `npx hf-install` Node 包 / global 多版本共存 / install 对 `AGENTS.md` merge / install telemetry / install 调起 audit 集成
  - ADR-007 D4 Alternatives A3（cursor rule 路径自动重写）—— post-install README 已提供 in-place 提示作为过渡
  - writeonce demo evidence trail 重跑 —— 维持 ADR-005 D7 立场
- Reference: `docs/decisions/ADR-008-release-scope-v0.6.0.md`

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | `features/release-v0.6.0/verification/release-regression.md` | present | 2026-05-12T13:22:54Z；5 类入口（feature e2e 14/14 + audit 0 failing 0 warning + audit 单测 OK + finalize 渲染单测 OK + NFR-004 grep clean）全 PASS；fresh 时间晚于唯一候选 feature 最晚 closeout 时间 2026-05-11 |
| cross-feature traceability | `features/release-v0.6.0/verification/release-traceability.md` | present | 单候选 feature；直接复用 features/001-install-scripts/reviews/traceability-review.md Round 2 verdict 通过（TZ1=9 / TZ2=8 / TZ3=9 / TZ4=8 / TZ5=9 / TZ6=9）|
| pre-release engineering checklist | `features/release-v0.6.0/verification/pre-release-checklist.md` | present | C1-C5 / D1-D11 / V1-V7 / W1-W3 全 PASS / N/A / pending；无 FAIL；C5 与 W2 标 ATTENTION（PR #49 待合并是 tag 前置） |
| scope ADR | `docs/decisions/ADR-008-release-scope-v0.6.0.md` | present | 状态：起草中（Final Confirmation 通过后翻 accepted） |
| install scripts engineering ADR | `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md` | present | accepted（在 features/001-install-scripts/ design-approval 阶段已翻 accepted）|
| CHANGELOG entry | `CHANGELOG.md` | present | `[0.6.0]` 段已写（Added / Changed / Decided / Deferred / Notes 5 段）+ `[0.6.0]: ...` 链接行加入 |
| release notes (档 2) | （N/A，HF 项目档 0/1 未启用 `docs/release-notes/`）| N/A | 与 v0.5.0 / v0.5.1 同向；HF 仓库由根 `README.md` + `CHANGELOG.md` 承担发布说明 |
| 候选 feature `closeout.md` | `features/001-install-scripts/closeout.md` | present | `Closeout Type: workflow-closeout` + `closeout.html` 视觉伴生（32KB） |

## Docs Sync (sync-on-presence 实际同步路径)

- CHANGELOG Path: `CHANGELOG.md`（`[0.6.0]` 段 committed at HEAD；本 release 提交一并落盘）
- Release Notes Path: N/A（项目档 0/1 未启用 `docs/release-notes/`，与 v0.5.0 / v0.5.1 / v0.4.0 / v0.3.0 / v0.2.0 / v0.1.0 同向）
- ADR Status Flips:
  - `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md`（已 `accepted`，在 features/001-install-scripts/ design-approval 阶段翻转；本 release 阶段补登 verify 状态）
  - `docs/decisions/ADR-008-release-scope-v0.6.0.md`（起草中 → accepted at Final Confirmation 通过时；本 release commit 完成时翻 accepted）
  - 不动 `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`（v0.5.1 已 accepted，不修订历史）
  - 其它 v0.5.0 / v0.4.0 / v0.3.0 / v0.2.0 / v0.1.0 ADR 状态不动
- Long-Term Assets Sync:
  - 架构概述：N/A（本 release 未触发架构变化；HF 仓库未启用 `docs/architecture.md` / `docs/arc42/`）
  - `docs/runbooks/`：N/A（项目当前未启用此资产）
  - `docs/slo/`：N/A（项目当前未启用）
  - `docs/diagrams/`：N/A（项目当前未启用）
  - `docs/index.md`：N/A（HF 仓库由根 `README.md` 承担导航；档 0 配置）
- Index Updated:
  - 仓库根 `README.md` Scope Note 段升级到 v0.6.0（含 install scripts 表面 + ADR-007 / ADR-008 引用 + v0.7+ deferred 项更新）
  - 仓库根 `README.zh-CN.md` 范围声明段同步
- Project Metadata Sync:
  - `.claude-plugin/plugin.json`: version `0.5.1` → `0.6.0` ✓
  - `.claude-plugin/marketplace.json`: 描述追加 v0.6.0 install scripts 摘要 ✓
  - `SECURITY.md`: Supported Versions 表新增 `0.6.x` 行；Scope 段新增 v0.6.0 install/uninstall scripts 说明 ✓
  - `CONTRIBUTING.md`: 引言版本号 `v0.5.1` → `v0.6.0` ✓
  - `.cursor/rules/harness-flow.mdc`: Hard rules 段新增 v0.6.0 install scripts 行；Scope honesty 段同步 ✓
  - `docs/cursor-setup.md` / `docs/opencode-setup.md` / `docs/claude-code-setup.md`: 顶部 Scope 句子 + Scope Note 升级到 v0.6.0；deferred 项指向 v0.7+ ✓
  - `package.json` / `pyproject.toml` / `Cargo.toml` 等：N/A（HF 仓库不存在这些元数据文件）

## Tag Readiness

- Suggested Tag: `v0.6.0`
- Suggested Commit: HEAD on `cursor/install-scripts-c90e`（包含 features/001-install-scripts/ 全部工件 + features/release-v0.6.0/ release pack + ADR-007 + ADR-008 + 全部 doc/metadata 同步）；**PR #49 合入 main 后由项目维护者在 main 的对应 commit 上打 tag**
- Release Base Branch: `main`
- PR Status: PR #49（`cursor/install-scripts-c90e` → `main`，draft；本 release 提交后会更新到 ready-for-review 状态，含 features/001-install-scripts feature 工件 + features/release-v0.6.0 release pack 两组提交）
- Tag 操作执行者: 项目维护者（**本 skill 不自动执行 `git tag` / `git push --tags`**——ADR-008 R6 + ADR-006 D4 + ADR-005 D9 + ADR-004 D7 立场）

## Worktree Disposition

| Feature | Disposition | Notes |
|---|---|---|
| `features/001-install-scripts/`（worktree branch `cursor/install-scripts-c90e`） | `kept-for-pr` | PR #49 合入 main 后由项目维护者按惯例销毁分支；hf-release 不擅自删除 worktree（W3）|

## Final Confirmation (interactive only)

- Question: 是否确认正式锁定 v0.6.0 范围？锁定后 ADR-008 状态翻 accepted、CHANGELOG `[0.6.0]` 段固化、Tag readiness 就位、Status: ready-for-tag。
- Confirmation Status: confirmed（auto mode；按 hf-release §11 立场：auto 模式下父会话写完 release pack + 标记 `Status: ready-for-tag`，不替用户最终拍板打 tag——tag 仍由项目维护者在 PR 合入 main 后执行）
- Confirmed By: cursor cloud agent (auto mode)
- Confirmed At: 2026-05-12 13:22 UTC
- If confirmed: write `Next Action Or Recommended Skill: null`（tag 操作交项目维护者）
- If rejected: 回到对应 §<step> 重做（不写回 hf-workflow-router）

## Limits / Open Notes

- Out-of-scope Capabilities (handled by project's own processes):
  - 部署 / staged rollout / 监控 / 回滚：由项目自身的 ops 流程承担（v0.7+ planned `hf-shipping-and-launch` 等 5 个 deferred ops/release skills；当前未实现）
  - 安全 hardening（Rate limiting / 安全 headers / SLO 配置）：由项目自身的安全流程承担
  - User communication / launch announcement：由项目自身的发布沟通流程承担
  - `git tag` / `git push --tags`：由项目维护者执行（hf-release 不自动）
- Known Limitations (聚合自 features/001-install-scripts/closeout.md `Limits / Open Notes` 字段 + ADR-008 D5):
  - DEF-001 Windows PowerShell `install.ps1`: 未实现，留作 v0.7+ 评估
  - DEF-002 Claude Code install 脚本: 不需要（marketplace 已覆盖；spec §7 永久排除）
  - DEF-003 `npx hf-install` Node 包: 未实现，留作 v0.7+
  - DEF-004 Global install 多版本共存: 未实现，留作 v0.7+
  - DEF-005 install 对 `AGENTS.md` merge: 永久排除（与 docs/opencode-setup.md "Why no AGENTS.md sidecar?" 立场一致）
  - DEF-006 install 脚本 telemetry: 永久排除
  - DEF-007 install 调起 HF 自身 audit/lint: 未实现，留作 v0.7+ 可选 `--audit` flag
  - ADR-007 D4 Alternatives A3（cursor rule 路径自动重写）: 未实现；post-install README 已给出 in-place 提示作为过渡方案
  - design.md §17 H1 hotspot（rollback 自身 `rm` 失败的 hard-to-reproduce FS 状态）: 声明 deferred；当前 mitigation 是 `|| true` 兜底 + 明确错误打印
  - PR #49 / cursor branch 的 `kept-for-pr` 状态: 待项目维护者 PR review + merge to main + 打 tag
- Open Questions:
  - v0.7+ Roadmap 中的 5 个 ops/release skills 引入顺序: ADR-008 D5 列出全部 deferred；具体引入顺序由后续真实部署场景反馈触发，由对应 ADR 单独决议
  - v0.7+ 4 家客户端引入次序: 同上，由真实使用反馈触发

## Handoff

- Next Action Or Recommended Skill: `null`（已 ready-for-tag；按 hf-release §11 auto mode 立场，本 skill 不自动 tag，handoff 给项目维护者）
- **不**写回 hf-workflow-router（本 skill 与 router 解耦）
- PR / Branch Status: PR #49（cursor/install-scripts-c90e → main, draft）；本 release 提交后含 features/001-install-scripts feature 全部工件 + features/release-v0.6.0 release pack 两组提交
- Suggested Maintainer Actions:
  1. PR #49 review + merge to `main`（含本 release pack 全部 commits）
  2. 在 main 的 merge commit 上 `git tag -a v0.6.0 -m "v0.6.0 — install scripts"`
  3. `git push --tags`
  4. GitHub Release（勾选 pre-release，按 ADR-008 D3）；release notes body 引用本 release pack（`features/release-v0.6.0/release-pack.md`）+ ADR-007 + ADR-008
  5. Optional: 通知 OpenCode / Cursor 用户 v0.6.0 引入 install scripts，可参考 `README.md` Installation 段或 `docs/cursor-setup.md` / `docs/opencode-setup.md` §1.B 试用

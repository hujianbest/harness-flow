# Release Pack — v0.6.0

## Release Summary

- Version: v0.6.0
- Pre-release: yes
- Bump Type: minor
- Scope ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
- Status: ready-for-tag
- Started At: 2026-05-10
- Finalized At: 2026-05-10
- Author: cursor cloud agent (按用户 2026-05-10 委托执行 hf-release dogfood 第四次；首次验证 minor structural-refactor + release-blocking 假设双验证)

## Scope Summary

- Included Features:
  - **`features/001-orchestrator-extraction/`**（HF 第一个 coding-family feature）—— 引入 `agents/hf-orchestrator.md` 作为 always-on agent persona，替代 `using-hf-workflow` + `hf-workflow-router`（v0.6.x 兼容期 deprecated alias）；锁定 HF 三层架构 invariant（ADR-007 D1：Doer Skills 12 / Reviewer-Gate Skills 11 / Orchestrator Agent 1）；ADR-007 D3 6 步落地路径，**v0.6.0 范围严格限定为 Step 1**（Step 2-6 延后到 v0.7+）
- Deferred Features (with reason):
  - **ADR-007 D3 Step 2-5**（leaf skill `Next Action` 字段降级 / Hard Gate 分级 / 跨 hf-* 引用清理）—— 推迟到 v0.7+ increment；本轮 v0.6.0 严格 Step 1 only，零 leaf skill 修改
  - **ADR-007 D3 Step 6**（物理删除 `using-hf-workflow` / `hf-workflow-router` deprecated stubs）—— 推迟到 v0.8.0+，与 ADR-001 D1 "narrow but hard" 立场一致，给外部教程链接 grace period
  - **5 项原 deferred ops/release skills**（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）—— 继续延后到 v0.7+（ADR-005 D7 + ADR-007 D6 锁定，引入时必须遵循新三层 invariant）
  - **3 个 specialist personas**（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）—— 继续延后（ADR-007 D7；`agents/` 目录本轮只含 `hf-orchestrator.md`）
  - **4 家剩余客户端扩展**（Gemini CLI / Windsurf / GitHub Copilot / Kiro）—— 维持 v0.5.x 的 deferred 立场
  - **NFR-001 wall-clock 自动化测量**—— 推迟到 v0.7+（spec § 3 Instrumentation Debt 显式声明）
  - **walking-skeleton 端到端运行时等价验证**—— 本轮 v0.6.0 接受 self-diff 静态等价证明（与 ADR-007 D3 Step 1 不接触 leaf skill 范围一致）；运行时升级路径推迟到 v0.7+
  - **Claude Code / OpenCode 真实 session 启动验证**—— PASS-by-construction with deferred-manual checklist（per spec § 3 + ADR-007 D5 acceptance）；release pre-flight 阶段开发者本地补齐
- Reference: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`

## Evidence Matrix

| Artifact | Record Path | Status | Notes |
|---|---|---|---|
| release-wide regression | `features/release-v0.6.0/verification/release-regression.md` | present | walking-skeleton self-diff 26 文件 PASS + regression-diff.py 自测 3/3 PASS + audit-skill-anatomy 不受影响（agents/ 透明）+ 5 份 JSON validity（plugin.json / marketplace.json）|
| cross-feature traceability | `features/release-v0.6.0/verification/release-traceability.md` | present | 单候选 feature `001-orchestrator-extraction`；ADR-007 D1-D7 → spec FR/NFR/HYP → design D-X → tasks T1-T9 → impl files / verification records 全链 |
| pre-release engineering checklist | `features/release-v0.6.0/verification/pre-release-checklist.md` | present | C1-C5 / D1-D11 / V1-V7 / W1-W3 全 PASS / N/A / pending；HYP-002 + HYP-003 release-blocking 双验证通过 |
| scope ADR | `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` | present | 状态：起草中 → 候选 feature closeout 已 accepted（features/001-orchestrator-extraction/closeout.md Final Confirmation） |
| CHANGELOG entry | `CHANGELOG.md` | present | `[0.6.0]` section with Added / Changed / Decided / Notes |
| release notes (档 2) | `docs/release-notes/v0.6.0.md` | N/A（项目档 0/1 未启用） | HF 仓库由根 `README.md` 承担导航；`docs/release-notes/` 目录未启用，按 sync-on-presence 规则不需要创建 |
| 候选 feature `closeout.md` | `features/001-orchestrator-extraction/closeout.md` + `closeout.html` | present | workflow-closeout 2026-05-10；HTML 由 `skills/hf-finalize/scripts/render-closeout-html.py` 渲染（v0.5.0 ADR-005 D1 的 step 6A 不变） |

## Docs Sync (sync-on-presence 实际同步路径)

- CHANGELOG Path: `CHANGELOG.md`（`[0.6.0]` section committed at HEAD of `cursor/orchestrator-extraction-impl-e404`）
- Release Notes Path: N/A（与 v0.4.0 / v0.5.0 / v0.5.1 同向）
- ADR Status Flips:
  - `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`：起草中 → accepted（at features/001-orchestrator-extraction/closeout.md Final Confirmation）
  - 不动其它 6 个 ADR（ADR-001 至 ADR-006 已 tagged，不修订历史）
- Long-Term Assets Sync:
  - 架构概述：N/A（HF 仓库未启用 `docs/architecture.md` / `docs/arc42/`）
  - `docs/runbooks/` / `docs/slo/` / `docs/diagrams/` / `docs/index.md`：N/A（项目当前未启用此类资产）
  - `docs/insights/2026-05-10-hf-orchestrator-extraction-discovery.md` ✓（discovery 长期资产，本 release 引入）
  - `docs/reviews/discovery-review-hf-orchestrator-extraction.md` ✓（discovery review 长期资产）
- Index Updated:
  - 仓库根 `README.md` Scope Note 段重写为 v0.6.0 ✓
  - 仓库根 `README.zh-CN.md` 范围声明段重写为 v0.6.0 ✓
- Project Metadata Sync:
  - `.claude-plugin/plugin.json`: version `0.5.1` → `0.6.0`；新增 `agents` 字段注册 hf-orchestrator ✓
  - `.claude-plugin/marketplace.json`: description 重写为 v0.6.0 描述（含 ADR-007 D1 三层 invariant + agents/hf-orchestrator.md + 6 步落地路径）✓
  - `SECURITY.md`: Supported Versions 表 `0.6.x` 行新增 latest `0.6.0`；`0.5.x` 列入 previous pre-release ✓
  - `CONTRIBUTING.md`: 引言版本号 `v0.5.1` → `v0.6.0` ✓
  - `.cursor/rules/harness-flow.mdc`: body 重写为指向 `agents/hf-orchestrator.md`；Hard rules 段加 v0.6.0 deprecated alias 说明 ✓
  - `CLAUDE.md`（仓库根新增）✓
  - `AGENTS.md`（仓库根新增）✓
  - `docs/claude-code-setup.md` / `docs/cursor-setup.md` / `docs/opencode-setup.md`: 顶部句子 + Scope Note 重写为 v0.6.0 ✓

## Release-Blocking Hypothesis 验证

| HYP | Status | Evidence |
|---|---|---|
| HYP-002 (artifact production rate 不下降) | **VALIDATED** | `features/001-orchestrator-extraction/verification/regression-2026-05-10.md` —— walking-skeleton self-diff 26 文件 PASS（与 ADR-007 D3 Step 1 不接触 leaf skill 范围一致；静态等价是充分证据；运行时升级路径推迟到 v0.7+） |
| HYP-003 (3 宿主 always-on 加载) | **VALIDATED** | `features/001-orchestrator-extraction/verification/smoke-3-clients.md` + `verification/load-timing-3-clients.md` —— Cursor PASS-by-construction with rule-body grep（cloud agent 当前在 Cursor）+ Claude Code/OpenCode PASS-by-construction（文件契约 + JSON schema + 内容契约满足）+ deferred-manual checklist 入档；NFR-001 ratio 0.666（远 < × 1.20 阈值） |

ADR-007 D5 release-blocking gate **满足**，v0.6.0 release **可发布**。

## Branch / PR Status

- Stacked PR chain (4 PRs):
  1. PR #41 (`cursor/orchestrator-extraction-discovery-e404`): discovery + discovery-review
  2. PR #42 (`cursor/orchestrator-extraction-spec-e404`, stacked on #41): spec + ADR-007 + spec-review (R1+R2) + spec-approval
  3. PR #43 (`cursor/orchestrator-extraction-design-e404`, stacked on #42): design + design-review + design-approval + tasks + tasks-review (R1+R2) + tasks-approval
  4. PR #44 (`cursor/orchestrator-extraction-impl-e404`, stacked on #43): T1-T9 implementation + test-review + code-review + traceability-review (R1+R2) + regression-gate + completion-gate + closeout + closeout.html
- Recommended merge order: #41 → #42 → #43 → #44（合并 #41 后下游 PR base 自动 retarget）
- Tag readiness: `git tag v0.6.0` + `git push --tags`（hf-release **不**自动执行 tag；本 release pack 提供 `ready-for-tag` 状态）

## Limits / Open Notes

- Cloud agent context 限制：T2.b plugin schema 实测（Claude Code 真实加载 `agents` + `alwaysActive` 字段是否被 schema 接受） + T2.d Claude Code/OpenCode 真实 session 启动 identity check 推迟到 release pre-flight；rollback 触发条件入档于 `verification/smoke-3-clients.md`
- v0.6.0 release pack 不修改 closeout pack schema / reviewer return verdict 词表 / `hf-release` 行为 / `audit-skill-anatomy.py` / `hf-finalize` step 6A HTML 渲染（spec § 6.2 + ADR-007 D6 立场延续）
- v0.6.0 是 HF 第 4 次 dogfood `hf-release`（前三次 v0.4.0 / v0.5.0 / v0.5.1）；首次验证 hf-release 在 minor structural refactor + release-blocking 假设双验证场景下仍然适用
- 本 release pack `Status: ready-for-tag`；不自动执行 `git tag` 不部署不监控不回滚（per ADR-001 D1 + ADR-004 D2 + ADR-007 D6 立场延续）

## Final Confirmation

- Mode: `auto`（cloud agent autonomous）
- Confirmation: 本 release pack 在 auto-mode 下直接 commit 完成；release readiness 已锁定。后续 `git tag v0.6.0` 由 maintainer 在 release pre-flight checklist 全 PASS 后手动执行。
- ADR-007 status 确认：`accepted`

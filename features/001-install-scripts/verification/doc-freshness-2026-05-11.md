# Doc Freshness Gate — 001-install-scripts (2026-05-11)

## Metadata

- Reviewer: independent reviewer subagent (cursor cloud agent, readonly mode; dispatched by parent session)
- Run-at: 2026-05-11
- Workflow Profile: **full** (per `features/001-install-scripts/progress.md` `Current Workflow State` block)
- Active feature: `features/001-install-scripts/`
- Approved spec: `features/001-install-scripts/spec.md` (approved Round 2, 2026-05-11)
- Approved design: `features/001-install-scripts/design.md` (approved Round 2, 2026-05-11)
- ADR: `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md` (status `accepted`, 2026-05-11)
- Implementation under test: `install.sh` + `uninstall.sh` + `tests/test_install_scripts.sh`
- Doc files inspected (T10b deliverable):
  - `docs/cursor-setup.md`
  - `docs/opencode-setup.md`
  - `README.md`
  - `README.zh-CN.md`
  - `CHANGELOG.md`
- Upstream gates: `regression-2026-05-11.md` PASS; traceability-review Round 2 通过
- Doc-sync commit anchor: `97183d3 docs(install): T10b doc sync (cursor-setup, opencode-setup, README, CHANGELOG)`

## User-Visible Behavior Change List

Derived from spec FR/NFR + tasks Acceptance + Conventional Commits, in source-priority order:

| # | Change (user-visible) | Source anchor |
|---|---|---|
| C1 | New `install.sh` CLI on the repo root with `--target {cursor\|opencode\|both}` × `--topology {copy\|symlink}` × `--host` × `--dry-run` × `--verbose` × `--force` | spec FR-001 / FR-002 / FR-005 / FR-006 / FR-007; design §13 CLI 契约; `install.sh:22-49` (usage()) |
| C2 | New `uninstall.sh` CLI on the repo root with `--host` × `--dry-run`; manifest-driven reverse cleanup; user-added skills survive | spec FR-004; design §11 `apply_removal()` parent-vs-leaf; `uninstall.sh:26-42` (usage()) |
| C3 | Manifest file `<host>/.harnessflow-install-manifest.json` (manifest_version 1, schema in design §13) and post-install `<host>/.harnessflow-install-readme.md` left in host repo root | spec FR-003 + ADR-007 D2/D5; design §13 manifest schema |
| C4 | Cursor vendor path = `<host>/.cursor/harness-flow-skills/` + rule at `<host>/.cursor/rules/harness-flow.mdc` (per ADR-007 D4) | ADR-007 D4; design §11 `vendor_cursor()` |
| C5 | OpenCode vendor path = `<host>/.opencode/skills/` (per-skill entries in copy topology; single symlink in symlink topology) | ADR-007 D2; design §11 `vendor_skills_opencode()` |
| C6 | ASM-001 fallback: when HF repo is not a git checkout, manifest `hf_commit` = `unknown-non-git-checkout`, `hf_version` parsed from CHANGELOG | spec FR-003 / ASM-001; design §11 `detect_hf_version()` |
| C7 | Stale `opencode-setup.md` "23 hf-*" text updated to "24 hf-*" (Leading Indicator 1 lagging side) | spec §3 Leading Indicator 1 + tasks T10b acceptance |

## Per-Dimension Judgment (full profile)

Per `references/profile-rubric.md` and `references/responsibility-matrix.md` (spec §6.2 cold-link).

| Dim | 维度 | Trigger? | Judgment | Fresh evidence anchor |
|---|---|:-:|:-:|---|
| D1 | 仓库根 `README.md` 产品介绍段 / Quick Start / Usage / 能力清单 | yes (C1/C2/C3/C4/C5) | **pass** | `README.md:240-250` (OpenCode `install.sh` one-liner + manifest + per-skill survives uninstall + manual fallback retained) ; `README.md:263-275` (Cursor `install.sh` + `--target both` + manifest + post-install readme + manual fallback retained) ; commit `97183d3` |
| D2 | i18n 副本 `README.zh-CN.md` | yes (mirror of D1) | **pass** | `README.zh-CN.md:240-250` (OpenCode 段同形覆盖) ; `README.zh-CN.md:263-275` (Cursor 段同形覆盖含 `--target both` + 卸载 + 手工 fallback) ; commit `97183d3` |
| D3 | 模块层 / 子包 README — `docs/cursor-setup.md` (用户文档) | yes (C1/C3/C4) | **pass** | `docs/cursor-setup.md:30-67` §1.B 重写为 install.sh 推荐路径 + 手工 fallback 标 advanced users + 显式 cursor rule path note 指向 `.cursor/harness-flow-skills/...` 引用方式（与 ADR-007 D4 + D5 readme 提示一致）; commit `97183d3` |
| D4 | 模块层 / 子包 README — `docs/opencode-setup.md` (用户文档) | yes (C1/C3/C5/C7) | **pass** | `docs/opencode-setup.md:44-63` §1.B 重写为 install.sh 推荐路径 + 手工 fallback 标 advanced users + 显式说明 user-added skill survives uninstall (per-skill manifest)；`docs/opencode-setup.md:20` 与 `:42` 与 `:100` 文本均为 "24 `hf-*`"，stale "23" 已被消除（C7 闭合）; commit `97183d3` |
| D5 | 公共 API doc / OpenAPI / docstring — `install.sh` / `uninstall.sh` 的 `usage()` + 顶部 docstring | yes (C1/C2) | **pass** | `install.sh:1-15` 顶部 docstring 含 design / ADR / spec 三类 cold-link + 编码约束 (`bash 3.2+`、`set -Eeuo pipefail`、POSIX coreutils only)；`install.sh:22-49` `usage()` 完整列出全部 6 个 flag + topology 解释 + manifest/readme 落点 + uninstall 指引；`uninstall.sh:1-12` 顶部 docstring + `:26-42` `usage()` 含 exit codes 表 |
| D6 | i18n 副本之外的 i18n 资产 | no | **N/A** | 项目当前未启用其它 i18n 副本（仅 `README.zh-CN.md`，已在 D2 覆盖） |
| D7 | `CONTRIBUTING.md` / onboarding doc | no | **N/A** | 本 task / feature 未触发 contributor onboarding 资产变化（install scripts 是 user-facing 能力，不改变 maintainer 贡献流程；`CONTRIBUTING.md` 上次同步在 v0.5.1，仍准确） |
| D8 | 用户文档站 source | no | **N/A** | 项目当前未启用独立 docs 站（HF 文档全部驻 `docs/` 与 README，已在 D1-D4 覆盖；无 sphinx / docusaurus 等 site source） |
| D9 | Conventional Commits `docs:` 标记自检 | yes | **pass** | `97183d3 docs(install): T10b doc sync (cursor-setup, opencode-setup, README, CHANGELOG)` 标准 `docs(scope):` 前缀 |
| D10 | `CHANGELOG.md` `[Unreleased]` 段 | — | **N/A (delegated to hf-finalize)** | 责任矩阵权威 `references/responsibility-matrix.md` 表第 `CHANGELOG.md 写入 vX.Y.Z 入口` 行明确归 `hf-finalize`，本 gate ❌；reviewer **不**对 CHANGELOG 出 verdict（避免跨行归类违反 spec §6.2）。Advisory inspection（不进 verdict 聚合）：`CHANGELOG.md:7-22` `[Unreleased]` 含 Added (install.sh/uninstall.sh, tests/, ADR-007) + Changed (cursor-setup §1.B / opencode-setup §1.B + stale 23→24 + README.md / README.zh-CN.md install.sh entries)，与 feature scope 一一对应；hf-finalize 阶段无补漏需求 |

## Stale Assertion Findings

按 spec §3 Leading Indicator 1 + Lagging Indicator 双扫描 + sample grep（`23\s*(个\s*)?hf-\*`、`mkdir -p .opencode/skills.*cp -R` 等）：

- **无遗留 stale 表述**。
  - `opencode-setup.md` 文本中 "23" 字符仅出现于"23rd `hf-browser-testing` (v0.2.0)"这一历史叙事行（line 100），上下文是"v0.2.0 added `hf-browser-testing` as the 23rd; v0.4.0 added `hf-release` as the 24th"，是版本沿革叙述而非 stale claim。
  - `CHANGELOG.md` 中所有 "23 hf-*" / "22 hf-*" 出现位置均在 v0.2.x / v0.3.0 / v0.4.0 历史 release entry 中，是历史快照不可改写（per Keep a Changelog 不可重写已发布段约定）。
  - `cursor-setup.md` / `opencode-setup.md` 的 `Manual fallback (advanced users)` 子段保留 `mkdir -p / cp -R / ln -s` 不构成 stale，已显式标 "advanced users" + 与 install.sh 段并列；与 spec §3 Lagging Indicator "保留 troubleshooting + 高级用户的手动 fallback" 立场一致。
  - `opencode-setup.md` §1.C `Install HarnessFlow globally` 仍用手工 `cp -R`：实现侧 `install.sh` 当前**未**实现 `--global` flag（spec §6 列为可选边界、§7 deferred 仅"global 多版本共存"），故该手工块**不**构成 stale；属于 known limitation 而非文档漂移。

## Spec ↔ Commits 一致性检测 (FR-007)

- spec FR-001..FR-008 + NFR-001..NFR-004 + ASM-001 全部由 `install.sh` / `uninstall.sh` / `tests/test_install_scripts.sh` 实现 + 14/14 e2e PASS（regression-gate 已确认）；commits 行为与 spec 一致，无 spec ↔ commits 实质漂移。
- Conclusion: FR-007 负路径（spec ↔ commits 不一致 → blocked → hf-increment）**不触发**。

## Aggregate Verdict

聚合规则（SKILL.md §3 末尾）：

- 维度 verdict 集合 = {pass, pass, pass, pass, pass, N/A, N/A, N/A, pass, N/A(delegated)}
- 任一 blocked? 否
- 任一 partial? 否
- 至少一个 pass? 是 (D1, D2, D3, D4, D5, D9 共 6 项 pass)
- 整体 verdict = **pass**

## Next Action

- next = `hf-completion-gate`（`pass` → completion-gate evidence bundle 引用本 verdict 路径；FR-005 第一条）
- 本 verdict 路径作为 completion-gate evidence bundle 一项被 reference: `features/001-install-scripts/verification/doc-freshness-2026-05-11.md`
- `reroute_via_router=false`

## Reviewer-Return JSON

```json
{
  "skill": "hf-doc-freshness-gate",
  "reviewer": "independent reviewer subagent (cursor cloud agent, readonly)",
  "active_feature_dir": "features/001-install-scripts",
  "workflow_profile": "full",
  "conclusion": "pass",
  "next_action_or_recommended_skill": "hf-completion-gate",
  "record_path": "features/001-install-scripts/verification/doc-freshness-2026-05-11.md",
  "dimension_breakdown": {
    "readme_root_en": "pass",
    "readme_root_zh": "pass",
    "module_doc_cursor_setup": "pass",
    "module_doc_opencode_setup": "pass",
    "cli_usage_docstring": "pass",
    "i18n_other": "N/A",
    "contributing_onboarding": "N/A",
    "user_docs_site": "N/A",
    "conventional_commits_docs_marker": "pass",
    "changelog_unreleased": "N/A (delegated to hf-finalize per spec §6.2)"
  },
  "stale_assertions_found": [],
  "spec_commit_consistency": "consistent",
  "doc_sync_commit": "97183d3",
  "evidence_bundle_for_completion_gate": [
    "features/001-install-scripts/verification/doc-freshness-2026-05-11.md"
  ],
  "reroute_via_router": false
}
```

# Pre-Release Engineering Checklist — v0.6.0 (2026-05-15)

- Run-by: cursor cloud agent (按 hf-release §8 协议；纯工程级 hygiene；显式不含 ops 项)
- Profile / Mode: full
- Verdict: **PASS** (all C / D / V / W items pass or explicit N/A)

## Code & Evidence (C 系列)

- [x] **C1**: §6 release-wide regression 通过（`features/release-v0.6.0/verification/release-regression.md` PASS）
- [x] **C2**: §7 cross-feature traceability 摘要落盘（`features/release-v0.6.0/verification/release-traceability.md` PASS）
- [x] **C3**: 所有候选 feature 是 `workflow-closeout` 状态（features/002 closeout type 确认）
- [x] **C4**: 所有 lint / type / build 在 release base branch 上通过 — HF 仓库无 lint / type 工具链（纯 markdown + stdlib python），audit-skill-anatomy.py + 12 测试套件 = 等价 lint/type 检查；全 PASS

## Documentation Sync (D 系列，sync-on-presence 协议)

- [x] **D1**: `CHANGELOG.md` `[v0.6.0]` 段已写 — 待 §11 Final Confirmation 通过时由本 skill 从 `[Unreleased]` 翻入
- [x] **D2**: 顶层导航已更新 — README.md / README.zh-CN.md docs refresh 完成（4 / 4 处 wording 改为 "out-of-scope per ADR-008 D1"）；档 0/1 仓库根 README 即顶层导航
- [x] **D3**: 涉及的 ADR 状态批量翻转 — ADR-008 / ADR-009 / ADR-010 已 `accepted`（v0.6 主 PR #53 / #54 内已落）；本版新增 ADR-011 状态待 Final Confirmation 后翻 accepted
- [x] **D4**: 按存在同步以下资产：
  - `docs/release-notes/v0.6.0.md` — N/A（项目档 0/1，未启用 release notes 目录；与 v0.5.x 同向）
  - `docs/architecture.md` / `docs/arc42/` — N/A（未启用）
  - `docs/runbooks/` / `docs/slo/` / `docs/diagrams/` — N/A（未启用）
- [x] **D5**: 每个 feature 的 closeout `Release / Docs Sync` 字段与本次 release 的 docs 同步对账一致 — features/002 closeout.md `## Release / Docs Sync` 段四项与本版 docs 状态一致（README × 2 / soul.md / CHANGELOG）
- [x] **D6**: Migration / breaking changes — N/A（本版 minor bump 无 breaking change；所有 SKILL.md 修改为 surgical add）
- [x] **D7**: Known Limitations — 已聚合 features/002 closeout 的 `Limits / Open Notes` 段（v0.7 runtime 解耦；entry-id 间隔 4 WARN；hf-gap-analyzer / hf-context-mesh evals 内容空可选；test_install_scripts.sh --help 既有遗留；README "Skill Inventory" 段补 4 新 skill 的描述待后续）

## Versioning Hygiene (V 系列)

- [x] **V1**: §3 release scope ADR 已 commit — `docs/decisions/ADR-011-release-scope-v0.6.0.md` 落盘；草稿状态可，等 Final Confirmation 后翻 accepted
- [x] **V2**: §4 SemVer + pre-release 决策已写入 release pack — minor bump v0.5.1 → v0.6.0；pre-release: yes（沿用 ADR-001 D6 默认）
- [x] **V3**: `.claude-plugin/plugin.json` `version` 字段 — N/A（文件不存在；HF marketplace plugin 通过 git tag 拉取，不依赖 manifest 内 version）
- [x] **V4**: `.claude-plugin/marketplace.json` 描述同步 — 不修改（NFR-003 严守；marketplace 内描述为 plugin 元数据，与版本号正交）
- [x] **V5**: `SECURITY.md` Supported Versions 表 — `0.5.x` 行已存在；本版**不**为 `0.6.x` 加新行（目前 SECURITY.md "Supported Versions" 段单点维护当前 release，不做历史多版本维护；与 ADR-005 V5 同向处理）
- [x] **V6**: 项目级元数据版本号同步 — 检查 `package.json` / `pyproject.toml` / `Cargo.toml` 等 — HF 仓库无这些文件（纯 markdown + stdlib python；不发布 npm / pypi 包）；**N/A**

## Worktree / Branch State (W 系列)

- [x] **W1**: §5 worktree disposition 全部记录 — features/002 closeout `## Worktree` 段 disposition = `kept-for-pr` (PR #54 open)；本 release 不擅自删除
- [x] **W2**: 无 release-blocking PR 仍 open — PR #53 已 merged；PR #54 含本版全部 v0.6 改动 + 本 release pack；将在 release 后由架构师合并
- [x] **W3**: release base branch 已是各候选 feature 合并后的状态 — `origin/main` 已含 PR #53 (commit `ed6ee46`) + PR #55 hotfix (commit `5251481`)；PR #54 将在本 release 后合入

## Out of Scope (显式列出本 skill **不**做的事)

按 hf-release SKILL.md §8 末尾约定：

- 部署到 production / staging / canary — out-of-scope（项目自身 ops 流程承担）
- Feature flag 0% → 5% → 100% 的 staged rollout — out-of-scope
- 监控仪表盘 / 错误上报 / SLO 配置 — out-of-scope
- 回滚 procedure / 回滚演练 — out-of-scope
- Health check / CDN / DNS / SSL / Rate limiting — out-of-scope
- 上线后的观察窗口 — out-of-scope

以上**永久**不在 hf-release 范围（按 ADR-008 D1 + ADR-011 D3 + 本 release ADR），由项目自身 ops 流程承担。

## Verdict

**PASS** — C1~C4 / D1~D7 / V1~V6 / W1~W3 全部勾选或显式 N/A；Out of Scope 6 项明确列出且未越权承诺。可进入 §9 Evidence Matrix → §10 Release Pack → §11 Final Confirmation。

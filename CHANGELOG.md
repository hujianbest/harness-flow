# Changelog

All notable changes to HarnessFlow will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

（无）

## [0.2.1] - 2026-05-07 — pre-release patch

> **Docs-and-metadata-only patch.** No skill content changes, no behavior changes, no API changes. Fixes **two install-blocking bugs** discovered during real-environment smoke against the v0.2.0 tag (Claude Code marketplace SSH default + marketplace/plugin name collision), and syncs three stale-metadata items that v0.2.0 GA shipped with.

### Fixed

- **Claude Code marketplace install no longer hangs in a name-collision loop on `harness-flow@harness-flow`.** `.claude-plugin/marketplace.json` `name` field renamed from `harness-flow` (which clashed with the plugin name `harness-flow` and triggered Claude Code's resolver to recursively try to install the marketplace as a plugin) to `hujianbest-harness-flow`, mirroring how `addyosmani/agent-skills` uses `addy-agent-skills` (marketplace) vs `agent-skills` (plugin) to keep the two layers distinct. **The new install command is `/plugin install harness-flow@hujianbest-harness-flow`**; the old `harness-flow@harness-flow` no longer resolves. Users who already added the v0.2.0 marketplace must run `/plugin marketplace remove harness-flow` (note: the OLD marketplace name) before re-adding with the new name.
- **Claude Code marketplace install no longer fails on `git@github.com: Permission denied (publickey)`** for users without GitHub SSH keys. `docs/claude-code-setup.md` now leads with the **HTTPS URL form** (`https://github.com/hujianbest/harness-flow.git`, with explicit `.git` suffix), matching how `addyosmani/agent-skills` documents the same Claude Code marketplace SSH default. The shortcut form `hujianbest/harness-flow` makes the marketplace default to SSH cloning, which is what triggered the first user-reported failure on v0.2.0 smoke. The HTTPS URL form forces HTTPS cloning regardless of SSH key configuration.
- **`.claude-plugin/marketplace.json` plugin description** bumped from `22 hf-* skills` to `23 hf-* skills` (the v0.2.0 `[0.2.0]` Changed entry claimed this happened but the actual file edit was never landed before the v0.2.0 tag — this patch ships the actual edit). Description also now mentions `hf-browser-testing` as the new verify-stage addition.
- **`docs/audits/v0.2.0-skill-anatomy-baseline.md` + `.json`** regenerated against current 24-skill state. The original baseline was written at R1.2 (23 skills, before R2 added `hf-browser-testing`) and never refreshed afterwards; the v0.2.0 GA shipped with that stale baseline.

### Changed

- **`.claude-plugin/marketplace.json`** — `name` renamed from `harness-flow` to `hujianbest-harness-flow` (mirrors `addyosmani/agent-skills`'s `addy-agent-skills` pattern). Plugin's own `name` field stays `harness-flow` (that's the plugin identity users actually consume); only the marketplace top-level `name` changed, since it's the install-command suffix `@<marketplace>` that needs to differ from the plugin-name prefix.
- **`docs/claude-code-setup.md`** — Marketplace install section now leads with HTTPS URL form **and** the new `harness-flow@hujianbest-harness-flow` install command. Added explanatory paragraph on the `<plugin>@<marketplace>` format and why v0.2.0's `harness-flow@harness-flow` self-collided. Added "Already hit the SSH / collision error?" recovery callout (`/plugin marketplace remove harness-flow` against the OLD name → re-add with HTTPS → install with the new name). Kept the global git config rewrite + add-an-SSH-key paths as alternatives, with explicit side-effect warning on the global rewrite. Scope Note + "What is NOT included" section also synced to v0.2.x phrasing.
- **`docs/opencode-setup.md`** — Scope Note synced to v0.2.0 with D11 narrowing note. `/skills` verification list adds `hf-browser-testing` (now 23rd hf-* skill). "What is NOT included" section synced to ADR-002 D1 / D11.
- **`README.md`** — Claude Code install command updated to use `harness-flow@hujianbest-harness-flow` + HTTPS URL form. OpenCode verification line bumped from `22 hf-*` to `23 hf-*` mentioning `hf-browser-testing`.
- **`README.zh-CN.md`** — Claude Code 安装命令同步更新到 `harness-flow@hujianbest-harness-flow` + HTTPS URL form。
- **`.claude-plugin/plugin.json`** — `version` bumped `0.2.0` → `0.2.1`.

### Notes

- The marketplace rename is a **breaking change for users who already installed v0.2.0** — they must remove the old marketplace entry (`/plugin marketplace remove harness-flow` against the OLD name) and re-add with the new name. This is unavoidable: the v0.2.0 marketplace name `harness-flow` is what causes the collision; keeping it would mean keeping the bug. Users on v0.1.0 are unaffected because the marketplace was not yet actively installable (real-environment install was a known gap per CONTRIBUTING.md "Known Limitations").
- This patch is **strongly recommended to tag** (unlike a purely additive docs patch). Without a `v0.2.1` tag the marketplace at `main` works but the `v0.2.0` tag remains broken in cache for any user who already added it. After tagging, suggest users `/plugin marketplace remove harness-flow` (the OLD cached name) + `/plugin marketplace update` (or re-add) to pick up the rename.
- Two user smokes triggered this patch:
  1. First smoke: `Permission denied (publickey)` during `/plugin install` after `/plugin marketplace add hujianbest/harness-flow` (shortcut form). Fixed via HTTPS URL form recovery in `docs/claude-code-setup.md` § 1.
  2. Second smoke: install hung on `harness-flow@harness-flow` due to marketplace/plugin name collision. Fixed via marketplace rename to `hujianbest-harness-flow`.

## [0.2.0] - 2026-05-07 — pre-release

> **Second public release.** Marked as a **pre-release** on GitHub Releases.
>
> v0.2.0 is a **质量纪律内核硬化** release. 在 v0.1.0 基础上加 1 个 verify-stage skill (`hf-browser-testing`)，把 SKILL.md 的"防 agent 偷懒"段（`Common Rationalizations`）从可选升级为必需，配套一个 advisory audit 脚本。客户端面、personas、ops/release 段全部留给 v0.3+。
>
> 完整范围决策见 [`docs/decisions/ADR-002-release-scope-v0.2.0.md`](docs/decisions/ADR-002-release-scope-v0.2.0.md)（含 D11 校准说明 R3/R4/R5 撤回原因；D11 撤回了 D2/D3/D4/D8——5 家客户端扩展 / 真实环境冒烟硬门禁 / 3 personas / persona 命名空间）。

### Added (v0.2.0 core)

- **`skills/hf-browser-testing/`** — verify 阶段的 runtime evidence side node：取 DOM / 控制台 / 网络三层证据，由 `hf-test-driven-dev` 在 GREEN 后按需拉取；不签发 verdict，不修改主链 FSM 主路径，不引入新 slash 命令；spec 未声明 UI surface 或 task 不触碰前端时由 router 自动跳过。含 `SKILL.md` + `references/runtime-evidence-protocol.md`（工具映射 / 目录约定 / `metadata.json` schema / `observations.md` 格式 / severity → canonical next action 映射 / 显式 non-goals）。(ADR-002 D1, D7)
- **`scripts/audit-skill-anatomy.py`** + **`scripts/test_audit_skill_anatomy.py`** — SKILL.md anatomy advisory audit：5 项结构存在性检查（frontmatter `name` 与目录名一致 + `When to Use` / `Workflow` / `Verification` / `Common Rationalizations` 必需 + `和其他 Skill 的区别` 禁止）+ 1 项预算 warning（< 500 行）。CI 上挂 advisory check，**不阻塞 PR merge**。6 个 unittest（compliant / forbidden / missing-required / name-mismatch / missing-skill-md / code-block-headings-ignored）全部通过。撤回 ADR-001 D11 "audit 脚本不进 v0.1.0" 子条款（仅就脚本本身）。(ADR-002 D5)
- **`## Common Rationalizations` 段补到全部 23 + 1 = 24 份 SKILL.md** — 每条必须引用本 skill 已有的 Hard Gates / Workflow stop rule / Verification 条款，不能凭空编造新 rule。覆盖 authoring (5) / review (8) / implementation (1) / gates (3) / side-branch (3) / finalize (1) / routing (2) + 新增的 `hf-browser-testing` (1)。重新激活 ADR-001 D8，强制时点延后到 v0.2.0。(ADR-002 D9)
- **`docs/audits/v0.2.0-skill-anatomy-baseline.md`** + **`v0.2.0-skill-anatomy-baseline.json`** — audit 首次 baseline，24/24 OK / 0 warning / exit 0。
- **`docs/decisions/ADR-002-release-scope-v0.2.0.md`** — v0.2.0 完整范围决策；2026-05-06 锁定 10 项决策，2026-05-07 D11 校准撤回 D2/D3/D4/D8。
- **`examples/writeonce/features/001-walking-skeleton/verification/browser-testing-skip-2026-05-07.md`** — `hf-browser-testing` 在 writeonce demo 上的激活规则核对（结论 SKIP：spec 未声明 UI surface 且 task-001 未触碰前端表面，3 条件中 2/3 不命中）+ 4 条独立旁证。

### Changed (v0.2.0 core)

- **`docs/principles/skill-anatomy.md`** — 部分恢复合规基线性质（仅就 `Common Rationalizations` 必需 + `和其他 Skill 的区别` 禁止两节，从 v0.2.0 起由 audit 脚本强制）。其余段落（`Object Contract` / `Methodology` / `Hard Gates` / `Output Contract` / `Red Flags` / `Common Mistakes` 等）继续保持 ADR-001 D11 的"按需写"性质。`soul.md` 仍是宪法层不变。具体修订点：文件头加 v0.2.0 baseline 提示；主文件骨架表加新行；删除 `Common Rationalizations` 在"默认不建议扩散"列表中的引用 + 新增"显式禁止的章节"段；`和其他 Skill 的区别` 子段重写为 `Common Rationalizations` 写作指南 + 邻接 skill 边界折叠回 `When to Use` 的指南；删除独立的 `和其他 Skill 的区别：最低要求` H2；Canonical skeleton 加 `Common Rationalizations` 占位；Common Mistakes 表加两行；检查清单加两条。(ADR-002 D10)
- **`skills/hf-workflow-router/references/profile-node-and-transition-map.md`** — 把 `hf-browser-testing` 加到 full profile 节点表（标 conditional verify-stage side node，不修改主链 FSM 主路径）；新增 `hf-browser-testing 激活与回流` 一节，覆盖 3 条激活条件（GREEN 已成立 + spec 声明 UI surface + task 触碰前端）+ 3 种回流情形（0/0 → regression-gate；blocking → test-driven-dev with finding；major → suggested next）+ router 的机械路由职责声明（不读 evidence 内容，不参与 severity 改判）。
- **`skills/hf-test-driven-dev/SKILL.md`** — Workflow 步骤 5 后追加 "Verify 拐点 (v0.2.0 / ADR-002 D7)" 提示，指向 router reference；不改 Hard Gates / Object Contract / Workflow（保 ADR-002 D7 "no FSM main-path change"）。
- **`examples/writeonce/` demo refresh**（v0.2.0 evidence trail，**无实现 / 测试 / spec / design / tasks 修改**）：
  - `features/001-walking-skeleton/closeout.md` Evidence Matrix 加 SKIP 行
  - `features/001-walking-skeleton/README.md` Artifacts 表 + Reviews & Approvals 表各加 SKIP 行
  - `features/001-walking-skeleton/progress.md` Progress Notes 加 v0.2.0 Refresh 子段，Evidence Paths 加 SKIP 记录路径
  - `examples/writeonce/CHANGELOG.md` 新增 `[Unreleased] — HF v0.2.0 refresh` 段
- **`.claude-plugin/plugin.json`** — `version` 从 `0.1.0` 升级到 `0.2.0`。
- **`.claude-plugin/marketplace.json`** — plugin description 从 22 hf-* 升级到 23 hf-*（`hf-browser-testing` 已含；释出 v0.2.0 时附在 release-prep 阶段刷新）。
- **`docs/claude-code-setup.md`** — Marketplace install 改用 **HTTPS URL** (`https://github.com/hujianbest/harness-flow.git`) 作为主要路径，规避 Claude Code marketplace 默认 SSH 克隆（`git@github.com: Permission denied (publickey)`）的常见错误；保留 SSH 配置 + 全局 `git config --global url."https://github.com/".insteadOf "git@github.com:"` 作为备选。新增"已经踩过 SSH 错"的恢复步骤（`/plugin marketplace remove harness-flow` → 用 HTTPS 重新 add → install）。Scope Note 同步 v0.2.0 措辞。
- **`docs/opencode-setup.md`** — Scope Note 同步 v0.2.0；`/skills` 验证清单从 22 hf-* 升级到 23 hf-*（追加 `hf-browser-testing`）；"What is NOT included" 段同步 v0.2.0 + ADR-002 D11 措辞。
- **`README.md` + `README.zh-CN.md`** — Scope Note 升级到 v0.2.0 pre-release（保持 Claude Code + OpenCode 两家客户端，不扩展；ADR-002 D11 已撤回 7 客户端提案）。
- **`SECURITY.md`** — Supported Versions 表新增 `0.2.x (pre-release)` 行，原 `0.1.x` 行降级。
- **`CONTRIBUTING.md`** — 引言中 `single-maintainer pre-release (v0.1.0)` 升级到 `(v0.2.0)`，Scope Note 引用同步指向 ADR-002。

### Removed (v0.2.0 core)

- **`## 和其他 Skill 的区别` 段从全部 23 份既有 SKILL.md 移除**（24 份新基线含 v0.2.0 新增的 `hf-browser-testing` 也不允许有此段）。该段在 v0.1.x 时期与 `When to Use` 语义重复；移除前已逐份核对 `When to Use` 已覆盖等价 reroute 条目，是去重而非信息损失。(ADR-002 D9)
- **`hf-bug-patterns` skill** — standalone "knowledge side node" 已删除（含 `references/`、`evals/`、`test-prompts.json`）。该 skill 是可选 learning loop，不在主链或任何 review/gate 上。`hf-test-review`（description / methodology row / workflow step 1 / checklist TT3）的 risk-input 措辞改指 "项目缺陷模式记录 / 风险清单 / hotfix 历史"，仍然消费项目自家约定的 defect catalog。`docs/bug-patterns/catalog.md` 工件槽位从 `docs/principles/sdd-artifact-layout.md`、`skills/hf-workflow-router/references/workflow-shared-conventions.md`、`skills/hf-finalize/SKILL.md` 中移除——仍想保留的项目可在自家约定中声明路径。README 与 marketplace 描述中 skill 数对应改成 22 + 1（v0.2.0 新增 hf-browser-testing） = 23 hf-* + `using-hf-workflow`。

### Added (v0.1.x stabilization, also shipping in v0.2.0)

- `SECURITY.md` — security policy with scope, supported versions, private reporting via GitHub Security Advisory.
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1.
- `CONTRIBUTING.md` — narrow, single-maintainer-aware contribution guide aligned with ADR-001 D1 / D11 scope.
- `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md` — issue templates that prompt readers to check the Scope Note + ADR-001 before filing.
- `.github/ISSUE_TEMPLATE/config.yml` — disables blank issues; adds contact links to security advisory + Code of Conduct + Scope Note.
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template with Scope Note check + per-area testing prompts (no CI yet, see `CONTRIBUTING.md` "Known Limitations").

### Fixed (v0.1.x stabilization, also shipping in v0.2.0)

- **OpenCode install path** now actually works out-of-the-box. The previous setup told users to "clone the repo and open it in OpenCode", but OpenCode's [`skill` tool](https://opencode.ai/docs/skills/) only auto-discovers `SKILL.md` files under `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`, or their global counterparts — a top-level `skills/` directory was never picked up, so `using-hf-workflow` and the 23 leaf skills were invisible to OpenCode agents. Added a `.opencode/skills -> ../skills` symlink so clone-and-open works without duplicating files.
- **`docs/opencode-setup.md`** rewritten to describe OpenCode's real skill-discovery model and the three legitimate install topologies (clone-and-open, vendor into another project's `.opencode/skills/`, global install under `~/.config/opencode/skills/`), with a `/skills` verification step and updated troubleshooting.
- **`README.md` + `README.zh-CN.md`** OpenCode sections updated to match: shipped symlink + verification command + cross-project install guidance.

### Decided (v0.2.0)

- **v0.2.0 仍是 pre-release** on GitHub Releases. Tier 1 只覆盖 1/7 ops，仍未达到 GA 承诺面；且 v0.2.0 的工程纪律硬化不扩展对外承诺面。(ADR-002 D6)
- **官方支持客户端仍为 Claude Code + OpenCode**（与 v0.1.0 一致；ADR-002 D11 撤回了 D2 的 7 客户端扩展）。
- **主链终点仍是 `hf-finalize`**。`hf-browser-testing` 是 verify-stage runtime evidence 节点，不是 ship/deploy/ops 节点。
- **`docs/principles/` 的整体定位仍是设计参考**（ADR-001 D11）；v0.2.0 D10 仅就 `Common Rationalizations`（必需）与 `和其他 Skill 的区别`（禁止）两节恢复合规基线，其它段落不动。

### Voided / Superseded (v0.2.0)

- **ADR-002 D2** (5 客户端扩展：Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro) — **superseded by D11**. v0.2.0 不扩展客户端面；R3 实现已 git revert，原 commit 保留在历史中（`18b1d99`、`0c93809`）方便 v0.3+ cherry-pick。
- **ADR-002 D3** (真实环境 install smoke 硬门禁) — **superseded by D11**. v0.2.0 不增设新硬门禁；R5 骨架已删。
- **ADR-002 D4** (3 user-facing personas: `hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — **superseded by D11**. v0.2.0 不引入 `agents/` 目录；R4 实现已 git revert，原 commit 保留在 `560ac26`。
- **ADR-002 D8** (Persona 命名空间约定 + `docs/principles/persona-anatomy.md`) — **superseded by D11**（D4 撤回的连带影响；persona-anatomy.md 一并删除，与 ADR-001 D11 删除 audit 脚本对称）。

### Deferred (to v0.3+)

- 6 项剩余 ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）—与 ADR-001 D1 / ADR-002 D1 一致。
- 5 家新客户端扩展 + 6 个 Gemini CLI commands。
- 3 个 user-facing personas + `docs/principles/persona-anatomy.md`。
- 真实环境 install smoke 硬门禁。
- `docs/principles/` 其它段落升级为合规基线（继续保持 ADR-001 D11 "设计参考" 性质）。

### Notes

- audit script 是 advisory，不阻塞 PR merge；v0.2.0 GA 后视实际 SKILL.md 漂移率再决定是否升级为 hard gate。
- writeonce demo 的 v0.2.0 refresh 仅是 evidence trail 补全（SKIP 记录 + 4 处索引），不改实现 / 测试 / spec / design / tasks / review verdict / gate verdict（与 ADR-001 D9 "demo deliverable is the artifact trail, not the product" 一致）。
- 真实环境 marketplace install 验证仍是已知 limitation（自 v0.1.x 沿用至今；CONTRIBUTING.md "Known Limitations" 已声明），v0.2.0 不再视其为 GA 硬门禁（D11 撤回 D3）。

## [0.1.0] - pre-release

> **First public release.** Marked as a **pre-release** on GitHub Releases.
>
> Release scope, alternatives considered, and reversibility for every decision below are recorded in [`docs/decisions/ADR-001-release-scope-v0.1.0.md`](docs/decisions/ADR-001-release-scope-v0.1.0.md).

### Added

- **MIT `LICENSE`** at the repository root. Copyright `hujianbest`. (ADR-001 D2)
- **Claude Code plugin manifest**:
  - `.claude-plugin/plugin.json` — name `harness-flow`, version `0.1.0`, MIT, repo `hujianbest/harness-flow`.
  - `.claude-plugin/marketplace.json` — marketplace entry for `/plugin marketplace add hujianbest/harness-flow`.
  (ADR-001 D3, D5)
- **6 short slash commands** for Claude Code (ADR-001 D4):
  - `/hf` — route-first default (`using-hf-workflow` → `hf-workflow-router`).
  - `/spec` — bias toward `hf-specify`.
  - `/plan` — combined design + tasks (router decides between `hf-design`, `hf-ui-design`, `hf-tasks`).
  - `/build` — bias toward `hf-test-driven-dev` (only when one `Current Active Task` is locked).
  - `/review` — router dispatches to the matching `hf-*-review`.
  - `/ship` — `hf-completion-gate` → `hf-finalize`.
- **`docs/claude-code-setup.md`** — Claude Code install (marketplace + local), verify, troubleshooting.
- **`docs/opencode-setup.md`** — OpenCode setup using agent-driven routing; no `AGENTS.md` sidecar required (ADR-001 D3).
- **README Scope Note** at the top of `README.md` and `README.zh-CN.md`: pre-release; Claude Code + OpenCode only; main chain ends at `hf-finalize` (engineering-level closeout); release / ops out of scope. (ADR-001 D1, D6)
- **Acknowledgements** section in both READMEs listing every method source and where it lands in HarnessFlow (Karpathy skills, Google SWE / engineering-practices, Evans, Vernon, Brandolini, Beck, Fowler, Martin, Fagan, Brown, Starke, ISO/IEC 25010, STRIDE, Nielsen, WCAG, PMBOK, Ulwick / Christensen JTBD, Torres OST). (ADR-001 D7)
- **`CHANGELOG.md`** (this file). Versioning starts at `v0.1.0`. (ADR-001 D6)

### Decided

- **Pillar C = P-Honest (narrow but hard).** v0.1.0 does **not** add release / ops skills (no `hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`, `hf-browser-runtime-evidence`). Main chain terminates at `hf-finalize`. (ADR-001 D1)
- **Officially supported clients = Claude Code + OpenCode only.** Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro are deferred to v0.2+. HarnessFlow is plain Markdown so it may run elsewhere, but those paths are not part of the v0.1.0 commitment. (ADR-001 D3)
- **Repository ownership stays at `hujianbest/harness-flow`.** No org migration; no npm / PyPI / marketplace name pre-claim for v0.1.0. (ADR-001 D5)
- **Versioning policy: SemVer; `v0.1.0` is a pre-release.** GitHub Release will have "Set as a pre-release" checked. (ADR-001 D6)
- **`docs/principles/` is design reference only**, not a runtime dependency, not a release gate, and not a SKILL.md compliance baseline. `soul.md` remains the constitution layer for the user-as-architect / HF-as-engineering-team contract only. (ADR-001 D11)
- **R1 (quality baseline hardening) concluded.** v0.1.0 maintains the existing 24 `hf-*` skills + `using-hf-workflow` as-is. No SKILL.md content edits in this release. (ADR-001 D11)

### Deferred (to v0.2+)

- All release / deployment / observability / incident-response / security-hardening / performance-gate / deprecation-and-migration / browser-runtime-evidence skills.
- Plugin / setup support for Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro.
- `/hotfix` slash command (use natural language + `/hf` so the router can branch into `hf-hotfix` / `hf-increment`).
- `/gate` slash command (gates are pulled by the canonical next action of upstream nodes, not pushed by the user).
- Any batched `Common Rationalizations` / `Object Contract` rewrites across the 24 skills.
- Automated SKILL.md anatomy audit script and `docs/audits/` baseline reports.

### Voided / Superseded

- **ADR-001 D8** (force every SKILL.md to add `Common Rationalizations`) — **superseded by D11**. v0.1.0 does not require this; future versions may re-evaluate based on actual feedback.
- **ADR-001 D10** (Object Contract enforcement level: recommended in v0.1.0, mandatory in v0.2.0) — **voided by D11**. Object Contract is back to "author writes it when needed", neither mandatory nor recommended in v0.1.0.

### Quickstart demo (delivered)

- **`examples/writeonce/` — WriteOnce demo, full HarnessFlow main-chain trace** (ADR-001 D9):
  - 16 HF nodes (`hf-product-discovery` → `hf-finalize`) each produced a reviewable artifact under `examples/writeonce/features/001-walking-skeleton/` and `examples/writeonce/docs/insights/`.
  - Walking-skeleton implementation: Node.js 20 + TypeScript + minimal CLI; Markdown → Medium with Zhihu / WeChat MP declared as extension points but not implemented; 23 vitest cases passing offline in ~370 ms.
  - 3 demo-internal ADRs (`examples/writeonce/docs/adr/0001..0003`).
  - Demo-internal `examples/writeonce/CHANGELOG.md`.
- Per ADR-001 D9: the demo's **deliverable is the trail of HF main-chain artifacts**, not a finished product. The demo does not publish to a real Medium account; all HTTP is intercepted by `RecordingHttpClient`.
- Per the user's 2026-04-29 delegation, the demo's product scope (target users / platforms / MVP / tech stack) was locked by the cursor agent and recorded as `seed input` in `examples/writeonce/docs/insights/2026-04-29-writeonce-discovery.md` section 0, then carried forward by `hf-specify`. Discovery / spec / design / tasks approval gates were each signed off by the cursor agent on that delegation.

[Unreleased]: https://github.com/hujianbest/harness-flow/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/hujianbest/harness-flow/releases/tag/v0.2.1
[0.2.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.2.0
[0.1.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.1.0

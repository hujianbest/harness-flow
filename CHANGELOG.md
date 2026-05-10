# Changelog

All notable changes to HarnessFlow will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Documentation

- **`README.md` / `README.zh-CN.md`** —— 在三处 reviewer-facing 介绍面同步补齐 `hf-browser-testing`（v0.2.0 / ADR-002 D1 / D7 引入的 verify-stage conditional side node），与 `hf-experiment` / `hf-ui-design` / `hf-release` 同等待遇：(1) `## Overview` / `## 项目概览` 概述 bullets 加一行 `Browser runtime evidence`；(2) `### Execution and reviews` / `### 执行与评审` 方法论矩阵加 `hf-browser-testing` 一行（Three-layer Runtime Evidence + Walking Skeleton Scenario + Fresh Evidence Principle + Observation-not-Verdict + Author/Reviewer/Gate Separation）；(3) `## Workflow Shape` / `## 工作流形状` 流程图加 `(optional) hf-browser-testing` 行 + 流程图下方加专门的激活与回流说明段（指向 `skills/hf-browser-testing/SKILL.md` 与 `skills/hf-workflow-router/references/profile-node-and-transition-map.md` 的 `hf-browser-testing 激活与回流` 一节）。修复此前 README 仅在 OpenCode 验证段一处提及其存在性、却在三个核心介绍面都漏掉它的不一致；不改 skill 行为、不改 FSM、不改 router transition map、不改 slash 命令面、不改任何 SKILL.md。

## [0.5.1] - 2026-05-09 — pre-release

> **Patch release on top of v0.5.0.** Marked as a **pre-release** on GitHub Releases.
>
> v0.5.1 修复 v0.5.0 引入的一个 vendoring 缺陷：v0.5.0 把 `hf-finalize` step 6A 的 hard gate 工具 `render-closeout-html.py` 放在仓库根 `scripts/`，但 OpenCode `.opencode/skills/` 软链接 + Cursor `.cursor/rules/` + "vendor by copying `skills/`" 三种集成路径都**只**带 `skills/` 不带仓库根 `scripts/`，导致 step 6A 在这两条路径下跑不通。本版把脚本物理迁移到 `skills/hf-finalize/scripts/`，并把这一区分锁成 HF skill anatomy v2（4 类子目录：`SKILL.md` + `references/` + `evals/` + `scripts/`；仓库根 `scripts/` 收紧为跨 skill 维护者工具）。
>
> 完整范围决策见 [`docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`](docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md)（4 项决策）。本 release 是 HF 自身**第三次** dogfood `hf-release`（前两次为 v0.4.0 / v0.5.0），首次验证 patch release 流程；release pack 落到 [`features/release-v0.5.1/release-pack.md`](features/release-v0.5.1/release-pack.md)。
>
> **不**改 closeout pack schema、**不**改 closeout HTML 输出语义、**不**触动其它 23 个 skill；只动 hf-finalize 的脚本物理位置 + 配套契约文本。

### Fixed

- **vendoring 缺陷修复**（ADR-006 D2）—— v0.5.0 把 `render-closeout-html.py` 放在仓库根 `scripts/` 是判断失误：OpenCode `.opencode/skills/` 软链接 / Cursor `.cursor/rules/` + 复制 `skills/` / "vendor by copying `skills/`" 三种集成路径下 hf-finalize step 6A 的 hard gate 跑不通——脚本不在 vendoring 树里。本版把脚本物理搬到 `skills/hf-finalize/scripts/render-closeout-html.py` + `skills/hf-finalize/scripts/test_render_closeout_html.py`，三种集成路径自动恢复完整。

### Changed

- **HF skill anatomy v2**（ADR-006 D1）—— skill anatomy 从 v0.2.0 起约定的 3 类子目录（`SKILL.md` + `references/` + `evals/`）扩展为 4 类，新增 `skills/<name>/scripts/` 作为 **skill-owned 工具** 子目录；仓库根 `scripts/` 同步收紧为 **跨 skill 维护者工具**（典型：`audit-skill-anatomy.py`）。区分依据是 **工具受众**：用户每次跑该 skill 都要跑的工具属于 skill-owned，受众是仓库 contributor 的工具留在仓库根。**向前兼容**：v0.4.0 / v0.5.0 留下的 3 类布局仍合法；本版只新增一类，不淘汰旧约定；其它 23 个 skill 当前没有 skill-owned 工具，按需后续 ADR 单独迁移。
- **`skills/hf-finalize/SKILL.md`** —— step 6A 命令、生成方式描述、Reference Guide 表行、Verification 列表项中所有脚本路径同步从 `scripts/render-closeout-html.py` 改为 `skills/hf-finalize/scripts/render-closeout-html.py`；Reference Guide 行额外注明 `ADR-006 引入的 skill-owned 工具约定` 与 `仓库根 scripts/ 保留给跨 skill 的维护者工具` 立场。
- **`skills/hf-finalize/references/finalize-closeout-pack-template.md`** —— 顶部使用说明 + `HTML Companion Report` 段中的 2 处脚本路径同步更新。
- **`skills/hf-finalize/scripts/render-closeout-html.py`** —— 顶部 docstring 加 `Note on script location (since v0.5.0)` 段，解释 ADR-006 立场（为什么住在 skill 目录下）。脚本本体逻辑 / 输出语义完全不变。
- **`scripts/audit-skill-anatomy.py`** —— 顶部 docstring 加段说明 v0.5.1 起的 4 类子目录约定；审计行为不变（仅读 `<skill>/SKILL.md`，不遍历子目录，新加的 `skills/*/scripts/` 子目录对它完全透明）。
- **`.claude-plugin/plugin.json`** —— `version` 从 `0.5.0` 升级到 `0.5.1`。
- **`.claude-plugin/marketplace.json`** —— description 段追加 v0.5.1 vendoring fix 说明 + 脚本路径同步。
- **`SECURITY.md`** —— Supported Versions 表 `0.5.x` 行 latest 从 `0.5.0` 升到 `0.5.1`。
- **`CONTRIBUTING.md`** —— 引言版本号 `v0.5.0` → `v0.5.1`（patch refresh）。
- **`.cursor/rules/harness-flow.mdc`** —— Hard rules 段 step 6A 命令脚本路径同步。
- **`README.md` / `README.zh-CN.md`** —— Scope Note / 范围声明段加 v0.5.1 patch 注解；脚本路径同步。
- **`docs/claude-code-setup.md` / `docs/cursor-setup.md` / `docs/opencode-setup.md`** —— 顶部句子 + Scope Note + cross-references 段脚本路径与版本号同步。
- **`examples/writeonce/features/001-walking-skeleton/closeout.html`** —— 由新位置渲染器重新生成；HTML 仅 footer 1 行（生成器路径文本）+ 嵌入时间戳差异。

### Decided

- **v0.5.1 是 patch release，不是 minor。** 不引入新功能（HTML 伴生报告本身在 v0.5.0 已 GA）；不改 closeout.md schema / closeout.html 输出语义；修复的是物理位置 / vendoring 链路的工程债务——典型 patch 范畴。仍勾 pre-release on GitHub Releases。(ADR-006 D3)
- **不保留旧路径 symlink。** 避免双源混乱与 Windows 上 symlink 行为差异；旧路径 `scripts/render-closeout-html.py` 在 v0.5.1 升级后立即失效；任何项目级 CI / 别名 / 文档中 hardcode 了旧路径的地方需手工同步——见 Notes 段 migration 提示。(ADR-006 D2)
- **HF 第三次 dogfood `hf-release`**（首次验证 patch release 流程）。前两次（v0.4.0 / v0.5.0）都是 minor；本次验证 hf-release / `references/release-pack-template.md` / `pre-release-engineering-checklist.md` 在 patch 范畴下仍然适用——release pack `Fixed` 子段替代 `Added` 子段；其它结构不变。(ADR-006 D4)
- **不动其它 22 个 skill 的 anatomy。** ADR-006 D1 引入的 4 类子目录约定是**新增**而非强制迁移；其它 skill 当前没有 skill-owned 工具，按需后续 ADR 单独迁移。

### Notes

- **Migration 提示**：升级到 v0.5.1 的项目下次跑 `hf-finalize` 会自动用新路径 `skills/hf-finalize/scripts/render-closeout-html.py`；任何项目级 CI / 别名 / 文档 / sidecar 中 **hardcode** 了旧路径 `scripts/render-closeout-html.py` 的地方需要同步更新。如果你之前在自己的 `package.json` scripts 段 / Makefile / GitHub Actions workflow / 项目本地 hf-finalize sidecar 写过类似 `python3 scripts/render-closeout-html.py ...` 的命令，请改为 `python3 skills/hf-finalize/scripts/render-closeout-html.py ...`。
- v0.5.0 已落盘的 `closeout.md` / `closeout.html` 不需要修订（schema / 输出语义不变）；v0.5.0 已落盘的 `features/release-v0.5.0/` 也不修订（已是 tagged 历史）。
- v0.5.1 是 HF 自身**首个 patch release**（v0.0.0–v0.4.0 都是 minor，v0.5.0 也是 minor）；首次验证 ADR / release pack / pre-release-engineering-checklist 在 patch 范畴下仍然适用——release pack 模板 `Fixed` 子段替代 `Added` 子段，其它结构不变。
- 本 release diff 极小（约 3 commit；脚本 git mv + 7 处契约文本同步 + ADR-006 + release pack 三件套 + 顶层文档版本号同步）；体现"工程债务发现立即修，不留 v0.6.0 一起带"的节奏。

## [0.5.0] - 2026-05-09 — pre-release

> **Fifth public release.** Marked as a **pre-release** on GitHub Releases.
>
> v0.5.0 是一次 **reviewer 体验切面** 版本。在 v0.4.0 基础上**不**扩 skill 集合（仍 24 `hf-*` + `using-hf-workflow`），**不**新增 slash 命令（仍 7 条），**不**改主链 FSM，**不**进 router transition map；而是给 `hf-finalize` 的输出契约新增一份**视觉伴生制品**——`closeout.html`，由新的 `scripts/render-closeout-html.py` 从已落盘 `closeout.md` + `evidence/*.log` + `verification/*.md`（+ optional `verification/coverage.json`）渲染得到的**自包含**单文件 HTML（嵌入式 CSS / 极小 vanilla JS / 离线可读 / 暗亮主题 / 可打印）。视觉系统按 `hf-ui-design` 方法论 + `references/anti-slop-checklist.md` 自检 S1-S8 全条覆盖；脚本仅依赖 Python 3 stdlib，与 `audit-skill-anatomy.py` 同款约束。
>
> 完整范围决策见 [`docs/decisions/ADR-005-release-scope-v0.5.0.md`](docs/decisions/ADR-005-release-scope-v0.5.0.md)（9 项决策；与 ADR-001 / ADR-002 / ADR-003 / ADR-004 立场兼容——P-Honest 仍然成立，本版严格停在工程级 closeout reviewer 体验改进，未承诺部署 / 监控 / 回滚）。
>
> 本 release 是 HF 自身**第二次** dogfood `hf-release`（首次为 v0.4.0），用以验证 `references/release-scope-adr-template.md` / `release-pack-template.md` / `pre-release-engineering-checklist.md` 在"小颗粒度 minor release + 单候选 engineering-tier feature"场景下仍然实用。Release pack 落到 [`features/release-v0.5.0/release-pack.md`](features/release-v0.5.0/release-pack.md)。

### Added

- **`scripts/render-closeout-html.py`** — 把 `features/<active>/closeout.md` 渲染为视觉伴生 `closeout.html` 的 stdlib-only Python 脚本（< 800 行）。从 closeout pack schema 的 H2 段（Closeout Summary / Evidence Matrix / State Sync / Release/Docs Sync / Handoff）+ 表格 / bullet 双形态 evidence rows 解析，输出含 closeout 类型徽标 + conclusion blockquote、HF 主链节点 timeline rail（实心圆点 / 空心圆点 / 红点三态）、tests 大号 tabular 数字 + SVG donut rings 覆盖率（pct 缺失时显式渲染"未提供"，**不**阻塞 closeout）、可搜索可排序 evidence matrix（client-side vanilla JS）、单列垂直 release/docs sync + numbered handoff notes。视觉系统按 `hf-ui-design` 方法论：脚本顶部 docstring 含 "System Manifesto"（vocalize the system）+ "Anti-slop checks consumed" 段，逐条覆盖 `skills/hf-ui-design/references/anti-slop-checklist.md` § 1-3 的 S1-S8 八条 AI 默认审美陷阱（无渐变 / 无左竖线 callout / 显式字体理由 / 非默认蓝紫 / 无装饰 SVG / 非千篇一律 dashboard / 无 glassmorphism / 无浮起卡片）。WCAG 2.2 AA 对比度 + `:focus-visible` + `prefers-reduced-motion` + `prefers-color-scheme` 暗亮自适应 + 打印样式（隐藏 toolbar、展开折叠行）。(ADR-005 D1, D2, D3)
- **`scripts/test_render_closeout_html.py`** — 17 个单元测试覆盖 markdown 解析两种形态（table + bullet）/ vitest + jest + pytest 测试日志解析 / istanbul + json-summary 覆盖率两种来源 / 完整 + blocked 渲染 / sub-bullet 不溢出到 sibling section 回归 / Status Fields Synced 子项渲染 / HTML 转义 / CLI exit code。所有 17 测试 PASS（< 0.02 秒）。
- **`docs/decisions/ADR-005-release-scope-v0.5.0.md`** — v0.5.0 完整范围决策；2026-05-09 锁定 9 项决策（D1 hf-finalize 必出 closeout HTML / D2 stdlib-only Python 实现栈 / D3 反 slop 视觉系统显式入档 / D4 唯一修订 hf-finalize 不动其它 23 个 skill / D5 不引入新 skill 不动 router / D6 minor bump + pre-release / D7 5 项原 deferred ops/release skill 漂移到 v0.6+ / D8 不刷新 writeonce demo / D9 不自动 git tag / 不部署 / 不做 ops）。
- **`features/release-v0.5.0/`** — 本版 release pack 工件目录：`release-pack.md`（主 pack）+ `verification/release-regression.md` + `verification/release-traceability.md` + `verification/pre-release-checklist.md`。Status: `ready-for-tag`。
- **`examples/writeonce/features/001-walking-skeleton/closeout.html`** — 由 `scripts/render-closeout-html.py` 对真实 walking-skeleton closeout.md 渲染得到的"reference 实现样例"。证明渲染脚本对真实 closeout pack 可用；不修改 demo 事实层（按 ADR-005 D8 / ADR-003 D10 / ADR-004 D9 立场）。

### Changed

- **`skills/hf-finalize/SKILL.md`** — 工作流新增 step 6A "产出 closeout HTML 工作总结报告"（在 step 6 落盘 closeout.md 之后必须额外执行 `python3 scripts/render-closeout-html.py <feature-dir>` 生成 `closeout.html`）；Hard Gates 加 1 条（"落盘 closeout.md 后必须同时产出 closeout.html 视觉伴生报告"）；Reference Guide 表加 1 行链接到新脚本；Verification 列表加 1 项（HTML 报告必出）；Red Flags 加 1 条（"只写 closeout.md 不生成 closeout.html，或在 HTML 里捏造 closeout.md 之外的 conclusion / 测试数据 / 覆盖率"）。其余 23 个 skill 在本版**不**做内容修订（含 v0.4.0 新引入的 `hf-release`）；entry shell `using-hf-workflow` § 5 entry bias 表不动。(ADR-005 D4, D5)
- **`skills/hf-finalize/references/finalize-closeout-pack-template.md`** — 追加 "HTML Companion Report" 段，列出生成命令 + 覆盖率数据源优先级（`verification/coverage.json` → `verification/*.md` → `evidence/*.log`）+ "HTML 只是 closeout.md 的视觉渲染，不允许引入新事实" 约束；模板顶部使用说明同步加一句关于 HTML 伴生报告的 hard gate。
- **`.claude-plugin/plugin.json`** — `version` 从 `0.4.0` 升级到 `0.5.0`。
- **`.claude-plugin/marketplace.json`** — plugin description 追加 v0.5.0 closeout HTML 伴生报告说明（24 hf-* 不变；hf-finalize 新增 step 6A；剩余 5 项 ops/release skill 漂移到 v0.6+）。
- **`README.md` + `README.zh-CN.md`** — Scope Note / 范围声明段升级到 v0.5.0；skill 数 24 不变；Slash 命令面 7 条不变；客户端面 3 家不变；新增 v0.5.0 简述段（hf-finalize 输出契约扩展 + 新脚本）；"What is NOT included" 调整：5 项原 deferred ops/release skill roadmap 标签从 "v0.5+" 改为 "v0.6+"。
- **`docs/claude-code-setup.md`** — 顶部句子 v0.4.0 → v0.5.0；Scope Note 重写为 v0.5.0；§ "What is NOT included" 5 项 ops/release skill 改为 v0.6+；§ cross-references 加 ADR-005。
- **`docs/opencode-setup.md`** — 同形改动：顶部 + Scope Note v0.4.0 → v0.5.0；NL intent → node 映射表不动（hf-release 行保留）；§ "What is NOT included" 同步 v0.5.0 措辞；§ cross-references 加 ADR-005。
- **`docs/cursor-setup.md`** — 同形改动：顶部 + Scope Note v0.4.0 → v0.5.0；§ NL intent → router 映射不动；§ "What is NOT included in v0.4.0" → "v0.5.0"；§ cross-references 加 ADR-005。
- **`.cursor/rules/harness-flow.mdc`** — `Scope honesty` 段更新到 v0.5.0：声明 v0.5.0 引入了 hf-finalize closeout HTML 伴生制品 + 新 stdlib 脚本，**不**改主链；剩余 5 项 ops/release skills 继续延后到 v0.6+ roadmap（ADR-005 D7）。
- **`SECURITY.md`** — Supported Versions 表加 `0.5.x` 行；`0.4.x` 降级为 best-effort security-only；`0.3.x` / `0.2.x` / `0.1.x` 标签调整；out-of-scope 段对 ADR 的引用补全为 ADR-001 D1 + ADR-002 D1 + ADR-003 D2 + ADR-004 D2 + ADR-005 D9。
- **`CONTRIBUTING.md`** — 引言版本号 `v0.4.0` → `v0.5.0` + Scope Note 文案更新（24 skills 不变；7 slash 命令不变；hf-finalize 新增 step 6A；5 项 ops/release skill 漂移到 v0.6+）；Will accept / Will defer 段补 ADR-005 引用；feature_request 提示从 ADR-004 改成 ADR-005 first。

### Decided

- **v0.5.0 仍是 pre-release** on GitHub Releases。理由：主链覆盖未达 100%（仍缺 5 项 ops/release skill；ADR-005 D7 显式延后到 v0.6+）；客户端面无变化（仍 3 家）；与 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 / ADR-004 D8 同向，版本号不跨 v1.0。(ADR-005 D6)
- **`hf-finalize` 是本版唯一修订的 skill；不引入新 skill。** 用户反馈是 "hf-finalize 加 HTML 伴生报告"，颗粒度是"已存在 skill 的输出契约扩展"，不是"新工作流节点"。加独立 `hf-html-report` 之类 skill 会引入不必要的契约决策；step 6A 直接绑死在 hf-finalize 内最简洁。(ADR-005 D4, D5)
- **HTML 报告与 closeout.md 是渲染关系而非平行事实。** 渲染脚本读 closeout.md + 已落盘 evidence；不允许在 HTML 中加入新 conclusion / 测试数据 / 覆盖率（"sync-on-presence + 不引入新事实" 立场）。覆盖率缺失时 HTML 显式渲染"未提供"，**不**阻塞 closeout。(ADR-005 D1)
- **渲染脚本仅依赖 Python 3 stdlib。** 与 v0.4.0 已建立的"纯 Python stdlib 脚本工具链"（`audit-skill-anatomy.py`）路径一致；不引入 Node.js / Markdown 解析库 / SSG，避免把 HF 仓库变成"半个前端项目"。(ADR-005 D2)
- **视觉系统按 hf-ui-design 方法论自检；反 AI slop 立场显式入档。** 脚本顶部 docstring 含 System Manifesto + Anti-slop checks consumed 段，逐条覆盖 anti-slop-checklist S1-S8；这是 HF 自身首次对外的 reviewer-facing 视觉产物，必须显式入档以拒绝后续 PR 渐进侵入默认 SaaS 审美。(ADR-005 D3)
- **5 项原 deferred ops/release skill roadmap 漂移到 v0.6+。** v0.4.0 文档将 `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery` 写为 "deferred to v0.5+"；v0.5.0 prioritized hf-finalize reviewer 视觉化体验，5 项 ops 切面继续延后到 v0.6+。诚实承认 roadmap 演化，**不**承诺没做的事。(ADR-005 D7)
- **不刷新 `examples/writeonce/` demo evidence trail；只新增 closeout.html 作为渲染脚本的 reference 实现样例。** 与 ADR-003 D10 / ADR-004 D9 同向。demo 是 v0.1.0 范围一次性产出的真实工件，不应被 v0.5.0 反向修订。(ADR-005 D8)
- **不自动执行 `git tag v0.5.0` / 不部署 / 不做上线侧动作。** 与 ADR-004 D7 + `hf-release` SKILL.md Hard Gates 立场一致；tag 操作由项目维护者按 hf-release `Tag Readiness` 段约定手工执行。(ADR-005 D9)
- **官方支持客户端仍为 Claude Code + OpenCode + Cursor（3 家）。** 其余 4 家（Gemini CLI / Windsurf / GitHub Copilot / Kiro）继续延后到 v0.6+。

### Deferred (to v0.6+)

- 5 项原 deferred ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）继续延后。v0.4.0 新增的 `hf-release` 不属于这 6 项，覆盖"工程级版本切片"切面；v0.5.0 新增的 closeout HTML 伴生报告也不属于这 6 项，覆盖"reviewer 视觉化体验"切面。两者均**不**替代 ops 切面。
- 4 家剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）+ Gemini CLI 的 6+1 条 slash 命令。
- 3 个 user-facing personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）+ `agents/` 命名空间约定 + `docs/principles/persona-anatomy.md`。
- 真实环境 install smoke 硬门禁（视客户端面铺开节奏 / 真实事故触发再启动）。
- `docs/principles/` 其它段落升级为合规基线（继续保持 ADR-001 D11 "设计参考" 性质）。
- `audit-skill-anatomy.py` 升级为 hard gate（视 SKILL.md 漂移率）。
- `examples/writeonce/` demo evidence trail 下次主链节点变更或 release-tier dogfood 同步触发。
- HTML 报告若用户反馈"想要更多视觉切片"（如 release pack HTML / cross-feature traceability HTML），再独立评估并 ADR。

### Notes

- v0.5.0 是 v0.4.0 之后的第二个 minor release，体现"先把 release-tier 切片做出来、再回头补 reviewer 视觉化"的节奏：v0.1.0 → v0.2.0 是质量纪律内核硬化；v0.3.0 是单客户端扩张（Cursor，2 → 3 家）；v0.4.0 是首次扩 skill 集合（23 → 24，引入 hf-release release-tier 独立 skill）；v0.5.0 不扩 skill，而是 reviewer 体验切面（hf-finalize 输出契约扩展，24 不变）。两个 minor release 都**不**触动主链 FSM 与 router transition map。
- **Hard gate 严化的影响**：升级到 v0.5.0 的 HF 仓库下次执行 `hf-finalize` 必须额外跑一次 `scripts/render-closeout-html.py`；CI / 本地工作流加 1 步（脚本执行成本极低，< 0.5 秒）。对历史 closeout 不追溯——旧 feature 目录补跑脚本即可生成 HTML，不需要修订任何已落盘工件。
- 本 release 是 1 新增脚本（< 800 行，含顶部 docstring）+ 1 SKILL.md 工作流补丁 + 1 模板段追加 + 元数据 / 文档同步，工作面规模与 v0.3.0 patch 量级相当；不涉及主链 FSM 编辑、router transition map 编辑、demo 工件刷新。
- 本 release 是 HF 自身**第二次** dogfood `hf-release`（v0.4.0 是首次 dogfood）。本次 dogfood 验证了 `references/release-scope-adr-template.md` / `release-pack-template.md` / `pre-release-engineering-checklist.md` 在"小颗粒度 minor release + 单候选 engineering-tier feature"场景下仍然实用——release pack 模板的 `Included Features` 段可以容纳"对已存在 skill 的输出契约扩展"形态的 feature，不强制要求每次 release 都有独立的 `features/<feature-id>/closeout.md` 候选（详见 `features/release-v0.5.0/release-pack.md` `Limits / Open Notes` 段第二条）。
- HTML 报告设计借鉴了 RFC / postmortem / commit log 的纸感读体验，**拒绝** SaaS marketing dashboard 默认审美：单列 typography-led / 同色面板 + hairline 区隔 / OKLCH 推导的中性灰 + ONE 克制 indigo accent / system stack 字体（自包含 + CJK） / 3 档 radius / 1 档 easing / 1 档 hairline / 默认零 shadow。具体设计宣言记入 `scripts/render-closeout-html.py` 顶部 docstring "System Manifesto" 段，未来维护 PR 不允许绕过 anti-slop-checklist 自检。

## [0.4.0] - 2026-05-09 — pre-release

> **Fourth public release.** Marked as a **pre-release** on GitHub Releases.
>
> v0.4.0 是一次**首个 release-tier skill 引入**版本。在 v0.3.0 基础上首次扩大 skill 集合（23 → **24** `hf-*` + `using-hf-workflow`）：新增 `hf-release` 作为**独立 standalone 工具型 skill**，把多个已 `workflow-closeout` 的 feature 汇总成 vX.Y.Z **engineer-level release**（版本切片 + release-wide regression + docs aggregation + tag readiness pack）。**不**改主链 FSM；**不**进 `hf-workflow-router` transition map；**不**做部署 / staged rollout / 监控 / 回滚（仍归 v0.5+ planned `hf-shipping-and-launch`，**当前尚未实现**）。Slash 命令面从 6 → **7**：新增 `/release` direct invoke `hf-release`，不经 router。
>
> 完整范围决策见 [`docs/decisions/ADR-004-hf-release-skill.md`](docs/decisions/ADR-004-hf-release-skill.md)（9 项决策；与 ADR-003 D2 / D4 立场兼容——P-Honest 仍然成立，本版严格停在工程级 release，未把"代码合并 / 工程 closeout"伪装成"上线到生产"）。

### Added

- **`skills/hf-release/`** — release-tier 独立 skill：把 N 个 `workflow-closeout` 的 feature 汇总成 vX.Y.Z 工程级发版。Standalone，不依赖 `hf-workflow-router` / `hf-finalize` / `hf-regression-gate` / `hf-doc-freshness-gate` 在同一 session 跑过；read-only 消费各 feature 的 `closeout.md`，写入 `features/release-vX.Y.Z/release-pack.md` + `docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md` + `CHANGELOG.md` 的 `[vX.Y.Z]` 段 + `docs/release-notes/vX.Y.Z.md`（按存在）。Workflow 11 步覆盖 entry-vs-recovery / 候选盘点 / scope ADR 起草 / SemVer 决策 / worktree 盘点 / release-wide regression（协议内联）/ cross-feature traceability 摘要 / pre-release engineering checklist / evidence matrix / release pack 产出 / interactive Final Confirmation。SKILL.md 通过 `audit-skill-anatomy.py` 全部检查（含 `Common Rationalizations` 必需段、禁 `和其他 Skill 的区别`、< 500 行预算）。配 3 份 references 模板（`release-scope-adr-template.md` / `pre-release-engineering-checklist.md` / `release-pack-template.md`）+ `evals/` baseline 4 条用例。(ADR-004 D1, D2, D3, D5, D6, D7)
- **`.claude/commands/release.md`** — 第 7 条 Claude Code slash 命令。语义与既有 6 条不同：**direct invoke** `skills/hf-release/SKILL.md`，**不**先经 `using-hf-workflow` → `hf-workflow-router`（与 `/spec` / `/plan` / `/build` / `/review` / `/ship` 的"router-first"模式区分）。命令体明列 11 步 workflow 简版 + Hard rules（standalone、engineer-level only、no auto git tag、no ops actions）。OpenCode / Cursor **不**注册等价 slash 命令文件——延续 ADR-001 D3 + ADR-003 D6 立场，那两家走 NL + entry shell 触发。(ADR-004 D4)
- **`docs/decisions/ADR-004-hf-release-skill.md`** — v0.4.0 完整范围决策；2026-05-09 锁定 9 项决策（D1 引入 `hf-release` / D2 与 `hf-shipping-and-launch` 正交不替代 / D3 完全解耦于 router / D4 新增 `/release` slash 命令 / D5 standalone 不依赖任何上游 skill 已运行 / D6 release-tier 工件目录用 `features/release-vX.Y.Z/` / D7 内置 SemVer + pre-release 默认 / D8 v0.4.0 仍是 pre-release / D9 不刷新 `examples/writeonce/` demo evidence trail）。

### Changed

- **`.claude-plugin/plugin.json`** — `version` 从 `0.3.0` 升级到 `0.4.0`。
- **`.claude-plugin/marketplace.json`** — plugin description 从 23 hf-* 升级到 24 hf-*，加入 `release (hf-release, v0.4.0)` 条目，并显式说明"engineer-level release; deployment / staged rollout / monitoring / rollback remain v0.5+ planned `hf-shipping-and-launch`"。
- **`skills/using-hf-workflow/SKILL.md`** — § 5 entry bias 表加 1 行（"切版本 / 出 release / 打 tag / 发版本号" → direct invoke `hf-release`）；`Boundary With Product Skills` 段加 1 行说明（`hf-release` 是 release-tier 独立 skill，不进 coding family / discovery family 主链，不进 router transition map；entry shell 加这一行只用于"用户表达切版本意图时直接 direct invoke"）。**审视过 router 不动**：`skills/hf-workflow-router/references/profile-node-and-transition-map.md` 不改、`skills/hf-finalize/SKILL.md` 不改、`skills/hf-regression-gate/SKILL.md` 不改、`skills/hf-doc-freshness-gate/SKILL.md` 不改——release-wide regression 协议与 sync-on-presence 协议**内联**到 `hf-release` 自己（D3 / D5）。
- **`README.md` + `README.zh-CN.md`** — Scope Note 升级到 v0.4.0；Slash 命令表从 6 → 7（新增 `/release` 行）；skill 数 23 → 24；项目概览 / Workflow Shape 段对照说明 `hf-release` 为 release-tier 独立 skill 不进主链；"What is NOT included" 调整：`hf-shipping-and-launch` 仍延后到 v0.5+，但 `hf-release` 从延后清单移除。
- **`docs/claude-code-setup.md`** — 顶部句子 v0.3.0 → v0.4.0；Scope Note 重写为 v0.4.0（3 客户端不变、24 skills、新增 `/release` 命令、`hf-shipping-and-launch` 仍 v0.5+ planned）；Slash 命令章节加 `/release` 行；§ 4 "What is NOT included in v0.3.0" → "v0.4.0"，6 ops skill 修订为 5 + 1 deferred-but-renamed（`hf-release` 已落地，剩余 5 项 ops skill 仍延后）；§ 6 cross-references 加 ADR-004。
- **`docs/opencode-setup.md`** — 顶部句子 + Scope Note v0.3.0 → v0.4.0；`/skills` 验证清单 23 → 24（追加 `hf-release`）；NL intent → node 映射加"切版本 / 出 release"行直指 `hf-release`（**direct invoke**，不经 router）；§ 7 "What is NOT included" 同步 v0.4.0 措辞；§ 8 cross-references 加 ADR-004。
- **`docs/cursor-setup.md`** — 同形改动：顶部、Scope Note、`.cursor/rules/harness-flow.mdc` 解读段、§ 4 NL intent → router 映射加"切版本 / 出 release"行直指 `hf-release`、§ 6 "What is NOT included in v0.3.0" → "v0.4.0"、§ 7 cross-references 加 ADR-004。
- **`.cursor/rules/harness-flow.mdc`** — `Scope honesty` 段更新到 v0.4.0：声明 v0.4.0 引入了 `hf-release` 作为 release-tier 独立 skill，**不**进主链；剩余 5 项 ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）继续延后到 v0.5+ roadmap（ADR-004 D2）；3 deferred personas + 4 deferred clients 立场不变。
- **`SECURITY.md`** — Supported Versions 表加 `0.4.x` 行；`0.3.x` 降级为 security-only；`0.2.x` 降级为 older；out-of-scope 段对 ADR 的引用补全为 ADR-001 D1 + ADR-002 D1 + ADR-003 D2 + ADR-004 D2。
- **`CONTRIBUTING.md`** — 引言版本号 `v0.3.0` → `v0.4.0` + Scope Note 文案更新（24 skills、`/release` 命令、`hf-shipping-and-launch` 仍 v0.5+ planned）；Will accept / Will defer 段补 ADR-004 与 v0.5+ 引用；feature_request 提示从 ADR-003 改成 ADR-004 first。

### Decided

- **v0.4.0 仍是 pre-release** on GitHub Releases。理由：主链覆盖未达 100%（仍缺 5 项 ops/release skill；ADR-004 D2 显式不补）；客户端面无变化（仍 3 家）；与 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 同向，版本号不跨 v1.0。(ADR-004 D8)
- **`hf-release` 与 `hf-shipping-and-launch` 正交，不替代。** `hf-release` 处理"版本切片"（多 feature → vX.Y.Z + 全量回归 + 发布文档聚合）；`hf-shipping-and-launch`（v0.5+ planned，**当前尚未实现**）处理"上线时刻"（feature flag / staged rollout / 监控 / 回滚）。两者解决的工程问题不同，合并违反 `docs/principles/skill-anatomy.md` 一个 skill 一个 concern 立场。(ADR-004 D2)
- **`hf-release` 完全解耦于 `hf-workflow-router`。** 不进 transition map，不修改主链 FSM，不与 `hf-finalize` / `hf-regression-gate` / `hf-doc-freshness-gate` 互引；release-wide regression 协议与 sync-on-presence 协议**内联**到 `hf-release` 自身。(ADR-004 D3, D5)
- **`/release` 命令在 Claude Code 注册；OpenCode / Cursor 不注册等价 slash 命令文件。** 沿用 ADR-001 D3 + ADR-003 D6 立场（OpenCode / Cursor 走 NL + entry shell）。(ADR-004 D4)
- **release-tier 工件目录用 `features/release-vX.Y.Z/`。** 与 router 既有 `features/<active>/` 路径假设兼容；不引入新顶级目录扩大工作面承诺。(ADR-004 D6)
- **`hf-release` 内置 SemVer + pre-release 默认策略，但允许项目级覆盖。** 默认沿用 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 "主链未达 100% 时勾 pre-release" 立场；项目可在自家 guidelines / `CONTRIBUTING.md` 中显式声明 CalVer / 项目自定义版本策略。(ADR-004 D7)
- **不刷新 `examples/writeonce/` demo evidence trail。** 与 ADR-003 D10 同向；`hf-release` 是 standalone skill 不进主链，writeonce demo 没有自然演示位；强加 refresh 段是空洞的版本号同步。(ADR-004 D9)
- **官方支持客户端仍为 Claude Code + OpenCode + Cursor（3 家）。** 其余 4 家（Gemini CLI / Windsurf / GitHub Copilot / Kiro）继续延后到 v0.5+。

### Deferred (to v0.5+)

- 6 项原 deferred ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）**全部**继续延后到 v0.5+。v0.4.0 新增的 `hf-release` 是**新 skill**（不在原 6 项 deferred 列表中），覆盖"工程级版本切片"切面（多 feature 汇总 / scope ADR / release-wide regression / 发布文档聚合 / tag readiness）；它**不**替代 `hf-shipping-and-launch`，二者正交（前者管"版本切片"，后者管"上线时刻"）。与 ADR-001 D1 / ADR-002 D1 / ADR-003 D2 / ADR-004 D2 一致。
- 4 家剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）+ Gemini CLI 的 6+1 条 slash 命令。
- 3 个 user-facing personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）+ `agents/` 命名空间约定 + `docs/principles/persona-anatomy.md`。
- 真实环境 install smoke 硬门禁（视客户端面铺开节奏 / 真实事故触发再启动）。
- `docs/principles/` 其它段落升级为合规基线（继续保持 ADR-001 D11 "设计参考" 性质）。
- `audit-skill-anatomy.py` 升级为 hard gate（视 SKILL.md 漂移率）。
- `examples/writeonce/` demo evidence trail 下次主链节点变更或 release-tier dogfood 同步触发。

### Notes

- v0.4.0 是 v0.3.0 之后的第一个 minor release，体现"先把客户端面收敛、再把 release-tier 切片做出来"的节奏：v0.1.0 → v0.2.0 是质量纪律内核硬化（`hf-browser-testing` + audit advisory + `Common Rationalizations` 合规基线）；v0.3.0 是单客户端扩张（Cursor，2 → 3 家）；v0.4.0 首次扩 skill 集合（23 → 24）但限制为 release-tier 独立 skill。
- `hf-release` 起草借鉴了 `addyosmani/agent-skills` 的 `shipping-and-launch` SKILL anatomy 风格（process 分小节 + verification 前后两段 + red flags + rationalizations），但内容上严格停在工程级 release。`addyosmani/shipping-and-launch` 对应的 HF 等价物是 v0.5+ planned `hf-shipping-and-launch`（**当前尚未实现**），与 `hf-release` 正交。
- `hf-release` 第一次为 standalone 工具型 skill 在 entry shell 开 direct invoke 通道（既有 `using-hf-workflow` § 5 entry bias 表的 6 行均涉及 router-first；本次新增第 7 行直 direct invoke `hf-release`）。这是"分类器层" vs "runtime FSM 层"的明确分离——entry shell 仍只识别意图、分流给正确 leaf skill，不替代 router 做任何 authoritative routing。
- 本 release 是新 skill + 1 条命令 + entry shell 1 行 patch + 元数据 / 文档同步，工作面规模与 v0.3.0 patch 量级相当；不涉及主链 FSM 编辑、router transition map 编辑、demo 工件刷新。
- v0.4.0 GA 之后，HF 自身的下一次发版可以用 `hf-release` 走通自举（dogfood）；首次 dogfood 需手工对照 ADR-001/002/003/004 模板做，验证 `references/release-scope-adr-template.md` 实战可用。

## [0.3.0] - 2026-05-09 — pre-release

> **Third public release.** Marked as a **pre-release** on GitHub Releases.
>
> v0.3.0 is a **single-client-expansion** release. 在 v0.2.1 基础上把 **Cursor** 加入正式支持的客户端列表（成为第 3 家），**不**新增任何 `hf-*` skill，**不**引入 personas，**不**改主链 FSM。Skill 集合保持 23 `hf-*` + `using-hf-workflow` 不变；主链终点保持 `hf-finalize` 不变；其余 4 家延后客户端（Gemini CLI / Windsurf / GitHub Copilot / Kiro）继续延后到 v0.4+。
>
> 完整范围决策见 [`docs/decisions/ADR-003-release-scope-v0.3.0.md`](docs/decisions/ADR-003-release-scope-v0.3.0.md)（10 项决策；与 ADR-002 D11 同向，"窄而硬，一次进一家"）。

### Added

- **`.cursor/rules/harness-flow.mdc`** — Cursor 入口规则，frontmatter `alwaysApply: true`。每次 Cursor 会话自动加载，告诉 agent 把 `skills/using-hf-workflow/SKILL.md` 作为入口 shell 加载、在意图模糊时切换到 `skills/hf-workflow-router/SKILL.md`，并执行 HF 的 hard rules（One Current Active Task / 评审与门禁是 first-class 节点 / evidence-based routing / Fagan 作者-评审分离）。文件附带 scope-honesty 段：v0.3.0 没有改主链、没加新 skill、没引入 personas。(ADR-003 D1, D6)
- **`docs/cursor-setup.md`** — Cursor 集成完整 setup 文档（109 行起），同形于 `docs/claude-code-setup.md` 与 `docs/opencode-setup.md`：
  - § 1 install：A. clone-and-open 本仓库；B. vendor 到自己项目（`.cursor/rules/` + `skills/` 软链接）
  - § 2 the shipped rule：解释 `.cursor/rules/harness-flow.mdc` 干什么 / 为什么不要替换为 cheatsheet
  - § 3 verify：first prompt + 期望路由行为
  - § 4 NL intent → router 映射（9 行表，含 `hf-browser-testing`）
  - § 5 troubleshooting（7 行表）
  - § 6 What is NOT included in v0.3.0（明列 6 ops skill / 4 延后客户端 / 3 personas / install smoke 不是硬门禁）
  - § 7 cross-references（ADR-003 + ADR-002 + ADR-001 + 其他 setup 文档 + Cursor rules 官方文档）
- **`docs/decisions/ADR-003-release-scope-v0.3.0.md`** — v0.3.0 完整范围决策；2026-05-09 锁定 10 项决策（D1 仅引入 Cursor / D2 不引入新 skill / D3 不引入 personas / D4 主链终点不变 / D5 仍是 pre-release / D6 Cursor 走 NL + router 不注册 slash 命令 / D7 不增设 install smoke 硬门禁 / D8 audit 仍是 advisory / D9 docs/principles/ 仍是设计参考 / D10 不刷新 demo evidence trail）。

### Changed

- **`.claude-plugin/plugin.json`** — `version` 从 `0.2.1` 升级到 `0.3.0`。
- **`.claude-plugin/marketplace.json`** — plugin description 末尾追加："v0.3.0 adds Cursor as the third officially-supported client (Claude Code + OpenCode + Cursor)"，skill 数 23 不变。
- **`README.md` + `README.zh-CN.md`** — Scope Note 升级到 v0.3.0 pre-release（3 客户端：Claude Code + OpenCode + Cursor）；Installation 段头部从"两条路径 / Both paths"改为"三条路径 / All three paths"；新增 `### Cursor (new in v0.3.0)` / `### Cursor（v0.3.0 新增）` 子段；"Other clients (deferred)" 子段从 v0.2+ → v0.4+，列表从 5 家改为 4 家（Cursor 移出延后列表）；Slash Commands 段尾追加"OpenCode and Cursor do not ship slash command files"说明（ADR-003 D6）。`README.zh-CN.md` 顺手修复 v0.2.0 sync 时漏掉的一处 `22 个 hf-*` → `23 个 hf-*`（OpenCode `/skills` 验证行；英文 README 在 v0.2.0 时已修复）。
- **`docs/claude-code-setup.md`** — 顶部句子 v0.2.0 → v0.3.0；Scope Note 重写为 v0.3.0（3 客户端，4 家延后）；§ 4 "What is NOT included in v0.2.0" → "v0.3.0"，"No 5-client expansion" → "No 4-client expansion"，Cursor 从延后列表移除；§ 6 cross-references 加 ADR-003 与 cursor-setup.md。
- **`docs/opencode-setup.md`** — 同形改动：顶部句子、Scope Note、§ 7 "What is NOT included in v0.3.0"、§ 8 cross-references 加 ADR-003 与 cursor-setup.md。
- **`SECURITY.md`** — Scope 段 setup 文档列表加 `docs/cursor-setup.md` + `.cursor/rules/harness-flow.mdc`；Supported Versions 表加 `0.3.x` 行，`0.2.x` 降级为 security-only，`0.1.x` 降级为 older；out-of-scope 段对 ADR 的引用补全为 ADR-001 D1 + ADR-002 D1 + ADR-003 D2。
- **`CONTRIBUTING.md`** — 引言版本号 `v0.2.0` → `v0.3.0` + Scope Note 文案更新（Cursor + "no new skills, no personas"）；Will accept / Will defer 段补 ADR-003 与 v0.4+ 引用；新增 personas 行（ADR-002 D11 + ADR-003 D3 延后到 v0.4+）；Known Limitations 段重写：CI 仍是 v0.4+ work item、audit script advisory（ADR-002 D5 + ADR-003 D8）、install smoke 不是硬门禁（ADR-003 D7）；feature_request 提示从 ADR-001 改成 ADR-003 first。

### Decided

- **v0.3.0 仍是 pre-release** on GitHub Releases。理由同 ADR-001 D6 / ADR-002 D6：主链未达 100%（仍缺 6 项 ops；ADR-003 D2 显式不补）；客户端面只增加 1 家（2 → 3）不构成 GA 信号。(ADR-003 D5)
- **官方支持客户端为 Claude Code + OpenCode + Cursor（3 家）。** 其余 4 家（Gemini CLI / Windsurf / GitHub Copilot / Kiro）继续延后到 v0.4+。沿用 ADR-002 D11 "一次进一家" 立场——v0.3.0 先把 Cursor 落地，其余客户端待真实使用反馈成熟后再批量进。(ADR-003 D1)
- **主链终点仍是 `hf-finalize`**。v0.3.0 不引入任何新主链节点。(ADR-003 D2, D4)
- **Cursor 集成走 rules-based 路径，不注册 Cursor slash 命令。** 与 OpenCode 一致采取 NL + router 模型；Claude Code 的 6 条短 slash 命令（ADR-001 D4）是 Claude-Code-specific 历史决策，不向 Cursor 复制。(ADR-003 D6)
- **不增设真实环境 install smoke 硬门禁。** 沿用 ADR-002 D11 撤回 D3 的判断；3 家客户端仍然是 maintainer 自验范围；Cursor 路径承担与 v0.1.x stabilization "Known Limitations" 相同的"已知缺口"性质（cloud agent VM 无 Cursor binary）。(ADR-003 D7)
- **`audit-skill-anatomy.py` 仍是 advisory**（不升级为 hard gate；ADR-003 D8）。
- **`docs/principles/` 其余段落继续保持 "设计参考" 性质**（ADR-001 D11 + ADR-002 D10 + ADR-003 D9）；`Common Rationalizations`（必需）+ `和其他 Skill 的区别`（禁止）两节是 v0.2.0 起的硬规则，v0.3.0 不扩展硬规则面。
- **不刷新 `examples/writeonce/` demo evidence trail。** v0.3.0 没有新主链节点 / 没改 skill 集合 / 没改 SKILL.md 内容；按 ADR-001 D9 "demo deliverable is the trail of HF main-chain artifacts" 立场，没有新工件可加，强加 refresh 段会是空洞的版本号同步。(ADR-003 D10)

### Deferred (to v0.4+)

- 6 项剩余 ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）—与 ADR-001 D1 / ADR-002 D1 / ADR-003 D2 一致。
- 4 家剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）+ Gemini CLI 的 6 条 slash 命令（含原 `/plan` → `/planning` 重命名）。ADR-002 D11 撤回的 R3 实现 commit `18b1d99` / `0c93809` 在 v0.3.0 仅取 Cursor 部分手工摘出复用，其余 4 家继续在 git 历史中等待 v0.4+ cherry-pick。
- 3 个 user-facing personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）+ `agents/` 命名空间约定 + `docs/principles/persona-anatomy.md`。ADR-002 D11 撤回的 D4 / D8 在 v0.3.0 继续延后；R4 实现 commit `560ac26` 同样保留在历史中等待 v0.4+ cherry-pick。
- 真实环境 install smoke 硬门禁（视客户端面铺开节奏 / 真实事故触发再启动）。
- `docs/principles/` 其它段落升级为合规基线（继续保持 ADR-001 D11 "设计参考" 性质）。
- `audit-skill-anatomy.py` 升级为 hard gate（视 SKILL.md 漂移率）。
- `examples/writeonce/` demo evidence trail 下次主链节点变更时同步触发。

### Notes

- v0.3.0 是 v0.2.1 之后的第一个 minor release，体现"一次进一家"的客户端铺开节奏：v0.1.0 起步 2 家（Claude Code + OpenCode），v0.3.0 加 1 家（Cursor → 3 家），v0.4+ 视真实使用反馈再决定下一家。
- Cursor 集成内容（`docs/cursor-setup.md` + `.cursor/rules/harness-flow.mdc`）的种子来源是 ADR-002 R3 的 commit `18b1d99`（被 D11 撤回）。v0.3.0 选择手工摘 Cursor 部分 + 重写文案匹配 v0.3.0 承诺面（3 客户端、ADR-003 而非 ADR-002 D2）；未做 git cherry-pick，因为原 R3 commit 同时引入 5 客户端 + 5 份 setup 文档，整 cherry-pick 会带入 4 家不需要的工件。
- v0.2.1 的两个 install bug（marketplace SSH 默认 + name-collision）是 Claude Code 一家的，与 Cursor 集成正交；它们已经在 v0.2.1 修复，并在 `docs/claude-code-setup.md` 留下了恢复说明。Cursor 自己的真实环境 install smoke 仍是 known limitation（ADR-003 D7）。
- 本 release 是 doc-and-metadata-only 加 1 个 Cursor rule 文件，工作面规模与 v0.2.1 patch 量级相当；不涉及 SKILL.md 内容编辑、router profile-node 表编辑、demo 工件刷新。

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

[Unreleased]: https://github.com/hujianbest/harness-flow/compare/v0.5.1...HEAD
[0.5.1]: https://github.com/hujianbest/harness-flow/releases/tag/v0.5.1
[0.5.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.5.0
[0.4.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.4.0
[0.3.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.3.0
[0.2.1]: https://github.com/hujianbest/harness-flow/releases/tag/v0.2.1
[0.2.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.2.0
[0.1.0]: https://github.com/hujianbest/harness-flow/releases/tag/v0.1.0

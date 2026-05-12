# ADR-008: HarnessFlow v0.6.0 对外发布范围

- 状态：accepted（2026-05-12，hf-release §11 auto mode Final Confirmation 通过 + release pack `Status: ready-for-tag`）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 协作契约执行）
- 关联文档：
  - `docs/decisions/ADR-005-release-scope-v0.5.0.md`（v0.5.0 引入 closeout HTML companion；v0.6+ roadmap 中的 5 个 ops/release skills + 4 客户端 + 3 personas + writeonce demo trail 重跑由本 ADR 重新评估）
  - `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`（v0.5.1 patch；本 ADR 在此 anatomy v2 基础上推进，不动 anatomy）
  - `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md`（v0.6.0 唯一新引入的核心工程能力——install/uninstall scripts；本 ADR 把它纳入 v0.6.0 范围并把 ADR-007 状态在 §11 Final Confirmation 时翻 accepted）
  - `docs/decisions/ADR-004-hf-release-skill.md`（v0.4.0 引入 hf-release；本 ADR 是该 skill 的第四次 dogfood）
  - `features/release-v0.6.0/release-pack.md`（本 ADR 配套 release pack）
  - `features/001-install-scripts/closeout.md`（本版唯一候选 feature 的 workflow-closeout 工件）

## 背景

v0.5.0 / v0.5.1 是 HF 的两次 closeout HTML 工作总结报告相关 release：v0.5.0 引入 `hf-finalize` step 6A + `scripts/render-closeout-html.py`，v0.5.1 把脚本从仓库根 `scripts/` 物理迁移到 `skills/hf-finalize/scripts/` 修复 vendoring 缺陷，并把 HF skill anatomy 从 3 类子目录锁到 4 类（`SKILL.md` + `references/` + `evals/` + `scripts/`）。两次 release 都是 patch / minor 范围，没有改变客户端面（仍是 Claude Code + OpenCode + Cursor 三家），没有改变 skill 集合（仍是 24 hf-* + using-hf-workflow），没有引入 personas，也没有触动 `hf-shipping-and-launch` 等 5 个 ops/release skills。

v0.5.x 阶段累积了一个真实的工程缺口反馈：HF 三种官方集成路径里，OpenCode `.opencode/skills/` 与 Cursor `.cursor/rules/` 这两条都依赖用户**手动**执行 `mkdir + cp -R + ln -s` 完成 vendoring。这有 4 个具体痛点（来自同侪项目 `affaan-m/everything-claude-code` install 拓扑对比）：

1. **多步操作**：用户需要分别处理 skills 目录、rule 文件、可能的全局 `~/.config/opencode/skills`，错一步不会有清晰报错
2. **无幂等保证**：第二次运行 `cp -R` 会覆盖宿主已修改的同名文件，但没有 dry-run / backup
3. **无卸载手段**：装完之后想退出，没有"我装了哪些文件"的 manifest，宿主仓库不知道哪些文件是 HF 装进来的
4. **缺少跨拓扑兼容**：Cursor / OpenCode 两边的目录布局不同，当前手册要求用户**自己理解差异**

ADR-006 D2 在 v0.5.1 已经正面承认过类似 vendoring bug（hf-finalize 渲染脚本误放仓库根 `scripts/`），但那次只解决"工具是否在 vendor 树里"，没有解决"vendor 这件事本身能不能一键化"。

工作面盘点（2026-05-12 grep 实测）：

- 候选 feature 数：1 个（`features/001-install-scripts/closeout.md` `Closeout Type: workflow-closeout`，2026-05-11 closed）
- closeout 状态：每条 evidence matrix 项都 `present`；HYP-002 Blocking + NFR-002 双双有直接 PASS 证据；scenario #1-#14 全 PASS（14/14）
- regression 入口存在性：`tests/test_install_scripts.sh`（feature 自身）+ `scripts/audit-skill-anatomy.py`（HF 跨 skill 维护）+ `scripts/test_audit_skill_anatomy.py` + `skills/hf-finalize/scripts/test_render_closeout_html.py`，共 4 类 release-wide regression 入口
- 元数据现状：`.claude-plugin/plugin.json` version=0.5.1；`.claude-plugin/marketplace.json` 描述包含 v0.5.1 vendoring fix；`SECURITY.md` Supported Versions 表最新行 `0.5.x`；`CONTRIBUTING.md` 引言版本号 `v0.5.1`；`.cursor/rules/harness-flow.mdc` Hard rules 段引用 v0.5.0 / v0.5.0+ 标记；`docs/cursor-setup.md` / `docs/opencode-setup.md` / `docs/claude-code-setup.md` 已在 001-install-scripts feature 的 T10b doc sync 中部分同步到 v0.6.0 的 install scripts 表面

为什么这次 release 不应该把 v0.6+ deferred 项一次清完——P-Honest 立场（同 ADR-005 D7）：

- **5 个 ops/release skills**（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）：跨度大、涉及部署/监控/回滚/SLO 等真实生产能力；本版主线工作（install scripts）已经走完整 SDD 主链 6 周次（spec×2 / design×2 / tasks×2 / TDD / test-review×2 / code-review / traceability×2 / regression / doc-freshness / completion / finalize），再叠加 5 个 ops skills 会让 v0.6.0 同时承担两件性质迥异的事，违反"窄而硬"立场
- **4 个剩余客户端**（Gemini CLI / Windsurf / GitHub Copilot / Kiro）：本版没有真实使用反馈触发其纳入；ADR-003 D6 沿袭至今的"一次进一家"策略仍然适用
- **3 个 personas**（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）：ADR-002 D11 已经撤回过，ADR-003 / ADR-004 / ADR-005 全部维持 deferred
- **writeonce demo evidence trail 重跑**：低频价值；ADR-005 D7 显式 deferred；本版不触发其重新评估的条件

本 ADR 一次性锁定 v0.6.0 对外发版的 8 项范围决策。

## 决策

### Decision 1 — 本版引入 1 个核心工程能力：HF install/uninstall scripts

v0.6.0 把 `features/001-install-scripts/`（已 workflow-closeout）的工程交付物正式纳入对外发布：

- 仓库根 `install.sh` + `uninstall.sh`（bash 3.2+ 兼容、零新增运行时依赖）
- 仓库根 `tests/test_install_scripts.sh`（14 scenario e2e driver）
- 5 处文档同步：`docs/cursor-setup.md` §1.B / `docs/opencode-setup.md` §1.A / §1.B / §2 / line 20 / `README.md` / `README.zh-CN.md` 各自的 OpenCode 与 Cursor 安装段
- ADR-007（install-scripts-topology-and-manifest）状态在 §11 Final Confirmation 通过时翻 `accepted`

理由：

- **真实工程缺口**：v0.5.x 三种官方集成路径里两种（OpenCode + Cursor）的 vendoring 仍然手动；ADR-007 的 5 个关键决策（D1 纯 shell / D2 manifest 唯一权威 + per-skill entries / D3 不依赖 jq / D4 cursor vendor 路径 / D5 post-install readme）已经走完 SDD 主链
- **完整 evidence**：feature workflow-closeout，14/14 e2e PASS，HYP-002 Blocking（用户自加 skill uninstall 后保留）+ NFR-002（中途失败 rollback 闭合）双双有直接 PASS 证据
- **零依赖**：不引入 jq / python / node / npm，与 HF 自身依赖最小化哲学一致
- **不破坏既有 anatomy**：install scripts 落仓库根而非 `skills/<name>/scripts/`，因为它们是仓库级入口而非 skill-owned 工具；ADR-006 D1 锁定的 4 类子目录约定不动

### Decision 2 — 本版**不**引入新的 hf-* skill；skill 集合稳定在 24 hf-* + using-hf-workflow

v0.6.0 不新增 / 不修改 / 不移除任何 `hf-*` skill。install scripts 不被建模为 hf-* skill，因为它们是仓库级入口而非工作流节点（不在 `hf-workflow-router` transition map 内，也不被 `using-hf-workflow` entry shell bias 表引用）。

理由：

- **窄而硬**立场：本版的核心工程交付是 install scripts；额外引入新 skill 会稀释 review 焦点
- **anatomy 一致性**：install scripts 不属于任何 skill 的 4 类子目录之一，强行套 skill 是 over-modeling
- **路径选择有 ADR 锚定**：ADR-007 D-impl-notes 显式说"install scripts 落仓库根（与 ECC 同源）；ADR-006 D1 收紧的'仓库根 scripts/'是指 python 工具，shell 入口脚本仍允许在根目录"

### Decision 3 — pre-release 标记沿用：vX.Y.Z 在 GitHub Releases 仍**勾选 pre-release**

v0.6.0 在项目 release 渠道（GitHub Releases）上 **勾选 pre-release**，沿用 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 / ADR-004 D6 / ADR-005 D8 / ADR-006 D3 立场。

理由：

- **主链覆盖**：v0.6.0 没有改变主链节点集合（仍是 product-discovery → ... → finalize），主链覆盖度同 v0.5.x
- **客户端面**：仍是 3 家（Claude Code + OpenCode + Cursor），没有质变
- **用户场景**：install scripts 是新引入的入口能力，需要真实使用反馈一段时间才能宣称稳定
- **ops 缺口仍在**：5 个 deferred ops/release skills 仍未实现；HF 主线终点仍是 `hf-finalize`（单 feature 工程级 closeout），距离 GA 缺口未填

### Decision 4 — 版本号 bump 决策：从 v0.5.1 → **v0.6.0（minor bump）**

按 SemVer 2.0.0 决策表：

- **breaking change 清单（含/不含）**：本版**不含** breaking change。install scripts 是新增的可选入口，老用户继续走文档手册的"manual fallback"路径完全不受影响；HF 自身的 24 个 hf-* + using-hf-workflow 行为完全不变；CLI / SKILL.md / 任何 SDD 工件 schema 都不变。
- **新功能（backward-compatible）**：install/uninstall scripts + tests/test_install_scripts.sh + ADR-007 + 5 处 doc sync——按 SemVer 应为 **minor bump**
- **bug fix（backward-compatible）**：本版无独立 bug fix 项目（install scripts 是新功能，不是 fix）

按 SemVer 2.0.0：含 backward-compatible 新功能（无 breaking）→ **minor bump**。从 v0.5.1 切到 v0.6.0 跨 minor 段。

### Decision 5 — v0.6+ Roadmap 的 deferred 项**不**在本版承担

显式列出本版 **不做** 的事：

- **5 个 ops/release skills**：`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`——继续 deferred
- **4 个剩余客户端**：Gemini CLI / Windsurf / GitHub Copilot / Kiro——继续 deferred
- **3 个 personas**：`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`——继续 deferred
- **install scripts 的 7 项 deferred**（来自 `features/001-install-scripts/spec-deferred.md` DEF-001..DEF-007）：
  - DEF-001 Windows PowerShell `install.ps1`
  - DEF-002 Claude Code 的 install 脚本（marketplace 已覆盖）
  - DEF-003 `npx hf-install` Node 包
  - DEF-004 Global install 多版本共存
  - DEF-005 install 脚本对 `AGENTS.md` 的写入或 merge
  - DEF-006 install 脚本的 telemetry / 使用统计
  - DEF-007 install 脚本调起 HF 自身 audit / lint
- **install scripts 的 ADR-007 D4 alternative A3**（cursor rule 路径自动重写）：post-install README 已给出 in-place 提示作为过渡
- **writeonce demo evidence trail 重跑**：维持 ADR-005 D7 立场

理由：

- **窄而硬**：本版主线（install scripts）已经走完整 6 周次 SDD review；再叠加任一 deferred 项都会让 v0.6.0 失焦
- **deferred 项各有自身评估窗口**：5 个 ops/release skills 需要先有真实部署场景反馈；4 个客户端需要真实使用证据；3 个 personas 在 ADR-002 D11 之后立场未变
- **install scripts deferred 7 项**：DEF-001/-003/-005/-006/-007 在 ADR-007 D5 自身已经显式排除；DEF-002 因 Claude Code 走 marketplace 不需要；DEF-004 多版本共存属于 v0.6+ usage 反馈触发

### Decision 6 — Release-wide regression 范围

v0.6.0 的 release-wide regression 范围 = `union(候选 feature affected modules)` = `install.sh` + `uninstall.sh` + `tests/test_install_scripts.sh` + `docs/cursor-setup.md` + `docs/opencode-setup.md` + `README.md` + `README.zh-CN.md` + `CHANGELOG.md` + 各 hf-* skill anatomy（验证 install scripts 不破坏既有 skill 体系）。

具体 regression 入口（5 类）：

1. `bash tests/test_install_scripts.sh`（feature 自身 14 scenario）
2. `python3 scripts/audit-skill-anatomy.py`（验证 24 hf-* + using-hf-workflow anatomy 完整）
3. `python3 scripts/test_audit_skill_anatomy.py`（audit 自身单元测试）
4. `python3 skills/hf-finalize/scripts/test_render_closeout_html.py`（v0.5.0/v0.5.1 引入的 hf-finalize 渲染单测）
5. `(awk '!/^[[:space:]]*#/' install.sh uninstall.sh) | grep -E '\b(jq|python|node|npm)\b'`（NFR-004 锁定）

理由：本版唯一 affected module 是 install scripts 本身 + 它接触的 5 个 doc 文件；不需要整体跑 HF 全部资产，只需保证既有 skill 体系不被新增工件破坏。fresh-evidence 时间戳必须晚于 001-install-scripts 最晚 closeout 时间（2026-05-11）。

### Decision 7 — Cross-feature traceability 摘要

v0.6.0 候选 feature 仅 1 个（001-install-scripts），不存在跨 feature traceability 风险（无跨 feature API 变化 / 无跨 feature 共享 contract）。`release-traceability.md` 直接复用 001-install-scripts 自身的 `reviews/traceability-review.md`（Round 2 verdict 通过）作为 feature-level verdict 锚点，不重做单 feature traceability。

理由：单候选 feature 时不需要跨 feature 聚合分析；按 hf-release §7 立场"只做版本级聚合，不重做单 feature traceability"。

### Decision 8 — `install.sh` 与 `uninstall.sh` 不进入 hf-skill anatomy v2 的 4 类子目录约定

仓库根 `install.sh` / `uninstall.sh` / `tests/test_install_scripts.sh` 不归入 ADR-006 D1 锁定的 `skills/<name>/scripts/` 子目录约定。它们是**仓库级入口**而非 **skill-owned 工具**：

- **受众**：用户（每个想 vendor HF 的人都要跑 install）vs ADR-006 区分的"维护者跨 skill 工具"（`scripts/audit-skill-anatomy.py`，受众是 HF contributor）vs "skill-owned 工具"（`skills/<name>/scripts/`，受众是用该 skill 的项目）
- **触发场景**：在用户 clone HF 仓库后**首次** vendor 进自己仓库时执行 vs `scripts/audit-skill-anatomy.py` 在 HF 自身 CI 跑 vs `skills/hf-finalize/scripts/render-closeout-html.py` 在 hf-finalize step 6A 跑
- **vendor 路径影响**：install/uninstall scripts 不在用户的 vendor 树里（用户 vendor 后是 `.opencode/skills/` 与 `.cursor/harness-flow-skills/`，install 脚本本身不被 vendor），所以放仓库根而非 `skills/<some-name>/scripts/`

理由：ADR-006 D1 锁定的 4 类子目录约定是**针对 skill-owned 工具**，install scripts 不属于此类；仓库根级别保留入口脚本是行业惯例（参考 ECC `install.sh`、Cargo / Bundler / npm 的 install workflow）。本 ADR 不修改 ADR-006 D1，只把 ADR-006 D1 的边界澄清写到本 D8。

## Tradeoffs（已考虑的备选 + 拒绝理由）

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| D1 范围 | 一次清完 v0.6+ 5 个 ops/release skills + 4 客户端 + 3 personas + writeonce demo trail 重跑 | 本版主线（install scripts SDD 6 周次）已是 cloud agent 单进程能力上限；叠加 deferred 项会让 v0.6.0 同时承担两件性质迥异的事，违反窄而硬立场 |
| D1 范围 | 把 install scripts 也算 patch（v0.5.2 而非 v0.6.0） | install scripts 是新功能（backward-compatible），不是 bug fix；按 SemVer 应为 minor bump；patch 版本号在用户感知上等同"小修小补"，与 install scripts 引入的能力不符 |
| D2 skill 集合 | 把 install scripts 包装成 `hf-install` skill | install scripts 不在主链 FSM 内，不是 workflow 节点；包装成 skill 会让 router transition map 与实际行为脱节；ADR-007 D-impl-notes 显式 deferred 此选项 |
| D3 pre-release | 直接 GA / 跨 v1.0 | 主链覆盖 + 客户端面 + 用户场景三轴均无质变；ops 缺口仍在；GA 需要更稳定的真实使用反馈 |
| D4 版本号 | major bump v1.0.0 | 无 breaking change；major bump 不符合 SemVer 2.0.0 决策表；GA 立场未到 |
| D4 版本号 | patch bump v0.5.2 | install scripts 是新功能，不是 fix；patch 不符合 SemVer 2.0.0 决策表 |
| D5 deferred | 把 5 个 ops/release skills 中的 1-2 个（如 `hf-ci-cd-and-automation`）纳入本版 | 没有真实使用反馈触发；ops 类 skill 设计深度不亚于 install scripts，需要独立的 SDD 周期 |
| D6 regression | 复用 001-install-scripts 单 feature 的历史 14/14 PASS 不重跑 | hf-release §6 hard gate：fresh-evidence 必须晚于所有候选 feature 最晚 closeout 时间；不允许拼贴历史记录 |
| D6 regression | 跑 HF 仓库的全量测试（如果有的话） | HF 仓库不存在"全量测试"概念；本版 affected modules 仅是 install scripts + 5 个 doc 文件；按 union 决定 release-wide scope 即可 |
| D7 traceability | 重做 001-install-scripts 单 feature traceability | 单 feature traceability 已在 closeout 前完成（Round 2 verdict 通过）；hf-release §7 立场"只做版本级聚合，不重做单 feature traceability" |
| D8 anatomy | install scripts 落 `skills/hf-install/scripts/` 同 ADR-006 D1 约定 | install scripts 是仓库级入口，不属于任何 skill；包装成 hf-install skill 与 D2 立场冲突；落仓库根更符合行业惯例（ECC / Cargo / Bundler 同源） |

## Consequences（影响）

正面：

- **降低集成门槛**：OpenCode / Cursor 用户无需手动 `mkdir + cp -R + ln -s` 三步操作即可 vendor HF；一条命令完成
- **可逆性**：manifest-based uninstall 让用户能干净退出；不会"装了之后想撤都撤不干净"
- **跨 topology 一致性**：3 target × 2 topology = 6 组合统一脚本入口，无需理解 OpenCode 与 Cursor 的目录差异
- **零依赖**：不引入 jq / python / node / npm，可在 macOS bash 3.2 + Linux bash 4/5 直接运行
- **anatomy 不动**：ADR-006 D1 锁定的 4 类子目录约定继续生效；本版只在 D8 明确 install scripts 不在该约定内
- **dogfood 第四次**：v0.4.0 / v0.5.0 / v0.5.1 之后，本版是 hf-release 的第四次自我使用，验证 minor release 流程（前三次：minor / minor / patch）

负面：

- **5 个 ops/release skills 仍未实现**：HF 距离"覆盖完整产品交付链"还有显著差距；用户需要在 hf-finalize 之后自行接 ops 流程
- **4 个客户端仍未支持**：Gemini CLI / Windsurf / GitHub Copilot / Kiro 用户继续被排除在官方支持外
- **install scripts 的 7 项 deferred**：Windows PowerShell / npx wrapper / global 多版本共存等都需等真实需求触发
- **ADR-007 D4 alternative A3 deferred**：cursor rule 路径自动重写未实现，依赖 post-install README 提示作为过渡
- **install scripts 体量上限**：纯 shell 实现对 schema 演进（manifest_version 升级 / 复杂 manifest 操作）不如 Node/Python 灵活；mitigation 通过 manifest_version 字段 + 锁定字段集

中性观察：

- 本 ADR 是 HF 第 4 次走 minor bump（v0.1.0 / v0.2.0 / v0.3.0 / v0.6.0），跳过 v0.6 之前的 v0.4 / v0.5 是因为 v0.4.0 / v0.5.0 / v0.5.1 期间没有 install/vendor 一键化的工程动作；v0.6.0 是该方向的首次集中投入
- v0.5.x → v0.6.0 跨 minor 段而不在 v0.5.x 内继续 patch，是因为 install scripts 是新增能力（minor）而非 bug fix（patch）
- ADR-006 D1 在本版没有被修改，仅 D8 澄清其边界；说明 anatomy v2 立场稳定

## v0.7+ Roadmap（由本版显式延后）

| 条目 | 来源 | 状态 |
|---|---|---|
| `hf-shipping-and-launch` | ADR-001 / ADR-002 / ADR-003 / ADR-004 / ADR-005 / 本 ADR D5 | 继续 deferred；待真实部署场景反馈触发 |
| `hf-ci-cd-and-automation` | 同上 | 继续 deferred |
| `hf-security-hardening` | 同上 | 继续 deferred |
| `hf-performance-gate` | 同上 | 继续 deferred |
| `hf-deprecation-and-migration` | 同上 | 继续 deferred |
| `hf-debugging-and-error-recovery` | 同上 | 继续 deferred |
| Gemini CLI 客户端支持 | ADR-003 / ADR-004 / ADR-005 / 本 ADR D5 | 继续 deferred；待真实使用反馈 |
| Windsurf 客户端支持 | 同上 | 继续 deferred |
| GitHub Copilot 客户端支持 | 同上 | 继续 deferred |
| Kiro 客户端支持 | 同上 | 继续 deferred |
| `hf-staff-reviewer` persona | ADR-002 D11 / 后续 ADR / 本 ADR D5 | 继续 deferred |
| `hf-qa-engineer` persona | 同上 | 继续 deferred |
| `hf-security-auditor` persona | 同上 | 继续 deferred |
| `install.ps1` (Windows PowerShell) | spec-deferred DEF-001 / 本 ADR D5 | 继续 deferred；待 Windows 用户反馈触发 |
| `npx hf-install` Node 包 | spec-deferred DEF-003 / 本 ADR D5 | 继续 deferred |
| Global install 多版本共存 | spec-deferred DEF-004 / 本 ADR D5 | 继续 deferred |
| install 脚本对 `AGENTS.md` merge | spec-deferred DEF-005 / 本 ADR D5 | 永不回收 |
| install 脚本 telemetry | spec-deferred DEF-006 / 本 ADR D5 | 永不回收 |
| install 脚本 audit/lint 集成 | spec-deferred DEF-007 / 本 ADR D5 | 继续 deferred |
| ADR-007 D4 Alt A3 cursor rule 路径自动重写 | ADR-007 D4 / 本 ADR D5 | 继续 deferred |
| writeonce demo evidence trail 重跑 | ADR-005 D7 / 本 ADR D5 | 继续 deferred |

## Implementation 计划（R1–R6）

- **R1（ADR）**：本文件起草并锁定。状态字段 `起草中` → `accepted`（在 §11 Final Confirmation 通过时翻转）。
- **R2（实现）**：`install.sh` / `uninstall.sh` / `tests/test_install_scripts.sh` 已在 features/001-install-scripts/ feature 内完成实现并 workflow-closeout（2026-05-11，commit `141d7b2` + 后续 polish）。本 ADR 不引入新代码改动。
- **R3（元数据 + 顶层文档同步）**：
  - `.claude-plugin/plugin.json` `version`: `0.5.1` → `0.6.0`
  - `.claude-plugin/marketplace.json` 描述追加 v0.6.0 install scripts 说明
  - `SECURITY.md` Supported Versions 表新增 `0.6.x` 行（latest `0.6.0`），原 `0.5.x` 行降级为 best-effort security-only
  - `CONTRIBUTING.md` 引言版本号 `v0.5.1` → `v0.6.0`
  - `.cursor/rules/harness-flow.mdc` Hard rules 段加 v0.6.0 install scripts 说明（保持 ADR-006 + ADR-005 既有行不变）
  - 顶层 `README.md` 与 `README.zh-CN.md` 顶部 Scope Note / 版本号引用同步到 v0.6.0（作为本版 release 时的 release-tier doc 同步，001-install-scripts feature 的 T10b 已经处理了 install 段；本步骤补 Scope Note + 顶部版本号）
  - `docs/claude-code-setup.md` / `docs/cursor-setup.md` / `docs/opencode-setup.md` 顶部 Scope 句子 + 注脚同步到 v0.6.0
- **R4（CHANGELOG）**：CHANGELOG 切到 `[0.6.0]` 段，按 Added / Changed / Decided / Deferred / Notes 5 段写完；`[Unreleased]` 段重置为空模板；版本号链接表加 `[0.6.0]` 行。
- **R5（Release pack）**：`features/release-v0.6.0/release-pack.md` + `verification/release-regression.md` + `verification/release-traceability.md` + `verification/pre-release-checklist.md` 全部落盘。
- **R6（发版）**：tag `v0.6.0`、Release notes 引用本 ADR + 001-install-scripts 的 closeout pack；勾选 pre-release（按 D3）。**本 ADR + hf-release 不自动执行 `git tag` / `git push --tags`**——tag 操作由项目维护者执行（与 ADR-005 D9 / ADR-006 D4 / ADR-004 D7 同向）。

## Notes

- 本 ADR 是 HF 自身第四次 dogfood `hf-release`（v0.4.0 / v0.5.0 / v0.5.1 是前三次）。前三次分别验证了 minor release（首次 hf-release 自检）、minor release（首个其他 skill 主导的版本）、patch release（vendoring fix）。本版验证的是"主线 SDD 完整 6 周次产出 + minor bump"——第一个真正用 SDD 主链产出 + hf-release 收尾的完整版本。
- 本 ADR 与 ADR-005 / ADR-006 的关系：延续（不撤回任何前作 decisions），范围扩展（新增 install scripts 能力 + 新增 ADR-007 + 新增 D8 边界澄清）。
- 本 ADR 与 ADR-007 的关系：ADR-007 是工程层决策（install scripts 5 个核心实现决策），本 ADR 是 release 层决策（把 ADR-007 的产出纳入 v0.6.0 范围 + 标记发版立场）；两 ADR 互不替代。
- 本 ADR 与 `docs/principles/soul.md` 的"窄而硬"立场对齐：本版只承担一条主线（install scripts），不试图同时清理 v0.6+ deferred 项；不替用户拍板降低 release-wide regression 门禁；不自动 git tag。
- forward reference：本 ADR D5 引用的 5 个 ops/release skills + 4 客户端 + 3 personas + DEF-001..DEF-007 全部为 **deferred / 待规划** 状态——明示而非编造其交付承诺。
- 本 ADR 不引入对 hf-release skill 自身的修改；hf-release 依然按 ADR-004 D3 与 router 解耦、不进 transition map、不自动打 tag、不承担 ops。

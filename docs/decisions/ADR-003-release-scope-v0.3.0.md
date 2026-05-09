# ADR-003: HarnessFlow v0.3.0 对外发布范围

- 状态：起草中（2026-05-09 锁定）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 的协作契约执行）
- 关联文档：
  - `docs/decisions/ADR-001-release-scope-v0.1.0.md`（v0.1.0 范围与遗留延后项）
  - `docs/decisions/ADR-002-release-scope-v0.2.0.md`（v0.2.0 范围；含 D11 校准撤回 D2/D3/D4/D8）
  - `docs/principles/soul.md`（soul / 不让步声明）
  - `docs/cursor-setup.md`（v0.3.0 新增）
  - `.cursor/rules/harness-flow.mdc`（v0.3.0 新增）
  - `README.md` / `README.zh-CN.md`（v0.3.0 GA 时同步 Scope Note）
  - `CHANGELOG.md`（v0.3.0 入口与 ADR-003 反向引用）

## 背景

v0.2.0 / v0.2.1 已经作为 pre-release 落地：

- 24 个 SKILL.md（23 `hf-*` + `using-hf-workflow`）+ Claude Code marketplace 入口（v0.2.1 修复了 SSH 默认 + name-collision 两个真实环境 install bug）+ OpenCode `.opencode/skills` 入口。
- v0.2.0 内部新增了 `hf-browser-testing` 一个 verify-stage runtime evidence side node、把 `Common Rationalizations` 从可选升为必需、删除全部 `和其他 Skill 的区别`、上 advisory `audit-skill-anatomy.py`。
- ADR-002 D11（2026-05-07）撤回了 v0.2.0 起草时锁定的 4 项："5 客户端扩展"（D2）/ "真实环境冒烟硬门禁"（D3）/ "3 personas"（D4）/ "persona 命名空间"（D8），理由是"太重 + 不完善"，整体退回到 v0.3+ roadmap。
- ADR-002 D11 退回时在 git 历史里保留了已落地的实现 commit：5 客户端 setup + Gemini commands 在 `18b1d99`、7 客户端 README sync 在 `0c93809`、3 personas 在 `560ac26`，明确"保留方便 v0.3+ cherry-pick"。

v0.3.0 起草时，用户对工作面再做一次显式收窄：

- **只补齐对 Cursor 的安装支持**（5 家延后客户端中**仅取 1 家**），不批量进 4 家。
- **不引入任何新的 `hf-*` skill**（Pillar C 在 v0.3.0 不推进；6 项 ops/release skill 继续 defer）。
- **不引入任何 personas**（ADR-002 D11 撤回的 D4 / D8 在 v0.3.0 继续延后到 v0.4+）。

这是一次 P-Honest 精神的 v0.3.0：与 v0.2.0 D11 撤回 R3/R4/R5 同向，**主动**保持窄而硬的工作面，把 5 家客户端逐家进、把 personas 单独决策、把 ops skill 单独决策。

工作面盘点（grep 实测）：

- 24 / 24 SKILL.md 集合不变。
- `skills/` 目录文件数与 v0.2.1 一致；router profile-node 表无新增节点。
- `.cursor/` 当前只有给 cloud agent 自用的 `skills/{brainstorming,writing-skills}/`，**没有面向最终用户的 HF 集成**——这是 v0.3.0 要补齐的唯一对外承诺面。

本 ADR 一次性锁定 v0.3.0 对外发版的 10 项范围决策。

## 决策

### Decision 1 — Pillar B 第一步：仅引入 1 家新客户端 Cursor

v0.3.0 在 v0.2.x 已支持的 Claude Code + OpenCode 之外，**仅**补齐对 **Cursor** 的安装支持。其余 4 家延后客户端（Gemini CLI / Windsurf / GitHub Copilot / Kiro）继续延后到 v0.4+。

理由：

- Cursor 是用户实际在用的客户端（本 cloud agent 即跑在 Cursor 环境内），有真实使用反馈；先把这一家做对，再把验证经验迁移到下一家，比一次性铺 5 家更符合 ADR-001 D11 / ADR-002 D11 的精神。
- 复用 ADR-002 R3 已经在 commit `18b1d99` 落地、被 D11 撤回的 Cursor 实现（`docs/cursor-setup.md` + `.cursor/rules/harness-flow.mdc`）作为种子，按 v0.3.0 当前承诺面重新校对文案，不重新设计集成机制。
- 客户端面从 2 家 → 3 家是渐进扩张；不会对既有 Claude Code / OpenCode 用户产生破坏性变更。

### Decision 2 — Pillar C 不推进：v0.3.0 不引入任何新 `hf-*` skill

v0.3.0 **不**引入 6 项延后的 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）。skill 集合保持 23 `hf-*` + `using-hf-workflow` 不变。

理由：

- 引入任意 ops/release skill 都涉及对主链终点的重新承诺（见 D4），是比"补一家客户端"大得多的范围决策，不应混入"补客户端"这一次发版。
- 主链终点 `hf-finalize` 改不改、release / ops 段如何切片，留给 v0.4+ 单独 ADR 评估。

### Decision 3 — 不引入 personas

v0.3.0 **不**引入 ADR-002 D4 撤回的 3 个 personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`），**不**引入 ADR-002 D8 撤回的 `agents/` 命名空间约定，**不**新增 `docs/principles/persona-anatomy.md`。

理由：

- ADR-002 D11 把 personas 撤回时给出的理由（"太重 + 不完善"）在 v0.3.0 仍然成立——personas 是与 review skill 边界耦合的设计决策，需要在客户端面成熟（≥ 3 家）后由真实使用反馈驱动，不应早于 D1 的客户端面铺开。
- review 角色继续由各自 `hf-*-review` skill 承担（与 v0.1.0 / v0.2.0 一致）。

### Decision 4 — 主链终点保持 `hf-finalize` 不变

v0.3.0 不改主链 FSM。`hf-finalize` 仍是 engineering-level closeout 的终点；release pipeline / deployment / observability / incident response / security hardening / performance gating / debugging-and-error-recovery / deprecation-and-migration **仍然不是** v0.3.0 的一等阶段。

理由：与 ADR-001 D1 / ADR-002 D1 一致（"P-Honest，窄而硬"）；D2 已显式拒绝在本次发版引入新的 ops/release skill。

### Decision 5 — v0.3.0 仍是 pre-release

v0.3.0 在 GitHub Releases 上仍勾选 **pre-release**。

理由：

- 主链覆盖未达 100%（仍缺 6 项 ops；D2 显式不补）。
- 客户端面只增加 1 家（2 → 3）；不构成 GA 信号。
- 与 ADR-001 D6 / ADR-002 D6 同样的判断：在主链承诺面没有质变之前，版本号不跨 v1.0。

### Decision 6 — Cursor 集成走 rules-based 路径，不注册 Cursor slash 命令

Cursor 集成采用：

1. `.cursor/rules/harness-flow.mdc`（frontmatter `alwaysApply: true`）作为入口规则，每次会话自动加载，告诉 Cursor 优先 load `skills/using-hf-workflow/SKILL.md` → `skills/hf-workflow-router/SKILL.md`。
2. `docs/cursor-setup.md` 描述两条 install 拓扑（A. clone-and-open 本仓库；B. vendor 到自己项目）+ verify + NL intent → router 映射 + troubleshooting + "What is NOT included"。
3. **不**引入 Cursor 专属 slash 命令。Cursor 走与 OpenCode 同样的 NL + router 路径。Claude Code 的 6 条短 slash 命令是 ADR-001 D4 历史决策，本次不向 Cursor 复制。

理由：

- Cursor 的 rules 系统是 alwaysApply 规则注入式的，不是 skill auto-discovery 式的（与 OpenCode 的 `.opencode/skills/` 自动发现机制不同）；rules 形态天然适合作为入口跳板，不需要复制 24 份 SKILL.md。
- ADR-001 D4 的 6 条 slash 命令"每条都是 bias，不是 bypass"语义在 Cursor 上没有 Claude Code 那么强的等价机制；与其在 Cursor 上仿造一套语义模糊的命令，不如让 router 接管所有意图分流（与 OpenCode 一致）。
- 这一选择把 Cursor 集成的代码面压到最小（1 个 rule 文件 + 1 份 setup 文档），与 D2"不引入新 skill"对称。

### Decision 7 — 不增设真实环境 install smoke 硬门禁

v0.3.0 **不**回收 ADR-002 D3（被 D11 撤回的真实环境 install smoke 硬门禁）。GA 验证仍走"维护者按 v0.2.x 同样路径自验"。

理由：

- ADR-002 D11 撤回 D3 的理由（"客户端面只有 2 家时冒烟价值有限"）在 3 家时仅边际性变化；3 家不是 D3 启动的合理触发点。
- v0.2.1 的两个 install bug（marketplace SSH 默认 + name-collision）是 Claude Code 一家的，与 Cursor 集成正交；它们已经在 v0.2.1 修复，并在 docs/claude-code-setup.md 留下了恢复说明。
- 在 cloud agent VM 内端到端测 Cursor install 不可行（无 Cursor binary）；Cursor 路径承担与 v0.1.x stabilization "Known Limitations" 相同的"已知缺口"性质。CONTRIBUTING.md 的 Known Limitations 段同步更新。
- 把"客户端面铺到 ≥ 5 家或出现真实用户冒烟事故"作为 D3 重新评估的触发条件，留给 v0.4+ ADR。

### Decision 8 — SKILL.md anatomy audit 仍是 advisory

`scripts/audit-skill-anatomy.py` 在 v0.3.0 **仍是** advisory check（不阻塞 PR merge），与 ADR-002 D5 子决策一致。

理由：v0.2.0 GA 至今 SKILL.md 集合未变（D2 也不变），24/24 baseline 仍 OK；没有出现漂移信号需要强化。升级为 hard gate 留给 v0.4+ 视实际反馈再决定。

### Decision 9 — `docs/principles/` 其余段落继续保持 "设计参考" 性质

ADR-001 D11 把 `docs/principles/` 整体定位为"设计参考"；ADR-002 D10 仅就 `Common Rationalizations`（必需）+ `和其他 Skill 的区别`（禁止）两节恢复合规基线。v0.3.0 **不**继续推进剩余段落（`Object Contract` / `Methodology` / `Hard Gates` / `Output Contract` / `Red Flags` / `Common Mistakes`）的合规基线化。

理由：与 D2 / D8 同向；本次发版不扩大对 SKILL.md 写作的强制承诺面。

### Decision 10 — 不刷新 `examples/writeonce/` demo evidence trail

v0.3.0 **不**给 `examples/writeonce/` 加 `[Unreleased] — HF v0.3.0 refresh` 段。demo 工件痕迹保持在 v0.2.0 refresh 的状态。

理由：

- ADR-001 D9 立场是"demo 的 deliverable 是 HF 主链工件痕迹，不是产品本身"。v0.3.0 不引入新主链节点（D2）、不改主链 FSM（D4）、不改任何既有 SKILL.md 内容——demo 没有新工件可加。
- v0.2.0 加 SKIP 行是因为 v0.2.0 引入了 `hf-browser-testing` 这个新节点；v0.3.0 没有等价的新节点，强加 refresh 段会是空洞的版本号同步，违反"工件痕迹不是版本号同步"原则。

## Tradeoffs（已考虑的备选 + 拒绝理由）

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| D1 客户端面 | 一次性把 5 家全做（cherry-pick `18b1d99` + `0c93809`） | ADR-002 D11 已经撤回过同一份 R3 工作，理由仍然成立：5 家一次进会让 v0.3.0 重蹈 v0.2.0 R3 覆辙（"太重 + 不完善"）。先做 1 家、由真实使用反馈驱动下一家 |
| D1 客户端面 | 一家都不做，v0.3.0 只做 ops skill | 用户在本轮 ADR 中显式锁定 "补 Cursor"；ops skill 涉及主链终点重新承诺（见 D4），范围比 "补客户端" 大 |
| D2 skill 集合 | 在 v0.3.0 引入 `hf-shipping-and-launch` 把主链终点后移 | 主链终点的重新承诺需要单独 ADR；不应混入"补客户端"这一次 |
| D3 personas | cherry-pick `560ac26` 的 3 personas | 与 D11 撤回理由同向；personas 是与 review skill 边界耦合的设计，应在客户端面成熟（≥ 3 家）后再评估 |
| D6 Cursor slash 命令 | 在 `.cursor/commands/` 下注册 6 条 Cursor 命令对齐 Claude Code | Cursor 没有与 Claude Code `commands` 完全等价的 namespace；NL + router 路径已被 OpenCode 验证可行，复制更小 |
| D6 入口机制 | 复制 24 份 SKILL.md 到 `.cursor/skills/` | Cursor rules 系统不是 skill auto-discovery；只需要 1 个 alwaysApply rule 引入 `using-hf-workflow` + router 即可；24 份复制是冗余 |
| D7 真实环境冒烟 | 把 Cursor install smoke 列为 v0.3.0 GA 硬门禁 | cloud agent VM 内无 Cursor binary，硬门禁无法在 CI 内自动跑；与 v0.2.x "已知缺口" 性质一致 |

## Consequences（影响）

正面：

- 客户端面从 2 家 → 3 家，覆盖用户实际在用的 Cursor 环境，对外发现性提升。
- 工作面规模与 v0.2.1 patch 量级相当（doc + 1 个 rule 文件 + ADR + 元数据同步），review 复杂度可控。
- 复用 ADR-002 R3 已经做过的 Cursor 实现（cherry-pick 思路），不重新设计集成机制；同时按 v0.3.0 当前承诺面校对文案，避免 R3 当时为 7 客户端服务的"对外承诺面太宽"措辞污染 v0.3.0。
- 与 v0.2.0 D11 撤回 R3 的精神一致：少承诺面积优先于堆客户端数量；先做 1 家、由真实使用反馈驱动下一家。

负面：

- 4 家剩余客户端（Gemini CLI / Windsurf / Copilot / Kiro）继续延后，对照 `addyosmani/agent-skills` 仍是 surface gap。
- 6 项 ops skill / 3 personas 继续延后，主链 P-Honest 注解（"代码合并 / 工程 closeout"≠"上线到生产"）继续承担发现性成本。
- Cursor 路径的端到端验证留为 known limitation，与 v0.2.x 沿用一致（首次真实环境冒烟需用户在 Cursor 内跑）。

## v0.4+ Roadmap（由 v0.3.0 显式延后）

| 条目 | 来源 | 状态 |
|---|---|---|
| Gemini CLI setup + 6 commands（含 `/planning` 重命名） | ADR-002 D2（D11 撤回） / ADR-003 D1 | v0.4+ |
| Windsurf setup + `.windsurf/rules.md` | ADR-002 D2（D11 撤回） / ADR-003 D1 | v0.4+ |
| GitHub Copilot setup + `.github/copilot-instructions.md` 块 | ADR-002 D2（D11 撤回） / ADR-003 D1 | v0.4+ |
| Kiro setup + `.kiro/skills` 拓扑 | ADR-002 D2（D11 撤回） / ADR-003 D1 | v0.4+ |
| `hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor` personas | ADR-002 D4 / D8（D11 撤回） / ADR-003 D3 | v0.4+ |
| `docs/principles/persona-anatomy.md` | ADR-002 D8（D11 撤回） / ADR-003 D3 | v0.4+ |
| 真实环境 install smoke 硬门禁 | ADR-002 D3（D11 撤回） / ADR-003 D7 | v0.4+（视客户端面铺开节奏 / 真实事故触发） |
| 6 项剩余 ops/release skill（shipping / ci-cd / security / performance / debugging / deprecation） | ADR-001 D1 + ADR-002 D1 + ADR-003 D2 | v0.4+ |
| `audit-skill-anatomy.py` 升级为 hard gate | ADR-002 D5 子决策 + ADR-003 D8 | v0.4+（视 SKILL.md 漂移率） |
| `docs/principles/` 其余段落升级为合规基线 | ADR-001 D11 + ADR-002 D10 + ADR-003 D9 | v0.4+ |
| `examples/writeonce/` demo 工件痕迹 refresh | ADR-001 D9 + ADR-003 D10 | 与下一次主链节点变更同步触发 |

## Implementation 计划（R1–R6）

- **R1（ADR）**：本文件 `docs/decisions/ADR-003-release-scope-v0.3.0.md` 起草并锁定。**已落地**：本 commit。
- **R2（Cursor 集成实现）**：新增 `.cursor/rules/harness-flow.mdc`（alwaysApply 入口规则）+ `docs/cursor-setup.md`（install / verify / NL intent / troubleshooting / "What is NOT included" / Cross-references）。两份文件按 D6 框架，文案按 v0.3.0 承诺面（3 客户端、4 家延后、6 ops skill 延后、不引入 personas）写作。
- **R3（Scope Notes 同步）**：`README.md` + `README.zh-CN.md` 顶部 Scope Note 升级到 v0.3.0；Installation 段加 Cursor 子段；"Other clients (deferred)" 段从 5 家改为 4 家。`docs/claude-code-setup.md` + `docs/opencode-setup.md` 的 Scope Note + "What is NOT included" 同步——Cursor 从延后列表移除（变成 4 家延后）。
- **R4（元数据同步）**：`.claude-plugin/plugin.json` `version` 0.2.1 → 0.3.0；`.claude-plugin/marketplace.json` plugin description 同步当前承诺面（skill 数 23 不变，但措辞从"Cursor 不在范围"改为"3 客户端"无意义——只更新版本号语境）。`SECURITY.md` Supported Versions 表加 `0.3.x` 行；`CONTRIBUTING.md` 引言版本号 + ADR refs 升级。
- **R5（CHANGELOG）**：CHANGELOG 切到 `[0.3.0]` 段，按 Added / Changed / Removed / Decided / Voided / Deferred / Notes 七段写完；`[Unreleased]` 重置为"（无）"；版本号链接表加 `[0.3.0]`。
- **R6（发版）**：tag `v0.3.0`、GitHub Release 勾 pre-release、Release notes 引用 ADR-003。不附冒烟报告（D7 不增设硬门禁）。

## Notes

- 本 ADR 与 v0.2.1（pre-release patch）的关系：v0.2.1 是 install-blocking bug fix，不改承诺面；v0.3.0 在 v0.2.1 基础上首次扩大承诺面（客户端 2 → 3）。
- D6 选择 rules-based 路径而非 skill-auto-discovery 路径，是基于 Cursor 当前文档的事实判断；如果未来 Cursor 增加原生 skill 自动发现机制，可在 v0.4+ 评估是否切换为 OpenCode 同形式（`.cursor/skills/` 符号链接）；v0.3.0 不预留接口。
- ADR-002 R3 在 git 历史里保留的 Cursor 工作（commit `18b1d99`）是 v0.3.0 Cursor 文案与 rule 内容的种子，但未做 git cherry-pick（因为 R3 commit 同时引入 5 家客户端 + 5 份 setup 文档，cherry-pick 会带入 4 家不需要的工件）；v0.3.0 是手工把 Cursor 部分摘出来、重写文案以匹配 v0.3.0 承诺面（3 客户端、ADR-003 而非 ADR-002 D2）。

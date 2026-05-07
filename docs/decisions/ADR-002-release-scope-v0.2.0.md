# ADR-002: HarnessFlow v0.2.0 对外发布范围

- 状态：起草中（2026-05-06，由用户在 v0.1.0 发版后 surface 的 11 项 release gap 中选取 v0.2.0 范围）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 的协作契约执行）
- 关联文档：
  - `docs/decisions/ADR-001-release-scope-v0.1.0.md`（v0.1.0 范围与遗留延后项）
  - `docs/principles/soul.md`（soul / 不让步声明）
  - `docs/principles/skill-anatomy.md`（v0.2.0 D9 / D10 的写作基线落点）
  - `README.md` / `README.zh-CN.md`（v0.2.0 GA 时同步 Scope Note）
  - `CHANGELOG.md`（v0.2.0 入口与 ADR-002 反向引用）

## 背景

v0.1.0 已作为 pre-release 落地，对外公开了 22 个 `hf-*` skill + `using-hf-workflow`、Claude Code marketplace + OpenCode 两条安装入口、6 个短别名 slash 命令、致谢块、`examples/writeonce/` 全主链 demo、`SECURITY.md` / `CODE_OF_CONDUCT.md` / `CONTRIBUTING.md` / 三件 `.github/` 模板，以及 v0.1.x stabilization 阶段对 OpenCode 安装路径的修复（PR #30）和 `hf-bug-patterns` 的移除（PR #31）。

发版后用户对照基线 `addyosmani/agent-skills` 0.6.0 surface 出 11 项 release gap：

- **Tier 1（release/ops 段）**：7 项 ops/release skill。
- **Tier 2（多平台分发）**：5 个延后客户端的 setup + 命令；真实环境安装冒烟。
- **Tier 3（周边设施）**：Agent personas 层；SKILL.md 自动化质量基线。

用户在本轮 ADR 中**显式收窄 v0.2.0 工作面**，仅锁定 6 项；其余 6 项 Tier 1 skill 留给 v0.3+。

此外用户 surface 出 v0.1.0 阶段未做的两条 SKILL.md 结构修订：

- 移除所有 SKILL.md 的 `和其他 Skill 的区别` 章节（语义吸收回 `When to Use`）。
- 全量补 `Common Rationalizations` 章节（撤回 ADR-001 D11 对 D8 的 supersession，仅就这一条）。
- 上述两条要写入 `docs/principles/skill-anatomy.md`，作为 v0.2.0 起的 SKILL.md 合规基线。

工作面盘点（grep 实测）：

- 23 / 23 SKILL.md 当前存在 `和其他 Skill 的区别` → 全量删除。
- 0 / 23 SKILL.md 存在 `Common Rationalizations` → 全量新增。

本 ADR 一次性锁定 v0.2.0 对外发版的 10 项范围决策，避免在执行阶段反复回头。

## 决策

### Decision 1 — Pillar C 部分推进：仅引入 1 项 ops/release skill（`hf-browser-testing`）

ADR-001 D1 列出的 7 项延后 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery` / `hf-browser-runtime-evidence`），v0.2.0 **只引入 1 项**，命名为 `hf-browser-testing`（取代 ADR-001 D1 中的占位名 `hf-browser-runtime-evidence`，更对齐 AS 的 `browser-testing-with-devtools` 命名习惯，对外更易读）。

其余 6 项仍延后到 v0.3+。

主链终点保持 `hf-finalize` 不变。`hf-browser-testing` **不是新的 release/ship 节点**，而是 verify 阶段的 verification skill（详见 D7）。

理由：

- 与 `soul.md` 「不让步声明」一致——HF 主链不假装"上线"。
- v0.1.0 的 P-Honest 精神在 v0.2.0 仍然成立：少承诺面积优先于堆 skill 数量。
- 浏览器端到端验证是当前 `examples/writeonce/` 之外其它 demo 在 verify 阶段最容易踩空的能力（`hf-test-driven-dev` 默认通过 vitest 拿到 fresh evidence，但 UI 表面无 runtime evidence 是一个具体 gap），值得优先补。

### Decision 2 — 客户端扩展到 7 家：新增 Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro

v0.2.0 把官方支持客户端从 v0.1.0 的 2 家（Claude Code + OpenCode）扩展到 7 家。每个新增客户端交付：

| 客户端 | 交付物 | 备注 |
|---|---|---|
| Cursor | `docs/cursor-setup.md` + `.cursor/rules/` 引用方案 | rule-based，复用 `skills/` 目录 |
| Gemini CLI | `docs/gemini-cli-setup.md` + `.gemini/commands/` × 6（命名避开与 Gemini CLI 内置命令冲突，例如 `/plan` 若冲突则降级为 `/planning`） | `gemini skills install` 路径 |
| Windsurf | `docs/windsurf-setup.md` + Windsurf rules 配置说明 | rules-based |
| GitHub Copilot | `docs/copilot-setup.md` + `.github/copilot-instructions.md` 引用块 | 不引入 `agents/` 作为 Copilot persona（与 D4 解耦） |
| Kiro IDE / CLI | `docs/kiro-setup.md` + `.kiro/skills/` 安装拓扑说明 | 项目级 + 全局两种拓扑 |

每个 setup 文档至少覆盖：1) 安装命令；2) `/skills` 或等效的清单核对；3) 与 OpenCode 一致的"natural-language intent → router → leaf skill"映射表；4) 故障排查。

### Decision 3 — 真实环境安装冒烟作为 v0.2.0 GA 硬门禁

v0.1.0 stabilization 阶段（`CONTRIBUTING.md` Known Limitations）把"Claude Code marketplace 一键安装"和"OpenCode `/skills` 验证"标记为"无法在仓库内完成的剩余项"。v0.2.0 把这两条升级为发版硬门禁：

- **Claude Code**：在真实 Claude Code 环境执行 `/plugin marketplace add hujianbest/harness-flow` + `/plugin install harness-flow@harness-flow`，验证 6 个 slash 命令出现且能 invoke。
- **OpenCode**：在真实 OpenCode 环境执行 clone-and-open 拓扑，运行 `/skills` 验证 22 `hf-*` skill + `using-hf-workflow` + `hf-browser-testing`（共 24 项）全部出现。
- **新增 5 家客户端**：每家至少跑一次 setup 文档中的"recommended first prompt"，确认 `using-hf-workflow` 被实际加载。

冒烟结果记录到 `docs/audits/v0.2.0-install-smoke.md`，作为 GitHub Release 描述的引用证据。

不通过 → 停止 GA，回 R 阶段修复。

### Decision 4 — Agent personas 层（3 个）：作为 review skill 的 orchestration shortcut，不替代

v0.2.0 引入 3 个 user-facing 的 agent persona，命名与 AS 0.6.0 的 3 persona 对齐但加 `hf-` 前缀：

| Persona | 角色定位 | 委派的 review skill |
|---|---|---|
| `hf-staff-reviewer` | Senior Staff Engineer，做整体代码 / 架构 review | `hf-code-review` + `hf-design-review` + `hf-traceability-review` |
| `hf-qa-engineer` | QA Specialist，关注测试策略与覆盖 | `hf-test-review` + `hf-regression-gate`（only as evidence reader, not pull）|
| `hf-security-auditor` | Security Engineer，做威胁建模与安全审计 | 无对应 review skill（v0.2.0 未引入 `hf-security-hardening`），只做 STRIDE-style 风险输出与回写 `hf-design-review` finding；不签发 verdict |

设计原则（**核心**，与 Fagan 角色分离不冲突）：

- **Persona 是用户可见的 orchestration shortcut，不是新的工程权威**。它的唯一职责是：接收用户自然语言意图 → 决定调用哪些已有 `hf-*-review` skill → 把多个 review skill 的 verdict 合并展示。
- **Persona 不替代 review skill 产出 verdict**。所有"通过 / 不通过"的工程判断仍由 `hf-*-review` skill 自己产出，persona 只做 facade。
- **Persona 不调 implementation / authoring skill**，也不能编辑被审对象——保持 Fagan 作者与评审者分离。

### Decision 5 — 重新引入 SKILL.md anatomy audit baseline

撤回 ADR-001 D11 中"audit 脚本不进 v0.1.0"的子条款（仅就脚本本身，不撤回"docs/principles/ 是设计参考"的整体定位——见 D10 的范围澄清）。

v0.2.0 重新引入：

- `scripts/audit-skill-anatomy.py`（PR #20 撤回的脚本的简化版，仅检查结构存在性，不检查内容质量）
- `scripts/test_audit_skill_anatomy.py`（pytest 单测）
- `docs/audits/v0.2.0-skill-anatomy-baseline.md`（首次跑出的 baseline 报告）
- CI 上挂 advisory check（不阻塞 PR merge，仅 surface 偏差）

audit 检查项（最小集合）：

1. frontmatter 是否包含 `name` + `description`，且 `name` 与目录名一致。
2. SKILL.md 是否包含 `## When to Use`、`## Workflow`、`## Verification` 三个必需段。
3. 是否包含 D9 引入的 `## Common Rationalizations`（v0.2.0 起强制）。
4. 是否**不**包含 D9 引入禁止的 `## 和其他 Skill 的区别`（v0.2.0 起禁止）。
5. SKILL.md 主文件是否 < 500 行（与 anatomy.md 第 9 条预算对齐，超额仅 surface 警告）。

不强制（仅 advisory）：`Object Contract`、`Methodology`、`Hard Gates`、`Output Contract`、`Red Flags`、`Common Mistakes`——继续保持 ADR-001 D11 "作者按需写"的状态。

### Decision 6 — 版本号策略：v0.2.0 仍标记为 pre-release

- 启用 SemVer 不变。
- v0.2.0 在 GitHub Release 仍勾选 "Set as a pre-release"，理由：Tier 1 只覆盖 1/7 ops，仍未达到 GA 承诺面（无 security / performance / shipping / debugging / deprecation 等节点）。
- README Scope Note 更新为：「v0.2.0 pre-release。已支持 7 家客户端；主链终点仍是 `hf-finalize`；`hf-browser-testing` 是 verify 阶段的 runtime evidence 节点，不是 ship 节点。」
- `CHANGELOG.md` 增加 `[0.2.0] - pre-release` 段。

### Decision 7 — `hf-browser-testing` 边界澄清：verification skill，不修改主链 FSM

`hf-browser-testing` 在 HF 节点角色表（`docs/principles/skill-anatomy.md` § HF 节点角色）中归为 **Verification Side Node**（与 `hf-experiment` 同列），不是 Authoring / Review / Gate / Finalize 节点。

具体边界：

- **何时触发**：`hf-test-driven-dev` 在 GREEN 后，若 spec 声明了 UI surface 且当前 active task 触碰前端表面，则把 `hf-browser-testing` 列为 fresh evidence 来源之一；否则跳过。
- **产出**：浏览器 runtime evidence bundle（screenshot / console log / network trace），落到 `features/<active>/verification/browser-evidence/<task-id>/`。
- **不做什么**：不发表 verdict、不替代 `hf-test-review` 的测试质量评审、不替代 `hf-regression-gate` 的回归证据汇集、不替代 `hf-completion-gate` 的 DoD 判断。
- **不引入新 slash 命令**：通过 `/hf` 自然语言或 `/build` 中由 `hf-test-driven-dev` 拉取，不增加用户面命令负担（与 ADR-001 D4 一致）。
- **不修改 `hf-workflow-router` FSM 主路径**：仅在 `references/profile-node-and-transition-map.md` 增加一个可选 verify 拐点条目。

### Decision 8 — Persona 命名空间与目录拓扑

- Personas 文件居于仓库根的 `agents/`（与 AS 0.6.0 一致），命名为 `agents/hf-staff-reviewer.md` / `agents/hf-qa-engineer.md` / `agents/hf-security-auditor.md`。
- Persona 文件**不是** SKILL.md，不参与 anatomy audit（D5），使用独立的 persona 写作模板（在 `docs/principles/persona-anatomy.md` 中描述，作为 v0.2.0 新增 design reference）。
- Persona 在 Claude Code 上以 `Task` subagent 形式可用；OpenCode / Cursor / 其它客户端在对应 setup 文档中列出 invocation 方式。
- 与 `hf-*` skill 的命名空间差异：persona 用 `agents/hf-*` 前缀，skill 用 `skills/hf-*/SKILL.md` 前缀，两者不会路径冲突。

### Decision 9 — SKILL.md 强制结构变更：移除「和其他 Skill 的区别」，新增「Common Rationalizations」

v0.2.0 对全部 23 份 SKILL.md（22 `hf-*` + `using-hf-workflow`）+ Tier 1 新增的 `hf-browser-testing` SKILL.md（共 24 份）执行强制结构变更：

**变更 1 — 移除 `## 和其他 Skill 的区别` 章节**：

- 该章节当前在所有 23 份 SKILL.md 中都以"场景 → 用本 skill / 否则 reroute"的表格形式出现，与 `When to Use` 中的「适用 / 不适用 / reroute」语义重复。
- v0.2.0 起：该章节**禁止**出现在 SKILL.md 中。等价的 reroute 信息**必须**已经在 `When to Use` 段落里写清。
- 迁移策略：执行删除前，逐份检查 `When to Use` 是否已覆盖原表格中的 reroute 条目；缺失则补到 `When to Use` 再删原章节。

**变更 2 — 新增 `## Common Rationalizations` 章节**：

- 0/23 SKILL.md 当前存在该章节。v0.2.0 起：该章节为 SKILL.md **必需段**（在 audit script 中作为 hard rule）。
- 章节内容形式：

```markdown
## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "<skill 域内最常见的偷懒理由 1>" | <对应反驳，引用本 skill 的 Hard Gates / Verification 条目> |
| "<理由 2>" | <反驳> |
| ... | ... |
```

- 至少 3 条、至多 8 条。每条**必须**引用本 skill 已有的 Hard Gates / Workflow stop rule / Verification 条款，不能凭空编造新 rule。
- 推荐位置：`Red Flags` 后、`Verification` 前；如有 `Common Mistakes`，则放在 `Common Mistakes` 之后。

**ADR-001 D8 状态更新**：

- ADR-001 D11 撤回 D8 的 supersession 仅在 v0.1.0 阶段有效。
- v0.2.0 起：D8 重新激活，全量 SKILL.md 必须有 `Common Rationalizations`。
- 由 D9 的"v0.2.0 起强制"取代 D8 原文中的"v0.1.0 必须全量补"——**强制时点延后到 v0.2.0**，但强制范围一致。

### Decision 10 — 把 D9 写入 `docs/principles/skill-anatomy.md`，部分撤回 ADR-001 D11

ADR-001 D11 锁定的两条与本决策冲突：

1. "`docs/principles/` 是设计参考，不作 SKILL.md 合规基线"
2. "维持现有 SKILL.md 现状，不做内容编辑"

v0.2.0 阶段**部分撤回 D11**，范围限定如下：

- **仅 `skill-anatomy.md` 中关于以下两节的合规级别恢复为强制基线**：
  - `## Common Rationalizations` —— 从"默认不建议扩散的章节"移到"主文件骨架的必需段"。
  - `## 和其他 Skill 的区别` —— 从"按需但强烈建议"移到"禁止"，并显式说明等价信息应在 `When to Use` 中。
- **其它 anatomy 段落（`Object Contract` / `Methodology` / `Hard Gates` / `Output Contract` 等）继续保持 D11 的"按需写"**，不在 v0.2.0 升级。
- **`soul.md` 仍是宪法层不变**，本 ADR 不触碰 soul。

`skill-anatomy.md` 具体修订点（在 v0.2.0 实现阶段落地）：

1. § 主文件骨架表格中 `## Common Rationalizations` 行从"默认不建议扩散"改为"必需"。
2. § 主文件骨架表格中新增 `## 和其他 Skill 的区别` 行，标"禁止；语义吸收进 `When to Use`"。
3. § Canonical skeleton 模板中：删除 `## 和其他 Skill 的区别` 占位（如有），增加 `## Common Rationalizations` 占位。
4. § 检查清单：增加两条——"是否包含 `Common Rationalizations`"、"是否**不**包含 `和其他 Skill 的区别`"。
5. 文件头部 § 定位中追加一句：「本文件中关于 `Common Rationalizations`（必需）与 `和其他 Skill 的区别`（禁止）的两条规则，从 v0.2.0 起作为 SKILL.md 合规基线由 `scripts/audit-skill-anatomy.py` 强制；其余段落继续保持设计参考性质（ADR-002 D5 / D10）。」

## 被考虑的备选方案

| 决策 | 否决方案 | 否决理由 |
|---|---|---|
| D1 Pillar C | v0.2.0 直接补 7 项 ops/release skill | 工作量过大；与 v0.1.0 的 P-Honest 精神冲突；缺一线证据时无法保证 release skill 的成熟度 |
| D1 Pillar C | v0.2.0 不引入任何 ops skill，主链止步与 v0.1.0 一致 | 浏览器端 runtime evidence 是其它 demo 在 verify 阶段的真实空缺，跨过它会让 v0.2.0 成为"只是把客户端铺开"的版本，叙事单薄 |
| D1 命名 | 沿用 ADR-001 D1 中的 `hf-browser-runtime-evidence` | 名字过长且偏内部黑话；用户反馈倾向于对齐 AS 的 `browser-testing` 命名习惯，更易被外部读者识别 |
| D2 客户端 | 仅扩 Cursor + Gemini CLI 2 家 | 与 AS 0.6.0 的客户端覆盖差距太大；多平台分发是 v0.2.0 的核心叙事 |
| D2 命令 | Gemini CLI 命令直接复用 `/plan` | Gemini CLI 内部已有同名命令冲突（参考 AS 0.6.0 用 `/planning` 的 workaround）；保留 fallback 命名空间 |
| D3 冒烟 | 把冒烟列为发版后的 follow-up，不作硬门禁 | 与 v0.1.0 stabilization 留下的"无法在仓库内完成"问题同病；v0.2.0 必须在这条路径上前进 |
| D4 Personas | persona 直接调 implementation skill | 违反 Fagan 角色分离；persona 一旦能写代码就会演化为"另一个工程权威"，与 soul 冲突 |
| D4 Personas | 不引入 personas，把 review skill 直接对外暴露 | 对外发现性弱；"我想要一个 staff reviewer"是 AS 已经验证过的高频用户意图 |
| D5 audit | 强制 audit 作为 PR merge gate | 与 ADR-001 D11 "docs 是设计参考"的根契约冲突过强；先以 advisory 落地，待 v0.3+ 视实际反馈再升级 |
| D5 audit | 完全不引入 audit | 一旦扩到 7 家客户端 + 多人贡献，SKILL.md 漂移风险显著上升；advisory baseline 是最小可行成本 |
| D6 版本 | 直接 v1.0.0 | 与 v0.1.0 同样的理由：主链覆盖未达 100%（仍缺 6 项 ops），承诺"v1"会与 soul 冲突 |
| D6 版本 | v0.2.0 标记为正式版 | 同上，过度承诺 |
| D7 边界 | `hf-browser-testing` 引入新 slash 命令 `/browse` 或类似 | 用户面命令负担上升；与 ADR-001 D4 "命令是 bias 不是 bypass" 冲突 |
| D7 边界 | `hf-browser-testing` 自带 verdict 能力 | 会与 `hf-test-review` / `hf-regression-gate` 在 verdict 上重叠；保持单一证据源 |
| D8 Persona 路径 | personas 居于 `skills/agents/` | 与 SKILL.md 命名空间混淆，audit script 容易误判 |
| D9 章节 | 仅删 `和其他 Skill 的区别` 不补 `Common Rationalizations` | 删完之后 SKILL.md 对 agent 偷懒的内部防御变弱；两件事必须配对完成 |
| D9 章节 | 仅补 `Common Rationalizations` 不删 `和其他 Skill 的区别` | 后者与 `When to Use` 长期重复；保留下去对未来作者形成"该写哪一节"的反复决策成本 |
| D10 范围 | 全量撤回 D11，把整个 anatomy.md 升为合规基线 | 与"R1 完结"的根决定冲突；其它段落（OC / Methodology 等）的工作量再次失控 |
| D10 范围 | 不写入 anatomy.md，仅改 SKILL.md | audit script 没有可引用的"标准源"；将来作者无依据，质量基线很快漂回 |

## 后果

正面：

- 客户端覆盖从 2 家扩到 7 家，对外可用性接近 AS 0.6.0。
- `hf-browser-testing` 补齐 verify 阶段的 runtime evidence 空缺，主链 evidence 链路更完整。
- Personas 把"我想要一个 staff reviewer / qa engineer"的高频意图变成可调用入口，不破坏 Fagan 角色分离。
- 真实环境冒烟门禁让 v0.2.0 GA 的安装承诺真正可验证。
- D9 / D10 把 SKILL.md 长期漂移风险（重复段、缺防御段）一次性收紧。
- audit advisory baseline 让多客户端 + 多贡献者场景下的 SKILL.md 质量有自动提示。

负面：

- v0.2.0 工作面比 v0.1.0 大一个量级（24 份 SKILL.md 内容编辑 + 5 家客户端 setup + Tier 1 新 skill + 3 个 personas + 1 套 audit），单维护者节奏挑战大。
- D10 部分撤回 D11，必须仔细范围限定，否则会被误读为"docs 全面恢复合规基线"，引发 OC / Methodology 等其它段的连带争议。
- Persona 层是新引入的对外承诺面，未来若 review skill 能力升级，persona 的 facade 也要同步升级。
- 真实环境冒烟在仓库内不可完成，仍依赖外部环境（Claude Code / OpenCode / 5 家新客户端）实测。

中性：

- 仍维持 SemVer pre-release，没有把 v0.2.0 包装成 GA。
- `hf-finalize` 仍是主链终点，不假装"上线"。

## 可逆性评估

| 决策 | 可逆性 |
|---|---|
| D1 Pillar C 部分推进（hf-browser-testing） | 容易（v0.3 可继续补 6 项；也可只保持单 skill 状态） |
| D2 客户端扩展到 7 家 | 容易（每家 setup 文档独立，可单独回滚） |
| D3 冒烟硬门禁 | 容易（GA 标准是 ADR 条目，可在 v0.3 复议） |
| D4 Agent personas | 中等（persona 加入对外承诺面后，删除会破坏外部用户已建立的调用习惯） |
| D5 audit baseline | 容易（脚本独立，可降级或移除） |
| D6 版本号 | 容易（SemVer 自然演进） |
| D7 hf-browser-testing 边界 | 容易（边界改动只触及单个 skill 的 SKILL.md） |
| D8 Persona 命名空间 | 中等（变路径会破坏外部引用） |
| D9 SKILL.md 强制结构变更 | **难**（新作者养成习惯后再改回去会再次引发 24 份编辑成本） |
| D10 部分撤回 D11 + 写入 anatomy.md | 中等（anatomy.md 内 5 处修订可独立回滚；但 SKILL.md 已落地的修改是 D9 的可逆性问题） |

## 仍需用户拍板的子项（HF 不替你定）

按 `soul.md` 「方向 / 取舍 / 标准的最终权在用户」，下列 sub-decision **不在本 ADR 锁定**，由后续主链节点中拍板：

1. **D2 子项**：5 家新客户端中是否每家都需要 6 个 slash 命令的对等映射，还是部分客户端（例如 GitHub Copilot 没有原生 slash 概念）只交付 setup 文档而不交付命令文件——具体由 `hf-product-discovery` → `hf-specify` 阶段在 setup 文档对应 spec 中拍板。
2. **D4 子项**：3 个 persona 的具体角色范围（`hf-staff-reviewer` 是否要加入 ADR review、`hf-qa-engineer` 是否要把 `hf-traceability-review` 拉进委派范围、`hf-security-auditor` 在 v0.2.0 缺 `hf-security-hardening` 的情况下是否仍引入）——具体由 persona 的 spec 阶段拍板。
3. **D9 子项**：每个 SKILL.md 中 `Common Rationalizations` 的具体借口条目（一条 hard rule 是"必须引用本 skill 已有的 Hard Gates / Workflow stop rule / Verification 条款"，但具体借口选取由作者按 skill 域知识写）。
4. **D5 子项**：audit script 在 CI 上的失败行为（advisory annotation vs PR merge block），首发选 advisory，是否升级为 block 由 v0.2.0 GA 后视实际漂移率决定，本 ADR 不锁。

## 下一步

本 ADR 接受后，按以下顺序推进 v0.2.0 实现阶段（每一步进入主链由 `using-hf-workflow` / `hf-workflow-router` 接管，不由本 ADR 直接驱动）：

- **R0（基线落地）**：更新 `docs/principles/skill-anatomy.md`（D10），新增 `scripts/audit-skill-anatomy.py`（D5），新增 `docs/principles/persona-anatomy.md`（D8）。
- **R1（SKILL.md 全量结构修订）**：23 份现有 SKILL.md 执行 D9 变更（删 `和其他 Skill 的区别` + 补 `Common Rationalizations`）；audit script 跑过。
- **R2（Tier 1）**：新增 `hf-browser-testing/SKILL.md` + `references/` + `evals/`（按 D9 / D10 新基线写作）；接入 `hf-test-driven-dev` 与 `hf-workflow-router` 的拐点。
- **R3（Tier 2 客户端扩展）**：5 家新客户端 setup 文档 + 命令文件；READMEs 同步 7 家客户端清单；Scope Note 更新到 v0.2.0 措辞。
- **R4（Tier 3 personas）**：3 个 persona 文件 + persona-anatomy.md 完善 + README 引入 personas 章节。
- **R5（冒烟）**：在真实 Claude Code / OpenCode / 5 家新客户端环境跑 D3 冒烟，结果落到 `docs/audits/v0.2.0-install-smoke.md`。
- **R6（发版）**：CHANGELOG 切到 `[0.2.0]`、tag `v0.2.0`、GitHub Release 勾选 pre-release、Release notes 引用 ADR-002 + 冒烟报告。

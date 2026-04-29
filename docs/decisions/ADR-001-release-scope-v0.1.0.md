# ADR-001: HarnessFlow v0.1.0 对外发布范围

- 状态：已接受（2026-04-28，第二轮 review 关闭 D4/D9a；2026-04-29 增补 D10 Q1=B；2026-04-29 D11 校准撤回 D8 + 作废 D10 + 澄清 docs 定位）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 的协作契约执行）
- 关联文档：
  - `docs/principles/soul.md`（soul / 不让步声明）
  - `README.md` / `README.zh-CN.md`
  - 后续将由 `hf-product-discovery` → `hf-specify` 落地的 release feature spec

## 背景

HF 当前已具备 23 个 `hf-*` skill、宪法层文档（soul / skill-anatomy / skill-node-define / sdd-artifact-layout / coding-principles）、以及 `hf-product-discovery → hf-finalize` 的完整工程主链。

但作为一个**对外发布的 skill pack**，相对参照基线 `addyosmani/agent-skills` 仍存在以下 gap：

- 无 marketplace / 一键安装入口；无 slash command；无 plugin manifest
- 部分 SKILL.md 缺少 anti-rationalization 表（针对 agent 偷懒的 SKILL 内防御）
- 主链终点 `hf-finalize` 之后的 release / ops 段在 soul.md 已显式承认未覆盖
- 缺 LICENSE / CHANGELOG / SemVer 标签 / 中英 README 等深审校
- 缺一个真实可跑的 quickstart demo

本 ADR 一次性锁定 v0.1.0 对外发版的 8 项范围决策，避免在执行阶段再反复回头。

## 决策

### Decision 1 — Pillar C 路径：P-Honest（窄而硬）

v0.1.0 **不**新增 release / ops 类 skill（不补 `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-debugging-and-error-recovery` / `hf-browser-runtime-evidence`）。

主链终点保持 `hf-finalize`。在 README 顶部以一段**显眼的 Scope Note** 承认未覆盖范围，并把这些条目挂到未来 v0.2 / v0.3 的 roadmap 中。

理由：
- 与 `soul.md` 「不让步声明」一致——HF 不能悄悄把"工程级 closeout"伪装成"上线"
- 优先把已有 23 个 skill 做成"对外可承诺"的硬质量，而不是为发版赶工增加低成熟度节点
- 与"质量优先于进度"的硬纪律一致

### Decision 2 — License：MIT

仓库根添加 `LICENSE` 文件（MIT），作者署名以 `git config user.name` 为准。

### Decision 3 — 首发目标平台：Claude Code + OpenCode（**仅这两家**）

v0.1.0 仅做 Claude Code 与 OpenCode 的 setup 路径与发行入口；其它平台（Cursor / Gemini CLI / Windsurf / Copilot / Kiro）**显式延后到 v0.2+**，README 也要明确写出"v0.1.0 仅支持 Claude Code 与 OpenCode"，避免误导。

具体交付：
- `.claude-plugin/marketplace.json` + plugin manifest（Claude Code marketplace 注册）
- OpenCode 集成入口（PR #21 已删除 `skills/templates/AGENTS.md.example`，并将 skill 改为 self-contained，不再依赖 AGENTS.md sidecar；R2 阶段需重新评估 OpenCode 的 setup 路径——可能完全不需要 AGENTS.md 正本，仅需 `docs/opencode-setup.md` 引用 `skills/` 目录即可）
- `docs/claude-code-setup.md`
- `docs/opencode-setup.md`

### Decision 4 — Slash 命令命名空间与清单：使用更短别名（v0.1.0 锁定 6 条）

最终清单（架构师 2026-04-28 第二轮 review 锁定）：

| Slash | 别名映射到 | 触发的入口 / leaf | 备注 |
|---|---|---|---|
| `/hf` | route-first（默认） | `using-hf-workflow` → `hf-workflow-router` | 不确定就用它 |
| `/spec` | spec 起草 / 修订 | `hf-specify` | bias，不替代 router |
| `/plan` | **设计 + 任务拆解（合并）** | router 按工件证据派发到 `hf-design`（含 UI 时并行 `hf-ui-design`）或 `hf-tasks` | 合并理由见下 |
| `/build` | 实现当前活跃任务 | `hf-test-driven-dev` | 仅唯一活跃任务时生效 |
| `/review` | 评审请求 | router 按上下文派发到具体 `hf-*-review` | 含 spec / design / ui / tasks / test / code / traceability / discovery review |
| `/ship` | closeout / finalize | `hf-completion-gate` → `hf-finalize` | 由 gate 决定能否真的进入 finalize |

被砍掉的命令（架构师决定）：

- `/hotfix`：低频，且与"用自然语言描述线上问题 → router 自动分流到 `hf-hotfix`"重复。砍掉不影响主链能力，仅影响显式触发便利度。
- `/gate`：regression / completion gate 不应**主动**被用户触发，应由前序节点的 canonical next action 自动推进；显式 `/gate` 反而鼓励"跳过实现/评审直接撞门禁"的反模式。

`/plan` 合并 `/design` + `/tasks` 的理由：

- 在 HF 主链中，design 与 tasks 是同一 planning 阶段的两个连续节点（设计完才能拆任务）；用户视角上"我要做规划"是同一个意图，分两条命令反而需要用户判断"现在该用哪条"，违反"命令是 bias，工件状态决定下一步"。
- router 已具备按工件证据判断"当前在 design 还是 tasks"的能力（`hf-workflow-router/references/profile-node-and-transition-map.md`），合并后路由准确性不降。
- 与 D1（P-Honest，窄而硬）一致：少一条命令也少一份对外承诺面积。

跨 pack 命名冲突风险：`/spec` `/plan` `/build` `/review` `/ship` 是通用名，未来若与 OpenCode / Claude Code 其他 plugin 冲突，回退到 `/hf-*` 全前缀（可逆）。

### Decision 5 — 仓库归属与名称：保持 `hujianbest/harness-flow`，不预占包名

不迁移到独立 org，不预占 npm / PyPI / Marketplace 同名包。所有外部链接（README、setup 文档、marketplace.json）使用 `hujianbest/harness-flow`。

### Decision 6 — 版本号策略：直接 `v0.1.0`，走预发布通道

- 启用 SemVer
- v0.1.0 标记为 **pre-release**（GitHub Release "Set as a pre-release" 勾选）
- README 顶部 Scope Note 中明确写出"本版本为预发布"
- `CHANGELOG.md` 从 v0.1.0 开始

### Decision 7 — 方法论致谢块：在 README 顶层补全

在 README 顶部新增 `## Acknowledgements / 致谢` 一节，**显式列出**：

- forrestchang/andrej-karpathy-skills（已在现 README 中点名，挪到顶层致谢块）
- Software Engineering at Google + Google engineering-practices guide
- Eric Evans — Domain-Driven Design
- Vaughn Vernon — Implementing DDD（tactical patterns 主要来源）
- Alberto Brandolini — Event Storming
- Kent Beck — Test-Driven Development、Two Hats
- Martin Fowler — Refactoring、Patterns of Enterprise Application Architecture、Front Controller
- Robert C. Martin — Clean Architecture、SOLID
- Michael Fagan — Fagan Inspection
- Simon Brown — C4 Model
- Gernot Starke — ARC42
- ISO/IEC 25010 — Quality Attribute model
- Microsoft — STRIDE Threat Modeling
- Jakob Nielsen — Heuristic Evaluation
- W3C WAI — WCAG 2.2
- PMI — PMBOK（closeout / handoff 思路）
- Tony Ulwick / Clayton Christensen — Jobs-to-be-Done
- Teresa Torres — Opportunity Solution Tree

每条仅给"出处 + 在 HF 的哪个 skill 落地"两行，不展开。

### Decision 8 — anti-rationalization（**Superseded by Decision 11，2026-04-29**）

> **状态：作废，由 D11 取代**。原文保留作为决策追溯：
>
> 每个 SKILL.md 增加一节 `## Common Rationalizations`，结构：
>
> ```markdown
> | 借口 | 反驳 / Hard rule |
> |---|---|
> | "我先写实现，回头补测试" | Canon TDD：RED 必须先存在；跳过则任务作废重启 |
> | ... | ... |
> ```
>
> 原理由："HF 的"评审节点分离"是节点间防御；anti-rationalization 表是节点内防御。两者互补，不冲突。"
>
> 撤回原因：见 D11。简言之：(1) "应该补"被错误地扩大成"v0.1.0 必须全量补"，违反 D1 P-Honest「窄而硬，少承诺面积」精神；(2) 整改 24 个 SKILL.md 是大体量的内容编辑，超出 v0.1.0 critical path 范围。`docs/principles/skill-anatomy.md` 的相应修订也将一并回滚（参见 D11 实施细则）。

### Decision 9 — Quickstart Demo Feature：个人写作多平台发布应用（"WriteOnce"）

v0.1.0 quickstart 选用 **"个人写作多平台发布应用"** 作为 end-to-end 示例，工程代号暂定 `writeonce`。

> ⚠ **未关闭子项**：HF 仅锁定"主题方向"，但**目标平台清单 / MVP 范围 / 技术栈**应当由 `hf-product-discovery` → `hf-specify` 走标准主链产出，不在本 ADR 拍板（避免 HF 在产品方向上越权）。本 ADR 仅约束："这一轮 demo 必须把 HF 主链 `hf-product-discovery → hf-discovery-review → hf-specify → hf-spec-review → hf-design (|| hf-ui-design) → hf-design-review (|| hf-ui-review) → hf-tasks → hf-tasks-review → hf-test-driven-dev → hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-doc-freshness-gate → hf-completion-gate → hf-finalize` 完整跑一遍并留下可回读的 commit + 工件 + 截图"，这是 quickstart 的真正 deliverable。

demo 仓库归属：**`examples/writeonce/`**（架构师 2026-04-28 第二轮 review 锁定）。

理由：单仓库便于演示"安装 → 运行 → 主链"完整链路；demo 工件本身（spec / design / tasks / reviews / verification / closeout-pack）就是 HF 主链跑过的"活样本"，与 skill pack 同仓库便于交叉引用。

### Decision 10 — Object Contract 强制级别（**Voided by Decision 11，2026-04-29**）

> **状态：作废，由 D11 取代**。原文保留作为决策追溯：
>
> R1 step 1 anatomy 审计（PR #20）发现 `## Object Contract` 在 24/24 workflow skill 中全部缺失，且 `skill-anatomy.md` 把它列为 workflow skill **必备段**。架构师 2026-04-29 选 **B（暂时降级）**：
>
> - v0.1.0：`Object Contract` 为 **推荐**（recommended），缺位仅作 P2 提示，不阻塞 v0.1.0 发版。
> - v0.2.0：升为 **必需**（mandatory），与 `Methodology` 并列成为 workflow skill hard rule。
>
> 撤回原因：见 D11。该决策建立在"`docs/principles/skill-anatomy.md` 是合规基线"的前提上；架构师在 2026-04-29 后续校准中明确 `docs/` 下的文档**只是设计参考，不强制执行**。前提作废，"标准强制级别"概念随之失去意义——OC 既不必须、也无需被"放宽"。`skill-anatomy.md` 中相应的 v0.1.0/v0.2.0 表格修订将一并回滚。

### Decision 11 — docs/principles 定位澄清 + 撤回 D8/D10（2026-04-29 锁定）

#### 校准触发

- D8 把"应该补"扩大为"v0.1.0 必须全量补 24 个 SKILL.md"，与 D1 P-Honest 自相矛盾。
- D10 (Q1=B) 是为了对齐"`skill-anatomy.md` 把 `Object Contract` 列为必需"这一前提，但架构师明确该文档是**设计参考**，不是合规基线。
- 上述两条均属 HF 越权立标准（违反 `soul.md` 「立标准是用户的职责」）。

#### 决策

1. **`docs/principles/` 定位说明**：该目录下的所有文档（`soul.md` 除外）均属**设计参考**，不作 v0.1.0 发版门禁、不作 SKILL.md 合规基线、不作 audit 脚本的强制规则源。`soul.md` 仍是宪法层（仅就「方向 / 取舍 / 标准的最终权 + 用户是架构师 / HF 是工程团队」这一层契约保持硬约束）。
2. **撤回 D8**：v0.1.0 不再要求全量补 `Common Rationalizations`。是否在 v0.2.0 或更晚补，待发版后视实际反馈再定，不在本 ADR 锁定。
3. **作废 D10**：Object Contract 在 v0.1.0 既不强制也不"推荐"，回到"作者按需写"的状态。
4. **R1 阶段就此宣告完结**：R1 原本的目的（"质量基线硬化"）建立在"docs 是合规基线"前提上，前提作废后 R1 不再扩散到任何 SKILL.md 内容编辑；保留产物仅限 ADR-001 本身。
5. **维持现有 23 个 `hf-*` SKILL.md + `using-hf-workflow` 现状**，发版后再视实际反馈渐进改进。

#### 实施细则（落到 PR #19 与 PR #20）

- **PR #19（本 ADR）**：D8 标 Superseded by D11；D10 标 Voided by D11；本 D11 追加；ADR 头部状态行追加 D11 时间戳。
- **PR #20（anatomy audit）**：**关闭**（不合并）。
  - `scripts/audit-skill-anatomy.py` 与 `scripts/test_audit_skill_anatomy.py` 不进 v0.1.0；audit 报告 `docs/audits/` 不进 v0.1.0。
  - PR #20 之前对 `docs/principles/skill-anatomy.md` 的修订（CR 升「推荐」、OC 标 v0.1.0 推荐 / v0.2.0 必需、canonical skeleton 加 CR、checklist 增项）需要回滚到 PR #21 合入后的状态。
  - `.gitignore` 中 PR #20 添加的 `__pycache__/` `*.pyc` 两条，由于无副作用且对未来可能再写 Python 脚本仍有用，**保留**（不属 docs 修订，仅是仓库通用 housekeeping）。

#### 后果

正面：
- v0.1.0 critical path 真正聚焦"对外可承诺面"：LICENSE / 平台 setup / slash 命令 / Quickstart / README Scope Note / 致谢 / CHANGELOG / pre-release tag
- 不再把 24 个 SKILL.md 拖入发版工作面
- HF 不再越权把"参考文档"伪装成"合规基线"，与 soul 一致

负面：
- 之前已投入的 anatomy audit 工作（脚本 + 测试 + baseline 报告）对 v0.1.0 不产生交付价值
- 没有自动化机制保证 SKILL.md 长期质量基线（接受这一缺口；属"发版后再视实际反馈"决定的范围）

中性：
- `docs/principles/skill-anatomy.md` 等仍是"作者参考"，可继续被新作者阅读，只是不再被脚本或门禁机械化引用

#### 可逆性

高。任意时点可重新决策"把 anatomy 升为合规基线 + 重新引入 audit 脚本"。

## 被考虑的备选方案

| 决策 | 否决方案 | 否决理由 |
|---|---|---|
| Pillar C | P-Wide（吸收 AS 的 release/ops skill） | 短期内 release 段成熟度不足，强行补会违反"质量优先于进度" |
| 平台 | 5 平台一起首发 | 工作量过大；首发风险集中；与 P-Honest 的"窄而硬"精神冲突 |
| 版本 | 直接 v1.0.0 给"对外可承诺接口" | 主链覆盖未达 100%（release/ops 缺位），承诺"v1"会与 soul 冲突 |
| Slash | 全用 `/hf-*` 全前缀 | 长前缀降低使用频率；用户已倾向"更短别名" |
| Slash | 保留 `/design` `/tasks` 拆分两条命令 | 二者属同一 planning 阶段；命令应是 bias，工件状态决定下一步；分两条徒增用户判断 |
| Slash | 保留 `/hotfix` `/gate` | `/hotfix` 与自然语言+router 分流重复；`/gate` 鼓励跳过实现/评审直接撞门禁的反模式 |
| anti-rationalization | 不补，依赖评审节点分离 | 节点间防御无法覆盖 leaf skill 内部跳步；AS 已证明这是简单且高价值的防御 |
| demo 归属 | 独立仓库 | quickstart 演示"安装 → 跑通"应在同一 clone 内可达；demo 工件即"活样本"与 skill pack 交叉引用密集 |
| Object Contract | A 严格执行（v0.1.0 前 24 SKILL.md 全量补） | 工作量大、改动 contract、与 P-Honest 冲突 |
| Object Contract | C 核心 7 节点 | 需先列 7 节点清单；标准与 SKILL.md 之间长期不一致 |

## 后果

正面：
- 发版范围明确、可承诺；不夸大覆盖
- 与 soul "诚实抛回" 原则一致
- 工作量可控，避免"为发版而堆 skill"
- ~~anti-rationalization 与评审节点形成双层防御~~（D11 已撤回 D8）
- 致谢块明确归属，降低发版后的方法论引用纠纷风险

负面：
- 首发功能面比 AS 窄（无 perf / security / shipping 类 skill）
- 仅 Claude Code + OpenCode 两家平台，Cursor 用户首发即缺位（注：现仓库本身在 Cursor 中可用，但**不在 v0.1.0 的"已支持平台"承诺范围**）
- ~~23 个 SKILL.md 全量补 anti-rationalization 是一次大批量编辑，存在质量参差风险~~（D11 已撤回 D8；维持现有 SKILL.md 现状，无 SKILL.md 内容编辑）
- 没有自动化 SKILL.md 质量基线（D11 让 R1 完结，audit 脚本不进 v0.1.0；接受这一缺口，发版后视实际反馈再定）

中性：
- 仓库归属保持现状，不引入 org 迁移成本，但也未为长期治理做组织层准备
- 不预占包名，意味着未来若需要发 npm/PyPI 包，可能面临命名占用风险

## 可逆性评估

| 决策 | 可逆性 |
|---|---|
| 1 P-Honest | 容易回滚（v0.2 可改 P-Wide） |
| 2 License MIT | 难回滚（MIT 不可单方面收回，仅可对未来版本变更） |
| 3 平台仅 Claude+OpenCode | 容易扩展 |
| 4 Slash 别名 | 容易调整（命令文件即配置） |
| 5 仓库归属 | 中等成本（迁移可做） |
| 6 v0.1.0 pre-release | 容易（SemVer 自然演进） |
| 7 致谢块 | 容易增删 |
| 8 anti-rationalization | **Superseded by D11** |
| 9 demo 主题 | 中等（已投入的 demo 工件需重做） |
| 10 Object Contract 强制级别 | **Voided by D11** |
| 11 docs 定位 + R1 完结 | 高（任意时点可重新引入 audit 与合规化） |

## 仍需用户拍板的子项（HF 不替你定）

按 `soul.md` 「方向 / 取舍 / 标准的最终权在用户」，下列 sub-decision **不在本 ADR 锁定**，由后续主链节点中拍板：

1. **Decision 9 子项 b**：demo (`writeonce`) 的产品范围（目标平台清单 / MVP 边界 / 技术栈）将由 `hf-product-discovery → hf-discovery-review → hf-specify` 阶段产出，需要在 discovery 评审与 spec 评审两个 approval gate 上由用户拍板。本 ADR 不在此处替用户预设产品方向。

> 历史 surfaced 项已关闭：
> - D4 命令清单（2026-04-28 第二轮锁定为 6 条 + 砍 2 条 + 合并 design/tasks 为 /plan）
> - D9a demo 归属（2026-04-28 第二轮锁定为 `examples/writeonce/`）
> - D10 Q1 Object Contract 强制级别（2026-04-29 锁定为 B；同日由 D11 作废）
> - D11 校准（2026-04-29 锁定：撤回 D8、作废 D10、澄清 docs 定位、R1 完结）

## 下一步

本 ADR 接受后，按 R2 → R3 顺序推进（R1 由 D11 标记为完结，无后续 SKILL.md 编辑）：

- ~~R1（质量基线）~~：D11 已宣告完结。维持现有 23 个 `hf-*` SKILL.md + `using-hf-workflow` 现状，发版后视实际反馈渐进改进。
- R2（发行入口）：MIT LICENSE + Claude Code marketplace + OpenCode setup（PR #21 后无需 AGENTS.md sidecar）+ setup 文档 + slash 命令文件 × 6
- R3（对外叙事）：README 顶部 Scope Note + 致谢块 + Quickstart demo（writeonce，主链跑通）+ 中英 README 等深 + CHANGELOG + tag v0.1.0 pre-release

每一阶段进入主链时由 `using-hf-workflow` / `hf-workflow-router` 接管，不再由本 ADR 直接驱动实现。

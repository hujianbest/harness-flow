# ADR-001: HarnessFlow v0.1.0 对外发布范围

- 状态：已接受（2026-04-28，第二轮 review 关闭 D4/D9a 子项）
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

### Decision 8 — anti-rationalization：补到所有 23 个 `hf-*` SKILL.md

每个 SKILL.md 增加一节 `## Common Rationalizations`，结构：

```markdown
| 借口 | 反驳 / Hard rule |
|---|---|
| "我先写实现，回头补测试" | Canon TDD：RED 必须先存在；跳过则任务作废重启 |
| ... | ... |
```

理由：HF 的"评审节点分离"是节点间防御；anti-rationalization 表是节点内防御。两者互补，不冲突。

需要在 `docs/principles/skill-anatomy.md` 的"主文件骨架"表中把 `Common Rationalizations` 从"默认不建议扩散"改为"workflow skill 推荐"，以保持 anatomy 一致。（PR #21 合入后路径已从 `02 skill-anatomy.md` 重命名为 `skill-anatomy.md`，本条要求不变。）

### Decision 9 — Quickstart Demo Feature：个人写作多平台发布应用（"WriteOnce"）

v0.1.0 quickstart 选用 **"个人写作多平台发布应用"** 作为 end-to-end 示例，工程代号暂定 `writeonce`。

> ⚠ **未关闭子项**：HF 仅锁定"主题方向"，但**目标平台清单 / MVP 范围 / 技术栈**应当由 `hf-product-discovery` → `hf-specify` 走标准主链产出，不在本 ADR 拍板（避免 HF 在产品方向上越权）。本 ADR 仅约束："这一轮 demo 必须把 HF 主链 `hf-product-discovery → hf-discovery-review → hf-specify → hf-spec-review → hf-design (|| hf-ui-design) → hf-design-review (|| hf-ui-review) → hf-tasks → hf-tasks-review → hf-test-driven-dev → hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-doc-freshness-gate → hf-completion-gate → hf-finalize` 完整跑一遍并留下可回读的 commit + 工件 + 截图"，这是 quickstart 的真正 deliverable。

demo 仓库归属：**`examples/writeonce/`**（架构师 2026-04-28 第二轮 review 锁定）。

理由：单仓库便于演示"安装 → 运行 → 主链"完整链路；demo 工件本身（spec / design / tasks / reviews / verification / closeout-pack）就是 HF 主链跑过的"活样本"，与 skill pack 同仓库便于交叉引用。

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

## 后果

正面：
- 发版范围明确、可承诺；不夸大覆盖
- 与 soul "诚实抛回" 原则一致
- 工作量可控，避免"为发版而堆 skill"
- anti-rationalization 与评审节点形成双层防御
- 致谢块明确归属，降低发版后的方法论引用纠纷风险

负面：
- 首发功能面比 AS 窄（无 perf / security / shipping 类 skill）
- 仅 Claude Code + OpenCode 两家平台，Cursor 用户首发即缺位（注：现仓库本身在 Cursor 中可用，但**不在 v0.1.0 的"已支持平台"承诺范围**）
- 23 个 SKILL.md 全量补 anti-rationalization 是一次大批量编辑，存在质量参差风险——需通过 R1 阶段的 anatomy 审计 + evals 把关

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
| 8 anti-rationalization | 容易（删除节即可回滚） |
| 9 demo 主题 | 中等（已投入的 demo 工件需重做） |

## 仍需用户拍板的子项（HF 不替你定）

按 `soul.md` 「方向 / 取舍 / 标准的最终权在用户」，下列 sub-decision **不在本 ADR 锁定**，由后续主链节点中拍板：

1. **Decision 9 子项 b**：demo (`writeonce`) 的产品范围（目标平台清单 / MVP 边界 / 技术栈）将由 `hf-product-discovery → hf-discovery-review → hf-specify` 阶段产出，需要在 discovery 评审与 spec 评审两个 approval gate 上由用户拍板。本 ADR 不在此处替用户预设产品方向。

> 历史 surfaced 项已关闭：D4 命令清单（2026-04-28 第二轮锁定为 6 条 + 砍 2 条 + 合并 design/tasks 为 /plan）；D9a demo 归属（2026-04-28 第二轮锁定为 `examples/writeonce/`）。

## 下一步

本 ADR 接受后，按 R1 → R2 → R3 顺序推进（见 README 后续 roadmap 节）：

- R1（质量基线）：anatomy 审计 + token 预算 + evals 覆盖度 + anti-rationalization 全量补 + CI
- R2（发行入口）：MIT LICENSE + Claude Code marketplace + OpenCode setup（PR #21 后无需 AGENTS.md sidecar）+ setup 文档 + slash 命令文件
- R3（对外叙事）：README 顶部 Scope Note + 致谢块 + Quickstart demo（writeonce）+ 中英 README 等深 + CHANGELOG + tag v0.1.0 pre-release

每一阶段进入主链时由 `using-hf-workflow` / `hf-workflow-router` 接管，不再由本 ADR 直接驱动实现。

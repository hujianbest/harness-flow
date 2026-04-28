# ADR-001: HarnessFlow v0.1.0 对外发布范围

- 状态：已接受（2026-04-28）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/00 soul.md` 的协作契约执行）
- 关联文档：
  - `docs/principles/00 soul.md`（soul / 不让步声明）
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
- 与 `00 soul.md` 「不让步声明」一致——HF 不能悄悄把"工程级 closeout"伪装成"上线"
- 优先把已有 23 个 skill 做成"对外可承诺"的硬质量，而不是为发版赶工增加低成熟度节点
- 与"质量优先于进度"的硬纪律一致

### Decision 2 — License：MIT

仓库根添加 `LICENSE` 文件（MIT），作者署名以 `git config user.name` 为准。

### Decision 3 — 首发目标平台：Claude Code + OpenCode（**仅这两家**）

v0.1.0 仅做 Claude Code 与 OpenCode 的 setup 路径与发行入口；其它平台（Cursor / Gemini CLI / Windsurf / Copilot / Kiro）**显式延后到 v0.2+**，README 也要明确写出"v0.1.0 仅支持 Claude Code 与 OpenCode"，避免误导。

具体交付：
- `.claude-plugin/marketplace.json` + plugin manifest（Claude Code marketplace 注册）
- `AGENTS.md`（OpenCode 的 agent-driven skill 执行入口；本仓库已使用 `AGENTS.md.example` 模板，需要发布版正本）
- `docs/claude-code-setup.md`
- `docs/opencode-setup.md`

### Decision 4 — Slash 命令命名空间与清单：使用更短别名 `/hf-*` 系列

> ⚠ **未关闭子项**：用户已确定使用"更短别名"原则，但未列出具体命令清单。HF 给出**最小可发布提案**（见下表），由用户在 PR review 时确认或调整。HF 不擅自定。

提议命令清单（v0.1.0 最小集，复用 `using-hf-workflow/SKILL.md` 已声明的 entry bias）：

| Slash | 别名映射到 | 触发的入口 / leaf |
|---|---|---|
| `/hf` | route-first | `using-hf-workflow` → `hf-workflow-router`（默认入口） |
| `/spec` | spec 起草 / 修订 | `hf-specify` |
| `/design` | design 起草 / 修订 | `hf-design`（含 UI 时并行 `hf-ui-design`） |
| `/tasks` | 任务拆解 | `hf-tasks` |
| `/build` | 实现当前活跃任务 | `hf-test-driven-dev` |
| `/review` | 评审请求（按上下文路由到具体 review skill） | `hf-*-review` 任一 |
| `/gate` | 进入 regression / completion gate | `hf-regression-gate` 或 `hf-completion-gate` |
| `/ship` | closeout / finalize | `hf-completion-gate` → `hf-finalize` |
| `/hotfix` | 线上缺陷修复支线 | `hf-hotfix` |

注：`/spec` `/design` `/tasks` `/build` `/review` `/gate` `/ship` `/hotfix` 是**通用名**，跨 pack 可能与其他工具冲突——这是"更短别名"的固有 trade-off。如果发现冲突，回退到 `/hf-*` 全前缀。

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

需要在 `docs/principles/02 skill-anatomy.md` 的"主文件骨架"表中把 `Common Rationalizations` 从"默认不建议扩散"改为"workflow skill 推荐"，以保持 anatomy 一致。

### Decision 9 — Quickstart Demo Feature：个人写作多平台发布应用（"WriteOnce"）

v0.1.0 quickstart 选用 **"个人写作多平台发布应用"** 作为 end-to-end 示例，工程代号暂定 `writeonce`。

> ⚠ **未关闭子项**：HF 仅锁定"主题方向"，但**目标平台清单 / MVP 范围 / 技术栈**应当由 `hf-product-discovery` → `hf-specify` 走标准主链产出，不在本 ADR 拍板（避免 HF 在产品方向上越权）。本 ADR 仅约束："这一轮 demo 必须把 HF 主链 `hf-product-discovery → hf-discovery-review → hf-specify → hf-spec-review → hf-design (|| hf-ui-design) → hf-design-review (|| hf-ui-review) → hf-tasks → hf-tasks-review → hf-test-driven-dev → hf-test-review → hf-code-review → hf-traceability-review → hf-regression-gate → hf-doc-freshness-gate → hf-completion-gate → hf-finalize` 完整跑一遍并留下可回读的 commit + 工件 + 截图"，这是 quickstart 的真正 deliverable。

demo 仓库归属：**需用户拍板** —— 单独仓库 vs 本仓库 `examples/writeonce/`。HF 推荐 `examples/writeonce/`（单仓库便于演示"安装 → 运行 → 主链"完整链路），等用户确认。

## 被考虑的备选方案

| 决策 | 否决方案 | 否决理由 |
|---|---|---|
| Pillar C | P-Wide（吸收 AS 的 release/ops skill） | 短期内 release 段成熟度不足，强行补会违反"质量优先于进度" |
| 平台 | 5 平台一起首发 | 工作量过大；首发风险集中；与 P-Honest 的"窄而硬"精神冲突 |
| 版本 | 直接 v1.0.0 给"对外可承诺接口" | 主链覆盖未达 100%（release/ops 缺位），承诺"v1"会与 soul 冲突 |
| Slash | 全用 `/hf-*` 全前缀 | 长前缀降低使用频率；用户已倾向"更短别名" |
| anti-rationalization | 不补，依赖评审节点分离 | 节点间防御无法覆盖 leaf skill 内部跳步；AS 已证明这是简单且高价值的防御 |

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

按 `00 soul.md` 「方向 / 取舍 / 标准的最终权在用户」，下列 sub-decision **不在本 ADR 锁定**，由用户在本 PR review 或后续主链节点中拍板：

1. **Decision 4 子项**：slash 命令清单是否就用本 ADR 表中的 9 条？是否要删 `/hotfix` `/gate` 这种低频命令？
2. **Decision 9 子项 a**：demo 仓库归属——`examples/writeonce/` vs 独立仓库？
3. **Decision 9 子项 b**：demo 的产品范围（目标平台清单 / MVP 边界 / 技术栈）将由 `hf-product-discovery` 阶段产出，但需要你在那里再拍板一次。

## 下一步

本 ADR 接受后，按 R1 → R2 → R3 顺序推进（见 README 后续 roadmap 节）：

- R1（质量基线）：anatomy 审计 + token 预算 + evals 覆盖度 + anti-rationalization 全量补 + CI
- R2（发行入口）：MIT LICENSE + Claude Code marketplace + OpenCode AGENTS.md + setup 文档 + slash 命令文件
- R3（对外叙事）：README 顶部 Scope Note + 致谢块 + Quickstart demo（writeonce）+ 中英 README 等深 + CHANGELOG + tag v0.1.0 pre-release

每一阶段进入主链时由 `using-hf-workflow` / `hf-workflow-router` 接管，不再由本 ADR 直接驱动实现。

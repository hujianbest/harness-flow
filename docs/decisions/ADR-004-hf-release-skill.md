# ADR-004: HarnessFlow v0.4.0 引入 `hf-release` 独立 skill

- 状态：起草中（2026-05-09 锁定）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 协作契约执行）
- 关联文档：
  - `docs/decisions/ADR-001-release-scope-v0.1.0.md`（Pillar C "P-Honest，窄而硬" 立场）
  - `docs/decisions/ADR-002-release-scope-v0.2.0.md`（D11 校准 / 撤回 R3/R4/R5 立场延续到 v0.3.0）
  - `docs/decisions/ADR-003-release-scope-v0.3.0.md`（D2 显式延后 6 项 ops/release skill；D4 主链终点保持 `hf-finalize`；D6 Cursor 走 NL + router）
  - `docs/principles/soul.md`（soul / 不让步声明 / 主链终点为工程级 closeout）
  - `docs/principles/skill-anatomy.md`（v0.2.0 起 `Common Rationalizations` 必需 + `和其他 Skill 的区别` 禁止的合规基线）
  - `skills/hf-finalize/SKILL.md`（feature/workflow 级 closeout，与本 ADR 引入的 release-tier closeout 不重叠）
  - `skills/using-hf-workflow/SKILL.md`（entry shell；本 ADR 在其 entry bias 表加 1 行）

## 背景

v0.3.0（ADR-003）在"窄而硬"立场下做了一次**单客户端扩张**（Cursor，2 → 3 家），但：

- ADR-003 D2 显式声明 v0.3.0 **不引入任何新 `hf-*` skill**，把 6 项 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）整体延后到 v0.4+。
- ADR-003 D4 进一步声明主链终点保持 `hf-finalize` 不变。

v0.3.0 GA 后的真实使用反馈出现一类典型缺口（2026-05-09 用户原话）：

> 经过多轮迭代开发后，正式发布一个 release 版本，需要对全部功能做一次测试，并撰写相关发布文档。

把这句话拆成 4 个工程动作：

1. 跨多个已 closed 的 feature/iteration **锁定 vX.Y.Z 范围**
2. 对**整个版本**而非单 feature 做一次 full regression
3. 撰写**版本级**发布文档（CHANGELOG / release notes / migration / known limitations）
4. 真正部署 / staged rollout / 监控 / 回滚

`hf-finalize` 当前只覆盖单 feature 的 `task-closeout` / `workflow-closeout`；`hf-regression-gate` 是 impact-based 单 feature 回归；①②③ 是 v0.3.0 skill 集合**无法覆盖**的版本级动作。④ 仍由 v0.4+ planned `hf-shipping-and-launch` 承担，与本 ADR 不重叠。

`addyosmani/agent-skills` 的 `shipping-and-launch` skill 也**不能**覆盖 ①②③——它针对的是 trunk-based / 持续部署 / 单 feature staged rollout 节奏，假设"deploy ≠ release"，没有"多 feature 汇总成 SemVer 版本号 + full regression + 发布文档聚合"语义。HF 自身的 SemVer 节奏（pre-release / minor / patch；ADR-001/002/003 自身就是 release scope ADR 实践）需要本 ADR 显式建模成一等节点。

本 ADR 一次性锁定 v0.4.0 引入 `hf-release` 这一独立 skill 的 9 项决策。

## 决策

### Decision 1 — 引入 `hf-release` 独立 skill（解耦于 router）

v0.4.0 在 v0.3.0 的 23 `hf-*` + `using-hf-workflow` 集合上**新增 1 个** skill：`skills/hf-release/`。skill 集合规模变为 **24 `hf-*` + `using-hf-workflow`**。

`hf-release` 的核心职责：把多个已 `workflow-closeout` 的 feature 汇总成一次 vX.Y.Z 工程级发版（**engineer-level release**）的一等节点——锁范围、做版本级回归、聚合发布文档、产出 tag-ready pack。

理由：

- ① 多 feature → 版本号 ② full regression ③ release docs 聚合 是当前 skill 集合无法覆盖的真实工程缺口。
- 用 ADR-001/002/003 形式手工做 release scope ADR 是 HF 自身实践（pack-internal）；把它沉淀成给所有 HF 用户的 skill 是自然延伸。
- 与 ADR-001 D1 / ADR-002 D1 / ADR-003 D2 "P-Honest，窄而硬" 立场**仍然兼容**——本 ADR 严格停在"工程级 release"，不承诺部署 / 监控 / 回滚（见 D2）。

### Decision 2 — `hf-release` 不替代 `hf-shipping-and-launch`，二者正交

`hf-release` 处理"版本切片"（多 feature → vX.Y.Z 范围 + 全量回归 + 发布文档）；`hf-shipping-and-launch`（v0.4+ planned，**当前尚未实现**）处理"上线时刻"（feature flag lifecycle / staged rollout / 监控 / 回滚）。

明确边界：

- `hf-release` **不做**：feature flag 策略、staged rollout（0% → 5% → 100%）、监控仪表盘、错误上报、回滚 procedure、SLO、health check、CDN / DNS / SSL 配置、上线后观察窗口。
- `hf-shipping-and-launch`（仍 deferred）**不做**：跨 feature 范围决策、SemVer 切片、release notes 聚合、ADR 状态批量翻转、release-wide regression。

理由：

- 两者解决的工程问题不同（版本切片 vs 上线时刻），合并成一个 skill 会违反 `docs/principles/skill-anatomy.md` "一个 skill 一个 concern" 立场，且让用户看到大量与自己场景无关的 ops checklist。
- 当前用户场景（"对全部功能做一次测试 + 撰写发布文档"）**不**触发 `hf-shipping-and-launch` 的任何核心面；不应让用户走"上线 skill"来切版本号。
- `hf-shipping-and-launch` 涉及主链终点的重新承诺（部署 = 上线，HF 主链终点会从 `hf-finalize` 后移到 ship 节点），是比"补 release-tier skill"大得多的范围决策；继续延后到独立 ADR 评估。

### Decision 3 — `hf-release` 完全解耦于 `hf-workflow-router`

`hf-release` 是**独立工具型 skill**，不进入 `hf-workflow-router` 的 profile-node-and-transition-map，不修改主链 FSM，不与 `hf-finalize` / `hf-regression-gate` / `hf-doc-freshness-gate` 互引。

这意味着：

- `skills/hf-workflow-router/references/profile-node-and-transition-map.md` **不改**。
- `skills/hf-finalize/SKILL.md` **不改**（不引入"release-closeout"第 3 分支）。
- `skills/hf-regression-gate/SKILL.md` **不改**（不新增 `release-wide-scope.md` 子协议）。
- `skills/hf-doc-freshness-gate/SKILL.md` **不改**（不新增 `tier: release` 模式）。
- 上述能力**协议内联**到 `hf-release/SKILL.md` + `hf-release/references/`，由 `hf-release` 自给自足读盘 / 判断 entry vs recovery / 做版本级回归 / docs sync，不依赖 router 派发。

触发方式：

- **Claude Code**：新增 `.claude/commands/release.md` 注册 `/release [version]` slash 命令，body 直接 instruct agent 加载 `skills/hf-release/SKILL.md`。
- **OpenCode / Cursor**：不注册 slash 命令文件（与 ADR-003 D6 立场一致）；通过 NL 触发，由 `using-hf-workflow` entry shell 在 entry bias 表识别"切版本/出 release/打 tag"意图后 **direct invoke** `hf-release`，**不 route-first**，不进 router transition map。

理由：

- "解耦"是用户在 v0.4.0 立项时的显式架构决策（避免把 release-tier 节点塞进单 feature 主链 FSM，破坏 router profile 复杂度）。
- 与 `hf-experiment` / `hf-hotfix` / `hf-increment` 这些"分支/支线"节点相比，`hf-release` 比它们更独立——前者仍参与 router transition map（虽然是 conditional insertion），后者完全不进。
- 把 release-wide regression / docs sync 协议内联到 `hf-release` 自身而非引用 `hf-regression-gate` / `hf-doc-freshness-gate`，是为了让 `hf-release` 作为独立工具 skill 可以被任何项目按需启用，不依赖主链其他节点已落盘。
- 入口层 `using-hf-workflow` entry bias 表加 1 行（"切版本意图 → direct invoke `hf-release`"）是非 Claude Code 用户的最低对接面；entry shell 是分类器层，不是 runtime FSM——这一行不破坏解耦立场。

### Decision 4 — 新增 1 条 slash 命令 `/release`

Claude Code 现有 6 条 slash 命令（ADR-001 D4 锁定：`/hf` / `/spec` / `/plan` / `/build` / `/review` / `/ship`）变为 **7 条**：新增 `/release [version]`。

命令体（`.claude/commands/release.md`）的语义：

- direct invoke `skills/hf-release/SKILL.md`，**不**先经 `using-hf-workflow` → `hf-workflow-router`（与 `/spec` / `/plan` / `/build` / `/review` / `/ship` 的"router-first"语义不同）。
- "command is bias, not authority" 立场保留：用户传入的 `[version]` 是 hint，`hf-release` 自己仍要按 SKILL.md 内 SemVer 决策 + 候选 feature 盘点结果校验。

不在 OpenCode 注册 slash 命令文件（沿用 ADR-001 D3 + ADR-003 D6 "OpenCode 走 NL + agent-driven skill 工具加载"）。
不在 Cursor 注册 slash 命令文件（沿用 ADR-003 D6 "Cursor 走与 OpenCode 一致的 NL + router 模型"，不仿造 Claude Code 6 条短 slash 命令）。

理由：

- `/release` 与 `/ship` 语义不同：`/ship` 是 `hf-completion-gate` → `hf-finalize`（单 feature workflow closeout），`/release` 是 `hf-release` 独立 skill（多 feature 版本切片）。两条命令并存而不冲突。
- 命令名选 `/release` 而非 `/hf-release` 或 `/cut-release`：与既有 6 条短别名风格一致（动词 / 单词），且 `/ship` 在 v0.1.0 已占用"closeout"语义，无歧义碰撞。

### Decision 5 — `hf-release` 是 standalone skill，不依赖任何上游 skill 已运行

`hf-release` 的入口前置条件**只**依赖磁盘工件（候选 feature 的 `closeout.md`），不依赖 `hf-finalize` 在同一 session 内运行过、不依赖 `hf-completion-gate` / `hf-regression-gate` 在同一 session 内运行过。

具体表现为：

- `hf-release` 自己的 Hard Gates 检查"候选 feature 是否都是 `workflow-closeout` 状态"——读 `features/<feature-id>/closeout.md` 的 `Closeout Type` 字段。
- `hf-release` 自己内联 release-wide regression 协议（read fresh evidence; union(各 feature affected modules); profile-aware rigor），不引用 `hf-regression-gate` skill。
- `hf-release` 自己内联 sync-on-presence 协议（CHANGELOG 必出 / `docs/release-notes/vX.Y.Z.md` 按存在 / ADR 状态批量翻转 / 顶层导航更新），不引用 `hf-doc-freshness-gate` skill。
- 长期资产 sync 范围沿用 `hf-finalize` 第 4 步的"按存在同步"判断（架构概述 / runbooks / SLO / 等），仅扩展为 release-tier scope。

理由：

- "standalone + not coupled to router" 是 D3 的延伸：要让 `hf-release` 真正可被任何项目按需启用，它不能要求"必须先跑过哪几个 skill"；它只能要求"磁盘上必须有这些工件"。
- 这种 standalone 设计与 `hf-finalize` 的"读 gate 记录后做 closeout"模式同形，但作用域更宽（read closeout records → 做 release closeout）。

### Decision 6 — release-tier 工件目录用 `features/release-vX.Y.Z/`

`hf-release` 产出的工件统一落到 `features/release-vX.Y.Z/`，与 `features/<feature-id>/` 平级：

```
features/
  001-walking-skeleton/
    closeout.md
    ...
  002-some-feature/
    closeout.md
    ...
  release-v0.4.0/                          # ← hf-release 工件
    release-pack.md                        # 类似 closeout.md 的 release-tier 主工件
    scope-decision.md                      # 反向引用 ADR-NNN-release-scope-vX.Y.Z.md
    progress.md                            # 复用 feature progress schema
    verification/
      release-regression.md
      release-traceability.md
      pre-release-checklist.md
```

理由：

- 与 router 既有 `features/<active>/` 路径假设兼容（即使 router 不识别 `release-vX.Y.Z`，也不会把它当成误激活的 feature——router 只在用户/skill 显式声明 `Current Active Task` 时才扫 features 目录）。
- 备选 B（`releases/vX.Y.Z/` 顶级目录）会引入新顶级目录，扩大工作面承诺；备选 C（散落到 `docs/release-notes/` + `docs/decisions/`）会把过程性工件混进 `docs/`，与 sync-on-presence 边界不清。
- `release-pack.md` 与 `closeout.md` 的字段是同源 schema 的 release-tier 扩展，便于读者跨工件理解。

### Decision 7 — `hf-release` 内置 SemVer + pre-release 默认策略，但允许项目覆盖

`hf-release/SKILL.md` 默认采用 [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)；pre-release 标记策略默认沿用 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 "主链未达 100% 时勾选 pre-release" 的判断。

项目可在自家 guidelines / `CONTRIBUTING.md` / 宿主工具链配置中显式声明替代版本策略（CalVer / 项目自定义）；`hf-release` 应优先遵循项目级约定，否则退回默认。

理由：

- 不内置默认会让用户每次 `/release` 都要先回答一遍"用什么版本策略"，体验差。
- 默认值与 HF 自身实践对齐（v0.1.0 → v0.3.0 全部按 SemVer + pre-release 标记），用户读 ADR-001/002/003 即可理解默认行为。
- 项目级约定优先是 `docs/principles/skill-anatomy.md` 既定立场（路径写法要可迁移；项目工件路径优先遵循项目权威约定）。

### Decision 8 — v0.4.0 仍是 pre-release

v0.4.0 在 GitHub Releases 上仍勾选 **pre-release**。

理由：

- 主链覆盖未达 100%：原 6 项延后 ops/release skill（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）**全部**继续延后到 v0.5+。v0.4.0 引入的 `hf-release` 是**新 skill**（不在原 6 项延后清单中），覆盖工程级版本切片这一切面，与 `hf-shipping-and-launch` 正交；不构成"ops 全面落地"信号。
- 客户端面无变化（仍是 Claude Code + OpenCode + Cursor 3 家；剩余 4 家 Gemini CLI / Windsurf / GitHub Copilot / Kiro 继续延后）。
- 与 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 同样的判断：在主链承诺面没有质变之前，版本号不跨 v1.0。

### Decision 9 — 不刷新 `examples/writeonce/` demo evidence trail

v0.4.0 **不**给 `examples/writeonce/` 加 `[Unreleased] — HF v0.4.0 refresh` 段。

理由：

- ADR-003 D10 立场是"工件痕迹不是版本号同步"——demo 只在引入新主链节点时刷 evidence。
- `hf-release` 是 standalone 工具型 skill，**不进主链**（D3）；writeonce demo 走的是 `hf-product-discovery → hf-finalize` 主链工件痕迹，没有自然的 `hf-release` 演示位。
- 强加 refresh 段会变成空洞的版本号同步，违反 ADR-001 D9 "demo 的 deliverable 是 HF 主链工件痕迹" 立场。

未来若用户需要 release-tier 演示，可在 v0.4+ 后续 ADR 单独决策（例如把 writeonce 的 v1.0.0 切片当作 release demo 一次性补全）。

## Tradeoffs（已考虑的备选 + 拒绝理由）

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| D1 引入 skill | 不引入新 skill，把 release ADR 模板挂到 `hf-finalize/references/` | 模板路径解决文档问题，但解决不了 release-wide regression / 候选 feature 盘点 / SemVer 决策 / Tag readiness 这些动作；用户场景仍然落空 |
| D1 引入 skill | 用现有 `hf-finalize` 增加 `release-closeout` 第 3 分支 | 违反 ADR-003 D2 / D4（主链终点保持 `hf-finalize`），且会把 release-tier 责任面膨胀到 finalize 内，破坏 finalize 的"单 feature closeout"语义清晰度 |
| D2 与 shipping-and-launch 关系 | 把二者合并成一个 skill | 解决的工程问题不同（版本切片 vs 上线时刻），合并违反一个 skill 一个 concern；用户当前场景不触发任何 shipping-and-launch 核心面 |
| D3 解耦立场 | 让 `hf-release` 进 router transition map（与 `hf-experiment` 同形 conditional insertion） | router profile 复杂度上升；release-tier 节点不与单 feature workflow 共享触发条件，硬塞进 transition map 会让 router 长期带一段几乎不命中的分支 |
| D3 标准化协议 | 在 `hf-regression-gate` / `hf-doc-freshness-gate` 加 release-tier 子协议供 `hf-release` 引用 | 跨 skill 调用会让 `hf-release` 必须依赖那两个 skill 在同一 session 加载过；与 standalone 立场冲突 |
| D4 命令名 | `/hf-release` 或 `/cut-release` | 与既有 6 条短别名风格不一致；`/release` 与 `/ship` 语义清晰区分（版本切片 vs closeout） |
| D4 命令铺面 | 同时给 OpenCode / Cursor 注册 slash 命令文件 | 违反 ADR-001 D3 + ADR-003 D6（OpenCode / Cursor 走 NL + agent-driven 路径，不复制 Claude Code 短命令模式） |
| D6 工件目录 | `releases/vX.Y.Z/` 顶级目录 | 引入新顶级目录扩大工作面承诺；与 ADR-003 D2 "工作面规模可控" 立场冲突 |
| D6 工件目录 | `docs/releases/vX.Y.Z/` | 把过程性工件（regression record / progress / pack）混进 `docs/`；docs/ 是稳定参考资产载体，不应承担过程性工件 |
| D7 SemVer 默认 | 不内置默认，每次都问用户 | 用户体验差；默认值与 HF 自身实践对齐，项目可显式覆盖即可 |
| D8 pre-release 标记 | v0.4.0 直接 GA | 主链未达 100%；客户端面未质变；与 v0.1.0/v0.2.0/v0.3.0 同向，版本号不跨 v1.0 |
| D9 demo 刷新 | 给 writeonce 加 v0.4.0 release-tier demo | 与 ADR-003 D10 "工件痕迹不是版本号同步" 同向；writeonce demo 不走 release-tier，强加是空洞同步 |

## Consequences（影响）

正面：

- 用户的真实工程缺口（多 feature → 版本切片 + 全量回归 + 发布文档）得到一等节点支撑，不再需要手工拼接 `hf-finalize` + 多次 `hf-regression-gate` + 人脑维护 release ADR。
- HF 自身做了 v0.1.0 → v0.3.0 三轮的 release scope ADR 实践得到沉淀，复用为模板供所有 HF 用户使用。
- 解耦设计（D3）让 `hf-release` 可被任何项目按需启用，不需要主链其他节点已落盘——这与 HF "skill 是可复用技术参考" 立场一致。
- 与 `hf-shipping-and-launch` 边界清晰（D2），让 v0.4+ 后续 ADR 评估"上线"侧时不被 release-tier 范围混淆。
- 工作面规模可控：1 个新 skill + 1 条新命令 + 1 行 entry bias + 文档/元数据同步，与 v0.3.0 patch 量级相当（不改任何既有 SKILL.md 内容、不改 router transition map、不改主链 FSM）。

负面：

- skill 集合从 23 → 24，README / setup docs / marketplace description 中的 skill 数引用需要逐处同步。
- `using-hf-workflow` entry bias 表加 1 行是首次为 standalone 工具型 skill 在 entry shell 开"direct invoke"通道（既有 6 行均与 router-first 有关）；后续若引入更多 standalone skill（如 v0.4+ 的 `hf-shipping-and-launch`），entry shell 复杂度会同向增长。
- v0.4.0 仍是 pre-release（D8）—— `hf-release` 上线后，HF 自身的下一次发版可以用 `hf-release` 走通自举（dogfooding），但首次启用仍需手工对照 ADR-001/002/003 模板做。
- `hf-shipping-and-launch` 继续延后（D2 + ADR-003 D2），主链 P-Honest 注解（"代码合并 / 工程 closeout" ≠ "上线到生产"）继续承担发现性成本。

## v0.4+ Roadmap（由 v0.4.0 显式延后）

| 条目 | 来源 | 状态 |
|---|---|---|
| `hf-shipping-and-launch`（部署 / staged rollout / 监控 / 回滚） | ADR-001 D1 + ADR-002 D1 + ADR-003 D2 + ADR-004 D2 | v0.5+ |
| `hf-ci-cd-and-automation`（pipeline / shift-left / quality gate） | ADR-001 D1 + ADR-003 D2 | v0.5+ |
| `hf-security-hardening`（OWASP / threat modeling 上线侧） | ADR-001 D1 + ADR-003 D2 | v0.5+ |
| `hf-performance-gate`（perf 硬门禁） | ADR-001 D1 + ADR-003 D2 | v0.5+ |
| `hf-deprecation-and-migration`（淘汰与迁移） | ADR-001 D1 + ADR-003 D2 | v0.5+ |
| `hf-debugging-and-error-recovery`（系统级调试与恢复） | ADR-001 D1 + ADR-003 D2 | v0.5+ |
| Gemini CLI / Windsurf / GitHub Copilot / Kiro 客户端扩展 | ADR-002 D2（D11 撤回） / ADR-003 D1 | v0.5+ |
| `hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor` personas | ADR-002 D4 / D8（D11 撤回） / ADR-003 D3 | v0.5+ |
| 真实环境 install smoke 硬门禁 | ADR-002 D3（D11 撤回） / ADR-003 D7 | v0.5+ |
| `audit-skill-anatomy.py` 升级为 hard gate | ADR-002 D5 / ADR-003 D8 | v0.5+ |
| `docs/principles/` 其余段落升级为合规基线 | ADR-001 D11 / ADR-002 D10 / ADR-003 D9 | v0.5+ |
| `examples/writeonce/` release-tier demo | ADR-001 D9 / ADR-003 D10 / ADR-004 D9 | 与下一次主链节点变更或 release-tier dogfood 同步触发 |

## Implementation 计划（R1–R7）

- **R1（ADR）**：本文件 `docs/decisions/ADR-004-hf-release-skill.md` 起草并锁定。**已落地**：本 commit。
- **R2（Skill 主体）**：新增 `skills/hf-release/SKILL.md` + 3 份 references 模板（`release-scope-adr-template.md` / `pre-release-engineering-checklist.md` / `release-pack-template.md`）+ `evals/` 占位（`README.md` + `evals.json`）。SKILL.md 必须满足 `docs/principles/skill-anatomy.md` v0.2.0 合规基线（含 `Common Rationalizations` 必需段，禁 `和其他 Skill 的区别` 单独段；邻接边界写在 `When to Use`）。
- **R3（Command 注册）**：新增 `.claude/commands/release.md` 注册 `/release [version]`，body 直接 instruct agent 加载 `skills/hf-release/SKILL.md`，**不**先经 router。
- **R4（Entry shell patch）**：`skills/using-hf-workflow/SKILL.md` 步骤 5 entry bias 表加 1 行（"切版本 / 出 release / 打 tag" → direct invoke `hf-release`）+ Boundary 段加 1 行说明（"`hf-release` 是 release-tier 独立 skill，不进 coding family / discovery family 主链"）。
- **R5（元数据 + 顶层文档同步）**：`.claude-plugin/plugin.json` `version` 0.3.0 → 0.4.0；`.claude-plugin/marketplace.json` plugin description 23 hf-* → 24 hf-* + 提及 `hf-release` + 强调 v0.4.0 不破坏 v0.3.0 客户端面；`README.md` + `README.zh-CN.md` 顶部 Scope Note 升级到 v0.4.0、Slash 命令表 6 → 7、skill 数 23 → 24；`docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/cursor-setup.md` 同步 Scope Note + "What is included" + NL → node 映射加 `hf-release` 行；`SECURITY.md` Supported Versions 表加 `0.4.x`；`CONTRIBUTING.md` 引言版本号 + ADR refs 升级。
- **R6（CHANGELOG）**：CHANGELOG 切到 `[0.4.0]` 段，按 Added / Changed / Decided / Deferred / Notes 五段写完；`[Unreleased]` 重置为"（无）"；版本号链接表加 `[0.4.0]`。
- **R7（发版）**：tag `v0.4.0`、GitHub Release 勾 pre-release、Release notes 引用 ADR-004。不附冒烟报告（D7 不增设硬门禁）。

## Notes

- 本 ADR 与 v0.3.0（pre-release minor release）的关系：v0.3.0 是单客户端扩张（Cursor，2 → 3 家），不引入新 skill；v0.4.0 在 v0.3.0 基础上首次扩大 skill 集合（23 → 24），但客户端面不变（仍 3 家），ops 侧 6 项继续延后。
- D3 选择"完全解耦"路径而非"router conditional insertion"路径：与 `hf-experiment` / `hf-hotfix` / `hf-increment` 这些既有支线 skill 不同。理由是 `hf-release` 触发条件（用户切版本意图）不与单 feature workflow 共享上下文；硬塞进 router transition map 会让 router 带一段几乎不命中的长期分支。如果未来 `hf-release` 需要被某些主链节点（例如未来的 `hf-shipping-and-launch`）下游消费，可在 v0.5+ ADR 评估是否补 router transition；v0.4.0 不预留接口。
- `hf-release` 起草过程参考了 `addyosmani/agent-skills` 的 `shipping-and-launch` SKILL anatomy（process / verification / red flags / rationalizations），但**仅借鉴 anatomy 风格**——内容上 `hf-release` 严格停在工程级 release（版本切片），不包含 staged rollout / 监控 / 回滚等 ops 侧动作。`addyosmani/shipping-and-launch` 对应的 HF 等价物是 v0.5+ planned 的 `hf-shipping-and-launch`，与 `hf-release` 正交。
- Entry bias 表加 1 行（R4）是入口分类器层动作，不是 runtime FSM 动作；与 D3 "完全解耦于 router" 立场不冲突。`using-hf-workflow` 在文档中已声明自己是 public shell / front controller，不是 authoritative router；它的 entry bias 表本来就同时承载 router-first 行（6 行）与 direct invoke 行（如 `hf-product-discovery` / `hf-specify` 在条件满足时的 direct invoke 路径）。

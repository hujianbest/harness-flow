---
name: hf-release
description: 适用于把多个已 closed 的 feature/iteration 汇总成 vX.Y.Z 工程级发版（版本切片 + 全量回归 + 发布文档聚合）。当用户表达"切版本/出 release/打 tag/发版本号"时使用。不适用于单 feature closeout、上线/部署/监控/回滚（不在本 skill 范围；由项目自身的 ops 流程承担）。
---

# HF Release

把若干个已 `workflow-closeout` 的 feature 汇总成一次 vX.Y.Z **engineer-level release**。负责锁范围、做版本级回归、聚合发布文档、产出 tag-ready pack。**不**做部署 / staged rollout / 监控 / 回滚——这些不在本 skill 范围，由项目自身的 ops 流程承担。

## When to Use

适用：

- 用户表达 "切 vX.Y.Z" / "出 release" / "发版本号" / "打 tag" 意图（含 `/release [version]` 命令）
- 仓库累积 ≥ 1 个 `workflow-closeout` 的 feature，且需要切版本号
- 要做 **release-wide full regression**（不是单 feature 的 impact-based 回归）
- 要聚合多 feature 的 release notes / CHANGELOG / migration / known limitations
- 要产 release scope ADR（仿 ADR-001/002/003 风格的版本范围决策）

不适用：

- 单 feature closeout（task-closeout 或 workflow-closeout） → 收尾归档
- 实际部署 / feature flag rollout / 监控配置 / 回滚演练 → 不在本 skill 范围；由项目自身的 ops 流程承担
- 需要新实现或补 fresh evidence → 上游编排者 实现层 TDD / 各 gate；本 skill **不**写新代码
- 候选 feature 还没 `workflow-closeout` → 先回到 收尾归档 把它们 close 掉
- 阶段不清 / 用户意图不是切版本 → 上游编排者编排者 → 由 entry shell 重新分流

边界：本 skill 与 上游编排者 完全解耦——不进 router transition map，不修改主链 FSM，**不依赖** 收尾归档 / 回归门禁 / 文档新鲜度门禁 在同一 session 跑过。它只读磁盘工件（feature 的 `closeout.md` / `progress.md` / 既有 review / verification 记录）做版本级判断。

## Hard Gates

- 任一候选 feature 的 `closeout.md` 不是 `Closeout Type: workflow-closeout` → **拒入**（task-closeout / blocked 都不算）
- candidate feature 的 `completion` / `regression` 记录缺失或与 closeout 结论矛盾 → **拒入**
- release-wide regression 缺失或不 fresh（与本次 release scope 不匹配）→ **拒出**
- CHANGELOG `[vX.Y.Z]` 段未落盘 → **拒出**
- release scope ADR 草稿未落盘 → **拒出**
- `interactive` 模式下 Final Confirmation 未通过 → 不写 `Next Action: null`
- **不得**承诺部署 / 监控 / 回滚演练 / SLO / health check / staged rollout / feature flag——这些不在本 skill 范围
- **不得**自动执行 `git tag` / `git push --tags`——本 skill 只产 readiness pack，tag 操作交给项目维护者
- **不得**自动删除 worktree——只能记录 disposition
- **不得**让 release scope ADR 由作者自我批准——`docs/principles/soul.md` 立场：HF 不替用户验收自己；建议由独立人/会话评审 ADR draft 后再 commit

## Object Contract

- **Primary Object**: `Release Pack`——版本级工件聚合（scope 决策 + evidence matrix + docs sync 记录 + tag readiness）
- **Frontend Input Object**: 候选 feature 的 `closeout.md`（type=workflow-closeout）+ 各 feature 的 verification / reviews 记录 + 项目级版本号约定（若有）
- **Backend Output Object**: `features/release-vX.Y.Z/release-pack.md` + 仓库根 `CHANGELOG.md` 的 `[vX.Y.Z]` 段 + `docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md` + `docs/release-notes/vX.Y.Z.md`（按存在）+ ADR 状态批量翻转（`proposed → accepted`）
- **Object Transformation**: 输入是 N 份 `workflow-closeout` 的 closeout pack；输出是 1 份 release pack + 配套发布文档；中间步骤是 scope 决策 + release-wide regression + docs aggregation
- **Object Boundaries**: 不修改既有 `features/<feature-id>/closeout.md`（只读消费）；不修改 spec/design/tasks 等已批准工件；不替代 收尾归档 写单 feature closeout
- **Object Invariants**: 所有候选 feature 的 closeout 状态在 版本发布 执行前后一致；release pack 一旦写入，scope 已定，再要扩范围必须显式回到 §3 重做 scope 决策

## Methodology

| 方法 | 来源 | 落到哪一步 |
|---|---|---|
| Release Scope ADR | HF 自身 ADR-001/002/003 实践 | §3 |
| SemVer 2.0.0 + Pre-release Marker | semver.org / ADR-001 D6 / ADR-002 D6 / ADR-003 D5 | §4 |
| Cross-feature Regression（impact-based 的版本级扩展）| Regression Testing Best Practice | §6 |
| Cross-feature Traceability Aggregation | Zigzag Validation（向上延伸到版本范围） | §7 |
| Sync-on-Presence (release tier) | 同 文档新鲜度门禁（**协议内联**，不引用该 skill）| §8 |
| Release Readiness Review | PMBOK release readiness | §9 |
| Handoff Pack Pattern | 同 收尾归档（结构同源，scope 不同）| §10 |
| Standalone / No-Router Coupling | 本 skill 自包含运行原则（ADR-004 D3）| 全流程 |
| Author / Reviewer Separation (Fagan) | scope ADR 建议由独立人/会话评审 | §3 末尾 advisory |

## Workflow

### 1. Entry vs Recovery（自给自足，不依赖 router）

读 `features/release-vX.Y.Z/release-pack.md`：

- 不存在 → **新建 release**，进 §2
- 存在但 Final Confirmation 字段为空或 `Status: in-progress` → **续 release**，跳到上次中断的步骤
- 存在且 `Status: released` 或 `Final Confirmation: confirmed` → 已收口，告知用户后退出（不重做）

`vX.Y.Z` 版本号优先级：用户传入 hint > 项目级版本号约定 > 默认按 SemVer 推断（见 §4）。

### 2. 候选 Feature 盘点

- **Object**: 候选 feature 集合
- **Method**: 扫 `features/*/closeout.md`，筛 `Closeout Type: workflow-closeout`
- **Input**: 仓库 `features/` 目录
- **Output**: 候选清单（feature-id + closeout 路径 + 关闭日期 + affected modules 摘要）
- **Stop / continue**: 候选数 = 0 → 抛回用户"无可入版的 closed feature，建议先 收尾归档"；候选数 ≥ 1 → 继续

不要把 `task-closeout` / `blocked` 当成候选——这两类未真正完成单 feature workflow。

### 3. Release Scope ADR 起草

- **Object**: scope ADR 草稿
- **Method**: 仿 ADR-001/002/003 模板（背景 / Decisions / Tradeoffs / Consequences / v0.X+ Roadmap / Implementation R1–RN / Notes），见 `references/release-scope-adr-template.md`
- **Input**: §2 候选清单 + 用户口径（必入 / 显式 defer / 限制说明）
- **Output**: `docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md`（草稿）+ scope decision 摘要写入 release pack 的 `## Scope Summary`
- **Stop / continue**: scope 与候选清单不一致（含未列入的、含未在候选中的）→ 停下问用户；一致 → 继续

**Author/Reviewer separation (advisory)**：建议在 commit ADR draft 前，由独立人/会话评审一遍（HF Fagan 立场）。本 skill 不强制 hard gate——保持 standalone 性质，由项目自己决定评审节奏。

### 4. SemVer + Pre-release 判定

- **Object**: 版本号 + pre-release 标记
- **Method**: SemVer 2.0.0 决策表
  - 含任一 breaking change → **major** bump
  - 仅含 backward-compatible 新功能 → **minor** bump
  - 仅含 backward-compatible bug fix → **patch** bump
  - 主链覆盖未达 100% / 客户端面无质变 / 用户场景未稳定 → 仍勾 **pre-release**（沿用 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 默认）
- **Input**: §3 scope ADR + 既有版本号
- **Output**: vX.Y.Z + pre-release: yes/no
- **Stop / continue**: 项目级约定（CalVer / 自定义）覆盖默认时遵循项目约定

### 5. Worktree / 分支盘点

- **Object**: 各候选 feature 的 worktree disposition
- **Method**: 读 `features/<feature-id>/closeout.md` 的 `Worktree Disposition` 字段；对仍是 `kept-for-pr` 的 feature，确认对应 PR 已合并到 release base branch
- **Input**: §2 候选清单
- **Output**: worktree disposition 清单写入 release pack
- **Stop / continue**: 任一候选 feature 的 PR 仍 open → 抛回用户决定（要么先合并 PR，要么把该 feature 移出本次 scope）；不擅自删除 worktree

### 6. Release-wide Regression（协议内联）

- **Object**: 版本级回归 evidence
- **Method**: 内联 fresh-evidence 协议
  1. **Scope** = `union(各候选 feature 的 affected modules)`
  2. **Profile-aware rigor**：full / standard 必须跑 union 全集；lightweight 至少跑 critical path 子集
  3. **Fresh evidence**：执行点必须晚于所有候选 feature 最晚一次 closeout 时间
  4. **失败 = 拒出**，不允许把单 feature 历史 regression 记录拼贴当成 release-wide 通过
- **Input**: §5 scope + 项目测试入口（项目级约定优先；默认尝试 `npm test` / `pytest` / `make test` / 项目 CI 入口）
- **Output**: `features/release-vX.Y.Z/verification/release-regression.md`（含 scope / 执行命令 / 时间戳 / 通过/失败结论 / 失败时的 reroute 指向）
- **Stop / continue**: 失败 → 抛回用户 + 标记需修复哪个 feature；通过 → 继续

如果项目无统一测试入口或测试基础设施缺失，**不**降级回归——而是停下来抛回"项目缺乏 release-wide regression 入口，建议先建立"，让用户决定是延后发版还是临时降级；不替用户拍板降低门禁。

### 7. Cross-feature Traceability 摘要

- **Object**: 跨 feature 的 spec ↔ design ↔ tasks ↔ code ↔ tests 链聚合摘要
- **Method**: 不重做单 feature traceability（那是 追溯评审 在 closeout 前已经做过的事）；只做版本级聚合——把各 feature 的 traceability verdict 汇总
- **Input**: 各候选 feature 的 `reviews/traceability-*.md` / `closeout.md` `Evidence Matrix` 段
- **Output**: `features/release-vX.Y.Z/verification/release-traceability.md`（含每个 feature 的 traceability verdict + 跨 feature 风险（如有 API 变化跨多个 feature））
- **Stop / continue**: 任一候选 feature 缺 traceability verdict 且 profile 要求 → 抛回用户；profile 跳过的写 `N/A（按 profile 跳过）`

### 8. Pre-Release Engineering Checklist

按 `references/pre-release-engineering-checklist.md`，分小节核对（**仅工程级 hygiene；显式不含 ops 项**）：

#### Code & Evidence

- [ ] §6 release-wide regression 通过
- [ ] §7 cross-feature traceability 摘要落盘
- [ ] 所有候选 feature 是 `workflow-closeout` 状态
- [ ] 所有 lint / type / build 在 release base branch 上通过

#### Documentation Sync（sync-on-presence 协议内联）

- [ ] **CHANGELOG.md** 的 `[vX.Y.Z]` 段已写（**任何 tier 必填**）
- [ ] 顶层导航已更新：档 0/1 仓库根 `README.md` 中 active feature / 最近 release 行；档 2 `docs/index.md`
- [ ] 涉及的 ADR 状态已批量从 `proposed` 翻为 `accepted`（含本次 release scope ADR 翻转时机：在 Final Confirmation 通过时）
- [ ] 按存在同步：`docs/release-notes/vX.Y.Z.md`（仅档 2 启用时）/ `docs/architecture.md` 或 `docs/arc42/`（仅本 release 改了架构图景时）/ `docs/runbooks/` / `docs/slo/` / `docs/diagrams/`（仅对应目录已存在或本 release 触发首次启用）
- [ ] 每个 feature 的 closeout `Release / Docs Sync` 字段与本次 release 的 docs 同步**对账一致**（不允许 feature 声称已同步但 release 这一层没找到对应路径）
- [ ] Migration / breaking changes（若有）已写入 release notes 的 `## Migration Notes`
- [ ] Known Limitations 已聚合各 feature closeout 的 `Limits / Open Notes` 字段

#### Versioning Hygiene

- [ ] §3 release scope ADR 已 commit（草稿状态可，等 Final Confirmation 后翻 accepted）
- [ ] §4 SemVer + pre-release 决策已写入 release pack
- [ ] `.claude-plugin/plugin.json` `version` 字段（按存在）已同步到 vX.Y.Z
- [ ] `.claude-plugin/marketplace.json`（按存在）描述同步
- [ ] `SECURITY.md` Supported Versions 表（按存在）加 `X.Y.x` 行
- [ ] 任何项目级元数据中的版本号（package.json / pyproject.toml / Cargo.toml / 等）已同步

#### Worktree / Branch State

- [ ] §5 worktree disposition 全部记录在 release pack
- [ ] 无 release-blocking PR 仍 open
- [ ] release base branch 已是各候选 feature 合并后的状态

#### Out of Scope（显式列出本 skill **不**做的事）

- 部署到 production / staging / canary
- Feature flag 0% → 5% → 100% 的 staged rollout
- 监控仪表盘 / 错误上报 / SLO 配置
- 回滚 procedure / 回滚演练
- Health check / CDN / DNS / SSL / Rate limiting
- 上线后的观察窗口

以上不在本 skill 范围；如项目需要这些能力，由项目自身的 ops 流程承担——**不**写进本 skill 的 evidence。

### 9. 形成 Evidence Matrix

每条 release 证据写出：

- artifact name
- record path
- 是否适用于当前 profile
- 不适用时写 `N/A（按 profile 跳过）`

写入 release pack 的 `## Evidence Matrix` 段。

### 10. 产出 Release Pack

按 `references/release-pack-template.md` 写入 `features/release-vX.Y.Z/release-pack.md`。至少包含：

- Release Summary（version / pre-release flag / scope ADR 路径 / included features / deferred features）
- Evidence Matrix
- Docs Sync 实际同步路径
- Tag Readiness（建议 tag 名 / 建议 commit / 分支 / PR 状态）
- Worktree Disposition
- Final Confirmation（interactive only）
- Limits / Open Notes（明确告知部署 / 监控 / 回滚等上线侧能力不在本 skill 范围，由项目自身 ops 流程承担）

### 11. Final Confirmation（interactive only）

版本发布 完成后会让 release scope 正式锁定（ADR 状态翻转 / CHANGELOG 段固化 / tag readiness pack 就位）；这是项目的对外承诺面变化，不能由 skill 自行决定。

- `interactive`：先展示 Release Summary + Evidence Matrix + Docs Sync 实际路径 + Tag Readiness，等真人确认 "正式锁定 vX.Y.Z 范围"；
- `auto`：先写完 release pack（`Status: ready-for-tag`），把 Next Action 写成 `null`（实际 `git tag` 由项目维护者执行），不替用户最终拍板。

如果用户不同意锁定，回到 §3（scope 改动）或 §6（regression 失败）按需重做对应步骤。

## Output Contract

工件目录布局：

```
features/release-vX.Y.Z/
  release-pack.md                 # 主工件（必出）
  scope-decision.md               # 反向引用 docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md（按需）
  progress.md                     # 复用 feature progress schema（按需，记录 §1–§11 推进状态）
  verification/
    release-regression.md         # §6（必出）
    release-traceability.md       # §7（必出）
    pre-release-checklist.md      # §8（必出，含勾选状态）

docs/decisions/
  ADR-NNN-release-scope-vX.Y.Z.md # §3（必出）

CHANGELOG.md                      # 必出 [vX.Y.Z] 段

docs/release-notes/
  vX.Y.Z.md                       # 仅档 2 启用时
```

`release-pack.md` 必备字段见 `references/release-pack-template.md`。

Next Action 规则：

- **Final Confirmation 通过 / Status: released**：`Next Action Or Recommended Skill: null`（tag 操作由项目维护者执行；本 skill 不自动打 tag）
- **未通过 / 阻塞**：`Next Action Or Recommended Skill: <具体阻塞点描述>`，例如"§6 release-wide regression failed on module X，先回 实现层 TDD 修复对应 feature 的回归"
- **scope 还未锁定**：`Next Action Or Recommended Skill: 版本发布 §3`（同 skill 内回退）

不写回 上游编排者（本 skill 与 router 解耦，没有"交回 router"的语义）。

## Red Flags

- 把单 feature 的 release notes 直接当成 vX.Y.Z 整包发布说明
- 用 commit messages dump 充当 release notes
- 跳过 §6 release-wide regression，仅复用各 feature 的 impact-based 历史回归记录
- 候选 feature 的 ADR 仍是 `proposed` 就声称 release ready
- 在 release pack 中混入 ops 动作（feature flag / 监控 / 回滚演练）
- 把 release-pack 写到 `features/<某 feature-id>/closeout.md`（应在独立目录 `features/release-vX.Y.Z/`）
- 自动执行 `git tag` 或 `git push --tags`（本 skill 范围之外）
- 自动删除 worktree（只能记录 disposition）
- 一次发版同时纳入 breaking change + new feature + bug fix 而不分版本号语义（应按 SemVer 拆分或承认 major bump）
- 因为没有项目级 release-wide 测试入口就把 §6 写成 `N/A` 蒙混过关
- release scope ADR 由 skill 作者一手批准（违反 Fagan 分离 advisory）
- 把"用户当前在用什么客户端"作为 release 决策的输入（HF release 是 client-agnostic）
- 假设存在一个"现成的部署/上线 skill"可以承接被本 skill 拒绝的 ops 动作；out-of-scope 能力应直接说"由项目自身 ops 流程承担"，不要把读者推到一个虚构或未交付的 skill

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "/release 之后顺便 git tag + push 一下" | Hard Gates: 本 skill 只产 readiness pack；tag 是项目维护者动作，不在 skill 范围 |
| "复用各 feature 的 regression 记录就够了，不用再跑一次" | Hard Gates + §6: release-wide regression scope = union(features)，必须 fresh；拼贴 = 不通过 |
| "scope ADR 我自己拍就行了，多评审一轮浪费时间" | Author/Reviewer Separation 是 advisory 不是 hard gate，但 Red Flags 指出"作者一手批准"；与 `docs/principles/soul.md` "HF 不替用户验收自己" 立场冲突 |
| "这次 release 顺便配置一下 staged rollout / 监控 / 回滚" | Hard Gates: 本 skill 不承诺部署 / 监控 / 回滚；这些不在本 skill 范围，由项目自身的 ops 流程承担 |
| "router 应该把我派过来" / "我应该 handoff 回 router" | When to Use 边界 + ADR-004 D3: 版本发布 与 router 完全解耦；不进 transition map，不交回 router |
| "项目没有统一的测试入口，§6 就标 N/A 跳过" | Hard Gates + §6 stop rule: 不替用户拍板降低门禁；缺入口要抛回用户决定（延后发版或临时降级），不能自己跳过 |
| "task-closeout 的 feature 也算入版吧，反正快做完了" | Hard Gates: 候选必须是 `workflow-closeout`；task-closeout 还有剩余任务未完成 |
| "writeonce demo 顺便也 release 一下" | When to Use + ADR-004 D9: writeonce demo 不走 release-tier；强加是空洞同步 |

## Reference Guide

| 文件 | 用途 |
|------|------|
| `references/release-scope-adr-template.md` | release scope ADR 起草模板（仿 ADR-001/002/003 结构） |
| `references/pre-release-engineering-checklist.md` | §8 详细 checklist（仅工程级 hygiene；不含 ops 项） |
| `references/release-pack-template.md` | release pack 主工件模板（schema 与 收尾归档 closeout pack 同源） |
| `收尾归档/SKILL.md` | 单 feature closeout（前置依赖：候选 feature 必须先经此 skill 写出 `workflow-closeout` 的 closeout pack） |
| `实现层 TDD/references/worktree-isolation.md` | worktree disposition 收尾语义（不擅自删除；只记录 `kept-for-pr` / `cleaned-per-project-rule` / `in-place`） |
| `docs/decisions/ADR-001-release-scope-v0.1.0.md` 等 | HF 自身 release scope ADR 实践，可作 scope ADR 起草参考 |

## Verification

- [ ] §1 已判断 entry vs recovery（不依赖 router）
- [ ] §2 候选 feature 全部为 `workflow-closeout` 状态
- [ ] §3 release scope ADR 已落盘（草稿可），且与候选清单一致
- [ ] §4 SemVer + pre-release 标记已决策并写入 release pack
- [ ] §5 worktree disposition 全部记录
- [ ] §6 release-wide regression 通过且 fresh，evidence 路径已落盘
- [ ] §7 cross-feature traceability 摘要落盘
- [ ] §8 Pre-Release Engineering Checklist 各小节全部勾选或显式 N/A
- [ ] §9 Evidence Matrix 已写入 release pack
- [ ] §10 release pack 已写入 `features/release-vX.Y.Z/release-pack.md`
- [ ] §11 Final Confirmation（interactive 模式）已通过；ADR 状态从 proposed 翻为 accepted
- [ ] CHANGELOG.md `[vX.Y.Z]` 段已 commit
- [ ] 所有项目级元数据中的版本号字段已同步
- [ ] 未自动执行 `git tag` / `git push --tags`
- [ ] 未自动删除 worktree
- [ ] Next Action 写为 `null`（已 released）/ 具体阻塞点（未通过）/ `版本发布 §<step>`（同 skill 回退）；**不**写回 上游编排者
- [ ] release pack 中未越权承诺部署 / 监控 / 回滚（out-of-scope 能力已明确指向"项目自身 ops 流程"，未编造或假设其他 skill 接手）

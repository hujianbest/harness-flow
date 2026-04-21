# SDD Artifact Layout — HarnessFlow 工件管理约定

- 定位: 项目级原则文档，定义在 HarnessFlow 这套 SDD + TDD workflow 下，**过程交付件**与**项目长期资产**应该如何组织、命名与流转。
- 来源: 由用户讨论拍板（参见本仓库相关 PR/issue），上收为项目级约定。
- 关联:
  - HF family 共享文档: `skills/docs/hf-workflow-shared-conventions.md`
  - Skill 写作原则: `docs/principles/skill-anatomy.md`
  - SDD + TDD 设计原则: `docs/principles/hf-sdd-tdd-skill-design.md`

## 定位

本文回答一个具体问题：**在 HarnessFlow 风格的 SDD 开发过程中，工件应该放在哪里、叫什么名字、什么时候从过程交付件晋升为长期资产。**

它不替代 `skills/docs/hf-workflow-shared-conventions.md` 里的 progress schema、verdict 词表、record_path 语义等运行时约束；它只回答"工件物理布局与生命周期"这一层。

它也不引入隐藏目录（如 `.sdd/`）、frontmatter schema 或 CI 校验。约束完全靠：

- 模板（`skills/templates/`）
- skill 自身的 prose checklist 与 reviewer subagent
- 本文件定义的命名与目录纪律

如果未来项目体量超过这套"纯纪律"模型可承受的边界，再考虑引入轻量校验脚本，**不在本约定的范围内**。

## 核心原则：双根目录二分

仓库下文档资产分两个根目录：

| 目录 | 性质 | 时间尺度 | 演化方式 | 读者入口 |
|---|---|---|---|---|
| `docs/` | **项目长期资产** | 跨多个 feature 周期 | 慢、累积，被多个 feature 修改 | 任何接手项目的人/agent |
| `features/` | **过程交付件** | 单个 feature 周期内 | 一次性产出，closeout 后基本不动 | 顺着 active feature 进入 |

一句话：

> `docs/` 回答"系统现在是什么样、为什么是这样"；`features/` 回答"这一轮我们做了什么、怎么做的、谁批准的"。

这两个根**互不替代、互相引用**。`features/` 中的设计文档通过编号引用 `docs/adr/` 的 ADR；`docs/` 中的长期资产由 feature 周期内的设计阶段或 closeout 阶段触发更新。

## Minimal `docs/` Tiers

不同体量的项目对长期资产的需要量差别很大。本约定把 `docs/` 下的子目录按"不可省 / 强烈建议 / 按需启用"分成三档，允许项目按当前体量选择启用范围；HF skill 也按"按存在同步"策略对未启用的资产保持容错。

### 判断标准

一个 `docs/` 子目录是否能省，按两条标准判断：

1. 去掉它，**当前 feature 周期能不能完整跑完**？能 → 不属于强制项。
2. 去掉它，**未来某个 feature 起步时会不会丢失关键上下文**？会 → 不能省。

### 档 0：绝对最小（不可省）

```text
docs/
  principles/
    sdd-artifact-layout.md          # 本文件自身
    architecture-principles.md      # 可选放
  adr/
    0001-record-architecture-decisions.md
    NNNN-<slug>.md
```

加上仓库根：

```text
CHANGELOG.md                        # 用户可见变更（Keep a Changelog）
README.md                           # 仓库入口；至少列：当前 active feature + 系统一句话定位 + ADR 索引链接
```

不可省的理由：

- `docs/principles/sdd-artifact-layout.md` 是工件管理约定本身，`AGENTS.md` 中所有路径覆盖与 skill 中"项目级原则锚点"的引用都落到这里。
- `docs/adr/` 是架构决策**唯一不可被 feature 周期回收的载体**。`features/<NNN>/design.md` 通过 ADR ID 引用，feature closeout 后 design.md 仍在原地，但承载决策原文的必须是独立于任何 feature 的 `docs/adr/NNNN-...md`。
- 仓库根 `README.md` 是没有 `docs/index.md` 时唯一的"哪个 feature 是 active"导航点。
- `CHANGELOG.md` 是用户视角的累计视图，不能被任何 feature 目录代偿。

### 档 1：强烈建议（典型项目几乎一定要）

在档 0 基础上加：

```text
docs/
  architecture.md                   # 单文件架构概述；合并 arc42 12 节为一文件
```

推荐结构（5–8 节即可）：

1. 系统目标与边界
2. 关键约束
3. 主要模块 / 组件视图（一张 Mermaid C4-Container 图就够）
4. 关键运行时交互（1–2 张 sequence/flow 图）
5. 关键非功能属性（performance / availability / security 怎么落地）
6. 已知风险与技术债
7. 术语表
8. ADR 索引链接

理由：没有架构概述时，新成员/新 agent 读 feature 周期的 `design.md` 会缺乏"系统现状"上下文，每个 feature 都要重新拼图。但 arc42 完整 12 节对小项目过重，单文件 `architecture.md` 解决 80% 问题。

### 档 2：按需启用

| 子目录 | 启用条件 |
|---|---|
| `docs/diagrams/` | 至少有一张图复杂到不适合内嵌 Mermaid（例如要用 Structurizr DSL / PlantUML 做静态分析） |
| `docs/runbooks/` | 系统已经在运行，需要值班/排障；或 `hf-finalize` 必须为新引入的运维点写 runbook |
| `docs/slo/` | 项目把 availability / latency / error budget 当作 first-class NFR |
| `docs/postmortems/` | 出过第一个值得复盘的事故 |
| `docs/release-notes/vX.Y.Z.md` | `CHANGELOG.md` 单文件已显著变长（>500 行）或需按版本独立链接 |
| `docs/bug-patterns/catalog.md` | `hf-bug-patterns` 在项目里实际启用并产出过 catalog 条目 |
| `docs/index.md` | 当 `features/` 下超过约 10 个目录、`docs/adr/` 超过约 20 个文件时，单纯靠仓库根 `README.md` 不够 |
| `docs/insights/` | `hf-product-discovery` 实际启用，且 discovery 草稿需长期留存 |
| `docs/arc42/` | 项目已大到 `architecture.md` 单文件难以维护（>1500 行），再拆为 arc42 12 节 |

### 推荐起步档位

绝大多数项目从**档 1** 起步。理由：

- 档 0 缺架构概述，第二个 feature 进来时一定会发现需要补；不如一开始就放一份骨架，逐步增长。
- 档 2 子目录"等需要时再加"是没问题的，因为 ADR 编号和 `architecture.md` 演化路径不会被它们的缺席破坏。

### 升级时机（事件驱动）

不要提前过度配置。当某个 skill 第一次因为某个目录不存在而判 `blocked` 或回到 router 时，自然就到了升级时机：

| 触发事件 | 应启用 |
|---|---|
| 第一次有图复杂到 Mermaid 不够 | `docs/diagrams/` |
| 第一次部署到生产，需要值班 | `docs/runbooks/` |
| 第一次声明 SLO / error budget | `docs/slo/` |
| 第一次出事故 | `docs/postmortems/` |
| `CHANGELOG.md` 超长 | 拆出 `docs/release-notes/vX.Y.Z.md` |
| 第一次启用 `hf-bug-patterns` | `docs/bug-patterns/catalog.md` |
| `features/` 数量难以一眼浏览 | `docs/index.md` |
| 启用 `hf-product-discovery` | `docs/insights/` |
| `architecture.md` 单文件过大 | 拆为 `docs/arc42/` 12 节 |

### Skill 的容错语义

HF skill 在引用 `docs/` 子目录时遵循 **read-on-presence + sync-on-presence** 原则：

- 读取（`hf-design` / `hf-workflow-router` 等）：若引用的 `docs/` 子目录不存在，**视为该资产未启用**，不阻塞当前节点；以"已存在的等价资产"或"项目当前未启用此类资产"作为判断结论。
- 同步（`hf-finalize`）：closeout 时只对 **`docs/` 下实际存在的子目录**做同步检查；未启用的资产不要求新建，也不据此判 `blocked`。
- 替代关系：
  - `docs/architecture.md` 存在但 `docs/arc42/` 不存在时，`hf-design` / `hf-finalize` 把 `docs/architecture.md` 当作架构图景的等价载体。
  - 仓库根 `README.md` 存在但 `docs/index.md` 不存在时，`hf-workflow-router` 把仓库根 `README.md` 当作 active feature 指针的等价来源。
  - `CHANGELOG.md` 存在但 `docs/release-notes/` 不存在时，`hf-finalize` 把 `CHANGELOG.md` 当作 release notes 的唯一载体。

详细 skill 适配规则见 `skills/docs/hf-workflow-shared-conventions.md` 的 *长期资产同步规则（promotion rules）* 与各 skill `SKILL.md`。

## `docs/` 下放什么（项目长期资产）

下面是**完整版**布局；带 tier 标记。最小化布局见上节 *Minimal `docs/` Tiers*。

```text
docs/
  principles/                  # [档 0]  项目原则 / "soul docs" / constitution
    sdd-artifact-layout.md     #         本文件，不可省
    architecture-principles.md
    product-principles.md
    coding-principles.md
  adr/                         # [档 0]  架构决策日志（仓库级 pool），不可省
    0001-record-architecture-decisions.md
    0042-introduce-rate-limiter.md
  architecture.md              # [档 1]  单文件架构概述；与 arc42/ 二选一
  arc42/                       # [档 2]  长期架构图景（arc42 12 节），仅当 architecture.md 单文件撑不住
    01_introduction_and_goals.md
    ...
    10_quality_requirements.md
    12_glossary.md
  diagrams/                    # [档 2]  源码化的图
    structurizr/
      workspace.dsl
    plantuml/
  runbooks/                    # [档 2]  运维手册
  slo/                         # [档 2]  可靠性指标
  postmortems/                 # [档 2]  事故复盘
  release-notes/               # [档 2]  用户可见变化（按版本一文件）；与仓库根 CHANGELOG.md 配合
    v1.4.0.md
    v1.5.0.md
  bug-patterns/                # [档 2]  hf-bug-patterns 沉淀
    catalog.md
  insights/                    # [档 2]  hf-product-discovery 草稿留存
  index.md                     # [档 2]  顶层导航；档 0/1 时由仓库根 README.md 代偿
```

约束：

- `docs/principles/` 是 `hf-design` 中"项目级设计原则锚点"的默认落点。`AGENTS.md` 中可写明 `design principles path: docs/principles/`。
- `docs/adr/` 是 ADR 的**唯一权威池**，仓库级顺序号、不复用、不按 feature 分散。
- 架构图景的载体按 tier 决定：档 1 用 `docs/architecture.md` 单文件；档 2 拆为 `docs/arc42/` 12 节。一次 feature 完成后，已存在的那一份必须被同步更新（同步规则见 *Promotion Rules*）。
- `CHANGELOG.md` 仍放仓库根（Keep a Changelog 惯例）。`docs/release-notes/vX.Y.Z.md` 是档 2 的"详细 release notes"载体；档 0/1 时仅 `CHANGELOG.md` 即可。
- 顶层导航按 tier 决定：档 0/1 由仓库根 `README.md` 承担（至少列出：当前 active feature + 系统一句话定位 + ADR 索引链接）；档 2 才启用 `docs/index.md`，列出更详细的 active feature / 最近若干个 closeout / ADR 编号最大值 / 当前 release。

## `features/` 下放什么（过程交付件）

```text
features/
  003-rate-limiting/
    README.md                  # feature 入口 + 状态总览
    spec.md                    # 需求规格
    design.md                  # 设计（链 docs/adr/ 中的 ADR 编号）
    ui-design.md               # 仅当声明 UI surface 时存在
    data-model.md              # 可选
    contracts/                 # 本次新增/变更的 API 契约草稿
      rate-limit.openapi.yaml
    tasks.md                   # 任务拆解
    task-board.md              # 可选；用于 task-to-task 自动推进
    progress.md                # feature 范围内的 task-progress（唯一权威）
    reviews/
      spec-review-2026-04-18.md
      design-review-2026-04-19.md
      ui-review-2026-04-19.md
      tasks-review-2026-04-19.md
      code-review-task-001.md
      test-review-task-001.md
      traceability-review.md
    approvals/
      spec-approval-2026-04-18.md
      design-approval-2026-04-19.md
      tasks-approval-2026-04-20.md
    verification/
      regression-2026-04-21.md
      completion-2026-04-21.md
    evidence/                  # fresh evidence（命令输出 / 日志 / 性能基线）
      task-001-red.log
      task-001-green.log
      bench-baseline.json
    closeout.md                # finalize 的 closeout pack
```

约束：

- **feature 目录是自包含的工件包**。同一 feature 的所有过程证据都聚在一个目录里，便于 PR diff、review、归档与移交。
- **`README.md` 是 feature 入口**，必须列出：feature 状态、关键日期、相关 ADR 编号、spec / design / tasks 文件路径、当前 active task、closeout 状态。在没有 catalog/CI 的前提下，这是 feature 内**可发现性的唯一兜底**。
- **`progress.md` 是该 feature 的唯一 task-progress 落点**。仓库根**不再保留全局 `task-progress.md`**——"当前 active feature 是哪个"由 `docs/index.md` 与 active feature 自身的 `progress.md` 共同表达。
- **closeout pack 文件名为 `closeout.md`**，不再叫 `finalize-closeout-pack.md`。模板内容仍以 `skills/templates/finalize-closeout-pack-template.md` 为准。
- **不引入 `archived/` / `done/` 子目录**。closeout 后的 feature 平铺保留在 `features/` 下，状态从 `closeout.md` 内读取。理由：归档移动会破坏所有从 `docs/adr/`、`docs/arc42/`、其它 feature 反向引用过来的相对路径链接。

## 命名约定

### Feature 目录

`features/NNN-kebab-slug/`

- `NNN`：三位顺序号，从 `001` 起。
- `slug`：kebab-case 短主题名。
- 编号一旦分配不再复用、不再改名（即使 feature 后来被 abandon）。
- 新 feature 编号 = `ls features/ | grep -E '^[0-9]{3}-' | sort | tail -n1` 的下一个数字。

### ADR

`docs/adr/NNNN-kebab-slug.md`

- `NNNN`：四位顺序号，从 `0001` 起，仓库级唯一。
- `slug`：kebab-case 决策短描述。
- 状态（proposed / accepted / deprecated / superseded）写在文档正文首段，不通过移动文件表达。
- ADR 永不删除、永不重新编号；被替代时更新 supersedes / superseded-by 双向链接（用 ADR ID 引用，不用路径）。

### Feature 目录内固定文件名

| 文件 | 必需性 | 说明 |
|---|---|---|
| `README.md` | 必需 | feature 入口与状态总览 |
| `spec.md` | 必需 | `hf-specify` 输出 |
| `design.md` | 必需 | `hf-design` 输出 |
| `tasks.md` | 必需 | `hf-tasks` 输出 |
| `progress.md` | 必需 | feature 范围 task-progress |
| `closeout.md` | finalize 后必需 | `hf-finalize` 输出 |
| `ui-design.md` | 条件必需 | 当 spec 声明 UI surface 时 |
| `data-model.md` | 可选 | 数据模型超出 design.md 容量时 |
| `task-board.md` | 可选 | 当需要 task-to-task 自动推进时 |
| `contracts/` | 可选 | 本次变更的 API 契约草稿目录 |

### Review / Approval / Verification

模式：`<kind>-<scope>-YYYY-MM-DD.md`

- review：`spec-review-YYYY-MM-DD.md`、`design-review-YYYY-MM-DD.md`、`code-review-task-NNN.md`（按任务编号而不是日期）、`traceability-review.md`（最终一次，无日期）。
- approval：`spec-approval-YYYY-MM-DD.md`、`design-approval-YYYY-MM-DD.md`、`tasks-approval-YYYY-MM-DD.md`。
- verification：`regression-YYYY-MM-DD.md`、`completion-YYYY-MM-DD.md`。
- 同日多份按需追加 `-NN` 序号后缀。

### Release notes

- `CHANGELOG.md`：仓库根，Keep a Changelog 风格。**档 0/1 必需。**
- `docs/release-notes/vX.Y.Z.md`：每个 release 一份详细描述。**档 2 启用；启用后 `CHANGELOG.md` 仍保留**，每个版本入口指向对应详细文件。

## Promotion Rules（过程交付件 → 长期资产）

这是双根布局最容易出问题的地方：feature 显然会修改 ADR、改 arc42、加 glossary 项、加 runbook。本约定采用**混合模式**：

| 长期资产类型 | 修改时机 | 修改方式 | 启用条件 |
|---|---|---|---|
| **ADR (`docs/adr/`)** | 设计阶段直接落到 `docs/adr/` | 起草时即分配 ADR ID，写入 `docs/adr/NNNN-...md`，状态 `proposed`；评审与 `设计真人确认` 通过后翻为 `accepted`。`design.md` 通过 ID 引用，不内联 ADR 全文。 | 档 0（不可省） |
| **架构概述（`docs/architecture.md` 或 `docs/arc42/`）** | closeout 阶段同步 | feature 设计稿可在 `design.md` 中描述对架构图景的影响；`hf-finalize` 在 closeout 时把已批准变更应用到现存的那一份载体（`docs/architecture.md` 或 `docs/arc42/` 对应节）。两者只能同时存在一份。 | 档 1 起；档 1 用单文件，档 2 拆 arc42 |
| **Glossary** | closeout 阶段同步 | 档 1 时归并到 `docs/architecture.md` 的术语表节；档 2 时落到 `docs/arc42/12_glossary.md`。feature spec / design 中引入的新术语由 closeout 同步。 | 跟随架构概述档位 |
| **Runbooks (`docs/runbooks/`)** | closeout 阶段同步 | feature 引入新运维关注点时，closeout 必须新增或更新对应 runbook。 | 档 2（仅当目录已存在或本 feature 引入第一个运维点） |
| **SLO (`docs/slo/`)** | closeout 阶段同步 | feature 引入新 SLO 或修改既有 SLO 时同步。 | 档 2（仅当目录已存在或本 feature 引入第一个 SLO） |
| **Diagrams (`docs/diagrams/`)** | 设计阶段或 closeout 阶段 | 源码化图（Structurizr DSL / PlantUML）允许在设计阶段直接编辑；review 阶段一并审核 diff。 | 档 2（仅当目录已存在或本 feature 引入需要源码化的图） |
| **Bug patterns (`docs/bug-patterns/catalog.md`)** | 由 `hf-bug-patterns` 旁路触发 | 不强制每个 feature 更新。 | 档 2 |
| **Release notes / CHANGELOG** | closeout 阶段同步 | 档 0/1：`hf-finalize` 写入仓库根 `CHANGELOG.md`。档 2：`hf-finalize` 写入 `docs/release-notes/vX.Y.Z.md` 并在 `CHANGELOG.md` 加版本入口。 | `CHANGELOG.md` 档 0 起；`docs/release-notes/` 档 2 启用 |
| **顶层导航（`docs/index.md` 或仓库根 `README.md`）** | closeout 阶段同步 | 档 0/1：`hf-finalize` 更新仓库根 `README.md` 中的 active feature / 最近 closeout / ADR 索引行。档 2：同步 `docs/index.md`。 | `README.md` 档 0 起；`docs/index.md` 档 2 启用 |

### 设计阶段就直接改 `docs/` 的两类例外

- **ADR**：必须有稳定 ID 才能被 `design.md` 引用；如果延迟到 closeout 才分配编号，则评审期间引用就是"待定 ID"，会发生冲突或链接断裂。
- **源码化图（Structurizr DSL / PlantUML）**：图本身就是 review 的一部分，回退到 closeout 同步反而割裂评审。

其余长期资产**统一由 closeout 阶段同步**，理由：
- `docs/` 始终保持"已批准状态"，避免设计未通过前 `docs/` 已被改。
- 多 feature 并行时降低 `docs/` 冲突频率。
- review 阶段评审范围聚焦 `features/<NNN>/`，不必横跨两个目录。

### `hf-finalize` 的同步责任（按存在同步）

`closeout.md` 必须显式列出本次 closeout 同步到 `docs/` 的所有路径，作为 release/docs sync 证据。**同步范围按当前 `docs/` 实际存在的子目录决定**，不要求未启用的资产被新建；缺失项目区分两种情况：

- **本 feature 没有触发该资产类型变化**：在 *Updated Long-Term Assets* 中显式写 `N/A`，不算缺失。
- **本 feature 触发了该资产类型变化但目录尚未启用**：按 *Minimal `docs/` Tiers* 的"升级时机"判断是否在本 closeout 顺带启用对应目录。例：本 feature 引入第一个生产部署运维点，应在 closeout 时新建 `docs/runbooks/` 并写入 runbook。

```markdown
## Release / Docs Sync

- Release Notes Path: `CHANGELOG.md` v1.5.0 入口（档 0/1）
                      或 `docs/release-notes/v1.5.0.md`（档 2）
- Updated Long-Term Assets:
  - `docs/architecture.md`（5. 关键运行时交互节，新增 RateLimiter 路径） / 或 `docs/arc42/05_building_block_view.md`（档 2）
  - `docs/arc42/12_glossary.md` 或 `docs/architecture.md` 术语表节（新增术语：token bucket）
  - `docs/runbooks/rate-limiter.md`（新建；本 closeout 顺带启用 runbooks 目录）
  - `docs/adr/0042-introduce-rate-limiter.md`（status: proposed → accepted）
  - `docs/slo/`：N/A（本 feature 未变 SLO）
  - `docs/postmortems/`：N/A（无事故）
- Index Updated: 仓库根 `README.md` 的 active feature 行（档 0/1）
                 或 `docs/index.md`（档 2）
```

判 `blocked` 的条件收紧为：

- 本 feature 触发了某类长期资产变化（例如新增模块 / 新增运维点 / 新增 SLO），但 closeout 既未同步现存目录，也未在合理升级时机启用新目录；
- 必需同步项（`docs/adr/` 状态翻转、`CHANGELOG.md`、`README.md`/`docs/index.md` 中的 active feature 状态）缺失。

未启用的可选资产（如档 2 中尚未触发的 `docs/slo/` / `docs/postmortems/`）不构成 `blocked` 依据。

## API 契约的归宿

- 当代码侧已存在 canonical 契约目录（如 `api/openapi.yaml`），feature 目录的 `contracts/` 只放本次变更的 draft / diff，作为评审与历史证据；canonical 契约随实现 commit 一起更新。
- 当代码侧不存在 canonical 契约目录，本约定**不强制**在 `docs/contracts/` 立 canonical 目录。契约就在 feature 目录内，随实现进入代码。
- 不允许 canonical 契约只存在于 feature 目录里——这会导致"找当前生效契约要去翻最近哪个 feature 改过它"。

## Discipline Without Schema / CI

本约定不引入 frontmatter schema、JSON schema 或 CI lint。维持纪律的手段是：

1. **模板就是最强的强制力**。`skills/templates/` 提供的模板（spec、design、tasks、review、closeout pack 等）保持完整与最新；agent 与人创建工件时复制模板，骨架自然一致。本约定**不**把模板搬到 `docs/templates/`，模板继续以 skill 内置形式分发，项目可在 `AGENTS.md` 中声明等价覆盖路径（沿用 HF 现有覆盖语义）。
2. **`README.md` 作为 feature 总览页**强制要求列出各阶段工件路径与状态，肉眼一看即可发现缺件。
3. **reviewer subagent 的 checklist 作为运行时强制**。各 `hf-*-review` 与 `hf-*-gate` skill 中的 *Practical Checklist* 与 *Verification* 段，必须由 reviewer 逐条勾对实际工件。
4. **`docs/index.md` 作为长期资产 + active feature 索引**，由 `hf-finalize` 在 closeout 时更新。
5. **commit message 规范**：建议 commit message 显式 reference feature 目录（例如 `Refs: features/003-rate-limiting`），让 `git log` 自然成为过程证据流。

承认的剩余风险：当 feature 数到 30+、ADR 数到 50+ 时，纯靠纪律会出现散文式漂移（链接失效、ADR 状态过期、glossary 漏更新）。届时再考虑加一个超轻的 `scripts/sdd-check.sh`（不是 CI、不是 schema，就是 shell 扫一遍 broken link / orphan ADR / closeout 缺件）。**不**提前引入。

## 与 HarnessFlow 现有默认路径的映射

`skills/docs/hf-workflow-shared-conventions.md` 中的 *Default 逻辑工件布局* 表格描述的是 HF 出厂默认路径。本约定通过 `AGENTS.md` 声明覆盖，使其按下表落地：

| 逻辑工件 | HF 默认 | 本约定路径 |
|---|---|---|
| requirement spec | `docs/specs/YYYY-MM-DD-<topic>-srs.md` | `features/NNN-<slug>/spec.md` |
| design doc | `docs/designs/YYYY-MM-DD-<topic>-design.md` | `features/NNN-<slug>/design.md` |
| ui design doc | （未指定） | `features/NNN-<slug>/ui-design.md` |
| task plan | `docs/tasks/YYYY-MM-DD-<topic>-tasks.md` | `features/NNN-<slug>/tasks.md` |
| task board | `docs/tasks/YYYY-MM-DD-<topic>-task-board.md` | `features/NNN-<slug>/task-board.md` |
| progress state | 仓库根 `task-progress.md` | `features/NNN-<slug>/progress.md`（**仓库根不再保留全局 progress 文件**） |
| reviews | `docs/reviews/` | `features/NNN-<slug>/reviews/<kind>-...md` |
| approvals | `docs/approvals/` | `features/NNN-<slug>/approvals/<kind>-...md` |
| verification | `docs/verification/` | `features/NNN-<slug>/verification/<kind>-...md` |
| ADR | （HF 暗含、未集中） | `docs/adr/NNNN-<slug>.md`（仓库级 pool） |
| closeout pack | `docs/finalize/`（按模板） | `features/NNN-<slug>/closeout.md` |
| release notes | `RELEASE_NOTES.md` | `CHANGELOG.md` + `docs/release-notes/vX.Y.Z.md` |
| 长期架构图景 | （未指定） | `docs/arc42/` + `docs/diagrams/` |
| 项目原则锚点 | （未指定，由 `AGENTS.md` 声明） | `docs/principles/` |
| 运维资产 | （未指定） | `docs/runbooks/` / `docs/slo/` / `docs/postmortems/` |

`AGENTS.md` 中至少应声明：

```text
- requirement spec path: features/<active>/spec.md
- design doc path: features/<active>/design.md
- task plan path: features/<active>/tasks.md
- progress path: features/<active>/progress.md
- review path: features/<active>/reviews/
- approval path: features/<active>/approvals/
- verification path: features/<active>/verification/
- closeout pack path: features/<active>/closeout.md
- adr pool path: docs/adr/
- design principles path: docs/principles/
- arc42 path: docs/arc42/
- runbooks path: docs/runbooks/
- release notes path: docs/release-notes/
- changelog path: CHANGELOG.md
```

`<active>` 在每个 workflow 周期开始时由 router 锁定为具体 feature 目录名。

## Lifecycle 总览

```text
[ 新 feature 启动 ]
  └─> 在 features/NNN-<slug>/ 下创建 README.md + spec.md（来自 skills/templates/）
       │
       ▼
[ specify ] ──> features/<active>/spec.md（草稿）
       │           reviews/spec-review-YYYY-MM-DD.md
       │           approvals/spec-approval-YYYY-MM-DD.md
       ▼
[ design ] ───> features/<active>/design.md（草稿）
       │           docs/adr/NNNN-...md（status: proposed → accepted）
       │           docs/diagrams/...（如需）
       │           reviews/design-review-YYYY-MM-DD.md
       │           approvals/design-approval-YYYY-MM-DD.md
       ▼
[ tasks ] ────> features/<active>/tasks.md
       │           reviews/tasks-review-...md
       │           approvals/tasks-approval-...md
       ▼
[ test-driven-dev / reviews / gates ]
       │           features/<active>/reviews/code-review-task-NNN.md
       │           features/<active>/evidence/...
       │           features/<active>/verification/regression-...md
       │           features/<active>/verification/completion-...md
       ▼
[ finalize ] ─> features/<active>/closeout.md
                  docs/arc42/...（同步变更）
                  docs/runbooks/...（同步/新增）
                  docs/release-notes/vX.Y.Z.md
                  CHANGELOG.md
                  docs/index.md（更新 active feature / 最近 closeout）
```

closeout 后 `features/NNN-<slug>/` 进入只读状态，仅在以下情况修改 `README.md`：

- 该 feature 的 ADR 被新 feature supersede，加一行 backlink；
- 出 hotfix 复用了该 feature 的边界，加 incident 链接。

## Red Flags

- 在 `features/<NNN>/` 内内联 ADR 全文，而不是引用 `docs/adr/NNNN-...md`。
- closeout 时只写 `closeout.md`，未同步 `docs/` 中已存在的相关长期资产载体。
- 把 closeout 后的 feature 移动到 `features/archived/`，破坏其它工件的反向引用。
- 仓库根又出现了全局 `task-progress.md`（应只在 feature 目录内）。
- ADR 因被 supersede 而被删除或重新编号。
- canonical API 契约只存在于某个 feature 目录里。
- review / approval / verification 的散文记录散落到 `docs/reviews/` 等仓库级目录而不是 feature 目录内。
- feature 目录命名只用 slug 不带 `NNN-` 顺序号，导致顺序难以排序。
- 没有 `docs/principles/sdd-artifact-layout.md` 与 `docs/adr/` 就声称已采用本约定（这两者属于档 0，是任何档位下都不可省的最小集）。
- 同时存在 `docs/architecture.md` 与 `docs/arc42/`（架构概述应二选一；档 1→档 2 升级时应明确把单文件拆解到 arc42 12 节后再删 `architecture.md`）。
- 没引入 `docs/runbooks/` / `docs/slo/` / `docs/postmortems/` 等档 2 资产时，`hf-finalize` 仍因这些目录缺失判 `blocked`（应改为 `N/A`）。

## Verification

档 0 必须满足：

- [ ] `docs/principles/sdd-artifact-layout.md` 已存在（本文件本身）
- [ ] `docs/adr/` 已存在，至少含 `0001-record-architecture-decisions.md`
- [ ] 仓库根 `README.md` 至少列出当前 active feature + 系统一句话定位 + ADR 索引链接
- [ ] 仓库根 `CHANGELOG.md` 已存在（Keep a Changelog 风格）
- [ ] 每个 active feature 在 `features/` 下有自包含目录，且目录名形如 `NNN-kebab-slug/`
- [ ] feature 目录内 `README.md` / `spec.md` / `design.md` / `tasks.md` / `progress.md` 均存在
- [ ] feature 目录内 `reviews/` / `approvals/` / `verification/` 已收口，文件命名遵循 `<kind>-<scope>-YYYY-MM-DD.md`
- [ ] 设计阶段引用的所有 ADR 已落到 `docs/adr/NNNN-...md`，状态字段已写
- [ ] closeout 后 `closeout.md` 已写，且 *Release / Docs Sync* 区块按"按存在同步"列出实际同步路径与 `N/A` 项
- [ ] 仓库根没有遗留全局 `task-progress.md`
- [ ] `AGENTS.md` 已声明本约定要求的路径覆盖

档 1 增量满足：

- [ ] `docs/architecture.md` 已存在（哪怕只是一页骨架）
- [ ] `hf-finalize` 在 closeout 时同步 `docs/architecture.md` 的相关节（如本 feature 改变了架构图景）

档 2 按启用资产增量满足：

- [ ] 已启用的 `docs/arc42/` / `docs/diagrams/` / `docs/runbooks/` / `docs/slo/` / `docs/postmortems/` / `docs/release-notes/` / `docs/bug-patterns/` / `docs/insights/` / `docs/index.md` 各自的同步语义在 closeout 中体现
- [ ] 启用 `docs/arc42/` 时，已删除（或显式弃用）`docs/architecture.md`

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

## `docs/` 下放什么（项目长期资产）

```text
docs/
  index.md                     # 顶层导航（手工维护）
  principles/                  # 项目原则 / "soul docs" / constitution
    architecture-principles.md
    product-principles.md
    coding-principles.md
    sdd-artifact-layout.md     # 本文件
  arc42/                       # 长期架构图景（arc42 12 节）
    01_introduction_and_goals.md
    ...
    10_quality_requirements.md
    12_glossary.md
  adr/                         # 架构决策日志（仓库级 pool）
    0001-record-architecture-decisions.md
    0042-introduce-rate-limiter.md
  diagrams/                    # 源码化的图
    structurizr/
      workspace.dsl
    plantuml/
  runbooks/                    # 运维手册
  slo/                         # 可靠性指标
  postmortems/                 # 事故复盘
  release-notes/               # 用户可见变化（按版本一文件）
    v1.4.0.md
    v1.5.0.md
  bug-patterns/                # hf-bug-patterns 沉淀
    catalog.md
```

约束：

- `docs/principles/` 是 `hf-design` 中"项目级设计原则锚点"的默认落点。`AGENTS.md` 中可写明 `design principles path: docs/principles/`。
- `docs/adr/` 是 ADR 的**唯一权威池**，仓库级顺序号、不复用、不按 feature 分散。
- `docs/arc42/` 描述的是"系统当前状态"，不是"某次变更"。一次 feature 完成后，arc42 的相关节应被同步更新（同步规则见 *Promotion Rules*）。
- `CHANGELOG.md` 仍放仓库根（Keep a Changelog 惯例）；`docs/release-notes/vX.Y.Z.md` 写每个 release 的详细描述。
- `docs/index.md` 是手工维护的顶层导航，至少列出：当前 active feature、最近若干个 closeout 的 feature、ADR 编号最大值、当前 release。

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

- `CHANGELOG.md`：仓库根，Keep a Changelog 风格。
- `docs/release-notes/vX.Y.Z.md`：每个 release 一份详细描述。

## Promotion Rules（过程交付件 → 长期资产）

这是双根布局最容易出问题的地方：feature 显然会修改 ADR、改 arc42、加 glossary 项、加 runbook。本约定采用**混合模式**：

| 长期资产类型 | 修改时机 | 修改方式 |
|---|---|---|
| **ADR (`docs/adr/`)** | 设计阶段直接落到 `docs/adr/` | 起草时即分配 ADR ID，写入 `docs/adr/NNNN-...md`，状态 `proposed`；评审与 `设计真人确认` 通过后翻为 `accepted`。`design.md` 通过 ID 引用，不内联 ADR 全文。 |
| **arc42 (`docs/arc42/`)** | closeout 阶段同步 | feature 设计稿可在 `design.md` 中描述对架构图景的影响；`hf-finalize` 在 closeout 时把已批准变更应用到 `docs/arc42/` 对应节。 |
| **Glossary (`docs/arc42/12_glossary.md`)** | closeout 阶段同步 | feature spec / design 中引入的新术语，由 closeout 同步到 glossary。 |
| **Runbooks (`docs/runbooks/`)** | closeout 阶段同步 | feature 引入新运维关注点时，closeout 必须新增或更新对应 runbook。 |
| **SLO (`docs/slo/`)** | closeout 阶段同步 | feature 引入新 SLO 或修改既有 SLO 时同步。 |
| **Diagrams (`docs/diagrams/`)** | 设计阶段或 closeout 阶段 | 源码化图（Structurizr DSL / PlantUML）允许在设计阶段直接编辑；review 阶段一并审核 diff。 |
| **Bug patterns (`docs/bug-patterns/catalog.md`)** | 由 `hf-bug-patterns` 旁路触发 | 不强制每个 feature 更新。 |
| **Release notes / CHANGELOG** | closeout 阶段同步 | 由 `hf-finalize` 写入。 |

### 设计阶段就直接改 `docs/` 的两类例外

- **ADR**：必须有稳定 ID 才能被 `design.md` 引用；如果延迟到 closeout 才分配编号，则评审期间引用就是"待定 ID"，会发生冲突或链接断裂。
- **源码化图（Structurizr DSL / PlantUML）**：图本身就是 review 的一部分，回退到 closeout 同步反而割裂评审。

其余长期资产**统一由 closeout 阶段同步**，理由：
- `docs/` 始终保持"已批准状态"，避免设计未通过前 `docs/` 已被改。
- 多 feature 并行时降低 `docs/` 冲突频率。
- review 阶段评审范围聚焦 `features/<NNN>/`，不必横跨两个目录。

### `hf-finalize` 的同步责任

`closeout.md` 必须显式列出本次 closeout 同步到 `docs/` 的所有路径，作为 release/docs sync 证据：

```markdown
## Release / Docs Sync

- Release Notes Path: `docs/release-notes/v1.5.0.md`
- Updated Docs:
  - `docs/arc42/05_building_block_view.md`（新增 RateLimiter 模块）
  - `docs/arc42/12_glossary.md`（新增术语：token bucket）
  - `docs/runbooks/rate-limiter.md`（新建）
  - `docs/adr/0042-introduce-rate-limiter.md`（status: proposed → accepted）
- CHANGELOG: `CHANGELOG.md`（v1.5.0 入口）
```

如果同步项缺失，`hf-finalize` 应判 `blocked` 并回 `hf-workflow-router`。

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
- closeout 时只写 `closeout.md`，未同步 `docs/arc42/` / `docs/runbooks/` / release notes。
- 把 closeout 后的 feature 移动到 `features/archived/`，破坏其它工件的反向引用。
- 仓库根又出现了全局 `task-progress.md`（应只在 feature 目录内）。
- ADR 因被 supersede 而被删除或重新编号。
- canonical API 契约只存在于某个 feature 目录里。
- review / approval / verification 的散文记录散落到 `docs/reviews/` 等仓库级目录而不是 feature 目录内。
- feature 目录命名只用 slug 不带 `NNN-` 顺序号，导致顺序难以排序。

## Verification

- [ ] 每个 active feature 在 `features/` 下有自包含目录，且目录名形如 `NNN-kebab-slug/`
- [ ] feature 目录内 `README.md` / `spec.md` / `design.md` / `tasks.md` / `progress.md` 均存在
- [ ] feature 目录内 `reviews/` / `approvals/` / `verification/` 已收口，文件命名遵循 `<kind>-<scope>-YYYY-MM-DD.md`
- [ ] 设计阶段引用的所有 ADR 已落到 `docs/adr/NNNN-...md`，状态字段已写
- [ ] closeout 后 `closeout.md` 已写，且 *Release / Docs Sync* 区块列出实际同步到 `docs/` 的路径
- [ ] 仓库根没有遗留全局 `task-progress.md`
- [ ] `docs/index.md` 反映了当前 active feature 与最近 closeout
- [ ] `AGENTS.md` 已声明本约定要求的路径覆盖

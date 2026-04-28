# dev-flow (df) Artifact Layout

- 定位: 定义 `dev-flow`（简称 `df`）skills 在团队日常需求开发 / 问题修改中的工件组织、命名与生命周期。
- 关联:
  - 最高原则: `docs/df-principles/00 soul.md`
  - Skill-node 设计契约: `docs/df-principles/01 skill-node-define.md`
  - Skill 写作原则: `docs/df-principles/02 skill-anatomy.md`
  - Workflow 架构: `docs/df-principles/04 workflow-architecture.md`

## Purpose

本文回答：

> df workflow 产出的规格澄清、spec review、组件实现设计、AR 实现设计、测试证据、TDD 后测试有效性审查、代码检视记录应该放在哪里、叫什么、何时更新？

df 服务团队日常嵌入式软件开发，不做产品发现。项目是多仓库工程，各组件由不同团队维护，并分布在不同 git 仓库中。因此工件布局以**组件仓库**为边界：每个组件仓库有自己的 `docs/` 和 `features/`，二者同级。

## Core Principles

1. **组件仓库是工件边界。** 不假设存在一个覆盖所有组件的大 `docs/`；每个组件仓库维护自己的 `docs/` 和 `features/`。
2. **正式设计文档进 `docs/`。** 组件实现设计文档和 AR 实现设计文档需要进入组件仓库 `docs/`，并随代码一起 git 提交。
3. **过程文档进 `features/`。** df 开发过程中产生的澄清、评审、证据、检视、completion、closeout 等过程文档放到组件仓库 `features/<AR...>/`。
4. **AR 是最小开发单元。** 大多数过程工件默认围绕 AR 或问题修改单组织。
5. **追溯链不可断。** IR -> SR -> AR -> 组件设计 -> AR 设计 -> 代码 -> 测试 -> 测试有效性审查 -> 代码检视必须能回读。
6. **测试有效性审查独立保存。** TDD 中写出的测试不能天然视为有效，必须有独立 test-check record。

## Recommended Roots

以下结构位于**每个组件 git 仓库**内。**只有 `docs/component-design.md` 与 `docs/ar-designs/` 是 df 默认要求长期维护的资产**；`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md` 是**可选 / 按需启用**的子资产，团队没建立时缺失即缺失，不构成 df 节点的阻塞条件。

```text
<component-repo>/
  docs/
    component-design.md           # 必需（component-impact 触发时）
    ar-designs/                   # AR 工作项必需
      AR<id>-<slug>.md
    interfaces.md                 # 可选；项目启用了才有
    dependencies.md               # 可选
    runtime-behavior.md           # 可选

  features/
    AR<id>-<slug>/
    DTS<id>-<slug>/
```

| Root | 性质 | 内容 |
|---|---|---|
| `docs/` | 组件仓库长期资产 | 组件实现设计、AR 实现设计；可选的接口 / 依赖 / 运行时行为文档 |
| `features/<id>/` | 单次开发过程资产 | 单个 AR / DTS 的澄清、review、测试证据、检视、completion、closeout |

如果某组件仓库已有固定目录或团队 `AGENTS.md` 声明了等价路径，df skill 应**优先读取团队约定**；本文作为默认逻辑布局。跨组件 AR 应在每个受影响组件仓库内分别维护对应 `features/<id>/`，并在各自 `docs/` 中更新本组件相关的正式设计文档。

### Read-On-Presence

df skill 在读取上述 `docs/` 资产时遵循 **Read-On-Presence**：

- 必需资产（`docs/component-design.md`：在 component-impact / 修订组件级行为的 AR 与 DTS 中必需；`docs/ar-designs/AR<id>-<slug>.md`：在 AR 工作项 finalize 时必需）缺失 → 阻塞，回上游创建。
- 可选资产（`docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`、以及未来团队添加的其它子资产）缺失 → **不阻塞**；df 节点应跳过对应读取并按"项目当前未启用此资产"作为判断依据继续。
- closeout 时按 sync-on-presence：项目已启用的资产若本次触发变化必须同步；未启用的资产写 `N/A（项目未启用）`，不构成 blocked。
- 是否要在 closeout 时**新建**某个可选资产（例如本次 AR 第一次引入了运行时行为约定，team 决定开始维护 `docs/runtime-behavior.md`），由模块架构师 / 开发负责人决定，df 不自动创建未启用资产。

## Long-Lived Component Assets

```text
<component-repo>/
  docs/
    component-design.md           # 默认资产
    ar-designs/                   # 默认资产
      AR1234-short-title.md
    interfaces.md                 # 可选 / 按需启用
    dependencies.md               # 可选 / 按需启用
    runtime-behavior.md           # 可选 / 按需启用
```

### `component-design.md`（默认资产）

组件实现设计的默认位置。它描述组件，不描述单个 AR。该文件属于正式设计文档，需要进入组件仓库 `docs/` 并随代码 git 提交。

至少包含：

- 组件职责与非职责。
- SOA 服务 / 接口。
- 依赖组件。
- 数据模型和状态机。
- 并发、实时性、资源生命周期。
- 错误处理和降级策略。
- 配置项和编译条件。
- 对 AR 实现设计的约束。

> 接口 / 依赖 / 运行时行为的细节如果团队尚未拆出独立子文件，应直接归并到本文件相应章节；可选子资产仅在团队明确决定单独维护时才存在。

### `interfaces.md`（可选）

可选子资产。当团队决定把组件对外接口和服务契约从 `component-design.md` 中拆出独立文件维护时使用。适合记录：

- 服务名和接口。
- 输入输出。
- 错误码。
- 时序约束。
- 兼容性要求。

未启用时，相关内容应在 `component-design.md` 的 SOA 服务 / 接口章节中维护；df 不要求拆分。

### `dependencies.md`（可选）

可选子资产。当团队决定把组件依赖关系从 `component-design.md` 拆出独立文件维护时使用。适合记录：

- 内部组件依赖。
- 版本约束。
- 初始化 / shutdown 顺序。
- 风险和限制。

未启用时，相关内容应在 `component-design.md` 的依赖组件章节中维护。

### `runtime-behavior.md`（可选）

可选子资产。当团队决定把组件运行时行为约定从 `component-design.md` 拆出独立文件维护时使用。适合记录：

- 启动 / 关停顺序与状态。
- 调度 / 时序 / 节拍。
- 故障与恢复路径。

未启用时，相关内容应在 `component-design.md` 的并发 / 实时性 / 资源生命周期章节中维护。

### `docs/ar-designs/AR<id>-<slug>.md`

AR 实现设计的正式落点。它描述一个 AR 的代码层设计，不描述整个组件。该文件需要进入组件仓库 `docs/` 并随代码 git 提交。

至少包含：

- AR ID、SR link、所属组件。
- 设计目标和范围。
- 受影响文件 / 模块 / 接口。
- 数据结构和控制流。
- C / C++ 实现策略。
- 错误处理。
- 资源生命周期。
- 并发 / 实时性影响。
- 与组件实现设计的一致性说明。
- 测试设计章节。

## Work Item Assets

每个 AR 或问题修改在所属组件仓库的 `features/` 下建立一个过程目录。

```text
features/
  AR1234-short-title/
    README.md
    requirement.md
    ar-design-draft.md
    traceability.md
    implementation-log.md
    reviews/
      spec-review.md
      ar-design-review.md
      test-check.md
      code-review.md
    evidence/
      unit/
      integration/
    completion.md
    closeout.md
```

问题修改可以使用：

```text
features/
  DTS5678-short-title/
    reproduction.md
    root-cause.md
    fix-design.md
    ...
```

## Required Work Item Files

### `README.md`

工作单元入口。至少包含：

- Work item ID。
- 类型: `AR` / `DTS` / `CHANGE`。
- 所属组件。
- 关联 IR / SR / AR。
- 当前状态。
- 当前下一步。
- 关键工件链接。

### `requirement.md`

规格澄清记录。适合 `df-specify` 写入。

至少包含：

- 原始输入。
- IR / SR / AR 关系。
- 所属子系统和组件。
- 范围 / 非范围。
- 待决问题。
- 验收标准。

### `ar-design-draft.md`

AR 实现设计草稿或过程版本。正式 AR 实现设计应同步到 `docs/ar-designs/AR<id>-<slug>.md` 并 git 提交。

至少包含：

- AR ID、SR link、所属组件。
- 设计目标和范围。
- 受影响文件 / 模块 / 接口。
- 数据结构和控制流。
- C / C++ 实现策略。
- 错误处理。
- 资源生命周期。
- 并发 / 实时性影响。
- 与组件实现设计的一致性说明。
- 测试设计章节。

### 测试设计章节

测试设计不作为独立 `test-design.md` 文件管理，应作为 `ar-design-draft.md` 或正式 AR 实现设计的章节。

至少包含：

- 测试用例列表。
- 每个用例覆盖的 AR 行为。
- 预期结果。
- 测试层级: unit / integration / simulation。
- 需要 mock / stub / 仿真的说明。
- RED / GREEN 证据记录要求。

### `traceability.md`

追溯矩阵。

推荐列：

| IR | SR | AR | Design Section | Code / File | Test Case | Verification |
|---|---|---|---|---|---|---|

### `implementation-log.md`

实现日志。记录：

- 本轮修改摘要。
- 关键设计决策。
- RED / GREEN / REFACTOR 证据。
- 本地编译 / 单测 / 静态分析结果。
- 未解决风险。

### `reviews/`

默认记录：

- `ar-design-review.md`
- `test-check.md`
- `code-review.md`

review record 必须包含 verdict、findings、severity、下一步。

### `evidence/`

推荐子目录：

```text
evidence/
  unit/
  integration/
  static-analysis/
  build/
```

证据文件应记录：

- 命令或验证动作。
- 环境。
- 软件版本 / 包。
- 配置。
- 结果。
- 新鲜度锚点，例如 commit、build ID、包版本。
- 覆盖的风险或行为。

### `completion.md`

完成门禁记录。由 `df-completion-gate` 写入。

至少包含：

- 输入工件清单。
- 设计通过状态。
- TDD 后测试有效性审查状态。
- 代码检视状态。
- 测试证据。
- 完成 verdict。
- 下一步: `df-finalize` 或返工节点。

## Progress State

默认进度文件：

```text
features/<id>/progress.md
```

推荐字段：

| 字段 | 含义 |
|---|---|
| `Current Stage` | 当前 canonical `df-*` 节点 |
| `Work Item Type` | `AR` / `DTS` / `CHANGE` |
| `Work Item ID` | AR 或问题单编号 |
| `Owning Component` | 唯一所属组件 |
| `Related IR` | 原始需求编号，按需 |
| `Related SR` | 系统需求编号 |
| `Related AR` | 分配需求编号 |
| `Execution Mode` | `interactive` / `auto`，如团队允许 |
| `Pending Reviews And Gates` | 未完成 review / gate |
| `Next Action Or Recommended Skill` | 唯一 canonical 下一步 |

## Naming Rules

- Work item 目录使用 `features/AR<id>-<short-slug>` 或 `features/DTS<id>-<short-slug>`。
- 正式 AR 实现设计使用 `docs/ar-designs/AR<id>-<short-slug>.md`。
- review 文件使用 `<kind>-review.md` 或 `<kind>-review-YYYY-MM-DD.md`。
- evidence 文件使用 `<kind>-<scope>-YYYY-MM-DD.md`。
- 不把自由文本下一步写进 progress；只能写 canonical `df-*` 节点名。

## Promotion Rules

`features/<id>/` 中的过程内容按以下规则同步到 `docs/`：

- 组件实现设计新增或修订时，同步 `docs/component-design.md`。
- AR 实现设计通过相应 review 后，同步 `docs/ar-designs/AR<id>-<slug>.md`。
- 接口、依赖或运行时行为有正式变化时，按 sync-on-presence 同步：项目已启用 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md` 的，分别更新对应文件；尚未启用的，把变化合并进 `docs/component-design.md` 相应章节，**不**为单次变化强行新建可选子资产（是否启用由模块架构师 / 开发负责人决定）。

没有触发组件长期资产变化时，`features/<id>/closeout.md` 只需记录 `N/A`，不要无意义更新长期文档。但 AR 实现设计作为本次 AR 的正式设计文档，仍应在完成前进入 `docs/ar-designs/`。

## Red Flags

- AR 没有唯一所属组件。
- SR / AR 追溯关系不清却进入实现。
- AR 实现设计试图修改组件架构。
- 组件实现设计已过期但下游继续引用。
- 正式组件实现设计或 AR 实现设计只留在 `features/`，没有同步到 `docs/`。
- TDD 完成后缺少 `test-check.md`。
- completion gate 只引用聊天摘要。

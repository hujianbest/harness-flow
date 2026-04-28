# df Workflow Shared Conventions

本文档汇总 `df-*` skills 在团队日常需求开发 / 问题修改工作流中共享的约定。每个 df skill 通过本文档锚定相同的工件路径、字段名、handoff 字段和角色边界。

- 上位原则: `docs/df-principles/00 soul.md`
- Skill-node 设计契约: `docs/df-principles/01 skill-node-define.md`
- Skill 写作原则: `docs/df-principles/02 skill-anatomy.md`
- 工件管理约定: `docs/df-principles/03 artifact-layout.md`
- Workflow 架构: `docs/df-principles/04 workflow-architecture.md`

## 工件根目录

df 服务的项目是多组件多仓库工程。**工件边界以组件 git 仓库为单位**，本文中默认路径假设当前活跃 work item 所在的组件仓库为根。

```text
<component-repo>/
  docs/
    component-design.md
    interfaces.md
    dependencies.md
    runtime-behavior.md
    ar-designs/
      AR<id>-<slug>.md
  features/
    AR<id>-<slug>/
    DTS<id>-<slug>/
```

`features/<id>/` 是单次需求 / 问题修改的过程目录；`docs/` 是组件仓库的长期资产。任何与项目本地约定不一致的路径，由该项目 `AGENTS.md` 显式声明覆盖；df skill 必须**优先读取项目 `AGENTS.md` 声明的路径映射**，本文路径仅作为默认逻辑布局。

## Work Item 类型

| 类型 | 适用场景 | 默认目录 |
|---|---|---|
| `AR` | 需求开发（已分配给本组件的 AR） | `features/AR<id>-<slug>/` |
| `DTS` | 缺陷 / 问题修改单 | `features/DTS<id>-<slug>/` |
| `CHANGE` | 团队认可的轻量变更（非 AR / 非 DTS） | `features/CHANGE<id>-<slug>/` |

## Work Item 过程目录骨架

```text
features/AR<id>-<slug>/
  README.md                   # work item 入口与状态总览
  progress.md                 # canonical 状态字段
  requirement.md              # df-specify 写入：需求规格澄清
  ar-design-draft.md          # df-ar-design 写入：AR 实现设计草稿（含测试设计章节）
  traceability.md             # IR/SR/AR/Design/Code/Test 追溯矩阵
  implementation-log.md       # df-tdd-implementation 写入：RED/GREEN/REFACTOR 证据摘要
  reviews/
    spec-review.md
    component-design-review.md  # 仅在 component-impact route 出现
    ar-design-review.md
    test-check.md             # df-test-checker 写入
    code-review.md
  evidence/
    unit/
    integration/
    static-analysis/
    build/
  completion.md               # df-completion-gate 写入
  closeout.md                 # df-finalize 写入
```

DTS 目录可酌情合并 / 增加文件：

```text
features/DTS<id>-<slug>/
  README.md
  progress.md
  reproduction.md             # df-problem-fix 写入：复现路径
  root-cause.md               # df-problem-fix 写入：根因
  fix-design.md               # df-problem-fix 写入：最小修复边界
  ar-design-draft.md          # 若问题修改需要补 AR 实现设计
  ...                         # 其余同 AR 目录
```

## Canonical Progress 字段

`features/<id>/progress.md` 必须使用以下 canonical 字段名。`df-workflow-router` 与所有 leaf skill 都消费这些字段。

| 字段 | 含义 | 取值约束 |
|---|---|---|
| `Work Item Type` | `AR` / `DTS` / `CHANGE` | 必填 |
| `Work Item ID` | 例 `AR12345`、`DTS67890` | 必填 |
| `Owning Component` | 唯一所属组件名 | 必填 |
| `Related IR` | 上游 IR 编号 | 可空 |
| `Related SR` | 上游 SR 编号 | AR 工作项必填 |
| `Related AR` | 关联 AR 编号 | DTS 修改若涉及功能需求时填写 |
| `Workflow Profile` | `standard` / `component-impact` / `hotfix` / `lightweight` | 由 router 决定，下游不得自改 |
| `Execution Mode` | `interactive` / `auto` | 由 router 归一化，下游不得自改 |
| `Current Stage` | 当前 canonical `df-*` 节点 | 必填 |
| `Pending Reviews And Gates` | 待完成 review / gate | 列表 |
| `Next Action Or Recommended Skill` | 唯一 canonical `df-*` 节点名 | 不允许自由文本 |
| `Blockers` | 阻塞项摘要 | 可空 |
| `Last Updated` | 时间戳 | 必填 |

任何 df skill 完成节点工作时，**必须**用 canonical 字段名同步 `progress.md`，禁止把自由文本下一步写进 `Next Action Or Recommended Skill`。

## 角色 / 责任边界

| 角色 | 拍板权 | df 行为 |
|---|---|---|
| 模块架构师 | 组件边界、SOA 接口、组件实现设计、跨组件影响 | df 工程化执行 + 提示阻塞，不替架构师决定 |
| 开发负责人 / 需求负责人 | AR 是否进入开发、范围边界、SR/IR/AR 追溯 | df 提供澄清 + 待决问题列表 |
| 开发人员 | AR 实现设计、代码、单测、修复说明 | df 提供模板执行 + 证据收集 |
| df | 不拍板任何专业判断 | 把判断落成可执行 / 可验证 / 可追溯的工程过程 |

## Canonical 节点名

```text
using-df-workflow            # 公开入口（不写入 handoff）
df-workflow-router           # 运行时编排
df-specify
df-spec-review
df-component-design          # 仅 component-impact route
df-component-design-review   # 仅 component-impact route
df-ar-design
df-ar-design-review
df-tdd-implementation
df-test-checker
df-code-review
df-completion-gate
df-finalize
df-problem-fix               # 仅 hotfix / DTS route
```

## Handoff 摘要最小字段

每个 df leaf skill 完成时返回的结构化 handoff 至少包含：

- `current_node`：刚完成的节点（canonical 名称）
- `work_item_id`：例 `AR12345`、`DTS67890`
- `owning_component`：唯一组件名
- `result` / `verdict`：节点专属结论（如 review verdict、gate 结论）
- `artifact_paths`：本节点产出 / 修订的文件路径列表
- `record_path`：review / gate / verification 主记录路径（如适用）
- `evidence_summary`：本轮证据摘要
- `traceability_links`：IR / SR / AR / 设计 / 代码 / 测试的链接
- `blockers`：未闭合的阻塞项
- `next_action_or_recommended_skill`：唯一 canonical `df-*` 节点名
- `reroute_via_router`：`true` / `false`，下一步无法唯一映射时为 `true` 并指向 `df-workflow-router`

`next_action_or_recommended_skill` **不得**写入 `using-df-workflow`，**不得**写入自由文本。

## Workflow Profile 与下游合法节点

| Profile | 触发信号 | 合法节点路径 |
|---|---|---|
| `standard` | 既有组件 AR 增量、组件设计稳定 | specify → spec-review → ar-design → ar-design-review → tdd-implementation → test-checker → code-review → completion-gate → finalize |
| `component-impact` | 新增组件 / 修改 SOA 接口 / 修改组件职责或依赖 / 组件设计缺失或过期 | specify → spec-review → component-design → component-design-review → ar-design → ar-design-review → tdd-implementation → test-checker → code-review → completion-gate → finalize |
| `hotfix` | 紧急 DTS / 已上线缺陷 | problem-fix → (可选) ar-design → ar-design-review → tdd-implementation → test-checker → code-review → completion-gate → finalize |
| `lightweight` | 极小、低风险、纯局部修改 | specify（极简）→ spec-review → ar-design → ar-design-review → tdd-implementation → test-checker → code-review → completion-gate → finalize |

`lightweight` **不允许跳过** test-checker 与 code-review；只能压缩文档量，不能压缩证据。Profile 由 `df-workflow-router` 决定，下游 leaf skill 不得自行降级。

## Hard Stops（任一命中必须停下）

- 需求输入不清且涉及方向 / 范围 / 验收 → 停在 `df-specify` 或回需求负责人
- IR / SR / AR 追溯关系冲突 → 阻塞
- AR 不属于唯一组件 → 阻塞
- 缺组件实现设计但本次修改影响组件边界 → 进 `df-component-design`
- AR 实现设计未含测试设计章节 → 回 `df-ar-design`
- TDD 完成后测试用例未经 `df-test-checker` 审查 → 不得进入 `df-code-review`
- 代码修改破坏 SOA 边界或引入未解释跨组件依赖 → review 阻塞
- 存在未解释的 critical 静态分析 / 编译告警 / 编码规范违反 → completion 阻塞
- review / gate 结论无法唯一映射下一步 → 回 `df-workflow-router`

## 测试设计是 AR 实现设计的章节

df 不维护独立的 `test-design.md`。测试用例、覆盖目标、预期 I/O、mock / stub / 仿真说明、RED / GREEN 证据要求都作为 `ar-design-draft.md`（过程版）和 `docs/ar-designs/AR<id>-<slug>.md`（正式版）的章节存在。

`df-tdd-implementation` 必须以 AR 实现设计中的测试设计章节为驱动，不得跳过。

## Promotion Rules（过程目录 → 长期资产）

| 触发 | 同步动作 |
|---|---|
| 组件实现设计新增 / 修订并通过 review | 写入 / 更新 `docs/component-design.md` |
| AR 实现设计通过 review | 写入 `docs/ar-designs/AR<id>-<slug>.md` |
| 接口 / 依赖 / 运行时行为有正式变化 | 同步 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md` |
| 本次修改未触发任何长期资产变化 | `closeout.md` 中 `Long-Term Assets Sync` 写 `N/A` |

未触发时不要无意义重写长期文档；触发时不得只留在 `features/` 而不进入 `docs/`。

## Static / Dynamic 质量证据

| 类别 | 默认落点 |
|---|---|
| 单元测试运行结果 | `features/<id>/evidence/unit/` |
| 集成 / 仿真测试 | `features/<id>/evidence/integration/` |
| 静态分析结果 | `features/<id>/evidence/static-analysis/` |
| 编译 / build 输出 | `features/<id>/evidence/build/` |

所有证据文件必须包含：命令、环境、版本 / 包、配置、结果、新鲜度锚点（commit / build ID）。

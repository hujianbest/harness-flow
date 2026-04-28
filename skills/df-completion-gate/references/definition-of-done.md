# df Definition of Done

> 配套 `df-completion-gate/SKILL.md`。规定 df 单 AR / DTS work item 在不同 profile 下的完成定义。

## 通用 DoD（任何 profile 都必须满足）

1. requirement.md 存在；spec-review verdict = `通过`
2. AR 实现设计存在并通过 ar-design-review；测试设计章节完整
3. C / C++ 代码改动可定位（diff 可读）
4. 实现交接块 + Refactor Note 完整（Hat Discipline / In-task Cleanups / Architectural Conformance / Documented Debt / Escalation Triggers / Static Analysis Evidence）
5. test-check verdict = `通过`
6. code-review verdict = `通过`
7. 本轮验证命令全部成功执行；退出码、摘要、新鲜度锚点齐全
8. evidence/{unit,static-analysis,build}/ 含本轮 fresh evidence
9. traceability.md 全链路（IR / SR / AR / 设计 / 代码 / 测试 / 验证）已填到本节点对应行
10. 嵌入式风险（内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI / SOA 边界）无未解释 critical 项
11. critical 静态分析 / 编译告警 / 编码规范违反已闭环（修 / 解释 / 抑制并附理由）

## Profile-Specific 加项

### `standard`

通用 DoD + 无额外加项。

### `component-impact`

通用 DoD + 以下：

- component-design-review verdict = `通过`
- 模块架构师 sign-off 已记录
- `docs/component-design.md`（以及必要的 `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`）的同步已规划，由 `df-finalize` 完成同步
- 跨组件影响（若有）：受影响组件的 work item 状态已显式说明（已开 / 未开 / 同步关闭）

### `hotfix`

通用 DoD 中 1-2 项可改为：

- 不必有完整 requirement.md，但必须有 reproduction.md + root-cause.md + fix-design.md
- AR 实现设计可被 fix-design.md 替代（仍需含测试设计章节或与现有 AR 设计的差异说明）
- 其余项目（test-check / code-review / fresh evidence / 嵌入式风险审计 / 静态分析）**全部保留**

紧急不等于绕过；hotfix 压缩文档量，不压缩证据。

### `lightweight`

与 `standard` 相同的 DoD 集合，证据要求**不**降低。

允许压缩文档量：

- requirement.md 可极简（核心 row 可少）
- ar-design-draft.md 可极简，但仍需含测试设计章节
- evidence 可只保留本轮真实跑过的最少必要文件

不允许压缩：test-check / code-review verdict、fresh evidence、嵌入式风险 audit。

## 嵌入式风险审计字段

`completion.md` 的 Quality Risk Audit 段必须显式列出以下维度的状态：

| 维度 | 状态选项 |
|---|---|
| 内存（边界 / 池化 / 栈 / 生命周期） | `clean` / `documented-debt` / `critical-open` |
| 并发（中断 / 锁 / 临界区 / 竞态） | 同上 |
| 实时性（latency / deadline / 调度） | 同上 |
| 资源生命周期（句柄 / 文件 / 缓冲区） | 同上 |
| 错误处理（输入校验 / 错误码 / 降级） | 同上 |
| ABI / API 兼容 | 同上 |
| SOA 边界 / 跨组件依赖 | 同上 |

`critical-open` 任一维度命中 → completion `阻塞`。

`documented-debt` 项必须在 `Documented Debt` 中可定位，并有处理计划（可在 closeout 中保留）。

## Verdict 决策

| 条件 | conclusion | 下一步 |
|---|---|---|
| 通用 DoD + Profile 加项均满足，无 critical-open，本轮验证全绿 | `通过` | `df-finalize` |
| 任一项缺失但可在 1-2 轮回修内补齐 | `需修改` | `df-tdd-implementation` |
| 工具链 / 环境问题阻塞验证 | `阻塞` | `df-completion-gate`（恢复后重审） |
| profile / route 冲突 / 跨组件协调缺失 / 实质修改组件边界 | `阻塞`（workflow） + `reroute_via_router=true` | `df-workflow-router` |

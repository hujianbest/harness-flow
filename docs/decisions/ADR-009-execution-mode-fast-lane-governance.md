# ADR-009 — Execution Mode Fast Lane Governance（D3 + D4 reconciliation）

- 状态: accepted（2026-05-13，架构师本会话拍板 D3 = A + D4 = A，并显式说明"auto mode 完成中间不要停下来"）
- 日期: 2026-05-13
- Feature: `features/002-omo-inspired-v0.6/`（v0.6 落地 `hf-ultrawork` skill）
- 决策者: 架构师（user）拍板 D3 + D4；cursor cloud agent 落 ADR
- 关联 ADR:
  - ADR-008（同会话）—— 路线图与 D3 / D4 / D6 / D7 项的范围锚点
  - ADR-002 D8 / `hf-workflow-router` execution-mode preference 既有约定
- 关联 soul / principles:
  - **`docs/principles/soul.md`** —— 第 1 条硬纪律"方向、取舍、标准不清时，默认是停下来澄清"；本 ADR 化解 D3 + D4 与该硬纪律的张力
  - `using-hf-workflow/SKILL.md` 步骤 3：Execution Mode 偏好提取已有
  - `hf-workflow-router/references/workflow-shared-conventions.md`：execution-mode 既有口径

## 1. Context

OMO 的 manifesto 主张 **"Human Intervention is a Failure Signal"**：把人接管视为系统失败信号，对应实现包括 `todo-continuation-enforcer`（idle 时把 agent 拽回来继续干）+ `ralph-loop`（自我引用循环不到 100% 不停）+ `keyword-detector` 识别 `ulw` / `ultrawork` 关键词激活模式。

HF 的 `docs/principles/soul.md` 第 1 条硬纪律相反：**"方向、取舍、标准不清时，默认是停下来澄清，而不是选一个看起来合理的方向继续推进"**。

2026-05-13 架构师拍板：

- **D3 = A**：引入 Boulder Loop / Todo Enforcer，HF 也变成"不做完不停"
- **D4 = A**：提供 `ultrawork` fast lane（架构师显式 opt-in 时跳过部分中间确认）
- 额外约束："auto mode 完成，中间不要停下来"

D3 + D4 与 soul.md 第 1 条直接张力。本 ADR 化解张力：把 D3 + D4 治理为"架构师显式 opt-in 的 fast lane"，**不是默认行为**，且 **Fagan author/reviewer 分离 + 硬门禁 verdict 不可绕过**。

## 2. Decision

### D1：D3 + D4 永远不是默认行为，必须由架构师 explicit opt-in

**决策**：HF 默认仍走 standard execution mode（每个节点结束后由 router 决定下一步、需要 approval 时停下抛回用户）。fast lane 行为只在以下任一条件命中时启用：

- 架构师在会话中显式说出 `auto mode` / `ultrawork` / `ulw` / `自动执行` / `不用等我确认` / `不要停下来` / `自动跑完` 等关键词
- `features/<active>/README.md` Metadata 段写了 `Execution Mode: auto` 或 `Execution Mode: ultrawork`
- `using-hf-workflow` 步骤 3 把上述 Execution Mode preference 解析出来并随 handoff 带到下游

**禁止默认开启**：HF 仓库自身的 `using-hf-workflow/SKILL.md` 第 3 步**不**默认假设 `auto mode`；缺省必须仍是 `standard`。

**理由**：
- soul.md 第 1 条 + 第 23 行"用户是架构师"组合起来的语义是：**架构师有权改变标准；HF 不替架构师改标准**。架构师 explicit opt-in 即是改了"什么时候停"的标准
- 不 explicit opt-in 时按 standard 行为，避免新用户被默认 fast lane 误伤

**Reversibility**：高（关闭 fast lane 只需在会话中说"恢复 standard mode"或编辑 `features/<f>/README.md` 的 Metadata 段）。

### D2：fast lane **永远不能绕过** Fagan author/reviewer 分离 + 硬门禁 verdict

**决策**：fast lane 只压缩"中间状态确认"，**不压缩**：

| 不可压缩的项 | 原因 |
|---|---|
| `hf-spec-review` / `hf-design-review` / `hf-ui-review` / `hf-tasks-review` / `hf-test-review` / `hf-code-review` / `hf-traceability-review` 8 个 Fagan review 节点 | author ≠ reviewer 是工程纪律的根；fast lane 不能让作者自审 |
| `hf-regression-gate` / `hf-doc-freshness-gate` / `hf-completion-gate` 3 个 gate verdict | gate 是"证据是否足以推进"的独立判断，fast lane 不能绕过 |
| `hf-finalize` 的 closeout pack 完整性（含 closeout HTML companion） | closeout 是 PMBOK-style handoff，fast lane 不减项 |
| spec / design / tasks **approval step**（`needs_human_confirmation=true`） | 架构师在 explicit opt-in 时已把"我确认"前置，approval step 改为"自动 APPROVED"是允许的；但 approval 工件本身**必须**写入磁盘 |
| 任何 `Hard Gates` 段落里的"方向 / 取舍 / 标准不清必须停下抛回用户"条款 | 这是 soul.md 第 1 条的直接落点，fast lane 不豁免 |

**fast lane 实际可压缩的项**：
- 节点之间的"是否继续到下一节点"的逐次确认（router 在 explicit opt-in 时直接走 canonical next action，不再询问）
- spec / design / tasks 的 approval step 从"等待用户手动 APPROVED"改为"自动 APPROVED 并写工件，标注由 architect explicit opt-in 触发"
- review 节点的 `verdict: 通过` 后的"要不要进 approval step"的确认
- `hf-test-driven-dev` 单 task 内 RED → GREEN → REFACTOR 各阶段之间的"是否进入下一阶段"的确认

**理由**：
- 架构师 explicit opt-in 解决的是"我已经知道我要什么，不要在每一步问我"，**不解决** "我不需要质量证据"
- Fagan + gate 是 HF 不可让步的工程纪律（soul.md 第 2 条 / 第 4 条）；ultrawork 不能让 HF 蜕化为"看起来很快但没有可回读证据"

**Reversibility**：低（fast lane 任何阶段都不允许跳过这些项；即便架构师在会话中说"跳过 review"也不能执行——必须先关闭 fast lane 切回 standard mode 再走流程）。

### D3：引入 `hf-ultrawork` skill 作为 fast lane 的承载节点

**决策**：v0.6 新增 `skills/hf-ultrawork/SKILL.md`，由 `using-hf-workflow` 在识别到 architect explicit opt-in 时 direct invoke。`hf-ultrawork` 的核心职责：

1. **声明 fast lane 边界**：在 SKILL.md 顶部用 `Hard Gates` 段写清"哪些项可压缩 / 哪些项绝对不可压缩"（即 D2 表格）
2. **Boulder loop 触发**：发现节点输出含未完成 todo 时（task 内的 step / feature 内的 task 队列），不询问直接驱动下一项
3. **Todo continuation enforcer 等价**：在 fast lane 进行中检测到 host agent 出现 idle / 假装完成 / 跳步信号时，直接重新 dispatch
4. **Escalation boundary**：命中以下任一条件时**强制停下抛回架构师**——这是 fast lane 的 hard escape：
   - 任一节点的 `Hard Gates` 命中"方向 / 取舍 / 标准不清"
   - 任一 review verdict = `阻塞`
   - 任一 gate verdict = FAIL
   - `hf-wisdom-notebook` 的 `problems.md` 出现新增 status=open 项
   - 连续 3 次同一节点 rewrite loop 仍未通过
   - 架构师在会话中说"停 / 暂停 / 等等 / hold on / wait"

**`hf-ultrawork` 不替代任何现有节点**：它只在节点之间的"是否继续"的判断点上接管决策权（架构师已 explicit opt-in 的前提下），不修改任何节点内的工作流。

**Slash 命令**：v0.6 **不**新增 `/ultrawork` 命令。原因：
- `/hf` 默认入口已经会经过 `using-hf-workflow`，而 `using-hf-workflow` 已经识别 `auto mode` / `ultrawork` 关键词
- 新增 `/ultrawork` 命令会与 `/hf` 默认入口竞争，且容易被误解为"绕过 HF workflow"

**Reversibility**：高（`hf-ultrawork` 是新 skill，删除即可恢复 standard mode）。

### D4：fast lane 的所有自动决策必须留 audit trail

**决策**：`hf-ultrawork` 在 fast lane 中代替架构师做的每一项决策（自动 APPROVED / 自动选 canonical next action / 自动重新 dispatch / Boulder loop 触发等），都必须写入 `features/<active>/progress.md` 的"Fast Lane Decisions"段（v0.6 在 progress.md schema 中新增此段）。

**Schema**：

```markdown
## Fast Lane Decisions

| 时间 | 节点 | 决策类型 | 决策内容 | 触发条件 | escape 是否启用 |
|---|---|---|---|---|---|
| 2026-05-13T10:32Z | hf-spec-review → hf-design | auto-approve | spec approval 自动 APPROVED | architect explicit `auto mode` (会话原话: "auto mode 完成") | no |
```

**理由**：
- soul.md 第 3 条"所有交付物必须可回读、可恢复"
- 架构师在事后审计 fast lane 行为时必须能从工件恢复"哪些节点是我点的、哪些是 ultrawork 自动点的"
- escape 列让架构师能快速定位 fast lane 自己识别到的需要人介入的边界

**Reversibility**：高（progress.md 增加一段，向前兼容）。

### D5：fast lane 与现有 `Execution Mode preference` 的合并

**决策**：v0.6 之前 HF 的 `using-hf-workflow/SKILL.md` 步骤 3 已经识别 `auto mode` 等关键词作为 Execution Mode preference 并随 handoff 带给下游，但现有口径**只**作为下游 skill 的"行为偏好提示"，没有定义具体压缩边界。

v0.6 起：
- `using-hf-workflow` 步骤 3 的 Execution Mode preference 解析逻辑保持不变
- 解析出 `auto mode` / `ultrawork` 后，`using-hf-workflow` 的 step 5（entry bias）新增一行：**Execution Mode = auto 且当前不在 review/gate 节点 → direct invoke `hf-ultrawork`**
- `hf-ultrawork` 接管后续 router 的"是否继续"决策；router 自身仍然是 authoritative 的下一节点选择者，`hf-ultrawork` 只在"router 选完下一节点后，是否要等用户确认才进入"这个判断点接管

**理由**：避免 fast lane 与 router 双层决策互相覆盖；router 仍是节点选择权威，`hf-ultrawork` 只是"决策点之间的自动推进器"。

**Reversibility**：高（`using-hf-workflow` step 5 新增一行，向前兼容）。

## 3. Consequences

**好的**：
- 架构师在 explicit opt-in 时获得"中间不停"的体验，与 OMO ultrawork 等价
- soul.md 第 1 条硬纪律的语义被精确化：默认仍是"停下抛回"，opt-in 时由架构师改了标准
- Fagan + gate 不可绕过，HF 不会蜕化为"看起来很快但没证据"
- 所有 fast lane 决策有 audit trail，可回读 / 可恢复

**坏的 / 风险**：
- 架构师可能滥用 fast lane（在尚未充分理解 HF 工作流时就 opt-in），需要 `hf-ultrawork/SKILL.md` 的 `When to Use` 段明确警示"首次使用 HF 不建议直接 fast lane"
- fast lane 进行中如果架构师中途想停，必须用明确关键词（"停 / 暂停 / wait"等），否则 `hf-ultrawork` 不会主动让出
- progress.md 的 Fast Lane Decisions 段会显著增长，长 feature 时需要 v0.6 评估是否分文件（如 `progress.fast-lane.md`）

**中性**：
- v0.6 27 → 28 个 skill（`hf-ultrawork` 单独算）
- v0.7 runtime（ADR-010）的 `todo-continuation-enforcer` 等价物会作为 `hf-ultrawork` 的 *运行时支撑*，但 markdown 形态的 `hf-ultrawork` 在 runtime 不可用时仍能工作（只是 idle 检测精度下降）

## 4. Alternatives considered

- **A1：拒绝 D3 + D4，保护 soul.md 第 1 条原貌**
  - 拒绝原因：架构师 explicit choose A，且诉求是"auto mode 完成"。本 ADR 通过"explicit opt-in + Fagan/gate 不让步"化解张力。
- **A2：D3 + D4 默认开启，关闭需要 explicit opt-out**
  - 拒绝原因：违反 soul.md 第 1 条的语义内核（默认是停下抛回，不是默认推进）。
- **A3：fast lane 同时允许跳过 review / gate**
  - 拒绝原因：直接违反 soul.md 第 2 条（HF 不替用户验收自己）+ 第 4 条（质量优先于进度）。Fagan + gate 是 HF 工程纪律的根。
- **A4：fast lane 通过 slash 命令 `/ultrawork` 触发**
  - 拒绝原因：见 D3 § Slash 命令。`using-hf-workflow` + 关键词识别已经够用，不需要新增命令面。

## 5. Out of Scope

- `hf-ultrawork/SKILL.md` 的具体 workflow 步骤 → v0.6 design / tasks 阶段决定
- fast lane 关键词集合的最终扩展（中文 / 英文同义词覆盖度）→ v0.6 design 阶段决定
- runtime 层的 `todo-continuation-enforcer` / `ralph-loop` 实现细节 → ADR-010 + v0.7 feature spec
- 多人协作场景下 fast lane 的权限模型（HF 当前是单架构师模型，多人协作不在 v0.6 / v0.7 / v0.9 / v1.0 任一阶段范围内）

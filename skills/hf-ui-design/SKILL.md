---
name: hf-ui-design
description: 适用于规格含 UI surface（页面/组件/交互/前端）且设计未批准、或 hf-ui-review 返回需修改/阻塞需修订的场景。不适用于纯后端/脚本/API-only（不激活本节点）、架构与 API 契约（→ hf-design）、规格仍是草稿（→ hf-specify）、设计已批准需拆任务（→ hf-tasks）、只需执行 UI 评审（→ hf-ui-review）、阶段不清或证据冲突（→ hf-workflow-router）。
---

# HF UI 设计

当任务含 UI surface 时，把已批准规格转化为可评审的 **UI 设计文档**，说明"界面如何承载需求、用户如何完成任务、视觉如何成为产品的一部分"，让后续任务规划与前端实现不再靠猜测推进。

本 skill 是 **design stage 的 conditional peer**：与 `hf-design`（技术/架构设计）**同层并行**，不 bypass 主链。两者都通过各自 review 才能进入 `hf-tasks`（联合 design approval）。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **Information Architecture** | 在 wireframe 之前先锁定站点地图、导航结构与内容分组，不让交互设计跑在 IA 之前 | Rosenfeld & Morville,《Information Architecture》 | 步骤 3 — 锁 IA 与用户流 |
| **Atomic Design** | 组件按 Atoms / Molecules / Organisms / Templates / Pages 分层，与 Design System 映射 | Brad Frost,《Atomic Design》 | 步骤 5 — 组件映射；步骤 6 — 编写文档 |
| **Design System / Design Tokens** | 所有颜色/字号/间距/圆角/阴影/动效走 token，不硬编码，视觉一致性优先于单页美化 | W3C Design Tokens CG；Material / HIG / Ant Design 等共同基础 | 步骤 4 — 视觉与 token 策略 |
| **Nielsen 十大可用性启发式** | 可用性冷读 rubric；每个关键页面可在评审阶段按十条反查 | Nielsen Norman Group | 步骤 7 — 自检 |
| **WCAG 2.2 AA** | 可访问性硬门槛：色彩对比、键盘可达、语义/ARIA、焦点管理、reduced motion | W3C | 步骤 4 — 视觉策略；步骤 7 — 自检 |
| **Interaction State Inventory** | 每个关键交互必须至少覆盖 idle / hover / focus / active / disabled / loading / empty / error / success，防止只设计 happy path | Smashing Magazine、Adam Silver 等通用实践 | 步骤 3 — 用户流；步骤 5 — 组件映射 |
| **ADR（继承自 hf-design）** | UI 层关键决策（导航范式、组件库选型、布局模式、视觉方向）用同一 ADR 模板记录，含可逆性评估 | Nygard | 步骤 4 — 选定方案；步骤 6 — 编写文档 |

补充借用（按需，不作为硬门）：**Risk-Driven Architecture (Fairbanks)** 用于对高频/高业务风险页面投入更多打磨；**YAGNI + Complexity Matching** 防止规格未要求的动效或多主题过度设计。

## When to Use

使用：

- 规格已批准，且规格声明了 UI surface（页面 / 组件 / 交互 / 前端 / 用户可见）
- `hf-ui-review` 返回 `需修改` 或 `阻塞`，需要按 findings 修订
- `hf-design` 已进入起草、需要并行起 UI 设计（parallel 默认模式）

不使用：

- 规格未声明 UI surface（API-only / 脚本 / 数据管道 / CLI / 纯后端）→ 本节点不激活，只走 `hf-design`
- 规格仍是草稿/待批准 → `hf-specify` / `hf-spec-review`
- 架构/模块/API 契约/数据模型 → `hf-design`
- 设计已批准，需要任务计划 → `hf-tasks`
- 只要求执行 UI 评审 → `hf-ui-review`
- 阶段不清或证据冲突 → `hf-workflow-router`

直接调用信号："开始做 UI 设计"、"把页面和交互先定下来"、"UI 设计被打回了"、"先别拆任务，把界面想清楚"。

## Chain Contract

读取：

- 已批准规格（重点：UI surface 声明、可用性 / 性能 / a11y / i18n NFR、关键用户任务）
- `hf-design` 当前最新稿（读 API 契约、错误模型、鉴权模型、状态形状；parallel 模式下可读草稿，标记"待 peer 锁定"条目）
- `task-progress.md`
- `AGENTS.md` 中声明的 design-system / brand / a11y / i18n / frontend principles 锚点（若存在）

产出：可评审 UI 设计草稿 + UI 决策 ADR + peer 交接说明。

Handoff：`hf-ui-review`（独立 reviewer subagent，不在父会话内联）。

**联合 approval 规则**：`hf-design-review` 与 `hf-ui-review` **同时通过**后才能进入 `设计真人确认`；任一未过，另一方可继续稳定部分，但 approval step 不解锁。

## Hard Gates

- UI 设计未 `hf-ui-review` 通过前，不得拆解任务或编写前端实现代码
- `hf-design-review` 与 `hf-ui-review` 双通过前，不发起 `设计真人确认`
- 未经 `using-hf-workflow` 或 `hf-workflow-router` 入口判断（含 UI surface 激活条件判定），不直接开始 UI 设计
- 规格未声明 UI surface 时不得以"反正要有界面"为由主动激活本节点；应先回 `hf-specify` 显式补齐 UI surface 声明

## Design Constraints

### MUST DO

- 先锁 IA（站点地图 / 导航 / 内容分组）与关键用户流（User Flow），再进入 wireframe
- 所有视觉样式走 Design Token（颜色 / 字号 / 间距 / 圆角 / 阴影 / 动效时长），不硬编码
- 组件按 Atomic Design 分层（Atoms / Molecules / Organisms / Templates / Pages），关键组件映射到 Design System 或显式扩展
- 关键交互至少覆盖 **loading / empty / error** 三态；高风险交互扩展到完整状态矩阵（含 success / partial / offline / skeleton / disabled / focus）
- 每个关键页面/组件达成 WCAG 2.2 AA：对比度、键盘可达、语义 HTML / ARIA、focus ring、reduced motion
- 至少比较两个可行视觉/交互方案并 ADR 记录选定理由（导航范式、布局范式、组件库、视觉方向等关键决策）
- 若规格含响应式 / i18n / 性能预算，逐项落到具体布局 / token / 预算数字
- 在文档中显式区分规格层（做什么）、UI 设计层（界面如何承载）、任务层（分步实施，属 `hf-tasks`）

### MUST NOT DO

- 规格未要求的华丽动效、多主题切换、花哨过渡不做（YAGNI）
- 不做"只画 happy path"的 wireframe；漏掉 loading / empty / error 视为不完整
- 视觉决策不能只给口号（"现代、简洁、有科技感"），必须落到 token 与可冷读的视觉方向 ADR
- 不做未经 Design System 登记的硬编码色值、字号、间距
- 不把 UI 设计退化成"把组件库页面照抄一遍"，仍需做规格对应的 IA 与交互裁剪
- 不越界承担架构/API 契约决策（那是 `hf-design` 的职责）；需要时在文档标注"依赖 hf-design 锁定 <X>"

## Workflow

### 1. 阅读已批准规格并提取 UI 驱动因素

读取 `AGENTS.md` 路径映射、`task-progress.md`、已批准规格相关部分、`hf-design` 当前最新稿（若已有）。

提取：

- UI surface 声明（哪些页面/组件/交互是产品对用户的暴露面）
- 关键用户任务（Jobs-to-be-Done）与关键用户路径
- 可用性 / 可访问性 / i18n / 响应式 / 性能预算 NFR
- 品牌/语气/目标受众（若规格或 `AGENTS.md` 声明）
- 约束：目标设备与浏览器、技术栈（框架、是否已有 Design System）

规格若缺以下信息，不假设默认：
- 会改变 UI surface 边界 / 验收标准 / 关键交互 / 目标设备 → 回到 `hf-workflow-router`
- 属于 UI 实现级澄清（如某处是 toast 还是 modal）、不改变需求边界 → 可在当前轮次补充确认

### 2. 了解最少必要 UI 上下文

读取：

- 现有前端栈与关键库（框架、路由、状态管理、组件库、样式方案）
- 已有 Design System / Token / 品牌规范（优先继承，不新造）
- 已有关键页面的视觉现状（复用、扩展还是重做）
- `AGENTS.md` 中声明的前端原则锚点（如"无硬编码颜色"、"禁止引入新组件库"）

不提前进入前端编码规划。若用户输入仍是 brainstorming（组件库名、页面截图灵感、零散视觉偏好混写）：

- 先归一化为 `候选方向 / 决策驱动因素 / 硬性约束 / 假设 / 明显越界的实现细节`
- 不把"随口提过的组件库或 UI kit"直接当作已比较完成的候选方向
- 先抽出真正影响方案选择的比较维度（密度、响应式、a11y、主题能力、生态成熟度、引入成本）

### 3. 锁 IA、用户流与状态矩阵

**3.1 Information Architecture**

产出至少一份站点地图或导航结构图（Mermaid / 文本树均可），含：

- 顶层导航与二级导航
- 关键页面列表与归属分组
- 权限/角色对可见性的影响（若规格含角色）

**3.2 User Flow**

对每条关键用户任务画出端到端路径。最少覆盖：

- 主路径（happy path）
- 至少 1 条错误/异常路径（鉴权失败、网络错误、空数据、表单校验不通过等）
- 关键回退/退出路径

**3.3 Interaction State Inventory**

对每个关键交互（表单提交、数据加载、列表筛选、权限受限操作等）列状态矩阵：

| 交互 | idle | hover | focus | active | disabled | loading | empty | error | success | offline/partial |
|---|---|---|---|---|---|---|---|---|---|---|
| 示例 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

高风险交互至少全列；一般交互至少覆盖 loading / empty / error 三态。状态矩阵是后续组件映射和任务拆解的必要输入。

### 4. 提出 2-3 个视觉/交互候选方向并选定

对每个候选方向至少说明：

- **风格主张**：一句可冷读的定位（如"编辑器化工具感，信息密度高，克制装饰"、"消费级仪表盘，对比强、留白大、动效节制"）——参考 Anthropic `frontend-design` skill 关于 "commit to a BOLD aesthetic direction" 的提法，本 skill 采纳"**明确的视觉主张优于折衷的安全选择**"这一原则，但在企业/工程化语境下默认倾向"intentional restraint（有意识的克制）"而非"maximalist chaos"，除非规格显式要求。
- **typography 方向**：显示字体 + 正文字体组合范围（允许用 system stack，但需显式声明理由；避免默认套用 Inter / Roboto 就完事）
- **色彩策略**：主色 / 功能色 / 语义色（success / warning / danger / info）映射到 token，声明亮/暗主题策略
- **空间与节奏**：间距 scale（如 4 / 8 倍率）、布局密度、栅格基准
- **动效策略**：是否使用动效、时长与缓动 token、是否尊重 `prefers-reduced-motion`
- **对规格关键 NFR 的匹配度**（性能预算、a11y、i18n、响应式）
- **主要风险**（生态成熟度、引入成本、学习曲线、与既有 Design System 冲突）

形成紧凑 **compare view**（表格或矩阵）——至少能冷读出：

- 候选方向之间最关键的 trade-offs
- 选定方向为什么比其他方向更匹配当前规格
- 哪些决策已稳定、哪些仍待后续澄清

复用既有 Design System 时，也要把"沿用现状"写入 compare view，而不是跳过比较。

选定后用 ADR 模板（见 `references/adr-template.md`，与 `hf-design` 共用）记录关键决策：视觉方向、组件库选型、导航范式、布局范式、主题策略、动效策略等。

若是因 `hf-ui-review` 打回而重入：先读 findings → 修复阻塞问题 → 不重做未受影响的部分。

### 5. 关键页面 wireframe 与组件映射

**5.1 Wireframe**

对关键页面（规格中声明或 User Flow 中覆盖的核心页面）给出：

- 低保真或中保真线框（可用 Mermaid、ASCII、文字布局、或外链图片）
- 内容优先级（首屏 vs 折叠下、主操作 vs 次级操作）
- 响应式断点下的差异（若规格含多端）

不要求像素级视觉稿；要求能冷读出"这个页面承担了哪条用户任务、主要操作在哪里、关键状态如何呈现"。

**5.2 Atomic Design 组件映射**

对关键组件按 Atomic 分层列出：

| 层级 | 组件 | 来源（复用 DS / 扩展 DS / 新增） | 依赖 token | 对应任务（待 `hf-tasks` 细化） |
|---|---|---|---|---|
| Atom | Button | 复用 shadcn/ui | color.primary, radius.md | ... |
| Molecule | SearchInput | 扩展（加 loading 图标） | ... | ... |
| Organism | DataTableWithFilters | 新增 | ... | ... |

新增组件需给出：职责、props 边界、关键状态、a11y 语义（role、aria-*）、键盘交互。

### 6. 编写 UI 设计文档

按 `references/ui-design-doc-template.md` 的默认结构（或 `AGENTS.md` 覆盖的模板）。

明确区分规格层（做什么）、UI 设计层（界面如何承载）、任务层（分步实施，属 `hf-tasks`）。

默认要显式落下以下文档级语义：

- 候选视觉/交互方向对比与选定理由
- IA + User Flow + 状态矩阵
- 视觉系统声明（typography / color / spacing / motion token 映射）
- 关键页面 wireframe
- 组件映射（Atomic 分层 + 来源 + 依赖 token）
- a11y / i18n / 响应式 / 性能预算声明
- 与 `hf-design` 的 peer 依赖交接块：本 UI 设计依赖对方锁定的 X/Y/Z；本 UI 设计已锁定并可供对方依赖的 A/B/C
- task planning readiness：哪些 UI 边界、组件粒度、状态矩阵已足以支撑 `hf-tasks`
- 开放问题的阻塞 / 非阻塞分类

### 7. 评审前自检与 handoff

交 `hf-ui-review` 前确认：

- [ ] UI 设计不是规格复述，也不是前端实现伪代码
- [ ] IA 与关键用户流已锁，状态矩阵至少覆盖 loading / empty / error
- [ ] 至少比较了两个视觉/交互方向并 ADR 记录选定理由
- [ ] 所有视觉决策走 token，无硬编码色值/字号/间距
- [ ] 关键页面 wireframe 与 Atomic 组件映射已给出
- [ ] WCAG 2.2 AA 逐项声明（对比度、键盘、语义、焦点、reduced motion）
- [ ] 若规格含响应式 / i18n / 性能预算，对应策略已落到具体布局/token/预算数字
- [ ] 与 `hf-design` 的 peer 依赖交接块已写明（依赖的、已锁的、冲突的）
- [ ] task planning readiness 已明确，不把未定 UI 硬推给 `hf-tasks`
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项不会污染后续任务拆解
- [ ] UI 设计草稿已保存到约定路径（默认 `docs/designs/YYYY-MM-DD-<topic>-ui-design.md`）
- [ ] `task-progress.md` 已按 canonical schema 更新 Current Stage 和 Next Action

准备好后，启动独立 reviewer subagent 执行 `hf-ui-review`，不在父会话内联评审。

## Reference Guide

按需加载详细参考内容：

| 主题 | Reference | 加载时机 |
|------|-----------|---------|
| 项目级设计原则锚点 | `AGENTS.md`（查找 design principles / design system / frontend principles / brand / a11y / i18n 的声明路径） | 项目存在此类锚点时，先按声明路径加载并用于筛选候选方向 |
| ADR 模板 | `../hf-design/references/adr-template.md` | 记录 UI 关键决策时（与 hf-design 共用） |
| UI 设计文档模板 | `references/ui-design-doc-template.md` | 编写 UI 设计文档时 |
| 交互状态清单 | `references/interaction-state-inventory.md` | 列状态矩阵时 |
| a11y 检查清单 | `references/a11y-checklist.md` | 做可访问性声明与自检时 |
| UI 决策矩阵模板 | `references/ui-decision-matrix.md` | 写候选方向 compare view 时 |

## Red Flags

- UI 设计文档写成前端实现伪代码（写出了完整的 React/Vue 组件源码）
- 复制规格而无 IA / 交互决策
- 只画 happy path，漏 loading / empty / error
- 候选方向只有名称或口号，没有可冷读的 compare view
- 视觉决策只给形容词（"简洁"、"现代"、"科技感"），不落到 token
- 直接硬编码色值/字号/间距，不走 token
- 把 `hf-design` 的 API 契约/数据模型决策写进 UI 文档
- 动效滥用（规格未要求却写了复杂动画）或动效缺失（规格含动效要求却未设计）
- 未声明 WCAG AA 或键盘可达仅写一句"支持键盘"
- Atomic 分层只写组件名，不写来源、token 依赖、a11y 语义
- peer 依赖交接块缺失却声称"设计可以直接往下走"

## 和其他 Skill 的区别

| 易混淆 skill | 区别 |
|-------------|------|
| `hf-design` | 本 skill 与 `hf-design` 是同层 peer：`hf-design` 管架构/模块/API 契约/数据模型/后端 NFR；本 skill 管 IA/wireframe/交互/视觉/组件/前端 a11y/i18n/响应式。**两者共同进入联合 design approval。** |
| `hf-ui-review` | 本 skill 负责起草 UI 设计；`hf-ui-review` 负责独立评审。不能自审自交。 |
| `hf-specify` | specify 回答"做什么"；本 skill 回答"界面如何承载"。规格未声明 UI surface 时本节点不激活。 |
| `hf-tasks` | 本 skill 回答"UI 长什么样、交互怎么流、组件怎么组"；tasks 回答"分几步实现"。UI 设计未双通过前不拆任务。 |
| `hf-workflow-router` | router 负责阶段判断、激活判定和路由；本 skill 假设阶段已确定为"设计（含 UI surface）"。 |

## Output Contract

完成时产出：

- 可评审 UI 设计草稿（保存到约定路径）
- IA / User Flow / 状态矩阵 / 视觉 token 策略 / wireframe / Atomic 组件映射 / ADR / peer 交接块
- `task-progress.md` 更新：`Current Stage` → `hf-ui-design`；`Next Action Or Recommended Skill` → `hf-ui-review`

若 `hf-design` 也在并行，`task-progress.md` 以最新进入的 skill 为 `Current Stage`，两条 skill 的 Next Action 分别登记在各自设计文档的状态字段中，由父会话/router 在联合 approval 时汇总。

推荐输出：

```markdown
UI 设计文档草稿已起草完成，下一步应派发独立 reviewer subagent 执行 `hf-ui-review`。

推荐下一步 skill: `hf-ui-review`
```

若 UI 设计稿仍未达评审门槛，不伪造 handoff；明确还缺什么，继续修订。

## Verification

- [ ] UI 设计草稿已保存到约定路径（非规格文件、非 `hf-design` 文件、非任务文件）
- [ ] 至少两个视觉/交互候选方向已比较，选定理由已用 ADR 格式记录
- [ ] IA / User Flow / 状态矩阵（≥ loading/empty/error）齐备
- [ ] Design Token 映射覆盖 typography / color / spacing / motion，关键样式无硬编码
- [ ] Atomic 组件映射已列出层级、来源、token 依赖、a11y 语义
- [ ] WCAG 2.2 AA 逐项声明（对比度 / 键盘 / 语义 / 焦点 / reduced motion）
- [ ] 响应式 / i18n / 性能预算若规格含要求，均已落地
- [ ] 与 `hf-design` 的 peer 依赖交接块已写明
- [ ] task planning readiness 已明确，足以进入 `hf-tasks`
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项已关闭或回上游
- [ ] `task-progress.md` 已按 canonical schema 更新 Current Stage 和 Next Action
- [ ] handoff 目标唯一指向 `hf-ui-review`
- [ ] UI 设计草稿不含任务拆解或前端实现源码

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
| **Design Context First** | 不在缺失既有 Design System / 品牌 / 既有产品上下文时从零起手；优先复用，必要时显式偏离 | Anthropic Claude `Claude-Design` 系统提示词 | 步骤 0 — 设计上下文获取 |
| **Anti-Slop Discipline** | 对抗 AI 默认审美：拒绝渐变滥用、紫色默认、Inter/Roboto 默认、左竖线圆角容器、装饰 SVG、emoji 当图标、通用 dashboard 模板等惯性 | Anthropic Claude `Claude-Design` 系统提示词；行业反 slop 经验 | 步骤 4 — 视觉方向；步骤 7 — 自检 |
| **Earn-Its-Place Content** | 每个 section / 文案 / 图标 / 数字必须能回指真实需求；缺资源时占位优于劣质仿制；规格之外不擅自加 section | Anthropic Claude `Claude-Design` 系统提示词；编辑规约 | 步骤 5 — wireframe；步骤 6 — 编写文档 |
| **Vocalize the System Up Front** | 进入 wireframe 之前，显式说出"将采用什么系统"（layout grid / 节奏 / 背景色用法 / 标题与图像分工等），让后续页面级决策对齐 | Anthropic Claude `Claude-Design` 系统提示词 | 步骤 4 — 视觉与 token 策略 |

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
- feature `progress.md`（默认 `features/<active>/progress.md`）
- 项目声明的 design-system / brand / a11y / i18n / frontend principles 锚点（若存在）

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

- **先取设计上下文**：在进入候选方向比较之前完成 `references/design-context-acquisition.md`，写出"视觉语汇摘要"（缺资源时显式标注与用户确认）
- 先锁 IA（站点地图 / 导航 / 内容分组）与关键用户流（User Flow），再进入 wireframe
- 所有视觉样式走 Design Token（颜色 / 字号 / 间距 / 圆角 / 阴影 / 动效时长），不硬编码
- 扩展色板时使用 OKLCH 在既有色域内推导，保持色调与既有色板和谐；不硬调 RGB 凭感觉造色
- 组件按 Atomic Design 分层（Atoms / Molecules / Organisms / Templates / Pages），关键组件映射到 Design System 或显式扩展
- 关键交互至少覆盖 **loading / empty / error** 三态；高风险交互扩展到完整状态矩阵（含 success / partial / offline / skeleton / disabled / focus）
- 每个关键页面/组件达成 WCAG 2.2 AA：对比度、键盘可达、语义 HTML / ARIA、focus ring、reduced motion；触控/移动端 hit target ≥ 44×44px
- 至少比较两个可行视觉/交互方案并 ADR 记录选定理由（导航范式、布局范式、组件库、视觉方向等关键决策），其中至少 1 条沿用既有视觉语汇、至少 1 条做有意识偏离
- **进入 wireframe 之前 vocalize the system**：显式声明本设计采用的 layout grid / 节奏 / 背景色用法 / 标题与图像的分工 / 1-2 个变化锚点，让后续页面级决策对齐
- 缺图标/插画/真实图片/品牌资产时，使用带语义的 placeholder（如 `{{ image:hero-product, 16:9 }}`、`{{ icon:warning }}`、`{{ copy:hero-headline-pending }}`），不要让 LLM 自画 SVG 或自编正文
- 若是嵌入或扩展既有产品，先冷读既有 UI 的视觉 DNA（色板/字号/圆角/密度/动效/微文案语气），写入文档顶部，再决定沿用 / 扩展 / 显式偏离
- 若规格含响应式 / i18n / 性能预算，逐项落到具体布局 / token / 预算数字
- 在文档中显式区分规格层（做什么）、UI 设计层（界面如何承载）、任务层（分步实施，属 `hf-tasks`）

### MUST NOT DO

- 规格未要求的华丽动效、多主题切换、花哨过渡不做（YAGNI）
- 规格未要求的 section / 文案 / 数据徽标不擅自添加；感觉某区域"应该再加点东西"时，先问用户而不是先加（earn-its-place）
- 不做"只画 happy path"的 wireframe；漏掉 loading / empty / error 视为不完整
- 视觉决策不能只给口号（"现代、简洁、有科技感"），必须落到 token 与可冷读的视觉方向 ADR
- 不做未经 Design System 登记的硬编码色值、字号、间距
- **拒绝 AI 默认审美的惯性产物**（按 `references/anti-slop-checklist.md`）：紫色 / 紫蓝渐变默认主色、Inter / Roboto / 系统栈无理由套用、所有 callout 都是"左 4px 彩条 + 圆角卡片"、emoji 当图标、自画"科技感" SVG 插画、千篇一律的 dashboard 模板、glassmorphism 滥用、5+ 不同阴影同页混用
- 不把 UI 设计退化成"把组件库页面照抄一遍"，仍需做规格对应的 IA 与交互裁剪
- 不越界承担架构/API 契约决策（那是 `hf-design` 的职责）；需要时在文档标注"依赖 hf-design 锁定 <X>"
- 不在缺失既有 Design System / 品牌 / 既有产品上下文时强行从零起手；先取上下文，否则只能产出 AI 默认审美

## Workflow

### 0. 取设计上下文（Design Context Acquisition）

按 `references/design-context-acquisition.md` 完成：

- 索取或定位 P0 资产（既有产品代码 / Storybook / Design System / token 表）与 P1 资产（品牌指南、既有产品截图）
- 写出 **视觉语汇摘要**（色板 / 字体 / scale / 圆角 / 阴影 / 密度 / 动效 / 微文案语气 / iconography），落到 `ui-design.md` 顶部
- 缺资源时按规约用 placeholder 与显式声明，不让 LLM 自补

未取到 P0 + P1 + 用户确认 → 不进入步骤 3（候选方向比较）。这是反 AI 默认审美的硬门，不可跳过。

### 1. 阅读已批准规格并提取 UI 驱动因素

读取 项目级路径约定（若项目已声明）、feature `progress.md`（默认 `features/<active>/progress.md`）、已批准规格（默认 `features/<active>/spec.md`）相关部分、`hf-design` 当前最新稿（若已有，默认 `features/<active>/design.md`）。

提取：

- UI surface 声明（哪些页面/组件/交互是产品对用户的暴露面）
- 关键用户任务（Jobs-to-be-Done）与关键用户路径
- 可用性 / 可访问性 / i18n / 响应式 / 性能预算 NFR
- 品牌/语气/目标受众（若规格或 项目声明）
- 约束：目标设备与浏览器、技术栈（框架、是否已有 Design System）

规格若缺以下信息，不假设默认：
- 会改变 UI surface 边界 / 验收标准 / 关键交互 / 目标设备 → 回到 `hf-workflow-router`
- 属于 UI 实现级澄清（如某处是 toast 还是 modal）、不改变需求边界 → 可在当前轮次补充确认

### 2. 了解最少必要 UI 上下文

读取：

- 现有前端栈与关键库（框架、路由、状态管理、组件库、样式方案）
- 已有 Design System / Token / 品牌规范（优先继承，不新造）
- 已有关键页面的视觉现状（复用、扩展还是重做）
- 项目声明的前端原则锚点（如"无硬编码颜色"、"禁止引入新组件库"）

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

**Vocalize the System（进入 wireframe 之前必做）**：在选定方向 ADR 之后、wireframe 之前，显式写出本设计的"系统宣言"。最少包含：

- 主 layout grid（列数 / 间距 / 内容上限宽度 / 响应式断点）
- 节奏与变化锚点（如"section 头部用大号 display 字 + 短语，正文区用 16px / 24px 行高 + 测量友好行长 60-75ch；每 3 个常规 section 后插入一个全宽幅段落作为节奏断点"）
- 1-2 个一致的背景色用法（如"主背景用 surface.0；强调段落用 surface.1；section 切换不再换更多背景色"）
- 标题与图像的分工（如"图像主导页 → display 标题 + 图像优先；信息密集页 → 单列 + 排版主导，不强行配图"）
- 约束 1-2 个视觉变量在全局保持稳定（如"全局只允许 1 种动效缓动函数；圆角全局只允许 sm/md/lg 三档"）

系统宣言写完后立刻冷读：能否只看宣言就预测出所有关键页面的视觉骨架？不能 → 宣言不够；继续补。

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

按 `references/ui-design-doc-template.md` 的默认结构（或 项目级覆盖的模板）。

明确区分规格层（做什么）、UI 设计层（界面如何承载）、任务层（分步实施，属 `hf-tasks`）。

默认要显式落下以下文档级语义：

- 视觉语汇摘要（既有产品冷读，文档顶部 §0）
- 候选视觉/交互方向对比与选定理由（含至少 1 条沿用 + 至少 1 条偏离）
- 系统宣言（vocalize the system，§6.5）
- IA + User Flow + 状态矩阵
- 视觉系统声明（typography / color / spacing / motion token 映射；扩展色板用 OKLCH 推导关系）
- 关键页面 wireframe（缺资源处使用 `{{ image:... }}` / `{{ icon:... }}` / `{{ copy:... }}` 占位）
- 组件映射（Atomic 分层 + 来源 + 依赖 token）
- a11y / i18n / 响应式 / 性能预算声明（含触控/移动端 hit target ≥ 44×44px）
- 与 `hf-design` 的 peer 依赖交接块：本 UI 设计依赖对方锁定的 X/Y/Z；本 UI 设计已锁定并可供对方依赖的 A/B/C
- task planning readiness：哪些 UI 边界、组件粒度、状态矩阵已足以支撑 `hf-tasks`
- 反 AI slop 自检记录（§20，按 `references/anti-slop-checklist.md` 第 5 节冷读 5 项）
- 开放问题的阻塞 / 非阻塞分类

### 7. 评审前自检与 handoff

交 `hf-ui-review` 前确认：

- [ ] **设计上下文已取**：P0 + P1 资产已获取或显式标注与用户确认；视觉语汇摘要已写入文档顶部
- [ ] UI 设计不是规格复述，也不是前端实现伪代码
- [ ] IA 与关键用户流已锁，状态矩阵至少覆盖 loading / empty / error
- [ ] 至少比较了两个视觉/交互方向并 ADR 记录选定理由；其中至少 1 条沿用既有视觉语汇、至少 1 条做有意识偏离
- [ ] **系统宣言（vocalize the system）已写出**：layout grid / 节奏锚点 / 背景色用法 / 标题与图像分工 / 全局视觉约束已显式
- [ ] 所有视觉决策走 token，无硬编码色值/字号/间距；扩展色板用 OKLCH 推导
- [ ] 关键页面 wireframe 与 Atomic 组件映射已给出；缺资源处用带语义的 placeholder
- [ ] WCAG 2.2 AA 逐项声明（对比度、键盘、语义、焦点、reduced motion）；触控/移动端 hit target ≥ 44×44px
- [ ] 若规格含响应式 / i18n / 性能预算，对应策略已落到具体布局/token/预算数字
- [ ] **反 AI slop 自检完成**：按 `references/anti-slop-checklist.md` 第 5 节冷读 5 项已过；任何被标记为可疑 slop 的元素已修正或显式辩护
- [ ] 与 `hf-design` 的 peer 依赖交接块已写明（依赖的、已锁的、冲突的）
- [ ] task planning readiness 已明确，不把未定 UI 硬推给 `hf-tasks`
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项不会污染后续任务拆解
- [ ] UI 设计草稿已保存到约定路径（默认 `features/<active>/ui-design.md`）
- [ ] feature `progress.md` 已按 canonical schema 更新 Current Stage 和 Next Action

准备好后，启动独立 reviewer subagent 执行 `hf-ui-review`，不在父会话内联评审。

## Reference Guide

按需加载详细参考内容：

| 主题 | Reference | 加载时机 |
|------|-----------|---------|
| 项目级设计原则锚点 | 项目级约定（查找 design principles / design system / frontend principles / brand / a11y / i18n 的声明路径） | 项目存在此类锚点时，先按声明路径加载并用于筛选候选方向 |
| ADR 模板 | `../hf-design/references/adr-template.md` | 记录 UI 关键决策时（与 hf-design 共用） |
| UI 设计文档模板 | `references/ui-design-doc-template.md` | 编写 UI 设计文档时 |
| 交互状态清单 | `references/interaction-state-inventory.md` | 列状态矩阵时 |
| a11y 检查清单（含最小尺寸表） | `references/a11y-checklist.md` | 做可访问性声明与自检时；定移动端 / 演示稿 / 印刷物最小尺寸时 |
| UI 决策矩阵模板（含多样性策略） | `references/ui-decision-matrix.md` | 写候选方向 compare view 时 |
| **设计上下文获取** | `references/design-context-acquisition.md` | 步骤 0；任何含 UI surface 的 feature 启动时必读 |
| **反 AI slop 设计清单** | `references/anti-slop-checklist.md` | 步骤 4 视觉方向决策 + 步骤 7 自检；评审时也用于 anti-pattern 检测 |

## Red Flags

- UI 设计文档写成前端实现伪代码（写出了完整的 React/Vue 组件源码）
- 复制规格而无 IA / 交互决策
- 只画 happy path，漏 loading / empty / error
- 候选方向只有名称或口号，没有可冷读的 compare view
- 候选方向 3 条都是同维度微调（如只换主色 hue），缺真正的跨维度差异
- 缺少与既有视觉语汇对照的"沿用候选方向"，全部是"全新视觉"
- 视觉决策只给形容词（"简洁"、"现代"、"科技感"），不落到 token
- 直接硬编码色值/字号/间距，不走 token；扩展色板用随手 RGB 而非 OKLCH 推导
- 设计中出现紫色/紫蓝渐变默认主色、Inter/Roboto 默认字体、左 4px 彩条 + 圆角卡片当唯一信息层级范式（典型 AI 默认审美 slop）
- 自画"科技感" SVG 插画 / 用 emoji 当图标 / 数据可视化堆砌"+12.4%"等无业务定义的数字（数据 slop）
- 在规格未要求时擅自添加 Testimonials / Features grid / FAQ / CTA banner 等填充式 section
- 缺真实图标 / 图片 / 文案时让 LLM 自补，而不是用 `{{ image:... }}` / `{{ copy:... }}` 占位
- 把 `hf-design` 的 API 契约/数据模型决策写进 UI 文档
- 动效滥用（规格未要求却写了复杂动画）或动效缺失（规格含动效要求却未设计）
- 未声明 WCAG AA 或键盘可达仅写一句"支持键盘"
- 移动端 hit target < 44×44px 而无场景说明
- Atomic 分层只写组件名，不写来源、token 依赖、a11y 语义
- peer 依赖交接块缺失却声称"设计可以直接往下走"
- 未取设计上下文（无既有 Design System / 品牌 / 既有产品截图）就直接进入候选方向比较
- 系统宣言（vocalize the system）缺失，wireframe 各页面背景色 / layout grid / 节奏锚点彼此不一致

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
- feature `progress.md` 更新：`Current Stage` → `hf-ui-design`；`Next Action Or Recommended Skill` → `hf-ui-review`

若 `hf-design` 也在并行，feature `progress.md` 以最新进入的 skill 为 `Current Stage`，两条 skill 的 Next Action 分别登记在各自设计文档的状态字段中，由父会话/router 在联合 approval 时汇总。

推荐输出：

```markdown
UI 设计文档草稿已起草完成，下一步应派发独立 reviewer subagent 执行 `hf-ui-review`。

推荐下一步 skill: `hf-ui-review`
```

若 UI 设计稿仍未达评审门槛，不伪造 handoff；明确还缺什么，继续修订。

## Verification

- [ ] UI 设计草稿已保存到约定路径（非规格文件、非 `hf-design` 文件、非任务文件）
- [ ] 设计上下文（P0 + P1 资产）已取或显式标注与用户确认；视觉语汇摘要已写入文档顶部
- [ ] 系统宣言（vocalize the system）已写出：layout grid / 节奏锚点 / 背景色用法 / 标题与图像分工 / 全局视觉约束
- [ ] 至少两个视觉/交互候选方向已比较，选定理由已用 ADR 格式记录；至少 1 条沿用既有视觉语汇、至少 1 条做有意识偏离
- [ ] IA / User Flow / 状态矩阵（≥ loading/empty/error）齐备
- [ ] Design Token 映射覆盖 typography / color / spacing / motion，关键样式无硬编码；扩展色板用 OKLCH 推导
- [ ] Atomic 组件映射已列出层级、来源、token 依赖、a11y 语义
- [ ] WCAG 2.2 AA 逐项声明（对比度 / 键盘 / 语义 / 焦点 / reduced motion）；触控/移动端 hit target ≥ 44×44px
- [ ] 响应式 / i18n / 性能预算若规格含要求，均已落地
- [ ] 反 AI slop 自检完成（按 `references/anti-slop-checklist.md` 第 5 节）；缺资源处用带语义的 placeholder
- [ ] 与 `hf-design` 的 peer 依赖交接块已写明
- [ ] task planning readiness 已明确，足以进入 `hf-tasks`
- [ ] 开放问题已区分阻塞 / 非阻塞，阻塞项已关闭或回上游
- [ ] feature `progress.md` 已按 canonical schema 更新 Current Stage 和 Next Action
- [ ] handoff 目标唯一指向 `hf-ui-review`
- [ ] UI 设计草稿不含任务拆解或前端实现源码

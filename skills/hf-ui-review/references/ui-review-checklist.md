# UI 设计评审检查清单

评审 UI 设计文档时，至少对以下 9 个维度逐项审查。每个维度内部评分 `0-10`，评分帮助区分轻微缺口与阻塞问题。

## 评分辅助规则

- 任一关键维度低于 `6/10` → 不得返回 `通过`
- 任一维度低于 `8/10` → 通常至少对应一条具体发现项或薄弱点
- U5（可访问性）关键项（色彩对比、键盘可达、focus 可见）未达标 → 自动 `critical`

## 评审维度

| ID | 维度 | Pass Condition |
|---|---|---|
| `U1` | 需求覆盖与追溯 | UI 设计覆盖规格中 UI surface 声明项，新增 UI 能力可回指已批准规格或 UX NFR |
| `U2` | IA 与用户流完整性 | 站点地图 / 导航 / 内容分组明确；关键用户任务端到端路径（含异常/回退）已画清 |
| `U3` | 交互状态覆盖 | 每个关键交互至少覆盖 loading / empty / error 三态，高风险交互扩展到完整矩阵 |
| `U4` | 视觉一致性与 Design Token 合规 | typography / color / spacing / radius / motion 走 token；无硬编码；Atomic 分层与来源显式 |
| `U5` | 可访问性（WCAG 2.2 AA） | 色彩对比、键盘可达、语义/ARIA、focus 可见、reduced motion、目标大小等逐项声明 |
| `U6` | 响应式 / i18n / 性能预算适配 | 若规格含要求，均已落到具体布局 / token / 预算数字 |
| `U7` | 决策质量与 trade-offs | 至少比较两个视觉/交互方向（含至少 1 条沿用既有视觉语汇 + 至少 1 条有意识偏离），选型理由与代价可冷读；关键决策有 ADR |
| `U8` | 任务规划准备度与 peer 交接 | 组件粒度、状态矩阵、a11y 实现边界足以支撑 `hf-tasks`；与 `hf-design` 的 peer 依赖交接块显式 |
| `U9` | 设计上下文与反 AI slop 合规 | 设计上下文（既有 DS / 品牌 / 既有产品视觉语汇摘要）已取或显式标注与用户确认；系统宣言（vocalize the system）已写出；按 `../hf-ui-design/references/anti-slop-checklist.md` 不命中 AI 默认审美与填充式内容反模式 |

### `U1` 需求覆盖与追溯

- UI 设计是否覆盖了规格中声明的 UI surface？
- 每个关键页面/组件能否回指到需求编号、UX NFR 或等价规格锚点？
- 是否存在新增 UI 能力（新页面 / 新交互模式 / 新数据呈现）却无法追溯到已批准规格？
- 是否误将 `hf-design` 层的架构或 API 决策写入了本文档？

### `U2` IA 与用户流完整性

- 站点地图 / 导航结构是否清晰？
- 关键用户任务是否都有端到端路径？
- 异常路径（鉴权失败、网络错误、空数据、校验失败）是否画清？
- 回退 / 退出路径是否明确？
- 是否存在"从某页跳到某页"的隐性依赖但未画出？

### `U3` 交互状态覆盖

- 每个关键交互是否至少覆盖 loading / empty / error 三态？
- 高风险交互（支付、权限变更、删除、批量操作）是否覆盖完整矩阵？
- 状态转换是否避免布局抖动（CLS 隐患）？
- 错误态是否说明原因 + 下一步（而不是仅"出错了"）？
- 空态是否给出引导主操作（而不是空白）？

### `U4` 视觉一致性与 Design Token 合规

- 所有颜色 / 字号 / 间距 / 圆角 / 阴影 / 动效时长是否都走 token？
- 语义 token（success/warning/danger/info）是否单独列出，不与主色复用？
- 亮/暗主题策略是否明确？
- 字体选择是否显式说明理由（避免默认 Inter/Roboto 无理由套用）？
- Atomic 分层（Atoms/Molecules/Organisms/Templates/Pages）是否显式，每层有来源（复用/扩展/新增）和 token 依赖？
- 新增组件是否定义 props 边界、关键状态、a11y 语义（role、aria-*）、键盘交互？

### `U5` 可访问性（WCAG 2.2 AA）

见 `../hf-ui-design/references/a11y-checklist.md`。评审时至少确认：

- **色彩对比**：正文 ≥ 4.5:1；大字号 ≥ 3:1；UI 组件/状态指示 ≥ 3:1（逐项计算或工具验证，不接受"视觉上差不多"）
- **键盘可达**：所有控件可 Tab / Enter / Space / 方向键操作；自定义组件遵循 WAI-ARIA APG 对应键盘模式
- **focus 可见**：全局 `:focus-visible` 样式已声明；不使用无替代的 `outline: none`
- **语义结构**：heading 层级连续、label 与 input 显式关联、list 用 `ul`/`ol`
- **reduced motion**：所有 motion token 在 `prefers-reduced-motion: reduce` 下的降级策略明确
- **目标大小**：交互控件 ≥ 24×24px（WCAG 2.2 新增）
- **错误提示**：非仅颜色（含图标 / 文字 / `aria-describedby`）

任一关键项未声明或声明为含糊表述（如"支持可访问性"、"达到 AA 标准"而无证据）→ `critical`。

### `U6` 响应式 / i18n / 性能预算适配

仅在规格含对应要求时评审：

- **响应式**：断点是否明确？断点下内容优先级是否显式（首屏 vs 折叠下、主操作 vs 次级操作）？
- **i18n**：文案抽取策略、数字/日期格式、RTL 镜像（若支持）是否明确？多语种下的排版边界情况是否考虑（长词、行高、字形覆盖）？
- **性能预算**：LCP / INP / CLS 目标是否显式？首屏字节预算、关键渲染路径策略是否落实？动效/图片/字体加载是否有约束？

规格有要求而本文档未响应 → `important` 或 `critical`（视规格强度）。

### `U7` 决策质量与 trade-offs

- 是否真的比较了至少两个可行视觉/交互方向？
- 是否说明为什么选定当前方向？
- 关键决策（视觉方向、组件库、导航范式、布局范式、表单模式、数据呈现模式）是否有 ADR？
- ADR 是否包含可逆性评估？
- reviewer 能否冷读出 trade-off，而不需要从 prose 猜测？
- 复用既有 Design System 是否也作为候选方向写入矩阵（而非跳过比较）？

### `U8` 任务规划准备度与 peer 交接

- 组件映射是否足以让 `hf-tasks` 稳定拆解前端任务？
- 状态矩阵是否足以让 `hf-test-driven-dev` 设计出 fail-first 测试？
- 关键页面 wireframe 是否稳定到可以进入实现？
- 与 `hf-design` 的 peer 依赖交接块是否显式列出：
  - 本文档依赖 `hf-design` 锁定的条目
  - 本文档已锁定、可供 `hf-design` 依赖的条目
  - 冲突或待协商的条目
- 是否还存在会直接破坏任务拆解的 UI 空洞？
- 文档是否显式说明了 task planning readiness，而不是把缺口留给下游猜？

### `U9` 设计上下文与反 AI slop 合规

见 `../hf-ui-design/references/design-context-acquisition.md` 与 `../hf-ui-design/references/anti-slop-checklist.md`。评审时至少确认：

- **设计上下文已取**：文档顶部存在"视觉语汇摘要"（色板 / 字体 / scale / 圆角 / 阴影 / 密度 / 动效 / 微文案语气 / iconography），或显式标注"无既有产品上下文，已与用户确认本轮采用通用专业语境默认"
- **候选方向沿用 vs 偏离的对照存在**：至少 1 条沿用既有视觉语汇、至少 1 条做有意识偏离（偏离条必须 ADR 解释偏离理由与可逆性）
- **系统宣言（vocalize the system）已写出**：layout grid / 节奏锚点 / 背景色用法 / 标题与图像分工 / 全局视觉约束在 wireframe 之前已显式声明
- **不命中 AI 默认审美 slop**（按 `anti-slop-checklist.md` 第 1 节 S1–S8）：
  - S1 渐变滥用（大面积彩色背景渐变 / 渐变主按钮 / 渐变描边）
  - S2 所有 callout / alert / quote 都是"左 4px 彩条 + 圆角卡片"
  - S3 typography 直接套 Inter / Roboto / Arial / 系统栈而无理由说明
  - S4 紫色 / 紫蓝渐变默认主色、品牌 #6366F1 类 Tailwind 默认色当主色
  - S5 自画"科技感" SVG / 用 emoji 当图标
  - S6 千篇一律 dashboard 模板（顶 nav + 左 rail + 卡片网格 + 趋势图 + KPI 大数字，无场景化裁剪）
  - S7 glassmorphism / 高斯模糊滥用且无对比度计算
  - S8 同页 5+ 不同阴影深度 / 所有卡片"浮起来"
- **不命中内容 slop**（按 `anti-slop-checklist.md` 第 2 节 C1–C5）：填充式 hero copy、无业务定义的数据徽标、规格之外擅自加 section、伪装成正文的占位文本、无语义的图标堆叠
- **不命中结构 slop**（按 `anti-slop-checklist.md` 第 3 节 ST1–ST4）：无来源 token、未声明的视觉宣言、状态切换无设计、happy-path-only IA
- **嵌入既有产品时**（按 `anti-slop-checklist.md` 第 4 节 E1–E3）：不命中"未读既有视觉语汇就开始新设计"、"新增组件无既有对应物对照"、"两套命名 / 两套 token 并存"
- **缺资源处使用 placeholder**：图标 / 插画 / 真实图片 / 文案缺失时使用 `{{ image:... }}` / `{{ icon:... }}` / `{{ copy:... }}` 等带语义的占位标记，而非 LLM 自补
- **扩展色板用 OKLCH 推导**：新增色值能说出与既有色板的色域关系，而不是凭感觉调 RGB

任一关键项失败（设计上下文缺失、系统宣言缺失、命中两个及以上 slop 反模式）→ 通常 `important` 起；若同时与无障碍达标冲突 → `critical`。

## Anti-Pattern 检测

评审时主动检测以下常见反模式：

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `AU1` | Happy Path Only | 关键交互无 loading/empty/error 态 | 补状态矩阵，高风险交互补完整矩阵 |
| `AU2` | 无根据的视觉宣言 | 只写"现代/简洁/有科技感"之类形容词 | 落到 typography / color / spacing / motion 的具体 token 和理由 |
| `AU3` | 硬编码样式 | 设计中出现具体十六进制色值 / px 数字而无对应 token | 全部通过 token 映射，或显式扩展 token |
| `AU4` | 默认 AI 审美 | 套用 Inter / 紫色渐变 / 通用 dashboard 模板无场景化 | 按规格语境做差异化选择；引用 Anthropic frontend-design 原则"intentional direction, not generic defaults" |
| `AU5` | a11y 口号化 | 只写"支持 WCAG AA"无逐项声明 | 按 `a11y-checklist.md` 逐项落地 |
| `AU6` | 跨权决策 | UI 文档里写死了 API 契约、数据模型、后端错误码 | 只引用 `hf-design` 锁定内容；自己范围外用 peer 交接块标记 |
| `AU7` | 组件名即设计 | Atomic 映射只写组件名，无来源/token/a11y 语义 | 补齐表格所有列 |
| `AU8` | 状态转换无设计 | 画了状态但没画状态切换的过渡/反馈 | 补过渡时机、反馈方式、是否符合 reduced-motion |
| `AU9` | 未比较的"推荐方案" | 只给一个方案 + 一个明显的稻草人 | 至少两个真实可行方向 + 完整矩阵 |
| `AU10` | peer 交接含糊 | "需要和后端对齐"、"API 待定"类含糊表述 | 具体到字段、时序、错误码、状态码 |
| `AU11` | 设计上下文缺失就开工 | 文档无视觉语汇摘要；候选方向不引用任何既有产品 / DS / 品牌资产 | 回 `hf-ui-design` 步骤 0 取上下文；缺资源时显式标注与用户确认 |
| `AU12` | 系统宣言（vocalize the system）缺失 | 各页面 wireframe 的背景色 / layout grid / 节奏锚点彼此不一致；整体看不出统一系统 | 在视觉方向 ADR 之后、wireframe 之前补写系统宣言 |
| `AU13` | AI 默认审美 slop | 紫色 / 紫蓝渐变默认主色、Inter / Roboto 默认字体、左 4px 彩条 + 圆角卡片单一信息层级范式、千篇一律 dashboard 模板、emoji 当图标 | 按 `anti-slop-checklist.md` S1–S8 修正；视觉方向 ADR 显式说明拒绝这些惯性的理由 |
| `AU14` | 填充式内容 / 数据 slop | 规格之外擅自加 Testimonials / Features grid / FAQ；仪表盘塞满"+12.4%"等无业务定义数字 | 按 `anti-slop-checklist.md` C1–C5；规格未要求的 section 先问用户而非先加 |
| `AU15` | LLM 自补缺失资源 | 自画"科技感" SVG 插画 / 自编正文 / 自造品牌色 | 用 `{{ image:... }}` / `{{ copy:... }}` / `{{ icon:... }}` 占位；扩展色板用 OKLCH 在既有色域内推导 |
| `AU16` | 候选方向无沿用 vs 偏离对照 | 3 条候选方向都是"全新视觉"或都是同维度微调（只换主色 hue） | 至少 1 条沿用既有视觉语汇 + 至少 1 条有意识偏离；3 条之间至少 2 个维度有显著差异 |

## Finding 写法对比

✅ 具体：`[critical][LLM-FIXABLE][U5] 所有 error 态仅使用红色边框传达错误，未附图标或 inline 文案，违反 WCAG 1.4.1 Use of Color；应在每个 error 态补充 icon + 文字 + aria-describedby`

❌ 模糊：`可访问性不够`

✅ 具体：`[important][LLM-FIXABLE][U3] 搜索结果列表未定义 partial 态与 offline 态；规格 NFR-3 要求断网可读取本地缓存结果，当前设计无对应状态矩阵行`

❌ 模糊：`状态不全`

✅ 具体：`[critical][LLM-FIXABLE][U8] 与 hf-design 的 peer 交接块仅写"错误码待对齐"；应具体到 401/403/429 的各自 UI 处置路径`

❌ 模糊：`和后端设计需要联动`

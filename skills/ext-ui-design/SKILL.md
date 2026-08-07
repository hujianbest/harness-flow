---
name: ext-ui-design
description: UI 设计领域扩展。绑定阶段: plan、build、verify。触发条件: 特性包含用户界面(页面、组件、可视交互)。注入反 AI-slop 视觉纪律、交互三态覆盖、可访问性底线、动效性能护栏，并把详细检查清单委托给 references/ui-checklist.md。
---

# UI 设计扩展

## 绑定

- 绑定阶段: plan、build、verify
- 触发条件: 特性包含用户界面(页面 / 组件 / 可视交互)

## 计划阶段 (plan) 规则

`plan.md`（或档位 3 的 `design.md`）追加 **"UI 设计"** 一节（置于测试策略之后、任务清单之前），必须覆盖：

### 信息架构与交互先行

- 先锁定页面结构、导航与内容分组，再进入组件与视觉细节
- 每个关键交互至少覆盖 **loading / empty / error** 三态；高风险交互（支付、删除、提交）补齐 disabled / success / focus
- 只画 happy path 的交互设计视为不完整，gate 会拒绝

### 视觉系统与 token 纪律

- 有既有 Design System / 品牌规范或 `DESIGN.md` 时**必须先冷读并复用**：色板、字体、间距、圆角、密度；偏离要显式说明理由并记入 `assumptions.md`
- 颜色、字号、间距、圆角、阴影一律走 design token，禁止硬编码字面量（如 `#3b82f6`、`text-[14px]`、`rounded-[7px]`）；扩展色板从既有色域推导
- 有 `DESIGN.md` 时优先从中取值（见 `ext-design-md`）；无则先在 plan 的 token 表里命名再使用
- 缺图标 / 图片 / 文案资产时使用带语义的占位符（如 `{{ image:hero, 16:9 }}`），不自画 SVG、不自编正文

### 反 AI-slop 审美（硬拒绝项）

以下惯性产物一律拒绝，除非用户在 `decisions.md` 明确要求：

- 无理由的紫色 / 紫蓝渐变主色、Inter / Roboto 默认字体
- 千篇一律的"左彩条 + 圆角卡片" callout、emoji 当功能图标、无理由 glow 效果
- 需求没要求的装饰性动效、glassmorphism（`backdrop-blur` 大面积模糊）、多套阴影混用
- 未回指真实需求的 section、文案、数字徽标（每个元素要能说出对应哪条需求）
- 空状态不给下一步动作（每个 empty state 必须有一个明确的 CTA）

### 可访问性底线

- 文本对比度满足 WCAG AA（正文 ≥ 4.5:1，大字 ≥ 3:1）
- 交互元素键盘可达、焦点可见；icon-only 按钮必须有 `aria-label`
- 语义化 HTML / 正确的 ARIA；触控目标 ≥ 44×44px
- 详见 `references/ui-checklist.md` 的可访问性专项

## 实现阶段 (build) 规则

- UI 相关任务的测试设计需覆盖交互三态（loading / empty / error）的可验证行为
- token 纪律延续到代码：发现硬编码色值 / 字号即在 REFACTOR 步清理
- 进入 build 前加载 `references/ui-checklist.md`，按清单逐项自查后再提请 verify

## 验证阶段 (verify) 规则

- 运行时冒烟必须包含**真实渲染验证**：浏览器 / 模拟器中渲染确认页面正常；只有单元测试不构成 UI 冒烟
- 交互三态至少各有一份可核对的验证（截图确认或断言三态的测试）
- 可访问性用 axe / lighthouse 等工具跑一次自动检查；critical 违规必须修复后才能 ship

## 评审检查项

以下条目追加到对应阶段 checklist：

- [ ] (plan) UI 章节存在，关键交互覆盖三态，视觉决策落到 token 而非口号
- [ ] (plan) 复用了既有 Design System / DESIGN.md，或偏离处有显式理由
- [ ] (plan) 反 slop 硬拒绝项逐一排查，无侥幸产物
- [ ] (code) 无硬编码视觉样式；可访问性要求有落实证据
- [ ] (code) 真实渲染的 smoke 验证已完成，不只有单元测试
- [ ] (code) 交互三态各有验证；a11y 自动检查无 critical 违规

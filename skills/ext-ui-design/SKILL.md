---
name: ext-ui-design
description: UI 设计领域扩展。绑定阶段: to-spec、implement、code-review。触发条件: 特性包含用户界面(页面、组件、可视交互)。注入反 AI-slop 视觉纪律、交互三态覆盖、可访问性底线、动效性能护栏，并把详细检查清单委托给 references/ui-checklist.md。
---

# UI 设计扩展

## 绑定

- 绑定阶段: to-spec、implement、code-review
- 触发条件: 特性包含用户界面(页面 / 组件 / 可视交互)

## 规格阶段 (to-spec) 规则

`spec.md` 的 Implementation / Testing Decisions 或专设 **UI 设计** 节须覆盖:

### 信息架构与交互先行

- 先锁定页面结构、导航与内容分组，再进入组件与视觉细节
- 每个关键交互至少覆盖 **loading / empty / error** 三态；高风险交互补齐 disabled / success / focus
- 只画 happy path 视为不完整

### 视觉系统与 token 纪律

- 有既有 Design System / 品牌规范或 `DESIGN.md` 时**必须先冷读并复用**
- 颜色、字号、间距、圆角、阴影一律走 design token，禁止硬编码字面量
- 有 `DESIGN.md` 时优先取值（见 `ext-design-md`）；无则先在 spec 里命名 token
- 缺资产时用语义占位符，不自画 SVG、不自编正文

### 反 AI-slop 审美（硬拒绝项）

除非用户在 decisions/ADR 明确要求，拒绝: 无理由紫渐变、Inter/Roboto 默认字体、左彩条圆角卡片 callout、emoji 当图标、无理由 glow、装饰性动效、大面积 glassmorphism、未回指需求的 section/徽标、空状态无 CTA。

### 可访问性底线

- 正文对比度 WCAG AA；键盘可达与焦点可见；icon-only 须 `aria-label`；触控目标 ≥ 44×44px
- 详见 `references/ui-checklist.md`

## 实现阶段 (implement) 规则

- UI 相关票的测试覆盖交互三态可验证行为
- token 纪律延续到代码；硬编码在重构步清理
- 提请 code-review 前加载 `references/ui-checklist.md` 自查

## 代码评审阶段 (code-review) 规则

- 冒烟须含**真实渲染**验证；仅单测不构成 UI 冒烟
- 交互三态各有可核对验证；a11y 自动检查无 critical

## 评审检查项

- [ ] (spec) UI 决策覆盖三态，视觉落到 token
- [ ] (spec) 复用 Design System / DESIGN.md 或偏离有理由
- [ ] (spec) 反 slop 硬拒绝项排查
- [ ] (code) 无硬编码视觉样式；a11y 有落实证据
- [ ] (code) 真实渲染验证完成；三态与 a11y 检查通过

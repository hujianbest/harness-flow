# UI 检查清单

进入 build 前逐项自查；verify 阶段逐项核对证据。每项给出"为什么"和"怎么查"。

## 1. 反 AI-slop 视觉（plan + verify）

| 检查项 | 为什么 | 怎么查 |
|--------|--------|--------|
| 无无理由渐变主色 | AI 默认审美暴露 | 搜 `gradient` / `bg-gradient`，每个都要能回指需求或 decisions.md |
| 无紫色 / 紫蓝默认主色 | 最常见的 AI 配色惯性 | 检查主色 token 值是否落在 `oklch(0.5+ 0.2+ 270-300)` 或 `hsl(240-280)` |
| 无 emoji 当功能图标 | 不专业、跨平台不一致 | 搜 emoji unicode 范围出现在 `icon` / `button` 上下文 |
| 无 glassmorphism 大面积模糊 | 性能差 + 视觉廉价 | 搜 `backdrop-blur`，只允许小面积（如单个 badge） |
| 无 glow 效果当主交互提示 | 可发现性差 | 搜 `shadow` + `blur` 组合、`drop-shadow` |
| 空状态有 CTA | 用户不知道下一步 | 每个 empty state 截图里能看到一个按钮或链接 |
| 每个元素回指需求 | 防"凑数"组件 | 抽查 3 个 section，说出对应 product.md / plan.md 哪条 |

## 2. Token 纪律（build）

| 检查项 | 为什么 | 怎么查 |
|--------|--------|--------|
| 无硬编码颜色 | 无法换肤、暗色模式断裂 | 搜 `#[0-9a-fA-F]{3,8}`、`rgb(`、`hsl(`、`oklch(` 出现在 className 或 style |
| 无硬编码字号 | 排版节奏断裂 | 搜 `text-[`、`font-size:` 后跟数字 |
| 无硬编码间距 / 圆角 | 密度系统断裂 | 搜 `p-[`、`m-[`、`rounded-[`、`gap-[` 后跟数字 |
| 有 DESIGN.md 时从其中取值 | 单一事实源 | 对比 plan 的 token 表与 DESIGN.md frontmatter |
| 无 DESIGN.md 时 plan 内有 token 表 | 临时也要有命名 | plan.md 的 UI 设计节有命名 token 列表 |

## 3. 可访问性（plan + verify）

优先用原生 HTML，只在原生不够时加 ARIA。

### 关键（critical）

- 每个交互控件有 accessible name（icon-only 按钮必须有 `aria-label`，装饰性图标 `aria-hidden`）
- 所有交互元素 Tab 可达，焦点可见
- 不用 `div` / `span` + `onclick` 冒充按钮，改用 `<button>`
- 模态打开时 trap focus，关闭后焦点回到触发元素
- Escape 可关闭 dialog / overlay

### 高（high）

- 不跳标题层级（h1→h3 是违规）
- 表单错误用 `aria-describedby` 关联到字段，`aria-invalid="true"`
- 必填字段有 `aria-required` 或 `<label>` 标注
- 禁用提交按钮要说明为什么禁用

### 中（medium）

- 文本对比度 ≥ 4.5:1（大字 ≥ 3:1）——用 axe / lighthouse 自动跑
- hover-only 交互有键盘等价
- 禁用状态不只靠颜色区分
- `prefers-reduced-motion` 下非必要动效停止

**工具**：`npx @axe-core/cli <url>` 或浏览器 axe DevTools。

## 4. 动效性能（build）

只在用户或需求明确要求时加动效；默认不动。

### 关键（critical）

- 只动 compositor 属性（`transform`、`opacity`），不动 layout（`width`、`height`、`top`、`left`、`margin`、`padding`）
- 不在同一帧交错读写 layout（layout thrashing）
- 不用 `scrollTop` / `scrollY` / scroll 事件驱动动画，用 `scroll-timeline` / `IntersectionObserver`
- 不持续动画大面积 `blur()` 或 `backdrop-filter`

### 高（high）

- 交互反馈动效 ≤ 200ms，入场用 `ease-out`
- 离屏时暂停循环动画（`IntersectionObserver`）
- `will-change` 只在活跃动画期间用，用完移除
- `prefers-reduced-motion` 时降级或停止

### 检查方法

```bash
# Chrome DevTools Performance 录制 → 检查没有紫色 layout 条
# 或 Lighthouse Performance 跑一次
npx lighthouse <url> --only-categories=performance --output=json --output-path=./lh.json
```

## 5. 交互三态验证模板

verify 阶段每个关键交互至少三态验证（截图确认或断言三态的测试）：

```
loading   — 确认骨架屏/aria-busy="true" 渲染正确
empty     — 确认空状态渲染且含一个明确 CTA
error     — 确认错误状态渲染正确
```

高风险交互额外补：disabled、success、focus 各一份。

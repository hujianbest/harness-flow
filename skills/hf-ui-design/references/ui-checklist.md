# UI 检查清单

进入构建阶段前逐项自查；验证阶段逐项核对证据。每项都给出“为什么”和“怎么查”。

## 1. 反 AI 粗制滥造视觉（规划 + 验证）

| 检查项 | 为什么 | 怎么查 |
|--------|--------|--------|
| 无无理由渐变主色 | AI 默认审美暴露 | 搜 `gradient` / `bg-gradient`，每个都要能回指需求或 decisions.md |
| 无紫色 / 紫蓝默认主色 | 最常见的 AI 配色惯性 | 检查主色令牌值是否落在 `oklch(0.5+ 0.2+ 270-300)` 或 `hsl(240-280)` |
| 无表情符号充当功能图标 | 不专业、跨平台不一致 | 搜索出现在 `icon` / `button` 上下文中的表情符号 Unicode 范围 |
| 无大面积玻璃拟态模糊 | 性能差 + 视觉廉价 | 搜索 `backdrop-blur`，只允许小面积使用（如单个徽标） |
| 无发光效果充当主要交互提示 | 可发现性差 | 搜索 `shadow` + `blur` 组合及 `drop-shadow` |
| 空状态有 CTA | 用户不知道下一步 | 每个 empty state 截图里能看到一个按钮或链接 |
| 每个元素回指需求 | 防止出现“凑数”组件 | 抽查 3 个分区，指出其对应 `product.md` / `plan.md` 中的具体条目 |

## 2. 令牌纪律（构建）

| 检查项 | 为什么 | 怎么查 |
|--------|--------|--------|
| 无硬编码颜色 | 无法换肤、暗色模式断裂 | 搜索出现在 `className` 或 `style` 中的 `#[0-9a-fA-F]{3,8}`、`rgb(`、`hsl(`、`oklch(` |
| 无硬编码字号 | 排版节奏断裂 | 搜 `text-[`、`font-size:` 后跟数字 |
| 无硬编码间距 / 圆角 | 密度系统断裂 | 搜 `p-[`、`m-[`、`rounded-[`、`gap-[` 后跟数字 |
| 有 `DESIGN.md` 时从其中取值 | 单一事实源 | 对比规划中的令牌表与 `DESIGN.md` 的前置元数据 |
| 无 `DESIGN.md` 时规划中有令牌表 | 临时内容也必须命名 | `plan.md` 的 UI 设计一节中有已命名的令牌列表 |

## 3. 可访问性（规划 + 验证）

优先用原生 HTML，只在原生不够时加 ARIA。

### 关键

- 每个交互控件都有可访问名称（纯图标按钮必须有 `aria-label`，装饰性图标须有 `aria-hidden`）
- 所有交互元素 Tab 可达，焦点可见
- 不用 `div` / `span` + `onclick` 冒充按钮，改用 `<button>`
- 模态框打开时限制焦点范围，关闭后焦点回到触发元素
- Escape 键可以关闭对话框 / 覆盖层

### 高

- 不跳标题层级（h1→h3 是违规）
- 表单错误用 `aria-describedby` 关联到字段，`aria-invalid="true"`
- 必填字段有 `aria-required` 或 `<label>` 标注
- 禁用提交按钮要说明为什么禁用

### 中

- 文本对比度 ≥ 4.5:1（大字 ≥ 3:1）——使用 axe / Lighthouse 自动检查
- 仅悬停触发的交互具有等效键盘操作
- 禁用状态不只靠颜色区分
- `prefers-reduced-motion` 下非必要动效停止

**工具**：`npx @axe-core/cli <url>` 或浏览器 axe DevTools。

## 4. 动效性能（构建）

只在用户或需求明确要求时加动效；默认不动。

### 关键

- 只对合成器属性（`transform`、`opacity`）应用动画，不对布局属性（`width`、`height`、`top`、`left`、`margin`、`padding`）应用动画
- 不在同一帧中交错读写布局，以免造成布局抖动
- 不使用 `scrollTop` / `scrollY` / 滚动事件驱动动画，改用 `scroll-timeline` / `IntersectionObserver`
- 不持续动画大面积 `blur()` 或 `backdrop-filter`

### 高

- 交互反馈动效 ≤ 200ms，入场使用 `ease-out`
- 离屏时暂停循环动画（`IntersectionObserver`）
- `will-change` 只在活跃动画期间用，用完移除
- `prefers-reduced-motion` 时降级或停止

### 检查方法

```bash
# 使用 Chrome DevTools 的 Performance 面板录制 → 检查没有紫色布局条
# 或运行一次 Lighthouse Performance
npx lighthouse <url> --only-categories=performance --output=json --output-path=./lh.json
```

## 5. 交互三态验证模板

验证阶段中，每个关键交互至少进行三态验证（截图确认或通过测试断言三态）：

```
loading   — 确认骨架屏/aria-busy="true" 渲染正确
empty     — 确认空状态渲染且含一个明确 CTA
error     — 确认错误状态渲染正确
```

高风险交互额外补充 `disabled`、`success`、`focus` 各一份。

# 样式、响应式与动效详表

> `frontend-development` 的 **样式与响应式 / 动效与运动性能** 维度深表。SKILL.md 承载红线，本文承载可直接套用的令牌体系与性能清单。

## 设计令牌：单一来源

把视觉决策收敛成命名令牌，组件引用令牌而非字面量——这样换主题、做暗色、保持一致都只改一处。

| 令牌类别 | 例子 | 反模式 |
|---|---|---|
| 颜色 | `--color-fg`、`--color-bg`、`--color-accent` | 各处散写 `#3b3b3b`、`rgb(...)` |
| 间距 | 比例尺 `4/8/12/16/24/32...` | 随手写 `13px`、`7px` |
| 字号/行高 | `text-sm/base/lg` + 对应行高 | 散写 `font-size: 15.5px` |
| 圆角/阴影 | `--radius-md`、`--shadow-card` | 每个卡片各调一套 |

- 语义令牌（`--color-fg`）映射到底层调色（`--gray-900`），主题切换只改映射层。
- 暗色/高对比通过令牌切换自动生效；**不要**在各组件里手写 `dark:` 覆盖魔法色值（必然漏改）。

```css
:root        { --color-fg: var(--gray-900); --color-bg: var(--gray-50); }
[data-theme="dark"] { --color-fg: var(--gray-50);  --color-bg: var(--gray-950); }
/* 组件只引用语义令牌 */
.card { color: var(--color-fg); background: var(--color-bg); }
```

## 响应式与移动优先

- 移动优先：基样式针对小屏，向上用断点增强，而非给大屏写基样式再往下打补丁。
- 用**动态视口单位**（`100dvh`）而非 `100vh`——移动端浏览器地址栏收放会让 `100vh` 溢出。
- 布局用 Grid/Flex，不用百分比 + 绝对定位硬算；容器查询适用于"组件随自身容器宽度自适应"。
- 触控目标至少约 44×44px（也是 a11y 要求）；可点区域不要小于视觉图标。
- 处理安全区（`env(safe-area-inset-*)`）避免内容被刘海/底部手势条遮挡。

```text
断点参考（随设计系统而定）
  base    < 640px   单列、堆叠
  md   >= 768px     两列、侧栏出现
  lg   >= 1024px    多列、固定侧栏
  xl   >= 1280px    内容最大宽度 + 居中留白
```

## 动效：只动 GPU 友好属性

| 可以动（合成层，便宜） | 不要动（触发重排/重绘，掉帧） |
|---|---|
| `transform`（translate/scale/rotate） | `width`/`height`、`top`/`left` |
| `opacity` | `margin`/`padding` |
| `filter` | `font-size` |
| `clip-path` | 改变文档流的几何属性 |

需要"移动/缩放"效果时用 `transform`，需要"展开"用 `transform: scaleY()` 或 `clip-path`，而不是动 `height`。

## 运动性能与清理

- **清理**：每个 `addEventListener`/`IntersectionObserver`/`ResizeObserver`/`requestAnimationFrame`/动画库 timeline 都要在 effect 返回里注销，否则泄漏 + 多重触发。
- **隔离**：持续运行的动画（呼吸点、跑马灯）放进 `React.memo` 叶子组件，避免父级重渲染连带；`will-change` 只在动画期间加，结束移除。
- **懒加载**：重动画/3D 库（GSAP、Three.js、Lottie 等）按需 `import()`，不要进首屏关键 bundle（与性能预算维度协同）。
- **节流**：`scroll`/`resize`/`mousemove` 处理器用 RAF 或节流，避免每帧多次重布局。

## 减动偏好与无障碍

- 尊重 `prefers-reduced-motion: reduce`：关闭或大幅减弱非必要动画（视差、自动轮播、夸张过渡），保留必要的状态反馈。
- 不让内容每秒闪烁 > 3 次（癫痫风险）。
- 自动播放的动画提供暂停手段；焦点可见环用 `outline` 而非仅靠 `box-shadow`。

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

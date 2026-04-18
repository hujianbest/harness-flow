# 可访问性检查清单（WCAG 2.2 AA）

UI 设计阶段必须逐项声明达成方式。不能只写"支持可访问性"。

## 1. 感知（Perceivable）

### 1.1 文本替代

- [ ] 非装饰图片有 `alt`；装饰性图片 `alt=""` 且 `role="presentation"`
- [ ] 图标按钮有无障碍名（`aria-label` 或可见文本）
- [ ] 复杂图表 / 数据可视化有 text alternative（data table、说明文字或 `aria-describedby`）

### 1.2 时序媒体

- [ ] 视频有字幕；音频有文字稿（若规格含媒体）
- [ ] 自动播放默认关闭或可一键关闭

### 1.3 可适应

- [ ] 语义 HTML：heading 层级连续、list 用 `ul`/`ol`、form 用 `label` 显式关联 `input`
- [ ] 不使用纯 CSS 布局破坏阅读顺序（`order` / `flex-direction: reverse` 需确保 DOM 顺序仍合理）
- [ ] 竖排 / 横排方向切换不丢失内容

### 1.4 可辨识

- [ ] **色彩对比**：正文 ≥ 4.5:1；18pt 或加粗 14pt 以上大字号 ≥ 3:1；UI 组件边界与状态指示 ≥ 3:1
- [ ] 不单纯依赖颜色传达信息（如错误必须有图标/文字，而非仅红色边框）
- [ ] 文本可放大到 200% 不丢失功能
- [ ] 行高 ≥ 1.5×字号；段间距 ≥ 2×字号（正文）

## 2. 可操作（Operable）

### 2.1 键盘可达

- [ ] 所有交互控件可通过 Tab / Shift+Tab / Enter / Space / 方向键操作
- [ ] 无键盘陷阱（焦点能进能出）
- [ ] 自定义组件（menu、combobox、tree、dialog）实现 WAI-ARIA Authoring Practices 对应键盘模式

### 2.2 足够时间

- [ ] 超时前警告用户，提供延长机制（若规格含会话超时）
- [ ] 自动刷新内容可暂停 / 停止 / 隐藏

### 2.3 癫痫与物理反应

- [ ] 闪烁内容低于每秒 3 次
- [ ] 尊重 `prefers-reduced-motion`，关闭非必要动效

### 2.4 可导航

- [ ] 提供跳过重复块的方式（"跳到主内容"链接）
- [ ] 页面有唯一且有意义的 `<title>`
- [ ] **focus 顺序**与视觉/阅读顺序一致
- [ ] 链接文本自说明（不是"点这里"）
- [ ] **focus 可见**：`:focus-visible` 样式不被全局 `outline: none` 消除

### 2.5 输入方式

- [ ] 点击目标最小 24×24px（WCAG 2.2 新增 `2.5.8 Target Size (Minimum)`）
- [ ] 拖拽操作有单击等价替代（WCAG 2.2 新增 `2.5.7 Dragging Movements`）

## 3. 可理解（Understandable）

### 3.1 可读

- [ ] `<html lang>` 声明语言
- [ ] 文本中外语片段用 `lang` 属性标注（若规格含多语）

### 3.2 可预测

- [ ] focus / input 不触发 context change（如自动提交、自动跳转）除非显式说明
- [ ] 导航在各页面位置一致

### 3.3 输入辅助

- [ ] 表单错误有 inline 提示 + `aria-describedby` 关联
- [ ] 重要动作（删除、支付、不可逆操作）有二次确认或撤销
- [ ] 自动完成字段使用 `autocomplete`（`email`、`tel`、`given-name` 等）
- [ ] 登录/注册字段支持密码管理器自动填充（WCAG 2.2 新增 `3.3.8 Accessible Authentication`）

## 4. 鲁棒（Robust）

### 4.1 兼容

- [ ] HTML 合法（开闭标签匹配、属性合法）
- [ ] ARIA 角色、状态、属性符合 WAI-ARIA 1.2 规范
- [ ] 状态变化（loading 结束、错误出现、选中变化）通过可访问性树暴露（`aria-live` / `aria-busy` / `aria-selected`）

## 在 UI 设计文档中的声明方式

不要只写"支持 WCAG AA"。至少列出：

```markdown
### 11. 可访问性（WCAG 2.2 AA）

| 类别 | 关键要求 | 在本设计的落地方式 | 备注 |
|---|---|---|---|
| 色彩对比 | 正文 ≥ 4.5:1 | 所有正文色 token 经计算均达标；详见 §7.2 | 亮/暗主题各自达标 |
| 键盘可达 | 全部控件可键盘操作 | 复用 shadcn/ui 组件（已内建）；新增组件遵循 ARIA APG | combobox 用 listbox 模式 |
| 焦点可见 | focus-visible 样式 | 全局 `:focus-visible` 用 `color.focus.ring` token 2px ring | 不使用 `outline: none` |
| 语义结构 | heading 层级、label 关联 | heading 按页面信息架构分配 h1-h3，详见 §8 wireframe | |
| reduced motion | 尊重用户偏好 | 所有 motion token 在 `prefers-reduced-motion: reduce` 下降级为 0ms 或替代呈现 | |
| 目标大小 | ≥ 24×24px | Button / IconButton / Tab token 最小尺寸 40×40 | 移动端手势区 44×44 |
| 错误提示 | 非仅颜色 | error 态 = 红色 + `!` 图标 + inline 文字 + `aria-describedby` | |
| 表单自动填充 | `autocomplete` | 登录/注册/结算表单字段均声明 | |
```

对每一行必须能 **冷读出"这个要求在哪里落地"**，而不是只写"达成"。

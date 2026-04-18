# UI 设计文档模板

若 `AGENTS.md` 为当前项目声明了 UI 设计模板，优先使用项目约定。以下为默认结构。

## 默认结构

```markdown
# <主题> UI 设计

- 状态: 草稿
- 主题: <主题>
- Peer: 对应 hf-design 文档路径

## 1. 概述与范围
## 2. UI 驱动因素（规格映射 + UX NFR）
## 3. 信息架构（站点地图 / 导航结构 / 内容分组）
## 4. 关键用户流（User Flow，含异常与回退路径）
## 5. 候选视觉 / 交互方向与对比
## 6. 选定方向与关键 UI 决策（ADR 摘要）
## 7. 视觉系统（Design Token 映射）
   - 7.1 Typography
   - 7.2 Color（含 semantic tokens）
   - 7.3 Spacing / Layout grid
   - 7.4 Radius / Elevation / Shadow
   - 7.5 Motion（时长、缓动、reduced-motion 策略）
## 8. 关键页面 wireframe
## 9. Atomic 组件映射（Atoms / Molecules / Organisms / Templates / Pages）
## 10. 交互状态矩阵（关键交互 × 状态集合）
## 11. 可访问性（WCAG 2.2 AA 声明）
## 12. 响应式与多端（若规格含要求）
## 13. i18n / 国际化（若规格含要求）
## 14. 前端性能预算（若规格含要求）
## 15. Microcopy 与语气
## 16. 与 hf-design 的 peer 依赖交接
## 17. 任务规划准备度（task planning readiness）
## 18. 明确排除与延后项
## 19. 风险与开放问题（区分阻塞 / 非阻塞）
```

## 编写要求

- 区分规格层（做什么）、UI 设计层（界面如何承载）、任务层（分步实施）
- 所有视觉决策走 token；不写硬编码色值 / 字号 / 间距
- 至少保留一个紧凑的候选方向对比视图，不让 reviewer 只能从 prose 猜 trade-off
- 每个关键交互至少覆盖 loading / empty / error 三态
- 关键页面至少给一份可冷读的 wireframe（Mermaid / ASCII / 文字布局 / 外链图均可）
- 提供足够支撑任务拆解的组件粒度与状态矩阵，但不要写成前端源码

## 候选方向最小对比视图

若项目模板未声明更强结构，`## 5. 候选视觉 / 交互方向与对比` 默认至少提供一个紧凑矩阵：

```markdown
| 方向 | 风格主张 | typography | 色彩策略 | 空间/密度 | 动效策略 | NFR / 约束匹配 | 主要风险 | 可逆性 |
|------|----------|-----------|---------|-----------|---------|--------------|---------|--------|
| A | ... | ... | ... | ... | ... | ... | ... | 高 / 中 / 低 |
| B | ... | ... | ... | ... | ... | ... | ... | 高 / 中 / 低 |
```

至少满足：

- 比较 2 个及以上真实可行方向，不是"推荐方向 + 稻草人"
- `主要风险` 不能留空
- `NFR / 约束匹配` 显式承接规格中的可用性 / a11y / i18n / 响应式 / 性能预算要求
- `可逆性` 与 ADR 口径一致
- 若复用既有 Design System，也把"沿用现状"作为候选方向之一写入矩阵

## 视觉系统（token）最小声明

```markdown
### 7.2 Color

| Token | Light | Dark | 用途 |
|-------|-------|------|------|
| color.bg.default | #FFFFFF | #0B0B0F | 页面背景 |
| color.fg.default | #111827 | #F3F4F6 | 正文字色 |
| color.primary | #2B6CB0 | #63B3ED | 主操作 |
| color.danger | #C53030 | #FC8181 | 危险操作 / 错误 |
| ... | ... | ... | ... |
```

确认：

- 对比度满足 WCAG AA（正文 ≥ 4.5:1，大字号 ≥ 3:1，非文本 UI 组件与状态指示 ≥ 3:1）
- 亮 / 暗主题一致（或显式声明只支持其中之一）
- 语义 token（success / warning / danger / info）单独列出，不让语义色复用主色

## 保存路径

默认：`docs/designs/YYYY-MM-DD-<topic>-ui-design.md`

若 `AGENTS.md` 声明了 UI 设计路径映射，优先使用映射路径。

## 状态同步

UI 设计草稿交评审后，应同步：

- UI 设计文档状态（`状态: 草稿`）
- `task-progress.md` 中的 `Current Stage: hf-ui-design`
- `task-progress.md` 中的 `Next Action Or Recommended Skill: hf-ui-review`

## 与 hf-design 的 peer 依赖交接块

在 `## 16. 与 hf-design 的 peer 依赖交接` 中至少写明：

```markdown
### 16.1 本文档依赖 hf-design 锁定的条目

- [待锁] API 错误返回的结构（影响 error 态 UI）
- [已锁] 鉴权失败的 401 流程（影响登录跳转 UI）

### 16.2 本文档已锁定、可供 hf-design 依赖的条目

- [已锁] 表单校验反馈时序（前端即时 + 后端最终校验）
- [已锁] 列表分页模式（游标分页，影响 API 契约）

### 16.3 冲突或待协商

- 无 / 或列出冲突项与建议处置
```

parallel 模式下，reviewer 将依据此交接块判断两条设计是否已对齐到可联合 approval 的程度。

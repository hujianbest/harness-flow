---
name: ext-design-md
description: DESIGN.md 设计令牌规范扩展。绑定阶段: architect、ship。触发条件: 项目含用户界面且选择建立设计令牌单一事实源。在架构阶段用证据驱动创建 DESIGN.md，在 ship 阶段把验收后的设计变更回写，保证 token 系统与实现同步。
---

# DESIGN.md 设计令牌规范扩展

## 绑定

- 绑定阶段: architect、ship
- 触发条件: 项目含用户界面，且用户选择建立设计令牌单一事实源（或项目根已有 `DESIGN.md`）

## 为什么需要这个扩展

`ext-ui-design` 在 plan/build/verify 阶段要求"视觉决策落到 token"。本扩展解决 token 从哪来：在 architect 阶段从**既有代码证据**提取 token 规范写入 `DESIGN.md`，让它成为全项目的设计令牌单一事实源，后续特性的 UI 决策都从这里取值。

## 架构阶段 (architect) 规则

### 创建决策

进入 architect 时判断：

1. 项目根已有 `DESIGN.md` → 跳过创建，但在 architecture.md 的"横切约定"里引用它
2. 项目有 UI 但无 DESIGN.md → 向用户提议创建（记录到 `assumptions.md`），获确认后执行下述流程
3. 项目无 UI → 本扩展不适用

### 证据驱动提取（不做审美发明）

DESIGN.md 记录**已有产品的设计语言**，不是重新设计。流程：

1. **冷读代码**：按以下顺序找证据——既有 `DESIGN.md` / 设计文档 → token / theme / CSS 变量文件 → 共享组件 primitives 及其 variants → 代表性路由的渲染消费方 → 页面局部实现
2. **只记录有管辖权的值**：一个值进入 DESIGN.md 当且仅当——它被项目 import / reference / inherit / render；排除提案、迁移、示例、生成物、legacy
3. **只写命名 token**：不把 utility class、重复字面量、组件局部值升格为 token scale
4. **格式契约**：frontmatter 用 mapping 不用 sequence，typography 子项用 `fontFamily` / `fontSize` / `lineHeight` / `fontWeight`（不用 `font-family` / 嵌套 source 对象）

### Frontmatter 最小结构

```yaml
---
version: alpha
name: <产品名>
description: <一句话>
---
```

按需加 `colors` / `typography` / `rounded` / `spacing` / `components`，**仅当**既有代码已定义该命名系统。不为了"完整"而发明 token。

### 正文节序（严格遵守）

Overview → Colors → Themes → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts。只为有证据的节建标题，不补空节。

### 验证（必须通过才能离开 architect）

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format <css-tailwind|json-tailwind|dtcg> DESIGN.md
```

每个有值的 frontmatter 类别在 export 输出里必须有对应 token 族；export 为空 = schema 失败，必须修 frontmatter 后重跑。export 产物不留存。

### 与 architecture.md 的关系

- `architecture.md` 的"横切约定"节引用 `DESIGN.md` 路径（一行）
- 不在 architecture.md 复述 token 值（单一事实源）

## ship 阶段规则

特性交付引入设计变更时（新 token、改值、废弃 token）：

1. 用既有证据或本特性的渲染证据更新 `DESIGN.md`
2. 重跑 lint + export 验证
3. 更新记入 ship 报告的"反馈回写产品层"条目

## 约束

- 只修改 `DESIGN.md`，不改产品源码做"对齐"（那是 build 阶段的事）
- 不把重复、局部样式、视觉偏好升格为产品意图
- 不发明品牌个性、受众、情感理由
- URL 模式（无源码时）需要渲染浏览器访问，从计算样式和已加载 stylesheet 取值，不从截图估读

## 评审检查项

- [ ] (architect) DESIGN.md 创建决策记入 assumptions.md
- [ ] (architect) frontmatter 用 mapping 格式，typography 子项用规范字段名
- [ ] (architect) lint + export 通过，每个有值类别都有对应 token 族输出
- [ ] (architect) architecture.md 引用了 DESIGN.md 路径
- [ ] (ship) 设计变更已回写 DESIGN.md 并重新验证

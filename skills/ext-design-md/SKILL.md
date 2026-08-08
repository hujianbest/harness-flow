---
name: ext-design-md
description: DESIGN.md 设计令牌规范扩展。绑定阶段: to-architecture、ship。触发条件: 项目含用户界面且选择建立设计令牌单一事实源。在架构阶段用证据驱动创建或引用 DESIGN.md，在 ship 阶段把验收后的设计变更回写，保证 token 系统与实现同步。
---

# DESIGN.md 设计令牌规范扩展

## 绑定

- 绑定阶段: to-architecture、ship
- 触发条件: 项目含用户界面，且用户选择建立设计令牌单一事实源（或项目根已有 `DESIGN.md`）

## 为什么需要本扩展

`ext-ui-design` 要求视觉决策落到 token。本扩展解决 token 从哪来：在 `hf-to-architecture` 从**既有代码证据**提取或引用 `DESIGN.md`，作为全项目令牌单一事实源。

## 架构阶段 (to-architecture) 规则

### 创建决策

1. 项目根已有 `DESIGN.md` → 跳过创建，在 `architecture.md` 横切约定中引用
2. 有 UI 无 DESIGN.md → 提议创建（记入 `product/assumptions.md`），确认后执行提取
3. 无 UI → 不适用

### 证据驱动提取

1. 冷读顺序：既有 DESIGN.md → token/theme/CSS 变量 → 共享 primitives → 代表性路由
2. 只记录有管辖权的值（被 import/reference/inherit/render）
3. 只写命名 token，不把 utility/局部字面量升格
4. frontmatter 用 mapping；typography 用 `fontFamily` / `fontSize` / `lineHeight` / `fontWeight`

### 验证

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format css-tailwind DESIGN.md
```

export 为空 = schema 失败，须修后重跑。

## Ship 阶段规则

验收后的视觉变更若改变 token 语义，回写 `DESIGN.md` 并再 lint；不得只改代码不改规范。

---
name: ext-design-md
description: DESIGN.md 设计令牌规范扩展。绑定阶段: to-architecture、ship。触发条件: 项目含用户界面且选择建立设计令牌单一事实源。在架构阶段用证据驱动创建或引用 DESIGN.md，在 ship 阶段把验收后的设计变更回写，保证令牌系统与实现同步。
---

# DESIGN.md 设计令牌规范扩展

## 绑定

- 绑定阶段: to-architecture、ship
- 触发条件: 项目含用户界面，且用户选择建立设计令牌单一事实源（或项目根已有 `DESIGN.md`）

## 为什么需要本扩展

`ext-ui-design` 要求视觉决策落实到令牌。本扩展解决令牌从何而来：在 `hf-to-architecture` 中根据**既有代码证据**提取或引用 `DESIGN.md`，将其作为全项目令牌的单一事实源。

## 架构阶段 (to-architecture) 规则

### 创建决策

1. 项目根已有 `DESIGN.md` → 跳过创建，在 `architecture.md` 横切约定中引用
2. 有 UI 但无 `DESIGN.md` → 提议创建（记入 `product/assumptions.md`），确认后执行提取
3. 无 UI → 不适用

### 证据驱动提取

1. 冷读顺序：既有 `DESIGN.md` → 令牌/主题/CSS 变量 → 共享基础组件 → 代表性路由
2. 只记录有管辖权的值（被导入/引用/继承/渲染）
3. 只写命名令牌，不把工具类/局部字面量升格
4. 前置元数据使用映射；排版使用 `fontFamily` / `fontSize` / `lineHeight` / `fontWeight`

### 验证

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format css-tailwind DESIGN.md
```

导出结果为空 = 模式校验失败，须修复后重新运行。

## Ship 阶段规则

验收后的视觉变更若改变令牌语义，回写 `DESIGN.md` 并再次运行检查；不得只改代码而不改规范。

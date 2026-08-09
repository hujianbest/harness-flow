# 产品层模板（绿地首次落盘）

由 `hf-grill-with-docs` 在无产品层时**手工创建**（不覆盖已有文件）。无 `hf_gate.py`。

## 目录

```
CONTEXT.md
product/
  assumptions.md
  decisions.md
  architecture.md      # 可由 hf-to-product-architecture 填写
  progress.md
  reviews/
docs/adr/
features/
```

## CONTEXT.md

```markdown
# CONTEXT

项目领域共享语言（术语表）。由 hf-grill-with-docs / hf-domain-modeling 维护。

- 用户确认:

## 术语

<!-- 术语 — 定义 -->
```

## product/assumptions.md

```markdown
# 假设台账

智能体替用户做的默认选择。标准动作: 提出带默认值的选项 → 记录 → 继续。
状态: 生效 | 已确认 | 已推翻
格式: `- A-<n> <日期> [状态] <假设内容> — 默认理由: <一句话>`
```

## product/decisions.md

```markdown
# 决策记录

已确认决策(用户确认或从假设台账迁入)。只追加。
格式: `- D-<n> <日期> <决策内容> — 依据: <一句话>`
```

## product/architecture.md

```markdown
# 产品架构

系统级架构地图（非特性实现设计）。由 hf-to-product-architecture 维护；≤120 行。

- 日期:
- 用户确认:

## 原则与风格
## 逻辑划分
## 开发视图
## 关键场景
## 横切与 ADR
```

## product/progress.md

```markdown
# 进度
- 当前阶段: grill-with-docs | to-product-architecture | ready
- 执行模式: interactive | auto
- 下一步: <一句话>
```

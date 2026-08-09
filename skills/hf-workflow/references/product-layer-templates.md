# 产品层模板（绿地首次落盘）

由 `hf-grill-with-docs` 在无产品层时**手工创建**（不覆盖已有文件）。

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

## 架构特征
<!-- 3~5 个驱动性质量属性，各配一条可检验场景（刺激→响应→度量） -->
## 原则与风格
<!-- 风格 + 依赖硬规则；声明如何服务上述特征 -->
## 逻辑划分
<!-- 3~7 模块/上下文：一句话职责 + 封住的易变性 -->
## 开发视图
<!-- 目录/测试放置/命名；「新代码放哪」须唯一显然 -->
## 关键场景
<!-- 2~5 条端到端路径；标注各自验证的特征 -->
## 横切与 ADR
## 演进与适应度
<!-- 易变性的演进路径、量化复核触发、适应度函数（校验方式/频率） -->
```

## product/progress.md

```markdown
# 进度
- 当前阶段: grill-with-docs | to-product-architecture | ready
- 执行模式: interactive | auto
- 下一步: <一句话>
```

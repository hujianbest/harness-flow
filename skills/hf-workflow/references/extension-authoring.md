# 编写扩展技能（ext-*）

扩展把领域要求注入主链特定阶段。主链不为扩展改代码——靠约定被 `hf-workflow` 发现加载。

## 目录与命名

```
skills/ext-<领域名>/
  SKILL.md
  references/   # 可选
```

## SKILL.md

```markdown
---
name: ext-<领域名>
description: <一句话> 绑定阶段: <合法阶段子集>。触发条件: <…>。
---
```

## 合法绑定阶段

`grill-with-docs` / `to-product-architecture` / `to-spec` / `to-architecture` / `to-tickets` / `implement` / `code-review` / `ship` / `close`

## 硬性约束

- `description` 必须包含「绑定阶段」与「触发条件」
- **只收紧建议，不放松评审/TDD 纪律**
- 正文 ≤ 150 行；可判定规则；不复述主链
- `python3 scripts/validate_skills.py` 须通过

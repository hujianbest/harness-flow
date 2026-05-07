# Persona Anatomy — HF Agent Persona 写作原则

- 定位：项目级原则文档（design reference，不作合规基线，与 `skill-anatomy.md` 同级），定义 HF agent persona 的目标态写法。
- 来源：ADR-002 D4 / D8（user-facing personas as orchestration shortcuts over review skills）。
- 关联：
  - 灵魂文档（最高锚点）：`docs/principles/soul.md`
  - SKILL.md anatomy：`docs/principles/skill-anatomy.md`
  - HF family 运行时共享约定：`skills/hf-workflow-router/references/workflow-shared-conventions.md`

## 定位

本文定义 HF agent persona 的目标态写法。

HF persona 是用户可见的 **orchestration shortcut**，把"我想要一个 staff reviewer / qa engineer / security auditor"这类高频意图直接绑到一个 persona 文件，由 persona 内部的指令把请求委派给一组 `hf-*-review` skill。

关键定位（与 SKILL.md 的硬区别）：

- **persona 不是 workflow node**，不参与 `hf-workflow-router` 的 FSM 编排；它在用户与 router/skill 之间多加一层 facade。
- **persona 不替代 review skill 产出 verdict**。所有"通过 / 不通过"的工程判断仍由 `hf-*-review` skill 产出，persona 只做合并展示。
- **persona 不调 implementation / authoring skill**，也不能编辑被审对象——保持 Fagan 作者与评审者分离。
- **persona 不写 SKILL.md 那种节点契约**（`Object Contract` / `Methodology` / `Workflow` 等），它的职责更窄。
- **persona 不进 anatomy audit script** 的检查范围（ADR-002 D5 / D8）。

## 文件位置与命名

- Personas 居于仓库根的 `agents/` 目录（与 AS 0.6.0 一致）。
- 命名规则：`agents/hf-<role>.md`，如 `agents/hf-staff-reviewer.md`。
- 与 `skills/hf-*/SKILL.md` 的命名空间显式区分，避免 audit script 误判。

## 推荐结构

```markdown
---
name: hf-<role>
description: <一句祈使句：什么时候找这个 persona>
---

# <Persona Title>

<1-2 句：这个 persona 的角色定位 + 不替代什么>

## 调用场景

<什么用户意图会触发这个 persona>

## 委派的 review skill

| 场景 | 委派到 | 产出 |
|---|---|---|
| ... | `hf-*-review` | finding set / verdict |

## 输出格式

<合并多个 review skill verdict 的展示模板>

## 不做什么

- 不替代 review skill 产出 verdict
- 不调 implementation / authoring skill
- 不编辑被审对象
- 不修改 spec / design / tasks / code

## 调用示例
```

最小 persona 可以只保留：frontmatter / 开场 / 「调用场景」 / 「委派的 review skill」 / 「不做什么」。

## Frontmatter

```yaml
---
name: hf-<role>
description: Use when <user intent>. Not for <reverse boundary>.
---
```

要求：

- `name` 与文件名一致（不含 `.md`）。
- `description` 是分类器，不是摘要——只回答"现在该不该把 persona 加载进来"。
- 触发条件优先用祈使句，且把"不做什么"放在 `Not for` 中显式收口。

## 与 SKILL.md 的最低差异清单

| 维度 | SKILL.md | Persona |
|---|---|---|
| 路径 | `skills/<name>/SKILL.md` | `agents/<name>.md` |
| 编排角色 | workflow node（authoring / review / gate / impl / finalize / side） | orchestration shortcut |
| 契约层 | `Object Contract` / `Methodology` / `Workflow` 必需 | 不写节点契约 |
| Hard Gates / Verification | 必需 | 不写（gate / verdict 由委派的 review skill 负责）|
| Common Rationalizations | v0.2.0 起必需 | 按需（不强制）|
| audit script | 受 `audit-skill-anatomy.py` 检查 | **不**受检查（ADR-002 D5）|
| 用户面命令绑定 | slash 命令 bias 到具体 skill | persona 文件本身就是用户调用入口 |

## 不让步（与 soul.md 一致）

- persona 不能替用户定方向、做取舍、改标准、验收自己。
- 凡涉及"是否通过"，必须 surface 委派 review skill 的 verdict 与证据，不能由 persona 自行折算。
- 多个 review skill verdict 冲突时，persona 必须如实展示冲突，不能自行裁决。

## 验证

新增或修改 persona 时至少检查：

- 是否在 `agents/` 下，命名为 `hf-<role>.md`。
- frontmatter 是否含 `name` 与 `description`，且 `description` 是分类器写法。
- 是否清楚列出"委派的 review skill"。
- 是否清楚列出"不做什么"，且与 SKILL.md / soul.md 的 Fagan 角色分离一致。
- 是否给出一个最简调用示例。

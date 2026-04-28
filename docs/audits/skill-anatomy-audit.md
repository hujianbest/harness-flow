# HF SKILL.md Anatomy 审计报告

- 来源标准：`docs/principles/02 skill-anatomy.md` § 检查清单
- 关联决策：`docs/decisions/ADR-001-release-scope-v0.1.0.md`
- 生成器：`scripts/audit-skill-anatomy.py`（只读）
- 审计 SKILL.md 数：24
- 通过 hard checks：0 / 24

## 摘要

| 指标 | 数量 | 占比 |
|---|---:|---:|
| 通过全部 hard checks | 0 | 0% |
| 超 token 预算 | 0 | 0% |
| 超行预算 | 0 | 0% |
| workflow skill 缺 Object Contract | 24 | 100% |
| workflow skill 缺 Methodology | 0 | 0% |
| 缺 Red Flags | 0 | 0% |
| 缺 Common Rationalizations（ADR-001 D8 要求） | 24 | 100% |

## 每个 Skill 的明细

| Skill | hard | lines | ~tokens | Obj | Meth | RF | CR | 备注 |
|---|:-:|---:|---:|:-:|:-:|:-:|:-:|---|
| `hf-bug-patterns` | ❌ | 191 | 987 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-code-review` | ❌ | 156 | 2150 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-completion-gate` | ❌ | 165 | 1690 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-design` | ❌ | 326 | 3838 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-design-review` | ❌ | 151 | 1165 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-discovery-review` | ❌ | 121 | 929 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-doc-freshness-gate` | ❌ | 177 | 2512 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-experiment` | ❌ | 203 | 1714 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-finalize` | ❌ | 266 | 2264 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-hotfix` | ❌ | 185 | 1097 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-increment` | ❌ | 262 | 1616 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-product-discovery` | ❌ | 208 | 2175 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-regression-gate` | ❌ | 140 | 1097 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-spec-review` | ❌ | 133 | 1073 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-specify` | ❌ | 273 | 2910 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-tasks` | ❌ | 173 | 1246 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-tasks-review` | ❌ | 134 | 1174 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-test-driven-dev` | ❌ | 239 | 3129 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-test-review` | ❌ | 134 | 1164 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-traceability-review` | ❌ | 143 | 1157 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-ui-design` | ❌ | 360 | 3777 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-ui-review` | ❌ | 180 | 1758 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `hf-workflow-router` | ❌ | 181 | 1565 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |
| `using-hf-workflow` | ❌ | 158 | 1442 | ❌ | ✅ | ✅ | ❌ | workflow skill 缺 `Object Contract`；缺 `Common Rationalizations`（ADR-001 D8 要求 v0.1.0 全量补齐） |

## 整改优先级建议

P0（v0.1.0 阻塞，发版前必须修复）：
- `hf-bug-patterns`：缺 Object Contract
- `hf-code-review`：缺 Object Contract
- `hf-completion-gate`：缺 Object Contract
- `hf-design`：缺 Object Contract
- `hf-design-review`：缺 Object Contract
- `hf-discovery-review`：缺 Object Contract
- `hf-doc-freshness-gate`：缺 Object Contract
- `hf-experiment`：缺 Object Contract
- `hf-finalize`：缺 Object Contract
- `hf-hotfix`：缺 Object Contract
- `hf-increment`：缺 Object Contract
- `hf-product-discovery`：缺 Object Contract
- `hf-regression-gate`：缺 Object Contract
- `hf-spec-review`：缺 Object Contract
- `hf-specify`：缺 Object Contract
- `hf-tasks`：缺 Object Contract
- `hf-tasks-review`：缺 Object Contract
- `hf-test-driven-dev`：缺 Object Contract
- `hf-test-review`：缺 Object Contract
- `hf-traceability-review`：缺 Object Contract
- `hf-ui-design`：缺 Object Contract
- `hf-ui-review`：缺 Object Contract
- `hf-workflow-router`：缺 Object Contract
- `using-hf-workflow`：缺 Object Contract

P1（ADR-001 D8 要求 v0.1.0 全量补 anti-rationalization）：
- `hf-bug-patterns` — 增加 `## Common Rationalizations` 表
- `hf-code-review` — 增加 `## Common Rationalizations` 表
- `hf-completion-gate` — 增加 `## Common Rationalizations` 表
- `hf-design` — 增加 `## Common Rationalizations` 表
- `hf-design-review` — 增加 `## Common Rationalizations` 表
- `hf-discovery-review` — 增加 `## Common Rationalizations` 表
- `hf-doc-freshness-gate` — 增加 `## Common Rationalizations` 表
- `hf-experiment` — 增加 `## Common Rationalizations` 表
- `hf-finalize` — 增加 `## Common Rationalizations` 表
- `hf-hotfix` — 增加 `## Common Rationalizations` 表
- `hf-increment` — 增加 `## Common Rationalizations` 表
- `hf-product-discovery` — 增加 `## Common Rationalizations` 表
- `hf-regression-gate` — 增加 `## Common Rationalizations` 表
- `hf-spec-review` — 增加 `## Common Rationalizations` 表
- `hf-specify` — 增加 `## Common Rationalizations` 表
- `hf-tasks` — 增加 `## Common Rationalizations` 表
- `hf-tasks-review` — 增加 `## Common Rationalizations` 表
- `hf-test-driven-dev` — 增加 `## Common Rationalizations` 表
- `hf-test-review` — 增加 `## Common Rationalizations` 表
- `hf-traceability-review` — 增加 `## Common Rationalizations` 表
- `hf-ui-design` — 增加 `## Common Rationalizations` 表
- `hf-ui-review` — 增加 `## Common Rationalizations` 表
- `hf-workflow-router` — 增加 `## Common Rationalizations` 表
- `using-hf-workflow` — 增加 `## Common Rationalizations` 表

## 抛回架构师的方向题（HF 不替你定）

下列发现**改变 skill 行为契约**而不仅是文档润色，按 `docs/principles/00 soul.md` 「方向 / 取舍 / 标准的最终权在用户」，需要你拍板后才能进入实现：

- **Q1 — Object Contract 全量缺位（24/24 workflow skills）**：`docs/principles/02 skill-anatomy.md` 把 `## Object Contract` 列为 workflow skill **必备段**（写明 Primary / Frontend Input / Backend Output Object 与 Object Transformation）。当前**没有任何一个** SKILL.md 写了。v0.1.0 是否把它作为发版门禁？候选：
  - **A. 严格执行**：v0.1.0 前给 24 个 SKILL.md 全部补 Object Contract。工作量大、改动 contract、需逐个评审；但符合现行 anatomy 标准。
  - **B. 暂时降级**：把`02 skill-anatomy.md` 中 Object Contract 改为 v0.1.0 「推荐」、v0.2.0 升级为「必备」。anatomy 标准放宽，发版速度快；但与 anatomy 文档现有口径冲突，需同时改 `02 skill-anatomy.md`。
  - **C. 折中**：v0.1.0 仅给 router / TDD / 三个 gate / finalize 等 **核心 7 节点** 补；其余下沉到 v0.2.0。需要在 ADR 中显式列出「核心 7 节点」清单。
- **Q2 — Common Rationalizations 全量缺位（24/24）**：ADR-001 D8 已锁定「v0.1.0 全量补」，**此项已决，无需再问**。本审计仅作为整改基线。

## 方法学说明

- Hard checks 等价于 `02 skill-anatomy.md` 检查清单的「不可协商」部分（identity / sections / workflow shape / budget）。
- Common Rationalizations 在 v0.1.0 之前不是 hard check，但因 ADR-001 D8 决议而成为发版门禁。
- token 估算用 `len(text)/4` 的粗略比例，仅用于发现违反预算的离群值；精确 token 数请按所用 tokenizer 复算。
- 本脚本只读，不修改任何 SKILL.md；整改由后续 PR 显式完成。

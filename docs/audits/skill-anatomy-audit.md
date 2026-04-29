# HF SKILL.md Anatomy 审计报告

- 来源标准：`docs/principles/skill-anatomy.md` § 检查清单
- 关联决策：`docs/decisions/ADR-001-release-scope-v0.1.0.md`
- 生成器：`scripts/audit-skill-anatomy.py`（只读）
- 审计 SKILL.md 数：24
- 通过 hard checks（anatomy 必需段）：24 / 24
- 通过 v0.1.0 release gate（hard + Common Rationalizations）：0 / 24

## 摘要

| 指标 | 数量 | 占比 |
|---|---:|---:|
| 通过 anatomy hard checks | 24 | 100% |
| 通过 v0.1.0 release gate（hard + CR） | 0 | 0% |
| 超 token 预算 | 0 | 0% |
| 超行预算 | 0 | 0% |
| workflow skill 缺 Methodology（必需） | 0 | 0% |
| 缺 Red Flags（必需） | 0 | 0% |
| workflow skill 缺 Common Rationalizations（v0.1.0 release gate） | 24 | 100% |
| workflow skill 缺 Object Contract（v0.1.0 推荐 / v0.2.0 必需） | 24 | 100% |

## 每个 Skill 的明细

列定义：`hard` = anatomy 必需段全部满足；`gate` = hard + Common Rationalizations（v0.1.0 发版门禁）；`Obj` = Object Contract （v0.1.0 推荐，缺位不计入 hard fail）。

| Skill | hard | gate | lines | ~tokens | Meth | RF | CR | Obj | 备注 |
|---|:-:|:-:|---:|---:|:-:|:-:|:-:|:-:|---|
| `hf-bug-patterns` | ✅ | ❌ | 191 | 986 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-code-review` | ✅ | ❌ | 156 | 2146 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-completion-gate` | ✅ | ❌ | 165 | 1693 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-design` | ✅ | ❌ | 327 | 3947 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-design-review` | ✅ | ❌ | 151 | 1162 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-discovery-review` | ✅ | ❌ | 121 | 924 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-doc-freshness-gate` | ✅ | ❌ | 177 | 2492 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-experiment` | ✅ | ❌ | 203 | 1714 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-finalize` | ✅ | ❌ | 266 | 2334 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-hotfix` | ✅ | ❌ | 185 | 1094 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-increment` | ✅ | ❌ | 262 | 1610 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-product-discovery` | ✅ | ❌ | 208 | 2168 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-regression-gate` | ✅ | ❌ | 140 | 1093 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-spec-review` | ✅ | ❌ | 133 | 1065 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-specify` | ✅ | ❌ | 273 | 2909 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-tasks` | ✅ | ❌ | 173 | 1237 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-tasks-review` | ✅ | ❌ | 134 | 1167 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-test-driven-dev` | ✅ | ❌ | 239 | 3155 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-test-review` | ✅ | ❌ | 134 | 1158 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-traceability-review` | ✅ | ❌ | 143 | 1151 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-ui-design` | ✅ | ❌ | 360 | 3765 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-ui-review` | ✅ | ❌ | 180 | 1754 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `hf-workflow-router` | ✅ | ❌ | 181 | 1623 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |
| `using-hf-workflow` | ✅ | ❌ | 210 | 2162 | ✅ | ✅ | ❌ | ❌ | workflow skill 缺 `Object Contract`（v0.1.0 推荐，v0.2.0 必需）；缺 `Common Rationalizations`（v0.1.0 release gate / ADR-001 D8） |

## 整改优先级建议

P0（anatomy 必需段缺失，违反 `skill-anatomy.md` hard rule）：
- 无

P1（v0.1.0 release gate，ADR-001 D8 全量补 anti-rationalization）：
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

P2（v0.1.0 推荐 / v0.2.0 必需，建议本次顺手补）：
- `hf-bug-patterns` — 增加 `## Object Contract` 段
- `hf-code-review` — 增加 `## Object Contract` 段
- `hf-completion-gate` — 增加 `## Object Contract` 段
- `hf-design` — 增加 `## Object Contract` 段
- `hf-design-review` — 增加 `## Object Contract` 段
- `hf-discovery-review` — 增加 `## Object Contract` 段
- `hf-doc-freshness-gate` — 增加 `## Object Contract` 段
- `hf-experiment` — 增加 `## Object Contract` 段
- `hf-finalize` — 增加 `## Object Contract` 段
- `hf-hotfix` — 增加 `## Object Contract` 段
- `hf-increment` — 增加 `## Object Contract` 段
- `hf-product-discovery` — 增加 `## Object Contract` 段
- `hf-regression-gate` — 增加 `## Object Contract` 段
- `hf-spec-review` — 增加 `## Object Contract` 段
- `hf-specify` — 增加 `## Object Contract` 段
- `hf-tasks` — 增加 `## Object Contract` 段
- `hf-tasks-review` — 增加 `## Object Contract` 段
- `hf-test-driven-dev` — 增加 `## Object Contract` 段
- `hf-test-review` — 增加 `## Object Contract` 段
- `hf-traceability-review` — 增加 `## Object Contract` 段
- `hf-ui-design` — 增加 `## Object Contract` 段
- `hf-ui-review` — 增加 `## Object Contract` 段
- `hf-workflow-router` — 增加 `## Object Contract` 段
- `using-hf-workflow` — 增加 `## Object Contract` 段

## 已关闭的方向题

- **Q1 — Object Contract 是否作为 v0.1.0 发版门禁？**架构师 2026-04-29 选 **B**：放宽 `skill-anatomy.md`，Object Contract 在 v0.1.0 为「推荐」、v0.2.0 升为「必需」。审计随即把它从 hard fail 降为 P2 推荐项；缺位不再阻塞 v0.1.0 发版。
- **Q2 — Common Rationalizations 衍生冲突**：`skill-anatomy.md` 已同步把 `Common Rationalizations` 从「默认不建议扩散」移到「workflow skill 推荐」，并写明 v0.1.0 全量补。审计把它升为 P1（v0.1.0 release gate）。

## 方法学说明

- **anatomy hard checks**：等价于 `skill-anatomy.md` 检查清单的「不可协商」部分（identity / Methodology / Workflow shape / Red Flags / Verification / token-line budget）。
- **v0.1.0 release gate**：在 hard checks 基础上额外要求 workflow skill 写 `Common Rationalizations`（ADR-001 D8）。
- **Object Contract**：v0.1.0 推荐、v0.2.0 必需（架构师 Q1=B 决议）。v0.1.0 缺位仅作 P2 提示，不阻塞发版。
- token 估算用 `len(text)/4` 的粗略比例，仅用于发现违反预算的离群值；精确 token 数请按所用 tokenizer 复算。
- 本脚本只读，不修改任何 SKILL.md；整改由后续 PR 显式完成。

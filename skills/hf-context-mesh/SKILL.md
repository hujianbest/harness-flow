---
name: hf-context-mesh
description: Use when a host project (vendoring HF) wants per-directory hierarchical context (project root / mid-directory / leaf-directory) auto-generated for any AI agent reading the codebase. Generates `AGENTS.md` (OpenCode), `.cursor/rules/*.mdc` (Cursor), or `CLAUDE.md` (Claude Code) skeletons; architect fills in conventions. Not for HF's own `docs/principles/` (untouched); not for spec / design / tasks artifacts (use upstream skills).
---

# HF Context Mesh

宿主项目按目录层级生成 hierarchical AI agent 上下文文件的脚手架生成器。对应 OMO `/init-deep` 的等价能力，但跨三客户端：

- **OpenCode** → `AGENTS.md`（被 `directoryAgentsInjector` hook 自动注入）
- **Cursor** → `.cursor/rules/<name>.mdc`（用 `globs: <dir>/**` 做目录级触发）
- **Claude Code** → `CLAUDE.md`（同目录约定文件名）

按 ADR-008 D1 / ADR-010 D3 维持三客户端可移植性：本 skill 在三客户端各自给出独立模板，互不依赖。

**HF 自身的 `docs/principles/` 永不被本 skill 触碰**（宪法层不变，按 `docs/principles/soul.md` 第 5 条）。

## When to Use

适用：
- 宿主项目（vendor HF 进自己仓库的项目）想一键生成层次化 AI agent 上下文骨架
- 项目目录树发生显著变化（新增 src/ 子模块 / 新增 docs/ 大段），需重新生成上下文骨架
- 架构师选择了客户端（OpenCode / Cursor / Claude Code / all 3），希望本 skill 生成对应模板

不适用：
- HF 仓库自身的 `docs/principles/` 不动（用 ADR / soul-doc 路径而非本 skill）
- 单 artifact 写作（spec / design / tasks）→ 上游 hf-* skill
- 上下文已存在且无目录树变化 → 不需要重新生成

## Hard Gates

- **不替架构师写约定**：本 skill 只生成骨架（headings + 占位），具体 Conventions / Patterns / Anti-Patterns 由架构师填；按 `docs/principles/soul.md` 第 5 条
- 不修改 HF 自身 `docs/principles/`（宪法层不变）
- 不修改宿主项目已有的 AGENTS.md / .mdc / CLAUDE.md（除非架构师 explicit `--force`）；冲突时先 dry-run 列出会动哪些文件
- 客户端选择必须由架构师拍板（Workflow 步骤 2）；不假设默认客户端

## Object Contract

- **Primary Object**: 宿主项目目录树下的 N 个 `AGENTS.md` / `.mdc` / `CLAUDE.md` 骨架文件
- **Frontend Input Object**: 宿主项目根路径 + 架构师选定的客户端（OpenCode / Cursor / Claude Code / all 3）
- **Backend Output Object**:
  1. 骨架文件落到目标目录（按客户端命名约定）
  2. 文件内容是 headings + 占位段，不含具体 convention 内容
- **Object Boundaries**:
  - 不动 HF `docs/principles/`
  - 不写架构师的约定内容
  - 不动宿主项目源代码
- **Object Invariants**:
  - 同一目录可同时存在 OpenCode / Cursor / Claude Code 三客户端文件（互不冲突）
  - root / mid / leaf 三层模板结构对齐（不同客户端对应同层使用同结构骨架，仅文件名 / frontmatter 不同）

## Methodology

| 方法 | 落地步骤 |
|---|---|
| **Per-Client Template Set** | references/agents-md-template.md 内 3 套独立模板 |
| **3-Layer Hierarchy (root / mid / leaf)** | Workflow 步骤 1：识别 3 类目录 |
| **Skeleton-Only Generation** | Hard Gates "不替架构师写约定" |
| **Architect-Driven Client Choice** | Workflow 步骤 2：询问客户端 |

详细模板：`references/agents-md-template.md`。

## Workflow

1. **扫描宿主项目目录树**
   - Object: 目录列表 + 每个目录的层级分类
   - Method: walk + 按规则分类（root = 项目根；mid = 含 ≥ 2 子目录或含 README.md 的中间目录；leaf = 仅含源文件无子目录）
   - Input: 宿主项目根路径（CLI arg / config）
   - Output: 目录清单 + 层级标注
   - Stop / continue: 目录数 ≤ 50 → 继续；> 50 → 提示架构师选 prefix 缩范围

2. **询问架构师选定客户端**
   - Object: 目标客户端集合（subset of {OpenCode, Cursor, Claude Code}）
   - Method: 直接 prompt 架构师；不假设默认
   - Input: 步骤 1 目录清单
   - Output: 客户端集合
   - Stop / continue: ≥ 1 客户端 → 继续；0 → 退出

3. **生成骨架文件**
   - Object: 每个目录 × 每个客户端 = 骨架文件
   - Method: 按 `references/agents-md-template.md` 的对应客户端 + 对应层级模板填充
   - Input: 步骤 1 + 步骤 2 输出
   - Output: 文件落到目标目录
   - Stop / continue: 文件冲突且无 `--force` → dry-run 列出冲突后退出；否则继续

4. **架构师填充 Conventions / Patterns / Anti-Patterns**
   - Object: 骨架占位段
   - Method: 架构师手动填写（不由本 skill 代笔）
   - Input: 步骤 3 骨架
   - Output: 完整 AGENTS.md / .mdc / CLAUDE.md 内容
   - Stop / continue: Hard Gates "不替架构师写约定"——本 skill 不主动建议内容，仅在架构师询问时给"参考其它项目的常见 pattern"链接（external）

## Output Contract

| 客户端 | 文件名 | 落点 |
|---|---|---|
| OpenCode | `AGENTS.md` | 每个识别的目录下 |
| Cursor | `.cursor/rules/<dir-slug>.mdc` | 项目根 `.cursor/rules/` 下，按目录 slug 命名（globs 字段指向对应目录） |
| Claude Code | `CLAUDE.md` | 每个识别的目录下 |

不写 progress.md（本 skill 不在 SDD workflow 主链）；不写 review record（不是 review 节点）。

## Red Flags

- 本 skill 主动写架构师的 Conventions（违反 Hard Gates）
- 触动 HF `docs/principles/`
- 默认假设客户端而不询问
- 覆盖宿主项目已有的 AGENTS.md / .mdc / CLAUDE.md（应先 dry-run + 架构师 confirm `--force`）

## Common Mistakes

| 错误 | 问题 | 修复 |
|---|---|---|
| 把 leaf 模板用到 root | root 期望项目级总览，leaf 不够 | 按目录层级严格选模板 |
| 给 Cursor `.mdc` 写错 globs | rule 不会按目录触发 | globs 字段必须 `<dir-from-project-root>/**` |
| 同时为 3 客户端生成但只填 1 份 conventions | 3 客户端用户体验不一致 | 架构师为每客户端独立填或在每个文件里 reference 同一份共享文档 |

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|---|---|
| "架构师会嫌麻烦，我帮 ta 填几条 convention 当例子。" | Hard Gates: 不替架构师写约定；填例子 = 替 ta 决定标准，违反 soul.md 第 5 条 |
| "默认客户端按宿主目录有没有 .opencode/ 自动判断。" | Hard Gates: 客户端必须架构师拍板；目录自动识别 = 替 ta 做选择 |
| "已有的 AGENTS.md 内容看起来过时，顺手覆盖。" | Hard Gates: 不覆盖已有文件除非 `--force`；先 dry-run 列出冲突让架构师决定 |
| "HF 自己的 docs/principles 也是按目录的，顺便给它生成。" | Hard Gates: 永不触动 HF 自身 docs/principles/，按 soul.md 宪法层不变 |

## Reference Guide

| 文件 | 用途 |
|---|---|
| `references/agents-md-template.md` | OpenCode / Cursor / Claude Code 三客户端各自的 root / mid / leaf 三层模板 |

## Verification

- [ ] 目录树扫描完成
- [ ] 架构师已选定客户端
- [ ] 骨架文件落到对应位置（OpenCode AGENTS.md / Cursor .mdc / Claude Code CLAUDE.md）
- [ ] 未填充 Conventions / Patterns / Anti-Patterns（架构师责任）
- [ ] 未触动 HF docs/principles/
- [ ] 已有文件冲突时已 dry-run 列出（除非 `--force`）

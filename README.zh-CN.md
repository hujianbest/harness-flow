# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**牵引 AI 编码代理从想法到交付的 harness：以 `hf-*` 命名承载 Matt 主链内容，保留 progress 恢复、auto、评审纪律、demo 验收与可插拔 `ext-*`。**

主链技能内容改编自 [mattpocock/skills](https://github.com/mattpocock/skills)（MIT，已获授权复制）。HarnessFlow 保留 `progress.md`、interactive/auto、跨阶段 `hf-review`。

## 安装

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

- **Cursor**：安装到 `.cursor/skills/`，并写入始终生效的 `.cursor/rules/harness-flow.mdc`（路径已重写）；保留项目中无关自定义技能。可用 `--mode symlink` 跟随本仓库 checkout。
- **OpenCode**：安装到 `.opencode/skills/`（生成物，已 gitignore）；真源仍是顶层 `skills/`。
- **Claude Code**：可作为本仓库 marketplace 插件安装，或把 `skills/` vendor 进项目。

在本仓库内用 OpenCode：`python scripts/install.py --target opencode --dest .`

## 使用说明

### 1. 每个项目先配置一次

让代理跑 `hf-grill-with-docs`，并按 `skills/hf-workflow/references/product-layer-templates.md` 落盘 `CONTEXT.md`、`product/…`、`docs/adr/`、`features/`。规格与任务票放在 `features/<id>/`。

### 2. 用自然语言开工

代理应先加载 `hf-workflow`。示例：

| 目标 | 示例说法 |
|------|----------|
| 想法 → 应用 | 「我有个想法：做个读书笔记应用。用 HarnessFlow。」 |
| 存量特性 | 「用 HarnessFlow：给通知 API 加限流。」 |
| 中断后续上 | 「继续」/「恢复 HarnessFlow 进度。」 |
| 全自动 | 「自动执行，不用等我确认（除非硬停）。」 |
| 探索原型 | 「先原型验证这个状态模型（即弃）。」 |

### 3. 沿主链推进

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-product-architecture — hf-review（产品架构）—
  → hf-to-spec            — hf-review（规格）—
  → hf-to-architecture    — hf-review（架构）—
  → hf-to-tickets
  → hf-implement          — hf-review → hf-code-review —
  → hf-ship
```

磁盘上大致会出现：

| 阶段 | 典型工件 |
|------|----------|
| 访谈 | `CONTEXT.md`、ADR、`product/assumptions.md`、可选特性目录 |
| 产品架构 | `product/architecture.md` + `product/reviews/product-architecture-review.md` |
| 规格 | `features/.../spec.md` + `reviews/spec-review.md` |
| 架构 | `features/.../architecture.md`（相对产品地图的增量）+ `reviews/architecture-review.md` |
| 拆票 | `features/.../tickets.md`（`- [ ] T-01 ...`） |
| 实现 | 代码 + `hf-tdd` 测试；票勾选 |
| 代码评审 | `reviews/code-review.md` |
| 收尾 | 回写 CONTEXT/产品架构/假设台账；`progress` → `done` |
| 可感知 UI | ship 前还要 demo 证据 + `reviews/demo-acceptance.md` |

探索路径：`hf-prototype` 或 `模式: 探索` → `conclusion.md`（**永远不能 ship**；禁止直接晋升原型代码）。

### 4. 从磁盘恢复（不靠聊天记忆）

阅读 `product/progress.md` 与各 `features/<id>/progress.md` 查看阶段与下一步。工件布局见各阶段技能与 `skills/hf-workflow/references/product-layer-templates.md`。

**要点**

- 规格 / 产品架构 / 特性架构 / 代码宜独立 `hf-review`（代码门另走 `hf-code-review`）。
- 欠定：提出默认 → 记入 `product/assumptions.md` → 继续。
- 只有你明确说 **自动执行** 时，评审通过即可不经等待推进；同会话降级评审在 auto 下硬停。

### 5. 执行模式

- **interactive**（默认）：评审与 demo 验收后等待你确认。
- **auto**：须明确开启。评审通过即推进（`auto-approved`）。底线：实现/评审走 subagent、降级禁自我确认、假设入台账；下次与人交互时主动呈上 demo。

## 核心技能

| 技能 | 职责 |
|------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | 入口、路由、auto、扩展 |
| [hf-grill-with-docs](skills/hf-grill-with-docs/SKILL.md) | 访谈 + CONTEXT.md / ADR |
| [hf-to-product-architecture](skills/hf-to-product-architecture/SKILL.md) | 产品级架构地图（特征驱动 / 易变性划分 / 演进适应度） |
| [hf-to-spec](skills/hf-to-spec/SKILL.md) | 综合规格 |
| [hf-to-architecture](skills/hf-to-architecture/SKILL.md) | spec 后的特性架构（增量） |
| [hf-to-tickets](skills/hf-to-tickets/SKILL.md) | 垂直切片票 + blocking |
| [hf-implement](skills/hf-implement/SKILL.md) | 按票实现（内驱 `hf-tdd`） |
| [hf-review](skills/hf-review/SKILL.md) | 跨阶段评审协议 |
| [hf-code-review](skills/hf-code-review/SKILL.md) | 代码双轴评审 |
| [hf-ship](skills/hf-ship/SKILL.md) | 收尾与回写 |

Meta：`hf-tdd`、`hf-grilling`、`hf-domain-modeling`、`hf-codebase-design`、`hf-prototype`。

## 扩展

按 frontmatter 的**绑定阶段**与**触发条件**加载：

- [ext-ui-design](skills/ext-ui-design/SKILL.md) — 有 UI 时绑定 `to-spec` / `implement` / `code-review`

扩展只收紧、不放松主链。编写指南：[extension-authoring](skills/hf-workflow/references/extension-authoring.md)。

## License

MIT。主链技能散文改编自 mattpocock/skills（MIT）。

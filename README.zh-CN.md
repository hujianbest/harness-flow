# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**牵引 AI 编码代理从想法到交付的 harness：以 `hf-*` 命名承载 Matt 主链内容，保留机械门禁、progress 恢复、auto、demo 验收与可插拔 `ext-*`。**

主链技能内容改编自 [mattpocock/skills](https://github.com/mattpocock/skills)（MIT，已获授权复制）。HarnessFlow 保留可靠性外壳：`hf_gate.py`、`progress.md`、interactive/auto、跨阶段 `hf-review`。

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

在目标项目里对代理说一次：

> 请运行 `hf-setup-skills`，配置 issue tracker（用本地文件即可）、必要时的 triage 标签，以及 CONTEXT/ADR 存放位置。

绿地也可先跑 `hf_gate.py init` 生成 `CONTEXT.md`、`product/assumptions.md`、`product/decisions.md`、`product/architecture.md`、`docs/adr/`、`features/`，需要接真实 tracker 时再跑 `hf-setup-skills`。

### 2. 用自然语言开工

代理应先加载 `hf-workflow`。示例：

| 目标 | 示例说法 |
|------|----------|
| 想法 → 应用 | 「我有个想法：做个读书笔记应用。用 HarnessFlow。」 |
| 存量特性 | 「用 HarnessFlow：给通知 API 加限流。」 |
| 中断后续上 | 「继续」/「恢复 HarnessFlow 进度。」 |
| 全自动 | 「自动执行，不用等我确认（除非硬停）。」 |
| 探索原型 | 「先原型验证这个状态模型（即弃）。」 |
| 外来 issue | 「先 triage 开放 issue，再实现 ready-for-agent 的。」 |

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

探索路径：`hf-prototype` 或 `模式: 探索` → `conclusion.md` + `check --to close`（**永远不能 ship**；禁止直接晋升原型代码）。

### 4. 随时恢复（不靠聊天记忆）

```bash
gate=skills/hf-workflow/scripts/hf_gate.py   # Cursor 安装后多为 .cursor/skills/hf-workflow/scripts/hf_gate.py
python3 $gate status                         # 产品层 + 各特性卡点 + 下一步
python3 $gate next                           # 下一个未完成特性/阶段
python3 $gate check --product
python3 $gate check --feature features/001-x --to to-architecture
```

`--to`：`to-spec` | `to-architecture` | `to-tickets` | `implement` | `ship` | `close`。

**要点**

- 进入阶段前必须 `check --to <stage>` **PASS**，并把 RESULT 写入 `progress.md`。
- 门禁看文件与结论行，不看聊天里的「可以」。
- 规格 / 产品架构 / 特性架构 / 代码都要独立 `hf-review`（代码门另走 `hf-code-review`）。
- 完整产品层：特性主链前须 `check --product` PASS；特性架构须声明对齐 `product/architecture.md`。
- 欠定：提出默认 → 记入 `product/assumptions.md` → 继续。
- 只有你明确说 **自动执行** 时，评审通过 + gate PASS 才可不经等待推进；同会话降级评审在 auto 下硬停。

### 5. 执行模式

- **interactive**（默认）：评审与 demo 验收后等待你确认。
- **auto**：须明确开启。评审通过 + gate PASS 即推进（`auto-approved`）。底线：实现/评审走 subagent、降级禁自我确认、gate 不可绕、假设入台账；下次与人交互时主动呈上 demo。

## 核心技能

| 技能 | 职责 |
|------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | 入口、路由、auto、扩展、门禁 |
| [hf-grill-with-docs](skills/hf-grill-with-docs/SKILL.md) | 访谈 + CONTEXT.md / ADR |
| [hf-to-product-architecture](skills/hf-to-product-architecture/SKILL.md) | 产品级架构地图 |
| [hf-to-spec](skills/hf-to-spec/SKILL.md) | 综合规格 |
| [hf-to-architecture](skills/hf-to-architecture/SKILL.md) | spec 后的特性架构（增量） |
| [hf-to-tickets](skills/hf-to-tickets/SKILL.md) | 垂直切片票 + blocking |
| [hf-implement](skills/hf-implement/SKILL.md) | 按票实现（内驱 `hf-tdd`） |
| [hf-review](skills/hf-review/SKILL.md) | 跨阶段评审协议 |
| [hf-code-review](skills/hf-code-review/SKILL.md) | 代码双轴评审 |
| [hf-ship](skills/hf-ship/SKILL.md) | 收尾与回写 |
| [hf-setup-skills](skills/hf-setup-skills/SKILL.md) | 每仓 tracker / 标签 / 领域文档配置 |

Meta / 旁路：`hf-tdd`、`hf-grilling`、`hf-domain-modeling`、`hf-codebase-design`、`hf-prototype`、`hf-triage`、`hf-diagnosing-bugs`、`hf-wayfinder`、`hf-handoff`、`hf-wizard` 等，见 `skills/hf-*`。

## 扩展

按 frontmatter 的**绑定阶段**与**触发条件**加载：

- [ext-ui-design](skills/ext-ui-design/SKILL.md) — 有 UI 时绑定 `to-spec` / `implement` / `code-review`
- [ext-design-md](skills/ext-design-md/SKILL.md) — 使用 `DESIGN.md` 时绑定 `to-architecture` / `ship`

扩展只收紧、不放松主链。编写指南：[extension-authoring](skills/hf-workflow/references/extension-authoring.md)。

## License

MIT。主链技能散文改编自 mattpocock/skills（MIT）。

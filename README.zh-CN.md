# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**牵引 AI 编码代理从想法到交付的 harness：以 `hf-*` 命名承载 Matt 主链内容，保留机械门禁、progress 恢复、auto、demo 验收与可插拔 `ext-*`。**

主链技能内容改编自 [mattpocock/skills](https://github.com/mattpocock/skills)（MIT，已获授权复制）。HarnessFlow 保留外壳：`hf_gate.py`、`progress.md`、interactive/auto、跨阶段 `hf-review`。

## 主链

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-spec            — hf-review（规格）—
  → hf-to-architecture    — hf-review（架构）—
  → hf-to-tickets
  → hf-implement          — hf-review → hf-code-review —
  → hf-ship
```

探索：`hf-prototype` / `模式: 探索` → `check --to close`（永不 ship）。外来票：`hf-triage`。难 bug：`hf-diagnosing-bugs`。

## 机械门禁

```bash
gate=skills/hf-workflow/scripts/hf_gate.py
python3 $gate init
python3 $gate status
python3 $gate next
python3 $gate check --product
python3 $gate check --feature features/001-x --to to-architecture
```

`--to`：`to-spec` | `to-architecture` | `to-tickets` | `implement` | `ship` | `close`。

门禁只看磁盘工件与评审结论行；语义由 `hf-review` / `hf-code-review` 与 demo 验收把关。

## 核心技能

| 技能 | 职责 |
|------|------|
| [hf-workflow](skills/hf-workflow/SKILL.md) | 入口、路由、auto、扩展、门禁 |
| [hf-grill-with-docs](skills/hf-grill-with-docs/SKILL.md) | 访谈 + CONTEXT.md / ADR |
| [hf-to-spec](skills/hf-to-spec/SKILL.md) | 综合规格 |
| [hf-to-architecture](skills/hf-to-architecture/SKILL.md) | spec 后的特性架构 |
| [hf-to-tickets](skills/hf-to-tickets/SKILL.md) | 垂直切片票 + blocking |
| [hf-implement](skills/hf-implement/SKILL.md) | 按票实现（内驱 `hf-tdd`） |
| [hf-review](skills/hf-review/SKILL.md) | 跨阶段评审协议 |
| [hf-code-review](skills/hf-code-review/SKILL.md) | 代码双轴评审 |
| [hf-ship](skills/hf-ship/SKILL.md) | 收尾与回写 |

Meta / 旁路见 `skills/hf-*`（如 `hf-tdd`、`hf-grilling`、`hf-setup-matt-pocock-skills` 等）。

## 扩展

`ext-ui-design`（to-spec / implement / code-review）、`ext-design-md`（to-architecture / ship）。编写指南见 [extension-authoring](skills/hf-workflow/references/extension-authoring.md)。

## 安装

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

## 执行模式

- **interactive**（默认）：评审与 demo 验收等待确认。
- **auto**：明确开启后，评审通过 + gate PASS 即推进（`auto-approved`）。底线：实现/评审走 subagent、降级禁自我确认、gate 不可绕、假设入台账。

## License

MIT。主链技能散文改编自 mattpocock/skills（MIT）。

---
name: hf-workflow
description: HarnessFlow 主工作流入口。凡开发新功能、修改行为、修复缺陷、从想法搭建应用,或用户提到开始开发/继续/恢复进度/harness-flow 时,必须先加载本技能。主链为 grill-with-docs → to-spec → to-architecture → to-tickets → implement → ship,横切 hf-review,机械门禁 hf_gate.py,支持 interactive/auto 与 ext-* 扩展。不适用于纯问答、只读代码等无代码变更请求。
---

# HarnessFlow 主工作流

主链内容对齐 Matt Pocock skills(MIT,已获授权复制),外壳保留 HarnessFlow 的门禁、progress 恢复、auto 与扩展机制。

## 主链

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-spec           ── hf-review(规格) ──►
  → hf-to-architecture   ── hf-review(架构) ──►
  → hf-to-tickets
  → hf-implement         ── hf-review → hf-code-review ──►
  → hf-ship
```

探索旁路:`hf-prototype`(或特性 `模式: 探索`) → 结论收尾 `check --to close`,**永远不能 ship**。

存量外来票:`hf-triage` → 就绪后 `hf-implement`。难 bug:`hf-diagnosing-bugs`。

## 进入规则

1. 先跑 `python3 skills/hf-workflow/scripts/hf_gate.py status` 恢复磁盘状态,不靠聊天记忆。
2. 进入任何阶段前 `check --to <stage>`(或绿地 `check --product`),把 RESULT 行写入该特性 `progress.md`;FAIL 不得进入。
3. 到达阶段时只读该阶段 `SKILL.md` 与匹配的 `ext-*`,不预读全链。
4. 有 `CONTEXT.md` / 特性 `architecture.md` 时先读地图再读相关代码,禁止每特性全库扫描。

## 机械门禁

```bash
gate=skills/hf-workflow/scripts/hf_gate.py
python3 $gate init
python3 $gate status
python3 $gate next
python3 $gate check --product
python3 $gate check --feature features/<NNN>-<slug> --to <stage>
```

`--to` 取值:`to-spec` | `to-architecture` | `to-tickets` | `implement` | `ship` | `close`。

门禁只裁决文件、结论行、勾选与确认;语义质量由 `hf-review` / `hf-code-review` 与用户 demo 验收把关。

## progress.md

```markdown
# 进度
- 特性: <NNN>-<slug>
- 当前阶段: grill-with-docs | to-spec | to-architecture | to-tickets | implement | code-review | ship | close | done
- 执行模式: interactive | auto
- 已加载扩展: <ext-* 或无>
- 下一步: <一句话>
- 门禁输出: <最近 RESULT 行>
```

## 执行模式

- `interactive`(默认):规格/架构/代码评审通过后与 demo 验收时等待用户确认。
- `auto`:用户明确说自动执行时启用。评审通过 + gate PASS 即推进,确认行写 `auto-approved <日期>`。底线:实现与评审走 subagent;降级评审在 auto 下硬停;gate 不可绕;替用户选择进 `product/assumptions.md`;demo 可先 auto-approved,下次交互必须主动呈上。

## 硬性规则

- 门禁 FAIL 不进下一阶段;评审「需修改」回作者阶段只修 findings。
- `hf-implement` 任务/票由 subagent 执行;主会话只编排。
- 作者/评审分离见 `hf-review`;代码门另遵 `hf-code-review`。
- 欠定不静默填补 → 假设台账。
- 用户可感知特性 ship 前须 demo 验收落盘。
- 探索产物禁止直接晋升。
- 压力催促不算豁免;用户坚持跳过时须在 progress 记录豁免。

## 扩展

进入阶段前扫描 `skills/ext-*/`,读 description 的绑定阶段与触发条件;匹配则加载。扩展只收紧不放松。合法绑定阶段见 `references/extension-authoring.md`。

## Meta 技能(按需)

`hf-grilling`、`hf-domain-modeling`、`hf-tdd`、`hf-codebase-design`、`hf-code-review`、`hf-prototype`、`hf-research`、`hf-handoff`、`hf-setup-skills`、`hf-wayfinder`、`hf-triage`、`hf-diagnosing-bugs`、`hf-wizard`、`hf-improve-codebase-architecture`、`hf-grill-me`。

首次使用工程技能前,若缺 tracker 配置,先走 `hf-setup-skills`(默认可用 local tickets)。

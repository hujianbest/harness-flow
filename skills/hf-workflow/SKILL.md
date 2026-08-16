---
name: hf-workflow
description: HarnessFlow 主工作流入口。凡开发新功能、修改行为、修复缺陷、从想法搭建应用，或用户提到开始开发/继续/恢复进度/harness-flow 时，必须先加载本技能。主链为 grill-with-docs → to-product-architecture → to-spec → to-architecture → to-tickets → implement → ship，横切 hf-review。支持 interactive/auto。有 UI 时加载 hf-ui-design。不适用于纯问答、只读代码等无代码变更请求。
---

# HarnessFlow 主工作流

主链内容对齐 Matt Pocock 技能（MIT，已获授权复制），外壳保留进度落盘与 `auto`；并含**产品级架构**阶段。

## 主链

```
hf-workflow
  → hf-grill-with-docs
  → hf-to-product-architecture ── hf-review(产品架构) ──►
  → hf-to-spec           ── hf-review(规格) ──►
  → hf-to-architecture   ── hf-review(架构) ──►
  → hf-to-tickets
  → hf-implement         ── hf-review(含代码门) ──►
  → hf-ship
```

探索旁路：特性 `模式: 探索` → 写 `conclusion.md` 收尾，**不应进入 `ship`**，禁止直接晋升探索产物。

存量热修可只建 `product/architecture.md`（仅架构地图），不强制完整产品层。规格与任务票默认落在 `features/<id>/`。

## 进入规则

1. 新会话读各特性/`product` 的 `progress.md` 与相关工件恢复状态，不靠聊天记忆。
2. 到达阶段时只读该阶段 `SKILL.md`；有 UI 时另加载 `hf-ui-design`。不预读全链。
3. 有 `CONTEXT.md` / `product/architecture.md` / 特性 `architecture.md` 时先读地图再读相关代码，禁止每特性全库扫描。
4. 绿地首次落盘见 `references/product-layer-templates.md`（由 `hf-grill-with-docs` 创建）。

## `progress.md`

特性：

```markdown
# 进度
- 特性: <NNN>-<slug>
- 当前阶段: grill-with-docs | to-spec | to-architecture | to-tickets | implement | code-review | ship | close | done
- 执行模式: interactive | auto
- 已加载: <hf-ui-design 或无>
- 下一步: <一句话>
```

产品层另用 `product/progress.md`（阶段含 `to-product-architecture` | `ready`）。

## 执行模式

- `interactive`（默认）：规格/架构/代码评审通过后以及演示验收时等待用户确认。
- `auto`：用户明确要求自动执行时启用。评审通过即可推进，确认行写 `auto-approved <日期>`。底线：实现与评审使用 subagent；降级评审在 `auto` 下硬停；替用户作出的选择写入 `product/assumptions.md`；演示可先记为 `auto-approved`，下次交互必须主动呈上。

## 硬性规则

- 评审结论为「需修改」时返回作者阶段，只修复发现项。
- `hf-implement` 任务/票由 subagent 执行；主会话只编排。
- 作者/评审分离见 `hf-review`（代码门为其中的 Standards + Spec 双轴）。
- 欠定不静默填补 → 假设台账。
- 用户可感知特性进入 `ship` 前，宜将演示验收结果落盘。
- 探索产物禁止直接晋升。
- 用户若要求跳过评审等纪律，在 `progress.md` 记录豁免后再继续。

## UI

特性含页面/组件/可视交互时，在 `to-spec`、`implement`、代码评审加载 `hf-ui-design`。

## 元技能（按需）

`hf-grilling`、`hf-domain-modeling`、`hf-tdd`、`hf-codebase-design`、`hf-ui-design`。

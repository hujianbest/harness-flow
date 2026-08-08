---
name: hf-to-tickets
description: 把已评审的 spec+architecture 拆成带 blocking edges 的垂直切片票。HarnessFlow 主链第五步;进入前 gate check --to to-tickets。默认写入 features/<id>/tickets.md。
---

# To Tickets

Break a plan, spec, or architecture into **tickets** — tracer-bullet vertical slices, each declaring tickets that **block** it.

## HarnessFlow 桥接

1. `check --feature features/<id> --to to-tickets`(须 architecture + architecture-review 已通过)。
2. 默认发布到 `features/<id>/tickets.md`(机器可读 `- [ ] T-NN` 行);若已配置 tracker 则按其发布,并在特性目录留索引副本供 gate 解析。
3. 首张可执行票应为最薄端到端路径(行走骨架判据),除非架构已声明存量无需。
4. 更新 progress;下一步 `check --to implement`。

## Process

### 1. Gather context

Read `spec.md`, `architecture.md`, reviews, `CONTEXT.md`.

### 2. Explore codebase (optional)

Use domain vocabulary. Prefactor opportunities: make the change easy, then make the easy change.

### 3. Draft vertical slices

- Each slice cuts a narrow COMPLETE path through layers — vertical, not horizontal
- Demoable or verifiable alone; sized for one fresh context window
- Prefactors first
- Each ticket has **blocking edges**

**Wide refactors** use expand–contract batches, not forced tracer bullets.

### 4. Quiz the user

Present title / blocked-by / what it delivers. Iterate until approved (`auto`: ledger assumptions for granularity choices).

### 5. Publish

**Local / HF default** — `tickets.md`:

```markdown
# Tickets

- [ ] T-01 <title> — Blocked by: None — <what it delivers>
- [ ] T-02 <title> — Blocked by: T-01 — <what it delivers>
```

Optional per-ticket files under `tickets/` for detail; **gate 只解析 `tickets.md` 的 `- [ ] T-NN` 行**。

**Real tracker** — one issue per ticket with native blocking; keep `tickets.md` mirror for gate.

Do NOT close/modify unrelated parent issues beyond linking.

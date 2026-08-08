---
name: hf-implement
description: 按 tickets/spec 实现工作,内驱 hf-tdd,完成后经 hf-review 与 hf-code-review。HarnessFlow 主链第六步;进入前 gate check --to implement。建造模式须红绿;探索模式见 hf-prototype/close。
---

# Implement

Implement the work described by the tickets (and spec/architecture).

## HarnessFlow 桥接

1. `check --feature features/<id> --to implement`。FAIL 停。
2. 同一时间只做一张**前沿票**(blockers 均已勾选)。
3. 建造模式:每个行为变更走 `hf-tdd`(红→绿→重构);实现任务派 **subagent**,主会话编排。
4. 票完成后勾选 `tickets.md` 对应 `- [x] T-NN`。
5. 全部票勾选后: `hf-review` → `hf-code-review` → `reviews/code-review.md` + 确认。
6. 用户可感知:准备 demo 证据与体验路径,供 ship 前验收。
7. 下一步 `check --to ship`。

## 主体

Use `hf-tdd` where possible, at pre-agreed seams from spec/architecture.

Run typechecking regularly, single test files regularly, and the full suite once at the end.

Once done, use `hf-review` / `hf-code-review` before ship.

Commit work on the current branch when the user/flow expects it.

## 探索模式

若 `feature.md` 为 `模式: 探索`:不强制 TDD;产物即弃;写 `conclusion.md` 后 `check --to close`;**禁止 ship、禁止直接晋升代码**。UI/逻辑试探优先走 `hf-prototype`。

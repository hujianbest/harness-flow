# Momus Rubric — `hf-tasks-review` 4 维 + N=3 Rewrite Loop

> 启发自 OMO Momus（`code-yeongyu/oh-my-openagent` `src/agents/momus.ts`）。把"task plan 是否可执行 / 可验证 / 可追溯"压成 4 个 boolean 阈值，**任一**不达标即 `verdict: rejected-rewrite`；连续 3 次仍未通过则升级架构师（fast lane escape #5 对齐）。

## 4 维度

| # | 维度 | 阈值 | 评分定义 |
|---|---|---|---|
| 1 | **Clarity** | **100%** | 100% 任务的 ID / 描述 / Acceptance / Files / Verify 字段全部齐全；缺一字段即 0% |
| 2 | **Verification** | **90%** | ≥ 90% 任务的 Acceptance 是 PASS/FAIL 可机械判断（不允许 "应该" / "尽可能" / "良好支持" / "合理处理" 等模糊词） |
| 3 | **Context** | **80%** | ≥ 80% 任务有"参考实现锚点"（指向已有代码 / spec / design / 别的 task / ADR / fixture / test）；剩余 ≤ 20% 可基于 design 直推（不需要外部 anchor 但需在 task 描述显式写"按 design §X 直推"） |
| 4 | **Big Picture** | **100%** | 100% 任务能映射回 spec FR / NFR / OQ（traceability matrix）；无悬空任务（"清理一下 X" / "完善 Y" 等无 spec anchor 的任务）|
| Z | **Zero-tolerance** | **0%** | 0 任务依赖未确认业务事实；0 critical red flag（含 scope creep / dangling reference / 隐式架构决策）|

## 评分语义

- **0% 容忍 vs 100% 阈值**：阈值是 boolean cliff，不是渐进区间。Clarity 99.5% = 0%（任一字段缺）= FAIL；Big Picture 99% = FAIL（1% 悬空任务也会让 hf-test-driven-dev 启动错任务）。Verification / Context 是 90% / 80%（容忍少量任务缺机械可判 acceptance / 缺外部 anchor）。
- **Zero-tolerance 行**：critical red flag 命中数必须为 0；任一命中即 FAIL，与上面 4 维不达标等价处理（都触发 rejected-rewrite）。

## 评分流程

reviewer 在 `hf-tasks-review` Workflow 步骤 2（多维评分与挑战式审查）执行：

1. 数 task 总数 N
2. 对每 task 逐 5 字段（ID / Description / Acceptance / Files / Verify）扫描 → Clarity 命中数 ÷ N × 100%
3. 对每 task Acceptance 扫模糊词 → Verification 命中数 ÷ N × 100%
4. 对每 task 扫"参考锚点"（grep design / spec / ADR / TASK-NNN / fixture 引用）→ Context 命中数 ÷ N × 100%
5. 对每 task 扫 spec / design 反向追溯 → Big Picture 命中数 ÷ N × 100%
6. 扫 Zero-tolerance 5 类（业务事实未确认 / scope creep / dangling ref / 隐式架构 / 跨 ≥ 3 模块跳过 escalation）→ 命中数（必须 = 0）

每维不达标 → 在 review record findings 段中按 `[important][LLM-FIXABLE][momus-<dim>]` 标注；不达标维度数 ≥ 1 即 `verdict: rejected-rewrite`。

## N=3 Rewrite Loop（与 fast lane escape #5 对齐）

```
Round 1: tasks-review verdict
  ↓
  ├─ 4 维全过 + 0% Zero-tolerance → verdict: 通过 → 任务真人确认
  └─ 任一维不达标 → verdict: rejected-rewrite → hf-tasks Round 2 修订
       ↓
       Round 2: 同样评分
       ↓
       ├─ 通过 → 任务真人确认
       └─ rejected-rewrite → hf-tasks Round 3
            ↓
            Round 3: 同样评分
            ↓
            ├─ 通过 → 任务真人确认
            └─ rejected-rewrite → **第 4 次仍未通过** → verdict: 阻塞 → 升级架构师（fast lane escape #5 触发，按 ADR-009 D3 第 4 项）
```

第 4 次升级后由架构师决定：
- (a) 接受 Round 3 修订作为最终（覆盖阈值）
- (b) 重写 design / spec（hf-increment 入口）
- (c) 降级 Acceptance（修订 spec OQ）
- (d) 接受 deferred backlog（部分 task 推到下一 release）

## 与 OMO Momus 的差异

| OMO Momus（`src/agents/momus.ts`） | HF momus 4 维 |
|---|---|
| 严格度：4 / 1 / 1 / 1 binary（OKAY 当且仅当 4 dim 全过）| 严格度：100 / 90 / 80 / 100 / 0 boolean cliff，不允许渐进 |
| 循环：无上限（直到 OKAY） | 循环：N=3 上限，第 4 次升级架构师（与 fast lane escape #5 对齐） |
| 字段：Clarity / Verification / Context / Big Picture | 字段：同 4 维 + 1 个 Zero-tolerance 行 |
| 调用：plan author（Prometheus）→ Momus → REJECT/OKAY 循环 | 调用：tasks author（hf-tasks）→ tasks-review reviewer 应用本 rubric → rejected-rewrite / 通过 |

OMO 的"无上限循环"在自动化场景下会陷入死循环风险（author 与 reviewer 都是 LLM）；HF 的 N=3 + 升级架构师让架构师在第 4 次保留控制权（按 soul.md "用户是架构师"）。

## reviewer 引用

`hf-tasks-review/SKILL.md` Workflow 步骤 2 / 3 / 4 引用本文件。verdict 字段引入 `rejected-rewrite` 取值，与既有 `通过` / `需修改` / `阻塞` 三档并存（`需修改` 是 rejected-rewrite 的旧名，v0.6 起新名优先）。

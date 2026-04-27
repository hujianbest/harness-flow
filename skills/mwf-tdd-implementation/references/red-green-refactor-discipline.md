# mwf RED / GREEN / REFACTOR Discipline

> 配套 `mwf-tdd-implementation/SKILL.md`。规定 mwf 中 TDD 步骤的纪律、Two Hats、Fowler vocabulary 与升级边界。

## Two Hats（必须严格分离）

| 帽子 | 允许的动作 | 禁止的动作 |
|---|---|---|
| **Changer 帽** | RED 步：写新失败测试；GREEN 步：写最小可行实现使测试通过 | 不做 cleanup / 不重构 / 不顺手 rename |
| **Refactor 帽** | REFACTOR 步：保持行为不变改结构（rename、extract、replace magic number、decompose conditional） | 不引入新行为；不让任何测试失败 |

**核心规则**：

- 一个步骤里只能戴一顶帽子
- GREEN 步内看到 cleanup 机会 → 记下来，留给 REFACTOR 步
- REFACTOR 步内发现仍需新行为 → 退出 REFACTOR，回到 RED

## RED 步骤纪律

1. **先写失败测试**：基于 AR 设计的测试设计章节中的 case，把 `Expected Result` 落成可执行断言
2. **跑出失败证据**：执行测试命令并保留：
   - 命令本身
   - 退出码
   - 失败摘要（关键 assertion 输出）
   - 为什么这个失败对应 AR 行为缺口（不是无关错误）
3. **保存到** `features/<id>/evidence/unit/RED-<case-id>-YYYY-MM-DD.md` 或 integration 子目录
4. **不调整 AR 设计**：发现 AR 设计有误 → 停下回 `mwf-ar-design`，不在 TDD 中悄悄改设计

无效 RED 信号：

- 没真跑过
- 一跑就绿（说明测试不验证目标行为）
- 失败原因与目标行为无关（旧的不相关测试）
- 看不出在证明什么

## GREEN 步骤纪律

1. **戴 Changer 帽**：写最小实现使 RED 步测试通过；不做超出本 case 范围的改动
2. **保持其他测试全绿**：跑完整测试套件，确认未引入回归
3. **保留 GREEN 证据**：
   - 命令、退出码、通过摘要、关键结果
   - 新鲜度锚点（commit hash / build ID）
4. **保存到** `features/<id>/evidence/unit/GREEN-<case-id>-YYYY-MM-DD.md`
5. **GREEN 步内禁止**：rename、extract method、replace magic number、修改风格、删除 dead code、调整布局——这些全部留给 REFACTOR

有效 GREEN 信号：

- 任务测试转绿
- 完整测试套件无回归
- 证明命令本次会话成功

## REFACTOR 步骤纪律

仅在所有任务测试 + 相关回归 + 静态分析 / 编译告警均为绿后才进入。

按以下顺序执行：

1. **In-task Cleanups**：仅清扫本 task 触碰范围内的 clean code 问题。每条 cleanup 用 Fowler vocabulary 命名：
   - Extract Method / Rename / Inline / Move
   - Replace Magic Number with Symbolic Constant
   - Decompose Conditional / Replace Conditional with Polymorphism
   - Remove Dead Code
   - Introduce Explaining Variable
2. **每次 cleanup 后跑一次完整测试**，保持全绿
3. **静态分析重新评估**：编译告警、MISRA / CERT / 团队编码规范违反项是否减少 / 持平
4. **不引入新抽象**：除非 AR 设计的 C/C++ 实现策略明确声明
5. **保留 REFACTOR 证据**（如发生 cleanup）：
   - cleanup 列表（Fowler vocabulary 命名 + 影响文件）
   - 完整测试通过命令与结果
   - 静态分析对比

## Escalation 边界（任一命中即停 task，回 router）

- cleanup 跨 ≥3 模块的结构性重构
- 改 ADR（架构决策记录）/ 组件边界 / SOA 接口契约
- 引入 AR 设计未声明的新抽象层 / 新模式
- 修改其他组件
- 触碰 fitness function（若项目存在）转红被 reviewer 写「和我无关」

命中边界时：

1. 立即停 task
2. 把当前状态写入 implementation-log.md
3. handoff 给 `mwf-workflow-router`
4. 由 router 路由到 `mwf-component-design` / `mwf-ar-design` / 重升 component-impact

## Refactor Note 必填字段（写入 implementation-log.md）

```md
### Refactor Note
- Hat Discipline: <RGR 是否守住 Two Hats；GREEN 步是否做了 cleanup>
- In-task Cleanups:
  - <Fowler vocabulary> @ <文件:范围> — <一行说明>
- Architectural Conformance: <与 ar-design / component-design 的一致性结论>
- Documented Debt:
  - <smell 名> @ <影响范围> — <为什么不在本 task 内修>
- Escalation Triggers: <None | escalate to mwf-workflow-router>
- Static Analysis Evidence: <命令 + 结果摘要；不存在则写 not-configured>
```

REFACTOR 即使本轮无任何 cleanup，仍要写：

- In-task Cleanups: `none`
- Documented Debt: `none`
- Escalation Triggers: `none`
- Hat Discipline / Architectural Conformance / Static Analysis Evidence 必须显式写结论

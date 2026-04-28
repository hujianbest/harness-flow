# df Profile And Route Map

> 配套 `df-workflow-router/SKILL.md`。展开 df 各 Workflow Profile 的合法节点集合、主链与支线，以及 hard stops 的具体表现。

## Standard Route

```text
using-df-workflow
  -> df-workflow-router
  -> df-specify
  -> df-spec-review
  -> df-ar-design
  -> df-ar-design-review
  -> df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

合法节点集合：

```text
{ df-specify, df-spec-review, df-ar-design, df-ar-design-review,
  df-tdd-implementation, df-test-checker, df-code-review,
  df-completion-gate, df-finalize }
```

非法节点（出现需立即升级 / 改路）：

- 修改影响组件边界 / SOA 接口 / 组件依赖 → 升级 component-impact
- DTS / 紧急缺陷 → 改 hotfix

## Component-Impact Route

```text
using-df-workflow
  -> df-workflow-router
  -> df-specify
  -> df-spec-review
  -> df-component-design
  -> df-component-design-review
  -> df-ar-design
  -> df-ar-design-review
  -> df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

触发条件（任一命中即升级）：

- 新增组件
- 修改 SOA 服务 / 接口 / 错误码 / 时序约束
- 修改组件职责、依赖方向、状态机或运行时机制
- AR 实现需要跨组件协调
- 现有组件实现设计缺失、过期或与代码明显不一致

注意：组件实现设计是 AR 实现设计的输入。AR 实现设计**不得**临时改写组件架构；必须先经过 `df-component-design`。

## Hotfix / Problem-Fix Route

```text
using-df-workflow
  -> df-workflow-router
  -> df-problem-fix
  -> (可选) df-ar-design -> df-ar-design-review
  -> df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

`df-problem-fix` 至少完成：复现路径或无法复现说明、根因、最小安全修复边界、是否需要补 AR 实现设计或组件实现设计、明确回流节点。

紧急 ≠ 绕过；hotfix 可以压缩文档量（例如不写完整 AR 实现设计，只写 fix-design.md），但**不能**跳过：

- `df-test-checker`
- `df-code-review`
- `df-completion-gate`

## Lightweight Route

```text
using-df-workflow
  -> df-workflow-router
  -> df-specify (极简)
  -> df-spec-review
  -> df-ar-design (极简，但必须含测试设计章节)
  -> df-ar-design-review
  -> df-tdd-implementation
  -> df-test-checker
  -> df-code-review
  -> df-completion-gate
  -> df-finalize
```

`lightweight` 仅在以下条件全部满足时使用：

- 修改局部、低风险（如 magic number、注释、日志措辞）
- 不影响 SOA 接口 / 组件依赖 / 状态机
- 测试覆盖已能直接锁定行为

`lightweight` **不允许**跳过 test-checker / code-review / completion-gate。允许压缩的是文档量（requirement.md 可数行、ar-design-draft.md 章节可合并），不是质量证据。

## Profile 升级规则（仅升级，不允许降级）

| 当前 profile | 升级触发 | 升级后 |
|---|---|---|
| `lightweight` | 发现影响 SOA / 组件依赖 / 状态机 | `component-impact` |
| `lightweight` | 发现是 DTS / 缺陷 | `hotfix` |
| `standard` | 发现影响 SOA / 组件依赖 / 状态机 | `component-impact` |
| `standard` | 发现是 DTS / 缺陷 | `hotfix` |
| `component-impact` | 发现是 DTS | 仍 `component-impact` 兼 hotfix 性质，启动 `df-problem-fix` 子线 |

降级（如发现 component-impact 不再成立）一律禁止。理由：profile 决定了证据要求，已经按更高 profile 准备的证据不会因为降级而消失，也避免因为「看起来简单了」就静默删减验证。

## Hard Stops

任一命中必须停下，标 `reroute_via_router=true`：

1. 需求输入不清且涉及方向 / 范围 / 验收 → 停在 `df-specify`，回需求负责人
2. IR / SR / AR 追溯关系冲突 → 阻塞，回需求负责人
3. AR 不属于唯一组件 → 阻塞
4. 缺组件实现设计但当前修改影响组件边界 → 进 `df-component-design`
5. AR 实现设计未含测试设计章节 → 回 `df-ar-design`
6. TDD 完成后测试用例未经 `df-test-checker` → 不得进 `df-code-review`
7. 代码修改破坏 SOA 边界或引入未解释跨组件依赖 → review 阻塞
8. 存在未解释的 critical 静态分析 / 编译告警 / 编码规范违反 → completion 阻塞
9. review / gate 结论无法唯一映射下一步 → router hard stop

## Reviewer Dispatch Anchor

review 节点必须派发独立 reviewer subagent，不内联：

| 来源节点 | 派发节点 |
|---|---|
| `df-specify` | `df-spec-review` |
| `df-component-design` | `df-component-design-review` |
| `df-ar-design` | `df-ar-design-review` |
| `df-tdd-implementation` | `df-test-checker` |
| `df-test-checker`（通过） | `df-code-review` |

reviewer subagent 返回 `阻塞`(workflow) 时，本节点必须 `reroute_via_router=true` 停下，由父会话决定是否升级 profile / 回上游。

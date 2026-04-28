# df Reproduction / Root Cause / Fix Design Templates

> 配套 `df-problem-fix/SKILL.md`。提供 DTS / hotfix 三个核心过程文件的最小模板。

## reproduction.md

```markdown
# DTS<id>-<slug> Reproduction

## Identity

- DTS ID:
- Owning Component:
- Owner / Reporter:
- Severity:                                # critical / important / minor
- 已上线版本:                              # 触发缺陷的部署版本 / commit
- 复现稳定性: `stable` | `flaky` | `unable-to-reproduce`

## 期望行为

- 锚点（已批准 spec / 设计 / API 契约 / 文档段落）:
- 期望:

## 实际行为

- 实际:

## 复现步骤

- 环境:                                    # OS、目标平台、固件版本
- 软件版本 / 包:
- 配置:
- 步骤:
  1.
  2.
- 触发条件 / 频率:

## 失败证据

- 命令 / 操作:
- 退出码 / 状态:
- 关键日志摘要 / Stack Trace:
- 详细日志路径:                            # features/DTS<id>-<slug>/evidence/...

## 横向影响初步评估

- 是否可能在相似路径上也存在:
- 已知绕过方法:
```

## root-cause.md

```markdown
# DTS<id>-<slug> Root Cause Analysis

## Identity

- DTS ID:
- Owning Component:
- Reproduction Reference: features/DTS<id>-<slug>/reproduction.md

## 5 Whys

- Why 1:
- Why 2:
- Why 3:
- Why 4:
- Why 5:                                   # 不强制 5 层；最少到根因

## 根因维度

- [ ] 编码错误（off-by-one、空指针、类型转换）
- [ ] 设计缺陷（接口契约不一致、状态机覆盖不全）
- [ ] 内存（生命周期、池化、栈溢出）
- [ ] 并发（中断上下文、临界区、竞态、死锁）
- [ ] 实时性（截止时间、调度、节拍）
- [ ] 资源生命周期（句柄 / 文件 / 缓冲区）
- [ ] 错误处理（输入校验、降级、恢复）
- [ ] 配置 / 编译条件
- [ ] 依赖 / 接口（跨组件 / 第三方 / 协议）
- [ ] ABI / API 兼容
- [ ] 其他:

## 信心程度

- Confidence: `demonstrated` | `probable`
- 直接证据:
- 间接证据:

## 横向影响

- 是否在其他相似路径上也存在:
- 是否与既有 ADR / 组件设计章节冲突:
- 是否影响其他 work item:

## 是否触发组件级修订

- 是否需要修订 docs/component-design.md（以及项目已启用的可选子资产 docs/interfaces.md / docs/dependencies.md / docs/runtime-behavior.md；未启用的写 N/A）:
- 如是，说明触发的修订点:
```

## fix-design.md

```markdown
# DTS<id>-<slug> Fix Design

## Identity

- DTS ID:
- Owning Component:
- Reproduction Reference: features/DTS<id>-<slug>/reproduction.md
- Root Cause Reference: features/DTS<id>-<slug>/root-cause.md
- 当前 profile: `hotfix`

## 修复边界（最小安全）

- 改什么:                                  # 文件 / 函数 / 配置
- 不改什么:                                # 显式列出避免顺手扩散
- 影响什么:
  - 用户可见行为:
  - 公共接口:
  - 数据契约:
  - 跨组件:
- 修复信心: `demonstrated-minimal` | `probable-narrow`

## 修复策略

- 实现策略概要:                            # 仅描述思路，不写完整代码
- 与既有 docs/component-design.md / docs/ar-designs/ 的一致性:
- 是否需要补正式 AR 实现设计: yes / no
- 是否需要修订组件实现设计: yes / no

## 测试设计要点

> 这是临时的测试设计要点。若需要正式 AR 实现设计，下一节点是 `df-ar-design`，测试设计章节应在那里完整化。

- 复现脚本作为 RED 用例:
- 额外覆盖的边界 / 异常 / 嵌入式风险用例:
- 集成 / 仿真测试需求（如适用）:
- RED / GREEN 证据要求:
- 嵌入式风险覆盖矩阵:
  - 内存:
  - 并发:
  - 实时性:
  - 资源生命周期:
  - 错误处理:
  - ABI / API 兼容:

## 嵌入式风险审计

- 修复是否引入新风险:
- 是否需要补静态分析配置:
- 是否需要更新编译告警基线:

## 回流节点

- Next Action Or Recommended Skill:        # df-tdd-implementation / df-ar-design / df-component-design / df-specify / df-workflow-router
- 选择理由:

## Open Questions

- 阻塞 (blocking):
- 非阻塞 (non-blocking):
```

## 反例

```text
❌ reproduction.md：「问题如下：服务起不来」
❌ root-cause.md：「应该是某个变量没初始化」
❌ fix-design.md：「改一下那个函数让它不崩了」
```

```text
✅ reproduction.md 含完整环境、版本、命令、退出码、可放进 RED 的失败证据
✅ root-cause.md 走完 5 Whys，明确根因维度（如「中断上下文中调用了阻塞 API」），信心 `demonstrated`
✅ fix-design.md 列出改 X.c 的 Y 函数；不改公共接口；用户可见行为不变；嵌入式风险审计每维度有结论
```

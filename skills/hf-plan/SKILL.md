---
name: hf-plan
description: HarnessFlow plan 阶段。frame 完成且风险档位 ≥2 时使用:档位 2 产出一份 plan.md(需求+设计+任务清单),档位 3 先产出 spec.md 评审通过后再产出 design.md。也用于 plan 层评审返回"需修改"后的修订。档位 1 不使用本技能。前提不满足(gate check --to plan 失败)时回 hf-frame。
---

# Plan(计划)

目标:产出让 build 阶段**不需要猜、也不需要临场做架构决策**的计划,且计划里每一条需求都能被测试验证。

前提:`gate check --to plan` PASS(输出贴入 progress.md)。

## 通用规则(两种档位都适用)

- **需求可测**:功能需求逐条编号 `FR-1`、`FR-2`……每条描述一个可观察行为,附至少一条 Given/When/Then 验收标准,覆盖失败路径与边界值,不只有 happy path。
- **禁止槽位幻觉**:模板任何小节可写"不适用: <一句理由>"。**严禁为填模板发明需求、约束或数字。** NFR 只在用户真实提出、或有真实依据(既有 SLA、现存性能问题)时才写;写则必须给出可判定阈值、验证方式和**出处**。
- **顺着现有代码走**:设计必须复用现有约定(目录结构、既有模式、测试组织、错误处理),偏离要写明理由;全新项目由本计划确立初始约定。
- **关键决策 ≥2 方案**:只对真实的决策点(存在不止一种合理做法且影响后续实现)做方案对比,理由可被评审冷读检验;没有真实决策点就写"不适用",不表演对比。
- **YAGNI**:只为已确认的需求设计,不为想象中的未来引入抽象层、接口、配置项。

## 任务清单(计划的收尾,机器可读)

```markdown
## 任务清单

- [ ] T-1 <打通最薄端到端路径> (覆盖: FR-1) — 判据: <哪些测试通过即完成>
- [ ] T-2 <...> (覆盖: FR-2, NFR-1) — 判据: <...>
```

- 格式固定为 `- [ ] T-<n> ...`,gate 靠它机械校验;勾选状态只存在于此(唯一事实源)。
- 每个任务一次 TDD 循环内可完成,有可判定的完成判据;按依赖排序,T-1 优先打通最薄端到端路径(walking skeleton)。
- "覆盖"标注必须穷尽全部 FR/NFR。
- frame 基线失败且尚未修复的,T-1 必须是"恢复环境基线"。

## 档位 2:一份 plan.md

按 `references/plan-template.md` 写 `features/<NNN>-<slug>/plan.md`(需求 → 设计 → 测试策略 → 任务清单)。自检后按 `hf-review` 派发 **plan 评审**(需求章节对照 requirements-checklist,设计与任务章节对照 design-checklist,一轮完成),记录落 `reviews/plan-review.md`。

## 档位 3:spec.md 与 design.md 分离

1. 按 `references/spec-template.md` 写 spec.md——只回答 WHAT(需求、范围、约束),出现类名、接口签名、表结构即是越界。派发规格评审(`reviews/spec-review.md`),通过并确认后运行 `gate check --to design`。
2. 按 `references/design-template.md` 写 design.md(架构、关键决策、接口与数据契约、错误处理、测试策略、任务清单)。派发设计评审(`reviews/design-review.md`)。
3. 设计中发现规格缺漏 → 停下,回改 spec.md 并重走规格评审;不在 design 里夹带规格没有的新需求。

## 送评审与循环

自检对照 `skills/hf-review/references/requirements-checklist.md` 与 `skills/hf-review/references/design-checklist.md` 后,按 `hf-review` 派发评审。返回"需修改"时只修 findings 指出的问题,再送复审。评审通过且确认落盘后:运行 `gate check --to build`,PASS 进 `hf-build`,RESULT 行记入 progress.md。

## 红线

- 档位 2 的 plan.md 膨胀成几百行的双文档堆叠 → 说明该升档位 3,回 hf-frame 重估
- 验收标准写成"功能正常工作"这类不可判定的句子
- 为填模板编造 NFR 阈值(说不出出处的"P95 < 200ms")
- 任务粒度大到一次 TDD 循环装不下,或没有映射到需求编号
- 计划里出现 frame 意图之外的新范围(范围变了 → 回 hf-frame 修订并重估档位)
- 把用户没确认的假设当成已确认事实写入正文

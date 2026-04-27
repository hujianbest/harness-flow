# mdc-workflow (mwf) Skill Node Define

- 定位: `mdc-workflow`（简称 `mwf`）workflow node 的设计契约，定义一个 `mwf-*` skill 如何成为可编排、可恢复、可审计的团队日常开发节点。
- 关联:
  - 最高原则: `docs/mwf-principles/00 soul.md`
  - Skill 写作原则: `docs/mwf-principles/02 skill-anatomy.md`
  - 工件管理约定: `docs/mwf-principles/03 artifact-layout.md`
  - Workflow 架构: `docs/mwf-principles/04 workflow-architecture.md`

## Purpose

本文回答一个问题：

> 一个 `mwf-*` skill 要成为 mwf workflow 中的合法节点，应该如何设计？

在 mwf 中，一个 workflow node 就是一个 skill。Router 编排的不是抽象阶段，而是一组面向嵌入式日常开发的 `mwf-*` skills：它们处理明确需求输入、组件 / AR 设计、C / C++ 实现和代码检视。

mwf 过程目录默认使用 `features/AR<id>-<slug>` 和 `features/DTS<id>-<slug>`。测试设计是 AR 实现设计的一部分，不作为独立 `test-design.md` 文件。

本文不维护完整路由表，也不替代每个 skill 的 `SKILL.md`。它定义 skill-as-node 的设计标准。

## Core Definition

一个 mwf skill node 是一个满足以下条件的 `mwf-*` skill：

1. 有唯一、清晰的团队开发职责。
2. 声明它处理的核心对象是什么。
3. 说明该对象如何承接上游输入对象、如何形成下游输出对象。
4. 声明它使用什么方法完成该职责。
5. 能把方法落成具体 workflow todo list。
6. 能读取权威工件，而不是依赖对话记忆。
7. 能产出或评审明确工件、record、evidence 或 handoff。
8. 能给出唯一下一步，或明确阻塞并回到 router。
9. 能被 `mwf-workflow-router` 根据磁盘证据重新进入。

```text
mwf skill node = skill + responsibility + object + methods + workflow todos + artifacts + evidence + handoff
```

## Five Contracts

每个 mwf node skill 必须满足五类 contract。


| Contract          | 回答的问题                    | 常见落点                                     |
| ----------------- | ------------------------ | ---------------------------------------- |
| Identity Contract | 这是什么节点，何时应该加载？           | frontmatter、H1、When to Use               |
| Object Contract   | 这个节点处理什么对象？输入 / 输出对象是什么？ | Object Contract、Workflow、Output Contract |
| Workflow Contract | 它按什么 todo list 执行？       | Workflow、Hard Gates、Verification         |
| Method Contract   | 它用什么工程方法完成职责？            | Methodology、rubric、review checklist      |
| Quality Contract  | 怎么证明做对了，什么时候必须停？         | Hard Gates、Red Flags、Verification、evals  |


## Node Role Types

mwf 节点按职责分类，不按主链顺序分类。


| Role                    | 代表 skill                      | 主职责                                   | 不应承担的事               |
| ----------------------- | ----------------------------- | ------------------------------------- | -------------------- |
| Public Entry            | `using-mwf-workflow`          | 判断 direct invoke 还是 route-first       | 代替 router 恢复全局状态     |
| Router                  | `mwf-workflow-router`         | 基于工件证据决定当前阶段、下一节点和阻塞                  | 代替 leaf skill 写设计或代码 |
| Specify                 | `mwf-specify`                 | 澄清明确输入的需求规格、边界、IR/SR/AR 关系            | 做产品发现、创造需求方向         |
| Spec Review             | `mwf-spec-review`             | 独立审查规格是否清楚、可追溯、可设计                    | 顺手回写规格或替负责人拍板        |
| Component Design        | `mwf-component-design`        | 产出或修订组件实现设计                           | 编写 AR 代码层设计          |
| Component Design Review | `mwf-component-design-review` | 独立评审组件实现设计                            | 顺手改设计                |
| AR Design               | `mwf-ar-design`               | 基于 AR 与组件设计编写 AR 实现设计和测试设计            | 改写组件架构或直接编码          |
| AR Design Review        | `mwf-ar-design-review`        | 独立评审 AR 实现设计、测试设计与追溯                  | 代替开发人员回修             |
| Implementation          | `mwf-tdd-implementation`      | 基于 AR 设计和测试设计进行 C / C++ TDD 实现        | 跳过测试、改变 AR 范围        |
| Test Checker            | `mwf-test-checker`            | TDD 完成后独立审查已编写测试用例是否有效、可执行、覆盖关键风险   | 代替实现节点补写测试或修改生产代码    |
| Code Review             | `mwf-code-review`             | 检查 C / C++ 代码质量、SOA 边界、内存 / 并发 / 实时风险 | 代替编译、测试或实现           |
| Completion Gate         | `mwf-completion-gate`         | 判断 AR / 问题修改是否满足完成条件                  | 制造缺失证据               |
| Finalize                | `mwf-finalize`                | 汇总交付记录、同步状态、形成 handoff                | 混入新实现或新需求            |
| Hotfix / Problem Fix    | `mwf-problem-fix`             | 处理缺陷复现、根因、最小安全修复和回流                   | 绕过设计与验证              |


## Object Contract

mwf skill node 必须明确它处理的对象。


| Node                     | Frontend Input Object   | Primary Object                        | Backend Output Object                  | Transformation          |
| ------------------------ | ----------------------- | ------------------------------------- | -------------------------------------- | ----------------------- |
| `mwf-specify`            | 明确输入需求、IR/SR/AR、缺陷单     | requirement specification model       | 澄清后的需求规格、待决问题、AR 边界                    | 把已有需求输入澄清为可设计对象         |
| `mwf-spec-review`        | 需求规格、IR/SR/AR 追溯、待决问题   | spec finding set                      | spec review record、verdict、next action | 把规格对象审查成发现项和迁移结论        |
| `mwf-component-design`   | 组件现状、SR/AR 影响、SOA 接口约束  | component implementation design model | 组件实现设计                                 | 把组件职责、接口、依赖、数据和运行机制写成设计 |
| `mwf-ar-design`          | AR、组件实现设计、团队模板          | AR implementation design model        | 含测试设计章节的 AR 实现设计                      | 把单个 AR 转成代码层设计和可执行测试意图  |
| `mwf-tdd-implementation` | AR 实现设计、测试设计、现有代码       | implementation slice                  | C / C++ code change、测试证据、handoff       | 把设计对象实现成被测试证据支撑的代码变化    |
| `mwf-test-checker`       | TDD 后测试代码、测试执行证据、AR 实现设计、AR 规格、组件约束 | implemented test quality finding set  | test-check record、verdict、next action  | 把已落地测试用例审查成覆盖性、有效性和可维护性结论 |
| `mwf-code-review`        | diff、AR 设计、组件设计、测试证据    | code quality finding set              | code review record、verdict、next action | 把实现对象检查成发现项和迁移结论        |
| `mwf-completion-gate`    | 设计、代码、检视、测试证据           | completion evidence bundle            | 完成结论、返工节点或 finalize 信号                 | 把多源证据判定为能否完成            |


Object Contract 要避免三类错误：

- 把用户输入的自然语言需求直接当成 AR 实现设计。
- 把组件实现设计和 AR 实现设计混写。前者描述组件，后者描述需求代码层实现。
- 把 TDD 中写出的测试用例当成天然有效。TDD 完成后，测试用例仍必须经过 `mwf-test-checker` 审查其覆盖性、有效性和可维护性。

## Method Contract

mwf 节点必须声明采用的方法，并说明方法如何支撑对象转换。

常见方法包括：

- **Requirements Traceability**: 保持 IR -> SR -> AR -> design -> code -> test -> verification 追溯。
- **SOA Component Boundary Analysis**: 检查组件职责、接口、服务契约、依赖方向和跨组件影响。
- **Clean Architecture Boundary Discipline**: 保持组件边界、依赖方向和稳定接口，不让实现细节倒灌到上层。
- **SOLID / GRASP**: 指导 AR 代码层设计保持职责清晰、低耦合、高内聚和可测试性。
- **C / C++ Defensive Design**: 关注内存、生命周期、错误处理、并发、实时性、资源释放和 ABI / API 兼容。
- **MISRA / CERT / Team Coding Standard**: 将团队 C / C++ 编码规范、静态分析和安全规则作为实现与 review 输入。
- **Template-Constrained Design**: 组件实现设计和 AR 实现设计必须符合团队模板。
- **Test Design Before Implementation**: AR 实现设计中以章节形式先声明测试用例，再进入 TDD。
- **Embedded TDD**: 以可运行的单元 / 集成 / 仿真测试驱动实现。
- **Refactoring Discipline**: 在 TDD 的 REFACTOR 步只做与当前 AR 相关、可解释、可验证的重构，不顺手改架构。
- **Post-TDD Test Effectiveness Review**: TDD 完成后独立检查已落地测试用例是否覆盖 AR 行为、边界、异常路径和嵌入式风险。
- **Static / Dynamic Quality Inspection**: 编译告警、静态分析、代码检视和可运行测试共同组成质量证据。

方法不能只出现在概念说明中。凡是会影响节点行为的方法，必须落到 workflow step、hard gate、review rubric 或 verification 中。

## Workflow Contract

每个 mwf skill 的 `Workflow` 必须写成带对象和方法的 todo list。

推荐格式：

```markdown
1. Precheck activation.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

2. Perform node-specific work.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

3. Write artifact / evidence / record.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:

4. Handoff.
   - Object:
   - Method:
   - Input:
   - Output:
   - Stop / continue:
```

每一步都必须支撑本节点职责达成。不能为了“看起来严谨”堆无关检查。

## Quality Contract

mwf skill node 必须定义 hard gates、red flags 和 verification。

常见 hard gates：

- IR / SR / AR 追溯关系缺失或冲突。
- AR 不属于唯一组件，或组件归属不清。
- 组件实现设计缺失，但当前 AR 修改依赖组件边界、接口或架构判断。
- AR 实现设计缺失测试设计，不能进入 TDD 实现。
- TDD 完成后的测试用例未经 `mwf-test-checker` 审查，不能进入后续代码质量闭环。
- 代码修改绕过 SOA 接口、破坏组件边界或引入隐式跨组件依赖。
- C / C++ 代码存在未解释的内存、并发、实时性、资源生命周期或错误处理风险。
- 存在未解释的 critical 静态分析 / 编译告警 / 编码规范违反项。
- review / verification 结论无法唯一决定下一步。

## Output And Handoff Contract

mwf 节点完成时，最小 handoff 应包含：

- `current_node`
- `object_summary`
- `result` 或 `verdict`
- `artifact_paths`
- `record_path`
- `evidence_summary`
- `traceability_links`
- `blockers`
- `next_action_or_recommended_skill`
- `reroute_via_router`，如适用

约束：

- `next_action_or_recommended_skill` 必须使用 canonical `mwf-*` 节点名。
- 设计、检视、测试结论必须落盘。
- 下一步不唯一时，必须回到 `mwf-workflow-router`。

## Design Checklist For New mwf Nodes

新增或重写一个 `mwf-*` skill 前，至少检查：

- 是否有独立团队开发职责，而不是现有节点的子步骤？
- 是否属于明确 node role？
- primary object 是什么？
- frontend input object 和 backend output object 是什么？
- 是否说明对象转换、边界和不变量？
- 是否清楚区分组件实现设计、AR 实现设计、代码实现和验证证据？
- 是否声明采用的方法，并落到 workflow / hard gate / verification？
- 是否读取必要上游工件，而不是依赖对话记忆？
- 是否能产出可回读 artifact / record / evidence？
- 是否能给出唯一 canonical next action？
- 是否覆盖嵌入式代码质量风险和组件边界风险？


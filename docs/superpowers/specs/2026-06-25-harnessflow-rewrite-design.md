# HarnessFlow 重写设计（对齐 DevFlow 架构）

- 日期：2026-06-25
- 状态：已批准（设计层面），待 spec 复核后进入实现计划
- 参考设计：`E:\workspace\devflow`（DevFlow 2.0）
- 目标仓库：`/mnt/e/workspace/harness-flow`

---

## 1. 背景与目标

HarnessFlow 当前有 **41 个技能**，存在严重的重复与结构膨胀：3 个 spec 技能（`hf-spec`/`hf-specify`）、3+ 个 design 技能、6 个 review 技能、2-3 个 discovery 技能、3 个重叠路由（`using-hf` + `using-hf-workflow` + `hf-workflow-router`），且缺少统一的质量模型主线。coding-standards 体积失控（cpp 603 行、java 586、python 566）。

本次重写目标：

1. **全面对齐 DevFlow 2.0 的精简架构**：三层质量模型 + 单阶段单技能 + overlay，把 41 个技能收敛到 **15 个**。
2. **让每个技能达到高星仓库蒸馏出的质量契约**：可判定规则、❌/✅ 正反例、反合理化表、自检清单、evals、范围纪律。
3. **重做 coding-standards**：按 DevFlow 契约蒸馏（≤300 行、语言级规则、工具链真实命令、evals ≥3），来源经 GitHub 检索确认权威性。
4. **绿地重写**：保留 `hf-` 命名与平台适配（commands/install/marketplace/Cursor/OpenCode 镜像），兼容已安装用户。
5. **文档中文为主**，README 保留中英双版本。

协作姿态、流程闭环、工件约定、运行模式均继承自 DevFlow。

---

## 2. 设计原则

### 2.1 三层质量模型（自外向内）

| 层 | 回答的问题 | 失败模式（无此层时） | 承载技能 |
|---|---|---|---|
| **第一层 SDD** | 做的是不是对的事？ | 需求含糊 → 模型靠猜 → 做错事 | `hf-specify` |
| **第二层 TDD** | 功能被证明正确了吗？ | 代码未验证 → 一堆 bug 给人 | `hf-tdd` |
| **第三层 Clean Code** | 代码本身写得好吗？ | 能跑但烂 → 难维护/审查/演进 | `hf-clean-code` + `*-coding-standards` + 领域 overlay |

前两层保证外部质量（做对的事、做对），第三层保证内在质量（做好）。`hf-design` 通过结构、接口契约、错误模型和测试设计为第三层奠基。三层不是三个产物，而是同一份代码的三个维度。目标一句话：**在 SDD 范式下生成 Clean Code，而不是仅仅能运行的代码。**

### 2.2 主流程闭环

```text
specify → R1 review → design → R2 review → tdd → R3 review → ship
```

缺陷旁路：

```text
fix → tdd → R3 review → ship
```

R1/R2/R3 是必经评审门禁（独立上下文，作者不自审），不是可选预审。

### 2.3 HF Skill 质量契约（每个技能必须满足）

蒸馏自 Superpowers（~237k★）、anthropics/skills（~155k★）、ComposioHQ/awesome-claude-skills（~66k★）、PatrickJS/awesome-cursorrules（~40k★）的共性：

1. frontmatter `description` = **触发条件**（含正/负触发），不总结流程。
2. 篇幅：阶段技能 ≤ ~400 行；coding-standards ≤ ~300 行；长尾进 `references/`。
3. 每条规则三要素：**可判定**（能裁定违规/不违规）+ **事故类**（防止什么失败）+ **❌/✅ 正反例**（目标语言/场景真实代码）。
4. **反合理化表**：点名具体偷懒话术 + 反驳。
5. **自检清单**：每个主题节 ≥1 可勾选项。
6. `evals/evals.json` ≥3 压力场景，覆盖该技能最高危失败。
7. 单一职责 + **范围纪律**（明确"不做什么"，堵住膨胀）。
8. artifact-first 恢复；祈使句 + 解释 why，不堆砌 `MUST`。

### 2.4 协作姿态与角色分离

- **human-on-the-loop**：AI 干活，人站在环上审查关键产物（规格、设计、测试、代码）。
- 三条硬规则：**作者不自审；评审者不动手修；人做最终把关。**
- 证据优于记忆：进度从 `plan.md`、`reviews/`、`traceability.md`、工件文件恢复，不依赖聊天记忆。

---

## 3. 目标技能集与旧→新合并图（41 → 15）

核心集（13）+ 领域 overlay（2）= 15。

| # | 新技能 | 类型 | 合并/吸收的旧技能 |
|---|---|---|---|
| 1 | `using-hf` | 入口 | `using-hf` + `using-hf-workflow` + `hf-workflow-router`（三路由 → 单入口 + `plan.md` 轻量状态机） |
| 2 | `hf-specify` | 阶段·SDD | `hf-spec` + `hf-specify` + `hf-discovery` + `hf-product-discovery` |
| 3 | `hf-design` | 阶段·设计 | `hf-design` + `hf-ui-design` + `hf-ui`（UI surface 作 conditional 段） |
| 4 | `hf-tdd` | 阶段·TDD | `hf-build` + `hf-test-driven-dev` + `hf-subagent-driven-dev` + `hf-tasks` + `hf-tasks-review` |
| 5 | `hf-review` | 阶段·评审 | `hf-review` + `hf-code-review` + `hf-test-review` + `hf-spec-review` + `hf-design-review` + `hf-discovery-review` + `hf-traceability-review` + `hf-gap-analyzer`（单技能承载 R1/R2/R3） |
| 6 | `hf-ship` | 阶段·收尾 | `hf-finalize` + `hf-verify` + `hf-completion-gate` + `hf-regression-gate` + `hf-doc-freshness-gate` + `hf-release` + `hf-browser-testing`（DoD/promotion/closeout） |
| 7 | `hf-fix` | 阶段·缺陷 | `hf-hotfix` |
| 8 | `hf-clean-code` | overlay | 重写现有 `hf-clean-code` |
| 9 | `c-coding-standards` | overlay | 按契约重写（旧 105 行偏薄，补齐正反例/工具链/evals 至 ≤300） |
| 10 | `cpp-coding-standards` | overlay | 瘦身重写（603 → ≤300） |
| 11 | `java-coding-standards` | overlay | 瘦身重写（586 → ≤300） |
| 12 | `python-coding-standards` | overlay | 瘦身重写（566 → ≤300） |
| 13 | `coding-standards-creator` | 工具 | 新增（对齐 DevFlow：把团队规范 → 语言技能） |
| 14 | `backend-development` | 领域 | 新增（API/数据/并发契约） |
| 15 | `frontend-development` | 领域 | 新增（含 UI 测试；吸收 browser-testing 的 playwright 要点） |

### 3.1 显式删除（范围纪律）

`hf-experiment`、`hf-ultrawork`、`hf-wisdom-notebook`、`hf-context-mesh`、`hf-ui-review`、`hf-increment`（范围变更逻辑并入 `using-hf` 路由：回 `hf-specify`）。

### 3.2 范围变更（increment）的处理

DevFlow 不把"需求变更"建模为独立缺陷技能。范围变更 = 回 `hf-specify` 修订规格 → 重走受影响的门禁。`using-hf` 的路由表与恢复表覆盖这一情况，不再单列 `hf-increment`。

---

## 4. 运行模式（继承 DevFlow attended / unattended）

工作流启动时**先问用户一次**运行模式，并记入 `plan.md` 头部。恢复执行的会话沿用 `plan.md` 中的模式，不重新猜测。用户未明确回答时按 `attended` 执行。

| 模式 | 行为 |
|---|---|
| `attended`（默认） | R 节点通过后停下，把评审记录与 verdict 呈给人确认后才进入下一阶段；TDD 任务之间不停顿；可由 AI 修复的 findings 仍先自动返工复审，不把修文/补测试/改代码的细节抛给人决策 |
| `unattended` | R 节点后不停顿连续执行，便于长时间运行；仅在缺业务事实、规格/设计不可决策、专家裁决、3 轮仍不通过时停下 |

**`unattended` 只移除人工停顿，不移除任何质量动作**：独立评审照做、评审记录照写、critical findings 照样阻塞（返工修复并复审，而非带病推进）、DoD 照核验。所有评审记录留存在 `reviews/`，供人事后统一审计。

补充语义（贯穿各阶段技能，实现时必须一致）：

- attended 的人工确认**附着在对应 R 节点 verdict 之后**，不替代独立评审，也不发生在评审之前。
- 同一 R 节点最多自动返工复审 **3 轮**，仍不通过则升级人裁决（写入 `reviews/` 并停下）。
- 无论哪种模式，TDD 任务完成后都按 `plan.md` 自动续跑到下一个唯一可执行任务；只有 `hf-specify`/`hf-design` 中无法由 AI 决定的业务规则、验收阈值、架构边界、专家取舍，TDD 队列无法唯一判定，以及自动返工达 3 轮上限，才需要向人提问。
- 评审 verdict 为"重新设计"或 findings 指向规格/设计漂移时，回 `hf-design`/`hf-specify` 修正上游工件并重走受影响门禁。

---

## 5. `using-hf` 结构（继承 `using-devflow` 写法）

`using-hf` 是单一入口，章节结构镜像 `using-devflow`，内容做 HarnessFlow 适配：

1. **HarnessFlow 是什么** — 三层质量模型表（层 / 问题 / 失败模式 / 承载技能）+ human-on-the-loop + 工件可冷读可审查的硬要求。
2. **工作流** — ASCII 流程图（`[0] 确认运行模式 → [1] specify → [R1] review → [2] design → [R2] review → [3] tdd → [R3] review → [4] ship`），评审是必经节点不是可选预审的说明。
3. **轻量状态机** — 不维护独立路由器或额外状态文件；`plan.md` 的门禁表 + 任务状态 + `reviews/` 记录即状态。门禁三态：`pending`（去评审）/ `passed`（verdict 通过，attended 还看人工确认列）/ `rework`（先修再评审）。R1 rework 默认回 `hf-specify`；R2 回 `hf-design`；R3 回 `hf-tdd`。
4. **Todo 投影规则** — 阶段节点、R 门禁节点、ship 节点是一级待办；TDD 内部任务不是多个人工确认节点；rework 不等于"立刻再评审"。
5. **运行模式** — attended/unattended 表与语义（见第 4 节）。
6. **何时可以裁剪** — 微小修改（spec 压成一段验收标准、design 省略、R1/R2 合并入 R3，但 TDD/R3/clean-code 不裁）；纯重构（无需 spec/design，但行为不变测试先行且 R3 照做）；拿不准不裁剪。裁剪的是文档量，不是质量门槛。
7. **工件约定** — 路径解析纪律（相对于目标组件仓库根，非会话目录；优先用户显式指定 → `AGENTS.md` 声明 → 当前组件仓库根）；工作项目录结构；恢复进度表（磁盘状态 → 下一步）。
8. **行为准则** — 7 条不可协商：不默默补全模糊需求 / 困惑停下不猜 / 方案有问题就说 / 强制简单 / 范围纪律 / 验证而非声称 / 作者不自审且阶段必评审。
9. **技能地图** — 一句话 + 何时读；语言与领域技能按命名约定/描述发现，是叠加约束。

工作项工件（`features/<id>-<slug>/`）：`spec.md`、`traceability.md`、`design.md`、`plan.md`（中断恢复单一入口）、`reviews/`、`closeout.md`/`fix.md`。长期资产在组件根 `docs/`（`component-design.md`、`ar-specs/`、`ar-designs/`），由 `hf-ship` 收尾时 promotion。

---

## 6. 逐技能质量标准与蒸馏来源

| 技能 | 质量重点 | 蒸馏/参考来源 |
|---|---|---|
| 全部阶段技能 | 触发条件 description、反合理化表、artifact-first 恢复、evals | DevFlow 同名技能 + Superpowers（verification-before-completion、writing-skills、test-driven-development） |
| `hf-specify` | EARS/BDD 验收、NFR QAS、可测试性、防"模型靠猜" | devflow-specify |
| `hf-design` | 接口契约、错误模型、测试设计、UI surface 判定（conditional） | devflow-design |
| `hf-tdd` | RED→GREEN→REFACTOR 证据行、Context Pack、assertion 强度、mock 边界、运行模式续跑 | devflow-tdd + Superpowers TDD |
| `hf-review` | 作者/评审分离、findings+resolution 闭环、独立上下文、attended 确认点 | devflow-review |
| `hf-ship` | DoD 核验、promotion 长期资产、closeout | devflow-ship |
| `hf-fix` | 复现 → 根因 → 最小修复边界，修复回 TDD | devflow-fix |
| `hf-clean-code` | 五维（简洁/可靠/可维护/可测试/高性能）+ 反投机抽象 + GREEN 改行为/REFACTOR 改表达 | devflow-clean-code |
| `c-coding-standards` | UB/整数溢出/手工内存所有权/宏陷阱/不安全 libc | CERT C + cppbestpractices；`gcc -std=c17 -Wall -Wextra -Werror -Wconversion`、ASan/UBSan、cppcheck、clang-tidy |
| `cpp-coding-standards` | RAII/Rule-of-5、生命周期/UB、move/noexcept、异常安全、concepts | C++ Core Guidelines + cppbestpractices；`g++ -std=c++20 ...`、clang-tidy |
| `java-coding-standards` | null/Optional、equals/hashCode、泛型 PECS、并发、try-with-resources | Google Java Style + Effective Java；google-java-format、ErrorProne、SpotBugs |
| `python-coding-standards` | 可变默认参数、异常 EAFP、资源 with、类型注解、相等 vs 身份 | PEP 8 + Google Pyguide + Effective Python；`ruff` + `mypy --strict` + `bandit` |
| `coding-standards-creator` | 归属判定 → 三要素改写 → 契约 → evals | devflow coding-standards-creator + coding-standards-skill-contract |
| `backend-development` | API 契约、数据所有权、并发与一致性、错误模型 | devflow backend-development |
| `frontend-development` | 组件边界、状态管理、UI 测试（playwright smoke）、可访问性 | devflow frontend-development + 旧 hf-browser-testing |

每个语言标准必须：声明"叠加在 `hf-clean-code` 之上、不替代它"；含**工具链节**（真实命令 + 基线，"历史就有"不豁免本次触碰）；含 `evals/`（≥3 高危场景）。

---

## 7. 文件结构与平台适配保留

```text
harness-flow/
├── skills/                    # 15 个技能
│   └── <name>/{SKILL.md, references/, evals/evals.json, test-prompts.json}
├── commands/                  # 斜杠命令重映射
├── agents/
│   ├── hf-implementer.md      # 单任务 + Context Pack（对齐 devflow-implementer）
│   └── hf-reviewer.md         # 独立评审、不修改（对齐 devflow-reviewer）
├── scripts/
│   └── validate_harnessflow.py  # 技能清单 + 契约一致性校验（对齐 validate_devflow.py）
├── tests/                     # pytest 契约/一致性测试
├── install.sh / .claude-plugin/  # 保留并更新技能清单（兼容已安装用户）
├── README.md / README.zh-CN.md
└── docs/{harnessflow-philosophy.md, harnessflow-core-architecture.md, ...}
```

### 7.1 commands 重映射

| 命令 | 目标技能 | 备注 |
|---|---|---|
| `/hf` | `using-hf` | 入口/恢复 |
| `/spec` | `hf-specify` | |
| `/plan` | `hf-design` | |
| `/build` | `hf-tdd` | |
| `/review` | `hf-review` | |
| `/ship` | `hf-ship` | |
| `/fix` | `hf-fix` | 新增 |
| ~~`/release`~~ | 删除 | release 并入 `hf-ship` |

命令是 bias 不是 bypass：仍按 on-disk 工件决定真实下一步（对齐 DevFlow 约定）。

### 7.2 校验门禁

- `python3 scripts/validate_harnessflow.py`：技能清单存在性 + frontmatter 合规 + 篇幅上限 + 每技能有 `evals/` + 旧技能名无残留引用。
- `python3 -m pytest tests/`：契约一致性测试。
- 二者作为实现与收尾的硬门禁。

---

## 8. 执行顺序（落地分阶段，每阶段可验证）

1. **骨架先行**：仓库结构 + `using-hf`（含三层模型、工作流、`plan.md` 状态机、attended/unattended）+ `scripts/validate_harnessflow.py` + `docs/harnessflow-philosophy.md` / `harnessflow-core-architecture.md`。
2. **阶段技能**（按闭环顺序，每个同步写 `evals/` 与 `references/`）：`hf-specify` → `hf-design` → `hf-tdd` → `hf-review` → `hf-ship` → `hf-fix`。
3. **overlay**：`hf-clean-code` → 4 个语言标准（按第 6 节来源蒸馏）→ `coding-standards-creator` → `backend-development` → `frontend-development`。
4. **适配层收尾**：commands 重映射、`agents/hf-implementer.md` + `hf-reviewer.md` 对齐、`install.sh`/`.claude-plugin`/Cursor/OpenCode 镜像更新、删除被合并的旧技能目录、README 与 philosophy 文档更新。
5. **校验**：`validate_harnessflow.py` + `pytest` 全绿；grep 确认无旧技能名残留引用；README 技能表与 `EXPECTED_SKILLS` 一致。

---

## 9. 验收标准

- [ ] `skills/` 恰好 15 个技能，命名与第 3 节一致。
- [ ] 每个技能满足第 2.3 节质量契约（触发条件 description、可判定规则、正反例、反合理化表、自检清单、evals ≥3）。
- [ ] coding-standards 全部 ≤300 行、含工具链节、声明叠加在 `hf-clean-code` 之上。
- [ ] `using-hf` 章节结构镜像 `using-devflow`，含 attended/unattended 与 `plan.md` 状态机。
- [ ] attended/unattended 语义在 `hf-review`/`hf-tdd`/`hf-ship` 中一致落地。
- [ ] commands 与第 7.1 节一致（删 `/release`、增 `/fix`）。
- [ ] `validate_harnessflow.py` + `pytest` 全绿；无旧技能名残留引用。
- [ ] README（中英）技能表、`.claude-plugin`、install 清单更新一致。

---

## 10. 范围外

- 不做 automotive/embedded 领域 overlay（后续可按 DevFlow 契约扩展）。
- 不重写平台宿主适配机制本身（OpenCode/Cursor 安装方式不变，仅更新技能清单）。
- 不引入独立路由器或额外状态文件（`plan.md` 即状态）。
- 不保留 `hf-experiment`/`hf-ultrawork`/`hf-wisdom-notebook`/`hf-context-mesh`。

---

## 11. 决策记录

| 决策 | 选择 | 理由 |
|---|---|---|
| 目标架构 | 全面对齐 DevFlow（~15 技能） | 结构最干净，三层质量模型收益完整 |
| 迁移方式 | 绿地重写，保留 hf- 命名 + 平台适配 | 质量最高、一次性到位，兼容已安装用户 |
| 文档语言 | 中文为主，README 中英双版本 | 对齐 DevFlow 风格与日常沟通语言 |
| 领域 overlay | 仅 backend + frontend | 通用价值最高，automotive/embedded 延后 |
| 删除清单 | experiment/ultrawork/wisdom-notebook/context-mesh/ui-review/increment | 范围纪律，防再膨胀 |
| commands | 删 `/release`、增 `/fix` | release 并入 ship；fix 是缺陷旁路独立入口 |
| 运行模式 | 继承 DevFlow attended/unattended | unattended 支持长会话，但不降质量门槛 |
| using-hf | 镜像 using-devflow 写法 | 入口一致性，继承被验证的结构 |

---

## 12. 研究来源（蒸馏依据）

**Skill 质量模式**：obra/Superpowers、anthropics/skills、ComposioHQ/awesome-claude-skills、PatrickJS/awesome-cursorrules、VoltAgent/awesome-agent-skills。

**语言标准来源**：CERT C、cppbestpractices（C/C++）；C++ Core Guidelines、Google C++ Style Guide（C++）；Google Java Style Guide、Effective Java、ErrorProne、SpotBugs（Java）；PEP 8、Google Python Style Guide、Effective Python、ruff/mypy/bandit（Python）。

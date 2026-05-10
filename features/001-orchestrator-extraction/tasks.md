# HF Orchestrator Extraction & Skill Decoupling 任务计划

- 状态: 草稿
- 主题: 把 workflow 编排从 leaf skill 抽出为 always-on agent persona（v0.6.0 范围 = ADR-007 D3 Step 1）
- 上游 spec: `features/001-orchestrator-extraction/spec.md`（approved）
- 上游 design: `features/001-orchestrator-extraction/design.md`（approved）
- 上游 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`

## 1. 概述

把 design § 11 的 14 个模块拆解为 12 个可独立 TDD 推进的任务（T1 / T2.{a,b,c,d} / T3 / T4 / T5 / T6.{a,b} / T7 / T8 实现层）+ **1 个 collation task**（T9，跨任务收口节点；不产出新文件，只校验完整性 + 状态同步）。任务设计原则：

- **每任务对应 design § 11 的一组职责相关模块**，避免单文件 task 过细
- **acceptance 锚定 spec FR/NFR + design D-X**，可冷读判定
- **fail-first 入口**：每任务在 RED 步先证伪（grep / wc / file-existence 类断言）
- **task-002 (3 宿主 stub) 按 design D-FR2-Tasks 拆为 4 sub-tasks**（每宿主独立 + identity gate 独立）
- **task-006 (docs sync) 按 D-FR2-Tasks FR-006 类比拆为 2 sub-tasks**（README ×2 vs setup docs ×3）

## 2. 里程碑

| 里程碑 | 包含任务 | 退出标准 | 对应需求 / 设计依据 |
|---|---|---|---|
| **M1: 物理层就位** | T1 / T3 / T2.{a,b,c,d} | orchestrator persona 文件 + 9 references 迁移 + 旧 skill stub + 3 宿主 always-on stub 全部到位；deprecated alias body marker grep 命中 | spec FR-001 / FR-002.a-d / FR-004；design D-Layout / D-Mig / D-Stub / D-Stub-Marker / D-Host-Cursor / D-Host-CC / D-Host-OC / D-Identity |
| **M2: 验证基础设施** | T4 | regression-diff.py 编写 + 自一致性测试通过 + mutation 测试拒绝白名单外差异 | spec NFR-005 / FR-003；design D-RegrLoc / D-RegrImpl |
| **M3: 等价语义实测** | T5 | walking-skeleton 实跑 + regression-diff.py PASS + 3 宿主 smoke + identity gate + load-timing 量化 | spec FR-003 / NFR-001 / NFR-004；HYP-002 / HYP-003 (release-blocking) |
| **M4: 文档与版本同步** | T6.{a,b} / T7 / T8 | README / setup docs / CHANGELOG / plugin manifest / 项目元数据全部 v0.6.0 ready | spec FR-006 / FR-007；design D-Layout 模块表 |
| **M5: 收尾** | T9 | features/001-orchestrator-extraction/ 各 reviews / verification / approvals 齐全；准备进入 hf-test-review chain | hf-tasks Workflow step 4 + design § 16 / § 18 |

## 3. 文件 / 工件影响图

### 创建（M1 + M2）
- `agents/hf-orchestrator.md` (新)
- `agents/references/{execution-semantics,profile-node-and-transition-map,profile-selection-guide,review-dispatch-protocol,reviewer-return-contract,routing-evidence-examples,routing-evidence-guide,ui-surface-activation,workflow-shared-conventions}.md` (新；从 `skills/hf-workflow-router/references/` 迁移)
- `CLAUDE.md` (新；仓库根 always-on stub)
- `AGENTS.md` (新；仓库根 always-on stub)
- `features/001-orchestrator-extraction/scripts/regression-diff.py` (新；M2)
- `features/001-orchestrator-extraction/scripts/test_regression_diff.py` (新；M2 自测)

### 修改
- `.cursor/rules/harness-flow.mdc` (body 改为指向 `agents/hf-orchestrator.md`；保留 frontmatter)
- `skills/using-hf-workflow/SKILL.md` (转 deprecated alias，≤30 行)
- `skills/hf-workflow-router/SKILL.md` (同上)
- `skills/hf-workflow-router/references/*.md` (9 个，每个转 redirect stub ≤ 10 行)
- `.claude-plugin/plugin.json` (version 0.5.1 → 0.6.0；尝试注册 orchestrator agent)
- `.claude-plugin/marketplace.json` (description 同步)
- `README.md` / `README.zh-CN.md` (Scope Note 加 v0.6.0 段)
- `docs/cursor-setup.md` / `docs/claude-code-setup.md` / `docs/opencode-setup.md` ("如何启用 HF" 段更新)
- `CHANGELOG.md` ([Unreleased] 加 v0.6.0 子段)
- `SECURITY.md` (Supported Versions v0.5.x → v0.6.x)
- `CONTRIBUTING.md` (引言版本号)

### 落盘验证记录（M3 / M5）
- `features/001-orchestrator-extraction/verification/regression-2026-05-XX.md`
- `features/001-orchestrator-extraction/verification/smoke-3-clients.md`
- `features/001-orchestrator-extraction/verification/load-timing-3-clients.md`

## 4. 需求与设计追溯

| 任务 | spec FR / NFR | design D-X 决策 | release-blocking? |
|---|---|---|---|
| T1 | FR-001 | D-Layout / D-Identity | 是（HYP-002 间接） |
| T2.a | FR-002.a | D-Host-Cursor | 是（HYP-003） |
| T2.b | FR-002.b | D-Host-CC | 是（HYP-003） |
| T2.c | FR-002.c | D-Host-OC | 是（HYP-003） |
| T2.d | FR-002.d | D-Identity | 是（HYP-003） |
| T3 | FR-004 / NFR-003 | D-Mig / D-Stub / D-Stub-Marker | 否 |
| T4 | FR-003 / NFR-005 | D-RegrLoc / D-RegrImpl | 否（infra） |
| T5 | FR-003 / NFR-001 / NFR-004 | D-NFR1-Schema | **是**（HYP-002 + HYP-003 双 release-blocking） |
| T6.a | FR-006.a | — | 否 |
| T6.b | FR-006.b | — | 否 |
| T7 | FR-007 | — | 否 |
| T8 | （ADR-005 立场延续；version bump） | — | 否 |
| T9 | hf-tasks Step 4 | — | 否 |

## 5. 任务拆解

### T1. 创建 orchestrator persona 主文件 + references 迁移

- **目标**: 在 `agents/hf-orchestrator.md` 落 always-on persona 主文件；同 commit 把 9 个 references 物理迁到 `agents/references/`（git mv 保留 history）
- **Acceptance**:
  - **(T1.a)** `agents/hf-orchestrator.md` 存在，frontmatter 含 `name: hf-orchestrator` + `description` 段
  - **(T1.b)** 文件第 2 段（H1 后第一段）含 grep 锚点 `"I am the HF Orchestrator"` 或等价中文
  - **(T1.c)** `wc -c agents/hf-orchestrator.md` ≤ 23,245 bytes（baseline 21,132 × 1.10；NFR-002）
  - **(T1.d)** `agents/references/` 含恰好 9 个文件，文件名与 `skills/hf-workflow-router/references/` 一致；`diff agents/references/<x>.md skills/hf-workflow-router/references/<x>.md.bak` 在迁移前应等价（`git mv` 后旧路径已为 stub）
  - **(T1.e)** orchestrator 主文件中所有 references 引用指向 `agents/references/`，**不**指向旧路径
- **依赖**: 无（M1 起点）
- **Ready When**: design approved（已满足）；分支 `cursor/orchestrator-extraction-impl-e404` 创建
- **初始队列状态**: ready
- **Selection Priority**: P0 + critical-path
- **Files / 触碰工件**: `agents/hf-orchestrator.md` (新); `agents/references/*.md` (9 个，新)
- **测试设计种子**:
  - 主要行为：persona 文件存在 + identity 锚点 + references 完整 + 字符数预算
  - 关键边界：references 数量恰好 9 个（不多不少）；每个 reference 内容与 baseline 等价
  - fail-first：先 RED `test -f agents/hf-orchestrator.md`（应不存在）→ GREEN 建立后通过
  - SUT Form: `naive`（直接落盘 markdown 文件）
- **Verify**: `wc -c agents/hf-orchestrator.md` + `ls agents/references/ | wc -l` + `grep -E "(I am the HF Orchestrator|我是 HF Orchestrator)" agents/hf-orchestrator.md`
- **预期证据**: shell 命令 + 输出捕获到交接块；NFR-002 commit-time check 通过
- **完成条件**: 上述 5 条 acceptance 全部通过；新文件已 git add + commit

### T2.a. Cursor always-on stub 同步

- **目标**: 修改 `.cursor/rules/harness-flow.mdc` body，从指向 `using-hf-workflow + router` 改为指向 `agents/hf-orchestrator.md`
- **Acceptance**:
  - **(T2.a.1)** 文件保留原 frontmatter（`alwaysApply` 等价语义不变）
  - **(T2.a.2)** body 顶部含一句 "本 workspace 自动以 HF orchestrator persona 启动" + "Read `agents/hf-orchestrator.md` immediately and act as that persona" 等价指令
  - **(T2.a.3)** 原"On every session: 1. Load entry shell ... 2. Hand off to router"两步指令已被替换或更新为指向 orchestrator
  - **(T2.a.4)** Hard rules 段中的版本号 v0.5.1 → v0.6.0 同步
- **依赖**: T1 (orchestrator 主文件存在，否则 stub 指向不存在)
- **Ready When**: T1 GREEN
- **初始队列状态**: blocked-by-T1
- **Selection Priority**: P0
- **Files / 触碰工件**: `.cursor/rules/harness-flow.mdc` (修改 body)
- **测试设计种子**:
  - fail-first: `grep -c "agents/hf-orchestrator.md" .cursor/rules/harness-flow.mdc` 在修改前 = 0；修改后 ≥ 1
  - 关键边界: frontmatter 不被破坏（`head -10` 检查 frontmatter 区域完整）
- **Verify**: `grep "agents/hf-orchestrator" .cursor/rules/harness-flow.mdc` + `head -5 .cursor/rules/harness-flow.mdc`
- **预期证据**: grep 输出 + frontmatter 完整性截图
- **完成条件**: 4 条 acceptance 通过

### T2.b. Claude Code always-on stub + plugin manifest

- **目标**: 仓库根新建 `CLAUDE.md`（含 always-on stub 段）+ 修改 `.claude-plugin/plugin.json` 注册 orchestrator agent（schema 不允许时降级到只 bump version）
- **Acceptance**:
  - **(T2.b.1)** `CLAUDE.md` 存在，含 "## HF Orchestrator (always on)" 段 + "Read `agents/hf-orchestrator.md` and adopt that persona" 指令
  - **(T2.b.2)** `.claude-plugin/plugin.json` `version` 从 `"0.5.1"` 改为 `"0.6.0"`
  - **(T2.b.3)** `.claude-plugin/plugin.json` 验证通过 `python3 -m json.tool` 不报错
  - **(T2.b.4)** 尝试注册 `agents` 字段（如 schema 允许）；不允许时显式记入交接块说明降级
- **依赖**: T1
- **Ready When**: T1 GREEN
- **初始队列状态**: blocked-by-T1
- **Selection Priority**: P0
- **Files / 触碰工件**: `CLAUDE.md` (新); `.claude-plugin/plugin.json` (修改); `.claude-plugin/marketplace.json` (description 同步)
- **测试设计种子**:
  - fail-first: `test -f CLAUDE.md` 修改前 = false；修改后 = true
  - JSON 校验: `python3 -m json.tool < .claude-plugin/plugin.json > /dev/null`
- **Verify**: `cat CLAUDE.md` + JSON validation
- **预期证据**: 命令输出 + 交接块标注 schema 是否接受 `agents` 字段
- **完成条件**: 4 条 acceptance 通过；schema fallback 决策记录

### T2.c. OpenCode always-on stub

- **目标**: 仓库根新建（或已有时追加段）`AGENTS.md`，含 orchestrator stub 段
- **Acceptance**:
  - **(T2.c.1)** `AGENTS.md` 存在
  - **(T2.c.2)** 含 "## HF Orchestrator (always on)" 段 + "Read `agents/hf-orchestrator.md` and act as that persona" 指令
  - **(T2.c.3)** 若 `AGENTS.md` 已有内容（不太可能；本仓库 v0.5.1 没有），追加段而非覆盖
- **依赖**: T1
- **Ready When**: T1 GREEN
- **初始队列状态**: blocked-by-T1
- **Selection Priority**: P0
- **Files / 触碰工件**: `AGENTS.md` (新)
- **测试设计种子**:
  - fail-first: `test -f AGENTS.md` 修改前 = false（验证假设：仓库目前无 AGENTS.md）
  - 关键边界: 若已存在，追加段 + 保留原内容
- **Verify**: `cat AGENTS.md`
- **预期证据**: 文件全文 grep "HF Orchestrator"
- **完成条件**: 3 条 acceptance 通过

### T2.d. 三宿主 identity gate verification

- **目标**: 落盘 `features/001-orchestrator-extraction/verification/smoke-3-clients.md`（**T2.d 是该文件唯一所有者**；T5 引用但不写），记录 3 宿主下的 identity check 实测（新启 session 后输入"who are you"，记录响应是否含 orchestrator identity 锚点）
- **Acceptance**:
  - **(T2.d.1)** verification 文件存在
  - **(T2.d.2)** 文件含 3 个 client 段：Cursor / Claude Code / OpenCode
  - **(T2.d.3)** 每段记录：实测时间、宿主版本（如可知）、user message、agent 响应摘要、identity 锚点是否命中（PASS/FAIL）
  - **(T2.d.4)** 至少 1/3 宿主（Cursor）能够实际验证（cloud agent 当前 session 已在 Cursor 中运行）；其它 2 宿主标 "deferred to manual verification post-merge" 但段必须存在
- **依赖**: T2.a / T2.b / T2.c（stub 必须先就位才能验证）
- **Ready When**: T2.a + T2.b + T2.c 全部 GREEN
- **初始队列状态**: blocked-by-T2.{a,b,c}
- **Selection Priority**: P0（HYP-003 release-blocking）
- **Files / 触碰工件**: `features/001-orchestrator-extraction/verification/smoke-3-clients.md` (新；**T2.d 唯一写入者**)
- **测试设计种子**:
  - 主要行为: 实际 new session 启动 → identity grep PASS
  - 关键边界: cloud agent 自身只能直接验证 Cursor；其它 2 宿主由开发者本地或后续 manual verify（接受 deferred 标记）
  - **fail-first（显式 RED 起点）**: 进入 T2.d 前 `test -f features/001-orchestrator-extraction/verification/smoke-3-clients.md` = false（文件不存在）→ T2.d 完成后 `test -f` = true 且 `grep -c "PASS\|deferred" smoke-3-clients.md` = 3
  - SUT Form: `naive`（纯文档；无 SUT 代码层）
- **Verify**: 文件存在 + 3 段齐全 + Cursor 段标 PASS（其它两段 PASS 或 deferred 均合法）
- **预期证据**: verification record 文件内容 + grep 输出
- **完成条件**: 4 条 acceptance 通过

### T3. 旧 skill 转 deprecated alias + references stub

- **目标**: 把 `skills/using-hf-workflow/SKILL.md` + `skills/hf-workflow-router/SKILL.md` + 9 个 router/references 转 redirect stub
- **Acceptance**:
  - **(T3.a)** 两个 skill SKILL.md frontmatter `description` 含 "deprecated alias, see agents/hf-orchestrator.md"
  - **(T3.b)** 两个 skill SKILL.md 顶部有 HTML 注释 marker `<!-- HF v0.6.0 deprecated alias: see agents/hf-orchestrator.md -->`
  - **(T3.c)** 两个 skill SKILL.md body ≤ 30 行（C-006）；含 deprecation notice + redirect 指引
  - **(T3.d)** 9 个 references 文件每个 ≤ 10 行 stub，含 HTML marker 和 H1 + 一句 redirect "see `agents/references/<same-name>.md`"
  - **(T3.e)** 11 个 stub 文件物理存在（不删除），可通过 `ls` 验证
- **依赖**: T1（references 已迁移到新位置，否则 stub redirect 目标不存在）
- **Ready When**: T1 GREEN（可与 T2.{a,b,c} 同 commit 中并行处理）
- **初始队列状态**: blocked-by-T1
- **Selection Priority**: P0
- **Files / 触碰工件**: `skills/using-hf-workflow/SKILL.md` + `skills/hf-workflow-router/SKILL.md` + 9 个 `skills/hf-workflow-router/references/*.md`
- **测试设计种子**:
  - fail-first: `wc -l skills/using-hf-workflow/SKILL.md` 修改前 = 179；修改后 ≤ 30
  - 关键边界: 文件**不被删除**（NFR-003），用 `test -f` 验证
- **Verify**: 11 个文件 wc -l + grep "deprecated alias" + grep HTML marker
- **预期证据**: 命令输出 + 11 个文件清单
- **完成条件**: 5 条 acceptance 通过

### T4. walking-skeleton regression-diff.py 编写 + 自测

- **目标**: 在 `features/001-orchestrator-extraction/scripts/` 编写 stdlib-only Python 3 diff 脚本 + 配套测试
- **Acceptance**:
  - **(T4.a)** `regression-diff.py` 存在；只 import stdlib（`difflib` / `re` / `sys` / `pathlib` 等；无 npm / pip 依赖）
  - **(T4.b)** 接受 `--baseline-dir` + `--candidate-dir` 两个 CLI 参数
  - **(T4.c)** 容许差异白名单硬编码为正则集合（design D-RegrImpl 列出的 4 条）
  - **(T4.d)** 输出 stdout 含 "PASS" 或 "FAIL"；exit 0 当且仅当 PASS
  - **(T4.e)** `test_regression_diff.py` 配套测试：(i) 自一致性（同一目录 diff 自己 → PASS）；(ii) mutation 测试（人工注入白名单外差异 → FAIL）；(iii) 白名单内差异（注入时间戳变化 → PASS）
  - **(T4.f)** `python3 features/001-orchestrator-extraction/scripts/test_regression_diff.py` 通过（exit 0；至少 3 个 test case 全绿）
- **依赖**: 无（M2 起点；可与 T1 并行）
- **Ready When**: design approved
- **初始队列状态**: ready
- **Selection Priority**: P1
- **Files / 触碰工件**: `features/001-orchestrator-extraction/scripts/regression-diff.py` + `test_regression_diff.py`
- **测试设计种子**:
  - 主要行为: 3 个 test case（自一致性 / mutation / 白名单内差异）
  - 关键边界: 容许白名单覆盖完整 + 白名单外严格 FAIL
  - SUT Form: `naive`（直接函数 + argparse；不引入 Strategy / Factory 等 GoF 模式）
  - fail-first: 先写测试（RED），再实现脚本通过（GREEN），最后 REFACTOR
- **Verify**: `python3 test_regression_diff.py` exit 0
- **预期证据**: 测试输出 stdout 摘要
- **完成条件**: 6 条 acceptance 通过

### T5. Walking-skeleton 实跑 + NFR-001 量化测量 + NFR-004 reviewer 标识检查

- **目标**: 用 T4 脚本对比 v0.5.1 walking-skeleton baseline 与本 commit walking-skeleton（应等价）；采集 NFR-001 wall-clock × 1.20 数据；校验 NFR-004 reviewer 分离纪律
- **INVEST Small 备注**：T5 内部含 3 类异质活动（regression diff / load-timing 测量 / NFR-004 grep），但**共享同一前置条件**（T1+T2+T3+T4 全部 GREEN）+ **共享同一目标**（HYP-002/003 release-blocking 双假设的 fresh evidence 落盘）+ **共享同一可逆点**（任一活动 FAIL → 全 task 回 hf-design）。打包不拆是为了维持 release-blocking 验证的原子性（任一活动 FAIL 都触发同一回滚路径）。如未来发现 hf-test-driven-dev 阶段单独跑某一活动更顺畅，可在 increment ADR 中拆为 T5.a / T5.b / T5.c
- **Acceptance**:
  - **(T5.a)** 跑 `python3 regression-diff.py --baseline-dir <v0.5.1 checkout 的 examples/writeonce/features/001-walking-skeleton/> --candidate-dir <本 commit 的同位置>` 得 PASS
  - **(T5.b)** `verification/regression-2026-05-XX.md` 落盘，记录命令 + 输出 + diff 摘要（**T5 是该文件唯一所有者**）
  - **(T5.c)** NFR-001 wall-clock 测量：在 Cursor 至少 1 个宿主上做 5 次重复 baseline-vs-candidate 测量，记录 raw + ratio **追加到** `verification/load-timing-3-clients.md`；至少已验证宿主的平均 ratio ≤ 1.20（**T5 是该文件唯一所有者**；T2.d 不写此文件）
  - **(T5.d)** 若 ratio > 1.20，立即停 task 回 hf-design 重评 D-Layout（M3 失败 → release-blocking）
  - **(T5.e)** review record 检查 100% 含 "独立 reviewer subagent" 标识（NFR-004；用本 feature 自身的 reviews/ 目录 4 个 review record 作为基线快速验证）
- **依赖**: T1 / T2.{a,b,c,d} / T3 / T4
- **Ready When**: T1 + T2.{a,b,c,d} + T3 + T4 全部 GREEN
- **初始队列状态**: blocked-by-many
- **Selection Priority**: P0（HYP-002 + HYP-003 release-blocking）
- **Files / 触碰工件**: `verification/regression-2026-05-XX.md` (新；T5 唯一所有者) + `verification/load-timing-3-clients.md` (新；T5 唯一所有者；与 T2.d 的 smoke-3-clients.md 物理分文件以避免所有权重叠)
- **测试设计种子**:
  - 主要行为: regression PASS + ratio ≤ 1.20 + 4 个 review record 全部含 "独立 reviewer subagent"
  - 关键边界: cloud agent 上下文限制——可能只能跑 Cursor 宿主测量，其它宿主标 "deferred manual" 写入 load-timing-3-clients.md
  - **fail-first（显式 RED 起点）**: 进入 T5 前 `test -f verification/regression-2026-05-XX.md` = false 且 `test -f verification/load-timing-3-clients.md` = false（两文件均不存在）；T5 完成后两文件均存在且 grep "PASS" 命中
  - SUT Form: `naive`（脚本调用 + 测量记录；无内部抽象）
- **Verify**: regression-diff stdout PASS + load-timing 文件含 ratio 数值 + `grep -c "独立 reviewer subagent" features/001-orchestrator-extraction/reviews/*.md docs/reviews/discovery-review-hf-orchestrator-extraction.md` ≥ 4
- **预期证据**: 上述 3 个 verification 文件齐全 + 命令输出 + grep 计数
- **完成条件**: 5 条 acceptance 通过；HYP-002 / HYP-003 release-blocking 验证完成

### T6.a. README 中英双语 Scope Note 同步

- **目标**: `README.md` + `README.zh-CN.md` 顶部 Scope Note 加 v0.6.0 段
- **Acceptance**:
  - **(T6.a.1)** 两份 README 顶部 Scope Note 含一段说明 v0.6.0 引入 `agents/hf-orchestrator.md`
  - **(T6.a.2)** 两份 README 显式说明：保留 24 个 hf-* skill 数量不变、保留 7 条 slash 命令不变、`hf-release` 行为不变
  - **(T6.a.3)** 两份 README 互相一致（中英对照不漂移）
- **依赖**: T1（orchestrator 文件存在后才能引用）
- **Ready When**: T1 GREEN
- **初始队列状态**: blocked-by-T1
- **Selection Priority**: P1
- **Files / 触碰工件**: `README.md` + `README.zh-CN.md`
- **测试设计种子**:
  - fail-first: `grep -c "v0.6.0" README.md` 修改前 = 0；修改后 ≥ 1
  - 关键边界: 中英对照一致
- **Verify**: 两份文件 head + grep 关键短语
- **预期证据**: grep 输出
- **完成条件**: 3 条 acceptance 通过

### T6.b. Setup docs ×3 同步

- **目标**: `docs/cursor-setup.md` + `docs/claude-code-setup.md` + `docs/opencode-setup.md` 的 "如何启用 HF" 段从"加载 entry shell + router"改为"orchestrator 自动加载，无需手动操作"
- **Acceptance**:
  - **(T6.b.1)** 3 个 setup docs 的 "如何启用 HF" 段全部更新
  - **(T6.b.2)** 每个 doc 引用 `agents/hf-orchestrator.md`
  - **(T6.b.3)** 不动其它 setup 段（diff 只在目标段范围内）
- **依赖**: T1
- **Ready When**: T1 GREEN
- **初始队列状态**: blocked-by-T1
- **Selection Priority**: P1
- **Files / 触碰工件**: `docs/cursor-setup.md` / `docs/claude-code-setup.md` / `docs/opencode-setup.md`
- **测试设计种子**:
  - fail-first: 3 个 doc 修改前不含 "agents/hf-orchestrator.md"；修改后含
- **Verify**: `grep -c "agents/hf-orchestrator" docs/{cursor,claude-code,opencode}-setup.md`
- **预期证据**: grep 输出
- **完成条件**: 3 条 acceptance 通过

### T7. CHANGELOG `[Unreleased]` v0.6.0 段

- **目标**: 在 `CHANGELOG.md` `[Unreleased]` 段加 v0.6.0 Added / Changed / Decided / Notes 子段
- **Acceptance**:
  - **(T7.a)** `[Unreleased]` 段含 4 个子段（Added / Changed / Decided / Notes）
  - **(T7.b)** Added 段列：`agents/hf-orchestrator.md` + `agents/references/` + `CLAUDE.md` + `AGENTS.md` + ADR-007
  - **(T7.c)** Changed 段列：`.cursor/rules/harness-flow.mdc` body / 旧 skill 转 deprecated alias / README / setup docs / `.claude-plugin/plugin.json` version
  - **(T7.d)** Decided 段引用 ADR-007 D1-D7
  - **(T7.e)** Notes 段说明：兼容期、本轮不动 leaf skill、6 步落地路径只走 Step 1
- **依赖**: T1-T6 全部 GREEN（CHANGELOG 反映已完成的工作）
- **Ready When**: T1-T6 全部 GREEN
- **初始队列状态**: blocked-by-many
- **Selection Priority**: P1
- **Files / 触碰工件**: `CHANGELOG.md`
- **测试设计种子**:
  - fail-first: `grep -A20 "## \[Unreleased\]" CHANGELOG.md` 修改前不含 v0.6.0 / agents/hf-orchestrator
- **Verify**: grep + 章节结构核对
- **预期证据**: CHANGELOG diff
- **完成条件**: 5 条 acceptance 通过

### T8. 项目元数据版本号同步

- **目标**: `SECURITY.md` Supported Versions / `CONTRIBUTING.md` 引言（`.cursor/rules/harness-flow.mdc` Hard rules 段已在 T2.a 同 commit 处理）的版本号 v0.5.1 → v0.6.0
- **Acceptance**:
  - **(T8.a)** SECURITY.md 中 v0.5.x 行 latest 改为 v0.6.0；或新增 v0.6.x 行
  - **(T8.b)** CONTRIBUTING.md 引言版本号 v0.5.1 → v0.6.0
- **依赖**: T1-T7
- **Ready When**: 大部分实现已完成
- **初始队列状态**: ready-after-T7
- **Selection Priority**: P2
- **Files / 触碰工件**: `SECURITY.md` / `CONTRIBUTING.md`
- **测试设计种子**:
  - 主要行为: 两个文件均含新版本号 v0.6.0
  - 关键边界: 不破坏 SECURITY.md 整体表格结构 / CONTRIBUTING.md 其它内容
  - fail-first：`grep -c "v0\.6\.0" SECURITY.md CONTRIBUTING.md` 修改前 = 0；修改后 ≥ 2
  - SUT Form: `naive`
- **Verify**: `grep -c "v0\.6\.0" SECURITY.md CONTRIBUTING.md` ≥ 2 + `grep -c "v0\.5\.1" CONTRIBUTING.md` 修改后 = 0（避免遗漏旧版本号引用）
- **预期证据**: grep 输出 + 两文件 diff
- **完成条件**: 2 条 acceptance 通过

### T9. Collation：进入 review/gate chain 前的状态收口

- **任务类型**: **collation task**（不产出新文件；只校验完整性 + 同步状态字段；为 hf-test-review chain 提供干净起点）
- **目标**: 收口 hf-tasks 阶段，准备进入 hf-test-review chain
- **Acceptance**:
  - **(T9.a)** 所有任务 T1-T8 acceptance 通过（grep 各任务对应 verification/evidence 文件齐全）
  - **(T9.b)** progress.md `Current Stage` 已更新为 `hf-test-review`；`Pending Reviews And Gates` 列出后续序列
  - **(T9.c)** README.md `Status Snapshot` 同步；Reviews & Approvals 表 design-review / design-approval 行已写入 verdict
  - **(T9.d)** 新分支 `cursor/orchestrator-extraction-impl-e404` 已创建（基于 design 分支 HEAD）；T1-T8 commit 已落到该分支
- **依赖**: T1-T8
- **Ready When**: T1-T8 全部 GREEN
- **初始队列状态**: blocked-by-many
- **Selection Priority**: P0（release-blocking gate 的前置入口）
- **Files / 触碰工件**: `progress.md` / `README.md`（仅状态字段同步；不产出新文件）
- **测试设计种子**:
  - 主要行为: 状态字段同步无遗漏；目录树完整
  - 关键边界: 各 verification 文件不为空（每个文件 `wc -l` ≥ 5）；reviews 目录至少含 design-review-2026-05-10.md / spec-review-2026-05-10.md / discovery-review（位于 docs/reviews/）
  - fail-first：进入 T9 前 progress.md `Current Stage` ≠ `hf-test-review`；T9 完成后 = `hf-test-review`
  - SUT Form: `naive`（纯文档状态字段更新；无代码）
- **Verify**:
  - `grep "Current Stage: hf-test-review" features/001-orchestrator-extraction/progress.md` 返回非空
  - `ls features/001-orchestrator-extraction/{reviews,approvals,verification,scripts}/` 各目录非空
  - `wc -l features/001-orchestrator-extraction/verification/*.md` 各文件 ≥ 5 行
- **预期证据**: 上述 grep / ls / wc 命令输出 + `git log --oneline cursor/orchestrator-extraction-impl-e404` 显示 T1-T8 commit 序列
- **完成条件**: 4 条 acceptance 通过；后续可立即派发 hf-test-review subagent

## 6. 依赖与关键路径

```
T1 ─┬─→ T2.a ┐
    ├─→ T2.b ┼─→ T2.d ┐
    ├─→ T2.c ┘        │
    ├─→ T3            ├─→ T5 ┐
T4 ─────────────────────────┘  │
                                ├─→ T7 → T8 → T9
T6.a ←─ T1 ────────────────────┤
T6.b ←─ T1 ────────────────────┘
```

**关键路径**: T1 → T2.{a,b,c}（并行）→ T2.d → T5 → T7 → T8 → T9

**最长串行链**: 7 步（T1 → T2.a → T2.d → T5 → T7 → T8 → T9）

## 7. 完成定义与验证策略

每任务的完成都需：

1. acceptance 全部 GREEN（fresh evidence）
2. 触碰文件已 git add + commit
3. 测试设计种子覆盖的 RED→GREEN→REFACTOR 循环已记录到交接块

总验证策略：跑 walking-skeleton 回归（T5）+ Cursor identity check（T2.d Cursor 段）。其余宿主 manual verify 推迟到 v0.6.0 release pre-flight。

## 8. 当前活跃任务选择规则

### Selection Priority 语义定义

- **P0**: 直接关联 release-blocking 假设（HYP-002 / HYP-003）OR 是 release-blocking task 的硬前置依赖。任一 P0 任务 GREEN 失败 → v0.6.0 不发布
- **P1**: 必须进入 v0.6.0 范围但不直接关联 release-blocking 假设；任一 P1 任务 GREEN 失败 → 可选择降级到 errata 但不阻塞 release（spec § 3 加分项的工程目标）
- **P2**: 锦上添花；可推迟到 v0.6.x patch；本轮发布不要求

按以下顺序决定当前活跃任务：

1. P0 + ready 优先于 P1 + ready 优先于 P2 + ready
2. 同 priority 时按依赖图拓扑序选最早可启动
3. 多任务可并行调度时按"最长路径优先"启动（缩短 critical path）

### 推荐启动顺序

```
Tier 0 (并行起点，无依赖):
  T1 (P0)  +  T4 (P0; T5 的硬前置；从 P1 提升到 P0)

Tier 1 (T1 GREEN 后并行):
  T2.a (P0)  +  T2.b (P0)  +  T2.c (P0)  +  T3 (P0)
  T6.a (P1)  +  T6.b (P1)

Tier 2 (T2.{a,b,c} GREEN 后):
  T2.d (P0)

Tier 3 (T1 + T2.{a-d} + T3 + T4 GREEN 后):
  T5 (P0)

Tier 4 (T5 GREEN 后):
  T7 (P1)

Tier 5 (T7 GREEN 后):
  T8 (P2)

Tier 6 (T8 GREEN 后):
  T9 (P0; collation task，gating)
```

**关于 T4 升 P0 的理由**：T4（regression-diff.py）虽然不直接关联 release-blocking 假设，但它是 T5（release-blocking 验证 task）的硬前置——T4 失败 → T5 无法跑 → HYP-002 验证 evidence 无法落盘 → release 被 hf-completion-gate 阻塞。按上面 P0 定义"是 release-blocking task 的硬前置依赖"自动晋升 P0。

**关于 T6.{a,b} P1 的理由**：README / setup docs 同步是 v0.6.0 范围内的 deliverable（spec FR-006 Should），但即使在 release pre-flight 阶段才补齐也不阻塞 hf-completion-gate；可以与 T5 并行调度提速。

## 9. 任务队列投影视图

简化任务清单（按推荐启动顺序）：

| # | Task ID | 标题 | Priority | Status |
|---|---|---|---|---|
| 1 | T1 | orchestrator main + references 迁移 | P0 | ready |
| 2 | T4 | regression-diff.py + 自测 | P0（T5 硬前置） | ready |
| 3 | T2.a | Cursor stub | P0 | blocked-by-T1 |
| 4 | T2.b | Claude Code stub + plugin | P0 | blocked-by-T1 |
| 5 | T2.c | OpenCode stub | P0 | blocked-by-T1 |
| 6 | T3 | deprecated alias × 11 | P0 | blocked-by-T1 |
| 7 | T2.d | identity gate verification | P0 | blocked-by-T2.{a,b,c} |
| 8 | T6.a | README ×2 sync | P1 | blocked-by-T1 |
| 9 | T6.b | Setup docs ×3 sync | P1 | blocked-by-T1 |
| 10 | T5 | walking-skeleton + NFR-001 测量 | P0 | blocked-by-T1/T2.{a,b,c,d}/T3/T4 |
| 11 | T7 | CHANGELOG | P1 | blocked-by-T1-T6 |
| 12 | T8 | 项目元数据版本号 | P2 | blocked-by-T7 |
| 13 | T9 | 进入 review chain 收口 | P0 | blocked-by-T1-T8 |

## 10. 风险与顺序说明

- **R1**: cloud agent 上下文限制——T2.b plugin schema 注册 / T2.d Claude Code + OpenCode identity check 在 cloud 中可能无法完整验证；预案：标 "deferred manual verification" 落盘到 verification/，由开发者本地或 release pre-flight 阶段补齐；不影响 v0.6.0 release-blocking gate 通过（HYP-003 接受 1/3 宿主完整 + 2/3 deferred 状态，前提是 deferred 状态显式记录）
- **R2**: walking-skeleton baseline checkout 跨 v0.5.1 vs v0.6.0 的 git 操作 → T5 需在 worktree 或临时 checkout 中跑；预案：使用 `git worktree add` 临时挂载 v0.5.1 commit，跑完后清理
- **R3**: NFR-001 wall-clock 测量在 cloud agent 自动化环境下可能噪声大 → 预案：5 次重复取均值；记录 raw 数据；如发现 ratio 跨次差异显著，扩到 10 次

## 11. ReviewHandoff

- 派发 `hf-tasks-review` 独立 reviewer subagent
- reviewer 应特别关注：T2.{a,b,c,d} 是否正确按 design D-FR2-Tasks 拆解；T5 是否正确锚定 release-blocking 假设；T9 收口完整性

---

## 状态同步

- 状态：草稿
- Current Stage：`hf-tasks`
- Next Action Or Recommended Skill：`hf-tasks-review`

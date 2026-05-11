# Tasks Review — 001-install-scripts (2026-05-11)

- Reviewer: 独立 reviewer subagent（cursor cloud agent 派发）
- Author of tasks under review: cursor cloud agent（hf-tasks 节点）
- Author / reviewer separation: ✅（不同会话）
- Tasks under review: `features/001-install-scripts/tasks.md`
- Approved spec basis: `features/001-install-scripts/spec.md`（approved 2026-05-11，spec-review Round 2 通过）
- Approved design basis: `features/001-install-scripts/design.md`（approved 2026-05-11，design-review Round 2 通过）
- 关联 ADR: `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md`（accepted）
- Profile / Mode: `full` / `auto`
- Rubric: `skills/hf-tasks-review/references/review-checklist.md`
- Template: `skills/hf-tasks-review/references/review-record-template.md`

## 结论

需修改

理由摘要：tasks.md 在结构、追溯、依赖图、关键路径、Walking Skeleton、active task 选择规则、queue projection、INVEST 6 维上整体达标；10 个 task 一对一映射到 design §16 的 12 个 e2e scenario，spec FR/NFR/ASM 在 §4 trace 表里均有承接。但存在 **1 条 important finding**（T2–T9 verify 行均引用 `tests/test_install_scripts.sh --only=N`，而该 driver 仅在 T10 落地，会在 hf-test-driven-dev 进入 T2 时立刻撞 "no such file"），加 **3 条 minor finding**（FR-007 verbose 行数验证未落到任何 task；FR-005 "uninstall.sh 也支持 --dry-run" acceptance 未被任一 task seed 覆盖；T10 单 task 同时承担 grep audit + e2e driver 实现 + 5 文件 doc sync 三类显著不同的工作），属于"定向回修可关闭"的内容缺口，不是计划结构性失败。

## Precheck

| 检查项 | 结果 | 说明 |
|---|---|---|
| 存在稳定 tasks draft | ✅ | `tasks.md` 10 章节齐全，状态字段=草稿 |
| 已批准上游证据可回读 | ✅ | spec-review-2026-05-11 verdict=通过；design-review-2026-05-11 verdict=通过；ADR-007=accepted |
| route / stage / 证据一致 | ✅ | progress.md Current Stage=`hf-tasks`（不影响审查） |
| trace 锚点可 dereference | ✅ | §4 trace 表 10 行所有 spec/design 锚点都能解析 |

→ Precheck 通过，进入正式 rubric。

## 维度评分

| ID | 维度 | 分数 (0-10) | 备注 |
|---|---|---|---|
| `TR1` | 可执行性 | 8 | 10 个 task 均小到能在单任务闭环内推进；T1 是冷启动入口（无依赖、ready 状态唯一）；T6 / T7 / T10 单 task 内职责略多但仍可冷读出"完成时什么必须为真"。T10 是最大颗粒（grep audit + 实现 e2e driver + 5 doc 文件同步）——属于 minor finding 4 |
| `TR2` | 任务合同完整性 | 9 | 10 个 task 全部具备 Goal / Acceptance / Dependencies / Ready When / Selection Priority / Files / 测试设计种子 / Verify / 完成条件；DoD 由 §7 一句话锁定（DoD = Acceptance + 对应 scenario PASS）；T1 与 T10 还显式列了"预期证据"段 |
| `TR3` | 验证与测试设计种子 | 7 | 每个 task 的"测试设计种子"均含主行为 + 关键边界；多数（T1/T2/T4/T6/T8/T9/T10）显式给出 fail-first 点；T3 / T5 缺 fail-first 点（T5 隐式指向 T8 rollback，T3 完全不写）——非阻塞，归 coverage 段说明 |
| `TR4` | 依赖与顺序正确性 | 6 | §6 mermaid 依赖图 + 关键路径 + T9 与 T7/T8 并行可执行说明完整、无环；§9 queue projection 表 priority + dependencies + 状态字段齐全；但 T2–T9 的 Verify 行均写 `bash tests/test_install_scripts.sh --only=N`，driver 仅 T10 实现——TDD agent 进入 T2 时会立刻撞 "no such file"，是 important finding 1 |
| `TR5` | 追溯覆盖 | 7 | §4 trace 表覆盖 T1–T10 → spec FR-001/002/003/004/006/008、NFR-001（部分）/002/004 + ASM-001；design §11/§13/§16/§18 锚点逐 task 列出；spec §16 e2e scenario #1–#12 在各 task Acceptance + Verify 中均有显式承接（#1→T2 #2→T4 #3→T3 #4→T4 #5→T5 #6→T5 #7→T7 #8→T1 #9→T7 #10→T10 #11→T9 #12→T8，12/12 覆盖完整）；但 FR-007 `--verbose` 的 acceptance（"verbose 行数 > 24，默认 < 10"）未被任何 task 的 acceptance 或 test seed 显式覆盖（minor finding 2），FR-005 中"uninstall.sh 在 --dry-run 下也只打印不删除"未被 T7/T1 任何 acceptance 覆盖（minor finding 3）|
| `TR6` | Router 重选就绪度 | 9 | §8 active task 选择规则三条（依赖满足 + Selection Priority 数字最小 + acceptance fail 回 hf-test-driven-dev）唯一可冷读；首个 Active Task=T1 显式标注；§9 queue 表稳定可回读；任务量 < 阈值，Task Board Path = N/A 显式声明（不是默写） |

按 review-checklist.md 评分辅助规则：所有 6 维 ≥ 6/10，TR4 = 6 必须对应具体 finding（important finding 1 已落）；TR3 / TR5 = 7 已对应若干 minor finding。

## 发现项

### Important

- [important][LLM-FIXABLE][TR4][TA3] **T2–T9 的 Verify 行引用 `tests/test_install_scripts.sh --only=N`，但该 driver 仅在 T10 落地**。
  - **Anchor**:
    - `tasks.md` T2 Verify（line 101）：`bash tests/test_install_scripts.sh --only=1`
    - 同样模式存在于 T3（line 117）/ T4（line 135）/ T5（line 152）/ T6（line 171）/ T7（line 190）/ T8（line 208）/ T9（line 225）
    - T10 Acceptance（line 233）：`tests/test_install_scripts.sh` 在本任务才被实现
    - T1 Verify（line 83）已经显式带括号注释 "（在 T10 落地，本任务先用 ad-hoc 命令）"，说明作者知道这个时序问题，但只在 T1 单点处置，没扩散到 T2–T9
  - **What**: TDD agent 在完成 T1 进入 T2 时，按 Verify 行执行 `bash tests/test_install_scripts.sh --only=1` 会立即报 `No such file or directory`；hf-test-driven-dev 在没有"先用 ad-hoc 命令"明确 fallback 的情况下，会在每个 task 上都重走一次"找不到 driver → 回查依赖 → 回查 T10 → 决定写 ad-hoc 还是 stub"的额外 loop，污染 6 次 task 的进入态。
  - **Why**: TR4（依赖/顺序正确性）的 hard rule 是"依赖关系正确 + 关键路径合理"——文档级"verify command 形式上指向尚未存在的 artifact" 是 dependency 漏边的轻量等价物；TA3（缺 Verify）的扩展解读：Verify 行如果指向不可执行的命令，等价于实际无 Verify。
  - **Suggested fix**（任选其一，作者择其轻）：
    - **A1**（轻）：把 T1 已经写的"（在 T10 落地，本任务先用 ad-hoc 命令）"caveat 复制到 T2–T9 的 Verify 行，或在 §7 顶部加一条说明 "T1–T9 期间 verify 用 ad-hoc 命令（design §16.2 矩阵字段直接转写），T10 落地后统一切到 driver"
    - **A2**（中）：把 T10 的 driver 实现部分前置——例如新增 T1.5 或修改 T1 包含 "tests/test_install_scripts.sh 最小骨架（支持 --only flag + scenario #8 一项）"，使 T2 起的 Verify 行天然可执行；这会让 T1 略大但消除整段时序错配
    - **A3**（重）：把 T10 拆成 T10a（driver 落地）+ T10b（grep audit + doc sync）；T10a 提前到 T2 之前
  - 推荐 A1（最小改动，不牵动 §6 依赖图）。

### Minor

- [minor][LLM-FIXABLE][TR5][TA6] **FR-007 `--verbose` 的 acceptance 未被任何 task seed 显式覆盖**。
  - **Anchor**: `spec.md` FR-007（line 156–161）"verbose 行数 > 24（每个 hf-* skill 顶层目录一行）；不带 verbose 行数 < 10"；`design.md` §11 `op()` 抽象（line 264–284）实现了 verbose 行为；`tasks.md` §4 trace 表（line 53–64）不含 FR-007 一行；T1–T10 任一 task 的 Acceptance / 测试设计种子均未提到 verbose 行数验证。
  - **What**: T1 实现 `op() / log() / err()` 时虽然天然附带 verbose 行为，但没有 task acceptance 锁定它；hf-test-driven-dev 不会写出 verbose 行数测试；hf-completion-gate 时该 acceptance 会"无声跳过"。
  - **Why**: TR5（追溯覆盖）的 hard rule 是"已批准规格的关键 FR 都必须有 task 承接"。FR-007 优先级 = Should 不是 Must，但仍是已批准 spec 的内容，不能默写省略。
  - **Suggested fix**：T1 测试设计种子里增补一条"关键边界：verbose 行数 > 24 / 默认 < 10"，并在 §4 trace 表新增 `T1 | FR-007 | §11 op() VERBOSE 分支` 一行；或把 FR-007 显式列入 spec-deferred.md 注明本轮不验证（不推荐——spec 已 approved 含此 FR）。

- [minor][LLM-FIXABLE][TR5][TA6] **FR-005 "uninstall.sh 在 `--dry-run` 下也只打印不删除"未被任一 task 覆盖**。
  - **Anchor**: `spec.md` FR-005（line 138–144）"install.sh 与 uninstall.sh 在 --dry-run 下必须打印将要执行的所有 mkdir / cp / ln / rm 操作，但不真实写入或删除任何文件"；`tasks.md` T1（line 70–86）只覆盖 install.sh 的 dry-run；T7（line 174–191）uninstall.sh acceptance 三条（user-skill 保留 / 缺 force / 带 force）均不涉及 uninstall --dry-run；design §13 CLI 契约（line 454）`uninstall.sh [--host <path>] [--dry-run]` 显式列了 flag。
  - **What**: 实现时 uninstall.sh 可能漏掉 dry-run 分支，或漏掉一行验证。
  - **Why**: 同 finding 2 ——已批准 spec 的 Must 级 FR 必须 task 落地。FR-005 优先级 = Must。
  - **Suggested fix**：在 T7 测试设计种子里增补一条"关键边界：uninstall --dry-run 下宿主仓库 `find` 与执行前一致"；或新增一个 e2e scenario 编号（已超出 design §16 12 scenario 范围，所以更轻的做法是 T7 acceptance 增第 4 条）。

- [minor][LLM-FIXABLE][TR1][TA1] **T10 单 task 内同时承担 3 类显著不同的工作**。
  - **Anchor**: `tasks.md` T10（line 228–246）：(a) NFR-004 grep audit 命令、(b) `tests/test_install_scripts.sh` 12 个 scenario 统一 driver 实现、(c) 5 文件 doc sync（cursor-setup.md / opencode-setup.md / README.md / README.zh-CN.md / CHANGELOG.md）。
  - **What**: 三类工作的失败模式与 fail-first 点完全不同：grep audit 是单行命令、driver 实现是 ~12 scenario 测试代码（最重的部分）、doc sync 涉及 5 个不同文件的不同段落。任一子项失败都会让整个 T10 卡住。
  - **Why**: TR1（可执行性）的 INVEST-Small 维度倾向于"一个 task 一个完成判定"。TA1 反模式：大任务打包多条行为。
  - **Suggested fix**（与 important finding 1 fix A3 联动）：把 T10 拆成 T10a（driver 落地，可前置到 T2 之前）+ T10b（grep audit + 5 文件 doc sync）；如果决定保留 T10 单 task，至少在 §6 顺序说明里点名"T10 内部子序：先建 driver → 跑 grep → 改 doc → 重跑 driver 验证"。

## 缺失或薄弱项（非阻塞、归 coverage 段）

- T3 / T5 测试设计种子缺 fail-first 点（T3 完全不写，T5 隐式指向 T8 rollback）。可补一行，例如 T3 fail-first = "宿主已有 `.cursor/rules/` 中存在同名 `harness-flow.mdc` 时不应被静默覆盖（与 design §11 `mark_will_create` pre-existing 检测对齐）"。
- T6 fail-first 点 "故意省略 `manifest_version` → JSON parse 仍可读" 实际上是"向前兼容空间"测试，不是 fail-first 实现锚点；建议改为 "manifest 写入到一半进程被 SIGKILL → manifest 不存在（要么完整要么不存在，与 NFR-002 invariant 一致）" 这种更贴 fail-first 语义的种子。
- T7 fail-first 点 "缺 manifest → uninstall exit 1" 是 acceptance 第二条的复述，不是新的 fail-first 维度；建议改为 "manifest entries[] 中含一条 host-relative path 指向宿主仓库**外**（恶意 manifest）→ uninstall 拒绝执行 + 报错"。
- §2 里程碑表 M5 包含 "T10（部分）"——milestone-task 颗粒一半重叠是无害的，但 router 在 milestone 维度做查询时可能困惑；建议要么把 doc sync 单拆成 T11，要么 M5 退化掉只留 M1–M4。
- §10 风险 1 "macOS / alpine 的 partial cp 失败模拟" 已经在 mitigation 里把"父目录只读"作为统一触发点，与 design §17 失败模式表自洽，无需新增 finding。

## 下一步

- `hf-tasks`（needs_human_confirmation=false；reroute_via_router=false）

## 记录位置

- `features/001-install-scripts/reviews/tasks-review-2026-05-11.md`

## 交接说明

- `hf-tasks` 节点接收本 review，按 important finding 1 + 3 条 minor finding 做定向回修；预计回修后 6 维评分 TR4 ≥ 8、TR1 ≥ 9、TR5 ≥ 9，可直接进入下一轮 tasks-review（应能 1 轮通过 → 任务真人确认 approval step）
- 缺失/薄弱项段落给作者参考，不强制回修
- 重审范围只看回修点；其余维度本轮已通过

---

## Round 2（2026-05-11）

- Reviewer: 同 Round 1 独立 reviewer subagent
- 重审范围: Round 1 1 important + 3 minor finding 的定向回修
- 评审依据: `features/001-install-scripts/tasks.md` 修订版 + 不变的 spec/design/ADR-007 上游证据

### 逐 finding 回修验证

| Round 1 Finding | 回修锚点 | 验证结果 |
|---|---|---|
| **[important][TR4]** T2–T9 verify 引用尚未存在的 driver | T2 line 103、T3 line 119、T4 line 137、T5 line 154、T6 line 173、T7 line 193、T8 line 211、T9 line 228 均加上"（driver 未落地前 ad-hoc 验证…）"caveat；T6 / T8 / T9 / T2 还附 ad-hoc 命令样例（`mktemp -d` + find / cat manifest + grep / 父目录设只读 / cp HF 仓库到 tmp + rm -rf .git） | ✅ **已闭合**。Round 1 推荐的 fix A1 + 部分 A3（见 finding 4）均落地。hf-test-driven-dev 进入 T2–T9 时不会再撞 "no such file" |
| **[minor][TR5]** FR-007 `--verbose` 行数 acceptance 未承接 | T1 测试设计种子新增"关键边界 2"显式验证 verbose > 24 / 默认 < 10；T1 完成条件新增"`--verbose` / 默认两态行数边界验证通过"；§4 trace 表 T1 行追加 `FR-007` | ✅ **已闭合**。FR-007 现在有显式 task acceptance 锚点。**轻量观察**：T1 的 install acceptance 只跑 `--dry-run`，但 design §11 的 `op()` 实现里 `DRY_RUN=1 OR VERBOSE=1` 都会触发逐行打印，所以"--verbose 行数 > 24" 的纯净对比需要 non-dry-run 模式；T1 skeleton 在 vendor_skills_opencode 未实现前 non-dry-run install 只会输出 1–2 行（仅 mkdir）。**不阻塞**：hf-test-driven-dev 在 T1 实现 plan_entries() 时若把"枚举所有 skills"包含进去，dry-run 下行数即可 > 24，与"verbose 是否开"对照可在 T2 完成后回测；写一行注释/说明即可，不影响通过 verdict |
| **[minor][TR5]** FR-005 `uninstall.sh --dry-run` acceptance 未承接 | T7 acceptance 第 4 条新增 "When `bash uninstall.sh --host /tmp/host --dry-run`，Then 退出码 0；标准输出含每条 entry 的 `[RM]` / `[RMDIR]` 计划行；宿主仓库**实际不动**（manifest / readme / vendor 文件全部仍在）—— FR-005 uninstall 分支验证"；§4 trace T7 行追加 `FR-005（uninstall 分支）` | ✅ **已闭合**。FR-005 install + uninstall 双分支均有 task 锚点 |
| **[minor][TR1]** T10 单 task 内打包 3 类工作 | T10 拆为 T10a（e2e driver + grep audit，priority 10）+ T10b（5 文件 doc sync，priority 11）；§2 milestones M4 / M5 重排；§4 trace 拆出 T10a / T10b 两行；§6 mermaid 依赖图新增 `T10a → T10b` 边；§9 queue projection 加 T10b 行 | ✅ **已闭合**。T10a / T10b 各自单职责；T10a 的 acceptance 三条（driver + grep + 12/12 PASS）聚合明确；T10b 五文件 doc sync 单一职责清晰 |

### 新增/残留观察（**不**阻塞通过）

- **[minor][TR2 文本一致性]** §1 line 12 仍写 "T1–T10 拆分"、§7 line 295 仍写 "T10 完成时"、§10 风险 3 仍写 "T10 docs 同步"、T1 Verify line 85 / T2 Verify line 103 caveat 内文写 "T10 落地" 与 "在 T10 才落地"——共 5 处残留旧引用未升级到 T10a / T10b。**不影响 router 重选或任何 acceptance 判定**（§9 queue projection 表与 §6 mermaid 是 router 的权威源，已正确升级）；纯属 Round 1 finding 4 拆分后的文本扫尾，归"作者参考的非阻塞细节"。建议在下一次 progress.md 同步前顺手扫一遍 `rg '\bT10\b' features/001-install-scripts/tasks.md` 把以上 5 处升级为 T10a / T10b（视上下文取其一）。
- **[轻量观察][TR3]** T1 关键边界 2 verbose 行数与 dry-run 模式存在的轻度互斥已在上面 finding 2 行内说明，hf-test-driven-dev 自然能解；不是新 finding。

### Round 2 维度评分增量

| ID | Round 1 | Round 2 | 增量原因 |
|---|---|---|---|
| TR1 | 8 | 9 | T10 拆分消除"单 task 三职责"问题 |
| TR2 | 9 | 9 | 不变（5 处文本残留属轻量、非合同字段） |
| TR3 | 7 | 8 | T1 verbose 行数边界 + T7 uninstall dry-run acceptance 补强 |
| TR4 | 6 | 9 | T2–T9 verify caveat 全量补齐，依赖图加 T10a→T10b 边 |
| TR5 | 7 | 9 | FR-007 / FR-005（uninstall 分支）trace + acceptance 双补齐 |
| TR6 | 9 | 9 | §9 queue projection 已扩到 T10b，selection rule 仍唯一 |

无维度低于 8/10，亦无新 important / critical finding。

### 结论（Round 2）

**通过**

理由：Round 1 全部 4 条 finding（1 important + 3 minor）在 tasks 层均已定向闭合；6 维评分全部 ≥ 8/10；未引入新 important 或 critical finding；§9 queue projection 与 §6 mermaid 这两个 router 重选的权威源已正确升级到 T10a / T10b 二阶段；§8 active task 选择规则唯一（首个 = T1，priority + 依赖完结二级排序）；12/12 e2e scenario × 全部 Must 级 FR/NFR/ASM 已被 task acceptance 覆盖；Walking Skeleton（M1 = T1+T2，scenario #1 + #8）路径稳定。tasks 计划具备进入"任务真人确认"approval step 的质量。

5 处 "T10" 残留文本是非阻塞的扫尾事项，不影响 hf-workflow-router、hf-test-driven-dev、hf-completion-gate 任何下游决策；建议作者在下一次 progress.md / README.md live update 时顺带刷新。

### 下一步

- `任务真人确认`（needs_human_confirmation=true；reroute_via_router=false）

### 交接说明（Round 2）

- 通过 verdict 触发 approval step；interactive mode 等待真人确认，auto mode 写 approval record（`features/001-install-scripts/approvals/`）
- 真人确认通过后 hf-workflow-router 会切换到 hf-test-driven-dev 节点，从 T1 开始
- 5 处 T10 残留文本已记录在"新增/残留观察"段，作者按需顺手清理

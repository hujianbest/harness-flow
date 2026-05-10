# Tasks Review: HF Orchestrator Extraction & Skill Decoupling

- 评审对象:
  - Tasks: `features/001-orchestrator-extraction/tasks.md`
- 上游证据:
  - 已批准 Spec: `features/001-orchestrator-extraction/spec.md`（spec-review Round 2 verdict = `通过`，approval record 已落盘）
  - 已批准 Design: `features/001-orchestrator-extraction/design.md`（design-review verdict = `通过`，approval step 由父会话承担）
  - 上游 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
  - Spec-review handoff (R2): `features/001-orchestrator-extraction/reviews/spec-review-2026-05-10.md` § "下一步" Round 2 末尾 4 项
  - Design-review handoff: `features/001-orchestrator-extraction/reviews/design-review-2026-05-10.md`
  - 任务计划模板: `skills/hf-tasks/references/task-plan-template.md`
- 评审 skill: `hf-tasks-review`
- 评审者: 独立 reviewer subagent（与 author 分离，符合 Fagan）
- 评审时间: 2026-05-10
- 评审方法: 6 维 rubric (`TR1`–`TR6`) + 反模式扫描 (`TA1`–`TA7`) + 父会话 7 项特殊关注核验 + 与 spec / design / ADR-007 一致性核验

## Precheck

| 检查项 | 结果 |
|---|---|
| 任务计划草稿存在且可定位 | ✓ `features/001-orchestrator-extraction/tasks.md` 11 章节 + 状态同步段 |
| 上游 spec 可回读且已批准 | ✓ spec-review R2 通过；approval record 已落盘（`approvals/spec-approval-2026-05-10.md`） |
| 上游 design 可回读且已批准 | ✓ design-review 通过；approval step 由父会话承担（progress.md 显示已进入 hf-tasks 阶段） |
| Author / Reviewer 分离 | ✓ 父会话起草 tasks.md，本 reviewer subagent 独立 |
| Stage / route / evidence 一致 | △ progress.md `Current Stage: hf-tasks-review` ✓；但 progress.md `Next Action` 仍写 `hf-design`、Session Log 也未记录 design / design-review / tasks 起草——见薄弱项 1（progress.md sync gap，不阻塞本评审） |
| 章节骨架与 `task-plan-template.md` 一致 | ✓ § 1–§ 11 顺序与默认结构一致；§ 5 任务拆解中关键任务字段（目标 / Acceptance / 依赖 / Ready When / 初始队列状态 / Selection Priority / Files / 测试设计种子 / Verify / 预期证据 / 完成条件）大体齐全——见 Finding 1（T8 / T9 字段残缺） |

Precheck 通过（progress.md sync gap 列入薄弱项，不阻塞 tasks-review 进入正式 rubric）。

## 父会话 7 项特殊关注核验

| # | 关注项 | 核验 | 结果 |
|---|---|---|---|
| 1 | D-FR2-Tasks 拆解：T2 = 4 sub-tasks (a/b/c/d) per host；T6 = 2 sub-tasks (a/b) | T2.a (Cursor stub) / T2.b (Claude Code stub + plugin manifest) / T2.c (OpenCode stub) / T2.d (3 宿主 identity gate verification) = 4 sub；T6.a (README ×2) / T6.b (Setup docs ×3) = 2 sub。与 design D-FR2-Tasks "每宿主独立 + identity gate 独立" / "README ×2 vs setup docs ×3" 完全一致 | ✓ |
| 2 | HYP-002 + HYP-003 release-blocking validation 是否在 T5 | T5 acceptance 5 条覆盖：T5.a regression-diff PASS（HYP-002 等价语义）/ T5.b regression record 落盘 / T5.c NFR-001 wall-clock × 1.20 量化（HYP-003 always-on 加载延迟）/ T5.d ratio > 1.20 立即停 task 回 hf-design / T5.e NFR-004 reviewer/author 分离纪律检查；§ 4 trace 表 T5 标 "**是**（HYP-002 + HYP-003 双 release-blocking）"；§ 2 M3 退出标准也明确包含此项 | ✓（但 HYP-003 identity 部分由 T2.d 承担，T5 与 T2.d 在 smoke-3-clients.md 文件上有所有权重叠——见 Finding 4） |
| 3 | 依赖图无循环 + 关键路径 = 7 步 | § 6 依赖图：T1 → {T2.a/b/c, T3, T6.a/b}；T2.{a,b,c} → T2.d；T2.d + T3 + T4 → T5；{T5, T6.a/b} → T7；T7 → T8 → T9。无环（拓扑序列存在：T1, T4 || T2.{a,b,c}, T6.{a,b}, T3 → T2.d → T5 → T7 → T8 → T9）。关键路径声明 "T1 → T2.{a,b,c}（并行）→ T2.d → T5 → T7 → T8 → T9"，最长串行链 = 7 步（T1 → T2.a → T2.d → T5 → T7 → T8 → T9）。逐节点核：T1(1) → T2.a(2) → T2.d(3) → T5(4) → T7(5) → T8(6) → T9(7) = 7 ✓ | ✓ |
| 4 | 每任务 fail-first 测试种子（RED→GREEN traceable） | T1 / T2.a / T2.b / T2.c / T3 / T4 / T6.a / T6.b / T7 共 9 个任务有显式 fail-first（多为 grep / wc / test -f 类断言）；**T2.d / T5 fail-first 隐式**（验证记录 / 实测，未显式标 RED）；**T8 / T9 完全缺 "测试设计种子" 段**——见 Finding 1（important）和 Finding 5（minor） | △ 部分达标 |
| 5 | INVEST 验证（特别是 Independent / Small / Testable） | I (Independent): 依赖图清晰，每任务依赖前置已显式声明；T1 与 T4 真正独立（M1/M2 双起点）；T6.a/b 与 T2.{a,b,c}/T3 各自独立。N (Negotiable): 每任务有完成条件，可在 hf-test-driven-dev 阶段调整实现细节。V (Valuable): § 4 trace 表逐任务回指 spec FR / NFR + design D-X。E (Estimable): 每任务有具体文件清单 + acceptance 条数（3-6 条）。**S (Small)**: T1 打包 "建主文件 + 9 references git mv"（design § 18 已许可同 commit）——边界尚 OK；T3 打包 "11 个 stub 文件" 但模板统一可批量；T5 打包 "regression + load-timing + reviewer dispatch spot-check + smoke 补齐" 4 类活动——见 Finding 4（minor，Small 边缘）。**T (Testable)**: T8 / T9 缺测试种子破坏 Testable 字段呈现——见 Finding 1 | △ Small / Testable 边缘 |
| 6 | Cloud-agent context 风险（R1）+ manual-verification 延迟路径 | § 10 R1 显式列出 cloud agent 上下文限制；T2.d acceptance T2.d.4 "至少 1/3 宿主（Cursor）能够实际验证 ... 其它宿主可标 'deferred to manual verification post-merge'"；T5 测试种子注 "可能只能跑 Cursor 宿主测量，其它宿主标 'deferred manual'"；R1 预案明确"不影响 v0.6.0 release-blocking gate 通过（HYP-003 接受 1/3 宿主完整 + 2/3 deferred 状态，前提是 deferred 状态显式记录）" | ✓（但此处的 "1/3 + 2/3 deferred" 接受度是 tasks 阶段新增的操作化语句，spec § 4 / ADR-007 D5 / design 中未显式锁定——见薄弱项 2） |
| 7 | Selection Priority (P0/P1/P2) 与 release-blocking 状态一致 | T1 / T2.{a,b,c,d} / T5 / T9 = P0；T3 = P0（trace 标"否" — 非 release-blocking 但 critical-path）；T4 = P1（**但 T5 release-blocking 强依赖 T4！**）；T6.{a,b} / T7 = P1；T8 = P2。**P0/P1/P2 语义未在 § 8 显式定义**——§ 8 只给排序规则 "P0 + ready 优先于 P1 + ready"。T4 标 P1 但其完成是 T5 (release-blocking) 的硬前置，与"release-blocking 优先级最高"直觉不一致——见 Finding 2（important） | △ 不一致 |

## 6 维 rubric 评审

| 维度 | 评分 | 关键观察 |
|---|---|---|
| **TR1 可执行性** | 8/10 | 关键任务（T1 / T2.{a,b,c,d} / T3 / T4 / T6.{a,b} / T7）均冷启动可执行（明确文件路径 + 命令式 acceptance）；无"实现某模块"式大任务；T5 实测任务依赖前置 GREEN 即可启动；T1 打包 "main + 9 references migration" 略大但有 design § 18 endorsement，可视作单 commit 单元；T3 打包 11 个 stub 文件但模板统一可批量。失分点：T8 / T9 字段残缺导致 hf-test-driven-dev 进入时缺失部分启动指令 |
| **TR2 任务合同完整性** | 7/10 | T1–T7 关键任务 Acceptance / Files / Verify / 完成条件齐全；**T8 完全缺 "测试设计种子" 与 "预期证据" 段**；**T9 完全缺 "测试设计种子" 与 "预期证据" 段**——TA4 anti-pattern 命中。reviewer 可冷读 T8 / T9 完成时必须为真的内容（依靠 Acceptance + Verify），但与其它任务的字段密度对齐性破坏 |
| **TR3 验证与测试设计种子** | 6/10 | T1 / T2.{a,b,c} / T3 / T4 / T6.{a,b} / T7 显式给出 fail-first 命令（grep / wc / test -f）+ GREEN 后期望；**T2.d 无显式 RED**（仅"主要行为：实际 new session 启动 → identity grep PASS"，未声明 file-not-exist 前置）；**T5 无显式 RED**（仅"主要行为：regression PASS + ratio ≤ 1.20"，未声明 baseline 模式 / 注入失败模式作为 RED 依据）；**T8 / T9 完全缺测试种子** |
| **TR4 依赖与顺序正确性** | 7/10 | 依赖图无环；critical path = 7 步与声明一致；并行度（T1 后 T2.{a,b,c} + T6.{a,b} + T3 + T4 全部 ready）合理；M1–M5 milestone 与任务依赖一致。失分点：T4 标 P1 但是 T5（release-blocking）的硬前置——若严格执行 § 8 "P0 + ready 优先于 P1 + ready" 规则下，T4 被 P0 任务永远挤后，T5 也随之延后；这与 T4 在 § 8 推荐启动顺序中位列第 2（"T1 → T4（P1 但与 T1 并行）"）的描述自相矛盾——见 Finding 2 / Finding 3 |
| **TR5 追溯覆盖** | 9/10 | § 4 trace 表逐任务回指 spec FR / NFR / HYP + design D-X；FR-005（ADR-007 锁定）显式标"在 spec PR 起草"——T8 trace "（ADR-005 立场延续；version bump）"略弱（无具体 FR 编号）但合理（FR-007 主要在 T7；T8 是元数据 housekeeping）；无 orphan task。design § 11 14 模块均落到具体任务（含 verification records 三件套） |
| **TR6 Router 重选就绪度** | 7/10 | § 8 当前活跃任务选择规则 + § 9 队列投影视图（13 行表，含 Priority + Status 列）使 router 可冷读；§ 9 状态写为 "ready" / "blocked-by-T1" / "blocked-by-T2.{a,b,c}" / "blocked-by-many" 等具体值；唯一选择规则在 § 8 给出。失分点：(a) "P0 + ready 优先于 P1 + ready" 规则与 § 8 第 3 句"推荐启动顺序：T1 → T4（P1 但与 T1 并行；可单独并行）..."实质冲突——cloud agent 单任务执行下不存在并行；(b) P0/P1/P2 语义未定义；(c) progress.md `Next Action` 仍写 `hf-design`，未同步到 `hf-tasks-review` 之后的下游推荐节点——见薄弱项 1 |

**关键阈值检查**: TR3 = 6/10（边缘）；其余维度 ≥ 7/10。无维度 < 6 → 不命中"不得返回 通过"硬规则；但 TR3 / TR2 / TR4 各对应至少一条具体 finding，且 Finding 1 / Finding 2 属 **important** → 适用"任一维度 < 8 通常对应 finding；任一关键 finding important → 不得 通过"惯例。

## 反模式扫描（`TA1`–`TA7`）

| ID | Anti-Pattern | 命中? | 说明 |
|---|---|---|---|
| `TA1` | 大任务 | ✗ | T1 / T3 / T5 略大但都有 acceptance 条数边界 + design 上游 endorsement；不打包多发布轮次 |
| `TA2` | 缺 Acceptance | ✗ | 所有 13 个任务（T1 / T2.{a,b,c,d} / T3 / T4 / T5 / T6.{a,b} / T7 / T8 / T9）均含 Acceptance 段，每段 2–6 条 |
| `TA3` | 缺 Files / Verify | ✗ | 所有 13 个任务均含 "Files / 触碰工件" + "Verify" 段 |
| **`TA4`** | 无 test seed | **✓ T8 / T9 命中** | T8 / T9 完全缺 "测试设计种子" 段；其它 11 个任务有，但 T2.d / T5 的 fail-first 不显式（弱化命中）——见 Finding 1 + Finding 5 |
| `TA5` | 里程碑冒充任务 | ✗ | § 2 milestone 表与 § 5 任务拆解分层表达；M1–M5 是包含任务的桶，不是任务本身 |
| `TA6` | orphan task | ✗ | § 4 trace 表覆盖 13 个任务，每个有 spec / design 回指 |
| `TA7` | unstable active task | △ 边缘 | § 8 选择规则唯一（"P0 + ready 优先于 P1 + ready"），但与 § 8 推荐启动顺序自相矛盾（T4 P1 ready 与 T1 P0 ready 并行）；strict-rule 下 router 选 T1，T4 等待——表面唯一规则，实质次序不一致——见 Finding 2 / Finding 3 |

## 与 spec / design / ADR-007 一致性核验

| 检查 | 结果 | 说明 |
|---|---|---|
| spec FR-001 → T1 | ✓ | T1 acceptance T1.a/b/c/d/e 覆盖 frontmatter + identity 锚点 + 字符数预算 + 9 references 完整 + 引用指向新路径 |
| spec FR-002.a/b/c/d → T2.a/b/c/d | ✓ | 4 个 sub-task 一一对应，acceptance 覆盖 stub 内容 + 降级路径（T2.b 的 plugin schema fallback）+ 已存在文件追加段而非覆盖（T2.c.3） |
| spec FR-003 → T5 | ✓ | T5.a regression-diff PASS + T5.b record 落盘；与 design D-RegrLoc / D-RegrImpl 一致 |
| spec FR-004 → T3 | ✓ | T3 acceptance 5 条覆盖 frontmatter `deprecated alias` + HTML marker + ≤30 行 + 9 references stub ≤10 行 + 文件不删除 |
| spec FR-005 → "ADR-007 已在 spec PR 起草" | ✓ | § 4 trace 表 FR-005 标"已起草"，本轮无 task；与 design § 19 一致 |
| spec FR-006 → T6.a/b | ✓ | 拆 README ×2 / setup docs ×3 与 D-FR2-Tasks 一致 |
| spec FR-007 → T7 | ✓ | T7 acceptance 5 条覆盖 [Unreleased] 4 子段 + ADR-007 D1-D7 引用 + 兼容期 Notes |
| spec NFR-001 wall-clock × 1.20 → T5.c | ✓ | 5 次重复测量 + raw + ratio + 落盘到 `load-timing-3-clients.md` 与 D-NFR1-Schema 一致 |
| spec NFR-002 字符数 × 1.10 → T1.c | ✓ | acceptance T1.c "wc -c agents/hf-orchestrator.md ≤ 23,245 bytes（baseline 21,132 × 1.10）"——与 design § 13.1 动态契约 + design-review Finding 1（baseline 实测 21,132 bytes）一致；硬编码值合法（已实测） |
| spec NFR-003 旧路径不 404 → T3.e | ✓ | acceptance T3.e "11 个 stub 文件物理存在（不删除），可通过 ls 验证" |
| spec NFR-004 reviewer/author 分离 → T5.e | ✓ | acceptance T5.e "review record 检查 100% 含 '独立 reviewer subagent' 标识" |
| spec NFR-005 容许差异白名单 → T4.e | ✓ | acceptance T4.e 三 test case（自一致性 + mutation + 白名单内差异）覆盖完整 |
| design § 11 14 模块 → 任务覆盖 | ✓ | 14 模块逐一映射到任务（orchestrator main + references → T1；3 host stubs → T2.{a,b,c}；2 deprecated alias 类 → T3；regression script → T4；3 个 verification records → T2.d + T5；2 README + 3 setup docs → T6.{a,b}；CHANGELOG → T7；plugin manifest → T2.b；project metadata → T8） |
| design § 18 关键路径并行度 | ✓ | "main + 3 host stub + alias 可同 commit" 在 § 6 依赖图中 T2.{a,b,c} / T3 / T6.{a,b} 都仅依赖 T1，体现并行度 |
| ADR-007 D5 release-blocking 假设 → T5 | ✓ | T5 标 P0；trace 表 "**是**（HYP-002 + HYP-003 双 release-blocking）"；§ 2 M3 退出标准明确"walking-skeleton 实跑 + regression-diff.py PASS + 3 宿主 smoke + identity gate + load-timing 量化" |
| spec § 6.2 12 项 out-of-scope 是否被任务静默引入 | ✓ | 逐项核（不动 24 leaf / 不删旧 skill / closeout schema 不变 / verdict 词表不变 / hf-release 不变 / audit-skill-anatomy.py 不变 / hf-finalize 6A 不变 / 不新增 hf-* skill / 不引新 slash / 不投资第三方独立消费 / agents/ 无 specialist personas / .cursor/rules/ 不引入新 mdc 文件）：T2.a 修改现有 `harness-flow.mdc` 不新建 mdc 文件 ✓；T3 转 alias 不删除文件 ✓；无任何任务触动 24 leaf skill 非-alias 内容 ✓；无任务新增 hf-* skill 或 slash 命令 ✓ | 0/12 命中 |

## 发现项

- **[important][LLM-FIXABLE][TR2 / TR3 / TA4] T8 与 T9 完全缺失"测试设计种子"段（也缺"预期证据"段），与其它 11 个任务的字段密度不对齐。** T8 任务结构：目标 / Acceptance / 依赖 / Ready When / 初始队列状态 / Selection Priority / Files / Verify / 完成条件——缺测试设计种子 + 预期证据；T9 同样缺该 2 段。`task-plan-template.md` 默认结构含"测试设计种子 / 预期证据"两个字段；TA4 anti-pattern = "任务进入实现前没有测试设计种子"明确命中。修订建议：T8 测试种子可写为 "fail-first: `grep '0.5.1' SECURITY.md CONTRIBUTING.md` 修改前 ≥1；修改后 = 0；`grep '0.6.0' SECURITY.md CONTRIBUTING.md` 修改前 = 0；修改后 ≥1"；T9 测试种子可写为 "主要行为: 各 reviews / verification / approvals 文件齐全；fail-first: T1–T8 acceptance 全集枚举检查（任一未完成则 RED），全 GREEN 时 router 可推进到 hf-test-review chain"。轻量补齐，不需新业务事实。

- **[important][LLM-FIXABLE][TR4 / TR6 / TA7] Selection Priority (P0/P1/P2) 语义未定义，且 T4 P1 与 release-blocking 强依赖关系冲突。** § 8 选择规则只写"P0 + ready 优先于 P1 + ready"但未解释 P0/P1/P2 语义；trace 表 § 4 与 § 5 任务体内的 Priority 标注产生 3 类含义混合：(a) release-blocking + critical-path = P0（T1 / T2.{a,b,c,d} / T5）；(b) critical-path 但非 release-blocking = P0（T3）；(c) gating 收口 = P0（T9）；(d) "needed for completion 但非 critical-path" = P1（T4 / T6.{a,b} / T7）；(e) housekeeping = P2（T8）。**核心问题**：T4（regression-diff.py）是 T5（release-blocking）的硬依赖（"T1 + T2.{a,b,c,d} + T3 + T4 全部 GREEN"），若 T4 失败则整个 release-blocking gate 不可达。把 T4 标 P1、把 T3 标 P0，与"release-blocking 优先级最高"的常识不对齐。修订建议：要么 (i) 把 T4 priority 升 P0（推荐）—— 与 T4 是 release-blocking gate 的硬前置一致；要么 (ii) 在 § 8 显式定义 P0/P1/P2 语义并说明为何 T4 不升 P0（如"P0 = M1 物理层就位 critical-path；T4 是 M2 验证基础设施，可与 M1 并行不抢占"）。当前不做选择会让 router 在 T1 GREEN 后选择 T2.a（P0）而 T4（P1 + ready）排到所有 P0 之后，延后 release-blocking gate 闭合时间。

- **[minor][LLM-FIXABLE][TR6 / TA7] § 8 推荐启动顺序"T1 → T4（P1 但与 T1 并行；可单独并行）→ T2.{a,b,c}..."与同节"P0 + ready 优先于 P1 + ready"规则在单任务执行环境下自相矛盾。** Cloud agent 单 session 单任务推进，不存在真实并行；strict-rule 下 router 选 T1（P0 + ready）开始，T4（P1 + ready）等待；T1 GREEN 后 T2.{a,b,c} / T3（P0）涌入 ready，T4 仍被排在 P0 后；最终 T4 在所有 M1 P0 任务完成后才被选中。"T4 与 T1 并行"是 multi-session / multi-agent 场景的描述。建议：在 § 8 增补一句澄清"并行表述适用于多 agent 环境；cloud agent 单任务执行下按 priority + dependency 拓扑序串行选择"，或将 Finding 2 修订（T4 升 P0）与本 finding 一并处理。

- **[minor][LLM-FIXABLE][TR2 / TR4] T5 与 T2.d 在 verification 文件 `smoke-3-clients.md` 上存在所有权重叠。** T2.d acceptance T2.d.1 "verification 文件存在" + T2.d.2/3 写 3 client 段；T5 Files 段写"`smoke-3-clients.md`（后者可能已 T2.d 完成，本 task 补齐）"。两个任务都对同一文件落盘负责，"补齐"语义不清——T5 真正需要补什么？建议：(i) 把 T2.d 定位为 `smoke-3-clients.md` 唯一 owner（identity gate 完整记录），T5 仅追加 reviewer/author 分离 spot-check（NFR-004）—— T5.e 的检查可在独立位置（如 `verification/regression-2026-05-XX.md` 的 evidence section）；(ii) 或者把 NFR-004 的 reviewer/author 分离 spot-check 拆为独立任务 T5.f / T10（更清晰）。轻量边界整理。

- **[minor][LLM-FIXABLE][TR3 / TA4] T2.d 与 T5 的 fail-first 不显式声明 RED 起点。** T2.d 测试种子写"主要行为：实际 new session 启动 → identity grep PASS"——RED 应该是 "verification 文件不存在 + 3 段未填" → GREEN "文件存在 + Cursor 段含 PASS"，但任务内未显式呈现 RED；T5 同样仅写"主要行为: regression PASS + ratio ≤ 1.20"，无 RED（应是 "regression-diff.py 在仅有 baseline 一份时 SET 应 RED 或 ratio > 1.20 时 FAIL"——这本就是 fail-first 设计）。建议在 T2.d / T5 测试种子段补一句 "fail-first: <verification 文件 / 测量 record> 创建前 = file-not-exist；GREEN 后含 ..."。轻量补齐。

- **[minor][LLM-FIXABLE][TR1 / Independent / Small] T5 打包了 4 类异质验证活动**（regression-diff 实跑 / NFR-001 wall-clock × 1.20 / NFR-004 reviewer dispatch spot-check / smoke-3-clients.md 补齐），acceptance 5 条相互正交但同任务承担。INVEST "Small" 边缘命中。考虑到 T5 是 release-blocking 单点，且各活动互为 cross-check（regression-diff PASS + ratio ≤ 1.20 + reviewer 分离纪律 = HYP-002/003 综合验证），保留打包尚可，但应明确 T5.e（reviewer/author 分离）的位置（见 Finding 4）。**不阻塞**——只需在 hf-test-driven-dev 阶段按 acceptance 5 条 sequential 推进。

- **[minor][LLM-FIXABLE][TR5 / 可读性] § 1 概述 narrative "9 个可独立 TDD 推进的任务（含 1 个跨任务 collation task）"未显式标注哪个任务是 collation task。** 任务总数：T1 / T2 (4 sub) / T3 / T4 / T5 / T6 (2 sub) / T7 / T8 / T9 = 9 顶层任务（T2/T6 各算 1）或 13 leaf 任务。"1 个跨任务 collation task" 推断为 T9（"进入 review chain 收口"），但未显式声明。建议在 § 1 末尾补一句"本任务计划共 9 顶层任务（含 13 leaf sub-tasks）；T9 为跨任务 collation task，承担 hf-tasks 阶段最终交接"。轻量 wording。

## 缺失或薄弱项

- **薄弱项 1: progress.md `Next Action` 与 Session Log 滞后于实际 stage**。progress.md `Current Stage: hf-tasks-review` ✓ 但 `Next Action Or Recommended Skill: hf-design` 滞后；Session Log 仅记录 spec 阶段（最后一条 "spec approval record 落盘"），未体现 design / design-review / design approval / hf-tasks 起草。这不影响 tasks.md 内容质量，但 router 若机械读 progress.md 会被误导。建议父会话在 hf-tasks-review approval 之后顺手把 progress.md 同步到当前真实状态（Next Action → `hf-test-driven-dev` 或 `任务真人确认`，Session Log 补 design + tasks 阶段事件）。属 router 重选就绪度边缘，不阻塞本轮 tasks-review。

- **薄弱项 2: HYP-003 release gate "1/3 宿主完整 + 2/3 deferred manual" 接受度首次出现在 tasks.md，spec / ADR-007 / design 中未显式锁定**。§ 10 R1 写 "不影响 v0.6.0 release-blocking gate 通过（HYP-003 接受 1/3 宿主完整 + 2/3 deferred 状态，前提是 deferred 状态显式记录）"——这是 cloud-agent 操作化语句，spec § 4 HYP-003 Validation Plan 仅写 "3 宿主 smoke test ... Cursor 当前 session 已经是直接证据" 暗示其它宿主可后续验证，未明确"deferred 仍然算 release-blocking 通过"。建议 hf-test-driven-dev 阶段实施 T2.d / T5 时，把 deferred 接受度同步落到 `verification/smoke-3-clients.md` 的 schema notes 段，使该接受度有 ADR-007 D5 / spec NFR-001 / design D-NFR1-Schema 之外的、独立可冷读的 evidence 锚点；或更稳妥地：在 hf-completion-gate 阶段重新评估这一接受度是否需要 ADR 升级。属 release-blocking gate 内部的接受度阈值定义薄弱，不阻塞 tasks 通过。

- **薄弱项 3: T7（CHANGELOG）依赖 T1–T6 全部 GREEN，但 acceptance T7.b/c/d 列举的内容（agents/hf-orchestrator.md、CLAUDE.md、AGENTS.md、ADR-007、各 setup docs、plugin.json version 等）实际上在 T1 / T2.{a,b,c} / T3 / T6.{a,b} 完成时就已经全部物理存在**。T7 真正在等的是 T5 的 verification record（用于 Decided / Notes 段引用）+ 文档与代码一致。但 T7 目前依赖声明"T1-T6 全部 GREEN"过严——T8 反而依赖 T7（"T8 依赖: T1-T7"），意味着 T8 项目元数据 bump 在 CHANGELOG 落盘后才进行，这与 CHANGELOG 内容是否引用 T8 的元数据变更存在循环风险（实际无循环，因为 T7 只引用 T1-T6 内容；但表达上有些误导）。属任务边界清晰度薄弱，不阻塞。

- **薄弱项 4: § 4 trace 表 T8 trace 写 "（ADR-005 立场延续；version bump）"，未给具体 FR 编号**。spec FR-007 涵盖 CHANGELOG（已被 T7 承担），spec 中无独立的 "version bump" FR；T8 实际在做 SECURITY.md / CONTRIBUTING.md / `.cursor/rules/harness-flow.mdc` Hard rules 段的 v0.5.1 → v0.6.0 housekeeping，与 spec § 6.1 In-scope #8（README / setup docs 同步）擦边。建议在 § 4 trace 表 T8 行明确写 "spec § 6.1 #8 + design § 11 'Project metadata' 模块；本 feature 内非 release-blocking 但 release pre-flight 必需"，提升 trace 完整度。轻量补充。

## 结论

**需修改**

理由：6 维 rubric 中 TR3（验证与测试设计种子）= 6/10 边缘、TR2（任务合同完整性）= 7/10 / TR4（依赖与顺序正确性）= 7/10 / TR6（router 重选就绪度）= 7/10 均对应至少一条 finding；2 条 **important** finding（Finding 1：T8/T9 缺测试设计种子；Finding 2：Selection Priority 语义未定义 + T4 P1 与 release-blocking 冲突）共同未通过 → 适用"任一关键 finding important → 不得 通过"惯例。其余 5 条 minor finding（recommended order 含糊 / T2.d-T5 文件所有权重叠 / fail-first 隐式 / T5 打包 / collation task 未标）均 LLM-FIXABLE 可与 important findings 一并修订。父会话 7 项特殊关注：D-FR2-Tasks 拆解（T2 = 4 sub / T6 = 2 sub）✓、HYP-002+HYP-003 release-blocking validation 在 T5 ✓、依赖图无环 + critical path = 7 步 ✓、cloud-agent R1 deferral path 已定义 ✓——4 项核心结构正确；fail-first（部分缺失）/ INVEST（T8/T9 Testable 边缘）/ Selection Priority（T4 不一致）3 项需要修订。spec § 6.2 12 项 out-of-scope **0/12 命中**；trace 覆盖 13 任务无 orphan；与 design § 11 14 模块 / § 18 关键路径并行度一致。范围与方向稳定，**仅需 wording / 字段补齐 / priority 调整层修订**，不需推倒重来。预计 1 轮定向回修可收敛到 `通过`。

## 下一步

- 唯一下一步：`hf-tasks`
- 修订重点（按优先级）:
  1. **Finding 1 (T8/T9 测试设计种子 + 预期证据补齐)**——为 T8 写 grep 版本号 fail-first；为 T9 写 acceptance enumeration fail-first
  2. **Finding 2 (Selection Priority 语义)**——首选方案: T4 升 P0（与其作为 release-blocking gate 硬前置一致）；次选方案: § 8 显式定义 P0/P1/P2 语义并保留 T4 P1
  3. （可选）Finding 3 / 4 / 5 / 6 / 7 与重点 1/2 一并定向修订
  4. （可选）薄弱项 1-4 中的 progress.md sync 与 § 4 trace 表 T8 行补齐
- 修订后**重新派发** `hf-tasks-review` 一次，预期 1 轮收敛到 `通过`
- **不**需要回 `hf-workflow-router`：route / stage / evidence 一致，无 workflow blocker（progress.md 滞后属 housekeeping，非 stage/route 冲突）
- **不**直接进入 `任务真人确认`：遵守 `hf-tasks-review` Hard Gates "tasks review 通过并完成 approval step 前，不得进入 `hf-test-driven-dev`"；**当前 verdict = 需修改**，不触发 approval step

## 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：**否**（`需修改` 默认 `false`，按 `references/review-record-template.md` 返回规则）
- 是否需要回 router（reroute_via_router）：**否**（route / stage / evidence 一致）
- USER-INPUT findings：**无**（7 条 finding 全部 LLM-FIXABLE，由 `hf-tasks` 起草节点直接修订；不需要业务裁决 / 外部阈值 / 真人拍板）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-tasks",
  "record_path": "features/001-orchestrator-extraction/reviews/tasks-review-2026-05-10.md",
  "key_findings": [
    "[important][LLM-FIXABLE][TR2/TR3/TA4] T8 与 T9 完全缺 '测试设计种子' 与 '预期证据' 段，与其它 11 任务字段密度不对齐",
    "[important][LLM-FIXABLE][TR4/TR6/TA7] Selection Priority (P0/P1/P2) 语义未定义；T4 标 P1 但是 T5 (release-blocking) 的硬前置，与 release-blocking 优先级最高直觉冲突",
    "[minor][LLM-FIXABLE][TR6/TA7] § 8 推荐启动顺序 'T1 → T4 (P1 但与 T1 并行)' 与 'P0 + ready 优先于 P1 + ready' 规则在单任务执行下自相矛盾",
    "[minor][LLM-FIXABLE][TR2/TR4] T5 与 T2.d 在 smoke-3-clients.md 文件所有权重叠（'本 task 补齐' 语义不清）",
    "[minor][LLM-FIXABLE][TR3/TA4] T2.d / T5 fail-first 不显式声明 RED 起点",
    "[minor][LLM-FIXABLE][TR1/Independent/Small] T5 打包 4 类异质验证活动（regression / NFR-001 / NFR-004 / smoke 补齐），INVEST Small 边缘",
    "[minor][LLM-FIXABLE][TR5/可读性] § 1 概述 '9 个可独立 TDD 推进的任务（含 1 个跨任务 collation task）' 未显式标注 collation task = T9"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR2/TR3/TA4",
      "summary": "T8 (项目元数据版本号) 与 T9 (review chain 收口) 任务体完全缺 '测试设计种子' 与 '预期证据' 两个字段；与其它 11 任务的字段密度不对齐；TA4 anti-pattern 命中。修订建议：T8 测试种子可写 grep 版本号 fail-first；T9 测试种子可写 acceptance enumeration fail-first"
    },
    {
      "severity": "important",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR4/TR6/TA7",
      "summary": "Selection Priority (P0/P1/P2) 语义未在 § 8 显式定义；T4 (regression-diff.py) 标 P1 但是 T5 (release-blocking gate) 的硬前置，若 router 严格执行 'P0 优先' 则 T4 被挤后到所有 P0 任务完成。修订建议：(i) T4 升 P0；或 (ii) § 8 显式定义 P0/P1/P2 语义并说明 T4 不升的理由"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR6/TA7",
      "summary": "§ 8 推荐启动顺序 'T1 → T4 (P1 但与 T1 并行；可单独并行)' 与同节 'P0 + ready 优先于 P1 + ready' 规则在 cloud-agent 单任务执行下自相矛盾；建议增补一句澄清并行描述适用于多 agent 环境"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR2/TR4",
      "summary": "T5 与 T2.d 在 verification 文件 smoke-3-clients.md 上所有权重叠 ('本 task 补齐' 语义不清)；建议把 T2.d 定位为唯一 owner，T5 的 NFR-004 reviewer/author 分离 spot-check 改写到 regression-2026-05-XX.md 或拆独立任务"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR3/TA4",
      "summary": "T2.d / T5 测试种子段缺显式 RED 起点；建议补 'fail-first: <verification 文件> 创建前 = file-not-exist；GREEN 后含 ...' 表达"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR1/Independent/Small",
      "summary": "T5 打包 4 类异质验证活动（regression-diff + NFR-001 wall-clock + NFR-004 reviewer 分离 spot-check + smoke-3-clients.md 补齐），INVEST 'Small' 边缘命中；保留打包尚可但应整理 T5.e 位置（见 Finding 4）"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR5/可读性",
      "summary": "§ 1 概述 '9 个可独立 TDD 推进的任务（含 1 个跨任务 collation task）' 未显式标注哪个是 collation task（推断为 T9），建议补 '本任务计划共 9 顶层任务（含 13 leaf sub-tasks）；T9 为 collation task' 提升冷读友好度"
    }
  ],
  "round": 1,
  "approval_step_required_after_pass": true
}
```

---

## 修订验证（Round 2）

- 修订提交：`0f5290b` on branch `cursor/orchestrator-extraction-design-e404`
- 修订基线：`9c56124`（design-approval + tasks 起草 commit）
- 验证方法：直接读取当前 HEAD 的 tasks.md；逐条核验 Round 1 7 条 finding 的 trigger condition 是否已消除；并扫描 diff 检查是否引入新 finding（regression）；不重跑全套 6 维 rubric / 反模式扫描 / 一致性矩阵——按父会话指令仅做定向修订验证。
- 验证时间：2026-05-10
- 验证者：同 Round 1 reviewer subagent（与 author 仍分离，符合 Fagan）

### 7 条 finding 修订核验表

| # | Finding (Round 1) | 修订证据（HEAD = 0f5290b） | 是否达标 |
|---|---|---|---|
| 1 | `[important][TR2/TR3/TA4]` T8 / T9 完全缺 "测试设计种子" 与 "预期证据" 段 | **T8** 现含 "测试设计种子"（主要行为 / 关键边界 / fail-first `grep -c "v0\.6\.0" SECURITY.md CONTRIBUTING.md` 修改前 = 0；修改后 ≥ 2 / SUT Form: naive）+ "预期证据"（grep 输出 + 两文件 diff）；Verify 段也扩展为双向 grep（`v0.6.0` ≥ 2 + `v0.5.1` 修改后 = 0 防遗漏）。**T9** 现含 "任务类型: collation task" + acceptance 由 3 条扩到 4 条（T9.a-d）+ "测试设计种子"（主要行为 / 关键边界 / fail-first `Current Stage` 字段切换 / SUT Form: naive）+ "预期证据"（grep / ls / wc 命令输出 + git log 显示 T1-T8 commit 序列）。两任务字段密度与其它 11 任务对齐。 | ✓ 达标 |
| 2 | `[important][TR4/TR6/TA7]` Selection Priority (P0/P1/P2) 语义未定义；T4 P1 与 release-blocking 硬前置冲突 | § 8 新增 "Selection Priority 语义定义" 段：P0 = release-blocking 假设直接关联 OR release-blocking task 的硬前置依赖；P1 = v0.6.0 范围内 deliverable 但不阻塞 release；P2 = 锦上添花。§ 9 队列投影表 T4 行升级为 "P0（T5 硬前置）"；§ 8 推荐启动顺序 Tier 0 把 T4 与 T1 并列为 P0 起点；并显式给出"T4 升 P0 的理由"（按 P0 定义"是 release-blocking task 的硬前置依赖"自动晋升）。**残留**：§ 5 任务体 T4 行（line 215）仍写 "Selection Priority: P1"，与 § 8 / § 9 / Tier 0 三处 P0 表述不一致——属documentation drift（功能性优先级以 § 9 队列投影为权威，router 不会被误导，但单文件内存在三正一负的 stale label）——见 Round 2 残留 finding R2-1（minor，cosmetic 单行编辑） | ✓ 实质达标（Round 1 important finding 的功能本质已修订；T4 body 残留是 minor cosmetic） |
| 3 | `[minor][TR6/TA7]` § 8 推荐启动顺序与 "P0 + ready 优先于 P1 + ready" 规则在单任务执行下自相矛盾 | § 8 完全重写为 Tier 0–6 模型：每 Tier 内的任务可并行调度，Tier 间严格 GREEN-gate；同时保留三条排序规则（P0 优先 / 同 priority 拓扑序 / 多任务并行时最长路径优先）。Tier 模型本质上把"并行表述"与"single-task router 选择规则"解耦——并行性表达在 Tier 内的多任务集合，不在跨 Tier 的并行声明里。原矛盾消除。 | ✓ 达标 |
| 4 | `[minor][TR2/TR4]` T2.d 与 T5 在 smoke-3-clients.md 文件所有权重叠 | **T2.d** 标题段已显式标"**T2.d 是该文件唯一所有者**；T5 引用但不写"；Files 段标"**T2.d 唯一写入者**"。**T5** Acceptance T5.b 标 regression-2026-05-XX.md "**T5 是该文件唯一所有者**"；T5.c 标 load-timing-3-clients.md "**T5 是该文件唯一所有者**；T2.d 不写此文件"；Files 段标"与 T2.d 的 smoke-3-clients.md 物理分文件以避免所有权重叠"。3 个 verification 文件物理分离，所有权清晰。 | ✓ 达标 |
| 5 | `[minor][TR3/TA4]` T2.d / T5 fail-first 不显式声明 RED 起点 | **T2.d** 测试种子新增 bullet "**fail-first（显式 RED 起点）**: 进入 T2.d 前 `test -f ... smoke-3-clients.md` = false（文件不存在）→ T2.d 完成后 `test -f` = true 且 `grep -c "PASS\\|deferred" smoke-3-clients.md` = 3"。**T5** 测试种子新增 bullet "**fail-first（显式 RED 起点）**: 进入 T5 前 `test -f regression-2026-05-XX.md` = false 且 `test -f load-timing-3-clients.md` = false（两文件均不存在）；T5 完成后两文件均存在且 grep 'PASS' 命中"。RED → GREEN traceable。 | ✓ 达标 |
| 6 | `[minor][TR1/Independent/Small]` T5 打包 4 类异质验证活动，INVEST Small 边缘 | T5 任务体新增 "INVEST Small 备注" 段（line 229）：(a) 共享前置（T1+T2+T3+T4 全部 GREEN）；(b) 共享目标（HYP-002 / HYP-003 release-blocking 双假设的 fresh evidence 落盘）；(c) 共享可逆点（任一活动 FAIL → 全 task 回 hf-design）。同时给出"如未来发现 hf-test-driven-dev 阶段单独跑某一活动更顺畅，可在 increment ADR 中拆为 T5.a/b/c"的逆向通道。打包合理性显式可冷读。 | ✓ 达标 |
| 7 | `[minor][TR5/可读性]` § 1 "9 个可独立 TDD 推进的任务（含 1 个跨任务 collation task）" 未显式标 collation task = T9 | § 1 概述重写为 "12 个可独立 TDD 推进的任务（T1 / T2.{a,b,c,d} / T3 / T4 / T5 / T6.{a,b} / T7 / T8 实现层）+ **1 个 collation task**（T9，跨任务收口节点；不产出新文件，只校验完整性 + 状态同步）"。T9 标题前缀加 "Collation：进入 review/gate chain 前的状态收口"；T9 任务体首行加 "**任务类型**: **collation task**" + 行为说明（不产出新文件；只校验完整性 + 同步状态字段）。collation task 标注三处显式（§ 1 / T9 标题 / T9 任务类型字段），冷读友好度大幅提升。 | ✓ 达标 |

### Regression 扫描

逐项检查修订是否破坏 spec / design / ADR-007 整体一致性：

| 检查 | 结果 |
|---|---|
| spec § 6.2 12 项 out-of-scope 是否被本轮修订引回？ | ✗ 无破坏。修订仅触动 § 1 narrative / § 5 各任务字段密度 / § 8 Selection Priority 语义 + Tier 模型 / § 9 T4 优先级，与 24 leaf skill 不动 / 不删旧 skill / closeout schema 不变 / verdict 词表不变 / hf-release 不变 / audit-skill-anatomy.py 不变 / hf-finalize 6A 不变 / 不新增 hf-* skill / 不引新 slash 命令 / 不投资第三方独立消费 / agents/ 无 specialist personas / .cursor/rules/ 不引新 mdc 文件等立场全部正交无关 |
| design D-X 决策是否被本轮修订矛盾？ | ✗ 无矛盾。D-FR2-Tasks (T2 = 4 sub / T6 = 2 sub) 维持；D-Layout / D-Disp / D-Mig / D-Stub / D-Stub-Marker / D-Host-Cursor/CC/OC / D-Identity / D-NFR1-Schema / D-RegrLoc / D-RegrImpl / D-Skip-DDD / D-Skip-Threat 全部保留 |
| ADR-007 D1-D7 是否被本轮修订冲击？ | ✗ 无冲击。D1 三层架构 invariant + 生效阶段子段 / D2 single source / D3 6 步落地路径 / D4 兼容期 deprecated alias / D5 release-blocking 假设清单 / D6 与 v0.6+ ops/release skill 关系 / D7 personas 不扩张——本轮修订全部正交 |
| T4 升 P0 后是否引入新依赖循环？ | ✗ 无。T4 本身依赖为空（M2 起点）；P0 仅是优先级 label 升级，不改依赖关系；§ 6 依赖图不变 |
| Tier 0–6 模型与 § 6 critical path 是否一致？ | ✓ 一致。critical path "T1 → T2.{a,b,c} → T2.d → T5 → T7 → T8 → T9" 沿 Tier 0 (T1) → Tier 1 (T2.a/b/c) → Tier 2 (T2.d) → Tier 3 (T5) → Tier 4 (T7) → Tier 5 (T8) → Tier 6 (T9) 推进，最长串行链 7 步与 Tier 间序数 7 一致 |
| T2.d / T5 文件所有权分离后，3 个 verification record（regression / smoke / load-timing）是否覆盖完整？ | ✓ 覆盖完整。T2.d → smoke-3-clients.md（identity gate）；T5 → regression-2026-05-XX.md（HYP-002 等价语义）+ load-timing-3-clients.md（HYP-003 wall-clock × 1.20）。design § 11 14 模块表中 verification records 三件套与 spec NFR-001 / NFR-005 / FR-002.d acceptance 一一对应 |
| T8 fail-first 双向 grep（`v0.6.0` ≥ 2 + `v0.5.1` 修改后 = 0）是否有副作用？ | ✗ 无。`grep -c "v0\\.5\\.1" CONTRIBUTING.md` 修改后 = 0 是正向防遗漏检查（避免 v0.5.1 旧引用残留），不影响 T7 CHANGELOG 中合法的 v0.5.1 历史 release 记录（不在 SECURITY.md / CONTRIBUTING.md 范围内） |
| T9 collation task 加 "新分支 cursor/orchestrator-extraction-impl-e404 已创建" (T9.d) 是否与 spec / design 冲突？ | ✗ 无冲突。spec / design 未约束实现分支命名；progress.md 也未要求；T9.d 是 author 本轮新增的 housekeeping 步骤，属合理收口；可冷读判定 |

**Regression 扫描结果：0 命中**。无新 finding 被引入，无现有 D-X / spec § 6.2 / ADR-007 D1-D7 立场被破坏。

### Round 2 残留 finding

- **R2-1（minor，LLM-FIXABLE，cosmetic）**：§ 5 T4 任务体 line 215 仍写 "Selection Priority: P1"，与 § 8 Selection Priority 语义定义、§ 8 推荐启动顺序 Tier 0 标 "T4 (P0)"、§ 9 队列投影表 T4 "P0（T5 硬前置）"、以及 § 8 末尾"关于 T4 升 P0 的理由"四处 P0 表述不一致。**功能性影响 = 0**：router 的 canonical 视图是 § 9 队列投影（已 P0）+ § 8 排序规则（已含 P0/P1/P2 语义），不会被 § 5 task body 单行 stale label 误导；此为单文件内 4 正 1 负的 documentation drift。修订建议：单行编辑——把 line 215 从 "**Selection Priority**: P1" 改为 "**Selection Priority**: P0（从 P1 提升；T5 硬前置依赖，按 § 8 P0 定义自动晋升）"。可在 hf-test-driven-dev 阶段 T4 启动前的 RED 步顺手处理，**不阻塞 tasks-review 通过**。

无其它残留 finding。

### 最终 Verdict

**通过**

理由：Round 1 7 条 finding 中 6 条 (Finding 1 / 3 / 4 / 5 / 6 / 7) 完全达标；Finding 2 (Selection Priority 语义 + T4 升 P0) 的功能本质已通过 § 8 新语义段 + § 9 队列投影 P0 + Tier 0 双起点 + § 8 末尾理由说明四处显式表达完成修订，仅残留 § 5 T4 task body line 215 单行 stale "P1" label（R2-1，minor cosmetic），不影响 router canonical 视图；Regression 扫描 0 命中，无新 finding，spec § 6.2 12 项 out-of-scope / design D-X / ADR-007 D1-D7 全部维持。tasks.md 现已具备进入 hf-test-driven-dev 阶段的稳定输入条件：所有关键任务 Acceptance / Files / Verify / 测试设计种子 / 预期证据 / 完成条件齐全；Selection Priority 语义清晰且 P0 任务集合与 release-blocking 假设/硬前置依赖一致；Tier 0–6 启动顺序与 critical path 7 步一致；T2.d / T5 文件所有权分离消除写冲突；T9 collation task 标注三处显式。

### 下一步

- 唯一下一步：**`任务真人确认`**（`needs_human_confirmation = true`，由父会话承担 approval step）
- approval 通过后再进入 `hf-test-driven-dev`
- **不**直接进入 `hf-test-driven-dev`：遵守 `hf-tasks-review` Hard Gates "tasks review 通过并完成 approval step 前，不得进入 `hf-test-driven-dev`" + "reviewer 不代替父会话完成 approval step"
- approval 后建议 hf-test-driven-dev 阶段在 T4 RED 步顺手把 R2-1（line 215 stale "P1" label）改为 P0 一致表述
- 另建议父会话在 hf-tasks-review approval 之后顺手把 progress.md `Next Action` (`hf-design` → `任务真人确认` 或 `hf-test-driven-dev`) + Session Log (补 design / design-review / design-approval / hf-tasks 起草 / hf-tasks-review R1+R2 事件) 同步——属 Round 1 薄弱项 1 的延伸，本轮维持原判定（不阻塞）

### 评审者元数据

- 是否需要人工裁决（needs_human_confirmation）：**是**（`通过` 触发"任务真人确认"步骤；与 `references/review-record-template.md` 返回规则 + `reviewer-return-contract.md` `hf-tasks-review` 通过 = `true` 一致）
- 是否需要回 router（reroute_via_router）：**否**（route / stage / evidence 一致，无 workflow blocker）
- USER-INPUT findings：**无**（R2-1 残留 minor cosmetic 由 hf-test-driven-dev 阶段顺手修订；不需要业务裁决 / 外部阈值 / 真人拍板）

### 更新后的结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "任务真人确认",
  "record_path": "features/001-orchestrator-extraction/reviews/tasks-review-2026-05-10.md",
  "key_findings": [
    "[minor][LLM-FIXABLE][TR4/cosmetic] § 5 T4 任务体 line 215 仍写 'Selection Priority: P1'，与 § 8 / § 9 / Tier 0 三处 P0 表述不一致（documentation drift；router canonical 视图为 § 9 已 P0；不阻塞，hf-test-driven-dev 阶段 T4 RED 步顺手单行编辑）"
  ],
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "TR4/cosmetic",
      "summary": "Round 1 Finding 2 残留：§ 5 T4 task body line 215 'Selection Priority: P1' 是 documentation drift；§ 8 Selection Priority 语义定义 / § 8 Tier 0 / § 9 队列投影表 / § 8 末尾理由说明 4 处均已 P0；功能性 router 视图不受影响；建议 hf-test-driven-dev 阶段 T4 RED 步顺手改为 P0 表述"
    }
  ],
  "round": 2,
  "round_1_findings_resolved": "6 of 7 fully resolved + 1 (Finding 2) 实质达标但 § 5 task body line 215 残留 cosmetic stale label",
  "round_2_new_findings": 1,
  "round_2_new_findings_severity": "minor (cosmetic, non-blocking)",
  "approval_step_required_before_test_driven_dev": true
}
```


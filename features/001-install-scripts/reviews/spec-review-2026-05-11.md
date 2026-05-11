# Spec Review — 001-install-scripts (2026-05-11)

- Reviewer: 独立 reviewer subagent（cursor cloud agent 派发）
- Author of spec under review: cursor cloud agent（hf-specify 节点）
- Author / reviewer separation: ✅（不同会话）
- Spec under review: `features/001-install-scripts/spec.md`
- Deferred backlog: `features/001-install-scripts/spec-deferred.md`
- Profile / Mode: `full` / `auto`
- Rubric: `skills/hf-spec-review/references/spec-review-rubric.md`
- Authoring contract: `skills/hf-specify/references/requirement-authoring-contract.md`
- NFR QAS contract: `skills/hf-specify/references/nfr-quality-attribute-scenarios.md`

## 结论

需修改

理由摘要：spec 整体结构、可追溯性、QAS 契约、HYP 表、deferred backlog 完整度都达到 hf-design 输入的水平；没有阻塞设计的 USER-INPUT 业务事实空洞。但 NFR-004 一条阈值与 NFR-003 内部不一致（"至少有 1 个跑通" vs "全部 PASS"），并且 §6 范围列举遗漏了一个 FR/NFR 普遍依赖的 flag (`--host`)，构成"作者修一轮即可达标"的 important + 若干 minor 收口。

## Precheck

| 检查项 | 结果 | 说明 |
|---|---|---|
| 存在稳定 spec draft | ✅ | `spec.md` 14 章节齐全，状态字段=草稿 |
| Route / stage / profile 已明确 | ✅ | `progress.md` Current Stage=`hf-specify`，Pending Reviews=`hf-spec-review`，Profile=`full`，Mode=`auto` |
| 上游证据一致 | ✅ | progress.md 引用的 ADR-006 / ADR-005 在仓库内确实存在；CHANGELOG `[0.5.0]` / `[0.5.1]` 段与 spec §1 / §11 引用一致 |
| Deferred backlog 已显式存在 | ✅ | DEF-001..DEF-007 与 spec §7 一一对应 |

→ Precheck 通过，进入正式 rubric。

## 发现项

### Important

- [important][LLM-FIXABLE][Q4][Q2] **NFR-004 Response Measure 阈值与 NFR-003 内部矛盾**。Anchor: `spec.md` §9 NFR-004（"在 macOS bash 3.2 + Linux bash 5.x 两个环境下，6 个 e2e scenario **至少有 1 个**跑通"）vs §9 NFR-003（"6 个组合**全部** PASS"）。What: 同一份 e2e 测试矩阵，在 NFR-003 中是"全部 PASS = 通过"，在 NFR-004 中阈值是"至少 1/6 = 通过"。Why: (a) 两条 NFR 互相冲突，reviewer 无法判断到底哪条是验收依据；(b) "至少 1/6" 作为 portability/no-extra-runtime-dep 的判定门槛过弱——只要 install 启动就算过，没法证明无 jq/python 隐式依赖在 6 个组合下都成立；(c) 配套的 "macOS bash 3.2" 与 §2 "bash 4+" 的口径差异在 NFR-004 内被引入，但 Acceptance 没说清两环境是否都要全 PASS。Suggested fix: 把 Response Measure 改为"在两个环境下 6 个 e2e scenario **全部** PASS（与 NFR-003 共享同一矩阵）"，或明确拆分为"NFR-003 = CI 默认环境全 PASS，NFR-004 = 仅做 Linux bash 5.x 全 PASS + macOS bash 3.2 上至少 N 个 PASS（N 由作者决定）"。如果 N < 6 是有意为之（mac 上某些 symlink 行为差异），应在 spec 内显式写明哪些 scenario 允许 SKIP 与 SKIP 理由。

### Minor

- [minor][LLM-FIXABLE][Q3][C2] **`--host` flag 在 §6 当前轮范围列举中缺失**。Anchor: `spec.md` §6 "提供 `install.sh`（bash）：`--target … × --topology … × --dry-run × --verbose × --force`" 与所有 FR Acceptance（FR-001/-002/-003/-004/-005/-006、NFR-001 Acceptance）均使用 `--host /tmp/host`（spec 内 `--host` 出现 11 次）。What: §6 把当前轮 CLI 表达面列举为 5 个 flag，但实际依赖的第 6 个 flag `--host <path>` 没有列出，且 spec 没有显式说明 host 的默认值是 `.`（NFR-001 Acceptance 暗示 `--host .` 可用）还是必填。Why: design 阶段需要确认 `--host` 是 FR-001 的子参数还是独立 flag，以及"省略 --host 时默认 cwd"是否在范围内。Suggested fix: §6 把 flag 列举补全为 `--target × --topology × --dry-run × --verbose × --force × --host <path>`，并补一句"省略 `--host` 时默认 `.`（cwd）"或显式声明 `--host` 必填。

- [minor][LLM-FIXABLE][Q4] **§2 与 NFR-004 关于 bash 版本兼容口径不一致**。Anchor: `spec.md` §2 "bash 4+（macOS 自带 3.x 也要兼容）" vs §9 NFR-004 "macOS bash 3.2 兼容；Linux bash 4+ / 5+ 主测"。What: §2 表述自相矛盾（"4+" 同时又"兼容 3.x"），下游 NFR-004 才把口径压实到"3.2 兼容 + 4/5 主测"。Why: 单读 §2 的人会以为 bash 4 是硬下限。Suggested fix: §2 改写为"bash 3.2+ 兼容（POSIX 子集），主测 bash 4/5"；或在 §2 加一句指针"具体兼容口径见 NFR-004"。

- [minor][LLM-FIXABLE][Q3] **FR-002 Acceptance 仅覆盖 opencode × {symlink, copy} 2 例，未覆盖 cursor × symlink 与 both × symlink**。Anchor: `spec.md` §8 FR-002 Acceptance（仅 opencode 两条）vs §3 Success Metrics "3 target × 2 topology = 6 个组合全部 PASS" 以及 NFR-003 e2e 测试矩阵。What: FR-002 是 topology FR，但只为 opencode 写了两个验收，cursor 与 both 在 symlink topology 下没有 FR-级 acceptance。Why: design 时如果某条 cursor symlink 行为没人想清楚（例如 `.cursor/rules/harness-flow.mdc` 是 symlink 还是 copy），FR-002 不会拦住它。Suggested fix: 在 FR-002 acceptance 补一条 cursor × symlink 用例，或者在 FR-002 后用一行明确"cursor / both target 下的 symlink 行为继承 opencode 同 topology 语义，详见 NFR-003 6 组合矩阵"。

- [minor][LLM-FIXABLE][Q1][Q8] **§3 Success Metrics 引用的 trace 锚点 "docs/opencode-setup.md §2 的'列出 24 个 hf-\*'" 与 opencode-setup.md §2 实际文本不匹配**。Anchor: `spec.md` §3 Outcome Metric / Leading Indicator 1 引用了 "docs/opencode-setup.md §2 / docs/cursor-setup.md §3 的 verify 文本"。What: opencode-setup.md §2 line 79 的实际文本是 "23 `hf-*` skills + `using-hf-workflow`（v0.2.0 added `hf-browser-testing` as the 23rd）"；cursor-setup.md §3 没有列出数字。spec 自己其它处用 24 是对的（与 CHANGELOG `[0.5.1]` / cursor-setup Scope Note "still 24 hf-* + using-hf-workflow" 一致）。Why: trace 锚点文本对不上会让 doc-freshness gate 误以为 spec 引用 stale 文档；这其实是 opencode-setup.md §2 自身的 stale 文本（v0.2.0 → v0.5.1 之间漏更新），但 spec 不应把不存在的"24"字面量假托给该位置。Suggested fix: 把 spec §3 引用改为"verify 步骤要求列出当前 HF 仓库内 `find skills -name SKILL.md -mindepth 2 -maxdepth 2` 全部条目（v0.5.1 = 24 个 hf-\* + 1 个 using-hf-workflow = 25 条）"，或写成"verify 步骤通过 = `find` 输出条数 ≥ 24 且包含 `using-hf-workflow` 与 `hf-workflow-router`"。

- [minor][LLM-FIXABLE][A3] **NFR-002 QAS Response 出现"in-memory 已记录条目"实现细节**。Anchor: `spec.md` §9 NFR-002 QAS Response。What: "基于 in-memory 已记录条目" 描述了一种回滚实现机制（脚本运行时变量栈）。Why: spec 阶段不必锁实现策略——也可以是"分阶段先写临时 manifest 再原子重命名"等。Suggested fix: 改写为"基于已落盘条目集合"或"基于本次 install 的 entries 集合"，让 design 自行选择"in-memory 跟踪 vs 临时 manifest"。

- [minor][USER-INPUT][C7] **FR-003 manifest 字段 `hf_commit` 隐含"HF 仓库始终是 git checkout"假设**。Anchor: `spec.md` §8 FR-003 / §12 假设段。What: 如果用户用 zip 下载 HF 仓库（GitHub Releases → Source code zip）或 detached snapshot，`git rev-parse HEAD` 不可用，`hf_commit` 字段无法填充。Why: 当前 §12 没有把这个假设显式列出；脚本在非 git 环境下应回退到读 `.git`-less marker（如 `CHANGELOG.md` 顶部版本号）还是直接报错？Suggested fix: 在 §12 加一行 ASM "假设 HF 仓库是 git checkout（含 `.git/` 目录）；若失效，FR-003 manifest `hf_commit` 字段降级为 `unknown` 字符串还是脚本拒绝运行，由 design 决定"，或把这个改成 design 的 O-005 开放问题。

## 缺失或薄弱项

- §3 Success Metrics 行 `Measurement Method` 与 `Non-goal Metrics` 与 `Instrumentation Debt` 同样以"行"形式排在表内（而非 `Outcome Metric` / `Leading Indicator` 系列的"指标 | 阈值 | 测量方法"三列结构），表头"指标 / 阈值 / 测量方法"在最后 3 行被语义复用为"角色 / 内容 / 空"，结构略显杂糅；不影响可读性，列为薄弱项不计入 finding。
- §6 关键边界第 2 条 "脚本只动 4 类目标路径之一" 与 §11 约束段没有重复列举，但 §11 没有把 "4 类路径" 显式锁住；建议 design 节点把这 4 类路径作为 FR-001 的 invariant 落到 design contract。
- HYP-002 Validation Plan 与 FR-004 Acceptance #1 等价（先 install → 加非 HF skill → uninstall → 验非 HF skill 仍在），spec 内部已自洽，但建议 design 阶段把这条同时标记为 TDD 第一道 RED test 用例，以兑现 §4 "HYP-002 PASS 证据是 hf-completion-gate 前置"。

## 覆盖检查

| Group | Rule | 检查结果 |
|---|---|---|
| Q | Q1 Correct | ✅ 每条 FR/NFR 都有 Source / Trace Anchor（用户请求 / HYP-XXX / 场景 X / ADR-006 D1 / CHANGELOG） |
| Q | Q2 Unambiguous | ⚠️ NFR-004 "至少 1 个跑通" 阈值偏弱且与 NFR-003 矛盾（important finding 1）；其余 NFR Response Measure 都有数字阈值（≤ 10s / ≤ 120s / ≥ 24 / ≥ 1） |
| Q | Q3 Complete | ⚠️ §6 缺 `--host` flag（minor finding 2）；FR-002 acceptance cursor symlink 案例缺（minor finding 4）；其余输入/输出/错误路径覆盖良好（FR-001 缺 --target / FR-004 缺 manifest / FR-005 dry-run / FR-006 重复 install） |
| Q | Q4 Consistent | ⚠️ §2 vs NFR-004 bash 口径不一致（minor finding 3）；NFR-003 vs NFR-004 阈值矛盾（important finding 1）；其余 FR / NFR / HYP 三表互相一致 |
| Q | Q5 Ranked | ✅ 8 条 FR + 4 条 NFR 都标注了 MoSCoW 优先级；FR-007 = Should，其余 = Must；无"全 Must"懒惰标注 |
| Q | Q6 Verifiable | ✅ 每条 FR / NFR 都有 BDD Acceptance；都能形成 PASS / FAIL 判断 |
| Q | Q7 Modifiable | ✅ FR / NFR / HYP / 范围 / 边界 分散在不同章节但内部不重复矛盾（除 finding 1 / 3） |
| Q | Q8 Traceable | ⚠️ §3 trace 锚点文本不完全匹配 opencode-setup.md §2 实际文字（minor finding 5）；其余 trace 锚点（ADR-006 D1 / CHANGELOG / 场景 A-F / HYP-001..004）可冷读回指 |
| A | A1 模糊词 | ✅ 没有"快 / 稳 / 友好 / 易用"等未量化词；所有 NFR 都用 QAS 5 要素格式 |
| A | A2 复合需求 | ✅ FR-001 / FR-002 / FR-005 / FR-006 / FR-007 都是单一关注点；FR-003 manifest 写入 + 字段约束在同一 FR 内（manifest schema 与"写入 manifest"是同一行为，不算复合） |
| A | A3 设计泄漏 | ⚠️ NFR-002 "in-memory" 表述（minor finding 6）；FR-003 manifest 字段名 / FR-005 dry-run 标准输出格式 处于"用户可观察 vs 实现细节"边界，可接受 |
| A | A4 无主体被动表达 | ✅ 所有 FR 主体均为"系统 / 脚本"；触发条件 / 用户角色清晰 |
| A | A5 占位或待定值 | ✅ 关键 FR / NFR 内无 TBD / 待确认；§13 O-001..O-004 已显式标"design 决定"且都不阻塞；spec §6 manifest 落点用"最终 schema 见 design"标记 design 决策点（合规） |
| A | A6 缺少负路径 | ✅ FR-001 缺 `--target` 失败、FR-004 manifest 缺失失败、FR-006 重复 install 拒绝、NFR-002 中断回滚均有显式负路径 acceptance |
| C | C1 Requirement contract | ✅ 8 FR + 4 NFR 全员具备 ID / Statement / Acceptance / Priority / Source；NFR 加 ISO 25010 维度 + QAS 五要素 |
| C | C2 Scope closure | ⚠️ §6 缺 `--host` 列举（minor finding 2）；§7 与 spec-deferred.md DEF-001..DEF-007 一一对应；其余范围内/外清晰 |
| C | C3 Open-question closure | ✅ §13 显式分"已关闭 / 非阻塞 / 阻塞 = 无"三段；4 条非阻塞 O-001..O-004 都明确 design 阶段决定 |
| C | C4 Template alignment | ✅ 14 章节遵循 hf-specify 默认骨架（背景 / 目标 / Success Metrics / HYP / 角色场景 / 范围 / 范围外 / FR / NFR / 接口依赖 / 约束 / 假设 / 开放问题 / 术语） |
| C | C5 Deferral handling | ✅ spec-deferred.md DEF-001..DEF-007 7 条；与 §7 文字一一对应；含"延后理由 + 回收触发信号"两列 |
| C | C6 Goal and success criteria | ✅ §2 总体成功标准 + §3 Success Metrics 表（Outcome / Leading Indicator 1-2 / Lagging Indicator）齐全；阈值具体可判 |
| C | C7 Assumption visibility | ⚠️ FR-003 `hf_commit` 隐含 git checkout 假设未显式（minor finding 7）；其余假设（HYP-001..004 + §10 接口失效影响 + §11 ADR-006 D1 / ADR-005 D9 / ADR-004 D7 约束 + §12 失效影响）显式入档 |
| G | G1 Oversized FR | ✅ 8 条 FR 都是单一关注点，没有 GS1-GS6 命中（无多角色打包 / 无 CRUD 打包 / 无场景爆炸 / 无跨层关注点 / 无多状态混写 / 无时间耦合） |
| G | G2 Mixed release boundary | ✅ 当前轮（shell install）与延后（PowerShell / npx / Claude Code install / global multi-version / AGENTS.md merge / telemetry / audit）在 §7 + spec-deferred.md 完全分离；无混写 |
| G | G3 Repairable scope | ✅ findings 全部可在 1 轮 hf-specify 回修内收敛；无需推倒重来 |

INVEST 抽样（FR-001 / FR-003 / NFR-002 / NFR-004）：
- Independent: ✅ 8 条 FR 之间没有强依赖（FR-004 依赖 FR-003 manifest 是合理的功能依赖，不是 INVEST 反模式）
- Negotiable: ✅ Acceptance 留出 design 决策空间（FR-001 cursor vendor 路径 / FR-003 manifest schema 落地 / O-001 JSON vs txt）
- Valuable: ✅ 每条 FR 都对应 §5 场景或 user 请求
- Estimable: ✅ 颗粒度足以让 hf-design / hf-tasks 估工
- Small: ✅ 8 条 FR 都在 1 个 e2e scenario 内可测
- Testable: ✅ 每条 FR 都有 BDD Acceptance；NFR 都有 QAS Response Measure

## 下一步

- 由 hf-spec-review 返回的 verdict = `需修改`，下一节点 = `hf-specify`
- 父会话需让 author 在 1 轮内修复 1 条 important + 6 条 minor，重点是 NFR-004 阈值与 NFR-003 对齐 + §6 列举补 `--host`
- 修复完成后回到 hf-spec-review 复审；预计 1 轮即可达 `通过`，不需要 `hf-workflow-router` 介入（route / stage / 证据均无冲突）

## 记录位置

- `features/001-install-scripts/reviews/spec-review-2026-05-11.md`

## 交接说明

- 本 verdict = `需修改`，按 `skills/hf-spec-review/references/review-record-template.md` 默认表 `needs_human_confirmation = false`，但 user 任务指令显式要求 `needs_human_confirmation: true`（"always true for spec review verdicts that aren't pure block"）—— 以 user 任务指令为准
- `reroute_via_router = false`（内容回修，非 workflow blocker）
- 所有 finding 归属 `LLM-FIXABLE`（5 条）+ `USER-INPUT`（1 条，FR-003 `hf_commit` 退化策略需要业务裁决）
- LLM-FIXABLE finding 不需要让用户回答；USER-INPUT 只有 1 条且粒度小（`hf_commit` 在非 git 环境下：报错 vs 写 `unknown` vs 写 `CHANGELOG` 版本号），父会话可一次性向用户问询

## 结构化返回（供父会话使用）

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-specify",
  "record_path": "features/001-install-scripts/reviews/spec-review-2026-05-11.md",
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "key_findings": [
    "[important][LLM-FIXABLE][Q4][Q2] NFR-004 '至少 1/6 跑通' 与 NFR-003 '全部 PASS' 矛盾，且作为 portability 验收偏弱",
    "[minor][LLM-FIXABLE][Q3][C2] §6 范围列举遗漏 `--host` flag，但 11 处 FR/NFR Acceptance 都在用",
    "[minor][LLM-FIXABLE][Q4] §2 'bash 4+（兼容 3.x）' 与 NFR-004 'bash 3.2 兼容' 表述不一致",
    "[minor][LLM-FIXABLE][Q3] FR-002 acceptance 仅覆盖 opencode × {symlink, copy} 2 例，未覆盖 cursor symlink",
    "[minor][LLM-FIXABLE][Q1][Q8] §3 trace 锚点 'opencode-setup §2 列出 24 个 hf-*' 与该文档实际 '23 hf-*' 文本不匹配",
    "[minor][LLM-FIXABLE][A3] NFR-002 QAS 'in-memory 已记录条目' 是实现细节，可去设计语言",
    "[minor][USER-INPUT][C7] FR-003 manifest `hf_commit` 隐含 'HF 是 git checkout' 假设未显式入档"
  ],
  "finding_breakdown": [
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "Q4+Q2", "summary": "NFR-004 阈值与 NFR-003 矛盾且偏弱"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q3+C2", "summary": "§6 缺 --host flag 列举"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q4", "summary": "§2 与 NFR-004 bash 口径不一致"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q3", "summary": "FR-002 acceptance 缺 cursor symlink 案例"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "Q1+Q8", "summary": "§3 trace 锚点与 opencode-setup §2 实际文本不一致"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "A3", "summary": "NFR-002 'in-memory' 实现细节泄漏"},
    {"severity": "minor", "classification": "USER-INPUT", "rule_id": "C7", "summary": "FR-003 hf_commit 在非 git 环境降级策略未入档"}
  ],
  "coverage_summary": {
    "groups_applied": ["Q1-Q8", "A1-A6", "C1-C7", "G1-G3"],
    "invest_sample": ["FR-001", "FR-003", "NFR-002", "NFR-004"],
    "precheck": "passed",
    "deferred_backlog_check": "passed (DEF-001..DEF-007 与 §7 一一对应)",
    "trace_anchor_check": "1 处 trace 文本不匹配（minor finding 5）；其余 ADR / CHANGELOG / 场景锚点全部可冷读回指",
    "blocking_open_questions": "无（§13 阻塞段为空）",
    "blocking_hypothesis_unvalidated": "无（HYP-002 = Blocking 但 confidence Medium + 明确 Validation Plan + 兜底说明）"
  }
}
```

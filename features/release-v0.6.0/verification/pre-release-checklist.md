# Pre-Release Engineering Checklist — v0.6.0

- 验证时间: 2026-05-10
- 执行人: HF Orchestrator (parent session)

## C — Candidate features 范围确认（5 项）

| # | Check | Status | Notes |
|---|---|---|---|
| C1 | Candidate features 列表清晰 | ✓ PASS | 单 candidate `features/001-orchestrator-extraction/`（HF 第一个 coding-family feature） |
| C2 | 每 candidate 有 workflow-closeout closeout.md | ✓ PASS | `features/001-orchestrator-extraction/closeout.md` Closeout Type = `workflow-closeout` |
| C3 | 每 candidate closeout.md 由对应 closeout.html 视觉渲染（v0.5.0 ADR-005 D1） | ✓ PASS | `closeout.html` 31,580 bytes（render-closeout-html.py 输出） |
| C4 | Deferred features 显式列出 + reason | ✓ PASS | release-pack.md § Scope Summary > Deferred Features 含 8 项延后理由 |
| C5 | Scope ADR 锁定 minor bump 决策 | ✓ PASS | ADR-007（minor structural refactor；不引入新功能扩张范围；ADR-007 D1 三层 invariant + D3 6 步路径 + D6 v0.7+ skill 约束 + D7 personas 延后） |

## D — Decisions 一致性（11 项；ADR-001 至 ADR-007 全核验）

| # | Check | Status | Notes |
|---|---|---|---|
| D1 | ADR-001 D1 "P-Honest narrow but hard" 延续 | ✓ PASS | v0.6.0 严格 ADR-007 D3 Step 1 范围；0 leaf skill 修改 |
| D2 | ADR-002 D11 reviewer verdict 词表 | ✓ PASS | 词表不动；7 reviews 使用既有 verdict 词汇（通过 / 需修改 / 阻塞） |
| D3 | ADR-003 D2 Cursor 第三宿主 | ✓ PASS | 3 宿主 always-on stub 全部覆盖 |
| D4 | ADR-004 D2 hf-release release-tier standalone（不部署不监控） | ✓ PASS | 本 release pack ready-for-tag 状态；不自动 git tag；不部署 |
| D5 | ADR-004 D3 hf-release 与 router 解耦 | ✓ PASS（关键先例） | ADR-007 D1 把 ADR-004 D3 解耦能力下放到 coding family；hf-release 自身行为不变 |
| D6 | ADR-005 D4 hf-finalize 唯一被改 skill（v0.5.0） | ✓ PASS | v0.6.0 不再修改 hf-finalize；step 6A 不变；render-closeout-html.py 位置不变 |
| D7 | ADR-005 D7 5 deferred ops/release skills + 3 personas | ✓ PASS | ADR-007 D6 + D7 锁定继续延后；本轮无新 skill / persona |
| D8 | ADR-006 D1 4 子目录 skill anatomy | ✓ PASS | `agents/` 是新引入的 agent persona 目录类别，不属于 skill anatomy；audit-skill-anatomy.py 透明 |
| D9 | ADR-006 D2 render-closeout-html.py 物理位置 | ✓ PASS | 仍在 `skills/hf-finalize/scripts/`（v0.5.1 位置不动） |
| D10 | ADR-007 D1-D7 全部锁定（本 release 候选 ADR） | ✓ PASS | ADR-007 起草中 → accepted（features/001-orchestrator-extraction/closeout.md Final Confirmation） |
| D11 | 本 release 不引入新 ADR 之外的架构反向决策 | ✓ PASS | 0 反向决策 |

## V — Verification（fresh evidence；7 项）

| # | Check | Status | Notes |
|---|---|---|---|
| V1 | release-wide regression 通过 | ✓ PASS | release-regression.md 10 项全部 GREEN |
| V2 | release-wide cross-feature traceability 通过 | ✓ PASS | release-traceability.md ADR-007 D1-D7 全链 + 6 先例 ADR 兼容 |
| V3 | Candidate feature closeout.md 已 accepted（含 ADR 翻 accepted） | ✓ PASS | features/001-orchestrator-extraction/closeout.md Final Confirmation done; ADR-007 → accepted |
| V4 | Candidate feature closeout.html 已生成 | ✓ PASS | 31,580 bytes |
| V5 | release-blocking hypotheses 验证 | ✓ PASS | HYP-002 + HYP-003 双 validated |
| V6 | Project metadata 同步（per ADR-006 D1 + ADR-007 D2 / 不漂移） | ✓ PASS | plugin.json v0.6.0 + agents[] / marketplace.json v0.6.0 description / SECURITY.md / CONTRIBUTING.md / .cursor/rules/ / CLAUDE.md / AGENTS.md / README × 2 / setup docs × 3 / CHANGELOG [0.6.0] 全部同步 |
| V7 | Walking-skeleton self-diff PASS（HYP-002 静态等价证明） | ✓ PASS | regression-diff.py PASS over 26 files |

## W — Warnings / Watch list（3 项）

| # | Check | Status | Notes |
|---|---|---|---|
| W1 | Cloud agent context 限制（T2.b plugin schema 真实加载 / T2.d Claude Code/OpenCode 真实 session） | ⚠ deferred-manual | release pre-flight checklist 已入档于 `verification/smoke-3-clients.md` § "接续工作"；rollback 触发条件（任一宿主 identity check FAIL → v0.6.0 rollback / hotfix 链）已明确 |
| W2 | NFR-001 wall-clock 自动化测量推迟到 v0.7+ | ⚠ pending | spec § 3 Instrumentation Debt 显式接受；本轮静态字符数对照（ratio 0.666）+ 体感作为 release-blocking gate 有效证据 |
| W3 | walking-skeleton 端到端运行时等价升级到 v0.7+ | ⚠ pending | 与 ADR-007 D3 Step 1 边界一致（不接触 leaf skill → 静态等价是充分证据）；运行时升级路径推迟到 v0.7+（Step 2-5 配套） |

## 结论

**通过**

C/D/V 全部 PASS；W 3 项 deferred-manual / pending 已显式入档（per spec § 3 Instrumentation Debt + ADR-007 D5 acceptance）。

Release `Status: ready-for-tag`。后续 `git tag v0.6.0` 由 maintainer 在执行 W1 deferred-manual checklist 全 PASS 后手动执行（hf-release 不自动 tag，per ADR-001 D1 + ADR-004 D2 立场）。

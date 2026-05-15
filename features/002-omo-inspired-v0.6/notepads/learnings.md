# Learnings — Feature 002-omo-inspired-v0.6

> 跨 task 累积，按 task 时间倒序追加。Schema 见 `skills/hf-wisdom-notebook/references/notebook-schema.md`（TASK-002 起正式承接）。

## TASK-009/010/011/012/013/014/015 — 2026-05-14T11:30Z — 7 modified-skill batched TDD pattern

- entry-id: `learn-0012`
- author: cursor cloud agent (hf-test-driven-dev TASK-009..015 batched)
- pattern: "modified-skill TDD via single-purpose verifier" —— 修改既有 skill 的 task 用一个独立 stdlib python 测试针对 *本次改动的具体 anchor* 写断言（如 momus 4 维 / Interview FSM 5 状态 / step-level recovery / category_hint 等），不重复测试整个 skill。RED 是 skill 文件未改 → 新断言失败；GREEN 是按 design diff 改 skill → 断言通过；audit-skill-anatomy.py 仍通过保证既有 anatomy 合规不退化
- applies-to: 任何"修改既有 skill 引入小特性"的 task；与"新 skill"task 的"全 anatomy 验证 verifier"区分
- evidence-anchor: 7 个 task × ~7 tests 各 = ~49 tests 一并 PASS；累计 12 测试套件 / 100 stdlib unittest in < 1s

## TASK-016/017 — 2026-05-14T12:30Z — 文档刷新统一措辞 "explicitly out-of-scope"

- entry-id: `learn-0013`
- author: cursor cloud agent (hf-test-driven-dev TASK-016+017)
- pattern: "永久删除 vs 待后续实现的 wording 区分" —— 路线图收敛时把 "v0.6+ planned X / not yet implemented" 措辞 *显式* 改为 "explicitly out-of-scope per ADR-NNN D-N (永久删除，不是 deferred)"；前者给用户错误期望"等等就有"，后者明确"项目不做这件事"
- applies-to: 后续任何 ADR 永久封禁某能力时的文档刷新
- evidence-anchor: README.md / README.zh-CN.md / docs/principles/soul.md 共 9 处 grep `out-of-scope per ADR-008 D1` 或等价中文 (4 + 4 + 1)

## TASK-003 — 2026-05-14T11:50Z — validate-wisdom-notebook.py 即立刻发现 dogfood 的真实 bug

- entry-id: `learn-0010`
- author: cursor cloud agent (hf-test-driven-dev TASK-003)
- pattern: "validator dogfood-first 反过来抓作者的真实 bug" —— validator 第一次跑就发现 features/002-.../notepads/ 内有 6 条 entry-id 真重复（learn-0001/0002 各 2 次 / dec-0001 2 次 / verify-0001/0002/0003 各 2 次），来自 TASK-002 closeout StrReplace 把已有 TASK-001 entries 重复进了新内容；validator 是 self-check，反过来抓住作者疏忽
- applies-to: 后续任何"自验工具落地后回头跑 dogfood"的场景；体现"有些 bug 写代码时看不到，跑工具才看到"
- evidence-anchor: TASK-003 RED → GREEN 之间 validator 报 6 FAIL on dogfood；REFACTOR step 内重写 3 notepad 文件去重 → 重跑 PASS（含 3 个非阻塞 WARN for 间隔 entry-id，符合 design）

## TASK-003 — 2026-05-14T11:50Z — entry-id 间隔/倒序 strict vs default 二档

- entry-id: `learn-0011`
- author: cursor cloud agent
- pattern: "validator 二档 strict / default" —— 严格性二档让"硬 bug"（duplicate / missing）总是 FAIL，但"软 bug"（gap / 倒序）默认 WARN（架构师可手动 strict）；避免引入 strict 后大量历史 notepads 一夜失败
- applies-to: 任何引入 lint / validator 的 v0.7 runtime 模块（如 record-evidence schema / progress-store schema 校验）
- evidence-anchor: validate-wisdom-notebook.py `--strict` 选项；test_non_monotonic_default_passes_with_warn + test_non_monotonic_strict_fails 双层覆盖；本 dogfood notepads 含 3 个 WARN 但 default mode PASS

## TASK-007 — 2026-05-14T02:50Z — hf-ultrawork SKILL.md + escape conditions 落地

- entry-id: `learn-0009`
- author: cursor cloud agent (hf-test-driven-dev TASK-007)
- pattern: "FR-008 强制 5-keyword enumeration"——对带"必须本地 enumerate" 类要求的 SKILL.md，verifier 用 5 个独立 regex 分别扫每一类必含项；任一缺失即失败，避免作者用"按 ADR-XXX D2 执行"一句话糊弄过 audit
- applies-to: 后续任何 SKILL.md 含"必须本地 enumerate"类 FR 时（如 v0.7 hf-runtime hashline-edit hard limits）
- evidence-anchor: `tests/test_ultrawork_skill.py::test_hard_gates_enumerates_5_noncompressibles`；regex 5 类含 Fagan / gate / closeout / approval 落盘 / 标准不清抛回；本 task SKILL.md 165 行全部 5 类 enumerated 通过

## TASK-006 — 2026-05-14T02:40Z — hf-context-mesh 三客户端模板共存约定

- entry-id: `learn-0008`
- author: cursor cloud agent (hf-test-driven-dev TASK-006)
- pattern: "三客户端共存时主版本 + 引用版本"——同目录可同时存在 OpenCode AGENTS.md / Cursor .mdc / Claude Code CLAUDE.md，但架构师只写 1 份完整 conventions（主版本），其它 2 份用 `> 见 ./AGENTS.md` 引用避免重复维护
- applies-to: vendor HF 的项目 + 任何需要跨多客户端给 AI agent 提供上下文的项目
- evidence-anchor: `skills/hf-context-mesh/references/agents-md-template.md` 末段"三客户端共存场景"

## TASK-005 — 2026-05-14T02:35Z — hf-gap-analyzer 是 author-side 而非 review 节点

- entry-id: `learn-0007`
- author: cursor cloud agent (hf-test-driven-dev TASK-005)
- pattern: "author-side self-check skill 必须显式 disclaim"——SKILL.md 必须在 frontmatter description + Hard Gates 第 1 条 + Object Boundaries + Workflow 末尾"作者吸收"四处冗余声明"不写 verdict / 不替代 Fagan review"，否则容易被误用为 review 替代品
- applies-to: 后续任何 author-side / pre-review 类 skill（如未来可能引入的 hf-design-self-check 等）
- evidence-anchor: `tests/test_gap_analyzer_skill.py::test_explicitly_not_fagan_review`；强制 SKILL.md 含"不是 Fagan review / 不写 verdict / not a Fagan review / does not produce verdict"任一表述

## TASK-002 — 2026-05-13T14:10Z — hf-wisdom-notebook SKILL.md + 2 references 落地

- entry-id: `learn-0004`
- author: cursor cloud agent
- pattern: "schema reference 末尾给 dogfood 指针"：每个 schema reference 文档（如 `notebook-schema.md` / `tasks-progress-schema.md`）必须在文末指向真实 dogfood 实例（如 `features/002-omo-inspired-v0.6/notepads/`），便于读者从抽象 schema 跳到真实使用场景
- applies-to: 后续 v0.6 / v0.7 任何引入 JSON / markdown schema 的 reference 文档
- evidence-anchor: `skills/hf-wisdom-notebook/references/notebook-schema.md` 末段 "## 例子" + `skills/hf-test-driven-dev/references/tasks-progress-schema.md` 末段 "## Canonical positive example"

## TASK-002 — 2026-05-13T14:10Z — structural-grep test pattern for SKILL.md tasks

- entry-id: `learn-0003`
- author: cursor cloud agent (hf-test-driven-dev TASK-002)
- pattern: "structural-grep test pattern for SKILL.md tasks": SKILL.md 类任务的 TDD verifier 用 stdlib `re` + `subprocess` 即可断言 (a) audit-skill-anatomy.py PASS (b) 必含段头 grep (c) 必含表格行计数 (d) wc -l + token budget 检查；不需要 markdown parser
- applies-to: TASK-005 (hf-gap-analyzer) / TASK-006 (hf-context-mesh) / TASK-007 (hf-ultrawork) 三个新 SKILL.md task 可直接复用同款 verifier 模板
- evidence-anchor: `tests/test_wisdom_notebook_skill.py` 9 tests PASS in 0.043s; SKILL.md 153 行 / 985 word ≈ 1281 token（远低 5000 上限）
- tags: skill-anatomy, structural-test, stdlib-pattern
- related-decisions: dec-0002

## TASK-001 — 2026-05-13T13:55Z — define tasks.progress.json schema

- entry-id: `learn-0001`
- author: cursor cloud agent (hf-test-driven-dev TASK-001)
- pattern: "stdlib-only mini JSON-Schema validator pattern" — 一个 ~30 行的 `_validate` 函数支持 type/required/properties/enum/pattern/items 子集即可校验本仓库所有手写 schema。不引入 jsonschema / pydantic 等第三方依赖与 audit-skill-anatomy.py / install.sh / test_install_scripts.sh 同等"stdlib only"约束一致
- applies-to: 后续任何 v0.6 / v0.7 SKILL.md 引入新 JSON 工件时（如 v0.7 record-evidence 输出 schema），可直接复用本验证器思路而非每次新引第三方库
- evidence-anchor: `tests/test_tasks_progress_schema.py` 的 `_validate` 函数；6 tests PASS in 0.001s

## TASK-001 — 2026-05-13T13:55Z — fixture-driven schema TDD on documentation tasks

- entry-id: `learn-0002`
- author: cursor cloud agent
- pattern: "schema-task TDD": 对纯 schema / reference 文档类任务，把 TDD 适配为 (positive fixture + N negative fixtures + tiny stdlib validator) 三件套；RED 阶段 schema doc 缺失 → file not found 错误即有效 RED；GREEN 阶段 schema doc 存在且 fixtures 通过 → 有效 GREEN
- applies-to: TASK-002 / TASK-005 / TASK-006 / TASK-007 / TASK-009 / TASK-010 等"主要产出是 SKILL.md / references/" 的任务，可以套同款 (skeleton check + reference rubric grep + Common Rationalizations 必含段) 三件套验证
- evidence-anchor: `verification/test-design-task-001.md` 的"待验证行为"4 项 + 实际 6 tests

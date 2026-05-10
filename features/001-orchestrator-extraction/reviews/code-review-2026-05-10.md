# Code Review Record — 001-orchestrator-extraction (T1–T9)

- 评审者: 独立 reviewer subagent (hf-code-review)
- 评审对象: 提交 `d93507d` (`impl: T1-T9 hf-test-driven-dev (orchestrator extraction Step 1)`)
- 分支: `cursor/orchestrator-extraction-impl-e404`
- 上游 spec: `features/001-orchestrator-extraction/spec.md`（已批准）
- 上游 design: `features/001-orchestrator-extraction/design.md`（已批准）
- 上游 ADR: `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md`
- 上游 review handoff: 父会话指定（`hf-test-review` 此前已通过；commit message 携带完整 Refactor Note）
- Author/Reviewer 分离: 是（reviewer ≠ implementer of T1–T9；本 record 由独立 subagent 撰写）

## 0. 输入证据基线 (Step 1)

| 输入类 | 路径 / 锚点 | 状态 |
|---|---|---|
| 实现交接块 + Refactor Note | commit `d93507d` 详细 message（Hat Discipline / SUT Form / Pattern Actual / In-task Cleanups / Boy Scout / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence 全部齐全）| ✓ |
| 代码变更 | 40 files：`agents/hf-orchestrator.md` + 9 references + `CLAUDE.md` + `AGENTS.md` + 2 stubs + 9 reference stubs + `.cursor/rules/harness-flow.mdc` + `.claude-plugin/plugin.json` + 2 Python 脚本 + 3 verification + docs/CHANGELOG/SECURITY/CONTRIBUTING/READMEs | ✓ |
| Spec / Design / ADR | spec FR-001..007 + NFR-001..005；design § 9 D-X 决策；ADR-007 D1–D7 | ✓ |
| Verification（fresh evidence）| `verification/{regression-2026-05-10,smoke-3-clients,load-timing-3-clients}.md` | ✓ |
| Reviews 链 | spec / design / tasks reviews 全部 `通过`；approvals 三件齐全 | ✓ |
| Skill 项目级约定 | `.cursor/rules/harness-flow.mdc` / `CLAUDE.md` / `AGENTS.md` | ✓ |

## 1.5 Precheck 结论

- 稳定实现交接块: **存在**（commit message 含完整 Refactor Note，9 个字段无缺失）
- 核心代码范围可定位: **是**（40 个文件全部在 spec § 6.1 In-scope 列表内）
- Refactor Note 中 Escalation Triggers: **None**（与 Next Action `hf-code-review` 一致；无 route/stage/escalation 边界冲突）
- Route/stage/profile 与上游 evidence: **一致**（profile=full；stage=hf-code-review；上游 hf-test-review 已通过）

→ Precheck 通过，进入正式审查。

## 2. 7 维评分

| 维度 | 评分 | 说明 |
|---|---|---|
| **CR1 正确性** | 9/10 | 3/3 测试用例通过（self_consistency / mutation_outside_allowlist / allowlist_timestamp）；orchestrator persona 主文件 14,067 bytes < 23,245 ceiling（NFR-002 通过 × 0.666）；11 个 deprecated stub 全部物理存在并满足 ≤ 30 / ≤ 10 行约束；3 宿主 always-on stub 引用一致；JSON 解析通过且 agents[] 结构合理 |
| **CR2 设计一致性** | 9/10 | 14 个 design § 11 模块全部到位；D-Layout / D-Mig / D-Stub / D-Stub-Marker / D-Host-{Cursor,CC,OC} / D-Identity / D-NFR1-Schema / D-RegrLoc / D-RegrImpl 全部按设计落地；ADR-007 D1 三层架构 invariant 守住（Layer 3 在 `agents/`；Layer 1/2 此轮未动）；C-006 ≤ 30 行 deprecated alias 约束满足 |
| **CR3 状态/错误/安全** | 8/10 | `regression-diff.py` argparse 输入校验 + `--baseline-dir` / `--candidate-dir` required；exit code 语义明确（0/1/2）；缺失 expected files 时 stderr 报错并 return 1；无静默失败；无安全敏感面（stdlib-only / 无网络 / 无敏感数据）；轻微耦合见 F2 |
| **CR4 可读性与可维护性** | 8/10 | 类型注解齐全（`Path` / `list[Path]` / `Iterable[str] | None`）；命名清晰（`collect_files` / `line_is_allowed` / `diff_two_files` / `run` / `main`）；docstring 描述 allowlist 来源（design D-RegrImpl）+ exit codes + Owners；常量提取为 `ALLOWLIST_PATTERNS` / `EXPECTED_FILES`；无死代码；轻微 import-style 见 F1 |
| **CR5 范围守卫** | 10/10 | 严格停在 spec § 6.1 In-scope；§ 6.2 12 项 Out-of-scope 全部守住（leaf skill 文件未被修改；旧 skill 文件物理保留；closeout pack schema 不变；audit-skill-anatomy.py 不变；不新增 hf-* skill；7 条 slash 命令不变） |
| **CR6 下游追溯就绪度** | 10/10 | 实现交接块（commit message）字段齐全；3 份 verification record 落盘；reviews/ + approvals/ 全链可读；可直接支持 `hf-traceability-review` 做 spec → design → tasks → impl 全链追溯 |
| **CR7 架构健康与重构纪律** | 9/10（主维度）| 详见下表 |

CR7 子维度分项：

| 子维度 | 评分 | 说明 |
|---|---|---|
| **CR7.1 Two Hats Hygiene** | 9/10 | Refactor Note 显式声明 "pure Changer hat throughout"（无既有代码可 refactor）；RED = file-existence pre-checks；GREEN = 直接落 markdown / Python 脚本；REFACTOR = regression-diff self-test loop；步骤边界清晰；单 commit 打包合理（commit message 已显式说明文档为主非代码改动；无 hat-mixing 风险） |
| **CR7.2 Refactor Note 完整性** | 10/10 | 9 字段全部齐全：Hat Discipline / SUT Form Declared / Pattern Actual / SUT Form Drift / In-task Cleanups (Fowler vocabulary) / Boy Scout Touches / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence；Documented Debt 显式枚举 NFR-001 wall-clock 自动化 + Claude Code/OpenCode identity-gate manual verification；Escalation Triggers 显式标 None |
| **CR7.3 Architectural Conformance** | 10/10 | ADR-007 D1 三层架构 invariant 守住（agent persona 物理位置在 `agents/` 而非 `skills/`；不进 `audit-skill-anatomy.py` 扫描）；ADR-006 D1 4 类子目录约定不被破坏（agent persona 不在 skill 子目录范围内）；旧 skill 物理保留为 deprecated alias（NFR-003 兼容性）；接口契约（reviewer return contract / dispatch protocol）通过 git mv 1:1 迁移到 `agents/references/`，逐字节等价（D-Mig）|
| **CR7.4 Architectural Smells Detection** | 9/10 | 触碰范围内无 god-class / cyclic-dep / layering-violation / leaky-abstraction（脚本 5 函数扁平 + 1 main；persona 文件单文档；deprecated alias stubs 单文档）；Refactor Note 显式 `In-task Cleanups: 0` + `Boy Scout Touches: 0`，与触碰范围一致；无 over-abstraction（regression-diff.py SUT Form=naive；无未声明的新抽象层）|
| **CR7.5 Boy Scout Compliance** | 10/10 | 触碰范围 clean code 健康度未退化；orchestrator persona 主文件结构清晰（14 章按 design § 10.3 顺序）；2 处 documentation drift（review-record-template baseline KB number / tasks.md T4 P1→P0 stale label）已在上游 design / tasks 分支吸收，本次 implement commit 不携带遗留 |

任一关键维度均 ≥ 6；CR7 主维度 ≥ 8；CR7 全部子维度 ≥ 8。具备 `通过` 资格。

## 3. 特别关注项核对（父会话指定）

| 关注项 | 结果 |
|---|---|
| 1. regression-diff.py 代码质量（stdlib-only / argparse / 错误处理 / naming / no dead code / no unexplained magic numbers / type hints） | ✅ 全部满足；唯一 import-style 偏好见 F1 |
| 2. test_regression_diff.py 覆盖 3 case + 任一失败非零退出 | ✅ 3/3 case 命中；`main()` failed 列表非空 → return 1；`raise SystemExit(main())` 传递 |
| 3. Deprecated alias stubs ≤ 30 行 (SKILL.md) / ≤ 10 行 (references) | ✅ using-hf-workflow=21 行；hf-workflow-router=21 行；9 references 各 9 行；HTML marker 全部命中 |
| 4. NFR-002 字符数预算 (× 1.10 of 21,132 = 23,245) | ✅ 14,067 bytes ≪ 23,245；ratio = 0.666 |
| 5. plugin.json JSON 合法 + agents[] 结构合理 | ✅ `python3 -m json.tool` 通过；agents[0] = {name, description, source, alwaysActive}；version 0.6.0 |
| 6. Clean Arch / SOLID 不适用 | ✅ 已在 CR7.3 / CR7.4 适配为 ADR-007 D1 三层 invariant + 模块边界 conformance；脚本 SUT Form=naive 无类层级 |
| 7. Markdown 内部一致性（operating loop 自洽 + skill catalog 24 hf-* + 1 entry deprecated）| ✅ Operating Loop 1–10（含 4A / 5A）章节互相引用一致；Skill Catalog = 12 doer + 11 reviewer/gate + 3 deprecated table 行（using-hf-workflow + hf-workflow-router + references/*.md）= 23 active hf-* + 1 deprecated hf-* (`hf-workflow-router`) + 1 entry shell deprecated (`using-hf-workflow`) → 24 hf-* + 1 entry，与 § Skill Catalog 标题描述一致 |
| 8. 跨工件 v0.6.0 / `agents/hf-orchestrator.md` / deprecated alias / v0.7.0+ deletion 一致性 | ✅ orchestrator 主文件 5 处 `v0.7.0` 命中；2 SKILL stub + 9 reference stubs 各 1 处；`CLAUDE.md` / `AGENTS.md` / `.cursor/rules/harness-flow.mdc` 各 1 处；ADR-007 D3 Step 6 引用全部对齐 |

## 4. 发现项

非阻塞 minor advisory（共 2 项；均 LLM-FIXABLE；不影响 verdict）：

- **F1 [minor][LLM-FIXABLE][CR4]** `features/001-orchestrator-extraction/scripts/regression-diff.py:86` 在 `diff_two_files` 函数内做局部 `import difflib`，附 comment "local import keeps top imports clean"。`difflib` 是该模块的核心依赖（diff 实现），按 Python 惯例应放在文件顶部 imports（PEP 8 § Imports）。当前形式不影响功能（脚本 stdlib-only / 单次执行；reload 性能非考量），但读者扫顶部 imports 时会漏掉 `difflib`，轻微影响可读性。建议把 `import difflib` 提到文件顶部 imports 区与 `argparse` / `re` / `sys` / `pathlib` 并列。
- **F2 [minor][LLM-FIXABLE][CR3]** `features/001-orchestrator-extraction/scripts/regression-diff.py:64` `collect_files` 在 root 不是目录时直接 `raise SystemExit(2)`。把 process-exit 语义耦合进 library-style 函数，使该函数在测试 / 复用语境下不便单元化（虽然当前 `test_regression_diff.py` 未触达此分支）。建议把异常类型改为 `FileNotFoundError(f"...")` 或 `NotADirectoryError`，由 `main()` 捕获后翻译为 `return 2`（与现有 `return 1` 错误路径风格一致）。当前实现一次性脚本可接受；列入下一轮 hardening 备忘。

无 important / critical finding。无 USER-INPUT finding（产品 / 业务决策无新增）。

## 5. 代码风险与下游追溯提示

- `regression-diff.py` 做的是行级 unified_diff + allowlist regex 过滤（而非 design D-RegrImpl "schema-by-schema" 字面意义上按 H2 段切分解析）。这是合理工程化简化（allowlist 已覆盖 design 列出的全部 4 类容许差异源），但 `hf-traceability-review` 阶段如果发现 closeout pack 引入了新的 schema-level 字段（例如未来 ADR-008+ 新增 closeout 段），需要同步检查 `EXPECTED_FILES` 与 `ALLOWLIST_PATTERNS` 是否需要扩增。
- v0.6.0 兼容期内 `hf-orchestrator.md` § 6 仍允许消费 leaf skill 的 `Next Action` 字段（D-Disp 双轨设计）。`hf-traceability-review` 评 v0.6.0 release 时应确认 ADR-007 D1 生效阶段（v0.6.0 = architectural commitment / v0.7.0+ = runtime enforcement）已显式记录在 ADR-007 D1，避免后续 increment 误以为 v0.6.0 已完成 runtime enforcement。
- HYP-002 / HYP-003 release-blocking fresh evidence（regression-2026-05-10.md / smoke-3-clients.md / load-timing-3-clients.md）由父会话已落盘；下游 `hf-regression-gate` / `hf-completion-gate` 需要消费这 3 份记录的 PASS / ratio≤1.20 / 4-of-4 reviewer-separation 标识。

## 6. 结论与下一步

- **Conclusion**: `通过`
- **Next Action Or Recommended Skill**: `hf-traceability-review`
- **Needs Human Confirmation**: `false`
- **Reroute Via Router**: `false`
- **Record Path**: `features/001-orchestrator-extraction/reviews/code-review-2026-05-10.md`

## 7. 结构化返回

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-traceability-review",
  "record_path": "features/001-orchestrator-extraction/reviews/code-review-2026-05-10.md",
  "key_findings": [
    "[minor][LLM-FIXABLE][CR4] regression-diff.py:86 局部 import difflib，建议按 PEP 8 提到文件顶部 imports 区",
    "[minor][LLM-FIXABLE][CR3] regression-diff.py:64 collect_files 直接 raise SystemExit(2) 耦合 process-exit；建议改为 FileNotFoundError 由 main() 翻译为 exit code"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR4",
      "summary": "regression-diff.py:86 局部 import difflib，建议按 PEP 8 提到文件顶部 imports 区"
    },
    {
      "severity": "minor",
      "classification": "LLM-FIXABLE",
      "rule_id": "CR3",
      "summary": "regression-diff.py:64 collect_files 直接 raise SystemExit(2) 耦合 process-exit；建议改为 FileNotFoundError 由 main() 翻译为 exit code"
    }
  ]
}
```

## 8. Verification 自检清单

- [x] review record 已落盘到 `features/001-orchestrator-extraction/reviews/code-review-2026-05-10.md`
- [x] 给出明确结论（`通过`）、findings（2 minor advisory）、code risks（3 项 traceability hint）、唯一下一步（`hf-traceability-review`）
- [x] findings 已标明 severity / classification / rule_id（CR3 / CR4）
- [x] 结构化摘要含 record_path 和 next_action_or_recommended_skill
- [x] 已对实现交接块的 Refactor Note 做 CR7 评审（5 子维度分项落盘）
- [x] CR7 未触发 escalation-bypass（CA8）；未实质修改 ADR / 模块边界 / 接口契约（仅物理迁移 + 单源化，逐字节等价）
- [x] precheck 通过；无 workflow blocker；`reroute_via_router=false`
- [x] Author/Reviewer 分离已声明（reviewer ≠ implementer of T1–T9）

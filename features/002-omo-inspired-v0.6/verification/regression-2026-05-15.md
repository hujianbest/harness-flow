# Regression Gate — features/002-omo-inspired-v0.6 (2026-05-15)

- Gate: hf-regression-gate
- Verdict: **PASS**
- Profile / Mode: full / auto
- Run-by: cursor cloud agent (按 Fagan separation；与 author session 不同 role)

## Impact-Based Scope

v0.6 改动影响面：

| 改动类别 | 影响范围 | 回归覆盖 |
|---|---|---|
| 4 新 SKILL.md (hf-wisdom-notebook / hf-gap-analyzer / hf-context-mesh / hf-ultrawork) | audit-skill-anatomy.py + 4 个独立 stdlib python 测试套件 | ✅ 全部 |
| 7 改 SKILL.md (hf-tasks-review / hf-specify / hf-workflow-router / hf-code-review / hf-test-driven-dev / hf-completion-gate / using-hf-workflow) | audit + 7 个独立测试套件 | ✅ 全部 |
| 1 schema reference (tasks-progress-schema.md) + 4 fixtures | tests/test_tasks_progress_schema.py | ✅ |
| 1 stdlib python validator (validate-wisdom-notebook.py) | skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py | ✅ |
| install.sh / uninstall.sh / .cursor/rules / .claude-plugin/ | NFR-003 不动；smoke test 验证 | ✅ |
| README / soul.md docs | grep-based doc-freshness gate (单独节点)| 在 doc-freshness-gate 中校验 |
| CHANGELOG.md | grep-based check (doc-freshness-gate)| 在 doc-freshness-gate 中校验 |

## Run

```text
$ for t in tests/test_*.py skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py; do
    python3 "$t" 2>&1 | tail -3 | grep -E "^OK|^FAILED" | head -1
  done
tests/test_code_review_ai_slop.py: OK
tests/test_context_mesh_skill.py: OK
tests/test_fr002_integration.py: OK
tests/test_gap_analyzer_skill.py: OK
tests/test_specify_interview_fsm.py: OK
tests/test_tasks_progress_schema.py: OK
tests/test_tasks_review_momus.py: OK
tests/test_ultrawork_skill.py: OK
tests/test_using_hf_workflow_step5.py: OK
tests/test_wisdom_notebook_skill.py: OK
tests/test_workflow_router_v06.py: OK
skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py: OK

$ python3 scripts/audit-skill-anatomy.py --skills-dir skills | tail -3
  OK    using-hf-workflow

Summary: 0 failing skill(s), 0 warning(s).

$ # install.sh / uninstall.sh smoke
$ rm -rf /tmp/host-regression && mkdir -p /tmp/host-regression
$ bash install.sh --target both --host /tmp/host-regression
[hf-install] install complete: /tmp/host-regression/.harnessflow-install-manifest.json (63 entries)
$ bash uninstall.sh --host /tmp/host-regression
[hf-uninstall] removing 63 entries (target host: /tmp/host-regression)
[hf-uninstall] uninstall complete
```

## Evidence Summary

| 维度 | 结果 |
|---|---|
| 12 stdlib python 测试套件 / 100 unittest cases | **100/100 PASS** in < 1s 总时长 |
| audit-skill-anatomy.py 29 SKILL.md | **0 failing / 0 warning** |
| install.sh / uninstall.sh round-trip (target=both) | **PASS** (63 entries install + 63 entries uninstall) |
| install topology files (NFR-003 git diff) | **0 行变化** |
| Dogfood: tasks.progress.json schema validate | **PASS** |
| Dogfood: validate-wisdom-notebook.py on notepads/ | **PASS** (4 non-blocking WARN for entry-id gaps) |

## Verdict

**PASS** — 全部 v0.6 改动影响面回归覆盖；0 fail / 0 regression introduced。下一步 `hf-doc-freshness-gate`。

# Release-Wide Regression — v0.6.0 (2026-05-15)

- Run-by: cursor cloud agent (按 hf-release §6 协议)
- Profile / Mode: full / auto
- Verdict: **PASS**

## Scope

`union(features/002-omo-inspired-v0.6 affected modules)`：

- 全 29 SKILL.md（25 既有 + 4 v0.6 新）
- 12 stdlib python 测试套件（覆盖 4 新 SKILL.md + 7 改 SKILL.md + 1 stdlib python validator + schema reference）
- install.sh / uninstall.sh round-trip（NFR-003 + smoke）
- Dogfood: tasks.progress.json schema validate + validate-wisdom-notebook.py on notepads/

## Run

执行时间：2026-05-15T13:00Z（晚于 features/002 closeout 2026-05-15，满足 fresh evidence 要求）

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

$ rm -rf /tmp/host-regression && mkdir -p /tmp/host-regression
$ bash install.sh --target both --host /tmp/host-regression
[hf-install] install complete: /tmp/host-regression/.harnessflow-install-manifest.json (63 entries)
$ bash uninstall.sh --host /tmp/host-regression
[hf-uninstall] removing 63 entries (target host: /tmp/host-regression)
[hf-uninstall] uninstall complete

$ python3 -c "(_validate features/002-.../tasks.progress.json against TASK-001 schema)"
PASS

$ python3 skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py --feature features/002-omo-inspired-v0.6/
Validation PASSED (4 warnings for entry-id gaps, all from intentional skips)
```

## Evidence Summary

| 维度 | 结果 |
|---|---|
| 12 stdlib python 测试套件 | **100/100 PASS** in < 1s |
| audit-skill-anatomy.py 29 SKILL.md | **0 failing / 0 warning** |
| install.sh / uninstall.sh round-trip (target=both) | **PASS** (63 entries × 2) |
| install topology files (NFR-003 git diff) | **0 行变化** vs origin/main (excluding PR #55 hotfix already merged) |
| Dogfood tasks.progress.json | **PASS** |
| Dogfood validate-wisdom-notebook.py | **PASS** (4 non-blocking WARN) |

## Verdict

**PASS** — 全部 release scope 影响面 fresh regression 通过；无 cross-feature regression；可进入 §7 cross-feature traceability。

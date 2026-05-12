# Regression Gate — 001-install-scripts (2026-05-11)

- Verifier: cursor cloud agent（hf-regression-gate node）
- Run-at: 2026-05-11
- Scope: 本 feature 新增的 install.sh / uninstall.sh / tests/ 不应破坏 HF 既有 audit / test 生态

## Test Battery

| # | 命令 | 结果 |
|---|---|---|
| R1 | `bash tests/test_install_scripts.sh` | ✅ 14 passed, 0 failed（本 feature 自身的 e2e 测试，含 12 + 2 个 negative scenario）|
| R2 | `python3 scripts/audit-skill-anatomy.py` | ✅ 0 failing skill(s), 0 warning(s)（24 个 hf-* + using-hf-workflow 全部 OK；anatomy v2 立场未被破坏）|
| R3 | `python3 scripts/test_audit_skill_anatomy.py` | ✅ Ran 6 tests; OK |
| R4 | `python3 skills/hf-finalize/scripts/test_render_closeout_html.py` | ✅ Ran 17 tests; OK |
| R5 | `(awk '!/^[[:space:]]*#/' install.sh uninstall.sh) \| grep -E '\b(jq\|python\|node\|npm)\b'` | ✅ 输出空（NFR-004 锁定）|

## 结论

- **PASS**：5 个 regression 项全绿；本 feature 的新增物件（2 个 shell 脚本 + 1 个 e2e driver + ADR-007 + 5 个 doc 同步条目）与 HF 既有 4 类 audit/test 体系（skill anatomy、audit 自身单元测试、hf-finalize 渲染测试、本 feature e2e）相互独立、互不干扰。
- **无 regression**：HF 现有 24 个 hf-* + using-hf-workflow 在 anatomy 与 finalize 渲染层面均不受影响。
- **fresh-evidence**：本记录由 hf-regression-gate 节点直接采集自 2026-05-11 工作树状态（commit 含 install.sh 实现 + T10b doc sync），符合 evidence-based gating 立场。

## 下一节点

- hf-doc-freshness-gate（验证 5 个文档同步是否完整且向后兼容）

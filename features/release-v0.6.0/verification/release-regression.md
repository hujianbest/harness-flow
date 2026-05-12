# Release-wide Regression — v0.6.0

- Scope: `union(候选 feature affected modules)` = install scripts (`install.sh` + `uninstall.sh` + `tests/test_install_scripts.sh`) + 5 个 doc 文件 + HF skill anatomy（验证 install scripts 不破坏既有 skill 体系）
- Profile: full
- Executed at: **2026-05-12T13:22:54Z**（晚于唯一候选 feature `001-install-scripts` 最晚 closeout 时间 `2026-05-11`，满足 fresh-evidence 协议）
- Executor: cursor cloud agent（hf-release §6 节点；自给自足，不依赖 router）

## Test Battery（5 类入口；按 ADR-008 D6 决策范围）

| # | 命令 | Exit Code | 结果 | 锚点 |
|---|---|---|---|---|
| R1 | `bash tests/test_install_scripts.sh` | 0 | ✅ 14 passed, 0 failed | features/001-install-scripts/spec.md FR-001..FR-008 / NFR-001..NFR-004 / ASM-001 / HYP-002 Blocking + NFR-002 |
| R2 | `python3 scripts/audit-skill-anatomy.py` | 0 | ✅ 0 failing skill(s), 0 warning(s)（24 个 hf-* + using-hf-workflow 全部 OK；ADR-006 D1 anatomy v2 立场不动）| ADR-006 D1 |
| R3 | `python3 scripts/test_audit_skill_anatomy.py` | 0 | ✅ Ran 6 tests; OK | audit 自身回归基线 |
| R4 | `python3 skills/hf-finalize/scripts/test_render_closeout_html.py` | 0 | ✅ Ran 17 tests; OK | ADR-005 D1 / D2（v0.5.0 引入的 closeout HTML 渲染脚本基线）|
| R5 | `(awk '!/^[[:space:]]*#/' install.sh uninstall.sh) \| grep -E '\b(jq\|python\|node\|npm)\b'` | 1（无输出）| ✅ no forbidden tokens | features/001-install-scripts/spec.md NFR-004 |

## 结论

**PASS**：5/5 项绿。本版**新增** install scripts 工件与 HF 既有 4 类 audit/test 体系（skill anatomy / audit 自身单元测试 / hf-finalize 渲染单元测试 / install scripts e2e）相互独立、互不干扰。

- 新增工件：`install.sh` + `uninstall.sh` + `tests/test_install_scripts.sh`
- 既有 24 个 hf-* + using-hf-workflow 在 anatomy v2 与 hf-finalize 渲染层面均不受影响
- NFR-004（不引入 jq / python / node / npm 运行时依赖）锁定持续生效

## Fresh-Evidence 锚点

- 所有 5 类命令于 2026-05-12T13:22:54Z 在 release base branch（`cursor/install-scripts-c90e`，含 install scripts 实现 + T10b doc sync + ADR-007 + ADR-008 起草）的最新 commit 上执行
- 执行点晚于唯一候选 feature `features/001-install-scripts/closeout.md` 的 `Closed: 2026-05-11`（间隔 ≥ 1 天）
- 不允许把任何单 feature 历史 regression 记录拼贴当作 release-wide 通过；上述 5 类全部为本次 hf-release §6 节点直接采集

## 失败时的 reroute（占位）

无失败项。如未来 release-wide regression fail：

- R1 fail → 回 `features/001-install-scripts/` 的 `hf-test-driven-dev` 修复对应 scenario
- R2 / R3 fail → 回 `hf-test-driven-dev` 修复对应 hf-* skill anatomy 或 audit
- R4 fail → 回 `features/release-v0.5.0/` 或 `features/release-v0.5.1/` 的 hf-finalize 渲染脚本修复
- R5 fail → 回 `features/001-install-scripts/` 的 `hf-test-driven-dev` 移除 install/uninstall 中的 jq/python/node/npm 引用

## 与候选 feature 历史 regression 的关系

`features/001-install-scripts/verification/regression-2026-05-11.md` 是**单 feature** regression（impact-based，scope 仅本 feature）；本 release-wide regression 是**版本级**（scope 是候选 feature affected modules 的 union）。两者结论一致（5/5 绿）但**互不替代**——本记录是 release tier 的独立 fresh evidence，不是单 feature 历史记录的拼贴。

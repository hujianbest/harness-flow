# Release-wide Regression — v0.5.0

## Metadata

- Verification Type: release-wide regression
- Scope: HarnessFlow v0.5.0（hf-finalize HTML companion 引入 + 新脚本 + 配套版本号 / 文档同步）
- Date: 2026-05-09
- Record Path: `features/release-v0.5.0/verification/release-regression.md`
- Worktree Path / Worktree Branch: `cursor/hf-finalize-html-closeout-report-eea2`（in-place）
- Re-run timestamp (post ADR-005 D10 skill anatomy migration): `2026-05-09T18:59:34Z` —— 验证脚本搬到 `skills/hf-finalize/scripts/` 后所有 release-wide regression 检查仍 PASS

## Upstream Evidence Consumed

- ADR: `docs/decisions/ADR-005-release-scope-v0.5.0.md`（D2 渲染脚本仅 stdlib + D3 反 slop 自检 + D6 minor bump + D8 不刷新 demo）
- 候选 feature scope: 单 feature（hf-finalize 输出契约扩展 + `skills/hf-finalize/scripts/render-closeout-html.py` 新增；脚本物理位置按 ADR-005 D10 引入的 skill-owned 工具约定），无独立 `features/<feature-id>/closeout.md` 候选（本版以 hf-release dogfood 形态打包 engineering-tier 改进，见 release-pack.md `Limits / Open Notes` 段）

## Claim Being Verified

Claim: v0.5.0 引入的所有变更（新脚本 + hf-finalize SKILL.md step 6A + 模板段追加 + 元数据 / 文档同步）**不**破坏：

- HF skill 集合的结构合规性（`audit-skill-anatomy.py` 全 PASS）
- 既有 audit 单元测试（`test_audit_skill_anatomy.py`）
- 新增渲染脚本的所有单元测试（`test_render_closeout_html.py`）
- 既有项目级 JSON 工件的有效性（plugin.json / marketplace.json / 各 evals.json / test-prompts.json）
- 真实 closeout pack（walking-skeleton）的渲染结果（脚本针对真实工件可用）

由于本 release 是 greenfield engineering 改进（渲染脚本是首次出现），release-wide regression 在事实上等价于：当前 HEAD 上一次性把所有项目级 hygiene 检查 + 新工具的单元测试 + 真实工件可用性验证全部跑通。

## Verification Scope

- Profile: `lightweight`（HF 仓库 v0.4.0 起即声明 lightweight tier；ADR-001 D11 + ADR-002 D11 立场延续）
- Included Coverage:
  - `scripts/audit-skill-anatomy.py`（24 `hf-*` + `using-hf-workflow` 全部结构合规）
  - `scripts/test_audit_skill_anatomy.py`（6 个单元测试）
  - `skills/hf-finalize/scripts/test_render_closeout_html.py`（17 个单元测试覆盖 markdown 解析 / vitest+jest+pytest 日志 / coverage.json + 内联 KV / 完整与 blocked 渲染 / sub-bullet 不溢出 / Status Fields Synced 子项渲染 / HTML 转义 / CLI exit code）
  - JSON validity：plugin.json / marketplace.json / hf-finalize/test-prompts.json / hf-finalize/evals.json / hf-release/evals.json
  - 真实样例渲染：`python3 skills/hf-finalize/scripts/render-closeout-html.py examples/writeonce/features/001-walking-skeleton`
- Uncovered Areas:
  - `examples/writeonce/` 自身的 vitest 套件（按 ADR-005 D8 + ADR-001 D9 立场，本 release 不修订 demo，因此 demo 测试套件不在 v0.5.0 release-wide regression scope）
  - 真实 client install smoke（按 ADR-002 D11 / ADR-003 D7 / ADR-004 立场，未升级为 hard gate）

## Commands And Results

```text
# 1. audit-skill-anatomy.py
python3 scripts/audit-skill-anatomy.py
```

- Exit Code: `0`
- Summary: `0 failing skill(s), 0 warning(s)`（24 `hf-*` + `using-hf-workflow` 全部 OK）

```text
# 2. test_audit_skill_anatomy.py
python3 scripts/test_audit_skill_anatomy.py
```

- Exit Code: `0`
- Summary: `Ran 6 tests in 0.019s, OK`

```text
# 3. test_render_closeout_html.py
python3 skills/hf-finalize/scripts/test_render_closeout_html.py
```

- Exit Code: `0`
- Summary: `Ran 17 tests in 0.012s, OK`

```text
# 4. JSON validity
python3 -m json.tool .claude-plugin/plugin.json > /dev/null
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
python3 -m json.tool skills/hf-finalize/test-prompts.json > /dev/null
python3 -m json.tool skills/hf-finalize/evals/evals.json > /dev/null
python3 -m json.tool skills/hf-release/evals/evals.json > /dev/null
```

- All Exit Codes: `0`
- Summary: 5 个 JSON 工件全部有效（含本版 `plugin.json` 升级到 0.5.0 后的解析）

```text
# 5. real sample render
python3 skills/hf-finalize/scripts/render-closeout-html.py examples/writeonce/features/001-walking-skeleton
```

- Exit Code: `0`
- Summary: `wrote examples/writeonce/features/001-walking-skeleton/closeout.html`
- Notable Output: 渲染结果对真实 walking-skeleton closeout pack 可用（v3 重设计后版本，与 v0.4.0 时期版本相比仅时间戳行差异，证明渲染 idempotent）

## Freshness Anchor

- Why this evidence is for the latest relevant code state: 5 项命令在同一次 shell 调用中按顺序执行；初次时间戳 `2026-05-09T17:34:59Z`（脚本在仓库根 `scripts/` 时）+ ADR-005 D10 迁移后 re-run 时间戳 `2026-05-09T18:59:34Z`（脚本已在 `skills/hf-finalize/scripts/`），两次执行全部检查 PASS；两次执行点都晚于本次 release 所有 hf-finalize SKILL.md / 模板 / 脚本 / 测试 commit
- Output Log / Terminal / Artifact: 终端输出已抓取（hf-release dogfood 不要求保留独立 log 文件，hf-release SKILL.md §6 只要求记录命令 / 时间戳 / 通过结论）

## Conclusion

- Conclusion: **PASS**
- Next Action Or Recommended Skill: 进入 `hf-release` §7 cross-feature traceability 摘要 → §8 pre-release engineering checklist

## Scope / Remaining Work Notes

- Remaining Task Decision: 5 项 ops/release skill + 4 家剩余客户端 + 3 personas 按 ADR-005 D5 / D7 显式延后到 v0.6+；不阻塞本 release
- Notes:
  - 本 release-wide regression 的执行成本极低（< 1 秒），与 v0.4.0 release 一致；这是 HF 仓库自身仍是 "Markdown skill pack + 少量 Python 工具脚本" 形态的直接结果
  - 后续 release 若引入更复杂的工具链（如真正的渲染服务 / SSG / 类型检查），release-wide regression 入口需扩展，本节点不预先承诺

## Related Artifacts

- `docs/decisions/ADR-005-release-scope-v0.5.0.md`（scope 决策）
- `features/release-v0.5.0/release-pack.md`（主 pack）
- `features/release-v0.5.0/verification/release-traceability.md`（cross-feature traceability 摘要）
- `features/release-v0.5.0/verification/pre-release-checklist.md`（pre-release engineering checklist 勾选状态）

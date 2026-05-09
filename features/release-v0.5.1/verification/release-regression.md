# Release-wide Regression — v0.5.1

## Metadata

- Verification Type: release-wide regression
- Scope: HarnessFlow v0.5.1（HF skill anatomy v2 + hf-finalize 脚本物理迁移 vendoring fix）
- Date: 2026-05-09
- Record Path: `features/release-v0.5.1/verification/release-regression.md`
- Worktree Path / Worktree Branch: `cursor/v0.5.1-skill-anatomy-vendoring-fix-eea2`（in-place）
- Re-run timestamp: `2026-05-09T18:59:34Z`（D2 物理迁移完成后；脚本现位于 `skills/hf-finalize/scripts/`）

## Upstream Evidence Consumed

- ADR: `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`（D1 anatomy v2 + D2 物理迁移 + D3 patch bump + D4 hf-release dogfood 第三次）
- 候选 feature scope: 单 feature（anatomy 扩展 + 脚本物理迁移；与 v0.5.0 hf-release dogfood 形态同源）
- v0.5.0 baseline: `features/release-v0.5.0/`（不修订；本版只在其上加 patch）

## Claim Being Verified

Claim: v0.5.1 的物理迁移（脚本从 `scripts/` 搬到 `skills/hf-finalize/scripts/`）+ 配套 SKILL.md / template / audit docstring 同步 + 顶层文档版本号同步**不**破坏：

- HF skill 集合的结构合规性（`audit-skill-anatomy.py` 全 PASS；新加的 `skills/hf-finalize/scripts/` 子目录对 audit 完全透明）
- 既有 audit 单元测试（`test_audit_skill_anatomy.py`）
- 渲染脚本的全部单元测试（`skills/hf-finalize/scripts/test_render_closeout_html.py`）
- 既有项目级 JSON 工件的有效性（plugin.json / marketplace.json / 各 evals.json / test-prompts.json）
- 真实 closeout pack（walking-skeleton）的渲染结果（脚本针对真实工件可用；从新位置调用脚本输出语义完全不变）

## Verification Scope

- Profile: `lightweight`（继承 v0.5.0 / v0.4.0 立场）
- Included Coverage:
  - `scripts/audit-skill-anatomy.py`（24 `hf-*` + `using-hf-workflow` 全部结构合规）
  - `scripts/test_audit_skill_anatomy.py`（6 个单元测试）
  - `skills/hf-finalize/scripts/test_render_closeout_html.py`（**新位置**，17 个单元测试）
  - JSON validity：plugin.json / marketplace.json / hf-finalize/test-prompts.json / hf-finalize/evals.json / hf-release/evals.json
  - 真实样例渲染（**新位置脚本**）：`python3 skills/hf-finalize/scripts/render-closeout-html.py examples/writeonce/features/001-walking-skeleton`
- Uncovered Areas:
  - `examples/writeonce/` 自身的 vitest 套件（按 ADR-005 D8 / ADR-006 D2 立场，本 release 不修订 demo 事实层；只更新 demo 内的 closeout.html 渲染产物，footer 1 行路径差异）

## Commands And Results

```text
# 1. audit-skill-anatomy.py
python3 scripts/audit-skill-anatomy.py
```

- Exit Code: `0`
- Summary: `0 failing skill(s), 0 warning(s)`（24 `hf-*` + `using-hf-workflow` 全部 OK；新加的 `skills/hf-finalize/scripts/` 子目录对 audit 透明，行为不变）

```text
# 2. test_audit_skill_anatomy.py
python3 scripts/test_audit_skill_anatomy.py
```

- Exit Code: `0`
- Summary: `Ran 6 tests in 0.007s, OK`

```text
# 3. test_render_closeout_html.py（新位置！）
python3 skills/hf-finalize/scripts/test_render_closeout_html.py
```

- Exit Code: `0`
- Summary: `Ran 17 tests in 0.019s, OK`

```text
# 4. JSON validity
python3 -m json.tool .claude-plugin/plugin.json > /dev/null
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
python3 -m json.tool skills/hf-finalize/test-prompts.json > /dev/null
python3 -m json.tool skills/hf-finalize/evals/evals.json > /dev/null
python3 -m json.tool skills/hf-release/evals/evals.json > /dev/null
```

- All Exit Codes: `0`
- Summary: 5 个 JSON 工件全部有效（含本版 `plugin.json` 升级到 0.5.1 后的解析）

```text
# 5. real sample render（新位置脚本！）
python3 skills/hf-finalize/scripts/render-closeout-html.py examples/writeonce/features/001-walking-skeleton
```

- Exit Code: `0`
- Summary: `wrote examples/writeonce/features/001-walking-skeleton/closeout.html`
- Notable Output: 渲染脚本从新位置调用，对真实 walking-skeleton closeout pack 仍可用；HTML 输出与 v0.5.0 时期渲染相比仅 footer 1 行（脚本路径文本）差异 + 嵌入时间戳差异，证明 D2 物理迁移**不破坏**渲染语义

## Freshness Anchor

- Why this evidence is for the latest relevant code state: 5 项命令在物理迁移完成后同一次 shell 调用中按顺序执行，时间戳 `2026-05-09T18:59:34Z`；执行点晚于本版所有 ADR-006 / SKILL.md / 脚本 / 文档 commit；执行点早于本 release-regression.md 落盘 commit
- Output Log / Terminal / Artifact: 终端输出已抓取（hf-release dogfood 不要求保留独立 log 文件）

## Conclusion

- Conclusion: **PASS**
- Next Action Or Recommended Skill: 进入 `hf-release` §7 cross-feature traceability 摘要 → §8 pre-release engineering checklist

## Scope / Remaining Work Notes

- Remaining Task Decision: 5 项 ops/release skill + 4 家剩余客户端 + 3 personas 按 ADR-006 D1 / ADR-005 D7 显式延后到 v0.6+；不阻塞本 release
- Notes:
  - v0.5.1 是 patch release，verification 重点在"脚本物理位置变化不破坏行为"——所有 5 项检查均能从新位置成功运行 = D2 物理迁移工程上正确
  - 后续如果其它 skill 引入 skill-owned 工具（按 ADR-006 D1），新位置 `skills/<name>/scripts/` 的运行模式已通过本版验证

## Related Artifacts

- `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md`（scope 决策）
- `features/release-v0.5.1/release-pack.md`（主 pack）
- `features/release-v0.5.1/verification/release-traceability.md`（cross-feature traceability 摘要）
- `features/release-v0.5.1/verification/pre-release-checklist.md`（pre-release engineering checklist 勾选状态）

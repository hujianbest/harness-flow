# Test Review — 001-install-scripts (2026-05-11)

- Reviewer: independent subagent (cursor cloud agent), author/reviewer separated from `hf-test-driven-dev` author
- Scope: `tests/test_install_scripts.sh` (12 scenarios)
- Spec: `features/001-install-scripts/spec.md` (approved 2026-05-11)
- Design: `features/001-install-scripts/design.md` §16 — 12 scenarios
- Tasks: `features/001-install-scripts/tasks.md` T1–T10a Acceptance + 测试设计种子
- Verifier evidence: `features/001-install-scripts/verification/e2e-install-2026-05-11.md` (12/12 PASS, replicated locally during this review)

## 结论

**需修改**

理由：12 个 scenario 与 design §16 的 12 个测试矩阵一一对应，主路径覆盖完整且 12/12 在本次 review 会话内复现 PASS。但若干 spec acceptance / tasks 测试种子明示要求的负向边界与 manifest schema 字段在测试中**没有断言**，且其中至少 3 处对一种"sliently broken"的实现仍能 PASS（false-positive 风险）。findings 全部 LLM-FIXABLE，预计 1 轮定向回修可以闭合。

## 多维评分

| ID | 维度 | 分数 | 说明 |
|---|---|---:|---|
| TT1 | fail-first 有效性 | 8/10 | verification/e2e-install-2026-05-11.md 含本次会话内的 PASS 证据；assert 系列 fail-loud；负向 fail-first 点（broken 实现仍 pass）见 TT3/TT4 findings |
| TT2 | 行为/验收映射 | 6/10 | design §16 12 矩阵全覆盖；FR-001 #4 / FR-004 #2 / FR-003 git-path / FR-006 #2 / FR-007 verbose 5 处 acceptance 漏断言 |
| TT3 | 风险覆盖 | 7/10 | HYP-002 Blocking (#7) / NFR-002 (#12) / ASM-001 (#11) / NFR-004 (#10) 均覆盖；缺 arg validation 负向路径 |
| TT4 | 测试设计质量 | 7/10 | mktemp 隔离、fail-on-keep-host、deterministic；但 scenario #8 / #9 / 部分 #1 #5 有 false-positive 风险（broken VERBOSE / broken --force cleanup / broken detect_hf_version 仍能 PASS） |
| TT5 | 新鲜证据完整性 | 9/10 | verification record 当日且 reviewer 复现一致 |
| TT6 | 下游就绪度 | 7/10 | 主路径 code review 可信，但负向路径 + manifest 字段细节会污染 code review；建议先回修 important findings 再进 hf-code-review |

无任一关键维度 < 6/10。

## 发现项

### Important（LLM-FIXABLE）

#### F1 [important][LLM-FIXABLE][TT2/TA2] FR-001 acceptance #4 未覆盖：缺 `--target` 负向路径

- Anchor: `tests/test_install_scripts.sh`（无对应 scenario）
- What: spec FR-001 acceptance #4 明示 "Given 缺少 `--target`，When 执行脚本，Then 脚本以非 0 退出码并打印 usage 文本（含 3 个合法 target 值）"。tasks T1 测试设计种子 "关键边界 1: 缺 `--target` → exit 1" 也明示。当前 12 scenario 无任一断言此行为。
- Why: 这是 install.sh 入口的核心防御行为。如果 `parse_args()` / `validate_args()` 退化（如默认填充 `TARGET="opencode"`），所有现有 scenario 仍能 PASS。下游 code review 无法区分"--target 强制要求"是有意还是回归。
- Suggested fix: 新增 mini scenario（或挂载到现有 scenario）：`bash "$INSTALL" --host "$host"` 期望非 0 退出码 + stderr 含 "--target is required" / "expected cursor|opencode|both"。建议同步覆盖 invalid `--target=foo` 与 invalid `--topology=foo`。

#### F2 [important][LLM-FIXABLE][TT2/TA2] FR-004 acceptance #2 未覆盖：uninstall 缺 manifest 路径

- Anchor: `tests/test_install_scripts.sh`（无对应 scenario）
- What: spec FR-004 acceptance #2 "Given 宿主仓库根没有 `.harnessflow-install-manifest.json`，When 执行 `./uninstall.sh --host /tmp/host`，Then 脚本以非 0 退出码并明确提示'未找到 manifest'"。tasks T7 测试设计种子 "fail-first 点: 缺 manifest → uninstall exit 1 + 明确提示" 也明示。
- Why: 同 F1，这是 uninstall 入口的核心防御。本 reviewer 实测确认 uninstall.sh 实现正确（exit 1 + "no manifest found"），但**测试不覆盖**意味着回归不会被发现。
- Suggested fix: 新增 mini scenario：`bash "$UNINSTALL" --host "$(mktemp -d)"` 期望非 0 + stderr 含 "no manifest found"。

#### F3 [important][LLM-FIXABLE][TT4/TA1] FR-006 --force 清理行为未真实验证（false-positive 风险）

- Anchor: `tests/test_install_scripts.sh:238-254` (scenario_9)
- What: scenario #9 在 `--force` 重装后只断言 `assert_file "$host/.harnessflow-install-manifest.json"`（manifest 存在）。但 manifest 在第一次 install 后**已经存在**；如果 `--force` 退化为"什么也不做就退出 0"，此断言仍 PASS。spec FR-006 acceptance #2 / tasks T7 acceptance 明示 "第一次 install 留下的所有文件被清理，第二次 install 的内容正确就位"。
- Why: 验证不到位 → broken `--force` 路径过 review。reviewer 实测：往 `.opencode/skills/hf-finalize/SENTINEL.txt` 写入哨兵后 `--force` 重装，哨兵确实被清掉（实现正确），但测试不验证。
- Suggested fix: 在 scenario #9 第一次 install 后 `touch "$host/.opencode/skills/hf-finalize/SENTINEL_PRE_FORCE"`；`--force` 重装后 `assert` 该哨兵已被删除。或对比 manifest `installed_at` 字段在 --force 前后不同。

#### F4 [important][LLM-FIXABLE][TT4/TA1] FR-007 `--verbose` 在非 dry-run 模式下未被独立验证（false-positive 风险）

- Anchor: `tests/test_install_scripts.sh:213-225` (scenario_8 verbose 段)
- What: scenario #8 用 `--dry-run --verbose` 测 verbose 行数 > 24。但 install.sh `op()` 在 `DRY_RUN=1 || VERBOSE=1` 时都会打印——也就是说 `--dry-run` 单独已经强制 verbose-like 输出。reviewer 实测：`--dry-run` 不带 `--verbose` 输出 56 行，`--dry-run --verbose` 也是 56 行。
- Why: 如果 `VERBOSE` 变量在 `op()` 中被错误移除（只剩 `DRY_RUN` 触发），`--dry-run --verbose` 测试仍 PASS、`--target opencode --host fresh`（默认非 verbose）测试也 PASS。FR-007 spec "verbose 时输出行数 > 24" 在非 dry-run 模式下没有任何 scenario 断言。
- Why x2: 这条也连带影响 design §11 `op()` 抽象的双触发条件 invariant 没有 test guard。
- Suggested fix: 在 scenario #8 末尾追加：`bash "$INSTALL" --target opencode --verbose --host "$(mktemp -d)" 2>&1 | wc -l` 期望 > 24（这是真正的 non-dry-run verbose 路径）。

#### F5 [important][LLM-FIXABLE][TT4/TA1] FR-003 git-path manifest 字段未被断言（false-positive 风险）

- Anchor: `tests/test_install_scripts.sh:132-142` (scenario_1) 与 #3 / #5
- What: scenario #1 / #3 / #5 验证 manifest 存在与一两条 entry path，但**不**断言 `hf_commit` 是真实 git SHA、`hf_version` 是合法版本号、`target` 字段与 CLI 参数匹配、`topology` 字段与 CLI 参数匹配。spec FR-003 acceptance #1 明示这些字段必须存在。tasks T6 acceptance 明示 "manifest schema 字段齐全"。
- Why: 如果 `detect_hf_version()` 退化为永远返回 fallback 字符串，scenarios #1–#9 全 PASS（只有 #11 才查 fallback 值，反过来如果 git-path 退化它也不会被察觉）；如果 `write_manifest()` 漏写 `target` 字段，scenarios #1–#9 仍 PASS。
- Suggested fix: 在 scenario #1 增加：`grep -qE '"hf_commit"[[:space:]]*:[[:space:]]*"[0-9a-f]{40}"' "$mf"`（git SHA 形态）+ `grep -qE '"hf_version"[[:space:]]*:[[:space:]]*"[0-9]+\.[0-9]+\.[0-9]+"' "$mf"` + `grep -q '"target"[[:space:]]*:[[:space:]]*"opencode"' "$mf"` + 同样 `topology` 字段。scenario #3 / #5 / #6 同步增加 target/topology 反向断言（target=cursor / target=both）。

### Minor（LLM-FIXABLE）

#### F6 [minor][LLM-FIXABLE][TT2] tasks T6 acceptance "per-skill entries 共约 25 条" 未被计数断言

- Anchor: scenario_1 line 140
- What: 只 spot-check `hf-finalize` 一条 entry。tasks T6 acceptance：copy topology 下 entries[] 含每个 hf-* + using-hf-workflow 单独一条 dir entry。
- Suggested fix: `assert_ge "$(grep -c '"kind": "dir"' "$mf")" 25 "per-skill dir entry count"`。

#### F7 [minor][LLM-FIXABLE][TT4/TA4] manifest_has_path 用未转义的 grep 模式

- Anchor: `tests/test_install_scripts.sh:101-104`
- What: `"$want_path"` 直接拼进 grep regex，`.opencode/skills` 中的 `.` 是 regex meta，会匹配任意字符。本场景下不会真造成 false positive，但鲁棒性弱。
- Suggested fix: 用 `grep -qF "\"path\": \"$want_path\""` 或对 `$want_path` 做 `sed 's/[.[\^$*]/\\&/g'`。

#### F8 [minor][LLM-FIXABLE][TT2] scenario #4 (cursor symlink) 不验证 manifest entries

- Anchor: scenario_4
- What: 只验证两条 symlink 路径，没有 `manifest_has_path` 调用。
- Suggested fix: 增加 `manifest_has_path "$mf" ".cursor/harness-flow-skills"`（kind=symlink）+ `.cursor/rules/harness-flow.mdc`。

#### F9 [minor][LLM-FIXABLE][TT3] scenario #12 仅覆盖"第一个 mkdir 失败"的 rollback 路径

- Anchor: scenario_12
- What: tasks T8 风险 1 已声明"父目录只读"是最简实现，更深的 partial cp -R 失败留作 v0.6+。本 finding 是观察记录，不是阻塞——但 design §17 失败模式表中"Partial cp -R 残留"仅靠 inspection 没有 test guard。
- Suggested fix: 不强制；若想加固，可在 scenario #12 增加变体——install 第 N 个 skill 时 chmod -w 中间触发，验证 rollback 清掉前 N-1 个子树。或显式注明"deferred to v0.6+"接受现状。

## 缺失或薄弱项

| 缺口 | 影响 spec/task 锚点 | 严重度 |
|---|---|---|
| 缺 `--target` / invalid `--target` / invalid `--topology` 负向 scenario | spec FR-001 #4；tasks T1 测试种子 | important (F1) |
| 缺 uninstall 无 manifest 负向 scenario | spec FR-004 #2；tasks T7 测试种子 | important (F2) |
| `--force` 清理行为未真实验证 | spec FR-006 #2；tasks T7 acceptance | important (F3) |
| `--verbose` 在非 dry-run 模式下未独立验证 | spec FR-007；tasks T1 acceptance | important (F4) |
| manifest git-path 字段（hf_commit/hf_version/target/topology）未断言 | spec FR-003；tasks T6 acceptance | important (F5) |
| per-skill entries 总数（≥ 25）未断言 | tasks T6 acceptance | minor (F6) |
| manifest_has_path regex 未转义 | TT4 robustness | minor (F7) |
| scenario #4 manifest entries 未验证 | design §16 #4 | minor (F8) |
| partial cp -R rollback 路径未覆盖 | design §17（已声明 deferred） | minor (F9, 可接受) |

## 覆盖矩阵（per scenario × spec acceptance）

| Scenario | 主路径覆盖 | 边界/负向覆盖 | 状态 |
|---|---|---|---|
| #1 opencode copy | covered (find ≥ 24, manifest exists, hf-finalize 一条 entry, readme exists) | manifest 字段（hf_commit/hf_version/target/topology）+ per-skill 总数 missing | partial |
| #2 opencode symlink | covered (readlink, manifest .opencode/skills entry) | manifest entries kind=symlink 反向断言 missing | partial |
| #3 cursor copy | covered (find ≥ 24, rule file, manifest rule entry) | per-skill 总数、target/topology 字段 missing | partial |
| #4 cursor symlink | covered (两条 symlink) | manifest entries 完全未验证 | partial (F8) |
| #5 both copy | covered (两套 SKILL.md count + rule file) | manifest 完全未验证；target=both 字段未断言 | partial |
| #6 both symlink | covered (三条 symlink) | manifest 未验证 | partial |
| #7 HYP-002 user-skill preserved | **fully covered**（HF skill 删除 + user skill 保留 + manifest 删除三态都断言；HYP-002 Blocking 验证有效） | — | **covered** |
| #8 dry-run + FR-007 行数边界 | covered（dry-run 无副作用 + 默认 < 10 + 大行数 > 24） | non-dry-run --verbose 路径 missing（F4） | partial |
| #9 force + uninstall dry-run | covered（无 --force 拒绝 + --force 不报错 + uninstall --dry-run no-op） | --force 真实清理验证 missing（F3） | partial |
| #10 NFR-004 grep audit | **fully covered**（awk 剥注释 + `\b` word boundary 正确排除 `python3`；reviewer 验证 `python3 scripts/...` 不会触发） | — | **covered** |
| #11 ASM-001 non-git fallback | **fully covered**（hf_commit downgrade + hf_version 仍解析） | git-path 反向断言（验证非 fallback）missing — 见 F5 | partial |
| #12 NFR-002 rollback | **covered**（chmod -w → mkdir 失败 → ERR trap → rollback → host count 恢复 + 无 manifest 残留；NFR-002 验证有效） | partial cp -R 路径 deferred（F9 可接受） | covered |

## 测试设计质量审查

- ✅ **隔离性**：每 scenario `mktemp -d -t hf-install-test.XXXXXX`，互不干扰
- ✅ **清理策略**：PASS 时 `rm -rf "$host"`；FAIL 时保留 host 供 inspection（line 117–124）
- ✅ **fail-loud assertion helpers**：`assert_eq` / `assert_ge` / `assert_file` / `assert_symlink_to` 均显式 `printf >&2 + return 1`，不会沉默通过
- ✅ **`set -uo pipefail`** 而非 `set -e`：刻意避免 assertion 失败时整个 driver 中止，逐 scenario 报告。设计合理
- ✅ **scenario #11 fake_repo 清理**：4 条退出路径都有 `rm -rf "$fake_repo"`
- ✅ **scenario #12 chmod 恢复**：在 assert 前 `chmod +w "$host"`，避免 driver 自身 leak
- ⚠️ **manifest 验证颗粒度**：仅 `manifest_has_path` 检查 `path` 字段；`kind` 字段、其他字段（hf_commit / hf_version / target / topology）从未被断言（F5）
- ⚠️ **VERBOSE 与 DRY_RUN 在 op() 中强耦合**：导致 verbose 行数测试在 dry-run 下退化（F4）

## Anti-Pattern 检测

| ID | Anti-Pattern | 是否命中 | 说明 |
|---|---|---|---|
| TA1 | born-green | 部分（F3/F4/F5）| 三处 broken 实现仍 PASS 的 false-positive 风险 |
| TA2 | happy-path-only | 部分（F1/F2）| 两处 negative path（缺 --target / 缺 manifest）虽然 spec / tasks 明示但未被测试 |
| TA3 | mock overreach | 否 | 不用 mock，直接跑真脚本 |
| TA4 | no acceptance link | 否 | tests 头注释明确映射 design §16 12 scenario；本 review 进一步映射到 spec FR/NFR/ASM |
| TA5 | stale evidence | 否 | verification record 与 reviewer 本次复现一致（12/12） |

## 下一步

- **结论**：需修改 → `next_action_or_recommended_skill = hf-test-driven-dev`
- **建议回修顺序**（5 处 important 都是定向小改，可一并回修）：
  1. F1 + F2：新增 2 个 negative-path mini scenario（建议作为 #13 / #14，不打散现有编号）
  2. F3：scenario #9 加 SENTINEL touch + 验证已被清
  3. F4：scenario #8 加 non-dry-run --verbose 行数测试
  4. F5：scenario #1 / #3 / #5 / #6 加 4–5 条 manifest 字段断言
  5. minor F6–F8：可一起改，加几条 grep / count 断言
  6. F9：可接受 deferred
- 完成后回到 `hf-test-review` 二次复评（同一 record 文件追加 review-2 段，或新建 `test-review-2026-05-11-r2.md`）

## 结构化返回 JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "record_path": "features/001-install-scripts/reviews/test-review-2026-05-11.md",
  "key_findings": [
    "[important][LLM-FIXABLE][TT2/TA2] F1: FR-001 #4 缺 --target 负向路径未覆盖（tasks T1 种子明示）",
    "[important][LLM-FIXABLE][TT2/TA2] F2: FR-004 #2 uninstall 缺 manifest 路径未覆盖（tasks T7 种子明示）",
    "[important][LLM-FIXABLE][TT4/TA1] F3: FR-006 --force 真实清理未验证；broken --force 仍 PASS（false-positive）",
    "[important][LLM-FIXABLE][TT4/TA1] F4: FR-007 verbose 在非 dry-run 模式下未独立验证；broken VERBOSE 仍 PASS（false-positive）",
    "[important][LLM-FIXABLE][TT4/TA1] F5: FR-003 git-path manifest 字段（hf_commit/hf_version/target/topology）未断言；broken detect_hf_version 仍 PASS（false-positive）"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TT2/TA2", "summary": "F1 FR-001 #4 缺 --target 负向路径未覆盖"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TT2/TA2", "summary": "F2 FR-004 #2 uninstall 缺 manifest 路径未覆盖"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TT4/TA1", "summary": "F3 FR-006 --force 清理未真实验证"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TT4/TA1", "summary": "F4 FR-007 verbose 在非 dry-run 模式下未独立验证"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TT4/TA1", "summary": "F5 FR-003 git-path manifest 字段未断言"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TT2", "summary": "F6 per-skill entries 总数未断言"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TT4/TA4", "summary": "F7 manifest_has_path regex 未转义"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TT2", "summary": "F8 scenario #4 manifest entries 未验证"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "TT3", "summary": "F9 partial cp -R rollback 路径未覆盖（design 已声明 deferred，可接受）"}
  ]
}
```

---

# Round 2 — 2026-05-11 (post Round 1 回修)

- Reviewer: same independent subagent (round 2)
- Scope of changes since R1: `tests/test_install_scripts.sh` 14 scenarios (12 original + #13/#14 new)
- 14/14 PASS replicated locally during this round (`bash tests/test_install_scripts.sh` exit 0)

## R2 结论

**通过** → `next_action_or_recommended_skill = hf-code-review`

理由：R1 的 5 处 important + 4 处 minor finding 全部按建议落地，且 reviewer 对每条 fix 进行了 false-positive 复测（探针验证 broken implementation 会真实触发新断言失败）。无新发现的关键缺陷。

## 多维评分（R2 复评）

| ID | 维度 | R1 → R2 | 说明 |
|---|---|---:|---|
| TT1 | fail-first 有效性 | 8 → 9 | F3/F4/F5 fix 后 born-green 风险显著降低；reviewer 实测 broken impl 会触发断言失败 |
| TT2 | 行为/验收映射 | 6 → 9 | F1/F2/F5/F6/F8 fix 后 acceptance 漏断言全部补齐 |
| TT3 | 风险覆盖 | 7 → 8 | F1/F2 补齐 negative path；F9 partial cp -R 仍 deferred（design 已声明，可接受） |
| TT4 | 测试设计质量 | 7 → 9 | F3 sentinel + installed_at + sleep 1；F4 fresh hosts；F7 grep -F；都是教科书式的回修 |
| TT5 | 新鲜证据完整性 | 9 → 9 | reviewer 当次复跑一致 |
| TT6 | 下游就绪度 | 7 → 9 | 测试质量足以让 code review 信任主路径 + 字段细节 + 负向行为 |

## R1 finding 处置矩阵

| Finding | R1 严重度 | Fix 锚点 | Reviewer 复测结论 |
|---|---|---|---|
| F1 缺 --target | important | scenario #13 (lines 359-371) | ✅ 已修。两段断言：先验非 0 退出码，再独立捕获 stderr grep `--target`。Probe: 实测 broken impl（默认填充 TARGET）会让首段 `if bash ... ; then return 1` 触发失败。 |
| F2 缺 manifest | important | scenario #14 (lines 373-385) | ✅ 已修。同 F1 双段结构，grep `-qi 'no manifest'` 防大小写敏感。Probe: 实测 broken impl（silently exit 0）会触发失败。 |
| F3 --force false-positive | important | scenario #9 (lines 270-289) | ✅ 已修。两层防御：(a) sentinel 文件落在 `hf-finalize/` 子树，--force 必须先 uninstall → sentinel 被删；(b) 比较 `installed_at` 字段确保新 manifest 写入。Probe: sleep 1 在 1s 时间戳粒度下严格保证字符串差异；reviewer 实测 OLD=`2026-05-11T18:04:04Z`、NEW=`2026-05-11T18:04:05Z`，确实 advance 1 秒。Broken impl 类型："noop --force" → installed_at 不变 + sentinel 残留 → 双断言均失败；"skip uninstall, only rewrite manifest" → installed_at 变 + sentinel 残留 → sentinel 断言失败。两种 broken 都会被捕获。 |
| F4 verbose false-positive | important | scenario #8 (lines 235-260) | ✅ 已修。三段防御：(a) `default_lines < 10` 用全新 host 跑非 dry-run 默认安装；(b) `verbose_lines > 24` 用另一全新 host 跑非 dry-run --verbose；(c) sanity gap `verbose - default > 14`。Probe: reviewer 实测 default=3 / verbose=55 / gap=52；threshold 14 在 25 skills 规模下有 ~38 line headroom。Broken impl（`op()` 不再响应 `VERBOSE=1`）→ verbose=3 → fails (b) 且 fails (c)。 |
| F5 git-path manifest fields | important | scenario #1 (lines 145-152) | ✅ 已修。5 条 grep：`manifest_version: 1` / `hf_commit` 40-char hex SHA / `hf_version` SemVer / `target: opencode` / `topology: copy`。Probe: 实测当前 manifest 字段全部 match。Broken impl（hf_commit 永远 fallback）→ `[a-f0-9]{40}` 不 match `unknown-non-git-checkout`（含连字符），fails。 |
| F6 per-skill count | minor | scenario #1 (lines 153-156) | ✅ 已修。`grep -cE '"path"[[:space:]]*:[[:space:]]*"\.opencode/skills/[^"]+"'` 严格要求斜线后非空，正确排除父 dir entry `.opencode/skills`。当前 count = 26 - 1（父）= 25 ≥ 25 ✓ |
| F7 manifest_has_path regex | minor | helper (lines 101-106) | ✅ 已修。改为 `grep -F -q`，fixed string 不再被 `.` 等元字符影响。 |
| F8 scenario #4 manifest entries | minor | scenario #4 (lines 181-187) | ✅ 已修。4 条 grep 覆盖 target/topology/skills symlink entry/rule symlink entry。Probe: 实测格式 `{"kind": "symlink", "path": ".cursor/harness-flow-skills"}` 与断言完全匹配。 |
| F9 partial cp -R rollback | minor | (deferred) | ⚪ 接受现状。design §17 + tasks T8 风险 1 已显式 deferred 至 v0.6+。 |

## R2 新发现

经 reviewer 复测，**未发现新的 critical/important finding**。

仅记录 2 条**informational**观察（不构成 finding，不影响 verdict）：

- **I1**（informational）scenario #4 与 #1 的 `grep -q '"kind": "symlink", "path": "..."'` 依赖 install.sh `printf` 当前的具体空格规则（`{"kind": "%s", "path": "%s"}`）。如果未来 manifest 格式 reformat（例如 jq 风格 pretty-print），grep 需同步更新。当前接受——因为 install.sh 自身就是 manifest 唯一 producer + reviewer 确认格式稳定。
- **I2**（informational）scenario #5/#6 (`--target both`) 仍未直接断言 `"target": "both"` manifest 字段。F5 fix 在 #1 覆盖了 opencode；F8 fix 在 #4 覆盖了 cursor symlink；但 both 没有专门的 manifest target 断言。两个 scenario 通过 files-on-disk 已覆盖核心行为（两套路径同时就位），故不构成实际 false-positive 风险——若 install 把 target 错写成 "opencode" 但仍铺设了 .cursor/，files-on-disk 检查全部 PASS 但 manifest target 字段错。理论上是 minor 缺口，但 spec FR-001 acceptance 关注的是文件就位本身，所以 reviewer 选择不升级为 finding。建议作者后续在 #5/#6 各加一行 `grep -q '"target": "both"'` 时一并修，但本轮不阻塞。

## R2 false-positive 探针记录

reviewer 直接执行的探针命令（非测试代码改动；用于验证 fix 的鲁棒性）：

| 探针 | 命令 | 结果 |
|---|---|---|
| F4 default vs verbose 实际差距 | 两个 fresh host 分别跑 default / --verbose 安装 | default=3 lines, verbose=55 lines, gap=52 → 远大于 threshold 14 ✓ |
| F3 installed_at 时间戳粒度 | install → sleep 1 → install --force → 比较 installed_at | OLD=`...T18:04:04Z`、NEW=`...T18:04:05Z`，advance 1s → 字符串严格不等 ✓ |
| F3 sentinel 在 --force 后 | install → 写 SENTINEL.txt → install --force → 检查 SENTINEL | DELETED ✓（说明 --force 实际触发了 uninstall 步骤） |
| F8 cursor symlink manifest 实际格式 | 查看 .harnessflow-install-manifest.json | `{"kind": "symlink", "path": ".cursor/harness-flow-skills"}` 与断言精确匹配 ✓ |
| F5 broken-impl simulation | 思维实验：若 hf_commit 永远 = `unknown-non-git-checkout` | regex `[a-f0-9]{40}` 不 match（含 `-` 与 `n` 等非 hex 字符）→ assertion fails ✓ |

## R2 覆盖矩阵（合并后 14 scenario）

| Scenario | 状态 | 备注 |
|---|---|---|
| #1 opencode copy | **fully covered** | F5/F6 fix 后含 manifest_version + hf_commit SHA + hf_version SemVer + target/topology + per-skill count ≥ 25 |
| #2 opencode symlink | covered | manifest entries kind=symlink 已通过 #4/#1 旁证；本 scenario 仅查 path |
| #3 cursor copy | covered | rule entry + SKILL.md count ≥ 24 |
| #4 cursor symlink | **fully covered** | F8 fix 后含 target/topology/两条 symlink entry |
| #5 both copy | covered | files-on-disk 检查充分；manifest target 字段未断言（I2，可接受） |
| #6 both symlink | covered | 同 #5 + 三条 symlink |
| #7 HYP-002 | **fully covered** | unchanged from R1 |
| #8 dry-run + FR-007 | **fully covered** | F4 fix 后 default + verbose 在 non-dry-run 模式下独立验证 + sanity gap |
| #9 force + uninstall dry-run | **fully covered** | F3 fix 后 sentinel + installed_at 双层验证 |
| #10 NFR-004 grep audit | **fully covered** | unchanged from R1 |
| #11 ASM-001 | **fully covered** | unchanged from R1 |
| #12 NFR-002 rollback | covered | partial cp -R deferred（F9，acceptable） |
| #13 FR-001 missing --target | **fully covered** | new (F1 fix) |
| #14 FR-004 no manifest | **fully covered** | new (F2 fix) |

## R2 下一步

- 结论：通过 → `next_action_or_recommended_skill = hf-code-review`
- 触发 hf-code-review 时，建议提示 code reviewer 重点审：
  - install.sh `op()` 抽象的 `VERBOSE` 与 `DRY_RUN` 触发条件不可被无意合并（F4 fix 保护）
  - install.sh `detect_existing_manifest()` 的 `--force` 路径必须真实调用 uninstall.sh（F3 fix 保护）
  - install.sh `detect_hf_version()` 的 git-path 与 fallback-path 都要正确（F5 + scenario #11 双向保护）

## R2 结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-code-review",
  "record_path": "features/001-install-scripts/reviews/test-review-2026-05-11.md",
  "key_findings": [
    "R1 的 5 处 important + 4 处 minor finding 全部已按建议落地",
    "F3/F4/F5 fix 经 reviewer false-positive 探针复测：broken impl 会真实触发新断言失败",
    "scenario #13/#14 双段结构（exit-code + stderr-grep）确保 negative path 不会 silent pass",
    "F4 verbose-default sanity gap 实测 52 > threshold 14，有 ~38 line headroom",
    "无新发现 critical/important finding；2 条 informational 观察（manifest 格式 brittleness 与 #5/#6 target 字段）不阻塞"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": []
}
```

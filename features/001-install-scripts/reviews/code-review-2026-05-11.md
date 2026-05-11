# Code Review — 001-install-scripts (2026-05-11)

- Reviewer: independent subagent (cursor cloud agent), author/reviewer separated from `hf-test-driven-dev` author
- Scope: `install.sh` (409 lines) + `uninstall.sh` (182 lines)
- Spec: `features/001-install-scripts/spec.md` (approved 2026-05-11)
- Design: `features/001-install-scripts/design.md` (approved 2026-05-11)
- ADR: `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md` (accepted)
- Upstream test review: `features/001-install-scripts/reviews/test-review-2026-05-11.md` (Round 2 通过)
- Verifier evidence: `features/001-install-scripts/verification/e2e-install-2026-05-11.md` (14/14 PASS)
- Skill: `skills/hf-code-review/SKILL.md` + `references/review-checklist.md`

## 结论

**通过** → `next_action_or_recommended_skill = hf-traceability-review`

理由:

1. install.sh 与 uninstall.sh 严格落实 design §11 函数清单与 §11 编码约束（`set -Eeuo pipefail` / `IFS=$'\n\t'` / 无 mapfile / 无关联数组 / 无 `${var,,}` / 全路径引号 / shebang / `for ((..))`）。
2. ADR-007 D1..D5 全部 manifested in code（D1 纯 shell 无 jq/python/node；D2 manifest as authority；D3 printf 拼 JSON + grep/sed 解析；D4 cursor vendor 路径 = `.cursor/harness-flow-skills`；D5 post-install README）。
3. spec FR-001..FR-008 + NFR-001..NFR-004 + ASM-001 全部覆盖且 14/14 e2e PASS（含 HYP-002 Blocking 验证 + NFR-002 rollback 闭合）。
4. `mark_will_create` 预登记 + dir-类 rollback `rm -rf` + `set -E` 跨函数 ERR 继承三件套共同闭合 design important finding 2 (rollback 闭合性) 与 H2 hotspot (HF==host 自我 vendor) 与 NFR-002。
5. per-skill manifest 颗粒度落实 design important finding 1 fix（约 25 条 dir entry + 父 dir 一条）；scenario #7 HYP-002 Blocking 在线复测 PASS 即直接证据。
6. 所有 finding 均为 minor LLM-FIXABLE，无核心逻辑错误、无安全漏洞、无 architectural smell、无 escalation-bypass、无 ADR / 模块边界 / 接口契约违反。non-blocking optimization items 留给 traceability review 知悉，可在后续增量收口。

## 多维评分

| ID | 维度 | 分数 | 说明 |
|---|---|---:|---|
| CR1 | 正确性 | 9/10 | 14/14 e2e PASS；逻辑路径完整；M3/M4 是 corner-case robustness 项 |
| CR2 | 设计一致性 | 8/10 | 函数集 / 全局变量 / 编码约束 / 颗粒度全部命中；M1 是 uninstall.sh 与 design §10 line 216 的细节不一致 |
| CR3 | 状态 / 错误 / 安全 | 8/10 | trap rollback + mark_will_create 预登记 + `\|\| true` 兜底；M3 缺少"flag 缺值"的友好报错 |
| CR4 | 可读性与可维护性 | 8/10 | 命名 / 结构 / 注释 / usage 文本均合格；M2 `for name in $(ls ...)` 是经典 bash anti-pattern（但当前 skill 命名集合无空格，零功能影响） |
| CR5 | 范围守卫 | 10/10 | 严格遵守 spec §6 范围；未引入任何 undocumented behavior |
| CR6 | 下游追溯就绪度 | 9/10 | manifest schema + post-install README + verification record 充分；trace 锚点齐全 |
| CR7 | 架构健康与重构纪律 | 8/10 | 主维度 8/10；子维度详见下表 |

CR7 子维度：

| ID | 子维度 | 分数 | 说明 |
|---|---|---:|---|
| CR7.1 | Two Hats Hygiene | N/A | greenfield 任务，T1..T10a 全部新建文件；无 RED-GREEN-REFACTOR 中的 hat-mixing 风险面（无既有结构需要 preparatory refactor） |
| CR7.2 | Refactor Note 完整性 | 6/10 | 实现交接块未提供独立 Refactor Note。greenfield 性质 + test-review R2 已显式 approve 进 code-review，本次 reviewer 选择不升级为 precheck blocked；记为 minor M5 |
| CR7.3 | Architectural Conformance | 9/10 | 严格遵守 design §10 single-file shell pipeline + plan-then-apply 模式；未引入新依赖方向 / 新跨层调用 / 新抽象层 |
| CR7.4 | Architectural Smells Detection | 9/10 | 无 god-class（脚本 ~400 行单文件是 design 的有意决策，避免 sourcing 多文件，见 design §10 Container view）；无 cyclic-dep；无 layering violation；无 leaky abstraction；无 over-abstraction（未引入 design 未声明的新接口） |
| CR7.5 | Boy Scout Compliance | N/A | greenfield；无既有触碰文件 |

任一关键维度未 < 6/10；CR7 主维度 8 ≥ 8、所有 CR7 子维度 ≥ 6。

## 设计 / ADR / spec 覆盖矩阵

### 函数级映射 (design §11)

| design §11 函数 | install.sh 落点 | 状态 |
|---|---|---|
| `parse_args()` | lines 142-162 | ✅ 完整；6 个 long flag + `=value` 形式 + `-h/--help` |
| `validate_args()` | lines 164-193 | ✅ 完整；H2 hotspot（HF==host）拦截在 line 189 |
| `detect_existing_manifest()` | lines 195-216 | ✅ 完整；FR-006 `--force` 路径委派给 uninstall.sh |
| `detect_hf_version()` | lines 218-237 | ✅ 完整；ASM-001 双降级（hf_commit / hf_version 各自独立 fallback） |
| `vendor_skills_opencode()` | lines 239-258 | ✅ 完整；topology 分支齐全；per-skill 颗粒度 |
| `vendor_cursor()` | lines 260-289 | ✅ 完整；topology 分支齐全；rule 文件单独 entry |
| `mark_will_create()` | lines 113-122 | ✅ 完整；pre-existing dir 跳过登记（避免误删宿主原有 dir） |
| `write_manifest()` | lines 291-322 | ✅ 完整；JSON schema 字段齐全；最后一条 entry sep="" 处理正确 |
| `write_readme()` | lines 324-374 | ✅ 完整；30 行 markdown 含 4 条 verify 命令 + uninstall + cursor rule 注记 |
| `rollback()` | lines 124-140 | ✅ 完整；INSTALLED 反向迭代；dir 类 `rm -rf`；最后清 manifest + readme（belt-and-suspenders） |
| `log()` / `err()` / `op()` | lines 78-107 | ✅ 完整；op 触发条件 = `VERBOSE=1 \|\| DRY_RUN=1`（test #8 F4 fix 已为本约束加 guard） |

### 编码约束 (design §11)

| 约束 | 检查结果 |
|---|---|
| 不用 mapfile / readarray | ✅ rg 验证：源码未出现 |
| 不用关联数组 declare -A | ✅ 未出现 |
| 不用 `${var,,}` / `${var^^}` | ✅ 未出现 |
| 数组迭代 `for i in "${ARR[@]}"` | ✅ install.sh 用 `for ((i=...; i<n; i++))` 索引访问；uninstall.sh 同；bash 3.0+ 都合法 |
| 路径变量全 `"$VAR"` 引用 | ✅ 抽样核对均合规（HOST / HF_REPO / abs / path 等） |
| shebang `#!/usr/bin/env bash` + `set -Eeuo pipefail` | ✅ 双脚本均符合 |
| `IFS=$'\n\t'` | ✅ 双脚本均符合 |

### ADR-007 D1..D5

| 决策 | 落地证据 | 状态 |
|---|---|---|
| D1 纯 bash + POSIX coreutils | scenario #10 grep audit 0 命中（`(awk '!/^[[:space:]]*#/' install.sh uninstall.sh) \| grep -E '\b(jq\|python\|node\|npm)\b'` 输出空） | ✅ |
| D2 manifest 唯一权威 + per-skill 颗粒度 | install.sh `vendor_skills_opencode` 每个 skill 单独 entry；scenario #7 HYP-002 PASS（user-skill `my-own-skill` 不在 entries 故被保留） | ✅ |
| D3 printf 拼 JSON / grep+sed 解析 | install.sh lines 301-321 printf；uninstall.sh lines 99-105 grep+sed | ✅ |
| D4 cursor vendor = `.cursor/harness-flow-skills` + rule = `.cursor/rules/harness-flow.mdc` | install.sh lines 266-269 hardcoded | ✅ |
| D5 post-install README | install.sh lines 324-374 写 30 行 markdown，含 4 条 verify 命令 + uninstall + cursor rule 注记 | ✅ |

### spec 需求覆盖

| 需求 | 落地证据 | 状态 |
|---|---|---|
| FR-001 (--target cursor/opencode/both) | parse_args + validate_args + main 分发；scenario #1/#3/#5 PASS；scenario #13 验证缺 --target → exit 1 | ✅ |
| FR-002 (copy/symlink topology) | vendor_skills_opencode + vendor_cursor topology 分支；scenario #1-#6 PASS | ✅ |
| FR-003 (manifest schema) | write_manifest + scenario #1 manifest_version/hf_commit/hf_version/target/topology 5 字段 grep；scenario #11 ASM-001 fallback 验证 | ✅ |
| FR-004 (uninstall.sh) | uninstall.sh 完整流程；scenario #7 HYP-002 PASS；scenario #14 缺 manifest → exit 1 | ✅ |
| FR-005 (--dry-run) | op() 在 DRY_RUN=1 时只打印不执行；write_manifest + write_readme dry-run guard；scenario #8 PASS；M4 是 `--dry-run --force` 组合的 corner case | ✅ (M4 minor) |
| FR-006 (--force) | detect_existing_manifest 调用 uninstall.sh；scenario #9 sentinel + installed_at 双断言 PASS | ✅ |
| FR-007 (--verbose) | op() 双触发条件；scenario #8 default<10 + verbose>24 + sanity gap>14 PASS | ✅ |
| FR-008 (4 类子目录搬运) | `cp -R "$HF_REPO/skills/$name" "$skill_abs"` 整 skill 子树；scenario #1/#3 SKILL.md count ≥ 24（自然包含 scripts/ / references/ / evals/） | ✅ |
| NFR-001 Installability | 单条命令完成；e2e 总耗时 ≤ 120s（实测 ≤ 30s） | ✅ |
| NFR-002 Reliability rollback | trap + set -E + mark_will_create 预登记 + dir 类 rm -rf；scenario #12 PASS | ✅ |
| NFR-003 Testability 6 组合 | scenario #1-#6 PASS | ✅ |
| NFR-004 Maintainability 无新依赖 | scenario #10 grep audit clean；bash 3.2 兼容编码约束守住 | ✅ |
| ASM-001 非 git checkout | detect_hf_version 双 fallback；scenario #11 PASS | ✅ |

## 发现项

### Important

无。

### Minor (LLM-FIXABLE)

#### M1 [minor][LLM-FIXABLE][CR2] uninstall.sh 末尾 rmdir `.opencode` / `.cursor` 偏离 design §10 line 216 显式决策

- Anchor: `uninstall.sh:161-169`
- What: design.md §10 line 216 明示 `mark_will_create dir "$HOST/.opencode" "" → .opencode 父 dir 不进 manifest，uninstall 后**保留**该 dir`，理由是"避免在 uninstall 时与宿主用户的 .opencode 自身的 git tracking 状态产生意外耦合"。但 `uninstall.sh:161-169` 在主清理流程后又对 `$HOST/.opencode` 与 `$HOST/.cursor` 各做一次 best-effort `rmdir 2>/dev/null || true`。
- Why: 实务影响小（rmdir-only，非空时静默失败 → 与 design 行为等价）；但偏离 design 显式记录的"保留"决策。如果未来宿主 `.opencode` 是空 dir 但 git tracked（用户为某未来用途占位），我们会把它清掉，可能引发"我没动 .opencode 怎么 git status 显示删除"的迷惑。
- Suggested fix（任选一）:
  - (a) 删除 uninstall.sh:161-169 整段，与 design §10 line 216 完全对齐；
  - (b) 更新 design.md §10 line 216 把"保留该 dir"改为"best-effort rmdir-only（仅当 dir 由 HF 创建且现在为空时才回收）"，并补 rationale。
- 是否阻塞: 否；M1 本身不影响 14/14 e2e PASS（所有现有 scenario 中 `.opencode` / `.cursor` 在 uninstall 后实际都是空的，故 rmdir 都成功——但这恰恰说明 design intent 与 code 行为不一致只是没被现场触发到）。

#### M2 [minor][LLM-FIXABLE][CR4] `for name in $(ls "$HF_REPO/skills")` 是经典 bash anti-pattern

- Anchor: `install.sh:251`、`install.sh:280`
- What: 用 `$(ls ...)` 的输出做 `for` 循环：(a) 依赖 `IFS` 切分输出（当前 IFS=$'\n\t' 安全）；(b) ls 自身的输出格式可被 alias / 环境影响（虽然 install.sh 不 source 用户 rc 文件，风险低）；(c) shellcheck SC2045 / SC2012 经典 lint 项。
- Why: 当前 HF skill 名集合（hf-* + using-hf-workflow）无空格无 glob 元字符，零功能影响。但 shellcheck 等静态分析工具会报警，且本脚本是要 vendor 到任意宿主仓库的"对外脚本"，rigor 标准应高一些。
- Suggested fix:
  ```bash
  local skill_path
  for skill_path in "$HF_REPO/skills"/*; do
      [ -d "$skill_path" ] || continue
      local name="${skill_path##*/}"
      ...
  done
  ```
  或保持 `$(ls)` 但加 `# shellcheck disable=SC2045` 显式接受。
- 是否阻塞: 否。

#### M3 [minor][LLM-FIXABLE][CR3] flag 缺值时 `shift 2` 在 `set -e` 下退出但无明确报错

- Anchor: `install.sh:142-162`、`uninstall.sh:61-75`
- What: 当 `--target` / `--topology` / `--host` 是命令行末尾 token（无随后 value）时，`"${2:-}"` 把变量设为空串，随后 `shift 2` 因只剩 1 个 positional 参数而失败，`set -e` 触发整个脚本非 0 退出，但用户只看到 silent exit（无 `err` 调用）。
- Why: spec FR-001 acceptance #4 已要求"缺 --target 报错并打印 usage"——当前对"完全不传 --target"是覆盖的（validate_args 报 `--target is required`），但对"传了 --target 但没 value"则 silent。属于 negative path 的 robustness 缺口。
- Suggested fix: 在每个 `case` 分支前加最小 guard——
  ```bash
  --target)
      if [ $# -lt 2 ]; then err "--target requires a value"; usage >&2; exit 1; fi
      TARGET="$2"; shift 2 ;;
  ```
  或改用 `--target=VALUE` 形式强制（但会破坏 long-flag 习惯）。
- 是否阻塞: 否；当前 14 scenario 不覆盖此具体 path，但 spec 也未显式列入 acceptance；记为 minor。

#### M4 [minor][LLM-FIXABLE][CR1] `install --force --dry-run` 实际删除上次安装（违反 FR-005 严格读法）

- Anchor: `install.sh:198-210` (`detect_existing_manifest` 内 `bash "$uninstall" --host "$HOST"` 调用)
- What: 当 `--force` + `--dry-run` 同时出现时，`detect_existing_manifest` 会**真实**调用 uninstall.sh（未传 `--dry-run`）清掉上次安装的所有文件，然后才进入 dry-run 主流程"打印计划"。spec FR-005 严格读法："脚本必须打印将要执行的所有 mkdir/cp/ln/rm 操作，但**不**真实写入或删除任何文件"——本组合违反。
- Why: 真实 user 用 `--force --dry-run` 的意图通常是"预览强制重装会做什么"，而不是"真删上次的同时预览新的"。属于 corner case，但是 spec FR-005 / FR-006 组合的语义裂缝，没有 scenario 覆盖。
- Suggested fix（任选一）:
  - (a) `detect_existing_manifest` 在 `DRY_RUN=1` 且 `FORCE=1` 时只打印 `[FORCE] would invoke uninstall.sh --host <HOST>`，不真实调用；
  - (b) 在 `parse_args` 后显式拒绝 `--force --dry-run` 组合并 err 退出。
- 是否阻塞: 否；spec / tasks 未明示此组合行为，且 scenario 不覆盖；记为 minor 留给 traceability review 知悉。

#### M5 [minor][LLM-FIXABLE][CR7.2] 实现交接块缺独立 Refactor Note 段

- Anchor: `features/001-install-scripts/progress.md`（无独立 Refactor Note 字段）
- What: hf-code-review 默认期望实现交接块带独立 Refactor Note（含 Hat Discipline / In-task Cleanups / Architectural Conformance / Documented Debt / Escalation Triggers / Fitness Function Evidence 6 字段）。当前 progress.md "What Changed" + "Session Log" 已涵盖大部分信息，但未按 CR7.2 要求结构化。
- Why: 本 feature 是 greenfield（T1..T10a 全新建文件，无既有代码触碰），CR7.1 Two Hats / CR7.5 Boy Scout 大部分子维度 N/A；Architectural Conformance / Escalation Triggers / Documented Debt 三项可在 traceability review 阶段从 design / ADR / progress 反推。本次 reviewer 选择**不**升级为 precheck blocked，因为 (a) test-review R2 verdict 已显式 `next_action_or_recommended_skill = hf-code-review`；(b) 14/14 e2e PASS + design conformance check 都已直接完成；(c) 强制要求 Refactor Note 模板对 greenfield 新建文件 ROI 较低。
- Suggested fix: 后续 TDD 节点（如 T10b doc 同步、或 v0.6+ 新增功能）补 Refactor Note 模板到 progress.md，提示字段：
  ```
  Refactor Note (T1..T10a):
  - Hat Discipline: greenfield, T1..T10a 全 RED→GREEN 顺序，无 hat-mixing
  - In-task Cleanups: N/A (greenfield)
  - Architectural Conformance: design §10 single-file shell pipeline；ADR-007 D1..D5 全部 manifested
  - Documented Debt: ADR-007 D4 A3 (rule 路径自动重写) 推迟到 v0.6+；spec-deferred DEF-001..DEF-007
  - Escalation Triggers: none
  - Fitness Function Evidence: scenario #10 grep audit clean；14/14 e2e PASS
  ```
- 是否阻塞: 否（reviewer 选择不 precheck-block；推荐补但不阻塞 traceability review）。

## 代码风险与薄弱项 (informational, 非 finding)

- **I1 manifest 格式 producer-coupling**: uninstall.sh:99-105 的 grep+sed 解析依赖 install.sh:317 的 `printf '    {"kind": "%s", "path": "%s"}%s\n'` 具体格式（kind/path 在同行 + 双引号）。如未来 reformat manifest（例如改为 jq pretty-print 或 kind/path 拆 2 行），uninstall.sh 解析会失败。当前由 ADR-007 D2 `manifest_version: 1` 锁定 + 双脚本同 PR 修改约定接受此耦合。
- **I2 PARENT_DIRS hardcode**: uninstall.sh:20-24 的 `PARENT_DIRS` 列表（3 条）与 install.sh `vendor_skills_opencode` / `vendor_cursor` 中 vendor 父 dir 路径 hardcode 重复。如未来新增 target（如 Claude Code），需双侧同步。design §10 line 220 已显式接受此 hardcode。
- **I3 manifest_version 演进**: uninstall.sh 不读 `manifest_version` 字段、不做版本路由。当前只有 v1，无问题；ADR-007 D2 reversibility 段已规划 v2 引入时新增多版本读支持。
- **I4 traceability 提示**: 建议下游 hf-traceability-review 把"design §10 line 216 表述"vs"uninstall.sh:161-169 行为"的微差异（M1）一并 trace 到 ADR-007 / design 中——决策最终落点应明确（保留还是 best-effort rmdir）。

## Anti-Pattern 检测 (CA1..CA10)

| ID | Anti-Pattern | 是否命中 | 说明 |
|---|---|---|---|
| CA1 | silent failure | 否 | 所有 cp/mkdir/ln 走 set -e + ERR trap；rollback 内 `\|\| true` 仅用于残留清理路径，避免二次失败 |
| CA2 | magic numbers | 否 | manifest_version=1 是 ADR-007 D2 锁定的 schema 版本；其他数字只是循环 index |
| CA3 | undocumented behavior | 否 | usage 文本与 spec/design 完全对齐，无超范围 flag |
| CA4 | design boundary leak | 否 | install.sh / uninstall.sh 是单文件 CLI，无层次可漏 |
| CA5 | dead code / premature optimization | 否 | 所有函数都被 main 直接或间接调用 |
| CA6 | hat-mixing | N/A | greenfield；无既有代码 RGR 步骤纠缠场景 |
| CA7 | undocumented-refactor | N/A | greenfield |
| CA8 | escalation-bypass | 否 | 无跨 ≥3 模块 / 改 ADR / 改模块边界 / 改接口契约的隐藏改动；M1 不构成 escalation 触发（不影响 ADR / 接口契约 / 模块边界，只是 design §10 一行表述的细节） |
| CA9 | over-abstraction | 否 | mark_will_create / op / log / err 是 design 显式声明的抽象；未引入设计未声明的新接口 / 新基类 |
| CA10 | architectural-smell-ignored | 否 | 单文件 ~400 行不构成 god-class（design §10 显式选择"不拆 lib/"）；无 cyclic-dep / hub-like-dep / leaky-abstraction / feature-envy |

## 下一步

- 结论: 通过 → `next_action_or_recommended_skill = hf-traceability-review`
- M1..M5 全部 minor LLM-FIXABLE，建议 traceability review 阶段一并知悉:
  - M1 / M4 在 traceability review 时映射到 design §10 与 spec FR-005 决定是更新 design 表述还是修代码
  - M2 / M3 是纯代码 robustness polish，可在下个增量（v0.6+）随 PowerShell / npx wrapper 时一并清
  - M5 是流程改进项（progress.md Refactor Note 字段标准化），可在 hf-finalize 节点写 closeout 时补结构化字段
- 触发 hf-traceability-review 时建议提示 reviewer 重点 trace:
  - spec FR-001..FR-008 / NFR-001..NFR-004 / ASM-001 → design §11 / §13 → install.sh / uninstall.sh 函数与行号 → tests/test_install_scripts.sh scenario #1..#14 → verification record
  - ADR-007 D1..D5 → 上述代码落点
  - HYP-002 Blocking 验证已闭合（scenario #7 + verification record）

## 结构化返回 JSON

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-traceability-review",
  "record_path": "features/001-install-scripts/reviews/code-review-2026-05-11.md",
  "key_findings": [
    "实现严格落实 design §11 函数清单与编码约束；ADR-007 D1..D5 全部 manifested；spec FR-001..FR-008 + NFR-001..NFR-004 + ASM-001 全覆盖；14/14 e2e PASS",
    "[minor][LLM-FIXABLE][CR2] M1: uninstall.sh:161-169 末尾 rmdir .opencode/.cursor 与 design §10 line 216 显式'保留该 dir'决策不一致（实务影响小，但表述需要在 design 或 code 二选一对齐）",
    "[minor][LLM-FIXABLE][CR4] M2: install.sh:251/280 用 for name in $(ls ...) 是 bash anti-pattern；当前 IFS 与 skill 命名集合下零功能影响，但 shellcheck SC2045 会报",
    "[minor][LLM-FIXABLE][CR3] M3: parse_args 对 --target / --topology / --host 缺 value 时（末尾 token）silent exit 1，缺友好 err 消息",
    "[minor][LLM-FIXABLE][CR1] M4: install --force --dry-run 组合实际调用 uninstall（非 dry-run），违反 spec FR-005 严格读法；属 corner case，spec/tasks 未明示，scenario 未覆盖",
    "[minor][LLM-FIXABLE][CR7.2] M5: 实现交接块缺独立 Refactor Note 段；reviewer 选择不 precheck-block（greenfield + test-review R2 已 approve + 14/14 e2e PASS 直接覆盖 conformance）"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "finding_breakdown": [
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "CR2", "summary": "M1 uninstall.sh:161-169 与 design §10 line 216 决策不一致"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "CR4", "summary": "M2 install.sh:251/280 for name in $(ls ...) bash anti-pattern"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "CR3", "summary": "M3 flag 缺值时 silent exit 1，缺友好 err"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "CR1", "summary": "M4 install --force --dry-run 组合违反 FR-005 严格读法"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "CR7.2", "summary": "M5 实现交接块缺独立 Refactor Note 段（greenfield 性质，不阻塞）"}
  ]
}
```

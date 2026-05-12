# Design Review — 001-install-scripts (2026-05-11)

- Reviewer: 独立 reviewer subagent（cursor cloud agent 派发）
- Author of design under review: cursor cloud agent（hf-design 节点）
- Author / reviewer separation: ✅（不同会话）
- Design under review: `features/001-install-scripts/design.md`
- ADR under review: `docs/decisions/ADR-007-install-scripts-topology-and-manifest.md`（proposed）
- Approved spec basis: `features/001-install-scripts/spec.md`（approved 2026-05-11）
- Spec review record: `features/001-install-scripts/reviews/spec-review-2026-05-11.md`（Round 2 = 通过）
- Profile / Mode: `full` / `auto`
- Rubric: `skills/hf-design-review/references/review-checklist.md`
- Template: `skills/hf-design-review/references/review-record-template.md`

## 结论

需修改

理由摘要：设计层在结构、追溯、ADR 格式、候选方案对比、bash 3.2 编码约束、6 组合测试矩阵等维度均已达到 hf-tasks 输入门槛。Domain Strategic / Tactical / STRIDE 三个 phase 0 章节按"显式跳过 + 理由"处理且理由站得住，§5 Event Storming 含 sequence + Process Modeling Hotspot 表（full profile 要求满足）。然而存在 **2 条 important 设计逻辑缺陷**，会让 spec 内 FR-004 acceptance #1 与 NFR-002 acceptance 在实现时直接 FAIL，并不在规格漂移层面，是设计层一轮定向回修可关闭的内容缺口；外加 5 条 minor 收口。

## Precheck

| 检查项 | 结果 | 说明 |
|---|---|---|
| 存在稳定 design draft | ✅ | `design.md` 21 章节齐全，状态字段=草稿 |
| 已批准规格可回读 | ✅ | spec.md Round 2 verdict=通过；本 design §3 traceability 表所有锚点都能 dereference |
| ADR 已落盘 | ✅ | `docs/decisions/ADR-007-...md` 5 个 D 完整；状态=proposed；alternatives + reversibility 字段齐全 |
| route / stage / 证据一致 | ✅ | progress.md Current Stage=`hf-design`，无证据冲突 |

→ Precheck 通过，进入正式 rubric。

## 维度评分

| ID | 维度 | 分数 (0-10) | 备注 |
|---|---|---|---|
| `D1` | 需求覆盖与追溯 | 8 | §3 traceability 表覆盖 8 FR + 4 NFR + ASM-001；FR-007 verbose/默认两态承接的 `log()` 函数在 §10 component view 出现但 §11 未定义（minor finding 3）|
| `D2` | 架构一致性 | 7 | §10 C4 三层视图完整（Context text + Container 表 + Component 树）；§5 sequence + Process Modeling Hotspot；战略 / 战术 / STRIDE 三个 Phase 0 跳过的理由可冷读站得住；但 cursor target 把 `.cursor` 与 `.cursor/rules` 当作 INSTALLED 条目，对宿主已有 `.cursor/` 的常见情况未显式承接（minor finding 6）|
| `D3` | 决策质量与 trade-offs | 9 | §7+§8 三方案对比矩阵满足 design-doc-template.md 默认 7 列要求（核心思路 / 优点 / 代价 / NFR 适配 / Success Metrics 影响 / 可逆性）；ADR-007 5 个 D 都有 alternatives + reversibility；GoF 模式（Strategy/Factory/Adapter/Observer/Decorator/Builder/Singleton）未被前置决策（A11 反模式未触发，§6 选定的 "Plan-then-Apply" 是流程模式，不是 GoF）|
| `D4` | 约束与 NFR 适配 | 7 | §14 QAS 承接表覆盖全部 4 条 NFR + observability + 验证方法；§11 编码约束显式排除 mapfile / 关联数组 / `${var,,}` 等 bash 4+ 特性；ADR-006 D1 的 4 类子目录通过 `cp -R skills/` 整树自然兜住（FR-008）；但 `set -euo pipefail` 缺 `set -E (errtrace)` —— bash 3.2 ERR trap 不会跨函数边界传播，trap rollback 在 `vendor_skills_opencode()` 内部失败时可能不触发（minor finding 5）；NFR-002 中"半装回滚"在 partial cp -R 场景下设计不闭合（important finding 2）|
| `D5` | 接口与任务规划准备度 | 6 | §13 CLI 契约 + manifest schema + I1–I4 不变量明确；§18 拆出 T1–T10 对应 §16 测试矩阵；但 manifest entries 颗粒度（`dir:.opencode/skills` 单条）与 FR-004 acceptance #1 的"保留宿主自加 skill"在实现时直接冲突（important finding 1）；ADR-007 D5 readme 内容未在 design 任何位置具象（design.md 与 ADR-007 都只列字段标题，未给出最小内容样例）（minor finding 4）|
| `D6` | 测试准备度与隐藏假设 | 6 | §16 12 个 scenario 与 §18 task 一一映射；Walking Skeleton 最薄路径 = scenario #1；但 #7（user-skill 保留）与 #12（中途失败回滚）在当前 manifest+rollback 设计下会 FAIL（important finding 1+2 直接波及）；test #10 的 grep audit 没说明如何排除注释段（minor finding 7）；ASM-001 + `detect_hf_version` 对 CHANGELOG `[Unreleased]` 的处理实际上正确（regex `\[[0-9]+\.[0-9]+\.[0-9]+` 自然跳过 `[Unreleased]`），spec-review Round 2 提及的"design 节点处理 Unreleased 解析约定"问题实际已经无声闭合（不计入 finding，只在 coverage 段记录）|

按 review-checklist.md 评分辅助规则：D5 / D6 = 6 → 必须对应具体 finding，不得返回"通过"；D5 = 6 也意味着 hf-tasks 拿到当前设计会在 T7 / T8 任务定义上撞到含糊。

## 发现项

### Important

- [important][LLM-FIXABLE][D5][D6][A4] **Manifest entries 颗粒度过粗，与 FR-004 acceptance #1 + ADR-007 D2 自身 rationale 冲突**。
  - **Anchor**:
    - `design.md` §11 `vendor_skills_opencode()`（line 250–266）：copy topology 下 `ENTRIES+=("dir:.opencode/skills")` 只 push **一条** dir entry；
    - `design.md` §13 manifest schema example（line 384–390）同样只列 `{"kind":"dir","path":".opencode/skills"}` 单条；
    - `design.md` §10 uninstall.sh component view（line 198）`apply_removal()` "反向 rm；遇空目录回收"（"反向 rm" 对 `kind=dir` 自然译为 `rm -rf <dir>` 或等价语义，否则一条 dir entry 无法被回收）；
    - `spec.md` FR-004 acceptance #1（line 135）：install (opencode copy) → 手动放 `.opencode/skills/my-own-skill/SKILL.md` → uninstall → my-own-skill **必须仍存在**；
    - `design.md` §16.3 #7（line 452）也复述了同一验证；
    - `ADR-007` D2 Alternatives A2（line 47）显式拒绝"`uninstall.sh` 直接 `rm -rf .opencode/skills`"，rationale = "会误删宿主仓库自己加的 skills（违反 FR-004 acceptance #1）"。
  - **What**: 设计在 §11 / §13 manifest schema 上等价于 ADR-007 D2 Alternatives A2 已经拒绝过的形态——manifest 只记 `dir:.opencode/skills`，uninstall 拿这一条做反向清理时，要么 `rm -rf .opencode/skills`（删掉 my-own-skill）要么 `rmdir`（非空直接失败，留下整棵 HF skills 不被清理）。两条路径都至少违反 1 条 spec acceptance。
  - **Why**: (a) HYP-002（Blocking）的验证用例 #7 在当前设计下**无法 PASS**，hf-completion-gate 会卡住；(b) ADR-007 D2 自我矛盾——决策正文说"以 manifest 为唯一权威源避免 A2 误删"，但 manifest schema 落地形态与 A2 等价；(c) cursor target 同样在 §11 `vendor_cursor()`（line 282–286）有 `dir:.cursor/harness-flow-skills` 的同型粗粒度 entry，影响面是双 target 的 copy topology；(d) hf-tasks 在 T6 / T7 拿到当前 schema 会直接编出"用户自加 skill 被误删"的实现。
  - **Suggested fix**（任选其一，design.md 与 ADR-007 D2 同步落地）：
    1. **per-skill entries**：copy topology 下 `vendor_skills_*()` 把 `<HF_REPO>/skills/<name>/` 逐个枚举成 manifest entries（约 25 条 dir entry：`dir:.opencode/skills/hf-finalize` / `dir:.opencode/skills/using-hf-workflow` / ...）；uninstall 时按列表 `rm -rf` + 父 dir `rmdir --ignore-fail-on-non-empty`（或 `rmdir 2>/dev/null || true`）。my-own-skill 不在列表中所以保留，`.opencode/skills` 父 dir 因还含 my-own-skill 自然非空 → 不被回收，符合 FR-004 acceptance #1 + ADR-007 D2 rationale。
    2. **per-file entries**：粒度更细，manifest `entries[]` 列每个文件 + 每个 dir；卸载逐文件删 + 空目录回收；schema 体量上升一个数量级（v0.5.1 24 个 skill × N 文件可能上千条），对 NFR-001 ≤ 10s 影响需评估。
    3. **snapshot diff**：install 前快照宿主 `.opencode/skills` `find` 列表，install 后再 `find` 一次，diff 落 manifest；uninstall 用 diff 列表。最贴近 ADR-007 D2 rationale，但实现复杂度高。
    - 推荐方案 (1)，与 §11 `vendor_skills_*()` 现有结构最接近，TDD 改动最小。fix 后需要同步更新：§11 `vendor_skills_*()` 的 ENTRIES push 循环、§13 manifest schema example、ADR-007 D2 Alternatives A2 的 rationale 文字（让"manifest 是唯一权威源"在 schema 落地形态上自洽）、§16 scenario #1 / #3 / #5 的"manifest entries 含 …"验收文字。

- [important][LLM-FIXABLE][D4][D5][D6][A2][A4] **Rollback 设计在 partial `cp -R` 失败场景下不闭合，与 NFR-002 acceptance 冲突**。
  - **Anchor**:
    - `design.md` §11 `op()`（line 230–248）：`op CP "$1" "$2"` 调用即 `cp -R`，**失败前不会写 INSTALLED**；
    - `design.md` §11 `vendor_skills_opencode()`（line 250–266）：`op CP "$HF_REPO/skills" "$dest"` **执行后**才 `INSTALLED+=("dir:$dest")`；
    - `design.md` §11 `rollback()`（line 314–333）对 `kind=dir` 用 `rmdir "$path" 2>/dev/null || true`（注释 `# only if empty`）；
    - `spec.md` NFR-002 Acceptance（line 204）：模拟 cp 失败 → 宿主仓库回到 install 前状态、无残留 manifest；
    - `design.md` §16.3 scenario #12（line 457）复述同样验证。
  - **What**: 当 `cp -R` 在中途失败（磁盘满 / 权限错 / 部分子树已落盘）时，设计有两层失败放大——
    - **第一层**：`cp -R` 失败 → `set -e` 触发 → trap rollback 立即跑 → 但 `INSTALLED+=("dir:$dest")` 还**没执行**（因为它在 `op CP` 之后），所以 `INSTALLED` 里只有 `.opencode` 父 dir，没有 `.opencode/skills`；
    - **第二层**：rollback 对 `dir` 类条目仅做 `rmdir`（only if empty），即便 `.opencode/skills` 进入 INSTALLED，也因为半拷贝子树非空而 silently 留下残留（`|| true` 吞掉 rmdir 失败）。
    最终宿主仓库残留 partial `.opencode/skills/<半拷贝>`，违反 NFR-002 "宿主仓库回到 install 前状态"。
  - **Why**: (a) NFR-002 是 spec 锁定的 Must NFR，scenario #12 在当前设计下 PASS 不了；(b) 设计 §6 自己写了 "Plan-then-Apply" 模式（先 plan 后 apply），但 rollback 实际只回退 INSTALLED（apply 中已成功的部分），没有用 ENTRIES 计划列表做"覆盖式清理"；(c) `set -euo pipefail` 缺 `set -E` 让问题更糟（minor finding 5）：function 内的失败甚至可能完全不触发 trap，rollback 根本不跑。
  - **Suggested fix**（一并落到 §11 与 §17）：
    1. **预登记意图（recommend）**：把 `INSTALLED+=("dir:$dest")` 移到 `op CP` **之前**（"我即将创建 $dest"），rollback 时不论是否成功都尝试清理；同时把 dir 类条目的 rollback 改为 `rm -rf "$path"`（而非 rmdir-only），既能清掉 partial cp -R 子树、又对 ADR-007 D2 manifest 模型零影响（rollback 是 in-process 临时态，不读 manifest）。
    2. **并补 `set -Eeuo pipefail`**：bash 3.2 起 `set -E` 让 ERR trap 跨函数继承，否则 `vendor_skills_opencode()` 内部 cp 失败可能根本不触发 rollback。
    3. **§17 失败模式表新增一行**：`partial cp -R 残留` → `mitigation: rm -rf 而非 rmdir，预登记意图`，与 H1 hotspot（rollback 自身 rm 失败）形成完整故障树。
    4. fix 后 §16.3 scenario #12 的"宿主仓库回到 install 前状态"才能在 PASS / FAIL 上做出干净判决。

### Minor

- [minor][LLM-FIXABLE][D1][D5] **`log()` 函数在 §10 component view 出现但 §11 未给出实现，FR-007 verbose / 默认两态输出机制不可冷读**。
  - **Anchor**: `design.md` §10 component view（line 188）列 `log() / op() / err() [verbose / dry-run 抽象]`；§11 仅展示 `op()`（line 230–248）；FR-007 acceptance 要求 verbose 行数 > 24、默认行数 < 10（spec.md line 161）。
  - **What**: `op()` 当前定义只在 `VERBOSE=1 || DRY_RUN=1` 时打印，默认模式下完全静默——这意味着默认模式下 install **不打印任何 banner**，连"开始 / 结束"都没有；spec FR-007 要求默认 < 10 行（言外之意 > 0）。
  - **Why**: hf-tasks 拿到当前 §11 会以为只需要实现 `op()` + 一对 stage banner echo，但 banner 数量 / 形式 / 错误打印路径未定。
  - **Suggested fix**: §11 加一段 `log()` / `err()` 函数定义（建议：`log()` 总是打印一行 banner，无视 verbose；`err()` 总是打印到 stderr）；或在 §10 component view 注释里写"`log()` 默认输出 stage banner（开始 / 结束 / 错误），与 verbose 无关；`op()` 在 verbose 时额外逐操作输出"。

- [minor][LLM-FIXABLE][D5] **ADR-007 D5 readme 文件内容仅有字段标题，design 与 ADR 都未给出最小内容样例**。
  - **Anchor**: `ADR-007` D5 决策（line 86）："包含：本次 install 的 target / topology / hf_version / 4 条快速验证命令 / uninstall 命令 / 已知 vendor 路径下 cursor rule 引用方式"；`design.md` §10 Container view 行 `<host>/.harnessflow-install-readme.md` markdown（line 173）；§11 `write_readme()`（line 186）只占位。
  - **What**: D5 的核心 mitigation —— 用 readme 提示用户"`.cursor/harness-flow-skills/using-hf-workflow/SKILL.md` 才是正确引用（不是 `skills/...`）"—— 需要具体 markdown body，否则 hf-tasks 在 T7 / T10 拿不到 fixture。
  - **Suggested fix**: §13（接口契约）或 §11 `write_readme()` 段加一个最小 markdown 模板（约 30 行 fenced code block 即可），含 4 条 verify 命令骨架（`find ... -name SKILL.md | wc -l` / `cat .harnessflow-install-manifest.json` / `readlink .opencode/skills`（symlink 模式）/ `ls .cursor/rules/harness-flow.mdc`） + uninstall 命令 + cursor rule 路径提示。

- [minor][LLM-FIXABLE][D2][D4] **`set -euo pipefail` 缺 `set -E`（errtrace），bash 3.2 下 trap ERR 不会跨函数边界继承**。
  - **Anchor**: `design.md` §11 编码约束（line 225）"shebang `#!/usr/bin/env bash` + `set -euo pipefail`"；§11 rollback 段（line 315）`trap 'rollback' ERR INT TERM`。
  - **What**: bash 手册明确写道"`set -E` (errtrace) 让 ERR trap 在 functions / command substitutions / subshells 中继承"。没有 `set -E` 时，`vendor_skills_opencode()` 内部 `op CP` 失败 → cp 返回非 0 → set -e 让函数退出，但 ERR trap **可能不在父作用域触发**，rollback 不跑，半装状态留在宿主仓库。
  - **Why**: 这是 important finding 2 的放大因子；即便 finding 2 修了 INSTALLED 预登记，没有 `set -E` rollback 可能根本不执行。
  - **Suggested fix**: §11 编码约束改为 `set -Eeuo pipefail`；并在 §17 failure modes 表里把 H1 hotspot 关联到这条。

- [minor][LLM-FIXABLE][D5][D6] **Cursor target 把宿主常见已存在的 `.cursor/` 与 `.cursor/rules/` 当作 INSTALLED 条目，rollback 与 uninstall 行为对宿主已有内容缺乏显式承接**。
  - **Anchor**: `design.md` §11 `vendor_cursor()`（line 273–276）：`op MKDIR "$HOST/.cursor/rules"` + `INSTALLED+=("dir:$HOST/.cursor")` + `INSTALLED+=("dir:$HOST/.cursor/rules")`；rollback `rmdir 2>/dev/null || true` 在 dir 非空时静默不删（mitigation 自然但未文档化）；uninstall manifest entries 同型条目同样在 cleanup 时尝试 rmdir。
  - **What**: 宿主仓库在 install HF 之前**通常已经**有 `.cursor/` 与 `.cursor/rules/`（用户自己的 cursor 配置），脚本对"我装 HF 之前这些 dir 是否已存在"没有探测，导致 manifest 里 `dir:.cursor` 与 `dir:.cursor/rules` 在 uninstall 时尝试 rmdir 用户原有 dir。当前靠 rmdir non-empty 静默失败兜底，但 rationale 没写到 §17。
  - **Suggested fix**: §11 `vendor_cursor()` 加一个 `dir_pre_existed("$HOST/.cursor")` 判断，pre-existing dir **不**进 ENTRIES（manifest）也**不**进 INSTALLED（rollback）；或在 §17 显式写入"`.cursor` / `.cursor/rules` 若 install 前已存在，由 rmdir-non-empty 静默兜底"作为已知设计行为。

- [minor][LLM-FIXABLE][D6] **§16.3 test #10 grep audit 未说明如何排除注释 / 文档段，照字面执行会误报**。
  - **Anchor**: `design.md` §16.3 #10（line 455）：`grep -E '\b(jq|python|node|npm)\b' install.sh uninstall.sh` 排除注释 / 文档段后输出为空；`spec.md` NFR-004 acceptance 第 3 条（line 238）同样口径。
  - **What**: bash 注释行用 `#`，但 grep -E 不会自动过滤注释；test #10 字面执行会把任何注释里的 "python / node" 命中，false positive 让测试 FAIL。
  - **Suggested fix**: 把 audit 命令改为 `grep -E '\b(jq|python|node|npm)\b' install.sh uninstall.sh | grep -v '^[[:space:]]*#'` 或 `awk '!/^[[:space:]]*#/' install.sh uninstall.sh | grep -E ...`，并在 §16.3 #10 显式写出最终命令。

## 薄弱或缺失的设计点

- ASM-001 + `detect_hf_version()` 对 CHANGELOG `[Unreleased]` 的处理实际上**已经正确**：design.md line 301 的 regex `'^## \[[0-9]+\.[0-9]+\.[0-9]+'` 自然跳过 `## [Unreleased]`（`Unreleased` 不匹配 `[0-9]+`），spec-review Round 2 留下的"design 节点处理 Unreleased 解析约定"待办在事实上已闭合。建议在 ASM-001 落地段（§11 `detect_hf_version()` 注释）显式写一句"regex 设计自然跳过 `[Unreleased]`"，方便 reviewer 后续不用重新推理。**不计入 finding**。
- §11 `op CP` 用 `cp -R src dst`：BSD（macOS）与 GNU（Linux）/ busybox（alpine）三家 `cp -R` 在 dst 已存在时的拷贝 inline / nested 语义有微差。设计选择 dst 不预先存在（`mkdir -p` 仅做父 dir）规避了大部分差异，但跨发行版兼容性最后还要靠 NFR-003 / NFR-004 e2e 矩阵兜底。**不计入 finding**（已有 e2e 兜底）。
- §10 Container view 显式说明"不拆 `lib/install-common.sh`"——这意味着 install.sh 与 uninstall.sh 之间会重复 `parse_args` / `op` / `log` / `err`。是显式 trade-off，与 NFR-001 "用户单文件入口"立场一致；**不计入 finding**，但建议在 §17 或 §20 加一行"设计代价：install.sh 与 uninstall.sh 函数重复，trade-off 是单文件入口"，让维护者后续看到不重复评估同一问题。
- §13 manifest 不变量 I1（"path 都是 host-relative"）与 §16 scenario 验收的 "manifest entries[] 含 `dir:.opencode/skills`" 字面一致 ✅，但 §11 `vendor_skills_opencode()` 的 push 是 `ENTRIES+=("dir:.opencode/skills")`（OK），而 INSTALLED 用 absolute（OK，rollback 用绝对路径）—— 两个数组的路径形态不同，已隐式区分但建议在 §11 头部"关键全局变量"表里把 ENTRIES 与 INSTALLED 的路径形态显式标出，避免 hf-tasks 在 T6 实现 `write_manifest()` 时混淆。**不计入 finding**（implementation guidance）。

## 覆盖检查

| 维度 | 检查项 | 结果 |
|---|---|---|
| Hard Gates | 设计未通过评审前不得进入 hf-tasks | ✅ 当前 verdict=需修改，本 reviewer 不替父会话写 approval |
| Hard Gates | reviewer 不代替父会话完成 approval / 不拆任务 / 不写代码 | ✅ |
| 评审作者 / 审查者分离 | author / reviewer 来自不同会话 | ✅ |
| `D1` 需求覆盖与追溯 | 8 FR + 4 NFR + ASM-001 全部承接 | ✅（log() gap = minor finding 3）|
| `D2` 架构一致性 | C4 三层视图 / DDD 战略战术显式跳过+理由 / Event Storming Hotspot | ✅ |
| `D3` 决策质量 | ≥ 2 候选方案对比 / 7 列矩阵 / Success Metrics 影响 | ✅（A 选定理由命中 NFR-004）|
| `D3` GoF 反模式 (A11) | 设计未把 GoF 模式前置决策列入 | ✅（§6 选定 "Plan-then-Apply" 是流程模式 / 非 GoF；§11 函数命名是动作语义 / 非 pattern label）|
| `D4` 约束 / NFR | bash 3.2 编码约束清单 / 4 NFR QAS 承接 / observability | ⚠️ set -E 缺（minor finding 5）；rollback 闭合性（important finding 2）|
| `D5` 接口 / 任务规划准备度 | CLI 契约 / manifest schema / 不变量 / T1–T10 拆分 | ⚠️ manifest 颗粒度（important finding 1）；readme 内容样例（minor finding 4）|
| `D6` 测试准备度 / 隐藏假设 | 12 scenario / Walking Skeleton / 显式 ASM | ⚠️ scenario #7 + #12 在当前设计下 FAIL；grep audit 注释排除（minor finding 7）|
| Anti-Pattern A1 NFR 评估缺位 | §14 QAS 表全覆盖 | ✅ |
| Anti-Pattern A2 只审 happy path | §5.2 + §17 + scenario #12 涵盖错误路径 | ⚠️ rollback 设计本身在错误路径不闭合（important finding 2 即 A2 实例）|
| Anti-Pattern A3 无权衡文档 | §8 + ADR-007 D1–D5 显式 trade-off | ✅ |
| Anti-Pattern A4 SPOF 未记录 | manifest 是 uninstall 唯一权威源（已识别） | ⚠️ 但 schema 颗粒度让该 SPOF 失效（important finding 1 即 A4 实例）|
| Anti-Pattern A5 实现后评审 | 当前是 design 评审 / 实现尚未开始 | ✅ |
| Anti-Pattern A6 上帝模块 | §10 install.sh 函数列表职责单一 | ✅ |
| Anti-Pattern A7 循环依赖 | install.sh / uninstall.sh 互不依赖 | ✅ |
| Anti-Pattern A8 分布式单体 | 不适用（单脚本） | N/A |
| Anti-Pattern A9 task planning gap | §18 显式 T1–T10；但 important finding 1+2 会让 T6 / T7 / T8 拿到含糊输入 | ⚠️ 由 important finding 间接承接 |
| Anti-Pattern A10 tactical-model-absent | §4.5 显式跳过 + 5 条不触发条件理由 | ✅ |
| Anti-Pattern A11 upfront-gof-pattern | 见 D3 行 | ✅ |
| 失败模式 | §17 6 行覆盖主要失败 | ⚠️ 缺 partial cp -R 残留行（important finding 2 mitigation）|
| 任务规划准备度 | §18 task 拆分清晰 | ⚠️ T6 / T7 / T8 任务定义会被 important finding 1+2 影响 |
| C4 视图 | §10 Context + Container + Component 三层 | ✅ |
| 开放问题分类 | §21 显式 非阻塞 / 阻塞=无 | ✅ |
| bash 3.2 兼容性约束 | §11 编码约束清单 + ADR-007 D1 | ✅（set -E 是补强，不是违反；listed in minor finding 5）|

## 下一步

- 由 hf-design-review 返回的 verdict = `需修改`，下一节点 = `hf-design`
- 父会话需让 author 在 1 轮 hf-design 内修复 **2 条 important + 5 条 minor** 共 7 条 finding；其中 important 1（manifest 颗粒度）与 important 2（rollback 闭合性）需要同步更新 `design.md §11 / §13 / §16 / §17` + `ADR-007 D2 Alternatives A2 rationale 文字`，让 ADR 决策与 manifest schema 落地形态自洽
- 修复完成后回到 hf-design-review 复审；预计 1 轮即可达 `通过`，不需要 `hf-workflow-router` 介入（本批 finding 全部 LLM-FIXABLE，无 USER-INPUT，无 route / stage / 证据冲突）
- finding 全部 `LLM-FIXABLE`（0 USER-INPUT），author 在 cloud agent 模式下可自主完成修复，不需要预先向用户问询

## 记录位置

- `features/001-install-scripts/reviews/design-review-2026-05-11.md`

## 交接说明

- 本 verdict = `需修改`，按 `skills/hf-design-review/references/review-record-template.md` 默认表 `needs_human_confirmation = false`、`reroute_via_router = false`
- reviewer subagent 不代替父会话写入批准结论；本 review 完成后父会话应：
  1. 读取本 review record + 结构化返回
  2. 触发 `hf-design` 节点按 finding 回修
  3. 回修完成后再次派发独立 reviewer subagent 执行 `hf-design-review` 复审
  4. 复审 `通过` 后才发起 `设计真人确认`（auto 模式下父会话写 approval record）

## 结构化返回（供父会话使用）

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-design",
  "record_path": "features/001-install-scripts/reviews/design-review-2026-05-11.md",
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "key_findings": [
    "[important][LLM-FIXABLE][D5+D6+A4] manifest entries 颗粒度过粗（dir:.opencode/skills 单条），与 FR-004 acceptance #1 + ADR-007 D2 自身 rationale 冲突，scenario #7 在当前设计下 FAIL",
    "[important][LLM-FIXABLE][D4+D5+D6+A2+A4] rollback 设计在 partial cp -R 失败场景不闭合（INSTALLED 在 op 之后才 push + dir 仅 rmdir-only），违反 NFR-002 acceptance，scenario #12 在当前设计下 FAIL",
    "[minor][LLM-FIXABLE][D1+D5] log() 函数在 §10 component view 出现但 §11 未定义；FR-007 verbose / 默认两态输出机制不可冷读",
    "[minor][LLM-FIXABLE][D5] ADR-007 D5 readme 文件内容仅字段标题，design 未给出最小 markdown 样例；T7 / T10 缺 fixture",
    "[minor][LLM-FIXABLE][D2+D4] set -euo pipefail 缺 set -E（errtrace），bash 3.2 下 trap ERR 不跨函数继承，rollback 可能根本不触发",
    "[minor][LLM-FIXABLE][D5+D6] cursor target 把宿主常见已存在的 .cursor / .cursor/rules 当作 INSTALLED 条目，rollback 与 uninstall 对宿主已有内容缺乏显式承接",
    "[minor][LLM-FIXABLE][D6] §16.3 test #10 grep audit 未说明如何排除注释段，照字面执行会误报"
  ],
  "finding_breakdown": [
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "D5+D6+A4", "summary": "manifest entries 颗粒度与 FR-004 acceptance #1 冲突"},
    {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "D4+D5+D6+A2+A4", "summary": "rollback 设计在 partial cp -R 失败下不闭合"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D1+D5", "summary": "log() 函数未定义 / FR-007 输出机制不可冷读"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D5", "summary": "ADR-007 D5 readme 内容样例缺失"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D2+D4", "summary": "set -E 缺，trap ERR 不跨函数继承"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D5+D6", "summary": "cursor 宿主已有 .cursor 目录承接缺位"},
    {"severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D6", "summary": "test #10 grep audit 注释排除缺失"}
  ],
  "dimension_scores": {
    "D1_requirement_coverage": 8,
    "D2_architectural_consistency": 7,
    "D3_decision_quality": 9,
    "D4_constraints_and_nfr": 7,
    "D5_interface_and_task_planning_readiness": 6,
    "D6_test_readiness_and_hidden_assumptions": 6
  },
  "coverage_summary": {
    "precheck": "passed",
    "hard_gates": "passed (verdict=需修改 不进 approval / 不拆任务)",
    "author_reviewer_separation": "passed",
    "rubric_dimensions_applied": ["D1", "D2", "D3", "D4", "D5", "D6"],
    "anti_patterns_screened": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"],
    "phase0_chapters_check": {
      "domain_strategic_model_§4": "skipped with rationale (acceptable: single CLI tool, no multi-business concepts)",
      "tactical_model_§4_5": "skipped with rationale (acceptable: BC=1 / no multi-entity invariants / no concurrency / no domain events)",
      "event_storming_§5": "full profile satisfied (sequence + Process Modeling Hotspot table)",
      "nfr_qas_承接_§14": "passed (4/4 NFR mapped to 模块 / 机制 / observability / 验证)",
      "stride_§15": "skipped with rationale (acceptable: no Security NFR / no cross-trust-boundary / no auth / no PII)"
    },
    "adr_format_check": "ADR-007 5 D / Decision / Rationale / Alternatives / Reversibility 字段齐全",
    "candidate_solutions_check": "≥ 2 候选方案 (3 个: A 纯 bash / B Node / C Python) + 7 列对比矩阵 + Success Metrics 影响列",
    "gof_upfront_check": "passed (no Strategy / Factory / Adapter / Observer / Decorator / Builder / Singleton 列入)",
    "bash_3_2_compatibility_check": "passed in §11 编码约束清单；set -E 是补强项 (minor finding 5)",
    "open_questions_classification": "passed (§21 非阻塞 O-005 / O-006；阻塞=无)",
    "task_planning_readiness": "T1–T10 拆分清晰，但 T6 / T7 / T8 会被 important finding 1+2 间接影响",
    "test_matrix_coverage": "12 scenario (6 矩阵 + 6 额外) + Walking Skeleton 最薄路径 = scenario #1"
  },
  "verdict_rationale": "设计在结构 / 追溯 / ADR / 候选方案 / Phase 0 跳过理由 / bash 3.2 编码约束 / 6 组合测试矩阵等维度均达 hf-tasks 输入门槛；但 manifest 颗粒度（important 1）让 FR-004 acceptance #1 + HYP-002 Blocking 验证用例 #7 直接 FAIL，且与 ADR-007 D2 自身 rationale 自相矛盾；rollback 闭合性（important 2）让 NFR-002 acceptance + scenario #12 直接 FAIL。两条 important 均为 LLM-FIXABLE，1 轮定向 hf-design 回修可关闭，不构成阻塞。"
}
```

---

## Round 2 — 复审（2026-05-11，同日）

- 触发：父会话报告 author 已对 7 条 finding（2 important + 5 minor）做了定向回修
- 复审范围：仅检查 Round 1 findings 是否在 design.md / ADR-007 层面真实落实，并判断回修是否引入新 BLOCKER/MAJOR/important 问题；同时核查 scenario #7（HYP-002 Blocking 验证）与 scenario #12（NFR-002）在新设计下是否 PASSable
- 评审作者 / 审查者分离: ✅（同 reviewer subagent 跨轮复审在 HF 流程中允许；author 仍是 hf-design 节点，与 reviewer 不同会话）

### 逐条验证

| Finding | Severity | Status | 落地位置 | 验证结论 |
|---|---|---|---|---|
| #1 manifest entries 颗粒度 | important | ✅ Fixed（含 1 条 minor 残留 → R2-#1）| `design.md` §11 `vendor_skills_opencode()`（line 287–314）+ `vendor_cursor()`（line 317–349）+ §13 manifest schema example（line 455–462）+ §13 颗粒度段（line 466–471）+ ADR-007 D2 Alternatives A2 rationale（line 47） | copy topology 下 `for name in $(ls "$HF_REPO/skills")` 把每个 hf-* / using-hf-workflow 单独 `mark_will_create dir` + `op CP`，约 25 条 dir entries 进 ENTRIES；symlink topology 保持单条 `symlink:.opencode/skills`（用户自加 skill 在 symlink 拓扑下不可能存在，逻辑自洽）；§13 颗粒度段显式说明"用户后加 my-own-skill 不在列表所以保留 + 父 dir 因还含用户 skill 自然非空，rmdir 失败被静默兜底"——意图清晰；ADR-007 D2 A2 rationale 直接引用本评审的 important finding 1 名义并锁死 schema 必须 per-skill。**唯一残留**：§10 + §11 uninstall.sh `apply_removal()` 伪代码未显式区分"parent dir entry 用 rmdir-only"vs"leaf skill dir entry 用 rm -rf"——意图在 §13 段落清晰但实现细节没落到 §10/§11，TDD T7 实现 uninstall 时若按 §10 字面"反向 rm"全部 rm -rf 父 dir，scenario #7 仍会 FAIL。详见 R2-#1。 |
| #2 rollback 闭合性 | important | ✅ Fixed | `design.md` §11 编码约束（line 225）`set -Eeuo pipefail` + 显式 `set -E` rationale；§11 `mark_will_create()`（line 271–282）在 `op` 之前预登记 INSTALLED；§11 `rollback()`（line 376–401）dir 类用 `rm -rf "$path" 2>/dev/null \|\| true`（取代 rmdir-only）；§11 rollback 注（line 404–407）解释 set -E + mark_will_create + rm -rf 三者协同；§17 失败模式表新增 "Partial cp -R 残留" 行（line 590） | 三层闭合性都补齐：(a) `set -Eeuo pipefail` 让 ERR trap 跨函数继承；(b) INSTALLED 在 op 之前预登记，op 失败也能被 rollback 看到；(c) dir 类 rollback 用 rm -rf 能清掉 partial cp -R 残留子树。reviewer 走查 scenario #12 路径（详见下方"scenario PASS 性核查"段）确认 NFR-002 acceptance 在新设计下 PASSable。 |
| #3 log() / err() 未定义 | minor | ✅ Fixed | `design.md` §11 line 228–242 显式给出 `log()` 与 `err()` 函数体；§11 `op()` 段（line 232）注释明确 "log 默认总是打印 / op 仅 verbose 或 dry-run 时打印"，与 FR-007 acceptance 行数差异（默认 < 10 / verbose > 24）共同满足 | 函数职责显式：log → 总是打印 stage banner；err → 总是 stderr；op → 仅 verbose / dry-run。hf-tasks T1 拿到现在的 §11 不再需要猜默认模式有没有输出。 |
| #4 ADR-007 D5 readme 内容样例 | minor | ✅ Fixed | `design.md` §13 line 473–513 给出约 30 行 markdown sample，含 ISO 时间戳 / hf_version / hf_commit / target / topology 元数据 + 4 条 quick verify 命令（find SKILL.md / cat manifest / readlink symlink / ls .cursor rule）+ uninstall 命令 + cursor rule 路径提示 + ADR-007 D4 A3 deferred 说明 | 30 行 fenced markdown 完整可冷读；ADR-007 D5 决策文字中 "4 条快速验证命令" 全部对应得上；hf-tasks T6 / T10 拿到 fixture。 |
| #5 set -E 缺失 | minor | ✅ Fixed | `design.md` §11 编码约束 line 225 改为 `set -Eeuo pipefail` 并显式标 "`set -E` / errtrace 让 ERR trap 在 function / subshell 内继承——bash 3.2 起支持；缺少时函数内的失败不会触发父作用域的 trap rollback ERR，是 §11 rollback 闭合性的前置条件"；§11 rollback 注 line 406 再次锚定 set -E 与 rollback 闭合性的因果 | 与 finding 2 一并落地，rationale 显式书写让未来回看者不会再 strip 掉 -E。 |
| #6 cursor 宿主已有 .cursor / .opencode 承接 | minor | ✅ Fixed | `design.md` §11 `mark_will_create()` line 274–276 显式 `if [ "$kind" = "dir" ] && [ -d "$abs" ]; then return 0; fi` —— pre-existing dir 既不进 INSTALLED（rollback 不删）也不进 ENTRIES（uninstall 不删）；§17 line 594 新增失败模式行 "宿主仓库在 install 前已有 .cursor / .opencode" → "mark_will_create 检测 pre-existing dir，跳过 INSTALLED + ENTRIES 登记"；§11 rollback 注 line 407 重申 "rollback 不会误删用户的 .cursor / .opencode 等原有目录" | 关注点已闭合且写到 §17 让维护者后续可见；剩余的"pre-existing 同名 file / symlink 怎么办"是 spec 范围外的 corner（未要求处理），不计入 finding。 |
| #7 grep audit 注释排除 | minor | ✅ Fixed | `design.md` §16.3 #10 line 577：`(awk '!/^[[:space:]]*#/' install.sh uninstall.sh) \| grep -E '\b(jq\|python\|node\|npm)\b'` 输出为空 —— 显式 awk 剥离行首注释后再 grep；段尾备注 "minor finding 7 fix" 锚定追溯 | 命令字面可执行，false positive 风险消除；与 spec NFR-004 acceptance 第 3 条口径仍一致（spec 说"排除注释 / 文档段"，design 用 awk 实现"行首 # 注释"作为最小可落地解释——未处理行尾注释，但 install.sh / uninstall.sh 不预期有 `code  # python ...` 模式，可接受）。 |

### Scenario PASS 性核查（reviewer 走查模拟）

#### Scenario #7（user-skill 保留 / HYP-002 Blocking 验证）

走查 `install.sh --target opencode --topology copy --host /tmp/host` 路径：

1. `mark_will_create dir "$HOST/.opencode" ""` —— `.opencode` 不预存在 → 进 INSTALLED，rel 为空所以**不**进 ENTRIES
2. `op MKDIR "$HOST/.opencode"` 成功
3. `mark_will_create dir "$skills_root_abs" ".opencode/skills"` → INSTALLED + ENTRIES 都加
4. `op MKDIR "$skills_root_abs"` 成功
5. for-loop：每个 hf-* skill 单独 `mark_will_create dir "$skill_abs" ".opencode/skills/<name>"` → ENTRIES 累计约 25 条
6. write_manifest 落 entries[] 含约 26 条 dir entries（1 父 + 25 leaf）+ readme file 1 条

用户手动放 `<host>/.opencode/skills/my-own-skill/SKILL.md`。

运行 `uninstall.sh --host /tmp/host`：
- load_manifest 读出 ~27 条 entries
- apply_removal "反向 rm；遇空目录回收"
- **关键判断**：apply_removal 对每条 dir entry 做 rm -rf 还是 rmdir-only？设计 §10 / §11 uninstall 段**未显式区分**。两种字面解读：
  - (a) 全部 rm -rf：第一个被反向处理的可能是 readme file → ok；然后 leaf skill dirs 逐个 rm -rf → ok（用户的 my-own-skill 不在列表所以不被触及）；最后到 `.opencode/skills` 父 dir → **如果**做 rm -rf，会连同 my-own-skill 一起删 → **scenario #7 FAIL**
  - (b) 全部 rmdir-only：leaf skill dirs 非空 → rmdir 失败 → HF 内容残留 → scenario #1-#6 "uninstall 后 host 回到空状态" FAIL
  - (c) 按设计意图（§13 颗粒度段明文）：leaf 用 rm -rf，parent 用 rmdir-only；需要 uninstall 实现时识别 "本 entry 是否是其它 entry 的 path 前缀"。但 §10 / §11 没把这个区分逻辑写到伪代码里
- 结论：设计**意图**正确（§13 颗粒度段写明了 my-own-skill 保留 + parent rmdir 静默兜底），但 §10 + §11 uninstall 伪代码**没把意图落到 apply_removal 的具体形态**。一个 LLM TDD 写手按 §10 字面 "反向 rm" 实现，scenario #7 仍可能 FAIL；按 §13 颗粒度段实现则 PASS。

→ **PASSable but with implementation interpretation risk**。计入 R2-#1 minor finding。

#### Scenario #12（NFR-002 中途失败回滚）

走查 `install.sh --target opencode --topology copy --host /tmp/host`，setup 把 `<host>/.opencode` 预先 chmod 0500（readonly）：

1. `mark_will_create dir "$HOST/.opencode" ""` —— `.opencode` 预存在 → **return 0**，不进 INSTALLED / ENTRIES（mark_will_create line 274–276 pre-existing dir 跳过）
2. `op MKDIR "$HOST/.opencode"` —— mkdir -p 在已存在 dir 上 no-op 成功（不写入）
3. `mark_will_create dir "$skills_root_abs" ".opencode/skills"` —— `.opencode/skills` 不存在 → 进 INSTALLED + ENTRIES
4. `op MKDIR "$skills_root_abs"` —— **FAIL**（.opencode 只读，无法 mkdir 子 dir）
5. `set -Eeuo pipefail` + `set -E` 让 ERR trap 在 vendor_skills_opencode 函数内传播到父作用域 → trap rollback ERR 触发
6. rollback 反向迭代 INSTALLED：唯一一条是 `dir:$HOST/.opencode/skills`；执行 `rm -rf "$HOST/.opencode/skills" 2>/dev/null || true` —— 该 dir 实际不存在（mkdir 失败），rm -rf 静默成功
7. rollback 末尾 `rm -f .harnessflow-install-manifest.json` 与 `.harnessflow-install-readme.md`（都不存在）静默成功
8. `exit "$rc"` 退出码非 0
9. **最终态**：`.opencode/` 仍是用户原 dir（未被触及，因为 pre-existing skip）；无 `.opencode/skills`；无 manifest；无 readme → **= install 前快照**

→ **scenario #12 PASS**。NFR-002 acceptance "宿主仓库回到 install 前状态、无残留 manifest" 闭合。

### 回修是否引入新问题

逐项核查：

- **R2-#1 [minor][LLM-FIXABLE][D5] uninstall apply_removal parent vs leaf 区分逻辑未写到伪代码**：见上方 scenario #7 走查。`design.md` §13 颗粒度段（line 466–471）的意图清晰，但 §10 uninstall component view（line 198）"反向 rm；遇空目录回收"与 §11 没把"parent dir 用 rmdir-only / leaf dir 用 rm -rf"区分逻辑落到伪代码。**Suggested fix**：在 §11 加一段 `apply_removal()` 伪代码，明确"如果 entry path 是其它 entry path 的严格前缀 → 视为 parent，rmdir-only；否则 → leaf，rm -rf"，或在 §13 颗粒度段加一句"uninstall 时按 path 前缀关系自动识别 parent dir 用 rmdir-only"。**严重性 minor**：意图已在 §13 + 测试 acceptance 双向锚定，TDD 实现 scenario #7 RED 时会立即暴露字面误读，可在 hf-test-driven-dev T7 阶段自然收敛——不阻塞 hf-tasks 拆分。

- **R2-#2 [minor][LLM-FIXABLE][D5] `.opencode` 父 dir 在 install 时（非 pre-existing 场景）只进 INSTALLED 不进 ENTRIES，uninstall 不会清理，留下空 `.opencode` 残留**：在干净宿主 install opencode + uninstall 后，`<host>/.opencode/`（空）残留，违反 scenario #1-#6 "uninstall 后 host 回到空状态" 的字面口径。**根因**：mark_will_create 用 `rel=""` 区分"rollback 要管 / uninstall 不要管"，对 install 创建的 `.opencode` 父 dir 起作用——但这条选择让"clean uninstall 也要清父 dir"的需求落空。`design.md` §10 uninstall apply_removal 写有"遇空目录回收"，可以读作"递归向上对父 dir rmdir if empty"，但walk-up scope（停在哪？host 根？）没说。**Suggested fix**：在 §11 写明"apply_removal 处理完所有 entries 后，对每个 entry 的父 dir 反复 rmdir 2>/dev/null \|\| true 直到非空或到达 host 根"，或者把 `.opencode` 也用 rel 形式登记到 ENTRIES（与 R2-#1 同型由 uninstall 用 rmdir-only 识别）。**严重性 minor**：与 R2-#1 同源，可在 hf-test-driven-dev T7 阶段一并解决。

- **R2-#3 [minor][LLM-FIXABLE][D1] §3 traceability 表 FR-002 行函数名 stale**：`design.md` §3 line 32 仍写 "vendor_skills() + vendor_cursor_rule() 的 topology 分支"，但 §11 实际函数名是 `vendor_skills_opencode()` 与 `vendor_cursor()`。trivial wording 不一致。**Suggested fix**：§3 表 FR-002 行同步更新为 "vendor_skills_opencode() + vendor_cursor() 的 topology 分支"。

- **§3 traceability 表 FR-008 行**："§11 vendor_skills() 直接 cp -R skills/ 整树（自然包含 scripts/）"——同 R2-#3 stale，且 "整树" 描述与 round-2 fix 后 per-skill cp -R 不再字面成立。但每个 per-skill cp -R 仍包含该 skill 的 4 类子目录（SKILL.md / references/ / evals/ / scripts/），FR-008 acceptance "find <vendored>/hf-finalize/scripts -name '*.py' \| wc -l ≥ 1" 仍能 PASS。**不计入新 finding**（与 R2-#3 合并即可）。

- **§10 component view install.sh apply_plan 行 (line 184)**："实际 cp / ln / mkdir，逐项 push 到 INSTALLED 数组" —— 这与 §11 改为 mark_will_create 在 op 之前 push 不一致。**不计入新 finding**（属于 §10 文字未与 §11 同步的 trivial wording，§11 是 source of truth）。

- **`for name in $(ls "$HF_REPO/skills")`（§11 line 307 / 340）**：`$(ls)` 不引用、依赖默认 IFS word splitting；HF skill 命名约定无空格（hf-finalize / using-hf-workflow），所以实际 PASS。但 NFR-004 / spec §11 路径约定第 4 条 "脚本必须能正确处理含空格的宿主仓库路径" 关注的是宿主路径不是 HF 仓库内 skill 命名；$(ls) 在 HF 仓库内的使用不冲突。**不计入新 finding**（HF naming convention prevents the issue）。

- **`mark_will_create` 对 file / symlink kind 不做 pre-existence skip**：若用户碰巧已有 `.cursor/rules/harness-flow.mdc`（非常罕见），install 会覆盖，rollback / uninstall 会删用户文件。spec FR-006 通过 manifest 探测拦住"上次 HF install 残留"，但不拦"用户自有同名文件"。这是 spec 范围外的 edge case，spec 没要求处理。**不计入新 finding**。

- **`detect_hf_version()` 对 CHANGELOG `[Unreleased]` 的处理**：regex `^## \[[0-9]+\.[0-9]+\.[0-9]+` 自然跳过 `[Unreleased]`（验证：CHANGELOG line 7 = `## [Unreleased]`，正则不匹配；line 后续才有 `## [0.5.1]`）。设计实际正确，spec-review Round 2 留下的 design 待办在事实上闭合。**不计入新 finding**（可在 §11 注释中显式标记，但属 polish）。

### 新增问题汇总

| ID | Severity | Classification | Rule | 摘要 |
|---|---|---|---|---|
| R2-#1 | minor | LLM-FIXABLE | D5 | uninstall apply_removal parent vs leaf 区分逻辑未写到伪代码；意图在 §13 颗粒度段清晰但 §10/§11 字面 "反向 rm" 有 scenario #7 FAIL 风险 |
| R2-#2 | minor | LLM-FIXABLE | D5 | `.opencode` 父 dir 在 install 时只进 INSTALLED 不进 ENTRIES，uninstall 不清理，留下空 `.opencode` 残留；apply_removal "遇空目录回收" walk-up scope 未指定 |
| R2-#3 | minor | LLM-FIXABLE | D1 | §3 traceability 表 FR-002 / FR-008 行函数名 stale（vendor_skills() / vendor_cursor_rule() vs §11 实际 vendor_skills_opencode() / vendor_cursor()）|

无新 BLOCKER / MAJOR / important finding。

### 更新后维度评分

| ID | 维度 | Round 1 分数 | Round 2 分数 | 变化原因 |
|---|---|---|---|---|
| `D1` | 需求覆盖与追溯 | 8 | 8 | log()/err() 显式定义 (+); §3 函数名 stale (-)；净中性 |
| `D2` | 架构一致性 | 7 | 8 | mark_will_create 抽象 + pre-existing dir 显式承接 |
| `D3` | 决策质量与 trade-offs | 9 | 9 | 无变化；ADR-007 D2 A2 rationale 进一步显式锁定 per-skill 颗粒度 |
| `D4` | 约束与 NFR 适配 | 7 | 9 | set -Eeuo + rollback 三层闭合（mark_will_create + rm -rf + set -E）|
| `D5` | 接口与任务规划准备度 | 6 | 8 | per-skill 颗粒度 + readme 内容样例 + mark_will_create；R2-#1 / R2-#2 残留小幅扣分 |
| `D6` | 测试准备度与隐藏假设 | 6 | 9 | scenario #7 + #12 PASSable; grep audit 注释排除 |

所有维度 ≥ 8，无低于 6/10 维度 → 满足"通过"评分门槛（review-checklist.md 评分辅助规则：任一关键维度 < 6 不得返回通过）。

### 更新后 verdict

**通过**

理由：Round 1 提出的 2 important + 5 minor LLM-FIXABLE 共 7 条 finding 全部在 design.md / ADR-007 层面真实落实——manifest 颗粒度（important 1）由 `vendor_skills_*()` 的 per-skill `mark_will_create + op CP` 循环 + ADR-007 D2 A2 rationale 锁定；rollback 闭合性（important 2）由 `set -Eeuo pipefail` + mark_will_create 预登记 + dir 类 `rm -rf` 三层协同闭合。reviewer 走查确认 scenario #7（HYP-002 Blocking 验证用例）与 scenario #12（NFR-002）在新设计下均 PASSable。回修引入 3 条 minor 残留（uninstall apply_removal 伪代码 parent/leaf 区分不显式 / `.opencode` 父 dir uninstall 不清 / §3 函数名 stale），均为 LLM-FIXABLE，可在 `hf-test-driven-dev` T7 阶段自然收敛或由 author 在进入 approval 前一轮 polish 解决——不阻塞 hf-tasks 拆分，不构成"通过" 标准下的"阻塞任务规划的设计空洞"。

下一节点：`设计真人确认`（auto 模式下父会话写 approval record）→ `hf-tasks`。

**给 author 的可选 polish 建议**（非阻塞，approval 前可一并修；或直接由 hf-test-driven-dev T7 / T1 自然收敛）：

1. §11 加一段 `apply_removal()` 伪代码，明确 parent vs leaf dir 的区分（path 前缀关系）与对应 rmdir-only / rm -rf 选择
2. §11 在 apply_removal 段写明 "处理完 entries 后递归向上 rmdir 父 dir 直到非空或到达 host 根"，关闭 `.opencode` 空残留
3. §3 traceability 表 FR-002 / FR-008 行同步函数名为 `vendor_skills_opencode()` + `vendor_cursor()`
4. （可选）§11 `detect_hf_version()` 注释里加一句 "regex 自然跳过 `## [Unreleased]`"，方便后续维护者不重新推理

### Round 2 结构化返回（供父会话使用）

```json
{
  "round": 2,
  "conclusion": "通过",
  "next_action_or_recommended_skill": "设计真人确认",
  "record_path": "features/001-install-scripts/reviews/design-review-2026-05-11.md",
  "needs_human_confirmation": true,
  "reroute_via_router": false,
  "round1_findings_resolution": [
    {"id": "R1-#1", "severity": "important", "status": "Fixed", "anchor": "design.md §11 vendor_skills_opencode/vendor_cursor + §13 manifest schema + §13 颗粒度段 + ADR-007 D2 A2 rationale"},
    {"id": "R1-#2", "severity": "important", "status": "Fixed", "anchor": "design.md §11 set -Eeuo + mark_will_create + rollback rm -rf + §17 失败模式表"},
    {"id": "R1-#3", "severity": "minor", "status": "Fixed", "anchor": "design.md §11 line 228–242 log/err 显式定义"},
    {"id": "R1-#4", "severity": "minor", "status": "Fixed", "anchor": "design.md §13 line 473–513 readme 30 行 markdown sample"},
    {"id": "R1-#5", "severity": "minor", "status": "Fixed", "anchor": "design.md §11 编码约束 set -Eeuo + rollback 注 line 406"},
    {"id": "R1-#6", "severity": "minor", "status": "Fixed", "anchor": "design.md §11 mark_will_create line 274–276 pre-existing dir skip + §17 line 594"},
    {"id": "R1-#7", "severity": "minor", "status": "Fixed", "anchor": "design.md §16.3 #10 line 577 awk + grep"}
  ],
  "scenario_passability_check": {
    "scenario_7_user_skill_preserved": "PASSable with implementation-interpretation risk (intent clear in §13 颗粒度段 but apply_removal pseudocode in §10/§11 doesn't explicitly distinguish parent rmdir-only vs leaf rm -rf; covered by R2-#1 minor finding; TDD T7 RED test will catch any literal misread)",
    "scenario_12_partial_failure_rollback": "PASS (set -Eeuo lets ERR trap propagate from vendor_skills_opencode function; mark_will_create pre-registers .opencode/skills before op MKDIR fails; pre-existing .opencode/ skip preserves user dir; rollback rm -rf cleans tracked entries; manifest+readme never written; final host state == install 前快照)"
  },
  "new_findings_introduced": [
    {"id": "R2-#1", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D5", "summary": "uninstall apply_removal 伪代码 parent vs leaf dir 区分逻辑未写出，scenario #7 PASS 依赖 TDD 实现者按 §13 颗粒度段意图而非 §10 字面 '反向 rm'"},
    {"id": "R2-#2", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D5", "summary": ".opencode 父 dir 在 install 时只进 INSTALLED 不进 ENTRIES，uninstall 后留下空 .opencode 残留；apply_removal '遇空目录回收' walk-up scope 未指定"},
    {"id": "R2-#3", "severity": "minor", "classification": "LLM-FIXABLE", "rule_id": "D1", "summary": "§3 traceability 表 FR-002 / FR-008 行函数名 stale（vs §11 实际函数名）"}
  ],
  "harmless_residual_wording_noted_but_not_findings": [
    "§10 component view install.sh apply_plan 行字面 '逐项 push 到 INSTALLED 数组' 与 §11 mark_will_create 在 op 之前 push 不完全一致（§11 是 source of truth）",
    "§3 traceability 表 FR-008 '整树' 描述与 round-2 per-skill cp -R 不字面成立，但 FR-008 acceptance 仍可 PASS",
    "for name in $(ls $HF_REPO/skills) 不引用，依赖 HF 命名无空格的约定；与 spec §11 路径约定第 4 条 (宿主路径含空格) 不冲突",
    "mark_will_create 不对 file/symlink kind 做 pre-existence skip——spec 范围外 edge case，未要求处理",
    "detect_hf_version regex 实际正确跳过 [Unreleased]，但设计未在注释里显式标记"
  ],
  "dimension_scores_round2": {
    "D1_requirement_coverage": 8,
    "D2_architectural_consistency": 8,
    "D3_decision_quality": 9,
    "D4_constraints_and_nfr": 9,
    "D5_interface_and_task_planning_readiness": 8,
    "D6_test_readiness_and_hidden_assumptions": 9
  },
  "verdict_rationale": "7/7 R1 finding 在 design / ADR 层落实；2 important 的 PASS 性已通过 reviewer 走查确认（scenario #7 PASSable + #12 PASS）；3 条 R2 minor 全部 LLM-FIXABLE 且属 polish / TDD-resolvable，不构成阻塞任务规划的设计空洞；所有维度 ≥ 8，满足 review-checklist.md 评分门槛。设计已具备 hf-tasks 稳定输入条件。",
  "next_step_for_parent": "auto 模式下父会话写 design approval record (features/001-install-scripts/approvals/design-approved-YYYY-MM-DD.md)，把 ADR-007 状态从 proposed 翻为 accepted，同步 progress.md Current Stage = 设计真人确认 → 完成后 = hf-tasks，Pending Reviews 清掉 hf-design-review。可选 polish（R2-#1/#2/#3）由 author 选择 approval 前修或留给 hf-test-driven-dev 自然收敛。reviewer subagent 不代替父会话写入 approval。"
}
```

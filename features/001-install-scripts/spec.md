# HarnessFlow 安装脚本（Cursor / OpenCode）需求规格说明

- 状态: 草稿
- 主题: 为 HarnessFlow 增加可一键安装到任意宿主仓库的 install/uninstall 脚本，覆盖 Cursor 与 OpenCode 两种官方支持的客户端集成路径

## 1. 背景与问题陈述

HarnessFlow（HF）当前在 v0.5.1 已经官方支持 3 个 AI 编辑器/CLI 客户端：Claude Code、OpenCode、Cursor（`docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/cursor-setup.md`）。这 3 份 setup 文档对 OpenCode 与 Cursor 的"vendor 到自己仓库"路径，目前只给出**手动 shell 命令**的拓扑（`mkdir -p .opencode && cp -R ../harness-flow/skills .opencode/skills`、`mkdir -p .cursor/rules && cp ../harness-flow/.cursor/rules/harness-flow.mdc .cursor/rules/`）。

这种纯文档化的安装方式有 4 个具体痛点（来自 user 的同侪项目 `affaan-m/everything-claude-code` install 拓扑对比）：

1. **多步操作**：用户需要分别处理 skills 目录、rule 文件、可能的全局 `~/.config/opencode/skills`，错一步不会有清晰报错。
2. **无幂等保证**：第二次运行 `cp -R` 会覆盖宿主仓库内已修改的同名文件，但没有任何 dry-run 或 backup 提示。
3. **无卸载手段**：装完之后想退出，没有"我装了哪些文件、放在哪里"的 manifest，宿主仓库不知道哪些文件是 HF 装进来的。
4. **缺少跨拓扑兼容**：Cursor 期望 `.cursor/rules/` 与 `skills/`（rule 内部对 `skills/using-hf-workflow/SKILL.md` 与 `skills/hf-workflow-router/SKILL.md` 的相对引用），OpenCode 期望 `.opencode/skills/<name>/SKILL.md` 列表，两边的目录布局不同；当前手册要求用户**自己理解差异**。

ADR-006 D2 在 v0.5.1 已经正面承认过类似 vendoring bug（hf-finalize 的 `scripts/render-closeout-html.py` 误放在仓库根 `scripts/` 而非 `skills/hf-finalize/scripts/`，导致 vendoring 后 OpenCode 与 Cursor 都跑不通）。这次新增 install 脚本是把"vendoring 这件事本身"标准化、可逆化，把"要 cp 哪些文件、放在哪里"的隐性知识固化成可执行脚本。

## 2. 目标与成功标准

**高层目标**：让任何想在自己仓库里使用 HarnessFlow 的用户，能用**一条命令**完成 Cursor 或 OpenCode 集成；并能用**另一条命令**干净卸载，宿主仓库的 git 历史看到的 diff 就只有这次 install 实际放进去的文件。

**总体成功标准口径**：

- 在一个干净宿主仓库里跑 `install.sh --target cursor` 或 `install.sh --target opencode`（或 `--target both`）后，相应客户端的 verify 步骤（`docs/cursor-setup.md §3` / `docs/opencode-setup.md §2` 的"列出 24 个 hf-* + using-hf-workflow"）必须直接通过。
- 跑 `uninstall.sh` 之后，宿主仓库的 `git status` 显示**所有**install 阶段新建的文件都被删掉，且没有动到 install 阶段没动过的任何文件。
- 脚本的依赖闭包：bash 3.2+ 兼容（覆盖 macOS 默认 bash），主测 bash 4/5（Linux）+ POSIX coreutils；不要求宿主机器装 Node、Python、PowerShell、jq 等额外工具。具体兼容口径见 NFR-004。

## 3. Success Metrics

| 指标 | 阈值 | 测量方法 |
|---|---|---|
| Outcome Metric: install 一条命令完成率 | 在 `verification/` 目录下的端到端测试中，3 个 target（`cursor` / `opencode` / `both`）+ 2 种拓扑（`copy` / `symlink`）= 6 个组合，**全部** PASS | 新增 `skills/.../scripts/test_install.sh`（实际落点见 design 阶段决定）跑 6 个组合，verification record 必须有 6 条 PASS |
| Leading Indicator 1: install 后 setup 文档的 verify 步骤通过率 | install 完成后，立即满足"`find <vendored> -mindepth 2 -maxdepth 2 -name SKILL.md` 输出条数 ≥ 24，且包含 `using-hf-workflow` + `hf-workflow-router` 两个 SKILL.md"——这是 `docs/opencode-setup.md §2` / `docs/cursor-setup.md §3` verify 步骤的可执行等价口径（注意 `opencode-setup.md §2` 文本残留 v0.2.0 的"23 个" stale 表述，由本 feature 的 doc-freshness gate 一并修正） | 端到端测试脚本里直接用 `find` + `grep` 校验 |
| Leading Indicator 2: uninstall 后宿主仓库脏文件数 | `uninstall.sh` 完成后，比对 install 前后的 `find` 快照，install 阶段新建的文件 100% 被清理；非 install 阶段引入的文件 0% 被误删 | 端到端测试用 `find` + `diff` |
| Lagging Indicator: 文档冗余删除 | `docs/cursor-setup.md` 与 `docs/opencode-setup.md` 中"vendor by copying / symlink"段落的手动 `mkdir / cp -R / ln -s` 命令被替换为指向 `install.sh` 的单条命令；保留"为什么/troubleshooting"段落 | doc-freshness gate 时人工 / grep 校对 |
| Measurement Method | 端到端测试脚本（`features/001-install-scripts/verification/e2e-install-test.sh` 或等价位置）+ doc-freshness gate 的 grep 校对 |
| Non-goal Metrics | **不**度量：跨平台（Windows PowerShell、Git Bash）的兼容性；安装速度（不是性能 feature）；并发安装（同时往同一宿主仓库装 2 次的行为不在本轮范围）|
| Instrumentation Debt | install 脚本本身的 `--dry-run` 与 `--verbose` 输出格式作为唯一观测点；不接入任何外部 telemetry |

## 4. Key Hypotheses

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-001 | bash 4+ + POSIX coreutils 足以表达"copy 或 symlink HF skills 与 cursor rule 到指定路径"，无需 Node/Python | Feasibility | 必须重做技术选型（引入 Node/Python，违反"无新增运行时依赖"约束） | High（参考 `affaan-m/everything-claude-code` 也是 install.sh 入口；ECC 的 install.sh 是 wrapper 而非业务逻辑，但本场景业务逻辑显著更简单——仅 cp / ln / mkdir，纯 shell 完全足够） | TDD 阶段先写一个 minimal install.sh 跑通 `--target opencode --topology symlink`，验证 shell 层可表达 | 否（即便 false 也能切换技术栈，但本轮规格基于 shell 假设） |
| HYP-002 | 把"我装了哪些文件"写成 `.harnessflow-install-manifest.json`（或 `.txt`，design 阶段决定）放在宿主仓库根目录，是足够支撑幂等 + 卸载的最小机制 | Design | 卸载会变成"递归 rm 整个 .opencode/skills"，可能误删宿主仓库自己加的 skills | Medium（ECC 用 SQLite state store + `node scripts/uninstall.js`；HF 体量小得多，纯 manifest 足以） | TDD 阶段验证：先 install → 在 `.opencode/skills/` 下手动加一个非 HF skill → uninstall → 确认非 HF skill 没被删 | 是（如果 manifest 模型不成立，整个 uninstall 设计要重做）|
| HYP-003 | Cursor 与 OpenCode 两个 target 共享同一份"复制 skills/ 到目标位置"的核心逻辑，差异只在最终路径与是否额外放置 `.cursor/rules/harness-flow.mdc` | Design | 两个 target 必须分成独立子命令，install.sh 内部复杂度上升 | High（看现有 `docs/*-setup.md`，差异确实只是路径与是否放 mdc）| spec-review 阶段冷读两份 setup 文档对照确认；TDD 阶段两个 target 共用 install_skills() 函数验证 | 否 |
| HYP-004 | 宿主仓库**无需**任何 HF 仓库的 sibling clone；脚本可以在"用户先把 HF 仓库 clone 到临时位置 / 或脚本本身从 HF 仓库内被调用"两种模式下都工作 | Usability | 脚本只能在"先 clone HF 仓库"前提下工作，限制了使用场景 | Medium-High（设计上脚本运行时只需 SCRIPT_DIR 能解析到 `skills/` 与 `.cursor/rules/harness-flow.mdc` 即可；自身在 HF 仓库根目录就足够）| TDD 阶段两种模式各跑一次 | 否（即便 false，也只是退化到"先 clone HF"单一模式）|

无 Blocking 假设处于"未验证"状态：HYP-002 是 Blocking，但 confidence Medium、有明确 Validation Plan，会在 TDD 阶段第一个验证通过后才允许 hf-completion-gate 通过；若验证 fail，触发 hf-increment 重做 design。

## 5. 用户角色与关键场景

**主要用户**：HarnessFlow 的潜在使用者——已经在自己项目里使用 Cursor 或 OpenCode 作为 AI 协作工具，希望引入 HF 的 SDD/TDD/Review 工作流到现有仓库的工程师。

**关键场景**：

- **场景 A — 首次 vendor 进自己仓库（Cursor）**：工程师在自己仓库根目录，想把 HF 的 24 个 hf-* skills + cursor rule 装进去，不想看 3 段 setup 文档手动操作。期望：一条命令完成。
- **场景 B — 首次 vendor 进自己仓库（OpenCode）**：同上，但目标是 `.opencode/skills/`。期望：一条命令完成；并支持 symlink 模式（ECC 风格的 `ln -s`）以便后续跟随 HF 上游更新。
- **场景 C — 同一个仓库同时用 Cursor 和 OpenCode**：工程师团队里有人用 Cursor 有人用 OpenCode，希望两套同时装。期望：一条命令 `install.sh --target both` 完成。
- **场景 D — 卸载**：试用后决定不再用 HF，期望：一条 `uninstall.sh` 把所有 install 阶段放进来的文件清掉，不动其他文件。
- **场景 E — 重复 install**：第二次运行同一条 install 命令（修复 / 升级场景），期望：脚本检测到已存在的 manifest，要么 `--force` 覆盖，要么明确报错给用户选择，**不**静默覆盖。
- **场景 F — dry-run 预览**：装之前想看会动哪些文件，期望：`install.sh --dry-run --target cursor` 只打印计划不执行。

## 6. 当前轮范围与关键边界

**当前轮范围**：

- 提供 `install.sh`（bash）：`--target cursor|opencode|both` × `--topology copy|symlink` × `--dry-run` × `--verbose` × `--force` × `--host <path>`（省略 `--host` 时默认 cwd `.`）
- 提供 `uninstall.sh`（bash）：基于 install 阶段写的 manifest，反向清理；支持 `--dry-run` × `--host <path>`
- Manifest 落点：宿主仓库根目录的 `.harnessflow-install-manifest.json`（最终 schema 见 design）
- 复制范围（`--target cursor`）：`skills/` 整树 + `.cursor/rules/harness-flow.mdc`；按 ADR-006 D1 锁定的 4 类子目录约定一并搬运（含 `skills/<name>/scripts/`）
- 复制范围（`--target opencode`）：`skills/` 整树（落到 `.opencode/skills/`，并保留 SKILL.md 自身的相对引用）
- 与现有 `docs/cursor-setup.md` / `docs/opencode-setup.md` 的衔接：替换"手动 mkdir / cp / ln"段落为"用 `install.sh`"，保留 troubleshooting + 高级用户的手动 fallback
- shell 端到端测试覆盖：6 个组合（3 target × 2 topology）

**关键边界**：

- 脚本只在 HF 仓库根目录执行，或被符号链接调用（`SCRIPT_DIR` 自解析），不要求宿主仓库与 HF 仓库的相对路径关系
- 脚本只动 4 类目标路径之一：`<host>/.opencode/`、`<host>/.cursor/`、`<host>/.harnessflow-install-manifest.json`、（可选 global 模式：`~/.config/opencode/skills/`）
- 不动宿主仓库的 `git` / `.gitignore` / `package.json` / 任何 CI 配置

## 7. 范围外内容

明确不做（写入 `spec-deferred.md` 跟踪）：

- **Windows PowerShell `install.ps1`**：ECC 有，但 HF v0.5.x 文档并未承诺 Windows 一等支持；deferred 到 v0.6+。
- **Claude Code 的 install 脚本**：Claude Code 使用 `/plugin install` marketplace 机制，无需 vendor 脚本（`docs/claude-code-setup.md §1`）；明确 deferred / 不需要。
- **`npx hf-install` Node 包发布**：需要 npm publish 流程，超出本轮 shell-only 范围；deferred 到 v0.6+。
- **Global install（`~/.config/opencode/skills/` × 全局）的多 HF 版本共存管理**：本轮只支持 project-local 与 global "覆盖式"安装；多版本共存 deferred。
- **install 脚本对宿主 `AGENTS.md` 的写入或 merge**：本轮明确不动 `AGENTS.md`（与 `docs/opencode-setup.md` "Why no AGENTS.md sidecar?" 一致）。
- **install 脚本的 telemetry / 使用统计**：永不引入。
- **install 脚本调起 HF 自身 audit / lint**：deferred；audit 仍由 HF 仓库的 `scripts/audit-skill-anatomy.py` 在 HF 自身 CI 跑。

## 8. 功能需求

### FR-001 提供 `install.sh` 入口脚本

- 优先级: Must
- 来源: 用户请求"参考 ECC 给 hf 增加安装脚本"；HYP-001
- 需求陈述: 系统必须提供一个位于 HarnessFlow 仓库根目录的可执行 `install.sh`，接收 `--target cursor|opencode|both` 选项决定安装目标。
- 验收标准:
  - Given 用户在 HF 仓库根目录、宿主仓库为 `/tmp/host`，When 执行 `./install.sh --target opencode --host /tmp/host`，Then `/tmp/host/.opencode/skills/using-hf-workflow/SKILL.md` 存在且可读。
  - Given 同上，When 执行 `./install.sh --target cursor --host /tmp/host`，Then `/tmp/host/.cursor/rules/harness-flow.mdc` 存在，且 `/tmp/host/.cursor/harness-flow-skills/using-hf-workflow/SKILL.md`（或等价 vendor 路径，design 阶段决定）存在。
  - Given 同上，When 执行 `./install.sh --target both --host /tmp/host`，Then 上述两组路径同时满足。
  - Given 缺少 `--target`，When 执行脚本，Then 脚本以非 0 退出码并打印 usage 文本（含 3 个合法 target 值）。

### FR-002 支持 `copy` 与 `symlink` 两种 topology

- 优先级: Must
- 来源: 场景 B（用户希望 symlink 跟随上游更新）；HYP-003
- 需求陈述: 在 `--topology symlink` 下，系统必须将宿主目标路径创建为指向 HF 仓库内对应路径的符号链接；在 `--topology copy`（默认）下，系统必须执行 `cp -R` 复制。3 个 target × 2 个 topology = 6 个组合都必须满足本 FR；cursor / both target 在 symlink topology 下的语义继承自 opencode 同 topology（即 `.cursor/harness-flow-skills` 与 `.cursor/rules/harness-flow.mdc` 均为 symlink），详见 NFR-003 6 组合矩阵。
- 验收标准:
  - Given `--target opencode --topology symlink --host /tmp/host`，When 执行脚本，Then `/tmp/host/.opencode/skills` 是指向 HF 仓库根 `skills/` 的符号链接（`readlink` 能解析回 HF 仓库 `skills/`）。
  - Given `--target opencode --topology copy --host /tmp/host`，When 执行脚本，Then `/tmp/host/.opencode/skills` 是普通目录，且 `find /tmp/host/.opencode/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l` ≥ 24（HF 当前 24 个 hf-* + 1 个 using-hf-workflow ≥ 25；此处保守取 24 兼容未来增删）。
  - Given `--target cursor --topology symlink --host /tmp/host`，When 执行脚本，Then `/tmp/host/.cursor/harness-flow-skills`（或 design 决定的等价 vendor 路径）是指向 HF 仓库根 `skills/` 的符号链接，`/tmp/host/.cursor/rules/harness-flow.mdc` 是指向 HF 仓库 `.cursor/rules/harness-flow.mdc` 的符号链接。
  - Given `--target both --topology symlink --host /tmp/host`，When 执行脚本，Then 上述 opencode + cursor 的 symlink 用例同时满足。

### FR-003 写入 `.harnessflow-install-manifest.json` 记录所有放入文件

- 优先级: Must
- 来源: HYP-002；场景 D 卸载需要
- 需求陈述: install 完成后，系统必须在宿主仓库根目录写入 `.harnessflow-install-manifest.json`，记录本次 install 的 target、topology、HF 仓库版本锚点（git commit + 解析自 CHANGELOG 的 version）、放入或链接的所有文件/目录路径列表。在 ASM-001 失效场景下（HF 非 git checkout），`hf_commit` 字段降级为字符串 `unknown-non-git-checkout`，但 `hf_version` 字段必须仍能填充。
- 验收标准:
  - Given install 已成功完成（HF 是 git checkout），When 读取 `.harnessflow-install-manifest.json`，Then 文件存在，是合法 JSON，且包含字段 `manifest_version` / `installed_at` / `hf_commit`（git SHA）/ `hf_version`（从 CHANGELOG 解析）/ `target` / `topology` / `entries[]`（entries 数组每条至少含 `path` 与 `kind`，`kind ∈ {file, dir, symlink}`）。
  - Given install 是 symlink topology，When 读取 manifest，Then `entries[]` 中对应 `kind=symlink` 的条目存在。
  - Given HF 不是 git checkout（无 `.git/`，模拟从 zip 解压的场景），When install 完成，Then manifest `hf_commit` = `unknown-non-git-checkout`，`hf_version` 仍为合法版本号字符串（如 `0.5.1`）。

### FR-004 提供 `uninstall.sh` 反向清理

- 优先级: Must
- 来源: 场景 D；HYP-002
- 需求陈述: 系统必须提供 `uninstall.sh`，读取宿主仓库根的 `.harnessflow-install-manifest.json`，删除其中记录的所有 entries，最后删除 manifest 自身。
- 验收标准:
  - Given install 已成功；宿主仓库另外手动放了一个非 HF 文件 `/tmp/host/.opencode/skills/my-own-skill/SKILL.md`，When 执行 `./uninstall.sh --host /tmp/host`，Then manifest 中记录的所有路径被删除，且 `/tmp/host/.opencode/skills/my-own-skill/SKILL.md` 仍然存在。
  - Given 宿主仓库根没有 `.harnessflow-install-manifest.json`，When 执行 `./uninstall.sh --host /tmp/host`，Then 脚本以非 0 退出码并明确提示"未找到 manifest"。

### FR-005 支持 `--dry-run` 预览

- 优先级: Must
- 来源: 场景 F
- 需求陈述: install.sh 与 uninstall.sh 在 `--dry-run` 下必须打印将要执行的所有 mkdir / cp / ln / rm 操作，但**不**真实写入或删除任何文件。
- 验收标准:
  - Given 干净宿主仓库 `/tmp/host`，When 执行 `./install.sh --target both --dry-run --host /tmp/host`，Then 退出码 0，标准输出含 `mkdir /tmp/host/.opencode` 与 `mkdir /tmp/host/.cursor/rules` 等行，且 `/tmp/host/.opencode` 与 `/tmp/host/.cursor` 实际不存在。

### FR-006 重复 install 时要求 `--force` 才覆盖

- 优先级: Must
- 来源: 场景 E；HYP-002（manifest 模型支撑）
- 需求陈述: 当宿主仓库根已存在 `.harnessflow-install-manifest.json` 时，install.sh 必须默认拒绝继续；用户加 `--force` 时，必须先用 manifest 反向清理上次安装，再执行新 install。
- 验收标准:
  - Given install 已成功一次，When 不带 `--force` 再次执行 install，Then 脚本以非 0 退出码并提示"已检测到 manifest，使用 `--force` 覆盖"。
  - Given install 已成功一次，When 带 `--force` 再次执行 install，Then 第一次 install 留下的所有文件被清理，第二次 install 的内容正确就位，且 manifest 反映最新一次 install 的 entries。

### FR-007 提供 `--verbose` 详细输出

- 优先级: Should
- 来源: 通用工程实践（debug 友好）
- 需求陈述: 在 `--verbose` 下，脚本必须输出每一个文件 / 目录的 install 或删除操作（路径 + 操作类型）；默认非 verbose 时只输出阶段性 banner（开始 / 结束 / 错误）。
- 验收标准:
  - Given install 成功完成，When 带 `--verbose`，Then 标准输出行数 > 24（至少每个 hf-* skill 顶层目录一行）；不带 `--verbose`，Then 标准输出行数 < 10。

### FR-008 复制范围严格遵守 ADR-006 D1（4 类子目录）

- 优先级: Must
- 来源: ADR-006 D1（spec 第 1 节背景中已显式承认）；HYP-003
- 需求陈述: install.sh 在复制 `skills/` 时，必须把每个 `skills/<name>/` 下的 4 类子目录（`SKILL.md` / `references/` / `evals/` / `scripts/`）一并搬运；不允许 skip 任何一类。
- 验收标准:
  - Given install 完成（任一 target），When `find <vendored>/hf-finalize/scripts -name '*.py' | wc -l`，Then 输出 ≥ 1（v0.5.1 该 skill 至少 1 个 python 脚本）。
  - Given install 完成，When `find <vendored> -name SKILL.md | wc -l`，Then 输出 ≥ 24。

## 9. 非功能需求 (ISO 25010 + Quality Attribute Scenarios)

### NFR-001 Installability — 单条命令完成

- 类别: Portability / Installability
- 优先级: Must
- 来源: 总体成功标准；user 请求；HYP-001

QAS:
- Stimulus Source: HF 潜在使用者（工程师）在自己仓库根目录
- Stimulus: 执行 `bash <hf-repo>/install.sh --target opencode --host .`
- Environment: 宿主仓库为干净状态（既无 `.opencode/skills`，也无 `.harnessflow-install-manifest.json`）；机器有 bash 4+ 与 POSIX coreutils；HF 仓库已 clone 到本地任意位置
- Response: 完成 vendor，宿主仓库根多出 `.opencode/skills` 与 `.harnessflow-install-manifest.json`
- Response Measure: 单次命令退出码 = 0；命令链长度 = 1（不需要 user 在前后再跑别的脚本 / mkdir / cd）；操作总耗时 ≤ 10s（本地 SSD，假设 HF skills 总大小 < 5MB）

Acceptance:
- Given 干净宿主仓库 + 已 clone 的 HF 仓库；When 执行单条 `bash <hf-repo>/install.sh --target opencode --host <host>`；Then 退出码 0，且宿主仓库根可见 `.opencode/skills` 与 `.harnessflow-install-manifest.json`。

### NFR-002 Reliability / Recoverability — install 中途失败可恢复

- 类别: Reliability / Fault tolerance + Recoverability
- 优先级: Must
- 来源: 工程实践（中断恢复）；HYP-002

QAS:
- Stimulus Source: 操作系统 / 用户
- Stimulus: install 过程中收到 SIGINT（Ctrl+C）或某个文件 cp 失败（磁盘满 / 权限错）
- Environment: install 中途，部分文件已落盘，manifest **尚未**写完整
- Response: 脚本必须捕获错误，反向回滚本次 install 的 entries 集合，不留下"半装"状态污染宿主仓库（具体回滚机制——in-memory tracking 还是 staging manifest——由 design 决定）
- Response Measure: 中断后宿主仓库 `find <host> -newer <pre-install-snapshot>` 输出**等于** install 前状态；manifest **不**落盘（要么完整要么不存在）

Acceptance:
- Given install 进行到一半，When 模拟 cp 失败（target 路径设为只读）；Then 脚本退出码非 0，宿主仓库回到 install 前状态，无残留 manifest。

### NFR-003 Maintainability / Testability — shell 端到端测试

- 类别: Maintainability / Testability
- 优先级: Must
- 来源: HF 自身工程纪律（参考 `skills/hf-finalize/scripts/test_render_closeout_html.py` 模式）

QAS:
- Stimulus Source: HF 维护者 / CI
- Stimulus: 执行 `bash skills/<owner-skill>/scripts/test_install.sh`（实际落点 design 决定）
- Environment: 干净 CI / 本地 sandbox 中
- Response: 脚本以临时目录扮演 6 个 host scenario，对每一种 target × topology 组合分别 install + verify + uninstall + verify
- Response Measure: 6 个组合**全部** PASS；任一 fail 整体退出非 0；总运行时间 ≤ 120s（保证可频繁运行）

Acceptance:
- Given 干净环境；When 执行 e2e 测试脚本；Then 6 个 scenario 全 PASS，退出码 0，总耗时 ≤ 120s。

### NFR-004 Maintainability / Modularity — 不引入新运行时依赖

- 类别: Maintainability / Modularity
- 优先级: Must
- 来源: HYP-001；现有 HF 仓库依赖最小化原则（Python 仅用 stdlib，shell 仅用 POSIX）

QAS:
- Stimulus Source: HF 维护者 / 用户
- Stimulus: 在 macOS 默认 bash 3.2、Linux bash 4.x/5.x、安装了 POSIX coreutils 的 minimal Docker（如 `alpine` + `bash`）执行 install.sh
- Environment: 无 node、无 python、无 jq、无 brew/apt 安装的额外工具
- Response: 脚本能正常运行
- Response Measure: 在主测环境（Linux bash 4.x/5.x）下，6 个 e2e scenario **全部 PASS**（与 NFR-003 共享同一矩阵）；macOS bash 3.2 上同样 6 个 e2e scenario **全部 PASS**（不允许 SKIP，因为 install 的核心动作 cp/ln/mkdir 在 bash 3.2 下都成立）；脚本顶部 shebang `#!/usr/bin/env bash`；`set -euo pipefail`；脚本源码 grep 不到 `jq` / `python` / `node` / `npm` 调用（注释 / 文档段除外）

Acceptance:
- Given Linux bash 5.x 环境（CI 主测）；When 执行 NFR-003 的 6 个 e2e scenario；Then 6/6 PASS。
- Given macOS bash 3.2 环境（兼容性硬门槛）；When 执行 NFR-003 的 6 个 e2e scenario；Then 6/6 PASS（若设计阶段发现某个 scenario 在 bash 3.2 上无法成立，必须回 hf-specify 显式列出 SKIP 项与 SKIP 理由，不允许默写降级）。
- Given 任一环境；When 对脚本源码执行 `grep -E '\b(jq|python|node|npm)\b'`（排除注释 / 文档段）；Then 输出为空。

## 10. 外部接口与依赖（按需）

| 接口 / 依赖 | 类型 | 版本 / 兼容口径 | 失效影响 |
|---|---|---|---|
| bash | runtime | macOS 自带 bash 3.2 兼容；Linux bash 4+ / 5+ 主测 | 不兼容 → install 直接失败；需在脚本入口校验版本 |
| POSIX coreutils（cp / mkdir / ln / find / readlink） | runtime | POSIX.1-2017 子集 | 不兼容 → install 失败；alpine 默认是 busybox，需明确兼容 busybox `cp -R` 与 `ln -s` 行为 |
| HF 仓库自身 | source | 当前版本（v0.5.1+），ADR-006 D1 锁定的 4 类子目录约定 | 若 anatomy 再变（v0.6+），install 脚本要随之扩展 |

## 11. 约束与兼容性要求

- **ADR-006 D1**：HF skill anatomy v2 锁定 4 类子目录（`SKILL.md` / `references/` / `evals/` / `scripts/`），install 必须搬运全部 4 类。
- **ADR-005 D9 / ADR-004 D7**：HF 不自动执行 git tag / 不部署；install 脚本不动宿主仓库的 git。
- **HF 仓库依赖最小化**：不引入新运行时（NFR-004）。
- **路径约定**：脚本必须能正确处理含空格的宿主仓库路径（用 `"$VAR"` 引用所有路径变量）。

## 12. 假设与失效影响（按需）

承接 Key Hypotheses 中非 Blocking 假设：

- HYP-001 false → 切换到 Node/Python 实现，本规格的 NFR-004 失效，需要重写
- HYP-003 false → install.sh 内部按 target 分支增加，复杂度上升但仍在 shell 范围内
- HYP-004 false → 限制脚本仅支持"先 clone HF"模式

Blocking HYP-002 验证由 TDD 阶段完成，hf-completion-gate 之前必须有 PASS 证据。

### 运行环境假设（FR-003 衍生）

- **ASM-001**：HF 仓库默认是 git checkout（含 `.git/` 目录），FR-003 manifest `hf_commit` 字段从 `git rev-parse HEAD` 读取。失效场景：用户从 GitHub Releases 下载 source code zip 或 tarball（无 `.git/`）。失效时 install 脚本必须**仍能正常运行**（不允许 hard fail），manifest `hf_commit` 字段降级写入 `unknown-non-git-checkout`，同时 `hf_version` 字段从仓库根 `CHANGELOG.md` 顶部最新 `## [X.Y.Z]` 解析作为补偿锚点（以便 uninstall / 调试时仍能识别 HF 来源版本）。具体降级实现由 design 落到 FR-003 manifest schema。

## 13. 开放问题（区分阻塞 / 非阻塞）

**已关闭（spec 起草时直接收敛）**：

- 是否同时提供 `install.ps1`？→ 否（spec §7 deferred）
- 是否包装成 `npx`？→ 否（spec §7 deferred）

**非阻塞（design 阶段决定即可）**：

- O-001：manifest 是 JSON 还是 plain text？JSON 对 `kind=symlink` 等 metadata 表达更好，但写入 / 读取需要 stdlib 可用的 shell 实现（不能 jq）。**design 决定**。
- O-002：Cursor target 下，`skills/` 在宿主仓库的 vendor 路径选哪个？`docs/cursor-setup.md §1.B` 给出 `.cursor/harness-flow-skills` symlink 与 `cp -R skills .cursor/harness-flow-skills` 两种；本脚本默认选哪个？**design 决定**。
- O-003：global install（`--host ~/.config/opencode/skills`）是否走同一脚本？还是单独 flag `--global`？本轮范围内允许，但 spec §6 明确"4 类目标路径"包含可选 global 模式；design 决定 flag 形态。
- O-004：测试脚本的 owner skill——本 install 工具不属于任何已有 hf-* skill，按 ADR-006 D1 应放在哪里？候选：（a）放在仓库根 `scripts/`（v0.5.1 已收紧"跨 skill 维护者工具"语义，本 install 工具是否属于"跨 skill"？）；（b）新建 `tools/install/`；（c）新建 skill `hf-install`（过度，spec §7 已 defer "Claude Code 用 marketplace、不需要"）。**design 决定**。

**阻塞（送 review 前必须关闭）**：无。

## 14. 术语与定义（按需）

- **Vendor / Vendoring**：把第三方代码（这里是 HF skills + cursor rule）复制或符号链接进自己的仓库的过程。
- **Topology**：本规格特指 install 时"`copy` vs `symlink`"两种放置策略。
- **Target**：本规格特指 install 的目的客户端集成 —— `cursor` / `opencode` / `both`。
- **Host repo**：被装入 HF 的宿主仓库（与 HF 仓库本身区分）。
- **Manifest**：宿主仓库根的 `.harnessflow-install-manifest.json`，记录本次 install 实际放入的所有 entries，是 uninstall 的唯一权威源。

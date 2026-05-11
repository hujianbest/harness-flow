# ADR-007 — Install Scripts: Topology & Manifest

- 状态: proposed
- 日期: 2026-05-11
- Feature: `features/001-install-scripts/`
- Spec: `features/001-install-scripts/spec.md`
- 决策者: cursor cloud agent（hf-design 节点；按 ADR 模板格式记录关键决策）
- 关联 ADR:
  - ADR-006 D1 / D2（HF skill anatomy v2 + vendoring fix）—— 本 ADR 把 ADR-006 D1 锁定的 4 类子目录（`SKILL.md` / `references/` / `evals/` / `scripts/`）一并搬运的约束变成 install 脚本的 invariant
  - ADR-005 D9 / ADR-004 D7（HF 不自动 git tag / 不部署）—— 本 ADR 立场：install 脚本不动宿主仓库的 git / CI

## 1. Context

HF 当前 v0.5.1 已经官方支持 3 个客户端（Claude Code / OpenCode / Cursor）。Cursor 与 OpenCode 的"vendor 进自己仓库"路径在 `docs/cursor-setup.md §1.B` 与 `docs/opencode-setup.md §1.B / §1.C` 中只给出**手动 shell 命令**，没有任何脚本化入口。

本 ADR 决定 install 脚本的 5 个关键设计决策（其余次要细节由 design.md 直承）。

## 2. Decision

### D1：脚本运行时 = 纯 bash + POSIX coreutils，不引入新运行时依赖

**决策**：install.sh 与 uninstall.sh 用 bash 3.2+ 兼容写法，仅依赖 POSIX coreutils（cp / mkdir / ln / find / readlink / cat / grep / awk / sed），不调用 jq / python / node / npm / PowerShell。

**理由**：
- HF 仓库自身依赖最小化（CHANGELOG、scripts、skills 全部 stdlib-only）
- 用户已经有 Cursor / OpenCode 客户端，不应被强制装第二个运行时
- 同侪项目 ECC 的 install.sh 也是 wrapper to Node，但本场景业务逻辑显著更简单（仅 cp / ln / mkdir + JSON 写入），shell 完全够用

**Alternatives considered**：
- A1: Node script（参考 ECC `scripts/install-apply.js`）—— 拒绝：违反"无新增运行时依赖"约束（NFR-004），且引入 npm 生态包体积
- A2: Python stdlib（参考 `skills/hf-finalize/scripts/render-closeout-html.py`）—— 拒绝：macOS 兼容性更好，但 install 脚本"被运行的环境"比"HF 仓库内被运行的脚本"更不可控（不能假定有 python3）
- A3: bash 4+ 强制（拒绝 macOS bash 3.2）—— 拒绝：把 macOS 默认 bash 用户挡在门外，影响显著

**Reversibility**：高（如果 HYP-001 后续被证伪——比如 manifest 复杂到 stdlib shell 无法表达——可以重新评估切换 Python；shell 实现作为 fallback 仍可保留）

### D2：宿主仓库根的 `.harnessflow-install-manifest.json` 作为唯一安装权威源

**决策**：install 完成时在宿主仓库根目录写一份 JSON manifest，记录本次 install 的所有 entries（path + kind ∈ {file, dir, symlink}）+ 元数据（manifest_version / installed_at / hf_commit / hf_version / target / topology）。uninstall 严格基于 manifest 反向清理，不做"递归 rm -rf .opencode/skills"。

**理由**：
- 区分"HF 装进来的"vs"宿主仓库自己加的"的唯一可靠机制（FR-004 acceptance #1 即验证此场景）
- 解决 ECC 同类问题的 SQLite state store 是本场景的过度设计；JSON 文件足够
- manifest 在宿主仓库根可见，对 reviewer / CI / git 友好

**Alternatives considered**：
- A1: SQLite state store（参考 ECC v1.9.0 `scripts/state-store.js`）—— 拒绝：HF 体量显著小，单 feature install 工具不应引入 SQLite 依赖
- A2: 不写 manifest，uninstall 直接 `rm -rf .opencode/skills .cursor/rules/harness-flow.mdc`—— 拒绝：会误删宿主仓库自己加的 skills（违反 FR-004 acceptance #1）。本 ADR D2 选定的 manifest schema **必须**做到 per-skill 颗粒度（每个 hf-* / using-hf-workflow 在 entries[] 中作为单独 dir entry），uninstall 按 entries[] 列表逐 skill `rm -rf`，宿主自加 skill 不在列表中所以保留——若 schema 退化到只记 `dir:.opencode/skills` 单条粗粒度 entry，本 ADR 与 A2 等价（这是 hf-design-review 2026-05-11 important finding 1 的成因，已在 design.md §13 manifest 颗粒度段 + §11 `vendor_skills_*()` 落地修复）
- A3: manifest 落到 `.harnessflow/` 子目录而非 dotfile—— 拒绝：dotfile 更接近 `.gitignore` / `.editorconfig` 约定，单文件更易 grep / 检查

**Reversibility**：中（manifest schema 变更需要 migration；本 ADR 把 schema 锁在 `manifest_version: 1`，未来 schema 升级时新增 `manifest_version: 2` 并在 uninstall.sh 中支持 N 个版本同时读）

### D3：JSON 写入用纯 shell（不依赖 jq）；读取用最小 grep + sed 解析

**决策**：JSON manifest 写入由 install.sh 内部 `printf` 拼接成形（manifest schema 字段集小且固定，不构造嵌套）；uninstall.sh 读取用 `grep -oE` + `sed` 提取 entries 数组（不需要完整 JSON parser）。

**理由**：
- 直接配合 D1（不引入 jq 依赖）
- manifest schema 受控扁平（`entries[]` 内每条只有 `path` + `kind` 两字段），不需要通用 parser
- 添加 `manifest_version` 让未来 schema 演进有路径

**Alternatives considered**：
- A1: 用 `jq`—— 拒绝（违反 D1）
- A2: manifest 写成 plain text（每行 `<kind>\t<path>`）—— 拒绝：spec FR-003 acceptance 显式要求"合法 JSON"，且 JSON 对人类与机器都更友好
- A3: 用 python 包装（仅 manifest 读写时调用）—— 拒绝（违反 D1）

**Reversibility**：高（如果未来发现纯 shell JSON 写法在某个 corner case 出错，可以增加 `--json-tool jq|shell` flag 选择实现，default 保持 shell）

### D4：Cursor target 的 vendor 路径 = `<host>/.cursor/harness-flow-skills`（symlink 或目录），rule = `<host>/.cursor/rules/harness-flow.mdc`

**决策**：Cursor target 下，HF skills 树落到 `<host>/.cursor/harness-flow-skills/`（与 `docs/cursor-setup.md §1.B` 给出的"or symlink under .cursor/harness-flow-skills"一致）；同时把 HF 仓库的 `.cursor/rules/harness-flow.mdc` 复制（或 symlink）到 `<host>/.cursor/rules/harness-flow.mdc`。

**理由**：
- 与现有 cursor-setup.md §1.B 文档约定一致，install 脚本本身**不**改变 vendor 路径约定
- `.cursor/harness-flow-skills` 命名前缀显式表明"HF 装的"，与宿主仓库自己 `.cursor/rules/*.mdc` 不冲突
- rule 文件内的相对引用 `skills/using-hf-workflow/SKILL.md` 在 vendor 之后失效——这是 ADR-006 D2 修过的同源问题；本 ADR 决定**不**在 install 阶段重写 rule 内的路径，而是用 D5 的 post-install README 提示用户用"`.cursor/harness-flow-skills/using-hf-workflow/SKILL.md`"作为正确引用（cursor-setup.md §2 要求的 rule 内容会在 doc-freshness gate 一并修正）

**Alternatives considered**：
- A1: 把 skills 直接复制到 `<host>/skills/`（与 HF 仓库根布局一致）—— 拒绝：会污染宿主仓库的根目录命名空间，可能与宿主仓库自己的 `skills/` 目录冲突
- A2: install 时同时在宿主仓库根创建一个 `skills/` symlink 指向 `.cursor/harness-flow-skills/`——拒绝：把判断"宿主仓库是否已有自己的 skills/"的复杂度引入 install 脚本，超出本轮范围
- A3: 把 rule 内的相对路径在 install 时重写为 `.cursor/harness-flow-skills/...`—— 推迟到下个增量（spec-deferred 候选）：本轮先用 D5 的 README 提示规避

**Reversibility**：中（A3 路径重写如果未来要做，需要 sed 替换 rule 文件，但 manifest 仍能 track 到该文件——uninstall 依然能清干净）

### D5：install 完成后在 manifest 同目录写一份 `.harnessflow-install-readme.md` 作为给宿主仓库工程师的简短入口提示

**决策**：install 完成时除 manifest 外，再写一份 `.harnessflow-install-readme.md`（约 30 行 markdown），包含：本次 install 的 target / topology / hf_version / 4 条快速验证命令 / uninstall 命令 / 已知 vendor 路径下 cursor rule 引用方式。

**理由**：
- 给宿主仓库工程师一个单文件入口（不用回 HF 仓库翻文档）
- 在 D4 描述的"rule 内相对路径"问题上提供 in-place 提示
- 与 manifest 一起作为 install 阶段唯一两个非 vendor 文件，uninstall 时一并清理

**Alternatives considered**：
- A1: 不写额外 readme，依赖宿主工程师回 HF 仓库 docs—— 拒绝：违反 NFR-001 "单条命令完成"的体验目标
- A2: 把 readme 写到 `<host>/docs/harnessflow.md`—— 拒绝：会污染宿主仓库的 docs 命名空间，且需要先 mkdir docs

**Reversibility**：高（readme 内容变更不影响 manifest schema；uninstall 严格按 manifest 清理）

## 3. Consequences

### 正面

- 单一脚本入口（`install.sh` + `uninstall.sh`）覆盖 6 个安装组合，对宿主工程师极简
- manifest-based uninstall 不会误删宿主仓库自己加的 skills
- 不引入新运行时依赖，对 NFR-004 形成 enforcement 锚点
- 与现有 docs/cursor-setup.md / docs/opencode-setup.md 的 vendor 路径约定一致，不破坏既有文档
- 给未来扩展（PowerShell / npx wrapper / global multi-version）保留路径

### 负面 / 已知 trade-offs

- 纯 shell JSON 写入对 schema 演进不如 jq 灵活（mitigation：用 `manifest_version` 字段 + 锁定字段集）
- bash 3.2 兼容意味着不能用 `mapfile` / `[[ -v ]]` 等 4+ 特性（mitigation：CI 中加 `bash --version` 检查；NFR-004 acceptance 已锁双环境 6/6 PASS）
- D4 决定不在 install 阶段重写 rule 路径，可能让宿主用户首次使用时仍需要看 README 提示（mitigation：D5 的 readme 提示 + 后续增量）

### 中性观察

- 本 ADR 不引入对 HF release 流程的任何变化（install 脚本与 hf-release 解耦）
- install 脚本本身不进入 HF skill 体系（不是一个 hf-* skill），而是仓库根级 maintainer 工具——按 ADR-006 D1"仓库根 `scripts/` 收紧为跨 skill 维护者工具"的精神，install/uninstall 脚本的合适落点是仓库**根目录**（`./install.sh` / `./uninstall.sh`），与 ECC 同源

## 4. Implementation Notes

- install.sh / uninstall.sh 落仓库根（与 ECC 一致；ADR-006 D1 收紧"仓库根 scripts/"是指 python 工具，shell 入口脚本仍允许在根目录）
- 端到端测试脚本：落到仓库根 `tests/` 子目录或 `scripts/test_install_scripts.sh`——design.md §16 决定具体落点
- CHANGELOG 记入下一个 Unreleased 段；本 feature 完成后由 hf-release 在下一个 vX.Y.Z 时一并发布

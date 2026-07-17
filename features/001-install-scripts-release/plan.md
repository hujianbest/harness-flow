# Install Scripts Release 计划

- 日期: 2026-07-07
- frame: ./frame.md

## 1. 需求

### FR-1: 恢复仓库验证基线
- 优先级: 必须
- 描述: 在实现安装脚本前，当前仓库的技能校验与门禁脚本测试必须能以真实命令通过。
- 验收标准:
  - Given 当前工作区存在空的旧 skill 目录 When 运行 `python scripts/validate_skills.py` Then 校验不得因为空目录缺少 `SKILL.md` 而失败。
  - Given 基线已恢复 When 运行 `python scripts/validate_skills.py && python -m unittest skills/hf-workflow/scripts/test_hf_gate.py` Then 命令退出码为 0。

### FR-2: 提供 Cursor 安装脚本
- 优先级: 必须
- 描述: 使用者可以用脚本把 HarnessFlow 安装到目标项目的 Cursor 配置中，使 Cursor 能加载规则和 vendored skills。
- 验收标准:
  - Given 一个空的目标项目 When 执行 Cursor 安装命令 Then 目标项目包含 `.cursor/rules/harness-flow.mdc` 与 `.cursor/harness-flow-skills/`。
  - Given 已安装到 Cursor 的目标项目 When 再次执行同一安装命令 Then 脚本保持幂等，不破坏已有用户文件。
  - Given Cursor 规则被安装到目标项目 When 读取规则内容 Then 规则中的 skill 入口指向 `.cursor/harness-flow-skills/hf-workflow/SKILL.md`，而不是假设目标项目根目录已有 `skills/`。

### FR-3: 提供 OpenCode 安装脚本
- 优先级: 必须
- 描述: 使用者可以用脚本把 HarnessFlow 安装到目标项目的 OpenCode skill 目录中，使 OpenCode 能发现 `SKILL.md` 文件。
- 验收标准:
  - Given 一个空的目标项目 When 执行 OpenCode 安装命令 Then 目标项目包含 `.opencode/skills/` 且其中有 HarnessFlow 的 skill 目录。
  - Given 目标项目已有用户自定义 `.opencode/skills/custom-skill/SKILL.md` When 执行 OpenCode 安装命令 Then 用户自定义 skill 不被删除或覆盖。
  - Given 已安装到 OpenCode 的目标项目 When 再次执行同一安装命令 Then 脚本保持幂等。

### FR-4: 同步文档与版本发布材料
- 优先级: 必须
- 描述: README、中文 README、变更记录和插件元数据应说明安装脚本入口，并准备一个新的 release 版本切片。
- 验收标准:
  - Given 用户阅读 README When 查看安装章节 Then 能看到 Cursor 与 OpenCode 的脚本安装命令。
  - Given release 元数据更新完成 When 读取 `.claude-plugin/plugin.json` 与 `.claude-plugin/marketplace.json` Then 版本和描述与本次安装脚本能力一致。
  - Given changelog 更新完成 When 读取 `CHANGELOG.md` Then `[Unreleased]` 清空并新增本次 release 段，底部比较链接包含新版本。

### 非功能需求
- NFR-1: 安装脚本运行时依赖 — 要求: 仅依赖 Python 标准库，不引入 npm、pip 或 jq 等额外工具 — 出处: README 声明 HarnessFlow 是纯 Markdown + stdlib Python 脚本 — 验证方式: 代码审查与 stdlib-only 单元测试。
- NFR-2: 跨平台基础兼容 — 要求: 安装脚本在 Windows 与 POSIX 路径模型下都使用 `pathlib`/`shutil`，测试覆盖 Windows 风格路径无硬编码 shell 分隔符 — 出处: 当前工作区运行在 Windows，README 面向通用项目 vendoring — 验证方式: Python 单元测试使用临时目录运行安装。

## 2. 设计

### 现状与改动面
当前 v3 仓库保留 `skills/`、`.cursor/rules/harness-flow.mdc` 与 `.opencode/skills`。README 只描述手工复制/指向，缺少可执行安装入口。实现将新增一个 stdlib Python 安装器和薄包装脚本：

- `scripts/install.py`: 唯一安装逻辑，支持 `--target cursor|opencode|both`、`--dest <project>`、`--mode copy|symlink`，默认 `copy`。
- `install.ps1` 与 `install.sh`: 调用 `scripts/install.py` 的平台友好入口，避免用户记完整 Python 路径。
- `tests/test_install.py`: 用临时目录覆盖 Cursor/OpenCode/both、copy/symlink、幂等、保留用户自定义 OpenCode skill、Cursor 规则路径重写。
- README / README.zh-CN / CHANGELOG / `.claude-plugin/*` 同步 release 文案与版本。

### 关键决策
D-1: 安装逻辑用 Python 还是 Bash/PowerShell 双实现 — 方案 A: Python stdlib 单实现，包装脚本只转发参数；方案 B: Bash 与 PowerShell 分别实现完整逻辑。选择 A，理由是仓库已有 stdlib Python 工具约定，测试更集中，Windows/POSIX 行为更一致。

D-2: Cursor 安装使用复制还是软链接作为默认 — 方案 A: 默认复制，`--mode symlink` 可选；方案 B: 默认软链接。选择 A，理由是 Windows 普通用户创建 symlink 权限不稳定，复制更可靠；开发者仍可选 symlink。

D-3: OpenCode 安装覆盖整个 `.opencode/skills` 还是只管理 HarnessFlow skill 目录 — 方案 A: 只同步 HarnessFlow 已知 skill 目录，保留其他目录；方案 B: 删除并重建整个 `.opencode/skills`。选择 A，理由是用户可能已有自定义 OpenCode skills，安装脚本不得破坏。

### 接口与数据契约
命令接口：

```text
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
python scripts/install.py --target both --dest /path/to/project --mode copy
```

包装脚本接口：

```text
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

安装结果：

- Cursor: `<dest>/.cursor/harness-flow-skills/<skill>/...` 与 `<dest>/.cursor/rules/harness-flow.mdc`。
- OpenCode: `<dest>/.opencode/skills/<skill>/...`。
- symlink 模式仅链接目录；copy 模式先替换 HarnessFlow 管理的 skill 目录，不删除未知用户目录。

### 错误处理
- 源仓库缺少 `skills/` 或 Cursor rule 时，安装器以非 0 退出并打印明确错误。
- `--dest` 不存在时创建目标目录；目标路径是文件时失败。
- symlink 创建失败时不静默降级，提示用户改用默认 copy。
- 删除或替换前只操作 HarnessFlow 管理的目标路径；未知文件保留。

## 3. 测试策略
每个任务都通过 `hf_gate.py run` 记录 red/green。新增测试使用 Python `unittest` 和 `tempfile`，不依赖真实 Cursor/OpenCode 可执行文件。全量验证命令为：

```text
python scripts/validate_skills.py && python -m unittest skills/hf-workflow/scripts/test_hf_gate.py tests/test_install.py
```

release 前冒烟使用安装器在临时目录执行 `--target both`，再检查 Cursor rule 与 OpenCode skills 产物存在。

## 4. 任务清单

- [x] T-1 恢复仓库验证基线 (覆盖: FR-1) — 判据: 删除或处理既有空 skill 目录后，`validate_skills.py` 与 `test_hf_gate.py` 通过并有 red/green 证据。
- [x] T-2 实现 Cursor 安装路径 (覆盖: FR-2, NFR-1, NFR-2) — 判据: 先写 Cursor 安装失败测试取得 red，再实现 `scripts/install.py` 的 Cursor copy 安装、规则路径重写与幂等逻辑取得 green。
- [x] T-3 实现 OpenCode 安装路径 (覆盖: FR-3, NFR-1, NFR-2) — 判据: 先写 OpenCode 安装失败测试取得 red，再实现 OpenCode copy 安装、保留用户自定义 skill 与幂等逻辑取得 green。
- [x] T-4 实现包装脚本与 symlink 模式 (覆盖: FR-2, FR-3, NFR-1, NFR-2) — 判据: 先写 wrapper/symlink 失败测试取得 red，再实现 `install.sh`、`install.ps1` 与 `--mode symlink` 取得 green。
- [x] T-5 同步文档与 release 元数据 (覆盖: FR-4) — 判据: README、README.zh-CN、CHANGELOG、插件元数据说明 `v3.1.0` 与安装脚本入口，校验套件通过。
- [x] T-6 发布前冒烟与 release 准备 (覆盖: FR-1, FR-2, FR-3, FR-4) — 判据: 临时目录安装冒烟、全量测试、CHANGELOG 链接与版本号检查均通过；实际 git tag / GitHub release 等待用户确认后执行。

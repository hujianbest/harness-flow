# 实现代码评审 (第 1 轮)

- 日期: 2026-07-17
- 评审方式: subagent
- 结论: 需修改

## 测试

- 评审者运行: `python scripts\validate_skills.py; if ($LASTEXITCODE -eq 0) { python -m unittest skills\hf-workflow\scripts\test_hf_gate.py tests.test_install }`
- 结果: 通过；技能校验 OK，35 个 unittest 通过。

## Findings

- [一般] `SECURITY.md`: 本次新增的 `scripts/install.py` 会在用户指定项目下创建和替换 `.cursor/`、`.opencode/` 内的 HarnessFlow 管理目录，但安全策略仍声明 HarnessFlow 不包含会触碰用户机器/数据的运行时代码，Scope 列表也未包含安装器。这会让新发布面的漏洞报告范围与实际能力不一致。→ 更新 `SECURITY.md` 的 Scope 描述，将 `scripts/install.py` 及其文件系统写入行为纳入安全策略覆盖范围，并避免继续声明项目没有此类运行时代码。

# 实现代码评审 (第 2 轮)

- 日期: 2026-07-17
- 评审方式: subagent
- 结论: 通过
- 用户确认: 2026-07-17

## 复审范围

仅确认第 1 轮 finding 是否闭合：`SECURITY.md` 是否将 `scripts/install.py` 及其对 `.cursor/`、`.opencode/` 的文件系统写入纳入安全策略覆盖范围，并避免继续声明项目没有此类运行时代码。

## 测试

- 评审者运行: `python scripts\validate_skills.py; if ($LASTEXITCODE -eq 0) { python -m unittest skills\hf-workflow\scripts\test_hf_gate.py tests.test_install }`
- 结果: 通过；技能校验 OK，35 个 unittest 通过。

## Findings

- 第 1 轮 finding 已闭合: `SECURITY.md` Scope 现声明 HarnessFlow 包含 stdlib-only installer/toolchain，明确列出 `scripts/install.py` 及其写入用户所选项目中 HarnessFlow 管理的 `.cursor/`、`.opencode/` 路径；旧的“不包含会触碰用户机器/数据的运行时代码”表述已移除。

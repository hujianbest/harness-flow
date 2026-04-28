# df Embedded Evidence Checklist

> 配套 `df-tdd-implementation/SKILL.md`。规定嵌入式 C / C++ TDD 实现期间需保留的静态 / 动态质量证据。

## 证据落点

```text
features/<id>/evidence/
  unit/                       # 单元测试 RED / GREEN / REFACTOR 证据
  integration/                # 集成 / 仿真 / SIL / HIL（如适用）
  static-analysis/            # 静态分析（编译告警、Coverity / Klocwork / cppcheck / clang-tidy / MISRA / CERT）
  build/                      # 编译命令 + 退出码 + 关键告警
```

## 每份证据的最小字段

无论哪类证据，必须含：

- **命令**：完整复制粘贴可重放的命令（含目标平台 / 架构 / 编译选项）
- **环境**：操作系统、编译工具链、目标平台、相关固件版本
- **软件版本 / 包**：测试框架、静态分析工具、依赖库的具体版本号
- **配置**：使用的配置文件路径与版本锚点
- **结果**：退出码 + 关键 stdout / stderr 摘要 + 详细日志路径
- **新鲜度锚点**：commit hash 或 build ID
- **覆盖的风险或行为**：本次证据证明了哪个 requirement row / Test Design Case ID

## 单元测试证据（RED / GREEN / REFACTOR）

| 证据类型 | 必含 |
|---|---|
| RED | 命令、退出码、失败摘要、对应 Test Design Case ID、为什么预期失败 |
| GREEN | 命令、退出码、通过摘要、关键 assertion 结果、新鲜度锚点 |
| REFACTOR | cleanup 列表（Fowler vocabulary）、完整测试通过命令与结果、静态分析对比 |

## 集成 / 仿真证据

适用条件：

- 测试设计章节中存在 `integration` / `simulation` 层级用例
- AR 涉及跨模块 / 跨组件协作（仍在本组件仓库内）
- 涉及实时性 / 时序的 NFR

必含：

- 仿真器版本与配置
- 关键时序 / latency / throughput 直方图（如 NFR 涉及）
- 异常路径触发结果
- 资源生命周期（句柄 / 内存）配对验证

## 静态分析证据

| 类型 | 必含 |
|---|---|
| 编译告警 | 编译命令、warning level、新增 / 减少的告警条目摘要 |
| 静态分析（cppcheck / clang-tidy / Coverity / 团队工具） | 命令、报告路径、严重项摘要、与基线的差异 |
| MISRA / CERT / 团队编码规范 | 工具命令、违反项 ID、是否已抑制 / 已修 / 已解释 |

critical 违反项**必须**有显式处理（修 / 抑制并附理由 / 升级路径）；不允许「先放着」。

## Build 证据

- 全量构建命令 + 退出码
- 增量构建命令（如适用）
- 关键告警摘要（按 warning level 分类）
- 多目标平台构建结果（如 AR 涉及多平台兼容性）

## 文件命名建议

```text
RED-<case-id>-YYYY-MM-DD.md
GREEN-<case-id>-YYYY-MM-DD.md
REFACTOR-<case-id>-YYYY-MM-DD.md
static-analysis-<tool>-YYYY-MM-DD.md
build-<target>-YYYY-MM-DD.md
integration-<scenario>-YYYY-MM-DD.md
```

## 反例

```text
❌ "测试通过了"
❌ "本地跑过没问题"
❌ "和我改的没关系的失败"
❌ 把巨大的原始日志直接粘进 implementation-log.md
```

```text
✅ RED-TC-001-2026-04-27.md：
   命令：./build/test/component_x_test --gtest_filter=ModeSwitch.SetNormal
   退出码：1
   失败摘要：Expected ModeChanged.event = NORMAL, got UNINITIALIZED
   对应 Test Design Case ID：TC-001（覆盖 FR-001）
   为什么预期失败：Service.SetMode 尚未实现，本次 RED 证明 NORMAL 切换路径未通
   commit：abc123def
```

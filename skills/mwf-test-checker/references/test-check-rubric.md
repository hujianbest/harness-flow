# mwf Test Check Rubric

> 配套 `mwf-test-checker/SKILL.md`。展开 7 维度评分细则与 rule IDs。

## 7 维度评分

| 维度 | 关键检查 |
|---|---|
| **TC1 Fresh RED / GREEN Validity** | RED 真失败、GREEN 本会话产生、新鲜度锚点（commit/build ID）完整 |
| **TC2 Behavior & Acceptance Mapping** | 每个用例回指 requirement row + Test Design Case ID；核心 row 至少一个用例覆盖 |
| **TC3 Boundary & Exception Coverage** | 边界 / null / 错误路径 / 异常路径覆盖 |
| **TC4 Embedded Risk Coverage** | 内存 / 并发 / 实时性 / 资源 / 错误处理 / ABI 被 `embedded-risk` 用例覆盖 |
| **TC5 Mock Boundary Discipline** | mock 限定真正边界；不 mock 内部纯逻辑；不引入「测试专用方法」 |
| **TC6 Assertion Strength** | 断言能证明行为，不只是证明代码被调用；可被 mutation 抓到 |
| **TC7 Stability & Maintainability** | 测试可独立运行 / 不依赖外部状态 / 命名清晰 / 无 flaky 信号 |

任一关键维度 < 6 → 不得 `通过`。

## Rule IDs

### Group TC1 - Fresh RED / GREEN

- `TC1.1` RED 证据存在且失败原因匹配预期
- `TC1.2` GREEN 证据本会话产生（命令、退出码、新鲜度锚点齐全）
- `TC1.3` REFACTOR 证据（如适用）未引入新行为
- `TC1.4` 大体量原始日志保存在 evidence 子目录而非 implementation-log.md

### Group TC2 - Behavior & Acceptance

- `TC2.1` 每个用例回指 requirement row
- `TC2.2` 每个用例回指 AR 设计 Test Design Case ID
- `TC2.3` 每条核心 requirement row 至少有一个用例覆盖
- `TC2.4` Acceptance 中的可判定条件被显式断言

### Group TC3 - Boundary & Exception

- `TC3.1` 输入边界（最大 / 最小 / null / 越界）覆盖
- `TC3.2` 错误路径（参数错、资源失败、依赖失败）覆盖
- `TC3.3` 异常状态恢复路径覆盖

### Group TC4 - Embedded Risk

- `TC4.1` 内存（边界、池化、栈）有专属用例
- `TC4.2` 并发（中断上下文、临界区、竞态）有专属用例
- `TC4.3` 实时性（latency、deadline）有可量化断言
- `TC4.4` 资源生命周期（句柄、文件、缓冲区）配对验证
- `TC4.5` 错误处理（输入校验、降级、恢复）有专属用例
- `TC4.6` ABI / API 兼容性（如 AR 触及）有专属用例
- `TC4.7` 嵌入式风险覆盖矩阵的所有触发维度均有实测用例

### Group TC5 - Mock Boundary

- `TC5.1` mock 仅限外部依赖 / 硬件 / 协议栈 / 跨组件 SOA 调用
- `TC5.2` 不 mock 内部纯逻辑
- `TC5.3` 不 mock 模块私有函数
- `TC5.4` 不引入「测试专用方法」（test-only public method）
- `TC5.5` 仿真器版本与配置已记录

### Group TC6 - Assertion Strength

- `TC6.1` 断言验证行为结果，不只是「调用过」
- `TC6.2` 断言能在实现 mutation 后失败（默认怀疑）
- `TC6.3` 不使用宽松断言（"不为 null"、"不抛"）覆盖关键行为
- `TC6.4` 数值断言含具体期望值，不只是范围

### Group TC7 - Stability & Maintainability

- `TC7.1` 测试可独立运行（不依赖其他用例顺序）
- `TC7.2` 不依赖外部状态 / 不依赖系统时钟（除实时性 NFR）
- `TC7.3` 命名清晰，能反映被测行为
- `TC7.4` 无 flaky 信号（重试、sleep、随机种子无锚点）
- `TC7.5` 测试代码遵循团队编码规范

## Severity 分级

- `critical`：阻塞 code review（无效 RED / GREEN、关键 requirement row 无覆盖、嵌入式风险全维度未覆盖、mock 越界严重）
- `important`：approval 前应修（断言过弱、边界覆盖不全、单个嵌入式维度未覆盖）
- `minor`：建议改进（命名、轻微稳定性问题）

## Classification

- `USER-INPUT`：业务接受度判定 / 阈值是否合理 → 上抛需求负责人 / 开发负责人
- `LLM-FIXABLE`：补用例、改断言、调整 mock 边界、补嵌入式风险用例 → 由 `mwf-tdd-implementation` 回修
- `TEAM-EXPERT`：实时性测试方法 / 仿真配置 / 内存模型断言 → 上抛资深嵌入式工程师

## Verdict 决策

| 评分 / findings 状态 | verdict |
|---|---|
| 7 维度均 ≥ 6、嵌入式矩阵实测覆盖、断言强度足够、无 critical USER-INPUT | `通过` |
| 评分某项 < 6 但 findings 可 1-2 轮定向修订 | `需修改` |
| 评分多项 < 6 / 测试过于薄弱 / 关键行为未覆盖 | `阻塞`（内容） |
| route / stage / profile / 上游证据冲突 | `阻塞`（workflow） + `reroute_via_router=true` |

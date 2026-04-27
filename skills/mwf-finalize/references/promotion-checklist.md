# mwf Long-Term Asset Promotion Checklist

> 配套 `mwf-finalize/SKILL.md`。规定如何把 `features/<id>/` 的过程产物正确 promote 到组件仓库 `docs/`，并在 closeout pack 中记录同步路径。

## 同步对象（按 work item 类型）

| Work Item Type | 必须同步 | 视情况同步 | 不同步 |
|---|---|---|---|
| `AR`（standard / lightweight） | `docs/ar-designs/AR<id>-<slug>.md` | `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md`（若本 AR 触发变化） | `docs/component-design.md`（standard / lightweight 不修改组件设计） |
| `AR`（component-impact） | `docs/component-design.md` + `docs/ar-designs/AR<id>-<slug>.md` | `docs/interfaces.md` / `docs/dependencies.md` / `docs/runtime-behavior.md` | — |
| `DTS`（不修改组件设计、不需要正式 AR 设计） | 至少在 `docs/component-design.md` 的变更记录章节追加修复记录（团队约定优先） | `docs/ar-designs/AR<id>-<slug>.md`（若 DTS 走了完整 AR 流程） | — |
| `DTS`（修改组件级行为） | `docs/component-design.md`（必要时其他长期资产） | 同上 | — |
| `CHANGE` | 视情况；至少更新 `docs/component-design.md` 变更记录章节 | 其余按团队约定 | — |

## Promote 改写要求

把 `features/<id>/` 的草稿 promote 到 `docs/` 时，**不能**直接复制原文。需要做以下语义化改写：

1. **去掉草稿专属内容**：例如「Open Questions」「待澄清项」「review findings 应答」「过程笔记」
2. **补长期文档结构**：保留团队组件设计 / AR 设计模板的全套章节（包括 mwf 占位模板未补齐时由开发负责人 / 模块架构师手动补齐的章节）
3. **保留追溯锚点**：AR ID / SR / IR / Owner / 测试设计章节 case ID / 关联 review 记录路径
4. **更新变更记录表**：在长期文档的「变更记录」章节追加本次修订（日期、修订者、触发 AR / DTS、摘要）
5. **统一模板版本**：长期文档头部应记录使用的团队模板版本

## docs/ar-designs/AR<id>-<slug>.md 必含

按 `docs/mwf-principles/03 artifact-layout.md`：

- AR ID、SR link、所属组件
- 设计目标和范围
- 受影响文件 / 模块 / 接口
- 数据结构和控制流
- C / C++ 实现策略
- 错误处理
- 资源生命周期
- 并发 / 实时性影响
- 与组件实现设计的一致性说明
- 测试设计章节（保留章节，不拆出独立文件）

## docs/component-design.md 修订（component-impact）

按 `docs/mwf-principles/03 artifact-layout.md`：

- 组件职责与非职责
- SOA 服务 / 接口
- 依赖组件
- 数据模型和状态机
- 并发、实时性、资源生命周期
- 错误处理和降级策略
- 配置项和编译条件
- 对 AR 实现设计的约束

修订时只更新本次受影响的章节，并在变更记录中记录触发 AR / DTS。

## docs/interfaces.md / dependencies.md / runtime-behavior.md

仅在本次触发变化时同步，按 `docs/mwf-principles/03 artifact-layout.md` 的最小字段：

- `interfaces.md`：服务名、接口、输入输出、错误码、时序约束、兼容性要求
- `dependencies.md`：内部组件依赖、版本约束、初始化 / shutdown 顺序、风险与限制
- `runtime-behavior.md`：运行时行为关键约定（启动 / 关停 / 故障 / 调度 / 时序）

## closeout pack 字段对应关系

`templates/mwf-closeout-template.md` 的 `Long-Term Assets Sync` 表必须显式列出：

| 长期资产 | 路径 | 本次是否同步 | 备注 |
|---|---|---|---|
| Component Implementation Design | `docs/component-design.md` | yes / no / N/A | |
| AR Implementation Design | `docs/ar-designs/AR<id>-<slug>.md` | yes / N/A | |
| Interfaces | `docs/interfaces.md` | yes / no / N/A | |
| Dependencies | `docs/dependencies.md` | yes / no / N/A | |
| Runtime Behavior | `docs/runtime-behavior.md` | yes / no / N/A | |

未触发变化的资产填 `N/A`，不算 blocked；项目当前未启用的资产（如团队尚未维护 `docs/runtime-behavior.md`）填 `N/A（项目未启用）`，不算 blocked。

## 反例

```text
❌ 把 ar-design-draft.md 原样 copy 到 docs/ar-designs/，保留 "TODO: 待澄清"、"Open Questions" 等过程内容
❌ component-impact 修订只在 closeout pack 写「已修订」但未真的更新 docs/component-design.md
❌ DTS 修改了组件状态机却不同步 docs/component-design.md
```

```text
✅ 把 ar-design-draft.md promote 时：
   - 去掉 Open Questions / Review Response / 过程笔记
   - 补全模板章节（包括团队模板原本留空、开发负责人手动补齐的章节）
   - 在文档头部记录 AR ID / SR / Owner / Created / Last Reviewed
   - 在变更记录表追加 (YYYY-MM-DD, owner, trigger=AR12345, summary)
✅ component-impact 修订时：
   - 只更新本次受影响的小节
   - 同步在 docs/component-design.md 的变更记录追加 (YYYY-MM-DD, 模块架构师, trigger=AR12345, summary)
   - 不顺手重排其他章节
```

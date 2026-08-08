# 需求评审 Checklist

适用于 `spec.md`。加载的 `ext-*` 若声明本层追加项,一并检查。

## 可测性

- [ ] 问题与方案从用户视角写清,非实现愿望
- [ ] User stories / 验收标准可判定(第三方能说出通过/不通过)
- [ ] 覆盖失败路径与边界,不只有 happy path
- [ ] Testing Decisions 写明缝与「测外部行为」原则

## 反幻觉

- [ ] 无未确认假设写成事实(假设在 `product/assumptions.md`)
- [ ] 模糊量词已量化或删除
- [ ] Implementation Decisions 无过期会烂的具体文件路径堆砌(原型决策片段除外)

## 完整与一致

- [ ] 与 grilling / CONTEXT 词汇一致
- [ ] Out of Scope 外显式列出
- [ ] 无与 ADR / CONTEXT 冲突的静默推翻

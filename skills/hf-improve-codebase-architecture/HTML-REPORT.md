# HTML 报告格式

架构评审会渲染为 OS 临时目录中的单个自包含 HTML 文件。Tailwind 和 Mermaid 均来自 CDN。Mermaid 能可靠处理图状图表；手工构建的 div 和内联 SVG 则负责更具编辑设计感的可视化（质量图、剖面图）。将两者混合使用——不要所有内容都依赖 Mermaid，否则报告会开始显得千篇一律。

## 脚手架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 页眉

仓库名称、日期，以及一个紧凑的图例：实线框 = module，虚线 = seam，红色箭头 = leakage，粗深色框 = deep module。不要写介绍段落——直接进入候选项。

## 候选项卡片

图表承担主要表达任务。文字应当少而直白，并自然使用 `/codebase-design` 技能中的术语表词汇，不做多余铺陈。

每个候选项对应一个 `<article>`：

- **标题（Title）**——简短，为深化操作命名（例如“合并 Order intake pipeline”）。
- **徽章行（Badge row）**——建议强度（`Strong` = 翠绿色，`Worth exploring` = 琥珀色，`Speculative` = 石板色），再加一个依赖类别标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **文件（Files）**——等宽字体列表，使用 `font-mono text-sm`。
- **前后对比图（Before / After diagram）**——核心内容。分为两列，并排展示。参见下方模式。
- **问题（Problem）**——一句话。说明痛点是什么。
- **方案（Solution）**——一句话。说明会改变什么。
- **收益（Wins）**——项目符号列表，每项不超过 6 个词。例如：“测试只命中一个 interface”“Pricing 逻辑不再泄漏”“删除 4 个 shallow wrapper”。
- **ADR 标注（ADR callout）**（如适用）——琥珀色调方框中的一行文字。

不要写解释性段落。如果必须用一个段落才能让人理解图表，就重新绘制图表。

## 图表模式

选择适合候选项的模式，并混合使用。不要让每张图看起来都一样——多样性本身就是目标的一部分。

### Mermaid 图（依赖/调用流的主力工具）

当表达重点是“X 调用 Y，Y 调用 Z，看看这有多混乱”时，使用 Mermaid `flowchart` 或 `graph`。将其包裹在 Tailwind 风格的卡片中，使它看起来不像凭空插入。使用 classDef 设置样式，将泄漏边设为红色，将深模块设为深色。序列图很适合表现“之前：6 次往返；之后：1 次”。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手工构建的方框与箭头（当 Mermaid 的布局不配合时）

将模块绘制为带边框和标签的 `<div>`。将箭头绘制为内联 SVG `<line>` 或 `<path>` 元素，并在相对定位容器上进行绝对定位。当你希望“之后”图呈现为一个带粗边框、内部元素灰显的深模块时，就使用这种方法——Mermaid 无法以恰当的视觉权重渲染这种效果。

### 剖面图（适合分层浅薄结构）

堆叠水平条带（`h-12 border-l-4`），展示一次调用所穿过的层。之前：6 个薄层，每层什么也没做。之后：1 个粗条带，标注合并后的职责。

### 质量图（适合“接口与实现一样宽”）

每个模块使用两个矩形——一个表示接口表面积，一个表示实现。之前：接口矩形几乎与实现矩形一样高（浅）。之后：接口矩形矮，实现矩形高（深）。

### 调用图折叠

之前：将函数调用树渲染为嵌套方框。之后：将同一棵树折叠到一个方框中，并在内部以淡化方式显示那些现已成为内部调用的内容。

## 样式指导

- 采用精简的编辑设计风格，而不是企业仪表盘风格。留出充足空白。标题可选用衬线字体（`font-serif` 与 stone/slate 配合良好）。
- 谨慎使用颜色：一种强调色（翠绿色或靛蓝色），再加上表示泄漏的红色和表示警告的琥珀色。
- 将图表高度保持在约 320px，使前后对比无需滚动即可舒适地并排显示。
- 对图表内的模块标签使用 `text-xs uppercase tracking-wider`——它们应呈现为示意图，而不是 UI。
- 唯一允许的脚本是 Tailwind CDN 和 Mermaid ESM import。报告的其他部分均为静态内容——没有应用代码，除 Mermaid 自身渲染外没有交互。

## 首要建议部分

一张较大的卡片。候选项名称、用一句话说明原因，以及指向该候选项卡片的锚点链接。仅此而已。

## 语气

使用直白、简洁的语言——但架构名词和动词必须直接取自 `/codebase-design` 技能。简洁不能成为偏离术语的借口。

**严格使用：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**绝不替换为：** component、service、unit（替代 module）· API、signature（替代 interface）· boundary（替代 seam）· layer、wrapper（当你表达的是 module 时替代 module）。

**符合该风格的表述：**

- “Order intake module 很浅——interface 几乎与 implementation 相当。”
- “Pricing 跨 seam 发生泄漏。”
- “深化：一个 interface，一个测试位置。”
- “两个 adapter 证明了 seam 的合理性：生产环境使用 HTTP，测试使用内存实现。”

**收益项目符号（Wins bullets）**应使用术语表中的词汇来命名收益：*“locality：缺陷集中在一个 module 中”*、*“leverage：一个 interface，N 个调用点”*、*“interface 缩小；implementation 吸收 wrappers”*。不要写*“更易维护”*或*“代码更整洁”*——这些词不在术语表中，没有资格出现在这里。

不要使用模棱两可的措辞，不要写开场套话，也不要写“值得注意的是……”。如果一句话可以写成项目符号，就把它写成项目符号。如果一个项目符号可以删掉，就删掉。如果某个术语不在 `/codebase-design` 术语表中，先从术语表里寻找合适词汇，再考虑创造新词。

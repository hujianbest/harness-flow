---
name: hf-codebase-design
description: 用于设计深模块的共享词汇。当用户想要设计或改进模块的接口、寻找深化机会、决定接缝的位置、使代码更易于测试或更便于 AI 导航，或者其他技能需要深模块词汇时使用。
---

# 代码库设计

设计**深模块（deep modules）**：将大量行为置于一个小接口之后，把接口放在清晰的接缝处，并且可以通过该接口进行测试。凡是设计或重构代码，都应使用这套语言和这些原则。目标是为调用方提供杠杆效应，为维护者提供局部性，并让所有人都能方便地测试。

## 术语表

请严格使用这些术语——不要用“component（组件）”“service（服务）”“API”或“boundary（边界）”替代。统一语言正是这一做法的全部意义。

**Module（模块）**——任何具有接口和实现的事物。刻意不限定规模：可以是函数、类、包，也可以是跨层切片。_避免使用_：unit、component、service。

**Interface（接口）**——调用方要正确使用模块所必须知道的一切：不仅包括类型签名，还包括不变量、顺序约束、错误模式、必需配置和性能特征。_避免使用_：API、signature（范围太窄——它们只指类型层面的表面）。

**Implementation（实现）**——模块内部的内容，即其代码主体。它不同于 **Adapter（适配器）**：一个事物可以是实现很大的小适配器（例如 Postgres repo），也可以是实现很小的大适配器（例如内存 fake）。讨论主题是接缝时使用“adapter”；其他情况下使用“implementation”。

**Depth（深度）**——接口处的杠杆效应：调用方（或测试）每学习一个单位的接口，能够驱动多少行为。当大量行为位于小接口之后时，模块是 **deep（深的）**；当接口几乎与实现一样复杂时，模块是 **shallow（浅的）**。

**Seam（接缝）** _（Michael Feathers）_——一个无需在该处进行编辑就能改变行为的地方；也就是模块接口所在的*位置*。接缝应放在哪里，本身就是一项设计决策，与接缝之后放什么是不同的问题。_避免使用_：boundary（它已被 DDD 的 bounded context 赋予过多含义）。

**Adapter（适配器）**——在接缝处满足接口的具体事物。它描述的是*角色*（填补什么位置），而不是实质（内部有什么）。

**Leverage（杠杆效应）**——调用方从深度中获得的收益：每学习一个单位的接口，就能获得更多能力。一个实现会在 N 个调用点和 M 个测试中持续带来回报。

**Locality（局部性）**——维护者从深度中获得的收益：变更、缺陷、知识和验证集中在一个地方，而不是散布到各个调用方。修复一次，处处修复。

## 深模块与浅模块

**深模块（Deep module）** = 小接口 + 大量实现：

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**浅模块（Shallow module）** = 大接口 + 少量实现（应避免）：

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

设计接口时，请问：

- 我能减少方法数量吗？
- 我能简化参数吗？
- 我能把更多复杂性隐藏在内部吗？

## 原则

- **深度是接口的属性，而不是实现的属性。** 深模块内部可以由小型、可 mock、可替换的部件组成——它们只是不属于接口。模块既可以有**内部接缝（internal seams）**（仅供其实现内部使用，并由自身测试使用），也可以在接口处有**外部接缝（external seam）**。
- **删除测试（deletion test）。** 设想删除该模块。如果复杂性随之消失，它原本只是一个透传层。如果复杂性重新出现在 N 个调用方中，它就在发挥应有的价值。
- **接口就是测试表面。** 调用方和测试跨越同一条接缝。如果你想越过接口去测试其内部，模块的形态很可能不正确。
- **一个适配器意味着一条假想接缝，两个适配器意味着一条真实接缝。** 除非确实有事物会跨接缝发生变化，否则不要引入接缝。

## 为可测试性而设计

良好的接口让测试自然发生：

1. **接受依赖，不要创建依赖。**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，不要产生副作用。**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **小表面积。** 方法越少 = 所需测试越少。参数越少 = 测试准备越简单。

## 关系

- 一个 **Module** 恰好有一个 **Interface**（它呈现给调用方和测试的表面）。
- **Depth** 是 **Module** 的属性，以其 **Interface** 为参照进行衡量。
- **Seam** 是 **Module** 的 **Interface** 所在的位置。
- **Adapter** 位于 **Seam** 处并满足 **Interface**。
- **Depth** 为调用方带来 **Leverage**，为维护者带来 **Locality**。

## 不采用的表述框架

- **把 Depth 定义为实现代码行数与接口代码行数之比**（Ousterhout）：这会奖励无意义地扩充实现。我们改用“深度即杠杆效应（depth-as-leverage）”。
- **把“Interface”理解为 TypeScript 的 `interface` 关键字或类的 public 方法**：范围太窄——这里的接口包括调用方必须知道的每一项事实。
- **“Boundary”**：它已被 DDD 的 bounded context 赋予过多含义。应使用 **seam** 或 **interface**。

## 进一步深入

- **根据依赖关系深化一个模块簇**——参见 [DEEPENING.md](DEEPENING.md)：依赖类别、接缝纪律，以及“替换而非叠加”的测试策略。
- **探索备选接口**——参见 [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)：启动并行 sub-agent，以数种截然不同的方式设计接口，然后从深度、局部性和接缝位置三个方面进行比较。

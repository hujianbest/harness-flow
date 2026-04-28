# C++ / GoogleTest Deep Guide

仅在当前项目是 C++ / GoogleTest / CMake 栈，且确实需要语言级实现细节时，再读取本参考。

主契约仍以当前 skill 的主文件 `../SKILL.md` 为准；本文件只补充语言级示例、模式和反模式。

## Overview

先写测试，看着它失败，再写最少的代码让它通过。

核心原则：

- 如果你没有亲眼看到测试失败，你就不知道它到底测的是什么。

## When to Use

始终使用：

- 新功能实现
- Bug 修复
- 重构
- 行为变更

例外（需要与用户确认）：

- 一次性原型
- 自动生成的代码
- 纯配置文件

## Iron Rule

```text
没有失败的测试，就不写产品代码
```

先写了实现代码？删掉它，从头来过。

没有例外：

- 不要把它留作“参考”
- 不要“一边写测试一边改它”
- 不要偷看它
- 删除就是删除

如果项目级约定或主 `SKILL.md` 明确声明某些纯配置或等价变更可例外豁免 fail-first，遵循项目约定；除此之外，不自创例外。

## Red Green Refactor

### RED

写一个最小的测试，描述期望的行为。

```cpp
TEST(RetryTest, RetriesFailedOperations3Times) {
  int attempts = 0;
  auto operation = [&]() -> std::string {
    ++attempts;
    if (attempts < 3) throw std::runtime_error("fail");
    return "success";
  };

  auto result = retry_operation(operation);

  EXPECT_EQ(result, "success");
  EXPECT_EQ(attempts, 3);
}
```

要求：

- 只测一个行为
- 测试名说明行为，例如 `RejectsEmptyInput`
- 用真实代码，mock 只在不得已时使用

验证 RED 时必须执行测试，并确认：

- 测试失败，而不是编译报错
- 失败原因符合预期
- 失败是因为功能缺失，而不是拼错了

以下情况不算有效 RED：

- 与当前任务无关的既有失败
- 环境损坏、依赖缺失或基础构建链本身异常
- 你看不出失败到底对应哪条行为预期

### GREEN

写最简单的代码让测试通过。

```cpp
template <typename F>
auto retry_operation(F&& fn, int max_retries = 3) -> decltype(fn()) {
  for (int i = 0; i < max_retries; ++i) {
    try {
      return fn();
    } catch (...) {
      if (i == max_retries - 1) throw;
    }
  }
  throw std::logic_error("unreachable");
}
```

不要加功能、不要顺手重构别的代码、不要“改进”超出测试要求的范围。

验证 GREEN 时必须确认：

- 当前测试通过
- 其他测试依然通过
- 编译输出干净，没有 warning 或 error
- 通过结果来自本次会话，而不是旧日志
- 已记录当前任务级 proving command 和关键输出摘要，便于写入实现交接块

### REFACTOR

只在全绿之后：

- 消除重复
- 改善命名
- 提取辅助函数

保持测试全绿，不添加新行为。

## Good Test Standards

| 品质 | 好 | 坏 |
|------|----|----|
| 最小 | 只测一件事。名字里有“并且”？拆开。 | `TEST(Validator, ValidatesEmailAndDomainAndWhitespace)` |
| 清晰 | 名字描述行为 | `TEST(Foo, Test1)` |
| 表达意图 | 展示理想的 API | 隐藏了代码该做什么 |

## GoogleTest Useful Patterns

### Test Fixture

当多个测试需要相同的准备工作时，使用 fixture：

```cpp
class CalculatorTest : public ::testing::Test {
protected:
  void SetUp() override {
    calc = std::make_unique<Calculator>();
  }

  std::unique_ptr<Calculator> calc;
};

TEST_F(CalculatorTest, AddsPositiveNumbers) {
  EXPECT_EQ(calc->add(2, 3), 5);
}
```

### Parameterized Tests

同一个逻辑、不同输入时，避免复制粘贴：

```cpp
struct EmailCase {
  std::string input;
  bool expected_valid;
};

class EmailValidationTest : public ::testing::TestWithParam<EmailCase> {};

TEST_P(EmailValidationTest, ValidatesCorrectly) {
  auto [input, expected] = GetParam();
  EXPECT_EQ(is_valid_email(input), expected);
}
```

### Assertion Selection

| 场景 | 推荐 | 说明 |
|------|------|------|
| 继续执行后续断言 | `EXPECT_*` | 失败后继续运行 |
| 失败则无法继续 | `ASSERT_*` | 失败后立即终止当前测试 |
| 浮点比较 | `EXPECT_NEAR(a, b, tol)` | 避免浮点精度问题 |
| 字符串包含 | `EXPECT_THAT(s, HasSubstr("x"))` | 需要 `#include <gmock/gmock-matchers.h>` |
| 异常 | `EXPECT_THROW(expr, ExType)` | 验证抛出指定类型异常 |
| 不抛异常 | `EXPECT_NO_THROW(expr)` | 验证无异常 |

### Dependency Injection and Mocks

C++ 中通过抽象基类注入依赖，方便隔离测试：

```cpp
class ILogger {
public:
  virtual ~ILogger() = default;
  virtual void log(std::string_view message) = 0;
};
```

mock 是为了隔离外部依赖（网络、文件系统、数据库），不是为了省事。如果一个类可以直接构造，就直接用真实对象。

详见 `../testing-anti-patterns.md`。

## Why Order Matters

“我先写完再补测试验证”不成立，因为后写的测试直接通过，直接通过什么也证明不了：

- 可能测的东西不对
- 可能测的是实现细节而非行为
- 可能遗漏了你没想到的边界
- 你从来没看到它抓住过 bug

先写测试，迫使你亲眼看到失败，才能证明测试确实在检查某件事。

## Common Excuses

| 借口 | 现实 |
|------|------|
| “太简单不用测” | 简单的代码也会坏，写个测试只要 30 秒 |
| “我先写完再补” | 后补的测试直接通过，什么也证明不了 |
| “手动测过了” | 临时测试不等于系统测试；没有记录，不可重现 |
| “删掉 X 小时太浪费” | 沉没成本。保留不可信的代码才是负债 |
| “留着当参考” | 你会改它，那就是后补测试；删除就是删除 |
| “需要先探索一下” | 可以。探索完，扔掉探索代码，从 TDD 开始 |
| “测试写不出来 = 设计不清楚” | 正是如此；难测试往往意味着接口太复杂 |
| “TDD 太慢了” | TDD 比调 bug 快；先测试更务实 |

## Red Lights

出现以下任一情况，立即停下，从头来过：

- 先写了实现代码
- 实现完了才补测试
- 测试直接通过
- 说不清测试为什么失败
- 打算“回头再加测试”
- 给自己找“就这一次”的理由

## Bug Fix Example

Bug：空字符串被接受为有效输入。

RED：

```cpp
TEST(InputValidatorTest, RejectsEmptyString) {
  InputValidator validator;
  auto result = validator.validate("");
  EXPECT_FALSE(result.ok);
  EXPECT_EQ(result.error, "input must not be empty");
}
```

GREEN：

```cpp
ValidationResult InputValidator::validate(std::string_view input) {
  if (input.empty()) {
    return {.ok = false, .error = "input must not be empty"};
  }
  // ...existing logic...
}
```

REFACTOR：

- 如果有多个字段需要非空校验，提取通用验证函数。

## Build and Run Tests

如果你不清楚如何运行当前项目的测试命令，优先查看项目级约定中关于编译、构建和验证的相关信息。

典型命令示例：

```bash
cd build && cmake --build . && ctest --output-on-failure
```

## Verification Checklist

- [ ] 每个新函数 / 方法都有对应测试
- [ ] 每个测试都亲眼看到失败
- [ ] 每个测试的失败原因是功能缺失，而不是拼写错误
- [ ] 每次只写了让测试通过的最少代码
- [ ] 所有测试通过
- [ ] 编译输出干净
- [ ] 测试使用真实代码，mock 只在不得已时使用
- [ ] 边界和错误情况已覆盖
- [ ] 已记录足够信息供实现交接块使用

## When Stuck

| 问题 | 解决 |
|------|------|
| 不知道怎么测 | 先写你期望的 API，先写断言，再向搭档求证 |
| 测试太复杂 | 设计太复杂，先简化接口 |
| 必须 mock 一切 | 耦合太紧，使用依赖注入 |
| setup 代码太长 | 提取到 Test Fixture；仍然复杂就继续简化设计 |

## Debugging Integration

发现 bug？先写一个能重现它的失败测试，再走 TDD 循环。测试既证明修复有效，又防止回归。

永远不要在没有测试的情况下修 bug。

## Testing Anti-Patterns

添加 mock 或测试工具时，先读 `../testing-anti-patterns.md`，尤其避免：

- 测试的是 mock 行为而非真实行为
- 给产品类加只有测试才用的方法
- 不了解依赖关系就乱 mock

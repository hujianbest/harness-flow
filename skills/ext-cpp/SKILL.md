---
name: ext-cpp
description: C++ 编程规范扩展。绑定阶段: tdd。触发条件: 项目主要语言为 C++(存在 CMakeLists.txt / *.cpp 主体代码)。约束 C++ 项目在 TDD 阶段的测试组织(GoogleTest)、资源管理与常见测试反模式。
---

# C++ 规范扩展

## 绑定

- 绑定阶段: tdd
- 触发条件: 项目主要语言为 C++

## 测试组织 (GoogleTest)

- 测试名描述行为:`TEST(RetryTest, RetriesFailedOperations3Times)`,不用 `Test1`、`WorksCorrectly`
- 一个 `TEST` 只验证一个行为;共享昂贵初始化用 `TEST_F` fixture,不用全局状态
- 断言优先级:能用 `EXPECT_EQ` 等具体断言就不用 `EXPECT_TRUE(a == b)`(失败信息更可读)
- 验证 RED 时必须区分**测试失败**与**编译失败**——编译错误不是有效 RED

## 测试反模式(发现即重写)

- 为测试暴露私有成员(`friend class XxxTest`、`#define private public`)→ 测公共行为,测不到说明设计有问题,回 `hf-design`
- 在产品类里加只给测试用的方法/构造函数
- mock 具体类而非接口边界;mock 值对象
- 测试依赖执行顺序或共享可变全局状态
- 用 `sleep` 等待异步结果 → 用条件变量/future 显式同步

## 实现规范

- 资源一律 RAII:new/delete 裸指针、手动 fclose/close 出现即在 REFACTOR 步清理
- 所有权语义显式:独占用 `std::unique_ptr`,共享才用 `shared_ptr`,观察用裸指针/引用并注释生命周期约定
- 遵循项目既有的错误处理约定(异常 vs 错误码 vs `expected`),不混用
- 编译警告即错误对待:新代码不得引入新警告

## 评审检查项

以下条目追加到代码评审 checklist:

- [ ] 无为测试而破坏封装的手段(friend 测试类、测试专用方法)
- [ ] 新代码资源管理全部 RAII,无裸 new/delete
- [ ] 测试无顺序依赖、无 sleep 式同步

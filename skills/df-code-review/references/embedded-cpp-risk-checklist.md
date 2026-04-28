# df Embedded C / C++ Risk Checklist

> 配套 `df-code-review/SKILL.md`。嵌入式 C / C++ 风险检视的速查清单，按维度展开常见 finding。

## 内存

- [ ] 动态分配是否符合组件设计（部分组件禁止 `malloc` / `new`）
- [ ] 栈对象大小是否受控；大数组是否在堆 / 静态池
- [ ] 句柄 / 缓冲区 / 文件描述符获取与释放配对
- [ ] 异常路径（return early / 错误码分支）下无泄漏
- [ ] 指针生命周期清晰；无悬垂指针 / use-after-free
- [ ] 内存对齐符合目标平台
- [ ] 跨边界传递的 buffer 长度与所有权语义清晰

## 并发 / 中断

- [ ] 中断上下文中代码无阻塞 API（mutex / 长 IO / 动态分配）
- [ ] 共享数据访问受锁 / 原子操作保护
- [ ] 锁顺序一致，避免嵌套锁循环 / 死锁
- [ ] volatile 用于真正硬件寄存器 / 中断共享变量
- [ ] memory order / barrier 用得正确（特别是无锁数据结构）
- [ ] 临界区代码尽可能短

## 实时性

- [ ] 关键路径无意外阻塞
- [ ] 调度优先级符合组件设计
- [ ] 时钟 / 节拍 / deadline 相关代码已经测试或证据支撑
- [ ] 不在硬实时路径上做日志 / 长 IO

## 资源生命周期

- [ ] 资源创建 / 销毁配对（RAII 或显式 init / shutdown）
- [ ] 错误路径下资源回收完整
- [ ] 全局 / 静态资源初始化顺序符合 component-design

## 错误处理

- [ ] 输入校验覆盖外部接口、协议、配置加载
- [ ] 错误码不被静默吞掉
- [ ] 错误码符合 `docs/component-design.md`（项目已启用 `docs/interfaces.md` 时同步以该文件为准）
- [ ] 降级路径在 component-design 中有定义且实现一致
- [ ] 失败时副作用（部分写入 / 部分初始化）已回滚

## ABI / API 兼容

- [ ] 公共接口签名变更已纳入 component-design 修订
- [ ] 新增错误码不破坏既有消费方
- [ ] 数据结构布局变化符合跨版本 / 跨平台兼容策略
- [ ] 编译条件 / 配置项变更与组件级依赖约定一致（项目已启用 `docs/dependencies.md` 时以该文件为准；未启用时以 `docs/component-design.md` 的依赖章节为准）

## 编码规范 / 静态分析

- [ ] 团队编码规范关键点（命名、注释、初始化、整数提升）
- [ ] MISRA / CERT 子集（按 `AGENTS.md` 声明）违反项处理
- [ ] 编译 warning level 一致；critical 告警闭环
- [ ] 静态分析 critical / blocker 项闭环
- [ ] 抑制（suppression）必须带理由 + 范围
- [ ] 不使用项目禁止的 API（如 raw `new`/`delete`、`std::shared_ptr` 在某些深嵌入式上下文）

## 反例

```text
❌ if (allocResource(&h) != OK) { return; }   // 句柄已部分初始化但未释放
❌ enter_critical(); do_long_blocking_io(); exit_critical();  // 临界区做长 IO
❌ // suppress(MISRA-10.3)  // 缺理由 + 范围
```

```text
✅ if (allocResource(&h) != OK) { return ERR_INTERNAL; }
   defer_or_explicit_release(h);   // 在错误路径中显式释放或使用 RAII
✅ enter_critical(); update_shared_counter(); exit_critical();
   schedule_io_outside_critical();
✅ // suppress(MISRA-10.3) — 此处对外部协议的整数转换已在协议层文档化（见 docs/component-design.md § SOA 接口 § 4.2，或项目已启用时见 docs/interfaces.md § 4.2），范围限定本函数
```

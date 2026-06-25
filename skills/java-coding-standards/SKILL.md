---
name: java-coding-standards
description: 在编写、修改或评审 Java 代码（类、record、枚举、JUnit 测试、Maven/Gradle 构建配置）时使用。提供 null/Optional、equals/hashCode 契约、泛型与 PECS、并发与可见性、异常策略、资源管理的具体规则与正反例。只适用于 Java（17+）；Kotlin/Scala/其他 JVM 语言用各自的语言技能，框架（Spring/Quarkus）专属约定见 references/。
---

# Java Coding Standards

## 总览

Java 的核心危险是**到处可能为 null、错误能被悄悄吞掉、并发可见性靠猜**。本技能在 `hf-clean-code` 的通用标准之上叠加 Java（17+）语言规则，不能替代通用 clean-code 自检。每条规则针对一类真实事故（NPE、丢数据、泄漏、被吞异常、`ClassCastException`、竞态）。项目声明了 Google Java Style / 团队规范子集时以项目为准，本文是未声明时的默认底线。

通用规则（函数长度、命名表意、注释写 why 不写 what）属 `hf-clean-code`，不在本技能重复；领域规则（API 状态码、领域不变量）属领域技能；流程规则（评审、提交）属 `AGENTS.md`。

## 反合理化表

| 话术 | 现实 |
|---|---|
| 「测试全绿，所以没问题」 | 单测只证明被覆盖的外部行为；NPE/竞态/泄漏要靠 `equals`/`hashCode` 契约 + 静态分析 + 并发正确性，测试不替代 |
| 「`equals` 就够了，`hashCode` 用默认」 | 放进 `HashMap`/`HashSet` 后同值对象散列到不同桶 = 丢数据；缺 `hashCode` 是缺陷不是风格 |
| 「这里肯定不会 null」 | 凡是跨边界返回值/参数都是 NPE 源，必须用 `Optional` 或空集合表达缺失，不能靠"肯定" |
| 「`catch (Exception e)` 最省事」 | 泛捕获掩盖所有 bug；吞掉的异常是定位事故的最大障碍 |
| 「这段是历史代码，告警一直就有」 | 历史告警不豁免本次触碰的文件；触碰即按 critical 闭环 |

## null 与 Optional

NPE 是 Java 头号事故。约定写进返回类型：

```java
// ❌ 集合返回 null——调用方稍后 NPE
public List<Order> findOrders(String userId) {
    if (none) return null;
    ...
}
// ✅ 集合永不返回 null，返回空集合
public List<Order> findOrders(String userId) {
    return none ? List.of() : orders;
}
// ✅ 单值可能缺失 → 返回 Optional，调用方被迫处理缺失
public Optional<Market> findBySlug(String slug) { ... }
market.map(MarketResponse::from)
      .orElseThrow(() -> new MarketNotFoundException(slug));
```

- `Optional` 只用于返回值表达"可能没有"；**不**用作字段、方法参数或集合元素（增加分配又不阻止 null）。
- **绝不**给 `Optional` 赋值 null，也**绝不**返回 null 类型的 `Optional`：用 `Optional.empty()`。
- 不裸调 `optional.get()`：用 `orElse` / `orElseThrow` / `map` / `ifPresent`。
- 外部输入与公共 API 边界做 null 校验：`Objects.requireNonNull(x, "x")`。

**事故类**：NPE、缺失值被静默忽略。**自检**：集合/数组不返回 null；可缺失单值用 `Optional` 返回且不裸 `get()`、不赋 null。

## equals 与 hashCode 契约

重写 `equals` 必须同时重写 `hashCode`（否则放进 `HashMap`/`HashSet` 后查不到）：

```java
// ❌ 只写 equals，hashCode 用 Object 默认 → 同值对象散列到不同桶，丢数据
@Override public boolean equals(Object o) { ... }
// ✅ 成对实现，基于同一组字段；优先用 record 让编译器生成
public record Money(BigDecimal amount, Currency currency) {}
```

- 用作 `Map` key 或放进 `Set` 的类型必须不可变，且 `equals`/`hashCode` 只依赖不可变字段。
- 比较可能为 null 的两值用 `Objects.equals(a, b)`，不用 `==` 后再判 null（`==` 比较引用）。
- 实现 `Comparable` 时 `compareTo` 与 `equals` 保持一致（否则 `TreeMap`/`TreeSet` 行为异常）。

**事故类**：丢数据（HashMap 查不到）、对称性违反、`Set` 含重复。**自检**：`equals`/`hashCode` 成对且基于同组字段；Map key/Set 元素不可变。

## 泛型与类型安全

不用裸类型（raw type）——丢失类型检查，错误延后到运行期 `ClassCastException`：

```java
// ❌ 裸类型：运行期炸
List items = new ArrayList();
items.add("x"); Integer n = (Integer) items.get(0);
// ✅ 声明类型参数
List<String> items = new ArrayList<>();
```

- 复用工具用有界通配符，遵循 **PECS**：生产者（只读）`<? extends T>`，消费者（只写）`<? super T>`；不写死具体类型牺牲复用。
- 不用裸类型；`@SuppressWarnings("unchecked")` 必须最小作用域 + 注释理由。
- 不对泛型数组、`instanceof` 擦除类型做未检查假设。

**事故类**：运行期 `ClassCastException`、复用性差。**自检**：无裸泛型类型；`@SuppressWarnings` 最小化且带理由；通配符符合 PECS。

## 并发与可见性

```java
// ❌ 非 volatile 的双重检查锁：其他线程可能看到未完成构造的对象
private Service instance;
public Service get() {
    if (instance == null) synchronized (this) {
        if (instance == null) instance = new Service();
    }
    return instance;          // instance 必须 volatile
}
```

- 共享可变状态最小化；能用不可变对象或 `java.util.concurrent`（`ConcurrentHashMap`、`AtomicX`、`ExecutorService`）就不用裸 `synchronized`。
- **不在 `this` 上同步**：用专门的 `private final Object lock = new Object();`，避免外部代码意外持锁导致死锁。
- 跨线程可见的可变字段用 `volatile` 或 `Atomic*`；复合操作（读-改-写）用原子方法或锁，`volatile` 不保证原子性。
- 持锁期间不调用外部回调/未知代码（死锁与重入风险）；锁的获取顺序固定；不跨线程共享非线程安全集合（`SimpleDateFormat`、普通 `HashMap`）。

**事故类**：数据竞争、可见性失效、死锁、重入。**自检**：共享可变状态用 j.u.concurrent / 原子 / 专属锁对象保护；持锁不调外部回调。

## 异常策略

被吞的异常是定位事故的最大障碍：

```java
// ❌ 吞掉异常：catch 空块 / 打印后继续 / 包装时丢掉 cause
try { parse(s); } catch (ParseException e) { /* ignore */ }
catch (IOException e) { throw new ConfigException("load failed"); }
// ✅ 处理或上抛；包装时用 cause 保留异常链
catch (IOException e) {
    throw new ConfigException("load failed: " + path, e);
}
```

- 不 `catch (Exception e)` / `catch (Throwable t)` 做泛捕获，除非边界处集中翻译并重新抛出/记录。
- **不** `throw new Exception(...)`：用具体的非受检异常子类（`MarketNotFoundException`），不用裸 `RuntimeException` 承载所有情况。
- 受检异常用于可恢复条件（调用方能采取动作）；不可恢复的编程错误用非受检异常。
- `finally` 块里不 `return`、不抛新异常（会吞掉 try 中的原异常）；不在循环里用异常做正常控制流。

**事故类**：被吞错误、堆栈断链、错误分类。**自检**：无被吞异常；包装保留 cause；无泛 `catch (Exception/Throwable)` 未翻译；无裸 `Exception` 抛出。

## 资源管理

实现 `AutoCloseable` 的资源（流、连接、锁包装）一律 try-with-resources，不手写 finally close：

```java
// ❌ 手写 finally：异常叠加时原异常被 close 异常覆盖，且容易漏 close
InputStream in = open(path);
try { return read(in); } finally { in.close(); }
// ✅ try-with-resources：按声明逆序关闭，异常被 suppressed 保留
try (InputStream in = open(path)) {
    return read(in);
}
```

- 多个资源在同一 try 里声明，自动逆序关闭。
- 自有资源类实现 `AutoCloseable`，`close()` 幂等；**不**写 `finalize`/`Cleaner` 释放资源（不可靠）。

**事故类**：资源泄漏、原异常被覆盖。**自检**：`AutoCloseable` 资源用 try-with-resources；无手写 finally close；无 finalizer。

## 不可变与封装

```java
// ❌ 暴露内部可变集合：调用方能从外部改坏不变量
private final List<Item> items = new ArrayList<>();
public List<Item> getItems() { return items; }
// ✅ 返回不可变视图
public List<Item> getItems() { return Collections.unmodifiableList(items); }
```

- 默认 `final` 字段；纯数据载体优先用 `record`。
- 构造完成即不变量成立；需要 `init()` 二段构造的设计先回 `hf-design` 审视。

**事故类**：不变量被外部破坏、别名修改。**自检**：可变内部不外泄（不可变视图/防御性拷贝）；字段默认 final；数据载体用 record。

## 工具链

基线命令（新代码零新增告警，"历史就有"不豁免本次触碰的文件）：

- 格式化：`google-java-format --replace $(git diff --name-only -- '*.java')`（或 Spotless 插件统一）。
- 静态分析：ErrorProne `-Xep:...`；SpotBugs（启用 `BAD_PRACTICE,CORRECTNESS,MALICIOUS_CODE,SECURITY`）；Checkstyle `google_checks.xml`。
- 空安全：`@Nullable`/`@NonNull` 注解按项目工具链（NullAway / JSpecifier）启用并在 CI 校验。
- 测试：JUnit 5 + AssertJ（流式断言）；Mockito 做边界 mock；无隐藏 `sleep` 的确定性测试。
- 新增 lint/类型告警必须修复，或带理由 + 范围就地抑制（`@SuppressWarnings("rule") // 理由：作用范围`）。

工具抓的就是本文每节的事故类：NPE、缺 `hashCode`、裸类型、竞态、吞异常、泄漏。

**自检**：格式化已应用；ErrorProne/SpotBugs/Checkstyle 零新增告警；抑制项带理由与范围。

## 自检清单（汇总）

- [ ] 集合/数组不返回 null；可缺失单值用 `Optional` 返回且不裸 `get()`、不赋 null
- [ ] `equals`/`hashCode` 成对且基于同组字段；Map key/Set 元素不可变
- [ ] 无裸泛型类型；`@SuppressWarnings` 最小化且带理由；通配符符合 PECS
- [ ] 共享可变状态用 j.u.concurrent / 原子 / 专属锁保护；不在 `this` 上同步；持锁不调外部回调
- [ ] 无被吞异常；包装保留 cause；无泛 `catch`；无裸 `Exception` 抛出
- [ ] `AutoCloseable` 资源用 try-with-resources；无手写 finally close；无 finalizer
- [ ] 可变内部不外泄；字段默认 final；数据载体用 record
- [ ] 格式化已应用；静态分析零新增告警；抑制项带理由与范围

## 支撑参考

| 文件 | 用途 |
|---|---|
| `references/framework-conventions.md` | Spring Boot / Quarkus 框架专属约定（DI、配置、异常映射、测试切片）——属框架而非语言，按项目栈选用 |

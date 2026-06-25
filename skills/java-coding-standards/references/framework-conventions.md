# Java 框架专属约定（Spring Boot / Quarkus）

> 这些是**框架**约定，不是语言级规则，因此不进 `SKILL.md`。仅当工作项使用对应框架时叠加；与项目实际版本/栈冲突时以项目为准。先从构建文件判定框架：含 `spring-boot` → 用 Spring 约定；含 `quarkus` → 用 Quarkus 约定；都没有 → 只用语言级规则。

## 依赖注入

```java
// [Spring] ✅ 构造器注入（不用字段 @Autowired）
@Service
public class MarketService {
    private final MarketRepository repo;
    public MarketService(MarketRepository repo) { this.repo = repo; }
}
// [Spring] ❌ 字段注入：无法 final、难测试、隐藏依赖
@Autowired private MarketRepository repo;

// [Quarkus] ✅ 构造器注入或包私有字段注入（避免代理问题）
@ApplicationScoped
public class MarketService {
    @Inject MarketRepository repo;   // 包私有可接受
}
// [Quarkus] ❌ 需要拦截/懒加载时用 @Singleton（不可代理）→ 用 @ApplicationScoped
```

## 异常映射（集中处理）

```java
// [Spring]
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MarketNotFoundException.class)
    public ResponseEntity<ErrorResponse> handle(MarketNotFoundException e) {
        return ResponseEntity.status(404).body(ErrorResponse.from(e));
    }
}

// [Quarkus] ExceptionMapper 或 @ServerExceptionMapper
@Provider
public class MarketNotFoundMapper implements ExceptionMapper<MarketNotFoundException> {
    public Response toResponse(MarketNotFoundException e) {
        return Response.status(404).entity(ErrorResponse.from(e)).build();
    }
}
```

错误响应的 HTTP 契约（状态码、错误信封、字段级细节）属服务端/API 领域约束，框架层只负责接入点与映射；命中相应领域技能时叠加其规则。

## 配置

```java
// [Spring] 类型安全配置
@ConfigurationProperties(prefix = "market")
public record MarketProperties(int maxPageSize, Duration cacheTtl) {}

// [Quarkus] 构建期校验的类型安全配置
@ConfigMapping(prefix = "market")
public interface MarketConfig { int maxPageSize(); Duration cacheTtl(); }
```

## 反应式（Quarkus）

```java
// ✅ 反应式端点返回 Uni/Multi，全程非阻塞
public Uni<Market> findBySlug(String slug) {
    return Market.<Market>find("slug", slug).firstResult()
        .onItem().ifNull().failWith(() -> new MarketNotFoundException(slug));
}
// ❌ 在 Uni/Multi 管道里做阻塞调用 → 阻塞事件循环
// ❌ 对共享 Uni 多次 subscribe（用 Uni.memoize()）
```

## 测试切片

| 框架 | 单元测试 | 集成测试 |
|---|---|---|
| Spring | `@WebMvcTest`（控制器）、`@DataJpaTest`（仓库）、Mockito | `@SpringBootTest` + `@MockBean` |
| Quarkus | 纯 JUnit 5 + Mockito（无 `@QuarkusTest`） | `@QuarkusTest` + `@InjectMock`；DB/Kafka/Redis 用 Dev Services |

## 常见框架反模式

- [Quarkus] `@Singleton` 误用于需要拦截/代理的 bean —— 用 `@ApplicationScoped`
- [Quarkus] 混用 `quarkus-resteasy-reactive` 与经典 `quarkus-resteasy` —— 选一个栈
- [Quarkus] 同一限界上下文里混用 Panache 活动记录与仓库模式 —— 选一个
- [Spring] 在切片测试里启动整个上下文（`@SpringBootTest`）做单元验证 —— 用对应切片注解

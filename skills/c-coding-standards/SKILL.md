---
name: c-coding-standards
description: 在编写、修改或评审 C 代码（.c 源文件、.h 头文件、C 单元测试、C ABI 边界、构建脚本中的 C 编译选项）时使用。提供指针所有权、手动内存、缓冲区容量、整数与未定义行为、宏、头文件、错误返回的具体规则与正反例。只适用于 C 语言；其他语言或 C++ 代码使用对应语言自己的 coding-standards 技能。
---

# C Coding Standards

## 总览

C 给了你足够的绳子。本技能在 `hf-clean-code` 的通用标准之上叠加 C 的语言规则，不能替代通用 clean-code 自检。每条规则针对一类真实事故（越界、悬垂、泄漏、未定义行为、整数溢出）。项目声明了 MISRA C / CERT C 子集时以项目为准，本文是未声明时的默认底线。

通用规则（函数长度、命名要表意、注释为何而非是什么）属于 `hf-clean-code`，不在本技能重复。领域规则（嵌入式内存预算、车载 MISRA 配置、协议字段语义）属于领域技能；流程规则（评审流程、提交规范）属于 `AGENTS.md`。

## 反合理化表

| 话术 | 现实 |
|---|---|
| 「测试全绿，所以没问题」 | 单测只证明被覆盖的外部行为；UB/泄漏/越界要靠编译告警 + sanitizer + 静态分析，测试不替代 |
| 「这段是历史代码，告警一直就有」 | 历史告警不豁免本次触碰的文件；触碰即按 critical 闭环 |
| 「这里肯定不会溢出/越界」 | 凡是依赖调用方输入的不变式都是事故源，必须显式校验，不能靠"肯定" |
| 「宏就这一次没事」 | 函数宏的多求值陷阱与本次调用无关，是宏本身的缺陷；要么 static inline，要么严格括号 |
| 「编译器/优化器会处理 UB」 | UB 是不存在的执行路径，编译器可合法地删掉你的检查；UB 不是"实现定义" |

## 指针与所有权

每个跨函数边界的指针必须能回答：**谁拥有它、它活多久、能否为 NULL**。约定写进签名和头文件注释：

```c
/* 返回的指针由调用方负责 free */
char *config_dump_alloc(const config_t *cfg);
/* 返回内部静态存储的指针：只读、下次调用前有效、不得 free */
const char *err_to_str(int err);
/* item 的所有权转移给队列：入队成功后调用方不得再访问 */
int queue_push_owned(queue_t *q, item_t *item);
/* buf 由调用方提供并保证在调用期间有效（借用） */
int frame_parse(const uint8_t *buf, size_t len, frame_t *out);
```

- 公共 API 的指针参数必须有 NULL 语义：要么文档写明"不得为 NULL"并在入口校验，要么定义 NULL 时的行为。
- **真正的防线是所有权唯一**：一块内存只有一个 owner 负责释放，其余都是借用。释放后置空只是局部惯用法，不能靠它防 UAF。
- 不返回局部变量地址；不把栈上 buffer 的指针存进生命周期更长的结构。
- 跨模块传 `void *ctx` 时，注册方与回调方必须是同一约定的两端；`void *` 的强转必须紧邻类型校验（魔数/类型 tag）。

**事故类**：悬垂指针、double-free、UAF、所有权不清导致的泄漏或重复释放。

```c
/* ❌ 返回栈地址——调用即悬垂 */
const char *label(void) { char buf[8] = "x"; return buf; }
/* ✅ 借用：调用方保证 buf 在调用期间有效 */
int parse(const uint8_t *buf, size_t len, frame_t *out);
```

**自检**：每个跨边界指针的所有权/生命周期/NULL 语义在签名或注释中可读。

## 内存与资源

- 每个 `malloc`/`open`/`lock` 出现时，先写它的释放路径再写中间逻辑。多资源获取用集中清理出口（goto cleanup）：获取顺序与释放顺序相反，失败跳到对应标签。
- `malloc` 返回必须检查；分配大小用 `sizeof(*p)` 而非 `sizeof(type)`（类型改名时不会悄悄错）：

```c
mode_entry_t *e = malloc(sizeof(*e));              /* ✅ */
mode_entry_t *e = malloc(sizeof(mode_entry_t *));  /* ❌ 经典事故：分配了指针大小 */
if (!e) return ERR_NOMEM;
```

- 结构体含指针成员时提供成对的 `xxx_create`/`xxx_destroy`，destroy 负责全部深层释放且可安全接受 NULL。
- 动态分配是否允许、允许在哪个阶段（仅初始化期 vs 运行期）由设计声明；命中领域技能时以该领域的内存和实时性约束为准。

**事故类**：泄漏（提前返回路径漏释放）、分配大小错误、UAF（destroy 后仍被引用）。

**自检**：多资源函数用集中清理出口；malloc 用 `sizeof(*p)` 且检查返回；create/destroy 成对。

## 缓冲区与字符串

- 所有写入 buffer 的接口同时传 buffer 与容量；内部用容量做上界，绝不信任"调用方肯定给够了"。
- 字符串拼装一律 `snprintf` 并检查返回值是否 ≥ 容量（截断检测）：

```c
/* ❌ strcpy/strcat/sprintf 进入新代码 = critical */
sprintf(path, "%s/%s", dir, name);
/* ✅ */
int n = snprintf(path, sizeof(path), "%s/%s", dir, name);
if (n < 0 || (size_t)n >= sizeof(path)) return ERR_NAME_TOO_LONG;
```

- `memcpy` 的 len 来自外部输入时，先校验 len ≤ 目标容量再拷贝；协议解析中"先读长度字段再按它拷贝"是最高危路径，必须有显式上界检查。
- 数组遍历的循环边界用 `sizeof(arr)/sizeof(arr[0])`（或项目的 ARRAY_SIZE 宏），不手写常数。
- 禁用 `gets`（已从 C11 移除）；新代码不用 `strcpy`/`strcat`/`sprintf`，改 `snprintf`/`strncpy_s` 等带容量版本。

**事故类**：栈/堆缓冲区溢出、off-by-one、字符串未终止、截断后数据损坏。

**自检**：无 strcpy/strcat/sprintf/gets 新增；外部长度参与的拷贝有上界检查。

## 整数与未定义行为

- 边界/长度/索引用 `size_t`；协议与寄存器字段用定宽类型（`uint8_t`/`uint32_t`），不用裸 `int`/`long` 承载有格式要求的数据。
- 有符号/无符号混合比较是事故源：`if (len - 1 > 0)` 在 `len==0` 且 len 为无符号时恒真。减法前先确认不下溢：`if (len > 0 && idx < len - 1)` 或改写为加法 `idx + 1 < len`。
- 乘法可能溢出的分配：`malloc(n * size)` 在 n 来自外部时先检查 `n <= MAX / size`，或用 `calloc`。
- 位运算的操作数显式无符号：`1u << bit`；移位量必须小于位宽（`<<` 负数或移位量 ≥ 位宽是 UB）。
- **有符号整数溢出是 UB**：累加、`a+b`、`a*b` 在可能溢出时先校验，不能假设回绕（无符号溢出是定义良好的回绕，但通常是 bug）。
- **严格别名（strict aliasing）是 UB**：不通过 `union` 或 `memcpy` 而用不兼容类型指针读写存储，编译器可据此"优化"掉你的代码：

```c
/* ❌ 严格别名违反：以 int* 读 float 存储 */
float f = 1.0f; int *p = (int *)&f; return *p;
/* ✅ 类型双关走 union（C 合法）或 memcpy */
uint32_t bits; memcpy(&bits, &f, sizeof bits); return bits;
```

- **求值顺序**：`a[i] = i++;`、`f(i++, i)` 等含多个未测序副作用的表达式是 UB。不要在同一表达式里对同一对象既修改又读取而无序列点。

**事故类**：整数溢出/下溢、符号扩展错误、UB 被优化器利用、类型双关读错值。

**自检**：无有符号/无符号混合比较告警；定宽类型用于协议/寄存器；溢出路径有显式校验；无违反严格别名的强转。

## 宏

能不用宏就不用：常量用 `enum` 或 `static const`，短函数用 `static inline`。必须用宏时：

```c
/* ❌ 多次求值：max(x++, y) 让 x 加了两次 */
#define MAX(a, b) ((a) > (b) ? (a) : (b))
/* ✅ 改用 static inline——有类型检查、可下断点、无求值陷阱 */
static inline int32_t max_i32(int32_t a, int32_t b) { return a > b ? a : b; }
```

- 仍需宏的场景（token 拼接、编译期开关、`_Generic` 泛型）：参数全部加括号、整体加括号、多语句体包 `do { ... } while (0)`。
- 宏名 `ALL_CAPS`（避免与变量冲突）；函数宏优先考虑 `static inline` 或 `_Generic`。
- 条件编译块尽量小且互斥分支都能编译；`#if 0` 不是注释手段（删）。

**事故类**：多求值副作用、宏展开优先级错误、宏名污染、不可调试。

**自检**：新增宏有必要性；函数宏满足括号 + do-while(0)，或已改 static inline；常量宏已转 enum/static const。

## 头文件

- 头文件是模块的契约：只放公共 API、公共类型、必要常量。内部函数 `static` 留在 .c；内部结构体用不透明指针隐藏：

```c
/* public.h —— 调用方只见句柄，结构体布局可自由演进 */
typedef struct mode_service mode_service_t;
mode_service_t *mode_service_create(const mode_config_t *cfg);
/* internal .c 里才有 struct mode_service { ... }; */
```

- 每个头文件自包含（include 它需要的一切）、有 include guard、能被单独编译。
- 头文件里不定义变量、不放 `static` 函数实现（`static inline` 的小函数除外）。
- include 顺序：自己的头文件最先（强制自包含检验），然后系统头、第三方、项目内。

**事故类**：模块耦合、重新定义、隐藏依赖、ABI 脆弱。

**自检**：头文件自包含、最小暴露、内部结构不透明、有 include guard。

## 错误返回

- 模块统一一种错误约定（负 errno 风格 / 项目错误码枚举 / 0=成功），不混用；出参与返回码分离：数据走出参，状态走返回值。
- 调用方检查每个可失败调用；本技能补充 C 特有项：`snprintf`/`read`/`write` 的部分成功（短写）要处理；注册回调的返回值约定写进回调 typedef 的注释。
- 失败路径上的出参状态写进契约（"失败时 `*out` 不被修改"是最友好的约定，实现也要真的遵守）。

**事故类**：错误被吞、错误码不一致、失败时调用方使用未初始化的出参。

**自检**：错误约定全模块一致；失败路径出参状态符合契约；每个可失败调用都被检查。

## const 与作用域

- 指针参数不修改指向内容 → `const T *`；查表数据 → `static const`（进只读段，嵌入式省 RAM）。
- 一切能 `static` 的文件内符号都 `static`（链接期命名空间卫生）。
- 变量在首次使用处声明并初始化；未初始化变量 + 复杂分支 = 未定义行为温床。

**事故类**：无意修改、符号冲突、读未初始化值（UB）。

**自检**：只读参数用 const；文件内符号 static；无读未初始化路径。

## 工具链

基线命令（新代码零新增告警，项目允许时加 `-Werror`）：

- 编译：`gcc -std=c17 -Wall -Wextra -Werror -Wconversion -pedantic`（`-Wconversion` 抓有符号/无符号与窄化；`-pedantic` 拒绝扩展方言）。
- 运行期：测试与本地调试开 `-fsanitize=address,undefined -g -fno-omit-frame-pointer`（ASan 抓越界/UAF/double-free，UBSan 抓溢出/移位/严格别名相关）。
- 静态分析：`cppcheck --enable=all`；`clang-tidy -checks='cert-*,bugprone-*,clang-analyzer-*'`。
- 新增告警必须修复，或带理由 + 范围就地抑制；"历史就有"不豁免本次触碰的文件。

工具抓的就是本文每节的事故类：越界、泄漏、悬垂、截断、溢出、宏陷阱、UB。

**自检**：编译零新增警告；静态分析新增项闭环；测试至少在本地跑过一次 ASan/UBSan。

## 自检清单（汇总）

- [ ] 每个跨边界指针的所有权/生命周期/NULL 语义在签名或注释中可读
- [ ] 多资源函数用集中清理出口；malloc 用 `sizeof(*p)` 且检查返回；create/destroy 成对
- [ ] 无 strcpy/strcat/sprintf/gets 新增；外部长度参与的拷贝有上界检查
- [ ] 无有符号/无符号混合比较告警；定宽类型用于协议/寄存器；溢出/严格别名路径闭环
- [ ] 新增宏有必要性；函数宏满足括号 + do-while(0)，或已改 static inline
- [ ] 头文件自包含、最小暴露、内部结构不透明
- [ ] 错误约定全模块一致；失败路径出参状态符合契约
- [ ] 编译零新增警告；静态分析/sanitizer 新增项闭环

---
name: python-coding-standards
description: 在编写、修改或评审 Python 代码（模块、包、pytest 测试、pyproject 配置）时使用。提供可变默认参数、类型注解、异常与 EAFP、资源管理、相等与身份、可变性与数据容器、并发的具体规则与正反例。只适用于 Python（3.9+）；静态类型语言用各自的语言技能。
---

# Python Coding Standards

## 总览

Python 的核心危险是**动态与隐式：错误延迟到运行期才暴露，可变共享状态在背后累积**。本技能在 `hf-clean-code` 的通用标准之上叠加 Python（3.9+）语言规则，不能替代通用 clean-code 自检。每条规则针对一类真实事故（跨调用状态污染、运行期类型错误、被吞异常、资源泄漏、身份/相等混淆）。项目声明了 PEP 8 / 团队规范子集时以项目为准，本文是未声明时的默认底线。

通用规则（函数长度、命名表意、注释写 why 不写 what）属 `hf-clean-code`，不在本技能重复；领域规则（API 契约、领域模型）属领域技能；流程规则（评审、提交）属 `AGENTS.md`。

## 反合理化表

| 话术 | 现实 |
|---|---|
| 「测试全绿，所以没问题」 | 单测只证明被覆盖路径；可变默认参数/类型错误/泄漏要靠 mypy + ruff + 具体规则，测试不替代 |
| 「可变默认参数没事，反正每次调用都用新的」 | 默认参数在函数定义时求值一次，所有调用共享同一对象 = 跨调用状态污染；这是 Python 最经典事故 |
| 「`except:` 兜底最省事」 | 裸 except 连 `KeyboardInterrupt`/`SystemExit` 都吞，掩盖所有 bug |
| 「`== None` 和 `is None` 一样」 | `==` 调用 `__eq__` 可能被重载返回错误结果；`is None` 才是身份判定，不可被覆盖 |
| 「类型注解是开销，跳过省事」 | 缺注解时类型错误拖到运行期；公共签名必须注解让 mypy 兜底 |
| 「这段是历史代码，lint 一直就有」 | 历史 lint 不豁免本次触碰的文件；触碰即按 critical 闭环 |

## 可变默认参数与共享可变状态

默认参数在函数定义时求值一次，可变默认值会在调用间累积——经典事故：

```python
# ❌ 同一个 list 被所有调用共享，跨调用累积
def append_to(item, items=[]):
    items.append(item)
    return items
# ✅ 用 None 哨兵，每次新建
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

- 默认参数只用不可变值（`None`、数字、字符串、元组）。
- **类属性上的可变容器会被所有实例共享**：实例级可变状态在 `__init__` 里创建，或用 `dataclass` 的 `field(default_factory=list)`。
- 不可变数据用元组 / `frozenset` / `frozen=True` 的 dataclass，避免别名修改。

**事故类**：跨调用状态污染、跨实例状态泄漏。**自检**：无可变默认参数；类级可变容器未被实例共享。

## 类型注解

注解是给 mypy 和读者的契约，缺失时类型错误拖到运行期：

```python
# ❌ 无注解，参数与返回类型靠猜，IDE/mypy 无法检查
def process(user_id, data, active=True):
    ...
# ✅ 公共函数签名全注解；3.9+ 用内置泛型，可缺失值用 X | None
def process(user_id: str, data: dict[str, Any], active: bool = True) -> User | None:
    ...
```

- 公共函数 / 方法签名必须注解参数与返回值；`mypy`（或 pyright）在 CI 校验。
- 不用裸 `Any` 逃避类型检查；确实动态时用 `object` 或 `Protocol` 表达约束。
- 接口约束优先用 `typing.Protocol`（结构化鸭子类型）而非继承。

**事故类**：运行期类型错误、IDE 补全失效、契约缺失。**自检**：公共签名有注解；无裸 `Any` 逃避；mypy 通过。

## 异常与 EAFP

Python 偏好 EAFP（先做再处理异常）而非过度前置检查；但捕获必须精确：

```python
# ❌ 裸 except 吞掉一切（含 KeyboardInterrupt/SystemExit），掩盖 bug
try:
    risky()
except:
    pass
# ✅ 捕获具体异常；包装时用 from 保留异常链
try:
    return Config.from_json(read(path))
except FileNotFoundError as e:
    raise ConfigError(f"config not found: {path}") from e
except json.JSONDecodeError as e:
    raise ConfigError(f"invalid JSON: {path}") from e
```

- 不写裸 `except:` 或 `except Exception: pass`；捕获最具体的异常。
- 重新抛出包装异常时用 `raise NewError(...) from e` 保留 traceback。
- 自定义异常建一个应用根类（`class AppError(Exception)`）再派生，便于边界统一捕获。
- 不用异常做正常控制流的高频路径（性能与可读性）。

**事故类**：被吞错误、异常链断、控制流滥用。**自检**：无裸 `except` / `except: pass`；包装异常用 `from`；捕获具体类型。

## 资源管理

```python
# ❌ 手动 open/close：异常时漏关
f = open(path)
data = f.read()
f.close()
# ✅ with 上下文管理器，异常路径也释放
with open(path) as f:
    data = f.read()
```

- 文件、锁、连接、事务一律用 `with`；多个资源用嵌套或 `with a, b:`。
- 自定义资源实现 `__enter__`/`__exit__`，或用 `@contextlib.contextmanager`；`__exit__` 返回 falsy（不吞异常，除非有意）。
- **不**在 `finally` 里手动 close 已被 `with` 接管的资源——重复释放与可读性问题。

**事故类**：资源泄漏、异常路径漏关。**自检**：文件/锁/连接用 `with`；自定义资源实现上下文管理协议。

## 相等与身份

```python
# ❌ 用 == 比较 None / 用 is 比较值
if value == None: ...
if name is "admin": ...   # 字符串驻留是实现细节，不可靠
# ✅ is 只用于 None 和单例；== 用于值比较
if value is None: ...
if name == "admin": ...
```

- `is`/`is not` 只用于 `None`、`True`/`False` 单例判定（身份，不可被 `__eq__` 覆盖）；其余值比较用 `==`。
- 类型判定用 `isinstance(x, T)`，不用 `type(x) == T`（破坏子类与多态）。
- 作为 dict key / set 元素的对象必须可哈希且不可变。

**事故类**：None 判定被 `__eq__` 污染、类型判定破坏多态。**自检**：`is` 仅用于 None/单例；值比较用 `==`；类型判定用 `isinstance`。

## 数据容器与可变性

```python
# ❌ 用裸 dict/tuple 在层间传业务对象，字段靠约定，拼写错误静默
user = {"id": "1", "naem": "Alice"}   # 拼错 key 不报错
# ✅ dataclass：字段、类型、__init__/__repr__/__eq__ 自动且受检
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: str
    name: str
    is_active: bool = True
```

- 多字段业务对象用 `@dataclass`（不可变用 `frozen=True`）或 `NamedTuple`，不用裸 dict/tuple 传递。
- dataclass 可变默认用 `field(default_factory=list)`，不用裸 `[]`/`{}`（同可变默认参数事故）。
- 需要修改时显式用 `dataclasses.replace` 或新建实例，不破坏 frozen 语义。
- 热路径上字段固定的小对象用 `__slots__` 降内存（也防止意外加属性）。

**事故类**：拼写错误静默、别名修改、跨实例共享。**自检**：业务对象用 dataclass/NamedTuple；可变默认用 `default_factory`；不可变用 `frozen=True`。

## 导入与 PEP 8 命名

PEP 8 的命名与导入是 Python 的语言特化规则（不是通用 clean-code）：

```python
# ❌ 通配导入污染命名空间、遮蔽名字、破坏静态分析
from os.path import *
# ✅ 显式导入；顺序：标准库 → 第三方 → 本地，各组间空行
import json
from pathlib import Path

import requests

from mypackage.models import User
```

- 不用 `from module import *`（`__init__.py` 的受控 re-export 除外，且配 `__all__`）。
- 命名：`snake_case`（函数/变量/模块）、`PascalCase`（类）、`UPPER_SNAKE_CASE`（常量）。
- 导入排序由 `isort`/`ruff` 自动维护；不在函数内部隐藏顶层依赖（循环依赖除外，且注明）。

**事故类**：命名遮蔽、隐藏依赖、静态分析失效。**自检**：无 `import *`；命名符合 PEP 8；导入分组有序。

## 并发

GIL 决定了选型：选错模型 = 白忙：

```python
# ❌ 在 async 协程里做阻塞调用，阻塞整个事件循环
async def handler():
    data = requests.get(url).text   # 同步阻塞
# ✅ async 路径全程 await 非阻塞 IO
async def handler():
    async with aiohttp.ClientSession() as s, s.get(url) as r:
        data = await r.text()
```

- IO 密集：`asyncio` 或 `ThreadPoolExecutor`；CPU 密集：`ProcessPoolExecutor`/多进程（线程受 GIL 限制无法并行算）。
- 不在 `async` 函数里调用同步阻塞 IO；阻塞调用放线程池（`loop.run_in_executor`）。
- 跨线程共享可变状态加锁；`concurrent.futures` 收集结果时处理每个 future 的异常。

**事故类**：事件循环阻塞、数据竞争、未处理的 future 异常。**自检**：并发模型与负载匹配；async 路径无阻塞调用；跨线程状态加锁。

## 工具链

基线命令（新代码零新增告警，"历史就有"不豁免本次触碰的文件）：

- 格式化与 lint：`ruff check --fix $(git diff --name-only -- '*.py') && ruff format`（替代 black + isort + flake8）。
- 类型：`mypy --strict .`（或至少 `--disallow-untyped-defs`）；CI 校验。
- 安全：`bandit -r .`；依赖 `pip-audit`。
- 测试：`pytest`（+ `pytest-cov`）；fixture 管理资源，参数化覆盖边界；无隐藏 `time.sleep`。
- 配置集中在 `pyproject.toml`（`[tool.ruff]`/`[tool.mypy]`/`[tool.pytest.ini_options]`）。
- 新增 lint / 类型告警必须修复，或带理由 + 范围就地抑制（`# noqa: CODE  # 理由：作用范围` / `# type: ignore[code]  # 理由`）。

工具抓的就是本文每节的事故类：可变默认、类型错误、吞异常、泄漏、`== None`。

**自检**：ruff/mypy 零新增告警；抑制项带理由与范围；测试无隐藏 sleep。

## 自检清单（汇总）

- [ ] 无可变默认参数；类级可变容器未被实例共享
- [ ] 公共签名有类型注解；无裸 `Any` 逃避；mypy 通过
- [ ] 无裸 `except` / `except: pass`；包装异常用 `from`；捕获具体类型
- [ ] 文件/锁/连接用 `with`；自定义资源实现上下文管理协议
- [ ] `is` 仅用于 None/单例；值比较用 `==`；类型判定用 `isinstance`
- [ ] 业务对象用 dataclass/NamedTuple；可变默认用 `default_factory`；不可变用 `frozen=True`
- [ ] 无 `import *`；命名符合 PEP 8；导入分组有序
- [ ] 并发模型与负载匹配；async 路径无阻塞调用；跨线程状态加锁
- [ ] ruff/mypy 零新增告警；抑制项带理由与范围

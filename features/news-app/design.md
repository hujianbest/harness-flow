# 技术设计：新闻 APP

## 概述

本设计定义新闻 APP 的技术实现方案。系统采用前后端分离架构，移动端使用 Flutter 实现跨平台，后端使用 FastAPI + PostgreSQL 提供内容聚合、智能推荐和用户服务。

**核心设计决策**：
- **移动端**：Flutter（一套代码支持 iOS/Android）
- **后端**：FastAPI + Python（快速开发、生态丰富）
- **数据库**：PostgreSQL（关系型数据）+ Redis（缓存）+ Qdrant（向量）
- **AI 服务**：OpenAI API（MVP 阶段）
- **推荐算法**：规则算法（MVP）→ ML 模型（v2.0）

## 架构

### 系统分层

```
┌─────────────────────────────────────────────────────────┐
│                    移动端 (Flutter)                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ 首页   │  │ 搜索   │  │ 收藏   │  │ 设置   │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │
└─────────────────────────────────────────────────────────┘
                           │ HTTPS/JSON
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    API 网关 (Nginx)                      │
│              限流、认证、路由、TLS 终止                    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   后端服务 (FastAPI)                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐            │
│  │ Auth 服务  │  │ Content 服务 │  │ User 服务 │            │
│  └───────────┘  └───────────┘  └───────────┘            │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐            │
│  │ Recommend │  │ Search    │  │ Feed      │            │
│  │   服务     │  │  服务      │  │ 服务      │            │
│  └───────────┘  └───────────┘  └───────────┘            │
└─────────────────────────────────────────────────────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Redis   │  │Qdrant    │  │OpenAI API│
│  (主库)  │  │  (缓存)  │  │ (向量DB) │  │  (LLM)   │
└─────────┘  └──────────┘  └──────────┘  └──────────┘
```

### 架构说明

**表示层（Flutter）**：
- 负责用户交互和界面渲染
- 状态管理：Provider/Riverpod
- 本地缓存：Hive/SQLite
- 网络请求：Dio

**API 网关（Nginx）**：
- TLS 终止（HTTPS）
- 限流（令牌桶算法）
- 请求路由
- 静态资源服务

**业务层（FastAPI）**：
- RESTful API 设计
- JWT 认证
- 异步处理（asyncio）
- 依赖注入

**数据层**：
- PostgreSQL：用户、文章、源、阅读记录
- Redis：会话、缓存、热点数据
- Qdrant：文章向量（v2.0 推荐）
- Elasticsearch：全文搜索（可选，v2.0）

## 模块设计

### 1. Auth 认证模块

**职责**：
- 用户注册、登录、登出
- Token 颁发和验证
- 第三方登录（微信、Apple ID）
- 密码重置

**接口**：
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `POST /api/auth/refresh` - 刷新 Token
- `POST /api/auth/reset-password` - 重置密码
- `GET /api/auth/verify/{token}` - 验证邮箱

**依赖**：
- User 服务（用户数据）
- Redis（Token 黑名单）
- 邮件服务（验证邮件）

### 2. Content 内容模块

**职责**：
- 新闻源管理（CRUD）
- 文章抓取和解析
- RSS 源验证
- 内容质量评分
- AI 摘要生成

**接口**：
- `GET /api/sources` - 获取新闻源列表
- `POST /api/sources` - 添加自定义源
- `DELETE /api/sources/{id}` - 删除源
- `POST /api/sources/{id}/validate` - 验证 RSS 源
- `GET /api/articles` - 获取文章列表
- `GET /api/articles/{id}` - 获取文章详情
- `POST /api/articles/{id}/quality` - 计算质量分
- `POST /api/articles/{id}/summary` - 生成摘要

**依赖**：
- Feed 服务（RSS 抓取）
- OpenAI API（摘要生成）
- PostgreSQL（内容存储）

### 3. User 用户模块

**职责**：
- 用户资料管理
- 兴趣标签管理
- 收藏管理
- 阅读历史
- 阅读统计
- 会员管理

**接口**：
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新用户信息
- `GET /api/users/me/tags` - 获取兴趣标签
- `PUT /api/users/me/tags` - 更新兴趣标签
- `GET /api/users/me/favorites` - 获取收藏列表
- `POST /api/users/me/favorites` - 添加收藏
- `DELETE /api/users/me/favorites/{id}` - 删除收藏
- `GET /api/users/me/history` - 获取阅读历史
- `GET /api/users/me/stats` - 获取阅读统计

**依赖**：
- PostgreSQL（用户数据）
- Redis（缓存）

### 4. Recommend 推荐模块

**职责**：
- 基于兴趣标签推荐
- 基于阅读历史推荐
- 排除已读文章
- 推荐反馈处理

**接口**：
- `GET /api/recommend/feed` - 获取推荐列表
- `POST /api/recommend/feedback` - 提交反馈（不感兴趣/相关）

**依赖**：
- User 服务（兴趣标签）
- Content 服务（文章数据）
- 阅读历史（已读过滤）

### 5. Search 搜索模块

**职责**：
- 全文搜索（标题+摘要）
- 标签筛选
- 搜索历史
- 热门搜索

**接口**：
- `GET /api/search` - 搜索文章
- `GET /api/search/history` - 搜索历史
- `GET /api/search/trending` - 热门搜索

**依赖**：
- PostgreSQL（全文搜索，v1.0）
- Elasticsearch（v2.0）

### 6. Feed 订阅模块

**职责**：
- RSS 定时抓取
- 文章解析和存储
- 源健康监控
- 抓取队列管理

**接口**：
- `POST /api/feed/trigger` - 手动触发抓取
- `GET /api/feed/status` - 抓取状态

**依赖**：
- Content 服务（文章存储）
- Celery/RQ（任务队列）

### 模块关系图

```
┌───────────┐     ┌───────────┐     ┌───────────┐
│   Auth    │────▶│   User    │────▶│ Recommend │
└───────────┘     └───────────┘     └───────────┘
                       │                   │
                       ▼                   ▼
                 ┌───────────┐     ┌───────────┐
                 │  Content  │◀────│  Search   │
                 └───────────┘     └───────────┘
                       ▲
                       │
                 ┌───────────┐
                 │   Feed    │
                 └───────────┘
```

## 接口设计

### POST /api/auth/register

**目的**: 用户注册

**输入**:
| 参数 | 类型 | 必需 | 描述 | 约束 |
|------|------|------|------|------|
| email | string | 是 | 用户邮箱 | 格式验证 |
| password | string | 是 | 密码 | 8-64 字符 |
| name | string | 是 | 用户名称 | 1-50 字符 |

**输出**:
| 字段 | 类型 | 描述 |
|------|------|------|
| userId | string | 用户 ID |
| token | string | JWT Token（30 天有效）|
| refreshToken | string | 刷新 Token |

**错误**:
| 错误 | 条件 | HTTP 状态 |
|------|------|-----------|
| ValidationError | 输入无效 | 400 |
| ConflictError | 邮箱已存在 | 409 |
| RateLimitError | 超过限流 | 429 |
| SystemError | 系统错误 | 500 |

**副作用**:
- 创建数据库用户记录
- 发送验证邮件
- 记录审计日志

**前置条件**:
- 邮箱未被注册
- IP 未超过注册限流（5 次/小时）

**后置条件**:
- 用户记录持久化
- 验证邮件入队

---

### POST /api/auth/login

**目的**: 用户登录

**输入**:
| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| email | string | 是 | 用户邮箱 |
| password | string | 是 | 密码 |

**输出**:
| 字段 | 类型 | 描述 |
|------|------|------|
| userId | string | 用户 ID |
| token | string | JWT Token |
| refreshToken | string | 刷新 Token |

**错误**:
| 错误 | 条件 | HTTP 状态 |
|------|------|-----------|
| ValidationError | 输入无效 | 400 |
| UnauthorizedError | 邮箱或密码错误 | 401 |
| RateLimitError | 登录尝试过多 | 429 |

---

### GET /api/articles

**目的**: 获取文章列表

**输入** (Query):
| 参数 | 类型 | 必需 | 描述 | 默认值 |
|------|------|------|------|--------|
| page | int | 否 | 页码 | 1 |
| pageSize | int | 否 | 每页数量 | 20 |
| sourceId | string | 否 | 筛选源 ID | - |
| tag | string | 否 | 筛选标签 | - |
| minQuality | int | 否 | 最低质量分 | 0 |

**输出**:
| 字段 | 类型 | 描述 |
|------|------|------|
| articles | array | 文章列表 |
| total | int | 总数 |
| page | int | 当前页 |
| pageSize | int | 每页数量 |

**Article 对象**:
```json
{
  "id": "uuid",
  "title": "文章标题",
  "summary": "智能摘要",
  "source": {
    "id": "uuid",
    "name": "源名称",
    "icon": "icon_url"
  },
  "publishedAt": "2024-01-01T00:00:00Z",
  "tags": ["科技", "AI"],
  "readTime": 5,
  "qualityScore": 4
}
```

---

### POST /api/sources

**目的**: 添加自定义 RSS 源

**输入**:
| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| url | string | 是 | RSS URL |
| name | string | 是 | 源名称 |

**输出**:
| 字段 | 类型 | 描述 |
|------|------|------|
| sourceId | string | 源 ID |
| status | string | pending/validated/failed |

**副作用**:
- 异步验证 RSS 源
- 验证通过后开始抓取

---

### GET /api/recommend/feed

**目的**: 获取个性化推荐

**输入** (Query):
| 参数 | 类型 | 必需 | 描述 | 默认值 |
|------|------|------|------|--------|
| page | int | 否 | 页码 | 1 |
| pageSize | int | 否 | 每页数量 | 20 |

**输出**:
| 字段 | 类型 | 描述 |
|------|------|------|
| articles | array | 推荐文章列表 |
| reason | string | 推荐理由（可选）|

**推荐算法（MVP）**:
1. 获取用户兴趣标签
2. 筛选匹配标签的文章
3. 按质量分 × 时效性权重排序
4. 排除已读文章
5. 返回结果

---

### GET /api/search

**目的**: 搜索文章

**输入** (Query):
| 参数 | 类型 | 必需 | 描述 | 默认值 |
|------|------|------|------|--------|
| q | string | 是 | 搜索关键词 | - |
| page | int | 否 | 页码 | 1 |
| pageSize | int | 否 | 每页数量 | 20 |
| tag | string | 否 | 标签筛选 | - |

**输出**:
| 字段 | 类型 | 描述 |
|------|------|------|
| articles | array | 搜索结果 |
| total | int | 总数 |
| query | string | 搜索词 |

**搜索实现（v1.0）**:
- PostgreSQL 全文搜索（`tsvector` + `GIN` 索引）
- 搜索字段：标题、摘要
- 高亮关键词

## 数据设计

### PostgreSQL Schema

```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    is_premium BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- 兴趣标签表
CREATE TABLE user_tags (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL,
    weight FLOAT DEFAULT 1.0,  -- 权重，用于推荐
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, tag)
);

-- 新闻源表
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    url VARCHAR(500) UNIQUE NOT NULL,
    icon_url VARCHAR(500),
    description TEXT,
    is_system BOOLEAN DEFAULT FALSE,  -- 系统预设或用户自定义
    is_active BOOLEAN DEFAULT TRUE,
    fetch_interval INT DEFAULT 3600,  -- 抓取间隔（秒）
    last_fetched_at TIMESTAMP,
    fetch_error_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sources_active ON sources(is_active) WHERE is_active = TRUE;

-- 文章表
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    summary TEXT,  -- AI 生成的摘要
    content TEXT,  -- 全文内容
    url VARCHAR(1000) UNIQUE NOT NULL,
    author VARCHAR(100),
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT NOW(),
    
    -- 质量评分
    quality_score INT CHECK (quality_score BETWEEN 1 AND 5),
    quality_originality FLOAT,  -- 原创性分
    quality_info_density FLOAT,  -- 信息密度分
    quality_accuracy FLOAT,  -- 准确性分
    quality_readability FLOAT,  -- 可读性分
    
    -- 摘要状态
    summary_status VARCHAR(20) DEFAULT 'pending',  -- pending/done/failed
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 全文搜索索引
ALTER TABLE articles ADD COLUMN search_vector tsvector 
    GENERATED ALWAYS AS (to_tsvector('simple', coalesce(title, '') || ' ' || coalesce(summary, ''))) STORED;
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- 文章标签关联
CREATE TABLE article_tags (
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL,
    PRIMARY KEY (article_id, tag)
);
CREATE INDEX idx_article_tags_tag ON article_tags(tag);

-- 阅读历史表
CREATE TABLE reading_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    read_at TIMESTAMP DEFAULT NOW(),
    read_duration INT,  -- 阅读时长（秒）
    read_percentage INT,  -- 阅读进度百分比
    is_completed BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_reading_history_user ON reading_history(user_id, read_at DESC);
CREATE INDEX idx_reading_history_article ON reading_history(article_id);

-- 收藏表
CREATE TABLE favorites (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, article_id)
);

CREATE INDEX idx_favorites_user ON favorites(user_id, created_at DESC);

-- 推荐反馈表
CREATE TABLE recommend_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    feedback VARCHAR(20) NOT NULL,  -- interested/not_interested
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, article_id)
);

-- 搜索历史表
CREATE TABLE search_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    query VARCHAR(200) NOT NULL,
    result_count INT,
    searched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_history_user ON search_history(user_id, searched_at DESC);

-- 限流记录表（可选，也可用 Redis）
CREATE TABLE rate_limits (
    id VARCHAR(100) PRIMARY KEY,  -- e.g., "register:ip:1.2.3.4"
    count INT DEFAULT 0,
    window_start TIMESTAMP DEFAULT NOW(),
    window_duration INT DEFAULT 3600  -- 秒
);

-- 会员订单表
CREATE TABLE membership_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    duration_months INT NOT NULL,
    payment_method VARCHAR(50),  -- wechat/apple_pay
    status VARCHAR(20) DEFAULT 'pending',  -- pending/paid/failed/refunded
    payment_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    paid_at TIMESTAMP
);

CREATE INDEX idx_membership_orders_user ON membership_orders(user_id, created_at DESC);
```

### Redis 数据结构

```redis
# Token 黑名单（登出时加入）
token:blacklist:{jwt_id} = 1  # TTL = token 剩余有效期

# 会话缓存
session:{user_id} = {
    "last_active": "2024-01-01T00:00:00Z",
    "device": "iOS"
}  # TTL = 30 天

# 热点文章缓存
articles:hot = "{article_ids}"  # TTL = 5 分钟

# 推荐缓存
recommend:{user_id}:{page} = "{article_ids}"  # TTL = 12 小时

# 限流计数器
ratelimit:{ip}:{action} = count  # TTL = 限流窗口

# 在线用户
online:users = "{user_ids}"  # SET
```

### 数据流

```
┌─────────────┐
│ RSS Feed    │
└──────┬──────┘
       │ 定时抓取
       ▼
┌─────────────┐
│ Feed 服务   │ ───▶ 验证/解析/去重
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│ PostgreSQL  │────▶│ Qdrant (v2.0)│
│ articles    │     │  向量化      │
└─────────────┘     └──────────────┘
       │                     │
       │ 推荐               │
       ▼                    ▼
┌─────────────┐     ┌──────────────┐
│ Recommend   │────▶│ 向量搜索     │
│   服务      │     │              │
└─────────────┘     └──────────────┘
       │
       ▼
┌─────────────┐
│   用户      │
└─────────────┘
```

## 技术选型

### 1. 移动端框架：Flutter

**问题**: 需要同时支持 iOS 和 Android

**选择**: Flutter

**理由**:
- 一套代码支持双平台，降低开发成本
- 性能接近原生
- UI 热重载，开发体验好
- 丰富的包生态
- 团队有 Dart/Flutter 经验

**替代方案**:
- React Native：JS 生态，但性能稍逊
- 原生开发：性能最优，但成本翻倍

**风险评估**:
- 低：Flutter 已成熟，多公司生产验证

---

### 2. 后端框架：FastAPI

**问题**: 需要 RESTful API 和异步处理

**选择**: FastAPI + Python

**理由**:
- 异步支持，性能优异
- 自动 API 文档（Swagger）
- 类型提示，代码质量高
- Python 生态丰富（AI/ML 库）
- 易于团队学习

**替代方案**:
- Go：性能更优，但 AI 库支持较弱
- Django：功能完整，但同步框架

**风险评估**:
- 低：FastAPI 与 OpenAI 等 AI 库集成良好

---

### 3. 数据库：PostgreSQL

**问题**: 需要关系型数据库和全文搜索

**选择**: PostgreSQL

**理由**:
- 成熟稳定，ACID 完整
- 内置全文搜索（满足 MVP）
- JSON 支持（灵活扩展）
- 强大的查询能力

**替代方案**:
- MySQL：功能相近
- MongoDB：NoSQL，但关系查询弱

**风险评估**:
- 低：PostgreSQL 是标准选择

---

### 4. 缓存：Redis

**问题**: 需要高性能缓存和会话存储

**选择**: Redis

**理由**:
- 性能极高
- 丰富数据结构
- 持久化选项
- 限流计数器支持

**风险评估**:
- 低：Redis 是标准缓存方案

---

### 5. 向量数据库：Qdrant

**问题**: v2.0 需要向量搜索实现语义推荐

**选择**: Qdrant

**理由**:
- 开源免费
- 性能优异
- 易于部署
- Python SDK 完善

**替代方案**:
- Milvus：功能更多，但部署复杂
- Pinecone：托管服务，但成本高

**风险评估**:
- 中：v2.0 功能，MVP 阶段不依赖

---

### 6. LLM 服务：OpenAI API

**问题**: 需要 AI 摘要生成

**选择**: OpenAI API（GPT-4o-mini）

**理由**:
- 质量稳定
- API 简单
- 成本可控（mini 模型）
- 延迟可接受

**替代方案**:
- Claude API：质量相近，选择 OpenAI 因团队熟悉
- 自部署模型：成本高，维护复杂

**风险评估**:
- 中：API 依赖，需备选方案（摘要降级为无）

---

### 7. 任务队列：Celery / RQ

**问题**: 需要异步任务（RSS 抓取、摘要生成）

**选择**: RQ（Redis Queue）

**理由**:
- 简单轻量
- Redis 已部署
- 满足当前需求

**替代方案**:
- Celery：功能更强，但复杂

**风险评估**:
- 低：RQ 满足 MVP 需求

## 错误处理

### 错误分类和处理策略

| 错误类型 | 检测 | 恢复 | 用户信息 | HTTP 状态 |
|---------|------|------|----------|-----------|
| ValidationError | 输入验证 | 返回错误详情 | "邮箱格式无效" | 400 |
| UnauthorizedError | Token 验证 | 重定向登录 | "请先登录" | 401 |
| ForbiddenError | 权限检查 | 返回权限提示 | "无权限访问" | 403 |
| NotFoundError | 资源查找 | 返回 404 | "资源不存在" | 404 |
| ConflictError | 约束检查 | 返回冲突详情 | "邮箱已被使用" | 409 |
| RateLimitError | 限流检查 | 返回重试时间 | "请求过多，请稍后重试" | 429 |
| ExternalServiceError | API 调用 | 降级或重试 | "服务暂时不可用" | 502 |
| SystemError | try-catch | 记录并返回通用错误 | "系统错误，请稍后重试" | 500 |

### 统一错误响应格式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "邮箱格式无效",
    "details": {
      "field": "email",
      "issue": "格式不正确"
    },
    "requestId": "uuid"
  }
}
```

### 错误日志策略

- **所有 5xx 错误**：立即记录，发送告警
- **4xx 错误**：聚合统计，异常模式告警
- ** requestId**：关联所有日志，便于追踪

### 降级策略

| 服务 | 降级方案 |
|------|----------|
| OpenAI API | 摘要使用文章前 200 字 |
| 推荐服务 | 降级为按时间排序 |
| RSS 抓取 | 跳过失败的源，记录错误 |
| 搜索 | 降级为标题匹配 |

## 安全考虑

### 1. 认证和授权

**认证机制**：
- JWT Token（Access Token + Refresh Token）
- Access Token 有效期：30 天
- Refresh Token 支持，无感刷新

**授权模型**：
- 基于角色的访问控制（RBAC）
- 角色：user, premium, admin
- Premium 用户访问高级功能

**第三方登录**：
- OAuth 2.0 流程
- 支持微信、Apple ID
- 首次登录自动创建用户

### 2. 输入验证

**验证层级**：
1. **客户端验证**：即时反馈
2. **API 验证**：Pydantic 模型
3. **业务验证**：业务规则检查
4. **数据库验证**：约束保护

**验证规则**：
```python
class UserRegister(BaseModel):
    email: EmailStr  # 邮箱格式验证
    password: SecretStr = Field(min_length=8, max_length=64)
    name: str = Field(min_length=1, max_length=50)
```

**防注入**：
- SQLAlchemy ORM 自动防 SQL 注入
- 输入清理防 XSS
- 文件上传限制（类型、大小）

### 3. 敏感数据保护

**密码**：
- bcrypt 哈希，salt 自动处理
- 不记录明文密码

**Token**：
- JWT 使用环境变量密钥签名
- Refresh Token 存储 Redis，可撤销

**数据库**：
- 敏感字段加密（如需）
- 连接字符串环境变量

### 4. 限流策略

**令牌桶算法**：
- Redis 实现
- 窗口期 + 计数

**限流规则**：
```python
# 用户注册：每 IP 每小时 5 次
@rate_limit("register", max_requests=5, window=3600, key_func=get_client_ip)

# API 调用：每用户每分钟 100 次
@rate_limit("api", max_requests=100, window=60, key_func=get_user_id)

# 搜索请求：每用户每分钟 10 次
@rate_limit("search", max_requests=10, window=60, key_func=get_user_id)

# 文章分享：每用户每分钟 20 次
@rate_limit("share", max_requests=20, window=60, key_func=get_user_id)
```

### 5. HTTPS 和传输安全

- **全站 HTTPS**：TLS 1.3
- **HSTS**：强制 HTTPS
- **证书管理**：Let's Encrypt 自动续期

### 6. CORS 策略

```python
CORS_ALLOW_ORIGINS = [
    "https://newsapp.com",
    "capacitor://localhost"  # Flutter iOS
]

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE"]
CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
```

### 7. 内容安全

**内容审核**（v2.0）：
- 敏感词过滤
- 图片审核
- 用户举报机制

**数据合规**：
- GDPR 合规（用户数据导出/删除）
- 隐私政策明确

## 测试策略

### 测试层级

```
┌─────────────────────────────────────────────────────────┐
│                    E2E 测试 (10%)                        │
│  - 关键用户流程                                          │
│  - 跨服务验证                                            │
├─────────────────────────────────────────────────────────┤
│                   集成测试 (20%)                         │
│  - API 端点测试                                          │
│  - 数据库集成                                            │
│  - 外部服务 Mock                                         │
├─────────────────────────────────────────────────────────┤
│                  单元测试 (70%)                          │
│  - 业务逻辑                                              │
│  - 工具函数                                              │
│  - 数据验证                                              │
└─────────────────────────────────────────────────────────┘
```

### 单元测试（覆盖率 ≥ 80%）

**框架**：
- Python：pytest + pytest-cov
- Flutter：test + flutter test

**测试内容**：
- 业务逻辑函数
- 工具函数
- 数据模型验证
- 错误处理

```python
# 示例：推荐算法测试
def test_recommend_filter_exclude_read():
    user_id = "test-user"
    read_articles = ["article-1", "article-2"]
    
    result = recommend_service.get_recommendations(
        user_id, exclude=read_articles
    )
    
    assert all(a.id not in read_articles for a in result)
```

### 集成测试

**框架**：
- Python：pytest + httpx
- Flutter：integration_test

**测试内容**：
- API 端点
- 数据库操作
- Redis 缓存
- 外部服务 Mock

```python
# 示例：注册 API 测试
async def test_register_success(client):
    response = await client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "userId" in data
    assert "token" in data
    
    # 验证数据库
    user = db.query(User).filter_by(email="test@example.com").first()
    assert user is not None
```

### E2E 测试

**框架**：
- Flutter：flutter_driver / integration_test

**测试场景**：
1. 用户注册→登录→阅读文章→收藏
2. 用户搜索→筛选→阅读
3. 用户查看推荐→反馈

```dart
// 示例：阅读流程 E2E
testWidgets('complete reading flow', (tester) async {
  // 启动应用
  await app.main();
  await tester.pumpAndSettle();
  
  // 登录
  await tester.enterText(find.byKey('email'), 'test@example.com');
  await tester.enterText(find.byKey('password'), 'password123');
  await tester.tap(find.text('登录'));
  await tester.pumpAndSettle();
  
  // 进入文章
  await tester.tap(find.text('第一条新闻'));
  await tester.pumpAndSettle();
  
  // 验证标题显示
  expect(find.text('第一条新闻的详细内容'), findsOneWidget);
  
  // 收藏
  await tester.tap(find.byIcon(Icons.favorite_border));
  await tester.pumpAndSettle();
  
  // 验证收藏
  expect(find.byIcon(Icons.favorite), findsOneWidget);
});
```

### 性能测试

**工具**：
- Locust（API 压力测试）
- Flutter DevTools（移动端性能）

**测试目标**：
- 10,000 并发用户
- API 响应 P95 ≤ 300ms
- 首屏加载 ≤ 2s（4G）

```python
# 示例：Locust 测试
class NewsUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # 登录
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["token"]
    
    @task(3)
    def view_feed(self):
        self.client.get("/api/articles", headers={
            "Authorization": f"Bearer {self.token}"
        })
    
    @task(1)
    def search(self):
        self.client.get("/api/search?q=AI", headers={
            "Authorization": f"Bearer {self.token}"
        })
```

### 测试数据

**策略**：
- 单元测试：Fixture 数据
- 集成测试：测试数据库隔离
- E2E 测试：测试环境独立

## 部署考虑

### 环境配置

**开发环境**：
- Docker Compose 本地运行
- 热重载

**测试环境**：
- Kubernetes 集群
- 自动化测试

**生产环境**：
- 阿里云 Kubernetes
- 自动扩缩容

### Docker 配置

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/newsapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=newsapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 迁移策略

**数据库迁移**：
- Alembic 管理 schema 变更
- 每次部署前自动迁移

**数据迁移**：
- 渐进式迁移
- 双写验证

### 回滚计划

**回滚触发条件**：
- 错误率 > 5%
- P95 延迟 > 1s
- 关键功能不可用

**回滚步骤**：
1. 停止流量（灰度发布）
2. 切换到旧版本
3. 回滚数据库（如需）
4. 验证功能
5. 分析问题

## 开放问题

| # | 问题 | 影响 | 计划解决时间 |
|---|------|------|--------------|
| 1 | Elasticsearch 是否需要 v1.0 | 搜索性能 | MVP 后评估 |
| 2 | 图片存储方案（CDN） | 用户体验 | MVP 阶段使用外部链接 |
| 3 | 推送通知实现 | 用户留存 | v1.1 |
| 4 | 国际化支持 | 市场扩展 | v2.0 |
| 5 | Apple Watch 端 | 用户场景 | MVP 后评估 |

## 附录

### 参考资源

- [Flutter 官方文档](https://flutter.dev/docs)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)
- [Redis 文档](https://redis.io/docs/)
- [OpenAI API 文档](https://platform.openai.com/docs)

### 决策记录

- 技术栈选择：2024-01-15，记录于 spec.md
- 推荐算法 MVP 方案：2024-01-16
- 数据库 schema 最终确认：2024-01-17

## 成功标准

完成本设计后的可验证条件：

- [ ] 架构图清晰完整
- [ ] 所有模块职责明确
- [ ] 接口契约完整（输入、输出、错误）
- [ ] 数据模型规范且有索引
- [ ] 技术选型有理由和替代方案
- [ ] 错误处理全面考虑
- [ ] 安全威胁评估
- [ ] 测试策略可行
- [ ] 部署方案明确

## 下一步

设计完成后：
1. 调用 `hf-review(design)` 进行评审
2. 通过后进入 `hf-build` 实现

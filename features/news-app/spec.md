# 规格: 新闻 APP

## 背景

忙碌的专业人士需要高效获取高质量新闻信息。现有新闻 APP 存在信息过载、推荐不准、广告干扰等问题。我们构建一个以内容质量为核心、支持碎片化阅读的新闻 APP。

## 目标用户

**主要用户**：25-40 岁忙碌的专业人士

**用户画像**：
- 工作繁忙，只有碎片时间阅读
- 需要快速了解行业动态
- 注重内容质量和阅读效率
- 愿意为高质量内容付费

## 成功指标

- **日活跃用户**：≥ 10,000（上线 3 个月内）
- **次日留存率**：≥ 40%
- **人均日使用时长**：≥ 15 分钟
- **阅读完成率**：≥ 60%
- **用户满意度（NPS）**：≥ 40

## 技术栈

**移动端**：
- iOS: Swift + SwiftUI
- Android: Kotlin + Jetpack Compose
- 或跨平台：Flutter (Dart) / React Native (TypeScript)

**后端**：
- 语言：Python (FastAPI) 或 Go
- 数据库：PostgreSQL
- 缓存：Redis
- 消息队列：RabbitMQ / Kafka
- 搜索：Elasticsearch

**AI/ML**：
- LLM API: OpenAI GPT-4 / Claude / 自部署模型
- 推荐系统：协同过滤 + 内容过滤
- 向量数据库：Qdrant / Milvus

**基础设施**：
- 容器：Docker + Kubernetes
- CI/CD：GitHub Actions
- 监控：Prometheus + Grafana

## 命令

```bash
# 开发
npm run dev          # 启动开发服务器
npm run ios          # 启动 iOS 模拟器
npm run android      # 启动 Android 模拟器

# 测试
npm run test         # 单元测试
npm run test:e2e     # 端到端测试
npm run test:coverage # 测试覆盖率

# 构建
npm run build        # 生产构建
npm run build:ios    # iOS 构建
npm run build:android # Android 构建

# 代码检查
npm run lint         # ESLint / Pylint
npm run format       # Prettier / Black
npm run type-check   # TypeScript / mypy
```

## 项目结构

```
news-app/
├── apps/                    # 移动端应用
│   ├── ios/               # iOS 原生应用
│   └── android/           # Android 原生应用
├── shared/                 # 共享代码（如跨平台）
│   ├── components/        # 共享组件
│   ├── utils/            # 共享工具
│   └── types/            # 共享类型
├── backend/               # 后端服务
│   ├── api/              # REST API
│   ├── services/         # 业务逻辑
│   ├── models/           # 数据模型
│   ├── ml/               # 机器学习模型
│   └── tests/            # 后端测试
├── infrastructure/        # 基础设施代码
│   ├── docker/           # Docker 配置
│   ├── k8s/              # Kubernetes 配置
│   └── ci/               # CI/CD 配置
├── docs/                  # 项目文档
├── scripts/               # 工具脚本
└── tests/                 # 集成测试
```

## 代码风格

**TypeScript/Dart 示例**：
```typescript
// 接口定义清晰
interface Article {
  id: string;
  title: string;
  summary: string;
  content: string;
  source: string;
  publishedAt: Date;
  tags: string[];
  readTime: number; // 分钟
}

// async/await 优于 Promise chains
async function loadArticles(): Promise<Article[]> {
  try {
    const response = await fetch('/api/articles');
    const data = await response.json();
    return data.articles;
  } catch (error) {
    logger.error('Failed to load articles', error);
    throw new ArticleLoadError('Cannot load articles');
  }
}

// 使用可选链和空值合并
const summary = article?.summary ?? 'No summary available';
```

## 测试策略

**单元测试**（覆盖率 ≥ 80%）：
- 框架：Jest (TS)、pytest (Python)、JUnit (Kotlin)
- 位置：每个模块同级 `tests/` 目录
- 关注：业务逻辑、工具函数

**集成测试**：
- 框架：Supertest (API)、Espresso (Android)、XCTest (iOS)
- 位置：`tests/integration/`
- 关注：API 端点、数据流

**端到端测试**：
- 框架：Detox (React Native)、XCUITest (iOS)、UI Automator (Android)
- 位置：`tests/e2e/`
- 关注：核心用户流程

**测试层级分布**：
- 单元测试：70%
- 集成测试：20%
- 端到端测试：10%

## 边界

**始终做**：
- 提交前运行测试
- 遵循命名约定
- 验证所有用户输入
- API 响应包含错误信息
- 敏感操作记录日志

**先询问**：
- 数据库 schema 变更
- 添加新依赖（尤其是重量级的）
- 更改 CI/CD 配置
- 修改 API 契约
- 架构变更

**绝不**：
- 提交密钥或敏感信息
- 编辑 vendor 目录
- 删除失败测试而不修复
- 硬编码配置值
- 绕过代码审查

## 功能需求

### FR-001 用户注册和登录

**陈述**：系统应支持用户注册和登录，支持邮箱/手机号和第三方登录。

**验收标准**：
- Given 用户在登录页面
- When 用户输入有效邮箱和密码
- Then 系统创建账户并发送验证邮件
- And 用户可使用邮箱和密码登录
- And 用户可选择使用微信/Apple ID 第三方登录

**优先级**：Must

### FR-002 新闻源管理

**陈述**：系统应支持管理多个新闻源，包括系统预设和用户自定义。

**验收标准**：
- Given 用户已登录
- When 用户进入新闻源管理页面
- Then 显示系统预设新闻源列表（至少 20 个）
- And 用户可订阅/取消订阅新闻源
- And 用户可添加自定义 RSS 源
- And 系统验证 RSS 源有效性

**优先级**：Must

### FR-003 新闻内容展示

**陈述**：系统应以卡片形式展示新闻，支持摘要和全文两种模式。

**验收标准**：
- Given 用户在首页
- When 系统加载新闻列表
- Then 显示新闻卡片，包含标题、摘要、来源、发布时间
- And 卡片显示预计阅读时间
- And 用户点击卡片可进入全文阅读
- And 全文页面支持字体大小调节
- And 全文页面支持夜间模式

**优先级**：Must

### FR-004 智能推荐

**陈述**：系统应根据用户兴趣和行为推荐新闻内容。

**验收标准**：
- Given 用户有阅读历史
- When 系统生成推荐列表
- Then 推荐内容基于用户兴趣标签
- And 推荐内容排除已读文章
- And 推荐列表每日更新至少 2 次
- And 用户可对推荐内容反馈（不感兴趣/相关）

**优先级**：Must

### FR-005 内容搜索

**陈述**：系统应支持全文搜索和标签搜索。

**验收标准**：
- Given 用户在搜索页面
- When 用户输入搜索关键词
- Then 显示匹配的新闻列表（标题+摘要）
- And 搜索结果高亮关键词
- And 用户可按标签筛选搜索结果
- And 搜索支持历史记录

**优先级**：Should

### FR-006 收藏和分享

**陈述**：系统应支持收藏文章和分享到社交平台。

**验收标准**：
- Given 用户在阅读文章
- When 用户点击收藏按钮
- Then 文章添加到收藏列表
- And 收藏列表同步到云端
- When 用户点击分享按钮
- Then 显示分享选项（微信、朋友圈、微博等）
- And 分享内容包含标题、摘要和链接

**优先级**：Must

### FR-007 离线阅读

**陈述**：系统应支持离线下载和阅读已收藏的文章。

**验收标准**：
- Given 用户收藏了文章
- When 用户在离线状态
- Then 用户可阅读已下载的收藏文章
- And 系统显示文章离线状态

**优先级**：Should

### FR-008 内容质量评分

**陈述**：系统应对新闻内容进行质量评分（1-5 分），并显示给用户。

**验收标准**：
- Given 新闻文章被系统抓取
- When 系统分析文章内容
- Then 系统计算质量分数（1-5 分）
- And 质量分数基于以下维度（权重相等）：
  - 原创性：是否为原创内容（vs 转载/洗稿）
  - 信息量：信息密度和深度
  - 准确性：事实准确度（基于信源声誉）
  - 可读性：文章结构和语言质量
- And MVP 阶段使用规则算法：
  - 信源声誉分（40%）：权威媒体 > 一般媒体 > 自媒体
  - 内容长度分（20%）：适中长度（800-2000字）最优
  - 标题质量分（20%）：非标题党，描述准确
  - 完整度分（20%）：包含 5W1H
- And v2.0 引入 ML 模型，基于人工标注数据训练
- And 新闻卡片显示质量评分（星级图标）

**优先级**：Should

**技术说明**：
- MVP 阶段：规则算法，计算快速可解释
- 数据收集：同时收集用户反馈（点赞/踩）作为训练数据
- v2.0 目标：使用收集的数据训练 ML 模型

### FR-009 AI 摘要生成

**陈述**：系统应使用 LLM 自动生成长文章的智能摘要。

**验收标准**：
- Given 文章长度超过 500 字
- When 系统处理文章
- Then 生成 100-200 字的智能摘要
- And 摘要包含文章核心观点
- And 摘要显示在卡片和全文页面

**优先级**：Should

### FR-010 阅读历史和统计

**陈述**：系统应记录用户阅读历史并提供阅读统计。

**验收标准**：
- Given 用户使用 APP 30 天
- When 用户查看阅读统计
- Then 显示总阅读文章数、总阅读时长、偏好标签
- And 显示每日阅读趋势图
- And 显示最常阅读的源和话题

**优先级**：Could

### FR-011 个性化设置

**陈述**：系统应支持用户个性化偏好设置。

**验收标准**：
- Given 用户在设置页面
- When 用户修改偏好设置
- Then 用户可设置：字体大小、主题（亮/暗）、推送通知频率
- And 用户可管理兴趣标签
- And 用户可设置每日阅读目标

**优先级**：Should

### FR-012 付费会员功能

**陈述**：系统应支持付费会员，提供高级功能。

**验收标准**：
- Given 用户是付费会员（¥10/月或 ¥100/年）
- When 用户使用 APP
- Then 会员享有：无广告、无限收藏、深度内容访问、独家新闻
- And 系统支持微信/Apple Pay 支付
- And 会员状态同步到云端

**优先级**：Could

## 非功能需求

### 性能

- **首页加载时间**：4G ≤ 2s、5G ≤ 1s、WiFi ≤ 1s（首屏）
- **文章加载时间**：4G ≤ 1s、5G ≤ 0.5s、WiFi ≤ 0.5s（全文）
- **搜索响应时间**：≤ 500ms（P95）
- **推荐更新频率**：每 12 小时至少更新一次
- **API 响应时间**：P95 ≤ 300ms
- **图片加载**：懒加载，缩略图 ≤ 50KB

### 可用性

- **系统可用性**：≥ 99.5%
- **并发支持**：支持 10,000 并发用户
- **数据备份**：每日备份，保留 30 天

### 安全性

- **数据传输**：全站 HTTPS（TLS 1.3）
- **用户数据**：加密存储（AES-256），符合 GDPR
- **认证**：JWT Token，过期时间 30 天，支持刷新
- **API 安全**：限流、签名验证、CORS 策略
- **限流策略**：
  - 用户注册：每 IP 每小时 5 次
  - API 调用：每用户每分钟 100 次
  - 搜索请求：每用户每分钟 10 次
  - 文章分享：每用户每分钟 20 次

### 可维护性

- **代码覆盖率**：≥ 80%
- **文档完整**：API 文档、架构文档、部署文档
- **日志规范**：结构化日志，包含 trace ID

## 约束

**技术约束**：
- iOS 最低版本：iOS 15.0
- Android 最低版本：Android 10 (API 29)
- 后端响应必须兼容 JSON 格式

**业务约束**：
- 内容必须符合法律法规
- 必须提供内容举报机制
- 用户数据不得用于未经用户同意的目的

**时间约束**：
- MVP 版本：3 个月
- 完整版本：6 个月

## 范围外

**明确不做**（MVP 阶段）：
- ~~用户生成内容（UGC）~~：初期只聚合专业新闻源
- ~~评论系统~~：增加内容审核复杂度
- ~~视频内容~~：技术复杂度高，聚焦文字内容
- ~~社交功能~~：关注、粉丝等社交互动
- ~~直播功能~~：不在新闻核心场景

**原因**：这些功能增加复杂度和开发时间，MVP 应聚焦核心阅读体验。

## 开放问题

### 已决策（基于 MVP 原则）

1. **技术选型**：✅ 使用 Flutter（跨平台，降低开发成本）
2. **LLM 选择**：✅ 使用 OpenAI API（MVP 阶段，稳定可靠）
3. **推荐算法**：✅ MVP 使用规则推荐（兴趣标签 + 时效性 + 质量分），v2.0 引入协同过滤
4. **内容来源**：✅ 初期使用公开 RSS 源，无需授权（聚合性质）
5. **服务器部署**：✅ 使用阿里云（国内访问优化）

### 待确认

1. **国际化**：是否支持多语言？（MVP 仅中文）
2. **Apple Watch 支持**：是否需要手表端？（MVP 不支持）
3. **Web 端**：是否需要网页版？（MVP 仅移动端）

## 成功标准

完成本规格后的可验证条件：

- [ ] 所有功能需求有唯一 ID（FR-001 ~ FR-012）
- [ ] 每条需求有明确验收标准（Given-When-Then）
- [ ] 优先级已标记（Must/Should/Could）
- [ ] 技术栈已明确
- [ ] 非功能需求可量化
- [ ] 边界条件已定义
- [ ] 范围外已明确

## 下一步

规格完成后，进入 **hf-design** 进行技术设计。

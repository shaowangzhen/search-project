# 官方网站搜索引擎技术设计文档

## 1. 系统架构设计

### 1.1 整体架构

```
用户请求 → Nginx → PHP-FPM → FastAPI → Elasticsearch
                ↓
            Vue.js前端 ← Redis缓存 ← MySQL数据库
```

### 1.2 核心组件

#### 前端层 (LNMP Stack)
- **Nginx**: 反向代理、负载均衡、静态文件服务
- **PHP-FPM**: 处理PHP请求，与后端API通信
- **Vue.js**: 前端交互界面
- **MySQL**: 用户数据、配置信息存储

#### 后端层 (Python Microservices)
- **FastAPI**: RESTful API服务
- **Scrapy**: 网页爬虫框架
- **Celery**: 异步任务队列
- **Elasticsearch**: 全文搜索引擎

#### 数据层
- **MySQL**: 关系型数据存储
- **Elasticsearch**: 文档索引和搜索
- **Redis**: 缓存和会话存储

## 2. 核心算法设计

### 2.1 官方网站识别算法

#### 2.1.1 多维度评分体系

```python
def calculate_official_score(url, content, links):
    score = 0
    
    # 域名权威性 (40%)
    domain_score = check_domain_authority(url)
    score += domain_score * 0.4
    
    # 内容质量 (30%)
    content_score = analyze_content_quality(content)
    score += content_score * 0.3
    
    # 链接关系 (20%)
    link_score = analyze_link_relationships(links)
    score += link_score * 0.2
    
    # 技术指标 (10%)
    tech_score = check_technical_indicators(url)
    score += tech_score * 0.1
    
    return min(score, 1.0)
```

#### 2.1.2 域名权威性检测

```python
def check_domain_authority(url):
    domain = extract_domain(url)
    
    # 检查域名类型
    if domain.endswith('.gov.cn'):
        return 1.0  # 政府网站
    elif domain.endswith('.edu.cn'):
        return 0.9  # 教育网站
    elif domain.endswith('.org.cn'):
        return 0.8  # 组织网站
    elif domain.endswith('.com.cn'):
        return 0.7  # 商业网站
    
    # 检查域名年龄和注册信息
    domain_age = get_domain_age(domain)
    if domain_age > 5:  # 5年以上
        return 0.6
    
    return 0.3
```

### 2.2 内容质量分析

#### 2.2.1 文本质量评估

```python
def analyze_content_quality(content):
    score = 0
    
    # 文本长度检查
    if len(content) > 500:
        score += 0.2
    
    # 关键词密度
    keyword_density = calculate_keyword_density(content)
    if 0.02 <= keyword_density <= 0.05:
        score += 0.2
    
    # 结构化内容
    structured_score = check_structured_content(content)
    score += structured_score * 0.3
    
    # 语言质量
    language_score = check_language_quality(content)
    score += language_score * 0.3
    
    return min(score, 1.0)
```

### 2.3 搜索排序算法

#### 2.3.1 综合评分算法

```python
def calculate_search_score(query, document, official_score):
    # 文本相关性 (50%)
    text_relevance = calculate_text_relevance(query, document)
    
    # 权威性评分 (30%)
    authority_score = official_score
    
    # 新鲜度评分 (10%)
    freshness_score = calculate_freshness(document['timestamp'])
    
    # 用户行为评分 (10%)
    behavior_score = get_user_behavior_score(document['url'])
    
    # 综合评分
    final_score = (
        text_relevance * 0.5 +
        authority_score * 0.3 +
        freshness_score * 0.1 +
        behavior_score * 0.1
    )
    
    return final_score
```

## 3. 数据库设计

### 3.1 MySQL表结构

#### 3.1.1 网站表 (websites)

```sql
CREATE TABLE websites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    domain VARCHAR(255) NOT NULL UNIQUE,
    official_score DECIMAL(3,2) DEFAULT 0.00,
    last_crawled TIMESTAMP NULL,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_domain (domain),
    INDEX idx_official_score (official_score),
    INDEX idx_status (status)
);
```

#### 3.1.2 页面表 (pages)

```sql
CREATE TABLE pages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    website_id INT NOT NULL,
    url VARCHAR(1000) NOT NULL,
    title VARCHAR(500),
    content LONGTEXT,
    meta_description TEXT,
    last_updated TIMESTAMP NULL,
    page_rank DECIMAL(3,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(id),
    INDEX idx_website_id (website_id),
    INDEX idx_url (url(255)),
    INDEX idx_page_rank (page_rank)
);
```

### 3.2 Elasticsearch索引设计

#### 3.2.1 页面索引映射

```json
{
  "mappings": {
    "properties": {
      "id": {"type": "integer"},
      "url": {"type": "keyword"},
      "title": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "content": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "domain": {"type": "keyword"},
      "official_score": {"type": "float"},
      "page_rank": {"type": "float"},
      "last_updated": {"type": "date"},
      "tags": {"type": "keyword"},
      "category": {"type": "keyword"}
    }
  }
}
```

## 4. API设计

### 4.1 搜索API

#### 4.1.1 搜索接口

```http
GET /api/v1/search?q={query}&page={page}&size={size}&category={category}
```

**请求参数:**
- `q`: 搜索关键词 (必需)
- `page`: 页码 (默认: 1)
- `size`: 每页大小 (默认: 10, 最大: 50)
- `category`: 分类筛选 (可选)

**响应格式:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 1000,
    "page": 1,
    "size": 10,
    "results": [
      {
        "id": 123,
        "title": "页面标题",
        "url": "https://example.com/page",
        "snippet": "页面摘要...",
        "domain": "example.com",
        "official_score": 0.85,
        "last_updated": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

### 4.2 管理API

#### 4.2.1 网站管理

```http
POST /api/v1/admin/websites
PUT /api/v1/admin/websites/{id}
DELETE /api/v1/admin/websites/{id}
GET /api/v1/admin/websites
```

## 5. 部署架构

### 5.1 Docker Compose配置

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - php-fpm

  php-fpm:
    build: ./frontend
    volumes:
      - ./frontend:/var/www/html
    depends_on:
      - mysql
      - redis

  fastapi:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - redis
      - elasticsearch

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: search_engine
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  elasticsearch:
    image: elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

volumes:
  mysql_data:
  es_data:
```

## 6. 性能优化策略

### 6.1 缓存策略

- **Redis缓存**: 热门搜索结果、用户会话
- **CDN加速**: 静态资源分发
- **数据库缓存**: 查询结果缓存

### 6.2 搜索优化

- **索引优化**: 合理的ES索引分片和副本
- **查询优化**: 使用过滤器减少计算量
- **结果缓存**: 热门查询结果缓存

### 6.3 爬虫优化

- **分布式爬取**: 多进程/多机器并行爬取
- **智能限速**: 根据网站响应调整爬取频率
- **增量更新**: 只更新变化的内容

## 7. 监控和日志

### 7.1 监控指标

- **系统指标**: CPU、内存、磁盘、网络
- **应用指标**: 响应时间、错误率、吞吐量
- **业务指标**: 搜索量、点击率、用户活跃度

### 7.2 日志管理

- **结构化日志**: JSON格式日志
- **日志聚合**: ELK Stack (Elasticsearch + Logstash + Kibana)
- **告警机制**: 基于阈值的自动告警

## 8. 安全考虑

### 8.1 数据安全

- **数据加密**: 敏感数据加密存储
- **访问控制**: 基于角色的权限管理
- **数据备份**: 定期数据备份和恢复测试

### 8.2 系统安全

- **HTTPS**: 全站HTTPS加密
- **防火墙**: 网络访问控制
- **漏洞扫描**: 定期安全漏洞扫描

## 9. 扩展性设计

### 9.1 水平扩展

- **负载均衡**: Nginx负载均衡
- **数据库分片**: MySQL读写分离
- **缓存集群**: Redis集群部署

### 9.2 功能扩展

- **插件系统**: 支持第三方插件
- **API版本管理**: 向后兼容的API设计
- **多语言支持**: 国际化支持


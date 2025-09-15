# 开发分支说明

## 分支管理策略

### 分支结构
- `master`: 主分支，用于生产环境部署
- `dev`: 开发分支，用于日常开发工作

### 开发流程

1. **日常开发**
   ```bash
   # 切换到开发分支
   git checkout dev
   
   # 拉取最新代码
   git pull origin dev
   
   # 创建功能分支
   git checkout -b feature/功能名称
   
   # 开发完成后提交
   git add .
   git commit -m "feat: 添加新功能"
   
   # 推送到远程
   git push origin feature/功能名称
   ```

2. **合并到开发分支**
   ```bash
   # 切换回dev分支
   git checkout dev
   
   # 合并功能分支
   git merge feature/功能名称
   
   # 推送到远程dev分支
   git push origin dev
   ```

3. **发布到生产环境**
   ```bash
   # 切换到master分支
   git checkout master
   
   # 合并dev分支
   git merge dev
   
   # 推送到远程master分支
   git push origin master
   ```

## 提交规范

### 提交信息格式
```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```bash
git commit -m "feat(api): 添加搜索建议接口"
git commit -m "fix(crawler): 修复反爬虫检测问题"
git commit -m "docs(readme): 更新安装说明"
```

## 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/shaowangzhen/search-project.git
cd search-project
```

### 2. 切换到开发分支
```bash
git checkout dev
```

### 3. 设置开发环境
```bash
# 运行设置脚本
./scripts/setup_dev.sh
```

### 4. 启动服务
```bash
# 启动Redis
redis-server

# 启动Elasticsearch
elasticsearch

# 启动Python后端
cd backend
source venv/bin/activate
python -m uvicorn api.main:app --reload

# 启动PHP前端
cd frontend
php -S localhost:8080 -t public
```

## 代码规范

### Python代码规范
- 使用Black进行代码格式化
- 使用flake8进行代码检查
- 遵循PEP 8规范

### PHP代码规范
- 使用PSR-12编码规范
- 使用PHP_CodeSniffer进行检查

### 前端代码规范
- 使用Prettier进行代码格式化
- 使用ESLint进行代码检查

## 测试

### 运行测试
```bash
# Python测试
cd backend
python -m pytest

# PHP测试
cd frontend
composer test
```

## 部署

### 开发环境
- 使用本地开发服务器
- 数据库使用本地MySQL
- 缓存使用本地Redis

### 生产环境
- 使用Nginx + PHP-FPM
- 数据库使用MySQL主从复制
- 缓存使用Redis集群
- 搜索引擎使用Elasticsearch集群

## 注意事项

1. 开发前请先拉取最新代码
2. 提交前请运行测试确保代码质量
3. 提交信息要清晰明确
4. 定期合并到master分支
5. 遇到问题及时沟通

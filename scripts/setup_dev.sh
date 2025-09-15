#!/bin/bash
# 本地开发环境设置脚本

echo "🚀 设置官方网站搜索引擎开发环境..."

# 检查必要的工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安装，请先安装 $1"
        exit 1
    else
        echo "✅ $1 已安装"
    fi
}

echo "📋 检查必要工具..."
check_command "python3"
check_command "php"
check_command "mysql"
check_command "redis-server"

# 创建Python虚拟环境
echo "🐍 设置Python环境..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Python虚拟环境已创建"
fi

source venv/bin/activate
pip install -r requirements.txt
echo "✅ Python依赖已安装"

# 设置PHP环境
echo "�� 设置PHP环境..."
cd ../frontend
if [ ! -d "vendor" ]; then
    composer install
    echo "✅ PHP依赖已安装"
fi

# 创建配置文件
echo "⚙️ 创建配置文件..."
if [ ! -f "config/local.php" ]; then
    cp config/config.php config/local.php
    echo "✅ 本地配置文件已创建"
fi

# 设置数据库
echo "🗄️ 设置数据库..."
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS search_engine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p search_engine < ../database/init.sql
echo "✅ 数据库已初始化"

# 创建日志目录
echo "📝 创建日志目录..."
mkdir -p logs
mkdir -p ../backend/logs

# 设置权限
echo "🔐 设置文件权限..."
chmod -R 755 ../frontend/public
chmod -R 755 ../backend

echo "🎉 开发环境设置完成！"
echo ""
echo "📖 启动说明："
echo "1. 启动Redis: redis-server"
echo "2. 启动Elasticsearch: elasticsearch"
echo "3. 启动Python后端: cd backend && source venv/bin/activate && python -m uvicorn api.main:app --reload"
echo "4. 启动PHP前端: cd frontend && php -S localhost:8080 -t public"
echo ""
echo "🌐 访问地址："
echo "- 前端: http://localhost:8080"
echo "- 后端API: http://localhost:8000"
echo "- API文档: http://localhost:8000/docs"

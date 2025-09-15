#!/bin/bash
# 启动实时搜索版本 - Python 3.7兼容版

echo "🚀 启动官方网站搜索引擎 - 实时搜索版 (Python 3.7兼容)"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 检测到Python版本: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" < "3.7" ]]; then
    echo "❌ 需要Python 3.7或更高版本，当前版本: $PYTHON_VERSION"
    exit 1
fi

# 检查PHP环境
if ! command -v php &> /dev/null; then
    echo "❌ PHP 未安装，请先安装 PHP"
    exit 1
fi

# 进入后端目录
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活Python虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装Python依赖 (Python 3.7兼容版本)..."
pip install -r requirements_python37.txt

# 启动后端服务
echo "🐍 启动Python后端服务..."
python -m uvicorn api.main_realtime:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 进入前端目录
cd ../frontend

# 启动前端服务
echo "🐘 启动PHP前端服务..."
php -S localhost:8080 -t public &
FRONTEND_PID=$!

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "🌐 访问地址："
echo "   前端: http://localhost:8080"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "🔍 实时搜索特性："
echo "   - 多搜索引擎聚合 (Google, Bing, DuckDuckGo)"
echo "   - 实时官方网站识别"
echo "   - 权威性评分排序"
echo "   - 无数据存储依赖"
echo "   - Python 3.7兼容"
echo ""
echo "⏹️  停止服务: Ctrl+C"

# 等待用户中断
trap "echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

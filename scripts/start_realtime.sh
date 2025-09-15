#!/bin/bash
# 启动实时搜索版本

echo "🚀 启动官方网站搜索引擎 - 实时搜索版"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
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
echo "📥 安装Python依赖..."
pip install -r requirements_realtime.txt

# 启动后端服务
echo "🐍 启动Python后端服务..."
python -m uvicorn api.main_realtime:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端服务
#echo "🐘 启动PHP前端服务..."
#php -S localhost:8080 -t public &
#FRONTEND_PID=$!


echo "⏹️  停止服务: Ctrl+C"

# 等待用户中断
trap "echo '🛑 停止服务...'; kill $BACKEND_PID ; exit" INT
wait

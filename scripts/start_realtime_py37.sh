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

echo "⏹️  停止服务: Ctrl+C"

# 等待用户中断
trap "echo '🛑 停止服务...'; kill $BACKEND_PID; exit" INT
wait

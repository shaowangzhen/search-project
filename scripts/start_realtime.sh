#!/bin/bash
# 启动官方网站搜索引擎 - 实时搜索版

echo "🚀 启动官方网站搜索引擎 - 实时搜索版"

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
    echo "⚠️ PHP 未安装，前端服务将无法启动。但后端服务仍可运行。"
    # exit 1 # 不再强制退出，允许只启动后端
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

# 升级pip
echo "📦 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📥 安装Python依赖 (实时搜索版)..."
pip install -r requirements_realtime.txt

# 启动后端服务
echo "🐍 启动Python后端服务..."
python -m uvicorn api.main_realtime:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 等待后端启动
echo "⏳ 等待后端服务启动..."

# 循环检查端口状态，最多等待30秒 (15次 * 2秒)
for i in {1..15}; do
    sleep 2
    if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
        echo "✅ 后端服务启动成功 (PID: $BACKEND_PID)"
        break
    fi
    if [ $i -eq 15 ]; then
        echo "❌ 后端服务启动失败，端口8000未监听"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    echo "   等待中... ($i/15)"
done

echo ""
echo "🌐 后端API服务已在 http://localhost:8000 运行"
echo "📚 API文档可在 http://localhost:8000/docs 查看"
echo "💡 按 Ctrl+C 停止所有服务"

# 保持脚本运行，直到接收到中断信号
wait $BACKEND_PID

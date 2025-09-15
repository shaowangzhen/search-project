#!/bin/bash
# 启动实时搜索版本 - hao123风格首页

echo "🚀 启动官方网站搜索引擎 - hao123风格首页"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 检测到Python版本: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" < "3.8" ]]; then
    echo "❌ 需要Python 3.8或更高版本，当前版本: $PYTHON_VERSION"
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
echo "📥 安装Python依赖..."
pip install -r requirements_realtime.txt

# 启动后端服务
echo "🐍 启动Python后端服务..."
python -m uvicorn api.main_realtime:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 等待后端启动 - 增加等待时间并循环检查
echo "⏳ 等待后端服务启动..."
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

# 启动前端服务
echo "🌐 启动PHP前端服务 (hao123风格)..."
cd ../frontend/public
php -S localhost:8080 -t . index_hao123.php &
FRONTEND_PID=$!

# 等待前端启动
sleep 2

echo ""
echo "🎉 官方网站搜索引擎启动完成！"
echo ""
echo "📱 访问地址:"
echo "   前端 (hao123风格): http://localhost:8080"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "🔧 管理命令:"
echo "   停止服务: kill $BACKEND_PID $FRONTEND_PID"
echo "   查看日志: 查看终端输出"
echo ""
echo "💡 提示: 按 Ctrl+C 停止服务"

# 等待用户中断
wait

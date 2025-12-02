#!/bin/bash

# 投资组合分析工具启动脚本

echo "🚀 启动投资组合分析工具..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.7+"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  依赖未安装，正在安装..."
    pip3 install -r requirements.txt
fi

# 启动服务
echo "🌐 启动服务..."
echo "访问 http://localhost:8001 使用 Web 界面"
echo "访问 http://localhost:8001/docs 查看 API 文档"
echo ""
python3 main.py

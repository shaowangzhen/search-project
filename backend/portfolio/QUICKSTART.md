# 快速开始

## 1. 安装依赖

```bash
cd backend/portfolio
pip3 install -r requirements.txt
```

## 2. 启动服务

### 方法1: 使用启动脚本（推荐）

```bash
./start.sh
```

### 方法2: 直接启动

```bash
python3 main.py
```

## 3. 访问应用

启动后，打开浏览器访问：

- **Web界面**: http://localhost:8001
- **API文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health

## 4. 使用示例

### Web界面使用

1. 打开 http://localhost:8001
2. 在"添加资产"区域输入股票信息：
   - 股票代码：600000.SH
   - 股票名称：浦发银行
   - 持有数量：1000
   - 平均成本：10.5
3. 点击"添加资产"
4. 设置现金余额（可选）
5. 点击"开始分析"
6. 查看分析结果

### Python代码示例

```bash
python3 example.py
```

查看详细的使用示例。

### API调用示例

#### 获取股票价格

```bash
curl http://localhost:8001/market/price/600000.SH
```

#### 分析投资组合

```bash
curl -X POST http://localhost:8001/portfolio/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio": {
      "name": "我的组合",
      "assets": [{
        "symbol": "600000.SH",
        "name": "浦发银行",
        "asset_type": "stock",
        "quantity": 1000,
        "avg_cost": 10.5
      }],
      "cash": 50000
    },
    "risk_free_rate": 0.03
  }'
```

## 5. 常见问题

### Q: 依赖安装失败？

A: 尝试使用国内镜像：

```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 端口8001被占用？

A: 修改 main.py 最后一行的端口号：

```python
uvicorn.run(app, host="0.0.0.0", port=8002)  # 改为8002或其他端口
```

### Q: 获取不到股票数据？

A: 确认：
1. 股票代码格式正确（如 600000.SH, 000001.SZ）
2. 网络连接正常
3. 市场数据API可访问

### Q: 前端页面打不开？

A: 确认：
1. static/index.html 文件存在
2. 服务已正常启动
3. 访问 http://localhost:8001/api 查看API是否正常

## 6. 支持的股票代码格式

- 上海A股：600000.SH
- 深圳A股：000001.SZ
- 创业板：300001.SZ
- 科创板：688001.SH

## 7. 下一步

- 查看 [README.md](README.md) 了解详细功能
- 访问 http://localhost:8001/docs 查看完整API文档
- 运行 `python3 example.py` 查看更多示例

## 8. 停止服务

按 `Ctrl + C` 停止服务

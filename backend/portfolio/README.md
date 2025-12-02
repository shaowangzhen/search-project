# 投资组合分析工具

一个功能完整的投资组合分析工具，提供资产配置分析、收益率计算、风险评估和实时市场数据获取功能。

## 核心功能

- **资产管理**: 支持股票、债券、基金、ETF等多种资产类型
- **实时数据**: 获取A股市场实时价格数据
- **收益分析**: 计算总收益、收益率、年化收益率
- **风险评估**:
  - 波动率（标准差）
  - 最大回撤
  - VaR（风险价值）
  - CVaR（条件风险价值）
  - 夏普比率
- **资产配置**: 分析不同资产类型的配置比例
- **组合比较**: 对比多个投资组合的表现

## 技术架构

```
portfolio/
├── models/                     # 数据模型
│   ├── portfolio_models.py    # 投资组合相关模型
│   └── __init__.py
├── services/                   # 业务服务
│   ├── market_data_service.py # 市场数据服务
│   ├── portfolio_analysis_service.py  # 分析服务
│   └── __init__.py
├── utils/                      # 工具函数
│   └── __init__.py
├── main.py                     # FastAPI应用入口
├── example.py                  # 使用示例
├── requirements.txt            # 依赖包
└── README.md                   # 文档
```

## 快速开始

### 1. 安装依赖

```bash
cd backend/portfolio
pip install -r requirements.txt
```

### 2. 启动API服务

```bash
python main.py
```

服务将在 http://localhost:8001 启动

访问 http://localhost:8001/docs 查看API文档

### 3. 运行示例

```bash
python example.py
```

## API接口

### 市场数据接口

#### 获取实时价格

```bash
# 获取单个股票
GET /market/price/600000.SH

# 批量获取
POST /market/price
{
  "symbols": ["600000.SH", "000001.SZ"]
}
```

#### 搜索股票

```bash
GET /market/search/银行
```

### 投资组合分析接口

#### 分析投资组合

```bash
POST /portfolio/analyze
{
  "portfolio": {
    "name": "我的投资组合",
    "assets": [
      {
        "symbol": "600000.SH",
        "name": "浦发银行",
        "asset_type": "stock",
        "quantity": 1000,
        "avg_cost": 10.5
      }
    ],
    "cash": 50000
  },
  "risk_free_rate": 0.03
}
```

响应示例：

```json
{
  "portfolio": {...},
  "metrics": {
    "total_value": 150000.0,
    "total_cost": 100000.0,
    "total_return": 50000.0,
    "total_return_rate": 0.5,
    "annualized_return": 0.25,
    "volatility": 0.15,
    "sharpe_ratio": 1.47,
    "max_drawdown": -0.10,
    "var_95": -2500.0,
    "asset_allocation": {
      "stock": 0.7,
      "cash": 0.3
    }
  }
}
```

#### 获取资产配置

```bash
POST /portfolio/allocation
{
  "name": "我的投资组合",
  "assets": [...]
}
```

#### 比较投资组合

```bash
POST /portfolio/compare
[
  {
    "name": "组合A",
    "assets": [...]
  },
  {
    "name": "组合B",
    "assets": [...]
  }
]
```

## 使用示例

### Python代码示例

```python
import asyncio
from models.portfolio_models import Portfolio, Asset, AssetType
from services.portfolio_analysis_service import PortfolioAnalysisService

async def analyze_my_portfolio():
    # 创建投资组合
    portfolio = Portfolio(
        name="我的投资组合",
        assets=[
            Asset(
                symbol="600000.SH",
                name="浦发银行",
                asset_type=AssetType.STOCK,
                quantity=1000,
                avg_cost=10.5
            ),
        ],
        cash=50000.0
    )

    # 分析
    service = PortfolioAnalysisService()
    metrics = await service.analyze_portfolio(portfolio)

    # 打印结果
    print(f"总市值: ¥{metrics.total_value:,.2f}")
    print(f"总收益率: {metrics.total_return_rate * 100:.2f}%")
    print(f"夏普比率: {metrics.sharpe_ratio:.2f}")

    await service.market_data_service.close()

# 运行
asyncio.run(analyze_my_portfolio())
```

### cURL示例

```bash
# 获取股票价格
curl http://localhost:8001/market/price/600000.SH

# 分析投资组合
curl -X POST http://localhost:8001/portfolio/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio": {
      "name": "测试组合",
      "assets": [{
        "symbol": "600000.SH",
        "name": "浦发银行",
        "asset_type": "stock",
        "quantity": 1000,
        "avg_cost": 10.5
      }],
      "cash": 50000
    }
  }'
```

## 数据模型

### Asset（资产）

```python
{
  "symbol": str,          # 资产代码，如 "600000.SH"
  "name": str,            # 资产名称
  "asset_type": str,      # 资产类型: stock/bond/fund/etf/cash
  "quantity": float,      # 持有数量
  "avg_cost": float,      # 平均成本
  "current_price": float  # 当前价格（可选）
}
```

### Portfolio（投资组合）

```python
{
  "name": str,                # 组合名称
  "description": str,         # 组合描述（可选）
  "assets": List[Asset],      # 资产列表
  "cash": float,              # 现金余额
  "created_at": datetime,     # 创建时间
  "updated_at": datetime      # 更新时间
}
```

### PortfolioMetrics（组合指标）

```python
{
  "total_value": float,           # 总市值
  "total_cost": float,            # 总成本
  "total_return": float,          # 总收益
  "total_return_rate": float,     # 总收益率
  "annualized_return": float,     # 年化收益率
  "volatility": float,            # 波动率
  "sharpe_ratio": float,          # 夏普比率
  "max_drawdown": float,          # 最大回撤
  "var_95": float,                # 95% VaR
  "asset_allocation": Dict        # 资产配置
}
```

## 支持的资产类型

- `stock`: 股票
- `bond`: 债券
- `fund`: 基金
- `etf`: ETF
- `cash`: 现金
- `crypto`: 加密货币
- `commodity`: 商品
- `other`: 其他

## 指标说明

### 收益率指标

- **总收益率**: (当前市值 - 成本) / 成本
- **年化收益率**: 根据持有期限年化的收益率

### 风险指标

- **波动率**: 收益率的标准差，衡量投资的不确定性
- **夏普比率**: (年化收益率 - 无风险利率) / 波动率，衡量风险调整后的收益
- **最大回撤**: 从历史最高点到最低点的最大跌幅
- **VaR（风险价值）**: 在给定置信水平下的最大可能损失
- **CVaR（条件风险价值）**: 超过VaR的平均损失

## 数据源

- 实时行情: 新浪财经API
- 股票搜索: 腾讯财经API

## 注意事项

1. 本工具仅供学习和参考，不构成投资建议
2. 市场数据有延迟，请勿用于实盘交易决策
3. 风险指标计算基于历史数据和假设，实际风险可能不同
4. 请根据自己的风险承受能力做出投资决策

## 扩展功能

可以进一步扩展的功能：

- [ ] 接入更多数据源（如tushare、东方财富）
- [ ] 添加历史净值曲线
- [ ] 实现投资组合优化（马科维茨理论）
- [ ] 添加因子分析
- [ ] 支持期货、期权等衍生品
- [ ] 添加回测功能
- [ ] 导入/导出投资组合
- [ ] 数据库持久化

## License

MIT

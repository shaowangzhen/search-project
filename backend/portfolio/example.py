"""
投资组合分析工具使用示例
"""
import asyncio
from datetime import datetime
from models.portfolio_models import Portfolio, Asset, AssetType
from services.portfolio_analysis_service import PortfolioAnalysisService
from services.market_data_service import MarketDataService


async def example_basic_analysis():
    """基础分析示例"""
    print("=" * 60)
    print("示例1: 基础投资组合分析")
    print("=" * 60)

    # 创建投资组合
    portfolio = Portfolio(
        name="我的投资组合",
        description="包含几只A股股票的投资组合",
        assets=[
            Asset(
                symbol="600000.SH",
                name="浦发银行",
                asset_type=AssetType.STOCK,
                quantity=1000,
                avg_cost=10.5
            ),
            Asset(
                symbol="000001.SZ",
                name="平安银行",
                asset_type=AssetType.STOCK,
                quantity=500,
                avg_cost=15.2
            ),
            Asset(
                symbol="600036.SH",
                name="招商银行",
                asset_type=AssetType.STOCK,
                quantity=800,
                avg_cost=35.8
            ),
        ],
        cash=50000.0
    )

    # 创建分析服务
    analysis_service = PortfolioAnalysisService()

    # 分析投资组合
    print("\n正在分析投资组合...")
    metrics = await analysis_service.analyze_portfolio(portfolio, risk_free_rate=0.03)

    # 打印结果
    print(f"\n投资组合: {portfolio.name}")
    print(f"总市值: ¥{metrics.total_value:,.2f}")
    print(f"总成本: ¥{metrics.total_cost:,.2f}")
    print(f"总收益: ¥{metrics.total_return:,.2f}")
    print(f"总收益率: {metrics.total_return_rate * 100:.2f}%")

    if metrics.annualized_return:
        print(f"年化收益率: {metrics.annualized_return * 100:.2f}%")

    if metrics.volatility:
        print(f"波动率: {metrics.volatility * 100:.2f}%")

    if metrics.sharpe_ratio:
        print(f"夏普比率: {metrics.sharpe_ratio:.2f}")

    if metrics.max_drawdown:
        print(f"最大回撤: {metrics.max_drawdown * 100:.2f}%")

    if metrics.var_95:
        print(f"95% VaR: ¥{metrics.var_95:,.2f}")

    print("\n资产配置:")
    for asset_type, weight in metrics.asset_allocation.items():
        print(f"  {asset_type}: {weight * 100:.2f}%")

    # 打印每个资产的详情
    print("\n资产详情:")
    for asset in portfolio.assets:
        if asset.current_price:
            print(f"\n  {asset.name} ({asset.symbol})")
            print(f"    持仓: {asset.quantity} 股")
            print(f"    成本价: ¥{asset.avg_cost:.2f}")
            print(f"    当前价: ¥{asset.current_price:.2f}")
            print(f"    市值: ¥{asset.market_value:,.2f}")
            print(f"    盈亏: ¥{asset.profit_loss:,.2f}")
            print(f"    收益率: {asset.return_rate * 100:.2f}%")

    # 关闭市场数据服务
    await analysis_service.market_data_service.close()


async def example_market_data():
    """市场数据获取示例"""
    print("\n" + "=" * 60)
    print("示例2: 获取实时市场数据")
    print("=" * 60)

    market_service = MarketDataService()

    # 获取单个股票价格
    print("\n获取浦发银行实时价格...")
    data = await market_service.get_realtime_price("600000.SH")

    if data:
        print(f"\n股票: {data['name']} ({data['symbol']})")
        print(f"当前价: ¥{data['current_price']:.2f}")
        print(f"涨跌额: ¥{data['change']:.2f}")
        print(f"涨跌幅: {data['change_percent']:.2f}%")
        print(f"今开: ¥{data['open']:.2f}")
        print(f"昨收: ¥{data['prev_close']:.2f}")
        print(f"最高: ¥{data['high']:.2f}")
        print(f"最低: ¥{data['low']:.2f}")
        print(f"成交量: {data['volume']:,.0f} 手")
        print(f"成交额: ¥{data['amount']:,.2f}")

    # 批量获取
    print("\n\n批量获取多只股票价格...")
    symbols = ["600000.SH", "000001.SZ", "600036.SH"]
    prices = await market_service.get_realtime_prices(symbols)

    print(f"\n成功获取 {len(prices)} 只股票的价格:")
    for symbol, data in prices.items():
        print(f"  {data['name']}: ¥{data['current_price']:.2f} ({data['change_percent']:+.2f}%)")

    # 搜索股票
    print("\n\n搜索股票...")
    results = await market_service.search_stock("银行")

    print(f"\n搜索到 {len(results)} 个结果:")
    for i, stock in enumerate(results[:5], 1):  # 只显示前5个
        print(f"  {i}. {stock['name']} ({stock['symbol']})")

    await market_service.close()


async def example_risk_metrics():
    """风险指标计算示例"""
    print("\n" + "=" * 60)
    print("示例3: 风险指标计算")
    print("=" * 60)

    analysis_service = PortfolioAnalysisService()

    # 模拟收益率序列（30天）
    import numpy as np
    np.random.seed(42)
    returns = np.random.normal(0.001, 0.02, 30).tolist()  # 均值0.1%, 标准差2%

    print("\n计算风险指标...")
    print(f"样本数: {len(returns)} 天")

    # 波动率
    volatility = analysis_service.calculate_volatility(returns)
    print(f"波动率: {volatility * 100:.2f}%")

    # 夏普比率
    sharpe = analysis_service.calculate_sharpe_ratio(returns, risk_free_rate=0.03/252)
    print(f"夏普比率: {sharpe:.2f}")

    # 模拟组合价值序列
    initial_value = 1000000
    values = [initial_value * (1 + sum(returns[:i+1])) for i in range(len(returns))]

    # 最大回撤
    max_dd = analysis_service.calculate_max_drawdown(values)
    print(f"最大回撤: {max_dd * 100:.2f}%")

    # VaR
    var_95 = analysis_service.calculate_var(returns, confidence_level=0.95, portfolio_value=initial_value)
    print(f"95% VaR: ¥{var_95:,.2f}")

    # CVaR
    cvar_95 = analysis_service.calculate_cvar(returns, confidence_level=0.95, portfolio_value=initial_value)
    print(f"95% CVaR: ¥{cvar_95:,.2f}")


async def example_compare_portfolios():
    """投资组合比较示例"""
    print("\n" + "=" * 60)
    print("示例4: 比较多个投资组合")
    print("=" * 60)

    # 创建两个投资组合
    portfolio1 = Portfolio(
        name="保守型组合",
        assets=[
            Asset(
                symbol="600000.SH",
                name="浦发银行",
                asset_type=AssetType.STOCK,
                quantity=1000,
                avg_cost=10.5
            ),
        ],
        cash=100000.0
    )

    portfolio2 = Portfolio(
        name="进取型组合",
        assets=[
            Asset(
                symbol="000001.SZ",
                name="平安银行",
                asset_type=AssetType.STOCK,
                quantity=2000,
                avg_cost=15.2
            ),
            Asset(
                symbol="600036.SH",
                name="招商银行",
                asset_type=AssetType.STOCK,
                quantity=1000,
                avg_cost=35.8
            ),
        ],
        cash=20000.0
    )

    analysis_service = PortfolioAnalysisService()

    print("\n正在比较投资组合...")
    results = await analysis_service.compare_portfolios([portfolio1, portfolio2])

    print("\n比较结果:")
    for result in results:
        metrics = result['metrics']
        print(f"\n{result['name']}:")
        print(f"  总市值: ¥{metrics.total_value:,.2f}")
        print(f"  总收益率: {metrics.total_return_rate * 100:.2f}%")
        if metrics.sharpe_ratio:
            print(f"  夏普比率: {metrics.sharpe_ratio:.2f}")

    await analysis_service.market_data_service.close()


async def main():
    """运行所有示例"""
    try:
        await example_basic_analysis()
        await example_market_data()
        await example_risk_metrics()
        await example_compare_portfolios()

        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("投资组合分析工具 - 使用示例")
    print("=" * 60)
    asyncio.run(main())

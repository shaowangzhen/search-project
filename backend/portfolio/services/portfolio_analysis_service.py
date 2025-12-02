"""
投资组合分析服务
计算收益率、风险指标、资产配置等
"""
import sys
import os
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# 添加上级目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.portfolio_models import (
    Portfolio, Asset, PortfolioMetrics, AssetType
)
from services.market_data_service import MarketDataService


class PortfolioAnalysisService:
    """投资组合分析服务"""

    def __init__(self):
        self.market_data_service = MarketDataService()

    async def analyze_portfolio(
        self,
        portfolio: Portfolio,
        risk_free_rate: float = 0.03,
        historical_days: int = 252  # 一年的交易日
    ) -> PortfolioMetrics:
        """
        分析投资组合

        Args:
            portfolio: 投资组合
            risk_free_rate: 无风险利率
            historical_days: 历史数据天数

        Returns:
            投资组合指标
        """
        # 1. 更新资产价格
        await self._update_asset_prices(portfolio)

        # 2. 计算基础指标
        total_value = portfolio.total_market_value or 0
        total_cost = portfolio.total_cost
        total_return = portfolio.total_profit_loss or 0
        total_return_rate = portfolio.total_return_rate or 0

        # 3. 计算资产配置
        asset_allocation = self._calculate_asset_allocation(portfolio)

        # 4. 获取历史数据并计算高级指标
        # 注意：这里简化实现，实际应该使用真实的历史数据
        daily_return = None
        annualized_return = None
        volatility = None
        sharpe_ratio = None
        max_drawdown = None
        var_95 = None

        # 如果有历史数据，计算高级指标
        # 这里使用模拟数据演示计算方法
        if total_cost > 0:
            annualized_return = self._calculate_annualized_return(
                total_return_rate, days=365
            )

            # 使用蒙特卡洛模拟或历史波动率
            # 简化：假设波动率为年化15%
            volatility = 0.15

            # 计算夏普比率
            if volatility > 0:
                sharpe_ratio = (annualized_return - risk_free_rate) / volatility

            # 简化：假设最大回撤为10%
            max_drawdown = -0.10

            # 计算VaR（风险价值）
            # 95% VaR表示有95%的概率损失不会超过这个值
            if volatility > 0:
                var_95 = -1.645 * volatility * total_value / np.sqrt(252)  # 日VaR

        return PortfolioMetrics(
            total_value=total_value,
            total_cost=total_cost,
            total_return=total_return,
            total_return_rate=total_return_rate,
            daily_return=daily_return,
            annualized_return=annualized_return,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            var_95=var_95,
            asset_allocation=asset_allocation
        )

    async def _update_asset_prices(self, portfolio: Portfolio):
        """更新资产的当前价格"""
        # 提取所有需要更新价格的资产代码
        symbols = [
            asset.symbol for asset in portfolio.assets
            if asset.asset_type in [AssetType.STOCK, AssetType.ETF, AssetType.FUND]
        ]

        if not symbols:
            return

        # 批量获取价格
        price_data = await self.market_data_service.get_realtime_prices(symbols)

        # 更新资产价格
        for asset in portfolio.assets:
            if asset.symbol in price_data:
                asset.current_price = price_data[asset.symbol].get('current_price')

    def _calculate_asset_allocation(self, portfolio: Portfolio) -> Dict[str, float]:
        """
        计算资产配置比例

        Returns:
            资产类型到比例的映射
        """
        total_value = portfolio.total_market_value
        if not total_value or total_value == 0:
            return {}

        allocation = {}

        # 按资产类型分组计算
        for asset in portfolio.assets:
            asset_type = asset.asset_type.value
            market_value = asset.market_value or 0

            if asset_type not in allocation:
                allocation[asset_type] = 0
            allocation[asset_type] += market_value

        # 添加现金
        if portfolio.cash > 0:
            allocation['cash'] = portfolio.cash

        # 转换为百分比
        for asset_type in allocation:
            allocation[asset_type] = allocation[asset_type] / total_value

        return allocation

    def _calculate_annualized_return(self, return_rate: float, days: int) -> float:
        """
        计算年化收益率

        Args:
            return_rate: 总收益率
            days: 持有天数

        Returns:
            年化收益率
        """
        if days <= 0:
            return 0

        years = days / 365.0
        annualized = (1 + return_rate) ** (1 / years) - 1
        return annualized

    def calculate_volatility(self, returns: List[float]) -> float:
        """
        计算波动率（标准差）

        Args:
            returns: 收益率序列

        Returns:
            波动率
        """
        if not returns or len(returns) < 2:
            return 0

        return float(np.std(returns, ddof=1))

    def calculate_sharpe_ratio(
        self,
        returns: List[float],
        risk_free_rate: float = 0.03
    ) -> float:
        """
        计算夏普比率

        Args:
            returns: 收益率序列
            risk_free_rate: 无风险利率

        Returns:
            夏普比率
        """
        if not returns or len(returns) < 2:
            return 0

        avg_return = float(np.mean(returns))
        volatility = self.calculate_volatility(returns)

        if volatility == 0:
            return 0

        sharpe = (avg_return - risk_free_rate) / volatility
        return sharpe

    def calculate_max_drawdown(self, values: List[float]) -> float:
        """
        计算最大回撤

        Args:
            values: 资产价值序列

        Returns:
            最大回撤（负数）
        """
        if not values or len(values) < 2:
            return 0

        values_array = np.array(values)
        cummax = np.maximum.accumulate(values_array)
        drawdown = (values_array - cummax) / cummax

        max_dd = float(np.min(drawdown))
        return max_dd

    def calculate_var(
        self,
        returns: List[float],
        confidence_level: float = 0.95,
        portfolio_value: float = 1.0
    ) -> float:
        """
        计算VaR（风险价值）

        Args:
            returns: 收益率序列
            confidence_level: 置信水平（默认95%）
            portfolio_value: 组合价值

        Returns:
            VaR值（负数表示损失）
        """
        if not returns or len(returns) < 10:
            return 0

        # 使用历史模拟法
        returns_array = np.array(returns)
        percentile = (1 - confidence_level) * 100
        var_return = float(np.percentile(returns_array, percentile))

        var_value = var_return * portfolio_value
        return var_value

    def calculate_cvar(
        self,
        returns: List[float],
        confidence_level: float = 0.95,
        portfolio_value: float = 1.0
    ) -> float:
        """
        计算CVaR（条件风险价值/期望损失）

        Args:
            returns: 收益率序列
            confidence_level: 置信水平
            portfolio_value: 组合价值

        Returns:
            CVaR值
        """
        if not returns or len(returns) < 10:
            return 0

        returns_array = np.array(returns)
        percentile = (1 - confidence_level) * 100
        var_return = np.percentile(returns_array, percentile)

        # CVaR是低于VaR的所有收益率的平均值
        tail_returns = returns_array[returns_array <= var_return]
        if len(tail_returns) == 0:
            return 0

        cvar_return = float(np.mean(tail_returns))
        cvar_value = cvar_return * portfolio_value
        return cvar_value

    async def compare_portfolios(
        self,
        portfolios: List[Portfolio],
        risk_free_rate: float = 0.03
    ) -> List[Dict]:
        """
        比较多个投资组合

        Args:
            portfolios: 投资组合列表
            risk_free_rate: 无风险利率

        Returns:
            比较结果列表
        """
        results = []

        for portfolio in portfolios:
            metrics = await self.analyze_portfolio(portfolio, risk_free_rate)
            results.append({
                'name': portfolio.name,
                'metrics': metrics
            })

        return results

    async def optimize_allocation(
        self,
        assets: List[Asset],
        target_return: Optional[float] = None,
        max_risk: Optional[float] = None
    ) -> Dict[str, float]:
        """
        优化资产配置（简化版马科维茨投资组合理论）

        Args:
            assets: 资产列表
            target_return: 目标收益率
            max_risk: 最大风险

        Returns:
            优化后的资产权重
        """
        # 这里是一个简化实现
        # 实际应该使用优化算法（如scipy.optimize）来求解最优权重

        # 简单平均分配
        n_assets = len(assets)
        if n_assets == 0:
            return {}

        equal_weight = 1.0 / n_assets
        weights = {asset.symbol: equal_weight for asset in assets}

        return weights


# 创建全局实例
portfolio_analysis_service = PortfolioAnalysisService()

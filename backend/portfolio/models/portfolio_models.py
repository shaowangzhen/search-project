"""
投资组合数据模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    """资产类型"""
    STOCK = "stock"  # 股票
    BOND = "bond"  # 债券
    FUND = "fund"  # 基金
    ETF = "etf"  # ETF
    CASH = "cash"  # 现金
    CRYPTO = "crypto"  # 加密货币
    COMMODITY = "commodity"  # 商品
    OTHER = "other"  # 其他


class Asset(BaseModel):
    """资产"""
    symbol: str = Field(..., description="资产代码，如 600000.SH")
    name: str = Field(..., description="资产名称")
    asset_type: AssetType = Field(..., description="资产类型")
    quantity: float = Field(..., ge=0, description="持有数量")
    avg_cost: float = Field(..., ge=0, description="平均成本")
    current_price: Optional[float] = Field(None, ge=0, description="当前价格")

    @property
    def cost_basis(self) -> float:
        """成本基础"""
        return self.quantity * self.avg_cost

    @property
    def market_value(self) -> Optional[float]:
        """市值"""
        if self.current_price is None:
            return None
        return self.quantity * self.current_price

    @property
    def profit_loss(self) -> Optional[float]:
        """盈亏"""
        if self.market_value is None:
            return None
        return self.market_value - self.cost_basis

    @property
    def return_rate(self) -> Optional[float]:
        """收益率"""
        if self.market_value is None or self.cost_basis == 0:
            return None
        return (self.market_value - self.cost_basis) / self.cost_basis


class Portfolio(BaseModel):
    """投资组合"""
    name: str = Field(..., description="组合名称")
    description: Optional[str] = Field(None, description="组合描述")
    assets: List[Asset] = Field(default_factory=list, description="资产列表")
    cash: float = Field(default=0.0, ge=0, description="现金余额")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    @property
    def total_cost(self) -> float:
        """总成本"""
        return sum(asset.cost_basis for asset in self.assets) + self.cash

    @property
    def total_market_value(self) -> Optional[float]:
        """总市值"""
        asset_values = [asset.market_value for asset in self.assets if asset.market_value is not None]
        if len(asset_values) != len(self.assets):
            return None
        return sum(asset_values) + self.cash

    @property
    def total_profit_loss(self) -> Optional[float]:
        """总盈亏"""
        if self.total_market_value is None:
            return None
        return self.total_market_value - self.total_cost

    @property
    def total_return_rate(self) -> Optional[float]:
        """总收益率"""
        if self.total_market_value is None or self.total_cost == 0:
            return None
        return (self.total_market_value - self.total_cost) / self.total_cost


class Transaction(BaseModel):
    """交易记录"""
    symbol: str = Field(..., description="资产代码")
    transaction_type: str = Field(..., description="交易类型: buy/sell")
    quantity: float = Field(..., gt=0, description="交易数量")
    price: float = Field(..., ge=0, description="交易价格")
    fee: float = Field(default=0.0, ge=0, description="手续费")
    timestamp: datetime = Field(default_factory=datetime.now, description="交易时间")
    note: Optional[str] = Field(None, description="备注")

    @property
    def total_amount(self) -> float:
        """交易总额"""
        return self.quantity * self.price + self.fee


class PortfolioMetrics(BaseModel):
    """投资组合指标"""
    total_value: float = Field(..., description="总市值")
    total_cost: float = Field(..., description="总成本")
    total_return: float = Field(..., description="总收益")
    total_return_rate: float = Field(..., description="总收益率")
    daily_return: Optional[float] = Field(None, description="日收益率")
    annualized_return: Optional[float] = Field(None, description="年化收益率")
    volatility: Optional[float] = Field(None, description="波动率（标准差）")
    sharpe_ratio: Optional[float] = Field(None, description="夏普比率")
    max_drawdown: Optional[float] = Field(None, description="最大回撤")
    var_95: Optional[float] = Field(None, description="95% VaR（风险价值）")
    asset_allocation: Dict[str, float] = Field(default_factory=dict, description="资产配置比例")


class MarketDataRequest(BaseModel):
    """市场数据请求"""
    symbols: List[str] = Field(..., description="资产代码列表")


class MarketDataResponse(BaseModel):
    """市场数据响应"""
    data: Dict[str, Dict[str, Any]] = Field(..., description="市场数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="数据时间")


class PortfolioAnalysisRequest(BaseModel):
    """投资组合分析请求"""
    portfolio: Portfolio = Field(..., description="投资组合")
    risk_free_rate: float = Field(default=0.03, description="无风险利率，默认3%")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")


class PortfolioAnalysisResponse(BaseModel):
    """投资组合分析响应"""
    portfolio: Portfolio = Field(..., description="投资组合")
    metrics: PortfolioMetrics = Field(..., description="投资组合指标")
    analysis_time: datetime = Field(default_factory=datetime.now, description="分析时间")

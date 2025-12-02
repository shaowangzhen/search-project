"""
投资组合分析工具 API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import sys
import os

# 确保可以导入模块
sys.path.append(os.path.dirname(__file__))

from models.portfolio_models import (
    Portfolio, Asset, AssetType, Transaction,
    PortfolioAnalysisRequest, PortfolioAnalysisResponse,
    MarketDataRequest, MarketDataResponse, PortfolioMetrics
)
from services.portfolio_analysis_service import PortfolioAnalysisService
from services.market_data_service import MarketDataService

# 创建FastAPI应用
app = FastAPI(
    title="投资组合分析工具 API",
    description="提供投资组合分析、收益率计算、风险评估、资产配置等功能",
    version="1.0.0",
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建服务实例
analysis_service = PortfolioAnalysisService()
market_service = MarketDataService()

# 挂载静态文件
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    static_index = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_index):
        return FileResponse(static_index)

    # 如果没有前端页面，返回API信息
    return {
        "message": "投资组合分析工具 API",
        "version": "1.0.0",
        "description": "提供投资组合分析、收益率计算、风险评估、资产配置等功能",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "market_data": "/market/price",
            "search_stock": "/market/search",
            "analyze": "/portfolio/analyze",
            "metrics": "/portfolio/metrics"
        }
    }


@app.get("/api")
async def api_info():
    """API信息"""
    return {
        "message": "投资组合分析工具 API",
        "version": "1.0.0",
        "description": "提供投资组合分析、收益率计算、风险评估、资产配置等功能",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "market_data": "/market/price",
            "search_stock": "/market/search",
            "analyze": "/portfolio/analyze",
            "metrics": "/portfolio/metrics"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "portfolio-analysis",
        "version": "1.0.0"
    }


# ==================== 市场数据接口 ====================

@app.post("/market/price", response_model=MarketDataResponse)
async def get_market_data(request: MarketDataRequest):
    """
    获取市场数据（实时价格）

    Example:
    ```json
    {
        "symbols": ["600000.SH", "000001.SZ"]
    }
    ```
    """
    try:
        data = await market_service.get_realtime_prices(request.symbols)
        return MarketDataResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取市场数据失败: {str(e)}")


@app.get("/market/price/{symbol}")
async def get_stock_price(symbol: str):
    """获取单个股票的实时价格"""
    try:
        data = await market_service.get_realtime_price(symbol)
        if data is None:
            raise HTTPException(status_code=404, detail=f"未找到股票 {symbol} 的数据")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取股票价格失败: {str(e)}")


@app.get("/market/search/{keyword}")
async def search_stock(keyword: str):
    """搜索股票"""
    try:
        results = await market_service.search_stock(keyword)
        return {
            "keyword": keyword,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索股票失败: {str(e)}")


# ==================== 投资组合分析接口 ====================

@app.post("/portfolio/analyze", response_model=PortfolioAnalysisResponse)
async def analyze_portfolio(request: PortfolioAnalysisRequest):
    """
    分析投资组合

    Example:
    ```json
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
    """
    try:
        # 分析投资组合
        metrics = await analysis_service.analyze_portfolio(
            request.portfolio,
            request.risk_free_rate
        )

        return PortfolioAnalysisResponse(
            portfolio=request.portfolio,
            metrics=metrics
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析投资组合失败: {str(e)}")


@app.post("/portfolio/metrics")
async def calculate_metrics(portfolio: Portfolio, risk_free_rate: float = 0.03):
    """计算投资组合指标"""
    try:
        metrics = await analysis_service.analyze_portfolio(portfolio, risk_free_rate)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算指标失败: {str(e)}")


@app.post("/portfolio/allocation")
async def get_asset_allocation(portfolio: Portfolio):
    """获取资产配置"""
    try:
        # 更新价格
        await analysis_service._update_asset_prices(portfolio)

        # 计算配置
        allocation = analysis_service._calculate_asset_allocation(portfolio)

        return {
            "portfolio": portfolio.name,
            "total_value": portfolio.total_market_value,
            "allocation": allocation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算资产配置失败: {str(e)}")


@app.post("/portfolio/compare")
async def compare_portfolios(portfolios: List[Portfolio], risk_free_rate: float = 0.03):
    """比较多个投资组合"""
    try:
        results = await analysis_service.compare_portfolios(portfolios, risk_free_rate)
        return {
            "comparison": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"比较投资组合失败: {str(e)}")


# ==================== 工具接口 ====================

@app.get("/utils/asset-types")
async def get_asset_types():
    """获取支持的资产类型"""
    return {
        "asset_types": [
            {"value": "stock", "label": "股票"},
            {"value": "bond", "label": "债券"},
            {"value": "fund", "label": "基金"},
            {"value": "etf", "label": "ETF"},
            {"value": "cash", "label": "现金"},
            {"value": "crypto", "label": "加密货币"},
            {"value": "commodity", "label": "商品"},
            {"value": "other", "label": "其他"}
        ]
    }


@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理资源"""
    await market_service.close()


if __name__ == "__main__":
    import uvicorn
    print("🚀 启动投资组合分析工具 API...")
    print("📊 访问 http://localhost:8001/docs 查看API文档")
    uvicorn.run(app, host="0.0.0.0", port=8001)

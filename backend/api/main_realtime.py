"""
官方网站搜索引擎 - 实时搜索版本
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
from loguru import logger
import asyncio

from .models import SearchRequest, SearchResponse, SearchResult
from .services.realtime_search_service import RealtimeSearchService

# 创建FastAPI应用
app = FastAPI(
    title="官方网站搜索引擎API - 实时搜索版",
    description="专注于官方网站检索的实时搜索引擎API",
    version="2.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "官方网站搜索引擎API - 实时搜索版",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "实时搜索",
            "官方网站识别",
            "多搜索引擎聚合",
            "权威性评分"
        ]
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "realtime-search",
        "version": "2.0.0"
    }

@app.post("/api/v1/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    实时搜索接口
    
    Args:
        request: 搜索请求参数
        
    Returns:
        SearchResponse: 搜索结果
    """
    try:
        logger.info(f"Realtime search request: {request.query}")
        
        # 使用实时搜索服务
        async with RealtimeSearchService() as search_service:
            results = await search_service.search(
                query=request.query,
                max_results=request.size
            )
        
        # 转换结果格式
        search_results = []
        for result in results['results']:
            search_results.append(SearchResult(
                id=hash(result['url']) % 1000000,  # 生成简单ID
                title=result['title'],
                url=result['url'],
                snippet=result['snippet'],
                domain=result['domain'],
                official_score=result.get('official_score', 0.0),
                last_updated=result.get('last_updated', '2024-01-01T00:00:00Z'),
                category=result.get('category'),
                source=result.get('source', 'Unknown')
            ))
        
        return SearchResponse(
            total=results['total'],
            page=request.page,
            size=request.size,
            results=search_results
        )
        
    except Exception as e:
        logger.error(f"Realtime search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/v1/suggest")
async def get_suggestions(
    q: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=20)
):
    """
    搜索建议接口（简化版）
    
    Args:
        q: 搜索关键词
        limit: 建议数量限制
        
    Returns:
        List[str]: 搜索建议列表
    """
    try:
        # 简化版搜索建议
        suggestions = [
            f"{q} 官方网站",
            f"{q} 官网",
            f"{q} 政府",
            f"{q} 教育",
            f"{q} 机构"
        ]
        
        return {"suggestions": suggestions[:limit]}
        
    except Exception as e:
        logger.error(f"Get suggestions failed: {e}")
        return {"suggestions": []}

@app.get("/api/v1/search/engines")
async def get_search_engines():
    """获取支持的搜索引擎列表"""
    return {
        "engines": [
            {
                "name": "Google",
                "status": "active",
                "description": "Google搜索引擎"
            },
            {
                "name": "Bing",
                "status": "active", 
                "description": "微软Bing搜索引擎"
            },
            {
                "name": "DuckDuckGo",
                "status": "active",
                "description": "DuckDuckGo隐私搜索引擎"
            }
        ]
    }

@app.get("/api/v1/search/stats")
async def get_search_stats():
    """获取搜索统计信息"""
    return {
        "total_searches": 0,  # 可以添加统计功能
        "active_engines": 3,
        "average_response_time": "2.5s",
        "last_updated": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_realtime:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

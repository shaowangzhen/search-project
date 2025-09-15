"""
官方网站搜索引擎 - FastAPI主应用
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
from loguru import logger

from .models import SearchRequest, SearchResponse, WebsiteInfo
from .services.search_service import SearchService
from .services.website_service import WebsiteService

# 创建FastAPI应用
app = FastAPI(
    title="官方网站搜索引擎API",
    description="专注于官方网站检索的搜索引擎API",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
search_service = SearchService()
website_service = WebsiteService()

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "官方网站搜索引擎API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 检查各个服务的健康状态
        es_status = await search_service.health_check()
        db_status = await website_service.health_check()
        
        return {
            "status": "healthy" if es_status and db_status else "unhealthy",
            "elasticsearch": es_status,
            "database": db_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")

@app.post("/api/v1/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    搜索接口
    
    Args:
        request: 搜索请求参数
        
    Returns:
        SearchResponse: 搜索结果
    """
    try:
        logger.info(f"Search request: {request.query}")
        
        # 执行搜索
        results = await search_service.search(
            query=request.query,
            page=request.page,
            size=request.size,
            category=request.category
        )
        
        return SearchResponse(
            total=results["total"],
            page=request.page,
            size=request.size,
            results=results["results"]
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/api/v1/suggest")
async def get_suggestions(
    q: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=20)
):
    """
    搜索建议接口
    
    Args:
        q: 搜索关键词
        limit: 建议数量限制
        
    Returns:
        List[str]: 搜索建议列表
    """
    try:
        suggestions = await search_service.get_suggestions(q, limit)
        return {"suggestions": suggestions}
        
    except Exception as e:
        logger.error(f"Get suggestions failed: {e}")
        raise HTTPException(status_code=500, detail="Get suggestions failed")

@app.get("/api/v1/websites", response_model=List[WebsiteInfo])
async def get_websites(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None
):
    """
    获取网站列表
    
    Args:
        page: 页码
        size: 每页大小
        category: 分类筛选
        
    Returns:
        List[WebsiteInfo]: 网站信息列表
    """
    try:
        websites = await website_service.get_websites(page, size, category)
        return websites
        
    except Exception as e:
        logger.error(f"Get websites failed: {e}")
        raise HTTPException(status_code=500, detail="Get websites failed")

@app.post("/api/v1/websites")
async def add_website(website: WebsiteInfo):
    """
    添加新网站
    
    Args:
        website: 网站信息
        
    Returns:
        dict: 操作结果
    """
    try:
        result = await website_service.add_website(website)
        return {"message": "Website added successfully", "id": result}
        
    except Exception as e:
        logger.error(f"Add website failed: {e}")
        raise HTTPException(status_code=500, detail="Add website failed")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

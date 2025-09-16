from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import sys
import os

# 确保可以导入同级目录的服务
sys.path.append(os.path.dirname(__file__))

from services.realtime_search_service import RealtimeSearchService

app = FastAPI(
    title="官方网站搜索引擎 API",
    description="一个实时搜索官方网站的API，支持2个中文搜索引擎，采用5秒快速响应策略：总超时5秒，单个请求5秒，真正的并行搜索。",
    version="1.0.0",
)

# 添加CORS支持
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建搜索服务实例
search_service = RealtimeSearchService()

# 请求模型
class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 20

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[Dict[str, Any]]
    search_time: str
    engines_used: List[str]
    engines_count: int

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy", 
        "version": "1.0.0",
        "search_engines": ["百度", "搜狗"],
        "total_engines": 2,
        "strategy": "5秒快速响应策略 - 只使用百度、搜狗两个搜索引擎",
        "timeout_settings": {
            "total_timeout": "5.0秒",
            "single_request_timeout": "5.0秒",
            "max_engines_used": 2
        }
    }

# 搜索引擎信息
@app.get("/engines")
async def get_search_engines():
    """获取支持的搜索引擎列表"""
    return {
        "engines": [
            {"name": "百度", "url": "https://www.baidu.com", "type": "中文", "priority": "高"},
            {"name": "搜狗", "url": "https://www.sogou.com", "type": "中文", "priority": "中"}
        ],
        "total": 2,
        "strategy": "5秒快速响应策略 - 只使用百度、搜狗两个搜索引擎",
        "timeout_settings": {
            "total_timeout": "5.0秒",
            "single_request_timeout": "5.0秒",
            "max_engines_used": 2
        }
    }

# 搜索接口
@app.post("/search", response_model=SearchResponse)
async def search_official_websites(request: SearchRequest):
    """搜索官方网站 - 5秒快速响应策略，只使用百度、搜狗两个搜索引擎"""
    try:
        print(f"🔍 收到搜索请求: {request.query}")
        
        # 执行搜索
        results = await search_service.search(
            query=request.query,
            max_results=request.max_results
        )
        
        print(f"🎯 搜索完成，返回 {results['total_results']} 个结果，使用了 {results['engines_count']} 个搜索引擎，耗时 {results['search_time']}")
        
        return SearchResponse(**results)
        
    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "官方网站搜索引擎",
        "version": "1.0.0",
        "description": "支持2个中文搜索引擎的实时官方网站搜索，采用5秒快速响应策略，真正的并行搜索",
        "search_engines": ["百度", "搜狗"],
        "strategy": "5秒快速响应策略 - 只使用百度、搜狗两个搜索引擎",
        "timeout_settings": {
            "total_timeout": "5.0秒",
            "single_request_timeout": "5.0秒",
            "max_engines_used": 2
        },
        "docs": "/docs",
        "health": "/health",
        "engines": "/engines"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

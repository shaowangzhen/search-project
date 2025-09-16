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
    description="一个实时搜索官方网站的API，支持6个搜索引擎，采用快速响应策略：只取前3个最快响应的搜索引擎结果。",
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
        "search_engines": ["Google", "Bing", "DuckDuckGo", "百度", "搜狗", "360搜索"],
        "total_engines": 6,
        "strategy": "快速响应 - 只取前3个最快响应的搜索引擎结果",
        "timeout": "8秒"
    }

# 搜索引擎信息
@app.get("/engines")
async def get_search_engines():
    """获取支持的搜索引擎列表"""
    return {
        "engines": [
            {"name": "Google", "url": "https://www.google.com", "type": "国际", "priority": "高"},
            {"name": "Bing", "url": "https://www.bing.com", "type": "国际", "priority": "高"},
            {"name": "DuckDuckGo", "url": "https://duckduckgo.com", "type": "隐私", "priority": "中"},
            {"name": "百度", "url": "https://www.baidu.com", "type": "中文", "priority": "高"},
            {"name": "搜狗", "url": "https://www.sogou.com", "type": "中文", "priority": "中"},
            {"name": "360搜索", "url": "https://www.so.com", "type": "中文", "priority": "中"}
        ],
        "total": 6,
        "strategy": "快速响应策略",
        "max_engines_used": 3,
        "timeout": "8秒"
    }

# 搜索接口
@app.post("/search", response_model=SearchResponse)
async def search_official_websites(request: SearchRequest):
    """搜索官方网站 - 快速响应策略"""
    try:
        print(f"收到搜索请求: {request.query}")
        
        # 执行搜索
        results = await search_service.search(
            query=request.query,
            max_results=request.max_results
        )
        
        print(f"搜索完成，返回 {results['total_results']} 个结果，使用了 {results['engines_count']} 个搜索引擎")
        
        return SearchResponse(**results)
        
    except Exception as e:
        print(f"搜索出错: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "官方网站搜索引擎",
        "version": "1.0.0",
        "description": "支持6个搜索引擎的实时官方网站搜索，采用快速响应策略",
        "search_engines": ["Google", "Bing", "DuckDuckGo", "百度", "搜狗", "360搜索"],
        "strategy": "只取前3个最快响应的搜索引擎结果",
        "timeout": "8秒",
        "docs": "/docs",
        "health": "/health",
        "engines": "/engines"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

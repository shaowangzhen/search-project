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
    description="一个实时搜索官方网站的API，支持多搜索引擎聚合和基础的官方网站识别。",
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

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "version": "1.0.0"}

# 搜索接口
@app.post("/search", response_model=SearchResponse)
async def search_official_websites(request: SearchRequest):
    """搜索官方网站"""
    try:
        print(f"收到搜索请求: {request.query}")
        
        # 执行搜索
        results = await search_service.search(
            query=request.query,
            max_results=request.max_results
        )
        
        print(f"搜索完成，返回 {results['total_results']} 个结果")
        
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
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

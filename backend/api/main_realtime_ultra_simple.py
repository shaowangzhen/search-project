"""
极简版实时搜索API - Python 3.7兼容
只使用最基础的依赖，确保在Python 3.7环境下能正常运行
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import sys
import os

# 添加服务路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from realtime_search_service_ultra_simple import UltraSimpleRealtimeSearchService

# 创建FastAPI应用
app = FastAPI(
    title="官方网站搜索引擎 - 极简版",
    description="实时搜索官方网站，Python 3.7兼容版本",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建搜索服务实例
search_service = UltraSimpleRealtimeSearchService()

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
        "message": "官方网站搜索引擎 - 极简版",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

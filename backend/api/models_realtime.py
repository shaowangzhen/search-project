"""
实时搜索数据模型定义
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str = Field(..., min_length=1, max_length=200, description="搜索关键词")
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=50, description="每页大小")
    category: Optional[str] = Field(None, description="分类筛选")

class SearchResult(BaseModel):
    """搜索结果模型"""
    id: int
    title: str
    url: str
    snippet: str
    domain: str
    official_score: float = Field(..., ge=0.0, le=1.0)
    last_updated: str  # 使用字符串格式，因为实时搜索没有具体时间
    category: Optional[str] = None
    source: Optional[str] = None  # 搜索引擎来源

class SearchResponse(BaseModel):
    """搜索响应模型"""
    total: int
    page: int
    size: int
    results: List[SearchResult]

class SearchEngineInfo(BaseModel):
    """搜索引擎信息模型"""
    name: str
    status: str
    description: str

class SearchStats(BaseModel):
    """搜索统计模型"""
    total_searches: int
    active_engines: int
    average_response_time: str
    last_updated: str

class RealtimeSearchConfig(BaseModel):
    """实时搜索配置模型"""
    max_results_per_engine: int = Field(5, ge=1, le=20)
    timeout_seconds: int = Field(30, ge=5, le=60)
    official_threshold: float = Field(0.6, ge=0.0, le=1.0)
    enable_engines: List[str] = Field(["Google", "Bing", "DuckDuckGo"])

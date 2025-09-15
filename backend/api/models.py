"""
数据模型定义
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
    last_updated: datetime
    category: Optional[str] = None

class SearchResponse(BaseModel):
    """搜索响应模型"""
    total: int
    page: int
    size: int
    results: List[SearchResult]

class WebsiteInfo(BaseModel):
    """网站信息模型"""
    id: Optional[int] = None
    domain: str = Field(..., min_length=1, max_length=255)
    official_score: float = Field(0.0, ge=0.0, le=1.0)
    status: str = Field("pending", regex="^(active|inactive|pending)$")
    last_crawled: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CrawlRequest(BaseModel):
    """爬取请求模型"""
    url: HttpUrl
    depth: int = Field(1, ge=1, le=3)
    force_update: bool = False

class CrawlResponse(BaseModel):
    """爬取响应模型"""
    success: bool
    message: str
    pages_crawled: int = 0
    errors: List[str] = []

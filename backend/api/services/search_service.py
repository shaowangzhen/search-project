"""
搜索服务模块
"""
from typing import List, Dict, Any, Optional
from elasticsearch import AsyncElasticsearch
from loguru import logger
import json

class SearchService:
    """搜索服务类"""
    
    def __init__(self):
        self.es_client = AsyncElasticsearch(
            hosts=["localhost:9200"],
            http_auth=None,  # 生产环境需要配置认证
            verify_certs=False,  # 开发环境
            ssl_show_warn=False
        )
        self.index_name = "official_websites"
    
    async def health_check(self) -> bool:
        """检查Elasticsearch健康状态"""
        try:
            health = await self.es_client.cluster.health()
            return health["status"] in ["green", "yellow"]
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {e}")
            return False
    
    async def search(
        self, 
        query: str, 
        page: int = 1, 
        size: int = 10, 
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            page: 页码
            size: 每页大小
            category: 分类筛选
            
        Returns:
            Dict: 搜索结果
        """
        try:
            # 构建搜索查询
            search_body = self._build_search_query(query, page, size, category)
            
            # 执行搜索
            response = await self.es_client.search(
                index=self.index_name,
                body=search_body
            )
            
            # 处理搜索结果
            results = self._process_search_results(response)
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def _build_search_query(
        self, 
        query: str, 
        page: int, 
        size: int, 
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """构建Elasticsearch搜索查询"""
        
        # 计算分页偏移
        from_index = (page - 1) * size
        
        # 基础查询
        search_query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^3", "content^1", "meta_description^2"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        }
                    ],
                    "filter": []
                }
            },
            "sort": [
                {"official_score": {"order": "desc"}},
                {"page_rank": {"order": "desc"}},
                {"_score": {"order": "desc"}}
            ],
            "from": from_index,
            "size": size,
            "highlight": {
                "fields": {
                    "title": {"fragment_size": 100},
                    "content": {"fragment_size": 200}
                }
            }
        }
        
        # 添加分类筛选
        if category:
            search_query["query"]["bool"]["filter"].append({
                "term": {"category": category}
            })
        
        # 只搜索官方网站（official_score > 0.5）
        search_query["query"]["bool"]["filter"].append({
            "range": {"official_score": {"gte": 0.5}}
        })
        
        return search_query
    
    def _process_search_results(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """处理搜索结果"""
        hits = response["hits"]
        
        results = []
        for hit in hits["hits"]:
            source = hit["_source"]
            highlight = hit.get("highlight", {})
            
            # 构建摘要
            snippet = self._build_snippet(source, highlight)
            
            result = {
                "id": source["id"],
                "title": source["title"],
                "url": source["url"],
                "snippet": snippet,
                "domain": source["domain"],
                "official_score": source["official_score"],
                "last_updated": source["last_updated"],
                "category": source.get("category")
            }
            
            results.append(result)
        
        return {
            "total": hits["total"]["value"],
            "results": results
        }
    
    def _build_snippet(self, source: Dict[str, Any], highlight: Dict[str, Any]) -> str:
        """构建搜索结果摘要"""
        # 优先使用高亮内容
        if "content" in highlight:
            return highlight["content"][0]
        elif "title" in highlight:
            return highlight["title"][0]
        
        # 使用meta_description
        if source.get("meta_description"):
            return source["meta_description"]
        
        # 截取内容前200字符
        content = source.get("content", "")
        if len(content) > 200:
            return content[:200] + "..."
        
        return content
    
    async def get_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """
        获取搜索建议
        
        Args:
            query: 搜索关键词
            limit: 建议数量
            
        Returns:
            List[str]: 搜索建议列表
        """
        try:
            # 使用Elasticsearch的suggest功能
            suggest_body = {
                "suggest": {
                    "suggestion": {
                        "prefix": query,
                        "completion": {
                            "field": "suggest",
                            "size": limit
                        }
                    }
                }
            }
            
            response = await self.es_client.search(
                index=self.index_name,
                body=suggest_body
            )
            
            suggestions = []
            if "suggest" in response and "suggestion" in response["suggest"]:
                for option in response["suggest"]["suggestion"][0]["options"]:
                    suggestions.append(option["text"])
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Get suggestions failed: {e}")
            return []
    
    async def close(self):
        """关闭Elasticsearch连接"""
        await self.es_client.close()

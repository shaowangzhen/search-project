"""
实时搜索服务
"""
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from loguru import logger
from ..analyzer.official_website_detector import OfficialWebsiteDetector

class RealtimeSearchService:
    """实时搜索服务类"""
    
    def __init__(self):
        self.detector = OfficialWebsiteDetector()
        self.session = None
        self.search_engines = [
            {
                'name': 'Google',
                'url': 'https://www.google.com/search',
                'params': {'q': '', 'num': 10}
            },
            {
                'name': 'Bing',
                'url': 'https://www.bing.com/search',
                'params': {'q': '', 'count': 10}
            },
            {
                'name': 'DuckDuckGo',
                'url': 'https://duckduckgo.com/html',
                'params': {'q': '', 'kl': 'cn-zh'}
            }
        ]
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        实时搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数量
            
        Returns:
            Dict: 搜索结果
        """
        try:
            logger.info(f"Starting realtime search for: {query}")
            
            # 并行搜索多个搜索引擎
            tasks = []
            for engine in self.search_engines:
                task = self._search_engine(engine, query, max_results // len(self.search_engines))
                tasks.append(task)
            
            # 等待所有搜索完成
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 合并和去重结果
            all_results = []
            for result in results:
                if isinstance(result, list):
                    all_results.extend(result)
                elif isinstance(result, Exception):
                    logger.error(f"Search engine error: {result}")
            
            # 去重和过滤
            unique_results = self._deduplicate_results(all_results)
            
            # 过滤官方网站
            official_results = await self._filter_official_websites(unique_results)
            
            # 按权威性排序
            sorted_results = self._sort_by_authority(official_results)
            
            # 限制结果数量
            final_results = sorted_results[:max_results]
            
            logger.info(f"Found {len(final_results)} official websites for query: {query}")
            
            return {
                'total': len(final_results),
                'results': final_results,
                'query': query,
                'search_time': 0  # 可以添加实际搜索时间统计
            }
            
        except Exception as e:
            logger.error(f"Realtime search failed: {e}")
            return {
                'total': 0,
                'results': [],
                'query': query,
                'error': str(e)
            }
    
    async def _search_engine(self, engine: Dict[str, Any], query: str, max_results: int) -> List[Dict[str, Any]]:
        """搜索单个搜索引擎"""
        try:
            params = engine['params'].copy()
            params['q'] = query
            
            async with self.session.get(engine['url'], params=params) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_search_results(html, engine['name'])
                else:
                    logger.warning(f"Search engine {engine['name']} returned status {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error searching {engine['name']}: {e}")
            return []
    
    def _parse_search_results(self, html: str, engine_name: str) -> List[Dict[str, Any]]:
        """解析搜索结果HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            if engine_name == 'Google':
                results = self._parse_google_results(soup)
            elif engine_name == 'Bing':
                results = self._parse_bing_results(soup)
            elif engine_name == 'DuckDuckGo':
                results = self._parse_duckduckgo_results(soup)
            
            return results
            
        except Exception as e:
            logger.error(f"Error parsing {engine_name} results: {e}")
            return []
    
    def _parse_google_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析Google搜索结果"""
        results = []
        
        # Google搜索结果选择器
        search_results = soup.find_all('div', class_='g')
        
        for result in search_results:
            try:
                # 提取标题和链接
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    title = title_elem.get_text().strip()
                    url = link_elem.get('href', '')
                    
                    # 清理Google重定向URL
                    if url.startswith('/url?q='):
                        url = url.split('/url?q=')[1].split('&')[0]
                    
                    # 提取摘要
                    snippet_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ''
                    
                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'domain': urlparse(url).netloc,
                            'source': 'Google'
                        })
            except Exception as e:
                logger.error(f"Error parsing Google result: {e}")
                continue
        
        return results
    
    def _parse_bing_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析Bing搜索结果"""
        results = []
        
        # Bing搜索结果选择器
        search_results = soup.find_all('li', class_='b_algo')
        
        for result in search_results:
            try:
                # 提取标题和链接
                title_elem = result.find('h2')
                link_elem = title_elem.find('a') if title_elem else None
                
                if title_elem and link_elem:
                    title = title_elem.get_text().strip()
                    url = link_elem.get('href', '')
                    
                    # 提取摘要
                    snippet_elem = result.find('p')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ''
                    
                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'domain': urlparse(url).netloc,
                            'source': 'Bing'
                        })
            except Exception as e:
                logger.error(f"Error parsing Bing result: {e}")
                continue
        
        return results
    
    def _parse_duckduckgo_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析DuckDuckGo搜索结果"""
        results = []
        
        # DuckDuckGo搜索结果选择器
        search_results = soup.find_all('div', class_='result')
        
        for result in search_results:
            try:
                # 提取标题和链接
                title_elem = result.find('a', class_='result__a')
                
                if title_elem:
                    title = title_elem.get_text().strip()
                    url = title_elem.get('href', '')
                    
                    # 提取摘要
                    snippet_elem = result.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ''
                    
                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'domain': urlparse(url).netloc,
                            'source': 'DuckDuckGo'
                        })
            except Exception as e:
                logger.error(f"Error parsing DuckDuckGo result: {e}")
                continue
        
        return results
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重搜索结果"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    async def _filter_official_websites(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """过滤官方网站"""
        official_results = []
        
        for result in results:
            try:
                url = result.get('url', '')
                snippet = result.get('snippet', '')
                
                # 使用官方网站检测器
                is_official = self.detector.is_official_website(
                    url=url,
                    content=snippet,
                    threshold=0.6  # 降低阈值以包含更多结果
                )
                
                if is_official:
                    # 计算权威性评分
                    official_score = self.detector.calculate_official_score(
                        url=url,
                        content=snippet
                    )
                    
                    result['official_score'] = official_score
                    result['is_official'] = True
                    official_results.append(result)
                    
            except Exception as e:
                logger.error(f"Error filtering official website {result.get('url', '')}: {e}")
                continue
        
        return official_results
    
    def _sort_by_authority(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按权威性排序"""
        return sorted(results, key=lambda x: x.get('official_score', 0), reverse=True)
    
    async def get_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """获取搜索建议（简化版）"""
        # 这里可以实现搜索建议逻辑
        # 暂时返回空列表
        return []

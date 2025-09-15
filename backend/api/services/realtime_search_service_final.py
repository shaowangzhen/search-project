"""
最终版实时搜索服务 - Python 3.7兼容
去掉所有有问题的依赖，确保在Python 3.7环境下能正常运行
"""

import asyncio
import aiohttp
import re
from typing import List, Dict, Any
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import sys
import os

# 简单的日志记录
class SimpleLogger:
    def info(self, msg):
        print(f"[INFO] {msg}")
    
    def error(self, msg):
        print(f"[ERROR] {msg}")
    
    def debug(self, msg):
        print(f"[DEBUG] {msg}")
    
    def warning(self, msg):
        print(f"[WARNING] {msg}")

logger = SimpleLogger()

class FinalRealtimeSearchService:
    """最终版实时搜索服务"""
    
    def __init__(self):
        self.search_engines = {
            'google': 'https://www.google.com/search?q={query}&num=10',
            'bing': 'https://www.bing.com/search?q={query}&count=10',
            'duckduckgo': 'https://duckduckgo.com/html/?q={query}'
        }
        
        # 官方网站关键词
        self.official_keywords = [
            '官网', '官方网站', 'official', 'homepage', 'main site',
            'company', 'corporate', 'enterprise', 'organization'
        ]
        
        # 非官方网站关键词
        self.non_official_keywords = [
            '广告', '推广', '营销', '代理', '经销商', '第三方',
            'advertisement', 'promotion', 'marketing', 'agent',
            'dealer', 'third-party', 'affiliate'
        ]

    async def search(self, query: str, max_results: int = 20) -> Dict[str, Any]:
        """执行实时搜索"""
        logger.info(f"开始搜索: {query}")
        
        # 并行搜索多个搜索引擎
        tasks = []
        for engine_name, search_url in self.search_engines.items():
            task = self._search_engine(engine_name, search_url, query)
            tasks.append(task)
        
        # 等待所有搜索完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 合并结果
        all_results = []
        for result in results:
            if isinstance(result, list):
                all_results.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"搜索出错: {result}")
        
        # 去重和排序
        unique_results = self._deduplicate_results(all_results)
        scored_results = self._score_results(unique_results, query)
        
        # 返回前N个结果
        final_results = scored_results[:max_results]
        
        return {
            'query': query,
            'total_results': len(final_results),
            'results': final_results,
            'search_time': '实时搜索'
        }

    async def _search_engine(self, engine_name: str, search_url: str, query: str) -> List[Dict[str, Any]]:
        """搜索单个搜索引擎"""
        try:
            url = search_url.format(query=query)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_search_results(html, engine_name)
                    else:
                        logger.warning(f"{engine_name} 搜索失败: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"{engine_name} 搜索异常: {e}")
            return []

    def _parse_search_results(self, html: str, engine_name: str) -> List[Dict[str, Any]]:
        """解析搜索结果"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        if engine_name == 'google':
            results = self._parse_google_results(soup)
        elif engine_name == 'bing':
            results = self._parse_bing_results(soup)
        elif engine_name == 'duckduckgo':
            results = self._parse_duckduckgo_results(soup)
        
        return results

    def _parse_google_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析Google搜索结果"""
        results = []
        
        # 查找搜索结果容器
        search_results = soup.find_all('div', class_='g')
        
        for result in search_results:
            try:
                # 提取标题和链接
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    title = title_elem.get_text().strip()
                    url = link_elem.get('href', '')
                    
                    # 提取描述
                    desc_elem = result.find('span', class_='aCOpRe')
                    description = desc_elem.get_text().strip() if desc_elem else ''
                    
                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'Google'
                        })
            except Exception as e:
                logger.debug(f"解析Google结果出错: {e}")
                continue
        
        return results

    def _parse_bing_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析Bing搜索结果"""
        results = []
        
        # 查找搜索结果容器
        search_results = soup.find_all('li', class_='b_algo')
        
        for result in search_results:
            try:
                # 提取标题和链接
                title_elem = result.find('h2')
                link_elem = title_elem.find('a') if title_elem else None
                
                if title_elem and link_elem:
                    title = title_elem.get_text().strip()
                    url = link_elem.get('href', '')
                    
                    # 提取描述
                    desc_elem = result.find('p')
                    description = desc_elem.get_text().strip() if desc_elem else ''
                    
                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'Bing'
                        })
            except Exception as e:
                logger.debug(f"解析Bing结果出错: {e}")
                continue
        
        return results

    def _parse_duckduckgo_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析DuckDuckGo搜索结果"""
        results = []
        
        # 查找搜索结果容器
        search_results = soup.find_all('div', class_='result')
        
        for result in search_results:
            try:
                # 提取标题和链接
                title_elem = result.find('a', class_='result__a')
                
                if title_elem:
                    title = title_elem.get_text().strip()
                    url = title_elem.get('href', '')
                    
                    # 提取描述
                    desc_elem = result.find('a', class_='result__snippet')
                    description = desc_elem.get_text().strip() if desc_elem else ''
                    
                    if url and title:
                        results.append({
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'DuckDuckGo'
                        })
            except Exception as e:
                logger.debug(f"解析DuckDuckGo结果出错: {e}")
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

    def _score_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """为结果评分并排序"""
        for result in results:
            score = self._calculate_score(result, query)
            result['score'] = score
            result['is_official'] = score > 0.6
        
        # 按分数排序
        return sorted(results, key=lambda x: x['score'], reverse=True)

    def _calculate_score(self, result: Dict[str, Any], query: str) -> float:
        """计算官方网站评分"""
        score = 0.0
        title = result.get('title', '').lower()
        description = result.get('description', '').lower()
        url = result.get('url', '').lower()
        
        # 基础分数
        score += 0.1
        
        # URL域名分析
        try:
            domain = urlparse(url).netloc
            if domain:
                # 检查是否包含查询关键词
                if any(keyword in domain for keyword in query.lower().split()):
                    score += 0.2
                
                # 检查域名长度（通常官方网站域名较短）
                if len(domain) < 20:
                    score += 0.1
        except:
            pass
        
        # 标题分析
        title_lower = title.lower()
        for keyword in self.official_keywords:
            if keyword in title_lower:
                score += 0.2
        
        for keyword in self.non_official_keywords:
            if keyword in title_lower:
                score -= 0.3
        
        # 描述分析
        desc_lower = description.lower()
        for keyword in self.official_keywords:
            if keyword in desc_lower:
                score += 0.1
        
        for keyword in self.non_official_keywords:
            if keyword in desc_lower:
                score -= 0.2
        
        # 确保分数在0-1之间
        return max(0.0, min(1.0, score))

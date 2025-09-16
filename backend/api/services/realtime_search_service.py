import httpx
from bs4 import BeautifulSoup
import re
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class RealtimeSearchService:
    def __init__(self):
        self.search_engines = {
            "google": os.getenv("GOOGLE_SEARCH_URL", "https://www.google.com/search?q="),
            "bing": os.getenv("BING_SEARCH_URL", "https://www.bing.com/search?q="),
            "duckduckgo": os.getenv("DUCKDUCKGO_SEARCH_URL", "https://duckduckgo.com/?q="),
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def _fetch_results(self, session: httpx.AsyncClient, engine: str, query: str):
        url = self.search_engines.get(engine) + query
        try:
            print(f"Fetching from {engine}: {url}")
            response = await session.get(url, headers=self.headers, follow_redirects=True, timeout=10)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            print(f"Error fetching from {engine}: {e}")
            return None

    def _parse_results(self, html_content: str, engine: str):
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        results = []

        if engine == "google":
            for g in soup.find_all('div', class_='tF2CMy'):
                title_tag = g.find('h3')
                link_tag = g.find('a')
                snippet_tag = g.find('div', class_='VwiC3b')

                title = title_tag.get_text() if title_tag else "No Title"
                link = link_tag['href'] if link_tag else "No Link"
                snippet = snippet_tag.get_text() if snippet_tag else "No Snippet"
                results.append({"title": title, "link": link, "snippet": snippet})
        elif engine == "bing":
            for b in soup.find_all('li', class_='b_algo'):
                title_tag = b.find('h2')
                link_tag = b.find('a')
                snippet_tag = b.find('p')

                title = title_tag.get_text() if title_tag else "No Title"
                link = link_tag['href'] if link_tag else "No Link"
                snippet = snippet_tag.get_text() if snippet_tag else "No Snippet"
                results.append({"title": title, "link": link, "snippet": snippet})
        elif engine == "duckduckgo":
            for d in soup.find_all('div', class_='web-result'):
                title_tag = d.find('h2', class_='result__title')
                link_tag = d.find('a', class_='result__url')
                snippet_tag = d.find('a', class_='result__snippet')

                title = title_tag.get_text() if title_tag else "No Title"
                link = link_tag['href'] if link_tag else "No Link"
                snippet = snippet_tag.get_text() if snippet_tag else "No Snippet"
                results.append({"title": title, "link": link, "snippet": snippet})
        return results

    def _is_official_website(self, link: str, query: str) -> bool:
        if not link:
            return False

        # 简单的域名匹配
        query_parts = re.split(r'\s+', query.lower())
        domain = re.sub(r'https?://(?:www\.)?', '', link).split('/')[0]

        # 检查域名是否包含查询词
        for part in query_parts:
            if part and part in domain:
                return True

        # 进一步检查顶级域名和常见官方后缀
        official_tlds = ['.gov', '.edu', '.org', '.mil', '.int']
        if any(tld in domain for tld in official_tlds):
            return True

        # 针对特定关键词的更严格检查
        if "官网" in query or "官方网站" in query:
            if "official" in domain or "gov" in domain or "edu" in domain:
                return True

        return False

    async def search(self, query: str, max_results: int = 10):
        """执行实时搜索"""
        all_results = []
        
        async with httpx.AsyncClient() as session:
            tasks = [self._fetch_results(session, engine, query) for engine in self.search_engines]
            responses = await asyncio.gather(*tasks)

            for i, response_text in enumerate(responses):
                engine = list(self.search_engines.keys())[i]
                parsed_results = self._parse_results(response_text, engine)
                all_results.extend(parsed_results)

        # 过滤官方网站
        official_results = []
        for result in all_results:
            if self._is_official_website(result.get("link"), query):
                official_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "description": result.get("snippet", ""),
                    "source": "搜索引擎"
                })
                if len(official_results) >= max_results:
                    break

        return {
            'query': query,
            'total_results': len(official_results),
            'results': official_results,
            'search_time': '实时搜索'
        }

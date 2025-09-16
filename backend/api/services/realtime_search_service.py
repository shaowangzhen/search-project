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
            "baidu": os.getenv("BAIDU_SEARCH_URL", "https://www.baidu.com/s?wd="),
            "sogou": os.getenv("SOGOU_SEARCH_URL", "https://www.sogou.com/web?query="),
            "360": os.getenv("360_SEARCH_URL", "https://www.so.com/s?q="),
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def _fetch_results(self, session: httpx.AsyncClient, engine: str, query: str):
        url = self.search_engines.get(engine) + query
        try:
            print(f"🚀 并行启动 {engine} 搜索: {url}")
            # 单个请求超时时间1.5秒
            response = await session.get(url, headers=self.headers, follow_redirects=True, timeout=1.5)
            response.raise_for_status()
            print(f"✅ {engine} 搜索完成")
            return response.text
        except httpx.RequestError as e:
            print(f"❌ {engine} 搜索失败: {e}")
            return None
        except asyncio.TimeoutError:
            print(f"⏰ {engine} 搜索超时 (1.5s)")
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
                
        elif engine == "baidu":
            # 百度搜索结果解析
            for result in soup.find_all('div', class_='result'):
                title_tag = result.find('h3')
                link_tag = result.find('a')
                snippet_tag = result.find('span', class_='content-right_8Zs40')

                if title_tag and link_tag:
                    title = title_tag.get_text().strip()
                    link = link_tag.get('href', '')
                    snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                    
                    # 处理百度重定向链接
                    if link.startswith('/link?url='):
                        # 提取真实URL
                        import urllib.parse
                        try:
                            decoded_url = urllib.parse.unquote(link.split('url=')[1].split('&')[0])
                            link = decoded_url
                        except:
                            continue
                    
                    results.append({"title": title, "link": link, "snippet": snippet})
                    
        elif engine == "sogou":
            # 搜狗搜索结果解析
            for result in soup.find_all('div', class_='result'):
                title_tag = result.find('h3')
                link_tag = result.find('a')
                snippet_tag = result.find('p', class_='str_info')

                if title_tag and link_tag:
                    title = title_tag.get_text().strip()
                    link = link_tag.get('href', '')
                    snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                    results.append({"title": title, "link": link, "snippet": snippet})
                    
        elif engine == "360":
            # 360搜索结果解析
            for result in soup.find_all('li', class_='res-list'):
                title_tag = result.find('h3')
                link_tag = result.find('a')
                snippet_tag = result.find('p', class_='res-desc')

                if title_tag and link_tag:
                    title = title_tag.get_text().strip()
                    link = link_tag.get('href', '')
                    snippet = snippet_tag.get_text().strip() if snippet_tag else ''
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
        official_tlds = ['.gov', '.edu', '.org', '.mil', '.int', '.gov.cn', '.edu.cn']
        if any(tld in domain for tld in official_tlds):
            return True

        # 针对特定关键词的更严格检查
        if "官网" in query or "官方网站" in query:
            if "official" in domain or "gov" in domain or "edu" in domain:
                return True

        # 中文官方网站关键词检查
        chinese_official_keywords = ['官网', '官方', '政府', '教育', '机构', '组织']
        for keyword in chinese_official_keywords:
            if keyword in query and keyword in domain:
                return True

        return False

    async def search(self, query: str, max_results: int = 10):
        """执行实时搜索 - 3秒内返回结果，真正的并行搜索"""
        import time
        start_time = time.time()
        
        all_results = []
        successful_engines = []
        
        async with httpx.AsyncClient() as session:
            # 创建所有搜索任务 - 真正的并行启动
            tasks = {}
            for engine in self.search_engines:
                task = asyncio.create_task(self._fetch_results(session, engine, query))
                tasks[engine] = task
            
            print(f"🚀 并行启动 {len(tasks)} 个搜索引擎任务")
            
            # 等待前3个成功的响应，总超时时间2.5秒
            completed_count = 0
            max_engines = 3
            total_timeout = 2.5  # 总超时时间2.5秒
            
            # 使用 asyncio.wait 实现真正的并行等待
            pending_tasks = set(tasks.values())
            completed_tasks = set()
            
            while pending_tasks and completed_count < max_engines:
                # 检查总时间是否超时
                if time.time() - start_time > total_timeout:
                    print(f"⏰ 总搜索时间超过 {total_timeout} 秒，停止等待")
                    break
                
                try:
                    # 等待任意一个任务完成，超时时间1秒
                    done, pending_tasks = await asyncio.wait(
                        pending_tasks, 
                        return_when=asyncio.FIRST_COMPLETED,
                        timeout=1.0
                    )
                    
                    for task in done:
                        # 找到对应的引擎名称
                        engine_name = None
                        for eng, t in tasks.items():
                            if t == task:
                                engine_name = eng
                                break
                        
                        if engine_name:
                            try:
                                response_text = await task
                                if response_text:
                                    parsed_results = self._parse_results(response_text, engine_name)
                                    all_results.extend(parsed_results)
                                    successful_engines.append(engine_name)
                                    completed_count += 1
                                    elapsed = time.time() - start_time
                                    print(f"✅ {engine_name} 搜索完成，获得 {len(parsed_results)} 个结果，耗时 {elapsed:.2f}s")
                                    
                                    # 如果已经获得3个引擎的结果，取消剩余任务
                                    if completed_count >= max_engines:
                                        print(f"🎯 已获得前3个引擎结果，取消剩余任务")
                                        for remaining_task in pending_tasks:
                                            remaining_task.cancel()
                                        break
                                else:
                                    print(f"❌ {engine_name} 未返回有效结果")
                            except Exception as e:
                                print(f"❌ {engine_name} 处理结果失败: {e}")
                        
                        completed_tasks.add(task)
                        
                except asyncio.TimeoutError:
                    elapsed = time.time() - start_time
                    print(f"⏰ 等待任务完成超时，总耗时 {elapsed:.2f}s")
                    break
                except Exception as e:
                    print(f"❌ 并行搜索过程出错: {e}")
                    break
            
            # 取消所有剩余任务
            for task in pending_tasks:
                if not task.done():
                    task.cancel()
                    print(f"❌ 取消剩余任务")

        total_elapsed = time.time() - start_time
        print(f"📊 搜索完成统计: 成功 {len(successful_engines)} 个引擎: {', '.join(successful_engines)}，总耗时 {total_elapsed:.2f}s")

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
            'search_time': f'{total_elapsed:.2f}s',
            'engines_used': successful_engines,
            'engines_count': len(successful_engines)
        }

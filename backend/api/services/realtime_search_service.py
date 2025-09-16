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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    async def _fetch_results(self, session: httpx.AsyncClient, engine: str, query: str):
        url = self.search_engines.get(engine) + query
        try:
            print(f"🚀 启动 {engine} 搜索: {url}")
            # 增加超时时间到3秒
            response = await session.get(url, headers=self.headers, follow_redirects=True, timeout=3.0)
            response.raise_for_status()
            print(f"✅ {engine} 搜索完成，状态码: {response.status_code}")
            return response.text
        except httpx.RequestError as e:
            print(f"❌ {engine} 搜索失败: {e}")
            return None
        except asyncio.TimeoutError:
            print(f"⏰ {engine} 搜索超时 (3.0s)")
            return None
        except Exception as e:
            print(f"❌ {engine} 搜索异常: {e}")
            return None

    def _parse_results(self, html_content: str, engine: str):
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        results = []

        if engine == "google":
            # Google搜索结果解析 - 多种选择器备选
            selectors = [
                'div.tF2CMy',
                'div.g',
                'div[data-ved]',
                'div.rc',
                'div[jscontroller]'
            ]
            
            for selector in selectors:
                for g in soup.select(selector):
                    title_tag = g.find('h3') or g.find('h2')
                    link_tag = g.find('a')
                    snippet_tag = g.find('div', class_='VwiC3b') or g.find('span', class_='aCOpRe')

                    if title_tag and link_tag:
                        title = title_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                        
                        # 处理Google重定向链接
                        if link.startswith('/url?q='):
                            try:
                                import urllib.parse
                                link = urllib.parse.unquote(link.split('/url?q=')[1].split('&')[0])
                            except:
                                continue
                        
                        results.append({"title": title, "link": link, "snippet": snippet})
                        
        elif engine == "bing":
            # Bing搜索结果解析 - 多种选择器备选
            selectors = [
                'li.b_algo',
                'div.b_algo',
                'li[data-bm]',
                'div[data-bm]'
            ]
            
            for selector in selectors:
                for b in soup.select(selector):
                    title_tag = b.find('h2') or b.find('h3')
                    link_tag = b.find('a')
                    snippet_tag = b.find('p') or b.find('div', class_='b_caption')

                    if title_tag and link_tag:
                        title = title_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                        results.append({"title": title, "link": link, "snippet": snippet})
                        
        elif engine == "baidu":
            # 百度搜索结果解析 - 多种选择器备选
            selectors = [
                'div.result',
                'div[data-log]',
                'div.c-container',
                'div[mu]',
                'div[data-click]'
            ]
            
            for selector in selectors:
                for result in soup.select(selector):
                    title_tag = result.find('h3') or result.find('h2')
                    link_tag = result.find('a')
                    snippet_tag = result.find('span', class_='content-right_8Zs40') or result.find('div', class_='c-abstract') or result.find('span', class_='c-color-text') or result.find('div', class_='c-span')

                    if title_tag and link_tag:
                        title = title_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                        
                        # 处理百度重定向链接
                        if link.startswith('/link?url='):
                            try:
                                import urllib.parse
                                decoded_url = urllib.parse.unquote(link.split('url=')[1].split('&')[0])
                                link = decoded_url
                            except:
                                continue
                        
                        results.append({"title": title, "link": link, "snippet": snippet})
            
            # 如果上面的选择器都没有找到结果，尝试更通用的方法
            if not results:
                print(f"🔍 {engine} 使用通用解析方法")
                for result in soup.find_all('div'):
                    title_tag = result.find('h3') or result.find('h2')
                    link_tag = result.find('a')
                    
                    if title_tag and link_tag and link_tag.get('href'):
                        title = title_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        
                        # 只处理包含http的链接
                        if link.startswith('http'):
                            snippet = ''
                            snippet_tag = result.find('span') or result.find('div')
                            if snippet_tag:
                                snippet = snippet_tag.get_text().strip()
                            
                            results.append({"title": title, "link": link, "snippet": snippet})
                            
                            if len(results) >= 10:  # 限制结果数量
                                break
                        
        elif engine == "sogou":
            # 搜狗搜索结果解析 - 多种选择器备选
            selectors = [
                'div.result',
                'div[data-log]',
                'div.vrwrap',
                'div[mu]'
            ]
            
            for selector in selectors:
                for result in soup.select(selector):
                    title_tag = result.find('h3') or result.find('h2')
                    link_tag = result.find('a')
                    snippet_tag = result.find('p', class_='str_info') or result.find('div', class_='str_info')

                    if title_tag and link_tag:
                        title = title_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                        results.append({"title": title, "link": link, "snippet": snippet})
                        
        elif engine == "360":
            # 360搜索结果解析 - 多种选择器备选
            selectors = [
                'li.res-list',
                'div.res-list',
                'li[data-log]',
                'div[data-log]'
            ]
            
            for selector in selectors:
                for result in soup.select(selector):
                    title_tag = result.find('h3') or result.find('h2')
                    link_tag = result.find('a')
                    snippet_tag = result.find('p', class_='res-desc') or result.find('div', class_='res-desc')

                    if title_tag and link_tag:
                        title = title_tag.get_text().strip()
                        link = link_tag.get('href', '')
                        snippet = snippet_tag.get_text().strip() if snippet_tag else ''
                        results.append({"title": title, "link": link, "snippet": snippet})
                    
        print(f"�� {engine} 解析到 {len(results)} 个结果")
        return results

    def _is_official_website(self, link: str, query: str) -> bool:
        if not link or link == "No Link":
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
            
            # 使用 asyncio.as_completed 实现真正的并行等待
            completed_count = 0
            max_engines = 3
            total_timeout = 3.0  # 总超时时间3.0秒
            
            try:
                # 使用 asyncio.as_completed 实现真正的并行处理
                for task in asyncio.as_completed(tasks.values(), timeout=total_timeout):
                    # 检查总时间是否超时
                    elapsed = time.time() - start_time
                    if elapsed > total_timeout:
                        print(f"⏰ 总搜索时间超过 {total_timeout} 秒，停止等待")
                        break
                    
                    if completed_count >= max_engines:
                        print(f"🎯 已获得前3个引擎结果，取消剩余任务")
                        break
                    
                    try:
                        response_text = await task
                        
                        # 找到对应的引擎名称
                        engine_name = None
                        for eng, t in tasks.items():
                            if t == task:
                                engine_name = eng
                                break
                        
                        if engine_name and response_text:
                            parsed_results = self._parse_results(response_text, engine_name)
                            all_results.extend(parsed_results)
                            successful_engines.append(engine_name)
                            completed_count += 1
                            elapsed = time.time() - start_time
                            print(f"✅ {engine_name} 搜索完成，获得 {len(parsed_results)} 个结果，耗时 {elapsed:.2f}s")
                        else:
                            print(f"❌ {engine_name} 未返回有效结果")
                            
                    except asyncio.TimeoutError:
                        elapsed = time.time() - start_time
                        print(f"⏰ 任务超时，总耗时 {elapsed:.2f}s")
                        break
                    except Exception as e:
                        print(f"❌ 任务处理失败: {e}")
                        continue
                        
            except asyncio.TimeoutError:
                elapsed = time.time() - start_time
                print(f"⏰ 总搜索超时，总耗时 {elapsed:.2f}s")
            
            # 取消所有剩余任务
            for engine, task in tasks.items():
                if not task.done():
                    task.cancel()
                    print(f"❌ 取消 {engine} 任务")

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

        print(f"🎯 官方网站过滤: 从 {len(all_results)} 个结果中筛选出 {len(official_results)} 个官方网站")

        return {
            'query': query,
            'total_results': len(official_results),
            'results': official_results,
            'search_time': f'{total_elapsed:.2f}s',
            'engines_used': successful_engines,
            'engines_count': len(successful_engines)
        }

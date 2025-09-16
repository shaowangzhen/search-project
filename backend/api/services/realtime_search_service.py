import httpx
from bs4 import BeautifulSoup
import re
import asyncio
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class RealtimeSearchService:
    def __init__(self):
        # 只保留搜狗搜索引擎，百度有反爬虫机制
        self.search_engines = {
            "sogou": os.getenv("SOGOU_SEARCH_URL", "https://www.sogou.com/web?query="),
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
        # 修复URL编码问题
        encoded_query = urllib.parse.quote(query)
        url = self.search_engines.get(engine) + encoded_query
        try:
            print(f"🚀 启动 {engine} 搜索: {url}")
            # 增加超时时间到5秒
            response = await session.get(url, headers=self.headers, follow_redirects=True, timeout=5.0)
            response.raise_for_status()
            print(f"✅ {engine} 搜索完成，状态码: {response.status_code}")
            # 使用response.text自动解压缩
            return response.text
        except httpx.RequestError as e:
            print(f"❌ {engine} 搜索失败: {e}")
            return None
        except asyncio.TimeoutError:
            print(f"⏰ {engine} 搜索超时 (5.0s)")
            return None
        except Exception as e:
            print(f"❌ {engine} 搜索异常: {e}")
            return None

    def _parse_results(self, html_content: str, engine: str):
        if not html_content:
            print(f"⚠️ {engine} HTML内容为空")
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        results = []
        
        print(f"🔍 {engine} 开始解析HTML内容，长度: {len(html_content)} 字符")

        if engine == "sogou":
            # 搜狗搜索结果解析 - 使用更通用的方法
            print(f"🔍 {engine} 使用通用解析方法...")
            
            for div in soup.find_all('div'):
                title_tag = div.find('h3') or div.find('h2') or div.find('a')
                if not title_tag:
                    continue
                    
                link_tag = div.find('a')
                if not link_tag or not link_tag.get('href'):
                    continue
                    
                title = title_tag.get_text().strip()
                link = link_tag.get('href', '')
                
                if link.startswith('http'):
                    snippet = ''
                    snippet_tag = div.find('p') or div.find('span') or div.find('div')
                    if snippet_tag:
                        snippet = snippet_tag.get_text().strip()
                    
                    print(f"📄 {engine} 解析到结果: 标题='{title[:50]}...', 链接='{link[:50]}...'")
                    results.append({"title": title, "link": link, "snippet": snippet})
                    
                    if len(results) >= 15:  # 增加结果数量限制
                        print(f"🔍 {engine} 达到结果数量限制，停止解析")
                        break
                    
        print(f"📊 {engine} 解析完成，共获得 {len(results)} 个结果")
        return results

    def _is_official_website(self, link: str, query: str) -> bool:
        if not link or link == "No Link":
            return False

        # 提取域名
        domain = re.sub(r'https?://(?:www\.)?', '', link).split('/')[0]
        print(f"     检查链接: {link}，域名: {domain}")

        # 扩展的中文到英文映射
        chinese_to_english = {
            '优酷': 'youku',
            '百度': 'baidu', 
            '腾讯': 'tencent',
            '阿里巴巴': 'alibaba',
            '新浪': 'sina',
            '网易': 'netease',
            '搜狐': 'sohu',
            '京东': 'jd',
            '淘宝': 'taobao',
            '天猫': 'tmall',
            '微信': 'wechat',
            'QQ': 'qq',
            '微博': 'weibo',
            '知乎': 'zhihu',
            '抖音': 'douyin',
            '快手': 'kuaishou',
            'B站': 'bilibili',
            '爱奇艺': 'iqiyi',
            '腾讯视频': 'v.qq',
            '芒果TV': 'mgtv',
            '哔哩哔哩': 'bilibili',
            '华为': 'huawei',
            '小米': 'xiaomi',
            'OPPO': 'oppo',
            'vivo': 'vivo',
            '美团': 'meituan',
            '滴滴': 'didi',
            '字节跳动': 'bytedance',
            '今日头条': 'toutiao',
            '拼多多': 'pinduoduo',
            '携程': 'ctrip',
            '去哪儿': 'qunar',
            '同程': 'ly',
            '马蜂窝': 'mafengwo',
            '途牛': 'tuniu',
            '飞猪': 'fliggy',
            '去哪儿网': 'qunar',
            '同程网': 'ly',
            '马蜂窝网': 'mafengwo',
            '途牛网': 'tuniu',
            '飞猪网': 'fliggy'
        }

        # 检查域名是否包含查询词（支持中英文匹配）
        query_parts = re.split(r'\s+', query.lower())
        for part in query_parts:
            if part and part in domain:
                print(f"    🎯 官方网站匹配: 查询词 '{part}' 匹配域名 '{domain}'")
                return True
            
            # 检查中文到英文的映射
            if part in chinese_to_english:
                english_part = chinese_to_english[part]
                if english_part in domain:
                    print(f"    🎯 官方网站匹配: 中文查询词 '{part}' 对应英文 '{english_part}' 匹配域名 '{domain}'")
                    return True

        # 进一步检查顶级域名和常见官方后缀
        official_tlds = ['.gov', '.edu', '.org', '.mil', '.int', '.gov.cn', '.edu.cn']
        if any(tld in domain for tld in official_tlds):
            print(f"    🎯 官方网站匹配: 域名 '{domain}' 包含官方后缀")
            return True

        # 针对特定关键词的更严格检查
        if "官网" in query or "官方网站" in query:
            if "official" in domain or "gov" in domain or "edu" in domain:
                print(f"    🎯 官方网站匹配: 查询包含官网关键词，域名 '{domain}' 匹配")
                return True

        # 中文官方网站关键词检查
        chinese_official_keywords = ['官网', '官方', '政府', '教育', '机构', '组织']
        for keyword in chinese_official_keywords:
            if keyword in query and keyword in domain:
                print(f"    🎯 官方网站匹配: 中文关键词 '{keyword}' 匹配域名 '{domain}'")
                return True

        # 放宽条件：如果查询词在标题中出现，也认为是官方网站
        # 这里我们需要从外部传入标题，暂时跳过

        print(f"    ❌ 未识别为官方网站")
        return False

    async def search(self, query: str, max_results: int = 10):
        """执行实时搜索 - 5秒内返回结果，只使用搜狗搜索引擎"""
        import time
        start_time = time.time()
        
        all_results = []
        successful_engines = []
        
        print(f"🔍 开始搜索: '{query}'，使用搜索引擎: {list(self.search_engines.keys())}")
        
        async with httpx.AsyncClient() as session:
            # 创建所有搜索任务 - 真正的并行启动
            tasks = {}
            for engine in self.search_engines:
                task = asyncio.create_task(self._fetch_results(session, engine, query))
                tasks[engine] = task
            
            print(f"🚀 并行启动 {len(tasks)} 个搜索引擎任务")
            
            # 修复：使用 asyncio.wait 而不是 asyncio.as_completed
            try:
                # 等待所有任务完成，但设置超时
                done, pending = await asyncio.wait(tasks.values(), timeout=5.0, return_when=asyncio.ALL_COMPLETED)
                
                # 处理完成的任务
                for task in done:
                    try:
                        # 找到对应的引擎名称
                        engine_name = None
                        for eng, t in tasks.items():
                            if t == task:
                                engine_name = eng
                                break
                        
                        if engine_name:
                            response_text = task.result()
                            if response_text:
                                print(f"🔍 {engine_name} 开始解析搜索结果...")
                                parsed_results = self._parse_results(response_text, engine_name)
                                
                                print(f"📊 {engine_name} 解析完成，获得 {len(parsed_results)} 个原始结果")
                                
                                # 显示解析到的结果详情
                                for i, result in enumerate(parsed_results[:5]):  # 显示前5个
                                    print(f"  📄 结果{i+1}: 标题='{result.get('title', '')[:30]}...', 链接='{result.get('link', '')[:50]}...'")
                                
                                all_results.extend(parsed_results)
                                successful_engines.append(engine_name)
                                elapsed = time.time() - start_time
                                print(f"✅ {engine_name} 搜索完成，获得 {len(parsed_results)} 个结果，耗时 {elapsed:.2f}s")
                            else:
                                print(f"❌ {engine_name} 未返回有效结果")
                        else:
                            print(f"❌ 无法找到对应的引擎名称")
                            
                    except Exception as e:
                        print(f"❌ 任务处理失败: {e}")
                        import traceback
                        traceback.print_exc()
                
                # 取消未完成的任务
                for task in pending:
                    task.cancel()
                    print(f"❌ 取消未完成的任务")
                        
            except asyncio.TimeoutError:
                elapsed = time.time() - start_time
                print(f"⏰ 总搜索超时，总耗时 {elapsed:.2f}s")
                # 取消所有任务
                for task in tasks.values():
                    if not task.done():
                        task.cancel()

        total_elapsed = time.time() - start_time
        print(f"📊 搜索完成统计: 成功 {len(successful_engines)} 个引擎: {', '.join(successful_engines)}，总耗时 {total_elapsed:.2f}s")
        print(f"📊 原始结果汇总: 共获得 {len(all_results)} 个原始搜索结果")

        # 过滤官方网站
        print(f"🔍 开始过滤官方网站...")
        official_results = []
        for i, result in enumerate(all_results):
            link = result.get("link", "")
            title = result.get("title", "")
            print(f"🔍 检查结果{i+1}: 标题='{title[:30]}...', 链接='{link[:50]}...'")
            
            if self._is_official_website(link, query):
                official_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "description": result.get("snippet", ""),
                    "source": "搜索引擎"
                })
                print(f"✅ 结果{i+1} 被识别为官方网站")
                if len(official_results) >= max_results:
                    print(f"🎯 已达到最大结果数量限制 {max_results}，停止过滤")
                    break
            else:
                print(f"❌ 结果{i+1} 不是官方网站")

        print(f"🎯 官方网站过滤完成: 从 {len(all_results)} 个原始结果中筛选出 {len(official_results)} 个官方网站")

        return {
            'query': query,
            'total_results': len(official_results),
            'results': official_results,
            'search_time': f'{total_elapsed:.2f}s',
            'engines_used': successful_engines,
            'engines_count': len(successful_engines)
        }

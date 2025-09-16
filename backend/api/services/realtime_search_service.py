import httpx
from bs4 import BeautifulSoup
import re
import asyncio
import os
import urllib.parse
import json
from dotenv import load_dotenv

load_dotenv()

class RealtimeSearchService:
    def __init__(self):
        # 添加百度、搜狗、360三个搜索引擎
        self.search_engines = {
            "baidu": os.getenv("BAIDU_SEARCH_URL", "https://www.baidu.com/s?wd="),
            "sogou": os.getenv("SOGOU_SEARCH_URL", "https://www.sogou.com/web?query="),
            "360": os.getenv("360_SEARCH_URL", "https://www.so.com/s?q="),
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        # 加载官网名录
        self.official_websites = self._load_official_websites()
        
        # 中英文映射
        self.chinese_to_english = {
            '百度': 'baidu', '谷歌': 'google', '搜狗': 'sogou', '360': '360',
            '微信': 'wechat', 'QQ': 'qq', '微博': 'weibo', '知乎': 'zhihu',
            '淘宝': 'taobao', '天猫': 'tmall', '京东': 'jd', '拼多多': 'pinduoduo',
            '哔哩哔哩': 'bilibili', '爱奇艺': 'iqiyi', '优酷': 'youku', '腾讯视频': 'tencent',
            '抖音': 'douyin', '快手': 'kuaishou', '美团': 'meituan', '饿了么': 'eleme',
            '滴滴': 'didi', '携程': 'ctrip', '人民网': 'people', '新华网': 'xinhua',
            '央视': 'cctv', 'GitHub': 'github', '阿里云': 'aliyun', '腾讯云': 'tencentcloud',
            '华为云': 'huawei', 'AWS': 'aws', '网易云音乐': 'netease', 'QQ音乐': 'qqmusic',
            '酷狗': 'kugou', '政府': 'gov', '中国银行': 'boc', '工商银行': 'icbc',
            '建设银行': 'ccb', '教育部': 'moe', '华为': 'huawei', '小米': 'xiaomi',
            '苹果': 'apple', '微软': 'microsoft', '亚马逊': 'amazon', 'Facebook': 'facebook',
            'Twitter': 'twitter', 'Instagram': 'instagram', 'LinkedIn': 'linkedin',
            'YouTube': 'youtube', 'Netflix': 'netflix', 'Spotify': 'spotify'
        }

    def _load_official_websites(self):
        """加载官网名录文件"""
        try:
            # 获取当前文件所在目录的上级目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, '..', '..', 'data')
            file_path = os.path.join(data_dir, 'official_websites.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ 成功加载官网名录，包含 {len(data.get('网站名录', {}))} 个分类")
                    return data.get('网站名录', {})
            else:
                print(f"⚠️ 官网名录文件不存在: {file_path}")
                return {}
        except Exception as e:
            print(f"❌ 加载官网名录失败: {e}")
            return {}

    def _search_official_websites(self, query):
        """在官网名录中搜索匹配的网站"""
        if not self.official_websites:
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        print(f"🔍 在官网名录中搜索: '{query}'")
        
        # 遍历所有分类
        for category, websites in self.official_websites.items():
            if isinstance(websites, dict):
                for name, info in websites.items():
                    if isinstance(info, dict) and '官网' in info:
                        # 检查网站名称是否匹配
                        if query_lower in name.lower():
                            results.append({
                                "title": f"{name} - {info.get('描述', '官方网站')}",
                                "url": info['官网'],
                                "description": info.get('描述', ''),
                                "source": "官网名录",
                                "category": category
                            })
                            print(f"    ✅ 匹配到: {name} -> {info['官网']}")
                        # 检查关键词是否匹配
                        elif '关键词' in info:
                            for keyword in info['关键词']:
                                if query_lower in keyword.lower():
                                    results.append({
                                        "title": f"{name} - {info.get('描述', '官方网站')}",
                                        "url": info['官网'],
                                        "description": info.get('描述', ''),
                                        "source": "官网名录",
                                        "category": category
                                    })
                                    print(f"    ✅ 关键词匹配: {keyword} -> {name} -> {info['官网']}")
                                    break
        
        print(f"📊 官网名录搜索完成，找到 {len(results)} 个匹配结果")
        return results

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

    def _parse_baidu_results(self, html_content: str) -> list:
        if not html_content:
            print("❌ Baidu 未收到有效HTML内容，无法解析。")
            return []

        print(f"🔍 Baidu 开始解析HTML内容，长度: {len(html_content)} 字符")
        soup = BeautifulSoup(html_content, 'lxml')
        results = []

        # 百度搜索结果通常在 <div class="result" ...> 或 <div class="c-container" ...> 中
        for item in soup.find_all(class_=re.compile(r'result|c-container')):
            title_tag = item.find('h3')
            if not title_tag:
                continue

            link_tag = title_tag.find('a', href=True)
            if not link_tag or not link_tag.get('href'):
                continue

            title = link_tag.get_text().strip()
            link = link_tag.get('href')

            # 百度链接可能需要进一步解析以获取真实URL
            if "/link?url=" in link:
                try:
                    real_link_match = re.search(r'url=([^&]+)', link)
                    if real_link_match:
                        decoded_url = urllib.parse.unquote(real_link_match.group(1))
                        link = decoded_url
                        print(f"    ➡️ Baidu 重定向链接解析: {link}")
                except Exception as e:
                    print(f"    ⚠️ Baidu 重定向链接解析出错: {e}")
                    pass

            snippet_tag = item.find(class_=re.compile(r'c-abstract|op_exactqa_s_abstract'))
            snippet = snippet_tag.get_text().strip() if snippet_tag else ''

            if link.startswith('http'):
                results.append({"title": title, "link": link, "snippet": snippet, "source": "baidu"})
                print(f"    📄 Baidu 解析到结果: 标题='{title[:50]}...', 链接='{link[:50]}...'")
                if len(results) >= 10:
                    print(f"    🔍 Baidu 达到结果数量限制 (10个)，停止解析。")
                    break
        print(f"📊 Baidu 解析完成，共获得 {len(results)} 个结果。")
        return results

    def _parse_sogou_results(self, html_content: str) -> list:
        if not html_content:
            print("❌ Sogou 未收到有效HTML内容，无法解析。")
            return []

        print(f"🔍 Sogou 开始解析HTML内容，长度: {len(html_content)} 字符")
        soup = BeautifulSoup(html_content, 'lxml')
        results = []

        # 搜狗搜索结果通常在 <div class="results"> 下的 <div> 中
        for item in soup.find_all('div', class_='vrwrap'):
            title_tag = item.find('h3')
            if not title_tag:
                continue
            
            link_tag = title_tag.find('a', href=True)
            if not link_tag or not link_tag.get('href'):
                continue
            
            title = link_tag.get_text().strip()
            link = link_tag.get('href')
            
            # 搜狗链接可能需要进一步解析以获取真实URL
            if "/link?url=" in link:
                try:
                    real_link_match = re.search(r'url=([^&]+)', link)
                    if real_link_match:
                        decoded_url = urllib.parse.unquote(real_link_match.group(1))
                        link = decoded_url
                        print(f"    ➡️ Sogou 重定向链接解析: {link}")
                except Exception as e:
                    print(f"    ⚠️ Sogou 重定向链接解析出错: {e}")
                    pass

            snippet_tag = item.find(class_=re.compile(r'fz-info|abstract'))
            snippet = snippet_tag.get_text().strip() if snippet_tag else ''
            
            if link.startswith('http'):
                results.append({"title": title, "link": link, "snippet": snippet, "source": "sogou"})
                print(f"    📄 Sogou 解析到结果: 标题='{title[:50]}...', 链接='{link[:50]}...'")
                if len(results) >= 10:
                    print(f"    🔍 Sogou 达到结果数量限制 (10个)，停止解析。")
                    break
        print(f"📊 Sogou 解析完成，共获得 {len(results)} 个结果。")
        return results

    def _parse_360_results(self, html_content: str) -> list:
        if not html_content:
            print("❌ 360 未收到有效HTML内容，无法解析。")
            return []

        print(f"🔍 360 开始解析HTML内容，长度: {len(html_content)} 字符")
        soup = BeautifulSoup(html_content, 'lxml')
        results = []

        # 360搜索结果通常在 <li class="res-list"> 中
        for item in soup.find_all('li', class_='res-list'):
            title_tag = item.find('h3')
            if not title_tag:
                continue
            
            link_tag = title_tag.find('a', href=True)
            if not link_tag or not link_tag.get('href'):
                continue
            
            title = link_tag.get_text().strip()
            link = link_tag.get('href')
            
            # 360链接可能需要进一步解析以获取真实URL
            if "/url.php?url=" in link:
                try:
                    real_link_match = re.search(r'url=([^&]+)', link)
                    if real_link_match:
                        decoded_url = urllib.parse.unquote(real_link_match.group(1))
                        link = decoded_url
                        print(f"    ➡️ 360 重定向链接解析: {link}")
                except Exception as e:
                    print(f"    ⚠️ 360 重定向链接解析出错: {e}")
                    pass

            snippet_tag = item.find(class_=re.compile(r'res-desc|mh-desc'))
            snippet = snippet_tag.get_text().strip() if snippet_tag else ''
            
            if link.startswith('http'):
                results.append({"title": title, "link": link, "snippet": snippet, "source": "360"})
                print(f"    📄 360 解析到结果: 标题='{title[:50]}...', 链接='{link[:50]}...'")
                if len(results) >= 10:
                    print(f"    🔍 360 达到结果数量限制 (10个)，停止解析。")
                    break
        print(f"📊 360 解析完成，共获得 {len(results)} 个结果。")
        return results

    def _parse_results(self, html_content: str, engine: str) -> list:
        if not html_content:
            print(f"❌ {engine} 未收到有效HTML内容，无法解析。")
            return []

        if engine == "baidu":
            return self._parse_baidu_results(html_content)
        elif engine == "sogou":
            return self._parse_sogou_results(html_content)
        elif engine == "360":
            return self._parse_360_results(html_content)
        else:
            print(f"⚠️ 未知搜索引擎: {engine}，使用通用解析方法。")
            return self._parse_generic_results(html_content, engine)

    def _parse_generic_results(self, html_content: str, engine: str) -> list:
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'lxml')
        results = []

        # 通用解析方法
        for item in soup.find_all('div'):
            title_tag = item.find('h3') or item.find('h2')
            if not title_tag:
                continue

            link_tag = title_tag.find('a', href=True)
            if not link_tag or not link_tag.get('href'):
                continue

            title = link_tag.get_text().strip()
            link = link_tag.get('href')

            snippet_tag = item.find('span') or item.find('div')
            snippet = snippet_tag.get_text().strip() if snippet_tag else ''

            if link.startswith('http'):
                results.append({"title": title, "link": link, "snippet": snippet, "source": engine})
                if len(results) >= 10:
                    break

        return results

    def _is_official_website(self, url: str, query: str) -> bool:
        """判断是否为官方网站"""
        if not url or not url.startswith('http'):
            return False

        # 检查是否为政府网站
        if '.gov.cn' in url or '.edu.cn' in url:
            return True

        # 检查是否为知名官方网站
        official_domains = [
            'baidu.com', 'google.com', 'sogou.com', 'so.com',
            'weixin.qq.com', 'qq.com', 'weibo.com', 'zhihu.com',
            'taobao.com', 'tmall.com', 'jd.com', 'pinduoduo.com',
            'bilibili.com', 'iqiyi.com', 'youku.com', 'v.qq.com',
            'douyin.com', 'kuaishou.com', 'meituan.com', 'ele.me',
            'didiglobal.com', 'ctrip.com', 'people.com.cn', 'xinhuanet.com',
            'cctv.com', 'github.com', 'stackoverflow.com', 'developer.mozilla.org',
            'aliyun.com', 'tencentcloud.com', 'huaweicloud.com', 'aws.amazon.com',
            'music.163.com', 'music.qq.com', 'kugou.com', 'gov.cn', 'moe.gov.cn',
            'boc.cn', 'icbc.com.cn', 'ccb.com'
        ]

        for domain in official_domains:
            if domain in url:
                return True

        # 检查URL中是否包含查询关键词的英文映射
        query_lower = query.lower()
        for chinese, english in self.chinese_to_english.items():
            if chinese in query_lower and english in url.lower():
                return True

        return False

    async def search(self, query: str, max_results: int = 10) -> dict:
        """执行搜索，优先从官网名录返回，没有的话走实时搜索"""
        print(f"🔍 收到搜索请求: {query}")
        
        # 首先在官网名录中搜索
        official_results = self._search_official_websites(query)
        
        if official_results:
            print(f"✅ 从官网名录找到 {len(official_results)} 个结果，直接返回")
            return {
                "results": official_results[:max_results],
                "total_results": len(official_results),
                "search_time": "0.01s",
                "engines_used": ["官网名录"],
                "engines_count": 1,
                "source": "官网名录"
            }
        
        print(f"⚠️ 官网名录中未找到匹配结果，开始实时搜索...")
        
        # 如果官网名录中没有，则进行实时搜索
        start_time = asyncio.get_event_loop().time()
        
        async with httpx.AsyncClient() as session:
            # 创建搜索任务
            tasks = []
            for engine in self.search_engines.keys():
                task = asyncio.create_task(self._fetch_results(session, engine, query))
                tasks.append((engine, task))
            
            print(f"🚀 并行启动 {len(tasks)} 个搜索引擎任务")
            
            # 等待所有任务完成
            all_results = []
            engines_used = []
            
            for engine, task in tasks:
                try:
                    html_content = await task
                    if html_content:
                        results = self._parse_results(html_content, engine)
                        if results:
                            all_results.extend(results)
                            engines_used.append(engine)
                            print(f"✅ {engine} 获得 {len(results)} 个结果")
                        else:
                            print(f"❌ {engine} 解析结果为空")
                    else:
                        print(f"❌ {engine} 未返回有效内容")
                except Exception as e:
                    print(f"❌ {engine} 处理出错: {e}")
            
            # 合并所有结果
            print(f"📊 原始结果汇总: 共获得 {len(all_results)} 个原始搜索结果")
            
            # 去重
            unique_results_map = {}
            for result in all_results:
                if result['link'] not in unique_results_map:
                    unique_results_map[result['link']] = result
            
            unique_results = list(unique_results_map.values())
            print(f"🔄 去重后剩余 {len(unique_results)} 个结果")
            
            # 排序策略：优先搜狗，其次360，最后百度
            engine_priority = {"sogou": 1, "360": 2, "baidu": 3}
            sorted_results = sorted(unique_results, key=lambda x: engine_priority.get(x.get("source", "unknown"), 99))
            print(f"🔄 按来源优先级排序完成")
            
            # 限制最终结果数量
            final_merged_results = sorted_results[:max_results]
            print(f"🔄 合并排序后剩余 {len(final_merged_results)} 个结果")
            
            # 过滤官方网站
            print(f"🔍 开始过滤官方网站...")
            official_results = []
            processed_urls = set()
            
            for result in final_merged_results:
                if result['link'] in processed_urls:
                    print(f"    ➡️ 忽略重复URL: {result['link']}")
                    continue
                
                print(f"🔍 检查结果 (来源:{result.get('source', '未知')}): 标题='{result.get('title', '')[:50]}...', 链接='{result.get('link', '')[:50]}...'")
                if self._is_official_website(result.get("link"), query):
                    official_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("link", ""),
                        "description": result.get("snippet", ""),
                        "source": result.get("source", "未知搜索引擎")
                    })
                    processed_urls.add(result['link'])
                    print(f"✅ 结果被识别为官方网站")
                    if len(official_results) >= max_results:
                        print(f"    🎯 达到最大结果数量限制 ({max_results}个)，停止过滤。")
                        break
                else:
                    print(f"❌ 结果不是官方网站")
            
            end_time = asyncio.get_event_loop().time()
            search_time = f"{end_time - start_time:.2f}s"
            
            print(f"🎯 官方网站过滤完成: 从 {len(final_merged_results)} 个原始结果中筛选出 {len(official_results)} 个官方网站")
            print(f"🎯 搜索完成，返回 {len(official_results)} 个结果，使用了 {len(engines_used)} 个搜索引擎，耗时 {search_time}")
            
            return {
                "results": official_results,
                "total_results": len(official_results),
                "search_time": search_time,
                "engines_used": engines_used,
                "engines_count": len(engines_used),
                "source": "实时搜索"
            }

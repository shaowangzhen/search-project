"""
官方网站爬虫
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any
import re
from loguru import logger
from ..analyzer.official_website_detector import OfficialWebsiteDetector

class OfficialWebsiteSpider(scrapy.Spider):
    """官方网站爬虫"""
    
    name = 'official_website_spider'
    
    def __init__(self, start_urls=None, max_pages=1000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.max_pages = max_pages
        self.crawled_pages = 0
        self.detector = OfficialWebsiteDetector()
        self.allowed_domains = set()
        
        # 初始化允许的域名
        for url in self.start_urls:
            domain = urlparse(url).netloc
            self.allowed_domains.add(domain)
    
    def start_requests(self):
        """开始爬取请求"""
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'depth': 0}
            )
    
    def parse(self, response):
        """解析页面"""
        if self.crawled_pages >= self.max_pages:
            return
        
        self.crawled_pages += 1
        
        # 检查是否为官方网站
        if not self._is_official_website(response):
            return
        
        # 提取页面信息
        page_data = self._extract_page_data(response)
        
        # 保存页面数据
        yield page_data
        
        # 继续爬取链接
        if response.meta.get('depth', 0) < 2:  # 限制爬取深度
            links = self._extract_links(response)
            for link in links:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse,
                    meta={'depth': response.meta.get('depth', 0) + 1}
                )
    
    def _is_official_website(self, response) -> bool:
        """判断是否为官方网站"""
        try:
            # 提取页面内容
            content = self._extract_text_content(response)
            
            # 提取链接
            links = self._extract_links(response)
            
            # 使用检测器判断
            return self.detector.is_official_website(
                url=response.url,
                content=content,
                links=links
            )
        except Exception as e:
            logger.error(f"Error checking official website: {e}")
            return False
    
    def _extract_page_data(self, response) -> Dict[str, Any]:
        """提取页面数据"""
        try:
            # 提取基本信息
            title = response.css('title::text').get() or ''
            meta_description = response.css('meta[name="description"]::attr(content)').get() or ''
            
            # 提取文本内容
            content = self._extract_text_content(response)
            
            # 提取链接
            links = self._extract_links(response)
            
            # 计算权威性评分
            official_score = self.detector.calculate_official_score(
                url=response.url,
                content=content,
                links=links
            )
            
            # 提取分类信息
            category = self._extract_category(response)
            
            # 提取标签
            tags = self._extract_tags(response)
            
            return {
                'url': response.url,
                'title': title.strip(),
                'meta_description': meta_description.strip(),
                'content': content,
                'domain': urlparse(response.url).netloc,
                'official_score': official_score,
                'category': category,
                'tags': tags,
                'links': links,
                'crawled_at': response.meta.get('crawled_at'),
                'status_code': response.status
            }
            
        except Exception as e:
            logger.error(f"Error extracting page data: {e}")
            return {}
    
    def _extract_text_content(self, response) -> str:
        """提取文本内容"""
        try:
            # 移除脚本和样式标签
            for script in response.css('script'):
                script.extract()
            for style in response.css('style'):
                style.extract()
            
            # 提取文本内容
            text_parts = []
            
            # 提取标题
            for selector in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                for element in response.css(selector):
                    text = element.css('::text').get()
                    if text:
                        text_parts.append(text.strip())
            
            # 提取段落
            for element in response.css('p'):
                text = element.css('::text').get()
                if text and len(text.strip()) > 10:
                    text_parts.append(text.strip())
            
            # 提取列表项
            for element in response.css('li'):
                text = element.css('::text').get()
                if text and len(text.strip()) > 5:
                    text_parts.append(text.strip())
            
            return ' '.join(text_parts)
            
        except Exception as e:
            logger.error(f"Error extracting text content: {e}")
            return ''
    
    def _extract_links(self, response) -> List[str]:
        """提取链接"""
        try:
            links = []
            
            # 提取所有链接
            for link in response.css('a::attr(href)').getall():
                if link:
                    # 转换为绝对URL
                    absolute_url = urljoin(response.url, link)
                    links.append(absolute_url)
            
            return links
            
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
            return []
    
    def _extract_category(self, response) -> str:
        """提取页面分类"""
        try:
            # 基于URL路径判断分类
            path = urlparse(response.url).path.lower()
            
            if '/about' in path or '/aboutus' in path:
                return 'about'
            elif '/contact' in path or '/contactus' in path:
                return 'contact'
            elif '/news' in path or '/news/' in path:
                return 'news'
            elif '/service' in path or '/services' in path:
                return 'service'
            elif '/product' in path or '/products' in path:
                return 'product'
            elif '/help' in path or '/faq' in path:
                return 'help'
            else:
                return 'homepage'
                
        except Exception as e:
            logger.error(f"Error extracting category: {e}")
            return 'unknown'
    
    def _extract_tags(self, response) -> List[str]:
        """提取页面标签"""
        try:
            tags = []
            
            # 提取meta关键词
            meta_keywords = response.css('meta[name="keywords"]::attr(content)').get()
            if meta_keywords:
                tags.extend([tag.strip() for tag in meta_keywords.split(',')])
            
            # 基于内容提取标签
            content = self._extract_text_content(response)
            if content:
                # 简单的关键词提取
                keywords = self._extract_keywords(content)
                tags.extend(keywords)
            
            return list(set(tags))  # 去重
            
        except Exception as e:
            logger.error(f"Error extracting tags: {e}")
            return []
    
    def _extract_keywords(self, content: str) -> List[str]:
        """从内容中提取关键词"""
        try:
            # 简单的关键词提取逻辑
            # 这里可以使用更复杂的NLP技术
            
            # 移除标点符号和数字
            text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\s]', '', content)
            
            # 分词（简单按空格分割）
            words = text.split()
            
            # 过滤长度和频率
            word_freq = {}
            for word in words:
                if len(word) > 2:  # 至少3个字符
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # 返回频率最高的前10个词
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:10]]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

class CrawlerManager:
    """爬虫管理器"""
    
    def __init__(self):
        self.settings = get_project_settings()
    
    def crawl_websites(self, start_urls: List[str], max_pages: int = 1000) -> List[Dict[str, Any]]:
        """
        爬取网站
        
        Args:
            start_urls: 起始URL列表
            max_pages: 最大爬取页面数
            
        Returns:
            List[Dict]: 爬取结果列表
        """
        try:
            # 配置爬虫设置
            self.settings.update({
                'USER_AGENT': 'Official Website Search Engine Bot 1.0',
                'ROBOTSTXT_OBEY': True,
                'DOWNLOAD_DELAY': 1,
                'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
                'CONCURRENT_REQUESTS': 16,
                'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                'AUTOTHROTTLE_ENABLED': True,
                'AUTOTHROTTLE_START_DELAY': 1,
                'AUTOTHROTTLE_MAX_DELAY': 10,
                'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
                'AUTOTHROTTLE_DEBUG': False,
                'COOKIES_ENABLED': False,
                'TELNETCONSOLE_ENABLED': False,
                'FEED_EXPORT_ENCODING': 'utf-8',
            })
            
            # 创建爬虫进程
            process = CrawlerProcess(self.settings)
            
            # 添加爬虫
            process.crawl(
                OfficialWebsiteSpider,
                start_urls=start_urls,
                max_pages=max_pages
            )
            
            # 启动爬虫
            process.start()
            
            logger.info(f"Successfully crawled {len(start_urls)} websites")
            
        except Exception as e:
            logger.error(f"Error crawling websites: {e}")
            raise

if __name__ == "__main__":
    # 示例用法
    start_urls = [
        'https://www.gov.cn',
        'https://www.edu.cn',
        'https://www.org.cn'
    ]
    
    manager = CrawlerManager()
    results = manager.crawl_websites(start_urls, max_pages=100)
    
    for result in results:
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Official Score: {result['official_score']}")
        print(f"Category: {result['category']}")
        print("-" * 50)

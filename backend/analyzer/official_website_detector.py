"""
官方网站识别算法
"""
import re
import requests
from urllib.parse import urlparse
from typing import Dict, List, Tuple
import whois
from datetime import datetime, timedelta
import ssl
import socket
from loguru import logger

class OfficialWebsiteDetector:
    """官方网站识别器"""
    
    def __init__(self):
        # 政府域名后缀
        self.gov_domains = ['.gov.cn', '.gov', '.gov.tw', '.gov.hk']
        
        # 教育域名后缀
        self.edu_domains = ['.edu.cn', '.edu', '.edu.tw', '.edu.hk']
        
        # 组织域名后缀
        self.org_domains = ['.org.cn', '.org', '.org.tw', '.org.hk']
        
        # 商业域名后缀
        self.com_domains = ['.com.cn', '.com', '.com.tw', '.com.hk']
        
        # 权威性关键词
        self.authority_keywords = [
            '官方', '官网', '政府', '教育', '学校', '大学', '学院',
            'official', 'government', 'education', 'university', 'college'
        ]
    
    def calculate_official_score(self, url: str, content: str = "", links: List[str] = None) -> float:
        """
        计算官方网站权威性评分
        
        Args:
            url: 网站URL
            content: 网页内容
            links: 相关链接列表
            
        Returns:
            float: 权威性评分 (0.0-1.0)
        """
        try:
            domain = urlparse(url).netloc.lower()
            
            # 域名权威性评分 (40%)
            domain_score = self._check_domain_authority(domain)
            
            # 内容质量评分 (30%)
            content_score = self._analyze_content_quality(content)
            
            # 链接关系评分 (20%)
            link_score = self._analyze_link_relationships(links or [])
            
            # 技术指标评分 (10%)
            tech_score = self._check_technical_indicators(url)
            
            # 综合评分
            final_score = (
                domain_score * 0.4 +
                content_score * 0.3 +
                link_score * 0.2 +
                tech_score * 0.1
            )
            
            logger.info(f"Official score for {url}: {final_score:.3f}")
            return min(final_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating official score for {url}: {e}")
            return 0.0
    
    def _check_domain_authority(self, domain: str) -> float:
        """检查域名权威性"""
        score = 0.0
        
        # 检查政府域名
        if any(domain.endswith(suffix) for suffix in self.gov_domains):
            score = 1.0
        # 检查教育域名
        elif any(domain.endswith(suffix) for suffix in self.edu_domains):
            score = 0.9
        # 检查组织域名
        elif any(domain.endswith(suffix) for suffix in self.org_domains):
            score = 0.8
        # 检查商业域名
        elif any(domain.endswith(suffix) for suffix in self.com_domains):
            score = 0.7
        else:
            # 检查域名年龄和注册信息
            try:
                domain_info = whois.whois(domain)
                if domain_info.creation_date:
                    if isinstance(domain_info.creation_date, list):
                        creation_date = domain_info.creation_date[0]
                    else:
                        creation_date = domain_info.creation_date
                    
                    # 域名年龄评分
                    age_years = (datetime.now() - creation_date).days / 365
                    if age_years > 10:
                        score = 0.6
                    elif age_years > 5:
                        score = 0.5
                    elif age_years > 2:
                        score = 0.4
                    else:
                        score = 0.3
            except:
                score = 0.2
        
        return score
    
    def _analyze_content_quality(self, content: str) -> float:
        """分析内容质量"""
        if not content:
            return 0.0
        
        score = 0.0
        
        # 文本长度检查
        if len(content) > 1000:
            score += 0.2
        elif len(content) > 500:
            score += 0.1
        
        # 权威性关键词检查
        content_lower = content.lower()
        keyword_count = sum(1 for keyword in self.authority_keywords if keyword in content_lower)
        if keyword_count > 0:
            score += min(keyword_count * 0.1, 0.3)
        
        # 结构化内容检查
        structured_score = self._check_structured_content(content)
        score += structured_score * 0.3
        
        # 语言质量检查
        language_score = self._check_language_quality(content)
        score += language_score * 0.2
        
        return min(score, 1.0)
    
    def _check_structured_content(self, content: str) -> float:
        """检查结构化内容"""
        score = 0.0
        
        # 检查HTML标签
        if '<h1>' in content or '<h2>' in content:
            score += 0.2
        if '<p>' in content:
            score += 0.1
        if '<ul>' in content or '<ol>' in content:
            score += 0.1
        if '<table>' in content:
            score += 0.1
        
        # 检查联系方式
        contact_patterns = [
            r'\d{3,4}-\d{7,8}',  # 电话
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 邮箱
            r'地址[:：]\s*[\u4e00-\u9fa5\d\s]+',  # 地址
        ]
        
        for pattern in contact_patterns:
            if re.search(pattern, content):
                score += 0.1
        
        return min(score, 1.0)
    
    def _check_language_quality(self, content: str) -> float:
        """检查语言质量"""
        if not content:
            return 0.0
        
        # 检查中文字符比例
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', content))
        total_chars = len(content)
        
        if total_chars == 0:
            return 0.0
        
        chinese_ratio = chinese_chars / total_chars
        
        # 中文内容质量更高
        if chinese_ratio > 0.7:
            return 0.8
        elif chinese_ratio > 0.3:
            return 0.6
        else:
            return 0.4
    
    def _analyze_link_relationships(self, links: List[str]) -> float:
        """分析链接关系"""
        if not links:
            return 0.0
        
        score = 0.0
        
        # 检查内部链接比例
        internal_links = 0
        external_links = 0
        
        for link in links:
            if link.startswith('http'):
                external_links += 1
            else:
                internal_links += 1
        
        if internal_links + external_links > 0:
            internal_ratio = internal_links / (internal_links + external_links)
            if internal_ratio > 0.7:
                score += 0.3
            elif internal_ratio > 0.5:
                score += 0.2
        
        # 检查权威网站链接
        authority_domains = [
            'gov.cn', 'edu.cn', 'org.cn', 'gov', 'edu', 'org'
        ]
        
        authority_link_count = 0
        for link in links:
            for domain in authority_domains:
                if domain in link:
                    authority_link_count += 1
                    break
        
        if authority_link_count > 0:
            score += min(authority_link_count * 0.1, 0.4)
        
        return min(score, 1.0)
    
    def _check_technical_indicators(self, url: str) -> float:
        """检查技术指标"""
        score = 0.0
        
        try:
            # 检查HTTPS
            if url.startswith('https://'):
                score += 0.3
            
            # 检查SSL证书
            try:
                parsed_url = urlparse(url)
                context = ssl.create_default_context()
                with socket.create_connection((parsed_url.netloc, 443), timeout=10):
                    with context.wrap_socket(socket.socket(), server_hostname=parsed_url.netloc) as s:
                        cert = s.getpeercert()
                        if cert:
                            score += 0.2
            except:
                pass
            
            # 检查响应时间
            try:
                response = requests.head(url, timeout=10)
                if response.status_code == 200:
                    score += 0.3
                elif response.status_code in [301, 302]:
                    score += 0.2
            except:
                pass
            
            # 检查网站结构
            if '/about' in url or '/contact' in url or '/index' in url:
                score += 0.2
            
        except Exception as e:
            logger.error(f"Error checking technical indicators for {url}: {e}")
        
        return min(score, 1.0)
    
    def is_official_website(self, url: str, content: str = "", links: List[str] = None, threshold: float = 0.6) -> bool:
        """
        判断是否为官方网站
        
        Args:
            url: 网站URL
            content: 网页内容
            links: 相关链接列表
            threshold: 判断阈值
            
        Returns:
            bool: 是否为官方网站
        """
        score = self.calculate_official_score(url, content, links)
        return score >= threshold

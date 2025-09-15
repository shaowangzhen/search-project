"""
网站管理服务
"""
from typing import List, Dict, Any, Optional
import mysql.connector
from mysql.connector import Error
from loguru import logger
import json

class WebsiteService:
    """网站管理服务类"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'search_engine',
            'user': 'root',
            'password': 'rootpassword',
            'charset': 'utf8mb4'
        }
    
    async def health_check(self) -> bool:
        """检查数据库健康状态"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                connection.close()
                return True
        except Error as e:
            logger.error(f"Database health check failed: {e}")
        return False
    
    async def get_websites(
        self, 
        page: int = 1, 
        size: int = 20, 
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取网站列表
        
        Args:
            page: 页码
            size: 每页大小
            category: 分类筛选
            
        Returns:
            List[Dict]: 网站列表
        """
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            
            # 构建查询
            offset = (page - 1) * size
            query = """
                SELECT w.*, 
                       COUNT(p.id) as page_count,
                       MAX(p.last_updated) as last_page_update
                FROM websites w
                LEFT JOIN pages p ON w.id = p.website_id
            """
            
            params = []
            if category:
                query += """
                    JOIN website_categories wc ON w.id = wc.website_id
                    JOIN categories c ON wc.category_id = c.id
                    WHERE c.name = %s
                """
                params.append(category)
            
            query += """
                GROUP BY w.id
                ORDER BY w.official_score DESC, w.created_at DESC
                LIMIT %s OFFSET %s
            """
            params.extend([size, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # 转换数据类型
            for result in results:
                if result['official_score']:
                    result['official_score'] = float(result['official_score'])
                if result['page_rank']:
                    result['page_rank'] = float(result['page_rank'])
            
            cursor.close()
            connection.close()
            
            return results
            
        except Error as e:
            logger.error(f"Error getting websites: {e}")
            return []
    
    async def add_website(self, website_data: Dict[str, Any]) -> int:
        """
        添加新网站
        
        Args:
            website_data: 网站数据
            
        Returns:
            int: 网站ID
        """
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            query = """
                INSERT INTO websites (domain, official_score, status, last_crawled)
                VALUES (%s, %s, %s, %s)
            """
            
            values = (
                website_data['domain'],
                website_data.get('official_score', 0.0),
                website_data.get('status', 'pending'),
                website_data.get('last_crawled')
            )
            
            cursor.execute(query, values)
            website_id = cursor.lastrowid
            
            # 添加分类关联
            if 'categories' in website_data:
                for category_name in website_data['categories']:
                    await self._add_website_category(cursor, website_id, category_name)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Added website: {website_data['domain']} (ID: {website_id})")
            return website_id
            
        except Error as e:
            logger.error(f"Error adding website: {e}")
            raise
    
    async def _add_website_category(self, cursor, website_id: int, category_name: str):
        """添加网站分类关联"""
        try:
            # 获取分类ID
            cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
            result = cursor.fetchone()
            
            if result:
                category_id = result[0]
                # 插入关联
                cursor.execute(
                    "INSERT IGNORE INTO website_categories (website_id, category_id) VALUES (%s, %s)",
                    (website_id, category_id)
                )
        except Error as e:
            logger.error(f"Error adding website category: {e}")
    
    async def update_website(self, website_id: int, website_data: Dict[str, Any]) -> bool:
        """
        更新网站信息
        
        Args:
            website_id: 网站ID
            website_data: 网站数据
            
        Returns:
            bool: 是否成功
        """
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # 构建更新查询
            set_clauses = []
            values = []
            
            for key, value in website_data.items():
                if key in ['domain', 'official_score', 'status', 'last_crawled']:
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
            
            if set_clauses:
                query = f"UPDATE websites SET {', '.join(set_clauses)} WHERE id = %s"
                values.append(website_id)
                
                cursor.execute(query, values)
                connection.commit()
            
            cursor.close()
            connection.close()
            
            logger.info(f"Updated website ID: {website_id}")
            return True
            
        except Error as e:
            logger.error(f"Error updating website: {e}")
            return False
    
    async def delete_website(self, website_id: int) -> bool:
        """
        删除网站
        
        Args:
            website_id: 网站ID
            
        Returns:
            bool: 是否成功
        """
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            cursor.execute("DELETE FROM websites WHERE id = %s", (website_id,))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            logger.info(f"Deleted website ID: {website_id}")
            return True
            
        except Error as e:
            logger.error(f"Error deleting website: {e}")
            return False
    
    async def get_website_by_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        根据域名获取网站信息
        
        Args:
            domain: 域名
            
        Returns:
            Optional[Dict]: 网站信息
        """
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT w.*, 
                       COUNT(p.id) as page_count,
                       MAX(p.last_updated) as last_page_update
                FROM websites w
                LEFT JOIN pages p ON w.id = p.website_id
                WHERE w.domain = %s
                GROUP BY w.id
            """
            
            cursor.execute(query, (domain,))
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return result
            
        except Error as e:
            logger.error(f"Error getting website by domain: {e}")
            return None

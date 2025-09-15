-- 官方网站搜索引擎数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS search_engine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE search_engine;

-- 网站表
CREATE TABLE IF NOT EXISTS websites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    domain VARCHAR(255) NOT NULL UNIQUE,
    official_score DECIMAL(3,2) DEFAULT 0.00,
    last_crawled TIMESTAMP NULL,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_domain (domain),
    INDEX idx_official_score (official_score),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 页面表
CREATE TABLE IF NOT EXISTS pages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    website_id INT NOT NULL,
    url VARCHAR(1000) NOT NULL,
    title VARCHAR(500),
    content LONGTEXT,
    meta_description TEXT,
    last_updated TIMESTAMP NULL,
    page_rank DECIMAL(3,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE,
    INDEX idx_website_id (website_id),
    INDEX idx_url (url(255)),
    INDEX idx_page_rank (page_rank)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 搜索历史表
CREATE TABLE IF NOT EXISTS search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    query VARCHAR(255) NOT NULL,
    user_ip VARCHAR(45),
    results_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_query (query),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 分类表
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认分类
INSERT INTO categories (name, description) VALUES
('government', '政府机构'),
('education', '教育机构'),
('organization', '组织机构'),
('enterprise', '企业官网'),
('news', '新闻媒体'),
('service', '服务机构');

-- 网站分类关联表
CREATE TABLE IF NOT EXISTS website_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    website_id INT NOT NULL,
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE KEY unique_website_category (website_id, category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建视图：网站统计
CREATE VIEW website_stats AS
SELECT 
    w.id,
    w.domain,
    w.official_score,
    w.status,
    COUNT(p.id) as page_count,
    MAX(p.last_updated) as last_page_update,
    w.last_crawled,
    w.created_at
FROM websites w
LEFT JOIN pages p ON w.id = p.website_id
GROUP BY w.id, w.domain, w.official_score, w.status, w.last_crawled, w.created_at;

-- 创建存储过程：更新网站评分
DELIMITER //
CREATE PROCEDURE UpdateWebsiteScore(IN website_id INT)
BEGIN
    DECLARE avg_score DECIMAL(3,2);
    
    SELECT AVG(page_rank) INTO avg_score
    FROM pages 
    WHERE website_id = website_id;
    
    UPDATE websites 
    SET official_score = COALESCE(avg_score, 0.00)
    WHERE id = website_id;
END //
DELIMITER ;

-- 创建触发器：页面更新时自动更新网站评分
DELIMITER //
CREATE TRIGGER update_website_score_after_page_update
AFTER UPDATE ON pages
FOR EACH ROW
BEGIN
    CALL UpdateWebsiteScore(NEW.website_id);
END //
DELIMITER ;

-- 创建触发器：页面插入时自动更新网站评分
DELIMITER //
CREATE TRIGGER update_website_score_after_page_insert
AFTER INSERT ON pages
FOR EACH ROW
BEGIN
    CALL UpdateWebsiteScore(NEW.website_id);
END //
DELIMITER ;

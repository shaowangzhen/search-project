<?php
/**
 * 搜索引擎核心类 - 适配后端API格式
 */

require_once __DIR__ . '/ApiClient.php';

class SearchEngine
{
    private $apiClient;
    private $config;
    
    public function __construct()
    {
        $this->config = require __DIR__ . '/../config/config.php';
        $this->apiClient = new ApiClient(
            $this->config['api']['base_url'],
            $this->config['api']['timeout']
        );
    }
    
    /**
     * 处理搜索请求
     */
    public function handleRequest()
    {
        try {
            // 检查API服务状态
            if (!$this->apiClient->isHealthy()) {
                $this->showError('后端服务暂时不可用，请稍后重试');
                return;
            }
            
            $this->handleSearch();
            
        } catch (Exception $e) {
            error_log('搜索处理错误: ' . $e->getMessage());
            $this->showError('搜索服务暂时不可用，请稍后重试');
        }
    }
    
    /**
     * 处理搜索逻辑
     */
    private function handleSearch()
    {
        $query = trim($_POST['query'] ?? '');
        
        if (empty($query)) {
            $this->showError('请输入搜索关键词');
            return;
        }
        
        // 获取搜索参数
        $page = max(1, (int)($_POST['page'] ?? 1));
        $limit = min(50, max(1, (int)($_POST['limit'] ?? 10)));
        $category = trim($_POST['category'] ?? '');
        
        // 调用API搜索
        $response = $this->apiClient->search($query, $page, $limit, $category);
        
        // 检查API响应格式
        if (isset($response['success']) && !$response['success']) {
            // 处理错误响应格式
            $this->showError($response['error'] ?? '搜索失败');
            return;
        }
        
        // 检查是否有results字段（正常响应格式）
        if (!isset($response['results'])) {
            $this->showError('搜索响应格式错误');
            return;
        }
        
        // 显示搜索结果
        $this->showSearchResults($response['results'], $query, $page, $limit);
    }
    
    /**
     * 显示搜索结果
     */
    private function showSearchResults($results, $query, $page, $limit)
    {
        $totalResults = count($results);
        $hasResults = $totalResults > 0;
        
        ?>
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>搜索结果 - 官网直达</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: "Microsoft YaHei", Arial, sans-serif;
                    background-color: #f0f4f8;
                    color: #2c3e50;
                    line-height: 1.6;
                }
                
                .header {
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    padding: 20px 0;
                    box-shadow: 0 2px 8px rgba(30, 60, 114, 0.2);
                }
                
                .header-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                    display: flex;
                    align-items: center;
                    gap: 20px;
                }
                
                .logo {
                    font-size: 28px;
                    font-weight: bold;
                    color: #ffffff;
                    text-decoration: none;
                }
                
                .search-form {
                    flex: 1;
                    max-width: 600px;
                    display: flex;
                    background: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
                }
                
                .search-input {
                    flex: 1;
                    padding: 12px 16px;
                    border: none;
                    outline: none;
                    font-size: 16px;
                }
                
                .search-btn {
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    cursor: pointer;
                    font-size: 16px;
                }
                
                .main-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                
                .search-info {
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .search-query {
                    font-size: 18px;
                    font-weight: bold;
                    color: #1e3c72;
                    margin-bottom: 10px;
                }
                
                .result-count {
                    color: #7f8c8d;
                    font-size: 14px;
                }
                
                .results {
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .result-item {
                    padding: 20px;
                    border-bottom: 1px solid #ecf0f1;
                    transition: background-color 0.3s ease;
                }
                
                .result-item:hover {
                    background-color: #f8f9fa;
                }
                
                .result-item:last-child {
                    border-bottom: none;
                }
                
                .result-title {
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 8px;
                }
                
                .result-title a {
                    color: #1e3c72;
                    text-decoration: none;
                }
                
                .result-title a:hover {
                    color: #3498db;
                    text-decoration: underline;
                }
                
                .result-url {
                    color: #27ae60;
                    font-size: 14px;
                    margin-bottom: 8px;
                    word-break: break-all;
                }
                
                .result-snippet {
                    color: #2c3e50;
                    font-size: 14px;
                    line-height: 1.5;
                }
                
                .no-results {
                    text-align: center;
                    padding: 40px 20px;
                    color: #7f8c8d;
                }
                
                .no-results h3 {
                    font-size: 24px;
                    margin-bottom: 10px;
                }
                
                .no-results p {
                    font-size: 16px;
                }
                
                .back-link {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: all 0.3s ease;
                }
                
                .back-link:hover {
                    background: linear-gradient(135deg, #2980b9 0%, #1f618d 100%);
                    transform: translateY(-2px);
                }
                
                .error-message {
                    background: #e74c3c;
                    color: white;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="header-content">
                    <a href="/" class="logo">官网直达</a>
                    <form method="POST" class="search-form">
                        <input type="text" name="query" class="search-input" value="<?php echo htmlspecialchars($query); ?>" placeholder="请输入搜索关键词...">
                        <button type="submit" class="search-btn">搜索</button>
                    </form>
                </div>
            </div>
            
            <div class="main-content">
                <div class="search-info">
                    <div class="search-query">搜索: "<?php echo htmlspecialchars($query); ?>"</div>
                    <div class="result-count">找到 <?php echo $totalResults; ?> 个结果</div>
                </div>
                
                <div class="results">
                    <?php if ($hasResults): ?>
                        <?php foreach ($results as $result): ?>
                            <div class="result-item">
                                <div class="result-title">
                                    <a href="<?php echo htmlspecialchars($result['url']); ?>" target="_blank">
                                        <?php echo htmlspecialchars($result['title']); ?>
                                    </a>
                                </div>
                                <div class="result-url"><?php echo htmlspecialchars($result['url']); ?></div>
                                <div class="result-snippet">
                                    <?php 
                                    // 修复：支持 description 和 snippet 两个字段
                                    $snippet = $result['description'] ?? $result['snippet'] ?? '暂无描述';
                                    echo htmlspecialchars($snippet); 
                                    ?>
                                </div>
                            </div>
                        <?php endforeach; ?>
                    <?php else: ?>
                        <div class="no-results">
                            <h3>未找到相关结果</h3>
                            <p>请尝试使用其他关键词或检查拼写</p>
                            <a href="/" class="back-link">返回首页</a>
                        </div>
                    <?php endif; ?>
                </div>
            </div>
        </body>
        </html>
        <?php
    }
    
    /**
     * 显示错误信息
     */
    private function showError($message)
    {
        ?>
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>搜索错误 - 官网直达</title>
            <style>
                body {
                    font-family: "Microsoft YaHei", Arial, sans-serif;
                    background-color: #f0f4f8;
                    color: #2c3e50;
                    padding: 20px;
                }
                .error-message {
                    background: #e74c3c;
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .back-link {
                    display: inline-block;
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="error-message">
                <h2>搜索服务暂时不可用</h2>
                <p><?php echo htmlspecialchars($message); ?></p>
            </div>
            <div style="text-align: center;">
                <a href="/" class="back-link">返回首页</a>
            </div>
        </body>
        </html>
        <?php
    }
}

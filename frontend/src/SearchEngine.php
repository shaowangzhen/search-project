<?php
/**
 * 搜索引擎核心类
 */

class SearchEngine {
    private $apiClient;
    
    public function __construct() {
        $this->apiClient = new ApiClient();
    }
    
    public function handleRequest() {
        $query = trim($_POST['query'] ?? '');
        
        if (empty($query)) {
            $this->showError('请输入搜索关键词');
            return;
        }
        
        // 调用API进行搜索
        $response = $this->apiClient->search($query);
        
        if ($response === false) {
            $this->showError('搜索服务暂时不可用，请稍后重试');
            return;
        }
        
        // 显示搜索结果
        $this->showResults($query, $response);
    }
    
    private function showError($message) {
        $this->showResults('', null, $message);
    }
    
    /**
     * 显示搜索结果
     */
    private function showResults($query, $response, $error = null) {
        $hasResults = false;
        $results = [];
        $totalResults = 0;
        $searchTime = '0.00s';
        $enginesUsed = [];
        
        if ($response && isset($response['results'])) {
            $hasResults = !empty($response['results']);
            $results = $response['results'] ?? [];
            $totalResults = $response['total_results'] ?? 0;
            $searchTime = $response['search_time'] ?? '0.00s';
            $enginesUsed = $response['engines_used'] ?? [];
        }
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
                    line-height: 1.4;
                    font-size: 14px;
                }
                
                /* 头部样式 - 与首页完全一致 */
                .header {
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    border-bottom: 2px solid #1e3c72;
                    padding: 15px 0;
                    box-shadow: 0 2px 8px rgba(30, 60, 114, 0.2);
                }
                
                .header-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 15px;
                    padding: 0 15px;
                }
                
                .logo {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;
                    text-decoration: none;
                    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
                    white-space: nowrap;
                    flex-shrink: 0;
                }
                
                .search-container {
                    flex: 1;
                    max-width: 600px;
                    position: relative;
                }
                
                .search-form {
                    display: flex;
                    background: #ffffff;
                    border: 3px solid #3498db;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
                    transition: all 0.3s ease;
                }
                
                .search-form:focus-within {
                    border-color: #2980b9;
                    box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
                    transform: translateY(-2px);
                }
                
                .search-input {
                    flex: 1;
                    padding: 16px 20px;
                    border: none;
                    outline: none;
                    font-size: 18px;
                    color: #2c3e50;
                    background: transparent;
                }
                
                .search-input::placeholder {
                    color: #95a5a6;
                    font-size: 16px;
                }
                
                .search-btn {
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    color: white;
                    border: none;
                    padding: 16px 30px;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    min-width: 100px;
                }
                
                .search-btn:hover {
                    background: linear-gradient(135deg, #2980b9 0%, #1f618d 100%);
                    transform: translateY(-1px);
                }
                
                .search-btn:active {
                    transform: translateY(0);
                }
                
                /* 响应式设计 - 与首页一致 */
                @media (max-width: 768px) {
                    .header-content {
                        flex-direction: column;
                        gap: 15px;
                    }
                    
                    .logo {
                        font-size: 28px;
                    }
                    
                    .search-container {
                        width: 100%;
                        max-width: none;
                    }
                    
                    .search-form {
                        flex-direction: column;
                    }
                    
                    .search-input {
                        padding: 12px 15px;
                        font-size: 16px;
                    }
                    
                    .search-btn {
                        padding: 12px 20px;
                        font-size: 16px;
                        min-width: auto;
                    }
                }
                
                .main-content {
                    max-width: 1200px;
                    margin: 20px auto;
                    padding: 0 15px;
                }
                
                .search-info {
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 10px;
                }
                
                .search-query {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2c3e50;
                }
                
                .result-count {
                    color: #7f8c8d;
                    font-size: 14px;
                }
                
                .search-stats {
                    display: flex;
                    gap: 20px;
                    font-size: 12px;
                    color: #95a5a6;
                }
                
                .stat-item {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }
                
                .stat-icon {
                    width: 16px;
                    height: 16px;
                    background: #3498db;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 10px;
                }
                
                .results {
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                
                .result-item {
                    padding: 25px;
                    border-bottom: 1px solid #ecf0f1;
                    transition: all 0.3s ease;
                    position: relative;
                }
                
                .result-item:hover {
                    background-color: #f8f9fa;
                    transform: translateX(5px);
                }
                
                .result-item:last-child {
                    border-bottom: none;
                }
                
                .result-title {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    line-height: 1.3;
                }
                
                .result-title a {
                    color: #1e3c72;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    display: block;
                }
                
                .result-title a:hover {
                    color: #3498db;
                    text-decoration: underline;
                    transform: translateY(-1px);
                }
                
                .result-url {
                    color: #27ae60;
                    font-size: 14px;
                    margin-bottom: 10px;
                    word-break: break-all;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                
                .url-icon {
                    width: 16px;
                    height: 16px;
                    background: #27ae60;
                    border-radius: 3px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 10px;
                    flex-shrink: 0;
                }
                
                .result-snippet {
                    color: #2c3e50;
                    font-size: 14px;
                    line-height: 1.6;
                    margin-bottom: 10px;
                }
                
                .result-source {
                    display: inline-block;
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: bold;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                .no-results {
                    text-align: center;
                    padding: 60px 20px;
                    color: #7f8c8d;
                }
                
                .no-results h3 {
                    font-size: 28px;
                    margin-bottom: 15px;
                    color: #95a5a6;
                }
                
                .no-results p {
                    font-size: 16px;
                    margin-bottom: 30px;
                }
                
                .back-link {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 24px;
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 25px;
                    transition: all 0.3s ease;
                    font-weight: bold;
                }
                
                .back-link:hover {
                    background: linear-gradient(135deg, #2980b9 0%, #1f618d 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
                }
                
                .error-message {
                    background: #e74c3c;
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    text-align: center;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <!-- 头部 - 与首页完全一致 -->
            <div class="header">
                <div class="header-content">
                    <a href="/" class="logo">官网直达</a>
                    <div class="search-container">
                        <form method="POST" class="search-form">
                            <input type="text" name="query" class="search-input" 
                                   value="<?php echo htmlspecialchars($query); ?>" 
                                   placeholder="请输入搜索关键词..." required>
                            <button type="submit" class="search-btn">搜索</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="main-content">
                <?php if ($error): ?>
                    <div class="error-message"><?php echo htmlspecialchars($error); ?></div>
                <?php endif; ?>
                
                <div class="search-info">
                    <div>
                        <div class="search-query">搜索: "<?php echo htmlspecialchars($query); ?>"</div>
                        <div class="result-count">找到 <?php echo $totalResults; ?> 个结果</div>
                    </div>
                    <div class="search-stats">
                        <div class="stat-item">
                            <div class="stat-icon">⏱</div>
                            <span><?php echo $searchTime; ?></span>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon">🔍</div>
                            <span><?php echo count($enginesUsed); ?> 个引擎</span>
                        </div>
                        <div class="stat-item">
                            <div class="stat-icon">✅</div>
                            <span><?php echo implode(', ', $enginesUsed); ?></span>
                        </div>
                    </div>
                </div>
                
                <div class="results">
                    <?php if ($hasResults): ?>
                        <?php foreach ($results as $index => $result): ?>
                            <div class="result-item">
                                <div class="result-title">
                                    <a href="<?php echo htmlspecialchars($result['url']); ?>" 
                                       target="_blank" 
                                       rel="noopener noreferrer"
                                       title="点击访问官方网站">
                                        <?php 
                                        $title = $result['title'] ?: '官方网站';
                                        echo htmlspecialchars($title); 
                                        ?>
                                    </a>
                                </div>
                                <div class="result-url">
                                    <div class="url-icon">🔗</div>
                                    <span><?php echo htmlspecialchars($result['url']); ?></span>
                                </div>
                                <div class="result-snippet">
                                    <?php 
                                    $snippet = $result['description'] ?? $result['snippet'] ?? '暂无描述';
                                    echo htmlspecialchars($snippet); 
                                    ?>
                                </div>
                                <?php if (isset($result['source'])): ?>
                                    <div class="result-source"><?php echo htmlspecialchars($result['source']); ?></div>
                                <?php endif; ?>
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
}

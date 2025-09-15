<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($title); ?></title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/realtime.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1 class="logo">
                    <a href="/">官方网站搜索引擎</a>
                    <span class="realtime-badge">实时搜索</span>
                </h1>
                
                <div class="search-container">
                    <form class="search-form" action="/" method="GET">
                        <input type="hidden" name="action" value="search">
                        <div class="search-box">
                            <input 
                                type="text" 
                                name="q" 
                                class="search-input" 
                                value="<?php echo htmlspecialchars($query); ?>"
                                placeholder="搜索官方网站..." 
                                autocomplete="off"
                                required
                            >
                            <button type="submit" class="search-button">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <path d="m21 21-4.35-4.35"></path>
                                </svg>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </header>
        
        <main class="main">
            <div class="search-info">
                <p class="search-stats">
                    找到约 <strong><?php echo number_format($results['total']); ?></strong> 条官方网站结果 
                    <span class="realtime-indicator">
                        <span class="loading-dot"></span>
                        实时搜索
                    </span>
                </p>
            </div>
            
            <div class="search-results">
                <?php if (!empty($results['results'])): ?>
                    <?php foreach ($results['results'] as $result): ?>
                        <div class="result-item realtime-result">
                            <h3 class="result-title">
                                <a href="<?php echo htmlspecialchars($result['url']); ?>" target="_blank">
                                    <?php echo htmlspecialchars($result['title']); ?>
                                </a>
                            </h3>
                            
                            <div class="result-url">
                                <span class="url"><?php echo htmlspecialchars($result['url']); ?></span>
                                <span class="official-badge">官方网站</span>
                                <?php if (!empty($result['source'])): ?>
                                    <span class="source-badge"><?php echo htmlspecialchars($result['source']); ?></span>
                                <?php endif; ?>
                            </div>
                            
                            <div class="result-snippet">
                                <?php echo htmlspecialchars($result['snippet']); ?>
                            </div>
                            
                            <div class="result-meta">
                                <span class="domain"><?php echo htmlspecialchars($result['domain']); ?></span>
                                <span class="score">权威性: <?php echo round($result['official_score'] * 100); ?>%</span>
                                <span class="realtime-tag">实时结果</span>
                            </div>
                        </div>
                    <?php endforeach; ?>
                <?php else: ?>
                    <div class="no-results">
                        <h3>没有找到相关结果</h3>
                        <p>请尝试使用不同的关键词或检查拼写</p>
                        <div class="search-tips">
                            <h4>搜索建议：</h4>
                            <ul>
                                <li>尝试使用更具体的关键词</li>
                                <li>检查拼写是否正确</li>
                                <li>尝试使用同义词</li>
                                <li>使用更通用的关键词</li>
                            </ul>
                        </div>
                    </div>
                <?php endif; ?>
            </div>
            
            <?php if (!empty($results['results']) && $results['total'] > $results['size']): ?>
                <div class="pagination">
                    <?php
                    $currentPage = $results['page'];
                    $totalPages = ceil($results['total'] / $results['size']);
                    $maxPages = 10;
                    
                    $startPage = max(1, $currentPage - 5);
                    $endPage = min($totalPages, $startPage + $maxPages - 1);
                    ?>
                    
                    <?php if ($currentPage > 1): ?>
                        <a href="?action=search&q=<?php echo urlencode($query); ?>&page=<?php echo $currentPage - 1; ?>" class="page-link">上一页</a>
                    <?php endif; ?>
                    
                    <?php for ($i = $startPage; $i <= $endPage; $i++): ?>
                        <a href="?action=search&q=<?php echo urlencode($query); ?>&page=<?php echo $i; ?>" 
                           class="page-link <?php echo $i == $currentPage ? 'active' : ''; ?>">
                            <?php echo $i; ?>
                        </a>
                    <?php endfor; ?>
                    
                    <?php if ($currentPage < $totalPages): ?>
                        <a href="?action=search&q=<?php echo urlencode($query); ?>&page=<?php echo $currentPage + 1; ?>" class="page-link">下一页</a>
                    <?php endif; ?>
                </div>
            <?php endif; ?>
            
            <!-- 搜索引擎信息 -->
            <div class="search-engines-info">
                <h4>搜索来源</h4>
                <div class="engines-list">
                    <span class="engine-item">Google</span>
                    <span class="engine-item">Bing</span>
                    <span class="engine-item">DuckDuckGo</span>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            <p>&copy; 2024 官方网站搜索引擎. 专注于提供纯净的实时搜索体验.</p>
        </footer>
    </div>
    
    <script src="/assets/js/app.js"></script>
    <script src="/assets/js/realtime.js"></script>
</body>
</html>

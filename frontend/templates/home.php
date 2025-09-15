<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($title); ?></title>
    <meta name="description" content="<?php echo htmlspecialchars($description); ?>">
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="logo">官方网站搜索引擎</h1>
            <p class="tagline">专注于官方网站检索的纯净搜索引擎</p>
        </header>
        
        <main class="main">
            <div class="search-container">
                <form class="search-form" action="/" method="GET">
                    <input type="hidden" name="action" value="search">
                    <div class="search-box">
                        <input 
                            type="text" 
                            name="q" 
                            class="search-input" 
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
                
                <div class="search-suggestions" id="suggestions" style="display: none;">
                    <!-- 搜索建议将在这里显示 -->
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎯</div>
                    <h3>专注官方网站</h3>
                    <p>只索引和展示官方网站内容，确保信息权威性</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🚫</div>
                    <h3>无广告干扰</h3>
                    <p>纯净的搜索体验，没有商业广告干扰</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🤖</div>
                    <h3>AI智能分析</h3>
                    <p>利用AI技术进行内容分析和权威性验证</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <h3>高性能搜索</h3>
                    <p>快速响应和准确结果，提升搜索效率</p>
                </div>
            </div>
        </main>
        
        <footer class="footer">
            <p>&copy; 2024 官方网站搜索引擎. 专注于提供纯净的搜索体验.</p>
        </footer>
    </div>
    
    <script src="/assets/js/app.js"></script>
</body>
</html>

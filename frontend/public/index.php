<?php
/**
 * 官方网站搜索引擎 - hao123风格首页
 */

// 设置错误报告
error_reporting(E_ALL);
ini_set('display_errors', 1);

// 设置时区
date_default_timezone_set('Asia/Shanghai');

// 引入配置
require_once __DIR__ . '/../config/config.php';

// 引入核心类
require_once __DIR__ . '/../src/SearchEngine.php';
require_once __DIR__ . '/../src/ApiClient.php';

// 初始化搜索引擎
$searchEngine = new SearchEngine();

// 处理搜索请求
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['query'])) {
    $searchEngine->handleRequest();
    exit;
}
?>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>官方网站搜索引擎 - 专业搜索官方网站</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: "Microsoft YaHei", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 48px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 18px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 30px;
        }
        
        .search-container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 40px;
        }
        
        .search-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .search-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .search-input:focus {
            border-color: #667eea;
        }
        
        .search-btn {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .search-btn:hover {
            transform: translateY(-2px);
        }
        
        .search-tips {
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        
        .links-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .link-section {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .section-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .link-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
        }
        
        .link-item {
            display: block;
            padding: 10px;
            text-decoration: none;
            color: #333;
            border-radius: 5px;
            transition: all 0.3s;
            text-align: center;
        }
        
        .link-item:hover {
            background: #f0f0f0;
            transform: translateY(-2px);
        }
        
        .link-name {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .link-desc {
            font-size: 12px;
            color: #666;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: rgba(255,255,255,0.8);
        }
        
        .feature-list {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 8px;
            color: rgba(255,255,255,0.9);
            font-size: 14px;
        }
        
        .feature-icon {
            width: 20px;
            height: 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .search-form {
                flex-direction: column;
            }
            
            .links-container {
                grid-template-columns: 1fr;
            }
            
            .feature-list {
                flex-direction: column;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🔍 官方网站搜索引擎</div>
            <div class="subtitle">专业搜索官方网站，过滤广告和推广内容</div>
            
            <div class="feature-list">
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span>实时搜索</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span>AI识别</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span>过滤广告</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span>权威评分</span>
                </div>
            </div>
        </div>
        
        <div class="search-container">
            <form method="POST" class="search-form">
                <input type="text" name="query" class="search-input" placeholder="请输入搜索关键词，如：Python官网、MySQL官方文档..." required>
                <button type="submit" class="search-btn">搜索官方网站</button>
            </form>
            <div class="search-tips">
                💡 提示：我们专门搜索官方网站，自动过滤广告和推广内容
            </div>
        </div>
        
        <div class="links-container">
            <div class="link-section">
                <div class="section-title">🛠️ 开发工具</div>
                <div class="link-grid">
                    <a href="https://www.python.org" class="link-item" target="_blank">
                        <div class="link-name">Python</div>
                        <div class="link-desc">编程语言</div>
                    </a>
                    <a href="https://nodejs.org" class="link-item" target="_blank">
                        <div class="link-name">Node.js</div>
                        <div class="link-desc">JavaScript运行时</div>
                    </a>
                    <a href="https://www.mysql.com" class="link-item" target="_blank">
                        <div class="link-name">MySQL</div>
                        <div class="link-desc">数据库</div>
                    </a>
                    <a href="https://www.postgresql.org" class="link-item" target="_blank">
                        <div class="link-name">PostgreSQL</div>
                        <div class="link-desc">数据库</div>
                    </a>
                    <a href="https://redis.io" class="link-item" target="_blank">
                        <div class="link-name">Redis</div>
                        <div class="link-desc">缓存数据库</div>
                    </a>
                    <a href="https://www.docker.com" class="link-item" target="_blank">
                        <div class="link-name">Docker</div>
                        <div class="link-desc">容器化</div>
                    </a>
                    <a href="https://git-scm.com" class="link-item" target="_blank">
                        <div class="link-name">Git</div>
                        <div class="link-desc">版本控制</div>
                    </a>
                    <a href="https://github.com" class="link-item" target="_blank">
                        <div class="link-name">GitHub</div>
                        <div class="link-desc">代码托管</div>
                    </a>
                </div>
            </div>
            
            <div class="link-section">
                <div class="section-title">🌐 前端框架</div>
                <div class="link-grid">
                    <a href="https://reactjs.org" class="link-item" target="_blank">
                        <div class="link-name">React</div>
                        <div class="link-desc">前端框架</div>
                    </a>
                    <a href="https://vuejs.org" class="link-item" target="_blank">
                        <div class="link-name">Vue.js</div>
                        <div class="link-desc">前端框架</div>
                    </a>
                    <a href="https://angular.io" class="link-item" target="_blank">
                        <div class="link-name">Angular</div>
                        <div class="link-desc">前端框架</div>
                    </a>
                    <a href="https://getbootstrap.com" class="link-item" target="_blank">
                        <div class="link-name">Bootstrap</div>
                        <div class="link-desc">CSS框架</div>
                    </a>
                    <a href="https://tailwindcss.com" class="link-item" target="_blank">
                        <div class="link-name">Tailwind CSS</div>
                        <div class="link-desc">CSS框架</div>
                    </a>
                    <a href="https://webpack.js.org" class="link-item" target="_blank">
                        <div class="link-name">Webpack</div>
                        <div class="link-desc">模块打包器</div>
                    </a>
                    <a href="https://vitejs.dev" class="link-item" target="_blank">
                        <div class="link-name">Vite</div>
                        <div class="link-desc">构建工具</div>
                    </a>
                    <a href="https://www.typescriptlang.org" class="link-item" target="_blank">
                        <div class="link-name">TypeScript</div>
                        <div class="link-desc">JavaScript超集</div>
                    </a>
                </div>
            </div>
            
            <div class="link-section">
                <div class="section-title">☁️ 云服务</div>
                <div class="link-grid">
                    <a href="https://aws.amazon.com" class="link-item" target="_blank">
                        <div class="link-name">AWS</div>
                        <div class="link-desc">亚马逊云</div>
                    </a>
                    <a href="https://azure.microsoft.com" class="link-item" target="_blank">
                        <div class="link-name">Azure</div>
                        <div class="link-desc">微软云</div>
                    </a>
                    <a href="https://cloud.google.com" class="link-item" target="_blank">
                        <div class="link-name">Google Cloud</div>
                        <div class="link-desc">谷歌云</div>
                    </a>
                    <a href="https://www.aliyun.com" class="link-item" target="_blank">
                        <div class="link-name">阿里云</div>
                        <div class="link-desc">阿里云服务</div>
                    </a>
                    <a href="https://www.tencentcloud.com" class="link-item" target="_blank">
                        <div class="link-name">腾讯云</div>
                        <div class="link-desc">腾讯云服务</div>
                    </a>
                    <a href="https://vercel.com" class="link-item" target="_blank">
                        <div class="link-name">Vercel</div>
                        <div class="link-desc">前端部署</div>
                    </a>
                    <a href="https://www.netlify.com" class="link-item" target="_blank">
                        <div class="link-name">Netlify</div>
                        <div class="link-desc">静态网站</div>
                    </a>
                    <a href="https://www.heroku.com" class="link-item" target="_blank">
                        <div class="link-name">Heroku</div>
                        <div class="link-desc">应用托管</div>
                    </a>
                </div>
            </div>
            
            <div class="link-section">
                <div class="section-title">📚 学习资源</div>
                <div class="link-grid">
                    <a href="https://developer.mozilla.org" class="link-item" target="_blank">
                        <div class="link-name">MDN</div>
                        <div class="link-desc">Web开发文档</div>
                    </a>
                    <a href="https://stackoverflow.com" class="link-item" target="_blank">
                        <div class="link-name">Stack Overflow</div>
                        <div class="link-desc">编程问答</div>
                    </a>
                    <a href="https://www.w3schools.com" class="link-item" target="_blank">
                        <div class="link-name">W3Schools</div>
                        <div class="link-desc">Web教程</div>
                    </a>
                    <a href="https://www.runoob.com" class="link-item" target="_blank">
                        <div class="link-name">菜鸟教程</div>
                        <div class="link-desc">编程教程</div>
                    </a>
                    <a href="https://www.liaoxuefeng.com" class="link-item" target="_blank">
                        <div class="link-name">廖雪峰</div>
                        <div class="link-desc">Python教程</div>
                    </a>
                    <a href="https://www.ruanyifeng.com" class="link-item" target="_blank">
                        <div class="link-name">阮一峰</div>
                        <div class="link-desc">技术博客</div>
                    </a>
                    <a href="https://www.zhihu.com" class="link-item" target="_blank">
                        <div class="link-name">知乎</div>
                        <div class="link-desc">知识问答</div>
                    </a>
                    <a href="https://www.csdn.net" class="link-item" target="_blank">
                        <div class="link-name">CSDN</div>
                        <div class="link-desc">技术社区</div>
                    </a>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 官方网站搜索引擎 | 专业搜索官方网站，过滤广告和推广内容</p>
        </div>
    </div>
</body>
</html>

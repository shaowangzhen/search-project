<?php
/**
 * 官方网站搜索引擎 - 完全模仿hao123.com
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
            background-color: #f5f5f5;
            color: #333;
        }
        
        .header {
            background: #fff;
            border-bottom: 1px solid #e5e5e5;
            padding: 10px 0;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #ff6600;
            text-decoration: none;
        }
        
        .search-box {
            flex: 1;
            max-width: 600px;
            margin: 0 20px;
            position: relative;
        }
        
        .search-form {
            display: flex;
            background: #fff;
            border: 2px solid #ff6600;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .search-input {
            flex: 1;
            padding: 12px 15px;
            border: none;
            outline: none;
            font-size: 16px;
        }
        
        .search-btn {
            background: #ff6600;
            color: white;
            border: none;
            padding: 12px 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        
        .search-btn:hover {
            background: #e55a00;
        }
        
        .nav-links {
            display: flex;
            gap: 20px;
        }
        
        .nav-links a {
            color: #333;
            text-decoration: none;
            font-size: 14px;
        }
        
        .nav-links a:hover {
            color: #ff6600;
        }
        
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .column {
            background: #fff;
            border-radius: 4px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .column-title {
            font-size: 16px;
            font-weight: bold;
            color: #ff6600;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #ff6600;
        }
        
        .link-list {
            list-style: none;
        }
        
        .link-list li {
            margin-bottom: 8px;
        }
        
        .link-list a {
            color: #333;
            text-decoration: none;
            font-size: 14px;
            display: block;
            padding: 3px 0;
        }
        
        .link-list a:hover {
            color: #ff6600;
        }
        
        .hot-links {
            background: #fff;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .hot-title {
            font-size: 18px;
            font-weight: bold;
            color: #ff6600;
            margin-bottom: 15px;
        }
        
        .hot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .hot-item {
            display: flex;
            align-items: center;
            padding: 8px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        .hot-item:hover {
            background: #f5f5f5;
        }
        
        .hot-item a {
            color: #333;
            text-decoration: none;
            font-size: 14px;
            display: flex;
            align-items: center;
            width: 100%;
        }
        
        .hot-item a:hover {
            color: #ff6600;
        }
        
        .hot-icon {
            width: 20px;
            height: 20px;
            margin-right: 8px;
            background: #ff6600;
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }
        
        .footer {
            background: #333;
            color: #999;
            text-align: center;
            padding: 20px;
            margin-top: 30px;
        }
        
        .footer a {
            color: #999;
            text-decoration: none;
        }
        
        .footer a:hover {
            color: #ff6600;
        }
        
        .ad-banner {
            background: #f0f0f0;
            border: 1px solid #ddd;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .ad-text {
            color: #666;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 15px;
            }
            
            .search-box {
                width: 100%;
                margin: 0;
            }
            
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .hot-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <a href="/" class="logo">官方网站搜索引擎</a>
            <div class="search-box">
                <form method="POST" class="search-form">
                    <input type="text" name="query" class="search-input" placeholder="请输入搜索关键词..." required>
                    <button type="submit" class="search-btn">搜索</button>
                </form>
            </div>
            <div class="nav-links">
                <a href="/">首页</a>
                <a href="#tools">开发工具</a>
                <a href="#cloud">云服务</a>
                <a href="#learn">学习资源</a>
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="hot-links">
            <div class="hot-title">🔥 热门官方网站</div>
            <div class="hot-grid">
                <div class="hot-item">
                    <a href="https://www.python.org" target="_blank">
                        <div class="hot-icon">Py</div>
                        <span>Python官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://nodejs.org" target="_blank">
                        <div class="hot-icon">JS</div>
                        <span>Node.js官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://reactjs.org" target="_blank">
                        <div class="hot-icon">R</div>
                        <span>React官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://vuejs.org" target="_blank">
                        <div class="hot-icon">V</div>
                        <span>Vue.js官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://www.mysql.com" target="_blank">
                        <div class="hot-icon">M</div>
                        <span>MySQL官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://www.docker.com" target="_blank">
                        <div class="hot-icon">D</div>
                        <span>Docker官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://github.com" target="_blank">
                        <div class="hot-icon">G</div>
                        <span>GitHub官网</span>
                    </a>
                </div>
                <div class="hot-item">
                    <a href="https://aws.amazon.com" target="_blank">
                        <div class="hot-icon">A</div>
                        <span>AWS官网</span>
                    </a>
                </div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="column" id="tools">
                <div class="column-title">🛠️ 开发工具</div>
                <ul class="link-list">
                    <li><a href="https://www.python.org" target="_blank">Python官网</a></li>
                    <li><a href="https://nodejs.org" target="_blank">Node.js官网</a></li>
                    <li><a href="https://www.mysql.com" target="_blank">MySQL官网</a></li>
                    <li><a href="https://www.postgresql.org" target="_blank">PostgreSQL官网</a></li>
                    <li><a href="https://redis.io" target="_blank">Redis官网</a></li>
                    <li><a href="https://www.docker.com" target="_blank">Docker官网</a></li>
                    <li><a href="https://git-scm.com" target="_blank">Git官网</a></li>
                    <li><a href="https://github.com" target="_blank">GitHub官网</a></li>
                    <li><a href="https://www.jetbrains.com" target="_blank">JetBrains官网</a></li>
                    <li><a href="https://code.visualstudio.com" target="_blank">VS Code官网</a></li>
                </ul>
            </div>
            
            <div class="column" id="cloud">
                <div class="column-title">☁️ 云服务</div>
                <ul class="link-list">
                    <li><a href="https://aws.amazon.com" target="_blank">AWS官网</a></li>
                    <li><a href="https://azure.microsoft.com" target="_blank">Azure官网</a></li>
                    <li><a href="https://cloud.google.com" target="_blank">Google Cloud官网</a></li>
                    <li><a href="https://www.aliyun.com" target="_blank">阿里云官网</a></li>
                    <li><a href="https://www.tencentcloud.com" target="_blank">腾讯云官网</a></li>
                    <li><a href="https://vercel.com" target="_blank">Vercel官网</a></li>
                    <li><a href="https://www.netlify.com" target="_blank">Netlify官网</a></li>
                    <li><a href="https://www.heroku.com" target="_blank">Heroku官网</a></li>
                    <li><a href="https://www.digitalocean.com" target="_blank">DigitalOcean官网</a></li>
                    <li><a href="https://www.linode.com" target="_blank">Linode官网</a></li>
                </ul>
            </div>
            
            <div class="column" id="learn">
                <div class="column-title">📚 学习资源</div>
                <ul class="link-list">
                    <li><a href="https://developer.mozilla.org" target="_blank">MDN官网</a></li>
                    <li><a href="https://stackoverflow.com" target="_blank">Stack Overflow官网</a></li>
                    <li><a href="https://www.w3schools.com" target="_blank">W3Schools官网</a></li>
                    <li><a href="https://www.runoob.com" target="_blank">菜鸟教程官网</a></li>
                    <li><a href="https://www.liaoxuefeng.com" target="_blank">廖雪峰官网</a></li>
                    <li><a href="https://www.ruanyifeng.com" target="_blank">阮一峰官网</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎官网</a></li>
                    <li><a href="https://www.csdn.net" target="_blank">CSDN官网</a></li>
                    <li><a href="https://www.jianshu.com" target="_blank">简书官网</a></li>
                    <li><a href="https://www.segmentfault.com" target="_blank">SegmentFault官网</a></li>
                </ul>
            </div>
        </div>
        
        <div class="ad-banner">
            <div class="ad-text">💡 提示：我们专门搜索官方网站，自动过滤广告和推广内容，为您提供最权威的搜索结果</div>
        </div>
    </div>
    
    <div class="footer">
        <p>© 2024 官方网站搜索引擎 | 专业搜索官方网站，过滤广告和推广内容 | 
        <a href="http://localhost:8000/docs" target="_blank">API文档</a> | 
        <a href="http://localhost:8000/health" target="_blank">服务状态</a></p>
    </div>
</body>
</html>

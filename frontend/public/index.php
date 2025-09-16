<?php
/**
 * 官方网站搜索引擎 - 完全模仿hao123.com
 */

// 设置错误报告
error_reporting(E_ALL);
ini_set('display_errors', 1);

// 设置时区
date_default_timezone_set('Asia/Shanghai');

// 处理搜索请求
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['query'])) {
    require_once '../src/SearchEngine.php';
    $searchEngine = new SearchEngine();
    $searchEngine->handleRequest();
    exit;
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>官网直达 - 专业直达官方网站</title>
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
        
        /* 头部样式 - 与搜索结果页完全一致 */
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
        
        /* 导航栏 - 优化高度和间距 */
        .nav-section {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            border-bottom: 1px solid #1e3c72;
            padding: 8px 0; /* 减少内边距 */
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 15px;
        }
        
        .nav-links {
            display: flex;
            justify-content: center;
            gap: 12px; /* 减少间距 */
            flex-wrap: wrap;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            gap: 6px; /* 减少图标和文字间距 */
            padding: 8px 16px; /* 减少内边距 */
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            text-decoration: none;
            border-radius: 20px;
            transition: all 0.3s ease;
            font-size: 14px; /* 减小字体 */
            font-weight: 500;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .nav-link:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        .nav-link.active {
            background: rgba(255, 255, 255, 0.3);
            border-color: #3498db;
        }
        
        .nav-icon {
            width: 18px; /* 减小图标尺寸 */
            height: 18px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            flex-shrink: 0;
        }
        
        .main-content {
            max-width: 1200px;
            margin: 15px auto; /* 减少顶部间距 */
            padding: 0 15px;
        }
        
        .hot-links {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 8px;
            padding: 15px; /* 减少内边距 */
            margin-bottom: 12px; /* 减少底部间距 */
            box-shadow: 0 4px 12px rgba(30, 60, 114, 0.1);
            border: 1px solid #e3f2fd;
        }
        
        .hot-title {
            font-size: 18px; /* 减小标题字体 */
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 12px; /* 减少底部间距 */
            text-shadow: 0 1px 2px rgba(30, 60, 114, 0.1);
        }
        
        .hot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); /* 减小最小宽度 */
            gap: 6px; /* 减少间距 */
        }
        
        .hot-item {
            display: flex;
            align-items: center;
            padding: 6px 8px; /* 减少内边距 */
            border-radius: 6px;
            transition: all 0.3s ease;
            background: #ffffff;
            border: 1px solid #e3f2fd;
        }
        
        .hot-item:hover {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(30, 60, 114, 0.2);
        }
        
        .hot-item a {
            color: #2c3e50;
            text-decoration: none;
            font-size: 13px; /* 减小字体 */
            display: flex;
            align-items: center;
            width: 100%;
        }
        
        .hot-item a:hover {
            color: #1e3c72;
        }
        
        .hot-icon {
            width: 18px; /* 减小图标尺寸 */
            height: 18px;
            margin-right: 6px; /* 减少右边距 */
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px; /* 减小字体 */
            font-weight: bold;
            flex-shrink: 0;
        }
        
        /* 内容网格 - 自适应列数 */
        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* 自适应列数 */
            gap: 10px; /* 减少间距 */
            margin-bottom: 12px; /* 减少底部间距 */
        }
        
        .column {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 8px;
            padding: 12px; /* 减少内边距 */
            box-shadow: 0 4px 12px rgba(30, 60, 114, 0.1);
            border: 1px solid #e3f2fd;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .column.highlight {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border: 2px solid #3498db;
            box-shadow: 0 8px 24px rgba(52, 152, 219, 0.3);
            transform: translateY(-4px);
        }
        
        .column.highlight::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            border-radius: 10px;
            z-index: -1;
        }
        
        .column-title {
            font-size: 16px; /* 减小标题字体 */
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 10px; /* 减少底部间距 */
            display: flex;
            align-items: center;
            gap: 8px;
            text-shadow: 0 1px 2px rgba(30, 60, 114, 0.1);
        }
        
        .link-list {
            list-style: none;
        }
        
        .link-list li {
            margin-bottom: 6px; /* 减少间距 */
        }
        
        .link-list a {
            color: #2c3e50;
            text-decoration: none;
            font-size: 13px; /* 减小字体 */
            display: block;
            padding: 4px 0; /* 减少内边距 */
            transition: all 0.3s ease;
            border-radius: 4px;
        }
        
        .link-list a:hover {
            color: #1e3c72;
            background-color: #e3f2fd;
            padding-left: 8px;
            transform: translateX(2px);
        }
        
        .ad-banner {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border: 1px solid #90caf9;
            border-radius: 8px;
            padding: 12px; /* 减少内边距 */
            margin: 15px 0; /* 减少上下间距 */
            text-align: center;
            box-shadow: 0 2px 8px rgba(30, 60, 114, 0.1);
        }
        
        .ad-text {
            color: #1e3c72;
            font-size: 14px; /* 减小字体 */
            font-weight: 500;
        }
        
        .footer {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            text-align: center;
            padding: 15px; /* 减少内边距 */
            margin-top: 20px;
            box-shadow: 0 -2px 8px rgba(30, 60, 114, 0.2);
        }
        
        .footer p {
            margin: 0;
            font-size: 13px; /* 减小字体 */
        }
        
        .footer a {
            color: #bbdefb;
            text-decoration: none;
            margin: 0 5px;
        }
        
        .footer a:hover {
            color: #ffffff;
            text-decoration: underline;
        }
        
        /* 移动端优化 - 与搜索结果页完全一致 */
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
                flex-direction: row;
                min-height: 50px;
            }
            
            .search-input {
                padding: 12px 15px;
                font-size: 16px;
                min-height: 50px;
            }
            
            .search-btn {
                padding: 12px 20px;
                font-size: 16px;
                min-width: 80px;
                flex-shrink: 0;
            }
            
            .nav-section {
                padding: 6px 0; /* 进一步减少导航栏高度 */
            }
            
            .nav-links {
                gap: 8px;
            }
            
            .nav-link {
                padding: 6px 12px;
                font-size: 13px;
            }
            
            .nav-icon {
                width: 16px;
                height: 16px;
                font-size: 9px;
            }
            
            .content-grid {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* 移动端自适应 */
            }
            
            .hot-grid {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 4px;
            }
            
            .hot-item {
                padding: 4px 6px;
            }
            
            .hot-item a {
                font-size: 12px;
            }
            
            .hot-icon {
                width: 16px;
                height: 16px;
                font-size: 10px;
                margin-right: 4px;
            }
        }
        
        @media (max-width: 480px) {
            .logo {
                font-size: 24px;
            }
            
            .search-form {
                min-height: 45px;
            }
            
            .search-input {
                padding: 10px 12px;
                font-size: 16px;
                min-height: 45px;
            }
            
            .search-btn {
                padding: 10px 15px;
                font-size: 14px;
                min-width: 70px;
                flex-shrink: 0;
            }
            
            .nav-section {
                padding: 4px 0; /* 最小导航栏高度 */
            }
            
            .nav-links {
                gap: 6px;
            }
            
            .nav-link {
                padding: 4px 8px;
                font-size: 12px;
            }
            
            .nav-icon {
                width: 14px;
                height: 14px;
                font-size: 8px;
            }
            
            .content-grid {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* 超小屏幕自适应 */
            }
            
            .hot-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 6px;
            }
            
            .hot-item {
                padding: 4px 6px;
            }
            
            .hot-item a {
                font-size: 11px;
            }
            
            .hot-icon {
                width: 14px;
                height: 14px;
                font-size: 9px;
                margin-right: 3px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <a href="/" class="logo">官网直达</a>
            <div class="search-container">
                <form method="POST" class="search-form">
                    <input type="text" name="query" class="search-input" placeholder="请输入搜索关键词..." required>
                    <button type="submit" class="search-btn">搜索</button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="nav-section">
        <div class="nav-content">
            <div class="nav-links">
                <a href="#news" class="nav-link" data-target="news">
                    <div class="nav-icon">📰</div>
                    <span>新闻资讯</span>
                </a>
                <a href="#shopping" class="nav-link" data-target="shopping">
                    <div class="nav-icon">🛒</div>
                    <span>购物网站</span>
                </a>
                <a href="#entertainment" class="nav-link" data-target="entertainment">
                    <div class="nav-icon">🎬</div>
                    <span>娱乐休闲</span>
                </a>
                <a href="#life" class="nav-link" data-target="life">
                    <div class="nav-icon">💼</div>
                    <span>生活服务</span>
                </a>
                <a href="#development" class="nav-link" data-target="development">
                    <div class="nav-icon">💻</div>
                    <span>开发工具</span>
                </a>
                <a href="#cloud" class="nav-link" data-target="cloud">
                    <div class="nav-icon">☁️</div>
                    <span>云服务</span>
                </a>
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="hot-links">
            <div class="hot-title">🔥 热门网站</div>
            <div class="hot-grid">
                <div class="hot-item">
                    <div class="hot-icon">百</div>
                    <a href="https://www.baidu.com" target="_blank">百度</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">微</div>
                    <a href="https://www.weibo.com" target="_blank">微博</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">淘</div>
                    <a href="https://www.taobao.com" target="_blank">淘宝</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">京</div>
                    <a href="https://www.jd.com" target="_blank">京东</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">腾</div>
                    <a href="https://www.qq.com" target="_blank">腾讯</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">支</div>
                    <a href="https://www.alipay.com" target="_blank">支付宝</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">抖</div>
                    <a href="https://www.douyin.com" target="_blank">抖音</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">知</div>
                    <a href="https://www.zhihu.com" target="_blank">知乎</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">B</div>
                    <a href="https://www.bilibili.com" target="_blank">B站</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">小</div>
                    <a href="https://www.xiaohongshu.com" target="_blank">小红书</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">美</div>
                    <a href="https://www.meituan.com" target="_blank">美团</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">饿</div>
                    <a href="https://www.ele.me" target="_blank">饿了么</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">滴</div>
                    <a href="https://www.didiglobal.com" target="_blank">滴滴</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">携</div>
                    <a href="https://www.ctrip.com" target="_blank">携程</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">爱</div>
                    <a href="https://www.iqiyi.com" target="_blank">爱奇艺</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">优</div>
                    <a href="https://www.youku.com" target="_blank">优酷</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">网</div>
                    <a href="https://www.163.com" target="_blank">网易</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">搜</div>
                    <a href="https://www.sogou.com" target="_blank">搜狗</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">3</div>
                    <a href="https://www.so.com" target="_blank">360</a>
                </div>
                <div class="hot-item">
                    <div class="hot-icon">头</div>
                    <a href="https://www.toutiao.com" target="_blank">今日头条</a>
                </div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="column" id="news">
                <div class="column-title">
                    <span>📰</span>
                    <span>新闻资讯</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.people.com.cn" target="_blank">人民网</a></li>
                    <li><a href="https://www.xinhuanet.com" target="_blank">新华网</a></li>
                    <li><a href="https://www.cctv.com" target="_blank">央视网</a></li>
                    <li><a href="https://www.chinanews.com" target="_blank">中国新闻网</a></li>
                    <li><a href="https://www.ce.cn" target="_blank">中国经济网</a></li>
                    <li><a href="https://www.gmw.cn" target="_blank">光明网</a></li>
                    <li><a href="https://www.news.cn" target="_blank">新华网</a></li>
                    <li><a href="https://www.cri.cn" target="_blank">国际在线</a></li>
                    <li><a href="https://www.china.com.cn" target="_blank">中国网</a></li>
                    <li><a href="https://www.ifeng.com" target="_blank">凤凰网</a></li>
                    <li><a href="https://www.sina.com.cn" target="_blank">新浪网</a></li>
                    <li><a href="https://www.sohu.com" target="_blank">搜狐网</a></li>
                    <li><a href="https://www.163.com" target="_blank">网易新闻</a></li>
                    <li><a href="https://www.qq.com" target="_blank">腾讯新闻</a></li>
                    <li><a href="https://www.toutiao.com" target="_blank">今日头条</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎</a></li>
                    <li><a href="https://www.douban.com" target="_blank">豆瓣</a></li>
                    <li><a href="https://www.huxiu.com" target="_blank">虎嗅网</a></li>
                    <li><a href="https://www.36kr.com" target="_blank">36氪</a></li>
                    <li><a href="https://www.pingwest.com" target="_blank">PingWest</a></li>
                </ul>
            </div>
            
            <div class="column" id="shopping">
                <div class="column-title">
                    <span>🛒</span>
                    <span>购物网站</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.taobao.com" target="_blank">淘宝网</a></li>
                    <li><a href="https://www.tmall.com" target="_blank">天猫</a></li>
                    <li><a href="https://www.jd.com" target="_blank">京东</a></li>
                    <li><a href="https://www.suning.com" target="_blank">苏宁易购</a></li>
                    <li><a href="https://www.vip.com" target="_blank">唯品会</a></li>
                    <li><a href="https://www.dangdang.com" target="_blank">当当网</a></li>
                    <li><a href="https://www.amazon.cn" target="_blank">亚马逊中国</a></li>
                    <li><a href="https://www.gome.com.cn" target="_blank">国美在线</a></li>
                    <li><a href="https://www.1688.com" target="_blank">1688</a></li>
                    <li><a href="https://www.pinduoduo.com" target="_blank">拼多多</a></li>
                    <li><a href="https://www.xiaohongshu.com" target="_blank">小红书</a></li>
                    <li><a href="https://www.meituan.com" target="_blank">美团</a></li>
                    <li><a href="https://www.ele.me" target="_blank">饿了么</a></li>
                    <li><a href="https://www.dianping.com" target="_blank">大众点评</a></li>
                    <li><a href="https://www.ctrip.com" target="_blank">携程</a></li>
                    <li><a href="https://www.qunar.com" target="_blank">去哪儿</a></li>
                    <li><a href="https://www.fliggy.com" target="_blank">飞猪</a></li>
                    <li><a href="https://www.mafengwo.cn" target="_blank">马蜂窝</a></li>
                    <li><a href="https://www.tuniu.com" target="_blank">途牛</a></li>
                    <li><a href="https://www.lvmama.com" target="_blank">驴妈妈</a></li>
                </ul>
            </div>
            
            <div class="column" id="entertainment">
                <div class="column-title">
                    <span>🎬</span>
                    <span>娱乐休闲</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.bilibili.com" target="_blank">哔哩哔哩</a></li>
                    <li><a href="https://www.iqiyi.com" target="_blank">爱奇艺</a></li>
                    <li><a href="https://www.youku.com" target="_blank">优酷</a></li>
                    <li><a href="https://v.qq.com" target="_blank">腾讯视频</a></li>
                    <li><a href="https://www.mgtv.com" target="_blank">芒果TV</a></li>
                    <li><a href="https://www.douyin.com" target="_blank">抖音</a></li>
                    <li><a href="https://www.kuaishou.com" target="_blank">快手</a></li>
                    <li><a href="https://www.xiaohongshu.com" target="_blank">小红书</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎</a></li>
                    <li><a href="https://www.douban.com" target="_blank">豆瓣</a></li>
                    <li><a href="https://www.weibo.com" target="_blank">微博</a></li>
                    <li><a href="https://www.toutiao.com" target="_blank">今日头条</a></li>
                    <li><a href="https://music.163.com" target="_blank">网易云音乐</a></li>
                    <li><a href="https://music.qq.com" target="_blank">QQ音乐</a></li>
                    <li><a href="https://www.kugou.com" target="_blank">酷狗音乐</a></li>
                    <li><a href="https://www.kuwo.cn" target="_blank">酷我音乐</a></li>
                    <li><a href="https://www.ximalaya.com" target="_blank">喜马拉雅</a></li>
                    <li><a href="https://www.lizhi.fm" target="_blank">荔枝FM</a></li>
                    <li><a href="https://www.huya.com" target="_blank">虎牙直播</a></li>
                    <li><a href="https://www.douyu.com" target="_blank">斗鱼直播</a></li>
                </ul>
            </div>                <ul class="link-list">
                    <li><a href="https://www.bilibili.com" target="_blank">哔哩哔哩</a></li>
                    <li><a href="https://www.iqiyi.com" target="_blank">爱奇艺</a></li>
                    <li><a href="https://www.youku.com" target="_blank">优酷</a></li>
                    <li><a href="https://www.tencent.com" target="_blank">腾讯视频</a></li>
                    <li><a href="https://www.mgtv.com" target="_blank">芒果TV</a></li>
                    <li><a href="https://www.douyin.com" target="_blank">抖音</a></li>
                    <li><a href="https://www.kuaishou.com" target="_blank">快手</a></li>
                    <li><a href="https://www.xiaohongshu.com" target="_blank">小红书</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎</a></li>
                    <li><a href="https://www.douban.com" target="_blank">豆瓣</a></li>
                    <li><a href="https://www.weibo.com" target="_blank">微博</a></li>
                    <li><a href="https://www.toutiao.com" target="_blank">今日头条</a></li>
                    <li><a href="https://www.qq.com" target="_blank">QQ</a></li>
                    <li><a href="https://www.weixin.qq.com" target="_blank">微信</a></li>
                    <li><a href="https://www.dingtalk.com" target="_blank">钉钉</a></li>
                    <li><a href="https://www.taobao.com" target="_blank">淘宝</a></li>
                    <li><a href="https://www.jd.com" target="_blank">京东</a></li>
                    <li><a href="https://www.meituan.com" target="_blank">美团</a></li>
                    <li><a href="https://www.ele.me" target="_blank">饿了么</a></li>
                    <li><a href="https://www.didiglobal.com" target="_blank">滴滴</a></li>
                </ul>
            </div>
            
            <div class="column" id="life">
                <div class="column-title">
                    <span>💼</span>
                    <span>生活服务</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.meituan.com" target="_blank">美团</a></li>
                    <li><a href="https://www.ele.me" target="_blank">饿了么</a></li>
                    <li><a href="https://www.didiglobal.com" target="_blank">滴滴出行</a></li>
                    <li><a href="https://www.ctrip.com" target="_blank">携程</a></li>
                    <li><a href="https://www.qunar.com" target="_blank">去哪儿</a></li>
                    <li><a href="https://www.fliggy.com" target="_blank">飞猪</a></li>
                    <li><a href="https://www.mafengwo.cn" target="_blank">马蜂窝</a></li>
                    <li><a href="https://www.tuniu.com" target="_blank">途牛</a></li>
                    <li><a href="https://www.lvmama.com" target="_blank">驴妈妈</a></li>
                    <li><a href="https://www.airbnb.cn" target="_blank">爱彼迎</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎</a></li>
                    <li><a href="https://www.douban.com" target="_blank">豆瓣</a></li>
                    <li><a href="https://www.xiaohongshu.com" target="_blank">小红书</a></li>
                    <li><a href="https://www.weibo.com" target="_blank">微博</a></li>
                    <li><a href="https://www.toutiao.com" target="_blank">今日头条</a></li>
                    <li><a href="https://www.qq.com" target="_blank">QQ</a></li>
                    <li><a href="https://www.weixin.qq.com" target="_blank">微信</a></li>
                    <li><a href="https://www.dingtalk.com" target="_blank">钉钉</a></li>
                    <li><a href="https://www.taobao.com" target="_blank">淘宝</a></li>
                    <li><a href="https://www.jd.com" target="_blank">京东</a></li>
                </ul>
            </div>
            
            <div class="column" id="development">
                <div class="column-title">
                    <span>💻</span>
                    <span>开发工具</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://github.com" target="_blank">GitHub</a></li>
                    <li><a href="https://gitlab.com" target="_blank">GitLab</a></li>
                    <li><a href="https://stackoverflow.com" target="_blank">Stack Overflow</a></li>
                    <li><a href="https://developer.mozilla.org" target="_blank">MDN</a></li>
                    <li><a href="https://www.w3schools.com" target="_blank">W3Schools</a></li>
                    <li><a href="https://reactjs.org" target="_blank">React官网</a></li>
                    <li><a href="https://vuejs.org" target="_blank">Vue官网</a></li>
                    <li><a href="https://angular.io" target="_blank">Angular官网</a></li>
                    <li><a href="https://getbootstrap.com" target="_blank">Bootstrap官网</a></li>
                    <li><a href="https://www.typescriptlang.org" target="_blank">TypeScript官网</a></li>
                    <li><a href="https://www.php.net" target="_blank">PHP官网</a></li>
                    <li><a href="https://www.java.com" target="_blank">Java官网</a></li>
                    <li><a href="https://golang.org" target="_blank">Go官网</a></li>
                    <li><a href="https://www.rust-lang.org" target="_blank">Rust官网</a></li>
                    <li><a href="https://www.swift.org" target="_blank">Swift官网</a></li>
                    <li><a href="https://www.python.org" target="_blank">Python官网</a></li>
                    <li><a href="https://nodejs.org" target="_blank">Node.js官网</a></li>
                    <li><a href="https://www.mysql.com" target="_blank">MySQL官网</a></li>
                    <li><a href="https://www.postgresql.org" target="_blank">PostgreSQL官网</a></li>
                    <li><a href="https://www.mongodb.com" target="_blank">MongoDB官网</a></li>
                </ul>
            </div>
            
            <div class="column" id="cloud">
                <div class="column-title">
                    <span>☁️</span>
                    <span>云服务</span>
                </div>
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
                    <li><a href="https://www.huaweicloud.com" target="_blank">华为云官网</a></li>
                    <li><a href="https://cloud.baidu.com" target="_blank">百度云官网</a></li>
                    <li><a href="https://www.jdcloud.com" target="_blank">京东云官网</a></li>
                    <li><a href="https://www.volcengine.com" target="_blank">火山引擎官网</a></li>
                    <li><a href="https://www.qingcloud.com" target="_blank">青云官网</a></li>
                    <li><a href="https://www.ucloud.cn" target="_blank">UCloud官网</a></li>
                    <li><a href="https://www.qcloud.com" target="_blank">腾讯云官网</a></li>
                    <li><a href="https://www.aliyun.com" target="_blank">阿里云官网</a></li>
                    <li><a href="https://www.huaweicloud.com" target="_blank">华为云官网</a></li>
                    <li><a href="https://www.aws.amazon.com" target="_blank">AWS官网</a></li>
                </ul>
            </div>
        </div>
        
        <div class="ad-banner">
            <div class="ad-text">💡 提示：我们专门直达官方网站，自动过滤广告和推广内容，为您提供最权威的搜索结果</div>
        </div>
    </div>
    
    <div class="footer">
        <p>© 2024 官网直达 | 专业直达官方网站，过滤广告和推广内容 | 
        <a href="http://localhost:8000/docs" target="_blank">API文档</a> | 
        <a href="http://localhost:8000/health" target="_blank">服务状态</a></p>
    </div>

    <script>
        // 导航锚点跳转和高亮功能
        document.addEventListener('DOMContentLoaded', function() {
            const navLinks = document.querySelectorAll('.nav-link');
            const columns = document.querySelectorAll('.column');
            
            // 平滑滚动到目标区域
            function smoothScrollTo(targetId) {
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 100; // 考虑导航栏高度
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
            
            // 高亮目标区域
            function highlightTarget(targetId) {
                // 移除所有高亮
                columns.forEach(column => {
                    column.classList.remove('highlight');
                });
                
                // 添加高亮到目标区域
                const targetColumn = document.getElementById(targetId);
                if (targetColumn) {
                    targetColumn.classList.add('highlight');
                    
                    // 3秒后移除高亮
                    setTimeout(() => {
                        targetColumn.classList.remove('highlight');
                    }, 3000);
                }
            }
            
            // 更新导航栏活动状态
            function updateActiveNav(targetId) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                });
                
                const activeLink = document.querySelector(`[data-target="${targetId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
            
            // 监听导航链接点击
            navLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const targetId = this.getAttribute('data-target');
                    smoothScrollTo(targetId);
                    highlightTarget(targetId);
                    updateActiveNav(targetId);
                });
            });
            
            // 监听滚动，更新导航栏活动状态
            let ticking = false;
            function updateActiveNavOnScroll() {
                if (!ticking) {
                    requestAnimationFrame(() => {
                        const scrollTop = window.pageYOffset;
                        let activeTarget = null;
                        
                        columns.forEach(column => {
                            const rect = column.getBoundingClientRect();
                            if (rect.top <= 150 && rect.bottom >= 150) {
                                activeTarget = column.id;
                            }
                        });
                        
                        if (activeTarget) {
                            updateActiveNav(activeTarget);
                        }
                        
                        ticking = false;
                    });
                    ticking = true;
                }
            }
            
            window.addEventListener('scroll', updateActiveNavOnScroll);
        });
    </script>
</body>
</html>

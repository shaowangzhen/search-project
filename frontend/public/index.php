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
            line-height: 1.3;
            font-size: 14px;
        }
        
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
        
        .nav-section {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            border-bottom: 1px solid #1e3c72;
            padding: 15px 0;
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
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .nav-links a {
            color: #ffffff;
            text-decoration: none;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 10px 18px;
            border-radius: 6px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .nav-links a:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .nav-links a.active {
            background: rgba(255, 255, 255, 0.3);
            border-color: #3498db;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
        }
        
        .nav-icon {
            width: 18px;
            height: 18px;
            background: #3498db;
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 11px;
            font-weight: bold;
        }
        
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 15px;
        }
        
        .hot-links {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(30, 60, 114, 0.1);
            border: 1px solid #e3f2fd;
        }
        
        .hot-title {
            font-size: 20px;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 15px;
            text-shadow: 0 1px 2px rgba(30, 60, 114, 0.1);
        }
        
        .hot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 8px;
        }
        
        .hot-item {
            display: flex;
            align-items: center;
            padding: 8px 10px;
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
            font-size: 14px;
            display: flex;
            align-items: center;
            width: 100%;
        }
        
        .hot-item a:hover {
            color: #1e3c72;
        }
        
        .hot-icon {
            width: 20px;
            height: 20px;
            margin-right: 8px;
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
            margin-bottom: 15px;
        }
        
        .column {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 8px;
            padding: 15px;
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
            background: linear-gradient(45deg, #3498db, #2980b9, #1e3c72, #2a5298);
            border-radius: 10px;
            z-index: -1;
            animation: highlightGlow 2s ease-in-out;
        }
        
        @keyframes highlightGlow {
            0% { opacity: 0; }
            50% { opacity: 0.8; }
            100% { opacity: 0; }
        }
        
        .column-title {
            font-size: 16px;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #3498db;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .column.highlight .column-title {
            color: #1e3c72;
            border-bottom-color: #2980b9;
        }
        
        .link-list {
            list-style: none;
        }
        
        .link-list li {
            margin-bottom: 4px;
        }
        
        .link-list a {
            color: #2c3e50;
            text-decoration: none;
            font-size: 13px;
            display: block;
            padding: 4px 0;
            line-height: 1.4;
            transition: all 0.3s ease;
            border-radius: 3px;
        }
        
        .link-list a:hover {
            color: #1e3c72;
            background: #e3f2fd;
            padding-left: 8px;
        }
        
        .footer {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #bdc3c7;
            text-align: center;
            padding: 20px;
            margin-top: 20px;
            font-size: 13px;
            box-shadow: 0 -2px 8px rgba(30, 60, 114, 0.2);
        }
        
        .footer a {
            color: #bdc3c7;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer a:hover {
            color: #ffffff;
        }
        
        .ad-banner {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border: 1px solid #90caf9;
            padding: 15px;
            text-align: center;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(30, 60, 114, 0.1);
        }
        
        .ad-text {
            color: #1e3c72;
            font-size: 14px;
            font-weight: 500;
        }
        
        @media (max-width: 1024px) {
            .content-grid {
                grid-template-columns: repeat(4, 1fr);
            }
            
            .nav-links {
                gap: 15px;
            }
            
            .search-container {
                max-width: 500px;
            }
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
            }
            
            .search-container {
                max-width: 100%;
                width: 100%;
            }
            
            .search-input {
                font-size: 16px;
                padding: 14px 16px;
            }
            
            .search-btn {
                font-size: 16px;
                padding: 14px 24px;
                min-width: 80px;
            }
            
            .content-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            .hot-grid {
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            }
            
            .nav-links {
                gap: 10px;
                justify-content: flex-start;
            }
            
            .nav-links a {
                padding: 8px 14px;
                font-size: 13px;
            }
        }
        
        @media (max-width: 480px) {
            .logo {
                font-size: 28px;
            }
            
            .search-input {
                font-size: 14px;
                padding: 12px 14px;
            }
            
            .search-btn {
                font-size: 14px;
                padding: 12px 20px;
                min-width: 70px;
            }
            
            .content-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .hot-grid {
                grid-template-columns: 1fr;
            }
            
            .nav-links {
                flex-direction: column;
                align-items: center;
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
                <div class="hot-item"><a href="https://www.baidu.com" target="_blank"><div class="hot-icon">百</div><span>百度</span></a></div>
                <div class="hot-item"><a href="https://www.taobao.com" target="_blank"><div class="hot-icon">淘</div><span>淘宝</span></a></div>
                <div class="hot-item"><a href="https://www.qq.com" target="_blank"><div class="hot-icon">Q</div><span>腾讯</span></a></div>
                <div class="hot-item"><a href="https://www.sina.com.cn" target="_blank"><div class="hot-icon">新</div><span>新浪</span></a></div>
                <div class="hot-item"><a href="https://www.163.com" target="_blank"><div class="hot-icon">网</div><span>网易</span></a></div>
                <div class="hot-item"><a href="https://www.sohu.com" target="_blank"><div class="hot-icon">搜</div><span>搜狐</span></a></div>
                <div class="hot-item"><a href="https://www.youku.com" target="_blank"><div class="hot-icon">优</div><span>优酷</span></a></div>
                <div class="hot-item"><a href="https://www.iqiyi.com" target="_blank"><div class="hot-icon">爱</div><span>爱奇艺</span></a></div>
                <div class="hot-item"><a href="https://www.douban.com" target="_blank"><div class="hot-icon">豆</div><span>豆瓣</span></a></div>
                <div class="hot-item"><a href="https://www.zhihu.com" target="_blank"><div class="hot-icon">知</div><span>知乎</span></a></div>
                <div class="hot-item"><a href="https://www.jd.com" target="_blank"><div class="hot-icon">京</div><span>京东</span></a></div>
                <div class="hot-item"><a href="https://www.tmall.com" target="_blank"><div class="hot-icon">天</div><span>天猫</span></a></div>
                <div class="hot-item"><a href="https://www.weibo.com" target="_blank"><div class="hot-icon">微</div><span>微博</span></a></div>
                <div class="hot-item"><a href="https://www.bilibili.com" target="_blank"><div class="hot-icon">B</div><span>哔哩哔哩</span></a></div>
                <div class="hot-item"><a href="https://www.douyin.com" target="_blank"><div class="hot-icon">抖</div><span>抖音</span></a></div>
                <div class="hot-item"><a href="https://www.kuaishou.com" target="_blank"><div class="hot-icon">快</div><span>快手</span></a></div>
                <div class="hot-item"><a href="https://www.meituan.com" target="_blank"><div class="hot-icon">美</div><span>美团</span></a></div>
                <div class="hot-item"><a href="https://www.dianping.com" target="_blank"><div class="hot-icon">大</div><span>大众点评</span></a></div>
                <div class="hot-item"><a href="https://www.ctrip.com" target="_blank"><div class="hot-icon">携</div><span>携程</span></a></div>
                <div class="hot-item"><a href="https://www.qunar.com" target="_blank"><div class="hot-icon">去</div><span>去哪儿</span></a></div>
                <div class="hot-item"><a href="https://www.58.com" target="_blank"><div class="hot-icon">5</div><span>58同城</span></a></div>
                <div class="hot-item"><a href="https://www.ganji.com" target="_blank"><div class="hot-icon">赶</div><span>赶集网</span></a></div>
                <div class="hot-item"><a href="https://www.12306.cn" target="_blank"><div class="hot-icon">1</div><span>12306</span></a></div>
                <div class="hot-item"><a href="https://www.ifeng.com" target="_blank"><div class="hot-icon">凤</div><span>凤凰网</span></a></div>
                <div class="hot-item"><a href="https://www.people.com.cn" target="_blank"><div class="hot-icon">人</div><span>人民网</span></a></div>
                <div class="hot-item"><a href="https://www.xinhuanet.com" target="_blank"><div class="hot-icon">新</div><span>新华网</span></a></div>
                <div class="hot-item"><a href="https://www.cctv.com" target="_blank"><div class="hot-icon">央</div><span>央视网</span></a></div>
                <div class="hot-item"><a href="https://www.360.cn" target="_blank"><div class="hot-icon">3</div><span>360</span></a></div>
                <div class="hot-item"><a href="https://www.sogou.com" target="_blank"><div class="hot-icon">搜</div><span>搜狗</span></a></div>
                <div class="hot-item"><a href="https://www.hao123.com" target="_blank"><div class="hot-icon">好</div><span>hao123</span></a></div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="column" id="news">
                <div class="column-title">
                    <span>📰</span>
                    <span>新闻资讯</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.baidu.com" target="_blank">百度新闻</a></li>
                    <li><a href="https://www.sina.com.cn" target="_blank">新浪新闻</a></li>
                    <li><a href="https://news.sohu.com" target="_blank">搜狐新闻</a></li>
                    <li><a href="https://news.qq.com" target="_blank">腾讯新闻</a></li>
                    <li><a href="https://www.ifeng.com" target="_blank">凤凰网</a></li>
                    <li><a href="https://www.people.com.cn" target="_blank">人民网</a></li>
                    <li><a href="https://www.xinhuanet.com" target="_blank">新华网</a></li>
                    <li><a href="https://www.cctv.com" target="_blank">央视网</a></li>
                    <li><a href="https://www.huanqiu.com" target="_blank">环球网</a></li>
                    <li><a href="https://www.guancha.cn" target="_blank">观察者网</a></li>
                    <li><a href="https://www.jiemian.com" target="_blank">界面新闻</a></li>
                    <li><a href="https://www.thepaper.cn" target="_blank">澎湃新闻</a></li>
                    <li><a href="https://www.toutiao.com" target="_blank">今日头条</a></li>
                    <li><a href="https://www.163.com" target="_blank">网易新闻</a></li>
                    <li><a href="https://www.zaobao.com" target="_blank">联合早报</a></li>
                    <li><a href="https://www.chinanews.com" target="_blank">中新网</a></li>
                    <li><a href="https://www.china.com.cn" target="_blank">中国网</a></li>
                    <li><a href="https://www.ce.cn" target="_blank">中国经济网</a></li>
                    <li><a href="https://www.21jingji.com" target="_blank">21经济网</a></li>
                    <li><a href="https://www.nbd.com.cn" target="_blank">每日经济新闻</a></li>
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
                    <li><a href="https://www.vip.com" target="_blank">唯品会</a></li>
                    <li><a href="https://www.suning.com" target="_blank">苏宁易购</a></li>
                    <li><a href="https://www.dangdang.com" target="_blank">当当网</a></li>
                    <li><a href="https://www.mogujie.com" target="_blank">蘑菇街</a></li>
                    <li><a href="https://www.gome.com.cn" target="_blank">国美在线</a></li>
                    <li><a href="https://www.1688.com" target="_blank">阿里巴巴</a></li>
                    <li><a href="https://www.xiaomi.com" target="_blank">小米商城</a></li>
                    <li><a href="https://www.huawei.com" target="_blank">华为商城</a></li>
                    <li><a href="https://www.2.taobao.com" target="_blank">闲鱼</a></li>
                    <li><a href="https://www.pinduoduo.com" target="_blank">拼多多</a></li>
                    <li><a href="https://www.youzan.com" target="_blank">有赞</a></li>
                    <li><a href="https://www.kaola.com" target="_blank">网易考拉</a></li>
                    <li><a href="https://www.yhd.com" target="_blank">1号店</a></li>
                    <li><a href="https://www.womai.com" target="_blank">我买网</a></li>
                    <li><a href="https://www.yixun.com" target="_blank">易迅网</a></li>
                    <li><a href="https://www.lashou.com" target="_blank">拉手网</a></li>
                    <li><a href="https://www.meituan.com" target="_blank">美团购物</a></li>
                </ul>
            </div>
            
            <div class="column" id="entertainment">
                <div class="column-title">
                    <span>🎬</span>
                    <span>娱乐休闲</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.iqiyi.com" target="_blank">爱奇艺</a></li>
                    <li><a href="https://v.qq.com" target="_blank">腾讯视频</a></li>
                    <li><a href="https://www.youku.com" target="_blank">优酷</a></li>
                    <li><a href="https://www.bilibili.com" target="_blank">哔哩哔哩</a></li>
                    <li><a href="https://www.mgtv.com" target="_blank">芒果TV</a></li>
                    <li><a href="https://www.douyin.com" target="_blank">抖音</a></li>
                    <li><a href="https://www.kuaishou.com" target="_blank">快手</a></li>
                    <li><a href="https://www.douyu.com" target="_blank">斗鱼</a></li>
                    <li><a href="https://www.huya.com" target="_blank">虎牙</a></li>
                    <li><a href="https://www.yy.com" target="_blank">YY直播</a></li>
                    <li><a href="https://music.163.com" target="_blank">网易云音乐</a></li>
                    <li><a href="https://y.qq.com" target="_blank">QQ音乐</a></li>
                    <li><a href="https://www.kugou.com" target="_blank">酷狗音乐</a></li>
                    <li><a href="https://www.kuwo.cn" target="_blank">酷我音乐</a></li>
                    <li><a href="https://www.douban.com" target="_blank">豆瓣</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎</a></li>
                    <li><a href="https://www.weibo.com" target="_blank">微博</a></li>
                    <li><a href="https://www.toutiao.com" target="_blank">今日头条</a></li>
                    <li><a href="https://www.xiaohongshu.com" target="_blank">小红书</a></li>
                    <li><a href="https://www.zhihu.com" target="_blank">知乎</a></li>
                </ul>
            </div>
            
            <div class="column" id="life">
                <div class="column-title">
                    <span>💼</span>
                    <span>生活服务</span>
                </div>
                <ul class="link-list">
                    <li><a href="https://www.58.com" target="_blank">58同城</a></li>
                    <li><a href="https://www.ganji.com" target="_blank">赶集网</a></li>
                    <li><a href="https://www.baixing.com" target="_blank">百姓网</a></li>
                    <li><a href="https://www.meituan.com" target="_blank">美团</a></li>
                    <li><a href="https://www.dianping.com" target="_blank">大众点评</a></li>
                    <li><a href="https://www.ctrip.com" target="_blank">携程</a></li>
                    <li><a href="https://www.qunar.com" target="_blank">去哪儿</a></li>
                    <li><a href="https://www.mafengwo.cn" target="_blank">马蜂窝</a></li>
                    <li><a href="https://www.tuniu.com" target="_blank">途牛</a></li>
                    <li><a href="https://www.12306.cn" target="_blank">12306</a></li>
                    <li><a href="https://www.ke.com" target="_blank">贝壳找房</a></li>
                    <li><a href="https://www.anjuke.com" target="_blank">安居客</a></li>
                    <li><a href="https://www.fang.com" target="_blank">房天下</a></li>
                    <li><a href="https://www.che168.com" target="_blank">二手车之家</a></li>
                    <li><a href="https://www.autohome.com.cn" target="_blank">汽车之家</a></li>
                    <li><a href="https://www.bitauto.com" target="_blank">易车网</a></li>
                    <li><a href="https://www.pcauto.com.cn" target="_blank">太平洋汽车</a></li>
                    <li><a href="https://www.chexun.com" target="_blank">车讯网</a></li>
                    <li><a href="https://www.51auto.com" target="_blank">51汽车</a></li>
                    <li><a href="https://www.chexiu.com" target="_blank">车秀网</a></li>
                </ul>
            </div>
            
            <div class="column" id="development">
                <div class="column-title">
                    <span>💻</span>
                    <span>开发工具</span>
                </div>
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
                    <li><a href="https://reactjs.org" target="_blank">React官网</a></li>
                    <li><a href="https://vuejs.org" target="_blank">Vue.js官网</a></li>
                    <li><a href="https://angular.io" target="_blank">Angular官网</a></li>
                    <li><a href="https://getbootstrap.com" target="_blank">Bootstrap官网</a></li>
                    <li><a href="https://www.typescriptlang.org" target="_blank">TypeScript官网</a></li>
                    <li><a href="https://www.php.net" target="_blank">PHP官网</a></li>
                    <li><a href="https://www.java.com" target="_blank">Java官网</a></li>
                    <li><a href="https://golang.org" target="_blank">Go官网</a></li>
                    <li><a href="https://www.rust-lang.org" target="_blank">Rust官网</a></li>
                    <li><a href="https://www.swift.org" target="_blank">Swift官网</a></li>
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
            
            // 绑定导航点击事件
            navLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const targetId = this.getAttribute('data-target');
                    
                    // 平滑滚动
                    smoothScrollTo(targetId);
                    
                    // 高亮目标区域
                    highlightTarget(targetId);
                    
                    // 更新导航状态
                    updateActiveNav(targetId);
                });
            });
            
            // 监听滚动事件，更新导航栏活动状态
            let ticking = false;
            function updateNavOnScroll() {
                if (!ticking) {
                    requestAnimationFrame(() => {
                        const scrollTop = window.pageYOffset;
                        const navHeight = document.querySelector('.nav-section').offsetHeight;
                        
                        columns.forEach(column => {
                            const columnTop = column.offsetTop - navHeight - 50;
                            const columnBottom = columnTop + column.offsetHeight;
                            
                            if (scrollTop >= columnTop && scrollTop < columnBottom) {
                                const columnId = column.getAttribute('id');
                                updateActiveNav(columnId);
                            }
                        });
                        
                        ticking = false;
                    });
                    ticking = true;
                }
            }
            
            window.addEventListener('scroll', updateNavOnScroll);
        });
    </script>
</body>
</html>

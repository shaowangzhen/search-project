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
            line-height: 1.2;
            font-size: 12px;
        }
        
        .header {
            background: #fff;
            border-bottom: 1px solid #e5e5e5;
            padding: 5px 0;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 10px;
        }
        
        .logo {
            font-size: 20px;
            font-weight: bold;
            color: #ff6600;
            text-decoration: none;
        }
        
        .search-box {
            flex: 1;
            max-width: 500px;
            margin: 0 15px;
            position: relative;
        }
        
        .search-form {
            display: flex;
            background: #fff;
            border: 2px solid #ff6600;
            border-radius: 3px;
            overflow: hidden;
        }
        
        .search-input {
            flex: 1;
            padding: 8px 12px;
            border: none;
            outline: none;
            font-size: 14px;
        }
        
        .search-btn {
            background: #ff6600;
            color: white;
            border: none;
            padding: 8px 15px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        
        .search-btn:hover {
            background: #e55a00;
        }
        
        .nav-links {
            display: flex;
            gap: 15px;
        }
        
        .nav-links a {
            color: #333;
            text-decoration: none;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .nav-links a:hover {
            color: #ff6600;
        }
        
        .nav-icon {
            width: 16px;
            height: 16px;
            background: #ff6600;
            border-radius: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 10px;
            font-weight: bold;
        }
        
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 10px;
        }
        
        .hot-links {
            background: #fff;
            border-radius: 3px;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .hot-title {
            font-size: 16px;
            font-weight: bold;
            color: #ff6600;
            margin-bottom: 8px;
        }
        
        .hot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 4px;
        }
        
        .hot-item {
            display: flex;
            align-items: center;
            padding: 3px 5px;
            border-radius: 2px;
            transition: background-color 0.2s;
        }
        
        .hot-item:hover {
            background: #f5f5f5;
        }
        
        .hot-item a {
            color: #333;
            text-decoration: none;
            font-size: 12px;
            display: flex;
            align-items: center;
            width: 100%;
        }
        
        .hot-item a:hover {
            color: #ff6600;
        }
        
        .hot-icon {
            width: 16px;
            height: 16px;
            margin-right: 4px;
            background: #ff6600;
            border-radius: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 10px;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            margin-bottom: 10px;
        }
        
        .column {
            background: #fff;
            border-radius: 3px;
            padding: 8px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .column-title {
            font-size: 13px;
            font-weight: bold;
            color: #ff6600;
            margin-bottom: 6px;
            padding-bottom: 3px;
            border-bottom: 1px solid #ff6600;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .link-list {
            list-style: none;
        }
        
        .link-list li {
            margin-bottom: 2px;
        }
        
        .link-list a {
            color: #333;
            text-decoration: none;
            font-size: 11px;
            display: block;
            padding: 1px 0;
            line-height: 1.2;
        }
        
        .link-list a:hover {
            color: #ff6600;
        }
        
        .footer {
            background: #333;
            color: #999;
            text-align: center;
            padding: 10px;
            margin-top: 15px;
            font-size: 11px;
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
            padding: 8px;
            text-align: center;
            margin: 8px 0;
            border-radius: 3px;
        }
        
        .ad-text {
            color: #666;
            font-size: 11px;
        }
        
        @media (max-width: 1024px) {
            .content-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 8px;
            }
            
            .search-box {
                width: 100%;
                margin: 0;
            }
            
            .content-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            .hot-grid {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            }
        }
        
        @media (max-width: 480px) {
            .content-grid {
                grid-template-columns: repeat(2, 1fr);
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
                <a href="/">
                    <div class="nav-icon">🏠</div>
                    <span>首页</span>
                </a>
                <a href="#news">
                    <div class="nav-icon">📰</div>
                    <span>新闻</span>
                </a>
                <a href="#shopping">
                    <div class="nav-icon">��</div>
                    <span>购物</span>
                </a>
                <a href="#entertainment">
                    <div class="nav-icon">��</div>
                    <span>娱乐</span>
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
            
            <div class="column">
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
            
            <div class="column">
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
            
            <div class="column">
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

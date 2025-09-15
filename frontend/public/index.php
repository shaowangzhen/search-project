<?php
/**
 * 官方网站搜索引擎 - 前端入口
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

// 处理请求
$searchEngine->handleRequest();
?>

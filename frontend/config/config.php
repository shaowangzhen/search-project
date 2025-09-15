<?php
/**
 * 配置文件
 */
return [
    'app' => [
        'name' => '官方网站搜索引擎',
        'version' => '1.0.0',
        'debug' => true
    ],
    
    'api' => [
        'base_url' => 'http://localhost:8000',
        'timeout' => 30
    ],
    
    'database' => [
        'host' => 'localhost',
        'port' => 3306,
        'dbname' => 'search_engine',
        'username' => 'root',
        'password' => 'rootpassword',
        'charset' => 'utf8mb4'
    ],
    
    'cache' => [
        'host' => 'localhost',
        'port' => 6379,
        'password' => '',
        'database' => 0
    ],
    
    'search' => [
        'default_page_size' => 10,
        'max_page_size' => 50,
        'suggestion_limit' => 10
    ],
    
    'ui' => [
        'theme' => 'default',
        'items_per_page' => 10,
        'show_ads' => false
    ]
];
?>

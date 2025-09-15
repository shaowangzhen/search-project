<?php
/**
 * 实时搜索配置文件
 */
return [
    'app' => [
        'name' => '官方网站搜索引擎 - 实时搜索版',
        'version' => '2.0.0',
        'debug' => true,
        'search_mode' => 'realtime'  // 实时搜索模式
    ],
    
    'api' => [
        'base_url' => 'http://localhost:8000',
        'timeout' => 60,  // 实时搜索需要更长的超时时间
        'realtime_endpoint' => '/api/v1/search'
    ],
    
    'search' => [
        'default_page_size' => 10,
        'max_page_size' => 50,
        'suggestion_limit' => 10,
        'realtime_timeout' => 30,  // 实时搜索超时时间
        'show_loading' => true,    // 显示加载状态
        'show_sources' => true     // 显示搜索引擎来源
    ],
    
    'ui' => [
        'theme' => 'default',
        'items_per_page' => 10,
        'show_ads' => false,
        'show_realtime_badge' => true,  // 显示实时搜索标识
        'show_search_engines' => true   // 显示搜索引擎信息
    ],
    
    'features' => [
        'realtime_search' => true,     // 启用实时搜索
        'multi_engine' => true,        // 多搜索引擎
        'official_filter' => true,     // 官方网站过滤
        'authority_scoring' => true,   // 权威性评分
        'search_suggestions' => true   // 搜索建议
    ]
];
?>

<?php
/**
 * 搜索引擎主类
 */
class SearchEngine
{
    private $apiClient;
    private $config;
    
    public function __construct()
    {
        $this->config = require __DIR__ . '/../config/config.php';
        $this->apiClient = new ApiClient($this->config['api']['base_url']);
    }
    
    /**
     * 处理请求
     */
    public function handleRequest()
    {
        $action = $_GET['action'] ?? 'search';
        
        switch ($action) {
            case 'search':
                $this->handleSearch();
                break;
            case 'suggest':
                $this->handleSuggest();
                break;
            case 'websites':
                $this->handleWebsites();
                break;
            default:
                $this->showHomePage();
                break;
        }
    }
    
    /**
     * 处理搜索请求
     */
    private function handleSearch()
    {
        $query = $_GET['q'] ?? '';
        $page = (int)($_GET['page'] ?? 1);
        $size = (int)($_GET['size'] ?? 10);
        $category = $_GET['category'] ?? '';
        
        if (empty($query)) {
            $this->showHomePage();
            return;
        }
        
        try {
            // 调用API搜索
            $results = $this->apiClient->search($query, $page, $size, $category);
            
            // 显示搜索结果
            $this->showSearchResults($query, $results);
            
        } catch (Exception $e) {
            $this->showError('搜索失败: ' . $e->getMessage());
        }
    }
    
    /**
     * 处理搜索建议请求
     */
    private function handleSuggest()
    {
        $query = $_GET['q'] ?? '';
        
        if (empty($query)) {
            echo json_encode(['suggestions' => []]);
            return;
        }
        
        try {
            $suggestions = $this->apiClient->getSuggestions($query);
            echo json_encode(['suggestions' => $suggestions]);
            
        } catch (Exception $e) {
            echo json_encode(['suggestions' => []]);
        }
    }
    
    /**
     * 处理网站列表请求
     */
    private function handleWebsites()
    {
        $page = (int)($_GET['page'] ?? 1);
        $size = (int)($_GET['size'] ?? 20);
        $category = $_GET['category'] ?? '';
        
        try {
            $websites = $this->apiClient->getWebsites($page, $size, $category);
            $this->showWebsites($websites);
            
        } catch (Exception $e) {
            $this->showError('获取网站列表失败: ' . $e->getMessage());
        }
    }
    
    /**
     * 显示首页
     */
    private function showHomePage()
    {
        $this->render('home', [
            'title' => '官方网站搜索引擎',
            'description' => '专注于官方网站检索的纯净搜索引擎'
        ]);
    }
    
    /**
     * 显示搜索结果
     */
    private function showSearchResults($query, $results)
    {
        $this->render('search_results', [
            'title' => "搜索结果: {$query}",
            'query' => $query,
            'results' => $results
        ]);
    }
    
    /**
     * 显示网站列表
     */
    private function showWebsites($websites)
    {
        $this->render('websites', [
            'title' => '官方网站列表',
            'websites' => $websites
        ]);
    }
    
    /**
     * 显示错误页面
     */
    private function showError($message)
    {
        $this->render('error', [
            'title' => '错误',
            'message' => $message
        ]);
    }
    
    /**
     * 渲染模板
     */
    private function render($template, $data = [])
    {
        extract($data);
        include __DIR__ . "/../templates/{$template}.php";
    }
}
?>

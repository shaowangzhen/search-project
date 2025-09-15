<?php
/**
 * API客户端类
 */
class ApiClient
{
    private $baseUrl;
    private $timeout;
    
    public function __construct($baseUrl, $timeout = 30)
    {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->timeout = $timeout;
    }
    
    /**
     * 搜索
     */
    public function search($query, $page = 1, $size = 10, $category = '')
    {
        $params = [
            'q' => $query,
            'page' => $page,
            'size' => $size
        ];
        
        if (!empty($category)) {
            $params['category'] = $category;
        }
        
        return $this->post('/api/v1/search', $params);
    }
    
    /**
     * 获取搜索建议
     */
    public function getSuggestions($query, $limit = 10)
    {
        $params = [
            'q' => $query,
            'limit' => $limit
        ];
        
        $response = $this->get('/api/v1/suggest', $params);
        return $response['suggestions'] ?? [];
    }
    
    /**
     * 获取网站列表
     */
    public function getWebsites($page = 1, $size = 20, $category = '')
    {
        $params = [
            'page' => $page,
            'size' => $size
        ];
        
        if (!empty($category)) {
            $params['category'] = $category;
        }
        
        return $this->get('/api/v1/websites', $params);
    }
    
    /**
     * 添加网站
     */
    public function addWebsite($websiteData)
    {
        return $this->post('/api/v1/websites', $websiteData);
    }
    
    /**
     * GET请求
     */
    private function get($endpoint, $params = [])
    {
        $url = $this->baseUrl . $endpoint;
        
        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }
        
        return $this->makeRequest('GET', $url);
    }
    
    /**
     * POST请求
     */
    private function post($endpoint, $data = [])
    {
        $url = $this->baseUrl . $endpoint;
        
        return $this->makeRequest('POST', $url, $data);
    }
    
    /**
     * 发送HTTP请求
     */
    private function makeRequest($method, $url, $data = null)
    {
        $ch = curl_init();
        
        curl_setopt_array($ch, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => $this->timeout,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Accept: application/json'
            ]
        ]);
        
        if ($data && in_array($method, ['POST', 'PUT', 'PATCH'])) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        
        curl_close($ch);
        
        if ($error) {
            throw new Exception("cURL Error: {$error}");
        }
        
        if ($httpCode >= 400) {
            throw new Exception("HTTP Error: {$httpCode}");
        }
        
        $decodedResponse = json_decode($response, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception("JSON Decode Error: " . json_last_error_msg());
        }
        
        return $decodedResponse;
    }
}
?>

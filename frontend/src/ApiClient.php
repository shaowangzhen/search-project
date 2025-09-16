<?php
/**
 * API客户端 - 使用file_get_contents替代curl
 */

class ApiClient
{
    private $baseUrl;
    private $timeout;
    
    public function __construct($baseUrl = 'http://localhost:8000', $timeout = 30)
    {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->timeout = $timeout;
    }
    
    /**
     * 发送GET请求
     */
    public function get($endpoint, $params = [])
    {
        $url = $this->baseUrl . $endpoint;
        if (!empty($params)) {
            $url .= '?' . http_build_query($params);
        }
        
        return $this->makeRequest('GET', $url);
    }
    
    /**
     * 发送POST请求
     */
    public function post($endpoint, $data = [])
    {
        $url = $this->baseUrl . $endpoint;
        return $this->makeRequest('POST', $url, $data);
    }
    
    /**
     * 执行搜索请求
     */
    public function search($query, $page = 1, $limit = 10, $category = '')
    {
        $data = [
            'query' => $query,
            'page' => $page,
            'limit' => $limit,
            'category' => $category
        ];
        
        return $this->post('/api/v1/search', $data);
    }
    
    /**
     * 使用file_get_contents发送HTTP请求
     */
    private function makeRequest($method, $url, $data = null)
    {
        $options = [
            'http' => [
                'method' => $method,
                'header' => [
                    'Content-Type: application/json',
                    'User-Agent: OfficialWebsiteSearch/1.0'
                ],
                'timeout' => $this->timeout,
                'ignore_errors' => true
            ]
        ];
        
        if ($method === 'POST' && $data) {
            $options['http']['content'] = json_encode($data);
        }
        
        $context = stream_context_create($options);
        
        try {
            $response = file_get_contents($url, false, $context);
            
            if ($response === false) {
                throw new Exception('请求失败: ' . error_get_last()['message']);
            }
            
            // 解析HTTP响应头
            $httpCode = $this->getHttpCode($http_response_header ?? []);
            
            if ($httpCode >= 400) {
                throw new Exception('HTTP错误: ' . $httpCode);
            }
            
            $decodedResponse = json_decode($response, true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                throw new Exception('JSON解析错误: ' . json_last_error_msg());
            }
            
            return $decodedResponse;
            
        } catch (Exception $e) {
            error_log('API请求错误: ' . $e->getMessage());
            return [
                'success' => false,
                'error' => '请求失败: ' . $e->getMessage(),
                'data' => []
            ];
        }
    }
    
    /**
     * 从HTTP响应头中提取状态码
     */
    private function getHttpCode($headers)
    {
        if (empty($headers)) {
            return 200;
        }
        
        $statusLine = $headers[0];
        if (preg_match('/HTTP\/\d\.\d\s+(\d+)/', $statusLine, $matches)) {
            return (int)$matches[1];
        }
        
        return 200;
    }
    
    /**
     * 检查API服务是否可用
     */
    public function isHealthy()
    {
        try {
            $response = $this->get('/health');
            return isset($response['status']) && $response['status'] === 'ok';
        } catch (Exception $e) {
            return false;
        }
    }
}

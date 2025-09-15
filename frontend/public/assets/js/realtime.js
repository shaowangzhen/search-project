/**
 * 实时搜索JavaScript功能
 */

class RealtimeSearchEngine extends SearchEngine {
    constructor() {
        super();
        this.isRealtimeMode = true;
        this.searchTimeout = null;
        this.currentSearchId = 0;
    }
    
    init() {
        super.init();
        this.initRealtimeFeatures();
    }
    
    initRealtimeFeatures() {
        // 添加实时搜索指示器
        this.addRealtimeIndicator();
        
        // 添加搜索引擎信息
        this.addSearchEnginesInfo();
        
        // 增强搜索体验
        this.enhanceSearchExperience();
    }
    
    addRealtimeIndicator() {
        const searchStats = document.querySelector('.search-stats');
        if (searchStats && !searchStats.querySelector('.realtime-indicator')) {
            const indicator = document.createElement('span');
            indicator.className = 'realtime-indicator';
            indicator.innerHTML = '<span class="loading-dot"></span>实时搜索';
            searchStats.appendChild(indicator);
        }
    }
    
    addSearchEnginesInfo() {
        // 在搜索结果后添加搜索引擎信息
        const searchResults = document.querySelector('.search-results');
        if (searchResults && !document.querySelector('.search-engines-info')) {
            const enginesInfo = document.createElement('div');
            enginesInfo.className = 'search-engines-info';
            enginesInfo.innerHTML = `
                <h4>搜索来源</h4>
                <div class="engines-list">
                    <span class="engine-item">Google</span>
                    <span class="engine-item">Bing</span>
                    <span class="engine-item">DuckDuckGo</span>
                </div>
            `;
            searchResults.appendChild(enginesInfo);
        }
    }
    
    enhanceSearchExperience() {
        // 添加搜索动画效果
        this.addSearchAnimations();
        
        // 添加结果加载效果
        this.addResultLoadingEffects();
        
        // 添加实时更新提示
        this.addRealtimeUpdates();
    }
    
    addSearchAnimations() {
        const searchForm = document.querySelector('.search-form');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                this.showLoadingOverlay();
            });
        }
    }
    
    showLoadingOverlay() {
        // 创建加载遮罩
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <div class="loading-text">正在实时搜索官方网站...</div>
                <div class="loading-subtext">从多个搜索引擎获取最新结果</div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        // 3秒后自动隐藏（实际项目中应该根据API响应时间）
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        }, 3000);
    }
    
    addResultLoadingEffects() {
        const resultItems = document.querySelectorAll('.result-item');
        resultItems.forEach((item, index) => {
            // 添加延迟加载效果
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.5s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    addRealtimeUpdates() {
        // 添加实时更新提示
        const searchInfo = document.querySelector('.search-info');
        if (searchInfo) {
            const updateInfo = document.createElement('div');
            updateInfo.className = 'realtime-update-info';
            updateInfo.innerHTML = '🔄 结果实时更新，确保获取最新信息';
            updateInfo.style.cssText = `
                background: #e8f5e8;
                color: #2e7d32;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-top: 10px;
                border-left: 3px solid #4caf50;
            `;
            searchInfo.appendChild(updateInfo);
        }
    }
    
    async handleSearch(event) {
        event.preventDefault();
        
        const form = event.target;
        const query = form.querySelector('.search-input').value.trim();
        
        if (!query) {
            return;
        }
        
        // 显示实时搜索加载状态
        this.showRealtimeLoading();
        
        // 记录搜索历史
        this.recordSearchHistory(query);
        
        // 提交表单
        form.submit();
    }
    
    showRealtimeLoading() {
        const searchButton = document.querySelector('.search-button');
        if (searchButton) {
            searchButton.innerHTML = '<div class="loading-spinner" style="width: 16px; height: 16px; border-width: 2px;"></div>';
            searchButton.disabled = true;
        }
        
        // 显示实时搜索提示
        this.showRealtimeSearchTip();
    }
    
    showRealtimeSearchTip() {
        const searchContainer = document.querySelector('.search-container');
        if (searchContainer) {
            const tip = document.createElement('div');
            tip.className = 'realtime-search-tip';
            tip.innerHTML = '🔍 正在从多个搜索引擎实时获取官方网站结果...';
            tip.style.cssText = `
                background: #e3f2fd;
                color: #1976d2;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-top: 10px;
                text-align: center;
                border: 1px solid #bbdefb;
            `;
            searchContainer.appendChild(tip);
            
            // 3秒后移除提示
            setTimeout(() => {
                if (tip.parentNode) {
                    tip.parentNode.removeChild(tip);
                }
            }, 3000);
        }
    }
    
    // 重写搜索建议方法，添加实时搜索特性
    async getSuggestions(query) {
        // 实时搜索模式下，提供更智能的建议
        const realtimeSuggestions = [
            `${query} 官方网站`,
            `${query} 官网`,
            `${query} 政府`,
            `${query} 教育`,
            `${query} 机构`,
            `${query} 官方`,
            `${query} 权威`
        ];
        
        return realtimeSuggestions;
    }
    
    // 添加实时搜索统计
    trackRealtimeSearch(query, results) {
        // 记录实时搜索统计
        const stats = {
            query: query,
            resultCount: results.length,
            timestamp: new Date().toISOString(),
            searchMode: 'realtime'
        };
        
        // 保存到本地存储
        try {
            let searchStats = JSON.parse(localStorage.getItem('realtimeSearchStats') || '[]');
            searchStats.push(stats);
            
            // 只保留最近100次搜索
            if (searchStats.length > 100) {
                searchStats = searchStats.slice(-100);
            }
            
            localStorage.setItem('realtimeSearchStats', JSON.stringify(searchStats));
        } catch (error) {
            console.error('Error tracking realtime search:', error);
        }
    }
    
    // 获取实时搜索统计
    getRealtimeSearchStats() {
        try {
            return JSON.parse(localStorage.getItem('realtimeSearchStats') || '[]');
        } catch (error) {
            console.error('Error getting realtime search stats:', error);
            return [];
        }
    }
}

// 页面加载完成后初始化实时搜索引擎
document.addEventListener('DOMContentLoaded', () => {
    new RealtimeSearchEngine();
});

// 添加实时搜索工具函数
window.RealtimeSearchUtils = {
    // 检查是否为实时搜索模式
    isRealtimeMode: () => {
        return document.querySelector('.realtime-badge') !== null;
    },
    
    // 获取搜索引擎信息
    getSearchEngines: () => {
        return [
            { name: 'Google', status: 'active' },
            { name: 'Bing', status: 'active' },
            { name: 'DuckDuckGo', status: 'active' }
        ];
    },
    
    // 显示实时搜索状态
    showRealtimeStatus: (message) => {
        const statusDiv = document.createElement('div');
        statusDiv.className = 'realtime-status';
        statusDiv.innerHTML = message;
        statusDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4ecdc4;
            color: white;
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        
        document.body.appendChild(statusDiv);
        
        setTimeout(() => {
            if (statusDiv.parentNode) {
                statusDiv.parentNode.removeChild(statusDiv);
            }
        }, 3000);
    }
};

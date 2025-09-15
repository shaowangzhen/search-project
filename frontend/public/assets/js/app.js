/**
 * 官方网站搜索引擎前端JavaScript
 */

class SearchEngine {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initSearchSuggestions();
    }
    
    bindEvents() {
        // 搜索表单提交
        const searchForm = document.querySelector('.search-form');
        if (searchForm) {
            searchForm.addEventListener('submit', this.handleSearch.bind(this));
        }
        
        // 搜索输入框事件
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', this.handleInput.bind(this));
            searchInput.addEventListener('focus', this.showSuggestions.bind(this));
            searchInput.addEventListener('blur', this.hideSuggestions.bind(this));
        }
        
        // 键盘导航
        document.addEventListener('keydown', this.handleKeydown.bind(this));
    }
    
    initSearchSuggestions() {
        this.suggestions = [];
        this.currentSuggestionIndex = -1;
        this.suggestionContainer = document.getElementById('suggestions');
    }
    
    async handleSearch(event) {
        event.preventDefault();
        
        const form = event.target;
        const query = form.querySelector('.search-input').value.trim();
        
        if (!query) {
            return;
        }
        
        // 显示加载状态
        this.showLoading();
        
        // 记录搜索历史
        this.recordSearchHistory(query);
        
        // 提交表单
        form.submit();
    }
    
    async handleInput(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        try {
            const suggestions = await this.getSuggestions(query);
            this.displaySuggestions(suggestions);
        } catch (error) {
            console.error('获取搜索建议失败:', error);
        }
    }
    
    async getSuggestions(query) {
        const response = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        return data.suggestions || [];
    }
    
    displaySuggestions(suggestions) {
        if (!this.suggestionContainer) {
            return;
        }
        
        this.suggestions = suggestions;
        this.currentSuggestionIndex = -1;
        
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        const html = suggestions.map((suggestion, index) => `
            <div class="suggestion-item" data-index="${index}">
                ${this.highlightQuery(suggestion, this.getCurrentQuery())}
            </div>
        `).join('');
        
        this.suggestionContainer.innerHTML = html;
        this.suggestionContainer.style.display = 'block';
        
        // 绑定点击事件
        this.suggestionContainer.querySelectorAll('.suggestion-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                this.selectSuggestion(suggestions[index]);
            });
        });
    }
    
    highlightQuery(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<strong>$1</strong>');
    }
    
    getCurrentQuery() {
        const searchInput = document.querySelector('.search-input');
        return searchInput ? searchInput.value.trim() : '';
    }
    
    selectSuggestion(suggestion) {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.value = suggestion;
            this.hideSuggestions();
            searchInput.focus();
        }
    }
    
    showSuggestions() {
        if (this.suggestionContainer && this.suggestions.length > 0) {
            this.suggestionContainer.style.display = 'block';
        }
    }
    
    hideSuggestions() {
        if (this.suggestionContainer) {
            this.suggestionContainer.style.display = 'none';
        }
    }
    
    handleKeydown(event) {
        if (!this.suggestionContainer || this.suggestionContainer.style.display === 'none') {
            return;
        }
        
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                this.navigateSuggestions(1);
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.navigateSuggestions(-1);
                break;
            case 'Enter':
                event.preventDefault();
                if (this.currentSuggestionIndex >= 0) {
                    this.selectSuggestion(this.suggestions[this.currentSuggestionIndex]);
                } else {
                    this.handleSearch(event);
                }
                break;
            case 'Escape':
                this.hideSuggestions();
                break;
        }
    }
    
    navigateSuggestions(direction) {
        if (this.suggestions.length === 0) {
            return;
        }
        
        this.currentSuggestionIndex += direction;
        
        if (this.currentSuggestionIndex < 0) {
            this.currentSuggestionIndex = this.suggestions.length - 1;
        } else if (this.currentSuggestionIndex >= this.suggestions.length) {
            this.currentSuggestionIndex = 0;
        }
        
        // 更新视觉状态
        this.suggestionContainer.querySelectorAll('.suggestion-item').forEach((item, index) => {
            item.classList.toggle('active', index === this.currentSuggestionIndex);
        });
    }
    
    showLoading() {
        const searchButton = document.querySelector('.search-button');
        if (searchButton) {
            searchButton.innerHTML = '<div class="loading"></div>';
            searchButton.disabled = true;
        }
    }
    
    recordSearchHistory(query) {
        try {
            let history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
            
            // 移除重复项
            history = history.filter(item => item !== query);
            
            // 添加到开头
            history.unshift(query);
            
            // 限制历史记录数量
            if (history.length > 10) {
                history = history.slice(0, 10);
            }
            
            localStorage.setItem('searchHistory', JSON.stringify(history));
        } catch (error) {
            console.error('保存搜索历史失败:', error);
        }
    }
    
    getSearchHistory() {
        try {
            return JSON.parse(localStorage.getItem('searchHistory') || '[]');
        } catch (error) {
            console.error('获取搜索历史失败:', error);
            return [];
        }
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new SearchEngine();
});

// 工具函数
const utils = {
    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // 格式化时间
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) { // 1分钟内
            return '刚刚';
        } else if (diff < 3600000) { // 1小时内
            return Math.floor(diff / 60000) + '分钟前';
        } else if (diff < 86400000) { // 1天内
            return Math.floor(diff / 3600000) + '小时前';
        } else {
            return Math.floor(diff / 86400000) + '天前';
        }
    },
    
    // 高亮文本
    highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
};

// 导出到全局
window.SearchEngine = SearchEngine;
window.utils = utils;

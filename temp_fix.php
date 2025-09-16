        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
            }
            
            .search-container {
                max-width: 100%;
                width: 100%;
            }
            
            .search-form {
                flex-direction: row; /* 保持水平布局 */
                min-height: 50px; /* 固定最小高度 */
            }
            
            .search-input {
                font-size: 16px; /* 使用16px防止iOS自动缩放 */
                padding: 14px 16px;
                min-height: 50px; /* 固定高度 */
            }
            
            .search-btn {
                font-size: 16px;
                padding: 14px 24px;
                min-width: 80px;
                flex-shrink: 0; /* 防止按钮被压缩 */
            }
            
            .content-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            .hot-grid {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 6px;
            }
            
            .hot-item {
                padding: 6px 8px;
            }
            
            .hot-item a {
                font-size: 13px;
            }
            
            .hot-icon {
                width: 18px;
                height: 18px;
                font-size: 11px;
                margin-right: 6px;
            }
            
            .nav-links {
                gap: 8px;
                justify-content: center;
            }
            
            .nav-links a {
                padding: 8px 12px;
                font-size: 13px;
                flex: 1;
                min-width: 0;
                justify-content: center;
            }
            
            .nav-icon {
                width: 16px;
                height: 16px;
                font-size: 10px;
            }
        }
        
        @media (max-width: 480px) {
            .logo {
                font-size: 28px;
            }
            
            .search-form {
                min-height: 45px;
            }
            
            .search-input {
                font-size: 16px; /* 保持16px防止iOS自动缩放 */
                padding: 12px 14px;
                min-height: 45px; /* 固定高度 */
            }
            
            .search-btn {
                font-size: 14px;
                padding: 12px 20px;
                min-width: 70px;
                flex-shrink: 0; /* 防止按钮被压缩 */
            }
            
            .content-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .hot-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
            }
            
            .hot-item {
                padding: 6px 8px;
            }
            
            .hot-item a {
                font-size: 12px;
            }
            
            .hot-icon {
                width: 16px;
                height: 16px;
                font-size: 10px;
                margin-right: 5px;
            }
            
            .nav-links {
                gap: 6px;
            }
            
            .nav-links a {
                padding: 6px 8px;
                font-size: 12px;
            }
            
            .nav-icon {
                width: 14px;
                height: 14px;
                font-size: 9px;
            }
        }

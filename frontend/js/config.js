// API Configuration
// Automatically detects environment and sets appropriate API URL

const config = {
    // Determine API URL based on environment
    API_URL: (() => {
        const hostname = window.location.hostname;
        
        // Check if API_URL is injected via environment variable (for platforms like Vercel)
        if (typeof window.ENV !== 'undefined' && window.ENV.API_URL) {
            return window.ENV.API_URL;
        }
        
        // Development environment
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:8000/api';
        }
        
        // Production environment
        // This will be replaced during deployment or can be set via window.ENV
        // Default: assume API is on same domain with /api path
        return `${window.location.protocol}//${window.location.host}/api`;
    })(),
    
    // Other configuration options can be added here
    APP_NAME: 'LearnHub',
    VERSION: '1.0.0'
};

// Make config available globally
window.APP_CONFIG = config;

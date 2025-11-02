// API Configuration
// Automatically detects environment and sets appropriate API URL

const config = {
    // Determine API URL based on environment
    API_URL: (() => {
        const hostname = window.location.hostname;
        
        // Development environment
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:8000/api';
        }
        
        // Production environment
        // Update this with your production API URL when deploying
        return 'https://your-production-api.com/api';
    })(),
    
    // Other configuration options can be added here
    APP_NAME: 'LearnHub',
    VERSION: '1.0.0'
};

// Make config available globally
window.APP_CONFIG = config;

// Authentication utility functions
const API_URL = 'http://localhost:8000/api';

// Get stored token
function getToken() {
    return localStorage.getItem('access_token');
}

// Get stored user
function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Check if user is authenticated
function isAuthenticated() {
    return getToken() !== null;
}

// Logout user
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// Make authenticated API request
async function authenticatedFetch(endpoint, options = {}) {
    const token = getToken();
    
    if (!token) {
        logout();
        return;
    }
    
    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        }
    });
    
    // If unauthorized, logout
    if (response.status === 401) {
        logout();
        return;
    }
    
    return response;
}

// Protect page - redirect to login if not authenticated
function protectPage() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}
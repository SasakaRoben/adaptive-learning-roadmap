// Authentication utility functions
const API_URL = 'http://localhost:8000/api';

// Get stored token
function getToken() {
    const token = localStorage.getItem('access_token');
    console.log('Getting token:', token ? 'Token found' : 'No token'); // Debug
    return token;
}

// Get stored user
function getUser() {
    const userStr = localStorage.getItem('user');
    console.log('Getting user:', userStr ? 'User found' : 'No user'); // Debug
    return userStr ? JSON.parse(userStr) : null;
}

// Check if user is authenticated
function isAuthenticated() {
    const authenticated = getToken() !== null;
    console.log('Is authenticated:', authenticated); // Debug
    return authenticated;
}

// Logout user
function logout() {
    console.log('Logging out...'); // Debug
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// Make authenticated API request
async function authenticatedFetch(endpoint, options = {}) {
    const token = getToken();
    
    if (!token) {
        console.error('No token found, redirecting to login');
        logout();
        return;
    }
    
    try {
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
            console.error('Unauthorized, redirecting to login');
            logout();
            return;
        }
        
        return response;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Protect page - redirect to login if not authenticated
function protectPage() {
    console.log('Protecting page...'); // Debug
    if (!isAuthenticated()) {
        console.log('Not authenticated, redirecting to login');
        window.location.href = 'login.html';
    } else {
        console.log('User is authenticated');
    }
}
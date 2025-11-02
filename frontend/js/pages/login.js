const API_URL = window.APP_CONFIG?.API_URL || 'http://localhost:8000/api';

const form = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const rememberMeCheckbox = document.getElementById('rememberMe');
const submitBtn = document.getElementById('submitBtn');
const spinner = document.getElementById('spinner');
const alertBox = document.getElementById('alertBox');

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    // Basic validation
    if (!username) {
        showAlert('Please enter your username or email', 'error');
        return;
    }

    if (!password) {
        showAlert('Please enter your password', 'error');
        return;
    }

    // Submit form
    submitBtn.style.display = 'none';
    spinner.style.display = 'block';

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Store JWT token and user data FIRST
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showAlert('Login successful! Redirecting...', 'success');
            
            // Wait a bit to ensure localStorage is written, then check assessment
            setTimeout(async () => {
                try {
                    const token = localStorage.getItem('access_token');
                    const statusResponse = await fetch(`${API_URL}/assessment/status`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    const status = await statusResponse.json();
                    
                    if (!status.completed) {
                        window.location.href = 'assessment.html';
                    } else {
                        window.location.href = 'dashboard.html';
                    }
                } catch (error) {
                    console.error('Error checking assessment:', error);
                    // Default to assessment page for new users
                    window.location.href = 'assessment.html';
                }
            }, 1500);
        } else {
            if (response.status === 401) {
                showAlert('Invalid username or password', 'error');
            } else {
                showAlert(data.detail || 'Login failed. Please try again.', 'error');
            }
        }
    } catch (error) {
        showAlert('Network error. Please check your connection and try again.', 'error');
        console.error('Login error:', error);
    } finally {
        submitBtn.style.display = 'block';
        spinner.style.display = 'none';
    }
});

// Helper function
function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type} show`;
    
    setTimeout(() => {
        alertBox.classList.remove('show');
    }, 5000);
}

// Clear error styling on input
usernameInput.addEventListener('input', function() {
    this.classList.remove('error');
    document.getElementById('usernameError').classList.remove('show');
});

passwordInput.addEventListener('input', function() {
    this.classList.remove('error');
    document.getElementById('passwordError').classList.remove('show');
});
const API_URL = window.APP_CONFIG?.API_URL || 'http://localhost:8000/api';

const form = document.getElementById('registrationForm');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const submitBtn = document.getElementById('submitBtn');
const spinner = document.getElementById('spinner');
const alertBox = document.getElementById('alertBox');

let usernameTimeout, emailTimeout;
let isUsernameAvailable = false;
let isEmailAvailable = false;

// Real-time username validation
usernameInput.addEventListener('input', function() {
    clearTimeout(usernameTimeout);
    const username = this.value.trim();
    
    if (username.length < 3) {
        showError('username', 'Username must be at least 3 characters');
        isUsernameAvailable = false;
        return;
    }

    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        showError('username', 'Username can only contain letters, numbers, and underscores');
        isUsernameAvailable = false;
        return;
    }

    document.getElementById('usernameChecking').style.display = 'block';
    clearMessages('username');

    usernameTimeout = setTimeout(() => checkUsername(username), 500);
});

// Real-time email validation
emailInput.addEventListener('input', function() {
    clearTimeout(emailTimeout);
    const email = this.value.trim();
    
    if (!email) return;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('email', 'Please enter a valid email address');
        isEmailAvailable = false;
        return;
    }

    document.getElementById('emailChecking').style.display = 'block';
    clearMessages('email');

    emailTimeout = setTimeout(() => checkEmail(email), 500);
});

// Password validation
passwordInput.addEventListener('input', function() {
    const password = this.value;
    validatePassword(password);
    validateConfirmPassword();
});

confirmPasswordInput.addEventListener('input', validateConfirmPassword);

// Check username availability
async function checkUsername(username) {
    try {
        const response = await fetch(`${API_URL}/check-username/${username}`);
        const data = await response.json();
        
        document.getElementById('usernameChecking').style.display = 'none';
        
        if (data.available) {
            showSuccess('username', 'Username is available!');
            isUsernameAvailable = true;
        } else {
            showError('username', 'Username is already taken');
            isUsernameAvailable = false;
        }
    } catch (error) {
        document.getElementById('usernameChecking').style.display = 'none';
        console.error('Error checking username:', error);
    }
}

// Check email availability
async function checkEmail(email) {
    try {
        const response = await fetch(`${API_URL}/check-email/${email}`);
        const data = await response.json();
        
        document.getElementById('emailChecking').style.display = 'none';
        
        if (data.available) {
            showSuccess('email', 'Email is available!');
            isEmailAvailable = true;
        } else {
            showError('email', 'Email is already registered');
            isEmailAvailable = false;
        }
    } catch (error) {
        document.getElementById('emailChecking').style.display = 'none';
        console.error('Error checking email:', error);
    }
}

// Validate password requirements
function validatePassword(password) {
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /[0-9]/.test(password)
    };

    document.getElementById('req-length').classList.toggle('valid', requirements.length);
    document.getElementById('req-uppercase').classList.toggle('valid', requirements.uppercase);
    document.getElementById('req-lowercase').classList.toggle('valid', requirements.lowercase);
    document.getElementById('req-number').classList.toggle('valid', requirements.number);

    return Object.values(requirements).every(req => req);
}

// Validate confirm password
function validateConfirmPassword() {
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (confirmPassword === '') {
        clearMessages('confirmPassword');
        return;
    }

    if (password !== confirmPassword) {
        showError('confirmPassword', 'Passwords do not match');
    } else {
        showSuccess('confirmPassword', 'Passwords match!');
    }
}

// Form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // Validate all fields
    if (!isUsernameAvailable) {
        showAlert('Please choose an available username', 'error');
        return;
    }

    if (!isEmailAvailable) {
        showAlert('Please use an available email address', 'error');
        return;
    }

    if (!validatePassword(password)) {
        showAlert('Please meet all password requirements', 'error');
        return;
    }

    if (password !== confirmPassword) {
        showAlert('Passwords do not match', 'error');
        return;
    }

    // Submit form
    submitBtn.style.display = 'none';
    spinner.style.display = 'block';

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('Registration successful! Redirecting to login...', 'success');
            form.reset();
            isUsernameAvailable = false;
            isEmailAvailable = false;
            
            // Redirect to login page
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showAlert(data.detail || 'Registration failed. Please try again.', 'error');
        }
    } catch (error) {
        showAlert('Network error. Please check your connection and try again.', 'error');
        console.error('Registration error:', error);
    } finally {
        submitBtn.style.display = 'block';
        spinner.style.display = 'none';
    }
});

// Helper functions
function showError(field, message) {
    const input = document.getElementById(field);
    const errorDiv = document.getElementById(`${field}Error`);
    const successDiv = document.getElementById(`${field}Success`);
    
    input.classList.add('error');
    input.classList.remove('success');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
    successDiv.classList.remove('show');
}

function showSuccess(field, message) {
    const input = document.getElementById(field);
    const errorDiv = document.getElementById(`${field}Error`);
    const successDiv = document.getElementById(`${field}Success`);
    
    input.classList.add('success');
    input.classList.remove('error');
    successDiv.textContent = message;
    successDiv.classList.add('show');
    errorDiv.classList.remove('show');
}

function clearMessages(field) {
    const input = document.getElementById(field);
    const errorDiv = document.getElementById(`${field}Error`);
    const successDiv = document.getElementById(`${field}Success`);
    
    input.classList.remove('error', 'success');
    errorDiv.classList.remove('show');
    successDiv.classList.remove('show');
}

function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type} show`;
    
    setTimeout(() => {
        alertBox.classList.remove('show');
    }, 5000);
}
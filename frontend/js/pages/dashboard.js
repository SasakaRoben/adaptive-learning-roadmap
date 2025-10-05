// Wait for DOM to be ready before protecting page
document.addEventListener('DOMContentLoaded', function() {
    // Protect the page - redirect to login if not authenticated
    protectPage();
    
    // Initialize dashboard
    initDashboard();
});

// DOM elements
const userName = document.getElementById('userName');
const userDisplayName = document.getElementById('userDisplayName');
const logoutBtn = document.getElementById('logoutBtn');
const continueBtn = document.getElementById('continueBtn');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const progressPercent = document.getElementById('progressPercent');

function initDashboard() {
    loadUserData();
    
    // Logout handler
    logoutBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to logout?')) {
            logout();
        }
    });

    // Continue learning handler
    continueBtn.addEventListener('click', () => {
        // TODO: Redirect to current learning module
        alert('Learning modules coming soon!');
    });
}

// Load user data
async function loadUserData() {
    try {
        const response = await authenticatedFetch('/me');
        if (!response) return;

        const user = await response.json();
        
        // Update user display
        userName.textContent = user.username;
        userDisplayName.textContent = user.username;
        
        // Load mock progress data (replace with real API later)
        loadProgressData();
        
    } catch (error) {
        console.error('Error loading user data:', error);
        showError('Failed to load user data');
    }
}

// Load progress data (mock data for now)
function loadProgressData() {
    // TODO: Replace with actual API call to get user's roadmap progress
    const mockProgress = {
        completed: 3,
        total: 10,
        percentage: 30,
        streak: 7,
        timeSpent: 12,
        achievements: 2
    };
    
    updateProgressDisplay(mockProgress);
}

// Update progress display
function updateProgressDisplay(data) {
    progressFill.style.width = `${data.percentage}%`;
    progressText.textContent = `${data.completed} of ${data.total} topics completed`;
    progressPercent.textContent = `${data.percentage}%`;
    
    document.getElementById('streakDays').textContent = data.streak;
    document.getElementById('completedTopics').textContent = data.completed;
    document.getElementById('timeSpent').textContent = `${data.timeSpent}h`;
    document.getElementById('achievements').textContent = data.achievements;
}

// Logout handler
logoutBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
        logout();
    }
});

// Continue learning handler
continueBtn.addEventListener('click', () => {
    // TODO: Redirect to current learning module
    alert('Learning modules coming soon!');
});

// Initialize dashboard
loadUserData();

function showError(message) {
    console.error(message);
    // TODO: Add proper error display UI
}
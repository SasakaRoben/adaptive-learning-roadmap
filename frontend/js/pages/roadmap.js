// Protect page
protectPage();

// DOM elements
const loading = document.getElementById('loading');
const roadmapContainer = document.getElementById('roadmapContainer');
const levelBadge = document.getElementById('levelBadge');
const completedCount = document.getElementById('completedCount');
const inProgressCount = document.getElementById('inProgressCount');
const totalCount = document.getElementById('totalCount');
const progressPercent = document.getElementById('progressPercent');
const logoutBtn = document.getElementById('logoutBtn');
const topicModal = document.getElementById('topicModal');
const modalBody = document.getElementById('modalBody');
const closeModal = document.querySelector('.close');

// State
let learningPath = null;

// Initialize
async function init() {
    await loadLearningPath();
    setupEventListeners();
}

// Load learning path
async function loadLearningPath() {
    try {
        const response = await authenticatedFetch('/learning-path/');
        if (!response) return;
        
        learningPath = await response.json();
        
        // Update summary
        levelBadge.textContent = learningPath.user_level.charAt(0).toUpperCase() + 
                                 learningPath.user_level.slice(1);
        levelBadge.className = `level-badge ${learningPath.user_level}`;
        
        completedCount.textContent = learningPath.completed_topics;
        inProgressCount.textContent = learningPath.in_progress_topics;
        totalCount.textContent = learningPath.total_topics;
        progressPercent.textContent = `${learningPath.progress_percentage}%`;
        
        // Display topics
        displayTopics(learningPath.topics);
        
        loading.style.display = 'none';
        roadmapContainer.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading learning path:', error);
        loading.innerHTML = '<p style="color: red;">Failed to load roadmap. Please refresh.</p>';
    }
}

// Display topics
function displayTopics(topics) {
    roadmapContainer.innerHTML = topics.map(topic => {
        const statusIcons = {
            completed: '✓',
            in_progress: '⟳',
            available: '▶',
            locked: '🔒'
        };
        
        const statusLabels = {
            completed: 'Completed',
            in_progress: 'In Progress',
            available: 'Available',
            locked: 'Locked'
        };
        
        return `
            <div class="topic-node ${topic.status}" data-topic-id="${topic.id}">
                <div class="topic-header">
                    <div class="topic-title">${topic.title}</div>
                    <div class="topic-status ${topic.status}">
                        ${statusIcons[topic.status]} ${statusLabels[topic.status]}
                    </div>
                </div>
                <div class="topic-description">${topic.description}</div>
                <div class="topic-meta">
                    <span>⏱ ${topic.estimated_hours}h</span>
                    <span>📊 ${topic.difficulty_level}</span>
                    ${topic.prerequisites.length > 0 ? 
                        `<span>🔗 ${topic.prerequisites.length} prerequisite(s)</span>` : ''}
                </div>
                ${topic.progress_percentage > 0 ? `
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: ${topic.progress_percentage}%"></div>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    // Add click listeners
    document.querySelectorAll('.topic-node').forEach(node => {
        node.addEventListener('click', () => {
            const topicId = parseInt(node.dataset.topicId);
            showTopicDetail(topicId);
        });
    });
}

// Show topic detail
async function showTopicDetail(topicId) {
    try {
        const response = await authenticatedFetch(`/learning-path/topics/${topicId}`);
        if (!response) return;
        
        const topic = await response.json();
        
        const statusColors = {
            completed: '#27ae60',
            in_progress: '#f39c12',
            available: '#667eea',
            locked: '#6c757d'
        };
        
        modalBody.innerHTML = `
            <h2 class="modal-title">${topic.title}</h2>
            <span class="modal-badge" style="background: ${statusColors[topic.status]}20; color: ${statusColors[topic.status]}">
                ${topic.difficulty_level} • ${topic.estimated_hours}h
            </span>
            
            <p class="modal-description">${topic.description}</p>
            
            ${topic.prerequisites.length > 0 ? `
                <div class="modal-content-section">
                    <h3>Prerequisites</h3>
                    <ul class="prerequisites-list">
                        ${topic.prerequisites.map(prereq => 
                            `<li>${prereq.title}</li>`
                        ).join('')}
                    </ul>
                </div>
            ` : ''}
            
            <div class="modal-content-section">
                <h3>Learning Content</h3>
                <p>${topic.content}</p>
            </div>
            
            ${topic.resources && topic.resources.length > 0 ? `
                <div class="modal-content-section">
                    <h3>📚 Learning Resources</h3>
                    <div class="resources-list">
                        ${topic.resources.map(resource => `
                            <a href="${resource.url}" target="_blank" rel="noopener" class="resource-item">
                                <div class="resource-icon">${getResourceIcon(resource.type)}</div>
                                <div class="resource-details">
                                    <div class="resource-title">${resource.title}</div>
                                    <div class="resource-meta">
                                        ${resource.platform || 'External'} • ${resource.duration || '?'} min
                                    </div>
                                </div>
                                <div class="resource-arrow">→</div>
                            </a>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            ${topic.resources && topic.resources.length > 0 ? `
                <div class="modal-content-section">
                    <h3>Learning Resources</h3>
                    <div class="resources-list">
                        ${topic.resources.map(resource => `
                            <a href="${resource.url}" target="_blank" class="resource-item">
                                <div class="resource-icon">${getResourceIcon(resource.type)}</div>
                                <div class="resource-details">
                                    <div class="resource-title">${resource.title}</div>
                                    <div class="resource-meta">
                                        ${resource.platform} • ${resource.duration} min
                                    </div>
                                </div>
                                <div class="resource-arrow">→</div>
                            </a>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            ${topic.time_spent_minutes > 0 ? `
                <div class="modal-content-section">
                    <h3>Your Progress</h3>
                    <p>Time spent: ${Math.floor(topic.time_spent_minutes / 60)}h ${topic.time_spent_minutes % 60}m</p>
                    <p>Progress: ${topic.progress_percentage}%</p>
                </div>
            ` : ''}
            
            <div style="margin-top: 30px; display: flex; gap: 15px;">
                ${topic.status === 'available' || topic.status === 'in_progress' ? `
                    <button class="btn btn-primary" onclick="startTopic(${topic.id})">
                        ${topic.status === 'available' ? 'Start Learning' : 'Continue Learning'}
                    </button>
                ` : ''}
                
                ${topic.status === 'in_progress' ? `
                    <button class="btn btn-success" onclick="completeTopic(${topic.id})">
                        Mark as Complete
                    </button>
                ` : ''}
                
                ${topic.status === 'completed' ? `
                    <button class="btn btn-success" disabled>
                        ✓ Completed
                    </button>
                ` : ''}
                
                ${topic.status === 'locked' ? `
                    <button class="btn btn-primary" disabled>
                        🔒 Complete prerequisites first
                    </button>
                ` : ''}
            </div>
        `;
        
        topicModal.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading topic details:', error);
        alert('Failed to load topic details');
    }
}

// Start topic
async function startTopic(topicId) {
    try {
        const response = await authenticatedFetch(`/learning-path/topics/${topicId}/start`, {
            method: 'POST'
        });
        
        if (!response) return;
        
        const result = await response.json();
        alert(result.message);
        
        // Reload the roadmap
        topicModal.style.display = 'none';
        await loadLearningPath();
        
    } catch (error) {
        console.error('Error starting topic:', error);
        alert('Failed to start topic');
    }
}

// Complete topic
async function completeTopic(topicId) {
    if (!confirm('Are you sure you completed this topic?')) return;
    
    try {
        const response = await authenticatedFetch(`/learning-path/topics/${topicId}/complete`, {
            method: 'POST'
        });
        
        if (!response) return;
        
        const result = await response.json();
        alert(result.message);
        
        // Reload the roadmap
        topicModal.style.display = 'none';
        await loadLearningPath();
        
    } catch (error) {
        console.error('Error completing topic:', error);
        alert('Failed to complete topic');
    }
}

// Setup event listeners
function setupEventListeners() {
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            logout();
        }
    });
    
    closeModal.addEventListener('click', () => {
        topicModal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === topicModal) {
            topicModal.style.display = 'none';
        }
    });
}

// Make functions global for inline onclick handlers
window.startTopic = startTopic;
window.completeTopic = completeTopic;

// Helper function for resource icons
function getResourceIcon(type) {
    const icons = {
        video: '🎥',
        article: '📄',
        interactive: '💻',
        documentation: '📚'
    };
    return icons[type] || '🔗';
}

// Initialize
init();
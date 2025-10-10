// Protect page - must be authenticated
protectPage();

// DOM elements
const loading = document.getElementById('loading');
const questionsContainer = document.getElementById('questionsContainer');
const resultsContainer = document.getElementById('resultsContainer');
const questionCard = document.getElementById('questionCard');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const goToDashboard = document.getElementById('goToDashboard');

// State
let questions = [];
let currentQuestionIndex = 0;
let userAnswers = {};

// Initialize
async function init() {
    // Check if already completed
    const status = await checkAssessmentStatus();
    if (status.completed) {
        // Redirect to dashboard if already completed
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Load questions
    await loadQuestions();
}

// Check assessment status
async function checkAssessmentStatus() {
    try {
        const response = await authenticatedFetch('/assessment/status');
        return await response.json();
    } catch (error) {
        console.error('Error checking status:', error);
        return { completed: false };
    }
}

// Load assessment questions
async function loadQuestions() {
    try {
        const response = await authenticatedFetch('/assessment/questions');
        questions = await response.json();
        
        loading.style.display = 'none';
        questionsContainer.style.display = 'block';
        
        displayQuestion();
    } catch (error) {
        console.error('Error loading questions:', error);
        loading.innerHTML = '<p style="color: red;">Failed to load questions. Please refresh.</p>';
    }
}

// Display current question
function displayQuestion() {
    const question = questions[currentQuestionIndex];
    const isAnswered = userAnswers[question.id] !== undefined;
    
    questionCard.innerHTML = `
        <h2 class="question-text">${question.question_text}</h2>
        <div class="options">
            ${question.options.map(option => `
                <div class="option ${userAnswers[question.id] === option ? 'selected' : ''}" 
                     onclick="selectAnswer(${question.id}, '${option}')">
                    ${option}
                </div>
            `).join('')}
        </div>
    `;
    
    // Update progress
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressFill.style.width = `${progress}%`;
    progressText.textContent = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
    
    // Update navigation buttons
    prevBtn.style.display = currentQuestionIndex > 0 ? 'block' : 'none';
    
    if (currentQuestionIndex === questions.length - 1) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'block';
        submitBtn.disabled = !isAnswered;
    } else {
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
        nextBtn.disabled = !isAnswered;
    }
}

// Select answer
function selectAnswer(questionId, answer) {
    userAnswers[questionId] = answer;
    displayQuestion();
}

// Navigation
prevBtn.addEventListener('click', () => {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
});

nextBtn.addEventListener('click', () => {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    }
});

// Submit assessment
submitBtn.addEventListener('click', async () => {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    try {
        // Format answers
        const answers = questions.map(q => ({
            question_id: q.id,
            answer: userAnswers[q.id]
        }));
        
        const response = await authenticatedFetch('/assessment/submit', {
            method: 'POST',
            body: JSON.stringify({ answers })
        });
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Error submitting assessment:', error);
        alert('Failed to submit assessment. Please try again.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Assessment';
    }
});

// Display results
function displayResults(result) {
    questionsContainer.style.display = 'none';
    resultsContainer.style.display = 'block';
    
    // Set icon based on level
    const icons = {
        beginner: '🌱',
        intermediate: '🚀',
        advanced: '⭐'
    };
    
    document.getElementById('resultIcon').textContent = icons[result.assigned_level];
    document.getElementById('scoreDisplay').textContent = `${result.score}/${result.total_questions}`;
    document.getElementById('percentageDisplay').textContent = `${result.percentage}%`;
    
    const levelBadge = document.getElementById('levelBadge');
    levelBadge.textContent = result.assigned_level.charAt(0).toUpperCase() + result.assigned_level.slice(1);
    levelBadge.className = `level-badge ${result.assigned_level}`;
    
    document.getElementById('resultMessage').textContent = result.message;
    document.getElementById('nextSteps').textContent = result.next_steps;
}

// Go to dashboard
goToDashboard.addEventListener('click', () => {
    window.location.href = 'dashboard.html';
});

// Start
init();
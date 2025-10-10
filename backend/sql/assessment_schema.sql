-- Add level to existing topics
ALTER TABLE topics ADD COLUMN IF NOT EXISTS level VARCHAR(20) 
    CHECK (level IN ('beginner', 'intermediate', 'advanced'));

-- Update existing topics with beginner level
UPDATE topics SET level = 'beginner' WHERE level IS NULL;

-- Assessment questions table
CREATE TABLE IF NOT EXISTS assessment_questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'multiple_choice',
    options JSONB,
    correct_answer TEXT,
    points INTEGER DEFAULT 1,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User assessments table
CREATE TABLE IF NOT EXISTS user_assessments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    assigned_level VARCHAR(20) CHECK (assigned_level IN ('beginner', 'intermediate', 'advanced')),
    answers JSONB,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- User's assigned path
ALTER TABLE users ADD COLUMN IF NOT EXISTS current_level VARCHAR(20) 
    CHECK (current_level IN ('beginner', 'intermediate', 'advanced')) DEFAULT 'beginner';
ALTER TABLE users ADD COLUMN IF NOT EXISTS has_completed_assessment BOOLEAN DEFAULT FALSE;

-- Insert assessment questions
INSERT INTO assessment_questions (question_text, question_type, options, correct_answer, points, order_index) VALUES
(
    'Have you written any code before (HTML, CSS, JavaScript, or any programming language)?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    1
),
(
    'Can you explain what a variable is in programming?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    2
),
(
    'Have you built a complete web project (even a simple one)?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    3
),
(
    'Are you comfortable with concepts like functions, loops, and conditionals?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    4
),
(
    'Have you worked with frameworks/libraries like React, Vue, or Angular?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    5
),
(
    'Can you build and consume APIs (REST/GraphQL)?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    6
),
(
    'Have you worked with databases (SQL or NoSQL)?',
    'yes_no',
    '["Yes", "No"]'::jsonb,
    'Yes',
    1,
    7
);

-- Add intermediate and advanced topics
INSERT INTO topics (title, description, content, difficulty_level, estimated_hours, order_index, level) VALUES
-- Intermediate topics (11-20)
('React Fundamentals', 'Component-based UI development', 'Learn React components, props, state...', 'intermediate', 8.0, 11, 'intermediate'),
('State Management', 'Managing application state with Redux/Context', 'Global state, reducers, actions...', 'intermediate', 6.0, 12, 'intermediate'),
('Node.js & Express', 'Server-side JavaScript development', 'Building REST APIs with Node.js...', 'intermediate', 10.0, 13, 'intermediate'),
('Database Integration', 'Working with PostgreSQL and MongoDB', 'CRUD operations, queries, relationships...', 'intermediate', 8.0, 14, 'intermediate'),
('Authentication & Security', 'User authentication and authorization', 'JWT, OAuth, security best practices...', 'intermediate', 7.0, 15, 'intermediate'),
('Testing', 'Unit and integration testing', 'Jest, React Testing Library...', 'intermediate', 6.0, 16, 'intermediate'),
('RESTful API Design', 'Building scalable APIs', 'REST principles, versioning, documentation...', 'intermediate', 5.0, 17, 'intermediate'),
('Git & Version Control', 'Collaborative development', 'Git workflows, branching, pull requests...', 'intermediate', 4.0, 18, 'intermediate'),
('Deployment Basics', 'Deploying applications to production', 'Heroku, Vercel, environment variables...', 'intermediate', 5.0, 19, 'intermediate'),
('Project: Full-Stack App', 'Build a complete CRUD application', 'Integrate frontend and backend...', 'intermediate', 20.0, 20, 'intermediate'),

-- Advanced topics (21-30)
('Advanced React Patterns', 'Higher-order components, render props, hooks', 'Advanced component patterns...', 'advanced', 10.0, 21, 'advanced'),
('Performance Optimization', 'Frontend and backend optimization', 'Code splitting, caching, lazy loading...', 'advanced', 8.0, 22, 'advanced'),
('Microservices Architecture', 'Building distributed systems', 'Service communication, API gateways...', 'advanced', 12.0, 23, 'advanced'),
('GraphQL', 'Modern API development', 'Schema design, resolvers, Apollo...', 'advanced', 10.0, 24, 'advanced'),
('WebSockets & Real-time', 'Real-time communication', 'Socket.io, WebRTC, live updates...', 'advanced', 8.0, 25, 'advanced'),
('Docker & Containers', 'Containerization and orchestration', 'Docker basics, Docker Compose...', 'advanced', 9.0, 26, 'advanced'),
('CI/CD Pipelines', 'Automated testing and deployment', 'GitHub Actions, Jenkins, automated workflows...', 'advanced', 7.0, 27, 'advanced'),
('System Design', 'Scalable architecture patterns', 'Load balancing, caching strategies, CDNs...', 'advanced', 15.0, 28, 'advanced'),
('Security Best Practices', 'Advanced security concepts', 'OWASP, penetration testing, encryption...', 'advanced', 10.0, 29, 'advanced'),
('Capstone Project', 'Build a production-ready full-stack application', 'Real-world project with all concepts...', 'advanced', 40.0, 30, 'advanced');

-- Update prerequisites for new topics
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
-- Intermediate prerequisites
(11, 8),  -- React requires Web Development Basics
(12, 11), -- State Management requires React
(13, 4),  -- Node.js requires Functions
(14, 13), -- Database Integration requires Node.js
(15, 13), -- Auth requires Node.js
(16, 11), -- Testing requires React
(17, 13), -- API Design requires Node.js
(19, 14), -- Deployment requires Database Integration
(20, 19), -- Project requires Deployment

-- Advanced prerequisites
(21, 12), -- Advanced React requires State Management
(22, 21), -- Performance requires Advanced React
(23, 17), -- Microservices requires API Design
(24, 14), -- GraphQL requires Database Integration
(25, 13), -- WebSockets requires Node.js
(26, 19), -- Docker requires Deployment Basics
(27, 26), -- CI/CD requires Docker
(28, 23), -- System Design requires Microservices
(29, 15), -- Advanced Security requires Auth
(30, 28); -- Capstone requires System Design
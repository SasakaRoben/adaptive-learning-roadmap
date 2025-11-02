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

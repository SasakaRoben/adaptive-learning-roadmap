-- Learning paths/roadmaps table
CREATE TABLE IF NOT EXISTS learning_paths (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Topics/nodes in the roadmap
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    content TEXT,
    difficulty_level VARCHAR(50) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    estimated_hours DECIMAL(5,2),
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User progress on topics
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    time_spent_minutes INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, topic_id)
);

-- Assessments/quizzes
CREATE TABLE IF NOT EXISTS assessments (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    questions JSONB NOT NULL,
    passing_score INTEGER DEFAULT 70 CHECK (passing_score >= 0 AND passing_score <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User assessment attempts
CREATE TABLE IF NOT EXISTS assessment_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    score INTEGER CHECK (score >= 0 AND score <= 100),
    answers JSONB,
    passed BOOLEAN,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Topic prerequisites (for roadmap dependencies)
CREATE TABLE IF NOT EXISTS topic_prerequisites (
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    prerequisite_topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    PRIMARY KEY (topic_id, prerequisite_topic_id),
    CHECK (topic_id != prerequisite_topic_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_topic ON user_progress(topic_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_status ON user_progress(status);
CREATE INDEX IF NOT EXISTS idx_learning_paths_user ON learning_paths(user_id);
CREATE INDEX IF NOT EXISTS idx_assessment_attempts_user ON assessment_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics(difficulty_level);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_learning_paths_updated_at BEFORE UPDATE
    ON learning_paths FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE
    ON user_progress FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample data for testing
INSERT INTO topics (title, description, content, difficulty_level, estimated_hours, order_index) VALUES
('Introduction to Programming', 'Learn the basics of programming concepts', 'Basic programming fundamentals...', 'beginner', 2.5, 1),
('Variables and Data Types', 'Understanding different data types', 'Learn about strings, numbers, booleans...', 'beginner', 1.5, 2),
('Control Flow', 'Learn about conditionals and loops', 'If statements, for loops, while loops...', 'beginner', 2.0, 3),
('Functions', 'Creating reusable code blocks', 'Function definition, parameters, return values...', 'intermediate', 3.0, 4),
('Object-Oriented Programming', 'Understanding OOP concepts', 'Classes, objects, inheritance...', 'intermediate', 4.0, 5),
('Data Structures', 'Arrays, lists, dictionaries', 'Common data structures and their uses...', 'intermediate', 5.0, 6),
('Algorithms', 'Problem-solving techniques', 'Sorting, searching, optimization...', 'advanced', 6.0, 7),
('Web Development Basics', 'Introduction to web technologies', 'HTML, CSS, JavaScript fundamentals...', 'beginner', 4.0, 8),
('Backend Development', 'Server-side programming', 'APIs, databases, authentication...', 'advanced', 8.0, 9),
('Database Design', 'Relational database concepts', 'SQL, normalization, relationships...', 'intermediate', 5.0, 10);

-- Add prerequisites
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(2, 1), -- Variables requires Introduction
(3, 2), -- Control Flow requires Variables
(4, 3), -- Functions requires Control Flow
(5, 4), -- OOP requires Functions
(6, 5), -- Data Structures requires OOP
(7, 6), -- Algorithms requires Data Structures
(9, 8), -- Backend requires Web Basics
(10, 9); -- Database Design requires Backend
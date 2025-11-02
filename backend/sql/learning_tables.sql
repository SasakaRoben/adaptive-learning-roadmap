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
    level VARCHAR(20) CHECK (level IN ('beginner', 'intermediate', 'advanced')),
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
CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_topics_level ON topics(level);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_learning_paths_updated_at ON learning_paths;
CREATE TRIGGER update_learning_paths_updated_at BEFORE UPDATE
    ON learning_paths FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_progress_updated_at ON user_progress;
CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE
    ON user_progress FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample data for testing
-- BEGINNER level topics
INSERT INTO topics (title, description, content, difficulty_level, estimated_hours, order_index, level) VALUES
('Introduction to HTML', 'Learn the basics of HTML structure and elements', 'HTML fundamentals, tags, attributes, semantic HTML...', 'beginner', 3.0, 1, 'beginner'),
('CSS Basics', 'Understanding styling and layout with CSS', 'Selectors, properties, box model, flexbox basics...', 'beginner', 4.0, 2, 'beginner'),
('JavaScript Fundamentals', 'Learn JavaScript basics and syntax', 'Variables, data types, operators, control flow...', 'beginner', 5.0, 3, 'beginner'),
('DOM Manipulation', 'Interact with HTML using JavaScript', 'Selecting elements, event listeners, modifying content...', 'beginner', 4.0, 4, 'beginner'),
('Git & Version Control', 'Learn version control with Git', 'Git basics, commits, branches, GitHub fundamentals...', 'beginner', 3.0, 5, 'beginner')
ON CONFLICT DO NOTHING;

-- INTERMEDIATE level topics
INSERT INTO topics (title, description, content, difficulty_level, estimated_hours, order_index, level) VALUES
('Advanced CSS & Responsive Design', 'Master CSS Grid, animations, and responsive layouts', 'CSS Grid, media queries, animations, preprocessors...', 'intermediate', 6.0, 1, 'intermediate'),
('JavaScript ES6+', 'Modern JavaScript features and patterns', 'Arrow functions, async/await, destructuring, modules...', 'intermediate', 5.0, 2, 'intermediate'),
('React Fundamentals', 'Build dynamic UIs with React', 'Components, props, state, hooks, lifecycle...', 'intermediate', 8.0, 3, 'intermediate'),
('Node.js & Express', 'Server-side JavaScript development', 'Node basics, Express routing, middleware, REST APIs...', 'intermediate', 7.0, 4, 'intermediate'),
('Database Fundamentals', 'Work with SQL databases', 'PostgreSQL, SQL queries, relationships, normalization...', 'intermediate', 6.0, 5, 'intermediate')
ON CONFLICT DO NOTHING;

-- ADVANCED level topics
INSERT INTO topics (title, description, content, difficulty_level, estimated_hours, order_index, level) VALUES
('Advanced React Patterns', 'State management, context, and optimization', 'Redux, Context API, performance optimization, custom hooks...', 'advanced', 10.0, 1, 'advanced'),
('RESTful API Design', 'Build scalable backend APIs', 'API architecture, authentication, validation, error handling...', 'advanced', 8.0, 2, 'advanced'),
('Database Design & Optimization', 'Advanced database concepts', 'Indexing, query optimization, transactions, migrations...', 'advanced', 7.0, 3, 'advanced'),
('Authentication & Security', 'Implement secure authentication systems', 'JWT, OAuth, password hashing, CORS, security best practices...', 'advanced', 9.0, 4, 'advanced'),
('Deployment & DevOps', 'Deploy and maintain applications', 'Docker, CI/CD, cloud platforms, monitoring, scaling...', 'advanced', 10.0, 5, 'advanced')
ON CONFLICT DO NOTHING;

-- Add prerequisites (based on new topic structure)
-- Beginner level - sequential learning
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(2, 1),  -- CSS Basics requires HTML
(3, 2),  -- JavaScript requires CSS
(4, 3),  -- DOM Manipulation requires JavaScript
(5, 1)   -- Git can be learned after HTML
ON CONFLICT DO NOTHING;

-- Intermediate level - build on beginner foundation
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(6, 2),  -- Advanced CSS requires CSS Basics (from beginner)
(7, 3),  -- JavaScript ES6+ requires JavaScript Fundamentals (from beginner)
(8, 7),  -- React requires JavaScript ES6+
(9, 7),  -- Node.js requires JavaScript ES6+
(10, 9)  -- Database Fundamentals requires Node.js
ON CONFLICT DO NOTHING;

-- Advanced level - build on intermediate foundation
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(11, 8),  -- Advanced React requires React Fundamentals
(12, 9),  -- RESTful API Design requires Node.js & Express
(13, 10), -- Database Design requires Database Fundamentals
(14, 12), -- Authentication requires API Design
(15, 14)  -- Deployment requires Authentication & Security
ON CONFLICT DO NOTHING;
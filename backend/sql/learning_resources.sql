-- Create table
CREATE TABLE IF NOT EXISTS learning_resources (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    resource_url VARCHAR(500) NOT NULL,
    resource_type VARCHAR(50) CHECK (resource_type IN ('video','article','interactive','documentation','course')),
    platform VARCHAR(100),
    duration_minutes INTEGER CHECK (duration_minutes IS NULL OR duration_minutes >= 0),
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Enforce a single resource per topic for now
    UNIQUE(topic_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_learning_resources_topic ON learning_resources(topic_id);
CREATE INDEX IF NOT EXISTS idx_learning_resources_type ON learning_resources(topic_id, resource_type);

-- Sample resources aligned with topics (1-15) using free video and article resources
INSERT INTO learning_resources (topic_id, title, resource_url, resource_type, platform, duration_minutes) VALUES
-- 1. Introduction to HTML
(1, 'HTML Crash Course', 'https://www.youtube.com/watch?v=UB1O30fR-EE', 'video', 'YouTube', 60),
-- 2. CSS Basics
(2, 'CSS Crash Course', 'https://www.youtube.com/watch?v=1Rs2ND1ryYc', 'video', 'YouTube', 45),
-- 3. JavaScript Fundamentals
(3, 'JavaScript Basics for Beginners', 'https://www.youtube.com/watch?v=W6NZfCO5SIk', 'video', 'YouTube', 90),
-- 4. DOM Manipulation
(4, 'DOM Manipulation Tutorial', 'https://www.youtube.com/watch?v=0ik6X4DJKCc', 'video', 'YouTube', 50),
-- 5. Git & Version Control
(5, 'Git Tutorial for Beginners', 'https://www.youtube.com/watch?v=8JJ101D3knE', 'video', 'YouTube', 75),
-- 6. Advanced CSS & Responsive Design
(6, 'CSS Grid Tutorial', 'https://www.youtube.com/watch?v=EFafSYg-PkI', 'video', 'YouTube', 120),
-- 7. JavaScript ES6+
(7, 'ES6 Features Tutorial', 'https://www.youtube.com/watch?v=NCwa_xi0Uuc', 'video', 'YouTube', 80),
-- 8. React Fundamentals
(8, 'React Tutorial for Beginners', 'https://www.youtube.com/watch?v=SqcY0GlETPk', 'video', 'YouTube', 120),
-- 9. Node.js & Express
(9, 'Node.js Crash Course', 'https://www.youtube.com/watch?v=Oe421EPjeBE', 'video', 'YouTube', 180),
-- 10. Database Fundamentals
(10, 'PostgreSQL Tutorial', 'https://www.youtube.com/watch?v=qw--VYLpxG4', 'video', 'YouTube', 300),
-- 11. Advanced React Patterns
(11, 'Advanced React Patterns', 'https://www.youtube.com/watch?v=GGo3MVBFr1A', 'video', 'YouTube', 75),
-- 12. RESTful API Design
(12, 'REST API Design Best Practices', 'https://www.youtube.com/watch?v=Q-BpqyOT3a8', 'video', 'YouTube', 90),
-- 13. Database Design & Optimization
(13, 'Database Indexing and Optimization', 'https://www.youtube.com/watch?v=HubezKbFL7E', 'video', 'YouTube', 60),
-- 14. Authentication & Security
(14, 'JWT Authentication Tutorial', 'https://www.youtube.com/watch?v=7Q17ubqLfaM', 'video', 'YouTube', 110),
-- 15. Deployment & DevOps
(15, 'Docker for Beginners', 'https://www.youtube.com/watch?v=9zUHg7xjIqQ', 'video', 'YouTube', 120);
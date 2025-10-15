-- Create table
CREATE TABLE IF NOT EXISTS learning_resources (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    resource_url VARCHAR(500) NOT NULL,
    resource_type VARCHAR(50),
    platform VARCHAR(100),
    duration_minutes INTEGER,
    is_free BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add sample resources (first 10 topics)
INSERT INTO learning_resources (topic_id, title, resource_url, resource_type, platform, duration_minutes) VALUES
(1, 'Programming Intro', 'https://www.youtube.com/watch?v=zOjov-2OZ0E', 'video', 'youtube', 15),
(1, 'freeCodeCamp', 'https://www.freecodecamp.org/learn', 'interactive', 'freecodecamp', 120),
(2, 'JavaScript Variables', 'https://www.youtube.com/watch?v=9emXNzqCKyg', 'video', 'youtube', 20),
(2, 'MDN Variables', 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps/Variables', 'documentation', 'mdn', 30),
(3, 'Control Flow Tutorial', 'https://www.youtube.com/watch?v=IsG4Xd6LlsM', 'video', 'youtube', 25),
(4, 'JavaScript Functions', 'https://www.youtube.com/watch?v=N8ap4k_1QEQ', 'video', 'youtube', 30),
(5, 'OOP JavaScript', 'https://www.youtube.com/watch?v=PFmuCDHHpwk', 'video', 'youtube', 40),
(6, 'Data Structures', 'https://www.youtube.com/watch?v=t2CEgPsws3U', 'video', 'youtube', 45),
(7, 'Algorithms Course', 'https://www.youtube.com/watch?v=rL8X2mlNHPM', 'video', 'youtube', 60),
(8, 'HTML & CSS', 'https://www.youtube.com/watch?v=UB1O30fR-EE', 'video', 'youtube', 60),
(9, 'Node.js Basics', 'https://www.youtube.com/watch?v=TlB_eWDSMt4', 'video', 'youtube', 90),
(10, 'SQL Tutorial', 'https://www.youtube.com/watch?v=HXV3zeQKqGY', 'video', 'youtube', 240);
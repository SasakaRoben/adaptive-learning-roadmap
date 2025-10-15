-- Clear and rebuild prerequisites
DELETE FROM topic_prerequisites;

-- Beginner topics (1-10) - sequential unlocking
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9);

-- Intermediate topics (11-20)
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(11, 10), (12, 11), (13, 11), (14, 13), (15, 14), 
(16, 12), (17, 13), (18, 17), (19, 15), (20, 19);

-- Advanced topics (21-30)
INSERT INTO topic_prerequisites (topic_id, prerequisite_topic_id) VALUES
(21, 20), (22, 21), (23, 17), (24, 14), (25, 13),
(26, 19), (27, 26), (28, 23), (29, 15), (30, 28);
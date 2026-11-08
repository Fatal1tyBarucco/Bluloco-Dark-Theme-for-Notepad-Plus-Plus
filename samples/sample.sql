-- Sample SQL code to test Bluloco Dark
-- Create table
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Complex query with JOIN and WHERE
SELECT u.username, o.order_date 
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.id > 10 
  AND o.status = 'completed'
ORDER BY o.order_date DESC
LIMIT 10;

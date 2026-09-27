-- =========================================================================
-- SQL Query Debugging and Correction
-- =========================================================================
-- Issues in the original query:
-- 1. Using a LEFT JOIN combined with a WHERE clause filtering the right table 
--    (o.order_status = 'COMPLETED') effectively turns the LEFT JOIN into an INNER JOIN, 
--    dropping customers who have no orders (since their status becomes NULL).
-- 2. Solution: Move the condition to the JOIN's ON clause to preserve all customers.
-- =========================================================================

SELECT 
    c.customer_id, 
    c.customer_name, 
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status = 'COMPLETED'
GROUP BY c.customer_id, c.customer_name;

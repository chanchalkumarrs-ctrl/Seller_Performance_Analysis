
SELECT customer_state, COUNT(DISTINCT order_id) AS total_orders
FROM olist_order_level_dataset
GROUP BY customer_state
ORDER BY total_orders DESC;

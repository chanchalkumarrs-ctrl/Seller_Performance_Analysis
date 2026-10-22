 7. Orders by category
SELECT main_category, COUNT(DISTINCT order_id) AS total_orders
FROM olist_order_level_dataset
GROUP BY main_category
ORDER BY total_orders DESC;
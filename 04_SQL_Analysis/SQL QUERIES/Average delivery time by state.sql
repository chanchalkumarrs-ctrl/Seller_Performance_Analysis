
SELECT customer_state, ROUND(AVG(delivery_days), 2) AS avg_delivery_days
FROM olist_order_level_dataset
GROUP BY customer_state
ORDER BY avg_delivery_days DESC;
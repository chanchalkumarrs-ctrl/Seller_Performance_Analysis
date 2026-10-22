 6. Monthly order trend
SELECT DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS order_month,
       COUNT(DISTINCT order_id) AS total_orders
FROM olist_order_level_dataset
GROUP BY order_month
ORDER BY order_month;

SELECT delivery_status, COUNT(*) AS order_count
FROM olist_order_level_dataset
GROUP BY delivery_status;

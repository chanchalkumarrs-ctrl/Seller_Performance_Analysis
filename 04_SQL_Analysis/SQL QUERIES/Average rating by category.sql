
SELECT main_category, ROUND(AVG(review_score), 2) AS average_rating
FROM olist_order_level_dataset
GROUP BY main_category
ORDER BY average_rating ASC;
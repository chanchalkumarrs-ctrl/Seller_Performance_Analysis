 5. Rating distribution
SELECT review_score, COUNT(*) AS review_count
FROM olist_order_level_dataset
GROUP BY review_score
ORDER BY review_score;
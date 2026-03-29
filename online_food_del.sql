USE food_delivery;

-- 1.Top-spending customers
SELECT customer_age, SUM(order_value) AS total_spent
FROM orders
GROUP BY customer_age
ORDER BY total_spent DESC
LIMIT 10;

-- 2.Age group vs order value
SELECT age_group, AVG(order_value) AS avg_order_value
FROM orders
GROUP BY age_group
ORDER BY avg_order_value DESC;

-- 3. Weekend vs weekday order patterns
SELECT day_type, COUNT(*) AS total_orders, AVG(order_value) AS avg_order_value
FROM orders
GROUP BY day_type;

-- 4. Monthly revenue trends
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, SUM(order_value) AS total_revenue
FROM orders
GROUP BY month
ORDER BY month;

-- 5. Impact of discounts on profit(Assuming discount info is embedded in profit margin — if you have a discount column, replace accordingly.)
SELECT order_status, AVG(profit_margin_pct) AS avg_profit_pct
FROM orders
GROUP BY order_status;

-- 6. High-revenue cities and cuisines
SELECT city, cuisine, SUM(order_value) AS total_revenue
FROM orders
GROUP BY city, cuisine
ORDER BY total_revenue DESC
LIMIT 10;

-- 7. Average delivery time by city
SELECT city, AVG(delivery_time) AS avg_delivery_time
FROM orders
GROUP BY city
ORDER BY avg_delivery_time;

-- 8. Distance vs delivery delay analysis
SELECT distance_km, AVG(delivery_time) AS avg_delivery_time
FROM orders
GROUP BY distance_km
ORDER BY distance_km;

-- 9. Delivery rating vs delivery time
SELECT ROUND(delivery_time,0) AS delivery_bucket, AVG(rating) AS avg_rating
FROM orders
WHERE rating IS NOT NULL
GROUP BY delivery_bucket
ORDER BY delivery_bucket;

-- 10. Top-rated restaurants(If you have a restaurant column; otherwise city+cuisine can be proxy.)
SELECT cuisine, AVG(rating) AS avg_rating
FROM orders
WHERE rating IS NOT NULL
GROUP BY cuisine
ORDER BY avg_rating DESC
LIMIT 10;

-- 11. Cancellation rate by restaurant
SELECT cuisine, 
       COUNT(CASE WHEN order_status = 'Cancelled' THEN 1 END) * 100.0 / COUNT(*) AS cancel_rate_pct
FROM orders
GROUP BY cuisine
ORDER BY cancel_rate_pct DESC;

-- 12. Cuisine-wise performance
SELECT cuisine, AVG(order_value) AS avg_order_value, AVG(rating) AS avg_rating
FROM orders
GROUP BY cuisine
ORDER BY avg_order_value DESC;

-- 13. Peak hour demand analysis
SELECT peak_hour, COUNT(*) AS total_orders, AVG(order_value) AS avg_order_value
FROM orders
GROUP BY peak_hour;

-- 14. Payment mode preferences(You don’t have a payment_mode column in schema — if you add one, query like this:)

SELECT payment_mode, COUNT(*) AS total_orders
FROM orders
GROUP BY payment_mode
ORDER BY total_orders DESC;

-- 15. Cancellation reason analysis
SELECT cancel_reason, COUNT(*) AS total_cancellations
FROM orders
WHERE order_status = 'Cancelled'
GROUP BY cancel_reason
ORDER BY total_cancellations DESC;
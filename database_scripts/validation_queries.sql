USE movie_rental_warehouse;

SELECT COUNT(*) AS total_customers
FROM dim_customer;

SELECT COUNT(*) AS total_films
FROM dim_film;

SELECT COUNT(*) AS total_rentals
FROM fact_rental;

SELECT COUNT(*) AS total_payments
FROM fact_payment;

SELECT 
    f.film_title,
    COUNT(r.rental_fact_key) AS total_rentals
FROM fact_rental r
JOIN dim_film f ON r.film_key = f.film_key
GROUP BY f.film_title
ORDER BY total_rentals DESC
LIMIT 10;

SELECT 
    s.store_id,
    SUM(p.payment_amount) AS total_revenue
FROM fact_payment p
JOIN dim_store s ON p.store_key = s.store_key
GROUP BY s.store_id
ORDER BY total_revenue DESC;

SELECT 
    d.year,
    d.month,
    SUM(p.payment_amount) AS monthly_revenue
FROM fact_payment p
JOIN dim_date d ON p.payment_date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

SELECT 
    c.full_name,
    COUNT(r.rental_fact_key) AS total_rentals
FROM fact_rental r
JOIN dim_customer c ON r.customer_key = c.customer_key
GROUP BY c.full_name
ORDER BY total_rentals DESC
LIMIT 10;

SELECT 
    f.category_name,
    COUNT(r.rental_fact_key) AS total_rentals
FROM fact_rental r
JOIN dim_film f ON r.film_key = f.film_key
GROUP BY f.category_name
ORDER BY total_rentals DESC;
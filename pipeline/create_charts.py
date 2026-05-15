import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "root"
password = quote_plus("Abcd@2026")
host = "localhost"
port = "3306"
database = "movie_rental_warehouse"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

os.makedirs("visuals", exist_ok=True)

# 1. Top rented films
top_films = pd.read_sql("""
SELECT 
    f.film_title,
    COUNT(r.rental_fact_key) AS total_rentals
FROM fact_rental r
JOIN dim_film f ON r.film_key = f.film_key
GROUP BY f.film_title
ORDER BY total_rentals DESC
LIMIT 10;
""", engine)

plt.figure(figsize=(12, 6))
plt.bar(top_films["film_title"], top_films["total_rentals"])
plt.title("Top 10 Rented Films")
plt.xlabel("Film")
plt.ylabel("Total Rentals")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("visuals/top_rented_films.png", dpi=300)
plt.close()

# 2. Revenue by store
store_revenue = pd.read_sql("""
SELECT 
    s.store_id,
    SUM(p.payment_amount) AS total_revenue
FROM fact_payment p
JOIN dim_store s ON p.store_key = s.store_key
GROUP BY s.store_id
ORDER BY total_revenue DESC;
""", engine)

plt.figure(figsize=(8, 5))
plt.bar(store_revenue["store_id"].astype(str), store_revenue["total_revenue"])
plt.title("Revenue by Store")
plt.xlabel("Store ID")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.savefig("visuals/revenue_by_store.png", dpi=300)
plt.close()

# 3. Monthly revenue trend
monthly_revenue = pd.read_sql("""
SELECT 
    d.year,
    d.month,
    SUM(p.payment_amount) AS total_revenue
FROM fact_payment p
JOIN dim_date d ON p.payment_date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
""", engine)

monthly_revenue["period"] = (
    monthly_revenue["year"].astype(str) + "-" +
    monthly_revenue["month"].astype(str)
)

plt.figure(figsize=(10, 5))
plt.plot(monthly_revenue["period"], monthly_revenue["total_revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/monthly_revenue_trend.png", dpi=300)
plt.close()

# 4. Rentals by category
category_rentals = pd.read_sql("""
SELECT 
    f.category_name,
    COUNT(r.rental_fact_key) AS total_rentals
FROM fact_rental r
JOIN dim_film f ON r.film_key = f.film_key
GROUP BY f.category_name
ORDER BY total_rentals DESC;
""", engine)

plt.figure(figsize=(10, 5))
plt.bar(category_rentals["category_name"], category_rentals["total_rentals"])
plt.title("Rentals by Film Category")
plt.xlabel("Category")
plt.ylabel("Total Rentals")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("visuals/rentals_by_category.png", dpi=300)
plt.close()

print("Charts created successfully inside visuals folder.")
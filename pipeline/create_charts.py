import os
from urllib.parse import quote_plus

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


USERNAME = "root"
PASSWORD = quote_plus("Abcd@2026")
HOST = "localhost"
PORT = "3306"
DATABASE = "movie_rental_warehouse"

OUTPUT_FOLDER = "visuals"


def get_engine():
    connection_url = (
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    )
    return create_engine(connection_url)


def save_bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename, color):
    plt.figure(figsize=(12, 6))
    plt.bar(df[x_col].astype(str), df[y_col], color=color)
    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename), dpi=300, bbox_inches="tight")
    plt.close()


def save_line_chart(df, x_col, y_col, title, xlabel, ylabel, filename, color):
    plt.figure(figsize=(10, 5))
    plt.plot(df[x_col].astype(str), df[y_col], marker="o", linewidth=2.5, color=color)
    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename), dpi=300, bbox_inches="tight")
    plt.close()


def create_charts():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    engine = get_engine()

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

    save_bar_chart(
        top_films,
        "film_title",
        "total_rentals",
        "Top 10 Rented Films",
        "Film Title",
        "Total Rentals",
        "top_rented_films.png",
        "#1565c0"
    )

    store_revenue = pd.read_sql("""
        SELECT 
            s.store_id,
            SUM(p.payment_amount) AS total_revenue
        FROM fact_payment p
        JOIN dim_store s ON p.store_key = s.store_key
        GROUP BY s.store_id
        ORDER BY total_revenue DESC;
    """, engine)

    save_bar_chart(
        store_revenue,
        "store_id",
        "total_revenue",
        "Revenue by Store",
        "Store ID",
        "Total Revenue",
        "revenue_by_store.png",
        "#2e7d32"
    )

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
        monthly_revenue["year"].astype(str)
        + "-"
        + monthly_revenue["month"].astype(str).str.zfill(2)
    )

    save_line_chart(
        monthly_revenue,
        "period",
        "total_revenue",
        "Monthly Revenue Trend",
        "Month",
        "Total Revenue",
        "monthly_revenue_trend.png",
        "#7c4cc2"
    )

    category_rentals = pd.read_sql("""
        SELECT 
            c.category_name,
            COUNT(r.rental_fact_key) AS total_rentals
        FROM fact_rental r
        JOIN dim_film f ON r.film_key = f.film_key
        JOIN bridge_film_category b ON f.film_key = b.film_key
        JOIN dim_category c ON b.category_key = c.category_key
        GROUP BY c.category_name
        ORDER BY total_rentals DESC;
    """, engine)

    save_bar_chart(
        category_rentals,
        "category_name",
        "total_rentals",
        "Rentals by Film Category",
        "Category",
        "Total Rentals",
        "rentals_by_category.png",
        "#ef6c00"
    )

    top_customers = pd.read_sql("""
        SELECT
            c.full_name,
            COUNT(r.rental_fact_key) AS total_rentals
        FROM fact_rental r
        JOIN dim_customer c ON r.customer_key = c.customer_key
        GROUP BY c.full_name
        ORDER BY total_rentals DESC
        LIMIT 10;
    """, engine)

    save_bar_chart(
        top_customers,
        "full_name",
        "total_rentals",
        "Top 10 Customers by Rentals",
        "Customer",
        "Total Rentals",
        "top_customers_by_rentals.png",
        "#c2185b"
    )

    print("Charts created successfully inside the visuals folder.")


if __name__ == "__main__":
    create_charts()
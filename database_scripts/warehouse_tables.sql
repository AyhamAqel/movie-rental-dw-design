CREATE DATABASE IF NOT EXISTS movie_rental_warehouse;
USE movie_rental_warehouse;

DROP TABLE IF EXISTS fact_payment;
DROP TABLE IF EXISTS fact_rental;
DROP TABLE IF EXISTS dim_staff;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_film;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    quarter INT,
    year INT,
    day_name VARCHAR(20)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id INT,
    full_name VARCHAR(100),
    email VARCHAR(100),
    active INT,
    address VARCHAR(255),
    district VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE dim_film (
    film_key INT PRIMARY KEY,
    film_id INT,
    film_title VARCHAR(255),
    description TEXT,
    release_year INT,
    language_name VARCHAR(50),
    category_name VARCHAR(50),
    rental_duration INT,
    rental_rate DECIMAL(5,2),
    length INT,
    replacement_cost DECIMAL(6,2),
    rating VARCHAR(10)
);

CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_id INT,
    manager_staff_id INT,
    address VARCHAR(255),
    district VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE dim_staff (
    staff_key INT PRIMARY KEY,
    staff_id INT,
    full_name VARCHAR(100),
    email VARCHAR(100),
    active INT,
    store_id INT
);

CREATE TABLE fact_rental (
    rental_fact_key INT PRIMARY KEY,
    rental_id INT,
    customer_key INT,
    film_key INT,
    store_key INT,
    staff_key INT,
    rental_date_key INT,
    return_date_key INT,
    rental_count INT,
    rental_duration_days INT,
    late_return_flag INT
);

CREATE TABLE fact_payment (
    payment_fact_key INT PRIMARY KEY,
    payment_id INT,
    rental_id INT,
    customer_key INT,
    film_key INT,
    store_key INT,
    staff_key INT,
    payment_date_key INT,
    payment_amount DECIMAL(8,2),
    payment_count INT
);
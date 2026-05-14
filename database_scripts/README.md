# Movie Rental Data Warehouse ETL Project

This project designs and implements a simple data warehouse for the Sakila Movie Rental database using Python, Pandas, SQLAlchemy, and MySQL.

## Project Objective

The goal of this project is to extract data from the OLTP Sakila database, transform it into a dimensional model, and load it into a data warehouse database for analytical reporting.

## Technologies Used

- Python
- Pandas
- SQLAlchemy
- PyMySQL
- MySQL Workbench
- Sakila Database

## Project Structure

```text
movie-rental-dw-design/
├── app.py
├── requirements.txt
├── README.md
├── database_scripts/
│   ├── warehouse_tables.sql
│   └── validation_queries.sql
├── pipeline/
│   ├── extract_stage.py
│   ├── transform_stage.py
│   └── load_stage.py
├── transformed_data/
├── visuals/
└── documentation/
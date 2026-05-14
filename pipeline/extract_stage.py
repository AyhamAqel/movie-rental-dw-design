from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine


def get_source_engine():
    username = "root"
    password = "Abcd@2026"
    host = "localhost"
    port = "3306"
    database = "sakila"

    encoded_password = quote_plus(password)

    connection_url = (
        f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}"
    )

    return create_engine(connection_url)


def extract_data():
    engine = get_source_engine()

    tables = {}

    source_tables = [
        "customer",
        "address",
        "city",
        "country",
        "film",
        "language",
        "category",
        "film_category",
        "inventory",
        "rental",
        "payment",
        "staff",
        "store"
    ]

    for table in source_tables:
        print(f"Extracting table: {table}")
        tables[table] = pd.read_sql(f"SELECT * FROM {table}", engine)

    print("Extract stage completed.")
    return tables
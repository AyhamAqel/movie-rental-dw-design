from urllib.parse import quote_plus
from sqlalchemy import create_engine, text


def get_warehouse_engine():
    username = "root"
    password = "Abcd@2026"
    host = "localhost"
    port = "3306"
    database = "movie_rental_warehouse"

    encoded_password = quote_plus(password)

    server_url = f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}"
    server_engine = create_engine(server_url)

    with server_engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
        connection.commit()

    warehouse_url = (
        f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}"
    )

    return create_engine(warehouse_url)


def load_to_warehouse(tables):
    engine = get_warehouse_engine()

    load_order = [
        "dim_date",
        "dim_customer",
        "dim_film",
        "dim_category",
        "dim_actor",
        "dim_store",
        "dim_staff",
        "bridge_film_category",
        "bridge_film_actor",
        "fact_rental",
        "fact_payment",
        "fact_inventory"
    ]

    for table_name in load_order:
        print(f"Loading table: {table_name}")

        tables[table_name].to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

    print("Load stage completed.")
import pandas as pd
import os


def build_date_dimension(rental_df, payment_df):
    rental_dates = pd.to_datetime(rental_df["rental_date"]).dt.date
    return_dates = pd.to_datetime(
        rental_df["return_date"],
        errors="coerce"
    ).dt.date

    payment_dates = pd.to_datetime(
        payment_df["payment_date"]
    ).dt.date

    all_dates = pd.concat([
        pd.Series(rental_dates),
        pd.Series(return_dates),
        pd.Series(payment_dates)
    ]).dropna().drop_duplicates()

    dim_date = pd.DataFrame({
        "full_date": pd.to_datetime(all_dates)
    })

    dim_date = dim_date.sort_values(
        "full_date"
    ).reset_index(drop=True)

    dim_date["date_key"] = (
        dim_date["full_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["day_name"] = dim_date["full_date"].dt.day_name()

    return dim_date[
        [
            "date_key",
            "full_date",
            "day",
            "month",
            "quarter",
            "year",
            "day_name"
        ]
    ]


def build_customer_dimension(customer, address, city, country):
    customer = customer.drop(columns=["last_update"], errors="ignore")
    address = address.drop(columns=["last_update"], errors="ignore")
    city = city.drop(columns=["last_update"], errors="ignore")
    country = country.drop(columns=["last_update"], errors="ignore")

    dim_customer = (
        customer
        .merge(address, on="address_id", how="left")
        .merge(city, on="city_id", how="left")
        .merge(country, on="country_id", how="left")
    )

    dim_customer["customer_key"] = range(
        1,
        len(dim_customer) + 1
    )

    dim_customer["full_name"] = (
        dim_customer["first_name"]
        + " "
        + dim_customer["last_name"]
    )

    dim_customer = dim_customer[
        [
            "customer_key",
            "customer_id",
            "full_name",
            "email",
            "active",
            "address",
            "district",
            "city",
            "country"
        ]
    ].drop_duplicates()

    return dim_customer


def build_film_dimension(
    film,
    language,
    film_category,
    category
):
    film = film.drop(columns=["last_update"], errors="ignore")
    language = language.drop(columns=["last_update"], errors="ignore")
    film_category = film_category.drop(columns=["last_update"], errors="ignore")
    category = category.drop(columns=["last_update"], errors="ignore")

    dim_film = (
        film
        .merge(
            language[["language_id", "name"]],
            on="language_id",
            how="left"
        )
        .merge(
            film_category,
            on="film_id",
            how="left"
        )
        .merge(
            category[["category_id", "name"]],
            on="category_id",
            how="left",
            suffixes=("_language", "_category")
        )
    )

    dim_film["film_key"] = range(
        1,
        len(dim_film) + 1
    )

    dim_film = dim_film.rename(columns={
        "title": "film_title",
        "name_language": "language_name",
        "name_category": "category_name"
    })

    dim_film = dim_film[
        [
            "film_key",
            "film_id",
            "film_title",
            "description",
            "release_year",
            "language_name",
            "category_name",
            "rental_duration",
            "rental_rate",
            "length",
            "replacement_cost",
            "rating"
        ]
    ].drop_duplicates()

    return dim_film


def build_store_dimension(store, address, city, country):
    store = store.drop(columns=["last_update"], errors="ignore")
    address = address.drop(columns=["last_update"], errors="ignore")
    city = city.drop(columns=["last_update"], errors="ignore")
    country = country.drop(columns=["last_update"], errors="ignore")

    dim_store = (
        store
        .merge(address, on="address_id", how="left")
        .merge(city, on="city_id", how="left")
        .merge(country, on="country_id", how="left")
    )

    dim_store["store_key"] = range(
        1,
        len(dim_store) + 1
    )

    dim_store = dim_store[
        [
            "store_key",
            "store_id",
            "manager_staff_id",
            "address",
            "district",
            "city",
            "country"
        ]
    ].drop_duplicates()

    return dim_store


def build_staff_dimension(staff):
    staff = staff.drop(columns=["last_update"], errors="ignore")

    dim_staff = staff.copy()

    dim_staff["staff_key"] = range(
        1,
        len(dim_staff) + 1
    )

    dim_staff["full_name"] = (
        dim_staff["first_name"]
        + " "
        + dim_staff["last_name"]
    )

    dim_staff = dim_staff[
        [
            "staff_key",
            "staff_id",
            "full_name",
            "email",
            "active",
            "store_id"
        ]
    ].drop_duplicates()

    return dim_staff


def build_fact_rental(
    rental,
    inventory,
    film,
    dim_customer,
    dim_film,
    dim_store,
    dim_staff
):
    rental = rental.drop(columns=["last_update"], errors="ignore")
    inventory = inventory.drop(columns=["last_update"], errors="ignore")

    fact_rental = rental.merge(
        inventory,
        on="inventory_id",
        how="left"
    )

    fact_rental["rental_date"] = pd.to_datetime(
        fact_rental["rental_date"]
    )

    fact_rental["return_date"] = pd.to_datetime(
        fact_rental["return_date"],
        errors="coerce"
    )

    fact_rental["rental_date_key"] = (
        fact_rental["rental_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    fact_rental["return_date_key"] = (
        fact_rental["return_date"]
        .dt.strftime("%Y%m%d")
    )

    fact_rental["return_date_key"] = (
        fact_rental["return_date_key"]
        .fillna(0)
        .astype(int)
    )

    fact_rental["rental_duration_days"] = (
        fact_rental["return_date"]
        - fact_rental["rental_date"]
    ).dt.days

    fact_rental = fact_rental.merge(
        film[["film_id", "rental_duration"]],
        on="film_id",
        how="left"
    )

    fact_rental["late_return_flag"] = (
        fact_rental["rental_duration_days"]
        > fact_rental["rental_duration"]
    ).astype(int)

    fact_rental["rental_count"] = 1

    fact_rental = fact_rental.merge(
        dim_customer[["customer_key", "customer_id"]],
        on="customer_id",
        how="left"
    )

    fact_rental = fact_rental.merge(
        dim_film[["film_key", "film_id"]],
        on="film_id",
        how="left"
    )

    fact_rental = fact_rental.merge(
        dim_store[["store_key", "store_id"]],
        on="store_id",
        how="left"
    )

    fact_rental = fact_rental.merge(
        dim_staff[["staff_key", "staff_id"]],
        on="staff_id",
        how="left"
    )

    fact_rental["rental_fact_key"] = range(
        1,
        len(fact_rental) + 1
    )

    fact_rental = fact_rental[
        [
            "rental_fact_key",
            "rental_id",
            "customer_key",
            "film_key",
            "store_key",
            "staff_key",
            "rental_date_key",
            "return_date_key",
            "rental_count",
            "rental_duration_days",
            "late_return_flag"
        ]
    ]

    return fact_rental


def build_fact_payment(
    payment,
    rental,
    inventory,
    dim_customer,
    dim_film,
    dim_store,
    dim_staff
):
    payment = payment.drop(columns=["last_update"], errors="ignore")
    rental = rental.drop(columns=["last_update"], errors="ignore")
    inventory = inventory.drop(columns=["last_update"], errors="ignore")

    fact_payment = (
        payment
        .merge(
            rental[["rental_id", "inventory_id"]],
            on="rental_id",
            how="left"
        )
        .merge(
            inventory[["inventory_id", "film_id", "store_id"]],
            on="inventory_id",
            how="left"
        )
    )

    fact_payment["payment_date"] = pd.to_datetime(
        fact_payment["payment_date"]
    )

    fact_payment["payment_date_key"] = (
        fact_payment["payment_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    fact_payment["payment_count"] = 1

    fact_payment = fact_payment.merge(
        dim_customer[["customer_key", "customer_id"]],
        on="customer_id",
        how="left"
    )

    fact_payment = fact_payment.merge(
        dim_film[["film_key", "film_id"]],
        on="film_id",
        how="left"
    )

    fact_payment = fact_payment.merge(
        dim_store[["store_key", "store_id"]],
        on="store_id",
        how="left"
    )

    fact_payment = fact_payment.merge(
        dim_staff[["staff_key", "staff_id"]],
        on="staff_id",
        how="left"
    )

    fact_payment["payment_fact_key"] = range(
        1,
        len(fact_payment) + 1
    )

    fact_payment = fact_payment.rename(columns={
        "amount": "payment_amount"
    })

    fact_payment = fact_payment[
        [
            "payment_fact_key",
            "payment_id",
            "rental_id",
            "customer_key",
            "film_key",
            "store_key",
            "staff_key",
            "payment_date_key",
            "payment_amount",
            "payment_count"
        ]
    ]

    return fact_payment


def build_fact_inventory(inventory, dim_film, dim_store):
    inventory = inventory.drop(columns=["last_update"], errors="ignore")

    fact_inventory = inventory.copy()

    fact_inventory["inventory_count"] = 1
    fact_inventory["available_flag"] = 1

    fact_inventory = fact_inventory.merge(
        dim_film[["film_key", "film_id"]],
        on="film_id",
        how="left"
    )

    fact_inventory = fact_inventory.merge(
        dim_store[["store_key", "store_id"]],
        on="store_id",
        how="left"
    )

    fact_inventory["inventory_fact_key"] = range(
        1,
        len(fact_inventory) + 1
    )

    fact_inventory = fact_inventory[
        [
            "inventory_fact_key",
            "inventory_id",
            "film_key",
            "store_key",
            "inventory_count",
            "available_flag"
        ]
    ]

    return fact_inventory


def save_csv_outputs(tables):
    output_folder = "transformed_data"

    os.makedirs(output_folder, exist_ok=True)

    for table_name, df in tables.items():
        path = os.path.join(
            output_folder,
            f"{table_name}.csv"
        )

        df.to_csv(path, index=False)

        print(f"Saved CSV: {path}")


def transform_data(raw):
    print("Transform stage started.")

    dim_date = build_date_dimension(
        raw["rental"],
        raw["payment"]
    )

    dim_customer = build_customer_dimension(
        raw["customer"],
        raw["address"],
        raw["city"],
        raw["country"]
    )

    dim_film = build_film_dimension(
        raw["film"],
        raw["language"],
        raw["film_category"],
        raw["category"]
    )

    dim_store = build_store_dimension(
        raw["store"],
        raw["address"],
        raw["city"],
        raw["country"]
    )

    dim_staff = build_staff_dimension(
        raw["staff"]
    )

    fact_rental = build_fact_rental(
        raw["rental"],
        raw["inventory"],
        raw["film"],
        dim_customer,
        dim_film,
        dim_store,
        dim_staff
    )

    fact_payment = build_fact_payment(
        raw["payment"],
        raw["rental"],
        raw["inventory"],
        dim_customer,
        dim_film,
        dim_store,
        dim_staff
    )

    fact_inventory = build_fact_inventory(
        raw["inventory"],
        dim_film,
        dim_store
    )

    transformed_tables = {
        "dim_date": dim_date,
        "dim_customer": dim_customer,
        "dim_film": dim_film,
        "dim_store": dim_store,
        "dim_staff": dim_staff,
        "fact_rental": fact_rental,
        "fact_payment": fact_payment,
        "fact_inventory": fact_inventory
    }

    save_csv_outputs(transformed_tables)

    print("Transform stage completed.")

    return transformed_tables
from pipeline.extract_stage import extract_data
from pipeline.transform_stage import transform_data
from pipeline.load_stage import load_to_warehouse


def main():
    print("Starting Movie Rental Data Warehouse ETL...")

    raw_tables = extract_data()

    transformed_tables = transform_data(raw_tables)

    load_to_warehouse(transformed_tables)

    print("ETL process completed successfully!")


if __name__ == "__main__":
    main()
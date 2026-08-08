import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "customer_revenue_platform"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

processed_path = Path("Dataset/processed")

files = {
    "customers": "olist_customers_dataset_cleaned.csv",
    "orders": "olist_orders_dataset_cleaned.csv",
    "order_items": "olist_order_items_dataset_cleaned.csv",
    "products": "olist_products_dataset_cleaned.csv",
    "sellers": "olist_sellers_dataset_cleaned.csv",
    "payments": "olist_order_payments_dataset_cleaned.csv",
    "reviews": "olist_order_reviews_dataset_cleaned.csv",
    "geolocation": "olist_geolocation_dataset_cleaned.csv",
    "category_translation": "product_category_name_translation_cleaned.csv",
    }

for table_name, file_name in files.items():

    csv_path = processed_path / file_name

    print(f"Loading {table_name}...")

    df = pd.read_csv(csv_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"✓ Loaded {len(df)} rows into {table_name}")


    # ==========================================
# LOAD REPORT FILES
# ==========================================

reports_path = Path("reports")

report_files = {
    "cleaning_report": "cleaning_report.csv",
    "validation_report": "validation_report.csv"
}

for table_name, file_name in report_files.items():

    csv_path = reports_path / file_name

    if csv_path.exists():

        print(f"Loading {table_name}...")

        df = pd.read_csv(csv_path)

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        print(f"✓ Loaded {len(df)} rows into {table_name}")

        

print("\nAll tables loaded successfully.")
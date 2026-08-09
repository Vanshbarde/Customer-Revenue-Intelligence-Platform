from sqlalchemy import create_engine
import pandas as pd


DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "customer_revenue_platform"


engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def log_pipeline_run(
    pipeline_name,
    start_time,
    end_time,
    status,
    records_processed
):

    run_df = pd.DataFrame([
        {
            "pipeline_name": pipeline_name,
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "records_processed": records_processed
        }
    ])

    run_df.to_sql(
        "pipeline_runs",
        con=engine,
        if_exists="append",
        index=False
    )
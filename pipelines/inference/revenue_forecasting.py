import pandas as pd
import joblib

from pathlib import Path
from sqlalchemy import create_engine


def run_revenue_forecasting():

    # Database Connection
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "customer_revenue_platform"

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print("Loading customer features...")

    query = """
    SELECT *
    FROM customer_features
    """

    df = pd.read_sql(
        query,
        engine
    )

    # Save actual revenue before dropping
    actual_revenue = df["total_revenue"].copy()

    drop_cols = [
        "customer_unique_id",
        "total_revenue",
        "first_purchase",
        "last_purchase"
    ]

    X = df.drop(
        columns=drop_cols,
        errors="ignore"
    )

    # Same preprocessing as training
    X = pd.get_dummies(
        X,
        drop_first=True
    )

    MODEL_DIR = (
        Path.cwd()
        / "Trained_Models"
        / "revenue_forecasting"
    )

    print("Loading model...")

    model = joblib.load(
        MODEL_DIR / "revenue_forecast.pkl"
    )

    feature_columns = joblib.load(
        MODEL_DIR / "feature_columns.pkl"
    )

    # Match training columns
    X = X.reindex(
        columns=feature_columns,
        fill_value=0
    )

    print("Generating forecasts...")

    predicted_revenue = model.predict(X)

    forecast_results = pd.DataFrame({
        "customer_unique_id":
            df["customer_unique_id"],

        "actual_revenue":
            actual_revenue,

        "predicted_revenue":
            predicted_revenue
    })

    forecast_results.to_sql(
        "revenue_forecasts",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        "Revenue Forecasting Inference Completed"
    )


if __name__ == "__main__":
    run_revenue_forecasting()
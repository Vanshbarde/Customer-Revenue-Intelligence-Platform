import pandas as pd
import joblib
from pathlib import Path
from sqlalchemy import create_engine


def run_customer_segmentation():

    # Database Connection
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "customer_revenue_platform"

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Load Customer Features
    query = """
    SELECT *
    FROM customer_features
    """

    customer_df = pd.read_sql(
        query,
        engine
    )

    # Features Used During Training
    segmentation_features = [
        "total_orders",
        "total_revenue",
        "avg_order_value",
        "avg_review_score",
        "customer_lifetime_days",
        "recency_days",
        "customer_tenure_months",
        "revenue_per_day",
        "customer_value_score"
    ]

    # Prepare Data
    X = customer_df[segmentation_features].copy()

    X = X.fillna(
        X.median(numeric_only=True)
    )

    # Load Saved Models
    MODEL_DIR = (
        Path.cwd()
        / "Trained_Models"
        / "customer_segmentation"
    )

    scaler = joblib.load(
        MODEL_DIR / "segmentation_scaler.pkl"
    )

    kmeans = joblib.load(
        MODEL_DIR / "kmeans_model.pkl"
    )

    # Transform Features
    X_scaled = scaler.transform(X)

    # Predict Segments
    customer_df["customer_segment"] = (
        kmeans.predict(X_scaled)
    )

    # Segment Labels
    segment_mapping = {
        0: "At Risk",
        1: "Potential Loyalists",
        2: "VIP Customers",
        3: "Low Value Customers",
        4: "Loyal Customers"
    }

    customer_df["segment_name"] = (
        customer_df["customer_segment"]
        .map(segment_mapping)
    )

    # Final Output
    result = customer_df[
        [
            "customer_unique_id",
            "customer_segment",
            "segment_name"
        ]
    ]

    # Save to PostgreSQL
    result.to_sql(
        "customer_segments",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Customer Segmentation Inference Completed")


if __name__ == "__main__":
    run_customer_segmentation()
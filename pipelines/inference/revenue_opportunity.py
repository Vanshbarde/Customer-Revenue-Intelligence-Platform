import pandas as pd

from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler


def run_revenue_opportunity():

    # Database Connection
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "customer_revenue_platform"

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print("Loading data...")

    customer_features = pd.read_sql(
        """
        SELECT *
        FROM customer_features
        """,
        engine
    )

    purchase_predictions = pd.read_sql(
        """
        SELECT *
        FROM purchase_predictions
        """,
        engine
    )

    customer_segments = pd.read_sql(
        """
        SELECT *
        FROM customer_segments
        """,
        engine
    )

    print("Merging datasets...")

    revenue_df = (
        customer_features
        .merge(
            purchase_predictions,
            on="customer_unique_id",
            how="left"
        )
        .merge(
            customer_segments,
            on="customer_unique_id",
            how="left"
        )
    )

    print("Calculating scores...")

    scaler = MinMaxScaler()

    revenue_df[
        [
            "revenue_score",
            "value_score",
            "recency_score"
        ]
    ] = scaler.fit_transform(
        revenue_df[
            [
                "total_revenue",
                "customer_value_score",
                "recency_days"
            ]
        ]
    )

    revenue_df["recency_score"] = (
        1 - revenue_df["recency_score"]
    )

    PURCHASE_WEIGHT = 0.30
    VALUE_WEIGHT = 0.30
    REVENUE_WEIGHT = 0.20
    RECENCY_WEIGHT = 0.20

    revenue_df["revenue_opportunity_score"] = (
        revenue_df["purchase_probability"] * PURCHASE_WEIGHT
        +
        revenue_df["value_score"] * VALUE_WEIGHT
        +
        revenue_df["revenue_score"] * REVENUE_WEIGHT
        +
        revenue_df["recency_score"] * RECENCY_WEIGHT
    ) * 100

    revenue_df["opportunity_level"] = pd.cut(
        revenue_df["revenue_opportunity_score"],
        bins=[0, 40, 70, 100],
        labels=[
            "Low",
            "Medium",
            "High"
        ]
    )

    print("Saving revenue opportunity scores...")

    revenue_df.to_sql(
        "revenue_opportunity_scores",
        con=engine,
        if_exists="replace",
        index=False
    )

    summary = (
        revenue_df
        .groupby("opportunity_level")
        .agg({
            "customer_unique_id": "count",
            "total_revenue": "mean",
            "purchase_probability": "mean",
            "revenue_opportunity_score": "mean"
        })
        .reset_index()
    )

    summary.to_sql(
        "revenue_opportunity_summary",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        "Revenue Opportunity Inference Completed"
    )


if __name__ == "__main__":
    run_revenue_opportunity()
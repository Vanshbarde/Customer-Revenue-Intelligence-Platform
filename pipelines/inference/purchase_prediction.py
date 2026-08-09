import pandas as pd
import joblib
from pathlib import Path
from sqlalchemy import create_engine


def run_purchase_prediction():

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

    customer_features = pd.read_sql(
        """
        SELECT *
        FROM customer_features
        """,
        engine
    )

    # ----------------------------------
    # Data Cleaning (same as training)
    # ----------------------------------

    customer_features["review_category"] = (
        customer_features["review_category"]
        .fillna("Unknown")
    )

    customer_features["recency_group"] = (
        customer_features["recency_group"]
        .fillna("Unknown")
    )

    # ----------------------------------
    # Remove Training-only Columns
    # ----------------------------------

    leakage_columns = [
        "next_purchase_date",
        "days_until_next_purchase"
    ]

    X = customer_features.drop(
        columns=[
            "customer_unique_id",
            "repeat_customer",
            "first_purchase",
            "last_purchase"
        ] + [
            col for col in leakage_columns
            if col in customer_features.columns
        ],
        errors="ignore"
    )

    # ----------------------------------
    # Same Encoding as Training
    # ----------------------------------

    X = pd.get_dummies(
        X,
        drop_first=True
    )

    # ----------------------------------
    # Load Saved Features
    # ----------------------------------

    MODEL_DIR = (
        Path.cwd()
        / "Trained_Models"
        / "purchase_prediction"
    )

    feature_columns = joblib.load(
        MODEL_DIR / "feature_columns.pkl"
    )

    # ----------------------------------
    # Match Training Columns
    # ----------------------------------

    X = X.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # ----------------------------------
    # Load Model
    # ----------------------------------

    model = joblib.load(
        MODEL_DIR / "xgboost.pkl"
    )

    print("Running predictions...")

    y_pred = model.predict(X)

    y_prob = model.predict_proba(X)[:, 1]

    # ----------------------------------
    # Create Output Table
    # ----------------------------------

    prediction_results = pd.DataFrame({
        "customer_unique_id":
            customer_features["customer_unique_id"],
        "prediction":
            y_pred,
        "purchase_probability":
            y_prob
    })

    # ----------------------------------
    # Save Predictions
    # ----------------------------------

    prediction_results.to_sql(
        "purchase_predictions",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        "Purchase Prediction Inference Completed"
    )


if __name__ == "__main__":
    run_purchase_prediction()
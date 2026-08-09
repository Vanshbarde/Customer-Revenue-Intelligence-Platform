import papermill as pm
from datetime import datetime

print("=" * 60)
print("TRAINING PIPELINE STARTED")
print(datetime.now())
print("=" * 60)

from pathlib import Path
import papermill as pm

BASE_DIR = Path(__file__).resolve().parent.parent

notebooks = [
    BASE_DIR / "notebooks" / "feature_engineering.ipynb",
    BASE_DIR / "notebooks" / "customer_segmentation.ipynb",
    BASE_DIR / "notebooks" / "Logistic_Regression.ipynb",
    BASE_DIR / "notebooks" / "Random_Forest.ipynb",
    BASE_DIR / "notebooks" / "XGBoost.ipynb",
    BASE_DIR / "notebooks" / "model_metrics.ipynb",
    BASE_DIR / "notebooks" / "Product_Recommendation.ipynb",
    BASE_DIR / "notebooks" / "Revenue_Opportunity_Score.ipynb",
    BASE_DIR / "notebooks" / "Revenue_Forecasting.ipynb"
]

for notebook in notebooks:

    print(f"\nRunning: {notebook}")

    pm.execute_notebook(
        notebook,
        notebook
    )

    print(f"Completed: {notebook}")

print("\n" + "=" * 60)
print("TRAINING PIPELINE COMPLETED")
print(datetime.now())
print("=" * 60)
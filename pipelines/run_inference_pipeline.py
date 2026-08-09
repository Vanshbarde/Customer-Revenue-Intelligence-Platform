import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

PIPELINES = [

    BASE_DIR / "inference" / "customer_segmentation.py",

    BASE_DIR / "inference" / "purchase_prediction.py",

    BASE_DIR / "inference" / "revenue_opportunity.py",

    BASE_DIR / "inference" / "revenue_forecasting.py"
]


for pipeline in PIPELINES:

    print(f"\nRunning: {pipeline}")

    result = subprocess.run(
        [sys.executable, str(pipeline)]
    )

    if result.returncode != 0:

        print(
            f"FAILED: {pipeline}"
        )

        sys.exit(1)

    print(
        f"Completed: {pipeline}"
    )


print(
    "\nInference Pipeline Completed Successfully"
)
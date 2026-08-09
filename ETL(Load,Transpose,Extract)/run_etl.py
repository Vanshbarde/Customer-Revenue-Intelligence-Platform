"""
==========================================================
ETL Pipeline Runner
Customer Revenue Opportunity Intelligence Platform

Purpose:
    Execute the complete ETL pipeline for all datasets.

Workflow
--------
1. Read dataset configuration
2. Load raw dataset
3. Validate columns
4. Clean dataset
5. Save cleaned dataset
6. Generate cleaning report
7. Continue with next dataset

=================================================
"""


# importing util for logging and pipeline run tracking the date and time of the run
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))

from datetime import datetime

from utils.pipeline_logger import (
    log_pipeline_run
)



import time
import logging
import subprocess
import sys
from pathlib import Path

import pandas as pd

from cleaning import (
    standardize_column_names,
    validate_required_columns,
    convert_blank_to_nan,
    remove_duplicate_rows,
    remove_missing_primary_key,
    clean_text_columns,
    convert_numeric_columns,
    convert_date_columns,
    standardize_case,
    reset_dataframe,
    cleaning_report
)

from config import (
    DATASETS,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    REPORT_PATH
)

from validation import run_validation_pipeline

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Create Required Folders
# ---------------------------------------------------------

def create_directories():

    """
    Create required folders if they do not exist.
    """

    RAW_DATA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    PROCESSED_DATA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )


# ---------------------------------------------------------
# Process One Dataset
# ---------------------------------------------------------

def process_dataset(
    dataset_name: str,
    config: dict
):

    """
    Generic ETL function.

    This function can clean ANY dataset
    simply by reading the configuration.
    """

    logger.info("=" * 60)
    logger.info(f"Processing Dataset : {dataset_name}")
    logger.info("=" * 60)

    start_time = time.time()

    input_file = RAW_DATA_PATH / config["input_file"]

    output_file = PROCESSED_DATA_PATH / config["output_file"]

    if not input_file.exists():

        raise FileNotFoundError(

            f"Dataset not found:\n{input_file}"

        )

    # ---------------------------------------------
    # Read Dataset
    # ---------------------------------------------

    df = pd.read_csv(input_file)

    rows_before = len(df)

    logger.info(f"Rows Loaded : {rows_before}")

    # ---------------------------------------------
    # Standardize Column Names
    # ---------------------------------------------

    df = standardize_column_names(df)

    # ---------------------------------------------
    # Validate Required Columns
    # ---------------------------------------------

    validate_required_columns(

        df,

        config["required_columns"]

    )

    # ---------------------------------------------
    # Convert Blank Values
    # ---------------------------------------------

    df = convert_blank_to_nan(df)

    # ---------------------------------------------
    # Remove Duplicates
    # ---------------------------------------------

    df, duplicates_removed = remove_duplicate_rows(df)

    logger.info(

        f"Duplicates Removed : {duplicates_removed}"

    )

    # ---------------------------------------------
    # Remove Missing Primary Key
    # ---------------------------------------------

    df, pk_removed = remove_missing_primary_key(

        df,

        config["primary_key"]

    )

    logger.info(

        f"Missing Primary Key Removed : {pk_removed}"

    )

    # ---------------------------------------------
    # Clean Text Columns
    # ---------------------------------------------

    df = clean_text_columns(df)

    # ---------------------------------------------
    # Convert Numeric Columns
    # ---------------------------------------------

    df = convert_numeric_columns(

        df,

        config["numeric_columns"]

    )

    # ---------------------------------------------
    # Convert Date Columns
    # ---------------------------------------------

    df = convert_date_columns(

        df,

        config["date_columns"]

    )


        # ---------------------------------------------
    # Standardize Text Case
    # ---------------------------------------------

    df = standardize_case(

        df,

        title_columns=config["title_columns"],

        upper_columns=config["upper_columns"],

        lower_columns=config["lower_columns"]

    )

    # ---------------------------------------------
    # Reset DataFrame Index
    # ---------------------------------------------

    df = reset_dataframe(df)

    rows_after = len(df)

    # ---------------------------------------------
    # Save Cleaned Dataset
    # ---------------------------------------------

    df.to_csv(

        output_file,

        index=False

    )

    logger.info(

        f"Cleaned dataset saved to : {output_file}"

    )

    # ---------------------------------------------
    # Generate Cleaning Report
    # ---------------------------------------------

    report = cleaning_report(

        rows_before=rows_before,

        rows_after=rows_after,

        duplicates_removed=duplicates_removed,

        primary_key_removed=pk_removed

    )

    # ---------------------------------------------
    # Additional Report Information
    # ---------------------------------------------

    report["Dataset"] = dataset_name

    report["Execution Time (Seconds)"] = round(

        time.time() - start_time,

        2

    )

    report["Input File"] = config["input_file"]

    report["Output File"] = config["output_file"]

    logger.info(

        f"Rows After Cleaning : {rows_after}"

    )

    logger.info(

        f"Execution Time : {report['Execution Time (Seconds)']} sec"

    )

    logger.info("=" * 60)

    return report


# ---------------------------------------------------------
# Run Complete ETL Pipeline
# ---------------------------------------------------------

def run_pipeline():

    """
    Execute the complete ETL pipeline.

    Returns
    -------
    list
        Cleaning report for every dataset.
    """

    reports = []

    total_datasets = len(DATASETS)

    success = 0

    failed = 0

    logger.info("")

    logger.info("=" * 70)

    logger.info("STARTING CUSTOMER REVENUE ETL PIPELINE")

    logger.info("=" * 70)

    logger.info("")

    create_directories()

    pipeline_start = time.time()

    # ---------------------------------------------
    # Loop Through Every Dataset
    # ---------------------------------------------


    for dataset_name, config in DATASETS.items():

        try:

            report = process_dataset(

                dataset_name,

                config

            )

            reports.append(report)

            success += 1

        except Exception as e:

            logger.exception(

                f"Error while processing {dataset_name}"

            )

            failed += 1

            reports.append(

                {

                    "Dataset": dataset_name,

                    "Status": "FAILED",

                    "Error": str(e)

                }

            )

    pipeline_time = round(

        time.time() - pipeline_start,

        2

    )

    logger.info("")

    logger.info("=" * 70)

    logger.info("PIPELINE EXECUTION COMPLETED")

    logger.info("=" * 70)

    logger.info(f"Total Datasets : {total_datasets}")

    logger.info(f"Successful     : {success}")

    logger.info(f"Failed         : {failed}")

    logger.info(f"Total Time     : {pipeline_time} seconds")

    logger.info("=" * 70)

    return reports


# ---------------------------------------------------------
# Load Processed Tables Into PostgreSQL
# ---------------------------------------------------------

def load_processed_tables_to_postgres():

    """
    Load processed CSV files and report tables into PostgreSQL.
    """

    logger.info("")
    logger.info("=" * 80)
    logger.info("LOADING PROCESSED TABLES INTO POSTGRESQL")
    logger.info("=" * 80)

    script_path = Path(__file__).parent / "load_to_postgres.py"

    subprocess.run(

        [sys.executable, str(script_path)],

        check=True

    )

    logger.info("PostgreSQL loading completed successfully.")


    # ---------------------------------------------------------
# Save Cleaning Report
# ---------------------------------------------------------

def save_cleaning_report(reports):

    """
    Save the complete ETL cleaning report as a CSV file.
    """

    if not reports:

        logger.warning("No reports available to save.")

        return

    report_df = pd.DataFrame(reports)

    report_file = REPORT_PATH / "cleaning_report.csv"

    report_df.to_csv(

        report_file,

        index=False

    )

    logger.info("")

    logger.info("=" * 70)

    logger.info("CLEANING REPORT GENERATED")

    logger.info("=" * 70)

    logger.info(f"Report Location : {report_file}")

    logger.info("=" * 70)


# ---------------------------------------------------------
# Display Final Summary
# ---------------------------------------------------------

def print_summary(reports):

    """
    Display ETL summary on the console.
    """

    print("\n")

    print("=" * 80)
    print(" CUSTOMER REVENUE OPPORTUNITY INTELLIGENCE PLATFORM ")
    print(" ETL PIPELINE SUMMARY ")
    print("=" * 80)

    success = 0
    failed = 0

    for report in reports:

        dataset = report.get("Dataset", "Unknown")

        status = report.get("Status", "SUCCESS")

        if status == "FAILED":

            failed += 1

            print(f"❌ {dataset:<25} FAILED")

        else:

            success += 1

            rows_before = report.get("Rows Before", "-")

            rows_after = report.get("Rows After", "-")

            duplicates = report.get("Duplicates Removed", "-")

            pk = report.get(

                "Rows Removed (Missing Primary Key)",

                "-"

            )

            print(

                f"✅ {dataset:<25}"

                f"Rows:{rows_before} -> {rows_after}"

                f" | Duplicates:{duplicates}"

                f" | Missing PK:{pk}"

            )

    print("-" * 80)

    print(f"Successful Datasets : {success}")

    print(f"Failed Datasets     : {failed}")

    print(f"Total Datasets      : {len(reports)}")

    print("=" * 80)

    print("\nETL Pipeline Completed Successfully.\n")


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def main():

    pipeline_start = time.time()

    start_time = datetime.now()

    try:

        logger.info("")

        logger.info("=" * 80)

        logger.info("STARTING ETL PIPELINE")

        logger.info("=" * 80)

        reports = run_pipeline()

        records_processed = 0

        for report in reports:

            if "Rows After" in report:

                records_processed += report["Rows After"]

        save_cleaning_report(
            reports
        )

        # =====================================================
        # VALIDATION PIPELINE
        # =====================================================

        logger.info("")

        logger.info("=" * 80)

        logger.info("STARTING VALIDATION PIPELINE")

        logger.info("=" * 80)

        validation_result = run_validation_pipeline(
            DATASETS
        )

        if validation_result["critical_failures"] == 0:

            if validation_result["warning_failures"] > 0:

                logger.warning(
                    "Validation completed with warnings."
                )

            else:

                logger.info(
                    "Validation completed successfully."
                )

            load_processed_tables_to_postgres()

            logger.info(
                "PostgreSQL load completed successfully."
            )

        else:

            logger.error(
                f"Critical validation failures detected: "
                f"{validation_result['critical_failures']}"
            )

            logger.error(
                "Skipping PostgreSQL load."
            )


        print_summary(
            reports
        )

        pipeline_end = round(
            time.time() - pipeline_start,
            2
        )

        logger.info("")

        logger.info("=" * 80)

        logger.info(
            f"TOTAL PIPELINE EXECUTION TIME : "
            f"{pipeline_end} seconds"
        )

        logger.info("=" * 80)

        logger.info("")

        end_time = datetime.now()

        log_pipeline_run(
            pipeline_name="ETL",
            start_time=start_time,
            end_time=end_time,
            status="Success",
            records_processed=records_processed
        )

    except Exception as e:

        end_time = datetime.now()

        log_pipeline_run(
            pipeline_name="ETL",
            start_time=start_time,
            end_time=end_time,
            status="Failed",
            records_processed=0
        )

        raise e


    
    logger.info("=" * 80)

    logger.info("")




      
# ---------------------------------------------------------
# Execute Pipeline
# ---------------------------------------------------------

if __name__ == "__main__":

    main()

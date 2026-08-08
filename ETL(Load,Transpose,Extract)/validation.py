"""
==========================================================
Validation Module
Customer Revenue Opportunity Intelligence Platform

Purpose:
    Generic data validation functions for all datasets.

Author:
    Your Name

==========================================================
"""

import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd


# ======================================================
# Logger Configuration
# ======================================================

logger = logging.getLogger(__name__)


# ======================================================
# Validation Report Creator
# ======================================================

def create_validation_report() -> List[Dict]:
    """
    Create an empty validation report.

    Returns
    -------
    List[Dict]
        Empty list used to store validation results.
    """

    return []


# ======================================================
# Add Validation Result
# ======================================================

def add_validation_result(
    report: List[Dict],
    dataset: str,
    validation_name: str,
    status: str,
    invalid_rows: int,
    remarks: str = ""
) -> None:
    """
    Add one validation result to the report.

    Parameters
    ----------
    report : list
        Validation report list.

    dataset : str
        Dataset name.

    validation_name : str
        Name of validation performed.

    status : str
        PASS / FAIL

    invalid_rows : int
        Number of invalid rows.

    remarks : str
        Additional information.
    """

    report.append({

        "Dataset": dataset,

        "Validation": validation_name,

        "Status": status,

        "Invalid Rows": invalid_rows,

        "Remarks": remarks

    })


# ======================================================
# Save Validation Report
# ======================================================

def save_validation_report(
    report: List[Dict],
    output_path: Path
) -> None:
    """
    Save validation report as CSV.

    Parameters
    ----------
    report : list
        Validation report.

    output_path : Path
        CSV output path.
    """

    report_df = pd.DataFrame(report)

    report_df.to_csv(

        output_path,

        index=False

    )

    logger.info("Validation report saved successfully.")

    logger.info(output_path)

    # ======================================================
# Validate Required Columns
# ======================================================

def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list
) -> tuple[bool, int, str]:
    """
    Validate that all required columns exist.
    """

    missing = [

        col

        for col in required_columns

        if col not in df.columns

    ]

    if missing:

        return (

            False,

            len(missing),

            f"Missing columns: {missing}"

        )

    return (

        True,

        0,

        "All required columns exist."

    )


# ======================================================
# Validate NOT NULL Columns
# ======================================================

def validate_not_null_columns(
    df: pd.DataFrame,
    columns: list
) -> tuple[bool, int, str]:
    """
    Validate columns that should not contain NULL values.
    """

    invalid_rows = 0

    failed_columns = []

    for col in columns:

        if col in df.columns:

            missing = df[col].isna().sum()

            if missing > 0:

                invalid_rows += missing

                failed_columns.append(

                    f"{col} ({missing})"

                )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(failed_columns)

        )

    return (

        True,

        0,

        "No NULL values."

    )


# ======================================================
# Validate Unique Columns
# ======================================================

def validate_unique_columns(
    df: pd.DataFrame,
    columns: list
) -> tuple[bool, int, str]:
    """
    Validate uniqueness of one or more columns.
    """

    invalid_rows = 0

    duplicate_columns = []

    for col in columns:

        if col in df.columns:

            duplicates = df.duplicated(

                subset=[col]

            ).sum()

            if duplicates > 0:

                invalid_rows += duplicates

                duplicate_columns.append(

                    f"{col} ({duplicates})"

                )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(duplicate_columns)

        )

    return (

        True,

        0,

        "Unique constraint passed."

    )


# ======================================================
# Validate Composite Unique Columns
# ======================================================

def validate_composite_unique_columns(
    df: pd.DataFrame,
    composite_keys: list
) -> tuple[bool, int, str]:
    """
    Validate composite primary keys.
    """

    invalid_rows = 0

    failed_keys = []

    for key in composite_keys:

        duplicates = df.duplicated(

            subset=key

        ).sum()

        if duplicates > 0:

            invalid_rows += duplicates

            failed_keys.append(

                f"{key} ({duplicates})"

            )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(failed_keys)

        )

    return (

        True,

        0,

        "Composite key validation passed."

    )


# ======================================================
# Validate Numeric Ranges
# ======================================================

def validate_numeric_ranges(
    df: pd.DataFrame,
    rules: dict
) -> tuple[bool, int, str]:
    """
    Validate numeric ranges.

    Example

    payment_value:
        (0, None)

    review_score:
        (1,5)
    """

    invalid_rows = 0

    failed_columns = []

    for col, limits in rules.items():

        if col not in df.columns:

            continue

        minimum, maximum = limits

        invalid = pd.Series(False, index=df.index)

        if minimum is not None:

            invalid |= df[col] < minimum

        if maximum is not None:

            invalid |= df[col] > maximum

        count = invalid.sum()

        if count > 0:

            invalid_rows += count

            failed_columns.append(

                f"{col} ({count})"

            )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(failed_columns)

        )

    return (

        True,

        0,

        "Numeric validation passed."

    )


# ======================================================
# Validate Allowed Values
# ======================================================

def validate_allowed_values(
    df: pd.DataFrame,
    rules: dict
) -> tuple[bool, int, str]:
    """
    Validate categorical values.
    """

    invalid_rows = 0

    failed_columns = []

    for col, allowed in rules.items():

        if col not in df.columns:

            continue

        invalid = ~df[col].isin(allowed)

        count = invalid.sum()

        if count > 0:

            invalid_rows += count

            failed_columns.append(

                f"{col} ({count})"

            )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(failed_columns)

        )

    return (

        True,

        0,

        "Allowed value validation passed."

    )


# ======================================================
# Validate Date Sequence
# ======================================================

def validate_date_sequence(
    df: pd.DataFrame,
    sequences: list
) -> tuple[bool, int, str]:
    """
    Validate that the earlier date in each pair does not
    occur after the later date.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset to validate.

    sequences : list of tuple
        List of (earlier_column, later_column) pairs.
        Example: [("order_purchase_timestamp", "order_approved_at")]
    """

    invalid_rows = 0

    failed_pairs = []

    for earlier_col, later_col in sequences:

        if earlier_col not in df.columns or later_col not in df.columns:

            continue

        earlier = pd.to_datetime(df[earlier_col], errors="coerce")

        later = pd.to_datetime(df[later_col], errors="coerce")

        # Only flag rows where BOTH dates are present and out of order.
        # Rows with a missing date (e.g. not yet delivered) are not
        # sequence violations - they're handled by NOT NULL validation.
        invalid = earlier.notna() & later.notna() & (earlier > later)

        count = invalid.sum()

        if count > 0:

            invalid_rows += count

            failed_pairs.append(

                f"{earlier_col} > {later_col} ({count})"

            )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(failed_pairs)

        )

    return (

        True,

        0,

        "Date sequence validation passed."

    )


# ======================================================
# Validate Foreign Keys
# ======================================================

def validate_foreign_keys(
    df: pd.DataFrame,
    foreign_keys: list,
    processed_path: Path = None
) -> tuple[bool, int, str]:
    """
    Validate that values in a column exist in the referenced
    dataset's cleaned output file.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset to validate.

    foreign_keys : list of dict
        Each dict has: column, reference_dataset, reference_column.

    processed_path : Path, optional
        Folder containing cleaned datasets.
        Defaults to Dataset/processed.
    """

    # Imported locally to avoid a circular import at module load time
    # (config.py does not import validation.py, so this is safe).
    from config import DATASETS

    if processed_path is None:

        processed_path = Path("Dataset") / "processed"

    invalid_rows = 0

    failed_keys = []

    for fk in foreign_keys:

        col = fk["column"]

        ref_dataset = fk["reference_dataset"]

        ref_col = fk["reference_column"]

        if col not in df.columns:

            continue

        if ref_dataset not in DATASETS:

            failed_keys.append(

                f"{col} (unknown reference dataset: {ref_dataset})"

            )

            continue

        ref_output_file = DATASETS[ref_dataset]["output_file"]

        ref_path = processed_path / ref_output_file

        if not ref_path.exists():

            failed_keys.append(

                f"{col} (reference file missing: {ref_path})"

            )

            continue

        ref_df = pd.read_csv(ref_path)

        if ref_col not in ref_df.columns:

            failed_keys.append(

                f"{col} (reference column {ref_col} missing)"

            )

            continue

        valid_values = set(ref_df[ref_col].dropna())

        # Only flag non-null values that don't exist in the reference.
        # Null FK values are handled separately by NOT NULL validation.
        invalid = df[col].notna() & ~df[col].isin(valid_values)

        count = invalid.sum()

        if count > 0:

            invalid_rows += count

            failed_keys.append(

                f"{col} -> {ref_dataset}.{ref_col} ({count})"

            )

    if invalid_rows > 0:

        return (

            False,

            invalid_rows,

            ", ".join(failed_keys)

        )

    return (

        True,

        0,

        "Foreign key validation passed."

    )


# ======================================================
# Validate Complete Dataset
# ======================================================

def validate_dataset(
    dataset_name: str,
    df: pd.DataFrame,
    dataset_config: dict,
    report: list
) -> bool:
    """
    Validate one complete dataset using rules
    defined inside config.py.

    Returns
    -------
    bool
        True  -> All validations passed
        False -> At least one validation failed
    """

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"VALIDATING DATASET : {dataset_name}")
    logger.info("=" * 60)

    validation_rules = dataset_config.get(
        "validation",
        {}
    )

    overall_status = True

    # --------------------------------------------------
    # Required Columns
    # --------------------------------------------------

    status, invalid_rows, remarks = validate_required_columns(

        df,

        dataset_config.get("required_columns", [])

    )

    add_validation_result(

        report,

        dataset_name,

        "Required Columns",

        "PASS" if status else "FAIL",

        invalid_rows,

        remarks

    )

    overall_status &= status

    # --------------------------------------------------
    # NOT NULL Validation
    # --------------------------------------------------

    if "not_null_columns" in validation_rules:

        status, invalid_rows, remarks = validate_not_null_columns(

            df,

            validation_rules["not_null_columns"]

        )

        add_validation_result(

            report,

            dataset_name,

            "NOT NULL Validation",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    # --------------------------------------------------
    # Unique Columns
    # --------------------------------------------------

    if "unique_columns" in validation_rules:

        status, invalid_rows, remarks = validate_unique_columns(

            df,

            validation_rules["unique_columns"]

        )

        add_validation_result(

            report,

            dataset_name,

            "Unique Columns",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    # --------------------------------------------------
    # Composite Unique Columns
    # --------------------------------------------------

    if "composite_unique_columns" in validation_rules:

        status, invalid_rows, remarks = validate_composite_unique_columns(

            df,

            validation_rules["composite_unique_columns"]

        )

        add_validation_result(

            report,

            dataset_name,

            "Composite Unique Columns",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    # --------------------------------------------------
    # Numeric Range Validation
    # --------------------------------------------------

    if "numeric_ranges" in validation_rules:

        status, invalid_rows, remarks = validate_numeric_ranges(

            df,

            validation_rules["numeric_ranges"]

        )

        add_validation_result(

            report,

            dataset_name,

            "Numeric Range",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    # --------------------------------------------------
    # Allowed Values Validation
    # --------------------------------------------------

    if "allowed_values" in validation_rules:

        status, invalid_rows, remarks = validate_allowed_values(

            df,

            validation_rules["allowed_values"]

        )

        add_validation_result(

            report,

            dataset_name,

            "Allowed Values",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    # ======================================================
    # Data sequence Validation
    # ======================================================

    if "date_sequences" in validation_rules:

        status, invalid_rows, remarks = validate_date_sequence(

            df,

            validation_rules["date_sequences"]

        )

        add_validation_result(

            report,

            dataset_name,

            "Date Sequence",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    # ======================================================
    # Foreign key validation
    # ======================================================

    if "foreign_keys" in validation_rules:

        status, invalid_rows, remarks = validate_foreign_keys(

            df,

            validation_rules["foreign_keys"]

        )

        add_validation_result(

            report,

            dataset_name,

            "Foreign Keys",

            "PASS" if status else "FAIL",

            invalid_rows,

            remarks

        )

        overall_status &= status

    logger.info(

        f"Validation Status : {'PASSED' if overall_status else 'FAILED'}"

    )

    return overall_status
# ======================================================
# Validate All Datasets
# ======================================================

def run_validation_pipeline(
    datasets: dict
):
    """
    Run validation on all cleaned datasets.
    """

    report = create_validation_report()

    overall_success = True

    for dataset_name, dataset_info in datasets.items():

        if "output_file" not in dataset_info:

            logger.warning(

                f"Skipping invalid config entry: {dataset_name}"

            )

            continue

        processed_file = (

            Path("Dataset") /
            "processed" /
            dataset_info["output_file"]

        )

        if not processed_file.exists():

            logger.warning(

                f"{processed_file} not found."

            )

            continue

        df = pd.read_csv(

            processed_file

        )

        status = validate_dataset(

            dataset_name,

            df,

            dataset_info,

            report

        )

        overall_success &= status

    report_path = (

        Path("reports") /

        "validation_report.csv"

    )

    report_path.parent.mkdir(

        exist_ok=True

    )

    save_validation_report(

        report,

        report_path

    )

    logger.info("")

    logger.info("=" * 60)
    logger.info("VALIDATION PIPELINE COMPLETED")
    logger.info("=" * 60)

    logger.info(

        f"Overall Status : {'PASSED' if overall_success else 'FAILED'}"

    )

    logger.info(

        f"Report Saved : {report_path}"

    )

    return overall_success


# ======================================================
# Main (Testing Only)
# ======================================================

if __name__ == "__main__":

    print(

        "Validation module loaded successfully."

    )

    print(

        "Run validation using run_etl.py"

    )
"""
==========================================================
Cleaning Module
Customer Revenue Opportunity Intelligence Platform

Purpose:
    Generic data cleaning functions for all datasets.

Author:
    Your Name
==========================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List
from datetime import datetime


# ---------------------------------------------------------
# Standardize Column Names
# ---------------------------------------------------------
def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names into standard format.
    Example:
    Customer ID  -> customer_id
    Customer-ID  -> customer_id
    CUSTOMER ID  -> customer_id
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


# ---------------------------------------------------------
# Validate Required Columns
# ---------------------------------------------------------
def validate_required_columns(
    df: pd.DataFrame,
    required_columns: List[str]
) -> None:
    """
    Check whether all required columns exist.
    """

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


# ---------------------------------------------------------
# Convert Blank Strings to NaN
# ---------------------------------------------------------
def convert_blank_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace empty strings and spaces with NaN.
    """

    df = df.copy()

    df.replace(
        r'^\s*$',
        np.nan,
        regex=True,
        inplace=True
    )

    return df


# ---------------------------------------------------------
# Remove Duplicate Rows
# ---------------------------------------------------------
def remove_duplicate_rows(
    df: pd.DataFrame
) -> Tuple[pd.DataFrame, int]:
    """
    Remove duplicate rows.
    """

    df = df.copy()

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    return df, removed


# ---------------------------------------------------------
# Remove Missing Primary Key
# ---------------------------------------------------------
def remove_missing_primary_key(
    df: pd.DataFrame,
    primary_key: str
) -> Tuple[pd.DataFrame, int]:
    """
    Remove rows where primary key is missing.

    If primary_key is None or empty, this is a no-op
    (some datasets may not have a single-column primary key).
    """

    df = df.copy()

    before = len(df)

    if not primary_key:

        return df, 0

    df = df.dropna(subset=[primary_key])

    removed = before - len(df)

    return df, removed


# ---------------------------------------------------------
# Clean Text Columns
# ---------------------------------------------------------
def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading and trailing spaces
    from all object/string columns.
    """

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in text_columns:

        df[col] = df[col].where(
            df[col].isna(),
            df[col].astype(str).str.strip()
        )

    return df


# ---------------------------------------------------------
# Convert Numeric Columns
# ---------------------------------------------------------
def convert_numeric_columns(
    df: pd.DataFrame,
    columns: List[str]
) -> pd.DataFrame:
    """
    Convert selected columns to numeric.
    """

    df = df.copy()

    for col in columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


# ---------------------------------------------------------
# Convert Date Columns
# ---------------------------------------------------------
def convert_date_columns(
    df: pd.DataFrame,
    columns: List[str]
) -> pd.DataFrame:
    """
    Convert selected columns to datetime.
    """

    df = df.copy()

    for col in columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                dayfirst = True
            )

    return df

# ---------------------------------------------------------
# Remove Invalid Date Sequences
# ---------------------------------------------------------
def remove_invalid_date_sequences(
    df,
    start_col,
    end_col
):
    """
    Remove rows where start date is greater than end date.
    """

    if start_col not in df.columns:
        return df, 0

    if end_col not in df.columns:
        return df, 0

    before = len(df)

    valid_mask = (
        df[start_col].isna()
        | df[end_col].isna()
        | (df[start_col] <= df[end_col])
    )

    df = df[valid_mask]

    removed = before - len(df)

    return df, removed


# ---------------------------------------------------------
# Standardize Text Case
# ---------------------------------------------------------
def standardize_case(
    df: pd.DataFrame,
    title_columns: List[str] = None,
    upper_columns: List[str] = None,
    lower_columns: List[str] = None
) -> pd.DataFrame:
    """
    Standardize text columns.
    """

    df = df.copy()

    title_columns = title_columns or []
    upper_columns = upper_columns or []
    lower_columns = lower_columns or []

    for col in title_columns:

        if col in df.columns:

            df[col] = df[col].where(
                df[col].isna(),
                df[col].astype(str).str.title()
            )

    for col in upper_columns:

        if col in df.columns:

            df[col] = df[col].where(
                df[col].isna(),
                df[col].astype(str).str.upper()
            )

    for col in lower_columns:

        if col in df.columns:

            df[col] = df[col].where(
                df[col].isna(),
                df[col].astype(str).str.lower()
            )

    return df


# ---------------------------------------------------------
# Reset DataFrame Index
# ---------------------------------------------------------
def reset_dataframe(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Reset dataframe index.
    """

    df = df.copy()

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


# ---------------------------------------------------------
# Cleaning Report
# ---------------------------------------------------------
def cleaning_report(
    rows_before: int,
    rows_after: int,
    duplicates_removed: int,
    primary_key_removed: int
) -> Dict:
    """
    Generate ETL cleaning report.
    """

    return {

        "Rows Before": rows_before,
        "Rows After": rows_after,
        "Duplicates Removed": duplicates_removed,
        "Rows Removed (Missing Primary Key)": primary_key_removed,
        "Status": "SUCCESS",
        "Execution Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }


# # ---------------------------------------------------------
# # Main Function (Temporary)
# # ---------------------------------------------------------
# def main() -> None:

#     base_dir = Path(__file__).resolve().parents[1]

#     input_path = (
#         base_dir /
#         "Dataset" /"raw" /
#         "olist_customers_dataset.csv"
#     )

#     output_path = (
#         base_dir /
#         "Dataset" / "processed" /
#         "olist_customers_dataset_cleaned.csv"
#     )

#     if not input_path.exists():
#         raise FileNotFoundError(
#             f"Input file not found:\n{input_path}"
#         )

#     raw_rows = pd.read_csv(input_path)

#     customers_df = standardize_column_names(raw_rows)

#     required_columns = [
#         "customer_id",
#         "customer_unique_id",
#         "customer_zip_code_prefix",
#         "customer_city",
#         "customer_state"
#     ]

#     validate_required_columns(
#         customers_df,
#         required_columns
#     )

#     customers_df = convert_blank_to_nan(customers_df)

#     customers_df, duplicates_removed = remove_duplicate_rows(
#         customers_df
#     )

#     customers_df, pk_removed = remove_missing_primary_key(
#         customers_df,
#         "customer_id"
#     )

#     customers_df = clean_text_columns(customers_df)

#     customers_df = standardize_case(
#         customers_df,
#         title_columns=["customer_city"],
#         upper_columns=["customer_state"]
#     )

#     customers_df = convert_numeric_columns(
#         customers_df,
#         ["customer_zip_code_prefix"]
#     )

#     customers_df = reset_dataframe(customers_df)

#     customers_df.to_csv(
#         output_path,
#         index=False
#     )

#     report = cleaning_report(
#         rows_before=len(raw_rows),
#         rows_after=len(customers_df),
#         duplicates_removed=duplicates_removed,
#         primary_key_removed=pk_removed
#     )

#     print("\n========== CLEANING REPORT ==========\n")

#     for key, value in report.items():
#         print(f"{key:<35}: {value}")

#     print("\n=====================================\n")
#     print(f"Cleaned dataset saved to:\n{output_path}")


# if __name__ == "__main__":
#     main()
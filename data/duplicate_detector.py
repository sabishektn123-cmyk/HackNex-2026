"""
Duplicate detection utilities for VERITYAI.

This module detects potential duplicate records without
deleting or modifying the original dataset.
"""

import pandas as pd


def detect_duplicates(dataframe: pd.DataFrame) -> dict:
    """
    Detect duplicate rows in a DataFrame.

    Returns information about duplicate records without
    modifying the original dataset.
    """

    duplicate_mask = dataframe.duplicated(keep=False)

    duplicate_rows = dataframe[duplicate_mask]

    duplicate_count = int(
        dataframe.duplicated(keep="first").sum()
    )

    duplicate_groups = int(
        duplicate_rows.drop_duplicates().shape[0]
    )

    return {
        "type": "DUPLICATE_RECORD",
        "duplicate_count": duplicate_count,
        "duplicate_rows": duplicate_rows.to_dict(
            orient="records"
        ),
        "duplicate_groups": duplicate_groups,
    }


def has_duplicates(dataframe: pd.DataFrame) -> bool:
    """
    Check whether a dataset contains duplicate rows.
    """

    return bool(dataframe.duplicated().any())


if __name__ == "__main__":
    print("Duplicate detector module loaded successfully.")
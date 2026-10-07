"""
Missing value detection utilities for VERITYAI.

This module detects missing values without modifying
the original dataset.
"""

import pandas as pd


def detect_missing_values(dataframe: pd.DataFrame) -> list[dict]:
    """
    Detect missing values in every column.

    Returns a list of warnings for columns containing
    missing values.
    """

    warnings = []

    for column in dataframe.columns:
        missing_count = int(dataframe[column].isna().sum())

        if missing_count > 0:
            total_rows = len(dataframe)

            percentage = (
                (missing_count / total_rows) * 100
                if total_rows > 0
                else 0
            )

            if percentage >= 50:
                severity = "HIGH"
            elif percentage >= 20:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            warnings.append({
                "type": "MISSING_VALUE",
                "column": str(column),
                "missing_count": missing_count,
                "missing_percentage": round(percentage, 2),
                "severity": severity,
            })

    return warnings


def get_missing_summary(dataframe: pd.DataFrame) -> dict:
    """
    Generate a summary of missing values.
    """

    total_missing = int(dataframe.isna().sum().sum())
    total_cells = int(dataframe.shape[0] * dataframe.shape[1])

    percentage = (
        (total_missing / total_cells) * 100
        if total_cells > 0
        else 0
    )

    return {
        "total_missing": total_missing,
        "total_cells": total_cells,
        "missing_percentage": round(percentage, 2),
    }


if __name__ == "__main__":
    print("Missing value detector module loaded successfully.")
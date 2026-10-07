"""
Date detection utilities for VERITYAI.

This module detects common date formats and identifies
potentially ambiguous dates without modifying the dataset.
"""

import re

import pandas as pd


def detect_date_format(value) -> str:
    """
    Detect the format/category of a single date value.

    Returns
    -------
    str
        Detected date format or UNKNOWN.
    """

    if pd.isna(value):
        return "MISSING"

    text = str(value).strip()

    # YYYY-MM-DD
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return "YYYY-MM-DD"

    # DD-MM-YYYY or MM-DD-YYYY
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", text):
        return "AMBIGUOUS_DATE"

    # DD/MM/YYYY or MM/DD/YYYY
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", text):
        first, second, _ = text.split("/")

        first = int(first)
        second = int(second)

        # If both values can represent months,
        # the format cannot be determined reliably.
        if first <= 12 and second <= 12:
            return "AMBIGUOUS_DATE"

        if first > 12:
            return "DD/MM/YYYY"

        if second > 12:
            return "MM/DD/YYYY"

    # Month name + year, e.g. Jan 2025
    if re.fullmatch(
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"\s+\d{4}",
        text,
        flags=re.IGNORECASE,
    ):
        return "MONTH_YEAR"

    # Quarter format, e.g. Q1 2025
    if re.fullmatch(r"Q[1-4]\s+\d{4}", text, flags=re.IGNORECASE):
        return "QUARTER_YEAR"

    # Financial year, e.g. FY2025
    if re.fullmatch(r"FY\s?\d{4}", text, flags=re.IGNORECASE):
        return "FINANCIAL_YEAR"

    return "UNKNOWN"


def analyze_date_column(
    dataframe: pd.DataFrame,
    column: str
) -> dict:
    """
    Analyze date formats in a DataFrame column.
    """

    if column not in dataframe.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    format_counts = {}

    for value in dataframe[column]:
        date_format = detect_date_format(value)

        format_counts[date_format] = (
            format_counts.get(date_format, 0) + 1
        )

    detected_formats = sorted(
        key for key in format_counts
        if key not in ["MISSING", "UNKNOWN"]
    )

    ambiguous_count = format_counts.get(
        "AMBIGUOUS_DATE", 0
    )

    if ambiguous_count > 0:
        status = "AMBIGUOUS_DATE_DETECTED"
    elif len(detected_formats) > 1:
        status = "MULTIPLE_DATE_FORMATS"
    elif len(detected_formats) == 1:
        status = "CONSISTENT"
    else:
        status = "NO_DATE_DETECTED"

    return {
        "column": column,
        "formats": detected_formats,
        "format_counts": format_counts,
        "ambiguous_count": ambiguous_count,
        "status": status,
    }


if __name__ == "__main__":
    print("Date detector module loaded successfully.")
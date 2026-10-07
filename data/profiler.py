"""
Dataset profiling utilities for VERITYAI.

This module analyzes a dataset without modifying the original data.
"""

from pathlib import Path

import pandas as pd


def detect_column_type(series: pd.Series) -> str:
    """
    Detect the general data type of a column.
    """

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_integer_dtype(series):
        return "integer"

    if pd.api.types.is_float_dtype(series):
        return "float"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    # Try detecting dates in object/string columns.
    if series.dtype == "object":
        non_null = series.dropna()

        if not non_null.empty:
            converted = pd.to_datetime(
                non_null,
                errors="coerce"
            )

            if converted.notna().mean() >= 0.8:
                return "datetime"

    return "string"


def profile_dataset(dataframe: pd.DataFrame) -> dict:
    """
    Generate a profile of a pandas DataFrame.

    The original DataFrame is not modified.
    """

    columns = []

    for column in dataframe.columns:
        series = dataframe[column]

        column_info = {
            "name": str(column),
            "type": detect_column_type(series),
            "pandas_dtype": str(series.dtype),
            "missing": int(series.isna().sum()),
            "missing_percentage": round(
                float(series.isna().mean() * 100),
                2
            ),
            "unique": int(series.nunique(dropna=True)),
        }

        # Add basic statistics for numeric columns.
        if pd.api.types.is_numeric_dtype(series):
            column_info["statistics"] = {
                "min": float(series.min())
                if not series.dropna().empty else None,
                "max": float(series.max())
                if not series.dropna().empty else None,
                "mean": round(float(series.mean()), 2)
                if not series.dropna().empty else None,
            }

        columns.append(column_info)

    profile = {
        "rows": int(len(dataframe)),
        "columns_count": int(len(dataframe.columns)),
        "columns": columns,
    }

    return profile


def profile_csv(file_path: str | Path) -> dict:
    """
    Load a CSV file and generate its dataset profile.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    dataframe = pd.read_csv(path)

    return profile_dataset(dataframe)


if __name__ == "__main__":
    print("Dataset profiler module loaded successfully.")
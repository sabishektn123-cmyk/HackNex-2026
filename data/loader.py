"""
Data loading utilities for VERITYAI.

This module loads CSV files without modifying the original data.
"""

from pathlib import Path

import pandas as pd

def load_excel(file_path: str | Path) -> pd.DataFrame:
    """
    Load an Excel file into a pandas DataFrame.

    Parameters
    ----------
    file_path : str | Path
        Path to the Excel file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() not in [".xlsx", ".xls"]:
        raise ValueError(
            f"Expected an Excel file, got: {path.suffix}"
        )

    try:
        dataframe = pd.read_excel(path)

    except Exception as exc:
        raise RuntimeError(
            f"Unable to read Excel file: {path}"
        ) from exc

    if dataframe.empty and len(dataframe.columns) == 0:
        raise ValueError(
            f"Excel file contains no usable data: {path}"
        )

    return dataframe

def load_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV file, got: {path.suffix}")

    try:
        try:
            dataframe = pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            dataframe = pd.read_csv(path, encoding="cp1252")

    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"CSV file is empty: {path}") from exc

    except pd.errors.ParserError as exc:
        raise RuntimeError(
            f"Unable to parse CSV file: {path}"
        ) from exc

    if dataframe.empty and len(dataframe.columns) == 0:
        raise ValueError(f"CSV file contains no usable data: {path}")

    return dataframe


if __name__ == "__main__":
    print("Testing Excel loader...")

    df = load_excel("data/test_sales.xlsx")

    print("\nExcel loaded successfully!")
    print(df)

    print("\nRows:", len(df))
    print("Columns:", len(df.columns))
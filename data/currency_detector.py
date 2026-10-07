"""
Currency detection utilities for VERITYAI.

This module detects common currency symbols and currency codes
without modifying the original dataset.
"""

import re

import pandas as pd


CURRENCY_PATTERNS = {
    "INR": [
        r"₹",
        r"\bINR\b",
        r"\bRs\.?\b",
        r"\bRupees?\b",
    ],
    "USD": [
        r"\$",
        r"\bUSD\b",
        r"\bUS\s*Dollars?\b",
    ],
    "EUR": [
        r"€",
        r"\bEUR\b",
        r"\bEuros?\b",
    ],
    "GBP": [
        r"£",
        r"\bGBP\b",
        r"\bPounds?\b",
    ],
    "JPY": [
        r"¥",
        r"\bJPY\b",
        r"\bYen\b",
    ],
}


def detect_currency(value) -> str | None:
    """
    Detect the currency represented by a single value.

    Returns
    -------
    str | None
        Currency code such as INR, USD, EUR, GBP, or JPY.
        Returns None if no currency is detected.
    """

    if pd.isna(value):
        return None

    text = str(value)

    detected_currencies = []

    for currency, patterns in CURRENCY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                detected_currencies.append(currency)
                break

    if len(detected_currencies) == 1:
        return detected_currencies[0]

    if len(detected_currencies) > 1:
        return "AMBIGUOUS"

    return None


def detect_currency_column(
    dataframe: pd.DataFrame,
    column: str
) -> dict:
    """
    Detect currencies present in a specific DataFrame column.
    """

    if column not in dataframe.columns:
        raise ValueError(
            f"Column not found: {column}"
        )

    detected_values = []

    for value in dataframe[column]:
        currency = detect_currency(value)

        if currency is not None:
            detected_values.append(currency)

    currency_counts = {}

    for currency in detected_values:
        currency_counts[currency] = (
            currency_counts.get(currency, 0) + 1
        )

    currencies = sorted(currency_counts.keys())

    if len(currencies) > 1:
        status = "CURRENCY_MISMATCH"
    elif len(currencies) == 1:
        status = "CONSISTENT"
    else:
        status = "NO_CURRENCY_DETECTED"

    return {
        "column": column,
        "currencies": currencies,
        "currency_counts": currency_counts,
        "status": status,
    }


if __name__ == "__main__":
    print("Currency detector module loaded successfully.")
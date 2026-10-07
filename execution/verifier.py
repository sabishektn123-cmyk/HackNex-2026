"""
VERITYAI Independent Verification Engine.

This module independently checks numerical results produced by
the execution engine.

The verifier does NOT trust the AI-generated result blindly.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass
class VerificationResult:
    """
    Result of an independent numerical verification.
    """

    status: str
    expected: Any = None
    actual: Any = None
    difference: float | None = None
    tolerance: float | None = None
    error: str | None = None


class Verifier:
    """
    Independently verifies numerical results.

    Status values:

    VERIFIED
        Expected and actual values agree within tolerance.

    VERIFICATION_FAILED
        Expected and actual values do not agree.

    CANNOT_DETERMINE
        The values cannot be safely compared.
    """

    VERIFIED = "VERIFIED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    CANNOT_DETERMINE = "CANNOT_DETERMINE"

    def __init__(
        self,
        absolute_tolerance: float = 1e-9,
        relative_tolerance: float = 1e-6,
    ):
        self.absolute_tolerance = absolute_tolerance
        self.relative_tolerance = relative_tolerance

    def verify(
        self,
        expected: Any,
        actual: Any,
    ) -> VerificationResult:
        """
        Compare expected and independently calculated numerical values.
        """

        if not self._is_valid_number(expected):
            return VerificationResult(
                status=self.CANNOT_DETERMINE,
                expected=expected,
                actual=actual,
                error="Expected value is not a valid finite number.",
            )

        if not self._is_valid_number(actual):
            return VerificationResult(
                status=self.CANNOT_DETERMINE,
                expected=expected,
                actual=actual,
                error="Actual value is not a valid finite number.",
            )

        expected_value = float(expected)
        actual_value = float(actual)

        difference = abs(expected_value - actual_value)

        tolerance = max(
            self.absolute_tolerance,
            self.relative_tolerance
            * max(abs(expected_value), abs(actual_value), 1.0),
        )

        if math.isclose(
            expected_value,
            actual_value,
            rel_tol=self.relative_tolerance,
            abs_tol=self.absolute_tolerance,
        ):
            return VerificationResult(
                status=self.VERIFIED,
                expected=expected_value,
                actual=actual_value,
                difference=difference,
                tolerance=tolerance,
            )

        return VerificationResult(
            status=self.VERIFICATION_FAILED,
            expected=expected_value,
            actual=actual_value,
            difference=difference,
            tolerance=tolerance,
            error="Expected and actual values do not match within tolerance.",
        )

    @staticmethod
    def _is_valid_number(value: Any) -> bool:
        """
        Return True only for finite integer/float-like values.

        Booleans are deliberately rejected because bool is a subclass
        of int in Python.
        """

        if isinstance(value, bool):
            return False

        if not isinstance(value, (int, float)):
            return False

        return math.isfinite(float(value))
    
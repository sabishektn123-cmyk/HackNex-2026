"""
VERITYAI Verification Pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .executor import Executor
from .verifier import VerificationResult, Verifier


@dataclass
class PipelineResult:
    status: str
    expected: Any = None
    actual: Any = None
    verification: VerificationResult | None = None
    execution_error: str | None = None


class VerificationPipeline:
    VERIFIED = "VERIFIED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    CANNOT_DETERMINE = "CANNOT_DETERMINE"
    EXECUTION_FAILED = "EXECUTION_FAILED"

    def __init__(self, timeout_seconds: float = 5.0):
        self.executor = Executor(timeout_seconds=timeout_seconds)
        self.verifier = Verifier()

    def verify_calculation(
        self,
        code: str,
        expected: Any,
    ) -> PipelineResult:

        execution = self.executor.execute(code)

        if execution.status != "SUCCESS":
            return PipelineResult(
                status=self.EXECUTION_FAILED,
                expected=expected,
                actual=execution.result,
                execution_error=execution.error,
            )

        if execution.result is None:
            return PipelineResult(
                status=self.CANNOT_DETERMINE,
                expected=expected,
                actual=None,
                execution_error="No valid VERITYAI result was produced.",
            )

        verification = self.verifier.verify(
            expected=expected,
            actual=execution.result,
        )

        return PipelineResult(
            status=verification.status,
            expected=verification.expected,
            actual=verification.actual,
            verification=verification,
        )

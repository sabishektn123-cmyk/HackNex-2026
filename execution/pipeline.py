"""
VERITYAI Verification Pipeline.

Coordinates execution, abstention, and independent verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .abstention import AbstentionEngine
from .executor import Executor
from .verifier import VerificationResult, Verifier


@dataclass
class PipelineResult:
    status: str
    expected: Any = None
    actual: Any = None
    verification: VerificationResult | None = None
    execution_error: str | None = None
    abstention_reason: str | None = None


class VerificationPipeline:
    VERIFIED = "VERIFIED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    CANNOT_DETERMINE = "CANNOT_DETERMINE"
    EXECUTION_FAILED = "EXECUTION_FAILED"

    def __init__(self, timeout_seconds: float = 5.0):
        self.executor = Executor(timeout_seconds=timeout_seconds)
        self.verifier = Verifier()
        self.abstention = AbstentionEngine()

    def verify_calculation(
        self,
        code: str,
        expected: Any,
        conflicting: bool = False,
        ambiguous: bool = False,
    ) -> PipelineResult:

        execution = self.executor.execute(code)

        # First decide whether verification is possible.
        abstention = self.abstention.evaluate(
            expected=expected,
            actual=execution.result,
            execution_status=execution.status,
            conflicting=conflicting,
            ambiguous=ambiguous,
        )

        if abstention.should_abstain:
            return PipelineResult(
                status=abstention.status,
                expected=expected,
                actual=execution.result,
                execution_error=execution.error,
                abstention_reason=abstention.reason,
            )

        # Only verified evidence reaches the verifier.
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
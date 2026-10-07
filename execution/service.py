"""
VERITYAI Verification Service.

Provides a stable application-level interface for the API layer.
The API does not need to know how validation, sandboxing,
abstention, or verification are implemented internally.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .integration import AgentCalculation, VerificationIntegration


class VerificationService:
    """
    Public service interface for VERITYAI verification.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.integration = VerificationIntegration(
            timeout_seconds=timeout_seconds
        )

    def verify(
        self,
        question: str,
        generated_code: str,
        claimed_result: Any,
        dataset: str = "",
        conflicting: bool = False,
        ambiguous: bool = False,
    ) -> dict[str, Any]:
        """
        Verify an AI-generated calculation and return
        a JSON-serializable response.
        """

        calculation = AgentCalculation(
            question=question,
            generated_code=generated_code,
            claimed_result=claimed_result,
            dataset=dataset,
        )

        result = self.integration.verify_agent_calculation(
            calculation=calculation,
            conflicting=conflicting,
            ambiguous=ambiguous,
        )

        response: dict[str, Any] = {
            "status": result.status,
            "expected": result.expected,
            "actual": result.actual,
            "execution_error": result.execution_error,
            "abstention_reason": result.abstention_reason,
        }

        if result.verification is not None:
            response["verification"] = asdict(result.verification)
        else:
            response["verification"] = None

        return response
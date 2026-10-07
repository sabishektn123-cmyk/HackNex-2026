"""
VERITYAI Verification Service.

Application-level interface for the API layer.

The service combines:
- secure execution
- abstention
- independent verification
- deterministic confidence
- audit trail
- proof package generation
"""

from __future__ import annotations

from typing import Any

from .audit import AuditTrail
from .confidence import ConfidenceEngine
from .integration import AgentCalculation, VerificationIntegration
from .proof import ProofPackage


class VerificationService:
    def __init__(self, timeout_seconds: float = 5.0):
        self.integration = VerificationIntegration(
            timeout_seconds=timeout_seconds
        )
        self.confidence = ConfidenceEngine()

    def verify(
        self,
        question: str,
        generated_code: str,
        claimed_result: Any,
        dataset: str = "",
        conflicting: bool = False,
        ambiguous: bool = False,
    ) -> dict[str, Any]:

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

        # ---------------------------------------------------------
        # Determine objective verification state
        # ---------------------------------------------------------

        verification_passed = (
            result.verification is not None
            and result.verification.status == "VERIFIED"
        )

        execution_success = (
            result.execution_error is None
            and result.status != "CANNOT_DETERMINE"
        )

        # ---------------------------------------------------------
        # Determine evidence quality
        # ---------------------------------------------------------

        if not dataset:
            evidence_quality = 0.0
        elif conflicting or ambiguous:
            evidence_quality = 0.0
        else:
            evidence_quality = 1.0

        # ---------------------------------------------------------
        # Calculate deterministic confidence
        # ---------------------------------------------------------

        confidence = self.confidence.calculate(
            execution_success=execution_success,
            verification_passed=verification_passed,
            evidence_quality=evidence_quality,
            conflicting=conflicting,
            ambiguous=ambiguous,
        )

        # ---------------------------------------------------------
        # Determine trusted answer
        # ---------------------------------------------------------

        if result.status == "VERIFIED":
            answer = result.actual
        else:
            answer = None

        # ---------------------------------------------------------
        # Collect warnings
        # ---------------------------------------------------------

        warnings: list[str] = []

        if result.execution_error:
            warnings.append(result.execution_error)

        if result.abstention_reason:
            warnings.append(result.abstention_reason)

        if result.verification is not None:
            if result.verification.error:
                warnings.append(result.verification.error)

        # ---------------------------------------------------------
        # Create audit record
        # ---------------------------------------------------------

        audit = AuditTrail.create_record(
            question=question,
            dataset=dataset,
            generated_code=generated_code,
            execution_status=(
                "SUCCESS"
                if execution_success
                else "FAILED"
            ),
            execution_error=result.execution_error,
            expected_result=claimed_result,
            actual_result=result.actual,
            verification_status=(
                result.verification.status
                if result.verification is not None
                else None
            ),
            verification_difference=(
                result.verification.difference
                if result.verification is not None
                else None
            ),
            verification_tolerance=(
                result.verification.tolerance
                if result.verification is not None
                else None
            ),
            abstention_reason=result.abstention_reason,
            confidence_score=confidence.score,
            confidence_level=confidence.level,
            warnings=warnings,
            final_status=result.status,
        )

        # ---------------------------------------------------------
        # Build proof package
        # ---------------------------------------------------------

        proof = ProofPackage.build(
            status=result.status,
            answer=answer,
            verification=result.verification,
            confidence=confidence,
            audit=audit,
        )

        return proof.to_dict()
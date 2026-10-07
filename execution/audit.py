"""
VERITYAI Audit Trail.

Creates structured, machine-readable records describing how a
numerical answer was executed, verified, or rejected.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuditRecord:
    question: str
    dataset: str
    generated_code: str

    execution_status: str
    execution_output: str = ""
    execution_error: str | None = None

    expected_result: Any = None
    actual_result: Any = None

    verification_status: str | None = None
    verification_difference: float | None = None
    verification_tolerance: float | None = None

    abstention_reason: str | None = None

    confidence_score: float | None = None
    confidence_level: str | None = None

    warnings: list[str] = field(default_factory=list)

    final_status: str = ""
    timestamp: str = ""

    code_hash: str = ""

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

        if not self.code_hash:
            self.code_hash = hashlib.sha256(
                self.generated_code.encode("utf-8")
            ).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=2,
            default=str,
        )


class AuditTrail:
    """
    Creates and validates structured audit records.
    """

    @staticmethod
    def create_record(
        question: str,
        dataset: str,
        generated_code: str,
        execution_status: str,
        execution_output: str = "",
        execution_error: str | None = None,
        expected_result: Any = None,
        actual_result: Any = None,
        verification_status: str | None = None,
        verification_difference: float | None = None,
        verification_tolerance: float | None = None,
        abstention_reason: str | None = None,
        confidence_score: float | None = None,
        confidence_level: str | None = None,
        warnings: list[str] | None = None,
        final_status: str = "",
    ) -> AuditRecord:

        return AuditRecord(
            question=question,
            dataset=dataset,
            generated_code=generated_code,
            execution_status=execution_status,
            execution_output=execution_output,
            execution_error=execution_error,
            expected_result=expected_result,
            actual_result=actual_result,
            verification_status=verification_status,
            verification_difference=verification_difference,
            verification_tolerance=verification_tolerance,
            abstention_reason=abstention_reason,
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            warnings=warnings or [],
            final_status=final_status,
        )
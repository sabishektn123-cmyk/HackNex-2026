"""
VERITYAI Proof Package.

Combines verification, confidence, and audit information into
a single API-friendly proof object.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .audit import AuditRecord
from .confidence import ConfidenceResult
from .verifier import VerificationResult


@dataclass
class ProofPackage:
    status: str
    answer: Any = None
    verification: dict[str, Any] | None = None
    confidence: dict[str, Any] | None = None
    audit: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "answer": self.answer,
            "verification": self.verification,
            "confidence": self.confidence,
            "audit": self.audit,
        }

    @classmethod
    def build(
        cls,
        status: str,
        answer: Any,
        verification: VerificationResult | None,
        confidence: ConfidenceResult | None,
        audit: AuditRecord | None,
    ) -> "ProofPackage":

        return cls(
            status=status,
            answer=answer,
            verification=(
                asdict(verification)
                if verification is not None
                else None
            ),
            confidence=(
                asdict(confidence)
                if confidence is not None
                else None
            ),
            audit=(
                audit.to_dict()
                if audit is not None
                else None
            ),
        )
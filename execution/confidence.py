"""
VERITYAI Deterministic Confidence Engine.

Produces a reproducible confidence score from objective
verification signals.

The score is NOT an LLM-generated probability.
"""


from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConfidenceResult:
    score: float
    level: str
    reasons: list[str]


class ConfidenceEngine:
    """
    Deterministic confidence calculator.

    Maximum score = 100.
    """

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    def calculate(
        self,
        execution_success: bool,
        verification_passed: bool,
        evidence_quality: float,
        conflicting: bool = False,
        ambiguous: bool = False,
    ) -> ConfidenceResult:

        reasons: list[str] = []
        score = 0.0

        # Execution reliability: 20 points
        if execution_success:
            score += 20
            reasons.append("Execution completed successfully.")
        else:
            reasons.append("Execution did not complete successfully.")

        # Independent verification: 40 points
        if verification_passed:
            score += 40
            reasons.append("Independent verification passed.")
        else:
            reasons.append("Independent verification did not pass.")

        # Evidence quality: 20 points
        evidence_quality = max(0.0, min(1.0, evidence_quality))
        evidence_points = evidence_quality * 20
        score += evidence_points

        reasons.append(
            f"Evidence quality contributed {evidence_points:.1f} points."
        )

        # Conflicting evidence: 10 points
        if not conflicting:
            score += 10
            reasons.append("No conflicting evidence detected.")
        else:
            reasons.append("Conflicting evidence detected.")

        # Ambiguity: 10 points
        if not ambiguous:
            score += 10
            reasons.append("No ambiguity detected.")
        else:
            reasons.append("Ambiguity detected.")

        score = round(min(100.0, max(0.0, score)), 2)

        if score >= 80:
            level = self.HIGH
        elif score >= 50:
            level = self.MEDIUM
        else:
            level = self.LOW

        return ConfidenceResult(
            score=score,
            level=level,
            reasons=reasons,
        )
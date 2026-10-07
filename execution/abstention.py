"""
VERITYAI Abstention Engine.

Determines when VERITYAI should refuse to provide a numerical
answer because the available evidence is insufficient,
ambiguous, conflicting, or invalid.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AbstentionResult:
    should_abstain: bool
    status: str
    reason: str


class AbstentionEngine:
    """
    Deterministic rules for deciding when VERITYAI must abstain.
    """

    CANNOT_DETERMINE = "CANNOT_DETERMINE"
    PROCEED = "PROCEED"

    def evaluate(
        self,
        expected: Any = None,
        actual: Any = None,
        execution_status: str = "SUCCESS",
        conflicting: bool = False,
        ambiguous: bool = False,
    ) -> AbstentionResult:
        """
        Decide whether the system has enough evidence
        to continue verification.
        """

        if execution_status != "SUCCESS":
            return AbstentionResult(
                should_abstain=True,
                status=self.CANNOT_DETERMINE,
                reason=(
                    f"Execution did not complete successfully: "
                    f"{execution_status}"
                ),
            )

        if expected is None:
            return AbstentionResult(
                should_abstain=True,
                status=self.CANNOT_DETERMINE,
                reason="Expected value is missing.",
            )

        if actual is None:
            return AbstentionResult(
                should_abstain=True,
                status=self.CANNOT_DETERMINE,
                reason="Actual calculated value is missing.",
            )

        if conflicting:
            return AbstentionResult(
                should_abstain=True,
                status=self.CANNOT_DETERMINE,
                reason="Conflicting evidence was detected.",
            )

        if ambiguous:
            return AbstentionResult(
                should_abstain=True,
                status=self.CANNOT_DETERMINE,
                reason="Input or calculation is ambiguous.",
            )

        return AbstentionResult(
            should_abstain=False,
            status=self.PROCEED,
            reason="Sufficient evidence is available for verification.",
        )
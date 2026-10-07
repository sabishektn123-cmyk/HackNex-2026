"""
VERITYAI AI-Agent Integration Layer.

Receives untrusted output from the AI agent and routes it
through the security and verification pipeline.

The AI agent itself is never trusted to declare a result VERIFIED.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .pipeline import PipelineResult, VerificationPipeline


@dataclass
class AgentCalculation:
    """
    Represents calculation output received from the AI agent.
    """

    question: str
    generated_code: str
    claimed_result: Any
    dataset: str = ""


class VerificationIntegration:
    """
    Integration boundary between the AI agent and verification engine.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.pipeline = VerificationPipeline(
            timeout_seconds=timeout_seconds
        )

    def verify_agent_calculation(
        self,
        calculation: AgentCalculation,
        conflicting: bool = False,
        ambiguous: bool = False,
    ) -> PipelineResult:
        """
        Verify an AI-generated calculation.

        The claimed result is treated only as an expected value.
        The generated code must independently reproduce it.
        """

        return self.pipeline.verify_calculation(
            code=calculation.generated_code,
            expected=calculation.claimed_result,
            conflicting=conflicting,
            ambiguous=ambiguous,
        )
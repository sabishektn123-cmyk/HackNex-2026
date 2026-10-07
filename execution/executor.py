"""
VERITYAI Execution Engine.

Coordinates validation and sandbox execution and extracts
structured numerical results from approved calculation code.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Optional

from .sandbox import Sandbox
from .validator import CodeValidator


RESULT_MARKER = "__VERITY_RESULT__:"


@dataclass
class ExecutionResult:
    status: str
    result: Optional[Any] = None
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None


class Executor:
    def __init__(self, timeout_seconds: float = 5.0):
        self.validator = CodeValidator()
        self.sandbox = Sandbox(timeout_seconds=timeout_seconds)

    def execute(self, code: str) -> ExecutionResult:
        """
        Validate and safely execute generated calculation code.
        """

        if not isinstance(code, str):
            return ExecutionResult(
                status="ERROR",
                error="Code must be provided as a string.",
            )

        if not code.strip():
            return ExecutionResult(
                status="ERROR",
                error="Code cannot be empty.",
            )

        validation = self.validator.validate(code)

        if not validation.valid:
            return ExecutionResult(
                status="REJECTED",
                error="Code validation failed.",
                stderr="\n".join(validation.errors),
            )

        sandbox_result = self.sandbox.run(code)

        result = None

        if sandbox_result["status"] == "SUCCESS":
            result = self._extract_result(
                sandbox_result["stdout"]
            )

        return ExecutionResult(
            status=sandbox_result["status"],
            result=result,
            stdout=sandbox_result["stdout"],
            stderr=sandbox_result["stderr"],
            execution_time_ms=sandbox_result["execution_time_ms"],
            error=sandbox_result["error"],
        )

    @staticmethod
    def _extract_result(stdout: str) -> Optional[float]:
        """
        Extract the machine-readable result from stdout.

        Expected format:

        __VERITY_RESULT__: 25000
        """

        for line in stdout.splitlines():
            line = line.strip()

            if not line.startswith(RESULT_MARKER):
                continue

            value_text = line[len(RESULT_MARKER):].strip()

            try:
                value = float(value_text)
            except ValueError:
                return None

            if not math.isfinite(value):
                return None

            return value

        return None
"""
VERITYAI Execution Engine.

Coordinates validation and sandbox execution.
"""

from dataclasses import dataclass
from typing import Any, Optional

from .sandbox import Sandbox
from .validator import CodeValidator


@dataclass
class ExecutionResult:
    """
    Structured result returned by the execution layer.
    """

    status: str
    result: Optional[Any] = None
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None


class Executor:
    """
    Main execution interface for VERITYAI.

    Generated code must pass static validation before it is
    sent to the sandbox.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.validator = CodeValidator()
        self.sandbox = Sandbox(
            timeout_seconds=timeout_seconds
        )

    def execute(self, code: str) -> ExecutionResult:
        """
        Validate and execute generated Python code.
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

        return ExecutionResult(
            status=sandbox_result["status"],
            stdout=sandbox_result["stdout"],
            stderr=sandbox_result["stderr"],
            execution_time_ms=sandbox_result[
                "execution_time_ms"
            ],
            error=sandbox_result["error"],
        )
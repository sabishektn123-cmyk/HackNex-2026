"""
VERITYAI Sandbox

Runs validated Python calculation code in a separate process.

This is a hackathon-level isolation layer, not a production-grade
security boundary.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path
from typing import Optional


class SandboxError(Exception):
    """Raised when sandbox execution cannot be started safely."""


class Sandbox:
    """
    Controlled subprocess execution environment.

    The generated code is executed in a separate Python process.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout_seconds = timeout_seconds

    def run(self, code: str) -> dict:
        """
        Execute code in a controlled subprocess.

        Returns a structured dictionary containing:
        - status
        - stdout
        - stderr
        - execution_time_ms
        - error
        """

        if not isinstance(code, str):
            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": 0,
                "error": "Code must be provided as a string.",
            }

        if not code.strip():
            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": 0,
                "error": "Code cannot be empty.",
            }

        start_time = time.perf_counter()

        try:
            with tempfile.TemporaryDirectory(
                prefix="verityai_"
            ) as temp_dir:

                working_directory = Path(temp_dir)

                script_path = working_directory / "calculation.py"

                script_path.write_text(
                    textwrap.dedent(code),
                    encoding="utf-8",
                )

                environment = self._build_environment(
                    working_directory
                )

                process = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-S",
                        str(script_path),
                    ],
                    cwd=str(working_directory),
                    env=environment,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    shell=False,
                )

                elapsed_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                if process.returncode != 0:
                    return {
                        "status": "ERROR",
                        "stdout": process.stdout,
                        "stderr": process.stderr,
                        "execution_time_ms": elapsed_ms,
                        "error": (
                            f"Process exited with "
                            f"code {process.returncode}."
                        ),
                    }

                return {
                    "status": "SUCCESS",
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "execution_time_ms": elapsed_ms,
                    "error": None,
                }

        except subprocess.TimeoutExpired as exc:
            elapsed_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return {
                "status": "TIMEOUT",
                "stdout": self._decode_output(exc.stdout),
                "stderr": self._decode_output(exc.stderr),
                "execution_time_ms": elapsed_ms,
                "error": (
                    f"Execution exceeded the "
                    f"{self.timeout_seconds} second timeout."
                ),
            }

        except OSError as exc:
            elapsed_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return {
                "status": "ERROR",
                "stdout": "",
                "stderr": "",
                "execution_time_ms": elapsed_ms,
                "error": str(exc),
            }

    @staticmethod
    def _decode_output(output: Optional[object]) -> str:
        """Convert subprocess output to a safe string."""

        if output is None:
            return ""

        if isinstance(output, bytes):
            return output.decode(
                "utf-8",
                errors="replace",
            )

        return str(output)

    @staticmethod
    def _build_environment(
        working_directory: Path,
    ) -> dict[str, str]:
        """
        Build a minimal environment for the subprocess.
        """

        return {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUNBUFFERED": "1",
            "HOME": str(working_directory),
            "TEMP": str(working_directory),
            "TMP": str(working_directory),
        }
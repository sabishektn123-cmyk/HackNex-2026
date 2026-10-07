"""
VERITYAI Code Validator

Performs static security analysis of AI-generated Python code
before the code is allowed to execute.

This module uses Python's AST parser instead of executing code.
"""

import ast
from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationResult:
    """Result of static code validation."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class CodeValidator:
    """
    Static security validator for AI-generated Python code.

    The validator analyzes Python source code using AST and blocks
    dangerous imports, functions, and operations.
    """

    # Imports that should never be allowed in generated calculation code.
    BLOCKED_IMPORTS = {
        "os",
        "subprocess",
        "socket",
        "requests",
        "http",
        "urllib",
        "shutil",
        "pathlib",
        "sys",
        "ctypes",
        "pickle",
        "builtins",
        "multiprocessing",
        "threading",
    }

    # Dangerous built-in functions.
    BLOCKED_FUNCTIONS = {
        "eval",
        "exec",
        "compile",
        "__import__",
        "input",
        "breakpoint",
    }

    # Dangerous attribute calls.
    BLOCKED_ATTRIBUTES = {
        "system",
        "popen",
        "remove",
        "unlink",
        "rmdir",
        "rmtree",
        "chmod",
        "chown",
    }

    def validate(self, code: str) -> ValidationResult:
        """
        Validate Python source code without executing it.
        """

        if not isinstance(code, str):
            return ValidationResult(
                valid=False,
                errors=["Code must be provided as a string."]
            )

        if not code.strip():
            return ValidationResult(
                valid=False,
                errors=["Code cannot be empty."]
            )

        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            return ValidationResult(
                valid=False,
                errors=[
                    f"Syntax error at line {exc.lineno}: {exc.msg}"
                ]
            )

        errors = []
        warnings = []

        for node in ast.walk(tree):

            # -------------------------------------------------
            # IMPORT VALIDATION
            # -------------------------------------------------

            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]

                    if module in self.BLOCKED_IMPORTS:
                        errors.append(
                            f"Blocked import: {module}"
                        )

            elif isinstance(node, ast.ImportFrom):
                module = (node.module or "").split(".")[0]

                if module in self.BLOCKED_IMPORTS:
                    errors.append(
                        f"Blocked import: {module}"
                    )

            # -------------------------------------------------
            # FUNCTION VALIDATION
            # -------------------------------------------------

            elif isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):
                    function_name = node.func.id

                    if function_name in self.BLOCKED_FUNCTIONS:
                        errors.append(
                            f"Blocked function: {function_name}"
                        )

                elif isinstance(node.func, ast.Attribute):
                    attribute_name = node.func.attr

                    if attribute_name in self.BLOCKED_ATTRIBUTES:
                        errors.append(
                            f"Blocked operation: {attribute_name}"
                        )

            # -------------------------------------------------
            # DYNAMIC ATTRIBUTE ACCESS
            # -------------------------------------------------

            elif isinstance(node, ast.Attribute):

                if node.attr in {
                    "__globals__",
                    "__builtins__",
                    "__class__",
                    "__subclasses__",
                    "__bases__",
                    "__mro__",
                }:
                    errors.append(
                        f"Blocked dangerous attribute: {node.attr}"
                    )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
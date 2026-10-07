"""
VERITYAI Code Validator

Performs static security analysis of AI-generated Python code
before execution.

Important:
This validator is one layer of security.
It must always be combined with sandboxed execution.
"""

import ast
from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class CodeValidator:
    """
    Static security validator for AI-generated Python code.
    """

    # Imports that are never allowed.
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
        "importlib",
        "inspect",
    }

    # Functions that could execute arbitrary code,
    # access files, inspect the runtime, or dynamically load code.
    BLOCKED_FUNCTIONS = {
        "eval",
        "exec",
        "compile",
        "__import__",
        "input",
        "breakpoint",
        "open",
        "help",
        "dir",
        "globals",
        "locals",
        "vars",
        "getattr",
        "setattr",
        "delattr",
    }

    # Dangerous attribute operations.
    BLOCKED_ATTRIBUTES = {
        "system",
        "popen",
        "remove",
        "unlink",
        "rmdir",
        "rmtree",
        "chmod",
        "chown",
        "__globals__",
        "__builtins__",
        "__class__",
        "__subclasses__",
        "__bases__",
        "__mro__",
        "__dict__",
        "__getattribute__",
    }

    def validate(self, code: str) -> ValidationResult:
        """
        Validate Python code without executing it.
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

        # Parse only. Never execute.
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

            # -----------------------------------------
            # Import validation
            # -----------------------------------------
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

            # -----------------------------------------
            # Function-call validation
            # -----------------------------------------
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

            # -----------------------------------------
            # Attribute validation
            # -----------------------------------------
            elif isinstance(node, ast.Attribute):

                attribute_name = node.attr

                if attribute_name in self.BLOCKED_ATTRIBUTES:
                    errors.append(
                        f"Blocked dangerous attribute: {attribute_name}"
                    )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
import pytest

from execution.pipeline import VerificationPipeline
from execution.validator import CodeValidator


@pytest.fixture
def pipeline():
    return VerificationPipeline(timeout_seconds=1.0)


@pytest.fixture
def validator():
    return CodeValidator()


# ---------------------------------------------------------
# Dangerous imports
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [
        "import os",
        "import subprocess",
        "import socket",
        "import requests",
        "import shutil",
        "import pathlib",
        "import sys",
        "import ctypes",
        "import pickle",
        "import importlib",
        "import inspect",
        "import threading",
        "import multiprocessing",
    ],
)
def test_dangerous_imports_are_blocked(validator, code):
    result = validator.validate(code)

    assert result.valid is False


# ---------------------------------------------------------
# Dangerous built-in functions
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [
        'eval("1 + 1")',
        'exec("print(1)")',
        'compile("1 + 1", "", "eval")',
        '__import__("os")',
        'open("secret.txt")',
        "input()",
        "globals()",
        "locals()",
        "vars()",
        'getattr(object(), "__class__")',
        'setattr(object(), "x", 1)',
        'delattr(object(), "x")',
    ],
)
def test_dangerous_functions_are_blocked(validator, code):
    result = validator.validate(code)

    assert result.valid is False


# ---------------------------------------------------------
# Dangerous attributes
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [
        "x.__class__",
        "x.__dict__",
        "x.__globals__",
        "x.__builtins__",
        "x.__subclasses__()",
        "x.__bases__",
        "x.__mro__",
        "x.__getattribute__('x')",
    ],
)
def test_dangerous_attributes_are_blocked(validator, code):
    result = validator.validate(code)

    assert result.valid is False


# ---------------------------------------------------------
# Dangerous filesystem operations
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [
        'os.system("whoami")',
        'os.remove("important.txt")',
        'os.unlink("important.txt")',
        'os.rmdir("important")',
        'os.chmod("important.txt", 0o777)',
        'shutil.rmtree("important")',
    ],
)
def test_dangerous_operations_are_not_allowed(validator, code):
    result = validator.validate(code)

    assert result.valid is False


# ---------------------------------------------------------
# Pipeline security invariant
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [
        'import os\nprint("__VERITY_RESULT__:", os.system("whoami"))',
        'import subprocess\nprint("__VERITY_RESULT__:", 1)',
        'eval("print(1)")',
        'exec("print(1)")',
        'open("secret.txt").read()',
    ],
)
def test_malicious_code_never_becomes_verified(pipeline, code):
    result = pipeline.verify_calculation(
        code=code,
        expected=1,
    )

    assert result.status != "VERIFIED"


# ---------------------------------------------------------
# Infinite loop / timeout
# ---------------------------------------------------------


def test_infinite_loop_is_stopped(pipeline):
    result = pipeline.verify_calculation(
        code="""
while True:
    pass
""",
        expected=1,
    )

    assert result.status != "VERIFIED"


# ---------------------------------------------------------
# NaN / Infinity attacks
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "float('nan')",
        "float('inf')",
        "float('-inf')",
    ],
)
def test_non_finite_results_are_not_verified(pipeline, value):
    result = pipeline.verify_calculation(
        code=f"""
result = {value}
print("__VERITY_RESULT__:", result)
""",
        expected=1,
    )

    assert result.status != "VERIFIED"


# ---------------------------------------------------------
# Invalid result injection
# ---------------------------------------------------------


def test_fake_text_result_is_not_accepted(pipeline):
    result = pipeline.verify_calculation(
        code="""
print("__VERITY_RESULT__: TRUSTED")
""",
        expected=100,
    )

    assert result.status != "VERIFIED"


def test_missing_result_marker_is_not_accepted(pipeline):
    result = pipeline.verify_calculation(
        code="""
print("100")
""",
        expected=100,
    )

    assert result.status != "VERIFIED"


# ---------------------------------------------------------
# Syntax attack
# ---------------------------------------------------------


def test_malformed_code_is_not_verified(pipeline):
    result = pipeline.verify_calculation(
        code="""
result = (
""",
        expected=100,
    )

    assert result.status != "VERIFIED"


# ---------------------------------------------------------
# Invalid input
# ---------------------------------------------------------


def test_non_string_code_is_not_verified(pipeline):
    result = pipeline.verify_calculation(
        code=None,
        expected=100,
    )

    assert result.status != "VERIFIED"
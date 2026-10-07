from execution.pipeline import VerificationPipeline


def test_end_to_end_verified_answer():
    """
    Correct calculation should produce VERIFIED.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
sales = 1000
expenses = 400
profit = sales - expenses
print("__VERITY_RESULT__:", profit)
""",
        expected=600,
    )

    assert result.status == "VERIFIED"
    assert result.expected == 600.0
    assert result.actual == 600.0
    assert result.verification is not None
    assert result.verification.status == "VERIFIED"


def test_end_to_end_wrong_answer_is_rejected():
    """
    A mismatch between the expected answer and calculated
    result must never be accepted.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
sales = 1000
expenses = 400
profit = sales - expenses
print("__VERITY_RESULT__:", profit)
""",
        expected=700,
    )

    assert result.status == "VERIFICATION_FAILED"
    assert result.actual == 600.0
    assert result.expected == 700.0


def test_end_to_end_missing_result_abstains():
    """
    Code that does not produce a machine-readable result
    must result in CANNOT_DETERMINE.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
sales = 1000
expenses = 400
profit = sales - expenses
print(profit)
""",
        expected=600,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.actual is None
    assert result.abstention_reason is not None


def test_end_to_end_unsafe_code_is_not_verified():
    """
    Unsafe generated code must never become VERIFIED.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
import os
result = os.system("whoami")
print("__VERITY_RESULT__:", result)
""",
        expected=0,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.status != "VERIFIED"


def test_end_to_end_runtime_error_abstains():
    """
    Runtime errors must not produce a verified answer.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
sales = 1000
expenses = 0
profit = sales / expenses
print("__VERITY_RESULT__:", profit)
""",
        expected=600,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.status != "VERIFIED"


def test_end_to_end_timeout_abstains():
    """
    Infinite execution must be stopped by the sandbox.
    """

    pipeline = VerificationPipeline(timeout_seconds=0.5)

    result = pipeline.verify_calculation(
        code="""
while True:
    pass
""",
        expected=100,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.status != "VERIFIED"


def test_end_to_end_ambiguous_input_abstains():
    """
    Explicit ambiguity must prevent verification.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 500
print("__VERITY_RESULT__:", result)
""",
        expected=500,
        ambiguous=True,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.abstention_reason == (
        "Input or calculation is ambiguous."
    )


def test_end_to_end_conflicting_evidence_abstains():
    """
    Conflicting evidence must prevent verification.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 500
print("__VERITY_RESULT__:", result)
""",
        expected=500,
        conflicting=True,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.abstention_reason == (
        "Conflicting evidence was detected."
    )


def test_end_to_end_decimal_calculation():
    """
    Floating-point calculations within tolerance should verify.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
price = 19.99
quantity = 3
total = price * quantity
print("__VERITY_RESULT__:", total)
""",
        expected=59.97,
    )

    assert result.status == "VERIFIED"


def test_end_to_end_zero_result():
    """
    Zero is a valid numerical result and must not be treated
    as missing.
    """

    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 0
print("__VERITY_RESULT__:", result)
""",
        expected=0,
    )

    assert result.status == "VERIFIED"
    assert result.actual == 0.0
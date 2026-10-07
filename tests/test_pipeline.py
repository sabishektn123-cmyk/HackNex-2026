from execution.pipeline import VerificationPipeline


def test_correct_calculation_is_verified():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print("__VERITY_RESULT__:", result)
""",
        expected=300,
    )

    assert result.status == "VERIFIED"
    assert result.actual == 300.0


def test_wrong_calculation_fails_verification():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print("__VERITY_RESULT__:", result)
""",
        expected=350,
    )

    assert result.status == "VERIFICATION_FAILED"
    assert result.actual == 300.0
    assert result.expected == 350.0


def test_missing_result_cannot_be_verified():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print(result)
""",
        expected=300,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_unsafe_code_never_reaches_verification():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
import os
print("__VERITY_RESULT__:", os.system("whoami"))
""",
        expected=0,
    )

    assert result.status == "EXECUTION_FAILED"


def test_runtime_error_never_becomes_verified():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 1 / 0
print("__VERITY_RESULT__:", result)
""",
        expected=0,
    )

    assert result.status == "EXECUTION_FAILED"
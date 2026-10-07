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


def test_missing_result_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print(result)
""",
        expected=300,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.abstention_reason == (
        "Actual calculated value is missing."
    )


def test_missing_expected_value_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print("__VERITY_RESULT__:", result)
""",
        expected=None,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_ambiguous_calculation_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print("__VERITY_RESULT__:", result)
""",
        expected=300,
        ambiguous=True,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.abstention_reason == (
        "Input or calculation is ambiguous."
    )


def test_conflicting_evidence_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 100 + 200
print("__VERITY_RESULT__:", result)
""",
        expected=300,
        conflicting=True,
    )

    assert result.status == "CANNOT_DETERMINE"
    assert result.abstention_reason == (
        "Conflicting evidence was detected."
    )


def test_unsafe_code_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
import os
print("__VERITY_RESULT__:", os.system("whoami"))
""",
        expected=0,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_runtime_error_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 1 / 0
print("__VERITY_RESULT__:", result)
""",
        expected=0,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_timeout_abstains():
    pipeline = VerificationPipeline(timeout_seconds=0.5)

    result = pipeline.verify_calculation(
        code="""
while True:
    pass
""",
        expected=1,
    )

    assert result.status == "CANNOT_DETERMINE"
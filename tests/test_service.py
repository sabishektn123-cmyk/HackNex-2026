from execution.service import VerificationService


def test_service_returns_verified_response():
    service = VerificationService()

    response = service.verify(
        question="What is the total?",
        generated_code="""
a = 100
b = 200
result = a + b
print("__VERITY_RESULT__:", result)
""",
        claimed_result=300,
        dataset="sales.csv",
    )

    assert response["status"] == "VERIFIED"
    assert response["expected"] == 300.0
    assert response["actual"] == 300.0
    assert response["verification"]["status"] == "VERIFIED"


def test_service_returns_verification_failure():
    service = VerificationService()

    response = service.verify(
        question="What is the total?",
        generated_code="""
a = 100
b = 200
result = a + b
print("__VERITY_RESULT__:", result)
""",
        claimed_result=500,
        dataset="sales.csv",
    )

    assert response["status"] == "VERIFICATION_FAILED"
    assert response["expected"] == 500.0
    assert response["actual"] == 300.0


def test_service_returns_abstention():
    service = VerificationService()

    response = service.verify(
        question="What is the total?",
        generated_code="""
print("I cannot calculate this")
""",
        claimed_result=300,
        dataset="sales.csv",
    )

    assert response["status"] == "CANNOT_DETERMINE"
    assert response["abstention_reason"] is not None


def test_service_rejects_unsafe_code():
    service = VerificationService()

    response = service.verify(
        question="Execute command",
        generated_code="""
import os
os.system("whoami")
print("__VERITY_RESULT__:", 1)
""",
        claimed_result=1,
        dataset="data.csv",
    )

    assert response["status"] == "CANNOT_DETERMINE"
    assert response["status"] != "VERIFIED"


def test_service_handles_conflicting_evidence():
    service = VerificationService()

    response = service.verify(
        question="What is the total?",
        generated_code="""
result = 300
print("__VERITY_RESULT__:", result)
""",
        claimed_result=300,
        dataset="sales.csv",
        conflicting=True,
    )

    assert response["status"] == "CANNOT_DETERMINE"


def test_service_handles_ambiguous_evidence():
    service = VerificationService()

    response = service.verify(
        question="What is the total?",
        generated_code="""
result = 300
print("__VERITY_RESULT__:", result)
""",
        claimed_result=300,
        dataset="sales.csv",
        ambiguous=True,
    )

    assert response["status"] == "CANNOT_DETERMINE"
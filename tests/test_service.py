from execution.service import VerificationService


def test_verified_response_contains_proof():
    service = VerificationService()

    response = service.verify(
        question="What is 100 * 15?",
        generated_code="print('__VERITY_RESULT__:', 100 * 15)",
        claimed_result=1500,
        dataset="100 * 15",
    )

    assert response["status"] == "VERIFIED"
    assert response["answer"] == 1500

    assert response["verification"]["status"] == "VERIFIED"

    assert response["confidence"]["level"] == "HIGH"
    assert response["confidence"]["score"] == 100.0

    assert response["audit"]["final_status"] == "VERIFIED"
    assert len(response["audit"]["code_hash"]) == 64


def test_wrong_answer_has_no_trusted_answer():
    service = VerificationService()

    response = service.verify(
        question="What is 100 * 15?",
        generated_code="print('__VERITY_RESULT__:', 100 * 15)",
        claimed_result=1499,
        dataset="100 * 15",
    )

    assert response["status"] == "VERIFICATION_FAILED"
    assert response["answer"] is None

    assert response["verification"]["status"] == "VERIFICATION_FAILED"


def test_unsafe_code_cannot_be_verified():
    service = VerificationService()

    response = service.verify(
        question="Calculate result",
        generated_code="import os\nprint('__VERITY_RESULT__:', 100)",
        claimed_result=100,
        dataset="test",
    )

    assert response["status"] == "CANNOT_DETERMINE"
    assert response["answer"] is None
    assert response["confidence"]["level"] in {"LOW", "MEDIUM"}
    assert response["audit"]["final_status"] == "CANNOT_DETERMINE"


def test_ambiguous_data_abstains():
    service = VerificationService()

    response = service.verify(
        question="Calculate the value",
        generated_code="print('__VERITY_RESULT__:', 100)",
        claimed_result=100,
        dataset="ambiguous dataset",
        ambiguous=True,
    )

    assert response["status"] == "CANNOT_DETERMINE"
    assert response["answer"] is None
    assert response["audit"]["abstention_reason"] is not None


def test_conflicting_data_abstains():
    service = VerificationService()

    response = service.verify(
        question="Calculate the value",
        generated_code="print('__VERITY_RESULT__:', 100)",
        claimed_result=100,
        dataset="conflicting dataset",
        conflicting=True,
    )

    assert response["status"] == "CANNOT_DETERMINE"
    assert response["answer"] is None
    assert response["audit"]["abstention_reason"] is not None
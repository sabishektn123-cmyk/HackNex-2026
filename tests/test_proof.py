from execution.audit import AuditTrail
from execution.confidence import ConfidenceEngine
from execution.proof import ProofPackage
from execution.verifier import Verifier


def test_verified_proof_package():
    verifier = Verifier()

    verification = verifier.verify(
        expected=1500,
        actual=1500,
    )

    confidence = ConfidenceEngine().calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=1.0,
    )

    audit = AuditTrail.create_record(
        question="What is 100 * 15?",
        dataset="test dataset",
        generated_code="print('__VERITY_RESULT__:', 100 * 15)",
        execution_status="SUCCESS",
        execution_output="__VERITY_RESULT__: 1500",
        expected_result=1500,
        actual_result=1500,
        verification_status=verification.status,
        verification_difference=verification.difference,
        verification_tolerance=verification.tolerance,
        confidence_score=confidence.score,
        confidence_level=confidence.level,
        final_status="VERIFIED",
    )

    proof = ProofPackage.build(
        status="VERIFIED",
        answer=1500,
        verification=verification,
        confidence=confidence,
        audit=audit,
    )

    result = proof.to_dict()

    assert result["status"] == "VERIFIED"
    assert result["answer"] == 1500
    assert result["verification"]["status"] == "VERIFIED"
    assert result["confidence"]["level"] == "HIGH"
    assert result["audit"]["final_status"] == "VERIFIED"
    assert len(result["audit"]["code_hash"]) == 64
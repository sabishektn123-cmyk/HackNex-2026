import json

from execution.audit import AuditTrail


def test_audit_record_contains_required_information():
    record = AuditTrail.create_record(
        question="What is the total revenue?",
        dataset="sales.csv",
        generated_code="result = 100 + 200",
        execution_status="SUCCESS",
        execution_output="__VERITY_RESULT__: 300",
        expected_result=300,
        actual_result=300,
        verification_status="VERIFIED",
        final_status="VERIFIED",
    )

    assert record.question == "What is the total revenue?"
    assert record.dataset == "sales.csv"
    assert record.generated_code == "result = 100 + 200"
    assert record.execution_status == "SUCCESS"
    assert record.actual_result == 300
    assert record.verification_status == "VERIFIED"
    assert record.final_status == "VERIFIED"


def test_audit_record_generates_code_hash():
    record = AuditTrail.create_record(
        question="Calculate total",
        dataset="sales.csv",
        generated_code="result = 100 + 200",
        execution_status="SUCCESS",
    )

    assert record.code_hash
    assert len(record.code_hash) == 64


def test_same_code_produces_same_hash():
    first = AuditTrail.create_record(
        question="Calculate total",
        dataset="sales.csv",
        generated_code="result = 100 + 200",
        execution_status="SUCCESS",
    )

    second = AuditTrail.create_record(
        question="Another question",
        dataset="other.csv",
        generated_code="result = 100 + 200",
        execution_status="SUCCESS",
    )

    assert first.code_hash == second.code_hash


def test_different_code_produces_different_hash():
    first = AuditTrail.create_record(
        question="Calculate total",
        dataset="sales.csv",
        generated_code="result = 100 + 200",
        execution_status="SUCCESS",
    )

    second = AuditTrail.create_record(
        question="Calculate total",
        dataset="sales.csv",
        generated_code="result = 100 + 201",
        execution_status="SUCCESS",
    )

    assert first.code_hash != second.code_hash


def test_audit_record_serializes_to_json():
    record = AuditTrail.create_record(
        question="What is total revenue?",
        dataset="sales.csv",
        generated_code="result = 100 + 200",
        execution_status="SUCCESS",
        expected_result=300,
        actual_result=300,
        verification_status="VERIFIED",
        confidence_score=100.0,
        confidence_level="HIGH",
        final_status="VERIFIED",
    )

    data = json.loads(record.to_json())

    assert data["question"] == "What is total revenue?"
    assert data["dataset"] == "sales.csv"
    assert data["actual_result"] == 300
    assert data["verification_status"] == "VERIFIED"
    assert data["confidence_score"] == 100.0
    assert data["confidence_level"] == "HIGH"
    assert data["final_status"] == "VERIFIED"


def test_abstention_reason_is_recorded():
    record = AuditTrail.create_record(
        question="What is the total?",
        dataset="sales.csv",
        generated_code="print(123)",
        execution_status="SUCCESS",
        abstention_reason="Actual calculated value is missing.",
        final_status="CANNOT_DETERMINE",
    )

    assert record.abstention_reason == (
        "Actual calculated value is missing."
    )
    assert record.final_status == "CANNOT_DETERMINE"
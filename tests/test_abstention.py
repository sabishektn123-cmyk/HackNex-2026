from execution.abstention import AbstentionEngine


def test_valid_evidence_allows_verification():
    engine = AbstentionEngine()

    result = engine.evaluate(
        expected=300,
        actual=300,
        execution_status="SUCCESS",
    )

    assert result.should_abstain is False
    assert result.status == "PROCEED"


def test_missing_expected_value_abstains():
    engine = AbstentionEngine()

    result = engine.evaluate(
        expected=None,
        actual=300,
        execution_status="SUCCESS",
    )

    assert result.should_abstain is True
    assert result.status == "CANNOT_DETERMINE"


def test_missing_actual_value_abstains():
    engine = AbstentionEngine()

    result = engine.evaluate(
        expected=300,
        actual=None,
        execution_status="SUCCESS",
    )

    assert result.should_abstain is True
    assert result.status == "CANNOT_DETERMINE"


def test_execution_failure_abstains():
    engine = AbstentionEngine()

    result = engine.evaluate(
        expected=300,
        actual=None,
        execution_status="TIMEOUT",
    )

    assert result.should_abstain is True
    assert result.status == "CANNOT_DETERMINE"


def test_conflicting_evidence_abstains():
    engine = AbstentionEngine()

    result = engine.evaluate(
        expected=300,
        actual=300,
        execution_status="SUCCESS",
        conflicting=True,
    )

    assert result.should_abstain is True
    assert result.status == "CANNOT_DETERMINE"


def test_ambiguous_evidence_abstains():
    engine = AbstentionEngine()

    result = engine.evaluate(
        expected=300,
        actual=300,
        execution_status="SUCCESS",
        ambiguous=True,
    )

    assert result.should_abstain is True
    assert result.status == "CANNOT_DETERMINE"
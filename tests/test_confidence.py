from execution.confidence import ConfidenceEngine


def test_fully_verified_result_has_high_confidence():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=1.0,
        conflicting=False,
        ambiguous=False,
    )

    assert result.score == 100.0
    assert result.level == "HIGH"


def test_weak_evidence_reduces_confidence():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=0.5,
        conflicting=False,
        ambiguous=False,
    )

    assert result.score == 90.0
    assert result.level == "HIGH"


def test_conflicting_evidence_reduces_confidence():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=1.0,
        conflicting=True,
        ambiguous=False,
    )

    assert result.score == 90.0


def test_ambiguity_reduces_confidence():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=1.0,
        conflicting=False,
        ambiguous=True,
    )

    assert result.score == 90.0


def test_failed_execution_produces_low_confidence():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=False,
        verification_passed=False,
        evidence_quality=0.0,
        conflicting=True,
        ambiguous=True,
    )

    assert result.score == 0.0
    assert result.level == "LOW"


def test_evidence_quality_is_clamped():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=5.0,
    )

    assert result.score == 100.0


def test_negative_evidence_quality_is_clamped():
    engine = ConfidenceEngine()

    result = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=-5.0,
    )

    assert result.score == 80.0


def test_confidence_is_deterministic():
    engine = ConfidenceEngine()

    first = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=0.75,
        conflicting=False,
        ambiguous=False,
    )

    second = engine.calculate(
        execution_success=True,
        verification_passed=True,
        evidence_quality=0.75,
        conflicting=False,
        ambiguous=False,
    )

    assert first.score == second.score
    assert first.level == second.level
    assert first.reasons == second.reasons
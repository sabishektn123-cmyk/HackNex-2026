from execution.verifier import Verifier


def test_matching_integer_values_are_verified():
    verifier = Verifier()

    result = verifier.verify(
        expected=25000,
        actual=25000,
    )

    assert result.status == "VERIFIED"
    assert result.difference == 0


def test_matching_float_values_are_verified():
    verifier = Verifier()

    result = verifier.verify(
        expected=100.0,
        actual=100.00000001,
    )

    assert result.status == "VERIFIED"


def test_mismatching_values_fail_verification():
    verifier = Verifier()

    result = verifier.verify(
        expected=25000,
        actual=24750,
    )

    assert result.status == "VERIFICATION_FAILED"
    assert result.difference == 250


def test_non_numeric_expected_value_cannot_be_determined():
    verifier = Verifier()

    result = verifier.verify(
        expected="25000",
        actual=25000,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_non_numeric_actual_value_cannot_be_determined():
    verifier = Verifier()

    result = verifier.verify(
        expected=25000,
        actual="25000",
    )

    assert result.status == "CANNOT_DETERMINE"


def test_nan_is_rejected():
    verifier = Verifier()

    result = verifier.verify(
        expected=float("nan"),
        actual=100,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_infinity_is_rejected():
    verifier = Verifier()

    result = verifier.verify(
        expected=float("inf"),
        actual=100,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_boolean_is_not_treated_as_number():
    verifier = Verifier()

    result = verifier.verify(
        expected=True,
        actual=1,
    )

    assert result.status == "CANNOT_DETERMINE"
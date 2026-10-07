from execution.pipeline import VerificationPipeline


def test_missing_data_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
values = []
if not values:
    print("NO_DATA")
""",
        expected=100,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_empty_dataset_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
data = []
if len(data) == 0:
    print("EMPTY_DATASET")
""",
        expected=0,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_ambiguous_duplicate_values_abstain():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
values = [100, 100, 200]
result = 100
print("__VERITY_RESULT__:", result)
""",
        expected=100,
        ambiguous=True,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_conflicting_data_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
source_a = 500
source_b = 700
result = source_a
print("__VERITY_RESULT__:", result)
""",
        expected=500,
        conflicting=True,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_nan_data_is_not_verified():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = float("nan")
print("__VERITY_RESULT__:", result)
""",
        expected=100,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_infinite_data_is_not_verified():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = float("inf")
print("__VERITY_RESULT__:", result)
""",
        expected=100,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_extremely_large_value_is_handled():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 10 ** 100
print("__VERITY_RESULT__:", result)
""",
        expected=10 ** 100,
    )

    assert result.status == "VERIFIED"


def test_negative_value_is_valid_when_expected():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
revenue = 100
cost = 150
loss = revenue - cost
print("__VERITY_RESULT__:", loss)
""",
        expected=-50,
    )

    assert result.status == "VERIFIED"
    assert result.actual == -50.0


def test_zero_is_valid_data():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 0
print("__VERITY_RESULT__:", result)
""",
        expected=0,
    )

    assert result.status == "VERIFIED"


def test_malformed_numeric_output_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
print("__VERITY_RESULT__: not-a-number")
""",
        expected=100,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_missing_result_from_partial_data_abstains():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
data = [100, 200, None]

if any(value is None for value in data):
    print("INSUFFICIENT_DATA")
""",
        expected=300,
    )

    assert result.status == "CANNOT_DETERMINE"


def test_conflicting_evidence_never_becomes_verified():
    pipeline = VerificationPipeline()

    result = pipeline.verify_calculation(
        code="""
result = 600
print("__VERITY_RESULT__:", result)
""",
        expected=600,
        conflicting=True,
    )

    assert result.status != "VERIFIED"
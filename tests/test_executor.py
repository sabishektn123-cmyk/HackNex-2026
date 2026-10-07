from execution.executor import ExecutionResult, Executor


def test_executor_rejects_empty_code():
    executor = Executor()

    result = executor.execute("")

    assert result.status == "ERROR"
    assert result.error == "Code cannot be empty."


def test_executor_rejects_non_string_code():
    executor = Executor()

    result = executor.execute(None)

    assert result.status == "ERROR"
    assert result.error == "Code must be provided as a string."


def test_executor_requires_secure_execution():
    executor = Executor()

    result = executor.execute(
        "result = 100 + 200"
    )

    assert result.status == "NOT_IMPLEMENTED"
    assert result.error is not None
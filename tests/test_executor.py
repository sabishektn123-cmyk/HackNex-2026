from execution.executor import Executor


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


def test_executor_runs_safe_calculation():
    executor = Executor()

    result = executor.execute(
        "result = 100 + 200\nprint(result)"
    )

    assert result.status == "SUCCESS"
    assert "300" in result.stdout


def test_executor_blocks_os_import():
    executor = Executor()

    result = executor.execute(
        "import os\nresult = os.system('whoami')"
    )

    assert result.status == "REJECTED"
    assert "Blocked import: os" in result.stderr


def test_executor_blocks_subprocess():
    executor = Executor()

    result = executor.execute(
        "import subprocess\nsubprocess.run(['whoami'])"
    )

    assert result.status == "REJECTED"


def test_executor_handles_runtime_error():
    executor = Executor()

    result = executor.execute(
        "result = 1 / 0"
    )

    assert result.status == "ERROR"
    assert result.stderr


def test_executor_handles_timeout():
    executor = Executor(timeout_seconds=1.0)

    result = executor.execute(
        "while True:\n    pass"
    )

    assert result.status == "TIMEOUT"


def test_executor_extracts_numeric_result():
    executor = Executor()

    result = executor.execute(
        """
result = 100 + 200
print("__VERITY_RESULT__:", result)
"""
    )

    assert result.status == "SUCCESS"
    assert result.result == 300.0


def test_executor_returns_none_without_result_marker():
    executor = Executor()

    result = executor.execute(
        """
result = 100 + 200
print(result)
"""
    )

    assert result.status == "SUCCESS"
    assert result.result is None


def test_executor_rejects_nan_result():
    executor = Executor()

    result = executor.execute(
        """
result = float("nan")
print("__VERITY_RESULT__:", result)
"""
    )

    assert result.status == "SUCCESS"
    assert result.result is None
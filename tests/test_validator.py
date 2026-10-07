from execution.validator import CodeValidator


def test_safe_calculation_is_allowed():
    validator = CodeValidator()

    result = validator.validate(
        "result = 100 + 200"
    )

    assert result.valid is True
    assert result.errors == []


def test_os_import_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "import os\nresult = os.system('dir')"
    )

    assert result.valid is False
    assert any("Blocked import: os" in error for error in result.errors)


def test_subprocess_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "import subprocess\nsubprocess.run(['whoami'])"
    )

    assert result.valid is False


def test_eval_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "result = eval('100 + 200')"
    )

    assert result.valid is False


def test_exec_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "exec('result = 123')"
    )

    assert result.valid is False


def test_import_function_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "module = __import__('os')"
    )

    assert result.valid is False


def test_empty_code_is_rejected():
    validator = CodeValidator()

    result = validator.validate("")

    assert result.valid is False


def test_invalid_python_is_rejected():
    validator = CodeValidator()

    result = validator.validate(
        "result ="
    )

    assert result.valid is False
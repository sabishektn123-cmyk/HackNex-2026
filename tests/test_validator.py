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
def test_open_file_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "data = open('secret.txt').read()"
    )

    assert result.valid is False
    assert "Blocked function: open" in result.errors


def test_importlib_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "import importlib\nimportlib.import_module('os')"
    )

    assert result.valid is False
    assert "Blocked import: importlib" in result.errors


def test_globals_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "x = globals()"
    )

    assert result.valid is False
    assert "Blocked function: globals" in result.errors


def test_getattr_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "getattr(object, '__class__')"
    )

    assert result.valid is False
    assert "Blocked function: getattr" in result.errors


def test_dangerous_attribute_is_blocked():
    validator = CodeValidator()

    result = validator.validate(
        "x.__dict__"
    )

    assert result.valid is False
    assert any(
        "__dict__" in error
        for error in result.errors
    )


def test_normal_math_is_allowed():
    validator = CodeValidator()

    result = validator.validate(
        """
numbers = [10, 20, 30]
average = sum(numbers) / len(numbers)
print(average)
"""
    )

    assert result.valid is True
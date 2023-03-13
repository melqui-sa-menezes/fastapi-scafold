import pytest

from app.api.helpers.validators import (
    decimal_validator,
    empty_string_validator,
    number_validator,
)


def test_empty_string_validator():
    with pytest.raises(ValueError):
        empty_string_validator("")
    with pytest.raises(ValueError):
        empty_string_validator("  ")
    assert empty_string_validator("hello") == "hello"
    assert empty_string_validator("  hello  ") == "hello"


def test_decimal_validator():
    with pytest.raises(ValueError):
        decimal_validator(123.456)
    with pytest.raises(ValueError):
        decimal_validator(123456.78965)
    assert decimal_validator(12.34) == 12.34
    assert decimal_validator(12345.00) == 12345.00


def test_number_validator():
    with pytest.raises(ValueError):
        number_validator(0)
    with pytest.raises(ValueError):
        number_validator(-1)
    assert number_validator(1) == 1
    assert number_validator(100) == 100

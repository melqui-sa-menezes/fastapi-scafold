def empty_string_validator(text):
    if not text.strip():
        raise ValueError("Field cannot be an empty string")
    return text.strip()


def decimal_validator(number):
    if len(str(number).split(".")[-1]) > 2:
        raise ValueError("The value cannot have more than two decimal places")
    if len(str(number).replace('.', '')) > 10:
        raise ValueError("The value exceeds the expected size.")
    return number


def number_validator(number):
    if number <= 0:
        raise ValueError("The field must be greater than zero.")
    return number

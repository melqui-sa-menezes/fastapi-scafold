def empty_string_validator(text):
    if not text.strip():
        raise ValueError("O campo não pode ser uma string vazia")
    return text


def decimal_validator(number):
    if len(str(number).split(".")[-1]) > 2:
        raise ValueError("O valor não pode ter mais que duas casas decimais")
    if len(str(number).replace('.', '')) > 10:
        raise ValueError("O valor excede o tamanho esperado.")
    return number


def number_validator(number):
    if number <= 0:
        raise ValueError("O campo deve ser maior que zero")
    return number

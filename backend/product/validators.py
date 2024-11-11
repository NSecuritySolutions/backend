import re

from django.core.exceptions import ValidationError


def validate_field_name(value):
    """
    Валидатор проверяет, что строка содержит только латинские буквы, цифры и
    подчёркивания, и не начинается с цифры.
    """
    pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Допустимы только латинские буквы, цифры и подчёркивания, и строка не должна начинаться с цифры."
        )

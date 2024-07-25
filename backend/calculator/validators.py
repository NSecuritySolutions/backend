import re

from django.core.exceptions import ValidationError


def validate_latin_underscore(value: str):
    if not re.match(r"^[a-zA-Z_0-9]+$", value):
        raise ValidationError(
            "Поле может содержать только латинские символы и нижние подчеркивания."
        )

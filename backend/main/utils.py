import re

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class ParagraphsField(serializers.Field):
    def to_representation(self, value: str) -> list[str]:
        # Преобразование строки в массив абзацев
        paragraphs = re.split(r"\r?\n", value)
        return paragraphs


ParagraphsField = extend_schema_field(
    serializers.ListField(child=serializers.CharField())
)(ParagraphsField)

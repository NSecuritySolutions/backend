import re

from rest_framework import serializers


class ParagraphsField(serializers.Field):
    def to_representation(self, value: str):
        # Преобразование строки в массив абзацев
        paragraphs = re.split(r"\r?\n", value)
        return paragraphs

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from main.utils import ParagraphsField
from social.models import (
    Employee,
    OurGuarantees,
    Questions,
    QuestionsCategory,
    SocialInfo,
    Subguarantees,
    Team,
)


class QuestionsListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели вопроса."""

    answer = ParagraphsField()

    class Meta:
        model = Questions
        fields = ("id", "question", "answer")


class QuestionsByCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов, разбитых по категории."""

    questions = QuestionsListSerializer(many=True)

    class Meta:
        model = QuestionsCategory
        fields = ("id", "name", "icon", "questions")


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели работника."""

    phone = PhoneNumberField()

    class Meta:
        model = Employee
        fields = ("id", "image", "first_name", "last_name", "position", "phone")


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор для модели команды."""

    employees = EmployeeSerializer(many=True)
    description = ParagraphsField()

    class Meta:
        model = Team
        fields = ("id", "description", "employees", "active")


class SocialInfoSerializer(serializers.ModelSerializer):
    """Сериализатор модели социальной информации."""

    class Meta:
        model = SocialInfo
        fields = (
            "id",
            "phone",
            "email",
            "telegram",
            "whatsapp",
            "address",
            "founded",
            "projects_done",
            "active",
        )


class SubguranteeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подкатегории гарантии."""

    class Meta:
        model = Subguarantees
        fields = ("id", "text", "guarantee")


class OurGuaranteeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели гарантии."""

    subguarantees = SubguranteeSerializer(many=True)

    class Meta:
        model = OurGuarantees
        fields = ("id", "icon", "title", "is_big", "active", "subguarantees")

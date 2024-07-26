from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from social.models import OurGuarantees, QuestionsCategory, SocialInfo, Team
from social.serializers import (
    OurGuaranteeSerializer,
    QuestionsByCategorySerializer,
    SocialInfoSerializer,
    TeamSerializer,
)


@extend_schema(tags=["Вопросы"])
class QuestionsListView(ListModelMixin, GenericViewSet):
    """Список вопросов."""

    queryset = QuestionsCategory.objects.all()
    serializer_class = QuestionsByCategorySerializer


@extend_schema(tags=["Команда"])
class TeamListView(ListModelMixin, GenericViewSet):
    """Список команд."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("active",)


@extend_schema(tags=["Инфомация"])
class SocialInfoView(ListModelMixin, GenericViewSet):
    """Социальная информация."""

    queryset = SocialInfo.objects.all()
    serializer_class = SocialInfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("active",)


@extend_schema(tags=["Мы обеспечиваем"])
class OurGuaranteesView(ListModelMixin, GenericViewSet):
    """Список гарантий."""

    queryset = OurGuarantees.objects.all()
    serializer_class = OurGuaranteeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("active",)

from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from social.models import Questions, SocialInfo, Team
from social.serializers import (
    QuestionsListSerializer,
    SocialInfoSerializer,
    TeamSerializer,
)


@extend_schema(tags=["Вопросы"])
class QuestionsListView(ListModelMixin, GenericViewSet):
    """Список вопросов."""

    queryset = Questions.objects.all()
    serializer_class = QuestionsListSerializer


@extend_schema(tags=["Команда"])
class TeamListView(ListModelMixin, GenericViewSet):
    """Список команд."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@extend_schema(tags=["Инфомация"])
class SocialInfoView(ListModelMixin, GenericViewSet):
    """Социальная информация."""

    queryset = SocialInfo.objects.all()
    serializer_class = SocialInfoSerializer

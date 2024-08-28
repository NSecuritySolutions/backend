from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from application.models import Application
from application.serializers import (
    ApplicationListSerializer,
    ApplicationWithCalcSerializer,
    ApplicationWithFileSerializer,
    ApplicationWithSolutionCreateSerializer,
    ApplicationWithSolutionSerializer,
)


@extend_schema(
    tags=["Заявки"],
    responses=PolymorphicProxySerializer(
        component_name="Application",
        serializers=[
            ApplicationWithCalcSerializer,
            ApplicationWithFileSerializer,
            ApplicationWithSolutionSerializer,
        ],
        resource_type_field_name="model",
    ),
)
class ApplicationListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список заявок."""

    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer
    http_method_names = ("get",)


class ApplicationWithFileView(CreateModelMixin, GenericViewSet):
    """Создание обычной заявки."""

    serializer_class = ApplicationWithFileSerializer
    http_method_names = ("post",)


class ApplicationWithSolutionView(CreateModelMixin, GenericViewSet):
    """Создание заявки с готовым решением."""

    serializer_class = ApplicationWithSolutionCreateSerializer
    http_method_names = ("post",)


class ApplicationWithCalcView(CreateModelMixin, GenericViewSet):
    """Создание заявки с калькулятором."""

    serializer_class = ApplicationWithCalcSerializer
    http_method_names = ("post",)

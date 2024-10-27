from django.conf import settings
from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from application.celery_tasks import (
    send_calc_application,
    send_file_application,
    send_solution_application,
)
from application.models import Application
from application.serializers import (
    ApplicationListSerializer,
    ApplicationWithFileSerializer,
    ApplicationWithSolutionCreateSerializer,
    ApplicationWithSolutionSerializer,
    CalculatorJSONSerializer,
)


@extend_schema(
    tags=["Заявки"],
    responses=PolymorphicProxySerializer(
        component_name="Single application",
        serializers=[
            ApplicationWithFileSerializer,
            ApplicationWithSolutionSerializer,
        ],
        resource_type_field_name="polymorphic_ctype",
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

    def perform_create(self, serializer: ApplicationWithSolutionCreateSerializer):
        super().perform_create(serializer)
        if settings.BOT_TOKEN:
            send_file_application.delay(serializer.data)


class ApplicationWithSolutionView(CreateModelMixin, GenericViewSet):
    """Создание заявки с готовым решением."""

    serializer_class = ApplicationWithSolutionCreateSerializer
    http_method_names = ("post",)

    def perform_create(self, serializer: ApplicationWithSolutionCreateSerializer):
        super().perform_create(serializer)
        if settings.BOT_TOKEN:
            send_solution_application.delay(serializer.data)


class ApplicationWithCalcView(CreateModelMixin, GenericViewSet):
    """Создание заявки с калькулятором."""

    serializer_class = CalculatorJSONSerializer
    http_method_names = ("post",)

    def perform_create(self, serializer: CalculatorJSONSerializer):
        super().perform_create(serializer)
        if settings.BOT_TOKEN:
            send_calc_application.delay(serializer.data)

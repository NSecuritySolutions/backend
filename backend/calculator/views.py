from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from calculator.models import Calculator, PriceList
from calculator.serializers import CalculatorSerializer, PriceListSerializer


@extend_schema(tags=["Прайс лист"])
class PriceListView(ListModelMixin, GenericViewSet):
    """ViewSet для модели PriceList."""

    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    http_method_names = ("get",)


@extend_schema(tags=["Калькулятор"])
class CalculatorView(ListModelMixin, GenericViewSet):
    """Список калькуляторов."""

    queryset = Calculator.objects.all()
    serializer_class = CalculatorSerializer
    http_method_names = ("get",)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("active",)

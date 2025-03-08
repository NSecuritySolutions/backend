from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from calculator.models import Calculator
from calculator.serializers import CalculatorSerializer


@extend_schema(tags=["Калькулятор"])
class CalculatorView(ListModelMixin, GenericViewSet):
    """Список калькуляторов."""

    queryset = Calculator.objects.all()
    serializer_class = CalculatorSerializer
    http_method_names = ("get",)
    filterset_fields = ("active",)

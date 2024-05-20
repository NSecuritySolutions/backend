from rest_framework import viewsets
from .models import PriceList, Calculator
from .serializers import (
    PriceListSerializer,
    CalculatorSerializer
)
from drf_spectacular.utils import extend_schema


@extend_schema(exclude=True)
class PriceListView(viewsets.ModelViewSet):
    """ViewSet для модели PriceList."""
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    http_method_names = ("get", "post", "patch")


@extend_schema(tags=["Калькулятор"])
class CalculatorView(viewsets.ReadOnlyModelViewSet):
    """Список калькуляторов."""
    queryset = Calculator.objects.all()
    serializer_class = CalculatorSerializer

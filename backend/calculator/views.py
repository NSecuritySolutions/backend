from rest_framework import viewsets
from .models import PriceList, Calculator
from .serializers import (
    PriceListSerializer,
    CalculatorSerializer
)


class PriceListView(viewsets.ModelViewSet):
    """ViewSet для модели PriceList."""
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    http_method_names = ("get", "post", "patch")


class CalculatorView(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели PriceList."""
    queryset = Calculator.objects.all()
    serializer_class = CalculatorSerializer

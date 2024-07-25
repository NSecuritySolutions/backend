from rest_framework import viewsets
from .models import PriceList
from .serializers import (
    PriceListSerializer,
)


class PriceListView(viewsets.ModelViewSet):
    """ViewSet для модели PriceList."""
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    http_method_names = ("get", "post", "patch")

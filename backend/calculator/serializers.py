from rest_framework import serializers
from .models import PriceList


class PriceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList"""
    class Meta:
        model = PriceList
        fields = "__all__"
        exclude_fields = ('id',)

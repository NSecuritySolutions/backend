from rest_framework import serializers
from .models import Camera, CameraPrice, PriceList


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = [
            "time",
            "quality",
            "system_type",
            "external",
            "domestic",
            "total_price",
        ]


class CameraApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ["id", "name", "description", "email", "number"]


class CameraPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraPrice
        fields = "__all__"


class PriceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList"""
    class Meta:
        model = PriceList
        fields = "__all__"

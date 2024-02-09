from rest_framework import serializers
from .models import Camera, CameraPrice


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class CameraPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraPrice
        fields = '__all__'
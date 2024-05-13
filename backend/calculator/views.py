from rest_framework import generics, status
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CameraPrice, Camera
from .serializers import (
    CameraPriceSerializer,
    CameraSerializer,
    CameraApplicationSerializer,
)


class CameraView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request, *args, **kwargs):
        url = "http://localhost:8000/camera-pr/"

        # Выполнение GET-запроса к Django-серверу
        response = requests.get(url)

        # Initialize data variable
        data = None

        if response.status_code == 200:
            data = response.json()
        else:
            # Handle the case where the response status code is not 200
            return Response(
                {"error": "Failed to fetch pricing data"}, status=response.status_code
            )

        TIME_CHOICES = (
            ("7", data["seven"]),
            ("14", data["fourteen"]),
            ("30", data["thirty"]),
        )

        TYPE_SYSTEM_CHOICES = (("AHD", data["ahd"]), ("IP", data["ip"]))

        QUALITY_CHOICES = (
            ("HD", data["hd"]),
            ("FullHD", data["fullhd"]),
            ("2K-4K", data["two_k"]),
        )

        external_pr = data["external"]
        domestic_pr = data["domestic"]

        time = str(request.data.get("time"))
        quality = str(request.data.get("quality"))
        system_type = str(request.data.get("system_type"))
        domestic = int(request.data.get("domestic", 0))
        external = int(request.data.get("external", 0))

        # Find the corresponding price for the selected time, quality, and system type
        time_price = next((price for t, price in TIME_CHOICES if t == time), 0)
        quality_price = next((price for q, price in QUALITY_CHOICES if q == quality), 0)
        system_type_price = next(
            (price for st, price in TYPE_SYSTEM_CHOICES if st == system_type), 0
        )

        total_price = (
            time_price
            + quality_price
            + system_type_price
            + external * external_pr
            + domestic * domestic_pr
        )

        # Create a new instance of the Camera model and save it
        camera_instance = Camera(
            time=time,
            quality=quality,
            system_type=system_type,
            external=external,
            domestic=domestic,
            total_price=total_price,
        )
        camera_instance.save()

        response_data = {
            "time": time,
            "quality": quality,
            "system_type": system_type,
            "external": external,
            "domestic": domestic,
            "total_price": total_price,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CameraSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CameraPriceView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Assume there is only one CameraPrice instance in the database
            camera_price_instance = CameraPrice.objects.first()

            # Serialize the data
            serializer = CameraPriceSerializer(camera_price_instance)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CameraPrice.DoesNotExist:
            return Response(
                {"error": "CameraPrice instance not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

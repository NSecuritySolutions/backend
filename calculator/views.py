from rest_framework import generics, status
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer

class CameraView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request, *args, **kwargs):
        # Assume that the price per camera is 500
        TIME_CHOICES = (
            ('7', 100),
            ('14', 140),
            ('30', 250)
        )

        TYPE_SYSTEM_CHOICES = (
            ('AHD', 200),
            ('IP', 300)
        )

        QUALITY_CHOICES = (
            ('HD', 200),
            ('FullHD', 500),
            ('2K-4K', 1000)
        )

        external_pr = 3000
        domestic_pr = 1000

        time = str(request.data.get('time'))
        quality = str(request.data.get('quality'))
        system_type = str(request.data.get('system_type'))
        domestic = int(request.data.get('domestic', 0))
        external = int(request.data.get('external', 0))


        # Find the corresponding price for the selected time, quality, and system type
        time_price = next((price for t, price in TIME_CHOICES if t == time), 0)
        quality_price = next((price for q, price in QUALITY_CHOICES if q == quality), 0)
        system_type_price = next((price for st, price in TYPE_SYSTEM_CHOICES if st == system_type), 0)

        total_price = time_price + quality_price + system_type_price + external * external_pr + domestic * domestic_pr

        # Create a new instance of the Camera model and save it
        camera_instance = Camera(
            time=time,
            quality=quality,
            system_type=system_type,
            external=external,
            domestic=domestic,
            total_price=total_price
        )
        camera_instance.save()

        response_data = {
            'time': time,
            'quality': quality,
            'system_type': system_type,
            'external':external,
            'domestic':domestic,
            'total_price': total_price
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CameraSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

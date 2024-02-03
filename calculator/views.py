from rest_framework import generics
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer

class CameraView(generics.CreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request, *args, **kwargs):
        # Предположим, что цена за одну камеру составляет 500
        price_per_camera = 500
        test_pr = 100

        quantity = int(request.data.get('quantity', 1))
        test = int(request.data.get('test', 1))
        total_price = price_per_camera * quantity + test_pr * test

        response_data = {
            'quantity': quantity,
            'test': test,
            'total_price': total_price
        }
        return Response(response_data, status=201)
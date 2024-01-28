from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from .models import Product, PopularSolutions, OurService, OurWorks
from .serializers import ProductListSerializer, PopularSolutionsListSerializer, OurServiceListSerializer, \
OurWorksListSerializer

# Create your views here.

class OurServiceListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = OurService.objects.all()
        serializer = OurServiceListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OurWorksListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = OurWorks.objects.all()
        serializer = OurWorksListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PopularSolutionsListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = PopularSolutions.objects.all()
        serializer = PopularSolutionsListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    


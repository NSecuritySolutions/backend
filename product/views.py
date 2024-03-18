import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



from .models import Product, ReadySolutions, OurService, OurWorks, Category
from .serializers import ProductListSerializer, ReadySolutionsListSerializer, OurServiceListSerializer, \
OurWorksListSerializer, CategorySerializer


# Create your views here.

'''
    Вывод каталога
'''


class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

'''
    Вывод остальных функций
'''

class OurServiceListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = OurService.objects.all()
        serializer = OurServiceListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)

  
class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_data = []

        for category in categories:
            category_serializer = CategorySerializer(category, context={"request": request})
            products = Product.objects.filter(category=category)
            product_serializer = ProductListSerializer(products, many=True, context={"request": request})
            
            category_data.append({
                "category": category_serializer.data,
                "products": product_serializer.data
            })

        return Response(category_data, status=status.HTTP_200_OK)

class OurWorksListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = OurWorks.objects.all()
        serializer = OurWorksListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ReadySolutionsListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ReadySolutions.objects.all()
        serializer = ReadySolutionsListSerializer(queryset, many=True, context={"request":request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
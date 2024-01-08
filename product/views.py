from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, PopularSolutions
from .serializers import ProductListSerializer, CategoryListSerializer, PopularSolutionsListSerializer

# Create your views here.

class ProductListView(APIView):
    def get(self, request):
        # Получаем набор всех записей из таблицы Capital
        queryset = Product.objects.all()
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = ProductListSerializer(
            instance=queryset, # Передаём набор записей
            many=True # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data)
    
class CategoryListView(APIView):
    def get(self, request):
        # Получаем набор всех записей из таблицы Capital
        queryset = Category.objects.all()
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = CategoryListSerializer(
            instance=queryset, # Передаём набор записей
            many=True # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data)
    
class PopularSolutionsListView(APIView):
    def get(self, request):
        # Получаем набор всех записей из таблицы Capital
        queryset = PopularSolutions.objects.all()
        # Сериализуем извлечённый набор записей
        serializer_for_queryset = PopularSolutionsListSerializer(
            instance=queryset, # Передаём набор записей
            many=True # Указываем, что на вход подаётся именно набор записей
        )
        return Response(serializer_for_queryset.data)
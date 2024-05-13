from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import (
    Product,
    ReadySolutions,
    OurService,
    OurWorks,
    Category,
    Questions,
    Register,
)
from .serializers import (
    ProductListSerializer,
    ReadySolutionsListSerializer,
    OurServiceListSerializer,
    OurWorksListSerializer,
    CategorySerializer,
    QuestionsListSerializer,
    RegisterListSerializer,
)


class ProductListView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(
            queryset, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterListView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        queryset = Register.objects.all()
        serializer = RegisterListSerializer(
            queryset, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class OurServiceListView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        queryset = OurService.objects.all()
        serializer = OurServiceListSerializer(
            queryset, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_data = []

        # TODO Выглядит как костыль
        for category in categories:
            category_serializer = CategorySerializer(
                category
            )
            products = Product.objects.filter(category=category)
            product_serializer = ProductListSerializer(
                products, many=True
            )

            category_data.append(
                {
                    "category": category_serializer.data,
                    "products": product_serializer.data,
                }
            )

        return Response(category_data, status=status.HTTP_200_OK)


class OurWorksListView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        queryset = OurWorks.objects.all()
        serializer = OurWorksListSerializer(
            queryset, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReadySolutionsListView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        queryset = ReadySolutions.objects.all()
        serializer = ReadySolutionsListSerializer(
            queryset, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionsListView(APIView):
    # TODO docstring
    def get(self, request, *args, **kwargs):
        queryset = Questions.objects.all()
        serializer = QuestionsListSerializer(
            queryset, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

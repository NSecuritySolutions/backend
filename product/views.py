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
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Register.objects.all()
        serializer = RegisterListSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class OurServiceListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = OurService.objects.all()
        serializer = OurServiceListSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_data = []

        for category in categories:
            category_serializer = CategorySerializer(
                category, context={"request": request}
            )
            products = Product.objects.filter(category=category)
            product_serializer = ProductListSerializer(
                products, many=True, context={"request": request}
            )

            category_data.append(
                {
                    "category": category_serializer.data,
                    "products": product_serializer.data,
                }
            )

        return Response(category_data, status=status.HTTP_200_OK)


class OurWorksListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = OurWorks.objects.all()
        serializer = OurWorksListSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReadySolutionsListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ReadySolutions.objects.all()
        serializer = ReadySolutionsListSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionsListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Questions.objects.all()
        serializer = QuestionsListSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

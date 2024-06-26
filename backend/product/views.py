from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from product.models import (
    OurService,
    OurWorks,
    Product,
    ProductCategory,
    ReadySolution,
    Register,
)
from product.serializers import (
    CameraSerializer,
    CategorySerializer,
    OurServiceListSerializer,
    OurWorksListSerializer,
    ProductListSerializer,
    ReadySolutionsListSerializer,
    RegisterListSerializer,
)


@extend_schema(
    tags=["Товары"],
    responses=PolymorphicProxySerializer(
        component_name="Product",
        serializers=[CameraSerializer, RegisterListSerializer],
        resource_type_field_name="model",
    ),
)
class ProductListView(ListModelMixin, GenericViewSet):
    """Список товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


@extend_schema(exclude=True)
class RegisterListView(ListModelMixin, GenericViewSet):
    """Список регистраторов."""

    queryset = Register.objects.all()
    serializer_class = RegisterListSerializer


@extend_schema(tags=["Наши услуги"])
class OurServiceListView(ListModelMixin, GenericViewSet):
    """Список наших услуг."""

    queryset = OurService.objects.all()
    serializer_class = OurServiceListSerializer


@extend_schema(tags=["Категории"], exclude=True)
class CategoryView(APIView):
    """Список категорий с товарами."""

    # TODO docstring
    def get(self, request, *args, **kwargs):
        categories = ProductCategory.objects.all()
        category_data = []

        # TODO Выглядит как костыль
        for category in categories:
            category_serializer = CategorySerializer(category)
            products = Product.objects.filter(category=category)
            product_serializer = ProductListSerializer(products, many=True)

            category_data.append(
                {
                    "category": category_serializer.data,
                    "products": product_serializer.data,
                }
            )

        return Response(category_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Наши работы"])
class OurWorksListView(ListModelMixin, GenericViewSet):
    """Список наших работ."""

    queryset = OurWorks.objects.all()
    serializer_class = OurWorksListSerializer


@extend_schema(tags=["Готовые решения"])
class ReadySolutionsListView(ListModelMixin, GenericViewSet):
    """Список готовых решений."""

    queryset = ReadySolution.objects.all()
    serializer_class = ReadySolutionsListSerializer

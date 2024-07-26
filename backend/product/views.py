import requests
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from product.filters import ProductFilter
from product.models import (
    FACP,
    HDD,
    Camera,
    OurService,
    OurWorks,
    PACSProduct,
    Product,
    ProductCategory,
    ReadySolution,
    Register,
    Sensor,
)
from product.serializers import (
    CameraSerializer,
    CategorySerializer,
    FACPSerializer,
    HDDSerializer,
    OurServiceListSerializer,
    OurWorksListSerializer,
    PACSProductSerializer,
    ProductListSerializer,
    ReadySolutionsListSerializer,
    RegisterSerializer,
    SensorSerializer,
)


@extend_schema(
    tags=["Товары"],
    responses=PolymorphicProxySerializer(
        component_name="Product",
        serializers=[
            CameraSerializer,
            RegisterSerializer,
            HDDSerializer,
            FACPSerializer,
            SensorSerializer,
            PACSProductSerializer,
        ],
        resource_type_field_name="model",
    ),
)
class ProductListView(ListModelMixin, GenericViewSet):
    """Список товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


@extend_schema(exclude=True)
class RegisterListView(ListModelMixin, GenericViewSet):
    """Список регистраторов."""

    queryset = Register.objects.all()
    serializer_class = RegisterSerializer


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


@extend_schema(exclude=True)
@api_view(["GET"])
def api_view_test(request: Request) -> Response:
    instances = Product.objects.all()
    queryset: list[Camera | Register | HDD | FACP | Sensor | PACSProduct] = (
        instances.get_real_instances()
    )
    for instance in queryset:
        if instance.article is None:
            continue
        response = requests.get(
            f"https://b2b.pro-tek.pro/api/v1/product?filters[keyword]={instance.article}"
        )
        json = response.json()
        for item in json["items"]:
            if item["article"] == instance.article:
                instance.price = item["price"]["value"]
    instances.bulk_update(queryset, ["price"])
    return Response({"detail": "ok"})

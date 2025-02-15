from decimal import Decimal

import requests
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from product.filters import NewProductFilter, ProductFilter
from product.models import (
    FACP,
    HDD,
    Camera,
    NewProduct,
    OtherProduct,
    OurService,
    OurWorks,
    Product,
    ReadySolution,
    Register,
    Sensor,
    Tag,
)
from product.serializers import (
    CameraRetrieveSerializer,
    FACPRetrieveSerializer,
    HDDRetrieveSerializer,
    NewProductSerializer,
    OtherProductRetrieveSerializer,
    OurServiceListSerializer,
    OurWorksListSerializer,
    ProductRetrieveSerializer,
    ReadySolutionsSerializer,
    RegisterRetrieveSerializer,
    RegisterSerializer,
    SensorRetrieveSerializer,
    TagSerializer,
)


@extend_schema(
    tags=["Товары"],
    responses=PolymorphicProxySerializer(
        component_name="Single product",
        serializers=[
            CameraRetrieveSerializer,
            RegisterRetrieveSerializer,
            FACPRetrieveSerializer,
            SensorRetrieveSerializer,
            OtherProductRetrieveSerializer,
            HDDRetrieveSerializer,
        ],
        resource_type_field_name="polymorphic_ctype",
    ),
)
class ProductListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список товаров."""

    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    http_method_names = ("get",)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ("pk", "created_at", "updated_at")


@extend_schema(exclude=True)
class RegisterListView(ListModelMixin, GenericViewSet):
    """Список регистраторов."""

    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ("get",)
    ordering_fields = ("pk", "created_at", "updated_at")


@extend_schema(tags=["Наши услуги"])
class OurServiceListView(ListModelMixin, GenericViewSet):
    """Список наших услуг."""

    queryset = OurService.objects.all()
    serializer_class = OurServiceListSerializer
    http_method_names = ("get",)
    ordering_fields = ("pk", "created_at", "updated_at")


@extend_schema(tags=["Наши работы"])
class OurWorksListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список наших работ или объект по id."""

    queryset = OurWorks.objects.all()
    serializer_class = OurWorksListSerializer
    http_method_names = ("get",)
    ordering_fields = ("pk", "created_at", "updated_at")


@extend_schema(tags=["Готовые решения"])
class ReadySolutionsListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список готовых решений или объект по id."""

    queryset = ReadySolution.objects.annotate(
        equipment_price=Coalesce(
            Sum(F("equipment__product__price") * F("equipment__amount")), Decimal("0")
        )
    ).all()
    serializer_class = ReadySolutionsSerializer
    http_method_names = ("get",)
    ordering_fields = ("pk", "created_at", "updated_at")


@extend_schema(tags=["Тэги"])
class TagListView(ListModelMixin, GenericViewSet):
    """Список тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ("get",)
    ordering_fields = ("pk", "created_at", "updated_at")


@extend_schema(exclude=True)
@api_view(("GET",))
def api_view_test(request: Request) -> Response:
    instances = Product.objects.all()
    queryset: list[Camera | Register | FACP | Sensor | OtherProduct | HDD] = (
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


@extend_schema(tags=["Товары"])
class NewProductListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список товаров."""

    queryset = NewProduct.objects.all()
    serializer_class = NewProductSerializer
    http_method_names = ("get",)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NewProductFilter
    ordering_fields = ("pk", "created_at", "updated_at", "model")

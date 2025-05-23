from decimal import Decimal

from celery.result import AsyncResult
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from product.celery_tasks import update_prices
from product.filters import NewProductFilter
from product.models import (
    NewProduct,
    OurService,
    OurWorks,
    ProductCategory,
    ReadySolution,
    Tag,
)
from product.serializers import (
    CategoryListSerializer,
    NewProductSerializer,
    OurServiceListSerializer,
    OurWorksListSerializer,
    ReadySolutionsSerializer,
    TagSerializer,
)


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


@extend_schema(tags=["Товары"])
class NewProductListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список товаров."""

    queryset = NewProduct.objects.all()
    serializer_class = NewProductSerializer
    http_method_names = ("get",)
    filterset_class = NewProductFilter
    ordering_fields = (
        "pk",
        "created_at",
        "updated_at",
        "model",
        "product_type",
        "category",
    )


@extend_schema(tags=["Категории"])
class ProductCategoryListView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Список категорий продукции."""

    queryset = ProductCategory.objects.all()
    serializer_class = CategoryListSerializer
    http_method_names = ("get",)
    ordering_fields = ("pk", "created_at", "updated_at", "title")
    filterset_fields = ("parent__title", "title")


@extend_schema(exclude=True)
@api_view(("GET",))
def api_view_test(request: Request) -> Response:
    task = update_prices.delay()
    return Response({"detail": "ok", "task_id": task.id})


@extend_schema(exclude=True)
@api_view(("GET",))
def check_task_status(request: Request, task_id: str) -> Response:
    task_result = AsyncResult(task_id)
    return Response({"task_id": task_id, "status": task_result.status})

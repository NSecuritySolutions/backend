from django.db.models import QuerySet
from django_filters import AllValuesMultipleFilter, FilterSet, ModelMultipleChoiceFilter
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from product.models import NewProduct, ProductCategory


class NewProductFilter(FilterSet):
    manufacturer = AllValuesMultipleFilter(field_name="manufacturer__title")
    product_type = AllValuesMultipleFilter(field_name="product_type__name")
    category = ModelMultipleChoiceFilter(
        to_field_name="title",
        queryset=ProductCategory.objects.all(),
        method="filter_by_category",
    )

    class Meta:
        model = NewProduct
        fields = []

    @extend_schema_field(serializers.CharField())
    def filter_by_category(self, queryset: QuerySet[NewProduct], name, value):
        categories = set()
        for category in value:
            categories.update(category.get_descendants(include_self=True))

        if categories:
            return queryset.filter(category__in=categories)
        return queryset
